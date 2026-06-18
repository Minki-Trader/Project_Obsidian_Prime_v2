from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
RUN_ID = "frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1"
RUN_DIR = REPO_ROOT / "stages" / STAGE_ID / "02_runs" / RUN_ID
SOURCE_DIR = RUN_DIR / "source_registration"
LABEL_DIR = RUN_DIR / "first_touch_labels"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = REPO_ROOT / "stages" / STAGE_ID / "03_reviews"

RAW_M5_CSV = REPO_ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
RAW_M5_MANIFEST = REPO_ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.manifest.json"
F85B_READOUT_CSV = (
    REPO_ROOT
    / "stages/stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild"
    / "03_reviews/f85b_selected_firewall_row_readout.csv"
)

CLAIM_BOUNDARY = (
    "f86d_bounded_selected_row_tick_m1_label_source_materialized_no_strategy_tester_"
    "runtime_economics_no_runtime_authority_no_goal_achieve"
)
DEFAULT_POINT_SIZE = 0.01
BAR_SECONDS = 300
M1_OFFSETS = range(5)
M1_CHUNK_DAYS = 14
TICK_SEGMENT_SAFETY_CAP = 10_000_000


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def local_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with local_path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_identity(path: Path) -> dict[str, Any]:
    native = local_path(path)
    if not native.exists():
        return {"path": repo_rel(path), "exists": False}
    return {
        "path": repo_rel(path),
        "exists": True,
        "size": native.stat().st_size,
        "sha256": sha256_file(path),
    }


def write_json(path: Path, payload: Any) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    local_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


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


