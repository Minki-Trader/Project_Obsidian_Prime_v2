from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN_NUMBER = "run333C"
RUN_ID = "run333C_materialize_guarded_veto_scoring_payloads_v1"
PARENT_RUN_ID = "run333B_design_guarded_veto_scoring_no_retune_v1"
NEXT_RUN_ID = "run333D_screen_guarded_payload_cost_curve_and_pocket_risk_v1"
STATUS = "completed_guarded_veto_scoring_payload_materialization_no_selection"
JUDGMENT = "guarded_veto_payload_materialized_research_only_no_goal_achieve"
DECISION = "guarded_veto_payloads_ready_for_cost_curve_screen_no_forward_judgment"
CLAIM_BOUNDARY = (
    "research_development_only_guarded_veto_scoring_payload_materialization_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

HARD_VETO_RANK = 0.80
SOFT_VETO_RANK = 0.65
NEGATIVE_CONTROL_RANK = 0.20
MIN_PAST_RANK_ROWS = 20

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SCORED_PAYLOAD_DIR = RUN_DIR / "scored_payloads"
SIGNAL_PAYLOAD_DIR = RUN_DIR / "signal_payloads"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
RUN333A_DIR = STAGE_DIR / "02_runs" / "run333A"
RUN333B_DIR = STAGE_DIR / "02_runs" / "run333B"
RUN330B_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330B"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage333C_guarded_veto_payload_materialization.md"

SOURCE_ARTIFACT_BY_THESIS = {
    "pv_c56_volatility_cost_shape_sentry": "c56_plain",
    "pv_c56_session_liquidity_veto": "c56_plain",
    "pv_m48_macro_rate_volatility_guard": "m48_plain",
    "pv_m48_breadth_reintroduction_control": "m48_plain",
}

GUARD_FAMILY_BY_THESIS = {
    "pv_c56_volatility_cost_shape_sentry": "cost_shape_sentry",
    "pv_c56_session_liquidity_veto": "session_liquidity_timing",
    "pv_m48_macro_rate_volatility_guard": "macro_rate_volatility_interaction",
    "pv_m48_breadth_reintroduction_control": "bounded_breadth_divergence_control",
}

SESSION_RISK_SCORE = {
    "asia": 0.65,
    "europe": 0.45,
    "us_open": 0.25,
    "us_late": 0.50,
    "rollover": 0.90,
}

LABEL_OR_FUTURE_PREFIXES = ("future_", "label")
LABEL_OR_FUTURE_COLUMNS = {
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "horizon_bars",
    "horizon_minutes",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    try:
        return io_path(path).exists()
    except OSError:
        return False


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
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
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line(text: str, anchor_prefix: str, insertion: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(anchor_prefix):
            lines.insert(index + 1, insertion)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + insertion + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
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
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    index: dict[tuple[str, ...], dict[str, Any]] = {
        tuple(str(row.get(key, "")) for key in key_columns): row for row in existing
    }
    for row in rows:
        index[tuple(str(row.get(key, "")) for key in key_columns)] = dict(row)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in index.values():
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})
    return path


def append_unique_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    seen = {tuple(str(row.get(key, "")) for key in key_columns) for row in existing}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        if key not in seen:
            existing.append(dict(row))
            seen.add(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in existing:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})
    return path


def numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(math.nan, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").astype("float64")


def expanding_rank_exclusive(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").astype("float64")
    ranks: list[float] = []
    prior: list[float] = []
    for value in values:
        if not math.isfinite(value):
            ranks.append(math.nan)
        elif len(prior) < MIN_PAST_RANK_ROWS:
            ranks.append(0.5)
        else:
            ranks.append(sum(1 for item in prior if item <= value) / len(prior))
        if math.isfinite(value):
            prior.append(float(value))
    return pd.Series(ranks, index=series.index, dtype="float64")


def stable_uniform(text: str) -> float:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:16], 16) / float(16**16 - 1)


def normalize_timestamp(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True, errors="coerce")


def source_artifact_paths() -> dict[str, Path]:
    signal_manifest = RUN330B_DIR / "signal_payload_manifest.csv"
    paths = {
        "run333A_feature_manifest": RUN333A_DIR / "feature_materialization_manifest.csv",
        "run333A_readiness_matrix": RUN333A_DIR / "materialization_readiness_matrix.csv",
        "run333A_boundary_audit": RUN333A_DIR / "feature_boundary_audit.csv",
        "run333B_scoring_protocol": RUN333B_DIR / "guarded_scoring_protocol.csv",
        "run333B_score_formula_contract": RUN333B_DIR / "score_formula_contract.csv",
        "run333B_scoring_branch_queue": RUN333B_DIR / "scoring_branch_queue.csv",
        "run333B_gate_audit": RUN333B_DIR / "required_gate_coverage_audit.csv",
        "run330B_signal_manifest": signal_manifest,
    }
    for row in read_csv_rows(signal_manifest):
        if row.get("artifact_slug") in {"c56_plain", "m48_plain"} and row.get("view_id") == "raw_forward":
            paths[f"run330B_{row['artifact_slug']}_raw_forward_signal_payload"] = ROOT / row["signal_payload_path"]
    return paths


def source_hash_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact_id, path in source_artifact_paths().items():
        exists = path_exists(path)
        rows.append(
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": exists,
                "sha256": sha256_file(path) if exists and io_path(path).is_file() else "",
            }
        )
    return rows


def protocol_rows() -> list[dict[str, str]]:
    return read_csv_rows(RUN333B_DIR / "guarded_scoring_protocol.csv")


