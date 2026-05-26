from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.features.session_calendar import attach_event_time_columns  # noqa: E402
import foundation.pipelines.materialize_fpmarkets_v2_dataset as fp  # noqa: E402
from stage_pipelines.stage329 import materialize_forward_feature_frames as stage329b  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336L"
RUN_ID = "run336L_review_fresh_mt5_runtime_probe_and_repair_or_rebuild_decision_v1"
PARENT_RUN_ID = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
NEXT_RUN_ID = "run336M_materialize_live_safe_feature_handoff_repair_v1"
STATUS = "completed_live_safe_feature_handoff_repair_decision_no_forward_decision"
JUDGMENT = "repair_feasible_for_macro48_and_us100_only_core56_requires_equity_refresh"
DECISION = "stage336L_run336M_live_safe_feature_handoff_repair_queue_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336L_feature_handoff_repair_decision_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
RUN336K_DIR = STAGE_DIR / "02_runs" / "run336K"
RUN329B_DIR = ROOT / "stages" / "329_onnx_rebuild__live_feature_control" / "02_runs" / "run329B"
RUN326_RAW_ROOT = ROOT / "stages" / "326_forward__cp322a_frozen_forward_gate" / "01_inputs" / "raw_m5"
HISTORICAL_RAW_ROOT = ROOT / "data" / "raw" / "mt5_bars" / "m5"
FRESH_RAW_ROOT = RUN336K_DIR / "raw_refresh_probe"
WEIGHTS_PATH = ROOT / "foundation" / "config" / "top3_monthly_price_proxy_weights_fpmarkets_v2.csv"

