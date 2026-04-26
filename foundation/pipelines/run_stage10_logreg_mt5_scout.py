from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.models.baseline_training import (  # noqa: E402
    BaselineTrainingConfig,
    LABEL_NAMES,
    LABEL_ORDER,
    load_feature_order,
    train_baseline_model,
)
from foundation.pipelines.materialize_fpmarkets_v2_dataset import build_feature_frame  # noqa: E402
from foundation.pipelines.materialize_training_label_split_dataset import (  # noqa: E402
    TrainingLabelSplitSpec,
    assign_label_classes,
    assign_split,
    build_label_candidates,
    load_us100_close_series,
)


STAGE_ID = "10_alpha_scout__default_split_model_threshold_scan"
RUN_NUMBER = "run01A"
RUN_ID = "run01A_logreg_threshold_mt5_scout_v1"
EXPLORATION_LABEL = "stage10_Model__LogReg_MT5Scout"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
TIER_B_MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights"
TIER_B_FEATURE_SET_ID = "feature_set_v1_no_placeholder_top3_weight_features"
TIER_B_PARTIAL_CONTEXT_DATASET_ID = "stage10_run01A_tier_b_partial_context_core42_v1"
TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID = "feature_set_stage10_tier_b_core42_us100_session_v1"
TIER_B_PARTIAL_CONTEXT_POLICY_ID = "tier_b_partial_context_core42_fallback_v1"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
DEFAULT_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_TIER_B_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet"
)
DEFAULT_TIER_B_FEATURE_ORDER_PATH = DEFAULT_TIER_B_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_TRAINING_SUMMARY_PATH = Path(
    "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
)
DEFAULT_STAGE07_MODEL_PATH = Path(
    "stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/"
    "20260425_stage07_baseline_training_smoke_v1/model.joblib"
)
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
STAGE_RUN_LEDGER_PATH = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage10/run01A_logreg_threshold_mt5_scout_v1"
EA_SOURCE_PATH = Path("foundation/mt5/ObsidianPrimeV2_AlphaScoutEA.mq5")
EA_EXPERT_PATH = "Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_AlphaScoutEA.ex5"
EA_TESTER_SET_NAME = "ObsidianPrimeV2_AlphaScoutEA.set"
PROBABILITY_COLUMNS = ["p_short", "p_flat", "p_long"]
DECISION_CLASS_NO_TRADE = -1
DECISION_LABEL_NO_TRADE = "no_trade"
TIER_COLUMN = "tier_label"
TIER_A = "Tier A"
TIER_B = "Tier B"
TIER_AB = "Tier A+B"
ROUTE_ROLE_A_PRIMARY = "tier_a_primary"
ROUTE_ROLE_B_FALLBACK = "tier_b_fallback"
ROUTE_ROLE_NO_TIER = "no_tier"
TIER_B_CORE_FEATURE_ORDER = (
    "log_return_1",
    "log_return_3",
    "hl_range",
    "close_open_ratio",
    "gap_percent",
    "close_prev_close_ratio",
    "return_zscore_20",
    "hl_zscore_50",
    "overnight_return",
    "return_1_over_atr_14",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ema20_ema50_spread_zscore_50",
    "sma50_sma200_ratio",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
)
TIER_B_CONTEXT_GROUPS = {
    "macro": ("vix_change_1", "vix_zscore_20", "us10yr_change_1", "us10yr_zscore_20", "usdx_change_1", "usdx_zscore_20"),
    "constituent": ("nvda_xnas_log_return_1", "aapl_xnas_log_return_1", "msft_xnas_log_return_1", "amzn_xnas_log_return_1"),
    "basket": (
        "mega8_equal_return_1",
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
        "us100_minus_mega8_equal_return_1",
        "top3_weighted_return_1",
        "us100_minus_top3_weighted_return_1",
    ),
}
REQUIRED_TIER_VIEWS = (
    ("tier_a_separate", TIER_A),
    ("tier_b_separate", TIER_B),
    ("tier_ab_combined", TIER_AB),
)
ALPHA_LEDGER_COLUMNS = (
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
)
RUN_REGISTRY_COLUMNS = ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes")


@dataclass(frozen=True)
class ThresholdRule:
    threshold_id: str = "short045_long045_margin005"
    short_threshold: float = 0.45
    long_threshold: float = 0.45
    min_margin: float = 0.05