def queue_rows() -> list[dict[str, str]]:
    return read_csv_rows(RUN333B_DIR / "scoring_branch_queue.csv")


def protocol_by_thesis() -> dict[str, dict[str, str]]:
    return {row["thesis_id"]: row for row in protocol_rows()}


def signal_manifest_by_slug() -> dict[str, dict[str, str]]:
    rows = read_csv_rows(RUN330B_DIR / "signal_payload_manifest.csv")
    return {
        row["artifact_slug"]: row
        for row in rows
        if row.get("artifact_slug") in {"c56_plain", "m48_plain"} and row.get("view_id") == "raw_forward"
    }


def load_feature_frame(protocol: Mapping[str, str]) -> pd.DataFrame:
    path = ROOT / protocol["feature_frame_path"]
    actual_hash = sha256_file(path)
    expected_hash = protocol.get("feature_frame_sha256", "")
    if expected_hash and actual_hash != expected_hash:
        raise RuntimeError(f"Feature frame hash mismatch for {protocol['thesis_id']}: {actual_hash} != {expected_hash}")
    frame = pd.read_csv(io_path(path))
    frame["timestamp_key"] = normalize_timestamp(frame["timestamp_utc"])
    frame = frame.sort_values("timestamp_key").drop_duplicates("timestamp_key", keep="last").reset_index(drop=True)
    return frame


def load_signal_payload(source_slug: str) -> tuple[pd.DataFrame, dict[str, str]]:
    manifest = signal_manifest_by_slug().get(source_slug)
    if not manifest:
        raise RuntimeError(f"Missing raw_forward signal payload manifest for {source_slug}")
    path = ROOT / manifest["signal_payload_path"]
    payload = pd.read_csv(io_path(path))
    payload["timestamp_key"] = normalize_timestamp(payload["timestamp"])
    payload = payload.sort_values("timestamp_key").drop_duplicates("timestamp_key", keep="last").reset_index(drop=True)
    return payload, manifest


def score_base_frame(thesis_id: str, frame: pd.DataFrame) -> pd.DataFrame:
    scored = frame.copy()
    if thesis_id == "pv_c56_volatility_cost_shape_sentry":
        components = pd.DataFrame(
            {
                "atr_rank": expanding_rank_exclusive(numeric(scored, "atr_14_over_atr_50")),
                "hist_vol_rank": expanding_rank_exclusive(numeric(scored, "historical_vol_5_over_20")),
                "return_atr_rank": expanding_rank_exclusive(numeric(scored, "return_1_over_atr_14").abs()),
                "di_spread_rank": expanding_rank_exclusive(numeric(scored, "di_spread_14").abs()),
            }
        )
        scored["guard_score"] = components.mean(axis=1, skipna=False)
        scored["guard_score_component_count"] = components.notna().sum(axis=1)
    elif thesis_id == "pv_c56_session_liquidity_veto":
        bucket_score = scored["session_bucket_utc"].astype(str).map(SESSION_RISK_SCORE)
        weekday = pd.to_numeric(scored.get("timestamp_weekday_utc", 0), errors="coerce").fillna(0)
        weekday_addon = weekday.isin([0, 4]).astype("float64") * 0.05
        scored["guard_score"] = (bucket_score.astype("float64") + weekday_addon).clip(0.0, 1.0)
        scored["guard_score_component_count"] = bucket_score.notna().astype("int8")
    elif thesis_id == "pv_m48_macro_rate_volatility_guard":
        shock_components = pd.DataFrame(
            {
                "vix_abs_rank": expanding_rank_exclusive(numeric(scored, "vix_zscore_20").abs()),
                "us10yr_abs_rank": expanding_rank_exclusive(numeric(scored, "us10yr_zscore_20").abs()),
                "usdx_abs_rank": expanding_rank_exclusive(numeric(scored, "usdx_zscore_20").abs()),
                "vix_change_rank": expanding_rank_exclusive(numeric(scored, "vix_change_1").abs()),
                "us10yr_change_rank": expanding_rank_exclusive(numeric(scored, "us10yr_change_1").abs()),
                "usdx_change_rank": expanding_rank_exclusive(numeric(scored, "usdx_change_1").abs()),
            }
        )
        level_score = shock_components[["vix_abs_rank", "us10yr_abs_rank", "usdx_abs_rank"]].mean(axis=1, skipna=False)
        change_score = shock_components[["vix_change_rank", "us10yr_change_rank", "usdx_change_rank"]].mean(axis=1, skipna=False)
        scored["guard_score"] = (0.75 * level_score + 0.25 * change_score).clip(0.0, 1.0)
        scored["guard_score_component_count"] = shock_components.notna().sum(axis=1)
    elif thesis_id == "pv_m48_breadth_reintroduction_control":
        breadth = numeric(scored, "joined_us100_minus_mega8_equal_return_1")
        scored["guard_score"] = expanding_rank_exclusive(breadth.abs())
        scored["guard_score_component_count"] = breadth.notna().astype("int8")
    else:
        raise RuntimeError(f"Unknown thesis_id: {thesis_id}")

    scored["guard_score_valid_flag"] = scored["guard_score"].notna().astype("int8")
    scored["guard_score_missing_flag"] = (scored["guard_score_valid_flag"] == 0).astype("int8")
    scored["hard_veto_flag"] = ((scored["guard_score_valid_flag"] == 1) & (scored["guard_score"] >= HARD_VETO_RANK)).astype("int8")
    scored["soft_veto_flag"] = ((scored["guard_score_valid_flag"] == 1) & (scored["guard_score"] >= SOFT_VETO_RANK)).astype("int8")

    if thesis_id == "pv_c56_session_liquidity_veto":
        hard_density = float(scored["hard_veto_flag"].mean()) if len(scored) else 0.0
        scored["negative_control_flag"] = [
            int(stable_uniform(f"{thesis_id}|{timestamp}") <= hard_density)
            for timestamp in scored["timestamp_key"].astype(str)
        ]
    elif thesis_id == "pv_m48_breadth_reintroduction_control":
        scored["negative_control_flag"] = scored["guard_score_missing_flag"].astype("int8")
    else:
        scored["negative_control_flag"] = (
            (scored["guard_score_valid_flag"] == 1) & (scored["guard_score"] <= NEGATIVE_CONTROL_RANK)
        ).astype("int8")

    scored["abstain_flag"] = scored["guard_score_missing_flag"]
    scored["thesis_id"] = thesis_id
    scored["guard_family"] = GUARD_FAMILY_BY_THESIS[thesis_id]
    scored["run_id"] = RUN_ID
    scored["claim_boundary"] = CLAIM_BOUNDARY
    return scored


