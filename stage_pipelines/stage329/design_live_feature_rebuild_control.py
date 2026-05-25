from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_ID = "run329A_design_live_feature_rebuild_control_after_cp322a_block_v1"
RUN_NUMBER = "run329A"
STATUS = "completed_live_feature_rebuild_control_design_ready_for_materialization"
JUDGMENT = "research_rebuild_control_open_no_goal_achieve"
DECISION = "stage329_opened_live_feature_forward_rebuild_control_no_candidate_selected"
NEXT_ACTION = "run329B_parameterize_forward_feature_materializer_and_build_live_feature_frames"
CLAIM_BOUNDARY = (
    "research_development_only_no_new_data_tuning_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

STAGE328_DIR = ROOT / "stages" / "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
STAGE328_RUN_B = STAGE328_DIR / "02_runs" / "run328B"
STAGE328_DECISION = STAGE328_DIR / "03_reviews" / "final_stage328B_decision_report.md"
STAGE328_REBUILD_QUEUE = STAGE328_RUN_B / "rebuild_option_queue.csv"
STAGE328_FEATURE_MATRIX = STAGE328_RUN_B / "feature_live_rebuild_matrix.csv"

STAGE326_FORWARD = ROOT / "stages" / "326_forward__cp322a_frozen_forward_gate"
FORWARD_RAW_SUMMARY = STAGE326_FORWARD / "01_inputs" / "raw_m5" / "stage01_raw_export_summary.json"
FORWARD_DECISION = STAGE326_FORWARD / "03_reviews" / "final_forward_decision_report.md"

MODEL_INPUT_ROOT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
MODEL_INPUT_SUMMARY = MODEL_INPUT_ROOT / "model_input_summary.json"
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_ROOT / "model_input_feature_order.txt"
TRAINING_SUMMARY = (
    ROOT
    / "data"
    / "processed"
    / "training_datasets"
    / "label_v1_fwd12_split_v1_proxyw58"
    / "training_dataset_summary.json"
)
TOP3_PRICE_PROXY_WEIGHTS = ROOT / "foundation" / "config" / "top3_monthly_price_proxy_weights_fpmarkets_v2.csv"
FEATURE_MATERIALIZER = ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_dataset.py"
LABEL_MATERIALIZER = ROOT / "foundation" / "pipelines" / "materialize_training_label_split_dataset.py"
MODEL_INPUT_MATERIALIZER = ROOT / "foundation" / "pipelines" / "materialize_model_input_dataset.py"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

CORE58_FORBIDDEN_PREFIXES = ("stage316_", "stage317_")
RESEARCH_SCORE_FEATURES = {
    "payoff_edge_score",
    "anti_meta_score",
    "profit_quality_score",
    "density_head_score",
    "runtime_calibration_score",
    "profit_scale_score",
    "smooth_curve_score",
    "anti_regime_flag",
    "smooth_regime_flag",
    "precondition_pass",
    "source_code",
    "hyp_signal",
}
EQUITY_PREFIXES = (
    "nvda_",
    "aapl_",
    "msft_",
    "amzn_",
    "mega8_",
    "top3_",
    "us100_minus_mega8_",
    "us100_minus_top3_",
)
TOP3_FEATURES = {"top3_weighted_return_1", "us100_minus_top3_weighted_return_1"}
MACRO_PREFIXES = ("vix_", "us10yr_", "usdx_")
REQUIRED_CORE58_SYMBOLS = {
    "US100",
    "VIX",
    "US10YR",
    "USDX",
    "NVDA",
    "AAPL",
    "MSFT",
    "AMZN",
    "AMD",
    "GOOGL.xnas",
    "META",
    "TSLA",
}
REQUIRED_MACRO48_SYMBOLS = {"US100", "VIX", "US10YR", "USDX"}


def os_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return os_path(path).exists()


def read_text(path: Path) -> str:
    return os_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    os_path(path).write_text(text, encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, data: Any) -> Path:
    return write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    with os_path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
    h = hashlib.sha256()
    with os_path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    rows: list[dict[str, str]] = []
    if path_exists(path):
        with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or row.keys())
            rows = list(reader)
    else:
        fieldnames = list(row.keys())
    for name in row:
        if name not in fieldnames:
            fieldnames.append(name)
    clean_row = {name: str(row.get(name, "")) for name in fieldnames}
    replaced = False
    for idx, existing in enumerate(rows):
        if existing.get(key) == clean_row.get(key):
            rows[idx] = clean_row
            replaced = True
            break
    if not replaced:
        rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def upsert_many_csv(path: Path, key: str, new_rows: list[dict[str, Any]]) -> None:
    rows: list[dict[str, str]] = []
    if path_exists(path):
        with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    else:
        fieldnames = []
    for row in new_rows:
        for name in row:
            if name not in fieldnames:
                fieldnames.append(name)
    if not fieldnames and new_rows:
        fieldnames = list(new_rows[0].keys())
    keyed: dict[str, dict[str, str]] = {existing.get(key, ""): existing for existing in rows}
    order: list[str] = [existing.get(key, "") for existing in rows]
    for row in new_rows:
        clean_row = {name: str(row.get(name, "")) for name in fieldnames}
        row_key = clean_row.get(key, "")
        if row_key not in keyed:
            order.append(row_key)
        keyed[row_key] = clean_row
    merged = [keyed[row_key] for row_key in order if row_key in keyed]
    write_csv(path, fieldnames, merged)


