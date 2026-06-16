from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.baseline_training import LABEL_ORDER
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_20 import frontier20b_feature_state_rule_atlas_proxy_scout as f20b
from stage_pipelines.stage_frontier_22 import frontier22c_shock_pf_source_lifecycle_repair_scout as f22c
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
    terminal_processes,
)


STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
RUN_ID = "frontier66C_proxy_signal_mt5_backfill_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REVIEW_ROOT = Path("stages") / STAGE_ID / "03_reviews"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier66_proxy_signal_mt5_backfill"
RAW_US100 = Path("data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv")

CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

ID_FIELDS = (
    "candidate_id",
    "variant_id",
    "profile_id",
    "repair_id",
    "bridge_id",
    "archetype_id",
    "soft_union_id",
    "stability_union_id",
    "veto_candidate_id",
    "exit_variant_id",
)

SOURCE_ID_FIELDS = (
    "source_candidate_id",
    "source_stability_union_id",
    "source_soft_union_id",
    "source_f31_candidate_id",
    "source_f33b_candidate_id",
    "f30_candidate_id",
)

DIRECT_CANDIDATE_FILES = (
    "*candidate_summary.csv",
    "*metrics_by_split.csv",
    "*candidate_ledger.csv",
    "*variant_ledger.csv",
    "*top*diagnostic.csv",
    "*train_ranked*.csv",
    "*repair*.csv",
)

PREFERRED_IDS = {
    20: "f20b_pair_0359",
    21: "f21c_hold2_atr0p8_tp1p6_cd0",
    22: "f22b_0263__hold2_atr0p8_tp1p6_cd0",
    23: "f23c_0123",
    24: "f24c_0105",
    25: "f25b_0022",
    27: "f27b_0181",
    28: "f28b_0001",
    29: "f29b_0274",
    30: "f30b_0214",
    31: "f31b_0013",
    32: "f32b_0004",
    33: "f33b_0176",
}


@dataclass
class ProxyRuntimeSpec:
    stage_num: int
    stage_id: str
    candidate_id: str
    source_path: str
    source_kind: str
    side_value: int
    signal: np.ndarray
    max_hold_bars: int = 12
    cooldown_bars: int = 0
    stop_cap_log_return: float | None = None
    take_cap_log_return: float | None = None
    atr_stop_multiplier: float | None = None
    atr_take_profit_multiplier: float | None = None
    row_payload: dict[str, Any] | None = None
    reconstruction_notes: list[str] | None = None

    @property
    def feature_name(self) -> str:
        return f"frontier{self.stage_num:02d}_proxy_signal"

    @property
    def stage_label(self) -> str:
        return f"F{self.stage_num:02d}"


class RuleParser:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame
        self.train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
        token_re = r"(<=|>=|<|>|\(|\)|&)|\bOR\b|\bAND\b|\bNOT\b|[-+]?\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_\.]*"
        self.token_re = re.compile(token_re, re.IGNORECASE)
        self.tokens: list[str] = []
        self.pos = 0

    def parse(self, expression: str) -> np.ndarray:
        expression = re.sub(r"\s+@\s+[A-Za-z0-9_]+", "", expression)
        expression = re.sub(r"\b[A-Za-z0-9_]+:", "", expression)
        expression = expression.replace("&&", "&")
        self.tokens = [m.group(0) for m in self.token_re.finditer(expression)]
        self.pos = 0
        if not self.tokens:
            raise ValueError("empty rule expression")
        mask = self._expr()
        if self.pos != len(self.tokens):
            raise ValueError(f"unconsumed tokens: {self.tokens[self.pos:self.pos+5]}")
        return np.asarray(mask, dtype=bool)

    def _peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _take(self) -> str:
        token = self._peek()
        if token is None:
            raise ValueError("unexpected end of expression")
        self.pos += 1
        return token

    def _expr(self) -> np.ndarray:
        mask = self._term()
        while (self._peek() or "").upper() == "OR":
            self._take()
            mask = mask | self._term()
        return mask

    def _term(self) -> np.ndarray:
        mask = self._factor()
        while self._peek() == "&" or (self._peek() or "").upper() == "AND":
            self._take()
            mask = mask & self._factor()
        return mask

    def _factor(self) -> np.ndarray:
        token = self._peek()
        if token is None:
            raise ValueError("missing factor")
        if token.upper() == "NOT":
            self._take()
            return ~self._factor()
        if token == "(":
            self._take()
            mask = self._expr()
            if self._take() != ")":
                raise ValueError("missing closing parenthesis")
            return mask
        return self._condition()

    def _condition(self) -> np.ndarray:
        feature = self._take()
        operator = self._take()
        value_token = self._take()
        if feature not in self.frame.columns:
            raise ValueError(f"unknown feature in rule: {feature}")
        value = self._condition_value(feature, value_token)
        series = pd.to_numeric(self.frame[feature], errors="coerce").to_numpy(dtype="float64")
        finite = np.isfinite(series)
        if operator == "<=":
            return finite & (series <= value)
        if operator == ">=":
            return finite & (series >= value)
        if operator == "<":
            return finite & (series < value)
        if operator == ">":
            return finite & (series > value)
        raise ValueError(f"unsupported operator: {operator}")

    def _condition_value(self, feature: str, token: str) -> float:
        text = token.strip()
        lowered = text.lower()
        values = pd.to_numeric(self.frame.loc[self.train_mask, feature], errors="coerce").to_numpy(dtype="float64")
        values = values[np.isfinite(values)]
        if lowered.startswith("q"):
            raw = lowered[1:]
            q = float(raw)
            if q > 1.0:
                q = q / 100.0
            return float(np.nanquantile(values, q))
        if lowered in {"ge0p5", "lt0p5"}:
            return 0.5
        return float(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Frontier66 proxy-signal MT5 runtime probe backfill.")
    parser.add_argument("--stages", default="20-49")
    parser.add_argument("--execute-stages", default="")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--execute-existing", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = parse_stage_filter(args.stages)
    ensure_dirs()
    created_at = utc_now()
    if args.execute_existing:
        attempts = json.loads(io_path(RUN_ROOT / "frontier66_proxy_signal_mt5_attempts.json").read_text(encoding="utf-8-sig"))
        execute_selected = parse_stage_filter(args.execute_stages) if str(args.execute_stages).strip() else selected
        execute_attempts_subset = [attempt for attempt in attempts if int(attempt.get("stage_num", -1)) in execute_selected]
        result = execute_attempts(args, execute_attempts_subset, created_at)
        manifest_rows = read_csv_rows(RUN_ROOT / "frontier66_proxy_signal_materialization_manifest.csv")
        write_materialization_report(manifest_rows, result["runtime_rows"], created_at, materialize_only=False)
        print(json.dumps(json_ready({"status": result["status"], "runtime_rows": len(result["runtime_rows"])}), ensure_ascii=False, indent=2))
        return 0

    frame = f20b.load_frame()
    bars = load_us100_bars()
    parser = RuleParser(frame)
    row_index = build_row_index()

    specs: list[ProxyRuntimeSpec] = []
    manifest_rows: list[dict[str, Any]] = []
    for stage_num in sorted(selected):
        stage_dir = stage_dir_for_num(stage_num)
        if stage_dir is None:
            continue
        try:
            spec = build_spec(stage_num, stage_dir, frame, parser, row_index)
            if int(np.count_nonzero(spec.signal)) <= 0:
                manifest_rows.append(materialization_row(stage_num, stage_dir.name, "logic_zero_signal_no_mt5_attempt", None, "reconstructed signal has zero non-flat rows"))
                continue
            specs.append(spec)
            manifest_rows.append(materialization_row(stage_num, stage_dir.name, "proxy_signal_materialized_pending_mt5", spec, ""))
        except Exception as exc:
            reason = str(exc)
            if "zero executable" in reason or "zero non-flat" in reason:
                manifest_rows.append(materialization_row(stage_num, stage_dir.name, "logic_zero_signal_no_mt5_attempt", None, reason))
            else:
                manifest_rows.append(materialization_row(stage_num, stage_dir.name, "reconstruction_failed_needs_code_repair", None, reason))

    attempts = materialize_specs(specs, frame, bars, Path(args.common_files_root))
    write_csv(RUN_ROOT / "frontier66_proxy_signal_materialization_manifest.csv", manifest_rows)
    write_json(
        RUN_ROOT / "frontier66_proxy_signal_backfill_plan.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "selected_stages": sorted(selected),
            "spec_count": len(specs),
            "attempt_count": len(attempts),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    if args.materialize_only or not args.execute:
        write_materialization_report(manifest_rows, [], created_at, materialize_only=True)
        print(json.dumps(json_ready({"status": "materialized", "spec_count": len(specs), "attempt_count": len(attempts)}), ensure_ascii=False, indent=2))
        return 0

    execute_selected = parse_stage_filter(args.execute_stages) if str(args.execute_stages).strip() else selected
    execute_attempts_subset = [attempt for attempt in attempts if int(attempt.get("stage_num", -1)) in execute_selected]
    result = execute_attempts(args, execute_attempts_subset, created_at)
    write_materialization_report(manifest_rows, result["runtime_rows"], created_at, materialize_only=False)
    print(json.dumps(json_ready({"status": result["status"], "runtime_rows": len(result["runtime_rows"])}), ensure_ascii=False, indent=2))
    return 0


def parse_stage_filter(raw: str) -> set[int]:
    out: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            out.update(range(int(lo), int(hi) + 1))
        else:
            out.add(int(part))
    return {n for n in out if 2 <= n <= 64}


def ensure_dirs() -> None:
    for path in (RUN_ROOT, RUN_ROOT / "features", RUN_ROOT / "models", RUN_ROOT / "mt5", RUN_ROOT / "reports", REVIEW_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normal_path(path: Path) -> Path:
    text = str(path)
    return Path(text[4:]) if text.startswith("\\\\?\\") else path


def rel(path: Path) -> str:
    return normal_path(path).relative_to(ROOT).as_posix()


def stage_dir_for_num(stage_num: int) -> Path | None:
    matches = sorted(io_path(ROOT / "stages").glob(f"stage_frontier_{stage_num:02d}__*"))
    if not matches:
        return None
    return normal_path(matches[0])


def load_us100_bars() -> pd.DataFrame:
    bars = pd.read_csv(io_path(RAW_US100), usecols=["time_close_unix", "close"])
    bars["timestamp"] = pd.to_datetime(bars["time_close_unix"], unit="s", utc=True)
    return bars[["timestamp", "close"]].drop_duplicates("timestamp")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or ["empty"])
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value for key, value in row.items()})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "inf", "-inf", "none"}:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def safe_int(value: Any, default: int = 0) -> int:
    parsed = safe_float(value)
    return default if parsed is None else int(parsed)


