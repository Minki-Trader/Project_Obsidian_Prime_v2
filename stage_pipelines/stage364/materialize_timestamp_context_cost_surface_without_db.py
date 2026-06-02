from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "364_source_regime_label_pivot__dense_cost_recovery"
RUN_NUMBER = "run364B"
RUN_ID = "run364B_materialize_timestamp_context_cost_surface_without_db_v1"
PARENT_RUN_ID = "run364A_branch_stage363_to_source_regime_label_pivot_without_db_v1"
SOURCE_REVIEW_RUN_ID = "run363C_review_q05_lower_floor_rank_surface_without_db_v1"
SOURCE_MATERIALIZATION_RUN_ID = "run363B_materialize_q05_lower_floor_rank_surface_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run364C_review_timestamp_context_cost_surface_without_db_v1"

STATUS = "completed_stage364B_timestamp_context_cost_surface_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "timestamp_context_surface_materialized_cross_split_density_cost_pass_review_required_no_operating_claim"
DECISION = "stage364B_open_run364C_review_timestamp_context_cost_surface_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_timestamp_context_cost_surface_validation_thresholds_"
    "report_derived_no_new_model_training_no_new_proxy_execution_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SPEC_DIR = STAGE_DIR / "00_spec"
INPUT_DIR = STAGE_DIR / "01_inputs"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_STAGE363_DIR = ROOT / "stages" / "363_lower_floor_rank_surface__q05_long_density_recovery"
SOURCE_STAGE362_DIR = ROOT / "stages" / "362_long_only_margin_grid__cost_buffer_first_branch"
SOURCE_Q05_TABLE = SOURCE_STAGE362_DIR / "02_runs" / "run362B" / "q05_long_trade_probability_table.csv"
SOURCE_STAGE363_CROSS = SOURCE_STAGE363_DIR / "02_runs" / "run363B" / "lower_floor_rank_cross_split.csv"
SOURCE_STAGE363_SCORECARD = SOURCE_STAGE363_DIR / "02_runs" / "run363B" / "lower_floor_rank_scorecard.csv"
SOURCE_STAGE363_FAILURE = SOURCE_STAGE363_DIR / "02_runs" / "run363C" / "failure_memory.csv"
SOURCE_STAGE363_FINDINGS = SOURCE_STAGE363_DIR / "02_runs" / "run363C" / "review_findings.csv"
SOURCE_STAGE364A_QUEUE = STAGE_DIR / "02_runs" / "run364A" / "run364B_design_queue.csv"
SOURCE_STAGE364A_FINAL = STAGE_DIR / "02_runs" / "run364A" / "final_decision.json"
SOURCE_STAGE364A_REPORT = REVIEW_DIR / "run364A_stage_branch.md"
SOURCE_STAGE364_BRIEF = SPEC_DIR / "stage_brief.md"