def replace_or_append_csv_rows(path: Path, keys: list[str], new_rows: list[dict[str, Any]]) -> None:
    rows: list[dict[str, str]] = []
    if path_exists(path):
        with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    else:
        fieldnames = []
    for row in new_rows:
        for name in row:
            if name not in fieldnames:
                fieldnames.append(name)
    if not fieldnames and new_rows:
        fieldnames = list(new_rows[0].keys())
    for row in new_rows:
        clean_row = {name: str(row.get(name, "")) for name in fieldnames}
        replaced = False
        for idx, existing in enumerate(rows):
            if all(existing.get(key, "") == clean_row.get(key, "") for key in keys):
                rows[idx] = clean_row
                replaced = True
                break
        if not replaced:
            rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = os_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    write_text(path, text, encoding=encoding)


def append_text_if_missing(path: Path, marker: str, entry: str) -> None:
    raw = os_path(path).read_bytes() if path_exists(path) else b""
    if marker.encode("utf-8") in raw:
        return
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    suffix = entry.encode("utf-8")
    if raw and not raw.endswith((b"\n", b"\r")):
        raw += b"\n"
    os_path(path).write_bytes(raw.rstrip() + suffix)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def unix_to_iso(value: int | str | None) -> str:
    if value in (None, ""):
        return ""
    return datetime.fromtimestamp(int(value), timezone.utc).isoformat().replace("+00:00", "Z")


def read_feature_order() -> list[str]:
    return [line.strip() for line in read_text(MODEL_INPUT_FEATURE_ORDER).splitlines() if line.strip()]


