from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
    ledger_pairs,
    path_exists,
    read_csv_rows,
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
from foundation.control_plane.tier_context_materialization import (  # noqa: E402
    TIER_B_CORE_FEATURE_ORDER,
    build_tier_b_partial_context_frames,
)
from foundation.features.independent_alpha_campaign import (  # noqa: E402
    IndependentCandidateSpec,
    IndependentStageTopic,
    STAGE_TOPICS,
    apply_candidate_to_table,
    build_broad_candidate_grid,
    build_stage_model_context,
    summarize_candidate_frames,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import reopen_optimization_batch as reopen  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50AW"
PARENT_RUN_ID = "run50AW_stage56_independent_event_source_route_v1"
PACKET_ID = "stage56_run50AW_independent_event_source_route_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__IndependentEventSourceRoute"
BOUNDARY = "research_baseline_selection_only_no_operating_claim"
JUDGMENT = "in_progress_no_selected_research_baseline"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
REPORT_PATH = REVIEWS_ROOT / "run50AW_independent_event_source_route.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AW_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AW_audit.csv"
SOURCE_SUMMARY_CSV_PATH = REVIEWS_ROOT / "run50AW_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")

MODEL_INPUT_ROOT = Path("data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58")
MODEL_INPUT_DATASET_PATH = MODEL_INPUT_ROOT / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER_PATH = MODEL_INPUT_ROOT / "model_input_feature_order.txt"
MODEL_INPUT_SUMMARY_PATH = MODEL_INPUT_ROOT / "model_input_summary.json"
TRAINING_SUMMARY_PATH = Path("data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json")
RAW_MT5_ROOT = Path("data/raw/mt5_bars/m5")

VALIDATION_DAYS = 273.0
OOS_DAYS = 195.0
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_independent_event_source_route"
ARTIFACT_COLUMNS = ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes")


@dataclass(frozen=True)
class SourceVariant:
    variant_id: str
    source_stage_number: int
    source_candidate_id: str
    group: str
    max_hold_bars: int = 4
    reentry_cooldown_bars: int = 6
    routed_fallback_enabled: bool = True
    notes: str = ""


DEFAULT_VARIANTS: tuple[SourceVariant, ...] = (
    SourceVariant(
        variant_id="s43c02_h4c6",
        source_stage_number=43,
        source_candidate_id="c02_top8_stability_ranked_elasticnet",
        group="stage43_low_complexity_best_validation",
        notes="Stage43 top-8 low-complexity source; prior packet had strongest validation net/PF.",
    ),
    SourceVariant(
        variant_id="s43c08_h4c6",
        source_stage_number=43,
        source_candidate_id="c08_constrained_tree_stump_combo",
        group="stage43_low_complexity_best_oos",
        notes="Stage43 constrained-tree source; prior packet had strongest OOS net/PF.",
    ),
    SourceVariant(
        variant_id="s45c04_h4c6",
        source_stage_number=45,
        source_candidate_id="c04_histvol_ratio_expansion",
        group="stage45_volatility_expansion_density",
        notes="Stage45 realized-vol expansion source; tests broader volatility-event density.",
    ),
    SourceVariant(
        variant_id="s45c06_h4c6",
        source_stage_number=45,
        source_candidate_id="c06_direction_specific_expansion_breakout",
        group="stage45_directional_expansion_best_oos",
        notes="Stage45 directional expansion source; prior packet had strongest OOS net/PF.",
    ),
    SourceVariant(
        variant_id="s47c03_h4c6",
        source_stage_number=47,
        source_candidate_id="c03_majority_agreement",
        group="stage47_meta_majority_best_validation",
        notes="Stage47 majority agreement source; prior packet had strongest validation net/PF.",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_name(value: str, limit: int = 96) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def load_feature_order(path: Path = MODEL_INPUT_FEATURE_ORDER_PATH) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_label_threshold() -> float:
    payload = read_json(TRAINING_SUMMARY_PATH)
    threshold = float(payload["threshold_log_return"])
    if not math.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"invalid label threshold: {threshold}")
    return threshold


def load_model_input() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT_DATASET_PATH))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["timestamp_utc"] = frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    frame["validation_oos_split_label"] = (
        frame["split"].astype(str).map({"validation": "validation_is"}).fillna(frame["split"].astype(str))
    )
    return frame.sort_values("timestamp").reset_index(drop=True)