@dataclass(frozen=True)
class TesterMaterializationConfig:
    expert: str = EA_EXPERT_PATH
    symbol: str = "US100"
    period: str = "M5"
    model: int = 4
    deposit: float = 500.0
    leverage: str = "1:100"
    optimization: int = 0
    execution_mode: int = 0
    forward_mode: int = 0
    use_local: int = 1
    use_remote: int = 0
    use_cloud: int = 0
    from_date: str | None = None
    to_date: str | None = None
    report: str | None = None
    replace_report: int = 1
    shutdown_terminal: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize the Stage 10 run01A logistic MT5 scout payload.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--tier-b-model-input-path", default=str(DEFAULT_TIER_B_MODEL_INPUT_PATH))
    parser.add_argument("--tier-b-feature-order-path", default=str(DEFAULT_TIER_B_FEATURE_ORDER_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--training-summary-path", default=str(DEFAULT_TRAINING_SUMMARY_PATH))
    parser.add_argument("--stage07-model-path", default=str(DEFAULT_STAGE07_MODEL_PATH))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--tier-column", default=TIER_COLUMN)
    parser.add_argument("--random-seed", type=int, default=10)
    parser.add_argument("--max-iter", type=int, default=2000)
    parser.add_argument("--parity-rows", type=int, default=128)
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args()


def _io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def _path_exists(path: Path) -> bool:
    return _io_path(path).exists()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with _io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_file_lf_normalized(path: Path) -> str:
    raw = _io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def ordered_hash(names: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()


def mt5_runtime_module_hashes() -> list[dict[str, Any]]:
    include_root = REPO_ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime"
    paths = [REPO_ROOT / EA_SOURCE_PATH]
    if _path_exists(include_root):
        paths.extend(sorted(include_root.glob("*.mqh")))
    modules: list[dict[str, Any]] = []
    for path in paths:
        if not _path_exists(path):
            modules.append({"path": path.relative_to(REPO_ROOT).as_posix(), "status": "missing", "sha256": None})
            continue
        modules.append(
            {
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "status": "present",
                "sha256": sha256_file(path),
            }
        )
    return modules


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text(json.dumps(_json_ready(payload), indent=2), encoding="utf-8")


class _Mt5ReportTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "tr":
            self._current_row = []
        elif tag in {"td", "th"} and self._current_row is not None:
            self._current_cell = []

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self._current_cell is not None and self._current_row is not None:
            text = " ".join("".join(self._current_cell).split())
            self._current_row.append(text)
            self._current_cell = None
        elif tag == "tr" and self._current_row is not None:
            if any(cell for cell in self._current_row):
                self.rows.append(self._current_row)
            self._current_row = None


_REPORT_NUMBER_RE = re.compile(r"([-+]?\d[\d\s,]*(?:\.\d+)?)(\s*%)?")


def read_text_best_effort(path: Path) -> tuple[str, str]:
    raw = _io_path(path).read_bytes()
    for encoding in ("utf-16", "utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore"), "utf-8-ignore"


def _report_numbers(value: Any) -> list[tuple[float, bool]]:
    text = str(value or "").replace("\xa0", " ")
    numbers: list[tuple[float, bool]] = []
    for match in _REPORT_NUMBER_RE.finditer(text):
        number_text = match.group(1).replace(" ", "").replace(",", "")
        try:
            numbers.append((float(number_text), bool(match.group(2))))
        except ValueError:
            continue
    return numbers


def parse_report_number(value: Any) -> float | None:
    numbers = _report_numbers(value)
    return numbers[0][0] if numbers else None


def parse_count_percent(value: Any) -> dict[str, Any]:
    numbers = _report_numbers(value)
    count = int(round(numbers[0][0])) if numbers else None
    percent = next((number for number, is_percent in numbers if is_percent), None)
    if percent is None and len(numbers) > 1:
        percent = numbers[1][0]
    return {"count": count, "percent": percent}


def parse_amount_percent(value: Any) -> dict[str, Any]:
    numbers = _report_numbers(value)
    amount = next((number for number, is_percent in numbers if not is_percent), None)
    percent = next((number for number, is_percent in numbers if is_percent), None)
    if amount is None and numbers:
        amount = numbers[0][0]
    if percent is None and len(numbers) > 1:
        percent = numbers[1][0]
    return {"amount": amount, "percent": percent}


def _normalize_report_label(value: Any) -> str:
    return str(value or "").strip().rstrip(":").casefold()


def _cell_after(row: Sequence[str], aliases: Sequence[str]) -> str | None:
    normalized_aliases = {_normalize_report_label(alias) for alias in aliases}
    for index, cell in enumerate(row[:-1]):
        if _normalize_report_label(cell) in normalized_aliases:
            for next_cell in row[index + 1 :]:
                if str(next_cell).strip():
                    return next_cell
    return None


def _first_cell_after(rows: Sequence[Sequence[str]], aliases: Sequence[str]) -> str | None:
    for row in rows:
        value = _cell_after(row, aliases)
        if value is not None:
            return value
    return None


def _first_row_containing(rows: Sequence[Sequence[str]], aliases: Sequence[str]) -> Sequence[str] | None:
    normalized_aliases = {_normalize_report_label(alias) for alias in aliases}
    for row in rows:
        row_labels = {_normalize_report_label(cell) for cell in row}
        if row_labels & normalized_aliases:
            return row
    return None


def extract_mt5_strategy_report_metrics(report_path: Path) -> dict[str, Any]:
    text, encoding = read_text_best_effort(report_path)
    parser = _Mt5ReportTableParser()
    parser.feed(text)
    rows = parser.rows

    metrics: dict[str, Any] = {
        "status": "partial",
        "report_path": report_path.as_posix(),
        "source_encoding": encoding,
        "parsed_row_count": len(rows),
    }

    scalar_fields = {
        "net_profit": ("총수입", "Total Net Profit"),
        "gross_profit": ("누적 수익", "Gross Profit"),
        "gross_loss": ("누적 손실", "Gross Loss"),
        "profit_factor": ("Profit Factor",),
        "expectancy": ("예상 비용", "Expected Payoff"),
        "recovery_factor": ("Recovery Factor",),
        "sharpe_ratio": ("Sharpe Ratio",),
    }
    for field, aliases in scalar_fields.items():
        metrics[field] = parse_report_number(_first_cell_after(rows, aliases))

    for field, aliases in {
        "balance_drawdown_maximal": ("Balance Drawdown Maximal",),
        "equity_drawdown_maximal": ("Equity Drawdown Maximal",),
    }.items():
        parsed = parse_amount_percent(_first_cell_after(rows, aliases))
        metrics[f"{field}_amount"] = parsed["amount"]
        metrics[f"{field}_percent"] = parsed["percent"]

    trade_row = _first_row_containing(rows, ("매도거래수 (won %)", "Short Trades (won %)"))
    trade_count_value = _cell_after(trade_row, ("총 거래횟수", "Total Trades")) if trade_row else None
    metrics["trade_count"] = None if trade_count_value is None else int(round(parse_report_number(trade_count_value) or 0))
    if trade_row is not None:
        short = parse_count_percent(_cell_after(trade_row, ("매도거래수 (won %)", "Short Trades (won %)")))
        long = parse_count_percent(_cell_after(trade_row, ("매수거래수 (won %)", "Long Trades (won %)")))
        metrics["short_trade_count"] = short["count"]
        metrics["short_win_rate_percent"] = short["percent"]
        metrics["long_trade_count"] = long["count"]
        metrics["long_win_rate_percent"] = long["percent"]

    profit_row = _first_row_containing(rows, ("수익거래수 (% of total)", "Profit Trades (% of total)"))
    if profit_row is not None:
        deal_count_value = _cell_after(profit_row, ("총 거래횟수", "Total Deals"))
        metrics["deal_count"] = None if deal_count_value is None else int(round(parse_report_number(deal_count_value) or 0))
        winners = parse_count_percent(_cell_after(profit_row, ("수익거래수 (% of total)", "Profit Trades (% of total)")))
        losers = parse_count_percent(_cell_after(profit_row, ("손실거래수 (% of total)", "Loss Trades (% of total)")))
        metrics["winning_trade_count"] = winners["count"]
        metrics["win_rate_percent"] = winners["percent"]
        metrics["losing_trade_count"] = losers["count"]
        metrics["loss_rate_percent"] = losers["percent"]

    metrics["max_drawdown_amount"] = (
        metrics.get("equity_drawdown_maximal_amount") or metrics.get("balance_drawdown_maximal_amount")
    )
    metrics["max_drawdown_percent"] = (
        metrics.get("equity_drawdown_maximal_percent") or metrics.get("balance_drawdown_maximal_percent")
    )
    if metrics.get("expectancy") is None and metrics.get("trade_count"):
        metrics["expectancy"] = float(metrics["net_profit"] / metrics["trade_count"]) if metrics.get("net_profit") is not None else None
    if metrics.get("profit_factor") is None and metrics.get("gross_profit") is not None and metrics.get("gross_loss"):
        metrics["profit_factor"] = float(metrics["gross_profit"] / abs(metrics["gross_loss"]))
    if metrics.get("recovery_factor") is None and metrics.get("net_profit") is not None and metrics.get("max_drawdown_amount"):
        metrics["recovery_factor"] = float(metrics["net_profit"] / metrics["max_drawdown_amount"])

    required = [
        "net_profit",
        "profit_factor",
        "expectancy",
        "trade_count",
        "win_rate_percent",
        "max_drawdown_amount",
        "recovery_factor",
    ]
    missing = [field for field in required if metrics.get(field) is None]
    metrics["missing_required_metrics"] = missing
    metrics["status"] = "completed" if not missing else "partial"
    return metrics


def _json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def load_label_threshold(summary_path: Path) -> float:
    payload = json.loads(_io_path(summary_path).read_text(encoding="utf-8"))
    threshold = float(payload["threshold_log_return"])
    if not np.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"Invalid label threshold in {summary_path}: {threshold}")
    return threshold


def finite_feature_mask(frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.Series:
    missing = [name for name in feature_order if name not in frame.columns]
    if missing:
        raise RuntimeError(f"Frame is missing required feature columns: {missing}")
    matrix = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    return pd.Series(np.isfinite(matrix).all(axis=1), index=frame.index)


def classify_tier_b_partial_context(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    group_ready = {
        group_name: finite_feature_mask(result, feature_names)
        for group_name, feature_names in TIER_B_CONTEXT_GROUPS.items()
    }

    subtypes: list[str] = []
    missing_masks: list[str] = []
    available_masks: list[str] = []
    group_names = list(TIER_B_CONTEXT_GROUPS)
    for row_index in result.index:
        missing_groups = [name for name in group_names if not bool(group_ready[name].loc[row_index])]
        available_groups = [name for name in group_names if name not in missing_groups]
        missing_set = set(missing_groups)
        if not missing_groups:
            subtype = "B_full_context_outside_tier_a_scope"
        elif missing_set == {"macro"}:
            subtype = "B_macro_missing"
        elif missing_set == {"constituent"}:
            subtype = "B_constituent_missing"
        elif missing_set == {"basket"}:
            subtype = "B_basket_missing"
        elif missing_set == set(group_names):
            subtype = "B_core_only"
        else:
            subtype = "B_mixed_partial_context"
        subtypes.append(subtype)
        missing_masks.append("|".join(missing_groups) if missing_groups else "none")
        available_masks.append("|".join(available_groups) if available_groups else "core_only")

    result["partial_context_subtype"] = subtypes
    result["missing_feature_group_mask"] = missing_masks
    result["available_feature_group_mask"] = available_masks
    return result


def _timestamp_key(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True).astype("int64")


def _split_counts(frame: pd.DataFrame) -> dict[str, int]:
    split_values = frame["split"].astype(str) if "split" in frame.columns else pd.Series([], dtype="object")
    return {split: int(split_values.eq(split).sum()) for split in ("train", "validation", "oos")}


def _subtype_counts(frame: pd.DataFrame) -> dict[str, int]:
    if frame.empty or "partial_context_subtype" not in frame.columns:
        return {}
    counts = frame["partial_context_subtype"].astype(str).value_counts().sort_index()
    return {str(index): int(value) for index, value in counts.items()}


def _subtype_counts_by_split(frame: pd.DataFrame) -> dict[str, dict[str, int]]:
    payload: dict[str, dict[str, int]] = {}
    for split in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split)] if "split" in frame.columns else frame.iloc[0:0]
        payload[split] = _subtype_counts(split_frame)
    return payload


def build_tier_b_partial_context_frames(
    *,
    raw_root: Path,
    tier_a_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
    label_threshold: float,
) -> dict[str, Any]:
    spec = TrainingLabelSplitSpec()
    feature_frame, source_counts = build_feature_frame(raw_root)
    feature_frame = feature_frame.copy()
    feature_frame["timestamp"] = pd.to_datetime(feature_frame["timestamp"], utc=True)
    if "symbol" not in feature_frame.columns:
        feature_frame["symbol"] = "US100"

    cash_open = feature_frame["is_us_cash_open"].fillna(0).astype(bool)
    practical = feature_frame["timestamp"] >= spec.train_start_utc
    feature_frame = feature_frame.loc[practical & cash_open].sort_values("timestamp").reset_index(drop=True)

    raw_close_frame = load_us100_close_series(raw_root)
    labelable = build_label_candidates(feature_frame, raw_close_frame, spec)
    labelable = assign_label_classes(labelable, label_threshold)
    labelable["split"] = assign_split(labelable, spec)
    labelable["label_id"] = spec.label_id
    labelable["split_id"] = spec.split_id
    labelable["horizon_bars"] = spec.horizon_bars
    labelable["horizon_minutes"] = spec.horizon_minutes
    labelable["symbol"] = "US100"
    labelable = labelable.sort_values("timestamp").reset_index(drop=True)

    tier_a_keys = set(_timestamp_key(tier_a_frame["timestamp"]).tolist())
    labelable_keys = _timestamp_key(labelable["timestamp"])
    tier_a_available = labelable_keys.isin(tier_a_keys)
    tier_b_ready = finite_feature_mask(labelable, tier_b_feature_order)
    tier_a_full_feature_ready = finite_feature_mask(labelable, tier_a_feature_order)

    labelable["tier_a_primary_available"] = tier_a_available.to_numpy()
    labelable["tier_a_full_feature_ready"] = tier_a_full_feature_ready.to_numpy()
    labelable["tier_b_core_ready"] = tier_b_ready.to_numpy()
    labelable["route_role"] = np.select(
        [tier_a_available.to_numpy(), tier_b_ready.to_numpy()],
        [ROUTE_ROLE_A_PRIMARY, ROUTE_ROLE_B_FALLBACK],
        default=ROUTE_ROLE_NO_TIER,
    )

    labeled_with_context = classify_tier_b_partial_context(labelable)
    b_training = labeled_with_context.loc[tier_b_ready].copy().reset_index(drop=True)
    b_fallback = labeled_with_context.loc[~tier_a_available & tier_b_ready].copy().reset_index(drop=True)
    no_tier = labeled_with_context.loc[~tier_a_available & ~tier_b_ready].copy().reset_index(drop=True)

    b_training[TIER_COLUMN] = TIER_B
    b_fallback[TIER_COLUMN] = TIER_B
    no_tier["context_reject_reason"] = "core42_nonfinite_or_missing"
    no_tier["partial_context_subtype"] = "no_tier_core42_missing"
    no_tier["missing_feature_group_mask"] = "core42"
    no_tier["available_feature_group_mask"] = "insufficient_for_tier_b"

    by_split: dict[str, dict[str, int]] = {}
    for split in ("train", "validation", "oos"):
        by_split[split] = {
            "tier_a_primary_rows": int(tier_a_frame["split"].astype(str).eq(split).sum()),
            "tier_b_fallback_rows": int(b_fallback["split"].astype(str).eq(split).sum()),
            "no_tier_labelable_rows": int(no_tier["split"].astype(str).eq(split).sum()),
        }
        by_split[split]["routed_labelable_rows"] = (
            by_split[split]["tier_a_primary_rows"] + by_split[split]["tier_b_fallback_rows"]
        )

    summary = {
        "policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID,
        "dataset_id": TIER_B_PARTIAL_CONTEXT_DATASET_ID,
        "feature_set_id": TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
        "feature_count": int(len(tier_b_feature_order)),
        "feature_order_hash": ordered_hash(tier_b_feature_order),
        "label_threshold_log_return": float(label_threshold),
        "source_raw_rows": int(source_counts.get("raw_rows", 0)),
        "source_valid_rows": int(source_counts.get("valid_rows", 0)),
        "labelable_rows": int(len(labelable)),
        "tier_a_primary_rows": int(len(tier_a_frame)),
        "tier_b_training_rows": int(len(b_training)),
        "tier_b_fallback_rows": int(len(b_fallback)),
        "no_tier_labelable_rows": int(len(no_tier)),
        "by_split": by_split,
        "tier_b_fallback_by_subtype": _subtype_counts(b_fallback),
        "tier_b_fallback_by_split_subtype": _subtype_counts_by_split(b_fallback),
        "no_tier_by_split": _split_counts(no_tier),
        "note": (
            "Tier B fallback is built from partial-context rows that are outside the strict Tier A clean sample "
            "but still have finite US100/session core42 features."
        ),
    }
    return {
        "route_frame": labeled_with_context,
        "tier_b_training_frame": b_training,
        "tier_b_fallback_frame": b_fallback,
        "no_tier_frame": no_tier,
        "summary": summary,
    }


def validate_threshold_rule(rule: ThresholdRule) -> None:
    values = {
        "short_threshold": rule.short_threshold,
        "long_threshold": rule.long_threshold,
        "min_margin": rule.min_margin,
    }
    for name, value in values.items():
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite.")
    if not 0.0 <= rule.short_threshold <= 1.0:
        raise ValueError("short_threshold must be in [0, 1].")
    if not 0.0 <= rule.long_threshold <= 1.0:
        raise ValueError("long_threshold must be in [0, 1].")
    if rule.min_margin < 0.0:
        raise ValueError("min_margin must be non-negative.")


def probability_matrix(probabilities: pd.DataFrame | np.ndarray) -> np.ndarray:
    if isinstance(probabilities, pd.DataFrame):
        missing = [name for name in PROBABILITY_COLUMNS if name not in probabilities.columns]
        if missing:
            raise ValueError(f"Probability frame is missing columns: {missing}")
        matrix = probabilities.loc[:, PROBABILITY_COLUMNS].to_numpy(dtype="float64", copy=False)
    else:
        matrix = np.asarray(probabilities, dtype="float64")
    if matrix.ndim != 2 or matrix.shape[1] != 3:
        raise ValueError(f"Expected probability matrix shape [n, 3], got {matrix.shape}.")
    if not np.isfinite(matrix).all():
        raise ValueError("Probability matrix contains NaN or infinite values.")
    return matrix


def apply_threshold_rule(probabilities: pd.DataFrame | np.ndarray, rule: ThresholdRule) -> pd.DataFrame:
    validate_threshold_rule(rule)
    matrix = probability_matrix(probabilities)
    rows: list[dict[str, Any]] = []
    for p_short, p_flat, p_long in matrix:
        short_margin = float(p_short - max(p_flat, p_long))
        long_margin = float(p_long - max(p_flat, p_short))
        short_pass = bool(p_short >= rule.short_threshold and short_margin >= rule.min_margin)
        long_pass = bool(p_long >= rule.long_threshold and long_margin >= rule.min_margin)

        if short_pass and not long_pass:
            decision_class = 0
            decision_label = LABEL_NAMES[0]
            decision_probability = float(p_short)
            decision_margin = short_margin
        elif long_pass and not short_pass:
            decision_class = 2
            decision_label = LABEL_NAMES[2]
            decision_probability = float(p_long)
            decision_margin = long_margin
        elif short_pass and long_pass and p_short != p_long:
            decision_class = 0 if p_short > p_long else 2
            decision_label = LABEL_NAMES[decision_class]
            decision_probability = float(max(p_short, p_long))
            decision_margin = float(abs(p_short - p_long))
        else:
            decision_class = DECISION_CLASS_NO_TRADE
            decision_label = DECISION_LABEL_NO_TRADE
            decision_probability = float(max(p_short, p_flat, p_long))
            decision_margin = float(max(short_margin, long_margin))

        rows.append(
            {
                "threshold_id": rule.threshold_id,
                "p_short": float(p_short),
                "p_flat": float(p_flat),
                "p_long": float(p_long),
                "decision_label_class": decision_class,
                "decision_label": decision_label,
                "decision_probability": decision_probability,
                "decision_margin": decision_margin,
                "short_margin": short_margin,
                "long_margin": long_margin,
            }
        )
    return pd.DataFrame(rows)


def _threshold_id(short_threshold: float, long_threshold: float, min_margin: float) -> str:
    return f"short{short_threshold:.3f}_long{long_threshold:.3f}_margin{min_margin:.3f}"


def sweep_threshold_rules(
    probabilities: pd.DataFrame | np.ndarray,
    y_true: Sequence[int] | np.ndarray | pd.Series | None = None,
    *,
    short_thresholds: Sequence[float] = (0.40, 0.45, 0.50, 0.55, 0.60),
    long_thresholds: Sequence[float] | None = None,
    min_margins: Sequence[float] = (0.00, 0.025, 0.05, 0.075, 0.10),
) -> pd.DataFrame:
    if long_thresholds is None:
        long_thresholds = short_thresholds
    matrix = probability_matrix(probabilities)
    true_values = None if y_true is None else np.asarray(y_true, dtype="int64")
    if true_values is not None and true_values.shape[0] != matrix.shape[0]:
        raise ValueError("y_true length must match probability row count.")

    rows: list[dict[str, Any]] = []
    for short_threshold, long_threshold, min_margin in itertools.product(
        short_thresholds, long_thresholds, min_margins
    ):
        rule = ThresholdRule(
            threshold_id=_threshold_id(short_threshold, long_threshold, min_margin),
            short_threshold=float(short_threshold),
            long_threshold=float(long_threshold),
            min_margin=float(min_margin),
        )
        decisions = apply_threshold_rule(matrix, rule)
        decision_classes = decisions["decision_label_class"].to_numpy(dtype="int64", copy=False)
        signal_mask = decision_classes != DECISION_CLASS_NO_TRADE
        signal_count = int(signal_mask.sum())
        short_count = int((decision_classes == 0).sum())
        long_count = int((decision_classes == 2).sum())
        row: dict[str, Any] = {
            "threshold_id": rule.threshold_id,
            "short_threshold": rule.short_threshold,
            "long_threshold": rule.long_threshold,
            "min_margin": rule.min_margin,
            "rows": int(len(decisions)),
            "signal_count": signal_count,
            "short_count": short_count,
            "long_count": long_count,
            "coverage": float(signal_count / len(decisions)) if len(decisions) else 0.0,
            "no_trade_rate": float(1.0 - signal_count / len(decisions)) if len(decisions) else 1.0,
            "long_share_of_signals": float(long_count / signal_count) if signal_count else np.nan,
        }
        if true_values is not None:
            correct = decision_classes[signal_mask] == true_values[signal_mask]
            row["directional_hit_rate"] = float(correct.mean()) if signal_count else np.nan
            row["directional_correct_count"] = int(correct.sum()) if signal_count else 0
        rows.append(row)
    return pd.DataFrame(rows)


def select_threshold_from_sweep(
    sweep: pd.DataFrame,
    *,
    primary_metric: str = "directional_hit_rate",
    min_coverage: float = 0.01,
) -> dict[str, Any]:
    if sweep.empty:
        raise ValueError("Threshold sweep is empty.")
    if primary_metric not in sweep.columns:
        primary_metric = "coverage"
    candidates = sweep.loc[sweep["coverage"].fillna(0.0) >= min_coverage].copy()
    if candidates.empty:
        candidates = sweep.copy()
    candidates[primary_metric] = candidates[primary_metric].fillna(-np.inf)
    candidates = candidates.sort_values(
        [primary_metric, "coverage", "signal_count", "threshold_id"],
        ascending=[False, False, False, True],
    )
    return candidates.iloc[0].to_dict()


def classifier_classes(model: Any) -> list[int]:
    if hasattr(model, "named_steps"):
        for step in reversed(list(model.named_steps.values())):
            if hasattr(step, "classes_"):
                return [int(value) for value in step.classes_]
    if hasattr(model, "classes_"):
        return [int(value) for value in model.classes_]
    raise ValueError("Model does not expose classes_.")


def ordered_sklearn_probabilities(
    model: Any,
    values: np.ndarray,
    class_order: Sequence[int] = LABEL_ORDER,
) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = classifier_classes(model)
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    ordered = np.zeros((raw.shape[0], len(class_order)), dtype="float64")
    for output_index, label in enumerate(class_order):
        if int(label) not in class_to_index:
            raise ValueError(f"Model is missing class {label}; cannot build fixed probability order.")
        ordered[:, output_index] = raw[:, class_to_index[int(label)]]
    return ordered


def build_prediction_frame(
    model: Any,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    rule: ThresholdRule,
    *,
    tier_column: str = TIER_COLUMN,
) -> pd.DataFrame:
    values = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    probabilities = ordered_sklearn_probabilities(model, values)
    decisions = apply_threshold_rule(probabilities, rule)
    identity_columns = [
        name
        for name in (
            "timestamp",
            "symbol",
            "split",
            "label",
            "label_class",
            "route_role",
            "partial_context_subtype",
            "missing_feature_group_mask",
            "available_feature_group_mask",
            "tier_a_primary_available",
            "tier_a_full_feature_ready",
            "tier_b_core_ready",
            "context_reject_reason",
        )
        if name in frame.columns
    ]
    result = frame.loc[:, identity_columns].reset_index(drop=True).copy()
    if tier_column in frame.columns:
        result[tier_column] = frame[tier_column].to_numpy()
    return pd.concat([result, decisions], axis=1)


def normalize_tier_label(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    text = str(value).strip().lower().replace("_", " ")
    if text in {"tier a", "a"}:
        return TIER_A
    if text in {"tier b", "b"}:
        return TIER_B
    if text in {"tier a+b", "tier ab", "a+b", "ab", "combined"}:
        return TIER_AB
    return None


def build_tier_prediction_views(
    predictions: pd.DataFrame,
    *,
    tier_column: str = TIER_COLUMN,
) -> dict[str, pd.DataFrame]:
    empty = predictions.iloc[0:0].copy()
    if tier_column not in predictions.columns:
        return {view: empty.copy() for view, _scope in REQUIRED_TIER_VIEWS}

    normalized = predictions[tier_column].map(normalize_tier_label)
    tier_a = predictions.loc[normalized.eq(TIER_A)].copy()
    tier_b = predictions.loc[normalized.eq(TIER_B)].copy()
    combined = pd.concat([tier_a, tier_b], ignore_index=True)
    return {
        "tier_a_separate": tier_a.reset_index(drop=True),
        "tier_b_separate": tier_b.reset_index(drop=True),
        "tier_ab_combined": combined.reset_index(drop=True),
    }


def prediction_view_metrics(view: pd.DataFrame) -> dict[str, Any]:
    rows = int(len(view))
    payload: dict[str, Any] = {
        "rows": rows,
        "signal_count": 0,
        "short_count": 0,
        "long_count": 0,
        "no_trade_count": 0,
        "signal_coverage": 0.0,
        "probability_row_sum_max_abs_error": None,
    }
    if rows == 0:
        return payload

    if "decision_label" in view.columns:
        decision_labels = view["decision_label"].astype(str)
        payload["short_count"] = int(decision_labels.eq("short").sum())
        payload["long_count"] = int(decision_labels.eq("long").sum())
        payload["no_trade_count"] = int(decision_labels.eq(DECISION_LABEL_NO_TRADE).sum())
        payload["signal_count"] = int(payload["short_count"] + payload["long_count"])
        payload["signal_coverage"] = float(payload["signal_count"] / rows)

    if all(name in view.columns for name in PROBABILITY_COLUMNS):
        matrix = probability_matrix(view.loc[:, PROBABILITY_COLUMNS])
        payload["probability_row_sum_max_abs_error"] = float(np.abs(matrix.sum(axis=1) - 1.0).max())
        payload["mean_probability"] = {
            name: float(matrix[:, index].mean()) for index, name in enumerate(PROBABILITY_COLUMNS)
        }
    if "partial_context_subtype" in view.columns:
        payload["partial_context_subtype_counts"] = _subtype_counts(view)
        if "decision_label" in view.columns:
            signal_view = view.loc[view["decision_label"].astype(str).ne(DECISION_LABEL_NO_TRADE)]
            payload["partial_context_subtype_signal_counts"] = _subtype_counts(signal_view)
    return payload


def build_paired_tier_records(
    tier_views: Mapping[str, pd.DataFrame],
    *,
    run_id: str = RUN_ID,
    stage_id: str = STAGE_ID,
    base_path: str | Path | None = None,
    kpi_scope: str = "signal_probability_threshold",
    scoreboard_lane: str = "structural_scout",
    external_verification_status: str = "out_of_scope_by_claim",
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    base = None if base_path is None else Path(base_path)
    for record_view, tier_scope in REQUIRED_TIER_VIEWS:
        view = tier_views.get(record_view)
        metrics = prediction_view_metrics(view if view is not None else pd.DataFrame())
        status = "completed_payload" if metrics["rows"] > 0 else "missing_required"
        judgment = "inconclusive_payload_only" if metrics["rows"] > 0 else "inconclusive_tier_pair_incomplete"
        record_path = "" if base is None else (base / f"{record_view}_predictions.parquet").as_posix()
        records.append(
            {
                "ledger_row_id": f"{run_id}__{record_view}",
                "stage_id": stage_id,
                "run_id": run_id,
                "subrun_id": record_view,
                "parent_run_id": run_id,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": kpi_scope,
                "scoreboard_lane": scoreboard_lane,
                "status": status,
                "judgment": judgment,
                "path": record_path,
                "primary_kpi": {"signal_coverage": metrics["signal_coverage"]},
                "guardrail_kpi": {
                    "probability_row_sum_max_abs_error": metrics["probability_row_sum_max_abs_error"],
                },
                "external_verification_status": external_verification_status,
                "notes": "Tier labels are sample labels, not exploration gates.",
                "metrics": metrics,
            }
        )
    return records


def materialize_tier_prediction_views(
    tier_views: Mapping[str, pd.DataFrame],
    output_root: Path,
) -> dict[str, dict[str, Any]]:
    _io_path(output_root).mkdir(parents=True, exist_ok=True)
    payload: dict[str, dict[str, Any]] = {}
    for record_view, view in tier_views.items():
        if view.empty:
            payload[record_view] = {"status": "missing_required", "rows": 0, "path": None, "sha256": None}
            continue
        path = output_root / f"{record_view}_predictions.parquet"
        view.to_parquet(_io_path(path), index=False)
        payload[record_view] = {
            "status": "completed_payload",
            "rows": int(len(view)),
            "path": path.as_posix(),
            "sha256": sha256_file(path),
        }
    return payload


def _onnx_options_for_model(model: Any) -> dict[int, dict[str, Any]]:
    options = {id(model): {"zipmap": False}}
    if hasattr(model, "named_steps"):
        for step in model.named_steps.values():
            if hasattr(step, "predict_proba"):
                options[id(step)] = {"zipmap": False}
    return options


def _onnx_output_shape(output: Any) -> list[Any]:
    tensor_type = output.type.tensor_type
    dims: list[Any] = []
    for dim in tensor_type.shape.dim:
        if dim.dim_value:
            dims.append(int(dim.dim_value))
        elif dim.dim_param:
            dims.append(str(dim.dim_param))
        else:
            dims.append(None)
    return dims


def export_sklearn_to_onnx_zipmap_disabled(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
    input_name: str = "float_input",
    target_opset: int = 12,
) -> dict[str, Any]:
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType

    onnx_model = convert_sklearn(
        model,
        initial_types=[(input_name, FloatTensorType([None, int(feature_count)]))],
        options=_onnx_options_for_model(model),
        target_opset=target_opset,
    )
    non_tensor_outputs = [
        output.name for output in onnx_model.graph.output if output.type.WhichOneof("value") != "tensor_type"
    ]
    if non_tensor_outputs:
        raise RuntimeError(f"ONNX export produced non-tensor outputs, zipmap may be enabled: {non_tensor_outputs}")

    _io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(output_path).write_bytes(onnx_model.SerializeToString())
    outputs = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
            "shape": _onnx_output_shape(output),
        }
        for output in onnx_model.graph.output
    ]
    probability_outputs = [
        item["name"]
        for item in outputs
        if len(item["shape"]) == 2 and item["shape"][-1] in {len(LABEL_ORDER), "N"}
    ]
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "input_name": input_name,
        "target_opset": target_opset,
        "zipmap_disabled": True,
        "outputs": outputs,
        "probability_output_name": probability_outputs[0] if probability_outputs else outputs[-1]["name"],
    }


def _find_probability_output(outputs: Sequence[np.ndarray], class_count: int) -> np.ndarray:
    candidates = [
        output
        for output in outputs
        if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == class_count
    ]
    if len(candidates) != 1:
        shapes = [getattr(output, "shape", None) for output in outputs]
        raise RuntimeError(f"Expected one probability output with {class_count} columns; got shapes {shapes}.")
    return np.asarray(candidates[0], dtype="float64")


def check_onnxruntime_probability_parity(
    model: Any,
    onnx_path: Path,
    values: np.ndarray,
    *,
    class_order: Sequence[int] = LABEL_ORDER,
    tolerance: float = 1e-5,
) -> dict[str, Any]:
    import onnxruntime as ort

    classes = classifier_classes(model)
    if list(classes) != [int(label) for label in class_order]:
        raise ValueError(f"Model class order {classes} does not match expected class order {list(class_order)}.")
    X = np.asarray(values, dtype="float32")
    expected = ordered_sklearn_probabilities(model, X.astype("float64"), class_order=class_order)
    session = ort.InferenceSession(str(_io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: X})
    actual = _find_probability_output(outputs, len(class_order))
    diff = np.abs(actual - expected)
    row_sum_error = np.abs(actual.sum(axis=1) - 1.0)
    return {
        "passed": bool(float(diff.max()) <= tolerance),
        "rows": int(X.shape[0]),
        "class_order": [int(label) for label in class_order],
        "tolerance": float(tolerance),
        "max_abs_diff": float(diff.max()),
        "mean_abs_diff": float(diff.mean()),
        "onnx_row_sum_max_abs_error": float(row_sum_error.max()) if len(row_sum_error) else 0.0,
        "input_name": input_name,
        "output_names": [output.name for output in session.get_outputs()],
    }


def validate_feature_matrix(frame: pd.DataFrame, feature_order: Sequence[str]) -> np.ndarray:
    missing = [name for name in feature_order if name not in frame.columns]
    if missing:
        raise ValueError(f"Feature frame is missing feature columns: {missing}")
    matrix = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    if matrix.ndim != 2 or matrix.shape[1] != len(feature_order):
        raise ValueError("Feature matrix shape does not match feature order.")
    if not np.isfinite(matrix).all():
        raise ValueError("Feature matrix contains NaN or infinite values.")
    return matrix


def export_mt5_feature_matrix_csv(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    output_path: Path,
    *,
    timestamp_column: str = "timestamp",
    metadata_columns: Sequence[str] = (),
) -> dict[str, Any]:
    matrix = validate_feature_matrix(frame, feature_order)
    payload = pd.DataFrame()
    if timestamp_column in frame.columns:
        timestamps = pd.to_datetime(frame[timestamp_column], utc=True)
        payload["bar_time_server"] = timestamps.dt.strftime("%Y.%m.%d %H:%M:%S").to_numpy()
        payload["timestamp_utc"] = timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ").to_numpy()
    if "split" in frame.columns:
        payload["split"] = frame["split"].astype(str).to_numpy()
    for name in metadata_columns:
        if name in frame.columns and name not in payload.columns:
            payload[name] = frame[name].astype(str).to_numpy()
    payload["row_index"] = np.arange(len(frame), dtype="int64")
    feature_frame = pd.DataFrame(matrix.astype("float32"), columns=list(feature_order))
    payload = pd.concat([payload, feature_frame], axis=1)
    _io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(_io_path(output_path), index=False, encoding="utf-8", float_format="%.10g")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "rows": int(len(payload)),
        "feature_count": int(len(feature_order)),
        "feature_order_hash": ordered_hash(feature_order),
        "format": "csv_float32_ordered_features",
        "metadata_columns": [name for name in metadata_columns if name in frame.columns],
    }