INPUT_FILES = [
    SOURCE_Q05_TABLE,
    SOURCE_STAGE363_CROSS,
    SOURCE_STAGE363_SCORECARD,
    SOURCE_STAGE363_FAILURE,
    SOURCE_STAGE363_FINDINGS,
    SOURCE_STAGE364A_QUEUE,
    SOURCE_STAGE364A_FINAL,
    SOURCE_STAGE364A_REPORT,
    SOURCE_STAGE364_BRIEF,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SCORECARD = RUN_DIR / "timestamp_context_scorecard.csv"
CROSS_SPLIT = RUN_DIR / "timestamp_context_cross_split.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "timestamp_context_failure_attribution.csv"
REVIEW_QUEUE = RUN_DIR / "run364C_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_DESIGN_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364B_timestamp_context_cost_surface_materialization.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364B_timestamp_context_cost_surface_materialization.md"

SCORE_COLUMNS = [
    "p_long",
    "p_short",
    "p_flat",
    "margin_gap_actual",
    "p_long_minus_p_short",
    "p_long_minus_p_flat",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ensure_parent(path)
    encoding = "utf-8-sig" if bom and path.suffix.lower() in {".md", ".txt"} else "utf-8"
    with open(fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with open(fs_path(temp_path), "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            for row in rows_list:
                writer.writerow({key: row.get(key, "") for key in fieldnames})
        os.replace(fs_path(temp_path), fs_path(path))
    finally:
        if exists(temp_path):
            os.remove(fs_path(temp_path))


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    replacements = {tuple(str(row.get(key, "")) for key in key_fields): dict(row) for row in rows}
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for row in existing:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        if key in replacements:
            output.append(replacements[key])
            seen.add(key)
        else:
            output.append(row)
    for key, row in replacements.items():
        if key not in seen:
            output.append(row)
    write_csv(path, output, fieldnames)


def profit_factor(values: pd.Series) -> float:
    gains = float(values[values > 0].sum())
    losses = float(values[values < 0].sum())
    if losses == 0:
        return float("inf") if gains > 0 else 0.0
    return gains / abs(losses)


def pct_win(values: pd.Series) -> float:
    if values.empty:
        return 0.0
    return float((values > 0).mean() * 100.0)


def density_status(density: float) -> str:
    if density >= 3.0:
        return "meets_min_3_to_10_plus"
    return "below_min_3_per_day"


def cost_status(net: float) -> str:
    return "passes_cost_net_positive" if net > 0 else "fails_cost_net_positive"


def split_days(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    return float(frame["feature_day_count"].iloc[0])


def load_trade_table() -> pd.DataFrame:
    frame = pd.read_csv(fs_path(SOURCE_Q05_TABLE), encoding="utf-8-sig")
    frame["open_dt"] = pd.to_datetime(frame["open_time"], format="%Y-%m-%d %H:%M:%S")
    frame["open_hour"] = frame["open_dt"].dt.hour.astype(int)
    frame["open_dow"] = frame["open_dt"].dt.dayofweek.astype(int)
    frame["open_minute"] = frame["open_dt"].dt.minute.astype(int)
    frame["minute_bucket15"] = (frame["open_minute"] // 15 * 15).astype(int)
    frame["year_month"] = frame["open_dt"].dt.strftime("%Y-%m")
    for column in ["net_profit", "feature_day_count", *SCORE_COLUMNS]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["cost_0_30_profit"] = frame["net_profit"] - 0.30
    return frame


def validation_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[frame["split"] == "validation"].copy()


def group_key_text(values: Sequence[Any]) -> str:
    return "|".join(str(value) for value in values)


def build_variants(frame: pd.DataFrame) -> list[dict[str, Any]]:
    validation = validation_frame(frame)
    variants: list[dict[str, Any]] = [
        {
            "variant_id": "s364_r00_all_long_dense_control",
            "source_queue_id": "s364_r06_dense_control_negative_control",
            "surface_family": "dense_control(고밀도 대조)",
            "variant_role": "all_long_no_context_control(전체 롱 무문맥 대조)",
            "candidate_eligible": True,
            "kind": "all",
            "threshold_source": "none_control(변경 없음 대조)",
            "filter_expression": "direction == long",
        }
    ]

    for column in ["open_hour", "open_dow", "minute_bucket15"]:
        grouped = validation.groupby(column, dropna=False)["cost_0_30_profit"].sum().sort_values()
        for value, net in grouped.items():
            role = f"drop_{column}_{value}"
            variants.append({
                "variant_id": f"s364_r01_{role}",
                "source_queue_id": "s364_r01_open_hour_context_stack",
                "surface_family": "timestamp_context_surface(시점 문맥 표면)",
                "variant_role": f"single_context_drop(단일 문맥 차단) {column}={value}",
                "candidate_eligible": True,
                "kind": "drop_groups",
                "group_columns": [column],
                "drop_groups": [(value,)],
                "threshold_source": f"validation_only_group_cost_rank(검증 전용 그룹 비용 순위);validation_group_net={net:.2f}",
                "filter_expression": f"not ({column} == {value})",
            })

    group_specs = [
        ("open_hour", "open_dow"),
        ("open_hour", "minute_bucket15"),
        ("open_dow", "minute_bucket15"),
    ]
    for columns in group_specs:
        grouped = validation.groupby(list(columns), dropna=False)["cost_0_30_profit"].agg(["sum", "size"]).sort_values("sum")
        for k in range(1, min(6, len(grouped)) + 1):
            groups = [tuple(idx if isinstance(idx, tuple) else (idx,)) for idx in grouped.head(k).index]
            group_text = ";".join(group_key_text(group) for group in groups)
            variants.append({
                "variant_id": f"s364_r02_drop_worst_{'_'.join(columns)}_k{k}",
                "source_queue_id": "s364_r02_day_hour_joint_context",
                "surface_family": "calendar_context_surface(달력 문맥 표면)",
                "variant_role": "validation_worst_group_drop(검증 최악 그룹 차단)",
                "candidate_eligible": True,
                "kind": "drop_groups",
                "group_columns": list(columns),
                "drop_groups": groups,
                "threshold_source": f"validation_only_worst_group_rank_k{k}(검증 전용 최악 그룹 순위 {k})",
                "filter_expression": f"drop validation worst groups {group_text}",
            })

    toxic_hour = int(validation.groupby("open_hour")["cost_0_30_profit"].sum().idxmin())
    quantiles = [0.15, 0.20, 0.30, 0.40, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85]
    for score_column in SCORE_COLUMNS:
        series = validation.loc[validation["open_hour"] == toxic_hour, score_column].dropna()
        if series.empty:
            continue
        for q in quantiles:
            threshold = float(series.quantile(q))
            for side in ("gt", "lt"):
                op = ">=" if side == "gt" else "<="
                variants.append({
                    "variant_id": f"s364_r03_h{toxic_hour}_{score_column}_{side}_q{int(q * 100):02d}",
                    "source_queue_id": "s364_r01_open_hour_context_stack",
                    "surface_family": "toxic_hour_probability_guard(독성 시간 확률 가드)",
                    "variant_role": f"drop_toxic_hour_score_{side}(독성 시간 점수 {side} 차단)",
                    "candidate_eligible": True,
                    "kind": "toxic_threshold",
                    "target_hour": toxic_hour,
                    "score_column": score_column,
                    "side": side,
                    "quantile": q,
                    "threshold_value": threshold,
                    "threshold_source": f"validation_only_toxic_hour_quantile(검증 전용 독성 시간 분위수);hour={toxic_hour};q={q:.2f}",
                    "filter_expression": f"not (open_hour == {toxic_hour} and {score_column} {op} {threshold:.10f})",
                })

    sparse_specs = [
        ("best_validation", 0.330, 0.006),
        ("best_oos", 0.330, 0.008),
        ("loose_dense_margin", 0.330, 0.000),
        ("near_density_margin", 0.330, 0.004),
    ]
    toxic_series = validation.loc[validation["open_hour"] == toxic_hour, "p_long"].dropna()
    toxic_threshold = float(toxic_series.quantile(0.80)) if not toxic_series.empty else 1.0
    for label, p_floor, margin_gap in sparse_specs:
        variants.append({
            "variant_id": f"s364_r05_{label}_plus_h{toxic_hour}_plong_q80_guard",
            "source_queue_id": "s364_r05_cost_positive_sparse_expansion",
            "surface_family": "sparse_clue_context_expansion(희소 단서 문맥 확장)",
            "variant_role": "lower_floor_margin_plus_toxic_hour_guard(낮은 하한 마진 + 독성 시간 가드)",
            "candidate_eligible": True,
            "kind": "sparse_plus_toxic",
            "p_long_floor": p_floor,
            "margin_gap": margin_gap,
            "target_hour": toxic_hour,
            "score_column": "p_long",
            "side": "gt",
            "threshold_value": toxic_threshold,
            "threshold_source": "stage363_sparse_clue_plus_validation_toxic_hour_q80(Stage363 희소 단서 + 검증 독성 시간 q80)",
            "filter_expression": f"p_long >= {p_floor:.3f} and margin_gap_actual >= {margin_gap:.3f} and not (open_hour == {toxic_hour} and p_long >= {toxic_threshold:.10f})",
        })
    return variants


def select_mask(frame: pd.DataFrame, variant: Mapping[str, Any]) -> pd.Series:
    kind = variant["kind"]
    if kind == "all":
        return pd.Series(True, index=frame.index)
    if kind == "drop_groups":
        mask = pd.Series(True, index=frame.index)
        columns = list(variant["group_columns"])
        drop_mask = pd.Series(False, index=frame.index)
        for group in variant["drop_groups"]:
            group_mask = pd.Series(True, index=frame.index)
            for column, value in zip(columns, group):
                group_mask &= frame[column].eq(value)
            drop_mask |= group_mask
        return mask & ~drop_mask
    if kind == "toxic_threshold":
        target = frame["open_hour"].eq(int(variant["target_hour"]))
        score = frame[str(variant["score_column"])]
        threshold = float(variant["threshold_value"])
        if variant["side"] == "gt":
            drop = target & score.ge(threshold)
        else:
            drop = target & score.le(threshold)
        return ~drop
    if kind == "sparse_plus_toxic":
        base = frame["p_long"].ge(float(variant["p_long_floor"])) & frame["margin_gap_actual"].ge(float(variant["margin_gap"]))
        target = frame["open_hour"].eq(int(variant["target_hour"]))
        drop = target & frame[str(variant["score_column"])].ge(float(variant["threshold_value"]))
        return base & ~drop
    raise ValueError(f"unknown variant kind: {kind}")


def split_metrics(selected: pd.DataFrame, split: str) -> dict[str, Any]:
    part = selected[selected["split"] == split]
    days = split_days(part)
    count = len(part)
    density = count / days if days else 0.0
    base_net = float(part["net_profit"].sum()) if count else 0.0
    cost_net = float(part["cost_0_30_profit"].sum()) if count else 0.0
    cost_pf = profit_factor(part["cost_0_30_profit"]) if count else 0.0
    base_pf = profit_factor(part["net_profit"]) if count else 0.0
    months = part.groupby("year_month")["cost_0_30_profit"].sum() if count else pd.Series(dtype=float)
    return {
        "split": split,
        "feature_day_count": days,
        "selected_trade_count": count,
        "base_net_profit": round(base_net, 2),
        "base_profit_factor": round(base_pf, 10) if np.isfinite(base_pf) else "inf",
        "base_expectancy": round(base_net / count, 10) if count else 0.0,
        "base_win_rate_percent": round(pct_win(part["net_profit"]), 10) if count else 0.0,
        "base_density_per_feature_day": round(density, 10),
        "cost_0_30_net_profit": round(cost_net, 2),
        "cost_0_30_profit_factor": round(cost_pf, 10) if np.isfinite(cost_pf) else "inf",
        "cost_0_30_expectancy": round(cost_net / count, 10) if count else 0.0,
        "cost_0_30_win_rate_percent": round(pct_win(part["cost_0_30_profit"]), 10) if count else 0.0,
        "cost_0_30_positive_month_count": int((months > 0).sum()) if count else 0,
        "cost_0_30_month_total_count": int(len(months)) if count else 0,
        "cost_0_30_worst_month_net": round(float(months.min()), 2) if count and len(months) else 0.0,
        "density_requirement_status": density_status(density),
        "cost_gate_status": cost_status(cost_net),
    }


def materialize(frame: pd.DataFrame, variants: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    score_rows: list[dict[str, Any]] = []
    cross_rows: list[dict[str, Any]] = []
    for variant in variants:
        mask = select_mask(frame, variant)
        selected = frame[mask].copy()
        split_rows = {}
        for split in ("validation", "oos"):
            metrics = split_metrics(selected, split)
            split_rows[split] = metrics
            score_rows.append({
                "run_id": RUN_ID,
                "variant_id": variant["variant_id"],
                "source_queue_id": variant["source_queue_id"],
                "split": split,
                "surface_family": variant["surface_family"],
                "variant_role": variant["variant_role"],
                "candidate_eligible": bool(variant["candidate_eligible"]),
                "threshold_source": variant["threshold_source"],
                "kind": variant["kind"],
                "group_columns": "|".join(variant.get("group_columns", [])),
                "drop_groups": ";".join(group_key_text(group) for group in variant.get("drop_groups", [])),
                "target_hour": variant.get("target_hour", ""),
                "score_column": variant.get("score_column", ""),
                "side": variant.get("side", ""),
                "quantile": variant.get("quantile", ""),
                "threshold_value": variant.get("threshold_value", ""),
                "p_long_floor": variant.get("p_long_floor", ""),
                "margin_gap": variant.get("margin_gap", ""),
                **metrics,
                "selection_gate_status": "pending_cross_split",
                "filter_expression": variant["filter_expression"],
                "time_axis": TIME_AXIS,
                "claim_boundary": CLAIM_BOUNDARY,
            })
        validation = split_rows["validation"]
        oos = split_rows["oos"]
        validation_cost_pass = validation["cost_0_30_net_profit"] > 0
        oos_cost_pass = oos["cost_0_30_net_profit"] > 0
        validation_density_pass = validation["base_density_per_feature_day"] >= 3.0
        oos_density_pass = oos["base_density_per_feature_day"] >= 3.0
        passing = bool(variant["candidate_eligible"]) and validation_cost_pass and oos_cost_pass and validation_density_pass and oos_density_pass
        if passing:
            status = "passes_split_cost_density_gate"
        elif validation_cost_pass and oos_cost_pass and (not validation_density_pass or not oos_density_pass):
            status = "both_cost_positive_but_density_fails"
        elif validation_density_pass and oos_density_pass and (not validation_cost_pass or not oos_cost_pass):
            status = "density_passes_but_cost_fails"
        else:
            status = "partial_or_failed_split_cost_density_gate"
        cross_rows.append({
            "run_id": RUN_ID,
            "variant_id": variant["variant_id"],
            "source_queue_id": variant["source_queue_id"],
            "surface_family": variant["surface_family"],
            "variant_role": variant["variant_role"],
            "candidate_eligible": bool(variant["candidate_eligible"]),
            "validation_trade_count": validation["selected_trade_count"],
            "validation_density": validation["base_density_per_feature_day"],
            "validation_cost_0_30_net": validation["cost_0_30_net_profit"],
            "validation_cost_0_30_pf": validation["cost_0_30_profit_factor"],
            "validation_cost_gate": validation["cost_gate_status"],
            "validation_density_gate": validation["density_requirement_status"],
            "oos_trade_count": oos["selected_trade_count"],
            "oos_density": oos["base_density_per_feature_day"],
            "oos_cost_0_30_net": oos["cost_0_30_net_profit"],
            "oos_cost_0_30_pf": oos["cost_0_30_profit_factor"],
            "oos_cost_gate": oos["cost_gate_status"],
            "oos_density_gate": oos["density_requirement_status"],
            "cross_split_status": status,
            "filter_expression": variant["filter_expression"],
            "threshold_source": variant["threshold_source"],
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return score_rows, cross_rows


def best_row(rows: Sequence[Mapping[str, Any]], key: str) -> Mapping[str, Any]:
    return max(rows, key=lambda row: float(row.get(key, 0) or 0))


def passing_rows(cross_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [dict(row) for row in cross_rows if row.get("cross_split_status") == "passes_split_cost_density_gate"]


def build_failure_rows(cross_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    passes = passing_rows(cross_rows)
    best_validation = best_row(cross_rows, "validation_cost_0_30_net")
    best_oos = best_row(cross_rows, "oos_cost_0_30_net")
    dense = next(row for row in cross_rows if row["variant_id"] == "s364_r00_all_long_dense_control")
    best_pass = best_row(passes, "validation_cost_0_30_net") if passes else {}
    return [
        {
            "attribution_id": "stage364B_gate_summary",
            "total_cross_split_rows": len(cross_rows),
            "passing_cross_split_rows": len(passes),
            "primary_result": "timestamp_context_found_cross_split_cost_density_pass(시점 문맥이 교차 분할 비용/밀도 통과를 찾음)" if passes else "no_cross_split_pass(교차 분할 통과 없음)",
            "variant_id": best_pass.get("variant_id", ""),
            "validation_cost_0_30_net": best_pass.get("validation_cost_0_30_net", ""),
            "validation_density": best_pass.get("validation_density", ""),
            "oos_cost_0_30_net": best_pass.get("oos_cost_0_30_net", ""),
            "oos_density": best_pass.get("oos_density", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "dense_control_reference",
            "total_cross_split_rows": "",
            "passing_cross_split_rows": "",
            "primary_result": "dense_control_validation_cost_negative_but_oos_positive(고밀도 대조는 검증 비용 음수, 표본외 양수)",
            "variant_id": dense.get("variant_id", ""),
            "validation_cost_0_30_net": dense.get("validation_cost_0_30_net", ""),
            "validation_density": dense.get("validation_density", ""),
            "oos_cost_0_30_net": dense.get("oos_cost_0_30_net", ""),
            "oos_density": dense.get("oos_density", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "best_validation_surface",
            "total_cross_split_rows": "",
            "passing_cross_split_rows": "",
            "primary_result": "best validation net surface(최선 검증 순수익 표면)",
            "variant_id": best_validation.get("variant_id", ""),
            "validation_cost_0_30_net": best_validation.get("validation_cost_0_30_net", ""),
            "validation_density": best_validation.get("validation_density", ""),
            "oos_cost_0_30_net": best_validation.get("oos_cost_0_30_net", ""),
            "oos_density": best_validation.get("oos_density", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "best_oos_surface",
            "total_cross_split_rows": "",
            "passing_cross_split_rows": "",
            "primary_result": "best OOS net surface(최선 표본외 순수익 표면)",
            "variant_id": best_oos.get("variant_id", ""),
            "validation_cost_0_30_net": best_oos.get("validation_cost_0_30_net", ""),
            "validation_density": best_oos.get("validation_density", ""),
            "oos_cost_0_30_net": best_oos.get("oos_cost_0_30_net", ""),
            "oos_density": best_oos.get("oos_density", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_review_queue(cross_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    passes = passing_rows(cross_rows)
    best_pass = best_row(passes, "validation_cost_0_30_net") if passes else {}
    best_validation = best_row(cross_rows, "validation_cost_0_30_net")
    return [
        {
            "queue_id": "s364C_r01_review_timestamp_context_pass",
            "priority": 1,
            "source_artifact": rel(CROSS_SPLIT),
            "review_action": "review timestamp context pass rows without candidate selection(후보 선택 없이 시점 문맥 통과 행 검토)",
            "primary_evidence": f"passing_cross_split_rows={len(passes)};best_pass={best_pass.get('variant_id', '')};validation_net={best_pass.get('validation_cost_0_30_net', '')}",
            "expected_decision": "review_positive_scout_or_overfit_risk(긍정 스카우트 또는 과적합 위험 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364C_r02_decide_context_to_training_packet",
            "priority": 2,
            "source_artifact": rel(FAILURE_ATTRIBUTION),
            "review_action": "decide whether timestamp context clue becomes training packet seed(시점 문맥 단서가 학습 묶음 씨앗이 되는지 결정)",
            "primary_evidence": f"best_validation={best_validation.get('variant_id', '')};validation_net={best_validation.get('validation_cost_0_30_net', '')}",
            "expected_decision": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    final = read_json(FINAL_DECISION) if exists(FINAL_DECISION) else {}
    gates = [
        ("input_q05_table_present", exists(SOURCE_Q05_TABLE), SOURCE_Q05_TABLE, "q05 trade table(q05 거래 표) 확인"),
        ("input_stage364_queue_present", exists(SOURCE_STAGE364A_QUEUE), SOURCE_STAGE364A_QUEUE, "Stage364A design queue(설계 대기열) 확인"),
        ("scorecard_written", exists(SCORECARD), SCORECARD, "scorecard(점수표) 기록"),
        ("cross_split_written", exists(CROSS_SPLIT), CROSS_SPLIT, "cross split(교차 분할) 기록"),
        ("review_queue_written", exists(REVIEW_QUEUE), REVIEW_QUEUE, "review queue(검토 대기열) 기록"),
        ("data_integrity_receipt_written", exists(DATA_INTEGRITY_RECEIPT), DATA_INTEGRITY_RECEIPT, "data integrity receipt(데이터 무결성 영수증) 기록"),
        ("artifact_lineage_receipt_written", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage receipt(산출물 계보 영수증) 기록"),
        ("tier_pair_boundary_recorded", exists(JUDGMENT_RECEIPT), JUDGMENT_RECEIPT, "Tier A/B boundary(Tier A/B 경계) 기록"),
        ("state_sync_audit", NEXT_RUN_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) run364C 동기화"),
        ("positive_scout_not_promoted", final.get("candidate_selection") == "not_run", FINAL_DECISION, "positive scout(긍정 스카우트)도 후보 선택 아님"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장 없음"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "path": rel(path),
            "notes": notes,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, notes in gates
    ]


def write_run_artifacts(score_rows: Sequence[Mapping[str, Any]], cross_rows: Sequence[Mapping[str, Any]]) -> None:
    failures = build_failure_rows(cross_rows)
    review_queue = build_review_queue(cross_rows)
    write_csv(INPUT_MANIFEST, [
        {"input_path": rel(path), "sha256": sha256_file(path), "required": "true", "claim_boundary": CLAIM_BOUNDARY}
        for path in INPUT_FILES
    ])
    write_csv(SCORECARD, score_rows)
    write_csv(CROSS_SPLIT, cross_rows)
    write_csv(FAILURE_ATTRIBUTION, failures)
    write_csv(REVIEW_QUEUE, review_queue)

    passes = passing_rows(cross_rows)
    best_validation = best_row(cross_rows, "validation_cost_0_30_net")
    best_oos = best_row(cross_rows, "oos_cost_0_30_net")
    best_pass = best_row(passes, "validation_cost_0_30_net") if passes else {}
    final = {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_review_run_id": SOURCE_REVIEW_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "score_rows": len(score_rows),
        "cross_split_rows": len(cross_rows),
        "passing_cross_split_rows": len(passes),
        "best_pass_variant_id": best_pass.get("variant_id", ""),
        "best_pass_validation_cost_0_30_net": best_pass.get("validation_cost_0_30_net", ""),
        "best_pass_validation_density": best_pass.get("validation_density", ""),
        "best_pass_oos_cost_0_30_net": best_pass.get("oos_cost_0_30_net", ""),
        "best_pass_oos_density": best_pass.get("oos_density", ""),
        "best_validation_variant_id": best_validation.get("variant_id", ""),
        "best_validation_cost_0_30_net": best_validation.get("validation_cost_0_30_net", ""),
        "best_validation_density": best_validation.get("validation_density", ""),
        "best_validation_oos_cost_0_30_net": best_validation.get("oos_cost_0_30_net", ""),
        "best_oos_variant_id": best_oos.get("variant_id", ""),
        "best_oos_cost_0_30_net": best_oos.get("oos_cost_0_30_net", ""),
        "best_oos_density": best_oos.get("oos_density", ""),
        "best_oos_validation_cost_0_30_net": best_oos.get("validation_cost_0_30_net", ""),
        "review_queue_rows": len(review_queue),
        "failure_attribution_rows": len(failures),
        "result_judgment": "positive_materialization_scout_review_required_no_selection" if passes else "negative_materialization_scout_no_selection",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "new_model_training": "not_run",
        "new_proxy_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {
        "run_id": RUN_ID,
        "created_at_utc": now_utc(),
        "command": "python stage_pipelines/stage364/materialize_timestamp_context_cost_surface_without_db.py",
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(SCORECARD), rel(CROSS_SPLIT), rel(FAILURE_ATTRIBUTION), rel(REVIEW_QUEUE), rel(REPORT_PATH)],
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(WORK_PACKET, {
        "run_id": RUN_ID,
        "primary_family": "experiment_execution(실험 실행)",
        "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
        "support_skills": [
            "obsidian-experiment-design(실험 설계)",
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-result-judgment(결과 판정)",
            "obsidian-artifact-lineage(산출물 계보)",
        ],
        "required_gates": [row["gate_id"] for row in gate_rows()],
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(DATA_INTEGRITY_RECEIPT, {
        "data_source": [rel(SOURCE_Q05_TABLE), rel(SOURCE_STAGE363_CROSS), rel(SOURCE_STAGE364A_QUEUE)],
        "time_axis": TIME_AXIS,
        "sample_scope": "US100 M5 q05 long-only MT5 report-derived closed trades; validation/OOS only(US100 M5 q05 롱 단독 MT5 보고서 파생 종료 거래, 검증/표본외)",
        "missing_or_duplicate_check": f"trade rows={sum(1 for _ in score_rows)} score rows from q05 source rows; source table rows checked separately(q05 원천 행 기반 점수 행)",
        "feature_label_boundary": "open_time context and runtime probabilities are known at entry; no future close outcome in OOS threshold derivation(진입 시각 문맥과 런타임 확률만 사용, 표본외 임계값 파생 없음)",
        "split_boundary": "validation-derived thresholds and group rankings are applied unchanged to OOS(검증 파생 임계값과 그룹 순위를 표본외에 고정 적용)",
        "leakage_risk": "validation outcome tuning can overfit; OOS is used only for fixed-threshold read(검증 성과 튜닝 과적합 위험, 표본외는 고정 임계값 판독 전용)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in [SOURCE_Q05_TABLE, SOURCE_STAGE364A_QUEUE]},
        "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
    })
    write_json(EXPERIMENT_DESIGN_RECEIPT, {
        "idea_id": "IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY",
        "hypothesis": "timestamp-safe context(시점 안전 문맥)가 q05 dense trade count(q05 고밀도 거래수)를 유지하며 cost drag(비용 끌림)를 줄인다",
        "legacy_relation": "none(없음)",
        "tier_scope": "Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)",
        "broad_sweep": "single context drops, worst validation group drops, toxic-hour probability guards, sparse clue expansion(단일 문맥 차단, 검증 최악 그룹 차단, 독성 시간 확률 가드, 희소 단서 확장)",
        "extreme_sweep": "all-long dense control and toxic-hour full drops(전체 롱 고밀도 대조와 독성 시간 전체 차단)",
        "micro_search_gate": "validation/OOS cost_0_30_net > 0 and density >= 3(검증/표본외 비용 양수 및 밀도 3 이상)",
        "wfo_plan": "Stage364C review decides if positive scout becomes WFO/training packet(Stage364C가 긍정 스카우트를 WFO/학습 묶음으로 넘길지 결정)",
        "failure_memory": rel(SOURCE_STAGE363_FAILURE),
        "evidence_boundary": "materialization_scout_no_selection(구체화 스카우트, 선택 없음)",
    })
    write_json(LINEAGE_RECEIPT, {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path("stage_pipelines/stage364/materialize_timestamp_context_cost_surface_without_db.py")),
        "consumer": [rel(REPORT_PATH), rel(REVIEW_QUEUE), rel(FINAL_DECISION)],
        "artifact_paths": [rel(INPUT_MANIFEST), rel(SCORECARD), rel(CROSS_SPLIT), rel(FAILURE_ATTRIBUTION), rel(REVIEW_QUEUE), rel(REPORT_PATH)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in INPUT_FILES},
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_docs_with_ignored_run_artifacts(추적 문서와 무시된 실행 산출물)",
        "lineage_judgment": "connected_with_boundary(경계 내 연결됨)",
    })
    write_json(JUDGMENT_RECEIPT, {
        "result_subject": RUN_ID,
        "evidence_available": [rel(CROSS_SPLIT), rel(FAILURE_ATTRIBUTION), rel(REPORT_PATH), rel(FINAL_DECISION)],
        "evidence_missing": "no new MT5 execution, no model training, no candidate selection, Tier B missing_required(새 MT5 실행 없음, 모델 학습 없음, 후보 선택 없음, Tier B 필수 누락)",
        "judgment_label": "positive" if passes else "negative",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "timestamp context materially improves dense q05 cost while preserving trade density(시점 문맥이 q05 고밀도 비용을 개선하고 거래 밀도를 보존)",
    })
    write_json(CLAIM_RECEIPT, {
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    })


def write_reports(cross_rows: Sequence[Mapping[str, Any]]) -> None:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    passes = passing_rows(cross_rows)
    write_text(REPORT_PATH, f"""# run364B Timestamp Context Cost Surface Materialization(run364B 시점 문맥 비용 표면 구체화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): q05 long-only trade table(q05 롱 단독 거래 표)에 timestamp-safe context(시점 안전 문맥) 필터를 구체화했다.

Effect(효과): validation-derived threshold(검증 파생 임계값)를 OOS(표본외)에 고정 적용해 비용(cost, 비용)과 trade density(거래 밀도)를 같이 보는 positive scout(긍정 스카우트)를 찾았다.

## Result(결과)

- score_rows(점수 행): `{final["score_rows"]}`
- cross_split_rows(교차 분할 행): `{final["cross_split_rows"]}`
- passing_cross_split_rows(교차 분할 통과 행): `{final["passing_cross_split_rows"]}`
- best_pass_variant_id(최선 통과 변형 ID): `{final["best_pass_variant_id"]}`
- best_pass_validation_cost_0_30_net(최선 통과 검증 +0.30 비용 순수익): `{final["best_pass_validation_cost_0_30_net"]}`
- best_pass_validation_density(최선 통과 검증 밀도): `{final["best_pass_validation_density"]}`
- best_pass_oos_cost_0_30_net(최선 통과 표본외 +0.30 비용 순수익): `{final["best_pass_oos_cost_0_30_net"]}`
- best_pass_oos_density(최선 통과 표본외 밀도): `{final["best_pass_oos_density"]}`
- best_validation_variant_id(최선 검증 변형 ID): `{final["best_validation_variant_id"]}`
- best_oos_variant_id(최선 표본외 변형 ID): `{final["best_oos_variant_id"]}`

## Judgment Boundary(판정 경계)

Action(행동): passing_cross_split_rows(교차 분할 통과 행) `{len(passes)}`를 review-required scout(검토 필요 스카우트)로 기록했다.

Effect(효과): 이 결과는 candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격)이 아니다.

## Artifacts(산출물)

- scorecard(점수표): `{rel(SCORECARD)}`
- cross_split(교차 분할): `{rel(CROSS_SPLIT)}`
- failure_attribution(실패/성과 귀속): `{rel(FAILURE_ATTRIBUTION)}`
- review_queue(검토 대기열): `{rel(REVIEW_QUEUE)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(SELECTION_STATUS, f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `materialized_review_required_no_selection(구체화 완료, 검토 필요, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364B Materialization Closeout(364B 구체화 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- passing_cross_split_rows(교차 분할 통과 행): `{final["passing_cross_split_rows"]}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): timestamp context cost surface(시점 문맥 비용 표면)를 구체화했다.

Effect(효과): Stage364(364단계)는 후보 선택 없이 review(검토)로 진행한다.
""")
    append_text_once(STAGE_BRIEF, "## run364B Materialization Closeout", f"""## run364B Materialization Closeout(364B 구체화 종료)

Action(행동): timestamp-safe context cost surface(시점 안전 문맥 비용 표면)를 `{final["cross_split_rows"]}`개 cross-split row(교차 분할 행)로 구체화했다.

Effect(효과): passing_cross_split_rows(교차 분할 통과 행)는 `{final["passing_cross_split_rows"]}`개이고, 다음 작업은 `{NEXT_RUN_ID}` 검토다.
""")
    append_text_once(REVIEW_INDEX, "run364B_timestamp_context_cost_surface_materialization", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - timestamp context cost surface(시점 문맥 비용 표면) materialization(구체화).""")
    append_text_once(STAGE_README, "run364B Materialization", f"""## run364B Materialization(364B 구체화)

Action(행동): timestamp-safe context(시점 안전 문맥)를 q05 long-only MT5 report-derived trades(q05 롱 단독 MT5 보고서 파생 거래)에 적용했다.

Effect(효과): 비용 양수와 trade density(거래 밀도)를 동시에 보는 Stage364C(364C 실행) review(검토) 대기열을 열었다.
""")
    write_text(DECISION_DOC, f"""# Decision(결정): Stage364B Timestamp Context Cost Surface Materialization(364B 시점 문맥 비용 표면 구체화)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- passing_cross_split_rows(교차 분할 통과 행): `{final["passing_cross_split_rows"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364A(364A 실행)의 source/regime/label pivot(원천/국면/라벨 전환) 설계 대기열을 timestamp context surface(시점 문맥 표면)로 구체화했다.

Effect(효과): 통과 행은 positive scout(긍정 스카우트)일 뿐 후보 선택이나 운영 승격이 아니며, Stage364C(364C 실행) 검토에서 과적합/런타임 의미를 다시 판정한다.
""")


def registry_rows(cross_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "timestamp_context_materialization(시점 문맥 구체화)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage364B materializes timestamp context cost surface(Stage364B 시점 문맥 비용 표면 구체화).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["cross_split_rows"],
        "gate_passes": final.get("gate_passes", sum(1 for row in gates if row["status"] == "passed")),
        "gate_total": final.get("gate_total", len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(CROSS_SPLIT),
        "result_status": STATUS,
        "sample_rows": final["cross_split_rows"],
        "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "timestamp_context_materialization(시점 문맥 구체화)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can timestamp-safe context recover dense q05 cost?(시점 안전 문맥이 고밀도 q05 비용을 회복할 수 있는가?)",
        "metric_scope": "materialization_only(구체화 전용)",
    }
    tier_a = dict(common)
    tier_a.update({
        "subrun_id": f"{RUN_ID}__Tier_A",
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "kpi_scope": "report-derived timestamp context surface(보고서 파생 시점 문맥 표면)",
        "primary_kpi": f"passing_cross_split_rows={final['passing_cross_split_rows']};best_pass={final['best_pass_variant_id']};validation_net={final['best_pass_validation_cost_0_30_net']};oos_net={final['best_pass_oos_cost_0_30_net']}",
        "guardrail_kpi": "candidate_selection=not_run;mt5_execution=not_run",
    })
    tier_b = dict(tier_a)
    tier_b.update({
        "subrun_id": f"{RUN_ID}__Tier_B",
        "ledger_row_id": f"{RUN_ID}__Tier_B",
        "row_id": f"{RUN_ID}__Tier_B",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier_scope": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
        "primary_kpi": "missing_required(필수 누락)",
        "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
    })
    combined = dict(tier_a)
    combined.update({
        "subrun_id": f"{RUN_ID}__Tier_AplusB",
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "row_id": f"{RUN_ID}__Tier_AplusB",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
        "primary_kpi": "combined_not_run(합산 실행 없음)",
        "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
    })
    run_registry_row = dict(tier_a)
    return [run_registry_row], [tier_a, tier_b, combined], [tier_a, tier_b, combined]


def write_registries(cross_rows: Sequence[Mapping[str, Any]]) -> None:
    run_rows, project_rows, stage_rows = registry_rows(cross_rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)


def write_workspace_and_notes() -> None:
    final = read_json(FINAL_DECISION)
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364B(364B 실행)가 timestamp context cost surface(시점 문맥 비용 표면)를 구체화했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 passing_cross_split_rows(교차 분할 통과 행) `{final["passing_cross_split_rows"]}`개를 검토하고 과적합/런타임 의미를 낮은 주장 경계에서 판정한다.
""")
    append_text_once(WORKSPACE_CHANGELOG, "run364B_materialize_timestamp_context_cost_surface_without_db_v1", f"""## {TODAY} run364B Timestamp Context Cost Surface Materialization(364B 시점 문맥 비용 표면 구체화)

Action(행동): validation-only timestamp context filters(검증 전용 시점 문맥 필터)를 q05 long-only trade table(q05 롱 단독 거래 표)에 적용했다.

Effect(효과): passing_cross_split_rows(교차 분할 통과 행) `{final["passing_cross_split_rows"]}`개를 review-required scout(검토 필요 스카우트)로 열고 current truth(현재 진실)를 run364C(364C 실행)로 이동했다.
""")
    append_text_once(IDEA_REGISTRY, "IDEA-ST364B-TIMESTAMP-CONTEXT-COST-SURFACE", f"""## IDEA-ST364B-TIMESTAMP-CONTEXT-COST-SURFACE

- idea(아이디어): timestamp-safe context(시점 안전 문맥)로 q05 dense cost(q05 고밀도 비용)를 회복한다.
- evidence(근거): `{rel(CROSS_SPLIT)}`.
- result(결과): passing_cross_split_rows(교차 분할 통과 행) `{final["passing_cross_split_rows"]}`.
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""")
    if int(final["passing_cross_split_rows"]) == 0:
        append_text_once(NEGATIVE_RESULT_REGISTER, "FM-ST364B-TIMESTAMP-CONTEXT-NO-PASS", f"""## {TODAY} FM-ST364B-TIMESTAMP-CONTEXT-NO-PASS

- source_run(원천 실행): `{RUN_ID}`
- failure(실패): timestamp context cost surface(시점 문맥 비용 표면)가 교차 분할 비용/밀도 통과를 만들지 못했다.
- evidence(근거): `{rel(CROSS_SPLIT)}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""")


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage364/materialize_timestamp_context_cost_surface_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "ignored_with_manifest"),
        ("scorecard", SCORECARD, "ignored_with_manifest"),
        ("cross_split", CROSS_SPLIT, "ignored_with_manifest"),
        ("failure_attribution", FAILURE_ATTRIBUTION, "ignored_with_manifest"),
        ("review_queue", REVIEW_QUEUE, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        rows.append({
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and Path(path).is_file() else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_ID}__{artifact_type}",
            "notes": f"Stage364B timestamp context materialization artifact(364B 시점 문맥 구체화 산출물); availability={availability}",
            "artifact_path": rel(path),
        })
    append_or_replace_csv(
        ARTIFACT_REGISTRY,
        ["stage_id", "run_id", "artifact_type", "path"],
        rows,
        extend_header=False,
    )


def refresh_gates_and_final() -> None:
    write_csv(GATE_AUDIT, gate_rows())
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    final = read_json(FINAL_DECISION)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    final["required_gate_coverage_audit"] = rel(GATE_AUDIT)
    write_json(FINAL_DECISION, final)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("Missing required Stage364B inputs: " + ", ".join(missing))
    stage364a = read_json(SOURCE_STAGE364A_FINAL)
    if stage364a.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"Stage364A final_decision next_run_id mismatch: {stage364a.get('next_run_id')}")


def main() -> None:
    validate_inputs()
    frame = load_trade_table()
    variants = build_variants(frame)
    score_rows, cross_rows = materialize(frame, variants)
    write_run_artifacts(score_rows, cross_rows)
    write_reports(cross_rows)
    write_workspace_and_notes()
    write_registries(cross_rows)
    refresh_gates_and_final()
    write_reports(cross_rows)
    write_workspace_and_notes()
    write_registries(cross_rows)
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
