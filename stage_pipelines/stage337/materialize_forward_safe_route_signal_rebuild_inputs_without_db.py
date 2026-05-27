from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

import MetaTrader5 as mt5


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.collectors import export_fpmarkets_v2_mt5_bars as fp
from stage_pipelines.stage337 import design_forward_safe_route_signal_rebuild_packet_without_db as bn


aw = bn.aw
bg = bn.bg

TODAY = "2026-05-27"
STAGE_ID = bn.STAGE_ID
RUN_NUMBER = "run337BO"
RUN_ID = "run337BO_materialize_forward_safe_route_signal_rebuild_inputs_without_db_v1"
PARENT_RUN_ID = bn.RUN_ID
NEXT_RUN_ID = "run337BP_build_live_computable_feature_frame_preflight_without_db_v1"
STATUS = "completed_stage337BO_forward_safe_rebuild_inputs_materialized_no_training_no_selection"
JUDGMENT = "fresh_forward_data_and_live_computable_input_inventory_ready_for_feature_preflight"
DECISION = "stage337BO_open_run337BP_live_computable_feature_frame_preflight"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BO_forward_safe_route_signal_rebuild_input_materialization_"
    "no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bn.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
REVIEWS_DIR = bn.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BO_forward_safe_route_signal_rebuild_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BO_forward_safe_route_signal_rebuild_inputs.md"
SELECTED_STATUS = bn.SELECTED_STATUS
STAGE_BRIEF = bn.STAGE_BRIEF
WORKSPACE_STATE = bn.WORKSPACE_STATE
CURRENT_STATE = bn.CURRENT_STATE
CHANGELOG = bn.CHANGELOG
RUN_REGISTRY = bn.RUN_REGISTRY
ALPHA_LEDGER = bn.ALPHA_LEDGER
ARTIFACT_REGISTRY = bn.ARTIFACT_REGISTRY
STAGE_LEDGER = bn.STAGE_LEDGER

BN_DIR = STAGE_DIR / "02_runs" / "run337BN"
BN_FINAL = BN_DIR / "final_decision.json"
BN_WORK_PACKET = BN_DIR / "forward_safe_rebuild_work_packet_spec.csv"
BN_INPUT_CONTRACT = BN_DIR / "live_computable_input_contract.csv"
BN_NO_OVERFIT_GATES = BN_DIR / "no_overfit_gate_matrix.csv"
BN_NEGATIVE_CONTROLS = BN_DIR / "negative_control_matrix.csv"
BN_REBUILD_LANES = BN_DIR / "rebuild_lane_matrix.csv"
BN_MT5_PROOF = BN_DIR / "mt5_external_proof_plan.csv"
BN_DATASET_PLAN = BN_DIR / "dataset_materialization_plan.csv"
BN_QUEUE = BN_DIR / "run337BO_input_materialization_queue.csv"
BN_GATE_AUDIT = BN_DIR / "required_gate_coverage_audit.csv"

STAGE326_RAW_ROOT = ROOT / "stages" / "326_forward__cp322a_frozen_forward_gate" / "01_inputs" / "raw_m5"
STAGE326_SUMMARY = STAGE326_RAW_ROOT / "stage01_raw_export_summary.json"

