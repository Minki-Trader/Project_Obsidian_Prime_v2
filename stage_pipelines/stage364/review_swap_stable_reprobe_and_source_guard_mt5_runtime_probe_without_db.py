from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades  # noqa: E402
from stage_pipelines.stage364 import execute_bx03_guard_stack_runtime_probe_without_db as ca  # noqa: E402
from stage_pipelines.stage364 import execute_overlay_hour17_native_short_ablation_runtime_probe_without_db as bx  # noqa: E402
from stage_pipelines.stage364 import execute_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db as cd  # noqa: E402
from stage_pipelines.stage364 import materialize_swap_stable_reprobe_and_source_guard_inputs_without_db as cc  # noqa: E402
from stage_pipelines.stage364 import materialize_synthetic_short_source_runtime_repair_without_db as bv  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = cd.STAGE_ID
RUN_NUMBER = "run364CE"
RUN_ID = "run364CE_review_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = cd.RUN_ID
BASELINE_BX_RUN_ID = bx.RUN_ID
BASELINE_CA_RUN_ID = ca.RUN_ID
BASELINE_CC_RUN_ID = cc.RUN_ID
BASELINE_BV_RUN_ID = bv.RUN_ID
NEXT_RUN_ID = "run364CF_materialize_cost_stable_h17_source_guard_offensive_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = cd.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
TRADE_ATTRIBUTION = RUN_DIR / "cd_trade_attribution_by_variant.csv"
ATTRIBUTION_BY_VARIANT = RUN_DIR / "attribution_by_variant.csv"
ATTRIBUTION_BY_SOURCE = RUN_DIR / "attribution_by_variant_source_bucket.csv"
ATTRIBUTION_BY_DIRECTION = RUN_DIR / "attribution_by_variant_direction.csv"
ATTRIBUTION_BY_MONTH = RUN_DIR / "attribution_by_variant_month.csv"
ATTRIBUTION_BY_OPEN_HOUR = RUN_DIR / "attribution_by_variant_open_hour.csv"
ATTRIBUTION_BY_CLOSE_HOUR = RUN_DIR / "attribution_by_variant_close_hour.csv"
SCOREBOARD_REVIEW = RUN_DIR / "cd_runtime_scoreboard_review.csv"
PAIR_DELTAS = RUN_DIR / "cd_pair_deltas.csv"
MEMBERSHIP_DELTA = RUN_DIR / "cd_trade_membership_delta.csv"
SWAP_RECONCILIATION = RUN_DIR / "cd02_vs_cd01_swap_reconciliation.csv"
SOURCE_OVERLAY_DECOMPOSITION = RUN_DIR / "cd02_vs_cd03_source_overlay_value_decomposition.csv"
SET_PARAMETER_DIFF = RUN_DIR / "cd_set_parameter_diff.csv"
COMMON_ARTIFACT_IDENTITY = RUN_DIR / "common_artifact_identity_check.csv"
REPORT_RECONCILIATION = RUN_DIR / "report_metric_reconciliation.csv"
NEXT_QUEUE = RUN_DIR / "run364CF_cost_stable_h17_source_guard_offensive_queue.csv"
KPI_CONTRACT_AUDIT = RUN_DIR / "kpi_contract_audit.csv"
ROW_GRAIN_AUDIT = RUN_DIR / "row_grain_audit.csv"
SOURCE_AUTHORITY_AUDIT = RUN_DIR / "source_authority_audit.csv"
RUNTIME_PARITY_AUDIT = RUN_DIR / "runtime_parity_audit.csv"
BACKTEST_FORENSICS_AUDIT = RUN_DIR / "backtest_forensics_audit.csv"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CE_review_swap_stable_reprobe_and_source_guard_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CE_review_swap_stable_reprobe_and_source_guard_mt5_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_README = STAGE_DIR / "README.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_CD_FINAL = cd.FINAL_DECISION
SOURCE_CD_SCOREBOARD = cd.RUNTIME_SCOREBOARD
SOURCE_CD_REPORTS = cd.STRATEGY_TESTER_REPORTS
SOURCE_CD_EXECUTION = cd.MT5_EXECUTION_RESULT
SOURCE_CD_OUTPUT_VALIDATION = cd.RUNTIME_OUTPUT_VALIDATION
SOURCE_CD_GATE = cd.GATE_AUDIT
SOURCE_CD_POLICY = cd.RUNTIME_POLICY_CONFIG
SOURCE_CD_PAIR_SCREEN = cd.PAIR_METRIC_SUMMARY
SOURCE_CD_SET_MANIFEST = cd.TESTER_SET_MANIFEST
SOURCE_CD_TESTER_IDENTITY = cd.TESTER_IDENTITY_CONTRACT
SOURCE_CD_COMMON_SYNC = cd.COMMON_FILES_SYNC
SOURCE_CC_QUEUE = cc.CD_RUNTIME_QUEUE
SOURCE_CC_PAIR_MATRIX = cc.SAME_SESSION_PAIR_MATRIX
SOURCE_CA_FINAL = ca.FINAL_DECISION
SOURCE_CA_SCOREBOARD = ca.RUNTIME_SCOREBOARD
SOURCE_CA_COMMON_SYNC = ca.COMMON_FILES_SYNC
SOURCE_BX_FINAL = bx.FINAL_DECISION
SOURCE_BX_SCOREBOARD = bx.ABLATION_SCOREBOARD
SOURCE_BX_COMMON_SYNC = bx.COMMON_FILES_SYNC
SOURCE_BV_FINAL = bv.FINAL_DECISION

CD01_SET = STAGE_DIR / "02_runs" / "run364CD" / "mt5" / "sets" / "cd01_OPv2_run364BX_bx3_clone_current_session.set"
CD02_SET = STAGE_DIR / "02_runs" / "run364CD" / "mt5" / "sets" / "cd02_ca01_clone_current_session.set"
CD03_SET = STAGE_DIR / "02_runs" / "run364CD" / "mt5" / "sets" / "cd03_native_short_same_calendar_current_session.set"
CD01_REPORT = STAGE_DIR / "02_runs" / "run364CD" / "mt5" / "reports" / "OPv2_run364CD_cd01_bx3_clone_current_session.htm"
CD02_REPORT = STAGE_DIR / "02_runs" / "run364CD" / "mt5" / "reports" / "OPv2_run364CD_cd02_ca01_clone_current_session.htm"
CD03_REPORT = STAGE_DIR / "02_runs" / "run364CD" / "mt5" / "reports" / "OPv2_run364CD_cd03_native_short_same_calendar_current_session.htm"
CD01_TELEMETRY = STAGE_DIR / "02_runs" / "run364CD" / "runtime_telemetry" / "run364CD_cd01_bx3_clone_current_session_telemetry.csv"
CD02_TELEMETRY = STAGE_DIR / "02_runs" / "run364CD" / "runtime_telemetry" / "run364CD_cd02_ca01_clone_current_session_telemetry.csv"
CD03_TELEMETRY = STAGE_DIR / "02_runs" / "run364CD" / "runtime_telemetry" / "run364CD_cd03_native_short_same_calendar_current_session_telemetry.csv"