def build_common_table() -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    tier_a_raw = load_model_input()
    feature_order = load_feature_order()
    tier_b_payload = build_tier_b_partial_context_frames(
        raw_root=RAW_MT5_ROOT,
        tier_a_frame=tier_a_raw,
        tier_a_feature_order=feature_order,
        tier_b_feature_order=TIER_B_CORE_FEATURE_ORDER,
        label_threshold=load_label_threshold(),
    )
    tier_a = tier_a_raw.copy()
    tier_a["tier_label"] = mt5.TIER_A
    tier_a["routing_source"] = "tier_a_primary"
    tier_a["partial_context_subtype"] = "Tier_A_full_context"
    tier_a["tier_a_available"] = True
    tier_a["tier_b_fallback_available"] = False

    tier_b = tier_b_payload["tier_b_fallback_frame"].copy()
    tier_b["timestamp"] = pd.to_datetime(tier_b["timestamp"], utc=True)
    tier_b["timestamp_utc"] = tier_b["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    tier_b["validation_oos_split_label"] = (
        tier_b["split"].astype(str).map({"validation": "validation_is"}).fillna(tier_b["split"].astype(str))
    )
    tier_b["tier_label"] = mt5.TIER_B
    tier_b["routing_source"] = "tier_b_fallback"
    tier_b["tier_a_available"] = False
    tier_b["tier_b_fallback_available"] = True

    common_columns = [column for column in tier_a.columns if column in tier_b.columns]
    for column in (
        "timestamp",
        "timestamp_utc",
        "split",
        "validation_oos_split_label",
        "symbol",
        "label_class",
        "tier_label",
        "routing_source",
        "partial_context_subtype",
        "tier_a_available",
        "tier_b_fallback_available",
    ):
        if column not in common_columns and (column in tier_a.columns or column in tier_b.columns):
            common_columns.append(column)
    common = pd.concat(
        [tier_a.reindex(columns=common_columns), tier_b.reindex(columns=common_columns)],
        ignore_index=True,
        sort=False,
    )
    common = common.sort_values(["timestamp", "tier_label"]).reset_index(drop=True)
    common["stage56_event_source_row_id"] = range(len(common))
    route_coverage = route_coverage_from_common(common, tier_b_payload.get("summary", {}).get("no_tier_by_split", {}))
    lineage = source_lineage_entries()
    return common, route_coverage, lineage


def route_coverage_from_common(common: pd.DataFrame, no_tier_by_split: Mapping[str, Any] | None = None) -> dict[str, Any]:
    no_tier_by_split = no_tier_by_split or {}
    by_split: dict[str, dict[str, int]] = {}
    subtype: dict[str, dict[str, int]] = {}
    for split in ("validation", "oos"):
        view = common.loc[common["split"].astype(str).eq(split)]
        tier_a_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_A).sum())
        tier_b_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_B).sum())
        by_split[split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "no_tier_labelable_rows": int(no_tier_by_split.get(split, 0) or 0),
        }
        subtype[split] = (
            view.loc[view["tier_label"].astype(str).eq(mt5.TIER_B), "partial_context_subtype"]
            .astype(str)
            .value_counts()
            .to_dict()
        )
    return {
        "by_split": by_split,
        "tier_b_fallback_by_split_subtype": subtype,
        "no_tier_by_split": {str(key): int(value) for key, value in no_tier_by_split.items()},
    }


