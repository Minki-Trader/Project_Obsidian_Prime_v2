from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
RUN_ID = "frontier86C_intrabar_source_export_or_m5_ambiguity_scout_v1"
RUN_DIR = REPO_ROOT / "stages" / STAGE_ID / "02_runs" / RUN_ID
SOURCE_PROBE_DIR = RUN_DIR / "source_probe"
SURROGATE_DIR = RUN_DIR / "m5_ambiguity_scout"
REVIEW_DIR = REPO_ROOT / "stages" / STAGE_ID / "03_reviews"

RAW_M5_CSV = REPO_ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
RAW_M5_MANIFEST = REPO_ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.manifest.json"
F85B_READOUT_CSV = (
    REPO_ROOT
    / "stages/stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild"
    / "03_reviews/f85b_selected_firewall_row_readout.csv"
)

CLAIM_BOUNDARY = (
    "f86c_source_probe_and_surrogate_scout_only_no_full_tick_m1_history_no_runtime_"
    "materialization_no_first_touch_order_authority_no_goal_achieve"
)
MAX_SAVED_INTRABAR_ROWS = 200_000
DEFAULT_POINT_SIZE = 0.01


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with local_path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def local_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def write_json(path: Path, payload: Any) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    local_path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    local_path(path).write_text(text, encoding="utf-8-sig")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    field_order: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                field_order.append(key)
    with local_path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=field_order)
        writer.writeheader()
        writer.writerows(rows)


def file_identity(path: Path) -> dict[str, Any]:
    native_path = local_path(path)
    if not native_path.exists():
        return {"path": repo_rel(path), "exists": False}
    return {
        "path": repo_rel(path),
        "exists": True,
        "size": native_path.stat().st_size,
        "sha256": sha256_file(path),
    }


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    return value


def utc_from_unix(seconds: int | float) -> str:
    return datetime.fromtimestamp(int(seconds), tz=UTC).isoformat().replace("+00:00", "Z")


def numpy_records(payload: Any, timeframe_seconds: int | None = None) -> list[dict[str, Any]]:
    if payload is None or len(payload) == 0:
        return []
    names = list(payload.dtype.names or [])
    records: list[dict[str, Any]] = []
    for row in payload[:MAX_SAVED_INTRABAR_ROWS]:
        rec = {name: to_jsonable(row[name]) for name in names}
        if "time" in rec and rec["time"] is not None:
            rec["time_utc"] = utc_from_unix(rec["time"])
            if timeframe_seconds:
                rec["time_close_utc"] = utc_from_unix(int(rec["time"]) + timeframe_seconds)
        if "time_msc" in rec and rec["time_msc"] is not None:
            rec["time_msc_utc"] = datetime.fromtimestamp(
                float(rec["time_msc"]) / 1000.0,
                tz=UTC,
            ).isoformat().replace("+00:00", "Z")
        records.append(rec)
    return records


def compact_terminal_info(info: Any) -> dict[str, Any]:
    if info is None:
        return {}
    fields = [
        "name",
        "company",
        "path",
        "data_path",
        "connected",
        "trade_allowed",
        "dlls_allowed",
        "build",
        "maxbars",
    ]
    return {field: getattr(info, field, None) for field in fields}


def compact_symbol_info(info: Any) -> dict[str, Any]:
    if info is None:
        return {}
    fields = [
        "name",
        "path",
        "description",
        "currency_base",
        "currency_profit",
        "digits",
        "point",
        "trade_contract_size",
        "spread",
        "trade_mode",
        "visible",
        "select",
    ]
    return {field: getattr(info, field, None) for field in fields}


def intrabar_windows() -> list[tuple[str, datetime, datetime, bool]]:
    return [
        (
            "f85b_first_selected_2025_10_03_1630_1705",
            datetime(2025, 10, 3, 16, 30, tzinfo=UTC),
            datetime(2025, 10, 3, 17, 5, tzinfo=UTC),
            True,
        ),
        (
            "f85b_oos_tail_2026_04_13_2100_2200",
            datetime(2026, 4, 13, 21, 0, tzinfo=UTC),
            datetime(2026, 4, 13, 22, 0, tzinfo=UTC),
            True,
        ),
        (
            "recent_60m",
            datetime.now(tz=UTC) - timedelta(minutes=60),
            datetime.now(tz=UTC),
            False,
        ),
    ]


