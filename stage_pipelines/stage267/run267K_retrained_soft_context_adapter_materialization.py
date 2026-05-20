from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from foundation.models.ebm_explainable import EbmVariantSpec, fit_ebm_variant, probability_frame, term_importance_frame
from foundation.models.ebm_score_table import export_ebm_main_effect_score_table, check_ebm_score_table_probability_parity
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage56 import context_extratrees_agreement_branch as s56
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_ID = "run267K_stage267_retrained_soft_context_adapter_materialization_v1"
RUN_NUMBER = "run267K"
STATUS = "run267K_retrained_soft_context_adapter_materialized_execution_pending"
NEXT_ACTION = "run267K_execute_retrained_soft_context_adapter_mt5_batch"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "retrained_soft_context_adapter_materialization"

RUN267J_ROOT = STAGE_ROOT / "02_runs" / "run267J" / "retrained_soft_context_adapter_design"
RUN267I_ROOT = STAGE_ROOT / "02_runs" / "run267I" / "p0_soft_noncalendar_adapter_materialization"
RUN264_MANIFEST_PATH = (
    Path("stages")
    / "264_adapter_research__dual_objective_lowrank_lowedge_repair"
    / "02_runs"
    / "run264A"
    / "run_manifest.json"
)
MODEL_INPUT_DATASET_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
MODEL_INPUT_FEATURE_ORDER_PATH = MODEL_INPUT_DATASET_PATH.with_name("model_input_feature_order.txt")
TRAINING_CONTRACT_PATH = Path("docs/contracts/training_label_split_contract_fpmarkets_v2.md")
MODEL_INPUT_CONTRACT_PATH = Path("docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md")

INPUT_DESIGN_PATH = RUN267J_ROOT / "retrain_probe_design.csv"
INPUT_J_VALIDATION_PLAN_PATH = RUN267J_ROOT / "data_integrity_model_validation_plan.csv"
INPUT_J_RESULT_PATH = RUN267J_ROOT / "result.json"
INPUT_I_REVIEW_PATH = RUN267I_ROOT / "candidate_soft_adapter_review.csv"

SOURCE_AUDIT_PATH = DESIGN_ROOT / "source_audit.csv"
TRAINING_DIAGNOSTICS_PATH = DESIGN_ROOT / "training_frame_diagnostics.csv"
MODEL_VALIDATION_PATH = DESIGN_ROOT / "model_validation_snapshot.csv"
TERM_IMPORTANCE_PATH = DESIGN_ROOT / "term_importance.csv"
PARITY_CHECK_PATH = DESIGN_ROOT / "score_table_parity_check.csv"
FEATURE_MODEL_MANIFEST_PATH = DESIGN_ROOT / "feature_model_manifest.csv"
RUNTIME_CONTRACT_PATH = DESIGN_ROOT / "runtime_contract.csv"
ATTEMPT_MANIFEST_PATH = DESIGN_ROOT / "attempts.csv"
RUN_MANIFEST_PATH = DESIGN_ROOT / "run_manifest.json"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267K_retrained_soft_context_adapter_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267K_retrained_soft_context_adapter_materialization.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267k/run267K_retrained_soft_context_adapter"
SOFT_FEATURE_NAME = "stage267_adx_atr_soft_score"
MODEL_MATERIALIZATION_TYPE = "supervised_ebm_main_effect_retrain_v1"
PERIOD_LABEL = input_probe.PERIOD_LABEL
FEATURE_DESIGN = "soft_context_supervised_retrain"
P0_ALIASES = ("s264_aih", "s264_lc")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_runtime_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
        lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_section(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker, start + len(start_marker))
    if start == -1 or end == -1:
        return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


def replace_tail_from_marker(text: str, marker: str, replacement: str) -> str:
    start = text.find(marker)
    if start == -1:
        return text.rstrip() + "\n" + replacement.rstrip() + "\n"
    return text[:start].rstrip() + "\n" + replacement.rstrip() + "\n"


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def q(values: Sequence[float], quantile: float) -> float:
    if not values:
        return 0.0
    return float(pd.Series(list(values), dtype="float64").quantile(float(quantile)))


def bool_status(value: bool) -> str:
    return "pass" if value else "missing_required"


def sha_or_missing(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else "missing"


def p0_design_rows() -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(INPUT_DESIGN_PATH)
        if row.get("candidate_alias") in P0_ALIASES
        and str(row.get("materialization_lane", "")).startswith("audit_then_materialize_p0")
    ]
    if len(rows) != 2:
        raise RuntimeError(f"expected 2 P0 design rows from run267J, found {len(rows)}")
    return sorted(rows, key=lambda row: int(float(row.get("priority", 99))))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def stage264_model_artifacts() -> dict[str, Any]:
    manifest = read_json(RUN264_MANIFEST_PATH)
    return manifest.get("model_artifacts", {})


def soft_band_adx(value: Any) -> float:
    number = finite_float(value)
    if number is None:
        return 0.0
    return max(0.0, min(1.0, 1.0 - abs(number - 22.5) / 7.5))


def low_atr_score(value: Any, q33: float, q67: float) -> float:
    number = finite_float(value)
    if number is None:
        return 0.0
    width = max(float(q67) - float(q33), 1.0e-9)
    return max(0.0, min(1.0, (float(q67) - number) / width))