def feature_order_hash(features: list[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def csv_time_stats(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"exists": False}
    count = 0
    first_open: int | None = None
    last_open: int | None = None
    duplicates = 0
    non_monotonic = 0
    largest_gap_seconds = 0
    previous: int | None = None
    seen: set[int] = set()
    with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            count += 1
            ts = int(row["time_open_unix"])
            if first_open is None:
                first_open = ts
            last_open = ts
            if ts in seen:
                duplicates += 1
            seen.add(ts)
            if previous is not None:
                if ts <= previous:
                    non_monotonic += 1
                largest_gap_seconds = max(largest_gap_seconds, ts - previous)
            previous = ts
    return {
        "exists": True,
        "csv_row_count": count,
        "first_open_unix": first_open,
        "last_open_unix": last_open,
        "first_open_utc": unix_to_iso(first_open),
        "last_open_utc": unix_to_iso(last_open),
        "last_close_utc": unix_to_iso(last_open + 300 if last_open is not None else None),
        "duplicate_open_times": duplicates,
        "non_monotonic_steps": non_monotonic,
        "largest_gap_seconds": largest_gap_seconds,
    }


def load_forward_coverage() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    summary = read_json(FORWARD_RAW_SUMMARY)
    requested_to_unix = int(datetime.fromisoformat(summary["requested_to_utc"].replace("Z", "+00:00")).timestamp())
    rows: list[dict[str, Any]] = []
    common_core58_last_close: int | None = None
    common_macro48_last_close: int | None = None
    for item in summary["exported_symbols"]:
        symbol = str(item["contract_symbol"])
        csv_path = Path(item["csv_path"])
        manifest_path = Path(item["manifest_path"])
        manifest = read_json(manifest_path)
        stats = csv_time_stats(csv_path)
        last_open = int(item["last_open_unix"]) if item.get("last_open_unix") else None
        last_close = last_open + 300 if last_open is not None else None
        end_gap_hours = (requested_to_unix - last_open) / 3600 if last_open is not None else None
        required_core58 = symbol in REQUIRED_CORE58_SYMBOLS
        required_macro48 = symbol in REQUIRED_MACRO48_SYMBOLS
        if required_core58 and last_close is not None:
            common_core58_last_close = last_close if common_core58_last_close is None else min(common_core58_last_close, last_close)
        if required_macro48 and last_close is not None:
            common_macro48_last_close = last_close if common_macro48_last_close is None else min(common_macro48_last_close, last_close)
        if end_gap_hours is None:
            readiness = "missing"
        elif end_gap_hours <= 24:
            readiness = "covers_requested_end"
        elif symbol in REQUIRED_CORE58_SYMBOLS.difference(REQUIRED_MACRO48_SYMBOLS):
            readiness = "requires_equity_session_calendar_or_common_ready_end_trim"
        else:
            readiness = "incomplete"
        rows.append(
            {
                "symbol": symbol,
                "broker_symbol": item.get("broker_symbol"),
                "required_for_core58": "yes" if required_core58 else "no",
                "required_for_macro48": "yes" if required_macro48 else "no",
                "row_count_summary": item.get("row_count"),
                "row_count_csv": stats.get("csv_row_count"),
                "first_open_utc": unix_to_iso(item.get("first_open_unix")),
                "last_open_utc": unix_to_iso(item.get("last_open_unix")),
                "last_close_utc": unix_to_iso(last_close),
                "requested_to_utc": summary["requested_to_utc"],
                "end_gap_hours": "" if end_gap_hours is None else round(end_gap_hours, 2),
                "feature_rebuild_readiness": readiness,
                "timezone_status": manifest.get("timezone_status", ""),
                "duplicate_open_times": stats.get("duplicate_open_times", ""),
                "non_monotonic_steps": stats.get("non_monotonic_steps", ""),
                "largest_gap_seconds": stats.get("largest_gap_seconds", ""),
                "csv_path": rel(csv_path),
                "manifest_path": rel(manifest_path),
            }
        )
    summary_out = {
        "requested_from_utc": summary["requested_from_utc"],
        "requested_to_utc": summary["requested_to_utc"],
        "core58_common_ready_end_utc": unix_to_iso(common_core58_last_close),
        "macro48_common_ready_end_utc": unix_to_iso(common_macro48_last_close),
        "raw_summary_sha256": sha256_file(FORWARD_RAW_SUMMARY),
    }
    return rows, summary_out


def top3_weight_months() -> dict[str, Any]:
    rows = read_csv(TOP3_PRICE_PROXY_WEIGHTS)
    months = [row.get("month", "") for row in rows if row.get("month")]
    return {
        "min_month": min(months) if months else "",
        "max_month": max(months) if months else "",
        "row_count": len(rows),
        "sha256": sha256_file(TOP3_PRICE_PROXY_WEIGHTS),
    }


def split_feature_sets(features: list[str]) -> dict[str, list[str]]:
    core58 = list(features)
    core56 = [name for name in features if name not in TOP3_FEATURES]
    macro48 = [
        name
        for name in features
        if not name.startswith(EQUITY_PREFIXES) and name not in TOP3_FEATURES
    ]
    us100_technical42 = [
        name
        for name in macro48
        if not name.startswith(MACRO_PREFIXES)
    ]
    return {
        "core58_full_contract": core58,
        "core56_no_top3_weight_features": core56,
        "macro48_no_equity_breadth_or_top3": macro48,
        "us100_technical42_no_external": us100_technical42,
    }


def build_feature_set_matrix(features: list[str], weight_info: dict[str, Any], forward_summary: dict[str, Any]) -> list[dict[str, Any]]:
    sets = split_feature_sets(features)
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "feature_set_id": "core56_no_top3_weight_features",
            "feature_count": len(sets["core56_no_top3_weight_features"]),
            "feature_order_hash": feature_order_hash(sets["core56_no_top3_weight_features"]),
            "input_dependency": "US100+VIX+US10YR+USDX+mega8 equities; no top3 monthly weights",
            "forward_data_boundary": f"common_ready_end={forward_summary['core58_common_ready_end_utc']}",
            "status": "preferred_first_materialization_control",
            "anti_overfit_reason": "removes 2026-05 missing top3 weight contract while preserving broad live-computable context",
        }
    )
    rows.append(
        {
            "feature_set_id": "macro48_no_equity_breadth_or_top3",
            "feature_count": len(sets["macro48_no_equity_breadth_or_top3"]),
            "feature_order_hash": feature_order_hash(sets["macro48_no_equity_breadth_or_top3"]),
            "input_dependency": "US100+VIX+US10YR+USDX only",
            "forward_data_boundary": f"common_ready_end={forward_summary['macro48_common_ready_end_utc']}",
            "status": "parallel_resilience_control",
            "anti_overfit_reason": "tests whether external equity breadth dependency is required or merely overfit-supporting context",
        }
    )
    rows.append(
        {
            "feature_set_id": "us100_technical42_no_external",
            "feature_count": len(sets["us100_technical42_no_external"]),
            "feature_order_hash": feature_order_hash(sets["us100_technical42_no_external"]),
            "input_dependency": "US100 OHLC/session only",
            "forward_data_boundary": f"requested_to={read_json(FORWARD_RAW_SUMMARY)['requested_to_utc']}",
            "status": "minimal_parity_control",
            "anti_overfit_reason": "lowest dependency feature set for Python/MT5 parity and failure isolation",
        }
    )
    rows.append(
        {
            "feature_set_id": "core58_full_contract",
            "feature_count": len(sets["core58_full_contract"]),
            "feature_order_hash": feature_order_hash(sets["core58_full_contract"]),
            "input_dependency": "US100+VIX+US10YR+USDX+mega8 equities+top3 monthly weights",
            "forward_data_boundary": f"top3_weights_max_month={weight_info['max_month']}",
            "status": "blocked_until_2026_05_weight_contract_or_no_top3_variant",
            "anti_overfit_reason": "do not infer 2026-05 top3 weights dynamically at runtime",
        }
    )
    return rows