def build_row_index() -> dict[str, tuple[Path, dict[str, str]]]:
    index: dict[str, tuple[Path, dict[str, str]]] = {}
    for stage in io_path(ROOT / "stages").glob("stage_frontier_*__*"):
        stage_path = normal_path(stage)
        runs = stage_path / "02_runs"
        if not path_exists(runs):
            continue
        for pattern in DIRECT_CANDIDATE_FILES:
            for path in io_path(runs).rglob(pattern):
                csv_path = normal_path(path)
                for row in read_csv_rows(csv_path):
                    for field in ID_FIELDS:
                        value = str(row.get(field, "")).strip()
                        if value and value not in index:
                            index[value] = (csv_path, row)
    return index


def build_spec(
    stage_num: int,
    stage_dir: Path,
    frame: pd.DataFrame,
    parser: RuleParser,
    row_index: dict[str, tuple[Path, dict[str, str]]],
) -> ProxyRuntimeSpec:
    if stage_num == 11:
        return frontier11_argmax_spec(stage_num, stage_dir, frame)
    if stage_num == 15:
        return frontier15_score_threshold_spec(stage_num, stage_dir, frame)
    if stage_num == 18:
        return frontier18_trade_log_spec(stage_num, stage_dir, frame)
    if stage_num == 19:
        return frontier19_probability_spec(stage_num, stage_dir, frame)
    if stage_num == 21:
        return lifecycle_trade_log_spec(stage_num, stage_dir, "f21c_hold2_atr0p8_tp1p6_cd0", "frontier21C_lifecycle_density_repair_scout_v1", frame)
    if stage_num == 22:
        return lifecycle_trade_log_spec(stage_num, stage_dir, "f22b_0263__hold2_atr0p8_tp1p6_cd0", "frontier22C_shock_pf_source_repair_or_closeout_decision_v1", frame)
    if stage_num == 26:
        raise RuntimeError("stage logic generated zero executable joint-union signal")
    if stage_num in {46, 47, 48, 49}:
        return score_event_direct_spec(stage_num, stage_dir, frame)
    if stage_num in {38, 39, 44, 45}:
        return score_replay_spec(stage_num, stage_dir, frame)
    if stage_num in {41, 42, 43}:
        return json_best_variant_spec(stage_num, stage_dir, frame, parser)

    candidate_id = preferred_candidate_id(stage_num, stage_dir)
    if not candidate_id:
        raise RuntimeError("no preferred proxy candidate id recovered from stage notes or diagnostics")
    if candidate_id not in row_index:
        raise RuntimeError(f"preferred candidate id not found in proxy tables: {candidate_id}")
    source_path, row = row_index[candidate_id]
    mask = mask_for_row(row, parser, row_index)
    side = row_side_value(row)
    if side == 0:
        side = 1 if "long" in str(row.get("side", "")).lower() else -1
    signal = np.where(mask, side, 0).astype("int8")
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=candidate_id,
        source_path=rel(source_path),
        source_kind="rule_proxy_table",
        side_value=int(side),
        signal=signal,
        max_hold_bars=max_hold_from_row(row),
        cooldown_bars=safe_int(row.get("cooldown_bars"), 0),
        stop_cap_log_return=safe_float(row.get("stop_cap_log_return")),
        take_cap_log_return=safe_float(row.get("take_cap_log_return")),
        row_payload=dict(row),
        reconstruction_notes=["rule_definition_replayed_from_train_quantiles"],
    )


def preferred_candidate_id(stage_num: int, stage_dir: Path) -> str:
    if stage_num in PREFERRED_IDS:
        return PREFERRED_IDS[stage_num]
    selection_json = stage_dir / "04_selected" / "selection_status.json"
    if path_exists(selection_json):
        payload = json.loads(io_path(selection_json).read_text(encoding="utf-8-sig"))
        best = payload.get("best_variant") or payload.get("best_candidate") or {}
        if isinstance(best, Mapping):
            for key in ("variant_id", "candidate_id", "exit_variant_id"):
                if best.get(key):
                    return str(best[key])
    for rel_path in ("04_selected/preserved_clue.md", "04_selected/selection_status.md"):
        path = stage_dir / rel_path
        if not path_exists(path):
            continue
        text = io_path(path).read_text(encoding="utf-8-sig", errors="replace")
        matches = re.findall(r"f\d{2}[a-z]_(?:raw_)?\d{4}|f\d{2}b_pair_\d{4}", text)
        if matches:
            return matches[0]
    for path in io_path(stage_dir / "02_runs").rglob("*top*diagnostic.csv") if path_exists(stage_dir / "02_runs") else []:
        rows = read_csv_rows(normal_path(path))
        if rows:
            for field in ID_FIELDS:
                value = str(rows[0].get(field, "")).strip()
                if value:
                    return value
    return ""


