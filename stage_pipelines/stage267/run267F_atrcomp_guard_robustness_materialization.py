from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267C_p1_soft_axis_followup_materialization as p1_materializer
from stage_pipelines.stage267 import run267D_adapter_p2_materialization as run267d_materializer
from stage_pipelines.stage267 import run267D_adapter_p2_review as run267d_review
from stage_pipelines.stage267 import run267E_adapter_p2_followup_review as run267e_review


STAGE_ID = input_probe.STAGE_ID
RUN_ID = "run267F_stage267_atrcomp_guard_robustness_non_calendar_v1"
RUN_NUMBER = "run267F"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY
STAGE_ROOT = input_probe.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "atrcomp_guard_robustness"
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

INPUT_DESIGN_PATH = run267d_materializer.DESIGN_MATRIX_PATH
INPUT_REVIEW_PATH = run267d_review.CANDIDATE_AXIS_REVIEW_PATH
INPUT_E_REVIEW_PATH = run267e_review.GUARD_COMPARISON_PATH
INPUT_E_NEGATIVE_SLICE_PATH = run267e_review.NEGATIVE_SLICE_PATH

DESIGN_MATRIX_PATH = DESIGN_ROOT / "design.csv"
FEATURE_MANIFEST_PATH = DESIGN_ROOT / "feature_manifest.csv"
RUNTIME_CONTRACT_PATH = DESIGN_ROOT / "contract.csv"
ATTEMPT_MANIFEST_PATH = DESIGN_ROOT / "attempts.csv"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267F_guard_robustness_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267F_atrcomp_guard_robustness_materialization.py")

STATUS = "run267F_atrcomp_guard_robustness_materialized_execution_pending"
NEXT_ACTION = "run267F_execute_non_calendar_guard_mt5_batch"
PERIOD_LABEL = input_probe.PERIOD_LABEL
COMMON_ROOT = "OPV2/s267f/run267F_atrcomp_guard_robustness"
SOURCE_SIGNAL_COLUMN = input_probe.SOURCE_SIGNAL_COLUMN


@dataclass(frozen=True)
class GuardVariant:
    variant_id: str
    short_id: str
    comparison_anchor: str
    guard_family: str
    materialization_rule: str
    intent: str
    predicate: Callable[[Mapping[str, Any]], bool]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
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


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_runtime_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"missing replacement text: {old}")
    return text.replace(old, new, 1)


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def source_signal(row: Mapping[str, Any]) -> int:
    try:
        return int(round(float(row.get(SOURCE_SIGNAL_COLUMN) or 0.0)))
    except (TypeError, ValueError):
        return 0


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def review_by_pair() -> dict[tuple[str, str], dict[str, str]]:
    return {(row.get("candidate_alias", ""), row.get("feature_axis", "")): row for row in read_csv(INPUT_REVIEW_PATH)}


def run267e_by_alias() -> dict[str, dict[str, str]]:
    return {row.get("candidate_alias", ""): row for row in read_csv(INPUT_E_REVIEW_PATH)}


def common_path(path_text: str) -> Path:
    return COMMON_FILES_ROOT_DEFAULT / Path(path_text)


def build_context() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    source, source_info = input_probe.build_2024_source_frame()
    atr_values = pd.to_numeric(source.get("atr_14_over_atr_50"), errors="coerce").dropna()
    vol_values = pd.to_numeric(source.get("historical_vol_20"), errors="coerce").dropna()
    di_values = pd.to_numeric(source.get("di_spread_14"), errors="coerce").abs().dropna()
    if atr_values.empty or vol_values.empty or di_values.empty:
        raise RuntimeError("missing context edge inputs for run267F")
    atr_edge = float(atr_values.quantile(1 / 3))
    vol_edges = (float(vol_values.quantile(1 / 3)), float(vol_values.quantile(2 / 3)))
    di_abs_q33 = float(di_values.quantile(1 / 3))
    context = p1_materializer.source_context(source, atr_edge, vol_edges)
    context_info = {
        "source_info": source_info,
        "atr_14_over_atr_50_q33": atr_edge,
        "historical_vol_20_edges": vol_edges,
        "di_spread_14_abs_q33": di_abs_q33,
        "context_rows": len(context),
    }
    return context, context_info