def _format_mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def materialize_tester_set_file(parameters: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    _io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run_stage10_logreg_mt5_scout.py"]
    for key, value in parameters.items():
        lines.append(f"{key}={_format_mt5_value(value)}")
    _io_path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "mt5_set",
        "parameter_count": int(len(parameters)),
    }


def materialize_tester_ini_file(
    config: TesterMaterializationConfig,
    output_path: Path,
    *,
    set_file_path: Path | None = None,
) -> dict[str, Any]:
    tester_values: dict[str, Any] = {
        "Expert": config.expert,
        "Symbol": config.symbol,
        "Period": config.period,
        "Model": config.model,
        "Deposit": config.deposit,
        "Leverage": config.leverage,
        "Optimization": config.optimization,
        "ExecutionMode": config.execution_mode,
        "ForwardMode": config.forward_mode,
        "UseLocal": config.use_local,
        "UseRemote": config.use_remote,
        "UseCloud": config.use_cloud,
        "ReplaceReport": config.replace_report,
        "ShutdownTerminal": config.shutdown_terminal,
    }
    if config.from_date is not None:
        tester_values["FromDate"] = config.from_date
    if config.to_date is not None:
        tester_values["ToDate"] = config.to_date
    if config.report is not None:
        tester_values["Report"] = config.report
    if set_file_path is not None:
        tester_values["ExpertParameters"] = set_file_path.as_posix()

    lines = ["[Tester]"]
    for key, value in tester_values.items():
        lines.append(f"{key}={_format_mt5_value(value)}")
    _io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "mt5_tester_ini",
        "tester": tester_values,
    }


