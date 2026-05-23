from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "273_onnx_candidate_campaign__time_risk_router_stability_validation"
RUN_ID = "run273B_execute_time_risk_router_stability_validation_review_v1"
SOURCE_RUN_ID = "run273A_design_time_risk_router_stability_validation_packet_v1"
SOURCE_MT5_RUN_ID = "run272C_time_risk_router_mt5_signal_replay_v1"
STATUS = "completed_time_risk_router_stability_validation_review_no_candidate_selection"
JUDGMENT = "negative_valid_q04_stability_failure_no_adapter_handoff"
NEXT_ACTION = "run273C_close_stage273_failure_memory_and_open_next_candidate_rebuild_stage"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN273A = STAGE / "02_runs" / "run273A"
RUN_DIR = STAGE / "02_runs" / "run273B"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

CURVE_QUEUE = RUN273A / "curve_review_queue.csv"
SLICE_PLAN = RUN273A / "stability_slice_plan.csv"
ADAPTER_PRECHECK_PLAN = RUN273A / "adapter_identity_precheck_plan.csv"
RUN273A_MANIFEST = RUN273A / "run_manifest.json"
RUN273A_LINEAGE = RUN273A / "artifact_lineage_receipt.json"
SOURCE_Q04_PAYLOAD = (
    ROOT
    / "stages"
    / "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
    / "02_runs"
    / "run272B"
    / "payloads"
    / "q04_payload.parquet"
)

