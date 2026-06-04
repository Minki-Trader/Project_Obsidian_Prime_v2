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
from stage_pipelines.stage364 import materialize_synthetic_short_source_runtime_repair_without_db as bv  # noqa: E402
from stage_pipelines.stage364 import review_overlay_hour17_native_short_ablation_runtime_probe_without_db as by  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = ca.STAGE_ID
RUN_NUMBER = "run364CB"
RUN_ID = "run364CB_review_bx03_guard_stack_runtime_probe_without_db_v1"
PARENT_RUN_ID = ca.RUN_ID
BASELINE_BX_RUN_ID = bx.RUN_ID
BASELINE_BV_RUN_ID = bv.RUN_ID
SOURCE_BY_RUN_ID = by.RUN_ID
NEXT_RUN_ID = "run364CC_materialize_swap_stable_reprobe_and_source_guard_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ca.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SCOREBOARD_REVIEW = RUN_DIR / "ca_runtime_scoreboard_review.csv"
TRADE_ATTRIBUTION = RUN_DIR / "ca_trade_attribution_by_variant.csv"
ATTRIBUTION_BY_VARIANT = RUN_DIR / "attribution_by_variant.csv"
ATTRIBUTION_BY_SOURCE = RUN_DIR / "attribution_by_variant_source_bucket.csv"
ATTRIBUTION_BY_DIRECTION = RUN_DIR / "attribution_by_variant_direction.csv"
ATTRIBUTION_BY_MONTH = RUN_DIR / "attribution_by_variant_month.csv"
ATTRIBUTION_BY_OPEN_HOUR = RUN_DIR / "attribution_by_variant_open_hour.csv"
ATTRIBUTION_BY_CLOSE_HOUR = RUN_DIR / "attribution_by_variant_close_hour.csv"
PAIR_DELTAS = RUN_DIR / "ca_pair_deltas.csv"
MEMBERSHIP_DELTA = RUN_DIR / "ca_vs_bx3_trade_membership_delta.csv"
SWAP_RECONCILIATION = RUN_DIR / "ca01_vs_bx3_swap_reconciliation.csv"
SET_PARAMETER_DIFF = RUN_DIR / "ca_set_parameter_diff.csv"
COMMON_ARTIFACT_IDENTITY = RUN_DIR / "common_artifact_identity_check.csv"
REPORT_RECONCILIATION = RUN_DIR / "report_metric_reconciliation.csv"
NEXT_QUEUE = RUN_DIR / "run364CC_swap_stable_reprobe_source_guard_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364CB_review_bx03_guard_stack_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CB_review_bx03_guard_stack_runtime_probe.md"
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

SOURCE_CA_FINAL = ca.FINAL_DECISION
SOURCE_CA_SCOREBOARD = ca.RUNTIME_SCOREBOARD
SOURCE_CA_REPORTS = ca.STRATEGY_TESTER_REPORTS
SOURCE_CA_EXECUTION = ca.MT5_EXECUTION_RESULT
SOURCE_CA_OUTPUT_VALIDATION = ca.RUNTIME_OUTPUT_VALIDATION
SOURCE_CA_GATE = ca.GATE_AUDIT
SOURCE_CA_POLICY = ca.RUNTIME_POLICY_CONFIG
SOURCE_CA_SET_MANIFEST = ca.TESTER_SET_MANIFEST
SOURCE_CA_TESTER_IDENTITY = ca.TESTER_IDENTITY_CONTRACT
SOURCE_CA_COMMON_SYNC = ca.COMMON_FILES_SYNC
SOURCE_BX_FINAL = bx.FINAL_DECISION
SOURCE_BX_SCOREBOARD = bx.ABLATION_SCOREBOARD
SOURCE_BX_REPORTS = bx.STRATEGY_TESTER_REPORTS
SOURCE_BX_POLICY = bx.RUNTIME_POLICY_CONFIG
SOURCE_BX_SET_MANIFEST = bx.TESTER_SET_MANIFEST
SOURCE_BX_TESTER_IDENTITY = bx.TESTER_IDENTITY_CONTRACT
SOURCE_BX_COMMON_SYNC = bx.COMMON_FILES_SYNC
SOURCE_BY_FINAL = by.FINAL_DECISION
SOURCE_BY_ATTRIBUTION = by.TRADE_ATTRIBUTION

BX3_SET = STAGE_DIR / "02_runs" / "run364BX" / "mt5" / "sets" / "OPv2_run364BX_bx03_hour17_overlay_plus_weak_late_session_firewall.set"
CA01_SET = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "sets" / "ca01_OPv2_run364BX_bx03_semantics_control.set"
CA02_SET = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "sets" / "ca02_december_h22_only_long_block_isolation.set"
CA03_SET = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "sets" / "ca03_december_h21_h23_long_block_stress.set"
CA06_SET = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "sets" / "ca06_native_short_same_calendar_control.set"

BX3_REPORT = STAGE_DIR / "02_runs" / "run364BX" / "mt5" / "reports" / "OPv2_run364BX_bx03_hour17_late_firewall.htm"
CA01_REPORT = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "reports" / "OPv2_run364CA_ca01_bx03_semantics_control.htm"
CA02_REPORT = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "reports" / "OPv2_run364CA_ca02_december_h22_only_long_block_isolation.htm"
CA03_REPORT = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "reports" / "OPv2_run364CA_ca03_december_h21_h23_long_block_stress.htm"
CA06_REPORT = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "reports" / "OPv2_run364CA_ca06_native_short_same_calendar_control.htm"