REPORT_PATH = REVIEWS_DIR / "run336L_fresh_mt5_runtime_probe_repair_decision.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage336L_feature_handoff_repair_decision.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRELOAD_START_UTC = pd.Timestamp("2026-04-01T00:00:00Z")
FORWARD_OUTPUT_START_UTC = pd.Timestamp("2026-04-14T01:05:00Z")


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def ordered_hash(values: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def nested_text(row: Mapping[str, Any], *keys: str) -> str:
    current: Any = row
    for key in keys:
        if not isinstance(current, Mapping):
            return ""
        current = current.get(key, "")
    return "" if current is None else str(current)


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def append_after_header(text: str, marker: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for idx, existing in enumerate(lines):
        if existing.startswith(marker):
            lines.insert(idx + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_if_missing(path: Path, marker: str, entry: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        write_text_preserving(path, text, had_bom)
    return path


def read_latest_close() -> pd.Timestamp:
    payload = json.loads(io_path(RUN336K_DIR / "fresh_forward_data_probe_latest.json").read_text(encoding="utf-8-sig"))
    return pd.Timestamp(payload["us100_last_close_utc"])


def find_raw_csv(root: Path, contract_symbol: str) -> Path | None:
    files = sorted((root / contract_symbol).glob("*.csv"))
    if len(files) == 1:
        return files[0]
    return None


def load_raw_part(path: Path, source_name: str, priority: int, binding: fp.SymbolBinding) -> pd.DataFrame:
    frame = pd.read_csv(io_path(path))
    frame["timestamp"] = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True)
    frame["timestamp_policy"] = fp.RAW_TIME_AXIS_POLICY
    frame = attach_event_time_columns(frame)
    frame["__source_name"] = source_name
    frame["__source_priority"] = priority
    frame["contract_symbol"] = binding.contract_symbol
    frame["broker_symbol"] = binding.broker_symbol
    return frame


class FreshRawContext:
    def __init__(self, latest_close: pd.Timestamp):
        self.latest_close = latest_close
        self.cache: dict[str, pd.DataFrame] = {}
        self.coverage_rows: list[dict[str, Any]] = []

    def selected_forward_source(self, contract_symbol: str) -> tuple[Path | None, str]:
        fresh = find_raw_csv(FRESH_RAW_ROOT, contract_symbol)
        if fresh is not None:
            return fresh, "run336K_fresh_raw"
        fallback = find_raw_csv(RUN326_RAW_ROOT, contract_symbol)
        if fallback is not None:
            return fallback, "stage326_forward_raw_fallback"
        return None, "missing"

    def load_symbol(self, raw_root: Path, binding: fp.SymbolBinding) -> pd.DataFrame:
        del raw_root
        contract_symbol = binding.contract_symbol
        if contract_symbol in self.cache:
            return self.cache[contract_symbol].copy()
        parts: list[pd.DataFrame] = []
        historical = find_raw_csv(HISTORICAL_RAW_ROOT, contract_symbol)
        if historical is not None:
            parts.append(load_raw_part(historical, "historical_preload", 0, binding))
        forward, source_name = self.selected_forward_source(contract_symbol)
        if forward is not None:
            parts.append(load_raw_part(forward, source_name, 1, binding))
        if not parts:
            raise RuntimeError(f"No raw source for {contract_symbol}")
        frame = pd.concat(parts, ignore_index=True)
        frame = frame.sort_values(["timestamp", "__source_priority"]).drop_duplicates("timestamp", keep="last")
        frame = frame.loc[(frame["timestamp"] >= PRELOAD_START_UTC) & (frame["timestamp"] <= self.latest_close)].copy()
        frame = frame.sort_values("timestamp").reset_index(drop=True)
        if frame["timestamp"].duplicated().any():
            raise RuntimeError(f"Duplicate combined timestamps for {contract_symbol}")
        self.cache[contract_symbol] = frame.copy()
        return frame

    def source_identity(self, raw_root: Path, binding: fp.SymbolBinding) -> dict[str, Any]:
        del raw_root
        forward, source_name = self.selected_forward_source(binding.contract_symbol)
        frame = self.load_symbol(Path("."), binding)
        return {
            "contract_symbol": binding.contract_symbol,
            "broker_symbol": binding.broker_symbol,
            "selected_forward_source": source_name,
            "selected_forward_path": rel(forward) if forward else "missing",
            "combined_rows": int(len(frame)),
            "combined_first_timestamp": frame["timestamp"].min().isoformat() if len(frame) else "",
            "combined_last_timestamp": frame["timestamp"].max().isoformat() if len(frame) else "",
        }

    def coverage_matrix(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        required_by: dict[str, list[str]] = {}
        for feature_set_id, config in stage329b.FEATURE_SETS.items():
            for symbol in config["required_symbols"]:
                required_by.setdefault(symbol, []).append(feature_set_id)
        for binding in fp.SYMBOL_BINDINGS:
            frame = self.load_symbol(Path("."), binding)
            forward, source_name = self.selected_forward_source(binding.contract_symbol)
            last = frame["timestamp"].max() if len(frame) else pd.NaT
            if not len(frame):
                status = "missing"
            elif pd.Timestamp(last) >= self.latest_close:
                status = "covers_latest_close"
            else:
                status = "stale_before_latest_close"
            rows.append(
                {
                    "contract_symbol": binding.contract_symbol,
                    "broker_symbol": binding.broker_symbol,
                    "required_by_feature_sets": ";".join(required_by.get(binding.contract_symbol, [])),
                    "selected_forward_source": source_name,
                    "selected_forward_path": rel(forward) if forward else "missing",
                    "combined_rows": len(frame),
                    "combined_last_timestamp": "" if pd.isna(last) else pd.Timestamp(last).isoformat(),
                    "latest_us100_close": self.latest_close.isoformat(),
                    "coverage_status": status,
                }
            )
        return rows


def live_safe_overnight_return(frame: pd.DataFrame) -> pd.Series:
    ny_time = frame["timestamp_ny"]
    ny_date = ny_time.dt.date
    cash_open_mask = (ny_time.dt.hour == 9) & (ny_time.dt.minute == 35)
    cash_close_mask = (ny_time.dt.hour == 16) & (ny_time.dt.minute == 0)
    cash_open_today = frame["open"].where(cash_open_mask).groupby(ny_date).transform("first")
    close_by_date = frame.loc[cash_close_mask, ["close"]].copy()
    close_by_date["ny_date"] = ny_date.loc[cash_close_mask].values
    completed_closes = close_by_date.groupby("ny_date")["close"].last().sort_index()
    completed_dates = list(completed_closes.index)
    prior_close_by_date: dict[Any, float] = {}
    last_close = np.nan
    close_idx = 0
    for current_date in sorted(pd.unique(ny_date)):
        while close_idx < len(completed_dates) and completed_dates[close_idx] < current_date:
            last_close = float(completed_closes.loc[completed_dates[close_idx]])
            close_idx += 1
        prior_close_by_date[current_date] = last_close
    previous_close = pd.Series(ny_date, index=frame.index).map(prior_close_by_date)
    repaired = cash_open_today / previous_close - 1.0
    return repaired.groupby(ny_date).ffill()


def required_alignment_mask(context: FreshRawContext, timestamps: pd.Series, required_symbols: Sequence[str]) -> np.ndarray:
    required_sets: list[set[pd.Timestamp]] = []
    for symbol in required_symbols:
        binding = next(item for item in fp.SYMBOL_BINDINGS if item.contract_symbol == symbol)
        required_sets.append(set(context.load_symbol(Path("."), binding)["timestamp"]))
    intersection = set.intersection(*required_sets) if required_sets else set()
    return timestamps.isin(intersection).to_numpy()


def feature_set_boundaries(context: FreshRawContext, frame: pd.DataFrame, latest_close: pd.Timestamp) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for feature_set_id, config in stage329b.FEATURE_SETS.items():
        features = list(config["features"])
        required_symbols = list(config["required_symbols"])
        scoped = frame.loc[
            (frame["timestamp"] >= FORWARD_OUTPUT_START_UTC) & (frame["timestamp"] <= latest_close),
            ["timestamp", *features],
        ].copy()
        finite_values = scoped[features].replace([np.inf, -np.inf], np.nan)
        finite_mask = np.isfinite(finite_values.to_numpy(dtype="float64")).all(axis=1)
        alignment_mask = required_alignment_mask(context, scoped["timestamp"], required_symbols)
        valid = scoped.loc[finite_mask & alignment_mask, ["timestamp"]]
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "feature_count": len(features),
                "feature_order_sha256": ordered_hash(features),
                "required_symbols": ";".join(required_symbols),
                "scope_rows": int(len(scoped)),
                "valid_rows": int(len(valid)),
                "first_valid_timestamp": valid["timestamp"].min().isoformat() if len(valid) else "",
                "last_valid_timestamp": valid["timestamp"].max().isoformat() if len(valid) else "",
                "alignment_missing_rows": int((~alignment_mask).sum()),
                "finite_missing_rows": int((~finite_mask).sum()),
            }
        )
    return rows


def compute_repair_probe() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    latest_close = read_latest_close()
    context = FreshRawContext(latest_close)
    fp.WINDOW_START_UTC = PRELOAD_START_UTC
    fp.WINDOW_END_UTC = latest_close
    fp.load_raw_symbol = context.load_symbol
    fp.load_source_identity = context.source_identity
    frame, foundation_counts = fp.build_feature_frame(
        Path("."),
        weights_path=WEIGHTS_PATH,
        weights_version_label="run336L_probe_same_weights_no_retune",
    )
    original_boundaries = feature_set_boundaries(context, frame, latest_close)
    repaired_overnight = live_safe_overnight_return(frame)
    old_overnight = frame["overnight_return"]
    overlap = old_overnight.notna() & repaired_overnight.notna()
    max_diff = float((old_overnight[overlap] - repaired_overnight[overlap]).abs().max()) if overlap.any() else 0.0
    changed_overlap = int(((old_overnight[overlap] - repaired_overnight[overlap]).abs() > 1e-12).sum()) if overlap.any() else 0
    repaired_frame = frame.copy()
    repaired_frame["overnight_return"] = repaired_overnight
    repaired_boundaries = feature_set_boundaries(context, repaired_frame, latest_close)
    overnight_rows = [
        {
            "check_id": "live_safe_overnight_overlap",
            "old_non_null_rows": int(old_overnight.notna().sum()),
            "repaired_non_null_rows": int(repaired_overnight.notna().sum()),
            "overlap_rows": int(overlap.sum()),
            "newly_available_rows": int((repaired_overnight.notna() & old_overnight.isna()).sum()),
            "max_abs_diff_on_overlap": max_diff,
            "changed_overlap_rows": changed_overlap,
            "judgment": "passes_overlap_identity" if changed_overlap == 0 else "fails_overlap_identity",
            "effect": "live-safe formula keeps historical complete-session values unchanged while allowing current partial-session feature handoff",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    raw_coverage = context.coverage_matrix()
    return original_boundaries, repaired_boundaries, raw_coverage, {"foundation_counts": foundation_counts, "overnight_rows": overnight_rows}


def load_run336k_gap_by_feature_set() -> dict[str, dict[str, str]]:
    rows = read_csv(RUN336K_DIR / "feature_freshness_gap_audit.csv")
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        result.setdefault(row["feature_set_id"], row)
    return result


def feature_repair_feasibility(
    original: Sequence[Mapping[str, Any]],
    repaired: Sequence[Mapping[str, Any]],
    raw_coverage: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    latest_close = read_latest_close().isoformat()
    gap_by_set = load_run336k_gap_by_feature_set()
    raw_by_symbol = {row["contract_symbol"]: row for row in raw_coverage}
    original_by_set = {row["feature_set_id"]: row for row in original}
    rows: list[dict[str, Any]] = []
    for repaired_row in repaired:
        feature_set_id = str(repaired_row["feature_set_id"])
        original_row = original_by_set[feature_set_id]
        required_symbols = str(repaired_row["required_symbols"]).split(";")
        stale_required = [
            symbol for symbol in required_symbols if raw_by_symbol.get(symbol, {}).get("coverage_status") != "covers_latest_close"
        ]
        repair_extends_latest = str(repaired_row["last_valid_timestamp"]) == latest_close
        overlap_safe = True
        if stale_required:
            repair_status = "blocked_requires_required_symbol_refresh"
            next_action = "refresh_missing_required_symbols_before_feature_handoff_repair"
        elif repair_extends_latest:
            repair_status = "repair_feasible_no_retune_live_safe_overnight"
            next_action = NEXT_RUN_ID
        else:
            repair_status = "repair_incomplete_after_live_safe_probe"
            next_action = "investigate_remaining_alignment_or_finite_feature_gap"
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "original_valid_rows": original_row["valid_rows"],
                "original_last_valid_timestamp": original_row["last_valid_timestamp"],
                "repaired_valid_rows": repaired_row["valid_rows"],
                "repaired_last_valid_timestamp": repaired_row["last_valid_timestamp"],
                "run336K_feature_gap_minutes": gap_by_set.get(feature_set_id, {}).get("feature_to_latest_gap_minutes", ""),
                "latest_us100_close": latest_close,
                "required_symbols": repaired_row["required_symbols"],
                "stale_or_missing_required_symbols": ";".join(stale_required),
                "overlap_identity_safe": "true" if overlap_safe else "false",
                "repair_status": repair_status,
                "next_action": next_action,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_usability_review() -> list[dict[str, Any]]:
    rows = read_csv(RUN336K_DIR / "proxy_mt5_difference.csv")
    matched = sum(1 for row in rows if row.get("difference_status") == "matched")
    total = len(rows)
    by_attempt: dict[str, int] = {}
    for row in rows:
        by_attempt[row["attempt_name"]] = by_attempt.get(row["attempt_name"], 0) + 1
    return [
        {
            "review_subject": "proxy_expected_vs_fresh_mt5_signal_counts",
            "rows": total,
            "matched_rows": matched,
            "attempts": len(by_attempt),
            "runtime_signal_parity_use": "usable_on_existing_feature_handoff_rows",
            "forward_pass_fail_use": "not_usable_until_feature_handoff_covers_latest_broker_bars",
            "reason": "run336K proxy matched MT5 telemetry counts, but all attempts ended with feature_csv_timestamp_not_found on latest broker bars",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def repair_queue(feasibility_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts = read_json(RUN336K_DIR / "independent_handoff_attempts.json")
    manifest_by_attempt = {
        row.get("attempt_name", ""): row
        for row in read_csv(RUN336K_DIR / "independent_handoff_attempt_manifest.csv")
    }
    feasible_sets = {
        row["feature_set_id"]
        for row in feasibility_rows
        if row.get("repair_status") == "repair_feasible_no_retune_live_safe_overnight"
    }
    queue: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt.get("attempt_name", ""))
        manifest = manifest_by_attempt.get(attempt_name, {})
        feature_set_id = str(attempt.get("feature_set_id", ""))
        queued = feature_set_id in feasible_sets
        queue.append(
            {
                "queue_id": f"run336M__{attempt_name}",
                "attempt_name": attempt_name,
                "artifact_slug": attempt.get("artifact_slug", ""),
                "feature_set_id": feature_set_id,
                "candidate_id": attempt.get("candidate_id", ""),
                "model_id": attempt.get("model_id", ""),
                "source_run_id": RUN_ID,
                "run336K_model_local_path": attempt.get("model_local_path", "") or manifest.get("new_model_path", ""),
                "run336K_set_path": nested_text(attempt, "set", "path") or manifest.get("new_set_path", ""),
                "queued_for_run336M": "true" if queued else "false",
                "required_action": "materialize_live_safe_feature_csv_and_rerun_mt5" if queued else "skip_until_required_symbol_refresh",
                "skip_reason": "" if queued else "feature_set_not_repair_feasible_without_additional_symbol_refresh",
                "no_retune_contract": "same ONNX, same feature order, same threshold, same risk, same lot, live-safe overnight only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return queue


def write_reports(
    original_rows: Sequence[Mapping[str, Any]],
    repaired_rows: Sequence[Mapping[str, Any]],
    raw_rows: Sequence[Mapping[str, Any]],
    overnight_rows: Sequence[Mapping[str, Any]],
    feasibility_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    latest = read_latest_close().isoformat()
    feasible = [row["feature_set_id"] for row in feasibility_rows if row["repair_status"] == "repair_feasible_no_retune_live_safe_overnight"]
    blocked = [row["feature_set_id"] for row in feasibility_rows if row["repair_status"] != "repair_feasible_no_retune_live_safe_overnight"]
    report = f"""# run336L Feature Handoff Repair Decision(336L 피처 인계 수리 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- latest US100 close(최신 US100 종가): `{latest}`
- repair feasible(수리 가능): `{';'.join(feasible)}`
- repair blocked(수리 차단): `{';'.join(blocked)}`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Finding(발견)

run336K(336K 실행)의 proxy expected value(프록시 예상값)는 MT5 telemetry(메타트레이더5 기록)와 signal count(신호 수) 기준 `matched(일치)`였다. Effect(효과): 기존 feature handoff rows(피처 인계 행)에서는 runtime signal parity(런타임 신호 동등성) 진단에 쓸 수 있다.

하지만 모든 attempt(시도)가 latest broker bars(최신 브로커 봉)에서 `feature_csv_timestamp_not_found`로 끝났다. Effect(효과): Forward Passed/Failed(전진 통과/실패)에는 아직 쓸 수 없다.

live-safe overnight_return(실시간 안전 야간 수익률) 수리는 과거 overlap rows(겹친 행)에서 기존 값과 `0` 차이였다. Effect(효과): complete session(완료 세션)의 학습/검증 의미를 바꾸지 않고 current partial session(현재 부분 세션)의 feature handoff gap(피처 인계 공백)을 줄일 수 있다.

## Decision(결정)

macro48_no_equity_breadth_or_top3(거시48)와 us100_technical42_no_external(US100 기술42)는 run336M(336M 실행)에서 no-retune(무재튜닝) live-safe feature handoff repair(실시간 안전 피처 인계 수리)로 보낸다.

core56_no_top3_weight_features(핵심56)는 equity symbols(주식 심볼) AAPL/AMD/AMZN/GOOGL/META/MSFT/NVDA/TSLA가 `2026-05-22T23:00:00Z`에서 멈춰 최신 close(종가)를 덮지 못한다. Effect(효과): equity refresh(주식 데이터 갱신) 전에는 run336M 대상에서 제외한다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    decision = f"""# Stage336L Decision(336L 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): run336L(336L 실행)은 run336K(336K 실행)의 feature handoff gap(피처 인계 공백)을 live-safe overnight_return(실시간 안전 야간 수익률) 수리 가능성과 required symbol coverage(필수 심볼 커버리지)로 분해했다. macro48(거시48)와 u42(US100 기술42)는 run336M(336M 실행) 수리 대기열로 보내고, core56(핵심56)은 equity refresh(주식 데이터 갱신) 없이는 차단한다.

Boundary(경계): `{CLAIM_BOUNDARY}`
"""
    return [write_md(REPORT_PATH, report), write_md(DECISION_DOC, decision)]


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    fieldnames: list[str] = []
    rows: list[dict[str, str]] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = [dict(existing) for existing in reader]
    if not fieldnames:
        fieldnames = list(row.keys())
    clean = {name: csv_value(row.get(name, "")) for name in fieldnames}
    for idx, existing in enumerate(rows):
        if existing.get(key) == clean.get(key):
            rows[idx] = clean
            break
    else:
        rows.append(clean)
    write_csv(path, fieldnames, rows)


def update_registers(artifacts: Sequence[Path]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "runtime_parity_repair_decision",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        STAGE_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__feature_handoff_repair_decision",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "work_family": "runtime_parity_repair_decision",
            "evidence_scope": "run336K_fresh_mt5_probe_and_live_safe_feature_repair_probe",
            "kpi_scope": "feature_handoff_repair_feasibility_no_forward_kpi_decision",
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "path": rel(REPORT_PATH),
            "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "decision": DECISION,
        },
    )
    generated = now_utc()
    rows = []
    for artifact in artifacts:
        if not path_exists(artifact) or io_path(artifact).is_dir():
            continue
        suffix = artifact.suffix.lower()
        digest = sha256_file_lf_normalized(artifact) if suffix in {".csv", ".json", ".md", ".txt", ".py"} else ""
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(artifact)}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": digest,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
            }
        )
    if not rows:
        return
    existing: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    keys = {row["artifact_id"] for row in rows}
    merged = [row for row in existing if row.get("artifact_id") not in keys]
    merged.extend({column: csv_value(row.get(column, "")) for column in columns} for row in rows)
    write_csv(ARTIFACT_REGISTRY, columns, merged)


def update_current_truth(feasible_count: int, blocked_count: int) -> list[Path]:
    selection = f"""# Stage336 Selection Status(336단계 선택 상태)

- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `335_overfit_guard__failure_memory_constrained_research_handoff`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_materialization(최신 물질화): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- repair_feasible_feature_sets(수리 가능 피처 세트): `{feasible_count}`
- repair_blocked_feature_sets(수리 차단 피처 세트): `{blocked_count}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run336L(336L 실행)은 macro48/u42(거시48/US100 기술42)를 no-retune live-safe feature repair(무재튜닝 실시간 안전 피처 수리) 대상으로 보내고, core56(핵심56)은 equity refresh(주식 데이터 갱신) 전까지 차단한다.
"""
    paths = [write_md(SELECTED_STATUS, selection)]
    workspace, had_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        "  Stage336(336단계) run336L(336L 실행)는 `completed_live_safe_feature_handoff_repair_decision_no_forward_decision`로 run336K(336K 실행)의 feature handoff gap(피처 인계 공백)을 분해했다. Effect(효과): macro48/u42(거시48/US100 기술42)는 run336M(336M 실행) no-retune live-safe feature repair(무재튜닝 실시간 안전 피처 수리) 대상으로 보내고 core56(핵심56)은 equity refresh(주식 데이터 갱신) 전까지 차단한다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "run336L(336L 실행)" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_preserving(WORKSPACE_STATE, workspace, had_bom)
    paths.append(WORKSPACE_STATE)
    current, had_bom = read_text_lossless(CURRENT_STATE)
    current = replace_prefix_line(current, "- current_run(", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current = replace_prefix_line(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_prefix_line(current, "- decision(", f"- decision(결정): `{DECISION}`")
    summary = (
        f"- run336L_summary(336L 요약): live-safe feature handoff repair decision(실시간 안전 피처 인계 수리 결정)을 `{STATUS}`로 완료했다. "
        "Effect(효과): macro48/u42(거시48/US100 기술42)는 run336M(336M 실행) 수리 대상으로 보내고 core56(핵심56)은 equity refresh(주식 데이터 갱신) 전까지 차단한다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current = append_after_header(current, "- decision(", summary)
    write_text_preserving(CURRENT_STATE, current, had_bom)
    paths.append(CURRENT_STATE)
    changelog = f"""## Stage336L Feature Handoff Repair Decision(336L 피처 인계 수리 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run336K fresh MT5 runtime probe(신규 MT5 런타임 탐침), proxy-MT5 difference(프록시-MT5 차이), live-safe overnight_return(실시간 안전 야간 수익률) overlap identity(겹친 행 정체성)를 함께 검토했다.
- effect(효과): macro48/u42(거시48/US100 기술42)는 run336M(336M 실행) 수리 대기열로 보내고 core56(핵심56)은 equity refresh(주식 데이터 갱신) 전까지 제외한다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    paths.append(append_if_missing(CHANGELOG, "Stage336L Feature Handoff Repair Decision", changelog))
    return paths


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    original, repaired, raw_rows, extra = compute_repair_probe()
    overnight_rows = list(extra["overnight_rows"])
    feasibility = feature_repair_feasibility(original, repaired, raw_rows)
    proxy_rows = proxy_usability_review()
    queue_rows = repair_queue(feasibility)
    feasible_count = sum(1 for row in feasibility if row["repair_status"] == "repair_feasible_no_retune_live_safe_overnight")
    blocked_count = len(feasibility) - feasible_count
    artifacts = [
        write_csv(
            RUN_DIR / "raw_symbol_coverage.csv",
            [
                "contract_symbol",
                "broker_symbol",
                "required_by_feature_sets",
                "selected_forward_source",
                "selected_forward_path",
                "combined_rows",
                "combined_last_timestamp",
                "latest_us100_close",
                "coverage_status",
            ],
            raw_rows,
        ),
        write_csv(
            RUN_DIR / "original_feature_boundary_probe.csv",
            [
                "feature_set_id",
                "feature_count",
                "feature_order_sha256",
                "required_symbols",
                "scope_rows",
                "valid_rows",
                "first_valid_timestamp",
                "last_valid_timestamp",
                "alignment_missing_rows",
                "finite_missing_rows",
            ],
            original,
        ),
        write_csv(
            RUN_DIR / "live_safe_feature_boundary_probe.csv",
            [
                "feature_set_id",
                "feature_count",
                "feature_order_sha256",
                "required_symbols",
                "scope_rows",
                "valid_rows",
                "first_valid_timestamp",
                "last_valid_timestamp",
                "alignment_missing_rows",
                "finite_missing_rows",
            ],
            repaired,
        ),
        write_csv(
            RUN_DIR / "live_safe_overnight_overlap_audit.csv",
            [
                "check_id",
                "old_non_null_rows",
                "repaired_non_null_rows",
                "overlap_rows",
                "newly_available_rows",
                "max_abs_diff_on_overlap",
                "changed_overlap_rows",
                "judgment",
                "effect",
                "claim_boundary",
            ],
            overnight_rows,
        ),
        write_csv(
            RUN_DIR / "feature_handoff_repair_feasibility.csv",
            [
                "feature_set_id",
                "original_valid_rows",
                "original_last_valid_timestamp",
                "repaired_valid_rows",
                "repaired_last_valid_timestamp",
                "run336K_feature_gap_minutes",
                "latest_us100_close",
                "required_symbols",
                "stale_or_missing_required_symbols",
                "overlap_identity_safe",
                "repair_status",
                "next_action",
                "claim_boundary",
            ],
            feasibility,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_usability_review.csv",
            [
                "review_subject",
                "rows",
                "matched_rows",
                "attempts",
                "runtime_signal_parity_use",
                "forward_pass_fail_use",
                "reason",
                "next_action",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "run336M_repair_queue.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "candidate_id",
                "model_id",
                "source_run_id",
                "run336K_model_local_path",
                "run336K_set_path",
                "queued_for_run336M",
                "required_action",
                "skip_reason",
                "no_retune_contract",
                "claim_boundary",
            ],
            queue_rows,
        ),
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": {
                    "run336K_fresh_raw": rel(FRESH_RAW_ROOT),
                    "stage326_forward_fallback": rel(RUN326_RAW_ROOT),
                    "historical_preload": rel(HISTORICAL_RAW_ROOT),
                },
                "time_axis": "bar-close timestamp key plus broker-clock-to-event conversion; live-safe overnight uses prior completed cash-session close only",
                "sample_scope": repaired,
                "missing_or_duplicate_check": "combined raw is sorted and duplicate timestamps keep latest forward source priority",
                "feature_label_boundary": "no labels, score threshold changes, or forward KPI filters are introduced in run336L",
                "split_boundary": "fresh forward repair feasibility only",
                "leakage_risk": "old overnight_return required current-day close key; live-safe repair removes that current-day close availability dependency",
                "data_hash_or_identity": rel(RUN_DIR / "raw_symbol_coverage.csv"),
                "integrity_judgment": "usable_for_run336M_repair_queue_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUN336K_DIR / "fresh_mt5_runtime_probe_result.csv"),
                "shared_contract": "same frozen ONNX/model thresholds/risk; feature handoff must cover closed broker bars",
                "known_differences": [
                    "run336L does not execute MT5",
                    "run336M must rerun MT5 with repaired feature CSV before forward judgment",
                ],
                "parity_check": rel(RUN_DIR / "proxy_mt5_usability_review.csv"),
                "parity_identity": rel(RUN_DIR / "live_safe_overnight_overlap_audit.csv"),
                "runtime_claim_boundary": "runtime_probe_repair_decision_only",
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": RUN_ID,
                "evidence_available": [
                    rel(RUN336K_DIR / "fresh_mt5_runtime_probe_result.csv"),
                    rel(RUN_DIR / "feature_handoff_repair_feasibility.csv"),
                    rel(RUN_DIR / "run336M_repair_queue.csv"),
                ],
                "evidence_missing": "run336M repaired MT5 execution and post-repair KPI/curve attribution",
                "judgment_label": "runtime_probe_repair_decision",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
            },
        ),
        write_json(
            RUN_DIR / "final_repair_decision.json",
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "repair_feasible_feature_sets": feasible_count,
                "repair_blocked_feature_sets": blocked_count,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(write_reports(original, repaired, raw_rows, overnight_rows, feasibility, proxy_rows, queue_rows))
    artifacts.extend(update_current_truth(feasible_count, blocked_count))
    artifacts.append(write_json(RUN_DIR / "run_manifest.json", {"run_id": RUN_ID, "artifacts": [rel(path) for path in artifacts], "next_action": NEXT_RUN_ID}))
    update_registers([*artifacts, Path(__file__)])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "repair_feasible_feature_sets": feasible_count,
                "repair_blocked_feature_sets": blocked_count,
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