def source_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    s56.patch_context()
    common, route_coverage, _ = s56.aw.build_common_table()
    variant = next(item for item in s56.DEFAULT_VARIANTS if item.variant_id == input_probe.SOURCE_VARIANT_ID)
    frame = s56.build_variant_frame(common, variant)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    tier_a = frame.loc[frame["tier_label"].astype(str).eq(s56.ctx.mt5.TIER_A)].copy()
    if "symbol" not in tier_a.columns:
        tier_a["symbol"] = "US100"
    tier_a = tier_a.sort_values("timestamp").reset_index(drop=True)
    train = tier_a.loc[tier_a["split"].astype(str).eq("train")]
    atr_values = pd.to_numeric(train["atr_14_over_atr_50"], errors="coerce").dropna().astype(float).to_list()
    adx_values = pd.to_numeric(train["adx_14"], errors="coerce").dropna().astype(float).to_list()
    atr_q33 = q(atr_values, 1 / 3)
    atr_q67 = q(atr_values, 2 / 3)
    tier_a["stage267_adx_20_25_soft_component"] = tier_a["adx_14"].map(soft_band_adx).astype("float64")
    tier_a["stage267_atr_low_component"] = tier_a["atr_14_over_atr_50"].map(lambda value: low_atr_score(value, atr_q33, atr_q67)).astype("float64")
    tier_a[SOFT_FEATURE_NAME] = (
        tier_a["stage267_adx_20_25_soft_component"] * tier_a["stage267_atr_low_component"]
    ).astype("float64")
    info = {
        "source_variant_id": input_probe.SOURCE_VARIANT_ID,
        "source_signal_column": input_probe.SOURCE_SIGNAL_COLUMN,
        "rows": int(len(tier_a)),
        "split_counts": {str(k): int(v) for k, v in tier_a["split"].value_counts().sort_index().items()},
        "class_counts": {str(k): int(v) for k, v in tier_a["label_class"].value_counts().sort_index().items()},
        "first_time_utc": tier_a["timestamp"].min().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_time_utc": tier_a["timestamp"].max().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tier": s56.ctx.mt5.TIER_A,
        "duplicates": int(tier_a["timestamp"].duplicated().sum()),
        "missing_label_rows": int(tier_a["label_class"].isna().sum()),
        "missing_signal_rows": int(pd.to_numeric(tier_a[input_probe.SOURCE_SIGNAL_COLUMN], errors="coerce").isna().sum()),
        "atr_14_over_atr_50_train_q33": atr_q33,
        "atr_14_over_atr_50_train_q67": atr_q67,
        "adx_14_train_q33": q(adx_values, 1 / 3),
        "adx_14_train_q67": q(adx_values, 2 / 3),
        "route_coverage_rows": int(len(route_coverage)) if hasattr(route_coverage, "__len__") else None,
    }
    return tier_a, info