def build_materializer_gap_rows(weight_info: dict[str, Any]) -> list[dict[str, Any]]:
    materializer_text = read_text(FEATURE_MATERIALIZER)
    return [
        {
            "gap_id": "feature_materializer_window_hardcoded",
            "evidence": "WINDOW_END_UTC = 2026-04-13" if "WINDOW_END_UTC = pd.Timestamp(\"2026-04-13" in materializer_text else "not_detected",
            "status": "requires_parameterization_or_stage_wrapper",
            "effect": "forward raw data after 2026-04-14 would be filtered out by the current foundation materializer.",
            "next_repair": "add explicit --window-start/--window-end/--dataset-id support without changing old default behavior",
        },
        {
            "gap_id": "top3_weight_contract_missing_2026_05",
            "evidence": f"max_month={weight_info['max_month']}; path={rel(TOP3_PRICE_PROXY_WEIGHTS)}",
            "status": "blocks_core58_may_rows",
            "effect": "core58 top3 features cannot be computed through May without an approved weight policy.",
            "next_repair": "use core56 no-top3 control first, or create a separate 2026-05 weight contract before core58",
        },
        {
            "gap_id": "forward_equity_calendar_alignment",
            "evidence": "equity symbols end before requested_to while US100 continues",
            "status": "requires_common_ready_end_or_market_calendar_binding",
            "effect": "exact external alignment will invalidate rows after equity common close unless a contract says otherwise.",
            "next_repair": "materialize both common-ready-end core56 and macro48 controls",
        },
        {
            "gap_id": "label_threshold_policy",
            "evidence": rel(TRAINING_SUMMARY),
            "status": "train_only_threshold_available",
            "effect": "labels can remain train-threshold based; forward rows must stay unlabeled until judgment-only replay.",
            "next_repair": "keep forward holdout untouched for final robustness checks",
        },
    ]


def build_anti_overfit_rows() -> list[dict[str, Any]]:
    return [
        {
            "control_id": "no_cp322a_repair_tuning",
            "rule": "Do not adjust cp322A threshold, D/B surface, lot, ATR, or runtime logic.",
            "effect": "prevents a failed frozen artifact from being silently repaired into a different artifact.",
        },
        {
            "control_id": "no_outcome_distillation_features",
            "rule": "Reject Stage316/317 scores, source_code, hyp_signal, and actual MT5 net_profit labels as model inputs.",
            "effect": "removes the Stage318 overfit path found in run328B.",
        },
        {
            "control_id": "train_only_thresholds",
            "rule": "Classification thresholds and label thresholds come from train split only; validation/OOS/forward cannot set them.",
            "effect": "stops forward or OOS data from becoming calibration data.",
        },
        {
            "control_id": "rolling_wfo_before_onnx",
            "rule": "Any candidate must survive rolling WFO and split pocket checks before ONNX packaging.",
            "effect": "single-split success cannot become model authority.",
        },
        {
            "control_id": "parity_first_materialization",
            "rule": "Build feature frames with hashes and feature order before training or MT5 claims.",
            "effect": "prevents Python model outputs from drifting away from runtime inputs.",
        },
        {
            "control_id": "untouched_forward_holdout",
            "rule": "2026-04-14+ data is used first for feature readiness and final forward checks, not for selecting thresholds.",
            "effect": "preserves the forward robustness question.",
        },
    ]


def build_rebuild_queue(feature_set_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run329B_core56_forward_feature_frame",
            "priority": 1,
            "action": "parameterize materializer and build core56 forward feature frame",
            "feature_set_id": "core56_no_top3_weight_features",
            "success_gate": "feature_order_hash fixed; no missing external rows before common-ready-end; no labels used for selection",
            "blocked_if": "materializer cannot preserve old outputs by default",
        },
        {
            "queue_id": "run329B_macro48_forward_feature_frame",
            "priority": 2,
            "action": "build macro48 forward feature frame as lower-dependency control",
            "feature_set_id": "macro48_no_equity_breadth_or_top3",
            "success_gate": "US100/VIX/US10YR/USDX exact timestamp alignment passes",
            "blocked_if": "regime symbols have unresolved timestamp binding",
        },
        {
            "queue_id": "run329C_train_wfo_rebuild_candidates",
            "priority": 3,
            "action": "train small ONNX-friendly models using old train/validation/OOS only",
            "feature_set_id": "core56 and macro48",
            "success_gate": "rolling WFO, split pocket, class balance, calibration, and parity receipts exist",
            "blocked_if": "feature materialization or label boundary fails",
        },
        {
            "queue_id": "run329D_forward_holdout_replay",
            "priority": 4,
            "action": "score untouched forward holdout after fixed train/WFO selection",
            "feature_set_id": "survivor only",
            "success_gate": "forward result exists without threshold retuning",
            "blocked_if": "no survivor or no MT5/runtime handoff parity",
        },
    ]


def build_reports(
    generated_at_utc: str,
    features: list[str],
    weight_info: dict[str, Any],
    forward_rows: list[dict[str, Any]],
    forward_summary: dict[str, Any],
    feature_set_rows: list[dict[str, Any]],
    materializer_gap_rows: list[dict[str, Any]],
    anti_overfit_rows: list[dict[str, Any]],
    rebuild_queue: list[dict[str, Any]],
) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            SPEC_DIR / "stage_brief.md",
            f"""
# Stage329 Live Feature Rebuild Control(329단계 실시간 피처 재구축 대조)

- active_question(활성 질문): cp322A(322A 후보)의 overfit/parity blocker(과적합/동등성 차단)를 고치기 위해, outcome distillation(결과 증류)과 split-local rank(분할 내부 순위)를 제거한 live-computable feature(실시간 계산 가능 피처) 기반 ONNX 연구 경로를 만들 수 있는가?
- source_blocker(원천 차단): Stage328B(328B 단계 실행)는 cp318A outcome source(cp318A 결과 원천)가 forward authority(전진 권한)가 아니라고 판정했다.
- stage_boundary(단계 경계): cp322A frozen artifact(고정 산출물)는 보존한다. 이 단계는 cp322A tuning(튜닝)이 아니라 rebuild-control(재구축 대조) 설계와 materialization readiness(물질화 준비도)를 만든다.
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_md(
            INPUTS_DIR / "input_refs.md",
            f"""