def source_lineage_entries() -> list[dict[str, Any]]:
    rows = []
    for role, path, kind, surface in (
        ("tier_a_model_input", MODEL_INPUT_DATASET_PATH, "input", "Tier A model input and label split"),
        ("tier_a_feature_order", MODEL_INPUT_FEATURE_ORDER_PATH, "input", "Tier A feature order"),
        ("model_input_summary", MODEL_INPUT_SUMMARY_PATH, "input", "model input diagnostics"),
        ("training_summary", TRAINING_SUMMARY_PATH, "input", "label threshold"),
        ("raw_mt5_bars", RAW_MT5_ROOT, "input", "Tier B fallback materialization"),
        ("mt5_runtime_ea", Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"), "MT5 handoff", "runtime entry"),
        ("source_stage43_packet", Path("stages/43_model_rebuild__low_complexity_feature_subset_regularized_signal/03_reviews/RUN37A~1.MD"), "prior_evidence", "source clue only"),
        ("source_stage45_packet", Path("stages/45_volatility_mechanism__compression_expansion_signal_rebuild/03_reviews/RUN39A~1.MD"), "prior_evidence", "source clue only"),
        ("source_stage47_packet", Path("stages/47_meta_signal__cross_model_agreement_disagreement_scout/03_reviews/RUN41A~1.MD"), "prior_evidence", "source clue only"),
    ):
        resolved = path if path.is_absolute() else REPO_ROOT / path
        rows.append(
            {
                "role": role,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(resolved) if resolved.is_file() else "directory_or_not_feasible",
                "artifact_kind": kind,
                "affects": surface,
                "required_for_reproducibility": kind != "prior_evidence",
            }
        )
    return rows


def topic_for_variant(variant: SourceVariant) -> IndependentStageTopic:
    return STAGE_TOPICS[variant.source_stage_number]


def spec_for_variant(variant: SourceVariant) -> IndependentCandidateSpec:
    topic = topic_for_variant(variant)
    specs = {spec.candidate_id: spec for spec in build_broad_candidate_grid(topic)}
    if variant.source_candidate_id not in specs:
        raise KeyError(f"unknown candidate {variant.source_candidate_id} for stage {variant.source_stage_number}")
    return specs[variant.source_candidate_id]


def selected_variants(args: argparse.Namespace) -> list[SourceVariant]:
    variants = list(DEFAULT_VARIANTS)
    if args.variant_id:
        wanted = set(args.variant_id)
        variants = [variant for variant in variants if variant.variant_id in wanted]
    if args.groups:
        groups = set(args.groups)
        variants = [variant for variant in variants if variant.group in groups]
    if args.max_variants is not None:
        variants = variants[: int(args.max_variants)]
    if not variants:
        raise RuntimeError("no variants selected")
    return variants


def export_signal_score_tables(topics: Sequence[IndependentStageTopic]) -> dict[int, dict[str, Any]]:
    payloads = {}
    for topic in topics:
        path = RUN_ROOT / "models" / f"stage{topic.stage_number}_{topic.signal_column}_discrete_signal_score_table.csv"
        payloads[topic.stage_number] = export_single_discrete_signal_score_table(
            path,
            feature_order=(topic.signal_column,),
            logit_strength=4.0,
            format_name="stage56_independent_event_source_single_signal_ebm_table_csv_v1",
        )
    return payloads


def export_feature_matrix(path: Path, frame: pd.DataFrame, signal_column: str) -> dict[str, Any]:
    payload = mt5.export_mt5_feature_matrix_csv(
        frame,
        (signal_column,),
        path,
        metadata_columns=(
            "variant_id",
            "source_stage_number",
            "source_candidate_id",
            "candidate_label",
            "mechanism_family",
            "rule_code",
            "tier_label",
            "routing_source",
            "partial_context_subtype",
            "entry_decision",
        ),
    )
    payload["path"] = rel(Path(payload["path"]))
    return payload


def build_variant_frames(
    variants: Sequence[SourceVariant],
    common: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, Any]], dict[int, dict[str, Any]]]:
    context_by_stage: dict[int, dict[str, Any]] = {}
    frames: dict[str, pd.DataFrame] = {}
    python_summary_rows: list[dict[str, Any]] = []
    for variant in variants:
        topic = topic_for_variant(variant)
        context = context_by_stage.setdefault(topic.stage_number, build_stage_model_context(common, topic))
        spec = spec_for_variant(variant)
        frame = apply_candidate_to_table(common, topic, spec, context)
        frame["variant_id"] = variant.variant_id
        frame["source_stage_number"] = variant.source_stage_number
        frame["source_candidate_id"] = variant.source_candidate_id
        frames[variant.variant_id] = frame
        summary = summarize_candidate_frames(topic, {variant.source_candidate_id: frame}, [spec])
        for row in summary:
            python_summary_rows.append(
                {
                    **dict(row),
                    "variant_id": variant.variant_id,
                    "source_stage_number": variant.source_stage_number,
                    "source_candidate_id": variant.source_candidate_id,
                    "max_hold_bars": variant.max_hold_bars,
                    "reentry_cooldown_bars": variant.reentry_cooldown_bars,
                    "group": variant.group,
                }
            )
    context_manifest = {stage: model_context_manifest(context) for stage, context in context_by_stage.items()}
    return frames, python_summary_rows, context_manifest


def model_context_manifest(context: Mapping[str, Any]) -> dict[str, Any]:
    payload = dict(context)
    sources = dict(payload.pop("source_signals", {}) or {})
    source_names = list(sources.get("source_names", []))
    source_summary: dict[str, Any] = {"source_names": source_names}
    for name in source_names:
        series = pd.Series(sources.get(name, []))
        numeric = pd.to_numeric(series, errors="coerce").fillna(0).astype("int8")
        source_summary[name] = {
            "rows": int(len(numeric)),
            "long": int(numeric.eq(1).sum()),
            "short": int(numeric.eq(-1).sum()),
            "flat": int(numeric.eq(0).sum()),
        }
    payload["source_signals"] = source_summary
    return payload


def export_candidate_feature_matrices(
    variants: Sequence[SourceVariant],
    frames: Mapping[str, pd.DataFrame],
) -> dict[str, dict[str, Any]]:
    exports: dict[str, dict[str, Any]] = {}
    for variant in variants:
        topic = topic_for_variant(variant)
        frame = frames[variant.variant_id]
        for source_split, runtime_split, split_token in (("validation", "validation_is", "val"), ("oos", "oos", "oos")):
            split_frame = frame.loc[frame["split"].astype(str).eq(source_split)]
            for tier_value, tier_name, tier_token in (
                (mt5.TIER_A, "tier_a", "a"),
                (mt5.TIER_B, "tier_b_fallback", "b"),
            ):
                tier_frame = split_frame.loc[split_frame["tier_label"].astype(str).eq(tier_value)].copy()
                out_path = RUN_ROOT / variant.variant_id / "features" / f"{variant.variant_id}_{tier_token}_{split_token}.csv"
                exports[f"{variant.variant_id}_{tier_name}_{runtime_split}"] = export_feature_matrix(
                    out_path,
                    tier_frame,
                    topic.signal_column,
                )
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
    model_artifacts: Mapping[int, Mapping[str, Any]],
    common_files_root: Path,
) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for topic_stage, payload in model_artifacts.items():
        local_path = resolve_artifact_path(payload["path"])
        copied.append(copy_to_common(local_path, f"{COMMON_ROOT}/models/s{topic_stage}_{local_path.name}", common_files_root))
    for payload in feature_exports.values():
        local_path = resolve_artifact_path(payload["path"])
        copied.append(copy_to_common(local_path, f"{COMMON_ROOT}/features/{local_path.name}", common_files_root))
    return copied