def load_csv(path: Path) -> list[dict[str, str]]:
    with local_path(path).open("r", newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def parse_timestamp_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def utc_from_unix(seconds: int | float) -> str:
    return datetime.fromtimestamp(int(seconds), tz=UTC).isoformat().replace("+00:00", "Z")


def utc_from_msc(milliseconds: int | float) -> str:
    return datetime.fromtimestamp(float(milliseconds) / 1000.0, tz=UTC).isoformat().replace("+00:00", "Z")


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


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


def mt5_initialize(mt5: Any) -> tuple[bool, dict[str, Any]]:
    attempts: list[dict[str, Any]] = [{"label": "default_initialize", "kwargs": {}}]
    for candidate in (Path("C:/Program Files/MetaTrader 5/terminal64.exe"), Path("C:/Program Files/MetaTrader 5/terminal.exe")):
        if candidate.exists():
            attempts.append({"label": f"path_initialize_{candidate.name}", "kwargs": {"path": str(candidate)}})
            attempts.append({"label": f"path_portable_initialize_{candidate.name}", "kwargs": {"path": str(candidate), "portable": True}})
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        ok = bool(mt5.initialize(**attempt["kwargs"]))
        result = {"label": attempt["label"], "ok": ok, "last_error": str(mt5.last_error())}
        results.append(result)
        if ok:
            return True, {"selected_attempt": attempt["label"], "attempts": results}
        try:
            mt5.shutdown()
        except Exception:
            pass
    return False, {"selected_attempt": None, "attempts": results}


def selected_rows() -> list[dict[str, str]]:
    rows = load_csv(F85B_READOUT_CSV)
    rows.sort(key=lambda row: parse_timestamp_utc(row["timestamp_utc"]))
    return rows


def load_m5_rows(timestamps: set[int]) -> dict[int, dict[str, str]]:
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


def rate_record(row: Any) -> dict[str, Any]:
    names = list(row.dtype.names or [])
    rec = {name: to_jsonable(row[name]) for name in names}
    if rec.get("time") is not None:
        rec["time_utc"] = utc_from_unix(rec["time"])
        rec["time_close_utc"] = utc_from_unix(int(rec["time"]) + 60)
    return rec


def tick_record(row: Any) -> dict[str, Any]:
    names = list(row.dtype.names or [])
    rec = {name: to_jsonable(row[name]) for name in names}
    if rec.get("time") is not None:
        rec["time_utc"] = utc_from_unix(rec["time"])
    if rec.get("time_msc") is not None:
        rec["time_msc_utc"] = utc_from_msc(rec["time_msc"])
    return rec


def export_m1_registry(mt5: Any, rows: list[dict[str, str]]) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    timestamps = [parse_timestamp_utc(row["timestamp_utc"]) for row in rows]
    start = min(timestamps)
    end = max(timestamps) + timedelta(seconds=BAR_SECONDS)
    m1_by_time: dict[int, dict[str, Any]] = {}
    chunk_rows: list[dict[str, Any]] = []
    chunk_start = start
    while chunk_start <= end:
        chunk_end = min(chunk_start + timedelta(days=M1_CHUNK_DAYS), end)
        rates = mt5.copy_rates_range("US100", mt5.TIMEFRAME_M1, chunk_start, chunk_end)
        count = 0 if rates is None else int(len(rates))
        if rates is not None:
            for raw in rates:
                rec = rate_record(raw)
                m1_by_time[int(rec["time"])] = rec
        chunk_rows.append(
            {
                "chunk_start_utc": chunk_start.isoformat().replace("+00:00", "Z"),
                "chunk_end_utc": chunk_end.isoformat().replace("+00:00", "Z"),
                "rows": count,
                "last_error": str(mt5.last_error()),
            }
        )
        chunk_start = chunk_end + timedelta(seconds=60)

    registry_rows: list[dict[str, Any]] = []
    missing_minutes = 0
    full_rows = 0
    for row in rows:
        bar_start = parse_timestamp_utc(row["timestamp_utc"])
        row_missing = 0
        for offset in M1_OFFSETS:
            minute_ts = int((bar_start + timedelta(minutes=offset)).timestamp())
            m1 = m1_by_time.get(minute_ts)
            if m1 is None:
                row_missing += 1
                missing_minutes += 1
                registry_rows.append(
                    {
                        "source_row_index": row.get("row_index", ""),
                        "timestamp_utc": row["timestamp_utc"],
                        "m1_offset": offset,
                        "m1_time_utc": utc_from_unix(minute_ts),
                        "m1_present": False,
                    }
                )
                continue
            registry_rows.append(
                {
                    "source_row_index": row.get("row_index", ""),
                    "timestamp_utc": row["timestamp_utc"],
                    "m1_offset": offset,
                    "m1_time_utc": m1.get("time_utc"),
                    "m1_present": True,
                    "open": m1.get("open"),
                    "high": m1.get("high"),
                    "low": m1.get("low"),
                    "close": m1.get("close"),
                    "tick_volume": m1.get("tick_volume"),
                    "spread": m1.get("spread"),
                    "real_volume": m1.get("real_volume"),
                }
            )
        if row_missing == 0:
            full_rows += 1

    registry_path = SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"
    write_csv(registry_path, registry_rows)
    summary = {
        "registry_path": repo_rel(registry_path),
        "selected_input_rows": len(rows),
        "expected_m1_rows": len(rows) * len(list(M1_OFFSETS)),
        "registered_m1_rows": sum(1 for row in registry_rows if row.get("m1_present") is True),
        "missing_m1_minutes": missing_minutes,
        "selected_rows_with_full_m1_window": full_rows,
        "chunk_rows": chunk_rows,
        "artifact": file_identity(registry_path),
    }
    return m1_by_time, summary


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
        "entry_price_proxy_m5_open": entry,
        "m5_high": high,
        "m5_low": low,
        "m5_close": close,
        "sl_price": sl_price,
        "tp_price": tp_price,
        "m5_sl_hit": sl_hit,
        "m5_tp_hit": tp_hit,
        "m5_path_class": path_class,
        "m5_close_direction_win": close_direction_win,
    }