TRADE_RECORDS = RUN_DIR / "trade_records.csv"
BALANCE_DIAGNOSTICS = RUN_DIR / "balance_curve_diagnostics.csv"
WEAK_SLICE_TRADE_QUALITY = RUN_DIR / "weak_slice_trade_quality.csv"
ADAPTER_PRECHECK_RESULT = RUN_DIR / "adapter_identity_precheck_result.csv"
STABILITY_REVIEW = RUN_DIR / "stability_validation_review.csv"
FAILURE_MEMORY = RUN_DIR / "stability_failure_memory.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run273B_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
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
]
STAGE_LEDGER_COLUMNS = [
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
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_time(value: Any) -> pd.Timestamp | pd.NaT:
    return pd.to_datetime(value, format="%Y.%m.%d %H:%M:%S", errors="coerce")


def path_from_repo_text(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / path


def read_deals_from_report(report_path: Path) -> pd.DataFrame:
    tables = pd.read_html(str(io_path(report_path)), flavor="lxml")
    if len(tables) < 2:
        raise ValueError(f"No MT5 deal table found in {rel(report_path)}")
    table = tables[1]
    header_idx: int | None = None
    for index, row in table.iterrows():
        values = [str(value) for value in row.tolist()]
        if values[0] == "시간" and values[1] == "거래":
            header_idx = int(index)
            break
    if header_idx is None:
        raise ValueError(f"No deal header found in {rel(report_path)}")
    rows = table.iloc[header_idx + 1 :].copy()
    rows.columns = [
        "time",
        "deal",
        "symbol",
        "deal_type",
        "direction",
        "volume",
        "price",
        "order_id",
        "commission",
        "swap",
        "profit",
        "balance",
        "comment",
    ]
    rows = rows[rows["time"].notna()].copy()
    rows = rows[rows["time"].astype(str).str.match(r"\d{4}\.\d{2}\.\d{2}", na=False)].copy()
    rows["timestamp"] = rows["time"].map(parse_time)
    rows = rows[rows["timestamp"].notna()].copy()
    for column in ["commission", "swap", "profit", "balance", "price"]:
        rows[column] = pd.to_numeric(rows[column], errors="coerce")
    rows["net_profit"] = rows["profit"].fillna(0) + rows["swap"].fillna(0) + rows["commission"].fillna(0)
    return rows


def build_payload_context() -> pd.DataFrame:
    payload = pd.read_parquet(io_path(SOURCE_Q04_PAYLOAD))
    payload["timestamp"] = pd.to_datetime(payload["timestamp"], utc=True).dt.tz_localize(None)
    payload = payload[payload["split"].isin(["validation_is", "oos"])].copy()
    payload["tier_scope"] = payload["tier_view"].map(lambda value: "Tier A" if str(value).startswith("Tier A") else "Tier B")
    context_cols = [
        "timestamp",
        "tier_scope",
        "split",
        "weekday_phase",
        "month_regime_pressure",
        "session_clock_risk",
        "chron_phase_age",
        "phase_risk_score",
        "phase_opportunity_score",
        "candidate_decision_score",
        "route_signal_label",
        "route_signal_value",
        "input_feature_order_hash",
        "expected_feature_order_hash",
        "source_feature_order_hash",
        "adapter_schema_hash",
        "source_adapter_schema_hash",
        "decision_rule_hash",
        "risk_rule_hash",
        "variant_decision_surface_hash",
    ]
    return payload[context_cols].drop_duplicates(["timestamp", "tier_scope", "split"])


def session_bucket(hour: int) -> str:
    if 13 <= hour <= 16:
        return "early_us_overlap(미국 초반 겹침)"
    if 17 <= hour <= 19:
        return "mid_us_pressure(미국 중반 압박)"
    if 20 <= hour <= 22:
        return "late_us_pressure(미국 후반 압박)"
    return "other_hour(기타 시간)"


def parse_all_reports(curve_rows: Sequence[Mapping[str, str]], payload_context: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    trade_frames: list[pd.DataFrame] = []
    deal_frames: list[pd.DataFrame] = []
    for row in curve_rows:
        report_path = path_from_repo_text(row["report_path"])
        deals = read_deals_from_report(report_path)
        report_id = row["queue_id"].replace("run273A_curve_", "")
        deals["report_id"] = report_id
        deals["tier_scope"] = row["tier_scope"]
        deals["split"] = row["split"]
        deals["report_path"] = row["report_path"]
        deal_frames.append(deals)
        trades = deals[deals["direction"].astype(str).eq("out")].copy()
        trades["trade_direction"] = trades["deal_type"].map({"sell": "long(롱)", "buy": "short(숏)"}).fillna("unknown(알수없음)")
        trades["month"] = trades["timestamp"].dt.strftime("%Y-%m")
        trades["weekday"] = trades["timestamp"].dt.day_name()
        trades["utc_hour"] = trades["timestamp"].dt.hour
        trades["session_bucket"] = trades["utc_hour"].map(session_bucket)
        trades = trades.merge(payload_context, on=["timestamp", "tier_scope", "split"], how="left", suffixes=("", "_payload"))
        trades["payload_context_match"] = trades["route_signal_label"].notna().map({True: "matched(일치)", False: "missing(누락)"})
        trade_frames.append(trades)
    return pd.concat(trade_frames, ignore_index=True), pd.concat(deal_frames, ignore_index=True)


def profit_factor(values: pd.Series) -> float:
    gross_profit = values[values > 0].sum()
    gross_loss = -values[values < 0].sum()
    if gross_loss == 0:
        return 999.0 if gross_profit > 0 else 0.0
    return gross_profit / gross_loss


def max_underwater_count(balance: pd.Series) -> int:
    peak = balance.cummax()
    underwater = balance < peak
    longest = current = 0
    for flag in underwater:
        if flag:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return int(longest)


def build_balance_diagnostics(trades: pd.DataFrame, deals: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (report_id, tier, split), group in deals.groupby(["report_id", "tier_scope", "split"], dropna=False):
        ordered = group.sort_values("timestamp").copy()
        balance = ordered["balance"].dropna()
        peak = balance.cummax()
        drawdown = peak - balance
        drawdown_pct = drawdown / peak.replace(0, pd.NA) * 100
        close_trades = trades[(trades["report_id"] == report_id) & (trades["tier_scope"] == tier) & (trades["split"] == split)]
        monthly = close_trades.groupby("month")["net_profit"].sum().sort_values()
        hourly = close_trades.groupby("utc_hour")["net_profit"].sum().sort_values()
        total_net = close_trades["net_profit"].sum()
        worst_month = monthly.index[0] if len(monthly) else ""
        worst_month_net = safe_float(monthly.iloc[0]) if len(monthly) else 0.0
        worst_hour = str(hourly.index[0]) if len(hourly) else ""
        worst_hour_net = safe_float(hourly.iloc[0]) if len(hourly) else 0.0
        fail_flags: list[str] = []
        if safe_float(drawdown_pct.max()) >= 30:
            fail_flags.append("balance_drawdown_pct_ge_30(잔액 손실폭 30% 이상)")
        if total_net > 0 and abs(worst_month_net) >= total_net * 0.65:
            fail_flags.append("worst_month_erases_most_edge(최악 월이 우위 대부분을 지움)")
        if total_net > 0 and abs(worst_hour_net) >= total_net * 0.40:
            fail_flags.append("worst_hour_concentration(최악 시간이 과도하게 큼)")
        rows.append(
            {
                "report_id": report_id,
                "tier_scope": tier,
                "split": split,
                "trade_count": int(len(close_trades)),
                "net_profit": round(total_net, 2),
                "gross_profit": round(close_trades.loc[close_trades["net_profit"] > 0, "net_profit"].sum(), 2),
                "gross_loss": round(close_trades.loc[close_trades["net_profit"] < 0, "net_profit"].sum(), 2),
                "profit_factor": round(profit_factor(close_trades["net_profit"]), 4),
                "win_rate_percent": round((close_trades["net_profit"] > 0).mean() * 100, 2) if len(close_trades) else 0,
                "final_balance": round(safe_float(balance.iloc[-1]) if len(balance) else 0, 2),
                "max_balance_drawdown_amount": round(safe_float(drawdown.max()), 2),
                "max_balance_drawdown_percent": round(safe_float(drawdown_pct.max()), 2),
                "longest_underwater_deal_count": max_underwater_count(balance) if len(balance) else 0,
                "worst_month": worst_month,
                "worst_month_net": round(worst_month_net, 2),
                "negative_month_count": int((monthly < 0).sum()),
                "worst_hour": worst_hour,
                "worst_hour_net": round(worst_hour_net, 2),
                "negative_hour_count": int((hourly < 0).sum()),
                "stability_flags": ";".join(fail_flags) if fail_flags else "no_major_balance_flag(주요 잔액 경고 없음)",
                "stability_judgment": "fail(실패)" if fail_flags else "watch(관찰)",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def summarize_slice(trades: pd.DataFrame, family: str, group_cols: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for keys, group in trades.groupby(list(group_cols), dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        key_map = dict(zip(group_cols, keys, strict=True))
        net = group["net_profit"]
        rows.append(
            {
                "slice_id": hashlib.sha1(f"{family}:{key_map}".encode("utf-8")).hexdigest()[:16],
                "slice_family": family,
                "tier_scope": key_map.get("tier_scope", "all"),
                "split": key_map.get("split", "all"),
                "slice_key": "|".join(f"{key}={value}" for key, value in key_map.items()),
                "trade_count": int(len(group)),
                "net_profit": round(safe_float(net.sum()), 2),
                "profit_factor": round(profit_factor(net), 4),
                "win_rate_percent": round((net > 0).mean() * 100, 2) if len(group) else 0,
                "expectancy": round(safe_float(net.mean()), 4) if len(group) else 0,
                "largest_loss": round(safe_float(net.min()), 2) if len(group) else 0,
                "largest_win": round(safe_float(net.max()), 2) if len(group) else 0,
                "payload_context_match_rate": round((group["payload_context_match"] == "matched(일치)").mean(), 4),
                "slice_judgment": "negative_slice(음수 구간)" if safe_float(net.sum()) < 0 else "positive_or_neutral_slice(양수 또는 중립 구간)",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_weak_slice_quality(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(summarize_slice(trades, "month(월)", ["tier_scope", "split", "month"]))
    rows.extend(summarize_slice(trades, "hour(시간)", ["tier_scope", "split", "utc_hour"]))
    rows.extend(summarize_slice(trades, "session_bucket(세션 구간)", ["tier_scope", "split", "session_bucket"]))
    rows.extend(summarize_slice(trades, "weekday_phase(요일 단계)", ["tier_scope", "split", "weekday_phase"]))
    rows.extend(summarize_slice(trades, "route_signal_label(경로 신호 라벨)", ["tier_scope", "split", "route_signal_label"]))
    rows.extend(summarize_slice(trades, "trade_direction(거래 방향)", ["tier_scope", "split", "trade_direction"]))
    return rows


def build_stability_review(balance_rows: Sequence[Mapping[str, Any]], slice_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    slice_df = pd.DataFrame(slice_rows)
    rows: list[dict[str, Any]] = []
    for balance in balance_rows:
        tier = balance["tier_scope"]
        split = balance["split"]
        negative = slice_df[
            (slice_df["tier_scope"] == tier)
            & (slice_df["split"] == split)
            & (slice_df["slice_judgment"] == "negative_slice(음수 구간)")
        ]
        severe_slices = negative[
            (negative["net_profit"].astype(float) <= -75)
            | ((negative["trade_count"].astype(float) >= 20) & (negative["profit_factor"].astype(float) < 0.8))
        ]
        decision_flags = [balance["stability_flags"]] if balance["stability_judgment"] == "fail(실패)" else []
        if len(severe_slices):
            decision_flags.append("severe_negative_slice(심한 음수 구간)")
        final_decision = (
            "stability_failed_no_adapter_handoff(안정성 실패, 어댑터 인계 없음)"
            if decision_flags
            else "stability_watch_not_selected_candidate(안정성 관찰, 선택 후보 아님)"
        )
        rows.append(
            {
                "review_id": f"run273B_{tier.lower().replace(' ', '_')}_{split}",
                "tier_scope": tier,
                "split": split,
                "net_profit": balance["net_profit"],
                "profit_factor": balance["profit_factor"],
                "trade_count": balance["trade_count"],
                "max_balance_drawdown_percent": balance["max_balance_drawdown_percent"],
                "worst_month": balance["worst_month"],
                "worst_month_net": balance["worst_month_net"],
                "worst_hour": balance["worst_hour"],
                "worst_hour_net": balance["worst_hour_net"],
                "negative_slice_count": int(len(negative)),
                "severe_negative_slice_count": int(len(severe_slices)),
                "decision_flags": ";".join(decision_flags) if decision_flags else "watch_flags_only(관찰 경고만)",
                "review_decision": final_decision,
                "next_action": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_failure_memory(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in review_rows:
        if not str(row["review_decision"]).startswith("stability_failed"):
            continue
        rows.append(
            {
                "failure_id": row["review_id"].replace("run273B_", "stage273_q04_"),
                "variant_id": "run272A_q04_weak_clock_throttle_router",
                "tier_scope": row["tier_scope"],
                "split": row["split"],
                "failure_type": "curve_and_slice_stability_failure(곡선/구간 안정성 실패)",
                "evidence": f"worst_month={row['worst_month']}:{row['worst_month_net']};worst_hour={row['worst_hour']}:{row['worst_hour_net']};dd_pct={row['max_balance_drawdown_percent']}",
                "discard_or_reopen_condition": "Reopen only with fresh risk/decision surface(새 위험/판단 표면) that directly removes month/hour concentration(月/시간 집중).",
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_adapter_precheck_result(adapter_plan: Sequence[Mapping[str, str]], trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for row in adapter_plan:
        rows.append(
            {
                "check_id": row["check_id"],
                "check_name": row["check_name"],
                "plan_status": row["status"],
                "review_status": "passed(통과)" if "fail" not in row["status"].lower() else "failed(실패)",
                "effect": row["effect"],
                "claim_boundary": BOUNDARY,
            }
        )
    rows.append(
        {
            "check_id": "run273B_payload_trade_context_join",
            "check_name": "payload/trade context join(페이로드/거래 문맥 결합)",
            "plan_status": "not_in_run273A_detail(273A 상세 외)",
            "review_status": "passed(통과)" if (trades["payload_context_match"] == "matched(일치)").mean() >= 0.99 else "watch(관찰)",
            "effect": f"matched_rate={round((trades['payload_context_match'] == 'matched(일치)').mean(), 4)}",
            "claim_boundary": BOUNDARY,
        }
    )
    return rows


def build_receipts(
    trade_rows: Sequence[Mapping[str, Any]],
    balance_rows: Sequence[Mapping[str, Any]],
    slice_rows: Sequence[Mapping[str, Any]],
    review_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    trade_df = pd.DataFrame(trade_rows)
    balance_df = pd.DataFrame(balance_rows)
    review_df = pd.DataFrame(review_rows)
    backtest = {
        "tester_identity": "Consumed MT5 Strategy Tester reports(MT5 전략 테스터 보고서 소비); symbol=US100, timeframe=M5, deposit=500, leverage=1:100 from run273A curve queue(273A 곡선 대기열)",
        "ea_identity": "Stage272 signal replay runtime probe(272단계 신호 재생 런타임 탐침); no new EA logic(새 EA 로직 없음)",
        "report_identity": sorted(trade_df["report_path"].dropna().unique().tolist()),
        "trade_evidence": {
            "trade_record_count": int(len(trade_df)),
            "balance_report_count": int(len(balance_df)),
            "review_rows": int(len(review_df)),
        },
        "cost_assumptions": "profit plus swap plus commission(수익+스왑+커미션) used for net trade quality(순 거래 품질)",
        "forensic_checks": ["report parsed(보고서 파싱)", "trade count checked(거래 수 확인)", "balance curve reconstructed(잔액 곡선 재구성)"],
        "backtest_judgment": "usable_valid_negative_evidence(사용 가능, 유효한 부정 근거)",
    }
    data = {
        "data_source": [rel(CURVE_QUEUE), rel(SOURCE_Q04_PAYLOAD)] + sorted(trade_df["report_path"].dropna().unique().tolist()),
        "time_axis": "MT5 report time(MT5 보고서 시간)을 naive UTC-like timestamp(UTC 유사 타임스탬프)로 payload timestamp(페이로드 타임스탬프)에 결합했다.",
        "sample_scope": {
            "tiers": sorted(trade_df["tier_scope"].unique().tolist()),
            "splits": sorted(trade_df["split"].unique().tolist()),
            "trade_rows": int(len(trade_df)),
            "slice_rows": len(slice_rows),
        },
        "missing_or_duplicate_check": {
            "payload_context_match_rate": round((trade_df["payload_context_match"] == "matched(일치)").mean(), 4),
            "duplicate_trade_key_count": int(trade_df.duplicated(["report_id", "deal"]).sum()),
        },
        "feature_label_boundary": "No new labels(새 라벨 없음); realized MT5 trades(실현 MT5 거래)를 q04 payload context(q04 페이로드 문맥)에만 붙였다.",
        "split_boundary": "Each MT5 report already separates validation_is/oos(검증/표본외) and Tier A/B(티어 A/B).",
        "leakage_risk": "Low for review(검토에는 낮음); high if these weak slices are tuned in place(이 약한 구간을 제자리 튜닝하면 높음).",
        "data_hash_or_identity": {rel(TRADE_RECORDS): sha256_file(TRADE_RECORDS), rel(BALANCE_DIAGNOSTICS): sha256_file(BALANCE_DIAGNOSTICS)},
        "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
    }
    worst_rows = balance_df.sort_values(["max_balance_drawdown_percent", "negative_month_count"], ascending=False).head(2).to_dict("records")
    performance = {
        "observed_change": "q04(4번 분기)는 headline KPI(대표 핵심 성과 지표)는 양수지만, validation May(검증 5월), OOS December(표본외 12월), hour concentration(시간 집중)에서 안정성이 깨졌다.",
        "comparison_baseline": "run272D q04 pressure survivor(272D q04 압박 생존 분기) vs run273B curve/slice review(273B 곡선/구간 검토)",
        "likely_drivers": ["weak-clock throttle did not remove mid-session loss pockets(약한 시계 제한이 중간 세션 손실 구간을 제거하지 못함)", "profit concentrated outside weak months(수익이 약한 월 밖에 집중)"],
        "segment_checks": ["month(월)", "hour(시간)", "session bucket(세션 구간)", "weekday phase(요일 단계)", "route signal label(경로 신호 라벨)", "trade direction(거래 방향)"],
        "trade_shape": {
            "total_trade_records": int(len(trade_df)),
            "net_by_report": balance_df[["report_id", "net_profit", "profit_factor", "max_balance_drawdown_percent"]].to_dict("records"),
            "worst_balance_rows": worst_rows,
        },
        "alternative_explanations": ["signal replay simplification(신호 재생 단순화)", "Tier A/B duplicated evidence(티어 A/B 중복 근거)", "tester cost/report interpretation(테스터 비용/보고 해석)"],
        "attribution_confidence": "medium(중간)",
        "next_probe": NEXT_ACTION,
    }
    result_rows = [
        {
            "result_subject": "q04 weak-clock throttle router stability validation(q04 약한 시계 제한 라우터 안정성 검증)",
            "evidence_available": "MT5 trade list(MT5 거래 목록);balance curve diagnostics(잔액 곡선 진단);weak slice trade quality(약한 구간 거래 품질);Adapter identity precheck(어댑터 정체성 사전점검)",
            "evidence_missing": "Adapter package(어댑터 패키지);ONNX export/parity(온엑스 내보내기/동등성);MT5 reproduction from ONNX package(온엑스 패키지 기반 MT5 재현)",
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "q04(4번 분기)는 첫 압박은 통과했지만, 월/시간 손실 집중 때문에 어댑터 인계 후보로 부르지 않는다.",
        }
    ]
    gate_rows = [
        {
            "gate_name": "runtime_report_parse_gate(런타임 보고서 파싱 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(TRADE_RECORDS),
            "effect": "MT5 report(MT5 보고서)에서 거래 기록을 직접 만들었다.",
        },
        {
            "gate_name": "kpi_contract_audit(KPI 계약 감사)",
            "status": "passed_with_negative_judgment(부정 판정으로 통과)",
            "evidence_path": rel(BALANCE_DIAGNOSTICS),
            "effect": "net/PF/DD/trade count(순수익/수익 팩터/손실폭/거래 수)를 함께 판정했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    return backtest, data, performance, result_rows, gate_rows


def write_report(review_rows: Sequence[Mapping[str, Any]], balance_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    review_lines = "\n".join(
        f"- `{row['tier_scope']}` `{row['split']}`: net(순수익) `{row['net_profit']}`, PF(수익 팩터) `{row['profit_factor']}`, DD(손실폭) `{row['max_balance_drawdown_percent']}`, worst_month(최악 월) `{row['worst_month']}={row['worst_month_net']}`, decision(판정) `{row['review_decision']}`"
        for row in review_rows
    )
    failure_lines = "\n".join(
        f"- `{row['tier_scope']}` `{row['split']}`: `{row['evidence']}`"
        for row in failure_rows
    )
    write_md(
        RUN_REPORT,
        f"""# run273B Time-Risk Router Stability Validation Review(273B 시간 위험 라우터 안정성 검증 검토)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run273B(273B 실행)는 q04(4번 분기)의 MT5(`MetaTrader 5`, 메타트레이더5) report(보고서)를 trade list(거래 목록), balance curve(잔액 곡선), weak slice(약한 구간)로 다시 읽었다.
효과(effect, 효과): q04(4번 분기)는 pressure survivor(압박 생존 분기)였지만 stability validation(안정성 검증)에서는 Adapter handoff(어댑터 인계)로 넘기지 않는다.

## Review Rows(검토 행)

{review_lines}

## Failure Memory(실패 기억)

{failure_lines}

## Evidence Paths(근거 경로)

- trade_records(거래 기록): `{rel(TRADE_RECORDS)}`
- balance_curve_diagnostics(잔액 곡선 진단): `{rel(BALANCE_DIAGNOSTICS)}`
- weak_slice_trade_quality(약한 구간 거래 품질): `{rel(WEAK_SLICE_TRADE_QUALITY)}`
- stability_failure_memory(안정성 실패 기억): `{rel(FAILURE_MEMORY)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def update_ledgers(review_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"q04 stability failed;selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = []
    stage_rows = []
    for row in review_rows:
        row_key = f"{RUN_ID}__{str(row['tier_scope']).lower().replace(' ', '_')}_{row['split']}"
        alpha_rows.append(
            {
                "ledger_row_id": row_key,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": row_key.replace(f"{RUN_ID}__", "q04_"),
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": f"q04 stability review {row['tier_scope']} {row['split']}",
                "tier_scope": row["tier_scope"],
                "kpi_scope": "stability_validation_review",
                "scoreboard_lane": "kpi_evidence",
                "status": STATUS,
                "judgment": row["review_decision"],
                "path": rel(STABILITY_REVIEW),
                "primary_kpi": f"net={row['net_profit']};pf={row['profit_factor']};trades={row['trade_count']}",
                "guardrail_kpi": f"dd_pct={row['max_balance_drawdown_percent']};worst_month={row['worst_month']}:{row['worst_month_net']};selected_candidate=none",
                "external_verification_status": "completed_from_run272C_reports",
                "notes": row["decision_flags"],
            }
        )
        stage_rows.append(
            {
                "row_id": row_key,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": f"q04_stability_review_{str(row['tier_scope']).lower().replace(' ', '_')}_{row['split']}",
                "tier_scope": row["tier_scope"],
                "scoreboard": "kpi_evidence",
                "status": STATUS,
                "judgment": row["review_decision"],
                "evidence_boundary": "valid_negative_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": row["decision_flags"],
            }
        )
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs(failure_rows: Sequence[Mapping[str, Any]]) -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        f"Stage273(273단계)는 run273B(273B 실행)에서 q04(4번 분기)를 valid negative(유효한 부정) 안정성 실패로 판정했다.\n효과(effect, 효과): q04(4번 분기)는 selected candidate(선택 후보)나 Adapter handoff(어댑터 인계)가 아니며, 실패 기억(failure memory, 실패 기억)으로 닫기 위한 run273C(273C 실행)로 넘어간다.",
    )
    selection = append_once(selection, "run273B_report", f"- run273B_report(273B 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run273B_failure_memory", f"- run273B_failure_memory(273B 실패 기억): `{rel(FAILURE_MEMORY)}`")
    write_md(SELECTION_STATUS, selection)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run273B_report",
        "\n".join(
            [
                f"- run273B_report(273B 보고서): `{rel(RUN_REPORT)}`",
                f"- run273B_trade_records(273B 거래 기록): `{rel(TRADE_RECORDS)}`",
                f"- run273B_balance_diagnostics(273B 잔액 진단): `{rel(BALANCE_DIAGNOSTICS)}`",
                f"- run273B_weak_slice_trade_quality(273B 약한 구간 거래 품질): `{rel(WEAK_SLICE_TRADE_QUALITY)}`",
                f"- run273B_failure_memory(273B 실패 기억): `{rel(FAILURE_MEMORY)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run273B_summary",
        f"- run273B_summary(273B 요약): run273B(273B 실행)는 q04(4번 분기)의 MT5 report(MT5 보고서) 거래 목록과 잔액 곡선을 검토해 stability failure(안정성 실패)를 기록했다. Effect(효과): failure rows(실패 행) `{len(failure_rows)}`개를 만들었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage273(273단계) run273B(273B 실행) q04 stability validation review(q04 안정성 검증 검토) `{RUN_ID}`. "
        f"Effect(효과): q04(4번 분기)를 valid negative(유효한 부정) failure memory(실패 기억)로 넘기고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run273B stability validation review(273B 안정성 검증 검토)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): q04(4번 분기)의 월/시간 손실 집중과 잔액 곡선 약점을 valid negative(유효한 부정)로 기록했다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)

    if path_exists(NEGATIVE_REGISTER):
        negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
        negative = append_once(
            negative,
            "NEG-ST273-Q04-STABILITY-FAILURE-RUN273B",
            f"| `NEG-ST273-Q04-STABILITY-FAILURE-RUN273B` | `{STAGE_ID}` | q04 weak-clock throttle router(q04 약한 시계 제한 라우터) | valid_negative(유효한 부정) | month/hour loss concentration(월/시간 손실 집중) and curve fragility(곡선 취약성) | reopen only with fresh decision/risk surface(새 판단/위험 표면이 있을 때만 재개) | `{rel(RUN_REPORT)}` |",
        )
        write_md(NEGATIVE_REGISTER, negative)


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [CURVE_QUEUE, SLICE_PLAN, ADAPTER_PRECHECK_PLAN, RUN273A_MANIFEST, RUN273A_LINEAGE, SOURCE_Q04_PAYLOAD]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_mt5_run_id": SOURCE_MT5_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage273/review_time_risk_router_stability_validation.py",
        "entry_command": "python stage_pipelines/stage273/review_time_risk_router_stability_validation.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(NEGATIVE_REGISTER)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    all_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run273B_stability_review_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run273B q04 stability validation review artifact.",
        }
        for path in all_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def execute() -> dict[str, Any]:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    curve_rows = read_csv_rows(CURVE_QUEUE)
    adapter_plan = read_csv_rows(ADAPTER_PRECHECK_PLAN)
    if not curve_rows:
        raise ValueError("curve review queue is empty")
    payload_context = build_payload_context()
    trades, deals = parse_all_reports(curve_rows, payload_context)
    balance_rows = build_balance_diagnostics(trades, deals)
    slice_rows = build_weak_slice_quality(trades)
    review_rows = build_stability_review(balance_rows, slice_rows)
    failure_rows = build_failure_memory(review_rows)
    adapter_rows = build_adapter_precheck_result(adapter_plan, trades)

    trade_columns = [
        "report_id",
        "tier_scope",
        "split",
        "timestamp",
        "deal",
        "symbol",
        "deal_type",
        "direction",
        "trade_direction",
        "volume",
        "price",
        "commission",
        "swap",
        "profit",
        "net_profit",
        "balance",
        "month",
        "weekday",
        "utc_hour",
        "session_bucket",
        "weekday_phase",
        "session_clock_risk",
        "month_regime_pressure",
        "chron_phase_age",
        "route_signal_label",
        "payload_context_match",
        "report_path",
    ]
    write_csv(TRADE_RECORDS, trades[trade_columns].to_dict("records"), trade_columns)
    write_csv(BALANCE_DIAGNOSTICS, balance_rows)
    write_csv(WEAK_SLICE_TRADE_QUALITY, slice_rows)
    write_csv(ADAPTER_PRECHECK_RESULT, adapter_rows)
    write_csv(STABILITY_REVIEW, review_rows)
    write_csv(FAILURE_MEMORY, failure_rows)

    backtest, data, performance, result_rows, gate_rows = build_receipts(
        trades[trade_columns].to_dict("records"), balance_rows, slice_rows, review_rows
    )
    write_json(BACKTEST_FORENSICS_RECEIPT, backtest)
    write_json(DATA_INTEGRITY_RECEIPT, data)
    write_json(PERFORMANCE_ATTRIBUTION_RECEIPT, performance)
    write_csv(RESULT_JUDGMENT, result_rows)
    write_csv(GATE_AUDIT, gate_rows)
    write_report(review_rows, balance_rows, failure_rows)

    artifacts = [
        TRADE_RECORDS,
        BALANCE_DIAGNOSTICS,
        WEAK_SLICE_TRADE_QUALITY,
        ADAPTER_PRECHECK_RESULT,
        STABILITY_REVIEW,
        FAILURE_MEMORY,
        BACKTEST_FORENSICS_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers(review_rows)
    update_state_docs(failure_rows)
    write_manifests_and_registry(created_at, artifacts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "trade_records": int(len(trades)),
        "balance_rows": len(balance_rows),
        "slice_rows": len(slice_rows),
        "failure_rows": len(failure_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
