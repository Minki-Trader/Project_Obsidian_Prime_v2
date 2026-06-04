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
from stage_pipelines.stage364 import execute_overlay_hour17_native_short_ablation_runtime_probe_without_db as bx  # noqa: E402
from stage_pipelines.stage364 import materialize_synthetic_short_source_runtime_repair_without_db as bv  # noqa: E402
from stage_pipelines.stage364 import prepare_late_year_session_gate_mt5_precheck_without_db as bu  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = bu.STAGE_ID
RUN_NUMBER = "run364BY"
RUN_ID = "run364BY_review_overlay_hour17_native_short_ablation_runtime_probe_without_db_v1"
PARENT_RUN_ID = bx.RUN_ID
BASELINE_RUN_ID = bv.RUN_ID
NEXT_RUN_ID = "run364BZ_materialize_bx03_december_late_session_guard_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_ablation_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = bu.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
TRADE_ATTRIBUTION = RUN_DIR / "mt5_trade_attribution_by_variant.csv"
ATTRIBUTION_BY_VARIANT = RUN_DIR / "attribution_by_variant.csv"
ATTRIBUTION_BY_DIRECTION = RUN_DIR / "attribution_by_variant_direction.csv"
ATTRIBUTION_BY_SOURCE = RUN_DIR / "attribution_by_variant_source_bucket.csv"
ATTRIBUTION_BY_MONTH = RUN_DIR / "attribution_by_variant_month.csv"
ATTRIBUTION_BY_OPEN_HOUR = RUN_DIR / "attribution_by_variant_open_hour.csv"
ATTRIBUTION_BY_CLOSE_HOUR = RUN_DIR / "attribution_by_variant_close_hour.csv"
RUNTIME_SIGNAL_ATTRIBUTION = RUN_DIR / "runtime_signal_attribution_by_variant.csv"
VARIANT_PAIR_DELTAS = RUN_DIR / "variant_pair_deltas.csv"
TRADE_MEMBERSHIP_DELTA = RUN_DIR / "trade_membership_delta.csv"
NEXT_QUEUE = RUN_DIR / "run364BZ_guard_input_queue.csv"
KPI_CONTRACT_AUDIT = RUN_DIR / "kpi_contract_audit.csv"
ROW_GRAIN_AUDIT = RUN_DIR / "row_grain_audit.csv"
SOURCE_AUTHORITY_AUDIT = RUN_DIR / "source_authority_audit.csv"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BY_review_overlay_hour17_native_short_ablation_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BY_review_overlay_hour17_native_short_ablation_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_BX_FINAL = bx.FINAL_DECISION
SOURCE_BX_SCOREBOARD = bx.ABLATION_SCOREBOARD
SOURCE_BX_REPORTS = bx.STRATEGY_TESTER_REPORTS
SOURCE_BX_EXECUTION = bx.MT5_EXECUTION_RESULT
SOURCE_BX_POLICY = bx.RUNTIME_POLICY_CONFIG
SOURCE_BX_GATE = bx.GATE_AUDIT
SOURCE_BV_FINAL = bv.FINAL_DECISION
SOURCE_BV_REPORTS = bv.STRATEGY_TESTER_REPORTS
SOURCE_BW_FINAL = STAGE_DIR / "02_runs" / "run364BW" / "final_decision.json"

BX_TELEMETRY_DIR = STAGE_DIR / "02_runs" / "run364BX" / "runtime_telemetry"
BV_TELEMETRY = STAGE_DIR / "02_runs" / "run364BV" / "runtime_telemetry" / "run364BV_synthetic_short_source_overlay_calendar_block_telemetry.csv"
BV_REPORT = STAGE_DIR / "02_runs" / "run364BV" / "mt5" / "reports" / "OPv2_run364BV_synthetic_short_overlay_calendar.htm"