def first_touch_from_ticks(side: str, sl_price: float, tp_price: float, ticks: Any) -> tuple[str, dict[str, Any]]:
    if ticks is None or len(ticks) == 0:
        return "unresolved_tick_missing", {"tick_count": 0}
    first_sl: dict[str, Any] | None = None
    first_tp: dict[str, Any] | None = None
    for raw in ticks:
        tick = tick_record(raw)
        bid = tick.get("bid")
        ask = tick.get("ask")
        if bid is None or ask is None:
            continue
        if side == "long":
            sl_hit = float(bid) <= sl_price
            tp_hit = float(bid) >= tp_price
            price_field = "bid"
        elif side == "short":
            sl_hit = float(ask) >= sl_price
            tp_hit = float(ask) <= tp_price
            price_field = "ask"
        else:
            continue
        event = {
            "time_utc": tick.get("time_utc"),
            "time_msc_utc": tick.get("time_msc_utc"),
            "time_msc": tick.get("time_msc"),
            "bid": bid,
            "ask": ask,
            "price_field": price_field,
        }
        if sl_hit and first_sl is None:
            first_sl = event
        if tp_hit and first_tp is None:
            first_tp = event
        if first_sl is not None and first_tp is not None:
            break
    if first_sl is None and first_tp is None:
        return "unresolved_tick_no_hit", {"tick_count": int(len(ticks))}
    if first_sl is None:
        return "tp_first_tick", {"tick_count": int(len(ticks)), "first_tp": first_tp}
    if first_tp is None:
        return "sl_first_tick", {"tick_count": int(len(ticks)), "first_sl": first_sl}
    sl_time = int(first_sl.get("time_msc") or 0)
    tp_time = int(first_tp.get("time_msc") or 0)
    if sl_time < tp_time:
        return "sl_first_tick", {"tick_count": int(len(ticks)), "first_sl": first_sl, "first_tp": first_tp}
    if tp_time < sl_time:
        return "tp_first_tick", {"tick_count": int(len(ticks)), "first_sl": first_sl, "first_tp": first_tp}
    return "same_tick_both_hit", {"tick_count": int(len(ticks)), "first_sl": first_sl, "first_tp": first_tp}