def common_ref(*parts: str) -> str:
    return "/".join([COMMON_RUN_ROOT, *parts])


def mt5_short_profile_ini_name(tier_name: str, split_name: str) -> str:
    if tier_name == TIER_AB:
        tier_code = "rt"
    else:
        tier_code = "ta" if tier_name == TIER_A else "tb"
    split_code = "v" if split_name == "validation_is" else "o"
    return f"opv2_{RUN_NUMBER}_{tier_code}_{split_code}.ini"


def materialize_mt5_attempt_files(
    *,
    run_output_root: Path,
    tier_name: str,
    split_name: str,
    local_onnx_path: Path,
    local_feature_matrix_path: Path,
    rule: ThresholdRule,
    feature_count: int,
    feature_order_hash: str,
    from_date: str,
    to_date: str,
) -> dict[str, Any]:
    stem = f"{tier_name.lower().replace(' ', '_').replace('+', 'ab')}_{split_name}"
    common_model = common_ref("models", local_onnx_path.name)
    common_matrix = common_ref("features", local_feature_matrix_path.name)
    common_telemetry = common_ref("telemetry", f"{stem}_telemetry.csv")
    common_summary = common_ref("telemetry", f"{stem}_summary.csv")
    set_path = run_output_root / "mt5" / f"{stem}.set"
    ini_path = run_output_root / "mt5" / f"{stem}.ini"
    set_payload = materialize_tester_set_file(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": tier_name,
            "InpSplitLabel": split_name,
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpModelPath": common_model,
            "InpModelId": f"{RUN_ID}_{tier_name.lower().replace(' ', '_').replace('+', 'ab')}",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_matrix,
            "InpFeatureCount": feature_count,
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": rule.short_threshold,
            "InpLongThreshold": rule.long_threshold,
            "InpMinMargin": rule.min_margin,
            "InpAllowTrading": "true",
            "InpFixedLot": 0.1,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpFeatureOrderHash": feature_order_hash,
            "InpMagic": 1001001 if tier_name == TIER_A else 1001002,
        },
        set_path,
    )
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{stem}"
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            from_date=from_date,
            to_date=to_date,
            report=report_name,
            shutdown_terminal=1,
        ),
        ini_path,
        set_file_path=Path(EA_TESTER_SET_NAME),
    )
    return {
        "tier": tier_name,
        "split": split_name,
        "set": set_payload,
        "ini": ini_payload,
        "common_model_path": common_model,
        "common_feature_matrix_path": common_matrix,
        "common_telemetry_path": common_telemetry,
        "common_summary_path": common_summary,
        "local_feature_matrix_path": local_feature_matrix_path.as_posix(),
    }


def materialize_mt5_routed_attempt_files(
    *,
    run_output_root: Path,
    split_name: str,
    primary_onnx_path: Path,
    primary_feature_matrix_path: Path,
    primary_feature_count: int,
    primary_feature_order_hash: str,
    fallback_onnx_path: Path,
    fallback_feature_matrix_path: Path,
    fallback_feature_count: int,
    fallback_feature_order_hash: str,
    rule: ThresholdRule,
    from_date: str,
    to_date: str,
) -> dict[str, Any]:
    stem = f"routed_{split_name}"
    common_primary_model = common_ref("models", primary_onnx_path.name)
    common_primary_matrix = common_ref("features", primary_feature_matrix_path.name)
    common_fallback_model = common_ref("models", fallback_onnx_path.name)
    common_fallback_matrix = common_ref("features", fallback_feature_matrix_path.name)
    common_telemetry = common_ref("telemetry", f"{stem}_telemetry.csv")
    common_summary = common_ref("telemetry", f"{stem}_summary.csv")
    set_path = run_output_root / "mt5" / f"{stem}.set"
    ini_path = run_output_root / "mt5" / f"{stem}.ini"
    primary_model_id = f"{RUN_ID}_tier_a_primary"
    fallback_model_id = f"{RUN_ID}_tier_b_fallback"
    set_payload = materialize_tester_set_file(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": TIER_AB,
            "InpSplitLabel": split_name,
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpModelPath": common_primary_model,
            "InpModelId": primary_model_id,
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_primary_matrix,
            "InpFeatureCount": primary_feature_count,
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFeatureOrderHash": primary_feature_order_hash,
            "InpFallbackEnabled": "true",
            "InpFallbackTierLabel": "Tier B partial-context fallback",
            "InpFallbackFeatureCsvPath": common_fallback_matrix,
            "InpFallbackFeatureCount": fallback_feature_count,
            "InpFallbackModelPath": common_fallback_model,
            "InpFallbackModelId": fallback_model_id,
            "InpFallbackFeatureOrderHash": fallback_feature_order_hash,
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": rule.short_threshold,
            "InpLongThreshold": rule.long_threshold,
            "InpMinMargin": rule.min_margin,
            "InpAllowTrading": "true",
            "InpFixedLot": 0.1,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpMagic": 1001010,
        },
        set_path,
    )
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{stem}"
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            from_date=from_date,
            to_date=to_date,
            report=report_name,
            shutdown_terminal=1,
        ),
        ini_path,
        set_file_path=Path(EA_TESTER_SET_NAME),
    )
    return {
        "tier": TIER_AB,
        "split": split_name,
        "routing_mode": "tier_a_primary_tier_b_fallback",
        "routing_detail": "tier_a_primary_tier_b_partial_context_fallback",
        "set": set_payload,
        "ini": ini_payload,
        "common_model_path": common_primary_model,
        "common_feature_matrix_path": common_primary_matrix,
        "common_telemetry_path": common_telemetry,
        "common_summary_path": common_summary,
        "primary": {
            "tier": TIER_A,
            "model_id": primary_model_id,
            "common_model_path": common_primary_model,
            "common_feature_matrix_path": common_primary_matrix,
            "feature_count": primary_feature_count,
            "feature_order_hash": primary_feature_order_hash,
            "local_feature_matrix_path": primary_feature_matrix_path.as_posix(),
        },
        "fallback": {
            "tier": TIER_B,
            "model_id": fallback_model_id,
            "common_model_path": common_fallback_model,
            "common_feature_matrix_path": common_fallback_matrix,
            "feature_count": fallback_feature_count,
            "feature_order_hash": fallback_feature_order_hash,
            "policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID,
            "local_feature_matrix_path": fallback_feature_matrix_path.as_posix(),
        },
    }


def copy_to_common_files(common_files_root: Path, local_path: Path, common_path: str) -> dict[str, Any]:
    destination = common_files_root / Path(common_path)
    _io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(_io_path(local_path), _io_path(destination))
    return {
        "source": local_path.as_posix(),
        "common_path": common_path,
        "absolute_path": destination.as_posix(),
        "sha256": sha256_file(destination),
    }


def compile_mql5_ea(metaeditor_path: Path, source_path: Path, log_path: Path) -> dict[str, Any]:
    command = [str(metaeditor_path), f"/compile:{source_path.resolve()}", f"/log:{log_path.resolve()}"]
    if not _path_exists(metaeditor_path):
        return {
            "status": "blocked",
            "command": command,
            "returncode": None,
            "log_path": log_path.as_posix(),
            "blocker": "metaeditor_missing",
        }
    _io_path(log_path.parent).mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, timeout=120)
    actual_log_path = log_path
    if not _path_exists(actual_log_path) and log_path.suffix:
        extensionless_log = log_path.with_suffix("")
        if _path_exists(extensionless_log):
            actual_log_path = extensionless_log

    log_text = ""
    if _path_exists(actual_log_path):
        raw_log = _io_path(actual_log_path).read_bytes()
        for encoding in ("utf-16", "utf-8-sig", "cp949"):
            try:
                log_text = raw_log.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if not log_text:
            log_text = raw_log.decode("utf-8", errors="ignore")

    lowered = log_text.lower()
    zero_errors = "0 errors" in lowered or "0 error" in lowered or "0 error(s)" in lowered
    has_error = "error" in lowered and not zero_errors
    completed = (proc.returncode == 0 or zero_errors) and not has_error
    return {
        "status": "completed" if completed else "blocked",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "log_path": actual_log_path.as_posix(),
        "log_sha256": sha256_file(actual_log_path) if _path_exists(actual_log_path) else None,
    }