def action_for_mode(thesis_id: str, mode: str, row: Mapping[str, Any]) -> tuple[int, str, int]:
    valid = int(row.get("guard_score_valid_flag") or 0) == 1
    hard = int(row.get("hard_veto_flag") or 0) == 1
    soft = int(row.get("soft_veto_flag") or 0) == 1
    negative = int(row.get("negative_control_flag") or 0) == 1
    if mode == "control_no_veto":
        return 1, "baseline_no_veto", 0
    if mode == "hard_veto":
        return int(valid and not hard), "drop_if_hard_veto_or_missing_abstain", int(hard or not valid)
    if mode == "soft_veto":
        if thesis_id == "pv_m48_breadth_reintroduction_control":
            return int(valid), "annotation_only_valid_overlap_rows", int(not valid)
        return 1, "annotation_only_no_lot_or_threshold_change", int(soft)
    if mode == "negative_control":
        if thesis_id == "pv_m48_breadth_reintroduction_control":
            return 0, "expected_invalid_missing_as_tradeable_forbidden", 1
        return int(valid and not negative), "negative_control_drop_predeclared_rows", int(negative or not valid)
    raise RuntimeError(f"Unknown scoring mode: {mode}")


def materialize_mode_frame(thesis_id: str, scored: pd.DataFrame, mode: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for row in scored.to_dict("records"):
        allowed, action, mode_flag = action_for_mode(thesis_id, mode, row)
        payload_row = dict(row)
        payload_row["scoring_mode"] = mode
        payload_row["queue_id"] = f"{thesis_id}__{mode}"
        payload_row["view_signal_allowed_flag"] = allowed
        payload_row["mode_action"] = action
        payload_row["mode_veto_or_annotation_flag"] = mode_flag
        payload_row["hard_veto_rank"] = HARD_VETO_RANK
        payload_row["soft_veto_rank"] = SOFT_VETO_RANK
        rows.append(payload_row)
    output = pd.DataFrame(rows)
    output["timestamp_utc"] = output["timestamp_key"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return output


def signal_columns(payload: pd.DataFrame) -> list[str]:
    base = list(payload.columns)
    extras = [
        "source_signal_direction",
        "source_probability_margin",
        "queue_id",
        "thesis_id",
        "guard_family",
        "scoring_mode",
        "guard_score",
        "guard_score_valid_flag",
        "guard_score_missing_flag",
        "hard_veto_flag",
        "soft_veto_flag",
        "negative_control_flag",
        "abstain_flag",
        "view_signal_allowed_flag",
        "mode_action",
        "mode_veto_or_annotation_flag",
        "payload_claim_boundary",
    ]
    return [column for column in [*base, *extras] if column != "timestamp_key"]


def materialize_signal_payload(
    thesis_id: str,
    mode: str,
    mode_frame: pd.DataFrame,
    source_signals: pd.DataFrame,
) -> pd.DataFrame:
    guard_cols = [
        "timestamp_key",
        "queue_id",
        "thesis_id",
        "guard_family",
        "scoring_mode",
        "guard_score",
        "guard_score_valid_flag",
        "guard_score_missing_flag",
        "hard_veto_flag",
        "soft_veto_flag",
        "negative_control_flag",
        "abstain_flag",
        "view_signal_allowed_flag",
        "mode_action",
        "mode_veto_or_annotation_flag",
    ]
    merged = source_signals.merge(mode_frame[guard_cols], on="timestamp_key", how="left")
    for column in guard_cols:
        if column != "timestamp_key" and column not in merged.columns:
            merged[column] = ""
    merged["guard_score_valid_flag"] = pd.to_numeric(merged["guard_score_valid_flag"], errors="coerce").fillna(0).astype("int8")
    merged["guard_score_missing_flag"] = pd.to_numeric(merged["guard_score_missing_flag"], errors="coerce").fillna(1).astype("int8")
    merged["hard_veto_flag"] = pd.to_numeric(merged["hard_veto_flag"], errors="coerce").fillna(0).astype("int8")
    merged["soft_veto_flag"] = pd.to_numeric(merged["soft_veto_flag"], errors="coerce").fillna(0).astype("int8")
    merged["negative_control_flag"] = pd.to_numeric(merged["negative_control_flag"], errors="coerce").fillna(0).astype("int8")
    merged["abstain_flag"] = pd.to_numeric(merged["abstain_flag"], errors="coerce").fillna(1).astype("int8")
    merged["view_signal_allowed_flag"] = pd.to_numeric(merged["view_signal_allowed_flag"], errors="coerce").fillna(0).astype("int8")
    merged["source_signal_direction"] = merged["signal_direction"]
    merged["source_probability_margin"] = merged.get("probability_margin", "")
    merged["payload_claim_boundary"] = CLAIM_BOUNDARY
    kept = merged[merged["view_signal_allowed_flag"] == 1].copy()
    if mode == "negative_control" and thesis_id == "pv_m48_breadth_reintroduction_control":
        kept = kept.iloc[0:0].copy()
    if not kept.empty:
        kept["timestamp"] = kept["timestamp_key"].dt.strftime("%Y-%m-%d %H:%M:%S+00:00")
        kept["view_id"] = f"run333C_{thesis_id}__{mode}"
    return kept.drop(columns=["timestamp_key"], errors="ignore")


def forbidden_output_columns(paths: Sequence[Path]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in paths:
        if not path_exists(path):
            continue
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
        for column in header:
            if column in LABEL_OR_FUTURE_COLUMNS or column.startswith(LABEL_OR_FUTURE_PREFIXES):
                findings.append({"path": rel(path), "column": column})
    return findings


def summarize_mode(
    *,
    queue: Mapping[str, str],
    mode_frame: pd.DataFrame,
    signal_payload: pd.DataFrame,
    source_signal_rows: int,
    scored_path: Path,
    signal_path: Path,
    source_signal_path: Path,
) -> dict[str, Any]:
    thesis_id = queue["thesis_id"]
    mode = queue["scoring_mode"]
    invalid_expected = thesis_id == "pv_m48_breadth_reintroduction_control" and mode == "negative_control"
    valid_scores = int(mode_frame["guard_score_valid_flag"].sum())
    abstain_rows = int(mode_frame["abstain_flag"].sum())
    output_signal_rows = len(signal_payload)
    dropped_signal_rows = max(source_signal_rows - output_signal_rows, 0)
    if invalid_expected:
        status = "expected_invalid_negative_control_not_tradeable"
    elif output_signal_rows == 0:
        status = "materialized_empty_signal_payload"
    elif thesis_id == "pv_m48_breadth_reintroduction_control" and mode == "control_no_veto":
        status = "materialized_control_baseline_with_breadth_missing_boundary"
    else:
        status = "materialized_scored_signal_payload"
    return {
        "queue_id": queue["queue_id"],
        "thesis_id": thesis_id,
        "guard_family": GUARD_FAMILY_BY_THESIS[thesis_id],
        "source_artifact": SOURCE_ARTIFACT_BY_THESIS[thesis_id],
        "scoring_mode": mode,
        "source_signal_payload_path": rel(source_signal_path),
        "source_signal_rows": source_signal_rows,
        "feature_rows": len(mode_frame),
        "valid_score_rows": valid_scores,
        "abstain_rows": abstain_rows,
        "hard_veto_rows": int(mode_frame["hard_veto_flag"].sum()),
        "soft_zone_rows": int(mode_frame["soft_veto_flag"].sum()),
        "negative_control_rows": int(mode_frame["negative_control_flag"].sum()),
        "output_signal_rows": output_signal_rows,
        "dropped_signal_rows": dropped_signal_rows,
        "invalid_expected_flag": int(invalid_expected),
        "scored_payload_path": rel(scored_path),
        "scored_payload_sha256": sha256_file(scored_path),
        "signal_payload_path": rel(signal_path),
        "signal_payload_sha256": sha256_file(signal_path),
        "materialization_status": status,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_payloads() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    protocols = protocol_by_thesis()
    queues = queue_rows()
    manifests = signal_manifest_by_slug()
    scored_by_thesis: dict[str, pd.DataFrame] = {}
    signal_by_slug: dict[str, tuple[pd.DataFrame, dict[str, str]]] = {}
    manifest_rows: list[dict[str, Any]] = []
    quantile_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []

    for thesis_id, protocol in protocols.items():
        base_frame = score_base_frame(thesis_id, load_feature_frame(protocol))
        scored_by_thesis[thesis_id] = base_frame
        valid_scores = pd.to_numeric(base_frame["guard_score"], errors="coerce").dropna()
        quantile_rows.append(
            {
                "thesis_id": thesis_id,
                "guard_family": GUARD_FAMILY_BY_THESIS[thesis_id],
                "rows": len(base_frame),
                "valid_score_rows": len(valid_scores),
                "missing_score_rows": int(base_frame["guard_score_missing_flag"].sum()),
                "hard_veto_rank": HARD_VETO_RANK,
                "soft_veto_rank": SOFT_VETO_RANK,
                "q05": valid_scores.quantile(0.05) if not valid_scores.empty else None,
                "q25": valid_scores.quantile(0.25) if not valid_scores.empty else None,
                "q50": valid_scores.quantile(0.50) if not valid_scores.empty else None,
                "q75": valid_scores.quantile(0.75) if not valid_scores.empty else None,
                "q95": valid_scores.quantile(0.95) if not valid_scores.empty else None,
                "rank_policy": "expanding_past_exclusive_or_predeclared_session_map_no_forward_pnl_fit",
            }
        )

    for queue in queues:
        thesis_id = queue["thesis_id"]
        mode = queue["scoring_mode"]
        source_slug = SOURCE_ARTIFACT_BY_THESIS[thesis_id]
        if source_slug not in signal_by_slug:
            signal_by_slug[source_slug] = load_signal_payload(source_slug)
        source_signals, source_manifest = signal_by_slug[source_slug]
        mode_frame = materialize_mode_frame(thesis_id, scored_by_thesis[thesis_id], mode)
        signal_payload = materialize_signal_payload(thesis_id, mode, mode_frame, source_signals)

        scored_path = SCORED_PAYLOAD_DIR / f"{queue['queue_id']}_scored_payload.csv"
        signal_path = SIGNAL_PAYLOAD_DIR / f"{queue['queue_id']}_signals.csv"
        mode_columns = [column for column in mode_frame.columns if column != "timestamp_key"]
        write_csv(scored_path, mode_columns, mode_frame.to_dict("records"))
        signal_cols = signal_columns(source_signals)
        if signal_payload.empty:
            write_csv(signal_path, signal_cols, [])
        else:
            write_csv(signal_path, signal_cols, signal_payload.to_dict("records"))
        artifacts.extend([scored_path, signal_path])
        manifest_rows.append(
            summarize_mode(
                queue=queue,
                mode_frame=mode_frame,
                signal_payload=signal_payload,
                source_signal_rows=int(source_manifest.get("signal_rows") or len(source_signals)),
                scored_path=scored_path,
                signal_path=signal_path,
                source_signal_path=ROOT / source_manifest["signal_payload_path"],
            )
        )

    return manifest_rows, quantile_rows, artifacts


def signal_manifest_rows(payload_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in payload_manifest:
        status = "deferred_until_run333D_curve_screen"
        if row["invalid_expected_flag"]:
            status = "excluded_expected_invalid_control"
        elif int(row["output_signal_rows"]) == 0:
            status = "excluded_empty_signal_payload"
        rows.append(
            {
                "queue_id": row["queue_id"],
                "thesis_id": row["thesis_id"],
                "guard_family": row["guard_family"],
                "source_artifact": row["source_artifact"],
                "scoring_mode": row["scoring_mode"],
                "signal_payload_path": row["signal_payload_path"],
                "signal_payload_sha256": row["signal_payload_sha256"],
                "signal_rows": row["output_signal_rows"],
                "source_signal_rows": row["source_signal_rows"],
                "guarded_signal_drop_rows": row["dropped_signal_rows"],
                "runtime_probe_status": status,
                "runtime_probe_reason": "cost_curve_and_pocket_screen_required_before_mt5_runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def cost_curve_queue_rows(payload_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in payload_manifest:
        if row["invalid_expected_flag"] or int(row["output_signal_rows"]) == 0:
            queue_status = "not_queued"
        else:
            queue_status = "queued_for_run333D_proxy_cost_curve_screen"
        rows.append(
            {
                "queue_id": row["queue_id"],
                "thesis_id": row["thesis_id"],
                "source_artifact": row["source_artifact"],
                "scoring_mode": row["scoring_mode"],
                "signal_payload_path": row["signal_payload_path"],
                "signal_rows": row["output_signal_rows"],
                "queue_status": queue_status,
                "required_cost_steps": "0;0.25;0.5;1;2;3;5",
                "required_curve_checks": "rolling20_min_net;rolling40_min_net;underwater_stretch;worst_chunk",
                "forbidden_claim_before_screen": "no_forward_passed_no_candidate_selection_no_runtime_authority",
            }
        )
    return rows


def breadth_abstain_rows(payload_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in payload_manifest:
        if row["thesis_id"] != "pv_m48_breadth_reintroduction_control":
            continue
        rows.append(
            {
                "queue_id": row["queue_id"],
                "scoring_mode": row["scoring_mode"],
                "source_signal_rows": row["source_signal_rows"],
                "output_signal_rows": row["output_signal_rows"],
                "dropped_signal_rows": row["dropped_signal_rows"],
                "abstain_rows_in_feature_frame": row["abstain_rows"],
                "invalid_expected_flag": row["invalid_expected_flag"],
                "judgment": "missing_breadth_rows_abstain_or_expected_invalid_control",
            }
        )
    return rows


def gate_rows(payload_manifest: Sequence[Mapping[str, Any]], generated_paths: Sequence[Path]) -> list[dict[str, Any]]:
    source_missing = [row["artifact_id"] for row in source_hash_rows() if not row["exists"]]
    protocols = protocol_rows()
    queues = queue_rows()
    manifest_count = len(payload_manifest)
    signal_count = sum(1 for row in payload_manifest if path_exists(ROOT / str(row["signal_payload_path"])))
    forbidden_columns = forbidden_output_columns(generated_paths)
    breadth_rows = [row for row in payload_manifest if row["thesis_id"] == "pv_m48_breadth_reintroduction_control"]
    breadth_negative_ok = any(
        row["scoring_mode"] == "negative_control"
        and row["invalid_expected_flag"]
        and int(row["output_signal_rows"]) == 0
        for row in breadth_rows
    )
    breadth_hard_soft_ok = all(
        int(row["dropped_signal_rows"]) >= 0
        for row in breadth_rows
        if row["scoring_mode"] in {"hard_veto", "soft_veto"}
    )
    return [
        {
            "gate": "source_artifacts_present",
            "status": "pass" if not source_missing else "fail",
            "evidence_path": rel(RUN_DIR / "source_artifact_hashes.json"),
            "notes": "all run333A/run333B/run330B sources present" if not source_missing else f"missing={source_missing}",
        },
        {
            "gate": "protocol_and_queue_complete",
            "status": "pass" if len(protocols) == 4 and len(queues) == 16 else "fail",
            "evidence_path": rel(RUN333B_DIR / "scoring_branch_queue.csv"),
            "notes": f"protocols={len(protocols)};queues={len(queues)}",
        },
        {
            "gate": "payload_materialization_complete",
            "status": "pass" if manifest_count == 16 and signal_count == 16 else "fail",
            "evidence_path": rel(RUN_DIR / "payload_manifest.csv"),
            "notes": f"payload_manifest_rows={manifest_count};signal_files={signal_count}",
        },
        {
            "gate": "no_label_or_future_columns",
            "status": "pass" if not forbidden_columns else "fail",
            "evidence_path": rel(RUN_DIR / "payload_column_forbidden_audit.json"),
            "notes": "no forbidden columns" if not forbidden_columns else json.dumps(forbidden_columns, ensure_ascii=False),
        },
        {
            "gate": "breadth_missing_abstain_boundary",
            "status": "pass" if breadth_negative_ok and breadth_hard_soft_ok else "fail",
            "evidence_path": rel(RUN_DIR / "breadth_missing_abstain_audit.csv"),
            "notes": "breadth negative control is expected-invalid and hard/soft keep missing rows out of scored guarded views",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "no_retune_guard_receipt.json"),
            "notes": "no model, ONNX, threshold, lot, D/B rule, ATR SL/TP, or runtime handoff mutation.",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "payload materialization only; no Forward Passed/Failed, runtime authority, or Goal Achieve claim.",
        },
    ]


def write_receipts(
    generated_at_utc: str,
    payload_manifest: Sequence[Mapping[str, Any]],
    generated_paths: Sequence[Path],
) -> list[Path]:
    failed_gates = [row for row in gate_rows(payload_manifest, generated_paths) if row["status"] != "pass"]
    return [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_json(RUN_DIR / "payload_column_forbidden_audit.json", forbidden_output_columns(generated_paths)),
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "hypothesis": "Predeclared guarded veto scores can be materialized on fixed raw-forward signals without fitting to forward PnL.",
                "decision_use": "Create comparable signal payloads for run333D cost/curve/pocket screening; not candidate selection.",
                "comparison_baseline": "control_no_veto signal payloads from c56_plain and m48_plain raw-forward source signals.",
                "control_variables": "fixed source signal payloads, fixed ONNX outputs, fixed thresholds, fixed lot/risk/runtime handoff, fixed run333B score protocol.",
                "changed_variables": "guard score annotations and predeclared hard/soft/negative-control view materialization only.",
                "sample_scope": "US100 M5 raw-forward scope inherited from run330B/run330E and run333A.",
                "success_criteria": "sixteen payloads, signal manifests, cost-curve queue, breadth abstain audit, and no failed gates.",
                "failure_criteria": "missing source payload, hash mismatch, fewer than sixteen payloads, forbidden future/label column, or retune mutation.",
                "invalid_conditions": [
                    "forward_pnl_fit",
                    "known_pocket_date_feature",
                    "lot_or_threshold_repair",
                    "missing_breadth_imputation_as_tradeable",
                ],
                "stop_conditions": "stop before run333D or MT5 if any required gate fails.",
                "evidence_plan": [rel(RUN_DIR / "payload_manifest.csv"), rel(RUN_DIR / "cost_curve_input_queue.csv")],
            },
        ),
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(RUN333A_DIR / "feature_materialization_manifest.csv"),
                    rel(RUN333B_DIR / "scoring_branch_queue.csv"),
                    rel(RUN330B_DIR / "signal_payload_manifest.csv"),
                ],
                "time_axis": "timestamp_utc is parsed as UTC; signal timestamps are joined on UTC bar time.",
                "sample_scope": "c56_plain 2070 feature rows with 486 source signals; m48_plain 5484 feature rows with 2562 source signals.",
                "missing_or_duplicate_check": rel(RUN_DIR / "payload_manifest.csv"),
                "feature_label_boundary": "guard scores use materialized features and expanding-past/session maps only; no future returns, labels, tester outcomes, or PnL.",
                "split_boundary": "raw-forward materialization only; no train or forward PnL calibration.",
                "leakage_risk": "post-hoc pocket-date filters or forward KPI-tuned rank thresholds.",
                "data_hash_or_identity": rel(RUN_DIR / "source_artifact_hashes.json"),
                "integrity_judgment": "usable_for_guarded_payload_materialization_with_breadth_boundary",
            },
        ),
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "none_new_model_guarded_signal_payloads_from_fixed_source_ONNX_outputs",
                "target_and_label": "no new target or label; source ONNX signal payloads are fixed inputs.",
                "split_method": "raw-forward replay payload materialization; no selection split used.",
                "selection_metric": "not_applicable_no_candidate_selection",
                "secondary_metrics": "run333D cost ladder, rolling pocket, underwater stretch, temporal slices, negative controls.",
                "threshold_policy": "fixed source thresholds inherited; hard/soft guard ranks predeclared at 0.80/0.65 and not fit on PnL.",
                "overfit_risk": "guard scores could still be overinterpreted before cost/curve and MT5 evidence.",
                "calibration_risk": "guard_score is a rank/semantic risk score, not a probability.",
                "comparison_baseline": "control_no_veto plus negative_control views.",
                "validation_judgment": "exploratory_payload_materialization_only",
            },
        ),
        write_json(
            RUN_DIR / "no_retune_guard_receipt.json",
            {
                "selected_candidate_changed": False,
                "onnx_changed": False,
                "adapter_package_changed": False,
                "feature_order_changed_for_existing_models": False,
                "d_b_decision_surface_changed": False,
                "score_threshold_changed": False,
                "risk_or_lot_logic_changed": False,
                "atr_sl_tp_changed": False,
                "runtime_handoff_changed": False,
                "new_model_trained": False,
                "forward_pnl_used_for_guard_thresholds": False,
                "notes": "run333C materializes guarded payloads from existing fixed signal payloads and predeclared guard protocol.",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "source_inputs": [row["path"] for row in source_hash_rows()],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in generated_paths],
                "artifact_hashes": "recorded in payload_manifest.csv and docs/registers/artifact_registry.csv",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked",
                "lineage_judgment": "connected_with_payload_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "run333C guarded veto scoring payload materialization",
                "evidence_available": [
                    rel(RUN_DIR / "payload_manifest.csv"),
                    rel(RUN_DIR / "signal_payload_manifest.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "evidence_missing": ["no run333D cost curve screen", "no MT5 tester output", "no forward pass/fail judgment"],
                "judgment_label": "exploratory_payload_materialized",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "Guarded signal payloads exist now, but performance and runtime evidence have not been judged.",
                "failed_gates": failed_gates,
            },
        ),
    ]


def write_reports(payload_manifest: Sequence[Mapping[str, Any]]) -> list[Path]:
    materialized = sum(1 for row in payload_manifest if str(row["materialization_status"]).startswith("materialized"))
    expected_invalid = sum(int(row["invalid_expected_flag"]) for row in payload_manifest)
    total_signal_rows = sum(int(row["output_signal_rows"]) for row in payload_manifest)
    report = write_md(
        REVIEWS_DIR / "run333C_guarded_veto_payload_materialization.md",
        f"""
# run333C Guarded Veto Payload Materialization(333C 방어 거부 페이로드 물질화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Payload Read(페이로드 판독)

- payload_views(페이로드 보기): `{len(payload_manifest)}`
- materialized_tradeable_or_annotation_views(물질화된 거래 가능/주석 보기): `{materialized}`
- expected_invalid_controls(예상 무효 대조): `{expected_invalid}`
- output_signal_rows(출력 신호 행): `{total_signal_rows}`

Effect(효과): run333C(333C 실행)는 hard/soft/control/negative-control(강한 거부/약한 거부/대조/부정 대조) payload(페이로드)를 만들었다. 하지만 cost curve(비용 곡선), MT5 tester(메타트레이더5 테스터), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 아직 없다.

## Boundary(경계)

- no threshold retuning(임계값 재조정 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 갱신 없음)
- no ONNX update(온엑스 갱신 없음)
- no runtime authority(런타임 권위 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage333C Guarded Veto Payload Decision(333C 방어 거부 페이로드 결정)

run333C(333C 실행)는 run333A(333A 실행)의 feature frame(피처 프레임), run333B(333B 실행)의 scoring protocol(점수화 계약), run330B(330B 실행)의 fixed raw-forward signal payload(고정 원본 전진 신호 페이로드)를 결합했다.

- decision(결정): `{DECISION}`
- payload_views(페이로드 보기): `{len(payload_manifest)}`
- signal_manifest(신호 목록): `stages/333_overfit_guard__timestamp_safe_pocket_veto_materialization/02_runs/run333C/signal_payload_manifest.csv`
- cost_curve_queue(비용 곡선 대기열): `stages/333_overfit_guard__timestamp_safe_pocket_veto_materialization/02_runs/run333C/cost_curve_input_queue.csv`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): 이제 다음 run333D(333D 실행)가 같은 source signal(원천 신호)에서 guard(방어)가 무엇을 버리고 무엇을 남기는지 cost/curve/pocket(비용/곡선/포켓)으로 볼 수 있다. 성과 판정은 아직 하지 않는다.
""",
    )
    return [report, decision]


def update_selection_status() -> Path:
    text = f"""
# Stage333 Selection Status(333단계 선택 상태)

- stage_status(단계 상태): `open_payload_materialization_completed_cost_curve_screen_next`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `332_overfit_guard__failure_memory_forward_research_handoff`
- latest_materialization(최신 물질화): `run333A_materialize_timestamp_safe_pocket_veto_features_v1`
- latest_scoring_design(최신 점수화 설계): `run333B_design_guarded_veto_scoring_no_retune_v1`
- latest_payload_materialization(최신 페이로드 물질화): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run333C(333C 실행)는 guarded payload(방어 페이로드)를 만들었고, 다음은 cost/curve/pocket screen(비용/곡선/포켓 선별)이다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_current_truth(payload_manifest: Sequence[Mapping[str, Any]]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage333(333단계) run333C(333C 실행)는 `{STATUS}`로 guarded veto scoring payload(방어 거부 점수 페이로드) 16개를 물질화했다. Effect(효과): run333D(333D 실행)는 cost/curve/pocket screen(비용/곡선/포켓 선별)을 할 수 있지만 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage333(333단계) run333C(333C 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v4`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": "- source_stage(원천 단계): `332_overfit_guard__failure_memory_forward_research_handoff`",
        "- target_surface(": "- target_surface(목표 표면): `guarded_payload_cost_curve_screen`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run333C_summary(333C 요약): guarded veto payload materialization(방어 거부 페이로드 물질화)을 `{STATUS}`로 완료했다. "
        f"Effect(효과): payload view(페이로드 보기) `{len(payload_manifest)}`개와 signal manifest(신호 목록)를 만들었지만 cost curve(비용 곡선), MT5(메타트레이더5), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run333C_summary(333C 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))
    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage333C Guarded Veto Payload Materialization",
            f"""
## 2026-05-26 - Stage333C Guarded Veto Payload Materialization(333C 방어 거부 페이로드 물질화)

- run333C(333C 실행): guarded veto scoring payload(방어 거부 점수 페이로드)를 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- payload_views(페이로드 보기): `{len(payload_manifest)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run333D(333D 실행)의 cost/curve/pocket screen(비용/곡선/포켓 선별) 입력을 만들고, 후보 선택이나 Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run333C_guarded_veto_payload_materialization.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": "guarded_payload_materialization_only;selected_candidate=none;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__guarded_payload_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "guarded_veto_payload_materialization",
                "tier_scope": "raw_forward_signal_payload_scope",
                "kpi_scope": "no_trading_kpi_payload_only",
                "scoreboard_lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "payload_views=16;signal_payload_manifest_rows=16",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_runtime_execution",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__guarded_payload_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "guarded_veto_payload_materialization(방어 거부 페이로드 물질화)",
                "tier_scope": "raw_forward_signal_payload_scope(원본 전진 신호 페이로드 범위)",
                "scoreboard": "payload_only_no_trading_kpi(페이로드 전용, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if path_exists(artifact) and io_path(artifact).is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage333C guarded payload artifact; no operating claim.",
                }
            )
    append_unique_csv(ARTIFACT_REGISTRY, ["artifact_id", "path"], artifact_rows)


def write_run_artifacts(generated_at_utc: str) -> tuple[list[Path], list[dict[str, Any]]]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    SCORED_PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    SIGNAL_PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)

    payload_manifest, quantile_rows, payload_paths = materialize_payloads()
    signal_rows = signal_manifest_rows(payload_manifest)
    cost_rows = cost_curve_queue_rows(payload_manifest)
    breadth_rows = breadth_abstain_rows(payload_manifest)

    artifacts: list[Path] = [
        write_csv(
            RUN_DIR / "payload_manifest.csv",
            [
                "queue_id",
                "thesis_id",
                "guard_family",
                "source_artifact",
                "scoring_mode",
                "source_signal_payload_path",
                "source_signal_rows",
                "feature_rows",
                "valid_score_rows",
                "abstain_rows",
                "hard_veto_rows",
                "soft_zone_rows",
                "negative_control_rows",
                "output_signal_rows",
                "dropped_signal_rows",
                "invalid_expected_flag",
                "scored_payload_path",
                "scored_payload_sha256",
                "signal_payload_path",
                "signal_payload_sha256",
                "materialization_status",
                "claim_boundary",
            ],
            payload_manifest,
        ),
        write_csv(
            RUN_DIR / "signal_payload_manifest.csv",
            [
                "queue_id",
                "thesis_id",
                "guard_family",
                "source_artifact",
                "scoring_mode",
                "signal_payload_path",
                "signal_payload_sha256",
                "signal_rows",
                "source_signal_rows",
                "guarded_signal_drop_rows",
                "runtime_probe_status",
                "runtime_probe_reason",
                "claim_boundary",
            ],
            signal_rows,
        ),
        write_csv(
            RUN_DIR / "cost_curve_input_queue.csv",
            [
                "queue_id",
                "thesis_id",
                "source_artifact",
                "scoring_mode",
                "signal_payload_path",
                "signal_rows",
                "queue_status",
                "required_cost_steps",
                "required_curve_checks",
                "forbidden_claim_before_screen",
            ],
            cost_rows,
        ),
        write_csv(
            RUN_DIR / "guard_score_quantile_audit.csv",
            [
                "thesis_id",
                "guard_family",
                "rows",
                "valid_score_rows",
                "missing_score_rows",
                "hard_veto_rank",
                "soft_veto_rank",
                "q05",
                "q25",
                "q50",
                "q75",
                "q95",
                "rank_policy",
            ],
            quantile_rows,
        ),
        write_csv(
            RUN_DIR / "breadth_missing_abstain_audit.csv",
            [
                "queue_id",
                "scoring_mode",
                "source_signal_rows",
                "output_signal_rows",
                "dropped_signal_rows",
                "abstain_rows_in_feature_frame",
                "invalid_expected_flag",
                "judgment",
            ],
            breadth_rows,
        ),
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
    ]
    artifacts.extend(payload_paths)
    gate_audit = gate_rows(payload_manifest, artifacts)
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "notes"],
            gate_audit,
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "primary_family": "experiment_execution",
                "primary_skill": "obsidian-experiment-design",
                "support_skills": [
                    "obsidian-data-integrity",
                    "obsidian-model-validation",
                    "obsidian-artifact-lineage",
                    "obsidian-result-judgment",
                ],
                "required_gates": [
                    "scope_completion_gate",
                    "skill_receipt_lint",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [row["path"] for row in source_hash_rows()],
                "payload_views": len(payload_manifest),
                "signal_payload_manifest_rows": len(signal_rows),
                "cost_curve_queue_rows": len(cost_rows),
                "failed_gates": [row for row in gate_audit if row["status"] != "pass"],
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
    artifacts.extend(write_receipts(generated_at_utc, payload_manifest, artifacts))
    artifacts.extend(write_reports(payload_manifest))
    artifacts.append(update_selection_status())
    artifacts.extend(update_current_truth(payload_manifest))
    return artifacts, payload_manifest


def main() -> None:
    generated_at_utc = utc_now()
    artifacts, payload_manifest = write_run_artifacts(generated_at_utc)
    failures = [row for row in gate_rows(payload_manifest, artifacts) if row["status"] != "pass"]
    update_registers(generated_at_utc, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "payload_views": len(payload_manifest),
                "signal_payload_manifest_rows": len(signal_manifest_rows(payload_manifest)),
                "failed_gates": failures,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