def row_side_value(row: Mapping[str, Any]) -> int:
    value = safe_float(row.get("side_value"))
    if value is not None and value != 0:
        return 1 if value > 0 else -1
    side = str(row.get("side", "")).lower()
    if "short" in side:
        return -1
    if "long" in side:
        return 1
    return 0


def max_hold_from_row(row: Mapping[str, Any]) -> int:
    for key in ("hold_bars", "max_hold_bars"):
        parsed = safe_int(row.get(key), 0)
        if parsed > 0:
            return parsed
    return 12


def mask_for_row(
    row: Mapping[str, Any],
    parser: RuleParser,
    row_index: dict[str, tuple[Path, dict[str, str]]],
    seen: set[str] | None = None,
) -> np.ndarray:
    seen = set(seen or set())
    row_id = first_id(row)
    if row_id:
        seen.add(row_id)
    direct_rule = str(row.get("rule_definition", "")).strip()
    source_rule = str(row.get("source_rule_definition", "")).strip()
    if source_rule and direct_rule and direct_rule != source_rule:
        return parser.parse(source_rule) & ~parser.parse(direct_rule)
    if direct_rule and is_parseable_rule(direct_rule):
        return parser.parse(direct_rule)
    source_mask: np.ndarray | None = None
    for field in SOURCE_ID_FIELDS:
        source_id = str(row.get(field, "")).strip()
        if not source_id or source_id in seen or source_id not in row_index:
            continue
        _source_path, source_row = row_index[source_id]
        source_mask = mask_for_row(source_row, parser, row_index, seen | {source_id})
        break
    if source_mask is None:
        raise ValueError(f"no parseable rule or source mask for row {row_id or 'unknown'}")
    gate = str(row.get("gate_definition", "")).strip()
    if gate:
        return source_mask & parser.parse(gate)
    return source_mask


def frontier11_argmax_spec(stage_num: int, stage_dir: Path, frame: pd.DataFrame) -> ProxyRuntimeSpec:
    run_root = stage_dir / "02_runs" / "frontier11B_subperiod_stability_proxy_scout_v1"
    selector_rows = read_csv_rows(run_root / "selector_comparison.csv")
    selected_row = next((row for row in selector_rows if "stability" in str(row.get("selector", "")).lower()), selector_rows[0] if selector_rows else {})
    candidate_id = str(selected_row.get("candidate_id", "")).strip()
    identity_path, identity_row = stage_row_by_id(run_root / "model_signal_identity.csv", "candidate_id", candidate_id)
    signal = argmax_signal_from_joblib(Path(identity_row["source_joblib_path"]), frame)
    row_payload = {**identity_row, **selected_row}
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=candidate_id,
        source_path=rel(identity_path),
        source_kind="stage11_stability_selected_argmax_joblib_replay",
        side_value=0,
        signal=signal,
        max_hold_bars=12,
        row_payload=row_payload,
        reconstruction_notes=["stability selector candidate replayed from source F10C joblib argmax"],
    )


def frontier15_score_threshold_spec(stage_num: int, stage_dir: Path, frame: pd.DataFrame) -> ProxyRuntimeSpec:
    from stage_pipelines.stage_frontier_15 import frontier15b_score_threshold_density_controlled_proxy_scout as f15b

    run_root = stage_dir / "02_runs" / "frontier15B_score_threshold_density_controlled_proxy_scout_v1"
    summary_path, row = first_csv_row(run_root / "candidate_summary.csv")
    probabilities = ordered_probabilities_from_joblib(Path(row["joblib_path"]), frame)
    score = f15b.score_values(probabilities, str(row["score_contract_id"]))
    threshold = float(row["threshold_value"])
    direction = np.where(probabilities[:, 0] >= probabilities[:, 2], -1, 1).astype("int8")
    selected = np.isfinite(score) & (score >= threshold)
    signal = np.where(selected, direction, 0).astype("int8")
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=str(row["candidate_id"]),
        source_path=rel(summary_path),
        source_kind="stage15_score_threshold_joblib_replay",
        side_value=0,
        signal=signal,
        max_hold_bars=parse_hold_bars(row),
        row_payload=dict(row),
        reconstruction_notes=["train-only score threshold signal replayed from selected joblib probabilities"],
    )


def frontier18_trade_log_spec(stage_num: int, stage_dir: Path, frame: pd.DataFrame) -> ProxyRuntimeSpec:
    run_root = stage_dir / "02_runs" / "frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1"
    summary_path, row = first_csv_row(run_root / "candidate_summary.csv")
    trade_log = run_root / "trade_log.csv"
    candidate_id = str(row["candidate_id"])
    signal = signal_from_trade_log(trade_log, frame, candidate_id, "candidate_id")
    atr_stop, atr_take = parse_atr_take_from_id(candidate_id)
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=candidate_id,
        source_path=rel(trade_log),
        source_kind="stage18_lifecycle_trade_log_replay",
        side_value=0,
        signal=signal,
        max_hold_bars=parse_hold_bars(row),
        atr_stop_multiplier=atr_stop,
        atr_take_profit_multiplier=atr_take,
        row_payload=dict(row),
        reconstruction_notes=[
            "entry timestamps replayed from proxy trade_log",
            f"candidate summary source={rel(summary_path)}",
        ],
    )


def frontier19_probability_spec(stage_num: int, stage_dir: Path, frame: pd.DataFrame) -> ProxyRuntimeSpec:
    run_root = stage_dir / "02_runs" / "frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1"
    top_path, row = first_csv_row(run_root / "top_candidates.csv")
    variant_id = str(row["variant_id"])
    audit_path, audit = stage_row_by_id(run_root / "model_export_parity_audit.csv", "variant_id", variant_id)
    probabilities = pd.read_parquet(io_path(Path(audit["probability_path"])))
    merged = frame[["timestamp"]].copy()
    merged["timestamp"] = pd.to_datetime(merged["timestamp"], utc=True)
    prob = probabilities.copy()
    prob["timestamp"] = pd.to_datetime(prob["timestamp"], utc=True)
    merged = merged.merge(prob[["timestamp", "p_short", "p_flat", "p_long"]], on="timestamp", how="left")
    values = merged[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64")
    labels = np.nanargmax(np.where(np.isfinite(values), values, -np.inf), axis=1)
    signal = np.zeros(len(frame), dtype="int8")
    finite = np.isfinite(values).all(axis=1)
    signal[finite & (labels == 0)] = -1
    signal[finite & (labels == 2)] = 1
    payload = {**audit, **row}
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=str(row["candidate_id"]),
        source_path=rel(audit_path),
        source_kind="stage19_probability_argmax_replay",
        side_value=0,
        signal=signal,
        max_hold_bars=12,
        row_payload=payload,
        reconstruction_notes=[
            "saved probability parquet replayed with argmax non-flat backbone-only decision",
            f"top candidate source={rel(top_path)}",
        ],
    )


def first_csv_row(path: Path) -> tuple[Path, dict[str, str]]:
    rows = read_csv_rows(path)
    if not rows:
        raise RuntimeError(f"CSV has no candidate rows: {path.as_posix()}")
    return path, rows[0]