def run_mt5_tester(
    terminal_path: Path,
    ini_path: Path,
    *,
    set_path: Path | None = None,
    tester_profile_set_path: Path | None = None,
    tester_profile_ini_path: Path | None = None,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    execution_ini_path = ini_path
    ini_copy_payload = None
    if tester_profile_ini_path is not None:
        _io_path(tester_profile_ini_path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(_io_path(ini_path), _io_path(tester_profile_ini_path))
        execution_ini_path = tester_profile_ini_path
        ini_copy_payload = {
            "source": ini_path.as_posix(),
            "destination": tester_profile_ini_path.as_posix(),
            "sha256": sha256_file(tester_profile_ini_path),
        }

    command = [str(terminal_path), f"/config:{execution_ini_path.resolve()}"]
    if not _path_exists(terminal_path):
        return {
            "status": "blocked",
            "command": command,
            "returncode": None,
            "blocker": "terminal_missing",
        }
    set_copy_payload = None
    if set_path is not None and tester_profile_set_path is not None:
        _io_path(tester_profile_set_path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(_io_path(set_path), _io_path(tester_profile_set_path))
        set_copy_payload = {
            "source": set_path.as_posix(),
            "destination": tester_profile_set_path.as_posix(),
            "sha256": sha256_file(tester_profile_set_path),
        }
    proc = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, timeout=timeout_seconds)
    return {
        "status": "completed" if proc.returncode == 0 else "blocked",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "tester_profile_set_copy": set_copy_payload,
        "tester_profile_ini_copy": ini_copy_payload,
    }


def report_name_from_attempt(attempt: Mapping[str, Any]) -> str:
    tester = attempt.get("ini", {}).get("tester", {})
    report_name = tester.get("Report")
    if not report_name:
        stem = f"{str(attempt['tier']).lower().replace(' ', '_').replace('+', 'ab')}_{attempt['split']}"
        report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{stem}"
    return str(report_name)


def remove_existing_mt5_report_artifacts(terminal_data_root: Path, attempt: Mapping[str, Any]) -> None:
    report_name = report_name_from_attempt(attempt)
    for suffix in (".htm", ".html", ".png"):
        path = terminal_data_root / f"{report_name}{suffix}"
        if _path_exists(path):
            _io_path(path).unlink()


def collect_mt5_strategy_report_artifacts(
    *,
    terminal_data_root: Path,
    run_output_root: Path,
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    reports_root = run_output_root / "mt5" / "reports"
    _io_path(reports_root).mkdir(parents=True, exist_ok=True)
    for existing_name in os.listdir(_io_path(reports_root)):
        if not existing_name.startswith("Project_Obsidian_Prime_v2_"):
            continue
        existing = reports_root / existing_name
        existing_io = _io_path(existing)
        if existing_io.is_file():
            existing_io.unlink()
    records: list[dict[str, Any]] = []
    for attempt in attempts:
        report_name = report_name_from_attempt(attempt)
        record: dict[str, Any] = {
            "tier": attempt["tier"],
            "split": attempt["split"],
            "report_name": report_name,
            "status": "missing",
        }
        html_source = next(
            (path for path in (terminal_data_root / f"{report_name}{suffix}" for suffix in (".htm", ".html")) if _path_exists(path)),
            None,
        )
        if html_source is not None:
            html_destination = reports_root / html_source.name
            shutil.copy2(_io_path(html_source), _io_path(html_destination))
            record["html_report"] = {
                "source_path": html_source.as_posix(),
                "path": html_destination.as_posix(),
                "sha256": sha256_file(html_destination),
            }
            record["metrics"] = extract_mt5_strategy_report_metrics(html_destination)
            record["status"] = record["metrics"]["status"]

        chart_source = terminal_data_root / f"{report_name}.png"
        if _path_exists(chart_source):
            chart_destination = reports_root / chart_source.name
            shutil.copy2(_io_path(chart_source), _io_path(chart_destination))
            record["chart"] = {
                "source_path": chart_source.as_posix(),
                "path": chart_destination.as_posix(),
                "sha256": sha256_file(chart_destination),
            }
        records.append(record)
    return records


def _to_int(value: Any) -> int:
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        return 0
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None


def attach_mt5_report_metrics(
    execution_results: list[dict[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> None:
    records_by_key = {(record.get("tier"), record.get("split")): record for record in report_records}
    for result in execution_results:
        report_record = records_by_key.get((result.get("tier"), result.get("split")))
        if report_record is not None:
            result["strategy_tester_report"] = dict(report_record)


def mt5_metrics_with_runtime_counts(result: Mapping[str, Any]) -> dict[str, Any]:
    metrics = dict(result.get("strategy_tester_report", {}).get("metrics", {}))
    last_summary = result.get("runtime_outputs", {}).get("last_summary", {})
    order_attempt_count = _to_int(last_summary.get("order_attempt_count"))
    order_fill_count = _to_int(last_summary.get("order_fill_count"))
    feature_skip_count = _to_int(last_summary.get("feature_skip_count"))
    reject_count = max(order_attempt_count - order_fill_count, 0)
    metrics.update(
        {
            "order_attempt_count": order_attempt_count,
            "fill_count": order_fill_count,
            "reject_count": reject_count,
            "skip_count": feature_skip_count,
            "fill_rate": float(order_fill_count / order_attempt_count) if order_attempt_count else None,
            "feature_ready_count": _to_int(last_summary.get("feature_ready_count")),
            "model_ok_count": _to_int(last_summary.get("model_ok_count")),
            "model_fail_count": _to_int(last_summary.get("model_fail_count")),
            "tier_a_used_count": _to_int(last_summary.get("tier_a_used_count")),
            "tier_b_fallback_used_count": _to_int(last_summary.get("tier_b_fallback_used_count")),
            "no_tier_count": _to_int(last_summary.get("no_tier_count")),
            "tier_a_long_count": _to_int(last_summary.get("tier_a_long_count")),
            "tier_a_short_count": _to_int(last_summary.get("tier_a_short_count")),
            "tier_a_flat_count": _to_int(last_summary.get("tier_a_flat_count")),
            "tier_a_order_attempt_count": _to_int(last_summary.get("tier_a_order_attempt_count")),
            "tier_a_order_fill_count": _to_int(last_summary.get("tier_a_order_fill_count")),
            "tier_b_fallback_long_count": _to_int(last_summary.get("tier_b_fallback_long_count")),
            "tier_b_fallback_short_count": _to_int(last_summary.get("tier_b_fallback_short_count")),
            "tier_b_fallback_flat_count": _to_int(last_summary.get("tier_b_fallback_flat_count")),
            "tier_b_fallback_order_attempt_count": _to_int(last_summary.get("tier_b_fallback_order_attempt_count")),
            "tier_b_fallback_order_fill_count": _to_int(last_summary.get("tier_b_fallback_order_fill_count")),
        }
    )
    return metrics


def routed_component_metrics(total_metrics: Mapping[str, Any], route_role: str) -> dict[str, Any]:
    if route_role == "primary_used":
        prefix = "tier_a"
        tier_scope = TIER_A
        record_status = "completed"
    elif route_role == "fallback_used":
        prefix = "tier_b_fallback"
        tier_scope = TIER_B
        record_status = "completed"
    else:
        raise ValueError(f"Unsupported route_role: {route_role}")

    used_count = _to_int(total_metrics.get(f"{prefix}_used_count"))
    long_count = _to_int(total_metrics.get(f"{prefix}_long_count"))
    short_count = _to_int(total_metrics.get(f"{prefix}_short_count"))
    flat_count = _to_int(total_metrics.get(f"{prefix}_flat_count"))
    order_attempt_count = _to_int(total_metrics.get(f"{prefix}_order_attempt_count"))
    fill_count = _to_int(total_metrics.get(f"{prefix}_order_fill_count"))
    route_denominator = _to_int(total_metrics.get("model_ok_count")) or (
        _to_int(total_metrics.get("tier_a_used_count")) + _to_int(total_metrics.get("tier_b_fallback_used_count"))
    )
    return {
        "status": record_status,
        "tier_scope": tier_scope,
        "route_role": route_role,
        "aggregation": "actual_routed_component",
        "profit_attribution": "not_separable_from_single_routed_account_path",
        "net_profit": None,
        "profit_factor": None,
        "expectancy": None,
        "trade_count": None,
        "win_rate_percent": None,
        "max_drawdown_amount": None,
        "max_drawdown_percent": None,
        "recovery_factor": None,
        "route_bar_count": used_count,
        "route_share": float(used_count / route_denominator) if route_denominator else None,
        "signal_count": long_count + short_count,
        "long_count": long_count,
        "short_count": short_count,
        "flat_count": flat_count,
        "order_attempt_count": order_attempt_count,
        "fill_count": fill_count,
        "reject_count": max(order_attempt_count - fill_count, 0),
        "skip_count": 0,
        "fill_rate": float(fill_count / order_attempt_count) if order_attempt_count else None,
    }


def build_mt5_kpi_records(execution_results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for result in execution_results:
        if result.get("status") != "completed":
            continue
        tier = str(result.get("tier"))
        split = str(result.get("split"))
        metrics = mt5_metrics_with_runtime_counts(result)
        if result.get("routing_mode") == "tier_a_primary_tier_b_fallback":
            for route_role, record_view, tier_scope in (
                ("primary_used", f"mt5_routed_tier_a_used_{split}", TIER_A),
                ("fallback_used", f"mt5_routed_tier_b_fallback_used_{split}", TIER_B),
            ):
                component = routed_component_metrics(metrics, route_role)
                records.append(
                    {
                        "record_view": record_view,
                        "tier_scope": tier_scope,
                        "split": split,
                        "status": component["status"],
                        "route_role": route_role,
                        "metrics": component,
                        "report": {
                            "aggregation": "actual_routed_component",
                            "source_report": result.get("strategy_tester_report", {}),
                            "profit_attribution": component["profit_attribution"],
                        },
                    }
                )
            metrics["aggregation"] = "actual_routed_tester_run"
            metrics["route_role"] = "routed_total"
            records.append(
                {
                    "record_view": f"mt5_routed_total_{split}",
                    "tier_scope": TIER_AB,
                    "split": split,
                    "status": metrics.get("status", "partial"),
                    "route_role": "routed_total",
                    "metrics": metrics,
                    "report": result.get("strategy_tester_report", {}),
                }
            )
            continue
        records.append(
            {
                "record_view": f"mt5_{tier.lower().replace(' ', '_').replace('+', 'ab')}_{split}",
                "tier_scope": tier,
                "split": split,
                "status": metrics.get("status", "partial"),
                "metrics": metrics,
                "report": result.get("strategy_tester_report", {}),
            }
        )
    return records


def enrich_mt5_kpi_records_with_route_coverage(
    records: Sequence[dict[str, Any]],
    route_coverage: Mapping[str, Any],
) -> list[dict[str, Any]]:
    split_aliases = {"validation_is": "validation", "validation": "validation", "oos": "oos", "train": "train"}
    by_split = route_coverage.get("by_split", {})
    subtype_by_split = route_coverage.get("tier_b_fallback_by_split_subtype", {})
    no_tier_by_split = route_coverage.get("no_tier_by_split", {})
    for record in records:
        split = split_aliases.get(str(record.get("split")), str(record.get("split")))
        metrics = record.setdefault("metrics", {})
        split_summary = dict(by_split.get(split, {})) if isinstance(by_split, Mapping) else {}
        metrics["route_coverage_split"] = split
        metrics["tier_a_primary_labelable_rows"] = split_summary.get("tier_a_primary_rows")
        metrics["tier_b_fallback_labelable_rows"] = split_summary.get("tier_b_fallback_rows")
        metrics["no_tier_labelable_rows"] = no_tier_by_split.get(split)
        metrics["routed_labelable_rows"] = split_summary.get("routed_labelable_rows")
        if record.get("route_role") in {"fallback_used", "routed_total"}:
            metrics["partial_context_subtype_counts"] = subtype_by_split.get(split, {})
    return list(records)


def _ledger_status(value: Any) -> str:
    text = str(value or "")
    return "completed" if text.startswith("completed") else text


def _ledger_value(value: Any) -> str:
    if value is None:
        return "NA"
    if isinstance(value, (np.integer, int)):
        return str(int(value))
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if not np.isfinite(number):
            return "NA"
        if number.is_integer():
            return str(int(number))
        return f"{number:.6g}"
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(_json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def _ledger_pairs(pairs: Sequence[tuple[str, Any]]) -> str:
    return ";".join(f"{key}={_ledger_value(value)}" for key, value in pairs)


def _ledger_path(path: Any) -> str:
    return Path(str(path)).as_posix() if path else ""


def build_alpha_ledger_rows(
    *,
    tier_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    selected_threshold_id: str,
    run_output_root: Path,
    external_verification_status: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    kpi_record_path = (run_output_root / "kpi_record.json").as_posix()
    report_paths: dict[str, Any] = {}
    for record in mt5_kpi_records:
        report = record.get("report", {})
        if not isinstance(report, Mapping):
            continue
        split = str(record.get("split"))
        html_report = report.get("html_report", {})
        metrics_report = report.get("metrics", {})
        if isinstance(html_report, Mapping) and html_report.get("path"):
            report_paths[split] = html_report.get("path")
        elif isinstance(metrics_report, Mapping) and metrics_report.get("report_path"):
            report_paths[split] = metrics_report.get("report_path")

    for record in tier_records:
        record_view = str(record.get("record_view"))
        metrics = record.get("metrics", {})
        row_view = f"python_{record_view}"
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{row_view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": row_view,
                "parent_run_id": RUN_ID,
                "record_view": row_view,
                "tier_scope": str(record.get("tier_scope")),
                "kpi_scope": "signal_probability_threshold",
                "scoreboard_lane": "structural_scout",
                "status": _ledger_status(record.get("status")),
                "judgment": "inconclusive_single_split_scout_payload",
                "path": _ledger_path(record.get("path")),
                "primary_kpi": _ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_coverage", metrics.get("signal_coverage")),
                        ("signal_count", metrics.get("signal_count")),
                        ("short", metrics.get("short_count")),
                        ("long", metrics.get("long_count")),
                    )
                ),
                "guardrail_kpi": _ledger_pairs(
                    (
                        ("prob_sum_err", metrics.get("probability_row_sum_max_abs_error")),
                        ("selected_threshold", selected_threshold_id),
                        ("subtype_counts", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": (
                    "Tier B partial-context fallback-only view"
                    if record.get("tier_scope") == TIER_B
                    else "Tier A primary plus Tier B fallback routed Python view"
                    if record.get("tier_scope") == TIER_AB
                    else "Tier A full-context primary view"
                ),
            }
        )

    for record in mt5_kpi_records:
        metrics = record.get("metrics", {})
        route_role = str(record.get("route_role") or "")
        split = str(record.get("split"))
        is_total = route_role == "routed_total"
        row_path = report_paths.get(split) if is_total else kpi_record_path
        if is_total:
            primary_kpi = _ledger_pairs(
                (
                    ("net_profit", metrics.get("net_profit")),
                    ("pf", metrics.get("profit_factor")),
                    ("expectancy", metrics.get("expectancy")),
                    ("trades", metrics.get("trade_count")),
                    ("win_rate", metrics.get("win_rate_percent")),
                )
            )
            guardrail_kpi = _ledger_pairs(
                (
                    ("a_used", metrics.get("tier_a_used_count")),
                    ("b_fallback", metrics.get("tier_b_fallback_used_count")),
                    ("no_tier_labelable", metrics.get("no_tier_labelable_rows")),
                    ("max_dd", metrics.get("max_drawdown_amount")),
                    ("recovery", metrics.get("recovery_factor")),
                    ("fill", metrics.get("fill_count")),
                    ("reject", metrics.get("reject_count")),
                    ("skip", metrics.get("skip_count")),
                )
            )
            notes = "Actual routed total from one MT5 tester account path; not a synthetic sum."
        else:
            primary_kpi = _ledger_pairs(
                (
                    ("route_bars", metrics.get("route_bar_count")),
                    ("route_share", metrics.get("route_share")),
                    ("signals", metrics.get("signal_count")),
                    ("long", metrics.get("long_count")),
                    ("short", metrics.get("short_count")),
                    ("fills", metrics.get("fill_count")),
                )
            )
            guardrail_kpi = _ledger_pairs(
                (
                    ("profit_attribution", metrics.get("profit_attribution")),
                    ("reject", metrics.get("reject_count")),
                    ("skip", metrics.get("skip_count")),
                    ("subtypes", metrics.get("partial_context_subtype_counts")),
                )
            )
            notes = (
                "Tier B partial-context fallback used component from one routed MT5 tester run."
                if route_role == "fallback_used"
                else "Tier A primary used component from one routed MT5 tester run."
            )
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{record.get('record_view')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": str(record.get("record_view")),
                "parent_run_id": RUN_ID,
                "record_view": str(record.get("record_view")),
                "tier_scope": str(record.get("tier_scope")),
                "kpi_scope": "trading_risk_execution" if is_total else "routed_signal_execution_usage",
                "scoreboard_lane": "runtime_probe",
                "status": _ledger_status(record.get("status")),
                "judgment": "inconclusive_routed_total_runtime_probe" if is_total else "inconclusive_routed_component_runtime_probe",
                "path": _ledger_path(row_path),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail_kpi,
                "external_verification_status": external_verification_status,
                "notes": notes,
            }
        )
    return rows


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not _path_exists(path):
        return []
    with _io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with _io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: _ledger_value(row.get(column, "")) for column in columns})


def _upsert_csv_rows(
    path: Path,
    columns: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    key: str,
) -> dict[str, Any]:
    existing = _read_csv_rows(path)
    new_keys = {str(row.get(key)) for row in rows}
    merged = [row for row in existing if str(row.get(key)) not in new_keys]
    merged.extend(dict(row) for row in rows)
    _write_csv_rows(path, columns, merged)
    return {
        "path": path.as_posix(),
        "sha256": sha256_file_lf_normalized(path),
        "hash_policy": "lf_normalized_text_register",
        "rows": len(merged),
        "upserted_rows": len(rows),
    }


def materialize_alpha_ledgers(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    stage_payload = _upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = _upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    return {"stage_run_ledger": stage_payload, "project_alpha_run_ledger": project_payload}


def materialize_run_registry_row(
    *,
    route_coverage: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    run_output_root: Path,
    external_verification_status: str,
) -> dict[str, Any]:
    totals = {str(record.get("split")): record.get("metrics", {}) for record in mt5_kpi_records if record.get("route_role") == "routed_total"}
    validation = totals.get("validation_is", {})
    oos = totals.get("oos", {})
    notes = _ledger_pairs(
        (
            ("routing", "tier_a_primary_tier_b_partial_context_fallback"),
            ("tier_b_fallback_rows", route_coverage.get("tier_b_fallback_rows")),
            ("no_tier_labelable_rows", route_coverage.get("no_tier_labelable_rows")),
            ("validation_net_profit", validation.get("net_profit")),
            ("validation_pf", validation.get("profit_factor")),
            ("validation_b_fallback_used", validation.get("tier_b_fallback_used_count")),
            ("oos_net_profit", oos.get("net_profit")),
            ("oos_pf", oos.get("profit_factor")),
            ("oos_b_fallback_used", oos.get("tier_b_fallback_used_count")),
            ("external_verification", external_verification_status),
            ("boundary", "runtime_probe_only"),
        )
    )
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if external_verification_status == "completed" else "payload_only",
        "judgment": "inconclusive_single_split_scout_mt5_routed_completed"
        if external_verification_status == "completed"
        else "inconclusive_single_split_scout_payload",
        "path": run_output_root.as_posix(),
        "notes": notes,
    }
    return _upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def validate_mt5_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> dict[str, Any]:
    telemetry_path = common_files_root / Path(str(attempt["common_telemetry_path"]))
    summary_path = common_files_root / Path(str(attempt["common_summary_path"]))
    payload: dict[str, Any] = {
        "telemetry_path": telemetry_path.as_posix(),
        "summary_path": summary_path.as_posix(),
        "telemetry_exists": _path_exists(telemetry_path),
        "summary_exists": _path_exists(summary_path),
        "status": "blocked",
    }
    if _path_exists(telemetry_path):
        payload["telemetry_sha256"] = sha256_file(telemetry_path)
    if _path_exists(summary_path):
        payload["summary_sha256"] = sha256_file(summary_path)
        try:
            summary = pd.read_csv(_io_path(summary_path))
            if not summary.empty:
                last = summary.iloc[-1].to_dict()
                payload["last_summary"] = _json_ready(last)
                deinit_reason = str(last.get("deinit_reason", ""))
                model_ok_count = int(last.get("model_ok_count", 0) or 0)
                feature_ready_count = int(last.get("feature_ready_count", 0) or 0)
                payload["status"] = (
                    "completed" if deinit_reason != "init_failed" and model_ok_count > 0 and feature_ready_count > 0 else "blocked"
                )
        except Exception as exc:  # pragma: no cover - defensive MT5 handoff parsing
            payload["parse_error"] = str(exc)
    return payload


def wait_for_mt5_runtime_outputs(
    common_files_root: Path,
    attempt: Mapping[str, Any],
    *,
    timeout_seconds: int = 600,
    poll_seconds: float = 2.0,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    latest = validate_mt5_runtime_outputs(common_files_root, attempt)
    while time.monotonic() < deadline:
        latest = validate_mt5_runtime_outputs(common_files_root, attempt)
        if latest["status"] == "completed":
            latest["wait_status"] = "completed"
            return latest
        time.sleep(poll_seconds)
    latest = validate_mt5_runtime_outputs(common_files_root, attempt)
    latest["wait_status"] = "timeout"
    latest["wait_timeout_seconds"] = timeout_seconds
    return latest


def build_run_manifest_payload(
    *,
    run_id: str,
    run_number: str,
    stage_id: str,
    exploration_label: str,
    input_refs: Mapping[str, Any],
    artifacts: Sequence[Mapping[str, Any]],
    threshold_selection: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
    external_verification_status: str = "out_of_scope_by_claim",
) -> dict[str, Any]:
    return {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": stage_id,
            "exploration_label": exploration_label,
            "lane": "single_split_scout",
            "scoreboard_lane": "structural_scout",
            "model_family": "sklearn_logistic_regression_multiclass",
        },
        "inputs": dict(input_refs),
        "artifacts": list(artifacts),
        "threshold": dict(threshold_selection),
        "tier_pair_records": list(tier_records),
        "onnx_probability_parity": dict(onnx_parity),
        "external_verification_status": external_verification_status,
        "judgment_boundary": {
            "status": "payload_generated_not_reviewed",
            "claim": "single_split_scout_payload_only",
            "not_claimed": [
                "alpha_quality",
                "live_readiness",
                "runtime_authority_expansion",
                "operating_promotion",
            ],
        },
    }


def build_kpi_record_payload(
    *,
    run_id: str,
    stage_id: str,
    threshold_sweep: pd.DataFrame,
    threshold_sweeps: Mapping[str, pd.DataFrame] | None = None,
    tier_records: Sequence[Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    best = select_threshold_from_sweep(threshold_sweep) if not threshold_sweep.empty else {}
    mt5_kpi_records = list(mt5_kpi_records or [])
    return {
        "run_id": run_id,
        "stage_id": stage_id,
        "scoreboard_lane": "runtime_probe",
        "kpi_scope": "signal_probability_threshold_trading_risk_execution",
        "signal": {
            "tier_pair_records": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "signal_count": record.get("metrics", {}).get("signal_count"),
                    "short_count": record.get("metrics", {}).get("short_count"),
                    "long_count": record.get("metrics", {}).get("long_count"),
                    "signal_coverage": record.get("metrics", {}).get("signal_coverage"),
                }
                for record in tier_records
            ],
        },
        "probability": {
            "onnx_probability_parity_passed": onnx_parity.get("passed"),
            "onnx_probability_max_abs_diff": onnx_parity.get("max_abs_diff"),
            "row_sum_guardrail": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "probability_row_sum_max_abs_error": record.get("metrics", {}).get("probability_row_sum_max_abs_error"),
                }
                for record in tier_records
            ],
        },
        "threshold": {
            "selection_scope": "validation_is_routed_tier_a_primary_tier_b_fallback_only",
            "selected_threshold_id": best.get("threshold_id"),
            "directional_hit_rate": best.get("directional_hit_rate"),
            "coverage": best.get("coverage"),
            "sweeps": {
                view: {
                    "rows": int(len(sweep)),
                    "best": select_threshold_from_sweep(sweep) if not sweep.empty else {},
                }
                for view, sweep in (threshold_sweeps or {"tier_ab_combined": threshold_sweep}).items()
            },
        },
        "routing": {
            "routing_mode": "tier_a_primary_tier_b_fallback",
            "primary_tier": TIER_A,
            "fallback_tier": TIER_B,
            "route_source_required": True,
            "fallback_reason_required": True,
            "records": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "split": record.get("split"),
                    "route_role": record.get("route_role"),
                    "aggregation": record.get("metrics", {}).get("aggregation"),
                    "profit_attribution": record.get("metrics", {}).get("profit_attribution"),
                    "route_bar_count": record.get("metrics", {}).get("route_bar_count"),
                    "route_share": record.get("metrics", {}).get("route_share"),
                    "partial_context_subtype_counts": record.get("metrics", {}).get("partial_context_subtype_counts"),
                    "no_tier_labelable_rows": record.get("metrics", {}).get("no_tier_labelable_rows"),
                    "routed_labelable_rows": record.get("metrics", {}).get("routed_labelable_rows"),
                }
                for record in mt5_kpi_records
            ],
        },
        "trading": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "net_profit": record.get("metrics", {}).get("net_profit"),
                "profit_factor": record.get("metrics", {}).get("profit_factor"),
                "expectancy": record.get("metrics", {}).get("expectancy"),
                "trade_count": record.get("metrics", {}).get("trade_count"),
                "win_rate_percent": record.get("metrics", {}).get("win_rate_percent"),
            }
            for record in mt5_kpi_records
        ],
        "risk": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "max_drawdown_amount": record.get("metrics", {}).get("max_drawdown_amount"),
                "max_drawdown_percent": record.get("metrics", {}).get("max_drawdown_percent"),
                "recovery_factor": record.get("metrics", {}).get("recovery_factor"),
            }
            for record in mt5_kpi_records
        ],
        "execution": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "fill_count": record.get("metrics", {}).get("fill_count"),
                "reject_count": record.get("metrics", {}).get("reject_count"),
                "skip_count": record.get("metrics", {}).get("skip_count"),
                "fill_rate": record.get("metrics", {}).get("fill_rate"),
            }
            for record in mt5_kpi_records
        ],
        "judgment_read": {
            "judgment": "inconclusive_single_split_scout_mt5_routed_completed" if mt5_kpi_records else "inconclusive_payload_only",
            "boundary": "runtime_probe only; not live readiness, runtime authority expansion, or operating promotion.",
            "mt5_record_count": len(mt5_kpi_records),
        },
        "tier_pair_records": list(tier_records),
    }