FRESH_RAW_INVENTORY = RUN_DIR / "fresh_raw_inventory.csv"
STAGE326_SNAPSHOT_INVENTORY = RUN_DIR / "stage326_snapshot_inventory.csv"
DATA_QUALITY_AUDIT = RUN_DIR / "data_quality_audit.csv"
LIVE_INPUT_AVAILABILITY = RUN_DIR / "live_input_availability_matrix.csv"
ASOF_JOIN_PREFLIGHT = RUN_DIR / "asof_join_preflight.csv"
OUTCOME_SOURCE_FIREWALL = RUN_DIR / "outcome_source_firewall.csv"
PARITY_PREFLIGHT_PLAN = RUN_DIR / "parity_preflight_plan.csv"
BLOCKED_INPUT_LIST = RUN_DIR / "blocked_input_list.csv"
RUN337BP_QUEUE = RUN_DIR / "run337BP_feature_frame_preflight_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BN_FINAL,
    BN_WORK_PACKET,
    BN_INPUT_CONTRACT,
    BN_NO_OVERFIT_GATES,
    BN_NEGATIVE_CONTROLS,
    BN_REBUILD_LANES,
    BN_MT5_PROOF,
    BN_DATASET_PLAN,
    BN_QUEUE,
    BN_GATE_AUDIT,
    STAGE326_SUMMARY,
)
OUTPUT_FILES = (
    FRESH_RAW_INVENTORY,
    STAGE326_SNAPSHOT_INVENTORY,
    DATA_QUALITY_AUDIT,
    LIVE_INPUT_AVAILABILITY,
    ASOF_JOIN_PREFLIGHT,
    OUTCOME_SOURCE_FIREWALL,
    PARITY_PREFLIGHT_PLAN,
    BLOCKED_INPUT_LIST,
    RUN337BP_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

M5_SECONDS = 300
REQUESTED_START_UTC = datetime(2026, 4, 14, tzinfo=UTC)
MAX_ASOF_AGE_MINUTES = 7 * 24 * 60
RAW_COLUMNS = (
    "time_open_unix",
    "time_close_unix",
    "contract_symbol",
    "broker_symbol",
    "timeframe",
    "price_basis",
    "open",
    "high",
    "low",
    "close",
    "tick_volume",
    "spread_points",
    "real_volume",
    "time_basis",
    "timezone_status",
)
INVENTORY_COLUMNS = (
    "contract_symbol",
    "broker_symbol",
    "status",
    "row_count",
    "first_open_utc",
    "last_open_utc",
    "last_close_utc",
    "lag_vs_us100_minutes",
    "csv_path",
    "manifest_path",
    "sha256",
    "last_error",
    "effect",
    "claim_boundary",
)
SNAPSHOT_COLUMNS = (
    "contract_symbol",
    "broker_symbol",
    "row_count",
    "first_open_utc",
    "last_open_utc",
    "last_close_utc",
    "csv_path",
    "manifest_path",
    "effect",
    "claim_boundary",
)
QUALITY_COLUMNS = (
    "contract_symbol",
    "row_count",
    "duplicate_open_count",
    "non_monotonic_count",
    "gap_count_gt_5m",
    "max_gap_minutes",
    "bad_ohlc_count",
    "zero_volume_count",
    "status",
    "effect",
    "claim_boundary",
)
AVAILABILITY_COLUMNS = (
    "lane_id",
    "required_symbols",
    "available_symbols",
    "missing_symbols",
    "max_lag_minutes",
    "status",
    "effect",
    "claim_boundary",
)
ASOF_COLUMNS = (
    "symbol",
    "source_role",
    "last_close_utc",
    "lag_vs_us100_minutes",
    "asof_join_status",
    "stale_if_over_minutes",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "artifact",
    "checked_columns",
    "forbidden_terms_found",
    "status",
    "effect",
    "claim_boundary",
)
PARITY_PLAN_COLUMNS = (
    "plan_id",
    "required_input",
    "preflight_status",
    "next_runtime_check",
    "blocked_status_if_missing",
    "effect",
    "claim_boundary",
)
BLOCKED_COLUMNS = (
    "blocker_id",
    "scope",
    "status",
    "evidence",
    "repair_action",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = bn.QUEUE_COLUMNS
GATE_COLUMNS = bn.GATE_COLUMNS

LANE_REQUIREMENTS = {
    "bn_lane_rank_free_absolute_score": [
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
    ],
    "bn_lane_live_market_regime_gate": ["US100", "VIX", "US10YR", "USDX"],
    "bn_lane_proxy_only_diagnostic": ["US100"],
}
SOURCE_ROLE = {
    "US100": "target(대상)",
    "VIX": "volatility_regime(변동성 국면)",
    "US10YR": "rate_regime(금리 국면)",
    "USDX": "usd_regime(달러 국면)",
    "NVDA": "mega_cap_context(대형주 문맥)",
    "AAPL": "mega_cap_context(대형주 문맥)",
    "MSFT": "mega_cap_context(대형주 문맥)",
    "AMZN": "mega_cap_context(대형주 문맥)",
    "AMD": "mega_cap_context(대형주 문맥)",
    "GOOGL.xnas": "mega_cap_context(대형주 문맥)",
    "META": "mega_cap_context(대형주 문맥)",
    "TSLA": "mega_cap_context(대형주 문맥)",
}
FORBIDDEN_TERMS = ("pnl", "profit", "trade_result", "mt5_result", "outcome", "label", "future", "rank_forward")


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_from_unix(value: int) -> str:
    return datetime.fromtimestamp(value, tz=UTC).isoformat().replace("+00:00", "Z")


def unix_from_iso(value: str) -> int:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return int(parsed.timestamp())


def rel(path: Path) -> str:
    return aw.rel(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def load_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BO inputs: {missing}")
    return {
        "bn_final": read_json(BN_FINAL),
        "bn_work": read_rows(BN_WORK_PACKET),
        "bn_input": read_rows(BN_INPUT_CONTRACT),
        "bn_gates": read_rows(BN_NO_OVERFIT_GATES),
        "bn_negative": read_rows(BN_NEGATIVE_CONTROLS),
        "bn_lanes": read_rows(BN_REBUILD_LANES),
        "bn_proof": read_rows(BN_MT5_PROOF),
        "bn_dataset": read_rows(BN_DATASET_PLAN),
        "bn_queue": read_rows(BN_QUEUE),
        "bn_gate_audit": read_rows(BN_GATE_AUDIT),
        "stage326_summary": read_json(STAGE326_SUMMARY),
    }


def init_mt5() -> dict[str, Any]:
    ok = mt5.initialize()
    info = mt5.terminal_info() if ok else None
    account = mt5.account_info() if ok else None
    return {
        "ok": bool(ok),
        "last_error": str(mt5.last_error()),
        "terminal_path": getattr(info, "path", None),
        "terminal_data_path": getattr(info, "data_path", None),
        "account_login_present": getattr(account, "login", None),
    }


def latest_closed_us100_open() -> datetime:
    rates = mt5.copy_rates_from_pos("US100", mt5.TIMEFRAME_M5, 0, 500)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"US100 latest bar probe failed: {mt5.last_error()}")
    now_ts = int(datetime.now(UTC).timestamp())
    closed_opens = [int(row["time"]) for row in rates if int(row["time"]) + M5_SECONDS <= now_ts]
    if not closed_opens:
        return datetime.fromtimestamp(int(rates[-1]["time"]), tz=UTC)
    return datetime.fromtimestamp(max(closed_opens), tz=UTC)


def normalize_symbol_dir(contract_symbol: str) -> str:
    return contract_symbol


def normalize_broker_file_token(broker_symbol: str) -> str:
    return broker_symbol.lower().replace(".", "_")


def rates_to_rows(contract_symbol: str, broker_symbol: str, rates: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in rates:
        opened = int(item["time"])
        rows.append(
            {
                "time_open_unix": opened,
                "time_close_unix": opened + M5_SECONDS,
                "contract_symbol": contract_symbol,
                "broker_symbol": broker_symbol,
                "timeframe": "M5",
                "price_basis": "Bid",
                "open": float(item["open"]),
                "high": float(item["high"]),
                "low": float(item["low"]),
                "close": float(item["close"]),
                "tick_volume": int(item["tick_volume"]),
                "spread_points": int(item["spread"]),
                "real_volume": int(item["real_volume"]),
                "time_basis": "MT5_PY_API_UNIX_SECONDS",
                "timezone_status": "UNRESOLVED_REQUIRES_MANUAL_BINDING",
            }
        )
    return rows


def write_raw_symbol(contract_symbol: str, broker_symbol: str, rows: Sequence[Mapping[str, Any]], requested_to: datetime, mt5_context: Mapping[str, Any]) -> tuple[Path, Path]:
    symbol_dir = RAW_REFRESH_DIR / normalize_symbol_dir(contract_symbol)
    file_token = normalize_broker_file_token(broker_symbol)
    csv_path = symbol_dir / f"bars_{file_token}_m5_mt5api_raw.csv"
    manifest_path = symbol_dir / f"bars_{file_token}_m5_mt5api_raw.manifest.json"
    aw.write_csv(csv_path, RAW_COLUMNS, rows)
    first_open = int(rows[0]["time_open_unix"])
    last_open = int(rows[-1]["time_open_unix"])
    manifest = {
        "manifest_version": "STAGE337BO_FORWARD_SAFE_RAW_REFRESH_V1",
        "contract_symbol": contract_symbol,
        "broker_symbol": broker_symbol,
        "timeframe": "M5",
        "requested_from_utc": REQUESTED_START_UTC.isoformat().replace("+00:00", "Z"),
        "requested_to_utc": requested_to.isoformat().replace("+00:00", "Z"),
        "resolved_first_open_unix": first_open,
        "resolved_last_open_unix": last_open,
        "resolved_last_close_unix": last_open + M5_SECONDS,
        "row_count": len(rows),
        "csv_file": str(csv_path.resolve()),
        "time_basis": "MT5_PY_API_UNIX_SECONDS",
        "source_timezone": "OPEN",
        "calendar_id": "OPEN",
        "timezone_status": "UNRESOLVED_REQUIRES_MANUAL_BINDING",
        "price_basis": "Bid",
        "terminal_path": mt5_context.get("terminal_path"),
        "terminal_data_path": mt5_context.get("terminal_data_path"),
        "account_login_present": mt5_context.get("account_login_present"),
        "generated_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    aw.write_json(manifest_path, manifest)
    return csv_path, manifest_path


def collect_fresh_raw() -> tuple[list[dict[str, Any]], list[Path], dict[str, Any]]:
    mt5_context = init_mt5()
    if not mt5_context["ok"]:
        return [], [], {"status": "blocked_mt5_initialize_failed", **mt5_context}
    artifacts: list[Path] = []
    inventory: list[dict[str, Any]] = []
    try:
        if not mt5.symbol_select("US100", True):
            return [], [], {"status": "blocked_us100_select_failed", **mt5_context, "last_error": str(mt5.last_error())}
        requested_to = latest_closed_us100_open()
        us100_last_close_unix = int(requested_to.timestamp()) + M5_SECONDS
        for binding in fp.DEFAULT_SYMBOL_BINDINGS:
            contract_symbol = binding.contract_symbol
            broker_symbol = binding.broker_symbol
            selected = mt5.symbol_select(broker_symbol, True)
            if not selected:
                inventory.append(
                    {
                        "contract_symbol": contract_symbol,
                        "broker_symbol": broker_symbol,
                        "status": "blocked_symbol_select_failed",
                        "row_count": 0,
                        "first_open_utc": "",
                        "last_open_utc": "",
                        "last_close_utc": "",
                        "lag_vs_us100_minutes": "",
                        "csv_path": "",
                        "manifest_path": "",
                        "sha256": "",
                        "last_error": str(mt5.last_error()),
                        "effect": "심볼 선택 실패로 해당 입력은 재구축 입력에서 제외된다.",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
                continue
            rates = mt5.copy_rates_range(broker_symbol, mt5.TIMEFRAME_M5, REQUESTED_START_UTC, requested_to)
            if rates is None or len(rates) == 0:
                inventory.append(
                    {
                        "contract_symbol": contract_symbol,
                        "broker_symbol": broker_symbol,
                        "status": "blocked_no_rates_returned",
                        "row_count": 0,
                        "first_open_utc": "",
                        "last_open_utc": "",
                        "last_close_utc": "",
                        "lag_vs_us100_minutes": "",
                        "csv_path": "",
                        "manifest_path": "",
                        "sha256": "",
                        "last_error": str(mt5.last_error()),
                        "effect": "원천 봉이 없어 해당 입력은 차단 목록으로 간다.",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
                continue
            rows = rates_to_rows(contract_symbol, broker_symbol, rates)
            csv_path, manifest_path = write_raw_symbol(contract_symbol, broker_symbol, rows, requested_to, mt5_context)
            first_open = int(rows[0]["time_open_unix"])
            last_open = int(rows[-1]["time_open_unix"])
            last_close = int(rows[-1]["time_close_unix"])
            lag_minutes = (us100_last_close_unix - last_close) / 60.0
            artifacts.extend([csv_path, manifest_path])
            inventory.append(
                {
                    "contract_symbol": contract_symbol,
                    "broker_symbol": broker_symbol,
                    "status": "completed",
                    "row_count": len(rows),
                    "first_open_utc": iso_from_unix(first_open),
                    "last_open_utc": iso_from_unix(last_open),
                    "last_close_utc": iso_from_unix(last_close),
                    "lag_vs_us100_minutes": round(lag_minutes, 4),
                    "csv_path": rel(csv_path),
                    "manifest_path": rel(manifest_path),
                    "sha256": aw.sha256_file(csv_path),
                    "last_error": str(mt5.last_error()),
                    "effect": "forward-safe rebuild(전진 안전 재구축)에 쓸 수 있는 원천 후보를 확보했다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        summary = {
            "status": "completed",
            "requested_from_utc": REQUESTED_START_UTC.isoformat().replace("+00:00", "Z"),
            "requested_to_utc": requested_to.isoformat().replace("+00:00", "Z"),
            "us100_last_close_utc": datetime.fromtimestamp(us100_last_close_unix, tz=UTC).isoformat().replace("+00:00", "Z"),
            **mt5_context,
        }
        return inventory, artifacts, summary
    finally:
        mt5.shutdown()


def build_stage326_snapshot(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in src["stage326_summary"].get("exported_symbols", []):
        first_open = int(item.get("first_open_unix", 0) or 0)
        last_open = int(item.get("last_open_unix", 0) or 0)
        rows.append(
            {
                "contract_symbol": item.get("contract_symbol", ""),
                "broker_symbol": item.get("broker_symbol", ""),
                "row_count": item.get("row_count", ""),
                "first_open_utc": iso_from_unix(first_open) if first_open else "",
                "last_open_utc": iso_from_unix(last_open) if last_open else "",
                "last_close_utc": iso_from_unix(last_open + M5_SECONDS) if last_open else "",
                "csv_path": item.get("csv_path", ""),
                "manifest_path": item.get("manifest_path", ""),
                "effect": "기존 Stage326(326단계) snapshot(스냅샷)과 새 refresh(갱신)를 비교하는 기준이다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def row_status_map(inventory: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("contract_symbol")): row for row in inventory}


def build_quality_audit(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    for item in inventory:
        csv_path_text = str(item.get("csv_path", ""))
        contract_symbol = str(item.get("contract_symbol", ""))
        if item.get("status") != "completed" or not csv_path_text:
            audits.append(
                {
                    "contract_symbol": contract_symbol,
                    "row_count": 0,
                    "duplicate_open_count": "",
                    "non_monotonic_count": "",
                    "gap_count_gt_5m": "",
                    "max_gap_minutes": "",
                    "bad_ohlc_count": "",
                    "zero_volume_count": "",
                    "status": "blocked_no_csv",
                    "effect": "CSV가 없어 품질 감사를 할 수 없다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        path = ROOT / csv_path_text
        rows = read_rows(path)
        opens = [int(row["time_open_unix"]) for row in rows]
        duplicate_count = len(opens) - len(set(opens))
        non_monotonic = sum(1 for left, right in zip(opens, opens[1:]) if right <= left)
        gaps = [right - left for left, right in zip(opens, opens[1:]) if right - left > M5_SECONDS]
        bad_ohlc = 0
        zero_volume = 0
        for row in rows:
            open_p = float(row["open"])
            high = float(row["high"])
            low = float(row["low"])
            close = float(row["close"])
            if not (low <= open_p <= high and low <= close <= high and low <= high):
                bad_ohlc += 1
            if int(float(row.get("tick_volume", 0) or 0)) <= 0:
                zero_volume += 1
        status = "passed" if duplicate_count == 0 and non_monotonic == 0 and bad_ohlc == 0 else "failed"
        audits.append(
            {
                "contract_symbol": contract_symbol,
                "row_count": len(rows),
                "duplicate_open_count": duplicate_count,
                "non_monotonic_count": non_monotonic,
                "gap_count_gt_5m": len(gaps),
                "max_gap_minutes": round(max(gaps) / 60.0, 4) if gaps else 0,
                "bad_ohlc_count": bad_ohlc,
                "zero_volume_count": zero_volume,
                "status": status,
                "effect": "중복/역순/OHLC 오류를 막고, 세션 공백은 별도 관찰값으로 남긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return audits


def build_availability(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_symbol = row_status_map(inventory)
    rows: list[dict[str, Any]] = []
    for lane_id, required in LANE_REQUIREMENTS.items():
        available = [symbol for symbol in required if by_symbol.get(symbol, {}).get("status") == "completed"]
        missing = [symbol for symbol in required if symbol not in available]
        lags = [
            float(by_symbol[symbol].get("lag_vs_us100_minutes", 0) or 0)
            for symbol in available
            if str(by_symbol[symbol].get("lag_vs_us100_minutes", "")) != ""
        ]
        max_lag = max(lags) if lags else math.inf
        status = "available" if not missing and max_lag <= MAX_ASOF_AGE_MINUTES else "blocked_or_stale"
        rows.append(
            {
                "lane_id": lane_id,
                "required_symbols": ";".join(required),
                "available_symbols": ";".join(available),
                "missing_symbols": ";".join(missing),
                "max_lag_minutes": "" if math.isinf(max_lag) else round(max_lag, 4),
                "status": status,
                "effect": "어떤 재구축 lane(경로)이 실제 입력을 갖는지 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_asof_preflight(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inventory:
        symbol = str(item.get("contract_symbol", ""))
        status = str(item.get("status", ""))
        lag_text = str(item.get("lag_vs_us100_minutes", ""))
        lag = float(lag_text) if lag_text not in {"", "inf"} else math.inf
        asof_status = "ready" if status == "completed" and lag <= MAX_ASOF_AGE_MINUTES else "blocked_or_stale"
        rows.append(
            {
                "symbol": symbol,
                "source_role": SOURCE_ROLE.get(symbol, "context(문맥)"),
                "last_close_utc": item.get("last_close_utc", ""),
                "lag_vs_us100_minutes": "" if math.isinf(lag) else round(lag, 4),
                "asof_join_status": asof_status,
                "stale_if_over_minutes": MAX_ASOF_AGE_MINUTES,
                "effect": "US100 추론 시각 이하의 최신 확정봉만 붙이는 조건을 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inventory:
        csv_path_text = str(item.get("csv_path", ""))
        if item.get("status") != "completed" or not csv_path_text:
            continue
        path = ROOT / csv_path_text
        columns, _ = aw.read_csv_table(path, prefer_head=False)
        found = [term for term in FORBIDDEN_TERMS if any(term in column.lower() for column in columns)]
        rows.append(
            {
                "artifact": rel(path),
                "checked_columns": ";".join(columns),
                "forbidden_terms_found": ";".join(found),
                "status": "passed" if not found else "failed",
                "effect": "결과 원천/거래 결과/미래 라벨 컬럼이 입력에 섞이지 않게 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_parity_plan(availability: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    technical_ready = any(row.get("lane_id") == "bn_lane_proxy_only_diagnostic" and row.get("status") == "available" for row in availability)
    regime_ready = any(row.get("lane_id") == "bn_lane_live_market_regime_gate" and row.get("status") == "available" for row in availability)
    rank_free_ready = any(row.get("lane_id") == "bn_lane_rank_free_absolute_score" and row.get("status") == "available" for row in availability)
    return [
        {
            "plan_id": "bp_plan_us100_technical42",
            "required_input": "US100 raw M5 refresh(US100 원천 M5 갱신)",
            "preflight_status": "ready" if technical_ready else "blocked",
            "next_runtime_check": "Python feature row versus MT5 closed-bar feature row(파이썬 피처 행 대 MT5 확정봉 피처 행)",
            "blocked_status_if_missing": "blocked_forward_data_missing",
            "effect": "최소 기술 피처 경로를 먼저 동등성 검사할 수 있게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "bp_plan_macro48",
            "required_input": "US100,VIX,US10YR,USDX as-of raw M5(시점 기준 원천 M5)",
            "preflight_status": "ready" if regime_ready else "blocked",
            "next_runtime_check": "as-of joined macro feature parity(시점 기준 결합 거시 피처 동등성)",
            "blocked_status_if_missing": "blocked_macro_context_missing",
            "effect": "VIX/USD/rate regime(변동성/달러/금리 국면)을 전진 안전하게 붙인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "bp_plan_core56",
            "required_input": "US100 plus external macro/equity context(US100과 외부 거시/주식 문맥)",
            "preflight_status": "ready" if rank_free_ready else "blocked",
            "next_runtime_check": "full as-of feature parity and signal handoff preflight(전체 시점 기준 피처 동등성 및 신호 인계 사전점검)",
            "blocked_status_if_missing": "blocked_external_context_missing",
            "effect": "넓은 문맥 경로를 쓰되 누락 원천을 명시한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_blockers(inventory: Sequence[Mapping[str, Any]], availability: Sequence[Mapping[str, Any]], quality: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inventory:
        if item.get("status") != "completed":
            rows.append(
                {
                    "blocker_id": f"missing_raw_{item.get('contract_symbol')}",
                    "scope": item.get("contract_symbol", ""),
                    "status": item.get("status", ""),
                    "evidence": item.get("last_error", ""),
                    "repair_action": "rerun MT5 raw refresh after symbol/account repair(심볼/계정 수리 후 MT5 원천 갱신 재실행)",
                    "effect": "누락 원천을 조용히 대체하지 않는다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for item in quality:
        if item.get("status") != "passed":
            rows.append(
                {
                    "blocker_id": f"quality_{item.get('contract_symbol')}",
                    "scope": item.get("contract_symbol", ""),
                    "status": item.get("status", ""),
                    "evidence": json.dumps({key: item.get(key) for key in ("duplicate_open_count", "non_monotonic_count", "bad_ohlc_count")}, ensure_ascii=False),
                    "repair_action": "repair raw source before feature frame(피처 프레임 전 원천 수리)",
                    "effect": "깨진 원천으로 feature(피처)를 만들지 않는다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for item in availability:
        if item.get("status") != "available":
            rows.append(
                {
                    "blocker_id": f"lane_{item.get('lane_id')}",
                    "scope": item.get("lane_id", ""),
                    "status": item.get("status", ""),
                    "evidence": f"missing={item.get('missing_symbols')};max_lag={item.get('max_lag_minutes')}",
                    "repair_action": "restrict next preflight to available lanes and repair missing symbols(다음 사전점검은 가능 경로만 쓰고 누락 심볼 수리)",
                    "effect": "부분 입력을 전체 경로로 과장하지 않는다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_queue(availability: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    available_lanes = [str(row.get("lane_id")) for row in availability if row.get("status") == "available"]
    return [
        {
            "queue_id": "run337BP_live_computable_feature_frame_preflight",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "live-computable feature frame preflight(실시간 계산 가능 피처 프레임 사전점검)",
            "inputs_to_review": ";".join(
                [
                    rel(FRESH_RAW_INVENTORY),
                    rel(DATA_QUALITY_AUDIT),
                    rel(LIVE_INPUT_AVAILABILITY),
                    rel(ASOF_JOIN_PREFLIGHT),
                    rel(OUTCOME_SOURCE_FIREWALL),
                    rel(PARITY_PREFLIGHT_PLAN),
                    rel(BLOCKED_INPUT_LIST),
                ]
            ),
            "must_confirm": "available lanes, no outcome source, deterministic as-of joins, feature parity plan(가능 경로, 결과 원천 없음, 결정적 시점 기준 결합, 피처 동등성 계획)",
            "must_reject_if": "forward fit, outcome-distilled source, missing US100 forward raw data(전진 적합, 결과 증류 원천, US100 전진 원천 누락)",
            "expected_outputs": f"feature preflight for lanes={';'.join(available_lanes)}",
            "priority": "P0",
            "effect": "원천 데이터 확보에서 피처 동등성 사전점검으로 이동한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_receipts(final: Mapping[str, Any], collection_summary: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            RUN_EVIDENCE_RECEIPT,
            {
                "work_family": "experiment_execution",
                "primary_skill": "obsidian-run-evidence-system",
                "mt5_collection_status": collection_summary.get("status"),
                "us100_last_close_utc": final.get("us100_last_close_utc"),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_boundary": "fresh MT5 M5 raw refresh after 2026-04-14(2026-04-14 이후 MT5 M5 원천 갱신)",
                "fresh_raw_symbols": final.get("fresh_raw_completed_symbols"),
                "blocked_inputs": final.get("blocked_input_rows"),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_boundary": "no training, no threshold tuning, no candidate selection(학습/임계값 조정/후보 선택 없음)",
                "allowed_next": "feature frame preflight only(피처 프레임 사전점검만)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "runtime_boundary": "MT5 API raw-data refresh only; no Strategy Tester KPI(MT5 API 원천 데이터 갱신만, 전략 테스터 KPI 없음)",
                "runtime_authority": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "lineage": f"parent={PARENT_RUN_ID};raw_refresh={rel(RAW_REFRESH_DIR)}",
                "artifact_boundary": "raw refresh and preflight artifacts(원천 갱신 및 사전점검 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "judgment": final["judgment"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in payloads]


def build_gates(
    src: Mapping[str, Any],
    inventory: Sequence[Mapping[str, Any]],
    quality: Sequence[Mapping[str, Any]],
    availability: Sequence[Mapping[str, Any]],
    firewall: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    collection_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    bn_passed = sum(1 for row in src["bn_gate_audit"] if row.get("status") == "passed")
    by_symbol = row_status_map(inventory)
    us100_ready = by_symbol.get("US100", {}).get("status") == "completed"
    quality_ok = all(row.get("status") == "passed" for row in quality if row.get("contract_symbol") == "US100")
    firewall_ok = all(row.get("status") == "passed" for row in firewall)
    available_lane_count = sum(1 for row in availability if row.get("status") == "available")
    fresh_beyond_stage326 = False
    if by_symbol.get("US100", {}).get("last_close_utc"):
        fresh_last = unix_from_iso(str(by_symbol["US100"]["last_close_utc"]))
        stage326_rows = build_stage326_snapshot(src)
        stage326_us100 = next((row for row in stage326_rows if row.get("contract_symbol") == "US100"), {})
        old_last = unix_from_iso(str(stage326_us100.get("last_close_utc"))) if stage326_us100.get("last_close_utc") else 0
        fresh_beyond_stage326 = fresh_last > old_last
    specs = [
        ("bo_gate_parent_final_loaded", src["bn_final"].get("next_action") == RUN_ID, f"parent_next={src['bn_final'].get('next_action')}", "run337BN opens run337BO(run337BN이 run337BO를 연다)"),
        ("bo_gate_parent_gates_passed", bn_passed == 12 and src["bn_final"].get("passed_gates") == 12, f"bn_gates={bn_passed}", "run337BN gates passed(run337BN 게이트 통과)"),
        ("bo_gate_mt5_collection_completed", collection_summary.get("status") == "completed", f"collection_status={collection_summary.get('status')}", "MT5 raw refresh completed(MT5 원천 갱신 완료)"),
        ("bo_gate_us100_forward_data_present", us100_ready, f"us100_status={by_symbol.get('US100', {}).get('status')}", "US100 forward raw data present(US100 전진 원천 존재)"),
        ("bo_gate_fresh_beyond_stage326", fresh_beyond_stage326, f"fresh_beyond_stage326={fresh_beyond_stage326}", "fresh refresh extends Stage326 snapshot(Stage326 스냅샷보다 최신)"),
        ("bo_gate_us100_quality_passed", quality_ok, f"us100_quality={quality_ok}", "US100 quality audit passed(US100 품질 감사 통과)"),
        ("bo_gate_firewall_passed", firewall_ok and len(firewall) > 0, f"firewall_rows={len(firewall)}", "outcome source firewall passed(결과 원천 방화벽 통과)"),
        ("bo_gate_at_least_one_lane_available", available_lane_count >= 1, f"available_lanes={available_lane_count}", "at least one rebuild lane available(최소 한 재구축 경로 가능)"),
        ("bo_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue_rows={len(queue_rows)}", "run337BP queue ready(run337BP 대기열 준비)"),
        ("bo_gate_no_goal_or_forward_pass_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "input materialization stays separate from model or forward claims(입력 물질화를 모델/전진 주장과 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BO Forward-Safe Route-Signal Rebuild Inputs(전진 안전 경로 신호 재구축 입력)

## Conclusion(결론)

run337BO(337BO 실행)는 MT5 API(MetaTrader5 API, 메타트레이더5 API)로 2026-04-14 이후 US100 M5 forward raw data(전진 원천 데이터)를 새로 확보했고, route-signal rebuild(경로 신호 재구축)에 필요한 입력 가능성/차단 목록/동등성 사전점검 계획을 만들었다.

Effect(효과): 이제 수익이나 후보 선택으로 뛰지 않고, run337BP(337BP 실행)에서 live-computable feature frame(실시간 계산 가능 피처 프레임)과 Python-MT5 parity(파이썬-MT5 동등성)를 먼저 확인한다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- US100 last close(US100 마지막 종가 시각): `{final['us100_last_close_utc']}`
- fresh raw symbols(갱신 원천 심볼): `{final['fresh_raw_completed_symbols']}`
- available lanes(가능 경로): `{final['available_lanes']}`
- blocked input rows(차단 입력 행): `{final['blocked_input_rows']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

- training(학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BO Forward-Safe Route-Signal Rebuild Inputs(결정: 337단계 337BO 전진 안전 경로 신호 재구축 입력)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): 최신 forward raw data(전진 원천 데이터)를 확보했고, 다음은 feature frame preflight(피처 프레임 사전점검)와 runtime parity(런타임 동등성)다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BO focus")
    workspace = bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        "- >-\n"
        "  Stage337 run337BO focus complete: forward-safe route-signal rebuild inputs"
        "(전진 안전 경로 신호 재구축 입력)를 물질화했다. Effect(효과): "
        "MT5 API(MetaTrader5 API, 메타트레이더5 API) raw refresh(원천 갱신), "
        "data quality audit(데이터 품질 감사), outcome-source firewall(결과 원천 방화벽), "
        "parity preflight plan(동등성 사전점검 계획)을 만들고 run337BP(337BP 실행)를 연다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bg.remove_markdown_section(current_text, "## Stage337 run337BO(337BO 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BO(337BO 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BO(337BO 실행)는 최신 US100 M5 raw data(원천 데이터)와 외부 문맥 입력을 갱신하고, 차단 목록/동등성 사전점검 계획을 만들었다. 학습/선택/전진 통과/목표 달성은 주장하지 않는다.
"""
    current = current.replace("## Stage337 run337BN(337BN 실행)", entry + "\n## Stage337 run337BN(337BN 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `forward_safe_inputs_materialized_for_feature_preflight`
- actual_mt5_execution(실제 MT5 실행): `not_run_raw_data_refresh_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cp322A exact(정확 cp322A)는 보존하고, 다음은 피처 프레임 사전점검과 파이썬-MT5 동등성이다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_text = (
        stage_text.rstrip()
        + f"\n- {TODAY}: run337BO(337BO 실행) materialized fresh forward raw inputs(최신 전진 원천 입력) and opened run337BP(337BP 실행) feature parity preflight(피처 동등성 사전점검). Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = (
        changelog_text.rstrip()
        + f"\n- {TODAY}: Stage337 run337BO refreshed MT5 raw M5 data(MT5 원천 M5 데이터), audited live-computable inputs(실시간 계산 가능 입력), and opened feature parity preflight(피처 동등성 사전점검).\n"
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "forward_safe_route_signal_rebuild_input_materialization_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_execution",
        "primary_artifact": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__forward_safe_rebuild_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "forward_safe_rebuild_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BO forward-safe route-signal rebuild inputs",
        "tier_scope": "input_materialization_no_trading_kpi",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"fresh_symbols={final['fresh_raw_completed_symbols']};available_lanes={final['available_lanes']}",
        "guardrail_kpi": "no_training;no_selection;no_forward_claim;no_goal_achieve",
        "external_verification_status": "mt5_api_raw_refresh_completed_no_strategy_tester(원천 갱신 완료, 전략 테스터 없음)",
        "notes": f"next_action={final['next_action']};us100_last_close={final['us100_last_close_utc']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__forward_safe_rebuild_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "fresh MT5 API raw M5 refresh and live-computable input preflight",
        "kpi_scope": "input_materialization_no_trading_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": "goal_achieve_not_claimed;forward_passed_not_claimed;training_not_run",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__forward_safe_rebuild_inputs",
        "family": "forward_safe_route_signal_rebuild_input_materialization_without_db",
        "question": "can fresh live-computable forward inputs be materialized for rebuild preflight",
        "metric_scope": "fresh_raw_inventory_data_quality_availability_firewall",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    inventory, raw_artifacts, collection_summary = collect_fresh_raw()
    snapshot_rows = build_stage326_snapshot(src)
    snapshot_path = aw.write_csv(STAGE326_SNAPSHOT_INVENTORY, SNAPSHOT_COLUMNS, snapshot_rows)
    inventory_path = aw.write_csv(FRESH_RAW_INVENTORY, INVENTORY_COLUMNS, inventory)
    quality_rows = build_quality_audit(inventory)
    quality_path = aw.write_csv(DATA_QUALITY_AUDIT, QUALITY_COLUMNS, quality_rows)
    availability_rows = build_availability(inventory)
    availability_path = aw.write_csv(LIVE_INPUT_AVAILABILITY, AVAILABILITY_COLUMNS, availability_rows)
    asof_rows = build_asof_preflight(inventory)
    asof_path = aw.write_csv(ASOF_JOIN_PREFLIGHT, ASOF_COLUMNS, asof_rows)
    firewall_rows = build_firewall(inventory)
    firewall_path = aw.write_csv(OUTCOME_SOURCE_FIREWALL, FIREWALL_COLUMNS, firewall_rows)
    parity_rows = build_parity_plan(availability_rows)
    parity_path = aw.write_csv(PARITY_PREFLIGHT_PLAN, PARITY_PLAN_COLUMNS, parity_rows)
    blocked_rows = build_blockers(inventory, availability_rows, quality_rows)
    blocked_path = aw.write_csv(BLOCKED_INPUT_LIST, BLOCKED_COLUMNS, blocked_rows)
    queue_rows = build_queue(availability_rows)
    queue_path = aw.write_csv(RUN337BP_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, inventory, quality_rows, availability_rows, firewall_rows, queue_rows, collection_summary)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    completed_symbols = [str(row.get("contract_symbol")) for row in inventory if row.get("status") == "completed"]
    available_lanes = [str(row.get("lane_id")) for row in availability_rows if row.get("status") == "available"]
    us100 = next((row for row in inventory if row.get("contract_symbol") == "US100"), {})
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BO_input_materialization_gate_failure",
        "judgment": JUDGMENT if all_gates_pass else "forward_safe_rebuild_input_materialization_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BO_inputs_before_feature_preflight",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BO_input_materialization_gate_failure_v1",
        "collection_status": collection_summary.get("status"),
        "fresh_raw_completed_symbols": len(completed_symbols),
        "fresh_raw_symbols": completed_symbols,
        "us100_last_close_utc": us100.get("last_close_utc", ""),
        "available_lanes": available_lanes,
        "available_lane_count": len(available_lanes),
        "blocked_input_rows": len(blocked_rows),
        "quality_rows": len(quality_rows),
        "firewall_rows": len(firewall_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": count_passed(gate_rows),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "training": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "collection_summary": collection_summary,
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in OUTPUT_FILES],
        "raw_artifacts": [rel(path) for path in raw_artifacts],
        "no_training": True,
        "no_selection": True,
        "generated_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = build_receipts(final, collection_summary)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final) if all_gates_pass else []
    register_paths = update_registers(final) if all_gates_pass else []
    artifact_inputs = [
        *raw_artifacts,
        snapshot_path,
        inventory_path,
        quality_path,
        availability_path,
        asof_path,
        firewall_path,
        parity_path,
        blocked_path,
        queue_path,
        gate_path,
        final_path,
        manifest_path,
        *receipt_paths,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_inputs, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "collection_status": final["collection_status"],
                "us100_last_close_utc": final["us100_last_close_utc"],
                "fresh_raw_completed_symbols": final["fresh_raw_completed_symbols"],
                "available_lanes": final["available_lanes"],
                "blocked_input_rows": final["blocked_input_rows"],
                "passed_gates": final["passed_gates"],
                "gate_rows": final["gate_rows"],
                "artifact_registry": rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