def build_attempts(
    variants: Sequence[SourceVariant],
    common: pd.DataFrame,
    feature_exports: Mapping[str, Mapping[str, Any]],
    model_artifacts: Mapping[int, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant in variants:
        topic = topic_for_variant(variant)
        model_name = Path(str(model_artifacts[topic.stage_number]["path"])).name
        model_common = f"{COMMON_ROOT}/models/s{topic.stage_number}_{model_name}"
        feature_hash = ordered_hash((topic.signal_column,))
        extra_set_values = {
            "InpReentryCooldownBars": int(variant.reentry_cooldown_bars),
            "InpEntryTransitionOnly": False,
            "InpEntryTransitionRearmMinConfidenceDelta": 0.0,
            "InpAtrSltpEnabled": False,
            "InpAtrPeriod": 14,
            "InpAtrStopMultiplier": 0.0,
            "InpAtrTakeProfitMultiplier": 0.0,
        }
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_frame = common.loc[
                common["split"].astype(str).eq(source_split)
                & common["tier_label"].astype(str).eq(mt5.TIER_A)
            ]
            from_date, to_date = split_dates_from_frame(split_frame, source_split)
            tier_a_matrix = Path(str(feature_exports[f"{variant.variant_id}_tier_a_{runtime_split}"]["path"])).name
            tier_b_matrix = Path(str(feature_exports[f"{variant.variant_id}_tier_b_fallback_{runtime_split}"]["path"])).name
            base_kwargs = {
                "run_root": RUN_ROOT / variant.variant_id,
                "run_id": f"{PARENT_RUN_ID}_{variant.variant_id}",
                "stage_number": 56,
                "exploration_label": EXPLORATION_LABEL,
                "split": runtime_split,
                "model_path": model_common,
                "model_id": f"{PARENT_RUN_ID}_{variant.variant_id}_signal_table",
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
                "extra_set_values": extra_set_values,
            }
            attempts.append(
                {
                    **attempt_payload(
                        **base_kwargs,
                        attempt_name=f"{variant.variant_id}_tier_a_only_{runtime_split}",
                        tier=mt5.TIER_A,
                        feature_path=f"{COMMON_ROOT}/features/{tier_a_matrix}",
                        primary_active_tier="tier_a",
                        attempt_role="tier_only_total",
                        record_view_prefix=f"mt5_tier_a_only_{variant.variant_id}",
                    ),
                    "variant_id": variant.variant_id,
                    "source_stage_number": variant.source_stage_number,
                    "source_candidate_id": variant.source_candidate_id,
                }
            )
            attempts.append(
                {
                    **attempt_payload(
                        **base_kwargs,
                        attempt_name=f"{variant.variant_id}_tier_b_fallback_only_{runtime_split}",
                        tier=mt5.TIER_B,
                        feature_path=f"{COMMON_ROOT}/features/{tier_b_matrix}",
                        primary_active_tier="tier_b_fallback",
                        attempt_role="tier_b_fallback_only_total",
                        record_view_prefix=f"mt5_tier_b_fallback_only_{variant.variant_id}",
                    ),
                    "variant_id": variant.variant_id,
                    "source_stage_number": variant.source_stage_number,
                    "source_candidate_id": variant.source_candidate_id,
                }
            )
            attempts.append(
                {
                    **attempt_payload(
                        **base_kwargs,
                        attempt_name=f"{variant.variant_id}_routed_{runtime_split}",
                        tier=mt5.TIER_AB,
                        feature_path=f"{COMMON_ROOT}/features/{tier_a_matrix}",
                        primary_active_tier="tier_a",
                        attempt_role="routed_total",
                        record_view_prefix=f"mt5_routed_{variant.variant_id}",
                        fallback_enabled=variant.routed_fallback_enabled,
                        fallback_model_path=model_common,
                        fallback_model_id=f"{PARENT_RUN_ID}_{variant.variant_id}_tier_b_signal_table",
                        fallback_model_backend="ebm_table",
                        fallback_feature_path=f"{COMMON_ROOT}/features/{tier_b_matrix}",
                        fallback_feature_count=1,
                        fallback_feature_order_hash=feature_hash,
                        fallback_short_threshold=SHORT_THRESHOLD,
                        fallback_long_threshold=LONG_THRESHOLD,
                        fallback_min_margin=MIN_MARGIN,
                        fallback_invert_signal=False,
                    ),
                    "variant_id": variant.variant_id,
                    "source_stage_number": variant.source_stage_number,
                    "source_candidate_id": variant.source_candidate_id,
                }
            )
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


def mt5_metric(record: Mapping[str, Any], *names: str) -> Any:
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    report = record.get("report", {}) if isinstance(record.get("report"), Mapping) else {}
    report_metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
    source_report = report.get("source_report", {}) if isinstance(report.get("source_report"), Mapping) else {}
    source_metrics = source_report.get("metrics", {}) if isinstance(source_report.get("metrics"), Mapping) else {}
    for name in names:
        if name in metrics:
            return metrics[name]
        if name in report_metrics:
            return report_metrics[name]
        if name in source_metrics:
            return source_metrics[name]
    return None


def as_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None or value == "":
            return default
        number = float(str(value).replace("%", ""))
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def report_path_from_record(record: Mapping[str, Any]) -> str:
    report = record.get("report", {}) if isinstance(record.get("report"), Mapping) else {}
    html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
    if html.get("path"):
        return str(html.get("path"))
    metrics_path = mt5_metric(record, "report_path")
    return "" if metrics_path is None else str(metrics_path)


def split_days(split: str) -> float:
    return VALIDATION_DAYS if split == "validation_is" else OOS_DAYS


def build_summary_rows(
    variants: Sequence[SourceVariant],
    kpi_records: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_record = {str(record.get("record_view")): record for record in kpi_records}
    audits = {
        (str(row.get("variant_id")), str(row.get("record_view"))): row
        for row in audit_rows
        if str(row.get("variant_id", "")).startswith("s")
    }
    rows: list[dict[str, Any]] = []
    for variant in variants:
        spec = spec_for_variant(variant)
        row: dict[str, Any] = {
            "variant_id": variant.variant_id,
            "source_stage_number": variant.source_stage_number,
            "source_candidate_id": variant.source_candidate_id,
            "source_candidate_label": spec.label,
            "group": variant.group,
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
                trade_count = as_float(mt5_metric(record, "trade_count", "total_trades"), 0.0)
                row[f"{view_name}_{split_prefix}_net"] = mt5_metric(record, "net_profit")
                row[f"{view_name}_{split_prefix}_pf"] = mt5_metric(record, "profit_factor")
                row[f"{view_name}_{split_prefix}_trades"] = mt5_metric(record, "trade_count", "total_trades")
                row[f"{view_name}_{split_prefix}_trades_per_day"] = None if trade_count is None else trade_count / split_days(split)
                row[f"{view_name}_{split_prefix}_max_dd"] = mt5_metric(record, "max_drawdown_amount", "max_drawdown")
                row[f"{view_name}_{split_prefix}_expectancy"] = mt5_metric(record, "expectancy")
                row[f"{view_name}_{split_prefix}_report_path"] = report_path_from_record(record)
            audit = audits.get((variant.variant_id, f"mt5_routed_{variant.variant_id}_{split}"), {})
            row[f"routed_{split_prefix}_cost_stressed_expectancy"] = audit.get("cost_stressed_expectancy")
            row[f"routed_{split_prefix}_mfe_capture_ratio"] = audit.get("mfe_capture_ratio")
            row[f"routed_{split_prefix}_same_move_reentry_ratio"] = audit.get("same_move_reentry_ratio")
            row[f"routed_{split_prefix}_trades_per_day_after_12bar_cooldown"] = audit.get("trades_per_day_after_cooldown")
            row[f"routed_{split_prefix}_density_gain_survives_12bar_cooldown"] = audit.get("density_gain_survives_12bar_cooldown")
        failed = failure_reasons(row)
        row["passed_stage56_research_baseline_gate"] = not failed
        row["failure_reasons"] = ";".join(failed)
        rows.append(row)
    rows.sort(
        key=lambda item: (
            bool(item.get("passed_stage56_research_baseline_gate")),
            as_float(item.get("routed_validation_pf"), 0.0) or 0.0,
            as_float(item.get("routed_oos_pf"), 0.0) or 0.0,
            as_float(item.get("routed_validation_net"), -999999.0) or -999999.0,
            as_float(item.get("routed_oos_net"), -999999.0) or -999999.0,
        ),
        reverse=True,
    )
    return rows


def failure_reasons(row: Mapping[str, Any]) -> list[str]:
    checks = (
        ("validation_density", as_float(row.get("routed_validation_trades_per_day"), 0.0) >= 5.0),
        ("oos_density", as_float(row.get("routed_oos_trades_per_day"), 0.0) >= 5.0),
        ("validation_net_positive", as_float(row.get("routed_validation_net"), 0.0) > 0.0),
        ("oos_net_positive", as_float(row.get("routed_oos_net"), 0.0) > 0.0),
        ("validation_pf", as_float(row.get("routed_validation_pf"), 0.0) >= 1.10),
        ("oos_pf", as_float(row.get("routed_oos_pf"), 0.0) >= 1.10),
        (
            "cost_stressed_expectancy",
            as_float(row.get("routed_validation_cost_stressed_expectancy"), -999.0) > 0.0
            and as_float(row.get("routed_oos_cost_stressed_expectancy"), -999.0) > 0.0,
        ),
        (
            "same_move_density",
            str(row.get("routed_validation_density_gain_survives_12bar_cooldown")).lower() == "true"
            and str(row.get("routed_oos_density_gain_survives_12bar_cooldown")).lower() == "true"
            and as_float(row.get("routed_validation_same_move_reentry_ratio"), 1.0) <= 0.35
            and as_float(row.get("routed_oos_same_move_reentry_ratio"), 1.0) <= 0.35,
        ),
    )
    return [name for name, passed in checks if not passed]


def audit_rows_for_result(result: Mapping[str, Any], variants: Sequence[SourceVariant], cost_stress_per_trade: float) -> list[dict[str, Any]]:
    market_data = MarketData.load(REPO_ROOT)
    reference_audits, reference_capture = reopen._reference_capture_by_split(market_data, cost_stress_per_trade)
    by_view = {str(record.get("record_view")): record for record in result.get("mt5_kpi_records", [])}
    rows: list[dict[str, Any]] = list(reference_audits)
    for variant in variants:
        variant_run_id = f"{PARENT_RUN_ID}_{variant.variant_id}"
        for split in ("validation_is", "oos"):
            record_view = f"mt5_routed_{variant.variant_id}_{split}"
            record = by_view.get(record_view, {})
            report_path = report_path_from_record(record)
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
                reopen._audit_report(
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


def artifact_rows(
    result: Mapping[str, Any],
    variants: Sequence[SourceVariant],
    source_lineage: Sequence[Mapping[str, Any]],
    extra_paths: Sequence[Path],
) -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []

    def add(artifact_id: str, artifact_type: str, path: Path | str, notes: str) -> None:
        p = Path(str(path))
        resolved = p if p.is_absolute() else REPO_ROOT / p
        sha = sha256_file_lf_normalized(resolved) if resolved.is_file() else "directory_or_not_feasible"
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
        add(f"stage56_{RUN_NUMBER}_{safe_name(path.stem, 80)}", path.suffix.lstrip(".") or "artifact", path, "Stage56 run50AW evidence artifact.")
    for item in source_lineage:
        path = str(item.get("path") or "")
        if path:
            add(
                f"stage56_{RUN_NUMBER}_lineage_{safe_name(str(item.get('role')), 60)}",
                str(item.get("artifact_kind") or "lineage"),
                path,
                str(item.get("affects") or "source lineage"),
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        if html.get("path"):
            add(
                f"stage56_{RUN_NUMBER}_mt5_report_{safe_name(str(report.get('attempt_name') or report.get('report_name')), 100)}",
                "mt5_html_report",
                str(html["path"]),
                "Actual MT5 Strategy Tester HTML report.",
            )
    for variant in variants:
        add(
            f"stage56_{RUN_NUMBER}_{variant.variant_id}_run_root",
            "run_root",
            RUN_ROOT / variant.variant_id,
            "Variant run directory; file hashes are recorded for durable child artifacts.",
        )
    return rows


def write_ledgers(result: Mapping[str, Any], variants: Sequence[SourceVariant], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    run_rows = [
        {
            "run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "stage56_independent_event_source_route",
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
                "notes": (
                    f"source_stage={variant.source_stage_number};source_candidate={variant.source_candidate_id};"
                    f"views=tier_a_only,tier_b_fallback_only,routed_total;boundary=runtime_probe_only"
                ),
            }
        )
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")

    ledger_rows: list[dict[str, Any]] = []
    for variant in variants:
        records = [
            record
            for record in result.get("mt5_kpi_records", [])
            if f"_{variant.variant_id}_" in str(record.get("record_view"))
        ]
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
            "record_view": "stage56_reopen_optimization_parent_review",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "stage56_selected_research_baseline_search",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if external == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": "selected_research_baseline=none",
            "guardrail_kpi": f"completed_variants={len(variants)};terminal_condition=not_satisfied;stage56_remains_open=1;no_operating_claim=1",
            "external_verification_status": external,
            "notes": "run50AW independent event source route branch; actual MT5 evidence only.",
        }
    )
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {
        "run_registry": run_payload,
        "stage_ledger": stage_payload,
        "project_alpha_ledger": project_payload,
        "artifact_registry": artifact_payload,
    }


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    if not rows:
        return None
    return max(
        rows,
        key=lambda row: (
            bool(row.get("passed_stage56_research_baseline_gate")),
            min(as_float(row.get("routed_validation_trades_per_day"), 0.0) or 0.0, as_float(row.get("routed_oos_trades_per_day"), 0.0) or 0.0),
            min(as_float(row.get("routed_validation_pf"), 0.0) or 0.0, as_float(row.get("routed_oos_pf"), 0.0) or 0.0),
            (as_float(row.get("routed_validation_net"), 0.0) or 0.0) + (as_float(row.get("routed_oos_net"), 0.0) or 0.0),
        ),
    )


def write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    best = best_row(rows) or {}
    lines = [
        "# Stage56 run50AW Independent Event Source Route(독립 이벤트 원천 라우트)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        f"- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Action(행동): Stage43/45/47 independent source(독립 원천)를 Stage56 actual MT5 routed path(실제 MT5 라우팅 경로)로 다시 실행했다.",
        "Effect(효과): 이전 source clue(원천 단서)가 현재 BaselineAdapter(기준선 어댑터) 밀도 병목을 풀 수 있는지 한 계정 경로(one tester account path, 단일 테스터 계정 경로)로 판정한다.",
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
        "| variant | source | val day | oos day | val PF | oos PF | val net | oos net | failures |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | s{stage}:{cand} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {fail} |".format(
                variant=row.get("variant_id", ""),
                stage=row.get("source_stage_number", ""),
                cand=row.get("source_candidate_id", ""),
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
            "## Audit Summary(감사 요약)",
            "",
            "| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in audit_rows:
        variant = str(row.get("variant_id") or "")
        if not variant.startswith("s"):
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
            "Effect(효과): run50AW(실행50AW)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다.",
        ]
    )
    write_md(REPORT_PATH, "\n".join(lines))


def fmt(value: Any) -> str:
    number = as_float(value)
    if number is None:
        return "" if value is None else str(value)
    return f"{number:.6f}" if abs(number) < 100 else f"{number:.2f}"


def update_current_truth(rows: Sequence[Mapping[str, Any]]) -> None:
    best = best_row(rows) or {}
    working = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- active stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) not_satisfied(미충족)

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50AW(실행50AW)는 independent event source route(독립 이벤트 원천 라우트)를 실제 MT5 validation/OOS(검증/표본외)로 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best.get('variant_id', 'none')}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`

## Current Bottleneck(현재 병목)

- run50AW judgment(실행50AW 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 사유) `{best.get('failure_reasons', '')}` 때문에 hard condition(강한 조건)을 닫지 않는다.
- next_hypothesis_branch(다음 가설 분기): `continue_independent_event_source_composite_or_new_source_branch`

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
"""
    write_md(CURRENT_WORKING_STATE_PATH, working)

    selection = f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `{PARENT_RUN_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `{best.get('variant_id', 'none')}`

## Latest Run50AW Intermediate Evidence(최신 50AW 중간 근거)

- packet(묶음): `{PACKET_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- summary_csv(요약 CSV): `{RESULTS_CSV_PATH.as_posix()}`
- audit_csv(감사 CSV): `{AUDIT_CSV_PATH.as_posix()}`
- aggregate_summary(합산 요약): `{AGGREGATE_SUMMARY_PATH.as_posix()}`

Best read(최선 판독) `{best.get('variant_id', 'none')}` validation/OOS(검증/표본외) trades/day(일 거래 수) `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`, PF(수익 팩터) `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`, net(순손익) `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`이다.

Failure(실패): `{best.get('failure_reasons', '')}`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
"""
    write_md(SELECTION_STATUS_PATH, selection)

    append_progress(best)
    update_workspace_state(best)


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(PROGRESS_LOG_PATH) else ""
    entry = f"""

## {utc_now()} run50AW Independent Event Source Route(독립 이벤트 원천 라우트)

- action(행동): Stage43/45/47 independent event source(독립 이벤트 원천)를 Stage56(56단계) actual MT5 validation/OOS(실제 MT5 검증/표본외)로 다시 실행했다.
- effect(효과): run50AV(실행50AV)에서 드러난 independent opportunity density(독립 기회 밀도) 병목을 새 source branch(원천 분기)로 압박했다.
- best_variant(현재 최선 변형): `{best.get('variant_id', 'none')}`
- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`{best.get('failure_reasons', '')}`.
"""
    write_md(PROGRESS_LOG_PATH, existing.rstrip() + entry)


def update_workspace_state(best: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {PARENT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        f"- Stage56(56단계) `{STAGE_ID}`: run50AW(실행50AW) independent event source route(독립 이벤트 원천 라우트) 완료; "
        f"best_variant(현재 최선 변형)는 `{best.get('variant_id', 'none')}`이고 validation/OOS(검증/표본외) "
        f"trades/day(일 거래 수) `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`, "
        f"PF(수익 팩터) `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`, "
        f"net(순손익) `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`이며 selected_research_baseline(선택 연구 기준선)은 `none`이다. "
        f"Effect(효과): independent source(독립 원천)는 `{best.get('failure_reasons', '')}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했고 Stage56(56단계)은 계속 열린다."
    )
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
    text = re.sub(r"latest_run50av_attribution_result:.*", r"latest_run50av_attribution_result: preserved_before_run50aw", text)
    if "run50aw_independent_event_source_result" not in text:
        text += (
            "\nstage56_run50aw_independent_event_source_route:\n"
            f"  packet_id: {PACKET_ID}\n"
            f"  current_run_id: {PARENT_RUN_ID}\n"
            f"  best_variant: {best.get('variant_id', 'none')}\n"
            f"  selected_research_baseline: none\n"
            f"  failure_reasons: {best.get('failure_reasons', '')}\n"
            "  boundary: research_baseline_selection_only_no_operating_claim\n"
            "  next_action: continue_independent_event_source_composite_or_new_source_branch\n"
        )
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8")


def write_run_files(
    result: Mapping[str, Any],
    variants: Sequence[SourceVariant],
    summary_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    python_summary_rows: Sequence[Mapping[str, Any]],
    source_lineage: Sequence[Mapping[str, Any]],
    context_manifest: Mapping[int, Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    write_csv(RESULTS_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows, reopen.AUDIT_COLUMNS)
    write_csv(SOURCE_SUMMARY_CSV_PATH, python_summary_rows)
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "variants": [variant.__dict__ for variant in variants],
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "compile": result.get("compile", {}),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
    })
    write_json(RUN_ROOT / "kpi_record.json", {
        "run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "execution_results": result.get("execution_results", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
    })
    write_json(RUN_ROOT / "source_context_manifest.json", context_manifest)
    write_json(RUN_ROOT / "source_lineage.json", list(source_lineage))
    write_json(AGGREGATE_SUMMARY_PATH, {
        "run_id": PARENT_RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "selected_research_baseline": "none",
        "stage56_remains_open": True,
        "terminal_condition": "not_satisfied",
        "best_variant": best_row(summary_rows),
        "summary_csv_path": RESULTS_CSV_PATH.as_posix(),
        "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
        "report_path": REPORT_PATH.as_posix(),
        "ledger_payload": ledger_payload,
        "artifact_hashes": {
            "summary_csv_sha256": sha256_file_lf_normalized(RESULTS_CSV_PATH) if path_exists(RESULTS_CSV_PATH) else None,
            "audit_csv_sha256": sha256_file_lf_normalized(AUDIT_CSV_PATH) if path_exists(AUDIT_CSV_PATH) else None,
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
    })


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 independent event source MT5 route branch.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--groups", action="append", default=[])
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
    common, route_coverage, lineage = build_common_table()
    frames, python_summary_rows, context_manifest = build_variant_frames(variants, common)
    topics = sorted({topic_for_variant(variant) for variant in variants}, key=lambda topic: topic.stage_number)
    model_artifacts = export_signal_score_tables(topics)
    feature_exports = export_candidate_feature_matrices(variants, frames)
    common_copies = copy_runtime_inputs(feature_exports, model_artifacts, Path(args.common_files_root))
    attempts = build_attempts(variants, common, feature_exports, model_artifacts)
    prepared = {
        "run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 56,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "feature_exports": feature_exports,
        "model_artifacts": model_artifacts,
        "common_copies": common_copies,
        "route_coverage": route_coverage,
        "source_lineage": lineage,
        "python_candidate_summary": python_summary_rows,
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage56_independent_event_source_single_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
    }
    result = execute_or_materialize(prepared, args)
    audit_rows = audit_rows_for_result(result, variants, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    summary_rows = build_summary_rows(variants, result.get("mt5_kpi_records", []), audit_rows)
    write_report(summary_rows, audit_rows, result)
    extra_paths = [
        REPORT_PATH,
        RESULTS_CSV_PATH,
        AUDIT_CSV_PATH,
        SOURCE_SUMMARY_CSV_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        RUN_ROOT / "source_context_manifest.json",
        RUN_ROOT / "source_lineage.json",
        AGGREGATE_SUMMARY_PATH,
    ]
    artifacts = artifact_rows(result, variants, lineage, extra_paths)
    ledger_payload = write_ledgers(result, variants, artifacts)
    write_run_files(
        result,
        variants,
        summary_rows,
        audit_rows,
        python_summary_rows,
        lineage,
        context_manifest,
        ledger_payload,
    )
    artifacts = artifact_rows(result, variants, lineage, extra_paths)
    ledger_payload = write_ledgers(result, variants, artifacts)
    write_json(AGGREGATE_SUMMARY_PATH, {**read_json(AGGREGATE_SUMMARY_PATH), "ledger_payload": ledger_payload})
    update_current_truth(summary_rows)
    print(json.dumps(json_ready({
        "status": "ok",
        "run_id": PARENT_RUN_ID,
        "selected_research_baseline": "none",
        "stage56_remains_open": True,
        "external_verification_status": result.get("external_verification_status"),
        "summary_csv": RESULTS_CSV_PATH.as_posix(),
        "audit_csv": AUDIT_CSV_PATH.as_posix(),
        "aggregate_summary": AGGREGATE_SUMMARY_PATH.as_posix(),
        "best_variant": best_row(summary_rows),
    }), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