def stage_row_by_id(path: Path, key: str, value: str) -> tuple[Path, dict[str, str]]:
    rows = read_csv_rows(path)
    for row in rows:
        if str(row.get(key, "")).strip() == str(value).strip():
            return path, row
    raise RuntimeError(f"row not found in {path.as_posix()}: {key}={value}")


def ordered_probabilities_from_joblib(joblib_path: Path, frame: pd.DataFrame) -> np.ndarray:
    import joblib

    model = joblib.load(io_path(joblib_path))
    feature_order = f23b.read_feature_order()
    values = frame.loc[:, feature_order].to_numpy(dtype="float64")
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = getattr(model, "classes_", None)
    if classes is None and hasattr(model, "steps") and model.steps:
        classes = getattr(model.steps[-1][1], "classes_", None)
    ordered = np.zeros((raw.shape[0], len(LABEL_ORDER)), dtype="float64")
    if classes is None:
        if raw.shape[1] != len(LABEL_ORDER):
            raise RuntimeError("joblib predict_proba output has no class order and unexpected width")
        return raw
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    for output_index, label in enumerate(LABEL_ORDER):
        if label in class_to_index:
            ordered[:, output_index] = raw[:, class_to_index[label]]
    return ordered


def argmax_signal_from_joblib(joblib_path: Path, frame: pd.DataFrame) -> np.ndarray:
    probabilities = ordered_probabilities_from_joblib(joblib_path, frame)
    labels = np.argmax(probabilities, axis=1)
    signal = np.zeros(len(frame), dtype="int8")
    signal[labels == 0] = -1
    signal[labels == 2] = 1
    return signal


def signal_from_trade_log(path: Path, frame: pd.DataFrame, candidate_id: str, id_field: str) -> np.ndarray:
    signal = np.zeros(len(frame), dtype="int8")
    index_by_time = {pd.Timestamp(ts).isoformat(): idx for idx, ts in enumerate(pd.to_datetime(frame["timestamp"], utc=True))}
    for trade in read_csv_rows(path):
        if str(trade.get(id_field, "")).strip() != candidate_id:
            continue
        key = pd.Timestamp(trade.get("entry_signal_timestamp")).tz_convert("UTC").isoformat()
        idx = index_by_time.get(key)
        if idx is not None:
            signal[idx] = int(float(trade.get("side", "0") or 0))
    return signal


def parse_hold_bars(row: Mapping[str, Any]) -> int:
    parsed = max_hold_from_row(row)
    if parsed > 0 and parsed != 12:
        return parsed
    text = " ".join(str(row.get(key, "")) for key in ("candidate_id", "target_id", "profile_id"))
    match = re.search(r"hold(\d+)", text)
    return int(match.group(1)) if match else parsed


def parse_atr_take_from_id(candidate_id: str) -> tuple[float | None, float | None]:
    def parse_token(prefix: str) -> float | None:
        match = re.search(prefix + r"(\d+)p(\d+)", candidate_id)
        if not match:
            return None
        return float(f"{match.group(1)}.{match.group(2)}")

    return parse_token("atr"), parse_token("tp")


def first_id(row: Mapping[str, Any]) -> str:
    for field in ID_FIELDS:
        value = str(row.get(field, "")).strip()
        if value:
            return value
    return ""


def is_parseable_rule(rule: str) -> bool:
    lowered = rule.lower()
    if "score " in lowered or "probability" in lowered or "density_preserving_preselector" in lowered:
        return False
    return any(op in rule for op in ("<=", ">=", "<", ">"))


def lifecycle_trade_log_spec(stage_num: int, stage_dir: Path, profile_id: str, run_id: str, frame: pd.DataFrame) -> ProxyRuntimeSpec:
    root = stage_dir / "02_runs" / run_id
    trade_log = root / "trade_log.csv"
    summary = root / "repair_candidate_summary.csv"
    if not path_exists(summary):
        summary = root / "candidate_summary.csv"
    profile_rows = [row for row in read_csv_rows(summary) if str(row.get("profile_id", "")).strip() == profile_id]
    if not profile_rows:
        raise RuntimeError(f"profile not found: {profile_id}")
    row = profile_rows[0]
    signal = np.zeros(len(frame), dtype="int8")
    index_by_time = {pd.Timestamp(ts).isoformat(): idx for idx, ts in enumerate(pd.to_datetime(frame["timestamp"], utc=True))}
    for trade in read_csv_rows(trade_log):
        if str(trade.get("profile_id", "")).strip() != profile_id:
            continue
        key = pd.Timestamp(trade.get("entry_signal_timestamp")).tz_convert("UTC").isoformat()
        idx = index_by_time.get(key)
        if idx is not None:
            signal[idx] = int(float(trade.get("side", "0") or 0))
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=profile_id,
        source_path=rel(trade_log),
        source_kind="entry_trade_log_replay",
        side_value=0,
        signal=signal,
        max_hold_bars=max_hold_from_row(row),
        cooldown_bars=safe_int(row.get("cooldown_bars"), 0),
        atr_stop_multiplier=safe_float(row.get("atr_stop_multiplier")),
        atr_take_profit_multiplier=safe_float(row.get("atr_take_profit_multiplier")),
        row_payload=dict(row),
        reconstruction_notes=["entry timestamps replayed from proxy trade_log"],
    )


def json_best_variant_spec(stage_num: int, stage_dir: Path, frame: pd.DataFrame, parser: RuleParser) -> ProxyRuntimeSpec:
    payload = json.loads(io_path(stage_dir / "04_selected" / "selection_status.json").read_text(encoding="utf-8-sig"))
    row = dict(payload.get("best_variant") or {})
    candidate_id = str(row.get("variant_id") or row.get("candidate_id"))
    mask = parser.parse(str(row["rule_definition"]))
    side = row_side_value(row)
    signal = np.where(mask, side, 0).astype("int8")
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=candidate_id,
        source_path=rel(stage_dir / "04_selected" / "selection_status.json"),
        source_kind="selection_json_best_variant_rule_replay",
        side_value=side,
        signal=signal,
        max_hold_bars=max_hold_from_row(row),
        stop_cap_log_return=safe_float(row.get("stop_cap_log_return")),
        take_cap_log_return=safe_float(row.get("take_cap_log_return")),
        row_payload=row,
        reconstruction_notes=["best_variant rule_definition replayed from train quantiles"],
    )


