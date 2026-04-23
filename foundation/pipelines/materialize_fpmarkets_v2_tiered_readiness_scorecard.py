from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

try:
    from foundation.pipelines.materialize_fpmarkets_v2_dataset import (
        DATASET_ID,
        EXPECTED_FEATURE_ORDER_HASH,
        PARSER_VERSION,
        PRACTICAL_MODELING_START_UTC,
        WINDOW_END_UTC,
        WINDOW_START_UTC,
        build_feature_frame,
    )
except ModuleNotFoundError:
    dataset_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_dataset.py")
    spec = importlib.util.spec_from_file_location("materialize_fpmarkets_v2_dataset", dataset_module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load dataset materializer from {dataset_module_path}")
    dataset_module = importlib.util.module_from_spec(spec)
    sys.modules["materialize_fpmarkets_v2_dataset"] = dataset_module
    spec.loader.exec_module(dataset_module)
    DATASET_ID = dataset_module.DATASET_ID
    EXPECTED_FEATURE_ORDER_HASH = dataset_module.EXPECTED_FEATURE_ORDER_HASH
    PARSER_VERSION = dataset_module.PARSER_VERSION
    PRACTICAL_MODELING_START_UTC = dataset_module.PRACTICAL_MODELING_START_UTC
    WINDOW_END_UTC = dataset_module.WINDOW_END_UTC
    WINDOW_START_UTC = dataset_module.WINDOW_START_UTC
    build_feature_frame = dataset_module.build_feature_frame


STAGE_NAME = "06_tiered_readiness_exploration"
SCORECARD_ID = "scorecard_fpmarkets_v2_tiered_readiness_0001"
REPORT_ID = "report_fpmarkets_v2_tiered_readiness_0001"
ROW_LABELS_FILENAME = "readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet"
SUMMARY_FILENAME = "readiness_scorecard_fpmarkets_v2_tiered_readiness_0001.json"
DEFAULT_OUTPUT_ROOT = Path("stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001")
DEFAULT_REPORT_PATH = Path(
    "stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md"
)
READINESS_POLICY_REF = "docs/policies/tiered_readiness_exploration.md@2026-04-20"
READINESS_DECISION_REF = "docs/decisions/2026-04-20_stage06_first_readiness_boundary.md@2026-04-20"

GROUP_TOKEN_ORDER = [
    "g1_contract_base",
    "g2_session_semantics",
    "g3_macro_proxy",
    "g4_leader_equity",
    "g5_breadth_extension",
]
SYMBOL_TOKEN_ORDER = [
    "VIX",
    "US10YR",
    "USDX",
    "NVDA.xnas",
    "AAPL.xnas",
    "MSFT.xnas",
    "AMZN.xnas",
    "AMD.xnas",
    "GOOGL.xnas",
    "META.xnas",
    "TSLA.xnas",
]
TIER_ORDER = ["tier_a", "tier_b", "tier_c"]
LANE_ORDER = ["strict_tier_a", "tier_b_exploration", "null"]
ROW_LABEL_COLUMNS = [
    "timestamp",
    "symbol",
    "within_practical_window",
    "valid_row",
    "invalid__warmup_incomplete",
    "invalid__main_symbol_missing",
    "invalid__external_alignment_missing",
    "invalid__session_semantics_missing",
    "invalid__numeric_invalid",
    "invalid__weights_unavailable",
    "invalid__contract_version_mismatch",
    "g1_contract_base_complete",
    "g2_session_semantics_complete",
    "g3_macro_proxy_complete",
    "g4_leader_equity_complete",
    "g5_breadth_extension_complete",
    "external_complete_group_count",
    "readiness_tier",
    "reporting_lane",
    "missing_groups",
    "missing_symbols",
]
SESSION_COLUMNS = [
    "overnight_return",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
]
G3_SYMBOL_COLUMNS = {
    "VIX": ["vix_change_1", "vix_zscore_20"],
    "US10YR": ["us10yr_change_1", "us10yr_zscore_20"],
    "USDX": ["usdx_change_1", "usdx_zscore_20"],
}
G4_SYMBOL_COLUMNS = {
    "NVDA.xnas": ["nvda_xnas_log_return_1"],
    "AAPL.xnas": ["aapl_xnas_log_return_1"],
    "MSFT.xnas": ["msft_xnas_log_return_1"],
    "AMZN.xnas": ["amzn_xnas_log_return_1"],
}
G5_SYMBOL_COLUMNS = {
    "AMD.xnas": ["amd_simple_return_1", "amd_simple_return_5"],
    "GOOGL.xnas": ["googl_xnas_simple_return_1", "googl_xnas_simple_return_5"],
    "META.xnas": ["meta_simple_return_1", "meta_simple_return_5"],
    "TSLA.xnas": ["tsla_simple_return_1", "tsla_simple_return_5"],
}
G5_ALL_COLUMNS = [
    "amd_simple_return_1",
    "amd_simple_return_5",
    "googl_xnas_simple_return_1",
    "googl_xnas_simple_return_5",
    "meta_simple_return_1",
    "meta_simple_return_5",
    "tsla_simple_return_1",
    "tsla_simple_return_5",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize the first Stage 06 tiered-readiness scorecard for FPMarkets v2."
    )
    parser.add_argument(
        "--raw-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative root containing raw M5 MT5 bar exports.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Repo-relative output root for the scorecard parquet and JSON artifacts.",
    )
    parser.add_argument(
        "--report-path",
        default=str(DEFAULT_REPORT_PATH),
        help="Repo-relative output path for the rendered Stage 06 review report.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=pd.Timestamp.now(tz="Asia/Seoul").date().isoformat(),
        help="Review date to stamp into the rendered report.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(_fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fs_path(path: Path) -> str | Path:
    resolved = path.resolve()
    path_text = str(resolved)
    if sys.platform != "win32":
        return resolved
    if path_text.startswith("\\\\?\\"):
        return path_text
    if path_text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path_text.lstrip("\\")
    return "\\\\?\\" + path_text


def _write_text(path: Path, text: str) -> None:
    with open(_fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def classify_tier_flags(
    *,
    g1_contract_base_complete: bool,
    g2_session_semantics_complete: bool,
    g3_macro_proxy_complete: bool,
    g4_leader_equity_complete: bool,
    g5_breadth_extension_complete: bool,
) -> str:
    if not g1_contract_base_complete or not g2_session_semantics_complete:
        return "tier_c"
    external_complete_group_count = (
        int(g3_macro_proxy_complete) + int(g4_leader_equity_complete) + int(g5_breadth_extension_complete)
    )
    if g3_macro_proxy_complete and g4_leader_equity_complete and g5_breadth_extension_complete:
        return "tier_a"
    if external_complete_group_count in (1, 2):
        return "tier_b"
    return "tier_c"


def reporting_lane_for_tier(readiness_tier: str) -> str | None:
    if readiness_tier == "tier_a":
        return "strict_tier_a"
    if readiness_tier == "tier_b":
        return "tier_b_exploration"
    return None


def serialize_pipe_tokens(tokens: Iterable[str], order: Sequence[str]) -> str:
    seen = set()
    unique_tokens = []
    for token in tokens:
        if token and token not in seen:
            seen.add(token)
            unique_tokens.append(token)
    order_index = {token: index for index, token in enumerate(order)}
    unique_tokens.sort(key=lambda token: (order_index.get(token, len(order)), token))
    return "|".join(unique_tokens)


def _all_columns_present(frame: pd.DataFrame, columns: Sequence[str]) -> pd.Series:
    return frame[list(columns)].notna().all(axis=1)


def compute_group_states(frame: pd.DataFrame) -> tuple[dict[str, pd.Series], dict[str, dict[str, pd.Series]]]:
    g1_complete = _all_columns_present(frame, ["open", "high", "low", "close"])
    g1_complete &= ~frame["invalid__main_symbol_missing"]
    g1_complete &= ~frame["invalid__numeric_invalid"]
    g1_complete &= ~frame["invalid__contract_version_mismatch"]

    g2_complete = _all_columns_present(frame, SESSION_COLUMNS)

    g3_symbol_complete = {
        symbol: _all_columns_present(frame, columns) for symbol, columns in G3_SYMBOL_COLUMNS.items()
    }
    g4_symbol_complete = {
        symbol: _all_columns_present(frame, columns) for symbol, columns in G4_SYMBOL_COLUMNS.items()
    }
    g5_symbol_complete = {
        symbol: _all_columns_present(frame, columns) for symbol, columns in G5_SYMBOL_COLUMNS.items()
    }

    g3_complete = pd.Series(True, index=frame.index)
    for symbol_complete in g3_symbol_complete.values():
        g3_complete &= symbol_complete

    g4_complete = pd.Series(True, index=frame.index)
    for symbol_complete in g4_symbol_complete.values():
        g4_complete &= symbol_complete

    g5_complete = _all_columns_present(frame, G5_ALL_COLUMNS)

    group_complete = {
        "g1_contract_base": g1_complete,
        "g2_session_semantics": g2_complete,
        "g3_macro_proxy": g3_complete,
        "g4_leader_equity": g4_complete,
        "g5_breadth_extension": g5_complete,
    }
    symbol_complete = {
        "g3_macro_proxy": g3_symbol_complete,
        "g4_leader_equity": g4_symbol_complete,
        "g5_breadth_extension": g5_symbol_complete,
    }
    return group_complete, symbol_complete


def build_scorecard_frame(frame: pd.DataFrame) -> pd.DataFrame:
    group_complete, symbol_complete = compute_group_states(frame)

    g1_arr = group_complete["g1_contract_base"].to_numpy(dtype=bool, copy=False)
    g2_arr = group_complete["g2_session_semantics"].to_numpy(dtype=bool, copy=False)
    g3_arr = group_complete["g3_macro_proxy"].to_numpy(dtype=bool, copy=False)
    g4_arr = group_complete["g4_leader_equity"].to_numpy(dtype=bool, copy=False)
    g5_arr = group_complete["g5_breadth_extension"].to_numpy(dtype=bool, copy=False)

    external_complete_group_count = (
        group_complete["g3_macro_proxy"].astype(int)
        + group_complete["g4_leader_equity"].astype(int)
        + group_complete["g5_breadth_extension"].astype(int)
    )

    readiness_tier = [
        classify_tier_flags(
            g1_contract_base_complete=g1_complete,
            g2_session_semantics_complete=g2_complete,
            g3_macro_proxy_complete=g3_complete,
            g4_leader_equity_complete=g4_complete,
            g5_breadth_extension_complete=g5_complete,
        )
        for g1_complete, g2_complete, g3_complete, g4_complete, g5_complete in zip(
            g1_arr,
            g2_arr,
            g3_arr,
            g4_arr,
            g5_arr,
            strict=True,
        )
    ]
    reporting_lane = [reporting_lane_for_tier(tier) for tier in readiness_tier]

    g3_symbol_arrays = {
        symbol: series.to_numpy(dtype=bool, copy=False)
        for symbol, series in symbol_complete["g3_macro_proxy"].items()
    }
    g4_symbol_arrays = {
        symbol: series.to_numpy(dtype=bool, copy=False)
        for symbol, series in symbol_complete["g4_leader_equity"].items()
    }
    g5_symbol_arrays = {
        symbol: series.to_numpy(dtype=bool, copy=False)
        for symbol, series in symbol_complete["g5_breadth_extension"].items()
    }

    missing_groups: list[str] = []
    missing_symbols: list[str] = []
    for row_index in range(len(frame)):
        row_missing_groups = []
        row_missing_symbols = []

        if not g1_arr[row_index]:
            row_missing_groups.append("g1_contract_base")
        if not g2_arr[row_index]:
            row_missing_groups.append("g2_session_semantics")
        if not g3_arr[row_index]:
            row_missing_groups.append("g3_macro_proxy")
            row_missing_symbols.extend(
                symbol for symbol, values in g3_symbol_arrays.items() if not values[row_index]
            )
        if not g4_arr[row_index]:
            row_missing_groups.append("g4_leader_equity")
            row_missing_symbols.extend(
                symbol for symbol, values in g4_symbol_arrays.items() if not values[row_index]
            )
        if not g5_arr[row_index]:
            row_missing_groups.append("g5_breadth_extension")
            row_missing_symbols.extend(
                symbol for symbol, values in g5_symbol_arrays.items() if not values[row_index]
            )

        missing_groups.append(serialize_pipe_tokens(row_missing_groups, GROUP_TOKEN_ORDER))
        missing_symbols.append(serialize_pipe_tokens(row_missing_symbols, SYMBOL_TOKEN_ORDER))

    scorecard = pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "symbol": "US100",
            "within_practical_window": frame["timestamp"] >= PRACTICAL_MODELING_START_UTC,
            "valid_row": frame["valid_row"].astype(bool),
            "invalid__warmup_incomplete": frame["invalid__warmup_incomplete"].astype(bool),
            "invalid__main_symbol_missing": frame["invalid__main_symbol_missing"].astype(bool),
            "invalid__external_alignment_missing": frame["invalid__external_alignment_missing"].astype(bool),
            "invalid__session_semantics_missing": frame["invalid__session_semantics_missing"].astype(bool),
            "invalid__numeric_invalid": frame["invalid__numeric_invalid"].astype(bool),
            "invalid__weights_unavailable": frame["invalid__weights_unavailable"].astype(bool),
            "invalid__contract_version_mismatch": frame["invalid__contract_version_mismatch"].astype(bool),
            "g1_contract_base_complete": group_complete["g1_contract_base"].astype(bool),
            "g2_session_semantics_complete": group_complete["g2_session_semantics"].astype(bool),
            "g3_macro_proxy_complete": group_complete["g3_macro_proxy"].astype(bool),
            "g4_leader_equity_complete": group_complete["g4_leader_equity"].astype(bool),
            "g5_breadth_extension_complete": group_complete["g5_breadth_extension"].astype(bool),
            "external_complete_group_count": external_complete_group_count.astype("int64"),
            "readiness_tier": readiness_tier,
            "reporting_lane": reporting_lane,
            "missing_groups": missing_groups,
            "missing_symbols": missing_symbols,
        }
    )
    return scorecard[ROW_LABEL_COLUMNS]


def _count_pipe_tokens(series: pd.Series, order: Sequence[str]) -> dict[str, int]:
    counts = Counter()
    for value in series.fillna(""):
        if not value:
            continue
        for token in value.split("|"):
            if token:
                counts[token] += 1
    return {token: int(counts[token]) for token in order if counts[token] > 0}


def summarize_window(frame: pd.DataFrame, *, start: str) -> dict[str, object]:
    end_inclusive = WINDOW_END_UTC.date().isoformat()
    readiness_counts = frame["readiness_tier"].value_counts()
    lane_counts = frame["reporting_lane"].fillna("null").value_counts()
    return {
        "start": start,
        "end_inclusive": end_inclusive,
        "row_count": int(len(frame)),
        "tier_counts": {tier: int(readiness_counts.get(tier, 0)) for tier in TIER_ORDER},
        "lane_counts": {lane: int(lane_counts.get(lane, 0)) for lane in LANE_ORDER},
        "missing_group_counts": _count_pipe_tokens(frame["missing_groups"], GROUP_TOKEN_ORDER),
        "missing_symbol_counts": _count_pipe_tokens(frame["missing_symbols"], SYMBOL_TOKEN_ORDER),
    }


def build_summary_payload(row_labels: pd.DataFrame, *, row_labels_path: str) -> dict[str, object]:
    practical = row_labels.loc[row_labels["within_practical_window"]].copy()
    return {
        "dataset_id": DATASET_ID,
        "scorecard_id": SCORECARD_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "readiness_policy_ref": READINESS_POLICY_REF,
        "readiness_decision_ref": READINESS_DECISION_REF,
        "row_labels_path": row_labels_path,
        "shared_window": summarize_window(row_labels, start=WINDOW_START_UTC.date().isoformat()),
        "practical_window": summarize_window(practical, start=PRACTICAL_MODELING_START_UTC.date().isoformat()),
    }


def _format_counts(counts: dict[str, int], *, top_n: int | None = None) -> str:
    items = list(counts.items())
    if top_n is not None:
        items = sorted(items, key=lambda item: (-item[1], item[0]))[:top_n]
    return "|".join(f"{key}={value}" for key, value in items) if items else "none"


def render_report(summary_payload: dict[str, object], *, reviewed_on: str) -> str:
    shared = summary_payload["shared_window"]
    practical = summary_payload["practical_window"]
    lines = [
        "# Stage 06 First Scorecard Review (첫 점수표 리뷰)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- stage: `{STAGE_NAME}`",
        f"- dataset_id: `{summary_payload['dataset_id']}`",
        f"- scorecard_id: `{summary_payload['scorecard_id']}`",
        f"- report_id: `{REPORT_ID}`",
        f"- readiness_policy_ref: `{summary_payload['readiness_policy_ref']}`",
        f"- readiness_decision_ref: `{summary_payload['readiness_decision_ref']}`",
        "",
        "## Boundary Read (경계 판독)",
        "- strict `Tier A` (엄격 `Tier A`) remains the only current runtime rule (실행 규칙) and is unchanged by this scorecard (점수표)",
        "- `Tier B` (부분 준비도 `Tier B`) is exploration-only (탐색 전용) and stays on the separate `tier_b_exploration` reporting lane (보고 레인)",
        "- `Tier C` (스킵 준비도 `Tier C`) remains a skip classification (스킵 분류) rather than a reporting lane (보고 레인)",
        "- no operating promotion (운영 승격) is claimed by this materialized scorecard (물질화 점수표)",
        "- additional helper-lane or broader-lane evidence remains an open question (열린 질문)",
        "",
        "## Shared Window (공유 구간)",
        f"- start: `{shared['start']}`",
        f"- end_inclusive: `{shared['end_inclusive']}`",
        f"- row_count: `{shared['row_count']}`",
        f"- tier_counts: `{_format_counts(shared['tier_counts'])}`",
        f"- lane_counts: `{_format_counts(shared['lane_counts'])}`",
        f"- top_missing_groups: `{_format_counts(shared['missing_group_counts'], top_n=5)}`",
        f"- top_missing_symbols: `{_format_counts(shared['missing_symbol_counts'], top_n=8)}`",
        "",
        "## Practical Window (실전 구간)",
        f"- start: `{practical['start']}`",
        f"- end_inclusive: `{practical['end_inclusive']}`",
        f"- row_count: `{practical['row_count']}`",
        f"- tier_counts: `{_format_counts(practical['tier_counts'])}`",
        f"- lane_counts: `{_format_counts(practical['lane_counts'])}`",
        f"- top_missing_groups: `{_format_counts(practical['missing_group_counts'], top_n=5)}`",
        f"- top_missing_symbols: `{_format_counts(practical['missing_symbol_counts'], top_n=8)}`",
        "",
        "## Notes (메모)",
        "- this pass materializes row-level labels (행 단위 라벨), a machine-readable summary (기계가독 요약), and a review report (리뷰 보고서) only",
        "- no reduced-risk runtime family (축소위험 런타임 계열) is materialized in this pass",
        "- the placeholder weights table (임시 가중치 테이블) remains in force, so future counts may change if a real monthly-weight source replaces it",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(
    *,
    output_root: Path,
    report_path: Path,
    row_labels: pd.DataFrame,
    reviewed_on: str,
) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    row_labels_path = output_root / ROW_LABELS_FILENAME
    summary_path = output_root / SUMMARY_FILENAME

    row_labels.to_parquet(_fs_path(row_labels_path), index=False)
    summary_payload = build_summary_payload(row_labels, row_labels_path=row_labels_path.as_posix())
    _write_text(summary_path, json.dumps(summary_payload, indent=2))
    _write_text(report_path, render_report(summary_payload, reviewed_on=reviewed_on))

    return {
        "row_labels_path": row_labels_path.as_posix(),
        "summary_path": summary_path.as_posix(),
        "report_path": report_path.as_posix(),
        "row_labels_sha256": sha256_file(row_labels_path),
        "summary_sha256": sha256_file(summary_path),
        "report_sha256": sha256_file(report_path),
        "summary": summary_payload,
    }


def main() -> int:
    args = parse_args()
    raw_root = Path(args.raw_root)
    output_root = Path(args.output_root)
    report_path = Path(args.report_path)

    frame, _ = build_feature_frame(raw_root)
    row_labels = build_scorecard_frame(frame)
    outputs = write_outputs(
        output_root=output_root,
        report_path=report_path,
        row_labels=row_labels,
        reviewed_on=args.reviewed_on,
    )

    payload = {
        "status": "ok",
        "dataset_id": DATASET_ID,
        "scorecard_id": SCORECARD_ID,
        "report_id": REPORT_ID,
        "output_root": str(output_root.resolve()),
        "report_path": str(report_path.resolve()),
        "shared_window_tier_counts": outputs["summary"]["shared_window"]["tier_counts"],
        "practical_window_tier_counts": outputs["summary"]["practical_window"]["tier_counts"],
        "hashes": {
            "row_labels_sha256": outputs["row_labels_sha256"],
            "summary_sha256": outputs["summary_sha256"],
            "report_sha256": outputs["report_sha256"],
        },
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