# Stage329 Input References(329단계 입력 참조)

- generated_at_utc(생성 시각): `{generated_at_utc}`
- stage328_decision(328단계 결정): `{rel(STAGE328_DECISION)}`
- stage328_rebuild_queue(328단계 재구축 대기열): `{rel(STAGE328_REBUILD_QUEUE)}`
- stage328_feature_matrix(328단계 피처 행렬): `{rel(STAGE328_FEATURE_MATRIX)}`
- forward_raw_summary(전진 원천 요약): `{rel(FORWARD_RAW_SUMMARY)}`
- forward_decision(전진 판정): `{rel(FORWARD_DECISION)}`
- old_model_input_summary(기존 모델 입력 요약): `{rel(MODEL_INPUT_SUMMARY)}`
- old_feature_order(기존 피처 순서): `{rel(MODEL_INPUT_FEATURE_ORDER)}`
- top3_weights(상위3 가중치): `{rel(TOP3_PRICE_PROXY_WEIGHTS)}`
- feature_materializer(피처 물질화기): `{rel(FEATURE_MATERIALIZER)}`

Effect(효과): Stage329(329단계)는 기존 forward raw data(전진 원천 데이터)와 기존 clean 58 feature contract(깨끗한 58개 피처 계약)를 사용하지만, cp322A threshold(임계값)나 D/B rule(D/B 규칙)은 건드리지 않는다.
""",
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "forward_raw_coverage_audit.csv",
            [
                "symbol",
                "broker_symbol",
                "required_for_core58",
                "required_for_macro48",
                "row_count_summary",
                "row_count_csv",
                "first_open_utc",
                "last_open_utc",
                "last_close_utc",
                "requested_to_utc",
                "end_gap_hours",
                "feature_rebuild_readiness",
                "timezone_status",
                "duplicate_open_times",
                "non_monotonic_steps",
                "largest_gap_seconds",
                "csv_path",
                "manifest_path",
            ],
            forward_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "live_feature_set_design_matrix.csv",
            [
                "feature_set_id",
                "feature_count",
                "feature_order_hash",
                "input_dependency",
                "forward_data_boundary",
                "status",
                "anti_overfit_reason",
            ],
            feature_set_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "materializer_gap_audit.csv",
            ["gap_id", "evidence", "status", "effect", "next_repair"],
            materializer_gap_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "anti_overfit_control_spec.csv",
            ["control_id", "rule", "effect"],
            anti_overfit_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "rebuild_run_queue.csv",
            ["queue_id", "priority", "action", "feature_set_id", "success_gate", "blocked_if"],
            rebuild_queue,
        )
    )
    artifacts.append(
        write_md(
            REVIEWS_DIR / "run329A_live_feature_rebuild_control_design.md",
            f"""
# run329A Live Feature Rebuild Control Design(329A 실시간 피처 재구축 대조 설계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## Why this stage exists(이 단계가 필요한 이유)

Stage328B(328B 단계 실행)는 cp318A(318A 후보)가 Stage317 validation+OOS(검증+표본외) 실제 MT5 손익을 학습한 outcome distillation(결과 증류)이라고 판정했다. 따라서 cp322A(322A 후보)를 forward(전진)에 억지로 통과시키는 대신, raw/live-computable feature(원천/실시간 계산 가능 피처)만 쓰는 rebuild-control(재구축 대조)을 새 단계로 연다.

## Data Readiness(데이터 준비도)

- forward_raw_requested(전진 원천 요청): `{forward_summary['requested_from_utc']}` to `{read_json(FORWARD_RAW_SUMMARY)['requested_to_utc']}`
- core58_common_ready_end(핵심58 공통 준비 종료): `{forward_summary['core58_common_ready_end_utc']}`
- macro48_common_ready_end(거시48 공통 준비 종료): `{forward_summary['macro48_common_ready_end_utc']}`
- top3_weight_month_coverage(상위3 가중치 월 범위): `{weight_info['min_month']}` to `{weight_info['max_month']}`

Effect(효과): forward raw data(전진 원천 데이터)는 존재하지만, core58(핵심58)은 2026-05 top3 weight contract(상위3 가중치 계약)과 equity session calendar(주식 세션 달력) 경계가 필요하다. 그래서 core56(상위3 제외)와 macro48(거시 전용)을 먼저 materialization control(물질화 대조)로 둔다.

## Feature Set Queue(피처 세트 대기열)

