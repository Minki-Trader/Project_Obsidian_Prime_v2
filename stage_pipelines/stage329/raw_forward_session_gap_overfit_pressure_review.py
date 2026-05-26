from __future__ import annotations

import argparse
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_NUMBER = "run329G"
RUN_ID = "run329G_raw_forward_session_gap_and_overfit_pressure_review_v1"
PARENT_RUN_ID = "run329F_forward_mt5_kpi_regime_cost_curve_review_v1"
STATUS = "completed_raw_forward_session_gap_and_overfit_pressure_review_no_forward_decision"
JUDGMENT = "raw_forward_gap_keeps_forward_decision_open_no_goal_achieve"
DECISION = "stage329G_session_parity_mt5_positive_but_raw_forward_gap_and_cp322a_handoff_unresolved"
NEXT_ACTION = "run329H_cp322A_exact_handoff_repair_feasibility_or_research_artifact_closeout"
CLAIM_BOUNDARY = (
    "research_development_only_raw_forward_session_gap_overfit_review_no_threshold_retuning_"
    "no_candidate_selection_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN329C_DIR = STAGE_DIR / "02_runs" / "run329C"
RUN329D_DIR = STAGE_DIR / "02_runs" / "run329D"
RUN329F_DIR = STAGE_DIR / "02_runs" / "run329F"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage329G_raw_forward_session_gap_overfit_review.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


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


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
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


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
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
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


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
    if path.exists():
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def to_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def safe_div(num: Any, den: Any) -> float | None:
    a = to_float(num)
    b = to_float(den)
    if a is None or b in {None, 0.0}:
        return None
    return a / b


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def load_prediction(slug: str, view: str) -> pd.DataFrame:
    path = RUN329D_DIR / "predictions" / f"{slug}_{view}_score.parquet"
    frame = pd.read_parquet(io_path(path))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return frame


def density_rows() -> pd.DataFrame:
    return load_csv(RUN329D_DIR / "density_shift_vs_oos.csv")


def mt5_kpi_rows() -> pd.DataFrame:
    return load_csv(RUN329F_DIR / "forward_mt5_kpi_report.csv")


def cost_rows() -> pd.DataFrame:
    return load_csv(RUN329F_DIR / "cost_stress_report.csv")


def curve_rows() -> pd.DataFrame:
    return load_csv(RUN329F_DIR / "curve_pocket_report.csv")


def candidate_screen() -> pd.DataFrame:
    return load_csv(RUN329C_DIR / "candidate_screen.csv")


def fixed_threshold_metrics() -> pd.DataFrame:
    return load_csv(RUN329C_DIR / "fixed_threshold_signal_metrics.csv")


def build_gap_rows() -> list[dict[str, Any]]:
    density = density_rows()
    kpi = mt5_kpi_rows()
    cost = cost_rows()
    curve = curve_rows()
    screen = candidate_screen()
    rows: list[dict[str, Any]] = []
    for slug in sorted(density["artifact_slug"].unique()):
        raw = density[(density["artifact_slug"] == slug) & (density["view_id"] == "raw_forward")].iloc[0].to_dict()
        session = density[(density["artifact_slug"] == slug) & (density["view_id"] == "old_session_parity")].iloc[0].to_dict()
        raw_pred = load_prediction(slug, "raw_forward")
        session_pred = load_prediction(slug, "old_session_parity")
        session_times = set(session_pred["timestamp"])
        exclusive = raw_pred.loc[~raw_pred["timestamp"].isin(session_times)]
        exclusive_signals = exclusive.loc[exclusive["signal"].astype(int).ne(0)]
        attempt_name = f"{slug}_sp"
        kpi_row = kpi.loc[kpi["artifact_slug"].eq(slug)].iloc[0].to_dict()
        cost_1 = cost[(cost["artifact_slug"] == slug) & (cost["extra_cost_per_round_trip_account_ccy"].astype(float) == 1.0)].iloc[0].to_dict()
        worst_rolling = curve[(curve["artifact_slug"] == slug) & (curve["chunk_type"] == "rolling_worst_net")]
        worst_third = curve[(curve["artifact_slug"] == slug) & (curve["chunk_type"] == "thirds")].sort_values("net_profit").head(1)
        screen_row = screen.loc[screen["artifact_slug"].eq(slug)].iloc[0].to_dict()
        rows.append(
            {
                "artifact_slug": slug,
                "candidate_id": raw["candidate_id"],
                "feature_set_id": raw["feature_set_id"],
                "model_id": raw["model_id"],
                "raw_rows": raw["rows"],
                "session_rows": session["rows"],
                "raw_session_row_ratio": safe_div(raw["rows"], session["rows"]),
                "raw_signals_per_day": raw["signals_per_day"],
                "session_signals_per_day": session["signals_per_day"],
                "raw_session_signal_per_day_ratio": safe_div(raw["signals_per_day"], session["signals_per_day"]),
                "raw_signal_rate": raw["signal_rate"],
                "session_signal_rate": session["signal_rate"],
                "raw_signal_rate_minus_session": (to_float(raw["signal_rate"]) or 0.0) - (to_float(session["signal_rate"]) or 0.0),
                "exclusive_raw_rows": int(exclusive.shape[0]),
                "exclusive_raw_signal_rows": int(exclusive_signals.shape[0]),
                "exclusive_raw_signal_rate": safe_div(exclusive_signals.shape[0], exclusive.shape[0]),
                "exclusive_raw_long_share": safe_div((exclusive_signals["signal_direction"].astype(int) > 0).sum(), exclusive_signals.shape[0]),
                "raw_long_share": raw["signal_long_share"],
                "session_long_share": session["signal_long_share"],
                "long_share_shift": (to_float(raw["signal_long_share"]) or 0.0) - (to_float(session["signal_long_share"]) or 0.0),
                "mt5_net": kpi_row.get("net_profit"),
                "mt5_pf": kpi_row.get("profit_factor"),
                "mt5_equity_dd_percent": kpi_row.get("equity_dd_percent"),
                "mt5_trades_per_day": kpi_row.get("trades_per_day"),
                "cost_1_net": cost_1.get("net_profit_after_cost"),
                "cost_1_pf": cost_1.get("profit_factor_after_cost"),
                "cost_1_survives_pf_gt_1": cost_1.get("survives_pf_gt_1"),
                "worst_rolling_net": None if worst_rolling.empty else worst_rolling.iloc[0].get("net_profit"),
                "worst_third_net": None if worst_third.empty else worst_third.iloc[0].get("net_profit"),
                "wfo_min_balanced_accuracy": screen_row.get("wfo_min_balanced_accuracy"),
                "wfo_std_balanced_accuracy": screen_row.get("wfo_std_balanced_accuracy"),
                "train_oos_balanced_accuracy_gap": screen_row.get("train_oos_balanced_accuracy_gap"),
            }
        )
    return rows


def classify_gap(row: Mapping[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    ratio = to_float(row.get("raw_session_signal_per_day_ratio")) or 0.0
    row_ratio = to_float(row.get("raw_session_row_ratio")) or 0.0
    exclusive_signal_rate = to_float(row.get("exclusive_raw_signal_rate")) or 0.0
    long_shift = abs(to_float(row.get("long_share_shift")) or 0.0)
    if ratio >= 3.0:
        reasons.append("raw_signal_density_explodes_vs_session")
    elif ratio >= 1.25:
        reasons.append("raw_signal_density_materially_above_session")
    if row_ratio >= 1.25:
        reasons.append("raw_row_supply_materially_above_session")
    if exclusive_signal_rate >= 0.25:
        reasons.append("exclusive_raw_rows_are_signal_dense")
    if long_shift >= 0.15:
        reasons.append("side_mix_shifts_between_raw_and_session")
    if not reasons:
        reasons.append("raw_session_gap_within_review_band")
        return "low", reasons
    if any(reason in reasons for reason in {"raw_signal_density_explodes_vs_session", "exclusive_raw_rows_are_signal_dense"}):
        return "high", reasons
    return "medium", reasons


def build_pressure_rows(gap_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    fixed = fixed_threshold_metrics()
    pressure_rows: list[dict[str, Any]] = []
    for row in gap_rows:
        slug = str(row["artifact_slug"])
        train = fixed[(fixed["artifact_slug"] == slug) & (fixed["split"] == "train")].iloc[0]
        val = fixed[(fixed["artifact_slug"] == slug) & (fixed["split"] == "validation")].iloc[0]
        oos = fixed[(fixed["artifact_slug"] == slug) & (fixed["split"] == "oos")].iloc[0]
        gap_level, gap_reasons = classify_gap(row)
        cost_survives = str(row.get("cost_1_survives_pf_gt_1")).lower() == "true"
        worst_third = to_float(row.get("worst_third_net")) or 0.0
        flags = list(gap_reasons)
        if (to_float(train.get("mean_proxy_log_return")) or 0.0) > 0 and (to_float(val.get("mean_proxy_log_return")) or 0.0) < 0:
            flags.append("train_validation_proxy_return_sign_flip")
        if not cost_survives:
            flags.append("fails_plus1_cost_stress")
        if worst_third < 0:
            flags.append("negative_curve_pocket_exists")
        if (to_float(row.get("mt5_pf")) or 0.0) <= 1.05:
            flags.append("session_mt5_pf_near_flat")
        score = pressure_score(flags)
        pressure_rows.append(
            {
                "artifact_slug": slug,
                "candidate_id": row["candidate_id"],
                "gap_level": gap_level,
                "pressure_score": score,
                "pressure_level": "high" if score >= 5 else "medium" if score >= 3 else "low",
                "pressure_flags": ";".join(flags),
                "train_signal_proxy_mean": train.get("mean_proxy_log_return"),
                "validation_signal_proxy_mean": val.get("mean_proxy_log_return"),
                "oos_signal_proxy_mean": oos.get("mean_proxy_log_return"),
                "session_mt5_net": row.get("mt5_net"),
                "session_mt5_pf": row.get("mt5_pf"),
                "cost_1_pf": row.get("cost_1_pf"),
                "worst_third_net": row.get("worst_third_net"),
                "raw_session_signal_per_day_ratio": row.get("raw_session_signal_per_day_ratio"),
                "exclusive_raw_signal_rate": row.get("exclusive_raw_signal_rate"),
                "claim_effect": "forward positive evidence is kept as research-only if pressure is medium/high",
            }
        )
    return pressure_rows


def pressure_score(flags: Sequence[str]) -> int:
    weights = {
        "raw_signal_density_explodes_vs_session": 3,
        "exclusive_raw_rows_are_signal_dense": 2,
        "raw_signal_density_materially_above_session": 1,
        "raw_row_supply_materially_above_session": 1,
        "side_mix_shifts_between_raw_and_session": 1,
        "train_validation_proxy_return_sign_flip": 1,
        "fails_plus1_cost_stress": 2,
        "negative_curve_pocket_exists": 1,
        "session_mt5_pf_near_flat": 2,
    }
    return sum(weights.get(flag, 0) for flag in flags)


def build_decision_payload(pressure_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    high = [row["artifact_slug"] for row in pressure_rows if row["pressure_level"] == "high"]
    medium = [row["artifact_slug"] for row in pressure_rows if row["pressure_level"] == "medium"]
    low = [row["artifact_slug"] for row in pressure_rows if row["pressure_level"] == "low"]
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "high_pressure": high,
        "medium_pressure": medium,
        "low_pressure": low,
        "research_read": (
            "Session-parity MT5 evidence is real, but raw-forward density and exclusive-row signal behavior "
            "show that the evidence cannot be promoted to Forward Passed yet."
        ),
        "next_action": NEXT_ACTION,
    }


def write_outputs(generated_at_utc: str) -> list[Path]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    SELECTED_DIR.mkdir(parents=True, exist_ok=True)
    gap_rows = build_gap_rows()
    pressure_rows = build_pressure_rows(gap_rows)
    decision_payload = build_decision_payload(pressure_rows)

    artifacts: list[Path] = []
    artifacts.append(
        write_csv(
            RUN_DIR / "raw_forward_session_gap_report.csv",
            [
                "artifact_slug",
                "candidate_id",
                "feature_set_id",
                "model_id",
                "raw_rows",
                "session_rows",
                "raw_session_row_ratio",
                "raw_signals_per_day",
                "session_signals_per_day",
                "raw_session_signal_per_day_ratio",
                "raw_signal_rate",
                "session_signal_rate",
                "raw_signal_rate_minus_session",
                "exclusive_raw_rows",
                "exclusive_raw_signal_rows",
                "exclusive_raw_signal_rate",
                "exclusive_raw_long_share",
                "raw_long_share",
                "session_long_share",
                "long_share_shift",
                "mt5_net",
                "mt5_pf",
                "mt5_equity_dd_percent",
                "cost_1_net",
                "cost_1_pf",
                "cost_1_survives_pf_gt_1",
                "worst_rolling_net",
                "worst_third_net",
                "wfo_min_balanced_accuracy",
                "wfo_std_balanced_accuracy",
                "train_oos_balanced_accuracy_gap",
            ],
            gap_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "overfit_pressure_report.csv",
            [
                "artifact_slug",
                "candidate_id",
                "gap_level",
                "pressure_score",
                "pressure_level",
                "pressure_flags",
                "train_signal_proxy_mean",
                "validation_signal_proxy_mean",
                "oos_signal_proxy_mean",
                "session_mt5_net",
                "session_mt5_pf",
                "cost_1_pf",
                "worst_third_net",
                "raw_session_signal_per_day_ratio",
                "exclusive_raw_signal_rate",
                "claim_effect",
            ],
            pressure_rows,
        )
    )
    artifacts.append(write_json(RUN_DIR / "final_forward_decision.json", decision_payload))
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "status": "completed",
                "overfit_pressure_report": rel(artifacts[1]),
                "raw_session_gap_report": rel(artifacts[0]),
                "validation_boundary": "no threshold retuning; no candidate selection; pressure flags only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            ["run_id", "status", "judgment", "decision", "forward_passed", "forward_failed", "goal_achieve", "next_action", "claim_boundary"],
            [{**decision_payload, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY}],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate_name", "status", "evidence_path", "effect"],
            [
                {
                    "gate_name": "data_integrity(데이터 무결성)",
                    "status": "completed_with_gap_warning",
                    "evidence_path": rel(artifacts[0]),
                    "effect": "raw_forward(원본 전진)와 old_session_parity(기존 세션 동등)의 행/신호 공급 차이를 분리한다.",
                },
                {
                    "gate_name": "model_validation(모델 검증)",
                    "status": "completed",
                    "evidence_path": rel(artifacts[1]),
                    "effect": "과적합 압력 신호를 수익성 주장과 분리한다.",
                },
                {
                    "gate_name": "result_judgment(결과 판정)",
                    "status": "passed_no_goal_achieve",
                    "evidence_path": rel(artifacts[4]),
                    "effect": "Forward Passed(전진 통과), Forward Failed(전진 실패), Goal Achieve(목표 달성)를 주장하지 않는다.",
                },
            ],
        )
    )
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    artifacts.append(write_json(RUN_DIR / "run_manifest.json", {"stage_id": STAGE_ID, "run_id": RUN_ID, "run_number": RUN_NUMBER, "parent_run_id": PARENT_RUN_ID, "generated_at_utc": generated_at_utc, **decision_payload, "claim_boundary": CLAIM_BOUNDARY}))
    artifacts.extend(write_reports(gap_rows, pressure_rows, decision_payload))
    artifacts.append(update_selection_status(decision_payload))
    artifacts.extend(update_current_truth(decision_payload))
    update_registers(generated_at_utc, decision_payload, artifacts)
    return artifacts


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        RUN329D_DIR / "density_shift_vs_oos.csv",
        RUN329D_DIR / "forward_score_summary.csv",
        RUN329D_DIR / "predictions",
        RUN329C_DIR / "candidate_screen.csv",
        RUN329C_DIR / "fixed_threshold_signal_metrics.csv",
        RUN329F_DIR / "forward_mt5_kpi_report.csv",
        RUN329F_DIR / "cost_stress_report.csv",
        RUN329F_DIR / "curve_pocket_report.csv",
    ]
    all_paths = list(dict.fromkeys([*artifacts, Path(__file__)]))
    return {
        "generated_at_utc": generated_at_utc,
        "source_inputs": [rel(path) for path in inputs],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in all_paths if path.exists()],
        "artifact_hashes": {rel(path): sha256_file(path) for path in all_paths if path.exists() and path.is_file()},
        "lineage_judgment": "connected_with_raw_forward_gap_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_reports(gap_rows: Sequence[Mapping[str, Any]], pressure_rows: Sequence[Mapping[str, Any]], decision_payload: Mapping[str, Any]) -> list[Path]:
    pressure_by_slug = {row["artifact_slug"]: row for row in pressure_rows}
    table_lines = [
        "| artifact(산출물) | pressure(압력) | raw/session signal ratio(원본/세션 신호 비율) | exclusive signal rate(전용 원본 신호율) | MT5 PF(MT5 수익 팩터) | cost+1 PF(비용+1 수익 팩터) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(gap_rows, key=lambda item: pressure_by_slug[item["artifact_slug"]]["pressure_score"], reverse=True):
        pressure = pressure_by_slug[row["artifact_slug"]]
        table_lines.append(
            f"| {row['artifact_slug']} | {pressure['pressure_level']}:{pressure['pressure_score']} | {csv_value(row['raw_session_signal_per_day_ratio'])} | {csv_value(row['exclusive_raw_signal_rate'])} | {csv_value(row['mt5_pf'])} | {csv_value(row['cost_1_pf'])} |"
        )
    report = write_md(
        REVIEWS_DIR / "run329G_raw_forward_session_gap_overfit_review.md",
        f"""
# run329G Raw Forward Session Gap Overfit Review(329G 원본 전진 세션 간극/과적합 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Pressure Table(압력 표)

{chr(10).join(table_lines)}

## Read(판독)

- high_pressure(높은 압력): `{', '.join(decision_payload['high_pressure']) or 'none'}`
- medium_pressure(중간 압력): `{', '.join(decision_payload['medium_pressure']) or 'none'}`
- low_pressure(낮은 압력): `{', '.join(decision_payload['low_pressure']) or 'none'}`
- effect(효과): session-parity MT5(세션 동등 MT5) 양수 근거가 있어도 raw_forward(원본 전진) 공급 구조가 다르면 Forward Passed(전진 통과)로 닫지 않는다.

## Next(다음)

`{NEXT_ACTION}`
""",
    )
    decision_doc = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage329G Raw Forward Session Gap Overfit Review Decision(329G 원본 전진 세션 간극/과적합 검토 결정)

- decision(결정): `{decision_payload['decision']}`
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): 세션 동등 MT5 결과를 인정하되, 원본 전진 세션 간극과 cp322A handoff(인계) 미해결 때문에 최종 전진 판정을 열어 둔다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    return [report, decision_doc]


def update_selection_status(decision_payload: Mapping[str, Any]) -> Path:
    return write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage329 Selection Status(329단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- research_onnx_status(연구 온엑스 상태): `raw_forward_session_gap_overfit_pressure_review_completed_no_selection`
- latest_runtime_probe(최신 런타임 탐침): `run329E_session_parity_forward_signal_payload_and_mt5_runtime_probe_v1`
- latest_forward_review(최신 전진 검토): `{RUN_ID}`
- high_pressure(높은 압력): `{', '.join(decision_payload['high_pressure']) or 'none'}`
- medium_pressure(중간 압력): `{', '.join(decision_payload['medium_pressure']) or 'none'}`
- low_pressure(낮은 압력): `{', '.join(decision_payload['low_pressure']) or 'none'}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): 원본 전진 간극과 과적합 압력을 확인했기 때문에 후보 선택이나 전진 통과 주장은 아직 없다.
""",
    )


def update_current_truth(decision_payload: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage329(329단계) run329G(329G 실행) raw-forward/session gap review(원본 전진/세션 간극 검토)를 `{decision_payload['status']}`로 닫았다. "
        "Effect(효과): 세션 동등 MT5 양수 근거를 전진 통과로 올리지 않고 과적합 압력으로 보존한다.\n"
    )
    if "Stage329(329단계) run329G(329G 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v7`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `raw_forward_session_gap_overfit_pressure_review`",
        "- status(": f"- status(상태): `{decision_payload['status']}`",
        "- decision(": f"- decision(판정): `{decision_payload['judgment']}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    current_text = replace_prefix_line(
        current_text,
        "- run329E_summary(329E 요약):",
        "- run329E_summary(329E 요약): session parity runtime probe(세션 동등 런타임 탐침)를 `completed_session_parity_runtime_probe_no_candidate_selection`로 다시 닫았다. Effect(효과): portable MT5(포터블 메타트레이더5)로 6/6 runtime/report/telemetry(런타임/보고서/실행 기록)를 확보했지만 selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.",
    )
    summary = (
        f"- run329G_summary(329G 요약): raw-forward/session gap and overfit pressure review(원본 전진/세션 간극 및 과적합 압력 검토)를 `{decision_payload['status']}`로 닫았다. "
        "Effect(효과): session-parity MT5(세션 동등 MT5) 성과는 연구 근거로 보존하지만 raw_forward(원본 전진) 공급 간극 때문에 Forward Passed(전진 통과)는 없다."
    )
    if "run329G_summary(329G 요약)" not in current_text:
        current_text = current_text.replace(f"- decision(판정): `{decision_payload['judgment']}`\n", f"- decision(판정): `{decision_payload['judgment']}`\n{summary}\n", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)
    append_if_missing(
        CHANGELOG,
        "Stage329G Raw Forward Session Gap Overfit Review",
        f"""
## 2026-05-26 - Stage329G Raw Forward Session Gap Overfit Review(329G 원본 전진 세션 간극/과적합 검토)

- run329G(329G 실행): raw_forward(원본 전진)와 old_session_parity(기존 세션 동등)의 행/신호 간극, exclusive raw signal(원본 전용 신호), 비용/곡선 취약성을 합쳐 과적합 압력을 기록했다.
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- effect(효과): Forward Passed(전진 통과), Forward Failed(전진 실패), selected candidate(선택 후보), Goal Achieve(목표 달성)를 주장하지 않는다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, decision_payload: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run329G_raw_forward_session_gap_overfit_review.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "model_validation",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "path": rel(report_path),
                "notes": "raw_forward_session_gap;overfit_pressure;no_selection;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__raw_forward_gap_overfit_pressure",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "raw_forward_gap_overfit_pressure",
                "tier_scope": "forward raw + old-session parity",
                "kpi_scope": "signal_density_cost_curve_pressure",
                "scoreboard_lane": "model_validation",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "path": rel(report_path),
                "primary_kpi": "raw_session_signal_per_day_ratio",
                "guardrail_kpi": "exclusive_raw_signal_rate;cost_stress;curve_pocket",
                "external_verification_status": "uses_completed_run329E_mt5_and_run329D_forward_scores",
                "notes": f"decision={decision_payload['decision']};next_action={NEXT_ACTION}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__raw_forward_gap_overfit_pressure",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "raw_forward_gap_overfit_pressure(원본 전진 간극/과적합 압력)",
                "tier_scope": "forward raw + old-session parity(전진 원본 + 기존 세션 동등)",
                "scoreboard": "signal_density_cost_curve_pressure(신호 밀도/비용/곡선 압력)",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": decision_payload["decision"],
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        if path.exists() and path.is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(path)}",
                    "artifact_type": "stage329G_raw_forward_gap_artifact",
                    "path": rel(path),
                    "sha256": sha256_file(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "raw-forward session gap and overfit pressure artifact; no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage329G raw-forward session gap and overfit pressure review.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "artifact_count": len(artifacts),
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