def canonical_tick_line(tick: dict[str, Any]) -> bytes:
    keep = {key: tick.get(key) for key in ("time", "time_msc", "bid", "ask", "last", "volume", "flags", "volume_real")}
    return (json.dumps(keep, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def materialize_labels(mt5: Any, rows: list[dict[str, str]], point_size: float) -> dict[str, Any]:
    timestamps = {int(parse_timestamp_utc(row["timestamp_utc"]).timestamp()) for row in rows}
    m5_by_time = load_m5_rows(timestamps)
    tick_path = SOURCE_DIR / "mt5_tick_both_hit_registry.csv"
    local_path(tick_path.parent).mkdir(parents=True, exist_ok=True)
    tick_fields = [
        "source_row_index",
        "timestamp_utc",
        "decision",
        "time",
        "time_msc",
        "time_utc",
        "time_msc_utc",
        "bid",
        "ask",
        "last",
        "volume",
        "flags",
        "volume_real",
    ]

    label_rows: list[dict[str, Any]] = []
    segment_rows: list[dict[str, Any]] = []
    counters: Counter[str] = Counter()
    split_counters: dict[str, Counter[str]] = {}
    total_tick_rows = 0
    safety_cap_hit = False

    with local_path(tick_path).open("w", newline="", encoding="utf-8") as fh:
        tick_writer = csv.DictWriter(fh, fieldnames=tick_fields)
        tick_writer.writeheader()
        for index, row in enumerate(rows, start=1):
            ts_dt = parse_timestamp_utc(row["timestamp_utc"])
            ts = int(ts_dt.timestamp())
            split = row.get("split", "")
            split_counters.setdefault(split, Counter())
            m5 = m5_by_time.get(ts)
            if m5 is None:
                label = "unresolved_missing_m5"
                classified: dict[str, Any] = {"m5_path_class": "missing_m5"}
                tick_meta: dict[str, Any] = {}
            else:
                classified = classify_m5_path(row, m5, point_size)
                path_class = str(classified["m5_path_class"])
                if path_class == "sl_only":
                    label = "sl_first_m5_single_hit"
                    tick_meta = {}
                elif path_class == "tp_only":
                    label = "tp_first_m5_single_hit"
                    tick_meta = {}
                elif path_class == "neither":
                    label = "none_hit_m5"
                    tick_meta = {}
                else:
                    end = ts_dt + timedelta(seconds=BAR_SECONDS)
                    ticks = mt5.copy_ticks_range("US100", ts_dt, end, mt5.COPY_TICKS_ALL)
                    label, tick_meta = first_touch_from_ticks(
                        row["decision"].lower(),
                        float(classified["sl_price"]),
                        float(classified["tp_price"]),
                        ticks,
                    )
                    segment_hash = hashlib.sha256()
                    tick_count = 0 if ticks is None else int(len(ticks))
                    if ticks is not None:
                        for raw_tick in ticks:
                            tick = tick_record(raw_tick)
                            segment_hash.update(canonical_tick_line(tick))
                            tick_writer.writerow(
                                {
                                    "source_row_index": row.get("row_index", ""),
                                    "timestamp_utc": row["timestamp_utc"],
                                    "decision": row.get("decision", ""),
                                    **{field: tick.get(field, "") for field in tick_fields if field not in {"source_row_index", "timestamp_utc", "decision"}},
                                }
                            )
                    total_tick_rows += tick_count
                    segment_rows.append(
                        {
                            "source_row_index": row.get("row_index", ""),
                            "timestamp_utc": row["timestamp_utc"],
                            "split": split,
                            "decision": row.get("decision", ""),
                            "tick_count": tick_count,
                            "segment_sha256": segment_hash.hexdigest() if tick_count else "",
                            "label": label,
                            "last_error": str(mt5.last_error()),
                        }
                    )
                    if total_tick_rows > TICK_SEGMENT_SAFETY_CAP:
                        safety_cap_hit = True
                        counters["safety_cap_hit"] += 1
                        break

            counters[label] += 1
            split_counters[split][label] += 1
            label_rows.append(
                {
                    "source_row_index": row.get("row_index", ""),
                    "timestamp_utc": row["timestamp_utc"],
                    "split": split,
                    "decision": row.get("decision", ""),
                    "session_bucket": row.get("session_bucket", ""),
                    "proxy_win": row.get("proxy_win", ""),
                    "runtime_win_bool": row.get("runtime_win_bool", ""),
                    "proxy_win_runtime_loss": row.get("proxy_win_runtime_loss", ""),
                    "proxy_loss_runtime_win": row.get("proxy_loss_runtime_win", ""),
                    "proxy_both_hit": row.get("proxy_both_hit", ""),
                    "proxy_exit_path_label": row.get("proxy_exit_path_label", ""),
                    "first_touch_label": label,
                    "label_resolution_method": "tick_bidask" if label.endswith("_tick") or label == "same_tick_both_hit" else "m5_single_hit_or_none",
                    "tick_count": tick_meta.get("tick_count", ""),
                    "first_sl_time_msc_utc": (tick_meta.get("first_sl") or {}).get("time_msc_utc", ""),
                    "first_tp_time_msc_utc": (tick_meta.get("first_tp") or {}).get("time_msc_utc", ""),
                    **classified,
                }
            )
            if index % 250 == 0:
                print(json.dumps({"progress_rows": index, "tick_rows": total_tick_rows, "labels": dict(counters)}, sort_keys=True))

    labels_path = LABEL_DIR / "first_touch_labels.csv"
    segments_path = SOURCE_DIR / "tick_segment_identity.csv"
    write_csv(labels_path, label_rows)
    write_csv(segments_path, segment_rows)
    materialized_rows = len(label_rows)
    unresolved = sum(count for key, count in counters.items() if key.startswith("unresolved"))
    status = "completed_bounded_first_touch_label_materialized"
    if safety_cap_hit:
        status = "partial_safety_cap_hit"
    elif unresolved:
        status = "completed_with_unresolved_tick_or_m5_gaps"
    return {
        "status": status,
        "selected_input_rows": len(rows),
        "materialized_label_rows": materialized_rows,
        "unresolved_label_rows": unresolved,
        "tick_rows_registered": total_tick_rows,
        "tick_segments": len(segment_rows),
        "tick_safety_cap": TICK_SEGMENT_SAFETY_CAP,
        "safety_cap_hit": safety_cap_hit,
        "label_counts": dict(counters),
        "split_label_counts": {split: dict(counter) for split, counter in split_counters.items()},
        "first_touch_label_path": repo_rel(labels_path),
        "tick_registry_path": repo_rel(tick_path),
        "tick_segment_identity_path": repo_rel(segments_path),
        "artifacts": [file_identity(labels_path), file_identity(tick_path), file_identity(segments_path)],
    }


def run_materializer() -> dict[str, Any]:
    started_at = now_utc()
    local_path(SOURCE_DIR).mkdir(parents=True, exist_ok=True)
    local_path(LABEL_DIR).mkdir(parents=True, exist_ok=True)
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
        write_json(RUN_DIR / "summary.json", summary)
        return summary

    rows = selected_rows()
    ok, init_receipt = mt5_initialize(mt5)
    if not ok:
        summary = {
            "run_id": RUN_ID,
            "status": "blocked_mt5_initialize_failed",
            "started_at_utc": started_at,
            "finished_at_utc": now_utc(),
            "initialize": init_receipt,
            "input_rows": len(rows),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        write_json(RUN_DIR / "summary.json", summary)
        return summary

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
            write_json(RUN_DIR / "summary.json", summary)
            return summary
        point_size = symbol_info.get("point") or DEFAULT_POINT_SIZE
        try:
            point_size = float(point_size)
        except (TypeError, ValueError):
            point_size = DEFAULT_POINT_SIZE
        _, m1_summary = export_m1_registry(mt5, rows)
        label_summary = materialize_labels(mt5, rows, point_size)
        status = label_summary["status"]
        if (
            status == "completed_bounded_first_touch_label_materialized"
            and m1_summary["selected_rows_with_full_m1_window"] == len(rows)
        ):
            run_status = "completed_bounded_m1_and_first_touch_label_source_materialized"
        elif status.startswith("completed"):
            run_status = "completed_with_source_gaps_or_unresolved_labels"
        else:
            run_status = status
        summary = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "status": run_status,
            "started_at_utc": started_at,
            "finished_at_utc": now_utc(),
            "initialize": init_receipt,
            "terminal_info": terminal_info,
            "symbol_info": symbol_info,
            "point_size_used": point_size,
            "input_rows": len(rows),
            "source_rows": [file_identity(F85B_READOUT_CSV), file_identity(RAW_M5_CSV), file_identity(RAW_M5_MANIFEST)],
            "m1_summary": m1_summary,
            "label_summary": label_summary,
            "source_authority": "bounded_selected_row_tick_m1_registration",
            "runtime_claim_boundary": "no_strategy_tester_no_onnx_no_ea_no_runtime_economics_claim",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        write_json(RUN_DIR / "summary.json", summary)
        write_json(SOURCE_DIR / "source_registration_summary.json", {"m1_summary": m1_summary, "label_summary": label_summary, "claim_boundary": CLAIM_BOUNDARY})
        write_json(LABEL_DIR / "first_touch_label_summary.json", label_summary)
        return summary
    finally:
        mt5.shutdown()


def write_run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    manifest = {
        "manifest_version": "frontier86d_tick_m1_label_materializer_manifest_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "script": file_identity(Path(__file__)),
        "work_family": "experiment_execution",
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "execution_command": "python stage_pipelines/stage_frontier_86/frontier86d_tick_m1_label_materializer.py",
        "inputs": [file_identity(F85B_READOUT_CSV), file_identity(RAW_M5_CSV), file_identity(RAW_M5_MANIFEST)],
        "outputs": [
            file_identity(RUN_DIR / "summary.json"),
            file_identity(RUN_DIR / "run_manifest.json"),
            file_identity(RUN_DIR / "kpi_record.json"),
            file_identity(SOURCE_DIR / "source_registration_summary.json"),
            file_identity(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"),
            file_identity(SOURCE_DIR / "mt5_tick_both_hit_registry.csv"),
            file_identity(SOURCE_DIR / "tick_segment_identity.csv"),
            file_identity(LABEL_DIR / "first_touch_label_summary.json"),
            file_identity(LABEL_DIR / "first_touch_labels.csv"),
            file_identity(REPORT_DIR / "result_summary.md"),
        ],
        "status": summary.get("status"),
        "source_authority": summary.get("source_authority"),
        "runtime_claim_boundary": summary.get("runtime_claim_boundary"),
    }
    write_json(RUN_DIR / "run_manifest.json", manifest)
    return manifest


def write_kpi_record(summary: dict[str, Any]) -> dict[str, Any]:
    m1 = summary.get("m1_summary", {})
    labels = summary.get("label_summary", {})
    record = {
        "kpi_record_version": "frontier86d_source_materializer_kpi_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "scoreboard": "structural_scout",
        "judgment_class": "positive_source_materialization_with_boundary"
        if summary.get("status") == "completed_bounded_m1_and_first_touch_label_source_materialized"
        else "inconclusive_source_materialization_with_gaps",
        "evidence_boundary": "bounded-source-label-materializer",
        "parity_level": "P0_unverified",
        "wfo_status": "not_applicable",
        "hard_gate_applicable": "no",
        "input_rows": summary.get("input_rows"),
        "registered_m1_rows": m1.get("registered_m1_rows"),
        "selected_rows_with_full_m1_window": m1.get("selected_rows_with_full_m1_window"),
        "materialized_label_rows": labels.get("materialized_label_rows"),
        "unresolved_label_rows": labels.get("unresolved_label_rows"),
        "tick_rows_registered": labels.get("tick_rows_registered"),
        "tick_segments": labels.get("tick_segments"),
        "label_counts": labels.get("label_counts", {}),
        "runtime_kpi": {
            "net_profit": None,
            "profit_factor": None,
            "drawdown": None,
            "trade_count": None,
            "trades_per_day": None,
            "n_a_reason": "No EA/ONNX/Strategy Tester runtime economics were executed in F86D.",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_DIR / "kpi_record.json", record)
    return record


def write_human_summary(summary: dict[str, Any]) -> None:
    m1 = summary.get("m1_summary", {})
    labels = summary.get("label_summary", {})
    text = f"""# F86D Result Summary(F86D 결과 요약)

## Conclusion

F86D materialized a bounded selected-row M1/tick source and first-touch label source(F86D는 범위 있는 선택 행 1분봉/틱 원천과 첫 터치 라벨 원천을 물질화했다).

This is source/label evidence(원천/라벨 근거), not Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## What changed

Run(실행): `{RUN_ID}`.

Input selected rows(입력 선택 행): `{summary.get("input_rows")}`.

M1 registered rows(등록 1분봉 행): `{m1.get("registered_m1_rows")}` / expected(예상) `{m1.get("expected_m1_rows")}`.

Selected rows with full M1 window(전체 1분봉 창이 있는 선택 행): `{m1.get("selected_rows_with_full_m1_window")}`.

First-touch labels(첫 터치 라벨): `{labels.get("materialized_label_rows")}` rows(행), unresolved(미해결) `{labels.get("unresolved_label_rows")}`.

Tick rows registered for both-hit windows(양방향 터치 창 등록 틱 행): `{labels.get("tick_rows_registered")}` across tick segments(틱 구간) `{labels.get("tick_segments")}`.

## Allowed claims

bounded_selected_row_m1_registered(범위 있는 선택 행 1분봉 등록), bounded_first_touch_label_source_materialized(범위 있는 첫 터치 라벨 원천 물질화), and source_materialization_learning_recorded(원천 물질화 학습 기록).

## Forbidden claims

completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), runtime verified(런타임 검증됨), Strategy Tester economics pass(전략 테스터 경제성 통과), EA/ONNX handoff complete(EA/ONNX 인계 완료).

## Next hardening step

F86E should turn the materialized first-touch label source(첫 터치 라벨 원천) into a leakage-safe feature/label surface(누수 안전 피처/라벨 표면) and only then test whether a meaningful runtime candidate(런타임 후보)가 exists.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_md(RUN_DIR / "result_summary.md", text)
    write_md(REPORT_DIR / "result_summary.md", text)


def write_review_summary(summary: dict[str, Any], manifest: dict[str, Any], kpi_record: dict[str, Any]) -> dict[str, Any]:
    review = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": summary.get("status"),
        "judgment_class": kpi_record.get("judgment_class"),
        "evidence_boundary": kpi_record.get("evidence_boundary"),
        "run_manifest": file_identity(RUN_DIR / "run_manifest.json"),
        "kpi_record": file_identity(RUN_DIR / "kpi_record.json"),
        "summary": file_identity(RUN_DIR / "summary.json"),
        "result_summary": file_identity(REPORT_DIR / "result_summary.md"),
        "first_touch_labels": file_identity(LABEL_DIR / "first_touch_labels.csv"),
        "source_registration": file_identity(SOURCE_DIR / "source_registration_summary.json"),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": (
            "Use the bounded first-touch label source to build leakage-safe label/feature surfaces. "
            "Do not claim runtime economics until Strategy Tester output exists."
        ),
    }
    write_json(REVIEW_DIR / "f86d_execution_summary.json", review)
    return review


def main() -> int:
    summary = run_materializer()
    manifest = write_run_manifest(summary)
    kpi_record = write_kpi_record(summary)
    write_human_summary(summary)
    review = write_review_summary(summary, manifest, kpi_record)
    print(json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