| feature_set(피처 세트) | count(수) | status(상태) | reason(이유) |
|---|---:|---|---|
| core56_no_top3_weight_features | {next(row['feature_count'] for row in feature_set_rows if row['feature_set_id'] == 'core56_no_top3_weight_features')} | preferred_first_materialization_control | May top3 weight(5월 상위3 가중치) 문제를 피한다. |
| macro48_no_equity_breadth_or_top3 | {next(row['feature_count'] for row in feature_set_rows if row['feature_set_id'] == 'macro48_no_equity_breadth_or_top3')} | parallel_resilience_control | 주식 바스켓 의존성을 줄인다. |
| us100_technical42_no_external | {next(row['feature_count'] for row in feature_set_rows if row['feature_set_id'] == 'us100_technical42_no_external')} | minimal_parity_control | Python/MT5 parity(파이썬/MT5 동등성) 격리 대조다. |
| core58_full_contract | {len(features)} | blocked | 2026-05 top3 weight contract(상위3 가중치 계약)이 없다. |

## Decision(결정)

Stage329(329단계)는 candidate selection(후보 선택)이 아니라 rebuild-control materialization(재구축 대조 물질화)로 열린다. 다음 실행은 `{NEXT_ACTION}`이다.

`{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_md(
            REVIEWS_DIR / "final_stage329A_decision_report.md",
            f"""
# Stage329A Final Decision(329A 최종 판정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A(322A 후보)를 수정하지 않고, outcome distillation(결과 증류)을 제거한 live feature rebuild control(실시간 피처 재구축 대조)을 새 Stage329(329단계)로 열었다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
        )
    )
    artifacts.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage329 Selection Status(329단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- package_queue(패키지 대기열): `core56_no_top3_weight_features`, `macro48_no_equity_breadth_or_top3`, `us100_technical42_no_external`
- core58_status(핵심58 상태): `blocked_until_2026_05_top3_weight_contract_or_no_top3_variant`
- forward_dataset_status(전진 데이터셋 상태): `raw_available_needs_parameterized_materializer_and_session_boundary`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): 과적합 수리(overfit repair, 과적합 수리)를 또 다른 과적합으로 만들지 않기 위해 train-only/WFO(학습 전용/워크포워드)와 untouched forward holdout(미접촉 전진 보류)를 고정한다.
""",
        )
    )
    return artifacts


def write_receipts(
    generated_at_utc: str,
    features: list[str],
    weight_info: dict[str, Any],
    forward_summary: dict[str, Any],
    feature_set_rows: list[dict[str, Any]],
) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "hypothesis": "A live-computable feature rebuild control(실시간 계산 가능 피처 재구축 대조) can remove the cp318/cp322 outcome-distillation overfit path.",
                "decision_use": "Open Stage329 materialization and later WFO/ONNX research without changing cp322A.",
                "comparison_baseline": "Stage328B cp318 outcome source audit",
                "control_variables": [
                    "cp322A frozen artifact unchanged",
                    "forward holdout starts 2026-04-14 and remains untouched for threshold selection",
                    "no Stage316/317/source_code/hyp_signal outcome features",
                ],
                "changed_variables": [
                    "feature set variants: core56, macro48, us100 technical42",
                    "materializer parameterization for forward window",
                ],
                "sample_scope": "old train/validation/OOS model input plus Stage326 forward raw M5 data",
                "success_criteria": "feature materialization queue, anti-overfit controls, and materializer gaps are explicit",
                "failure_criteria": "attempting to retune cp322A or infer split-local forward rank",
                "invalid_conditions": ["missing forward raw data", "unresolved timestamp binding", "untracked feature order changes"],
                "stop_conditions": ["do not select a candidate in run329A", "do not claim ONNX readiness"],
                "evidence_plan": [
                    rel(RUN_DIR / "forward_raw_coverage_audit.csv"),
                    rel(RUN_DIR / "live_feature_set_design_matrix.csv"),
                    rel(RUN_DIR / "materializer_gap_audit.csv"),
                    rel(RUN_DIR / "anti_overfit_control_spec.csv"),
                    rel(RUN_DIR / "rebuild_run_queue.csv"),
                ],
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(FORWARD_RAW_SUMMARY),
                    rel(MODEL_INPUT_SUMMARY),
                    rel(TRAINING_SUMMARY),
                    rel(TOP3_PRICE_PROXY_WEIGHTS),
                ],
                "time_axis": "Stage326 raw MT5 unix seconds; manifests still require timestamp/session binding before runtime claims",
                "sample_scope": {
                    "old_model_input": read_json(MODEL_INPUT_SUMMARY).get("split_summary", {}),
                    "forward_raw": forward_summary,
                },
                "missing_or_duplicate_check": rel(RUN_DIR / "forward_raw_coverage_audit.csv"),
                "feature_label_boundary": "forward data is feature-readiness only; labels/thresholds cannot be selected from it",
                "split_boundary": "train/validation/oos old contract plus 2026-04-14+ untouched forward holdout",
                "leakage_risk": "top3 weights, equity session gaps, materializer hard-coded old end, split-local rank",
                "data_hash_or_identity": {
                    "model_input_feature_order_hash": feature_order_hash(features),
                    "forward_raw_summary_sha256": sha256_file(FORWARD_RAW_SUMMARY),
                    "top3_weights_sha256": weight_info.get("sha256"),
                },
                "integrity_judgment": "usable_for_design_materialization_required",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "not_trained_in_run329A",
                "target_and_label": "label_v1_fwd12 train-threshold contract for future materialization only",
                "split_method": "train/validation/oos old plus untouched forward holdout",
                "selection_metric": "not_applicable_design_only",
                "secondary_metrics": ["feature coverage", "materializer gap", "anti-overfit controls", "future WFO gates"],
                "threshold_policy": "train_only_or_fixed_before_forward; no forward threshold tuning",
                "overfit_risk": "controlled by removing outcome-distillation features and rejecting split-local rank",
                "calibration_risk": "future scores cannot be probability claims before calibration receipts",
                "comparison_baseline": "cp322A blocked artifact and Stage328B outcome-source audit",
                "validation_judgment": JUDGMENT,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "source_inputs": [
                    rel(STAGE328_DECISION),
                    rel(STAGE328_REBUILD_QUEUE),
                    rel(STAGE328_FEATURE_MATRIX),
                    rel(FORWARD_RAW_SUMMARY),
                    rel(MODEL_INPUT_SUMMARY),
                    rel(MODEL_INPUT_FEATURE_ORDER),
                    rel(TOP3_PRICE_PROXY_WEIGHTS),
                ],
                "producer": rel(Path(__file__)),
                "consumer": [
                    rel(REVIEWS_DIR / "run329A_live_feature_rebuild_control_design.md"),
                    rel(REVIEWS_DIR / "final_stage329A_decision_report.md"),
                    rel(SELECTED_DIR / "selection_status.md"),
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                ],
                "artifact_paths": [
                    rel(RUN_DIR / "forward_raw_coverage_audit.csv"),
                    rel(RUN_DIR / "live_feature_set_design_matrix.csv"),
                    rel(RUN_DIR / "materializer_gap_audit.csv"),
                    rel(RUN_DIR / "anti_overfit_control_spec.csv"),
                    rel(RUN_DIR / "rebuild_run_queue.csv"),
                ],
                "artifact_hashes": {
                    "feature_order_hash": feature_order_hash(features),
                    "forward_raw_summary_sha256": sha256_file(FORWARD_RAW_SUMMARY),
                    "stage328_decision_sha256": sha256_file(STAGE328_DECISION),
                },
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked_design_and_generated_receipts",
                "lineage_judgment": "connected_with_boundary",
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate_name", "status", "evidence_path", "effect"],
            [
                {
                    "gate_name": "experiment_design(실험 설계)",
                    "status": "passed",
                    "evidence_path": rel(RUN_DIR / "experiment_design_receipt.json"),
                    "effect": "candidate selection(후보 선택) 없이 rebuild-control(재구축 대조) 범위를 고정했다.",
                },
                {
                    "gate_name": "data_integrity(데이터 무결성)",
                    "status": "passed_with_materialization_blockers_named",
                    "evidence_path": rel(RUN_DIR / "data_integrity_receipt.json"),
                    "effect": "forward raw data(전진 원천 데이터)는 있지만 materializer/session/weight gaps(물질화기/세션/가중치 공백)를 이름 붙였다.",
                },
                {
                    "gate_name": "model_validation(모델 검증)",
                    "status": "passed_design_only",
                    "evidence_path": rel(RUN_DIR / "model_validation_receipt.json"),
                    "effect": "training(학습) 전 overfit controls(과적합 방지 대조)를 고정했다.",
                },
                {
                    "gate_name": "artifact_lineage(산출물 계보)",
                    "status": "passed",
                    "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
                    "effect": "Stage328/326/data inputs(입력)와 Stage329 outputs(출력)를 연결했다.",
                },
                {
                    "gate_name": "result_judgment(결과 판정)",
                    "status": "passed_no_goal_achieve",
                    "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                    "effect": "Goal Achieve(목표 달성), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)를 주장하지 않는다.",
                },
            ],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            ["run_id", "status", "judgment", "decision", "goal_achieve", "next_action", "claim_boundary"],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_ACTION,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "generated_at_utc": generated_at_utc,
                "command": "python stage_pipelines/stage329/design_live_feature_rebuild_control.py",
                "candidate_mutation": "none",
                "selected_candidate": "none",
                "feature_set_rows": feature_set_rows,
                "next_action": NEXT_ACTION,
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    write_csv(
        REVIEWS_DIR / "stage_run_ledger.csv",
        [
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
        ],
        [
            {
                "row_id": f"{RUN_ID}__live_feature_rebuild_control_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "live_feature_rebuild_control_design(실시간 피처 재구축 대조 설계)",
                "tier_scope": "old train/validation/oos plus forward raw readiness(기존 학습/검증/표본외 및 전진 원천 준비도)",
                "scoreboard": "design_and_materialization_readiness(설계 및 물질화 준비도)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REVIEWS_DIR / "run329A_live_feature_rebuild_control_design.md"),
                "notes": "no_candidate_selected;goal_achieve_not_claimed;run329B_materialization_next.",
            }
        ],
    )
    artifacts.append(REVIEWS_DIR / "stage_run_ledger.csv")
    return artifacts


def update_registers(generated_at_utc: str, artifacts: list[Path]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "experiment_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329A_live_feature_rebuild_control_design.md"),
            "notes": "live_feature_rebuild_control_opened;no_candidate_selected;goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__live_feature_rebuild_control_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": "run328B_deep_audit_cp318_outcome_source_and_live_feature_rebuild_options_v1",
            "record_view": "live_feature_rebuild_control_design",
            "tier_scope": "old train/validation/oos plus forward raw readiness",
            "kpi_scope": "design_and_materialization_readiness",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329A_live_feature_rebuild_control_design.md"),
            "primary_kpi": "materialization_queue_created",
            "guardrail_kpi": "no_candidate_selected;goal_achieve_not_claimed;forward_holdout_untouched",
            "external_verification_status": "out_of_scope_by_claim_design_only_existing_raw_export",
            "notes": f"next_action={NEXT_ACTION}.",
        },
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not path_exists(artifact) or os_path(artifact).is_dir():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}".replace("-", "_"),
                "artifact_type": artifact.suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": STATUS,
            },
        )
    replace_or_append_csv_rows(ARTIFACT_REGISTRY, ["artifact_id", "run_id"], artifact_rows)


def update_current_truth() -> Path:
    workspace = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", "updated_on: '2026-05-26'")
    text = replace_prefix_line(text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        "  Stage329(329단계) run329A(329A 실행) live feature rebuild control design(실시간 피처 재구축 대조 설계)를 열고 닫았다. "
        "Effect(효과): cp322A(322A 후보)를 수정하지 않고 core56/macro48/us100-only rebuild queue(재구축 대기열)를 만들었으며, Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage329(329단계) run329A(329A 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_preserving(workspace, text, had_bom)

    current = ROOT / "docs" / "context" / "current_working_state.md"
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": "- source_stage(원천 단계): `328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction`",
        "- target_surface(": "- target_surface(목표 표면): `live_feature_rebuild_control_after_cp322a_block`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, new_line in replacements.items():
        text = replace_prefix_line(text, prefix, new_line)
    summary = (
        f"- run329A_summary(329A 요약): live feature rebuild control design(실시간 피처 재구축 대조 설계)을 `{STATUS}`로 닫았다. "
        "Effect(효과): core56/macro48/us100-only feature set(피처 세트) 대기열과 materializer gap(물질화기 공백)을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
    )
    if "run329A_summary(329A 요약)" not in text:
        text = text.replace(f"- decision(판정): `{JUDGMENT}`\n", f"- decision(판정): `{JUDGMENT}`\n{summary}\n", 1)
    write_text_preserving(current, text, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    entry = f"""

## 2026-05-26 - Stage329A Live Feature Rebuild Control(329A 실시간 피처 재구축 대조)

- run329A(329A 실행): Stage328B(328B 단계 실행)의 cp318 outcome source block(cp318 결과 원천 차단)을 받아 core56/macro48/us100-only feature set(피처 세트) materialization queue(물질화 대기열)를 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): cp322A(322A 후보)는 수정하지 않고, forward holdout(전진 보류)을 threshold tuning(임계값 튜닝)에 쓰지 않는 rebuild-control(재구축 대조)을 열었다.
"""
    append_text_if_missing(changelog, "## 2026-05-26 - Stage329A Live Feature Rebuild Control", entry)

    decision_doc = ROOT / "docs" / "decisions" / "2026-05-26_stage329A_live_feature_rebuild_control.md"
    return write_md(
        decision_doc,
        f"""
# Stage329A Live Feature Rebuild Control Decision(329A 실시간 피처 재구축 대조 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A(322A 후보)의 forward signal blocker(전진 신호 차단)를 튜닝으로 덮지 않고, live-computable feature(실시간 계산 가능 피처) 재구축 대조를 Stage329(329단계)로 열었다.
- next_action(다음 행동): `{NEXT_ACTION}`
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
    )


def main() -> None:
    generated_at_utc = utc_now()
    for directory in (SPEC_DIR, INPUTS_DIR, RUN_DIR, REVIEWS_DIR, SELECTED_DIR):
        os_path(directory).mkdir(parents=True, exist_ok=True)

    features = read_feature_order()
    weight_info = top3_weight_months()
    forward_rows, forward_summary = load_forward_coverage()
    feature_set_rows = build_feature_set_matrix(features, weight_info, forward_summary)
    materializer_gap_rows = build_materializer_gap_rows(weight_info)
    anti_overfit_rows = build_anti_overfit_rows()
    rebuild_queue = build_rebuild_queue(feature_set_rows)

    artifacts: list[Path] = []
    artifacts.extend(
        build_reports(
            generated_at_utc,
            features,
            weight_info,
            forward_rows,
            forward_summary,
            feature_set_rows,
            materializer_gap_rows,
            anti_overfit_rows,
            rebuild_queue,
        )
    )
    artifacts.extend(write_receipts(generated_at_utc, features, weight_info, forward_summary, feature_set_rows))
    artifacts.append(update_current_truth())
    update_registers(generated_at_utc, artifacts)

    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