def guard_variants(di_abs_q33: float) -> tuple[GuardVariant, ...]:
    return (
        GuardVariant(
            variant_id="atrcomp_adx20_25_noncalendar_guard",
            short_id="adx2025",
            comparison_anchor="run267E_atrcomp_monday_guard",
            guard_family="trend_strength_non_calendar",
            materialization_rule=(
                "entry signal(진입 신호)을 ADX 20-25(추세 강도 20-25) source context(원천 문맥)에서만 "
                "flat(무거래)으로 바꾼다."
            ),
            intent=(
                "run267E Monday guard(월요일 방어)와 비슷한 신호 차단 크기를 비달력 trend-strength(추세 강도) 축으로 "
                "재현할 수 있는지 확인한다."
            ),
            predicate=lambda row: row.get("adx_bucket") == "adx_20_25",
        ),
        GuardVariant(
            variant_id="atrcomp_di_low_q33_replacement_guard",
            short_id="dilowq33",
            comparison_anchor="run267E_atrcomp_monday_guard",
            guard_family="directional_imbalance_replacement",
            materialization_rule=(
                "entry signal(진입 신호)을 abs(DI spread 14)(DI 차이 절대값 14)가 하위 33% 이하인 "
                "source context(원천 문맥)에서만 flat(무거래)으로 바꾼다."
            ),
            intent=(
                "ADX(추세 강도 지표) 하나에 우연히 맞은 것인지 보려고 DI spread(방향성 차이)라는 유사 의미 피처로 "
                "더 강한 stress replacement(압박 대체)를 만든다."
            ),
            predicate=lambda row: (
                row.get("di_spread_14") is not None and abs(float(row.get("di_spread_14"))) <= di_abs_q33
            ),
        ),
    )