def score_event_direct_spec(stage_num: int, stage_dir: Path, frame: pd.DataFrame) -> ProxyRuntimeSpec:
    module = __import__(f"stage_pipelines.stage_frontier_{stage_num}.run_frontier{stage_num}_lifecycle", fromlist=["x"])
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    candidate_id = preferred_candidate_id(stage_num, stage_dir)
    source_path, row = stage_candidate_row(stage_dir, candidate_id)
    profile = str(row.get("profile", "")).strip() or ("repair" if candidate_id.startswith(f"f{stage_num}c_") else "initial")
    side = row_side_value(row) or int(getattr(module, "SIDE_VALUE", -1))

    x_raw = frame[feature_order].to_numpy(dtype="float64")
    valid_raw_features = np.isfinite(x_raw).all(axis=1)
    labels = path_labels[int(getattr(module, "SIDE_VALUE", side))]
    train_mask = f33b.split_mask(frame, "train") & valid_raw_features & labels["valid"]

    event_spec = select_named(module.event_specs(frame, labels, profile), "event_variant", row.get("event_variant"))
    y = np.asarray(event_spec["event"], dtype="int8")
    fit_mask = train_mask & np.isfinite(y)

    base_spec = select_named(module.base_scorer_specs(profile), "base_scorer_family", row.get("base_scorer_family"))
    base_model = base_spec["factory"]()
    base_model.fit(x_raw[fit_mask], y[fit_mask])
    base_score = np.full(len(frame), np.nan, dtype="float64")
    base_score[valid_raw_features] = module.event_probability(base_model, x_raw[valid_raw_features])
    finite_base_score = np.isfinite(base_score) & valid_raw_features

    context_spec = select_named(module.sequence_context_specs(profile), "context_variant", row.get("context_variant"))
    context = module.build_sequence_context(
        frame=frame,
        base_score=base_score,
        event=y,
        train_mask=train_mask & finite_base_score,
        context_spec=context_spec,
    )
    x_context = context["matrix"]
    valid_context = context["valid_context"] & valid_raw_features
    x_model = np.column_stack([x_raw, x_context])
    fit_mask_context = fit_mask & valid_context

    model_family = str(row.get("model_family", "")).strip()
    suffix = f"__{base_spec['base_scorer_family']}__{context_spec['context_variant']}"
    base_model_family = model_family[: -len(suffix)] if model_family.endswith(suffix) else model_family.split("__", 1)[0]
    model_spec = select_named(module.model_specs(profile), "model_family", base_model_family)
    model = model_spec["factory"]()
    model.fit(x_model[fit_mask_context], y[fit_mask_context])
    score = np.full(len(frame), np.nan, dtype="float64")
    score[valid_context] = module.event_probability(model, x_model[valid_context])
    finite_score = np.isfinite(score) & valid_context

    threshold = safe_float(row.get("score_threshold"))
    if threshold is None:
        score_q = safe_float(row.get("score_quantile")) or 0.86
        train_scores = score[train_mask & finite_score]
        threshold = float(np.nanquantile(train_scores, score_q))
    mask = finite_score & (score >= float(threshold))

    risk_variant = str(row.get("risk_budget_variant", "")).strip()
    if risk_variant:
        risk_spec = select_named(module.risk_budget_specs(profile), "risk_budget_variant", risk_variant)
        mask, risk_meta = module.apply_risk_budget_mask(
            frame=frame,
            base_mask=mask,
            train_mask=train_mask & finite_score,
            context=context,
            risk_spec=risk_spec,
        )
    else:
        risk_meta = {}

    signal = np.where(mask, side, 0).astype("int8")
    payload = dict(row)
    payload["direct_replay_risk_meta"] = risk_meta
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=candidate_id,
        source_path=rel(source_path),
        source_kind="stage_score_event_direct_replay",
        side_value=int(side),
        signal=signal,
        max_hold_bars=max_hold_from_row(row),
        stop_cap_log_return=safe_float(row.get("stop_cap_log_return")),
        take_cap_log_return=safe_float(row.get("take_cap_log_return")),
        row_payload=payload,
        reconstruction_notes=["selected event score candidate replayed directly without rebuilding full surface"],
    )


def stage_candidate_row(stage_dir: Path, candidate_id: str) -> tuple[Path, dict[str, str]]:
    if not candidate_id:
        raise RuntimeError("no candidate id recovered for direct event replay")
    runs = stage_dir / "02_runs"
    if not path_exists(runs):
        raise RuntimeError("stage 02_runs unavailable for direct event replay")
    for pattern in ("*candidate_summary.csv", "*candidate_ledger.csv"):
        for path in io_path(runs).rglob(pattern):
            csv_path = normal_path(path)
            for row in read_csv_rows(csv_path):
                if str(row.get("candidate_id", "")).strip() == candidate_id:
                    return csv_path, row
    selection_json = stage_dir / "04_selected" / "selection_status.json"
    if path_exists(selection_json):
        payload = json.loads(io_path(selection_json).read_text(encoding="utf-8-sig"))
        best = payload.get("best_variant") or {}
        if isinstance(best, Mapping) and str(best.get("candidate_id", "")).strip() == candidate_id:
            return selection_json, {key: str(value) for key, value in best.items()}
    raise RuntimeError(f"candidate row not found for direct event replay: {candidate_id}")


def select_named(items: Sequence[Mapping[str, Any]], key: str, value: Any) -> Mapping[str, Any]:
    target = str(value or "").strip()
    for item in items:
        if str(item.get(key, "")).strip() == target:
            return item
    raise RuntimeError(f"{key} not found in direct event replay: {target}")


def score_replay_spec(stage_num: int, stage_dir: Path, frame: pd.DataFrame) -> ProxyRuntimeSpec:
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    candidate_id = preferred_candidate_id(stage_num, stage_dir)
    if not candidate_id:
        raise RuntimeError("no score replay candidate id")
    candidates = score_replay_candidates(stage_num, frame, feature_order, path_labels, raw_path)
    match = next((item for item in candidates if str(item.get("candidate_id") or item.get("variant_id")) == candidate_id), None)
    if match is None:
        raise RuntimeError(f"score replay candidate not found after surface rebuild: {candidate_id}")
    mask = np.asarray(match["mask"], dtype=bool)
    side = row_side_value(match)
    signal = np.where(mask, side, 0).astype("int8")
    return ProxyRuntimeSpec(
        stage_num=stage_num,
        stage_id=stage_dir.name,
        candidate_id=candidate_id,
        source_path=rel(stage_dir / "04_selected" / "selection_status.md"),
        source_kind="stage_score_surface_replay",
        side_value=side,
        signal=signal,
        max_hold_bars=max_hold_from_row(match),
        stop_cap_log_return=safe_float(match.get("stop_cap_log_return")),
        take_cap_log_return=safe_float(match.get("take_cap_log_return")),
        row_payload={k: v for k, v in match.items() if k != "mask"},
        reconstruction_notes=["stage score surface rebuilt in memory to recover timestamp mask"],
    )