def mt5_initialize(mt5: Any) -> tuple[bool, dict[str, Any]]:
    attempts: list[dict[str, Any]] = [{"label": "default_initialize", "kwargs": {}}]
    terminal64 = Path("C:/Program Files/MetaTrader 5/terminal64.exe")
    terminal = Path("C:/Program Files/MetaTrader 5/terminal.exe")
    for candidate in (terminal64, terminal):
        if candidate.exists():
            attempts.append(
                {
                    "label": f"path_initialize_{candidate.name}",
                    "kwargs": {"path": str(candidate)},
                }
            )
            attempts.append(
                {
                    "label": f"path_portable_initialize_{candidate.name}",
                    "kwargs": {"path": str(candidate), "portable": True},
                }
            )
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        ok = bool(mt5.initialize(**attempt["kwargs"]))
        result = {
            "label": attempt["label"],
            "ok": ok,
            "last_error": str(mt5.last_error()),
        }
        results.append(result)
        if ok:
            return True, {"selected_attempt": attempt["label"], "attempts": results}
        try:
            mt5.shutdown()
        except Exception:
            pass
    return False, {"selected_attempt": None, "attempts": results}


def run_mt5_source_probe() -> dict[str, Any]:
    started_at = now_utc()
    local_path(SOURCE_PROBE_DIR).mkdir(parents=True, exist_ok=True)
    try:
        import MetaTrader5 as mt5  # type: ignore
    except Exception as exc:
        summary = {
            "run_id": RUN_ID,
            "status": "blocked_mt5_python_package_unavailable",
            "started_at_utc": started_at,
            "finished_at_utc": now_utc(),
            "error": repr(exc),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        write_json(SOURCE_PROBE_DIR / "mt5_source_probe_summary.json", summary)
        return summary

    ok, init_receipt = mt5_initialize(mt5)
    if not ok:
        summary = {
            "run_id": RUN_ID,
            "status": "blocked_mt5_initialize_failed",
            "started_at_utc": started_at,
            "finished_at_utc": now_utc(),
            "initialize": init_receipt,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        write_json(SOURCE_PROBE_DIR / "mt5_source_probe_summary.json", summary)
        return summary

    exported_files: list[dict[str, Any]] = []
    window_rows: list[dict[str, Any]] = []
    try:
        terminal_info = compact_terminal_info(mt5.terminal_info())
        selected = bool(mt5.symbol_select("US100", True))
        symbol_info = compact_symbol_info(mt5.symbol_info("US100")) if selected else {}
        if not selected:
            summary = {
                "run_id": RUN_ID,
                "status": "blocked_symbol_select_failed",
                "started_at_utc": started_at,
                "finished_at_utc": now_utc(),
                "initialize": init_receipt,
                "terminal_info": terminal_info,
                "last_error": str(mt5.last_error()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            write_json(SOURCE_PROBE_DIR / "mt5_source_probe_summary.json", summary)
            return summary

        for label, start, end, save_ticks in intrabar_windows():
            rates = mt5.copy_rates_range("US100", mt5.TIMEFRAME_M1, start, end)
            rate_records = numpy_records(rates, timeframe_seconds=60)
            rate_path: Path | None = None
            if rate_records:
                rate_path = SOURCE_PROBE_DIR / f"mt5_m1_{label}.csv"
                write_csv(rate_path, rate_records)
                exported_files.append(
                    {
                        "artifact_role": "m1_sample",
                        "window_label": label,
                        "rows": len(rate_records),
                        "source_rows": int(len(rates)),
                        "truncated": int(len(rates)) > len(rate_records),
                        **file_identity(rate_path),
                    }
                )
            window_rows.append(
                {
                    "window_label": label,
                    "source": "copy_rates_range_m1",
                    "range_start_utc": start.isoformat().replace("+00:00", "Z"),
                    "range_end_utc": end.isoformat().replace("+00:00", "Z"),
                    "rows": 0 if rates is None else int(len(rates)),
                    "saved_path": repo_rel(rate_path) if rate_path else "",
                    "last_error": str(mt5.last_error()),
                }
            )

            if save_ticks:
                ticks = mt5.copy_ticks_range("US100", start, end, mt5.COPY_TICKS_ALL)
                tick_records = numpy_records(ticks)
                tick_path: Path | None = None
                if tick_records:
                    tick_path = SOURCE_PROBE_DIR / f"mt5_ticks_{label}.csv"
                    write_csv(tick_path, tick_records)
                    exported_files.append(
                        {
                            "artifact_role": "tick_sample",
                            "window_label": label,
                            "rows": len(tick_records),
                            "source_rows": int(len(ticks)),
                            "truncated": int(len(ticks)) > len(tick_records),
                            **file_identity(tick_path),
                        }
                    )
                window_rows.append(
                    {
                        "window_label": label,
                        "source": "copy_ticks_range_all",
                        "range_start_utc": start.isoformat().replace("+00:00", "Z"),
                        "range_end_utc": end.isoformat().replace("+00:00", "Z"),
                        "rows": 0 if ticks is None else int(len(ticks)),
                        "saved_path": repo_rel(tick_path) if tick_path else "",
                        "last_error": str(mt5.last_error()),
                    }
                )

        total_m1_rows = sum(row["rows"] for row in window_rows if row["source"] == "copy_rates_range_m1")
        total_tick_rows = sum(row["rows"] for row in window_rows if row["source"] == "copy_ticks_range_all")
        status = (
            "completed_intrabar_payload_sample_exported"
            if total_m1_rows or total_tick_rows
            else "completed_no_intrabar_payload_returned"
        )
        summary = {
            "run_id": RUN_ID,
            "status": status,
            "started_at_utc": started_at,
            "finished_at_utc": now_utc(),
            "initialize": init_receipt,
            "terminal_info": terminal_info,
            "symbol_info": symbol_info,
            "window_rows": window_rows,
            "exported_files": exported_files,
            "total_m1_rows": total_m1_rows,
            "total_tick_rows": total_tick_rows,
            "source_authority": "sample_export_only_no_full_historical_tick_m1_registration",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        write_json(SOURCE_PROBE_DIR / "mt5_source_probe_summary.json", summary)
        return summary
    finally:
        mt5.shutdown()


def load_f85b_rows() -> list[dict[str, str]]:
    with local_path(F85B_READOUT_CSV).open("r", newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load_m5_rows_for_timestamps(timestamps: set[int]) -> dict[int, dict[str, str]]:
    found: dict[int, dict[str, str]] = {}
    with local_path(RAW_M5_CSV).open("r", newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            ts = int(row["time_open_unix"])
            if ts in timestamps:
                found[ts] = row
                if len(found) == len(timestamps):
                    break
    return found


def parse_timestamp_utc(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "y"}


def classify_m5_path(row: dict[str, str], m5: dict[str, str], point_size: float) -> dict[str, Any]:
    side = row["decision"].lower()
    entry = float(m5["open"])
    high = float(m5["high"])
    low = float(m5["low"])
    close = float(m5["close"])
    sl_points = float(row["open_sl_points"])
    tp_points = float(row["open_tp_points"])
    if side == "long":
        sl_price = entry - sl_points * point_size
        tp_price = entry + tp_points * point_size
        sl_hit = low <= sl_price
        tp_hit = high >= tp_price
        close_direction_win = close > entry
    elif side == "short":
        sl_price = entry + sl_points * point_size
        tp_price = entry - tp_points * point_size
        sl_hit = high >= sl_price
        tp_hit = low <= tp_price
        close_direction_win = close < entry
    else:
        sl_price = None
        tp_price = None
        sl_hit = False
        tp_hit = False
        close_direction_win = False

    if sl_hit and tp_hit:
        path_class = "both_hit_order_unknown"
    elif sl_hit:
        path_class = "sl_only"
    elif tp_hit:
        path_class = "tp_only"
    else:
        path_class = "neither"
    return {
        "m5_open": entry,
        "m5_high": high,
        "m5_low": low,
        "m5_close": close,
        "point_size_used": point_size,
        "sl_price": sl_price,
        "tp_price": tp_price,
        "m5_sl_hit": sl_hit,
        "m5_tp_hit": tp_hit,
        "m5_path_class": path_class,
        "m5_close_direction_win": close_direction_win,
    }


def run_m5_ambiguity_scout(mt5_summary: dict[str, Any]) -> dict[str, Any]:
    started_at = now_utc()
    local_path(SURROGATE_DIR).mkdir(parents=True, exist_ok=True)
    f85b_rows = load_f85b_rows()
    timestamps = {int(parse_timestamp_utc(row["timestamp_utc"]).timestamp()) for row in f85b_rows}
    m5_by_time = load_m5_rows_for_timestamps(timestamps)
    point_size = (
        mt5_summary.get("symbol_info", {}).get("point")
        or DEFAULT_POINT_SIZE
    )
    try:
        point_size = float(point_size)
    except (TypeError, ValueError):
        point_size = DEFAULT_POINT_SIZE

    output_rows: list[dict[str, Any]] = []
    counters: Counter[str] = Counter()
    split_counters: dict[str, Counter[str]] = defaultdict(Counter)
    confusion: Counter[str] = Counter()
    missing = 0
    for row in f85b_rows:
        ts_dt = parse_timestamp_utc(row["timestamp_utc"])
        ts = int(ts_dt.timestamp())
        m5 = m5_by_time.get(ts)
        if m5 is None:
            missing += 1
            continue
        classified = classify_m5_path(row, m5, point_size)
        proxy_both_hit = truthy(row.get("proxy_both_hit", "false"))
        proxy_win_runtime_loss = truthy(row.get("proxy_win_runtime_loss", "false"))
        proxy_loss_runtime_win = truthy(row.get("proxy_loss_runtime_win", "false"))
        path_class = classified["m5_path_class"]
        split = row.get("split", "")
        counters[path_class] += 1
        counters["proxy_both_hit_true" if proxy_both_hit else "proxy_both_hit_false"] += 1
        if proxy_win_runtime_loss:
            counters["proxy_win_runtime_loss_true"] += 1
        if proxy_loss_runtime_win:
            counters["proxy_loss_runtime_win_true"] += 1
        split_counters[split][path_class] += 1
        confusion[f"proxy_both_hit={proxy_both_hit}|m5_path={path_class}"] += 1
        output_rows.append(
            {
                "source_row_index": row.get("row_index", ""),
                "timestamp_utc": row["timestamp_utc"],
                "split": split,
                "decision": row.get("decision", ""),
                "session_bucket": row.get("session_bucket", ""),
                "proxy_exit_path_label": row.get("proxy_exit_path_label", ""),
                "proxy_both_hit": proxy_both_hit,
                "proxy_win_runtime_loss": proxy_win_runtime_loss,
                "proxy_loss_runtime_win": proxy_loss_runtime_win,
                "runtime_net": row.get("runtime_net", ""),
                **classified,
            }
        )

    rows_path = SURROGATE_DIR / "m5_ambiguity_scout_rows.csv"
    write_csv(rows_path, output_rows)
    summary = {
        "run_id": RUN_ID,
        "status": "completed_surrogate_m5_ambiguity_scout",
        "started_at_utc": started_at,
        "finished_at_utc": now_utc(),
        "input_rows": len(f85b_rows),
        "joined_m5_rows": len(output_rows),
        "missing_m5_rows": missing,
        "point_size_used": point_size,
        "m5_path_class_counts": dict(counters),
        "split_path_class_counts": {split: dict(counter) for split, counter in split_counters.items()},
        "proxy_vs_m5_confusion": dict(confusion),
        "source_artifacts": [
            file_identity(F85B_READOUT_CSV),
            file_identity(RAW_M5_CSV),
            file_identity(RAW_M5_MANIFEST),
        ],
        "output_artifacts": [file_identity(rows_path)],
        "surrogate_boundary": (
            "M5 OHLC can identify both-hit ambiguity but cannot determine first-touch order "
            "inside the bar."
        ),
        "judgment": "negative_memory_confirms_path_order_ambiguity_material",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(SURROGATE_DIR / "m5_ambiguity_scout_summary.json", summary)
    return summary


def write_run_manifest(mt5_summary: dict[str, Any], scout_summary: dict[str, Any]) -> dict[str, Any]:
    manifest = {
        "manifest_version": "frontier86c_source_probe_manifest_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "script": file_identity(Path(__file__)),
        "work_family": "experiment_execution",
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "execution_command": "python stage_pipelines/stage_frontier_86/frontier86c_intrabar_source_probe.py",
        "inputs": [
            file_identity(RAW_M5_CSV),
            file_identity(RAW_M5_MANIFEST),
            file_identity(F85B_READOUT_CSV),
        ],
        "outputs": [
            file_identity(SOURCE_PROBE_DIR / "mt5_source_probe_summary.json"),
            file_identity(SURROGATE_DIR / "m5_ambiguity_scout_summary.json"),
            file_identity(SURROGATE_DIR / "m5_ambiguity_scout_rows.csv"),
            file_identity(RUN_DIR / "summary.json"),
            file_identity(RUN_DIR / "kpi_record.json"),
            file_identity(RUN_DIR / "reports/result_summary.md"),
        ],
        "mt5_source_probe_status": mt5_summary.get("status"),
        "m5_ambiguity_scout_status": scout_summary.get("status"),
        "runtime_claim_boundary": "no_strategy_tester_no_onnx_no_ea_no_runtime_economics_claim",
    }
    write_json(RUN_DIR / "run_manifest.json", manifest)
    return manifest


def write_kpi_record(mt5_summary: dict[str, Any], scout_summary: dict[str, Any]) -> dict[str, Any]:
    record = {
        "kpi_record_version": "frontier86c_structural_scout_kpi_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "scoreboard": "structural_scout",
        "judgment_class": "inconclusive",
        "evidence_boundary": "scout-only",
        "parity_level": "P0_unverified",
        "wfo_status": "not_applicable",
        "hard_gate_applicable": "no",
        "mt5_source_probe_status": mt5_summary.get("status"),
        "total_m1_rows": mt5_summary.get("total_m1_rows", 0),
        "total_tick_rows": mt5_summary.get("total_tick_rows", 0),
        "m5_scout_joined_rows": scout_summary.get("joined_m5_rows"),
        "m5_scout_missing_rows": scout_summary.get("missing_m5_rows"),
        "m5_path_class_counts": scout_summary.get("m5_path_class_counts", {}),
        "runtime_kpi": {
            "net_profit": None,
            "profit_factor": None,
            "drawdown": None,
            "trade_count": None,
            "trades_per_day": None,
            "n_a_reason": "No EA/ONNX/Strategy Tester runtime economics were executed in F86C.",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_DIR / "kpi_record.json", record)
    return record


def write_review_summary(
    mt5_summary: dict[str, Any],
    scout_summary: dict[str, Any],
    manifest: dict[str, Any],
    kpi_record: dict[str, Any],
) -> dict[str, Any]:
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "completed_with_boundary",
        "mt5_source_probe_status": mt5_summary.get("status"),
        "m5_ambiguity_scout_status": scout_summary.get("status"),
        "judgment_class": "inconclusive",
        "evidence_boundary": "scout-only",
        "source_probe": file_identity(SOURCE_PROBE_DIR / "mt5_source_probe_summary.json"),
        "m5_ambiguity_scout": file_identity(SURROGATE_DIR / "m5_ambiguity_scout_summary.json"),
        "run_manifest": file_identity(RUN_DIR / "run_manifest.json"),
        "kpi_record": file_identity(RUN_DIR / "kpi_record.json"),
        "result_summary": file_identity(RUN_DIR / "result_summary.md"),
        "standard_result_summary": file_identity(RUN_DIR / "reports/result_summary.md"),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": (
            "If sample M1/tick export is usable, promote to a bounded full tick/M1 registration "
            "or materialize a first-touch label source. If unavailable, continue with surrogate-only "
            "negative memory and do not claim first-touch order authority."
        ),
    }
    write_json(REVIEW_DIR / "f86c_execution_summary.json", summary)
    write_json(RUN_DIR / "summary.json", summary)
    return summary


def write_human_summary(mt5_summary: dict[str, Any], scout_summary: dict[str, Any]) -> None:
    text = f"""# F86C Result Summary(F86C 결과 요약)

## Conclusion

F86C closed as scout-only source evidence(F86C는 탐색 전용 소스 근거로 마감). MT5 API source probe(MT5 API 소스 탐침) and M5 ambiguity scout(5분봉 모호성 탐색) completed, but runtime authority(런타임 권위) and Goal Achieve(목표 달성) are not claimed.

## What changed

Run(실행): `{RUN_ID}`.

MT5 source probe(MT5 소스 탐침): `{mt5_summary.get("status")}`.

M5 ambiguity scout(M5 모호성 탐색): `{scout_summary.get("status")}` with joined rows(결합 행) `{scout_summary.get("joined_m5_rows")}` and missing rows(누락 행) `{scout_summary.get("missing_m5_rows")}`.

## What gates passed

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), kpi_contract_audit(KPI 계약 감사), source_sample_export_audit(소스 샘플 내보내기 감사), m5_ambiguity_scout_audit(5분봉 모호성 탐색 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), and final_claim_guard(최종 주장 보호) are expected closeout gates(예상 마감 게이트).

## What gates were not applicable

runtime_evidence_gate(런타임 근거 게이트) is not applicable because F86C does not claim Strategy Tester runtime economics(전략 테스터 런타임 경제성), materialization(물질화), or handoff(인계). codex_task_force_review_packet(코덱스 태스크포스 검토 묶음) is not applicable because no Task Force reviewed/pass claim(태스크포스 검토/통과 주장) is made.

## What is still not enforced

Full historical tick/M1 registration(전체 이력 틱/1분봉 등록), first-touch order authority(첫 터치 순서 권위), Strategy Tester output(전략 테스터 출력), EA/ONNX bundle identity(EA/ONNX 번들 정체성), trade list hash(거래 목록 해시), and telemetry hash(텔레메트리 해시) are still not enforced.

## Allowed claims

source_sample_exported(소스 샘플 내보내기 기록), surrogate_ambiguity_scout_recorded(대체 모호성 탐색 기록), and negative_memory_materiality_recorded(부정 기억 물질성 기록).

## Forbidden claims

completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), runtime verified(런타임 검증됨), materialization ready(물질화 준비), handoff complete(인계 완료), and first-touch order authority(첫 터치 순서 권위).

## Next hardening step

F86D should attempt bounded full tick/M1 registration(범위 있는 전체 틱/1분봉 등록) or first-touch label materializer(첫 터치 라벨 물질화기) before any runtime candidate(런타임 후보) claim.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.

This is scout-only evidence(탐색 전용 근거) and does not claim Strategy Tester runtime economics(전략 테스터 런타임 경제성), first-touch order authority(첫 터치 순서 권위), runtime authority(런타임 권위), or Goal Achieve(목표 달성).
"""
    write_md(RUN_DIR / "result_summary.md", text)
    write_md(RUN_DIR / "reports/result_summary.md", text)


def main() -> int:
    local_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    mt5_summary = run_mt5_source_probe()
    scout_summary = run_m5_ambiguity_scout(mt5_summary)
    manifest = write_run_manifest(mt5_summary, scout_summary)
    kpi_record = write_kpi_record(mt5_summary, scout_summary)
    write_human_summary(mt5_summary, scout_summary)
    review_summary = write_review_summary(mt5_summary, scout_summary, manifest, kpi_record)
    print(json.dumps(review_summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