def transform_feature_file(
    source: Path,
    destination: Path,
    variant: GuardVariant,
    context: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    rows = read_csv(source)
    if not rows:
        raise RuntimeError(f"empty source feature file: {source}")
    columns = list(rows[0].keys())
    if SOURCE_SIGNAL_COLUMN not in columns:
        raise RuntimeError(f"missing source signal column: {source}")

    transformed: list[dict[str, Any]] = []
    total_signal_rows = 0
    long_signal_rows = 0
    short_signal_rows = 0
    matched_rows = 0
    blocked_signal_rows = 0
    blocked_long_signal_rows = 0
    blocked_short_signal_rows = 0
    context_missing_rows = 0
    for row in rows:
        current = dict(row)
        signal = source_signal(row)
        if signal != 0:
            total_signal_rows += 1
            if signal > 0:
                long_signal_rows += 1
            else:
                short_signal_rows += 1

        context_row = context.get(str(row.get("bar_time_server", "")))
        if context_row is None:
            context_missing_rows += 1
            should_block = False
        else:
            should_block = bool(variant.predicate(context_row))
        if should_block:
            matched_rows += 1
            if signal != 0:
                blocked_signal_rows += 1
                if signal > 0:
                    blocked_long_signal_rows += 1
                else:
                    blocked_short_signal_rows += 1
            current[SOURCE_SIGNAL_COLUMN] = "0"
        transformed.append(current)

    write_runtime_csv(destination, transformed, columns)
    kept_signal_rows = total_signal_rows - blocked_signal_rows
    return {
        "source_feature_file": rel(source),
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "feature_order": ";".join(columns[1:]),
        "feature_order_hash": input_probe.ordered_hash(tuple(columns[1:])),
        "rows": len(rows),
        "total_signal_rows": total_signal_rows,
        "long_signal_rows": long_signal_rows,
        "short_signal_rows": short_signal_rows,
        "matched_rows": matched_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "blocked_long_signal_rows": blocked_long_signal_rows,
        "blocked_short_signal_rows": blocked_short_signal_rows,
        "kept_signal_rows": kept_signal_rows,
        "signal_retention": kept_signal_rows / total_signal_rows if total_signal_rows else None,
        "context_missing_rows": context_missing_rows,
    }


def copy_model(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {
        "source_model_file": rel(source),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
    }


def build_attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "source_axis": attempt.get("source_axis"),
                "guard_variant": attempt.get("guard_variant"),
                "guard_family": attempt.get("guard_family"),
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


def build_materialization() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    context, context_info = build_context()
    variants = guard_variants(float(context_info["di_spread_14_abs_q33"]))
    design_input = [row for row in read_csv(INPUT_DESIGN_PATH) if row.get("axis") == "atrcomp"]
    if len(design_input) != 5:
        raise RuntimeError(f"expected 5 atrcomp design rows, found {len(design_input)}")
    reviews = review_by_pair()
    run267e_rows = run267e_by_alias()
    specs = specs_by_alias()

    design_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []

    for variant_index, variant in enumerate(variants, start=1):
        for candidate_index, row in enumerate(design_input, start=1):
            alias = row.get("candidate_alias", "")
            spec = specs[alias]
            review = reviews.get((alias, "atrcomp"), {})
            e_review = run267e_rows.get(alias, {})

            local_root = DESIGN_ROOT / variant.short_id / alias
            source_feature = common_path(str(row.get("common_feature_path", "")))
            source_model = common_path(str(row.get("common_model_path", "")))
            feature_path = local_root / "features" / f"{alias}_{variant.short_id}.csv"
            model_path = local_root / "models" / f"{alias}_{variant.short_id}_model.csv"
            feature_meta = transform_feature_file(source_feature, feature_path, variant, context)
            model_meta = copy_model(source_model, model_path)
            common_feature_path = f"{COMMON_ROOT}/{variant.short_id}/{alias}/features/{feature_path.name}"
            common_model_path = f"{COMMON_ROOT}/{variant.short_id}/{alias}/models/{model_path.name}"
            common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
            common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

            feature_row = {
                "candidate_alias": alias,
                "candidate_role": row.get("candidate_role"),
                "source_axis": "atrcomp",
                "guard_variant": variant.short_id,
                "guard_variant_id": variant.variant_id,
                "guard_family": variant.guard_family,
                "comparison_anchor": variant.comparison_anchor,
                "materialization_rule": variant.materialization_rule,
                "intent": variant.intent,
                "source_feature_file": feature_meta["source_feature_file"],
                "feature_file": feature_meta["feature_file"],
                "feature_sha256": feature_meta["feature_sha256"],
                "source_model_file": model_meta["source_model_file"],
                "model_file": model_meta["model_file"],
                "model_sha256": model_meta["model_sha256"],
                "common_feature_path": common_feature_path,
                "common_feature_sha256": common_feature["sha256"],
                "common_model_path": common_model_path,
                "common_model_sha256": common_model["sha256"],
                "feature_order": feature_meta["feature_order"],
                "feature_order_hash": feature_meta["feature_order_hash"],
                "rows": feature_meta["rows"],
                "total_signal_rows": feature_meta["total_signal_rows"],
                "matched_rows": feature_meta["matched_rows"],
                "blocked_signal_rows": feature_meta["blocked_signal_rows"],
                "blocked_long_signal_rows": feature_meta["blocked_long_signal_rows"],
                "blocked_short_signal_rows": feature_meta["blocked_short_signal_rows"],
                "kept_signal_rows": feature_meta["kept_signal_rows"],
                "signal_retention": feature_meta["signal_retention"],
                "context_missing_rows": feature_meta["context_missing_rows"],
            }
            feature_rows.append(feature_row)

            design_rows.append(
                {
                    "candidate_alias": alias,
                    "candidate_role": row.get("candidate_role"),
                    "source_axis": "atrcomp",
                    "guard_variant": variant.short_id,
                    "guard_variant_id": variant.variant_id,
                    "guard_family": variant.guard_family,
                    "comparison_anchor": variant.comparison_anchor,
                    "run267d_net_profit": review.get("net_profit", ""),
                    "run267d_profit_factor": review.get("profit_factor", ""),
                    "run267d_trade_count": review.get("trade_count", ""),
                    "run267d_equity_dd_percent": review.get("report_equity_drawdown_percent", ""),
                    "run267e_net_delta": e_review.get("net_delta_vs_run267d_atrcomp", ""),
                    "run267e_pf_delta": e_review.get("pf_delta_vs_run267d_atrcomp", ""),
                    "run267e_trade_delta": e_review.get("trade_delta_vs_run267d_atrcomp", ""),
                    "run267e_dd_delta": e_review.get("dd_delta_vs_run267d_atrcomp", ""),
                    "weakest_month_after_run267e": e_review.get("weakest_month", ""),
                    "weakest_month_net_after_run267e": e_review.get("weakest_month_net", ""),
                    "blocked_signal_rows": feature_meta["blocked_signal_rows"],
                    "kept_signal_rows": feature_meta["kept_signal_rows"],
                    "signal_retention": feature_meta["signal_retention"],
                    "common_feature_path": common_feature_path,
                    "common_model_path": common_model_path,
                    "design_read": (
                        "non_calendar_mirror_test(비달력 거울 시험)"
                        if variant.short_id == "adx2025"
                        else "similar_feature_replacement_stress(유사 피처 대체 압박)"
                    ),
                    "next_validation": "MT5 batch(묶음 실행), guard comparison(방어 비교), time-slice KPI(시간 구간 핵심 성과 지표), curve diagnostics(곡선 진단)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

            contract_rows.append(
                {
                    "candidate_alias": alias,
                    "source_axis": "atrcomp",
                    "guard_variant": variant.short_id,
                    "shared_contract": "feature_order;thresholds;model_csv;MT5 runtime settings;2024 historical stress window",
                    "feature_count": 3,
                    "feature_order": feature_meta["feature_order"],
                    "feature_order_hash": feature_meta["feature_order_hash"],
                    "model_backend": "ebm_table",
                    "short_threshold": spec.variant.short_threshold,
                    "long_threshold": spec.variant.long_threshold,
                    "min_margin": 0.0,
                    "max_hold_bars": spec.variant.max_hold_bars,
                    "close_on_flat_signal": spec.variant.close_on_flat_signal,
                    "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
                    "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
                    "known_difference": (
                        "run267F starts from run267D atrcomp source and changes only source-bar entry signals under "
                        f"{variant.short_id}; model and thresholds remain fixed."
                    ),
                    "runtime_claim_boundary": "research_only_runtime_execution_pending",
                }
            )

            lineage_rows.extend(
                [
                    {
                        "candidate_alias": alias,
                        "source_axis": "atrcomp",
                        "guard_variant": variant.short_id,
                        "artifact_role": "feature_csv",
                        "source_path": feature_meta["source_feature_file"],
                        "run267f_path": feature_meta["feature_file"],
                        "common_path": common_feature_path,
                        "run267f_sha256": feature_meta["feature_sha256"],
                        "common_sha256": common_feature["sha256"],
                    },
                    {
                        "candidate_alias": alias,
                        "source_axis": "atrcomp",
                        "guard_variant": variant.short_id,
                        "artifact_role": "model_csv",
                        "source_path": model_meta["source_model_file"],
                        "run267f_path": model_meta["model_file"],
                        "common_path": common_model_path,
                        "run267f_sha256": model_meta["model_sha256"],
                        "common_sha256": common_model["sha256"],
                    },
                ]
            )

            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{variant.short_id}", "ta"),
                    (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_{variant.short_id}", "rt"),
                ),
                start=1,
            ):
                magic = 26770000 + variant_index * 1000 + candidate_index * 100 + role_index
                payload = attempt_payload(
                    run_root=DESIGN_ROOT,
                    run_id=RUN_ID,
                    stage_number=267,
                    exploration_label=f"stage267_AtrcompGuardRobustness__{variant.short_id}",
                    attempt_name=f"{alias}_{variant.short_id}_{attempt_token}_2024",
                    tier=tier,
                    split=PERIOD_LABEL,
                    model_path=common_model_path,
                    model_id=f"{RUN_ID}_{alias}_{variant.variant_id}_2024",
                    model_backend="ebm_table",
                    feature_path=common_feature_path,
                    feature_count=3,
                    feature_order_hash=str(feature_meta["feature_order_hash"]),
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
                    common_root=f"{COMMON_ROOT}/{variant.short_id}/{alias}",
                    fallback_enabled=False,
                    close_on_flat_signal=spec.variant.close_on_flat_signal,
                    reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                    close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                    extra_set_values=input_probe.base_extra_set_values(spec, magic),
                )
                payload.update(
                    {
                        "candidate_alias": alias,
                        "candidate_role": row.get("candidate_role"),
                        "source_axis": "atrcomp",
                        "guard_variant": variant.short_id,
                        "guard_family": variant.guard_family,
                        "execution_status": "not_executed",
                    }
                )
                attempts.append(payload)

    return design_rows, feature_rows, contract_rows, attempts, lineage_rows, context_info


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def update_ledgers(created_at: str, feature_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    stage_row = {
        "row_id": "stage267_run267F_atrcomp_guard_robustness_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "atrcomp_guard_robustness_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 non-calendar guard attempts planned",
        "scoreboard": "experiment_materialization",
        "status": STATUS,
        "judgment": "materialized_execution_pending_no_candidate_selection",
        "evidence_boundary": "feature_set_ini_materialization_only_no_mt5_kpi_yet_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"feature_variants={len(feature_rows)};attempts={len(attempts)};next_action={NEXT_ACTION}.",
    }
    stage_rows = [row for row in read_csv(STAGE_LEDGER_PATH) if row.get("row_id") != stage_row["row_id"]]
    stage_rows.append(stage_row)
    write_csv(
        STAGE_LEDGER_PATH,
        stage_rows,
        (
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
        ),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_atrcomp_guard_robustness_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267F non-calendar guard variants materialized; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__atrcomp_guard_robustness_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "atrcomp_guard_robustness_materialization",
            "parent_run_id": RUN_ID,
            "record_view": "atrcomp_guard_robustness_materialization",
            "tier_scope": "Tier A and Tier A+B historical 2024 non-calendar guard attempts planned",
            "kpi_scope": "materialization_only",
            "scoreboard_lane": "experiment_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"feature_variants={len(feature_rows)};attempts={len(attempts)}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;mt5_execution=pending",
            "external_verification_status": "out_of_scope_by_claim",
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
    artifact_entries = (
        ("stage267_run267F_guard_robustness_materializer", "producer_script", PRODUCER_PATH, "Builds run267F non-calendar guard variants."),
        ("stage267_run267F_guard_robustness_design", "design_matrix", DESIGN_MATRIX_PATH, "Run267F non-calendar guard design matrix."),
        ("stage267_run267F_guard_robustness_feature_manifest", "feature_manifest", FEATURE_MANIFEST_PATH, "Feature/model/common file manifest for run267F."),
        ("stage267_run267F_guard_robustness_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract for run267F variants."),
        ("stage267_run267F_guard_robustness_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 set/ini attempt manifest for run267F."),
        ("stage267_run267F_guard_robustness_lineage", "artifact_lineage", LINEAGE_PATH, "Feature/model lineage for run267F."),
        ("stage267_run267F_guard_robustness_result", "review_result", RESULT_PATH, "JSON result for run267F materialization."),
        ("stage267_run267F_guard_robustness_report", "review_report", REPORT_PATH, "User-facing run267F materialization report."),
    )
    registry_rows = read_csv(ARTIFACT_REGISTRY_PATH)
    new_rows = []
    for artifact_id, artifact_type, path, notes in artifact_entries:
        new_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    replacements = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacements]
    merged.extend(new_rows)
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs() -> None:
    report_line_current = (
        "- Stage267(267단계) run267F atrcomp guard robustness materialization(ATR 압축 방어 견고성 물질화): "
        f"`{rel(REPORT_PATH)}`"
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_once(
        current,
        "- current_run(현재 실행): `run267E_stage267_adapter_p2_followup_design_v1`",
        f"- current_run(현재 실행): `{RUN_ID}`",
    )
    current = replace_once(
        current,
        "- status(상태): `run267E_atrcomp_monday_guard_mt5_review_completed`",
        f"- status(상태): `{STATUS}`",
    )
    current = append_after(
        current,
        "- Stage267(267단계) run267E atrcomp Monday guard MT5 review(ATR 압축 월요일 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md`",
        report_line_current,
    )
    current = replace_once(
        current,
        "- next_run(다음 실행): `run267F_design_atrcomp_guard_robustness_and_non_calendar_followup`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    current = replace_once(
        current,
        "- action(행동): run267E(267E 실행)에서 atrcomp Monday guard(ATR 압축 월요일 방어) MT5(MetaTrader 5, 메타트레이더5) batch(묶음 실행)와 review(검토)를 완료했다.",
        "- action(행동): run267F(267F 실행)에서 atrcomp(ATR 압축 대체) 기반 비달력 guard(방어) 2종을 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 물질화했다.",
    )
    current = replace_once(
        current,
        "- effect(효과): 순수익/PF(수익 팩터)/DD(drawdown, 손실폭)는 run267D(267D 실행) atrcomp(ATR 압축 대체)보다 좋아졌지만, 거래 수가 줄고 Monday(월요일)와 chron_mid(시간순 중간 구간) 약점이 남아 calendar prune(달력 절단)인지 다시 확인해야 한다.",
        "- effect(효과): run267E(267E 실행)의 Monday guard(월요일 방어) 개선이 calendar prune(달력 절단)에만 기대는지, ADX(추세 강도)와 DI spread(방향성 차이) 같은 비달력 축으로도 재현되는지 MT5(MetaTrader 5, 메타트레이더5) 실행에서 확인할 수 있게 했다.",
    )
    current = replace_once(
        current,
        "- next_action(다음 행동): `run267F_design_atrcomp_guard_robustness_and_non_calendar_followup`. Effect(효과): 월요일 하나를 자르는 미세 조정 루프가 아니라, 비달력 feature(피처) 또는 구조적 Adapter(어댑터) 축으로 같은 개선이 유지되는지 확인한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 20개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해 run267D/run267E(267D/267E 실행)와 비교 가능한 guard comparison(방어 비교)을 만든다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_once(
        selection,
        "- stage_status(단계 상태): `run267E_atrcomp_monday_guard_mt5_review_completed`",
        f"- stage_status(단계 상태): `{STATUS}`",
    )
    selection = replace_once(
        selection,
        "- current_run(현재 실행): `run267E_stage267_adapter_p2_followup_design_v1`",
        f"- current_run(현재 실행): `{RUN_ID}`",
    )
    selection = replace_once(
        selection,
        "- last_completed_run(마지막 완료 실행): `run267D_stage267_adapter_p2_materialization_v1`",
        "- last_completed_run(마지막 완료 실행): `run267E_stage267_adapter_p2_followup_design_v1`",
    )
    selection = append_after(
        selection,
        "- run267E_atrcomp_monday_guard_mt5_review(267E ATR 압축 월요일 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md`",
        f"- run267F_atrcomp_guard_robustness_materialization(267F ATR 압축 방어 견고성 물질화): `{rel(REPORT_PATH)}`",
    )
    selection = replace_once(
        selection,
        "- next_action(다음 행동): `run267F_design_atrcomp_guard_robustness_and_non_calendar_followup`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection = replace_once(
        selection,
        "Run267E(267E 실행)는 atrcomp Monday guard MT5 review(ATR 압축 월요일 방어 MT5 검토)를 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 atrcomp Monday guard(ATR 압축 월요일 방어)의 개선이 calendar prune(달력 절단)에만 기대는지 비달력 feature(피처)와 Adapter(어댑터) 구조로 다시 확인하는 작업이다.",
        "Run267F(267F 실행)는 atrcomp guard robustness materialization(ATR 압축 방어 견고성 물질화)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 ADX(추세 강도)와 DI spread(방향성 차이) guard(방어)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행해 calendar prune(달력 절단) 의존 여부를 확인하는 작업이다.",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_once(
        review,
        "- status(상태): `run267E_atrcomp_monday_guard_mt5_review_completed`",
        f"- status(상태): `{STATUS}`",
    )
    review = replace_once(
        review,
        "- current_run(현재 실행): `run267E_stage267_adapter_p2_followup_design_v1`",
        f"- current_run(현재 실행): `{RUN_ID}`",
    )
    review = replace_once(
        review,
        "- last_completed_run(마지막 완료 실행): `run267D_stage267_adapter_p2_materialization_v1`",
        "- last_completed_run(마지막 완료 실행): `run267E_stage267_adapter_p2_followup_design_v1`",
    )
    review = append_after(
        review,
        "- run267E_atrcomp_monday_guard_mt5_review(267E ATR 압축 월요일 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md`",
        f"- run267F_atrcomp_guard_robustness_materialization(267F ATR 압축 방어 견고성 물질화): `{rel(REPORT_PATH)}`",
    )
    review = replace_once(
        review,
        "Run267E(267E 실행)는 atrcomp Monday guard MT5 review(ATR 압축 월요일 방어 MT5 검토)를 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267F_design_atrcomp_guard_robustness_and_non_calendar_followup`에서 calendar prune(달력 절단) 의존 여부를 다시 확인한다.",
        f"Run267F(267F 실행)는 atrcomp guard robustness materialization(ATR 압축 방어 견고성 물질화)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`에서 비달력 guard(방어)를 실제 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)로 확인한다.",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_once(workspace, "current_run_id: run267E_stage267_adapter_p2_followup_design_v1", f"current_run_id: {RUN_ID}")
    workspace = replace_once(
        workspace,
        "Stage267(267단계) run267E(267E 실행) atrcomp Monday guard MT5 review(ATR 압축 월요일 방어 MT5 검토) `run267E_atrcomp_monday_guard_mt5_review_completed`. Effect(효과): MT5(MetaTrader 5, 메타트레이더5) batch(묶음 실행)와 trade/time-slice review(거래/시간 구간 검토)를 완료했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "Stage267(267단계) run267F(267F 실행) atrcomp guard robustness materialization(ATR 압축 방어 견고성 물질화) `run267F_atrcomp_guard_robustness_materialized_execution_pending`. Effect(효과): ADX(추세 강도)와 DI spread(방향성 차이) 비달력 guard(방어)를 MT5(MetaTrader 5, 메타트레이더5) 실행 가능한 묶음으로 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace = replace_once(
        workspace,
        "Next action(다음 행동)는 `run267F_design_atrcomp_guard_robustness_and_non_calendar_followup`이다. Effect(효과): atrcomp Monday guard(ATR 압축 월요일 방어)의 개선이 calendar prune(달력 절단)인지, 비달력 feature(피처)나 Adapter(어댑터) 구조로도 유지되는지 확인한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): run267F(267F 실행) 20개 attempt(시도)를 실행해 비달력 guard(방어)가 run267E(267E 실행)의 calendar prune(달력 절단) 의심을 줄이는지 확인한다.",
    )
    workspace = replace_once(
        workspace,
        "Stage266(266단계) `266_adapter_research__late_segment_stability_repair_after_stage265_review` was superseded before run execution(실행 전 대체) by the user-directed long R&D racing goal(장기 연구개발 경주 목표), and Stage267(267단계) `267_adapter_research__baseline_candidate_racing_protocol` is active_run267E_atrcomp_monday_guard_mt5_review_completed(267E ATR 압축 월요일 방어 검토 완료 활성). Effect(효과): a single-candidate late-segment repair(단일 후보 후반 구간 수리) no longer drives the next work; the five-candidate research baseline pool(연구 기준 후보군)이 같은 조건에서 비교된다.",
        "Stage266(266단계) `266_adapter_research__late_segment_stability_repair_after_stage265_review` was superseded before run execution(실행 전 대체) by the user-directed long R&D racing goal(장기 연구개발 경주 목표), and Stage267(267단계) `267_adapter_research__baseline_candidate_racing_protocol` is active_run267F_atrcomp_guard_robustness_materialized_execution_pending(267F ATR 압축 방어 견고성 물질화 완료, 실행 대기 활성). Effect(효과): a single-candidate late-segment repair(단일 후보 후반 구간 수리) no longer drives the next work; the five-candidate research baseline pool(연구 기준 후보군)이 같은 조건에서 비교된다.",
    )
    workspace = replace_once(workspace, "  status: run267E_atrcomp_monday_guard_mt5_review_completed", f"  status: {STATUS}")
    workspace = replace_once(workspace, "  current_run_id: run267E_stage267_adapter_p2_followup_design_v1", f"  current_run_id: {RUN_ID}")
    workspace = append_after(
        workspace,
        "  run267E_atrcomp_monday_guard_mt5_review_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md",
        f"  run267F_atrcomp_guard_robustness_report_path: {rel(REPORT_PATH)}",
    )
    workspace = replace_once(workspace, "  next_action: run267F_design_atrcomp_guard_robustness_and_non_calendar_followup", f"  next_action: {NEXT_ACTION}")
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(
    result: Mapping[str, Any],
    design_rows: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
    context_info: Mapping[str, Any],
) -> str:
    lines = [
        "# Stage267 Run267F Atrcomp Guard Robustness Materialization(267단계 267F ATR 압축 방어 견고성 물질화)",
        "",
        "- action(행동): run267D(267D 실행) atrcomp(ATR 압축 대체) feature(피처)를 출발점으로 ADX 20-25(추세 강도 20-25) guard(방어)와 DI-low q33(DI 낮은 33%) guard(방어)를 물질화했다.",
        "- effect(효과): run267E(267E 실행)의 Monday guard(월요일 방어)가 calendar prune(달력 절단)인지, 비달력 market-structure feature(시장 구조 피처)에서도 비슷한 개선을 만들 수 있는지 MT5(MetaTrader 5, 메타트레이더5)로 확인할 수 있다.",
        f"- feature_variants(피처 변형): `{result['feature_variant_count']}`",
        f"- attempts_planned(계획 시도): `{result['attempt_count']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "Stage58(58단계) 이후 연구를 충분히 활용했는가에 대한 답은 아직 `아니다`에 가깝다.",
        "이전 연구는 후보를 만든 재료로는 쓰였지만, 지금 goal(목표)이 요구하는 공통 검증판까지 충분히 펼쳐지진 않았다.",
        "이번 run267F(267F 실행)는 그 부족분 중 하나인 similar replacement(유사 대체)와 calendar-prune check(달력 절단 확인)를 실제 실행 가능한 묶음으로 바꾼 것이다.",
        "",
        "## Materialized Variants(물질화 변형)",
        "",
        "| candidate(후보) | guard(방어) | family(계열) | blocked signals(차단 신호) | retention(유지율) | run267E anchor(267E 기준) |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for row in feature_rows:
        e_row = next(
            (
                item
                for item in design_rows
                if item.get("candidate_alias") == row.get("candidate_alias")
                and item.get("guard_variant") == row.get("guard_variant")
            ),
            {},
        )
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['guard_variant']}` | `{row['guard_family']}` | {csv_value(row.get('blocked_signal_rows'))} | {csv_value(row.get('signal_retention'))} | net_delta={csv_value(e_row.get('run267e_net_delta'))}; PF_delta={csv_value(e_row.get('run267e_pf_delta'))} |"
        )
    lines.extend(
        [
            "",
            "## Experiment Design Receipt(실험 설계 기록)",
            "",
            "- hypothesis(가설): run267E(267E 실행)의 개선이 월요일이라는 calendar(달력) 자체 때문이 아니라 약한 trend-strength(추세 강도) 또는 directional imbalance(방향성 불균형) 구간을 줄인 효과라면, 비달력 guard(방어)에서도 일부 유지되어야 한다.",
            "- decision_use(결정 용도): run267E(267E 실행)를 계속 밀지, calendar prune(달력 절단) 의존으로 낮출지, Adapter(어댑터) 후보 축을 비달력 feature(피처) 쪽으로 다시 설계할지 판단한다.",
            "- comparison_baseline(비교 기준): run267D(267D 실행) atrcomp(ATR 압축 대체)와 run267E(267E 실행) atrcomp Monday guard(ATR 압축 월요일 방어).",
            "- control_variables(고정 변수): model CSV(모델 CSV), threshold(임계값), max_hold_bars(최대 보유 봉), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), 2024 historical window(2024 과거 구간).",
            "- changed_variables(변경 변수): source-bar entry signal(원천 봉 진입 신호)을 ADX 20-25(추세 강도 20-25) 또는 DI-low q33(DI 낮은 33%) 문맥에서만 0으로 바꾼다.",
            "- sample_scope(표본 범위): FPMarkets US100 M5, Tier A(티어 A)와 Tier A+B routed(티어 A+B 라우팅), 2024-01-02부터 2025-01-01 전까지.",
            "- success_criteria(성공 기준): 순수익/PF(수익 팩터)/DD(drawdown, 손실폭)가 run267E(267E 실행)와 비슷하게 방어되면서 trade count(거래 수)가 과하게 무너지지 않고 약한 월/chron_mid(시간순 중간 구간)가 덜 깨진다.",
            "- failure_criteria(실패 기준): 수익이 좋아 보여도 거래 수가 과하게 줄거나, DD(drawdown, 손실폭)와 약한 월이 그대로이거나, DI/ADX(방향성/추세 강도) 한 축에만 과적합된 모양이면 실패 또는 보류로 본다.",
            "- invalid_conditions(무효 조건): MT5(MetaTrader 5, 메타트레이더5) report(보고서) 누락, feature order(피처 순서) 불일치, parser error(파서 오류), set/ini(설정/초기화) 경로 누락.",
            "- stop_conditions(중단 조건): 같은 guard(방어)를 3 stage(단계) 이상 끌지 않는다. 2 stage(단계) 안에 살릴지, 버릴지, 구조 전환할지 닫는다.",
            "- evidence_plan(근거 계획): attempts.csv(시도 목록), MT5 report(보고서), trade_records(거래 기록), time_slice KPI(시간 구간 핵심 성과 지표), curve diagnostics(곡선 진단), guard comparison(방어 비교), ledger/register(장부/등록부).",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(INPUT_DESIGN_PATH)}`, `{rel(INPUT_REVIEW_PATH)}`, `{rel(INPUT_E_REVIEW_PATH)}`, `{rel(INPUT_E_NEGATIVE_SLICE_PATH)}`",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- consumer(소비자): `{NEXT_ACTION}`",
            f"- artifact_paths(산출물 경로): `{rel(DESIGN_MATRIX_PATH)}`, `{rel(FEATURE_MANIFEST_PATH)}`, `{rel(RUNTIME_CONTRACT_PATH)}`, `{rel(ATTEMPT_MANIFEST_PATH)}`, `{rel(LINEAGE_PATH)}`, `{rel(RESULT_PATH)}`",
            "- availability(가용성): repo tracked manifest(저장소 추적 목록) + Common Files(MT5 공용 파일) handoff(인계).",
            "- lineage_judgment(계보 판정): `connected_with_boundary`.",
            "",
            "## Context Edges(문맥 경계값)",
            "",
            f"- atr_14_over_atr_50_q33(ATR 14/50 하위 33%): `{csv_value(context_info.get('atr_14_over_atr_50_q33'))}`",
            f"- historical_vol_20_edges(20봉 과거 변동성 경계): `{csv_value(context_info.get('historical_vol_20_edges'))}`",
            f"- di_spread_14_abs_q33(DI 차이 절대값 하위 33%): `{csv_value(context_info.get('di_spread_14_abs_q33'))}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267F_atrcomp_guard_robustness_materialization`.",
            "- evidence_available(사용 가능 근거): feature/model lineage(피처/모델 계보), runtime contract(런타임 계약), set/ini attempt manifest(설정/초기화 시도 목록).",
            "- evidence_missing(빠진 근거): MT5(MetaTrader 5, 메타트레이더5) execution(실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice review(시간 구간 검토).",
            "- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def materialize() -> dict[str, Any]:
    created_at = utc_now()
    design_rows, feature_rows, contract_rows, attempts, lineage_rows, context_info = build_materialization()
    result = {
        "status": STATUS,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "design_rows": len(design_rows),
        "feature_variant_count": len(feature_rows),
        "contract_rows": len(contract_rows),
        "attempt_count": len(attempts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "design_matrix": rel(DESIGN_MATRIX_PATH),
            "feature_manifest": rel(FEATURE_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        DESIGN_MATRIX_PATH,
        design_rows,
        (
            "candidate_alias",
            "candidate_role",
            "source_axis",
            "guard_variant",
            "guard_variant_id",
            "guard_family",
            "comparison_anchor",
            "run267d_net_profit",
            "run267d_profit_factor",
            "run267d_trade_count",
            "run267d_equity_dd_percent",
            "run267e_net_delta",
            "run267e_pf_delta",
            "run267e_trade_delta",
            "run267e_dd_delta",
            "weakest_month_after_run267e",
            "weakest_month_net_after_run267e",
            "blocked_signal_rows",
            "kept_signal_rows",
            "signal_retention",
            "common_feature_path",
            "common_model_path",
            "design_read",
            "next_validation",
            "claim_boundary",
        ),
    )
    write_csv(
        FEATURE_MANIFEST_PATH,
        feature_rows,
        (
            "candidate_alias",
            "candidate_role",
            "source_axis",
            "guard_variant",
            "guard_variant_id",
            "guard_family",
            "comparison_anchor",
            "materialization_rule",
            "intent",
            "source_feature_file",
            "feature_file",
            "feature_sha256",
            "source_model_file",
            "model_file",
            "model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_order",
            "feature_order_hash",
            "rows",
            "total_signal_rows",
            "matched_rows",
            "blocked_signal_rows",
            "blocked_long_signal_rows",
            "blocked_short_signal_rows",
            "kept_signal_rows",
            "signal_retention",
            "context_missing_rows",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        contract_rows,
        (
            "candidate_alias",
            "source_axis",
            "guard_variant",
            "shared_contract",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "model_backend",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        build_attempt_rows(attempts),
        (
            "candidate_alias",
            "candidate_role",
            "source_axis",
            "guard_variant",
            "guard_family",
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
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "inputs": {
                "run267d_design": rel(INPUT_DESIGN_PATH),
                "run267d_review": rel(INPUT_REVIEW_PATH),
                "run267e_guard_comparison": rel(INPUT_E_REVIEW_PATH),
                "run267e_negative_slices": rel(INPUT_E_NEGATIVE_SLICE_PATH),
            },
            "context_info": context_info,
            "lineage": lineage_rows,
        },
    )
    write_json(RESULT_PATH, result | {"lineage_rows": len(lineage_rows), "context_info": context_info})
    write_md(REPORT_PATH, report_markdown(result, design_rows, feature_rows, context_info))
    update_current_truth_docs()
    update_ledgers(created_at, feature_rows, attempts)
    return result


def main() -> int:
    result = materialize()
    print(
        json.dumps(
            {
                "status": result["status"],
                "feature_variant_count": result["feature_variant_count"],
                "attempt_count": result["attempt_count"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