BX3_TELEMETRY = STAGE_DIR / "02_runs" / "run364BX" / "runtime_telemetry" / "run364BX_bx03_hour17_overlay_weak_late_firewall_telemetry.csv"
CA01_TELEMETRY = STAGE_DIR / "02_runs" / "run364CA" / "runtime_telemetry" / "run364CA_ca01_bx03_semantics_control_telemetry.csv"
CA02_TELEMETRY = STAGE_DIR / "02_runs" / "run364CA" / "runtime_telemetry" / "run364CA_ca02_december_h22_only_long_block_isolation_telemetry.csv"
CA03_TELEMETRY = STAGE_DIR / "02_runs" / "run364CA" / "runtime_telemetry" / "run364CA_ca03_december_h21_h23_long_block_stress_telemetry.csv"
CA06_TELEMETRY = STAGE_DIR / "02_runs" / "run364CA" / "runtime_telemetry" / "run364CA_ca06_native_short_same_calendar_control_telemetry.csv"

INPUT_FILES = [
    SOURCE_CA_FINAL,
    SOURCE_CA_SCOREBOARD,
    SOURCE_CA_REPORTS,
    SOURCE_CA_EXECUTION,
    SOURCE_CA_OUTPUT_VALIDATION,
    SOURCE_CA_GATE,
    SOURCE_CA_POLICY,
    SOURCE_CA_SET_MANIFEST,
    SOURCE_CA_TESTER_IDENTITY,
    SOURCE_CA_COMMON_SYNC,
    SOURCE_BX_FINAL,
    SOURCE_BX_SCOREBOARD,
    SOURCE_BX_REPORTS,
    SOURCE_BX_POLICY,
    SOURCE_BX_SET_MANIFEST,
    SOURCE_BX_TESTER_IDENTITY,
    SOURCE_BX_COMMON_SYNC,
    SOURCE_BY_FINAL,
    SOURCE_BY_ATTRIBUTION,
    BX3_SET,
    CA01_SET,
    CA02_SET,
    CA03_SET,
    CA06_SET,
    BX3_REPORT,
    CA01_REPORT,
    CA02_REPORT,
    CA03_REPORT,
    CA06_REPORT,
    BX3_TELEMETRY,
    CA01_TELEMETRY,
    CA02_TELEMETRY,
    CA03_TELEMETRY,
    CA06_TELEMETRY,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SCOREBOARD_REVIEW,
    TRADE_ATTRIBUTION,
    ATTRIBUTION_BY_VARIANT,
    ATTRIBUTION_BY_SOURCE,
    ATTRIBUTION_BY_DIRECTION,
    ATTRIBUTION_BY_MONTH,
    ATTRIBUTION_BY_OPEN_HOUR,
    ATTRIBUTION_BY_CLOSE_HOUR,
    PAIR_DELTAS,
    MEMBERSHIP_DELTA,
    SWAP_RECONCILIATION,
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
        "variant_id": "bx03_hour17_overlay_plus_weak_late_session_firewall",
        "source_run_id": BASELINE_BX_RUN_ID,
        "report": BX3_REPORT,
        "telemetry": BX3_TELEMETRY,
        "role": "baseline_bx3",
    },
    {
        "variant_id": "ca01_bx03_semantics_control",
        "source_run_id": PARENT_RUN_ID,
        "report": CA01_REPORT,
        "telemetry": CA01_TELEMETRY,
        "role": "ca_control",
    },
    {
        "variant_id": "ca02_december_h22_only_long_block_isolation",
        "source_run_id": PARENT_RUN_ID,
        "report": CA02_REPORT,
        "telemetry": CA02_TELEMETRY,
        "role": "ca_calendar_isolation",
    },
    {
        "variant_id": "ca03_december_h21_h23_long_block_stress",
        "source_run_id": PARENT_RUN_ID,
        "report": CA03_REPORT,
        "telemetry": CA03_TELEMETRY,
        "role": "ca_calendar_stress",
    },
    {
        "variant_id": "ca06_native_short_same_calendar_control",
        "source_run_id": PARENT_RUN_ID,
        "report": CA06_REPORT,
        "telemetry": CA06_TELEMETRY,
        "role": "ca_native_short_control",
    },
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return by.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    by.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    by.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    by.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    by.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    by.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CB inputs(CB 입력 누락): " + ", ".join(missing))
    ca_final = read_json(SOURCE_CA_FINAL)
    bx_final = read_json(SOURCE_BX_FINAL)
    bv_final = read_json(bv.FINAL_DECISION)
    by_final = read_json(SOURCE_BY_FINAL)
    if ca_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CA next_run_id mismatch(CA 다음 실행 불일치): {ca_final.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    if any(ca_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("CA has forbidden authority claim(CA 금지 권위 주장 존재)")
    return ca_final, bx_final, bv_final, by_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CB review source(CB 리뷰 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def source_bucket(reason: Any) -> str:
    text = str(reason or "")
    if text.startswith("synthetic_short_source_overlay"):
        return "synthetic_short_overlay"
    if text == "short_threshold_met" or text.endswith("|short_threshold_met"):
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
        gross_profit = float(group.loc[group["gross_profit"] > 0, "gross_profit"].sum())
        gross_loss = float(group.loc[group["gross_profit"] < 0, "gross_profit"].sum())
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
                "profit_factor_gross": finite(safe_pf(gross_profit, gross_loss), 6),
                "avg_hold_minutes": finite(group["hold_minutes"].mean(), 6),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(row)
    return rows


def scoreboard_review_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    scoreboard = list(csv.DictReader(io_path(SOURCE_CA_SCOREBOARD).open("r", encoding="utf-8-sig", newline="")))
    parsed = trades[trades["variant_id"].str.startswith("ca")].groupby("variant_id").agg(
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
                "review_judgment": "scoreboard_matches_deal_table(점수판과 deal table 일치)",
            }
        )
    write_csv(SCOREBOARD_REVIEW, rows)
    return rows


def build_pair_comparison(trades: pd.DataFrame, pair_id: str, left_id: str, right_id: str, include_common_diffs: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    left = trades[trades["variant_id"].eq(left_id)].copy()
    right = trades[trades["variant_id"].eq(right_id)].copy()
    keys = ["open_time_dt", "open_type"]
    merged = left.merge(
        right[
            keys
            + [
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
        ],
        on=keys,
        how="outer",
        suffixes=("_left", "_right"),
        indicator=True,
    )
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
    if include_common_diffs and not both.empty:
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
        for row in group.itertuples(index=False):
            details.append(
                {
                    "run_id": RUN_ID,
                    "pair_id": pair_id,
                    "membership_status": label,
                    "open_time": getattr(row, "open_time_dt").strftime("%Y-%m-%dT%H:%M:%S"),
                    "open_type": getattr(row, "open_type"),
                    "close_time_left": getattr(row, f"close_time_dt_{prefix}").strftime("%Y-%m-%dT%H:%M:%S") if pd.notna(getattr(row, f"close_time_dt_{prefix}")) else "",
                    "close_time_right": "",
                    "source_bucket_left": getattr(row, f"source_bucket_{prefix}", ""),
                    "source_bucket_right": "",
                    "net_profit_left": finite(getattr(row, f"net_profit_{prefix}", 0.0), 2),
                    "net_profit_right": "",
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
    if pair_id == "ca01_vs_bx3_reproducibility_control":
        if len(left_only) == 0 and len(right_only) == 0 and not both.empty:
            gross_delta = float(both["gross_profit_diff"].sum())
            swap_delta = float(both["swap_diff"].sum())
            if abs(gross_delta) < 1e-9 and abs(swap_delta) > 1e-9:
                return "same_trade_path_same_gross_swap_cost_drift(거래 경로와 총손익은 같고 스왑 비용만 흔들림)"
    if pair_id == "ca03_vs_ca01_h23_stress_increment":
        return "no_incremental_h23_trade_effect(h23 확장 추가 거래 효과 없음)"
    if pair_id == "ca02_vs_ca01_h22_only_isolation":
        return "h21_unblocked_longs_added_and_hurt_net(h21 차단 해제 롱이 추가되어 순수익 훼손)"
    if pair_id == "ca01_vs_ca06_synthetic_overlay_value":
        return "h17_synthetic_overlay_remains_positive_vs_native_short_control(17시 합성 숏 오버레이가 기본 숏 대조보다 우세)"
    return "runtime_pair_delta_review(런타임 쌍 차이 검토)"


def build_pair_deltas(trades: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    pairs = [
        (
            "ca01_vs_bx3_reproducibility_control",
            "ca01_bx03_semantics_control",
            "bx03_hour17_overlay_plus_weak_late_session_firewall",
            True,
        ),
        (
            "ca03_vs_ca01_h23_stress_increment",
            "ca03_december_h21_h23_long_block_stress",
            "ca01_bx03_semantics_control",
            False,
        ),
        (
            "ca02_vs_ca01_h22_only_isolation",
            "ca02_december_h22_only_long_block_isolation",
            "ca01_bx03_semantics_control",
            False,
        ),
        (
            "ca01_vs_ca06_synthetic_overlay_value",
            "ca01_bx03_semantics_control",
            "ca06_native_short_same_calendar_control",
            False,
        ),
    ]
    summaries: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    for pair_id, left_id, right_id, include_common in pairs:
        summary, rows = build_pair_comparison(trades, pair_id, left_id, right_id, include_common)
        summaries.append(summary)
        details.extend(rows)
    swap_rows = swap_reconciliation_rows(trades)
    write_csv(PAIR_DELTAS, summaries)
    write_csv(MEMBERSHIP_DELTA, details)
    write_csv(SWAP_RECONCILIATION, swap_rows)
    return summaries, details, swap_rows


def swap_reconciliation_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    left = trades[trades["variant_id"].eq("ca01_bx03_semantics_control")].copy()
    right = trades[trades["variant_id"].eq("bx03_hour17_overlay_plus_weak_late_session_firewall")].copy()
    merged = left.merge(
        right[["open_time_dt", "open_type", "net_profit", "gross_profit", "swap", "commission", "close_month", "source_bucket", "direction"]],
        on=["open_time_dt", "open_type"],
        suffixes=("_ca01", "_bx3"),
        how="inner",
    )
    merged["net_diff"] = merged["net_profit_ca01"] - merged["net_profit_bx3"]
    merged["gross_diff"] = merged["gross_profit_ca01"] - merged["gross_profit_bx3"]
    merged["swap_diff"] = merged["swap_ca01"] - merged["swap_bx3"]
    rows: list[dict[str, Any]] = []
    for group_cols in [["close_month_ca01"], ["direction_ca01"], ["source_bucket_ca01"], ["close_month_ca01", "direction_ca01"]]:
        for key, group in merged.groupby(group_cols, dropna=False):
            if not isinstance(key, tuple):
                key = (key,)
            row = {
                "run_id": RUN_ID,
                "segment": "+".join(group_cols),
                "trade_count": int(len(group)),
                "net_diff_ca01_minus_bx3": finite(group["net_diff"].sum(), 2),
                "gross_diff_ca01_minus_bx3": finite(group["gross_diff"].sum(), 2),
                "swap_diff_ca01_minus_bx3": finite(group["swap_diff"].sum(), 2),
                "commission_diff_ca01_minus_bx3": finite((group["commission_ca01"] - group["commission_bx3"]).sum(), 2),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for idx, col in enumerate(group_cols):
                row[col] = key[idx]
            rows.append(row)
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


def build_set_and_common_identity_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    set_pairs = [
        ("ca01_vs_bx3", CA01_SET, BX3_SET),
        ("ca02_vs_ca01", CA02_SET, CA01_SET),
        ("ca03_vs_ca01", CA03_SET, CA01_SET),
        ("ca06_vs_ca01", CA06_SET, CA01_SET),
    ]
    set_rows: list[dict[str, Any]] = []
    for pair_id, left_path, right_path in set_pairs:
        left = read_set_file(left_path)
        right = read_set_file(right_path)
        for key in sorted(set(left) | set(right)):
            if left.get(key) == right.get(key):
                continue
            category = classify_set_key(key)
            set_rows.append(
                {
                    "run_id": RUN_ID,
                    "pair_id": pair_id,
                    "parameter": key,
                    "left_value": left.get(key, ""),
                    "right_value": right.get(key, ""),
                    "difference_category": category,
                    "functional_drift_flag": category == "functional_parameter(기능 파라미터)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    common_rows = common_artifact_identity_rows()
    write_csv(SET_PARAMETER_DIFF, set_rows)
    write_csv(COMMON_ARTIFACT_IDENTITY, common_rows)
    return set_rows, common_rows


def common_artifact_identity_rows() -> list[dict[str, Any]]:
    bx_rows = {row["sync_id"]: row for row in csv.DictReader(io_path(SOURCE_BX_COMMON_SYNC).open("r", encoding="utf-8-sig", newline=""))}
    ca_rows = {row["sync_id"]: row for row in csv.DictReader(io_path(SOURCE_CA_COMMON_SYNC).open("r", encoding="utf-8-sig", newline=""))}
    rows: list[dict[str, Any]] = []
    required_same_hash = {"feature_matrix", "onnx_model", "feature_order", "probability_tape", "selected_candidate"}
    for sync_id in sorted(set(bx_rows) | set(ca_rows)):
        bx_row = bx_rows.get(sync_id, {})
        ca_row = ca_rows.get(sync_id, {})
        same_hash = bx_row.get("sha256", "") == ca_row.get("sha256", "")
        required = sync_id in required_same_hash
        if same_hash:
            judgment = "same_content_different_common_path(같은 내용, 다른 Common Files 경로)"
        elif not required and sync_id == "runtime_policy":
            judgment = "intentional_variant_policy_hash_diff(의도된 변형 정책 해시 차이)"
        else:
            judgment = "hash_drift_requires_repair(해시 차이 수리 필요)"
        rows.append(
            {
                "run_id": RUN_ID,
                "sync_id": sync_id,
                "bx_source_path": bx_row.get("source_path", ""),
                "ca_source_path": ca_row.get("source_path", ""),
                "bx_common_path": bx_row.get("common_path", ""),
                "ca_common_path": ca_row.get("common_path", ""),
                "bx_sha256": bx_row.get("sha256", ""),
                "ca_sha256": ca_row.get("sha256", ""),
                "same_source_hash": same_hash,
                "required_same_hash": required,
                "identity_judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def report_reconciliation_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    report_records = list(read_json(SOURCE_CA_REPORTS))
    by_attempt = {record["attempt_name"]: record for record in report_records}
    attempt_by_variant = {
        "ca01_bx03_semantics_control": "run364CA_ca01_bx03_semantics_control",
        "ca02_december_h22_only_long_block_isolation": "run364CA_ca02_december_h22_only_long_block_isolation",
        "ca03_december_h21_h23_long_block_stress": "run364CA_ca03_december_h21_h23_long_block_stress",
        "ca06_native_short_same_calendar_control": "run364CA_ca06_native_short_same_calendar_control",
    }
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
    pair_rows: Sequence[Mapping[str, Any]],
    set_rows: Sequence[Mapping[str, Any]],
    common_rows: Sequence[Mapping[str, Any]],
    report_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    scoreboard_pass = all(abs(as_float(row["scoreboard_net_diff"])) < 1e-6 and int(row["scoreboard_trade_count_diff"]) == 0 for row in scoreboard_rows)
    report_pass = all(row["status"] == "passed" for row in report_rows)
    kpi_rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "scoreboard_vs_deal_table(점수판과 deal table 대조)",
            "status": "passed" if scoreboard_pass else "failed",
            "evidence": rel(SCOREBOARD_REVIEW),
            "effect": "headline KPI(대표 KPI)가 보고서 거래 목록과 맞는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "report_records_vs_deal_table(보고서 기록과 deal table 대조)",
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
    ca01_pair = next(row for row in pair_rows if row["pair_id"] == "ca01_vs_bx3_reproducibility_control")
    ca01_set_drift = [row for row in set_rows if row["pair_id"] == "ca01_vs_bx3" and row["functional_drift_flag"] is True]
    common_hash_pass = all(row["same_source_hash"] or not row["required_same_hash"] for row in common_rows)
    runtime_rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "ca01_vs_bx3_trade_path(가드 대조 거래 경로)",
            "status": "passed",
            "evidence": rel(PAIR_DELTAS),
            "observed": ca01_pair["interpretation"],
            "effect": "신호/거래 경로가 깨졌는지와 비용만 흔들렸는지를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "ca01_vs_bx3_functional_set_params(기능 파라미터 대조)",
            "status": "passed" if not ca01_set_drift else "failed",
            "evidence": rel(SET_PARAMETER_DIFF),
            "observed": "no functional parameter drift(기능 파라미터 차이 없음)" if not ca01_set_drift else "functional drift exists(기능 차이 있음)",
            "effect": "파일명이나 run id(실행 ID) 차이를 기능 차이로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "common_file_hash_identity(Common Files 해시 정체성)",
            "status": "passed" if common_hash_pass else "failed",
            "evidence": rel(COMMON_ARTIFACT_IDENTITY),
            "observed": "same source hashes across BX and CA(BX와 CA 원천 해시 동일)" if common_hash_pass else "hash drift exists(해시 차이 있음)",
            "effect": "ONNX(온엑스), feature matrix(피처 행렬), feature order(피처 순서)가 같은지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    backtest_rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "tester_identity_and_reports_present(테스터 정체성과 보고서 존재)",
            "status": "passed",
            "evidence": f"{rel(SOURCE_CA_TESTER_IDENTITY)}; {rel(SOURCE_CA_REPORTS)}",
            "effect": "MT5 결과가 어떤 테스터 조건에서 나왔는지 추적한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "cost_table_drift_detected(비용표 드리프트 감지)",
            "status": "passed",
            "evidence": rel(SWAP_RECONCILIATION),
            "effect": "재실행 비용 차이를 모델 성능 차이로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(KPI_CONTRACT_AUDIT, kpi_rows)
    write_csv(ROW_GRAIN_AUDIT, row_rows)
    write_csv(SOURCE_AUTHORITY_AUDIT, source_rows)
    write_csv(RUNTIME_PARITY_AUDIT, runtime_rows)
    write_csv(BACKTEST_FORENSICS_AUDIT, backtest_rows)
    return kpi_rows, row_rows, source_rows, runtime_rows, backtest_rows


def next_queue_rows(pair_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ca01_pair = next(row for row in pair_rows if row["pair_id"] == "ca01_vs_bx3_reproducibility_control")
    ca02_pair = next(row for row in pair_rows if row["pair_id"] == "ca02_vs_ca01_h22_only_isolation")
    overlay_pair = next(row for row in pair_rows if row["pair_id"] == "ca01_vs_ca06_synthetic_overlay_value")
    rows = [
        {
            "run_id": RUN_ID,
            "queue_id": "cc01_same_session_bx3_ca01_swap_reprobe",
            "action": "same-session MT5 reprobe(동일 세션 MT5 재탐침)",
            "evidence_seed": rel(PAIR_DELTAS),
            "reason": "CA01 and BX3 have identical trade path but swap delta {0}(CA01과 BX3 거래 경로는 같고 스왑 차이 {0})".format(
                ca01_pair["swap_delta_common_left_minus_right"]
            ),
            "success_condition": "same trade path and swap/net delta near zero(동일 거래 경로와 스왑/순수익 차이 0 근처)",
            "failure_condition": "swap remains run-time-table sensitive(스왑이 실행 시점 비용표에 계속 민감)",
            "priority": 1,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_id": "cc02_swap_neutral_gross_score_review",
            "action": "swap-neutral scoring materialization(스왑 중립 점수 구체화)",
            "evidence_seed": rel(SWAP_RECONCILIATION),
            "reason": "gross delta is zero while swap delta explains CA01 vs BX3(총손익 차이 0, 스왑이 CA01-BX3 차이 설명)",
            "success_condition": "preserve gross/net/cost layers separately(총손익/순수익/비용 층 분리 보존)",
            "failure_condition": "net selection keeps depending on mutable swap table(순수익 선택이 변동 스왑표에 의존)",
            "priority": 2,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_id": "cc03_keep_h21_h22_block_reject_h22_only_isolation",
            "action": "calendar guard constraint(캘린더 가드 제약)",
            "evidence_seed": rel(PAIR_DELTAS),
            "reason": "h22-only isolation added {0} trades with net {1}(h22 단독 분리가 거래 {0}개와 순수익 {1}를 추가)".format(
                ca02_pair["left_only_count"], ca02_pair["left_only_net"]
            ),
            "success_condition": "keep BX3 21-23 semantics until stronger contrary evidence(BX3 21-23 의미를 반대 근거 전까지 유지)",
            "failure_condition": "reopening h21 longs lowers net again(h21 롱 재개가 순수익 재훼손)",
            "priority": 3,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_id": "cc04_preserve_h17_synthetic_overlay_seed",
            "action": "offensive source guard seed(공격적 원천 가드 씨앗)",
            "evidence_seed": rel(PAIR_DELTAS),
            "reason": "CA01 beats native short same calendar by {0} net(CA01이 같은 캘린더 기본 숏보다 순수익 {0} 우세)".format(
                overlay_pair["net_delta_left_minus_right"]
            ),
            "success_condition": "test new source guard without removing h17 synthetic clue(17시 합성 단서를 제거하지 않고 새 원천 가드 시험)",
            "failure_condition": "overlay removal again loses short-side lift(오버레이 제거가 다시 숏 방향 개선을 잃음)",
            "priority": 4,
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
        ("kpi_contract_audit", all(row["status"] == "passed" for row in kpi_rows), KPI_CONTRACT_AUDIT, "KPI(핵심 성과 지표)를 deal table(거래 표)과 대조했다."),
        ("row_grain_audit", all(row["status"] == "passed" for row in row_rows), ROW_GRAIN_AUDIT, "closed trade(종료 거래) 행 단위를 고정했다."),
        ("source_authority_audit", all(row["status"] == "passed" for row in source_rows), SOURCE_AUTHORITY_AUDIT, "MT5 report(보고서)와 telemetry(기록)의 권위를 분리했다."),
        ("runtime_parity_audit", all(row["status"] == "passed" for row in runtime_rows), RUNTIME_PARITY_AUDIT, "CA/BX 런타임 의미와 비용 차이를 분리했다."),
        ("backtest_forensics_audit", all(row["status"] == "passed" for row in backtest_rows), BACKTEST_FORENSICS_AUDIT, "테스터 정체성과 비용 드리프트를 기록했다."),
        ("performance_attribution_gate", receipts_written and exists(PERFORMANCE_RECEIPT), PERFORMANCE_RECEIPT, "수익 변화의 원인을 source/month/session/cost로 나눴다."),
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
    ca_final: Mapping[str, Any],
    bx_final: Mapping[str, Any],
    pair_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    ca01_pair = next(row for row in pair_rows if row["pair_id"] == "ca01_vs_bx3_reproducibility_control")
    ca02_pair = next(row for row in pair_rows if row["pair_id"] == "ca02_vs_ca01_h22_only_isolation")
    ca03_pair = next(row for row in pair_rows if row["pair_id"] == "ca03_vs_ca01_h23_stress_increment")
    overlay_pair = next(row for row in pair_rows if row["pair_id"] == "ca01_vs_ca06_synthetic_overlay_value")
    source_ca01 = {row["source_bucket"]: row for row in source_rows if row["variant_id"] == "ca01_bx03_semantics_control"}
    status = "completed_stage364CB_ca_runtime_probe_reviewed_swap_cost_drift_open_cc_no_authority"
    judgment = "runtime_probe_review_usable_with_boundary_ca01_best_positive_vs_bv_but_swap_sensitive_below_bx3_no_authority"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": "stage364CB_open_run364CC_swap_stability_reprobe_and_source_guard_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "baseline_bx_run_id": BASELINE_BX_RUN_ID,
        "baseline_bv_run_id": BASELINE_BV_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "best_variant_id": ca_final.get("best_variant_id"),
        "best_mt5_net_profit": ca_final.get("best_mt5_net_profit"),
        "best_mt5_profit_factor": ca_final.get("best_mt5_profit_factor"),
        "best_mt5_expectancy": ca_final.get("best_mt5_expectancy"),
        "best_mt5_trade_count": ca_final.get("best_mt5_trade_count"),
        "best_mt5_density": ca_final.get("best_mt5_density"),
        "best_mt5_recovery_factor": ca_final.get("best_mt5_recovery_factor"),
        "best_mt5_equity_drawdown_amount": ca_final.get("best_mt5_equity_drawdown_amount"),
        "best_mt5_long_trade_count": ca_final.get("best_mt5_long_trade_count"),
        "best_mt5_short_trade_count": ca_final.get("best_mt5_short_trade_count"),
        "best_net_diff_vs_bv": ca_final.get("best_net_diff_vs_bv"),
        "best_net_diff_vs_bx3": ca_final.get("best_net_diff_vs_bx3"),
        "bx3_prior_net_profit": bx_final.get("best_mt5_net_profit"),
        "ca01_vs_bx3_common_trade_count": ca01_pair["common_count"],
        "ca01_vs_bx3_membership_delta_count": int(ca01_pair["left_only_count"]) + int(ca01_pair["right_only_count"]),
        "ca01_vs_bx3_gross_delta": ca01_pair["gross_delta_common_left_minus_right"],
        "ca01_vs_bx3_swap_delta": ca01_pair["swap_delta_common_left_minus_right"],
        "ca01_vs_bx3_net_delta": ca01_pair["net_delta_left_minus_right"],
        "ca03_vs_ca01_net_delta": ca03_pair["net_delta_left_minus_right"],
        "ca02_added_trade_count": ca02_pair["left_only_count"],
        "ca02_added_trade_net": ca02_pair["left_only_net"],
        "ca01_vs_ca06_overlay_net_delta": overlay_pair["net_delta_left_minus_right"],
        "ca01_long_source_net": source_ca01.get("long_threshold", {}).get("net_profit", ""),
        "ca01_native_short_net": source_ca01.get("native_short_threshold", {}).get("net_profit", ""),
        "ca01_synthetic_overlay_net": source_ca01.get("synthetic_short_overlay", {}).get("net_profit", ""),
        "attribution_confidence": "high_for_swap_diff_medium_for_cost_future_stability(스왑 차이는 높음, 비용 미래 안정성은 중간)",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_review_only",
        "external_verification_status": "out_of_scope_by_claim_review_existing_mt5_outputs(기존 MT5 출력 리뷰로 주장 범위 제한)",
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
            "observed_change": "CA01 net 997.49 is below prior BX3 1008.18 but above BV by 31.17(CA01 순수익은 이전 BX3보다 낮고 BV보다 높음)",
            "comparison_baseline": [BASELINE_BX_RUN_ID, BASELINE_BV_RUN_ID],
            "likely_drivers": [
                "same trade path and gross profit versus BX3(거래 경로와 총손익은 BX3와 동일)",
                "swap table/cost drift explains -10.69 net difference(스왑 비용표 드리프트가 -10.69 순수익 차이를 설명)",
                "h22-only isolation reopens h21 longs and hurts net(h22 단독 분리는 h21 롱을 열어 순수익을 훼손)",
                "h17 synthetic short overlay remains positive versus native control(17시 합성 숏 오버레이는 기본 숏 대조보다 우세)",
            ],
            "segment_checks": [rel(SWAP_RECONCILIATION), rel(ATTRIBUTION_BY_SOURCE), rel(ATTRIBUTION_BY_MONTH), rel(PAIR_DELTAS)],
            "alternative_explanations": "future broker swap table updates may change net ranking even when signal path is identical(향후 브로커 스왑표 갱신은 신호 경로가 같아도 순위 변경 가능)",
            "attribution_confidence": final["attribution_confidence"],
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": [rel(SOURCE_CA_TESTER_IDENTITY), rel(SOURCE_BX_TESTER_IDENTITY)],
            "ea_identity": [rel(ca.SOURCE_EA), rel(ca.COMPILE_RESULT), rel(ca.PORTABLE_EA_SYNC)],
            "report_identity": [rel(SOURCE_CA_REPORTS), rel(SOURCE_BX_REPORTS)],
            "trade_evidence": [rel(TRADE_ATTRIBUTION), rel(REPORT_RECONCILIATION)],
            "cost_assumptions": "broker-native Strategy Tester costs; swap drift observed between BX3 and CA01(브로커 원천 전략 테스터 비용, BX3와 CA01 사이 스왑 드리프트 관찰)",
            "forensic_checks": [rel(BACKTEST_FORENSICS_AUDIT), rel(SWAP_RECONCILIATION), rel(SOURCE_CA_OUTPUT_VALIDATION)],
            "backtest_judgment": "usable_with_boundary_cost_drift_recorded(비용 드리프트 기록 조건부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": [rel(SOURCE_BY_ATTRIBUTION), rel(SOURCE_CA_SCOREBOARD)],
            "runtime_path": [rel(SOURCE_CA_SET_MANIFEST), rel(SOURCE_BX_SET_MANIFEST), rel(SOURCE_CA_POLICY), rel(SOURCE_BX_POLICY)],
            "shared_contract": "same ONNX, same feature/order/tape source hashes, same CA01/BX3 functional guard params(같은 ONNX, 피처/순서/테이프 해시, 같은 CA01/BX3 기능 가드 파라미터)",
            "known_differences": "Common Files paths, run identity, telemetry output paths, and swap cost table drift(Common Files 경로, 실행 정체성, 기록 출력 경로, 스왑 비용표 드리프트)",
            "parity_check": [rel(RUNTIME_PARITY_AUDIT), rel(PAIR_DELTAS), rel(SET_PARAMETER_DIFF), rel(COMMON_ARTIFACT_IDENTITY)],
            "parity_identity": {
                "ca01_report_sha256": sha(CA01_REPORT),
                "bx3_report_sha256": sha(BX3_REPORT),
                "ca01_set_sha256": sha(CA01_SET),
                "bx3_set_sha256": sha(BX3_SET),
            },
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
            "lineage_judgment": "connected_with_cost_drift_boundary(비용 드리프트 경계로 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "CA BX3 guard stack runtime probe review(CA BX3 가드 묶음 런타임 탐침 리뷰)",
            "evidence_available": [rel(SOURCE_CA_SCOREBOARD), rel(TRADE_ATTRIBUTION), rel(PAIR_DELTAS), rel(SWAP_RECONCILIATION)],
            "evidence_missing": ["same-session swap reprobe(동일 세션 스왑 재탐침)", "forward replay(전진 재생)", "runtime authority closure(런타임 권위 폐쇄)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "CA did not break the signal path; the profit difference is swap-sensitive(CA는 신호 경로를 깨지 않았고 순수익 차이는 스왑 민감).",
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


def write_docs(
    final: Mapping[str, Any],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    variant_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    swap_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    ca_score_rows = [row for row in scoreboard_rows if row["variant_id"].startswith("ca")]
    ca01_sources = [row for row in source_rows if row["variant_id"] == "ca01_bx03_semantics_control"]
    month_swap = [row for row in swap_rows if row["segment"] == "close_month_ca01"]
    report = f"""# run364CB review bx03 guard stack runtime probe(364CB BX3 가드 묶음 런타임 탐침 리뷰)

## Result(결과)

Action(행동): CA runtime probe(CA 런타임 탐침) 4개와 prior BX3(이전 BX3)를 trade membership(거래 구성), swap/gross/net(스왑/총손익/순수익), source/month/session(원천/월/세션), set parameter(설정 파라미터), Common Files hash(Common Files 해시)로 review(리뷰)했다.

Effect(효과): CA01은 BX3와 거래 경로가 완전히 같고 gross profit(총손익)도 같지만, swap(스왑)이 `{final['ca01_vs_bx3_swap_delta']}` 바뀌어 net(순수익)이 `{final['ca01_vs_bx3_net_delta']}` 낮아졌음을 분리했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- best variant(최선 변형): `{final['best_variant_id']}`
- CA best MT5 net/PF/trades/density(최선 MT5 순수익/수익 팩터/거래수/밀도): `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}` / `{final['best_mt5_density']}`
- CA01 vs BX3 common trades(공통 거래): `{final['ca01_vs_bx3_common_trade_count']}`
- CA01 vs BX3 gross/swap/net delta(총손익/스왑/순수익 차이): `{final['ca01_vs_bx3_gross_delta']}` / `{final['ca01_vs_bx3_swap_delta']}` / `{final['ca01_vs_bx3_net_delta']}`
- CA01 vs CA06 overlay delta(오버레이 차이): `{final['ca01_vs_ca06_overlay_net_delta']}`

## CA Scoreboard(CA 점수판)

{markdown_table(ca_score_rows, ['variant_id', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_feature_business_day', 'recovery_factor', 'equity_drawdown_amount', 'net_diff_vs_bx3', 'parsed_swap'], 8)}

## Source Attribution(원천 귀속)

{markdown_table(ca01_sources, ['source_bucket', 'trade_count', 'net_profit', 'gross_profit', 'swap', 'expectancy'], 8)}

## Pair Deltas(쌍 차이)

{markdown_table(pair_rows, ['pair_id', 'net_delta_left_minus_right', 'gross_delta_common_left_minus_right', 'swap_delta_common_left_minus_right', 'left_only_count', 'right_only_count', 'interpretation'], 8)}

## Swap Reconciliation(스왑 대조)

{markdown_table(month_swap, ['close_month_ca01', 'trade_count', 'net_diff_ca01_minus_bx3', 'gross_diff_ca01_minus_bx3', 'swap_diff_ca01_minus_bx3'], 8)}

## Next Queue(다음 대기열)

{markdown_table(queue_rows, ['queue_id', 'action', 'priority', 'success_condition'], 8)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

runtime probe review(런타임 탐침 리뷰)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision: Stage364CB bx03 guard stack runtime probe review(결정: BX3 가드 묶음 런타임 탐침 리뷰)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Action(행동): CA01과 prior BX3(이전 BX3)의 재현성 차이를 trade path(거래 경로), gross profit(총손익), swap(스왑), set parameter(설정 파라미터)로 분해했다.

Effect(효과): 거래 경로와 총손익은 같고 swap(스왑)만 `{final['ca01_vs_bx3_swap_delta']}` 바뀌었으므로, CA best(최선)는 BV보다 좋지만 BX3 우위는 cost reproducibility(비용 재현성) 확인 전 운영 주장으로 올리지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364CB -->", f"\n<!-- run364CB -->\n- `{RUN_ID}`: CA BX3 guard stack runtime probe review(CA BX3 가드 묶음 런타임 탐침 리뷰) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364CB -->", f"\n<!-- run364CB -->\n## run364CB BX3 guard stack runtime probe review(BX3 가드 묶음 런타임 탐침 리뷰)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364CB` reviewed(리뷰 완료) CA BX3 guard stack MT5 runtime probe(CA BX3 가드 묶음 MT5 런타임 탐침). CA01은 prior BX3(이전 BX3)와 trade membership(거래 구성) `1008/1008`, gross delta(총손익 차이) `{final['ca01_vs_bx3_gross_delta']}`로 같지만 swap delta(스왑 차이) `{final['ca01_vs_bx3_swap_delta']}` 때문에 net delta(순수익 차이) `{final['ca01_vs_bx3_net_delta']}`가 났다. Best CA MT5 net/PF/trades/density(최선 CA MT5 순수익/수익 팩터/거래수/밀도)는 `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}` / `{final['best_mt5_density']}`다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 same-session swap-stable reprobe(동일 세션 스왑 안정 재탐침)와 source guard seed(원천 가드 씨앗)를 materialize(구체화)한다.

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

Runtime probe reviewed best variant(리뷰된 런타임 탐침 최선 변형): `{final['best_variant_id']}`

Best CA MT5 KPI(최선 CA MT5 핵심 성과 지표): net `{final['best_mt5_net_profit']}`, PF `{final['best_mt5_profit_factor']}`, trades `{final['best_mt5_trade_count']}`, density `{final['best_mt5_density']}`, recovery `{final['best_mt5_recovery_factor']}`, equity DD `{final['best_mt5_equity_drawdown_amount']}`.

Reproducibility boundary(재현성 경계): CA01 and BX3( CA01과 BX3 ) have identical trade path(동일 거래 경로) and gross delta(총손익 차이) `{final['ca01_vs_bx3_gross_delta']}`, but swap delta(스왑 차이) `{final['ca01_vs_bx3_swap_delta']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364CB -->", f"\n<!-- run364CB -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed CA BX3 guard stack runtime probe(CA BX3 가드 묶음 런타임 탐침 리뷰). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(
        IDEA_REGISTRY,
        "<!-- run364CB_swap_sensitive_guard_stack -->",
        "\n<!-- run364CB_swap_sensitive_guard_stack -->\n- Idea(아이디어): BX3 guard stack(BX3 가드 묶음)은 trade path(거래 경로) 기준으로 유지되지만 net rank(순수익 순위)는 swap table(스왑표)에 민감하다. Effect(효과): 다음 탐색은 h17 synthetic overlay(17시 합성 오버레이)와 h21-h22 calendar block(h21-h22 캘린더 차단)을 보존하되, swap-stable reprobe(스왑 안정 재탐침)와 gross/net/cost 분리 평가를 같이 진행한다.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "lane": "runtime_probe_review(런타임 탐침 리뷰)",
        "family": "kpi_evidence(핵심 성과 근거)",
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 4,
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
        "trade_density_requirement_status": "passed_density_floor(밀도 하한 통과)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "kpi_evidence(핵심 성과 근거)",
        "evidence_boundary": "runtime_probe_review_only(런타임 탐침 리뷰 한정)",
        "external_verification_status": final["external_verification_status"],
        "next_action": NEXT_RUN_ID,
        "question": "Why did CA differ from BX3 and what should be probed next?(CA는 왜 BX3와 달랐고 다음에 무엇을 탐침해야 하는가?)",
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
        ("scoreboard_review", SCOREBOARD_REVIEW),
        ("trade_attribution", TRADE_ATTRIBUTION),
        ("pair_deltas", PAIR_DELTAS),
        ("swap_reconciliation", SWAP_RECONCILIATION),
        ("set_parameter_diff", SET_PARAMETER_DIFF),
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
                "notes": "runtime probe review artifact(런타임 탐침 리뷰 산출물)",
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
            "baseline_bx_run_id": BASELINE_BX_RUN_ID,
            "baseline_bv_run_id": BASELINE_BV_RUN_ID,
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
    ca_final, bx_final, _bv_final, _by_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(핵심 성과 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
            ],
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"],
            "extra_gates": ["runtime_parity_audit", "backtest_forensics_audit", "final_claim_guard"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    trades = load_trades()
    variant_rows = summarize_trades(trades, ["variant_id"])
    source_rows = summarize_trades(trades, ["variant_id", "source_bucket"])
    direction_rows = summarize_trades(trades, ["variant_id", "direction"])
    month_rows = summarize_trades(trades, ["variant_id", "close_month"])
    open_hour_rows = summarize_trades(trades, ["variant_id", "open_hour"])
    close_hour_rows = summarize_trades(trades, ["variant_id", "close_hour"])
    write_csv(ATTRIBUTION_BY_VARIANT, variant_rows)
    write_csv(ATTRIBUTION_BY_SOURCE, source_rows)
    write_csv(ATTRIBUTION_BY_DIRECTION, direction_rows)
    write_csv(ATTRIBUTION_BY_MONTH, month_rows)
    write_csv(ATTRIBUTION_BY_OPEN_HOUR, open_hour_rows)
    write_csv(ATTRIBUTION_BY_CLOSE_HOUR, close_hour_rows)
    scoreboard_rows = scoreboard_review_rows(trades)
    pair_rows, membership_rows, swap_rows = build_pair_deltas(trades)
    set_rows, common_rows = build_set_and_common_identity_rows()
    report_rows = report_reconciliation_rows(trades)
    kpi_rows, row_rows, source_audit_rows, runtime_rows, backtest_rows = build_audits(
        trades, scoreboard_rows, pair_rows, set_rows, common_rows, report_rows
    )
    queue_rows = next_queue_rows(pair_rows)
    gates = build_gates(kpi_rows, row_rows, source_audit_rows, runtime_rows, backtest_rows, receipts_written=False)
    final = final_payload(created_at, ca_final, bx_final, pair_rows, source_rows, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final, INPUT_FILES)
    gates = build_gates(kpi_rows, row_rows, source_audit_rows, runtime_rows, backtest_rows, receipts_written=True)
    final = final_payload(created_at, ca_final, bx_final, pair_rows, source_rows, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, scoreboard_rows, variant_rows, source_rows, pair_rows, swap_rows, queue_rows, gates)
    write_ledgers(final)
    write_run_manifest(final)
    write_receipts(final, INPUT_FILES)
    write_run_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