def materialize_manifest_and_kpi(
    output_root: Path,
    *,
    manifest_payload: Mapping[str, Any],
    kpi_payload: Mapping[str, Any],
) -> dict[str, Any]:
    manifest_path = output_root / "run_manifest.json"
    kpi_path = output_root / "kpi_record.json"
    write_json(manifest_path, manifest_payload)
    write_json(kpi_path, kpi_payload)
    return {
        "run_manifest": {"path": manifest_path.as_posix(), "sha256": sha256_file(manifest_path)},
        "kpi_record": {"path": kpi_path.as_posix(), "sha256": sha256_file(kpi_path)},
    }


def run_stage10_logreg_mt5_scout(
    *,
    model_input_path: Path,
    feature_order_path: Path,
    tier_b_model_input_path: Path,
    tier_b_feature_order_path: Path,
    raw_root: Path,
    training_summary_path: Path,
    stage07_model_path: Path,
    run_output_root: Path,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    tier_column: str = TIER_COLUMN,
    random_seed: int = 10,
    max_iter: int = 2000,
    parity_rows: int = 128,
    attempt_mt5: bool = False,
    terminal_path: Path = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe"),
    metaeditor_path: Path = Path(r"C:\Program Files\MetaTrader 5\MetaEditor64.exe"),
) -> dict[str, Any]:
    tier_a_feature_order = load_feature_order(feature_order_path)
    tier_a_feature_hash = ordered_hash(tier_a_feature_order)
    if tier_a_feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {tier_a_feature_hash} != {FEATURE_ORDER_HASH}")

    stage04_tier_b_feature_order = load_feature_order(tier_b_feature_order_path)
    tier_b_feature_order = list(TIER_B_CORE_FEATURE_ORDER)
    missing_core_features = sorted(set(tier_b_feature_order).difference(stage04_tier_b_feature_order))
    if missing_core_features:
        raise RuntimeError(f"Tier B core feature order is missing Stage04 reference features: {missing_core_features}")
    tier_b_feature_hash = ordered_hash(tier_b_feature_order)
    label_threshold = load_label_threshold(training_summary_path)

    tier_a_frame = pd.read_parquet(_io_path(model_input_path))
    tier_a_frame["timestamp"] = pd.to_datetime(tier_a_frame["timestamp"], utc=True)
    tier_a_frame["route_role"] = ROUTE_ROLE_A_PRIMARY
    tier_a_frame["partial_context_subtype"] = "Tier_A_full_context"
    tier_a_frame["missing_feature_group_mask"] = "none"
    tier_a_frame["available_feature_group_mask"] = "macro|constituent|basket"
    tier_a_frame["tier_a_primary_available"] = True
    tier_a_frame["tier_a_full_feature_ready"] = True
    tier_a_frame["tier_b_core_ready"] = True
    tier_b_context = build_tier_b_partial_context_frames(
        raw_root=raw_root,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
    )
    tier_b_training_frame = tier_b_context["tier_b_training_frame"]
    tier_b_frame = tier_b_context["tier_b_fallback_frame"]
    no_tier_frame = tier_b_context["no_tier_frame"]
    route_coverage = tier_b_context["summary"]
    config = BaselineTrainingConfig(random_seed=random_seed, max_iter=max_iter)
    tier_a_model = joblib.load(_io_path(stage07_model_path))
    tier_b_model = train_baseline_model(tier_b_training_frame, list(tier_b_feature_order), config)

    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    models_root = run_output_root / "models"
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    mt5_root = run_output_root / "mt5"
    reports_root = run_output_root / "reports"

    tier_a_model_path = models_root / "tier_a_stage07_model.joblib"
    tier_b_model_path = models_root / "tier_b_logreg_core42_model.joblib"
    tier_b_feature_order_path_run = models_root / "tier_b_core42_feature_order.txt"
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    no_tier_route_path = predictions_root / "no_tier_route_rows.parquet"
    route_coverage_path = predictions_root / "route_coverage_summary.json"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    threshold_sweep_path = sweeps_root / "threshold_sweep_validation_combined.csv"
    tier_a_onnx_path = models_root / "tier_a_stage07_logreg.onnx"
    tier_b_onnx_path = models_root / "tier_b_logreg_core42_partial_context.onnx"

    validation_a = tier_a_frame.loc[tier_a_frame["split"].astype(str).eq("validation")].copy()
    validation_b = tier_b_frame.loc[tier_b_frame["split"].astype(str).eq("validation")].copy()
    values_a = validation_a.loc[:, list(tier_a_feature_order)].to_numpy(dtype="float64", copy=False)
    values_b = validation_b.loc[:, list(tier_b_feature_order)].to_numpy(dtype="float64", copy=False)
    validation_probabilities = np.vstack(
        [
            ordered_sklearn_probabilities(tier_a_model, values_a),
            ordered_sklearn_probabilities(tier_b_model, values_b),
        ]
    )
    validation_labels = np.concatenate(
        [
            validation_a["label_class"].astype("int64").to_numpy(),
            validation_b["label_class"].astype("int64").to_numpy(),
        ]
    )
    threshold_sweeps = {
        "tier_a_separate": sweep_threshold_rules(
            ordered_sklearn_probabilities(tier_a_model, values_a),
            validation_a["label_class"].astype("int64").to_numpy(),
        ),
        "tier_b_separate": sweep_threshold_rules(
            ordered_sklearn_probabilities(tier_b_model, values_b),
            validation_b["label_class"].astype("int64").to_numpy(),
        ),
        "tier_ab_combined": sweep_threshold_rules(
            validation_probabilities,
            validation_labels,
        ),
    }
    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)
    threshold_sweep_paths = {
        "tier_a_separate": sweeps_root / "threshold_sweep_validation_tier_a.csv",
        "tier_b_separate": sweeps_root / "threshold_sweep_validation_tier_b.csv",
        "tier_ab_combined": threshold_sweep_path,
    }
    for view_name, sweep in threshold_sweeps.items():
        sweep.to_csv(_io_path(threshold_sweep_paths[view_name]), index=False)
    threshold_sweep = threshold_sweeps["tier_ab_combined"]
    selected = select_threshold_from_sweep(threshold_sweep)
    rule = ThresholdRule(
        threshold_id=str(selected["threshold_id"]),
        short_threshold=float(selected["short_threshold"]),
        long_threshold=float(selected["long_threshold"]),
        min_margin=float(selected["min_margin"]),
    )

    tier_a_predictions = build_prediction_frame(tier_a_model, tier_a_frame, tier_a_feature_order, rule)
    tier_b_predictions = build_prediction_frame(tier_b_model, tier_b_frame, tier_b_feature_order, rule)
    tier_a_predictions[tier_column] = TIER_A
    tier_b_predictions[tier_column] = TIER_B
    tier_a_predictions["feature_count"] = len(tier_a_feature_order)
    tier_b_predictions["feature_count"] = len(tier_b_feature_order)
    tier_a_predictions["feature_order_hash"] = tier_a_feature_hash
    tier_b_predictions["feature_order_hash"] = tier_b_feature_hash
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)
    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    no_tier_frame.to_parquet(_io_path(no_tier_route_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)
    write_json(route_coverage_path, route_coverage)

    tier_views = build_tier_prediction_views(predictions, tier_column=tier_column)
    tier_outputs = materialize_tier_prediction_views(tier_views, predictions_root)
    tier_records = build_paired_tier_records(tier_views, base_path=predictions_root)

    _io_path(models_root).mkdir(parents=True, exist_ok=True)
    _io_path(tier_b_feature_order_path_run).write_text("\n".join(tier_b_feature_order) + "\n", encoding="utf-8")
    joblib.dump(tier_a_model, _io_path(tier_a_model_path))
    joblib.dump(tier_b_model, _io_path(tier_b_model_path))
    tier_a_onnx_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model, tier_a_onnx_path, feature_count=len(tier_a_feature_order)
    )
    tier_b_onnx_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model, tier_b_onnx_path, feature_count=len(tier_b_feature_order)
    )
    tier_a_parity_values = values_a[: max(1, min(parity_rows, len(values_a)))]
    tier_b_parity_values = values_b[: max(1, min(parity_rows, len(values_b)))]
    tier_a_onnx_parity = check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx_path, tier_a_parity_values)
    tier_b_onnx_parity = check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx_path, tier_b_parity_values)
    onnx_parity = {
        "passed": bool(tier_a_onnx_parity["passed"] and tier_b_onnx_parity["passed"]),
        "tier_a": tier_a_onnx_parity,
        "tier_b": tier_b_onnx_parity,
    }

    split_specs = {
        "validation_is": ("validation", "2025.01.01", "2025.10.01"),
        "oos": ("oos", "2025.10.01", "2026.04.14"),
    }
    mt5_attempts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    _io_path(mt5_root).mkdir(parents=True, exist_ok=True)
    common_copies.append(copy_to_common_files(common_files_root, tier_a_onnx_path, common_ref("models", tier_a_onnx_path.name)))
    common_copies.append(copy_to_common_files(common_files_root, tier_b_onnx_path, common_ref("models", tier_b_onnx_path.name)))

    mt5_feature_matrices: dict[tuple[str, str], dict[str, Any]] = {}
    for split_label, (source_split, from_date, to_date) in split_specs.items():
        tier_a_split = tier_a_frame.loc[tier_a_frame["split"].astype(str).eq(source_split)].copy()
        tier_b_split = tier_b_frame.loc[tier_b_frame["split"].astype(str).eq(source_split)].copy()
        tier_a_feature_matrix_path = mt5_root / f"tier_a_{split_label}_feature_matrix.csv"
        tier_b_feature_matrix_path = mt5_root / f"tier_b_{split_label}_feature_matrix.csv"
        tier_a_matrix_payload = export_mt5_feature_matrix_csv(
            tier_a_split,
            tier_a_feature_order,
            tier_a_feature_matrix_path,
            metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
        )
        tier_b_matrix_payload = export_mt5_feature_matrix_csv(
            tier_b_split,
            tier_b_feature_order,
            tier_b_feature_matrix_path,
            metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
        )
        common_copies.append(
            copy_to_common_files(common_files_root, tier_a_feature_matrix_path, common_ref("features", tier_a_feature_matrix_path.name))
        )
        common_copies.append(
            copy_to_common_files(common_files_root, tier_b_feature_matrix_path, common_ref("features", tier_b_feature_matrix_path.name))
        )
        mt5_feature_matrices[(TIER_A, split_label)] = tier_a_matrix_payload
        mt5_feature_matrices[(TIER_B, split_label)] = tier_b_matrix_payload
        attempt = materialize_mt5_routed_attempt_files(
            run_output_root=run_output_root,
            split_name=split_label,
            primary_onnx_path=tier_a_onnx_path,
            primary_feature_matrix_path=tier_a_feature_matrix_path,
            primary_feature_count=len(tier_a_feature_order),
            primary_feature_order_hash=tier_a_feature_hash,
            fallback_onnx_path=tier_b_onnx_path,
            fallback_feature_matrix_path=tier_b_feature_matrix_path,
            fallback_feature_count=len(tier_b_feature_order),
            fallback_feature_order_hash=tier_b_feature_hash,
            rule=rule,
            from_date=from_date,
            to_date=to_date,
        )
        attempt["primary_feature_matrix"] = tier_a_matrix_payload
        attempt["fallback_feature_matrix"] = tier_b_matrix_payload
        mt5_attempts.append(attempt)

    compile_payload = None
    mt5_execution_results: list[dict[str, Any]] = []
    if attempt_mt5:
        for attempt in mt5_attempts:
            for common_output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[common_output_key]))
                if _path_exists(output_path):
                    _io_path(output_path).unlink()
            remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = compile_mql5_ea(metaeditor_path, EA_SOURCE_PATH, run_output_root / "mt5" / "metaeditor_alphascout_compile.log")
        if compile_payload["status"] == "completed":
            for attempt in mt5_attempts:
                result = run_mt5_tester(
                    terminal_path,
                    Path(attempt["ini"]["path"]),
                    set_path=Path(attempt["set"]["path"]),
                    tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                    tester_profile_ini_path=tester_profile_root / mt5_short_profile_ini_name(attempt["tier"], attempt["split"]),
                )
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                if "routing_mode" in attempt:
                    result["routing_mode"] = attempt["routing_mode"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = wait_for_mt5_runtime_outputs(common_files_root, attempt)
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                mt5_execution_results.append(result)

    mt5_report_records = collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=run_output_root,
        attempts=mt5_attempts,
    ) if attempt_mt5 else []
    attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    mt5_module_hashes = mt5_runtime_module_hashes()

    artifacts = [
        {"role": "tier_a_sklearn_model", "path": tier_a_model_path.as_posix(), "format": "joblib", "sha256": sha256_file(tier_a_model_path)},
        {"role": "tier_b_sklearn_model", "path": tier_b_model_path.as_posix(), "format": "joblib", "sha256": sha256_file(tier_b_model_path)},
        {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(tier_a_predictions_path)},
        {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(tier_b_predictions_path)},
        {"role": "no_tier_route_rows", "path": no_tier_route_path.as_posix(), "format": "parquet", "sha256": sha256_file(no_tier_route_path)},
        {"role": "route_coverage_summary", "path": route_coverage_path.as_posix(), "format": "json", "sha256": sha256_file(route_coverage_path)},
        {"role": "combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(combined_predictions_path)},
        {"role": "tier_b_core42_feature_order", "path": tier_b_feature_order_path_run.as_posix(), "format": "txt", "sha256": sha256_file(tier_b_feature_order_path_run)},
        {"role": "threshold_sweep", "path": threshold_sweep_path.as_posix(), "format": "csv", "sha256": sha256_file(threshold_sweep_path)},
        *[
            {
                "role": f"threshold_sweep_{view_name}",
                "path": path.as_posix(),
                "format": "csv",
                "sha256": sha256_file(path),
            }
            for view_name, path in threshold_sweep_paths.items()
        ],
        {"role": "tier_a_onnx_model", **tier_a_onnx_export, "format": "onnx"},
        {"role": "tier_b_onnx_model", **tier_b_onnx_export, "format": "onnx"},
        {"role": "mt5_attempts", "attempts": mt5_attempts},
        {"role": "mt5_common_file_copies", "copies": common_copies},
        {"role": "mt5_runtime_module_hashes", "modules": mt5_module_hashes},
        {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
        {"role": "tier_prediction_views", "views": tier_outputs},
    ]
    input_refs = {
        "tier_a": {
            "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
            "feature_set_id": FEATURE_SET_ID,
            "model_input_path": model_input_path.as_posix(),
            "model_input_sha256": sha256_file(model_input_path),
            "feature_order_path": feature_order_path.as_posix(),
            "feature_order_sha256": sha256_file(feature_order_path),
            "feature_count": len(tier_a_feature_order),
            "feature_order_hash": tier_a_feature_hash,
            "source_model_path": stage07_model_path.as_posix(),
            "source_model_sha256": sha256_file(stage07_model_path),
        },
        "tier_b": {
            "model_input_dataset_id": TIER_B_PARTIAL_CONTEXT_DATASET_ID,
            "feature_set_id": TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
            "model_input_path": "materialized_in_run_from_raw_feature_frame_and_label_contract",
            "model_input_sha256": None,
            "feature_order_path": tier_b_feature_order_path_run.as_posix(),
            "feature_order_sha256": sha256_file(tier_b_feature_order_path_run),
            "feature_count": len(tier_b_feature_order),
            "feature_order_hash": tier_b_feature_hash,
            "policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID,
            "boundary": "partial-context fallback surface; Stage04 56-feature quarantine artifact is a reference only",
            "route_coverage": route_coverage,
            "stage04_quarantine_reference": {
                "model_input_dataset_id": TIER_B_MODEL_INPUT_DATASET_ID,
                "feature_set_id": TIER_B_FEATURE_SET_ID,
                "model_input_path": tier_b_model_input_path.as_posix(),
                "model_input_sha256": sha256_file(tier_b_model_input_path),
                "feature_order_path": tier_b_feature_order_path.as_posix(),
                "feature_order_sha256": sha256_file(tier_b_feature_order_path),
            },
        },
    }
    mt5_runtime_completed = bool(mt5_execution_results) and all(item["status"] == "completed" for item in mt5_execution_results)
    mt5_reports_completed = len(mt5_kpi_records) >= 6 and all(
        item.get("status") == "completed" for item in mt5_kpi_records
    )
    external_status = "completed" if mt5_runtime_completed and mt5_reports_completed else (
        "blocked" if attempt_mt5 else "out_of_scope_by_claim"
    )
    ledger_rows = build_alpha_ledger_rows(
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        selected_threshold_id=rule.threshold_id,
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    ledger_payload = materialize_alpha_ledgers(ledger_rows)
    run_registry_payload = materialize_run_registry_row(
        route_coverage=route_coverage,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    artifacts.extend(
        [
            {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
            {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
            {"role": "project_run_registry", **run_registry_payload},
        ]
    )
    manifest = build_run_manifest_payload(
        run_id=RUN_ID,
        run_number=RUN_NUMBER,
        stage_id=STAGE_ID,
        exploration_label=EXPLORATION_LABEL,
        input_refs=input_refs,
        artifacts=artifacts,
        threshold_selection=selected,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
        external_verification_status=external_status,
    )
    manifest["routing_design"] = {
        "routing_mode": "tier_a_primary_tier_b_partial_context_fallback",
        "primary_tier": TIER_A,
        "fallback_tier": TIER_B,
        "fallback_policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID,
        "route_coverage": route_coverage,
    }
    manifest["mt5"] = {
        "attempted": bool(attempt_mt5),
        "compile": compile_payload,
        "execution_results": mt5_execution_results,
        "strategy_tester_reports": mt5_report_records,
        "kpi_records": mt5_kpi_records,
        "module_hashes": mt5_module_hashes,
        "tester_defaults": {
            "symbol": "US100",
            "period": "M5",
            "model": 4,
            "deposit": 500,
            "leverage": "1:100",
            "fixed_lot": 0.1,
            "max_hold_bars": 12,
            "max_concurrent_positions": 1,
        },
    }
    kpi = build_kpi_record_payload(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        threshold_sweep=threshold_sweep,
        threshold_sweeps=threshold_sweeps,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
        mt5_kpi_records=mt5_kpi_records,
    )
    kpi["routing"]["routing_mode"] = "tier_a_primary_tier_b_partial_context_fallback"
    kpi["routing"]["route_coverage_design"] = route_coverage
    kpi["mt5"] = {
        "scoreboard_lane": "runtime_probe",
        "external_verification_status": external_status,
        "compile": compile_payload,
        "execution_results": mt5_execution_results,
        "strategy_tester_reports": mt5_report_records,
        "kpi_records": mt5_kpi_records,
        "attempt_count": len(mt5_attempts),
    }
    payload_paths = materialize_manifest_and_kpi(run_output_root, manifest_payload=manifest, kpi_payload=kpi)
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "completed_payload" if onnx_parity["passed"] else "invalid_payload",
        "judgment": "inconclusive_single_split_scout_payload" if external_status != "completed" else "inconclusive_single_split_scout_mt5_routed_completed",
        "selected_threshold": selected,
        "tier_records": tier_records,
        "onnx_parity": onnx_parity,
        "external_verification_status": external_status,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "ledger_rows": ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
        "boundary": "single_split_scout only; not alpha quality, live readiness, runtime authority expansion, or operating promotion",
    }
    write_json(summary_path, summary)
    _io_path(result_summary_path.parent).mkdir(parents=True, exist_ok=True)
    mt5_records_by_view = {str(record.get("record_view")): record for record in mt5_kpi_records}

    def result_metric(record_view: str, metric_name: str) -> Any:
        record = mt5_records_by_view.get(record_view, {})
        return record.get("metrics", {}).get(metric_name)

    _io_path(result_summary_path).write_text(
        "\n".join(
            [
                "# Stage 10 run01A LogReg Threshold MT5 Scout(로지스틱 회귀 임계값 MT5 탐색)",
                "",
                f"- run_id(실행 ID): `{RUN_ID}`",
                f"- selected threshold(선택 임계값): `{rule.threshold_id}`",
                f"- external verification status(외부 검증 상태): `{external_status}`",
                f"- Tier A rows(Tier A 행 수): `{len(tier_a_predictions)}`",
                f"- Tier B fallback rows(Tier B 대체 행 수): `{len(tier_b_predictions)}`",
                f"- no_tier labelable rows(티어 없음 라벨 가능 행 수): `{len(no_tier_frame)}`",
                f"- MT5 KPI records(MT5 KPI 기록): `{len(mt5_kpi_records)}`",
                "- routing mode(라우팅 방식): `tier_a_primary_tier_b_partial_context_fallback`",
                f"- Tier B fallback subtype counts(Tier B 대체 하위유형 수): `{route_coverage.get('tier_b_fallback_by_subtype', {})}`",
                f"- validation Tier A used(검증 Tier A 사용): `{result_metric('mt5_routed_total_validation_is', 'tier_a_used_count')}`",
                f"- validation Tier B fallback used(검증 Tier B 대체 사용): `{result_metric('mt5_routed_total_validation_is', 'tier_b_fallback_used_count')}`",
                f"- validation net profit(검증 순수익): `{result_metric('mt5_routed_total_validation_is', 'net_profit')}`",
                f"- validation profit factor(검증 수익 팩터): `{result_metric('mt5_routed_total_validation_is', 'profit_factor')}`",
                f"- OOS Tier A used(표본외 Tier A 사용): `{result_metric('mt5_routed_total_oos', 'tier_a_used_count')}`",
                f"- OOS Tier B fallback used(표본외 Tier B 대체 사용): `{result_metric('mt5_routed_total_oos', 'tier_b_fallback_used_count')}`",
                f"- OOS net profit(표본외 순수익): `{result_metric('mt5_routed_total_oos', 'net_profit')}`",
                f"- OOS profit factor(표본외 수익 팩터): `{result_metric('mt5_routed_total_oos', 'profit_factor')}`",
                "",
                "## Boundary(경계)",
                "",
                "`single_split_scout(단일 분할 탐색)`이며 alpha quality(알파 품질), live readiness(실거래 준비), "
                "runtime authority expansion(런타임 권위 확장), operating promotion(운영 승격)을 주장하지 않는다.",
                "",
            ]
        ),
        encoding="utf-8-sig",
    )

    return {
        "status": "ok" if onnx_parity["passed"] else "failed",
        "run_id": RUN_ID,
        "run_output_root": run_output_root.as_posix(),
        "threshold_id": rule.threshold_id,
        "onnx_parity": onnx_parity,
        "external_verification_status": external_status,
        "mt5_attempted": attempt_mt5,
        "payload_paths": payload_paths,
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
    }


def main() -> int:
    args = parse_args()
    payload = run_stage10_logreg_mt5_scout(
        model_input_path=Path(args.model_input_path),
        feature_order_path=Path(args.feature_order_path),
        tier_b_model_input_path=Path(args.tier_b_model_input_path),
        tier_b_feature_order_path=Path(args.tier_b_feature_order_path),
        raw_root=Path(args.raw_root),
        training_summary_path=Path(args.training_summary_path),
        stage07_model_path=Path(args.stage07_model_path),
        run_output_root=Path(args.run_output_root),
        common_files_root=Path(args.common_files_root),
        terminal_data_root=Path(args.terminal_data_root),
        tester_profile_root=Path(args.tester_profile_root),
        tier_column=args.tier_column,
        random_seed=args.random_seed,
        max_iter=args.max_iter,
        parity_rows=args.parity_rows,
        attempt_mt5=args.attempt_mt5,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
    )
    print(json.dumps(_json_ready(payload), indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