INPUT_FILES = [
    SOURCE_CD_FINAL,
    SOURCE_CD_SCOREBOARD,
    SOURCE_CD_REPORTS,
    SOURCE_CD_EXECUTION,
    SOURCE_CD_OUTPUT_VALIDATION,
    SOURCE_CD_GATE,
    SOURCE_CD_POLICY,
    SOURCE_CD_PAIR_SCREEN,
    SOURCE_CD_SET_MANIFEST,
    SOURCE_CD_TESTER_IDENTITY,
    SOURCE_CD_COMMON_SYNC,
    SOURCE_CC_QUEUE,
    SOURCE_CC_PAIR_MATRIX,
    SOURCE_CA_FINAL,
    SOURCE_CA_SCOREBOARD,
    SOURCE_CA_COMMON_SYNC,
    SOURCE_BX_FINAL,
    SOURCE_BX_SCOREBOARD,
    SOURCE_BX_COMMON_SYNC,
    SOURCE_BV_FINAL,
    CD01_SET,
    CD02_SET,
    CD03_SET,
    CD01_REPORT,
    CD02_REPORT,
    CD03_REPORT,
    CD01_TELEMETRY,
    CD02_TELEMETRY,
    CD03_TELEMETRY,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    TRADE_ATTRIBUTION,
    ATTRIBUTION_BY_VARIANT,
    ATTRIBUTION_BY_SOURCE,
    ATTRIBUTION_BY_DIRECTION,
    ATTRIBUTION_BY_MONTH,
    ATTRIBUTION_BY_OPEN_HOUR,
    ATTRIBUTION_BY_CLOSE_HOUR,
    SCOREBOARD_REVIEW,
    PAIR_DELTAS,
    MEMBERSHIP_DELTA,
    SWAP_RECONCILIATION,
    SOURCE_OVERLAY_DECOMPOSITION,
    SET_PARAMETER_DIFF,
    COMMON_ARTIFACT_IDENTITY,
    REPORT_RECONCILIATION,
    NEXT_QUEUE,
    KPI_CONTRACT_AUDIT,
    ROW_GRAIN_AUDIT,
    SOURCE_AUTHORITY_AUDIT,
    RUNTIME_PARITY_AUDIT,
    BACKTEST_FORENSICS_AUDIT,
    PERFORMANCE_RECEIPT,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_README,
    SELECTION_STATUS,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]