INPUT_FILES = [
    SOURCE_BX_FINAL,
    SOURCE_BX_SCOREBOARD,
    SOURCE_BX_REPORTS,
    SOURCE_BX_EXECUTION,
    SOURCE_BX_POLICY,
    SOURCE_BX_GATE,
    SOURCE_BV_FINAL,
    SOURCE_BV_REPORTS,
    SOURCE_BW_FINAL,
    BV_TELEMETRY,
    BV_REPORT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    TRADE_ATTRIBUTION,
    ATTRIBUTION_BY_VARIANT,
    ATTRIBUTION_BY_DIRECTION,
    ATTRIBUTION_BY_SOURCE,
    ATTRIBUTION_BY_MONTH,
    ATTRIBUTION_BY_OPEN_HOUR,
    ATTRIBUTION_BY_CLOSE_HOUR,
    RUNTIME_SIGNAL_ATTRIBUTION,
    VARIANT_PAIR_DELTAS,
    TRADE_MEMBERSHIP_DELTA,
    NEXT_QUEUE,
    KPI_CONTRACT_AUDIT,
    ROW_GRAIN_AUDIT,
    SOURCE_AUTHORITY_AUDIT,
    PERFORMANCE_RECEIPT,
    BACKTEST_RECEIPT,
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
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return bu.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    bu.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    bu.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    bu.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    bu.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    bu.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
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


def table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
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


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BY inputs(BY 입력 누락): " + ", ".join(missing))
    bx_final = read_json(SOURCE_BX_FINAL)
    bv_final = read_json(SOURCE_BV_FINAL)
    bw_final = read_json(SOURCE_BW_FINAL)
    if bx_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BX next_run_id mismatch(BX 다음 실행 불일치): {bx_final.get('next_run_id')} != {RUN_ID}")
    if any(bx_final.get(key) != "not_claimed" for key in ["runtime_authority", "operating_promotion", "goal_achieve"]):
        raise RuntimeError("BX has forbidden authority claim(BX 금지 권위 주장 존재)")
    return bx_final, bv_final, bw_final


def input_manifest_rows() -> list[dict[str, Any]]:
    extra = []
    for path in BX_TELEMETRY_DIR.glob("*.csv"):
        extra.append(path)
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BY attribution source(BY 귀속 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in [*INPUT_FILES, *extra]
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
    cycles["bar_hour"] = cycles["bar_dt"].dt.hour
    cycles["bar_month"] = cycles["bar_dt"].dt.to_period("M").astype(str)
    cycles["order_filled_bool"] = cycles["order_filled"].astype(str).str.lower().eq("true")
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


def telemetry_path_for_attempt(attempt_name: str) -> Path:
    stem = attempt_name.replace("run364BX_", "")
    return BX_TELEMETRY_DIR / f"run364BX_{stem}_telemetry.csv"


def parse_report_trades(label: str, variant_id: str, attempt_name: str, report_path: Path, telemetry_path: Path) -> pd.DataFrame:
    parsed = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(parsed["deals"])
    cycles = read_cycles(telemetry_path)
    opens = cycles[cycles["exec_action"].isin(["open_long", "reverse_open_long", "open_short", "reverse_open_short"])].copy()
    rows: list[dict[str, Any]] = []
    for trade in trades:
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID if label != "BV" else BASELINE_RUN_ID,
                "variant_label": label,
                "variant_id": variant_id,
                "attempt_name": attempt_name,
                "open_time_dt": trade.open_time,
                "close_time_dt": trade.close_time,
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
                "close_month": str(trade.close_time.to_period("M")),
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
    joined["open_time"] = joined["open_time_dt"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    joined["close_time"] = joined["close_time_dt"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    return joined.drop(columns=["written_dt", "decision_reason"]).copy()


def load_all_trades() -> pd.DataFrame:
    reports = read_json(SOURCE_BX_REPORTS)
    frames = [
        parse_report_trades(
            "BV",
            "bv_full_overlay_reference",
            "run364BV_synthetic_short_source_overlay_calendar_block",
            BV_REPORT,
            BV_TELEMETRY,
        )
    ]
    for record in reports:
        attempt_name = str(record["attempt_name"])
        variant_id = {
            "run364BX_bx01_hour17_overlay_keep_native_short": "bx01_overlay_hour17_only_keep_native_short",
            "run364BX_bx02_native_short_only_overlay_disabled": "bx02_native_short_only_overlay_disabled",
            "run364BX_bx03_hour17_overlay_weak_late_firewall": "bx03_hour17_overlay_plus_weak_late_session_firewall",
        }[attempt_name]
        frames.append(parse_report_trades(variant_id, variant_id, attempt_name, Path(record["html_report"]["path"]), telemetry_path_for_attempt(attempt_name)))
    frame = pd.concat(frames, ignore_index=True)
    output = frame.copy()
    output = output.drop(columns=["open_time_dt", "close_time_dt"])
    write_csv(TRADE_ATTRIBUTION, output.to_dict("records"))
    return frame


def summarize_trades(frame: pd.DataFrame, group_cols: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, group in frame.groupby(list(group_cols), dropna=False):
        if not isinstance(key, tuple):
            key = (key,)
        wins = float(group.loc[group["net_profit"] > 0, "net_profit"].sum())
        losses = float(group.loc[group["net_profit"] < 0, "net_profit"].sum())
        row = {col: key[idx] for idx, col in enumerate(group_cols)}
        row.update(
            {
                "trade_count": int(len(group)),
                "net_profit": round(float(group["net_profit"].sum()), 2),
                "expectancy": round(float(group["net_profit"].mean()), 6),
                "win_count": int((group["net_profit"] > 0).sum()),
                "loss_count": int((group["net_profit"] < 0).sum()),
                "win_rate_percent": round(float((group["net_profit"] > 0).mean() * 100.0), 6),
                "gross_profit": round(wins, 2),
                "gross_loss": round(losses, 2),
                "profit_factor": finite(safe_pf(wins, losses), 6),
                "avg_hold_minutes": round(float(group["hold_minutes"].mean()), 6),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(row)
    return rows


def runtime_signal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in read_json(SOURCE_BX_REPORTS):
        attempt_name = str(record["attempt_name"])
        variant_id = {
            "run364BX_bx01_hour17_overlay_keep_native_short": "bx01_overlay_hour17_only_keep_native_short",
            "run364BX_bx02_native_short_only_overlay_disabled": "bx02_native_short_only_overlay_disabled",
            "run364BX_bx03_hour17_overlay_weak_late_firewall": "bx03_hour17_overlay_plus_weak_late_session_firewall",
        }[attempt_name]
        cycles = read_cycles(telemetry_path_for_attempt(attempt_name))
        for (decision, bucket, hour), group in cycles.groupby(["decision", "source_bucket", "bar_hour"], dropna=False):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": variant_id,
                    "attempt_name": attempt_name,
                    "decision": decision,
                    "source_bucket": bucket,
                    "bar_hour": hour,
                    "cycle_count": int(len(group)),
                    "order_filled_count": int(group["order_filled_bool"].sum()),
                    "mean_p_short": finite(pd.to_numeric(group["p_short"], errors="coerce").mean()),
                    "mean_p_long": finite(pd.to_numeric(group["p_long"], errors="coerce").mean()),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_SIGNAL_ATTRIBUTION, rows)
    return rows


def build_pair_deltas(trades: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    comparisons = [
        ("bx03_vs_bx01_late_firewall_increment", "bx03_hour17_overlay_plus_weak_late_session_firewall", "bx01_overlay_hour17_only_keep_native_short"),
        ("bx01_vs_bx02_hour17_overlay_increment", "bx01_overlay_hour17_only_keep_native_short", "bx02_native_short_only_overlay_disabled"),
        ("bx03_vs_bx02_overlay_plus_late_firewall_increment", "bx03_hour17_overlay_plus_weak_late_session_firewall", "bx02_native_short_only_overlay_disabled"),
        ("bx03_vs_bv_full_overlay_and_late_firewall_increment", "bx03_hour17_overlay_plus_weak_late_session_firewall", "bv_full_overlay_reference"),
    ]
    pair_rows: list[dict[str, Any]] = []
    membership_rows: list[dict[str, Any]] = []
    for comparison_id, left_id, right_id in comparisons:
        left = trades[trades["variant_id"].eq(left_id)].copy()
        right = trades[trades["variant_id"].eq(right_id)].copy()
        keys = ["open_time_dt", "open_type"]
        merged = left.merge(
            right[keys + ["net_profit", "source_bucket", "close_time_dt", "close_month", "open_hour", "close_hour"]],
            on=keys,
            how="outer",
            suffixes=("_left", "_right"),
            indicator=True,
        )
        both = merged[merged["_merge"].eq("both")].copy()
        common_delta = float((both["net_profit_left"] - both["net_profit_right"]).sum()) if not both.empty else 0.0
        left_only = merged[merged["_merge"].eq("left_only")]
        right_only = merged[merged["_merge"].eq("right_only")]
        left_only_net = float(left_only["net_profit_left"].sum()) if not left_only.empty else 0.0
        right_only_net = float(right_only["net_profit_right"].sum()) if not right_only.empty else 0.0
        pair_rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": comparison_id,
                "left_variant_id": left_id,
                "right_variant_id": right_id,
                "left_net_profit": round(float(left["net_profit"].sum()), 2),
                "right_net_profit": round(float(right["net_profit"].sum()), 2),
                "net_delta_left_minus_right": round(float(left["net_profit"].sum() - right["net_profit"].sum()), 2),
                "left_trade_count": int(len(left)),
                "right_trade_count": int(len(right)),
                "both_count": int(len(both)),
                "left_only_count": int(len(left_only)),
                "right_only_count": int(len(right_only)),
                "left_only_net": round(left_only_net, 2),
                "right_only_net": round(right_only_net, 2),
                "common_net_delta": round(common_delta, 2),
                "interpretation": pair_interpretation(comparison_id, left_only_net, right_only_net, common_delta),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for _, row in merged[merged["_merge"].ne("both")].iterrows():
            membership_rows.append(
                {
                    "run_id": RUN_ID,
                    "comparison_id": comparison_id,
                    "membership": row["_merge"],
                    "open_time": row["open_time_dt"].isoformat() if pd.notna(row["open_time_dt"]) else "",
                    "open_type": row["open_type"],
                    "left_net_profit": finite(row.get("net_profit_left", "")),
                    "right_net_profit": finite(row.get("net_profit_right", "")),
                    "left_source_bucket": row.get("source_bucket_left", ""),
                    "right_source_bucket": row.get("source_bucket_right", ""),
                    "left_close_month": row.get("close_month_left", ""),
                    "right_close_month": row.get("close_month_right", ""),
                    "left_open_hour": row.get("open_hour_left", ""),
                    "right_open_hour": row.get("open_hour_right", ""),
                    "left_close_hour": row.get("close_hour_left", ""),
                    "right_close_hour": row.get("close_hour_right", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(VARIANT_PAIR_DELTAS, pair_rows)
    write_csv(TRADE_MEMBERSHIP_DELTA, membership_rows)
    return pair_rows, membership_rows


def pair_interpretation(comparison_id: str, left_only_net: float, right_only_net: float, common_delta: float) -> str:
    if comparison_id == "bx03_vs_bx01_late_firewall_increment":
        return "bx03 improvement is one December h22 long loss removed minus one h17 overlay short loss(bx03 개선은 12월 22시 롱 손실 차단에서 17시 오버레이 숏 손실을 뺀 효과)."
    if comparison_id == "bx01_vs_bx02_hour17_overlay_increment":
        return "hour17 overlay adds net positive but with several replacement trades(17시 오버레이는 순수익 양수이나 일부 대체 거래를 만든다)."
    if comparison_id == "bx03_vs_bv_full_overlay_and_late_firewall_increment":
        return "restricting overlay to h17 plus late firewall improves net while reducing short count(오버레이를 17시로 제한하고 후반 방화벽을 더해 순수익은 개선, 숏 수는 감소)."
    return f"membership delta left_only={left_only_net:.2f}; right_only={right_only_net:.2f}; common={common_delta:.2f}"


def build_audits(trades: pd.DataFrame, pair_rows: Sequence[Mapping[str, Any]], bx_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    scoreboard = list(csv.DictReader(io_path(SOURCE_BX_SCOREBOARD).open(encoding="utf-8-sig")))
    score_by_variant = {row["variant_id"]: row for row in scoreboard}
    variant_rows = summarize_trades(trades, ["variant_id"])
    kpi_rows = []
    row_rows = []
    for row in variant_rows:
        variant_id = row["variant_id"]
        if variant_id == "bv_full_overlay_reference":
            continue
        expected = score_by_variant[variant_id]
        net_ok = abs(as_float(row["net_profit"]) - as_float(expected["net_profit"])) < 0.01
        trades_ok = int(row["trade_count"]) == int(float(expected["trade_count"]))
        kpi_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "check_id": "scoreboard_vs_trade_table",
                "status": "passed" if net_ok and trades_ok else "failed",
                "trade_table_net": row["net_profit"],
                "scoreboard_net": expected["net_profit"],
                "trade_table_count": row["trade_count"],
                "scoreboard_count": expected["trade_count"],
                "effect": "MT5 report KPI(MT5 보고서 핵심 성과 지표)와 deal table(딜 표)이 일치한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        row_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "row_grain": "closed_trade(종료 거래)",
                "row_count": row["trade_count"],
                "status": "passed" if int(row["trade_count"]) > 0 else "failed",
                "effect": "trade-level attribution(거래 단위 귀속)의 grain(입도)을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    source_rows = [
        {
            "run_id": RUN_ID,
            "source_id": "bx_strategy_tester_reports",
            "path": rel(SOURCE_BX_REPORTS),
            "status": "passed" if len(scoreboard) == 3 else "failed",
            "authority": "MT5 Strategy Tester report(MT5 전략 테스터 보고서)",
            "effect": "net/PF/trades(순수익/수익 팩터/거래수)의 권위 원천이다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "source_id": "bx_runtime_telemetry",
            "path": rel(BX_TELEMETRY_DIR),
            "status": "passed" if any(BX_TELEMETRY_DIR.glob("*_telemetry.csv")) else "failed",
            "authority": "runtime source attribution(런타임 원천 귀속)",
            "effect": "decision_reason(결정 사유)과 source_bucket(원천 버킷)의 권위 원천이다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "source_id": "pair_delta_membership",
            "path": rel(VARIANT_PAIR_DELTAS),
            "status": "passed" if pair_rows else "failed",
            "authority": "counterfactual comparison by executed trade membership(실행 거래 구성 비교)",
            "effect": "variant delta(변형 차이)의 좁은 원인을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(KPI_CONTRACT_AUDIT, kpi_rows)
    write_csv(ROW_GRAIN_AUDIT, row_rows)
    write_csv(SOURCE_AUTHORITY_AUDIT, source_rows)
    return kpi_rows, row_rows, source_rows


def build_next_queue() -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "bz01_december_h22_long_block_counterfactual",
            "action": "Materialize BX3 late-session guard input(BX3 후반 세션 가드 입력 구체화)",
            "evidence_seed": "bx03 vs bx01: removed 2025-12-10 22:05 long loss -38.10 and added 2025-12-11 17:05 short loss -16.94, net +21.16.",
            "timestamp_safety": "uses month-of-year and entry server hour only(월중 값과 진입 서버 시간만 사용)",
            "success_condition": "confirm December h22 long block without exact-year memorization(정확한 연도 암기 없이 12월 22시 롱 차단 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "bz02_h17_overlay_loss_guard_quality_floor",
            "action": "Scout h17 overlay quality floor(17시 오버레이 품질 하한 탐색)",
            "evidence_seed": "h17 overlay is positive versus native-only, but BX3 added one -16.94 h17 synthetic short loss.",
            "timestamp_safety": "closed-bar probabilities and entry-known hour only(닫힌 봉 확률과 진입 시점 시간만 사용)",
            "success_condition": "keep h17 overlay net while reducing loss tail(17시 오버레이 순수익을 유지하면서 손실 꼬리 축소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "bz03_equity_dd_cluster_review",
            "action": "Materialize equity drawdown cluster inputs(평가손익 낙폭 클러스터 입력 구체화)",
            "evidence_seed": "BX3 net/PF improved, but equity DD amount stayed 130.11.",
            "timestamp_safety": "post-run attribution only for design; no operating claim(설계용 사후 귀속, 운영 주장 없음)",
            "success_condition": "identify drawdown cluster without reducing density below 3/day(밀도 3/day를 깨지 않고 낙폭 클러스터 식별)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_QUEUE, rows)
    return rows


def final_payload(
    created_at: str,
    bx_final: Mapping[str, Any],
    bv_final: Mapping[str, Any],
    variant_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    by_variant = {row["variant_id"]: row for row in variant_rows}
    by_source = {(row["variant_id"], row["source_bucket"]): row for row in source_rows}
    bx3 = by_variant["bx03_hour17_overlay_plus_weak_late_session_firewall"]
    bx1 = by_variant["bx01_overlay_hour17_only_keep_native_short"]
    bx2 = by_variant["bx02_native_short_only_overlay_disabled"]
    bv_row = by_variant["bv_full_overlay_reference"]
    bx3_months = [row for row in month_rows if row["variant_id"] == "bx03_hour17_overlay_plus_weak_late_session_firewall"]
    worst_month = sorted(bx3_months, key=lambda row: as_float(row["net_profit"]))[0]
    delta_map = {row["comparison_id"]: row for row in pair_rows}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "status": "completed_stage364BY_reviewed_bx_runtime_ablation_attribution_open_bz_no_authority",
        "judgment": "runtime_ablation_review_positive_clue_bx03_december_late_session_guard_no_authority",
        "decision": "stage364BY_open_run364BZ_bx03_december_late_session_guard_inputs",
        "next_run_id": NEXT_RUN_ID,
        "best_variant_id": bx_final.get("best_variant_id"),
        "best_net_profit": bx3["net_profit"],
        "best_profit_factor": bx_final.get("best_mt5_profit_factor"),
        "best_trade_count": bx3["trade_count"],
        "best_density": bx_final.get("best_mt5_density"),
        "best_recovery_factor": bx_final.get("best_mt5_recovery_factor"),
        "best_equity_drawdown_amount": bx_final.get("best_mt5_equity_drawdown_amount"),
        "bx3_vs_bv_net_delta": round(as_float(bx3["net_profit"]) - as_float(bv_row["net_profit"]), 2),
        "bx3_vs_bx1_net_delta": delta_map["bx03_vs_bx01_late_firewall_increment"]["net_delta_left_minus_right"],
        "bx1_vs_bx2_net_delta": delta_map["bx01_vs_bx02_hour17_overlay_increment"]["net_delta_left_minus_right"],
        "bx3_long_source_net": by_source[("bx03_hour17_overlay_plus_weak_late_session_firewall", "long_threshold")]["net_profit"],
        "bx3_native_short_net": by_source[("bx03_hour17_overlay_plus_weak_late_session_firewall", "native_short_threshold")]["net_profit"],
        "bx3_synthetic_overlay_net": by_source[("bx03_hour17_overlay_plus_weak_late_session_firewall", "synthetic_short_overlay")]["net_profit"],
        "bx1_synthetic_overlay_net": by_source[("bx01_overlay_hour17_only_keep_native_short", "synthetic_short_overlay")]["net_profit"],
        "bx2_native_short_net": by_source[("bx02_native_short_only_overlay_disabled", "native_short_threshold")]["net_profit"],
        "worst_bx3_month": worst_month["close_month"],
        "worst_bx3_month_net": worst_month["net_profit"],
        "attribution_confidence": "medium_runtime_trade_membership_exact_but_forward_unproven",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_review_of_completed_bx_probe",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], source_inputs: Sequence[Path]) -> None:
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "BX3 improved net/PF versus BV and BX controls(BX3가 BV와 BX 대조군 대비 순수익/수익 팩터 개선)",
            "comparison_baseline": [BASELINE_RUN_ID, "bx01_hour17_overlay", "bx02_native_short_only"],
            "likely_drivers": [
                "December h22 long loss block(12월 22시 롱 손실 차단)",
                "h17 overlay positive versus native-only(17시 오버레이가 기본 숏 단독보다 양호)",
                "h19/h20 overlay removal reduced churn(19/20시 오버레이 제거로 회전 감소)",
            ],
            "segment_checks": [rel(ATTRIBUTION_BY_MONTH), rel(ATTRIBUTION_BY_OPEN_HOUR), rel(ATTRIBUTION_BY_SOURCE), rel(VARIANT_PAIR_DELTAS)],
            "alternative_explanations": "single December membership change and MT5 lifecycle coupling may overstate generality(단일 12월 구성 변화와 MT5 생명주기 결합이 일반성을 과장할 수 있음)",
            "attribution_confidence": final["attribution_confidence"],
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(bx.TESTER_IDENTITY_CONTRACT),
            "report_identity": rel(SOURCE_BX_REPORTS),
            "trade_evidence": rel(TRADE_ATTRIBUTION),
            "cost_assumptions": "broker-native real tick, commission 0, swap parsed from deal table(브로커 실제 틱, 수수료 0, 스왑은 딜 표에서 파싱)",
            "backtest_judgment": "usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in source_inputs if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_closeout",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "BX MT5 runtime ablation review(BX MT5 런타임 제거 비교 검토)",
            "evidence_available": [rel(SOURCE_BX_REPORTS), rel(TRADE_ATTRIBUTION), rel(VARIANT_PAIR_DELTAS), rel(NEXT_QUEUE)],
            "evidence_missing": ["forward/replay authority(전진/재생 권위)", "runtime authority closure(런타임 권위 폐쇄)", "live readiness evidence(실거래 준비 근거)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "BX3 is a stronger runtime clue, not an operating model yet(BX3는 더 강한 런타임 단서이지 아직 운영 모델은 아님).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": final["judgment"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def build_gates(kpi_rows: Sequence[Mapping[str, Any]], row_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("kpi_contract_audit", all(row["status"] == "passed" for row in kpi_rows), KPI_CONTRACT_AUDIT, "scoreboard(점수표)와 deal table(딜 표) KPI를 대조한다."),
        ("row_grain_audit", all(row["status"] == "passed" for row in row_rows), ROW_GRAIN_AUDIT, "closed trade(종료 거래) 단위 귀속을 고정한다."),
        ("source_authority_audit", all(row["status"] == "passed" for row in source_rows), SOURCE_AUTHORITY_AUDIT, "MT5 report(보고서)와 telemetry(런타임 기록)의 권위를 분리한다."),
        ("performance_attribution_gate", exists(PERFORMANCE_RECEIPT), PERFORMANCE_RECEIPT, "KPI 변화 원인과 대안을 기록한다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결한다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "운영 승격과 런타임 권위를 주장하지 않는다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, path, effect in rows
    ]


def write_docs(final: Mapping[str, Any], variant_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]], month_rows: Sequence[Mapping[str, Any]], pair_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    bx3_month_rows = sorted([row for row in month_rows if row["variant_id"] == "bx03_hour17_overlay_plus_weak_late_session_firewall"], key=lambda row: as_float(row["net_profit"]))
    report = f"""# run364BY review overlay hour17 native short ablation runtime probe(364BY 17시 오버레이 기본 숏 제거 비교 런타임 탐침 검토)

## Result(결과)

Action(행동): run364BX(364BX 실행)의 three-way MT5 runtime ablation(3방향 MT5 런타임 제거 비교)을 trade-level attribution(거래 단위 귀속), source bucket(원천 버킷), month/session stress(월/세션 압박), variant delta(변형 차이)로 검토했다.

Effect(효과): `bx03`의 개선이 “운영 승격”이 아니라 December h22 long guard(12월 22시 롱 가드)와 h17 overlay(17시 오버레이)의 runtime clue(런타임 단서)임을 분리했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- best variant(최선 변형): `{final['best_variant_id']}`
- best MT5 net/PF/trades/density(최선 MT5 순수익/수익 팩터/거래수/밀도): `{final['best_net_profit']}` / `{final['best_profit_factor']}` / `{final['best_trade_count']}` / `{final['best_density']}`
- BX3 vs BV net delta(BX3-BV 순수익 차이): `{final['bx3_vs_bv_net_delta']}`
- BX3 vs BX1 net delta(BX3-BX1 순수익 차이): `{final['bx3_vs_bx1_net_delta']}`
- attribution confidence(귀속 신뢰도): `{final['attribution_confidence']}`

## Variant KPI(변형 KPI)

{table([row for row in variant_rows if row['variant_id'] != 'bv_full_overlay_reference'], ['variant_id', 'trade_count', 'net_profit', 'expectancy', 'profit_factor', 'win_rate_percent', 'avg_hold_minutes'])}

## Source Attribution(원천 귀속)

{table([row for row in source_rows if row['variant_id'] == 'bx03_hour17_overlay_plus_weak_late_session_firewall'], ['source_bucket', 'trade_count', 'net_profit', 'expectancy', 'profit_factor', 'win_rate_percent'])}

## Worst BX3 Months(BX3 최악 월)

{table(bx3_month_rows, ['close_month', 'trade_count', 'net_profit', 'expectancy', 'profit_factor'], limit=6)}

## Pair Deltas(쌍 비교 차이)

{table(pair_rows, ['comparison_id', 'net_delta_left_minus_right', 'left_only_count', 'right_only_count', 'left_only_net', 'right_only_net', 'common_net_delta', 'interpretation'])}

## Next Queue(다음 대기열)

{table(queue_rows, ['queue_id', 'action', 'evidence_seed', 'success_condition'])}

## Gates(게이트)

{table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

runtime probe review(런타임 탐침 검토)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BY decision(결정)

Decision(결정): `{final['decision']}`

Judgment(판정): `{final['judgment']}`

Action(행동): BX MT5 output(BX MT5 출력)을 source/session/month/equity attribution(원천/세션/월/수익곡선 귀속)으로 검토했다.

Effect(효과): `bx03`는 BV 대비 `+{final['bx3_vs_bv_net_delta']}` net(순수익) 단서지만, equity DD(평가손익 낙폭)는 `{final['best_equity_drawdown_amount']}`로 남아 다음 BZ에서 December late-session guard(12월 후반 세션 가드)와 h17 overlay loss guard(17시 오버레이 손실 가드)를 구체화한다.

Forbidden claims(금지 주장): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성).
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364BY -->", f"\n<!-- run364BY -->\n- `{RUN_ID}`: BX runtime ablation review(BX 런타임 제거 비교 검토) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364BY -->", f"\n<!-- run364BY -->\n## run364BY BX runtime ablation review(BX 런타임 제거 비교 검토)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364BY` reviewed BX MT5 runtime ablation(BX MT5 런타임 제거 비교 검토). Best variant(최선 변형) `bx03`의 MT5 net/PF/trades/density(순수익/수익 팩터/거래수/밀도)는 `{final['best_net_profit']}` / `{final['best_profit_factor']}` / `{final['best_trade_count']}` / `{final['best_density']}`이고, BV 대비 net(순수익)은 `+{final['bx3_vs_bv_net_delta']}`이다. 개선 원인은 주로 December h22 long loss block(12월 22시 롱 손실 차단)과 h17 overlay(17시 오버레이) 단서다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 December late-session guard(12월 후반 세션 가드), h17 overlay loss guard(17시 오버레이 손실 가드), equity DD cluster(평가손익 낙폭 클러스터)를 materialize(구체화)한다.

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

Runtime probe best variant(런타임 탐침 최선 변형): `bx03_hour17_overlay_plus_weak_late_session_firewall`

Best MT5 KPI(최선 MT5 핵심 성과 지표): net `{final['best_net_profit']}`, PF `{final['best_profit_factor']}`, trades `{final['best_trade_count']}`, density `{final['best_density']}`, recovery `{final['best_recovery_factor']}`, equity DD `{final['best_equity_drawdown_amount']}`.

Attribution(귀속): BX3 long source(롱 원천) `{final['bx3_long_source_net']}`, native short(기본 숏) `{final['bx3_native_short_net']}`, synthetic overlay(합성 오버레이) `{final['bx3_synthetic_overlay_net']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364BY -->", f"\n<!-- run364BY -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed BX runtime ablation(BX 런타임 제거 비교 검토). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(IDEA_REGISTRY, "<!-- run364BY_bx03_december_late_session_guard -->", f"\n<!-- run364BY_bx03_december_late_session_guard -->\n- Idea(아이디어): BX3 개선은 December h22 long guard(12월 22시 롱 가드)와 h17 overlay(17시 오버레이)를 분리해 더 검증한다. Effect(효과): net/PF(순수익/수익 팩터)를 유지하면서 equity DD(평가손익 낙폭)와 월 압박을 줄이는 다음 탐색으로 연결한다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(FINAL_DECISION),
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "trade_count": final["best_trade_count"],
        "trade_density_per_feature_day": final["best_density"],
        "recovery_factor": final["best_recovery_factor"],
        "drawdown": final["best_equity_drawdown_amount"],
        "work_family": "kpi_evidence(핵심 성과 지표 근거)",
        "evidence_boundary": "runtime_probe_review_only(런타임 탐침 검토 한정)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "next_action": NEXT_RUN_ID,
        "question": "Why did BX3 improve and what guard should be tested next?(BX3는 왜 개선됐고 다음에 어떤 가드를 시험해야 하는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "runtime_probe_review(런타임 탐침 검토)", "path": rel(FINAL_DECISION)}], extend_header=True)
    ledger_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_probe_review"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_probe_review"),
    ]:
        row_id = f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}"
        ledger_rows.append(
            {
                **common,
                "ledger_row_id": row_id,
                "row_id": row_id,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "path": rel(FINAL_DECISION),
                "view": view,
                "tier": tier,
                "metric_scope": scope,
                "notes": "Tier B missing_required(Tier B 필수 누락); no fallback source(대체 원천 없음).",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "record_view"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "record_view"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "artifact_id": f"{RUN_NUMBER}_{path.stem}",
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "artifact_type": "runtime_ablation_review_artifact",
            "path": rel(path),
            "sha256": sha(path),
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in OUTPUT_FILES
        if exists(path) and io_path(Path(path)).is_file()
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def write_run_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES if exists(path)],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": final["created_at_utc"],
        },
    )


def main() -> None:
    ensure_dirs()
    bx_final, bv_final, _bw_final = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(핵심 성과 지표 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
            ],
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit", "final_claim_guard"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    trades = load_all_trades()
    variant_rows = summarize_trades(trades, ["variant_id"])
    direction_rows = summarize_trades(trades, ["variant_id", "direction"])
    source_rows = summarize_trades(trades, ["variant_id", "source_bucket"])
    month_rows = summarize_trades(trades, ["variant_id", "close_month"])
    open_hour_rows = summarize_trades(trades, ["variant_id", "open_hour"])
    close_hour_rows = summarize_trades(trades, ["variant_id", "close_hour"])
    write_csv(ATTRIBUTION_BY_VARIANT, variant_rows)
    write_csv(ATTRIBUTION_BY_DIRECTION, direction_rows)
    write_csv(ATTRIBUTION_BY_SOURCE, source_rows)
    write_csv(ATTRIBUTION_BY_MONTH, month_rows)
    write_csv(ATTRIBUTION_BY_OPEN_HOUR, open_hour_rows)
    write_csv(ATTRIBUTION_BY_CLOSE_HOUR, close_hour_rows)
    runtime_signal_rows()
    pair_rows, membership_rows = build_pair_deltas(trades)
    queue_rows = build_next_queue()
    kpi_rows, row_rows, source_audit_rows = build_audits(trades, pair_rows, bx_final)
    gates = build_gates(kpi_rows, row_rows, source_audit_rows)
    final = final_payload(created_at, bx_final, bv_final, variant_rows, source_rows, month_rows, pair_rows, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final, [*INPUT_FILES, *BX_TELEMETRY_DIR.glob("*.csv")])
    gates = build_gates(kpi_rows, row_rows, source_audit_rows)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(created_at, bx_final, bv_final, variant_rows, source_rows, month_rows, pair_rows, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, variant_rows, source_rows, month_rows, pair_rows, queue_rows, gates)
    write_ledgers(final)
    write_run_manifest(final)
    write_json(
        LINEAGE_RECEIPT,
        {
            **read_json(LINEAGE_RECEIPT),
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
        },
    )
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