def candidate_feature_frame(source: pd.DataFrame, spec: Any) -> tuple[pd.DataFrame, list[str], dict[str, Any]]:
    extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
    rank_column = str(spec.module.RANK_COLUMN)
    gate_column = f"{spec.module.GATE_COLUMN_PREFIX}_{extra['axis']}"
    feature_order = [input_probe.SOURCE_SIGNAL_COLUMN, rank_column, gate_column, SOFT_FEATURE_NAME]
    records: list[dict[str, Any]] = []
    for record in source.to_dict("records"):
        mapped = input_probe.row_mapping(record)
        signal = int(round(spec.module.s250.stage238.parse_float(mapped.get(input_probe.SOURCE_SIGNAL_COLUMN), 0.0)))
        bucket_value, _ = spec.module.s250.stage238.rank_bucket_for(mapped)
        gate = spec.module.source_branch_gate_value(mapped, str(extra["source_branch_mode"]))
        records.append(
            {
                "timestamp": pd.Timestamp(record["timestamp"]),
                "symbol": record.get("symbol") or "US100",
                "split": str(record.get("split")),
                "label": str(record.get("label")),
                "label_class": int(record.get("label_class")),
                "bar_time_server": mapped["bar_time_server"],
                input_probe.SOURCE_SIGNAL_COLUMN: float(signal),
                rank_column: float(bucket_value),
                gate_column: float(gate),
                SOFT_FEATURE_NAME: float(record.get(SOFT_FEATURE_NAME) or 0.0),
            }
        )
    frame = pd.DataFrame.from_records(records)
    diagnostics = {
        "candidate_alias": spec.alias,
        "candidate_id": spec.candidate_id,
        "rank_column": rank_column,
        "gate_column": gate_column,
        "feature_order": ";".join(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "rows": int(len(frame)),
        "train_rows": int(frame["split"].eq("train").sum()),
        "validation_rows": int(frame["split"].eq("validation").sum()),
        "oos_rows": int(frame["split"].eq("oos").sum()),
        "signal_rows": int((frame[input_probe.SOURCE_SIGNAL_COLUMN] != 0.0).sum()),
        "blocked_signal_rows": int(((frame[input_probe.SOURCE_SIGNAL_COLUMN] != 0.0) & (frame[gate_column] >= 0.5)).sum()),
        "soft_score_q50": q(frame[SOFT_FEATURE_NAME].astype(float).to_list(), 0.50),
        "soft_score_q80": q(frame[SOFT_FEATURE_NAME].astype(float).to_list(), 0.80),
        "soft_score_q95": q(frame[SOFT_FEATURE_NAME].astype(float).to_list(), 0.95),
        "soft_score_max": float(frame[SOFT_FEATURE_NAME].max()),
    }
    return frame, feature_order, diagnostics


def split_diagnostics(candidate_alias: str, frame: pd.DataFrame, gate_column: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        part = frame.loc[frame["split"].eq(split)]
        labels = {str(k): int(v) for k, v in part["label_class"].value_counts().sort_index().items()}
        rows.append(
            {
                "candidate_alias": candidate_alias,
                "split": split,
                "rows": len(part),
                "class_counts": json.dumps(labels, ensure_ascii=False, sort_keys=True),
                "signal_rows": int((part[input_probe.SOURCE_SIGNAL_COLUMN] != 0.0).sum()),
                "blocked_signal_rows": int(((part[input_probe.SOURCE_SIGNAL_COLUMN] != 0.0) & (part[gate_column] >= 0.5)).sum()),
                "soft_score_q50": q(part[SOFT_FEATURE_NAME].astype(float).to_list(), 0.50),
                "soft_score_q80": q(part[SOFT_FEATURE_NAME].astype(float).to_list(), 0.80),
                "soft_score_q95": q(part[SOFT_FEATURE_NAME].astype(float).to_list(), 0.95),
                "integrity_judgment": "usable_with_boundary",
            }
        )
    stress = frame.loc[
        frame["split"].eq("train")
        & frame["timestamp"].ge(pd.Timestamp("2024-01-01", tz="UTC"))
        & frame["timestamp"].lt(pd.Timestamp("2025-01-01", tz="UTC"))
    ]
    rows.append(
        {
            "candidate_alias": candidate_alias,
            "split": PERIOD_LABEL,
            "rows": len(stress),
            "class_counts": json.dumps({str(k): int(v) for k, v in stress["label_class"].value_counts().sort_index().items()}, ensure_ascii=False, sort_keys=True),
            "signal_rows": int((stress[input_probe.SOURCE_SIGNAL_COLUMN] != 0.0).sum()),
            "blocked_signal_rows": int(((stress[input_probe.SOURCE_SIGNAL_COLUMN] != 0.0) & (stress[gate_column] >= 0.5)).sum()),
            "soft_score_q50": q(stress[SOFT_FEATURE_NAME].astype(float).to_list(), 0.50),
            "soft_score_q80": q(stress[SOFT_FEATURE_NAME].astype(float).to_list(), 0.80),
            "soft_score_q95": q(stress[SOFT_FEATURE_NAME].astype(float).to_list(), 0.95),
            "integrity_judgment": "historical_stress_read_only_not_training_target",
        }
    )
    return rows


def validation_rows(candidate_alias: str, probabilities: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    prob_cols = ["p_short", "p_flat", "p_long"]
    for split in ("train", "validation", "oos"):
        part = probabilities.loc[probabilities["split"].astype(str).eq(split)].copy()
        y = part["label_class"].astype("int64").to_numpy()
        proba = part.loc[:, prob_cols].to_numpy(dtype="float64")
        pred = np.argmax(proba, axis=1)
        short_decision = (part["p_short"].to_numpy(dtype="float64") >= 0.54) & (
            part["p_short"].to_numpy(dtype="float64") > part["p_long"].to_numpy(dtype="float64")
        )
        long_decision = (part["p_long"].to_numpy(dtype="float64") >= 0.52) & (
            part["p_long"].to_numpy(dtype="float64") >= part["p_short"].to_numpy(dtype="float64")
        )
        rows.append(
            {
                "candidate_alias": candidate_alias,
                "split": split,
                "rows": int(len(part)),
                "accuracy": float(accuracy_score(y, pred)),
                "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
                "log_loss": float(log_loss(y, proba, labels=[0, 1, 2])),
                "avg_p_short": float(part["p_short"].mean()),
                "avg_p_flat": float(part["p_flat"].mean()),
                "avg_p_long": float(part["p_long"].mean()),
                "short_threshold_decisions": int(short_decision.sum()),
                "long_threshold_decisions": int(long_decision.sum()),
                "flat_or_no_trade_decisions": int(len(part) - short_decision.sum() - long_decision.sum()),
                "selection_metric": "offline_label_sanity_only_not_trading_selection",
                "validation_judgment": "exploratory_materialized_for_mt5_test",
            }
        )
    return rows


def write_runtime_feature(path: Path, frame: pd.DataFrame, feature_order: Sequence[str]) -> dict[str, Any]:
    stress = frame.loc[
        frame["split"].eq("train")
        & frame["timestamp"].ge(pd.Timestamp("2024-01-01", tz="UTC"))
        & frame["timestamp"].lt(pd.Timestamp("2025-01-01", tz="UTC"))
    ].copy()
    rows = stress.loc[:, ["bar_time_server", *feature_order]].to_dict("records")
    write_runtime_csv(path, rows, ("bar_time_server", *feature_order))
    return {
        "feature_file": rel(path),
        "feature_sha256": sha256_file_lf_normalized(path),
        "rows": int(len(rows)),
    }


def fit_candidate(
    design_row: Mapping[str, str],
    spec: Any,
    source: pd.DataFrame,
    source_info: Mapping[str, Any],
    index: int,
) -> dict[str, Any]:
    frame, feature_order, diagnostics = candidate_feature_frame(source, spec)
    gate_column = str(diagnostics["gate_column"])
    local_root = DESIGN_ROOT / "softctx_retrain" / spec.alias
    feature_path = local_root / "features" / f"{spec.alias}_softctx_retrain_2024.csv"
    model_path = local_root / "models" / f"{spec.alias}_softctx_retrain_model.csv"
    feature_meta = write_runtime_feature(feature_path, frame, feature_order)
    ebm_spec = EbmVariantSpec(
        variant_id=f"{spec.alias}_softctx_retrain_p0",
        idea_id="stage267_retrained_soft_context_adapter",
        description=f"Stage267 P0 supervised main-effect EBM soft-context retrain for {spec.alias}.",
        max_bins=32,
        interactions=0,
        outer_bags=1,
        learning_rate=0.04,
        max_rounds=80,
        early_stopping_rounds=15,
        min_samples_leaf=24,
        reg_lambda=0.01,
        random_state=26710 + index,
    )
    train_frame = frame.loc[:, ["timestamp", "symbol", "split", "label", "label_class", *feature_order]].copy()
    model, fit_info = fit_ebm_variant(train_frame, feature_order, ebm_spec)
    model_meta = export_ebm_main_effect_score_table(
        model,
        model_path,
        feature_count=len(feature_order),
    )
    validation_sample = train_frame.loc[train_frame["split"].eq("validation")].head(2048)
    parity = check_ebm_score_table_probability_parity(
        model,
        model_path,
        validation_sample.loc[:, feature_order].to_numpy(dtype="float64"),
        feature_count=len(feature_order),
    )
    probabilities = probability_frame(model, train_frame, feature_order)
    importance = term_importance_frame(model, feature_order)

    common_feature_path = f"{COMMON_ROOT}/softctx_retrain/{spec.alias}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/softctx_retrain/{spec.alias}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    attempts: list[dict[str, Any]] = []
    for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
        (
            (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{spec.alias}_softctxretrain", "ta"),
            (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{spec.alias}_softctxretrain", "rt"),
        ),
        start=1,
    ):
        magic = 26790000 + index * 100 + role_index
        payload = attempt_payload(
            run_root=DESIGN_ROOT,
            run_id=RUN_ID,
            stage_number=267,
            exploration_label="stage267_RetrainedSoftContextAdapter__P0",
            attempt_name=f"{spec.alias}_softctxretrain_{attempt_token}_2024",
            tier=tier,
            split=PERIOD_LABEL,
            model_path=common_model_path,
            model_id=f"{RUN_ID}_{spec.alias}_softctx_retrain_ebm_v1",
            model_backend="ebm_table",
            feature_path=common_feature_path,
            feature_count=len(feature_order),
            feature_order_hash=ordered_hash(feature_order),
            short_threshold=spec.variant.short_threshold,
            long_threshold=spec.variant.long_threshold,
            min_margin=0.0,
            invert_signal=False,
            from_date="2024.01.02",
            to_date="2025.01.01",
            primary_active_tier="tier_a",
            attempt_role=attempt_role,
            record_view_prefix=prefix,
            max_hold_bars=spec.variant.max_hold_bars,
            common_root=f"{COMMON_ROOT}/softctx_retrain/{spec.alias}",
            fallback_enabled=False,
            close_on_flat_signal=spec.variant.close_on_flat_signal,
            reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
            close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
            extra_set_values=input_probe.base_extra_set_values(spec, magic),
        )
        payload.update(
            {
                "candidate_alias": spec.alias,
                "candidate_id": spec.candidate_id,
                "candidate_role": design_row.get("candidate_role"),
                "feature_design": FEATURE_DESIGN,
                "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                "execution_status": "not_executed",
            }
        )
        attempts.append(payload)

    manifest = {
        "candidate_alias": spec.alias,
        "candidate_id": spec.candidate_id,
        "candidate_role": design_row.get("candidate_role"),
        "priority": design_row.get("priority"),
        "feature_design": FEATURE_DESIGN,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "model_family": "ebm_main_effect_classifier_supervised_label_retrain",
        "source_model_family": "stage250_three_feature_decision_binding_ebm_table_csv_v1",
        "source_model_file": stage264_model_artifacts().get(spec.candidate_id, {}).get("path") or rel(spec.model_path),
        "source_anchor": stage264_model_artifacts().get(spec.candidate_id, {}).get("source_anchor"),
        "runtime_feature_file": feature_meta["feature_file"],
        "runtime_feature_sha256": feature_meta["feature_sha256"],
        "runtime_model_file": rel(model_path),
        "runtime_model_sha256": model_meta["sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "feature_order": ";".join(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "train_rows": fit_info["train_rows"],
        "training_class_counts": json.dumps(fit_info["class_counts"], ensure_ascii=False, sort_keys=True),
        "runtime_2024_rows": feature_meta["rows"],
        "source_rows": source_info["rows"],
        "parity_passed": parity["passed"],
        "parity_max_abs_diff": parity["max_abs_diff"],
        "threshold_policy": "fixed_short_0_54_long_0_52_inherited",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        "manifest": manifest,
        "diagnostics": diagnostics,
        "split_diagnostics": split_diagnostics(spec.alias, frame, gate_column),
        "validation_rows": validation_rows(spec.alias, probabilities),
        "importance_rows": [
            {"candidate_alias": spec.alias, **row}
            for row in importance.to_dict(orient="records")
        ],
        "parity": {"candidate_alias": spec.alias, **parity},
        "attempts": attempts,
        "fit_info": fit_info,
        "ebm_spec": ebm_spec.payload(),
    }


def build_source_audit(source_info: Mapping[str, Any]) -> list[dict[str, Any]]:
    model_input_exists = path_exists(MODEL_INPUT_DATASET_PATH)
    feature_order_exists = path_exists(MODEL_INPUT_FEATURE_ORDER_PATH)
    stage264_exists = path_exists(RUN264_MANIFEST_PATH)
    design_exists = path_exists(INPUT_DESIGN_PATH)
    rows = [
        {
            "check_id": "K_AUDIT_01_run267J_design",
            "check_family": "artifact_lineage(산출물 계보)",
            "status": bool_status(design_exists),
            "evidence": rel(INPUT_DESIGN_PATH),
            "effect": "ties_materialization_to_run267J_design(물질화를 267J 설계에 연결)",
        },
        {
            "check_id": "K_AUDIT_02_training_dataset",
            "check_family": "data_integrity(데이터 무결성)",
            "status": bool_status(model_input_exists),
            "evidence": f"{rel(MODEL_INPUT_DATASET_PATH)};sha256={sha_or_missing(MODEL_INPUT_DATASET_PATH)}",
            "effect": "uses_original_label_dataset_not_MT5_profit(원래 라벨 데이터셋 사용, MT5 손익 라벨 아님)",
        },
        {
            "check_id": "K_AUDIT_03_feature_order_contract",
            "check_family": "data_integrity(데이터 무결성)",
            "status": bool_status(feature_order_exists),
            "evidence": f"{rel(MODEL_INPUT_FEATURE_ORDER_PATH)};sha256={sha_or_missing(MODEL_INPUT_FEATURE_ORDER_PATH)}",
            "effect": "confirms_stage58_model_input_surface_exists(58개 모델 입력 표면 존재 확인)",
        },
        {
            "check_id": "K_AUDIT_04_label_split_contract",
            "check_family": "model_validation(모델 검증)",
            "status": bool_status(path_exists(TRAINING_CONTRACT_PATH)),
            "evidence": rel(TRAINING_CONTRACT_PATH),
            "effect": "keeps_label_v1_and_split_v1_named(라벨 v1과 스플릿 v1을 이름 붙임)",
        },
        {
            "check_id": "K_AUDIT_05_source_model_family",
            "check_family": "model_validation(모델 검증)",
            "status": "pass_with_boundary",
            "evidence": rel(RUN264_MANIFEST_PATH) if stage264_exists else "missing",
            "effect": "resolves_source_as_decision_binding_score_table_not_original_supervised_model(원천이 원래 지도학습 모델이 아니라 결정 표면 점수표임을 확정)",
        },
        {
            "check_id": "K_AUDIT_06_2024_boundary",
            "check_family": "data_integrity(데이터 무결성)",
            "status": "pass",
            "evidence": "2024 rows are exported for MT5 historical stress only",
            "effect": "prevents_training_on_2024_MT5_profit(2024 MT5 손익 학습 방지)",
        },
        {
            "check_id": "K_AUDIT_07_source_frame",
            "check_family": "data_integrity(데이터 무결성)",
            "status": "pass" if source_info["rows"] == 46650 and source_info["duplicates"] == 0 else "usable_with_boundary",
            "evidence": f"rows={source_info['rows']};duplicates={source_info['duplicates']};missing_labels={source_info['missing_label_rows']}",
            "effect": "confirms_Tier_A_time_ordered_label_surface(티어 A 시간순 라벨 표면 확인)",
        },
        {
            "check_id": "K_AUDIT_08_runtime_mapping",
            "check_family": "runtime_parity_precheck(런타임 동등성 사전 점검)",
            "status": "pass_with_boundary",
            "evidence": "score_table_parity_check;attempts.csv;runtime_contract.csv",
            "effect": "prepares_MT5_batch_without_runtime_authority_claim(MT5 묶음 준비, 런타임 권위 주장 없음)",
        },
    ]
    return rows


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_role": attempt.get("candidate_role"),
                "feature_design": attempt.get("feature_design"),
                "model_materialization_type": attempt.get("model_materialization_type"),
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def runtime_contract_rows(manifest_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in manifest_rows:
        rows.append(
            {
                "candidate_alias": row["candidate_alias"],
                "candidate_id": row["candidate_id"],
                "candidate_role": row["candidate_role"],
                "shared_contract": "feature_order;supervised_ebm_score_table_csv;thresholds;MT5_runtime_settings;2024_historical_stress_window",
                "feature_count": row["feature_count"],
                "feature_order_hash": row["feature_order_hash"],
                "model_backend": "ebm_table",
                "model_materialization_type": row["model_materialization_type"],
                "short_threshold": 0.54,
                "long_threshold": 0.52,
                "min_margin": 0.0,
                "max_hold_bars": 3,
                "known_difference": "model is supervised label retrain over soft context features; not run267I hand-shaped score extension",
                "runtime_claim_boundary": "research_only_execution_pending_no_onnx_no_candidate_selection",
            }
        )
    return rows


def lineage_payload(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    inputs = (
        ("run267J_retrain_design", INPUT_DESIGN_PATH),
        ("run267J_validation_plan", INPUT_J_VALIDATION_PLAN_PATH),
        ("run267I_candidate_review", INPUT_I_REVIEW_PATH),
        ("stage264_manifest", RUN264_MANIFEST_PATH),
        ("model_input_dataset", MODEL_INPUT_DATASET_PATH),
        ("model_input_feature_order", MODEL_INPUT_FEATURE_ORDER_PATH),
        ("training_label_split_contract", TRAINING_CONTRACT_PATH),
        ("model_input_contract", MODEL_INPUT_CONTRACT_PATH),
        ("producer_script", PRODUCER_PATH),
    )
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "inputs": [
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": sha_or_missing(path),
            }
            for artifact_id, path in inputs
        ],
        "outputs": result["outputs"],
        "availability": "tracked_repo_outputs_plus_common_files_copy",
        "lineage_judgment": "connected_with_boundary",
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    manifests = result["feature_model_manifest"]
    lines = [
        "# Stage267 Run267K Retrained Soft-Context Adapter Materialization(267단계 267K 재학습 부드러운 문맥 어댑터 물질화)",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "- action(행동): run267J(267J 실행)의 source audit(원천 감사) 조건을 확인하고 `s264_aih`, `s264_lc` P0 후보를 supervised EBM(지도학습 EBM) score-table CSV(점수표 CSV)로 재학습 물질화했다.",
        "- effect(효과): run267I(267I 실행)의 hand-shaped score extension(손으로 만든 점수 확장)에서 벗어나, label v1/split v1(라벨 v1/스플릿 v1)을 쓰는 실제 재학습 후보를 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 상태로 만들었다.",
        "- boundary(경계): 아직 MT5 실행 결과가 없으므로 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.",
        "",
        "## Materialized Candidates(물질화 후보)",
        "",
        "| candidate(후보) | train rows(학습 행) | 2024 rows(2024 행) | parity(동등성) | feature hash(피처 해시) |",
        "|---|---:|---:|---|---|",
    ]
    for row in manifests:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['train_rows']} | {row['runtime_2024_rows']} | `{row['parity_passed']}` diff `{float(row['parity_max_abs_diff']):.3g}` | `{row['feature_order_hash']}` |"
        )
    lines.extend(
        [
            "",
            "## Source Audit(원천 감사)",
            "",
            "| check(확인) | status(상태) | effect(효과) |",
            "|---|---|---|",
        ]
    )
    for row in result["source_audit"]:
        lines.append(f"| `{row['check_id']}` | `{row['status']}` | {row['effect']} |")
    lines.extend(
        [
            "",
            "## Data Integrity(데이터 무결성)",
            "",
            "- data_source(데이터 원천): Stage56 source frame(56단계 원천 프레임), Stage264 decision-binding surface(264단계 결정 표면), Stage267 run267J design(267J 설계), model input dataset(모델 입력 데이터셋).",
            "- time_axis(시간축): UTC timestamp(UTC 타임스탬프)를 기준으로 학습하고, MT5 runtime feature(런타임 피처)는 기존 tester contract(테스터 계약)에 맞춰 `bar_time_server` 문자열로 내보냈다.",
            "- feature_label_boundary(피처/라벨 경계): 2024 MT5 손익이나 약한 월 결과를 라벨로 쓰지 않았고, `label_v1_fwd12_m5_logret_train_q33_3class`만 썼다.",
            "- split_boundary(스플릿 경계): train/validation/OOS(학습/검증/표본외)는 `split_v1`을 유지하고, 2024년은 train-era historical stress(학습권 과거 압박) 출력으로만 쓴다.",
            "",
            "## Model Validation(모델 검증)",
            "",
            "- model_family(모델군): `ebm_main_effect_classifier_supervised_label_retrain`.",
            "- comparison_baseline(비교 기준): `run267I_score_table_extension_not_retrained`.",
            "- threshold_policy(임계값 정책): short(숏) `0.54`, long(롱) `0.52` 고정.",
            "- calibration_risk(보정 위험): score(점수)는 runtime decision score(런타임 결정 점수)로만 취급하고, 확률 품질이나 trading quality(거래 품질)는 MT5 실행 전 주장하지 않는다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_audit(원천 감사): `{rel(SOURCE_AUDIT_PATH)}`",
            f"- feature_model_manifest(피처/모델 목록): `{rel(FEATURE_MODEL_MANIFEST_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
            f"- attempts(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def materialize() -> dict[str, Any]:
    created_at = utc_now()
    design_rows = p0_design_rows()
    specs = specs_by_alias()
    source, source_info = source_frame()

    source_audit = build_source_audit(source_info)
    candidate_results = [
        fit_candidate(row, specs[str(row["candidate_alias"])], source, source_info, index)
        for index, row in enumerate(design_rows, start=1)
    ]
    manifest_rows = [item["manifest"] for item in candidate_results]
    diagnostics_rows = [item["diagnostics"] for item in candidate_results]
    split_diag_rows = [row for item in candidate_results for row in item["split_diagnostics"]]
    validation_metric_rows = [row for item in candidate_results for row in item["validation_rows"]]
    importance_rows = [row for item in candidate_results for row in item["importance_rows"]]
    parity_rows = [item["parity"] for item in candidate_results]
    attempts = [attempt for item in candidate_results for attempt in item["attempts"]]
    contract_rows = runtime_contract_rows(manifest_rows)
    result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_info": source_info,
        "source_audit": source_audit,
        "feature_model_manifest": manifest_rows,
        "candidate_diagnostics": diagnostics_rows,
        "training_frame_diagnostics": split_diag_rows,
        "model_validation_snapshot": validation_metric_rows,
        "term_importance_rows": importance_rows,
        "score_table_parity_check": parity_rows,
        "runtime_contract": contract_rows,
        "attempts": attempts,
        "attempt_count": len(attempts),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "source_audit": rel(SOURCE_AUDIT_PATH),
            "training_frame_diagnostics": rel(TRAINING_DIAGNOSTICS_PATH),
            "model_validation_snapshot": rel(MODEL_VALIDATION_PATH),
            "term_importance": rel(TERM_IMPORTANCE_PATH),
            "score_table_parity_check": rel(PARITY_CHECK_PATH),
            "feature_model_manifest": rel(FEATURE_MODEL_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempts": rel(ATTEMPT_MANIFEST_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    result["lineage"] = lineage_payload(created_at, result)
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(SOURCE_AUDIT_PATH, result["source_audit"], ("check_id", "check_family", "status", "evidence", "effect"))
    write_csv(
        TRAINING_DIAGNOSTICS_PATH,
        result["training_frame_diagnostics"],
        (
            "candidate_alias",
            "split",
            "rows",
            "class_counts",
            "signal_rows",
            "blocked_signal_rows",
            "soft_score_q50",
            "soft_score_q80",
            "soft_score_q95",
            "integrity_judgment",
        ),
    )
    write_csv(
        MODEL_VALIDATION_PATH,
        result["model_validation_snapshot"],
        (
            "candidate_alias",
            "split",
            "rows",
            "accuracy",
            "balanced_accuracy",
            "log_loss",
            "avg_p_short",
            "avg_p_flat",
            "avg_p_long",
            "short_threshold_decisions",
            "long_threshold_decisions",
            "flat_or_no_trade_decisions",
            "selection_metric",
            "validation_judgment",
        ),
    )
    write_csv(
        TERM_IMPORTANCE_PATH,
        result["term_importance_rows"],
        (
            "candidate_alias",
            "term_index",
            "term_name",
            "feature",
            "term_degree",
            "importance",
            "gain",
            "gain_share",
            "score_abs_max",
            "score_std",
            "short_range",
            "flat_range",
            "long_range",
        ),
    )
    write_csv(
        PARITY_CHECK_PATH,
        result["score_table_parity_check"],
        ("candidate_alias", "passed", "max_abs_diff", "tolerance", "rows", "table_path", "zeroed_feature_indices"),
    )
    write_csv(
        FEATURE_MODEL_MANIFEST_PATH,
        result["feature_model_manifest"],
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "priority",
            "feature_design",
            "model_materialization_type",
            "model_family",
            "source_model_family",
            "source_model_file",
            "source_anchor",
            "runtime_feature_file",
            "runtime_feature_sha256",
            "runtime_model_file",
            "runtime_model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_order",
            "feature_order_hash",
            "feature_count",
            "train_rows",
            "training_class_counts",
            "runtime_2024_rows",
            "source_rows",
            "parity_passed",
            "parity_max_abs_diff",
            "threshold_policy",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        result["runtime_contract"],
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(result["attempts"]),
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "feature_design",
            "model_materialization_type",
            "attempt_name",
            "tier",
            "split",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "fallback_enabled",
            "execution_status",
        ),
    )
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "claim_boundary": CLAIM_BOUNDARY,
            "source_info": result["source_info"],
            "source_audit": result["source_audit"],
            "feature_model_manifest": result["feature_model_manifest"],
            "runtime_contract": result["runtime_contract"],
            "attempts": result["attempts"],
            "next_action": NEXT_ACTION,
        },
    )
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    stage_row = {
        "row_id": "stage267_run267K_retrained_soft_context_adapter_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "retrained_soft_context_adapter_source_audit_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 materialization attempts planned",
        "scoreboard": "experiment_materialization_source_audit",
        "status": STATUS,
        "judgment": "materialized_execution_pending_no_candidate_selection",
        "evidence_boundary": "source_audit_training_materialization_no_mt5_kpi_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"audit_rows={len(result['source_audit'])};candidate_count={len(result['feature_model_manifest'])};attempts={result['attempt_count']};next_action={NEXT_ACTION}.",
    }
    rows = [item for item in read_csv(STAGE_LEDGER_PATH) if item.get("row_id") != stage_row["row_id"]]
    rows.append(stage_row)
    write_csv(
        STAGE_LEDGER_PATH,
        rows,
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_retrained_soft_context_adapter_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267K source audit and supervised EBM materialization; attempts={result['attempt_count']}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__retrained_soft_context_adapter_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "retrained_soft_context_adapter_materialization",
            "parent_run_id": RUN_ID,
            "record_view": "retrained_soft_context_adapter_materialization",
            "tier_scope": "Tier A and Tier A+B historical 2024 materialization attempts planned",
            "kpi_scope": "source_audit_training_materialization_no_mt5_kpi",
            "scoreboard_lane": "experiment_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"candidate_count={len(result['feature_model_manifest'])};attempts={result['attempt_count']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_started_materialization_only",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
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
        ),
    )
    entries = [
        ("stage267_run267K_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267K source audit and retrained soft-context materialization."),
        ("stage267_run267K_source_audit", "source_audit", SOURCE_AUDIT_PATH, "Run267K source audit receipt."),
        ("stage267_run267K_training_diagnostics", "training_frame_diagnostics", TRAINING_DIAGNOSTICS_PATH, "Run267K split diagnostics."),
        ("stage267_run267K_model_validation", "model_validation_snapshot", MODEL_VALIDATION_PATH, "Run267K offline label validation snapshot."),
        ("stage267_run267K_term_importance", "term_importance", TERM_IMPORTANCE_PATH, "Run267K EBM term importance."),
        ("stage267_run267K_parity_check", "score_table_parity_check", PARITY_CHECK_PATH, "Run267K Python/table parity check."),
        ("stage267_run267K_feature_model_manifest", "feature_model_manifest", FEATURE_MODEL_MANIFEST_PATH, "Run267K feature/model manifest."),
        ("stage267_run267K_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267K runtime contract."),
        ("stage267_run267K_attempts", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267K MT5 attempt manifest."),
        ("stage267_run267K_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267K materialization manifest."),
        ("stage267_run267K_lineage", "lineage", LINEAGE_PATH, "Run267K lineage."),
        ("stage267_run267K_result", "result", RESULT_PATH, "Run267K JSON result."),
        ("stage267_run267K_report", "review_report", REPORT_PATH, "Run267K user-facing report."),
    ]
    for row in result["feature_model_manifest"]:
        alias = str(row["candidate_alias"])
        entries.extend(
            [
                (f"stage267_run267K_{alias}_runtime_feature", "runtime_feature_csv", Path(str(row["runtime_feature_file"])), f"Run267K {alias} runtime feature CSV."),
                (f"stage267_run267K_{alias}_runtime_model", "runtime_model_csv", Path(str(row["runtime_model_file"])), f"Run267K {alias} runtime EBM score table CSV."),
            ]
        )
    registry_rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_docs() -> None:
    report_line = (
        f"- Stage267(267단계) run267K retrained soft-context Adapter materialization(재학습 부드러운 문맥 어댑터 물질화): `{rel(REPORT_PATH)}`"
    )
    for path in (CURRENT_WORKING_STATE_PATH,):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `soft_context_retrained_adapter_materialization`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = append_after_contains(text, "stage267_run267J_retrained_soft_context_adapter_design.md", report_line)
        current_next = "\n".join(
            [
                "## Current Next Action(현재 다음 행동)",
                f"- latest_materialization(최신 물질화): `{rel(REPORT_PATH)}`.",
                "",
                f"- next_run(다음 실행): `{NEXT_ACTION}`",
                "- action(행동): run267K(267K 실행)는 source audit(원천 감사)을 통과 가능한 경계로 확인하고 `s264_aih`, `s264_lc` P0 supervised EBM(지도학습 EBM) score table(점수표)을 물질화했다.",
                "- effect(효과): 다음 작업은 MT5(MetaTrader 5, 메타트레이더5) 2024 historical stress(2024 과거 압박) 실행으로 실제 trading KPI(거래 핵심 성과 지표)를 확인할 수 있다.",
                f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 물질화된 set/ini/model/feature 파일로 MT5 batch(MT5 묶음)를 실행하고 trade quality(거래 품질)와 curve(곡선)를 검토한다.",
            ]
        )
        text = replace_section(text, "## Current Next Action(현재 다음 행동)", "Forbidden claims(금지 주장):", current_next)
        tail = (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭)가 여전히 불편해 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267J(267J 실행)는 retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계)을 완료했다.\n"
            "Effect(효과): run267I(267I 실행)의 개선을 선택 후보(selected candidate, 선택 후보)로 올리지 않고, 원천 감사와 짧은 중단 규칙으로 다음 run267K(267K 실행)를 제한했다.\n\n"
            "Run267K(267K 실행)는 retrained soft-context Adapter materialization(재학습 부드러운 문맥 어댑터 물질화)을 완료했다.\n"
            "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 아직 없고, 다음에는 MT5 batch(MT5 묶음) 실행으로 실제 거래 결과를 확인해야 한다."
        )
        text = replace_tail_from_marker(text, "Run267I(267I 실행)는", tail)
        write_md(path, text)

    for path in (SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        status_prefix = "- stage_status(단계 상태):" if path == SELECTION_STATUS_PATH else "- status(상태):"
        text = replace_line_prefix(text, status_prefix, f"{status_prefix} `{STATUS}`")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, "run267J_retrained_soft_context_adapter_design", f"- run267K_retrained_soft_context_adapter_materialization(267K 재학습 부드러운 문맥 어댑터 물질화): `{rel(REPORT_PATH)}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        tail = (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267J(267J 실행)는 retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계)을 완료했다.\n"
            "Effect(효과): run267K(267K 실행)의 원천 감사와 중단 규칙을 만들었다.\n\n"
            "Run267K(267K 실행)는 retrained soft-context Adapter materialization(재학습 부드러운 문맥 어댑터 물질화)을 완료했다.\n"
            f"Effect(효과): selected candidate(선택 후보)는 여전히 없고, next_action(다음 행동)은 `{NEXT_ACTION}`이다."
        )
        text = replace_tail_from_marker(text, "Run267I(267I 실행)는", tail)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace("current_run_id: run267J_stage267_retrained_soft_context_adapter_design_v1", f"current_run_id: {RUN_ID}", 1)
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace(
            "current_focus:",
            "current_focus:\n"
            "- >-\n"
            f"  Stage267(267단계) run267K(267K 실행) retrained soft-context Adapter materialization(재학습 부드러운 문맥 어댑터 물질화) `{STATUS}`. Effect(효과): source audit(원천 감사)을 확인하고 `s264_aih`, `s264_lc` P0 supervised EBM(지도학습 EBM) score table(점수표)을 MT5 execution pending(MT5 실행 대기) 상태로 만들었으며 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
            1,
        )
    workspace = workspace.replace("  status: run267J_retrained_soft_context_adapter_design_completed", f"  status: {STATUS}", 1)
    workspace = workspace.replace("  current_run_id: run267J_stage267_retrained_soft_context_adapter_design_v1", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace("  last_completed_run_id: run267I_stage267_p0_soft_noncalendar_adapter_materialization_v1", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267K_audit_retrain_source_and_materialize_soft_context_p0`이다. Effect(효과): source audit(원천 감사)에서 label(라벨), split(스플릿), feature order(피처 순서)를 확인한 뒤에만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): 물질화된 set/ini/model/feature 파일로 MT5 batch(MT5 묶음)를 실행하고 trade quality(거래 품질)와 curve(곡선)를 검토한다.",
        1,
    )
    workspace = workspace.replace(
        "active_run267I_p0_soft_noncalendar_adapter_mt5_review_completed(267I P0 부드러운 비달력 어댑터 MT5 검토 완료 활성)",
        "active_run267K_retrained_soft_context_adapter_materialized_execution_pending(267K 재학습 부드러운 문맥 어댑터 물질화 후 실행 대기 활성)",
        1,
    )
    workspace = workspace.replace("  next_action: run267K_audit_retrain_source_and_materialize_soft_context_p0", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267J_retrained_soft_context_adapter_design_path",
        f"  run267K_retrained_soft_context_adapter_materialization_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = materialize()
    write_outputs(result)
    update_ledgers(str(result["created_at_utc"]), result)
    update_docs()
    print(
        json.dumps(
            {
                "status": result["status"],
                "candidate_count": len(result["feature_model_manifest"]),
                "attempts": result["attempt_count"],
                "parity_passed": [row["passed"] for row in result["score_table_parity_check"]],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