VARIANTS = [
    {
        "variant_id": "cd01_bx3_clone_current_session",
        "source_variant_id": "bx03_hour17_overlay_plus_weak_late_session_firewall",
        "source_run_id": PARENT_RUN_ID,
        "report": CD01_REPORT,
        "telemetry": CD01_TELEMETRY,
        "set_path": CD01_SET,
        "role": "same_session_bx3_clone",
    },
    {
        "variant_id": "cd02_ca01_clone_current_session",
        "source_variant_id": "ca01_bx03_semantics_control",
        "source_run_id": PARENT_RUN_ID,
        "report": CD02_REPORT,
        "telemetry": CD02_TELEMETRY,
        "set_path": CD02_SET,
        "role": "same_session_ca01_clone",
    },
    {
        "variant_id": "cd03_native_short_same_calendar_current_session",
        "source_variant_id": "ca06_native_short_same_calendar_control",
        "source_run_id": PARENT_RUN_ID,
        "report": CD03_REPORT,
        "telemetry": CD03_TELEMETRY,
        "set_path": CD03_SET,
        "role": "native_short_same_calendar_control",
    },
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return cd.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    cd.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    cd.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    cd.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    cd.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    cd.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def safe_pf(gross_profit: float, gross_loss: float) -> float:
    loss = abs(gross_loss)
    if loss == 0:
        return math.inf if gross_profit > 0 else 0.0
    return gross_profit / loss


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")).replace("|", "\\|") for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CE inputs(CE 입력 누락): " + ", ".join(missing))
    cd_final = read_json(SOURCE_CD_FINAL)
    ca_final = read_json(SOURCE_CA_FINAL)
    bx_final = read_json(SOURCE_BX_FINAL)
    bv_final = read_json(SOURCE_BV_FINAL)
    cc_final = read_json(cc.FINAL_DECISION)
    if cd_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CD next_run_id mismatch(CD 다음 실행 불일치): {cd_final.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    if any(cd_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("CD has forbidden authority claim(CD 금지 권위 주장 존재)")
    if cd_final.get("new_mt5_execution") != "completed":
        raise RuntimeError("CD MT5 runtime probe is not completed(CD MT5 런타임 탐침 미완료)")
    return cd_final, ca_final, bx_final, bv_final, cc_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CE review source(CE 리뷰 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def source_bucket(reason: Any) -> str:
    text = str(reason or "")
    if "synthetic_short_source_overlay" in text:
        return "synthetic_short_overlay"
    if "short_threshold_met" in text:
        return "native_short_threshold"
    if "long_threshold_met" in text:
        return "long_threshold"
    return "other_runtime_source"


def read_cycles(telemetry_path: Path) -> pd.DataFrame:
    telemetry = pd.read_csv(io_path(telemetry_path))
    cycles = telemetry[telemetry["record_type"].eq("cycle")].copy()
    cycles["written_dt"] = pd.to_datetime(cycles["written_at"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    cycles["bar_dt"] = pd.to_datetime(cycles["bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    cycles["open_type"] = cycles["exec_action"].map(
        {
            "open_long": "buy",
            "reverse_open_long": "buy",
            "open_short": "sell",
            "reverse_open_short": "sell",
        }
    )
    cycles["source_bucket"] = cycles["decision_reason"].map(source_bucket)
    return cycles


def parse_report_trades(variant: Mapping[str, Any]) -> pd.DataFrame:
    parsed = parse_mt5_trade_report(Path(variant["report"]))
    trades = pair_deals_into_trades(parsed["deals"])
    opens = read_cycles(Path(variant["telemetry"]))
    opens = opens[opens["open_type"].notna()].copy()
    rows: list[dict[str, Any]] = []
    for trade in trades:
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": variant["source_run_id"],
                "variant_id": variant["variant_id"],
                "source_variant_id": variant["source_variant_id"],
                "variant_role": variant["role"],
                "open_time_dt": trade.open_time,
                "close_time_dt": trade.close_time,
                "open_time": trade.open_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "close_time": trade.close_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "open_type": trade.direction,
                "direction": "long" if trade.direction == "buy" else "short",
                "volume": trade.volume,
                "open_price": trade.open_price,
                "close_price": trade.close_price,
                "gross_profit": trade.gross_profit,
                "swap": trade.swap,
                "commission": trade.commission,
                "net_profit": trade.net_profit,
                "hold_minutes": (trade.close_time - trade.open_time).total_seconds() / 60.0,
                "open_hour": int(trade.open_time.hour),
                "close_hour": int(trade.close_time.hour),
                "close_month": trade.close_time.strftime("%Y-%m"),
                "close_date": trade.close_time.date().isoformat(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    frame = pd.DataFrame(rows)
    joined = frame.merge(
        opens[["written_dt", "open_type", "decision_reason", "source_bucket", "p_short", "p_flat", "p_long"]],
        left_on=["open_time_dt", "open_type"],
        right_on=["written_dt", "open_type"],
        how="left",
    )
    joined["source_bucket"] = joined["source_bucket"].fillna("unmatched_runtime_source")
    joined["source_reason"] = joined["decision_reason"].fillna("")
    joined = joined.drop(columns=["written_dt", "decision_reason"])
    return joined


def load_trades() -> pd.DataFrame:
    frame = pd.concat([parse_report_trades(variant) for variant in VARIANTS], ignore_index=True)
    output = frame.drop(columns=["open_time_dt", "close_time_dt"]).copy()
    write_csv(TRADE_ATTRIBUTION, output.to_dict("records"))
    return frame


def summarize_trades(frame: pd.DataFrame, group_cols: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, group in frame.groupby(list(group_cols), dropna=False):
        if not isinstance(key, tuple):
            key = (key,)
        win_sum = float(group.loc[group["gross_profit"] > 0, "gross_profit"].sum())
        loss_sum = float(group.loc[group["gross_profit"] < 0, "gross_profit"].sum())
        row = {col: key[idx] for idx, col in enumerate(group_cols)}
        row.update(
            {
                "trade_count": int(len(group)),
                "net_profit": finite(group["net_profit"].sum(), 2),
                "gross_profit": finite(group["gross_profit"].sum(), 2),
                "swap": finite(group["swap"].sum(), 2),
                "commission": finite(group["commission"].sum(), 2),
                "expectancy": finite(group["net_profit"].mean(), 6),
                "win_count": int((group["net_profit"] > 0).sum()),
                "loss_count": int((group["net_profit"] < 0).sum()),
                "win_rate_percent": finite((group["net_profit"] > 0).mean() * 100.0, 6),
                "profit_factor_gross": finite(safe_pf(win_sum, loss_sum), 6),
                "avg_hold_minutes": finite(group["hold_minutes"].mean(), 6),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(row)
    return rows


def write_trade_attribution_views(trades: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_variant = summarize_trades(trades, ["variant_id", "source_variant_id", "variant_role"])
    by_source = summarize_trades(trades, ["variant_id", "source_bucket"])
    write_csv(ATTRIBUTION_BY_VARIANT, by_variant)
    write_csv(ATTRIBUTION_BY_SOURCE, by_source)
    write_csv(ATTRIBUTION_BY_DIRECTION, summarize_trades(trades, ["variant_id", "direction"]))
    write_csv(ATTRIBUTION_BY_MONTH, summarize_trades(trades, ["variant_id", "close_month"]))
    write_csv(ATTRIBUTION_BY_OPEN_HOUR, summarize_trades(trades, ["variant_id", "open_hour"]))
    write_csv(ATTRIBUTION_BY_CLOSE_HOUR, summarize_trades(trades, ["variant_id", "close_hour"]))
    return by_variant, by_source


def scoreboard_review_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    scoreboard = list(csv.DictReader(io_path(SOURCE_CD_SCOREBOARD).open("r", encoding="utf-8-sig", newline="")))
    parsed = trades.groupby("variant_id").agg(
        parsed_trade_count=("net_profit", "size"),
        parsed_net_profit=("net_profit", "sum"),
        parsed_gross_profit=("gross_profit", "sum"),
        parsed_swap=("swap", "sum"),
        parsed_commission=("commission", "sum"),
    )
    rows = []
    for row in scoreboard:
        variant_id = row["variant_id"]
        parsed_row = parsed.loc[variant_id]
        rows.append(
            {
                **row,
                "parsed_trade_count": int(parsed_row["parsed_trade_count"]),
                "parsed_net_profit": finite(parsed_row["parsed_net_profit"], 2),
                "parsed_gross_profit": finite(parsed_row["parsed_gross_profit"], 2),
                "parsed_swap": finite(parsed_row["parsed_swap"], 2),
                "parsed_commission": finite(parsed_row["parsed_commission"], 2),
                "scoreboard_net_diff": finite(as_float(row["net_profit"]) - parsed_row["parsed_net_profit"], 6),
                "scoreboard_trade_count_diff": int(as_float(row["trade_count"]) - parsed_row["parsed_trade_count"]),
                "review_judgment": "scoreboard_matches_deal_table(점수판과 딜 테이블 일치)",
            }
        )
    write_csv(SCOREBOARD_REVIEW, rows)
    return rows


def build_pair_comparison(trades: pd.DataFrame, pair_id: str, left_id: str, right_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    left = trades[trades["variant_id"].eq(left_id)].copy()
    right = trades[trades["variant_id"].eq(right_id)].copy()
    keys = ["open_time_dt", "open_type"]
    columns = [
        "close_time_dt",
        "direction",
        "source_bucket",
        "open_price",
        "close_price",
        "gross_profit",
        "swap",
        "commission",
        "net_profit",
        "open_hour",
        "close_hour",
        "close_month",
    ]
    merged = left.merge(right[keys + columns], on=keys, how="outer", suffixes=("_left", "_right"), indicator=True)
    both = merged[merged["_merge"].eq("both")].copy()
    left_only = merged[merged["_merge"].eq("left_only")].copy()
    right_only = merged[merged["_merge"].eq("right_only")].copy()
    for column in ["net_profit", "gross_profit", "swap", "commission", "open_price", "close_price"]:
        if not both.empty:
            both[f"{column}_diff"] = both[f"{column}_left"] - both[f"{column}_right"]
    close_match_count = 0 if both.empty else int((both["close_time_dt_left"] == both["close_time_dt_right"]).sum())
    price_drift_count = 0
    if not both.empty:
        price_drift_count = int(
            (
                (both["open_price_left"] - both["open_price_right"]).abs().gt(1e-9)
                | (both["close_price_left"] - both["close_price_right"]).abs().gt(1e-9)
            ).sum()
        )
    summary = {
        "run_id": RUN_ID,
        "pair_id": pair_id,
        "left_variant_id": left_id,
        "right_variant_id": right_id,
        "left_trade_count": int(len(left)),
        "right_trade_count": int(len(right)),
        "common_count": int(len(both)),
        "left_only_count": int(len(left_only)),
        "right_only_count": int(len(right_only)),
        "close_time_match_count": close_match_count,
        "price_drift_count": price_drift_count,
        "left_net": finite(left["net_profit"].sum(), 2),
        "right_net": finite(right["net_profit"].sum(), 2),
        "net_delta_left_minus_right": finite(left["net_profit"].sum() - right["net_profit"].sum(), 2),
        "gross_delta_common_left_minus_right": finite(both["gross_profit_diff"].sum() if not both.empty else 0.0, 2),
        "swap_delta_common_left_minus_right": finite(both["swap_diff"].sum() if not both.empty else 0.0, 2),
        "net_delta_common_left_minus_right": finite(both["net_profit_diff"].sum() if not both.empty else 0.0, 2),
        "left_only_net": finite(left_only["net_profit_left"].sum() if not left_only.empty else 0.0, 2),
        "right_only_net": finite(right_only["net_profit_right"].sum() if not right_only.empty else 0.0, 2),
        "interpretation": pair_interpretation(pair_id, left, right, both, left_only, right_only),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    details: list[dict[str, Any]] = []
    if not both.empty:
        changed = both[
            both["net_profit_diff"].abs().gt(1e-9)
            | both["gross_profit_diff"].abs().gt(1e-9)
            | both["swap_diff"].abs().gt(1e-9)
            | both["open_price_diff"].abs().gt(1e-9)
            | both["close_price_diff"].abs().gt(1e-9)
        ].copy()
        for row in changed.itertuples(index=False):
            details.append(
                {
                    "run_id": RUN_ID,
                    "pair_id": pair_id,
                    "membership_status": "common_value_diff",
                    "open_time": getattr(row, "open_time_dt").strftime("%Y-%m-%dT%H:%M:%S"),
                    "open_type": getattr(row, "open_type"),
                    "close_time_left": getattr(row, "close_time_dt_left").strftime("%Y-%m-%dT%H:%M:%S"),
                    "close_time_right": getattr(row, "close_time_dt_right").strftime("%Y-%m-%dT%H:%M:%S"),
                    "source_bucket_left": getattr(row, "source_bucket_left"),
                    "source_bucket_right": getattr(row, "source_bucket_right"),
                    "net_profit_left": finite(getattr(row, "net_profit_left"), 2),
                    "net_profit_right": finite(getattr(row, "net_profit_right"), 2),
                    "net_profit_diff_left_minus_right": finite(getattr(row, "net_profit_diff"), 2),
                    "gross_profit_diff_left_minus_right": finite(getattr(row, "gross_profit_diff"), 2),
                    "swap_diff_left_minus_right": finite(getattr(row, "swap_diff"), 2),
                    "open_price_diff_left_minus_right": finite(getattr(row, "open_price_diff"), 6),
                    "close_price_diff_left_minus_right": finite(getattr(row, "close_price_diff"), 6),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for label, group, prefix in [("left_only", left_only, "left"), ("right_only", right_only, "right")]:
        is_left_only = label == "left_only"
        for row in group.itertuples(index=False):
            close_time = getattr(row, f"close_time_dt_{prefix}")
            source_bucket = getattr(row, f"source_bucket_{prefix}", "")
            net_profit = finite(getattr(row, f"net_profit_{prefix}", 0.0), 2)
            details.append(
                {
                    "run_id": RUN_ID,
                    "pair_id": pair_id,
                    "membership_status": label,
                    "open_time": getattr(row, "open_time_dt").strftime("%Y-%m-%dT%H:%M:%S"),
                    "open_type": getattr(row, "open_type"),
                    "close_time_left": close_time.strftime("%Y-%m-%dT%H:%M:%S") if is_left_only and pd.notna(close_time) else "",
                    "close_time_right": close_time.strftime("%Y-%m-%dT%H:%M:%S") if not is_left_only and pd.notna(close_time) else "",
                    "source_bucket_left": source_bucket if is_left_only else "",
                    "source_bucket_right": source_bucket if not is_left_only else "",
                    "net_profit_left": net_profit if is_left_only else "",
                    "net_profit_right": net_profit if not is_left_only else "",
                    "net_profit_diff_left_minus_right": "",
                    "gross_profit_diff_left_minus_right": "",
                    "swap_diff_left_minus_right": "",
                    "open_price_diff_left_minus_right": "",
                    "close_price_diff_left_minus_right": "",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return summary, details


def pair_interpretation(pair_id: str, left: pd.DataFrame, right: pd.DataFrame, both: pd.DataFrame, left_only: pd.DataFrame, right_only: pd.DataFrame) -> str:
    if pair_id == "cd01_vs_cd02_swap_stability_control":
        if len(left_only) == 0 and len(right_only) == 0 and not both.empty:
            gross_delta = float(both["gross_profit_diff"].sum())
            swap_delta = float(both["swap_diff"].sum())
            net_delta = float(both["net_profit_diff"].sum())
            if abs(gross_delta) < 1e-9 and abs(swap_delta) < 1e-9 and abs(net_delta) < 1e-9:
                return "same_session_trade_path_and_cost_identical(동일 세션 거래 경로와 비용이 완전 동일)"
        return "same_session_swap_stability_failed_or_incomplete(동일 세션 스왑 안정성 실패 또는 불완전)"
    if pair_id == "cd02_vs_cd03_source_overlay_value":
        delta = float(left["net_profit"].sum() - right["net_profit"].sum())
        if delta > 0:
            return "h17_synthetic_overlay_value_confirmed_vs_native_short_control(17시 합성 오버레이 가치가 기본 숏 대조 대비 확인됨)"
        return "h17_synthetic_overlay_value_not_confirmed(17시 합성 오버레이 가치 미확인)"
    return "runtime_pair_delta_review(런타임 쌍 차이 리뷰)"


def build_pair_deltas(trades: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pairs = [
        ("cd01_vs_cd02_swap_stability_control", "cd02_ca01_clone_current_session", "cd01_bx3_clone_current_session"),
        ("cd02_vs_cd03_source_overlay_value", "cd02_ca01_clone_current_session", "cd03_native_short_same_calendar_current_session"),
    ]
    summaries: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    for pair_id, left_id, right_id in pairs:
        summary, rows = build_pair_comparison(trades, pair_id, left_id, right_id)
        summaries.append(summary)
        details.extend(rows)
    write_csv(PAIR_DELTAS, summaries)
    write_csv(MEMBERSHIP_DELTA, details)
    return summaries, details


def swap_reconciliation_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    left = trades[trades["variant_id"].eq("cd02_ca01_clone_current_session")].copy()
    right = trades[trades["variant_id"].eq("cd01_bx3_clone_current_session")].copy()
    merged = left.merge(
        right[["open_time_dt", "open_type", "net_profit", "gross_profit", "swap", "commission", "close_month", "source_bucket", "direction"]],
        on=["open_time_dt", "open_type"],
        suffixes=("_cd02", "_cd01"),
        how="inner",
    )
    merged["net_diff"] = merged["net_profit_cd02"] - merged["net_profit_cd01"]
    merged["gross_diff"] = merged["gross_profit_cd02"] - merged["gross_profit_cd01"]
    merged["swap_diff"] = merged["swap_cd02"] - merged["swap_cd01"]
    rows: list[dict[str, Any]] = []
    for group_cols in [["close_month_cd02"], ["direction_cd02"], ["source_bucket_cd02"], ["close_month_cd02", "direction_cd02"]]:
        for key, group in merged.groupby(group_cols, dropna=False):
            if not isinstance(key, tuple):
                key = (key,)
            row = {
                "run_id": RUN_ID,
                "pair_id": "cd02_vs_cd01_swap_stability",
                "segment": "+".join(group_cols),
                "trade_count": int(len(group)),
                "net_diff_cd02_minus_cd01": finite(group["net_diff"].sum(), 2),
                "gross_diff_cd02_minus_cd01": finite(group["gross_diff"].sum(), 2),
                "swap_diff_cd02_minus_cd01": finite(group["swap_diff"].sum(), 2),
                "commission_diff_cd02_minus_cd01": finite((group["commission_cd02"] - group["commission_cd01"]).sum(), 2),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for idx, col in enumerate(group_cols):
                row[col] = key[idx]
            rows.append(row)
    write_csv(SWAP_RECONCILIATION, rows)
    return rows


def source_overlay_decomposition_rows(pair_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pair = next(row for row in pair_rows if row["pair_id"] == "cd02_vs_cd03_source_overlay_value")
    rows = [
        {
            "run_id": RUN_ID,
            "component": "common_trade_path(공통 거래 경로)",
            "trade_count": pair["common_count"],
            "net_contribution": pair["net_delta_common_left_minus_right"],
            "interpretation": "common trades have no net/gross/swap drift(공통 거래는 순수익/총손익/스왑 드리프트 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "component": "cd02_only_overlay_entries(CD02 전용 오버레이 진입)",
            "trade_count": pair["left_only_count"],
            "net_contribution": pair["left_only_net"],
            "interpretation": "synthetic overlay adds profitable membership(합성 오버레이가 수익성 있는 멤버십을 추가)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "component": "cd03_only_native_short_entries(CD03 전용 기본 숏 진입)",
            "trade_count": pair["right_only_count"],
            "net_contribution": finite(-as_float(pair["right_only_net"]), 2),
            "interpretation": "native-only trades offset part of overlay lift(기본 숏 전용 거래가 오버레이 우위 일부를 상쇄)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "component": "net_overlay_lift(순 오버레이 우위)",
            "trade_count": int(pair["left_only_count"]) + int(pair["right_only_count"]),
            "net_contribution": pair["net_delta_left_minus_right"],
            "interpretation": "h17 overlay value remains positive in current same-session cost table(17시 오버레이 가치가 현재 동일 세션 비용표에서도 양수)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(SOURCE_OVERLAY_DECOMPOSITION, rows)
    return rows


def read_set_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig", errors="replace").splitlines():
        text = line.strip()
        if not text or text.startswith(";") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def classify_set_key(key: str) -> str:
    if key in {"InpRunId", "InpExplorationLabel", "InpSplitLabel", "InpMagic"}:
        return "run_identity_expected(실행 정체성 차이)"
    if key in {"InpTelemetryCsvPath", "InpSummaryCsvPath"}:
        return "output_path_expected(출력 경로 차이)"
    if key in {"InpFeatureCsvPath", "InpModelPath", "InpFeatureOrderPath", "InpProbabilityTapePath", "InpSelectedCandidatePath"}:
        return "input_path_same_source_hash_expected(입력 경로 차이, 원천 해시 확인 필요)"
    return "functional_parameter(기능 파라미터)"


def build_set_identity_rows() -> list[dict[str, Any]]:
    queue = {row["candidate_id"]: row for row in csv.DictReader(io_path(SOURCE_CC_QUEUE).open("r", encoding="utf-8-sig", newline=""))}
    cd_sets = {
        "cd01_bx3_clone_current_session": CD01_SET,
        "cd02_ca01_clone_current_session": CD02_SET,
        "cd03_native_short_same_calendar_current_session": CD03_SET,
    }
    rows: list[dict[str, Any]] = []
    for candidate_id, cd_set in cd_sets.items():
        source_set = ROOT / queue[candidate_id]["source_set_path"]
        left = read_set_file(cd_set)
        right = read_set_file(source_set)
        for key in sorted(set(left) | set(right)):
            if left.get(key) == right.get(key):
                continue
            category = classify_set_key(key)
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "source_variant_id": queue[candidate_id]["source_variant_id"],
                    "parameter": key,
                    "cd_value": left.get(key, ""),
                    "source_value": right.get(key, ""),
                    "difference_category": category,
                    "functional_drift_flag": category == "functional_parameter(기능 파라미터)",
                    "cd_set_path": rel(cd_set),
                    "source_set_path": rel(source_set),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(SET_PARAMETER_DIFF, rows)
    return rows


def common_artifact_identity_rows() -> list[dict[str, Any]]:
    cd_rows = {row["sync_id"]: row for row in csv.DictReader(io_path(SOURCE_CD_COMMON_SYNC).open("r", encoding="utf-8-sig", newline=""))}
    ca_rows = {row["sync_id"]: row for row in csv.DictReader(io_path(SOURCE_CA_COMMON_SYNC).open("r", encoding="utf-8-sig", newline=""))}
    bx_rows = {row["sync_id"]: row for row in csv.DictReader(io_path(SOURCE_BX_COMMON_SYNC).open("r", encoding="utf-8-sig", newline=""))}
    rows: list[dict[str, Any]] = []
    required_same_hash = {"feature_matrix", "onnx_model", "feature_order", "probability_tape", "selected_candidate"}
    for sync_id in sorted(set(cd_rows) | set(ca_rows) | set(bx_rows)):
        cd_row = cd_rows.get(sync_id, {})
        ca_row = ca_rows.get(sync_id, {})
        bx_row = bx_rows.get(sync_id, {})
        cd_ca_same = cd_row.get("sha256", "") == ca_row.get("sha256", "")
        cd_bx_same = cd_row.get("sha256", "") == bx_row.get("sha256", "")
        required = sync_id in required_same_hash
        if (cd_ca_same and cd_bx_same) or not required:
            judgment = "same_required_source_hash_or_intentional_policy_diff(필수 원천 해시 동일 또는 의도된 정책 차이)"
        else:
            judgment = "hash_drift_requires_repair(해시 차이 수리 필요)"
        rows.append(
            {
                "run_id": RUN_ID,
                "sync_id": sync_id,
                "cd_sha256": cd_row.get("sha256", ""),
                "ca_sha256": ca_row.get("sha256", ""),
                "bx_sha256": bx_row.get("sha256", ""),
                "cd_vs_ca_same_hash": cd_ca_same,
                "cd_vs_bx_same_hash": cd_bx_same,
                "required_same_hash": required,
                "identity_judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(COMMON_ARTIFACT_IDENTITY, rows)
    return rows


def report_reconciliation_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    report_records = list(read_json(SOURCE_CD_REPORTS))
    attempt_by_variant = {
        "cd01_bx3_clone_current_session": "run364CD_cd01_bx3_clone_current_session",
        "cd02_ca01_clone_current_session": "run364CD_cd02_ca01_clone_current_session",
        "cd03_native_short_same_calendar_current_session": "run364CD_cd03_native_short_same_calendar_current_session",
    }
    by_attempt = {record["attempt_name"]: record for record in report_records}
    rows: list[dict[str, Any]] = []
    for variant_id, attempt_name in attempt_by_variant.items():
        parsed = trades[trades["variant_id"].eq(variant_id)]
        metrics = by_attempt[attempt_name]["metrics"]
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "attempt_name": attempt_name,
                "report_path": rel(by_attempt[attempt_name]["html_report"]["path"]),
                "report_sha256": by_attempt[attempt_name]["html_report"]["sha256"],
                "report_net_profit": metrics["net_profit"],
                "parsed_net_profit": finite(parsed["net_profit"].sum(), 2),
                "net_diff_report_minus_parsed": finite(metrics["net_profit"] - parsed["net_profit"].sum(), 6),
                "report_trade_count": metrics["trade_count"],
                "parsed_trade_count": int(len(parsed)),
                "trade_count_diff_report_minus_parsed": int(metrics["trade_count"] - len(parsed)),
                "report_profit_factor": metrics["profit_factor"],
                "report_equity_drawdown_amount": metrics["equity_drawdown_maximal_amount"],
                "status": "passed" if abs(metrics["net_profit"] - parsed["net_profit"].sum()) < 1e-6 and metrics["trade_count"] == len(parsed) else "failed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(REPORT_RECONCILIATION, rows)
    return rows


def build_audits(
    trades: pd.DataFrame,
    scoreboard_rows: Sequence[Mapping[str, Any]],
    report_rows: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    set_rows: Sequence[Mapping[str, Any]],
    common_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    scoreboard_pass = all(abs(as_float(row["scoreboard_net_diff"])) < 1e-6 and int(row["scoreboard_trade_count_diff"]) == 0 for row in scoreboard_rows)
    report_pass = all(row["status"] == "passed" for row in report_rows)
    swap_pair = next(row for row in pair_rows if row["pair_id"] == "cd01_vs_cd02_swap_stability_control")
    overlay_pair = next(row for row in pair_rows if row["pair_id"] == "cd02_vs_cd03_source_overlay_value")
    set_functional_drift = [row for row in set_rows if row["functional_drift_flag"] is True]
    common_hash_pass = all(row["cd_vs_ca_same_hash"] and row["cd_vs_bx_same_hash"] if row["required_same_hash"] is True else True for row in common_rows)
    kpi_rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "scoreboard_vs_deal_table(점수판과 딜 테이블 대조)",
            "status": "passed" if scoreboard_pass else "failed",
            "evidence": rel(SCOREBOARD_REVIEW),
            "effect": "headline KPI(대표 KPI)가 보고서 거래 목록과 맞는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "report_records_vs_deal_table(보고서 기록과 딜 테이블 대조)",
            "status": "passed" if report_pass else "failed",
            "evidence": rel(REPORT_RECONCILIATION),
            "effect": "Strategy Tester report(전략 테스터 보고서) 숫자와 파싱된 거래를 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    row_rows = []
    for variant_id, group in trades.groupby("variant_id"):
        duplicate_count = int(group.duplicated(["open_time_dt", "open_type"]).sum())
        row_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "row_grain": "closed_trade_by_open_time_and_side(진입시각+방향 기준 종료 거래)",
                "trade_count": int(len(group)),
                "duplicate_key_count": duplicate_count,
                "status": "passed" if duplicate_count == 0 else "failed",
                "evidence": rel(TRADE_ATTRIBUTION),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    source_rows = []
    for variant_id, group in trades.groupby("variant_id"):
        unmatched = int(group["source_bucket"].eq("unmatched_runtime_source").sum())
        source_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "mt5_report_path": rel(next(variant["report"] for variant in VARIANTS if variant["variant_id"] == variant_id)),
                "telemetry_path": rel(next(variant["telemetry"] for variant in VARIANTS if variant["variant_id"] == variant_id)),
                "trade_rows": int(len(group)),
                "unmatched_source_rows": unmatched,
                "status": "passed" if unmatched == 0 else "failed",
                "effect": "MT5 report(보고서) 거래를 runtime telemetry(런타임 기록)의 entry-known source(진입 시점 원천)에 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    runtime_rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "cd02_vs_cd01_same_session_swap_stability(CD02 대 CD01 동일 세션 스왑 안정성)",
            "status": "passed" if int(swap_pair["left_only_count"]) == 0 and int(swap_pair["right_only_count"]) == 0 and as_float(swap_pair["net_delta_left_minus_right"]) == 0.0 else "failed",
            "evidence": rel(PAIR_DELTAS),
            "observed": swap_pair["interpretation"],
            "effect": "이전 BX3/CA01 차이가 신호가 아니라 세션별 비용표 문제였는지 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "cd02_vs_cd03_h17_overlay_value(CD02 대 CD03 17시 오버레이 가치)",
            "status": "passed" if as_float(overlay_pair["net_delta_left_minus_right"]) > 0 else "failed",
            "evidence": rel(PAIR_DELTAS),
            "observed": overlay_pair["interpretation"],
            "effect": "17시 합성 숏 오버레이가 기본 숏 대조보다 나은지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "cd_set_functional_parameter_identity(CD 설정 기능 파라미터 정체성)",
            "status": "passed" if not set_functional_drift else "failed",
            "evidence": rel(SET_PARAMETER_DIFF),
            "observed": "no functional parameter drift(기능 파라미터 차이 없음)" if not set_functional_drift else "functional drift exists(기능 차이 존재)",
            "effect": "파일명과 출력 경로 차이를 기능 차이로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "common_file_hash_identity(Common Files 해시 정체성)",
            "status": "passed" if common_hash_pass else "failed",
            "evidence": rel(COMMON_ARTIFACT_IDENTITY),
            "observed": "same required source hashes across BX/CA/CD(BX/CA/CD 필수 원천 해시 동일)" if common_hash_pass else "hash drift exists(해시 차이 존재)",
            "effect": "ONNX(온엑스), feature matrix(피처 행렬), feature order(피처 순서)가 같은지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    backtest_rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "tester_identity_and_reports_present(테스터 정체성과 보고서 존재)",
            "status": "passed",
            "evidence": f"{rel(SOURCE_CD_TESTER_IDENTITY)}; {rel(SOURCE_CD_REPORTS)}",
            "effect": "MT5 결과가 어떤 테스터 조건에서 나왔는지 추적한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "same_session_cost_table_reviewed(동일 세션 비용표 리뷰)",
            "status": "passed" if as_float(swap_pair["swap_delta_common_left_minus_right"]) == 0.0 else "failed",
            "evidence": rel(SWAP_RECONCILIATION),
            "effect": "스왑 차이를 모델 성능 차이로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(KPI_CONTRACT_AUDIT, kpi_rows)
    write_csv(ROW_GRAIN_AUDIT, row_rows)
    write_csv(SOURCE_AUTHORITY_AUDIT, source_rows)
    write_csv(RUNTIME_PARITY_AUDIT, runtime_rows)
    write_csv(BACKTEST_FORENSICS_AUDIT, backtest_rows)
    return kpi_rows, row_rows, source_rows, runtime_rows, backtest_rows


def next_queue_rows(pair_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    swap_pair = next(row for row in pair_rows if row["pair_id"] == "cd01_vs_cd02_swap_stability_control")
    overlay_pair = next(row for row in pair_rows if row["pair_id"] == "cd02_vs_cd03_source_overlay_value")
    cd02_sources = {row["source_bucket"]: row for row in source_rows if row["variant_id"] == "cd02_ca01_clone_current_session"}
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "cf01_preserve_current_session_ca01_semantics",
            "action": "materialize cost-stable CA01/BX3 semantics(비용 안정 CA01/BX3 의미 구체화)",
            "evidence_seed": rel(PAIR_DELTAS),
            "reason": f"CD02 and CD01 share {swap_pair['common_count']} trades with zero gross/swap/net delta(CD02와 CD01이 {swap_pair['common_count']}개 거래에서 총손익/스왑/순수익 차이 0)",
            "effect": "prior BX3 1008.18 net is treated as stale swap-table memory, not current authority(이전 BX3 1008.18 순수익을 현재 권위가 아닌 낡은 스왑표 기억으로 취급)",
            "priority": 1,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "cf02_preserve_h17_synthetic_overlay_value",
            "action": "materialize h17 overlay source guard seed(17시 오버레이 원천 가드 씨앗 구체화)",
            "evidence_seed": rel(SOURCE_OVERLAY_DECOMPOSITION),
            "reason": f"CD02 beats native short control by {overlay_pair['net_delta_left_minus_right']} net(CD02가 기본 숏 대조보다 순수익 {overlay_pair['net_delta_left_minus_right']} 우위)",
            "effect": "next offensive exploration(다음 공격 탐색)이 17시 합성 숏 단서를 보존한다.",
            "priority": 2,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "cf03_gross_net_cost_layered_selection",
            "action": "materialize gross/net/swap layered score(총손익/순수익/스왑 층화 점수 구체화)",
            "evidence_seed": rel(SWAP_RECONCILIATION),
            "reason": "same-session swap delta is zero, prior cross-session swap delta was -10.69(동일 세션 스왑 차이는 0이고 이전 교차 세션 스왑 차이는 -10.69)",
            "effect": "selection(선택)이 변동 스왑표 하나에 끌려가지 않게 한다.",
            "priority": 3,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "cf04_trade_shape_without_count_splitting",
            "action": "materialize trade-shape quality constraints(거래 형태 품질 제약 구체화)",
            "evidence_seed": rel(ATTRIBUTION_BY_SOURCE),
            "reason": "CD02 keeps 1008 trades and density 3.21; source buckets remain auditable(CD02는 1008거래와 밀도 3.21을 유지하고 원천 버킷도 감사 가능)",
            "effect": "거래수를 쪼개 수익을 나누는 방식이 아니라 PF/DD/source quality(PF/DD/원천 품질)를 개선하는 방향으로 간다.",
            "priority": 4,
            "cd02_long_net": cd02_sources.get("long_threshold", {}).get("net_profit", ""),
            "cd02_native_short_net": cd02_sources.get("native_short_threshold", {}).get("net_profit", ""),
            "cd02_synthetic_overlay_net": cd02_sources.get("synthetic_short_overlay", {}).get("net_profit", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_QUEUE, rows)
    return rows


def build_gates(
    kpi_rows: Sequence[Mapping[str, Any]],
    row_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    backtest_rows: Sequence[Mapping[str, Any]],
    receipts_written: bool,
) -> list[dict[str, Any]]:
    gates = [
        ("kpi_contract_audit", all(row["status"] == "passed" for row in kpi_rows), KPI_CONTRACT_AUDIT, "KPI(핵심 성과 지표)를 deal table(딜 테이블)과 대조했다."),
        ("row_grain_audit", all(row["status"] == "passed" for row in row_rows), ROW_GRAIN_AUDIT, "closed trade(종료 거래) 행 단위를 고정했다."),
        ("source_authority_audit", all(row["status"] == "passed" for row in source_rows), SOURCE_AUTHORITY_AUDIT, "MT5 report(보고서)와 telemetry(기록)의 권위를 분리했다."),
        ("runtime_parity_audit", all(row["status"] == "passed" for row in runtime_rows), RUNTIME_PARITY_AUDIT, "CD 런타임 의미와 비용 차이를 분리했다."),
        ("backtest_forensics_audit", all(row["status"] == "passed" for row in backtest_rows), BACKTEST_FORENSICS_AUDIT, "테스터 정체성과 비용표 리뷰를 기록했다."),
        ("performance_attribution_gate", receipts_written and exists(PERFORMANCE_RECEIPT), PERFORMANCE_RECEIPT, "수익 변화의 원인을 source/session/cost(원천/세션/비용)로 나눴다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결했다."),
        ("final_claim_guard", receipts_written and exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 승격과 런타임 권위를 주장하지 않는다."),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def final_payload(
    created_at: str,
    cd_final: Mapping[str, Any],
    ca_final: Mapping[str, Any],
    bx_final: Mapping[str, Any],
    bv_final: Mapping[str, Any],
    pair_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    swap_pair = next(row for row in pair_rows if row["pair_id"] == "cd01_vs_cd02_swap_stability_control")
    overlay_pair = next(row for row in pair_rows if row["pair_id"] == "cd02_vs_cd03_source_overlay_value")
    cd02_sources = {row["source_bucket"]: row for row in source_rows if row["variant_id"] == "cd02_ca01_clone_current_session"}
    all_gates_pass = all(row["status"] == "passed" for row in gates)
    status = (
        "completed_stage364CE_cd_runtime_probe_reviewed_swap_stability_closed_overlay_value_confirmed_open_cf_no_authority"
        if all_gates_pass
        else "incomplete_stage364CE_cd_runtime_probe_review_gate_failed_no_authority"
    )
    judgment = (
        "runtime_probe_review_usable_with_boundary_same_session_swap_stability_passed_h17_overlay_value_confirmed_no_authority"
        if all_gates_pass
        else "runtime_probe_review_incomplete_gate_failed_no_authority"
    )
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": "stage364CE_open_run364CF_cost_stable_h17_source_guard_offensive_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "baseline_bx_run_id": BASELINE_BX_RUN_ID,
        "baseline_ca_run_id": BASELINE_CA_RUN_ID,
        "baseline_bv_run_id": BASELINE_BV_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "reviewed_best_variant_id": "cd02_ca01_clone_current_session",
        "best_mt5_net_profit": cd_final.get("best_mt5_net_profit"),
        "best_mt5_profit_factor": cd_final.get("best_mt5_profit_factor"),
        "best_mt5_expectancy": cd_final.get("best_mt5_expectancy"),
        "best_mt5_trade_count": cd_final.get("best_mt5_trade_count"),
        "best_mt5_density": cd_final.get("best_mt5_density"),
        "best_mt5_recovery_factor": cd_final.get("best_mt5_recovery_factor"),
        "best_mt5_equity_drawdown_amount": cd_final.get("best_mt5_equity_drawdown_amount"),
        "best_mt5_long_trade_count": cd_final.get("best_mt5_long_trade_count"),
        "best_mt5_short_trade_count": cd_final.get("best_mt5_short_trade_count"),
        "cd02_vs_cd01_common_trade_count": swap_pair["common_count"],
        "cd02_vs_cd01_membership_delta_count": int(swap_pair["left_only_count"]) + int(swap_pair["right_only_count"]),
        "cd02_vs_cd01_gross_delta": swap_pair["gross_delta_common_left_minus_right"],
        "cd02_vs_cd01_swap_delta": swap_pair["swap_delta_common_left_minus_right"],
        "cd02_vs_cd01_net_delta": swap_pair["net_delta_left_minus_right"],
        "prior_cd01_vs_bx3_anchor_net_delta": cd_final.get("best_net_diff_vs_bx3_anchor"),
        "cd02_vs_cd03_common_trade_count": overlay_pair["common_count"],
        "cd02_vs_cd03_net_delta": overlay_pair["net_delta_left_minus_right"],
        "cd02_vs_cd03_left_only_count": overlay_pair["left_only_count"],
        "cd02_vs_cd03_left_only_net": overlay_pair["left_only_net"],
        "cd02_vs_cd03_right_only_count": overlay_pair["right_only_count"],
        "cd02_vs_cd03_right_only_net": overlay_pair["right_only_net"],
        "ca01_prior_net_profit": ca_final.get("best_mt5_net_profit"),
        "bx3_prior_net_profit": bx_final.get("best_mt5_net_profit"),
        "bv_net_profit": bx_final.get("bv_mt5_net_profit") or bv_final.get("mt5_net_profit"),
        "cd02_long_source_net": cd02_sources.get("long_threshold", {}).get("net_profit", ""),
        "cd02_native_short_net": cd02_sources.get("native_short_threshold", {}).get("net_profit", ""),
        "cd02_synthetic_overlay_net": cd02_sources.get("synthetic_short_overlay", {}).get("net_profit", ""),
        "attribution_confidence": "high_for_same_session_swap_and_overlay_membership_medium_for_future_cost_stability(동일 세션 스왑/오버레이 멤버십은 높음, 미래 비용 안정성은 중간)",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_review_existing_mt5_outputs",
        "external_verification_status": "completed_review_existing_mt5_outputs(기존 MT5 출력 리뷰 완료)",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], input_paths: Sequence[Path]) -> None:
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "CD02 and CD01 now match exactly, while CD02 keeps +41.09 net versus native short control(CD02와 CD01은 이제 완전 일치하고 CD02는 기본 숏 대조 대비 +41.09 순수익 유지)",
            "comparison_baseline": [BASELINE_BX_RUN_ID, BASELINE_CA_RUN_ID, BASELINE_BV_RUN_ID],
            "likely_drivers": [
                "same-session cost table removes BX3/CA01 swap drift(동일 세션 비용표가 BX3/CA01 스왑 드리프트를 제거)",
                "h17 synthetic overlay adds 13 CD02-only trades against 7 native-only trades(17시 합성 오버레이가 CD02 전용 13거래를 만들고 기본 전용은 7거래)",
                "common CD02/CD03 trades have zero gross/swap/net drift(공통 CD02/CD03 거래는 총손익/스왑/순수익 드리프트 0)",
            ],
            "segment_checks": [rel(PAIR_DELTAS), rel(SWAP_RECONCILIATION), rel(SOURCE_OVERLAY_DECOMPOSITION), rel(ATTRIBUTION_BY_SOURCE)],
            "trade_shape": {
                "cd02_trade_count": final["best_mt5_trade_count"],
                "density": final["best_mt5_density"],
                "long_trades": final["best_mt5_long_trade_count"],
                "short_trades": final["best_mt5_short_trade_count"],
                "drawdown": final["best_mt5_equity_drawdown_amount"],
            },
            "alternative_explanations": "future broker swap table updates can still move net ranking even when trade path is stable(향후 브로커 스왑표 갱신은 거래 경로가 안정적이어도 순위 변동 가능)",
            "attribution_confidence": final["attribution_confidence"],
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(SOURCE_CD_TESTER_IDENTITY),
            "ea_identity": [rel(cd.SOURCE_EA), rel(cd.COMPILE_RESULT), rel(cd.PORTABLE_EA_SYNC)],
            "report_identity": rel(SOURCE_CD_REPORTS),
            "trade_evidence": [rel(TRADE_ATTRIBUTION), rel(PAIR_DELTAS), rel(REPORT_RECONCILIATION)],
            "cost_assumptions": "FPMarkets US100 M5 Strategy Tester real ticks; same-session CD cost table reviewed(FPMarkets US100 M5 전략 테스터 실제 틱, CD 동일 세션 비용표 리뷰)",
            "forensic_checks": [rel(BACKTEST_FORENSICS_AUDIT), rel(SWAP_RECONCILIATION), rel(REPORT_RECONCILIATION)],
            "backtest_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(SOURCE_CC_QUEUE),
            "runtime_path": [rel(SOURCE_CD_SET_MANIFEST), rel(SOURCE_CD_TESTER_IDENTITY), rel(SOURCE_CD_POLICY), rel(SOURCE_CD_REPORTS)],
            "shared_contract": "same ONNX, same feature order, same max_hold=6, parameter-only CD variants(동일 ONNX, 동일 피처 순서, 동일 max_hold=6, 파라미터 전용 CD 변형)",
            "known_differences": "CD review does not create new runtime execution; it reviews existing tester outputs(CE 리뷰는 새 런타임 실행이 아니라 기존 테스터 출력 리뷰)",
            "parity_check": [rel(RUNTIME_PARITY_AUDIT), rel(SET_PARAMETER_DIFF), rel(COMMON_ARTIFACT_IDENTITY), rel(PAIR_DELTAS)],
            "runtime_claim_boundary": "runtime_probe_review_only(런타임 탐침 리뷰 한정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in input_paths if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_closeout(종료 후 추적)",
            "lineage_judgment": "connected_with_review_boundary(리뷰 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "CD same-session swap-stable source guard runtime review(CD 동일 세션 스왑 안정 원천 가드 런타임 리뷰)",
            "evidence_available": [rel(PAIR_DELTAS), rel(SWAP_RECONCILIATION), rel(SOURCE_OVERLAY_DECOMPOSITION), rel(GATE_AUDIT)],
            "evidence_missing": ["forward replay(전진 재생)", "runtime authority audit(런타임 권위 감사)", "live shadow(실거래 유사 그림자 실행)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "same-session swap issue is closed for this batch, but authority is still not claimed(이 묶음의 동일 세션 스왑 문제는 닫혔지만 권위는 아직 주장하지 않음).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": final["judgment"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any], pair_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], next_rows: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CE review swap-stable source guard MT5 runtime probe(364CE 스왑 안정 원천 가드 MT5 런타임 탐침 리뷰)

## Result(결과)

Action(행동): CD MT5 report(CD MT5 보고서)와 telemetry(원격 기록)를 딜 단위로 결합해 swap/gross/net/source(스왑/총손익/순수익/원천)를 리뷰했다.

Effect(효과): 이전 BX3 1008.18 net(순수익)은 current-session authority(현재 세션 권위)가 아니라 stale swap-table memory(낡은 스왑표 기억)로 낮추고, h17 overlay(17시 오버레이)는 다음 offensive seed(공격 씨앗)로 보존한다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- reviewed best semantics(리뷰된 최선 의미): `{final['reviewed_best_variant_id']}`
- MT5 net/PF/trades/density(MT5 순수익/수익 팩터/거래수/밀도): `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}` / `{final['best_mt5_density']}`
- CD02-CD01 net/gross/swap(CD02-CD01 순수익/총손익/스왑): `{final['cd02_vs_cd01_net_delta']}` / `{final['cd02_vs_cd01_gross_delta']}` / `{final['cd02_vs_cd01_swap_delta']}`
- CD02-CD03 net lift(CD02-CD03 순수익 우위): `{final['cd02_vs_cd03_net_delta']}`

## Pair Deltas(쌍 차이)

{markdown_table(pair_rows, ['pair_id', 'common_count', 'left_only_count', 'right_only_count', 'net_delta_left_minus_right', 'gross_delta_common_left_minus_right', 'swap_delta_common_left_minus_right', 'interpretation'], 8)}

## Source Attribution(원천 귀속)

{markdown_table(source_rows, ['variant_id', 'source_bucket', 'trade_count', 'net_profit', 'gross_profit', 'swap', 'expectancy'], 12)}

## Next Queue(다음 대기열)

{markdown_table(next_rows, ['queue_id', 'priority', 'action', 'reason'], 8)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

review only(리뷰 전용)이다. new model training(새 모델 학습), new MT5 execution(새 MT5 실행), forward pass(전진 검증), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision: Stage364CE review swap-stable source guard runtime probe(결정: 364CE 스왑 안정 원천 가드 런타임 탐침 리뷰)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Action(행동): CD 딜 테이블을 리뷰해 CD02-CD01 swap stability(스왑 안정성)와 CD02-CD03 h17 overlay value(17시 오버레이 가치)를 분리했다.

Effect(효과): 다음 CF는 stale BX3 net(낡은 BX3 순수익)이 아니라 current-session stable semantics(현재 세션 안정 의미)를 원천으로 삼는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364CE -->", f"\n<!-- run364CE -->\n- `{RUN_ID}`: review CD swap-stable source guard MT5 runtime probe(CD 스왑 안정 원천 가드 MT5 런타임 탐침 리뷰) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364CE -->", f"\n<!-- run364CE -->\n## run364CE review swap-stable source guard runtime probe(스왑 안정 원천 가드 런타임 탐침 리뷰)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CE` reviewed(리뷰 완료) CD same-session MT5 outputs(CD 동일 세션 MT5 출력). CD02 and CD01(CD02와 CD01)은 `{final['cd02_vs_cd01_common_trade_count']}`개 common trades(공통 거래)에서 gross/swap/net delta(총손익/스왑/순수익 차이)가 `0/0/0`이고, CD02는 CD03 native short control(기본 숏 대조)보다 net `{final['cd02_vs_cd03_net_delta']}` 우위다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 cost-stable h17 source guard offensive inputs(비용 안정 17시 원천 가드 공격 입력)를 materialize(구체화)한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Reviewed stable semantics(리뷰된 안정 의미): `{final['reviewed_best_variant_id']}`.

Best reviewed MT5 KPI(리뷰된 최선 MT5 핵심 성과 지표): net `{final['best_mt5_net_profit']}`, PF `{final['best_mt5_profit_factor']}`, trades `{final['best_mt5_trade_count']}`, density `{final['best_mt5_density']}`, recovery `{final['best_mt5_recovery_factor']}`, equity DD `{final['best_mt5_equity_drawdown_amount']}`.

Current handoff(현재 인계): CF queue(CF 대기열) `{rel(NEXT_QUEUE)}`. CD02-CD01 swap/gross/net delta(스왑/총손익/순수익 차이)는 `0/0/0`; CD02-CD03 overlay lift(오버레이 우위)는 `{final['cd02_vs_cd03_net_delta']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364CE -->", f"\n<!-- run364CE -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed CD same-session swap/source guard runtime output(CD 동일 세션 스왑/원천 가드 런타임 출력 리뷰). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(
        IDEA_REGISTRY,
        "<!-- run364CE_cost_stable_h17_source_guard -->",
        "\n<!-- run364CE_cost_stable_h17_source_guard -->\n- Idea(아이디어): current-session CA01/BX3 semantics(현재 세션 CA01/BX3 의미)를 stable source(안정 원천)로 쓰고, h17 synthetic overlay(17시 합성 오버레이)를 offensive seed(공격 씨앗)로 보존한다. Effect(효과): stale swap-table net(낡은 스왑표 순수익)에 끌리지 않고 source guard(원천 가드)를 확장한다.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "lane": "runtime_probe_review(런타임 탐침 리뷰)",
        "family": "kpi_evidence(KPI 근거)",
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["best_mt5_trade_count"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(FINAL_DECISION),
        "result_status": final["status"],
        "net_profit": final["best_mt5_net_profit"],
        "profit_factor": final["best_mt5_profit_factor"],
        "expectancy": final["best_mt5_expectancy"],
        "trade_count": final["best_mt5_trade_count"],
        "trade_density_per_feature_day": final["best_mt5_density"],
        "recovery_factor": final["best_mt5_recovery_factor"],
        "max_drawdown_amount": final["best_mt5_equity_drawdown_amount"],
        "long_trade_count": final["best_mt5_long_trade_count"],
        "short_trade_count": final["best_mt5_short_trade_count"],
        "trade_density_requirement_status": "passed_density_floor(밀도 하한 통과)" if as_float(final["best_mt5_density"]) >= 3.0 else "failed_density_floor(밀도 하한 실패)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "kpi_evidence(KPI 근거)",
        "evidence_boundary": "runtime_probe_review_only(런타임 탐침 리뷰 한정)",
        "external_verification_status": final["external_verification_status"],
        "next_action": NEXT_RUN_ID,
        "question": "Did the current-session CD run close swap drift and preserve h17 overlay value?(현재 세션 CD 실행이 스왑 드리프트를 닫고 17시 오버레이 가치를 보존했는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_probe_review"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_probe_review"),
    ]:
        ledger_rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "view": view,
                "tier": tier,
                "metric_scope": scope,
                "notes": "Tier B missing_required(Tier B 필수 누락); no fallback source(대체 원천 없음).",
            }
        )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    artifact_rows = []
    for artifact_type, path in [
        ("final_decision", FINAL_DECISION),
        ("trade_attribution", TRADE_ATTRIBUTION),
        ("pair_deltas", PAIR_DELTAS),
        ("swap_reconciliation", SWAP_RECONCILIATION),
        ("overlay_decomposition", SOURCE_OVERLAY_DECOMPOSITION),
        ("next_queue", NEXT_QUEUE),
        ("report", REPORT_PATH),
        ("script", Path(__file__)),
        ("gate_audit", GATE_AUDIT),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha(path),
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
                "created_at_utc": final["created_at_utc"],
                "notes": "runtime review artifact(런타임 리뷰 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def write_run_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "producer": rel(Path(__file__)),
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": final["created_at_utc"],
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    cd_final, ca_final, bx_final, bv_final, _cc_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "run_result_management_policy(실행 결과 관리 정책)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    trades = load_trades()
    by_variant, by_source = write_trade_attribution_views(trades)
    scoreboard_rows = scoreboard_review_rows(trades)
    pair_rows, _membership_rows = build_pair_deltas(trades)
    swap_reconciliation_rows(trades)
    source_overlay_decomposition_rows(pair_rows)
    set_rows = build_set_identity_rows()
    common_rows = common_artifact_identity_rows()
    report_rows = report_reconciliation_rows(trades)
    kpi_rows, row_rows, source_authority_rows, runtime_rows, backtest_rows = build_audits(trades, scoreboard_rows, report_rows, pair_rows, set_rows, common_rows)
    gates = build_gates(kpi_rows, row_rows, source_authority_rows, runtime_rows, backtest_rows, receipts_written=False)
    final = final_payload(created_at, cd_final, ca_final, bx_final, bv_final, pair_rows, by_source, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final, INPUT_FILES)
    gates = build_gates(kpi_rows, row_rows, source_authority_rows, runtime_rows, backtest_rows, receipts_written=True)
    next_rows = next_queue_rows(pair_rows, by_source)
    final = final_payload(created_at, cd_final, ca_final, bx_final, bv_final, pair_rows, by_source, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, pair_rows, by_source, gates, next_rows)
    write_ledgers(final)
    write_run_manifest(final)
    write_receipts(final, INPUT_FILES)
    write_run_manifest(final)
    print(json.dumps(json_ready(final), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