def score_replay_candidates(
    stage_num: int,
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> list[dict[str, Any]]:
    if stage_num == 38:
        from stage_pipelines.stage_frontier_38 import run_frontier38_lifecycle as f38

        proxy = f38.build_model_score_proxy(frame, feature_order, path_labels, raw_path)
        repair = f38.build_model_score_repair(frame, feature_order, path_labels, raw_path)
        return list(proxy.get("candidates", [])) + list(repair.get("candidates", []))
    if stage_num == 39:
        from stage_pipelines.stage_frontier_39 import run_frontier39_lifecycle as f39

        return f39_candidates_with_masks(frame, feature_order, path_labels, raw_path, f39)
    if stage_num == 44:
        from stage_pipelines.stage_frontier_44 import run_frontier44_lifecycle as f44

        initial = f44.build_model_surface(
            frame,
            feature_order,
            path_labels,
            raw_path,
            run_id=f44.RUN_B,
            run_prefix="f44b",
            profile="initial",
            target_specs=f44.target_specs(frame, path_labels[f44.SIDE_VALUE], "initial"),
            model_specs=f44.model_specs("initial"),
            score_quantiles=f44.INITIAL_SCORE_QUANTILES,
            stop_quantiles=f44.INITIAL_STOP_QUANTILES,
            take_quantiles=f44.INITIAL_TAKE_QUANTILES,
            rr_floors=f44.INITIAL_RR_FLOORS,
            max_candidates=f44.INITIAL_MAX_CANDIDATES,
        )
        repair = f44.build_model_surface(
            frame,
            feature_order,
            path_labels,
            raw_path,
            run_id=f44.RUN_C,
            run_prefix="f44c",
            profile="repair",
            target_specs=f44.target_specs(frame, path_labels[f44.SIDE_VALUE], "repair"),
            model_specs=f44.model_specs("repair"),
            score_quantiles=f44.REPAIR_SCORE_QUANTILES,
            stop_quantiles=f44.REPAIR_STOP_QUANTILES,
            take_quantiles=f44.REPAIR_TAKE_QUANTILES,
            rr_floors=f44.REPAIR_RR_FLOORS,
            max_candidates=f44.REPAIR_MAX_CANDIDATES,
        )
        return list(initial.get("candidates", [])) + list(repair.get("candidates", []))
    if stage_num in {45, 46, 47, 48, 49}:
        module = __import__(f"stage_pipelines.stage_frontier_{stage_num}.run_frontier{stage_num}_lifecycle", fromlist=["x"])
        return score_event_module_candidates(stage_num, module, frame, feature_order, path_labels, raw_path)
    raise RuntimeError(f"score replay not implemented for F{stage_num:02d}")


def score_event_module_candidates(stage_num: int, module: Any, frame: pd.DataFrame, feature_order: list[str], path_labels: dict[int, dict[str, np.ndarray]], raw_path: dict[str, Any]) -> list[dict[str, Any]]:
    kwargs_common: dict[str, Any] = {
        "frame": frame,
        "feature_order": feature_order,
        "path_labels": path_labels,
        "raw_path": raw_path,
    }

    def call(profile: str, run_id: str, run_prefix: str, score_quantiles: tuple[float, ...], stop_quantiles: tuple[float, ...], take_quantiles: tuple[float, ...], rr_floors: tuple[float, ...], max_candidates: int) -> list[dict[str, Any]]:
        kwargs = {
            **kwargs_common,
            "run_id": run_id,
            "run_prefix": run_prefix,
            "profile": profile,
            "event_specs": module.event_specs(frame, path_labels[module.SIDE_VALUE], profile),
            "model_specs": module.model_specs(profile),
            "score_quantiles": score_quantiles,
            "stop_quantiles": stop_quantiles,
            "take_quantiles": take_quantiles,
            "rr_floors": rr_floors,
            "max_candidates": max_candidates,
        }
        if stage_num >= 46:
            kwargs["base_scorer_specs"] = module.base_scorer_specs(profile)
            kwargs["context_specs"] = module.sequence_context_specs(profile)
        if stage_num >= 47:
            kwargs["risk_budget_specs"] = module.risk_budget_specs(profile)
        surface = module.build_event_surface(**kwargs)
        return list(surface.get("candidates", []))

    return call(
        "initial",
        module.RUN_B,
        f"f{stage_num}b",
        module.INITIAL_SCORE_QUANTILES,
        module.INITIAL_STOP_QUANTILES,
        module.INITIAL_TAKE_QUANTILES,
        module.INITIAL_RR_FLOORS,
        module.INITIAL_MAX_CANDIDATES,
    ) + call(
        "repair",
        module.RUN_C,
        f"f{stage_num}c",
        module.REPAIR_SCORE_QUANTILES,
        module.REPAIR_STOP_QUANTILES,
        module.REPAIR_TAKE_QUANTILES,
        module.REPAIR_RR_FLOORS,
        module.REPAIR_MAX_CANDIDATES,
    )


def f39_candidates_with_masks(frame: pd.DataFrame, feature_order: list[str], path_labels: dict[int, dict[str, np.ndarray]], raw_path: dict[str, Any], f39: Any) -> list[dict[str, Any]]:
    labels = path_labels[-1]
    x = frame[feature_order].to_numpy(dtype="float64")
    valid_features = np.isfinite(x).all(axis=1)
    train = f33b.split_mask(frame, "train") & labels["valid"] & valid_features
    mfe60 = float(np.nanquantile(labels["mfe"][train], 0.60))
    mae40 = float(np.nanquantile(labels["mae"][train], 0.40))
    y = ((labels["mfe"] >= mfe60) & (labels["mae"] <= mae40)).astype(int)
    fit_mask = train & np.isfinite(y)
    regimes = f39.build_regimes(frame, train)
    rows: list[dict[str, Any]] = []
    for model_name, model in f39.model_specs():
        model.fit(x[fit_mask], y[fit_mask])
        score = np.asarray(model.predict_proba(x)[:, 1], dtype="float64")
        train_scores = score[train & np.isfinite(score)]
        for score_q in f39.SCORE_QUANTILES:
            score_threshold = float(np.nanquantile(train_scores, score_q))
            score_mask = valid_features & np.isfinite(score) & (score >= score_threshold)
            for stop_q, take_q, rr, stop_cap, take_cap in f39.threshold_rows(frame, score_mask, labels):
                a_train = f39.eval_path(frame, score_mask, stop_cap, take_cap, path_labels, raw_path, "train")
                if not f39.train_gate(a_train):
                    continue
                a_validation = f39.eval_path(frame, score_mask, stop_cap, take_cap, path_labels, raw_path, "validation")
                a_oos = f39.eval_path(frame, score_mask, stop_cap, take_cap, path_labels, raw_path, "oos")
                for regime in regimes:
                    b_mask = score_mask & regime["mask"]
                    b_train = f39.eval_path(frame, b_mask, stop_cap, take_cap, path_labels, raw_path, "train")
                    if not f39.train_gate(b_train, min_count=35, density_low=3.0, density_high=14.0, dd_cap=24.0):
                        continue
                    b_validation = f39.eval_path(frame, b_mask, stop_cap, take_cap, path_labels, raw_path, "validation")
                    b_oos = f39.eval_path(frame, b_mask, stop_cap, take_cap, path_labels, raw_path, "oos")
                    row = f39.ablation_row(model_name, score_q, score_threshold, stop_q, take_q, rr, stop_cap, take_cap, regime, a_train, a_validation, a_oos, b_train, b_validation, b_oos)
                    if row["f39_scout_clue_flag"] or row["f39_ablation_guardrail_pass"] or row["f39_seed_surface_flag"]:
                        row["mask"] = b_mask
                        row["side_value"] = -1
                        row["side"] = "short"
                        rows.append(row)
    rows = sorted(rows, key=lambda r: (bool(r.get("f39_runtime_candidate_flag")), bool(r.get("f39_seed_surface_flag")), bool(r.get("f39_ablation_guardrail_pass")), bool(r.get("f39_scout_clue_flag")), float(r.get("f39_read_score", 0.0))), reverse=True)
    for idx, row in enumerate(rows, start=1):
        row["candidate_id"] = f"f39b_{idx:04d}"
    return rows


def materialization_row(stage_num: int, stage_id: str, status: str, spec: ProxyRuntimeSpec | None, reason: str) -> dict[str, Any]:
    signal = spec.signal if spec is not None else np.asarray([], dtype="int8")
    return {
        "stage_num": stage_num,
        "stage_id": stage_id,
        "status": status,
        "candidate_id": spec.candidate_id if spec else "",
        "source_kind": spec.source_kind if spec else "",
        "source_path": spec.source_path if spec else "",
        "signal_rows": int(len(signal)),
        "signal_nonflat_count": int(np.count_nonzero(signal)),
        "signal_long_count": int(np.sum(signal > 0)) if len(signal) else 0,
        "signal_short_count": int(np.sum(signal < 0)) if len(signal) else 0,
        "max_hold_bars": spec.max_hold_bars if spec else "",
        "stop_cap_log_return": spec.stop_cap_log_return if spec else "",
        "take_cap_log_return": spec.take_cap_log_return if spec else "",
        "reason": reason,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_specs(specs: Sequence[ProxyRuntimeSpec], frame: pd.DataFrame, bars: pd.DataFrame, common_files_root: Path) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for spec in specs:
        artifact_tag = physical_artifact_tag(spec)
        model_path = RUN_ROOT / "models" / f"{artifact_tag}_signal_ebm_table.csv"
        model_payload = export_single_discrete_signal_score_table(model_path, feature_order=[spec.feature_name], logit_strength=4.0)
        model_payload["logical_candidate_id"] = spec.candidate_id
        model_payload["physical_artifact_tag"] = artifact_tag
        model_common = f"{COMMON_RUN_ROOT}/models/{model_path.name}"
        mt5.copy_to_common_files(common_files_root, model_path, model_common)
        for runtime_split, source_split in (("validation_is", "validation"), ("oos", "oos")):
            split_mask = frame["split"].astype(str).eq(source_split).to_numpy(dtype=bool)
            split_frame = frame.loc[split_mask, ["timestamp", "split"]].copy()
            split_signal = spec.signal[split_mask]
            split_frame[spec.feature_name] = split_signal.astype("float32")
            feature_path = RUN_ROOT / "features" / f"{artifact_tag}_{runtime_split}_features.csv"
            feature_payload = mt5.export_mt5_feature_matrix_csv(split_frame, [spec.feature_name], feature_path)
            feature_payload["logical_candidate_id"] = spec.candidate_id
            feature_payload["physical_artifact_tag"] = artifact_tag
            feature_common = f"{COMMON_RUN_ROOT}/features/{feature_path.name}"
            mt5.copy_to_common_files(common_files_root, feature_path, feature_common)
            from_date, to_date = split_dates(split_frame)
            attempt_name = safe_name(f"f66_{spec.stage_label.lower()}_{spec.candidate_id}_{runtime_split}", 60)
            extra_set_values = {
                "InpDecisionMode": "argmax",
                "InpEntryTransitionOnly": "false",
                "InpReentryCooldownBars": int(spec.cooldown_bars),
                "InpSameDirectionReentryCooldownBars": int(spec.cooldown_bars),
            }
            sltp_values = sltp_set_values(spec, frame.loc[split_mask, ["timestamp"]], bars)
            sltp_notes = str(sltp_values.pop("_sltp_notes", ""))
            extra_set_values.update(sltp_values)
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=66,
                exploration_label="frontier66_proxy_signal_mt5_backfill(전선66 프록시 신호 MT5 소급)",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=runtime_split,
                model_path=model_common,
                model_id=f"{artifact_tag}_signal_table",
                model_backend="ebm_table",
                feature_path=feature_common,
                feature_count=1,
                feature_order_hash=ordered_hash([spec.feature_name]),
                short_threshold=0.0,
                long_threshold=0.0,
                min_margin=0.0,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier=mt5.TIER_A,
                attempt_role="frontier_proxy_signal_runtime_probe_backfill",
                record_view_prefix=f"mt5_f66_{spec.stage_label.lower()}_{spec.candidate_id}",
                max_hold_bars=int(spec.max_hold_bars),
                common_root=COMMON_RUN_ROOT,
                close_on_flat_signal=False,
                reverse_on_opposite_signal=False,
                close_only_on_opposite_signal=False,
                extra_set_values=extra_set_values,
            )
            attempt.update(
                {
                    "stage_num": spec.stage_num,
                    "stage_id": spec.stage_id,
                    "candidate_id": spec.candidate_id,
                    "source_kind": spec.source_kind,
                    "source_path": spec.source_path,
                    "physical_artifact_tag": artifact_tag,
                    "model_payload": model_payload,
                    "feature_payload": feature_payload,
                    "expected_signal_count": int(np.count_nonzero(split_signal)),
                    "expected_long_count": int(np.sum(split_signal > 0)),
                    "expected_short_count": int(np.sum(split_signal < 0)),
                    "expected_rows": int(len(split_signal)),
                    "proxy_row_payload": spec.row_payload or {},
                    "reconstruction_notes": spec.reconstruction_notes or [],
                    "fixed_point_sltp_notes": sltp_notes,
                }
            )
            attempts.append(attempt)
            signal_rows.append(
                {
                    "stage_num": spec.stage_num,
                    "stage_id": spec.stage_id,
                    "candidate_id": spec.candidate_id,
                    "split": runtime_split,
                    "rows": len(split_signal),
                    "signal_count": int(np.count_nonzero(split_signal)),
                    "long_count": int(np.sum(split_signal > 0)),
                    "short_count": int(np.sum(split_signal < 0)),
                    "from_date": from_date,
                    "to_date": to_date,
                }
            )
    write_csv(RUN_ROOT / "frontier66_proxy_signal_expected_by_split.csv", signal_rows)
    write_json(RUN_ROOT / "frontier66_proxy_signal_mt5_attempts.json", attempts)
    return attempts


def split_dates(frame: pd.DataFrame) -> tuple[str, str]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def physical_artifact_tag(spec: ProxyRuntimeSpec) -> str:
    digest = sha256_file_lf_normalized_text(f"{spec.stage_label}:{spec.candidate_id}")[:12]
    return f"{spec.stage_label}_{digest}"


def sltp_set_values(spec: ProxyRuntimeSpec, split_frame: pd.DataFrame, bars: pd.DataFrame) -> dict[str, Any]:
    if spec.atr_stop_multiplier is not None or spec.atr_take_profit_multiplier is not None:
        stop = float(spec.atr_stop_multiplier or 0.0)
        take = float(spec.atr_take_profit_multiplier or 0.0)
        return {
            "InpAtrSltpEnabled": "true" if stop > 0 or take > 0 else "false",
            "InpAtrStopMultiplier": stop,
            "InpAtrTakeProfitMultiplier": take,
        }
    stop_points, take_points = fixed_points_from_log_caps(spec, split_frame, bars)
    if stop_points <= 0 and take_points <= 0:
        return {"InpAtrSltpEnabled": "false"}
    return {
        "InpAtrSltpEnabled": "true",
        "InpAtrStopMultiplier": 1.0 if stop_points > 0 else 0.0,
        "InpAtrTakeProfitMultiplier": 1.0 if take_points > 0 else 0.0,
        "InpAtrMinStopPoints": stop_points,
        "InpAtrMaxStopPoints": stop_points,
        "InpAtrMinTakeProfitPoints": take_points,
        "InpAtrMaxTakeProfitPoints": take_points,
        "_sltp_notes": "log_return_caps_approximated_as_fixed_points_using_split_median_close_and_point_0p01",
    }


def fixed_points_from_log_caps(spec: ProxyRuntimeSpec, split_frame: pd.DataFrame, bars: pd.DataFrame) -> tuple[float, float]:
    merged = split_frame[["timestamp"]].merge(bars, on="timestamp", how="left")
    close = float(np.nanmedian(pd.to_numeric(merged["close"], errors="coerce").to_numpy(dtype="float64")))
    point = 0.01
    stop = 0.0
    take = 0.0
    if spec.stop_cap_log_return is not None and spec.stop_cap_log_return > 0:
        stop = max(close * (math.exp(float(spec.stop_cap_log_return)) - 1.0) / point, 1.0)
    if spec.take_cap_log_return is not None and spec.take_cap_log_return > 0:
        take = max(close * (math.exp(float(spec.take_cap_log_return)) - 1.0) / point, 1.0)
    return round(stop, 3), round(take, 3)


def safe_name(value: str, limit: int) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
    if len(cleaned) <= limit:
        return cleaned
    digest = sha256_file_lf_normalized_text(cleaned)[:8]
    return f"{cleaned[:limit-9]}_{digest}"


def sha256_file_lf_normalized_text(value: str) -> str:
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    terminal_probe = terminal_processes()
    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append(blocked_result(attempt, "target_portable_terminal_already_running"))
    elif not can_run_terminal(compile_payload):
        for attempt in attempts:
            execution_results.append(blocked_result(attempt, "compile_blocked_and_no_portable_ex5_fallback"))
    else:
        for attempt in attempts:
            clear_runtime_outputs(Path(args.common_files_root), attempt)
            mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
            try:
                result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-2000:],
                    "stderr": (exc.stderr or "")[-2000:],
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                Path(args.common_files_root),
                attempt,
                timeout_seconds=int(args.wait_timeout_seconds),
                poll_seconds=2.0,
            )
            if runtime_outputs.get("status") != "completed":
                result["status"] = "blocked"
                result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            result.update(
                {
                    "runtime_outputs": runtime_outputs,
                    "attempt_name": attempt["attempt_name"],
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "record_view_prefix": attempt["record_view_prefix"],
                    "attempt_role": attempt["attempt_role"],
                    "stage_num": attempt.get("stage_num"),
                    "stage_id": attempt.get("stage_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "expected_signal_count": attempt.get("expected_signal_count"),
                    "expected_rows": attempt.get("expected_rows"),
                }
            )
            write_json(RUN_ROOT / "mt5" / f"{attempt['attempt_name']}_tester_execution.json", result)
            execution_results.append(result)
        report_records = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_ROOT,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    runtime_rows = runtime_rows_from_results(execution_results)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "compile_payload": compile_payload,
        "terminal_probe": terminal_probe,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "runtime_rows": runtime_rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_ROOT / "frontier66_proxy_signal_mt5_execution_result.json", payload)
    write_csv(RUN_ROOT / "frontier66_proxy_signal_runtime_rows.csv", runtime_rows)
    return {"status": "executed", "runtime_rows": runtime_rows}


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, RUN_ROOT / "mt5" / "mt5_compile.log")
    portable_payload = {
        "repo_ea_ex5": EA_BINARY.as_posix(),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists_before": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        portable_payload["copied"] = True
        portable_payload["portable_ea_ex5_exists_after"] = path_exists(PORTABLE_EA_BINARY)
        portable_payload["portable_ea_sha256"] = mt5.sha256_file(PORTABLE_EA_BINARY)
    payload = {"compile": compile_payload, "portable_ea": portable_payload}
    write_json(RUN_ROOT / "mt5" / "mt5_compile_result.json", payload)
    return payload


def can_run_terminal(compile_payload: Mapping[str, Any]) -> bool:
    compile_status = (compile_payload.get("compile") or {}).get("status")
    return compile_status == "completed" or path_exists(PORTABLE_EA_BINARY)


def blocked_result(attempt: Mapping[str, Any], blocker: str) -> dict[str, Any]:
    return {
        "status": "blocked",
        "blocker": blocker,
        "attempt_name": attempt["attempt_name"],
        "tier": attempt["tier"],
        "split": attempt["split"],
        "record_view_prefix": attempt.get("record_view_prefix"),
        "attempt_role": attempt.get("attempt_role"),
        "stage_num": attempt.get("stage_num"),
        "stage_id": attempt.get("stage_id"),
        "candidate_id": attempt.get("candidate_id"),
    }


def clear_runtime_outputs(common_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def runtime_rows_from_results(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        long_count = safe_int(last.get("long_count"), 0)
        short_count = safe_int(last.get("short_count"), 0)
        expected_signal = safe_int(result.get("expected_signal_count"), 0)
        expected_rows = safe_int(result.get("expected_rows"), 0)
        feature_ready = safe_int(last.get("feature_ready_count"), 0)
        rows.append(
            {
                "stage_num": result.get("stage_num"),
                "stage_id": result.get("stage_id"),
                "candidate_id": result.get("candidate_id"),
                "attempt_name": result.get("attempt_name"),
                "split": result.get("split"),
                "tester_status": result.get("status"),
                "runtime_status": runtime.get("status", "missing"),
                "report_status": report.get("status", "missing"),
                "expected_rows": expected_rows,
                "feature_ready_count": feature_ready,
                "feature_ready_diff": feature_ready - expected_rows,
                "expected_signal_count": expected_signal,
                "mt5_signal_count": long_count + short_count,
                "signal_count_diff": long_count + short_count - expected_signal,
                "order_attempt_count": safe_int(last.get("order_attempt_count"), 0),
                "order_fill_count": safe_int(last.get("order_fill_count"), 0),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "max_drawdown_percent": metrics.get("max_drawdown_percent"),
                "blocker": result.get("blocker", ""),
            }
        )
    return rows


def write_materialization_report(manifest_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], created_at: str, *, materialize_only: bool) -> None:
    total = len(manifest_rows)
    materialized = sum(1 for row in manifest_rows if str(row.get("status")) == "proxy_signal_materialized_pending_mt5")
    zero = sum(1 for row in manifest_rows if str(row.get("status")) == "logic_zero_signal_no_mt5_attempt")
    failed = sum(1 for row in manifest_rows if str(row.get("status")) == "reconstruction_failed_needs_code_repair")
    lines = [
        "# Frontier66C Proxy Signal MT5 Backfill(전선66C 프록시 신호 MT5 소급)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Mode(모드): {'materialize_only(물질화 전용)' if materialize_only else 'mt5_executed(MT5 실행)'}",
        "",
        "Action(행동): F20-F49 proxy surface(프록시 표면)를 -1/0/+1 signal(신호) EBM table(EBM 테이블)로 번역했습니다.",
        "",
        "Effect(효과): ONNX(온엑스)가 없던 proxy-only stage(프록시 전용 단계)도 MT5 RuntimeProbeEA(런타임 탐침 EA)에서 실제 주문/체결/리포트 관찰 대상으로 만들었습니다.",
        "",
        f"- total_stage_rows(총 단계 행): `{total}`",
        f"- materialized_signal_rows(신호 물질화 행): `{materialized}`",
        f"- logic_zero_signal_rows(단계 로직상 신호 0 행): `{zero}`",
        f"- reconstruction_repair_needed_rows(복구 코드 수리 필요 행): `{failed}`",
        "",
        "Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) only. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).",
        "",
        "## Materialization Table(물질화 표)",
        "",
        "| stage | candidate | status | signal | source | reason |",
        "|---:|---|---|---:|---|---|",
    ]
    for row in manifest_rows:
        lines.append(
            "| F{stage_num:02d} | `{candidate}` | `{status}` | {signal} | `{source}` | {reason} |".format(
                stage_num=int(row.get("stage_num", 0)),
                candidate=row.get("candidate_id", ""),
                status=row.get("status", ""),
                signal=row.get("signal_nonflat_count", 0),
                source=row.get("source_kind", ""),
                reason=str(row.get("reason", "")).replace("|", "/"),
            )
        )
    if runtime_rows:
        lines.extend(["", "## Runtime Rows(런타임 행)", "", "| stage | split | status | PF | DD | trades | signal_diff |", "|---:|---|---|---:|---:|---:|---:|"])
        for row in runtime_rows:
            lines.append(
                "| F{stage_num:02d} | `{split}` | `{status}` | {pf} | {dd} | {trades} | {diff} |".format(
                    stage_num=int(row.get("stage_num") or 0),
                    split=row.get("split", ""),
                    status=row.get("runtime_status", ""),
                    pf=row.get("profit_factor", ""),
                    dd=row.get("max_drawdown_percent", ""),
                    trades=row.get("trade_count", ""),
                    diff=row.get("signal_count_diff", ""),
                )
            )
    lines.append("")
    io_path(REVIEW_ROOT / "frontier66C_proxy_signal_mt5_backfill_report.md").write_text("\n".join(lines), encoding="utf-8-sig")


if __name__ == "__main__":
    raise SystemExit(main())
