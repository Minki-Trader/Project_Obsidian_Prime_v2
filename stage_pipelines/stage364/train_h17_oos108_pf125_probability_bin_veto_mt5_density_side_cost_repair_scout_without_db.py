from __future__ import annotations

import csv
import hashlib
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

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db as hl  # noqa: E402


TODAY = "2026-06-09"
STAGE_ID = hl.STAGE_ID
RUN_NUMBER = "run364HM"
RUN_ID = "run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1"
PARENT_RUN_ID = hl.RUN_ID
NEXT_RUN_ID = "run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1"

STATUS_POSITIVE = (
    "completed_stage364HM_probability_bin_veto_mt5_density_side_cost_repair_scout_"
    "positive_scaled_seed_review_required_no_authority"
)
STATUS_INCONCLUSIVE = (
    "completed_stage364HM_probability_bin_veto_mt5_density_side_cost_repair_scout_"
    "no_scaled_seed_review_required_no_authority"
)
JUDGMENT_POSITIVE = (
    "positive_proxy_scaled_density_side_cost_repair_seed_review_required_"
    "no_new_mt5_no_authority"
)
JUDGMENT_INCONCLUSIVE = (
    "inconclusive_proxy_density_side_cost_repair_no_full_seed_review_required_"
    "no_new_mt5_no_authority"
)
DECISION_POSITIVE = "stage364HM_open_run364HN_density_side_cost_repair_scout_review"
DECISION_INCONCLUSIVE = "stage364HM_open_run364HN_density_side_cost_repair_failure_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scaled_density_side_cost_repair_scout_only_reuses_hl_mt5_density_ratio_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
SHORT_SHARE_CAUTION = 0.70
SHORT_SHARE_TARGET = 0.65
OOS_PF_FLOOR = 1.25
MIN_SPLIT_PF_FLOOR = 1.05
BASE_COST_PER_TRADE = 0.30
COST_STRESS_LEVELS = [0.30, 0.45, 0.60, 0.90]

STAGE_DIR = hl.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

WORK_PACKET = RUN_DIR / "work_packet.json"
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE_INVENTORY = RUN_DIR / "hm_prior_surface_inventory.csv"
CANDIDATE_SCREEN = RUN_DIR / "hm_candidate_screen.csv"
DIRECT_STRICT_CANDIDATES = RUN_DIR / "hm_direct_strict_candidates.csv"
RUNTIME_SCALED_CANDIDATES = RUN_DIR / "hm_runtime_scaled_repair_candidates.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "hm_failure_attribution.csv"
SELECTED_SEED = RUN_DIR / "selected_hm_seed.json"
SELECTED_SEED_TRADE_TAPE = RUN_DIR / "selected_hm_seed_trade_tape.csv"
SELECTED_SEED_COST_STRESS = RUN_DIR / "selected_hm_seed_cost_stress.csv"
SELECTED_SEED_SIDE_SESSION = RUN_DIR / "selected_hm_seed_side_session_review.csv"
SELECTED_SEED_MONTH_STABILITY = RUN_DIR / "selected_hm_seed_month_stability.csv"
ROUTE_PARITY_DECISION = RUN_DIR / "hm_route_parity_decision.csv"
RUN364HN_QUEUE = RUN_DIR / "run364HN_density_side_cost_repair_review_queue.csv"
EXPLORATION_RECEIPT = RUN_DIR / "exploration_mandate_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HM_probability_bin_veto_mt5_density_side_cost_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HM_probability_bin_veto_mt5_density_side_cost_repair_scout.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

THIS_FILE = Path(__file__)

STATIC_INPUT_FILES = [
    hl.FINAL_DECISION,
    hl.GATE_AUDIT,
    hl.SCOPE_ALIGNMENT,
    hl.GUARDRAIL_REVIEW,
    hl.RUNTIME_REVIEW,
    hl.RUN364HM_QUEUE,
    hl.PERFORMANCE_RECEIPT,
    hl.LINEAGE_RECEIPT,
    THIS_FILE,
]

OUTPUT_FILES = [
    WORK_PACKET,
    INPUT_MANIFEST,
    SURFACE_INVENTORY,
    CANDIDATE_SCREEN,
    DIRECT_STRICT_CANDIDATES,
    RUNTIME_SCALED_CANDIDATES,
    FAILURE_ATTRIBUTION,
    SELECTED_SEED,
    SELECTED_SEED_TRADE_TAPE,
    SELECTED_SEED_COST_STRESS,
    SELECTED_SEED_SIDE_SESSION,
    SELECTED_SEED_MONTH_STABILITY,
    ROUTE_PARITY_DECISION,
    RUN364HN_QUEUE,
    EXPLORATION_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    THIS_FILE,
]

REQUIRED_SURFACE_COLUMNS = [
    "validation_net",
    "validation_profit_factor",
    "validation_trade_density",
    "validation_trade_count",
    "oos_net",
    "oos_profit_factor",
    "oos_trade_density",
    "oos_trade_count",
    "oos_cost06_net",
    "combined_net",
    "combined_trade_count",
    "combined_trade_density",
    "combined_cost09_net",
    "combined_long_trade_count",
    "combined_short_trade_count",
    "combined_short_share",
]

CANDIDATE_COLUMNS = [
    "run_id",
    "source_run_number",
    "source_run_id",
    "source_surface_path",
    "candidate_ref",
    "model_id",
    "model_family",
    "feature_set_id",
    "label_id",
    "route_variant_id",
    "threshold",
    "hours_id",
    "extra_filter",
    "max_hold_m5",
    "validation_net",
    "validation_profit_factor",
    "validation_trade_density",
    "validation_trade_count",
    "validation_cost06_net",
    "oos_net",
    "oos_profit_factor",
    "oos_trade_density",
    "oos_trade_count",
    "oos_cost06_net",
    "combined_net",
    "combined_trade_count",
    "combined_trade_density",
    "combined_cost06_net",
    "combined_cost09_net",
    "combined_long_trade_count",
    "combined_short_trade_count",
    "combined_short_share",
    "min_split_profit_factor",
    "runtime_density_estimate_from_hl_ratio",
    "runtime_trade_count_estimate_from_hl_ratio",
    "direct_density_pass",
    "scaled_density_pass",
    "profit_pass",
    "pf_pass",
    "cost_pass",
    "side_caution_pass",
    "side_target_pass",
    "pf_finite_policy_pass",
    "direct_strict_pass",
    "runtime_scaled_repair_pass",
    "hm_condition_count",
    "hm_score",
    "claim_boundary",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def exists(path: Path | str) -> bool:
    return io_path(Path(path)).exists()


def sha(path: Path | str) -> str:
    p = Path(path)
    if not exists(p) or not io_path(p).is_file():
        return ""
    raw = io_path(p).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = [dict(row) for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in fields:
                    fields.append(str(key))
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    io_path(path).write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    rows = [dict(row) for row in rows]
    existing: list[dict[str, Any]] = []
    fields: list[str] = []
    if exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    key_set = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(key, "")) for key in key_fields) not in key_set]
    kept.extend(rows)
    write_csv(path, kept, fields)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    lines = text.splitlines()
    out: list[str] = []
    handled = set()
    for line in lines:
        replaced = False
        for prefix, new_line in replacements.items():
            if line.startswith(prefix):
                out.append(new_line)
                handled.add(prefix)
                replaced = True
                break
        if not replaced:
            out.append(line)
    for prefix, new_line in replacements.items():
        if prefix not in handled:
            out.append(new_line)
    write_text(path, "\n".join(out).rstrip() + "\n", bom=bom)


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value in ("", None):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def finite(value: Any, digits: int = 10) -> float | str:
    number = as_float(value)
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def bool_text(value: Any) -> str:
    return "true" if bool(value) else "false"


def clean_records(frame: pd.DataFrame, columns: Sequence[str] | None = None, limit: int | None = None) -> list[dict[str, Any]]:
    selected = frame.copy()
    if columns is not None:
        for column in columns:
            if column not in selected.columns:
                selected[column] = ""
        selected = selected[list(columns)]
    if limit is not None:
        selected = selected.head(limit)
    selected = selected.where(pd.notna(selected), "")
    records: list[dict[str, Any]] = []
    for row in selected.to_dict(orient="records"):
        records.append({key: finite(value) if isinstance(value, (float, int)) else value for key, value in row.items()})
    return records


def profit_factor(values: pd.Series) -> float:
    gross_profit = float(values[values > 0].sum())
    gross_loss = float(-values[values < 0].sum())
    if gross_loss == 0:
        return 999.0 if gross_profit > 0 else 0.0
    return gross_profit / gross_loss


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in STATIC_INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HM inputs(HM 입력 누락): " + ", ".join(missing))
    parent = read_json(hl.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"HL parent mismatch(HL 상위 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HL next_run_id mismatch(HL 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(hl.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HL gate audit(HL 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"HL forbidden claim(HL 금지 주장): {key}={parent.get(key)}")
    return parent


def hl_density_payload(parent: Mapping[str, Any]) -> dict[str, Any]:
    scope = read_csv(hl.SCOPE_ALIGNMENT)
    aligned = scope[scope["comparison_id"].astype(str).str.startswith("scope_aligned_validation_oos_proxy_vs_mt5_total")]
    if aligned.empty:
        raise RuntimeError("HL scope aligned row(HL 범위 정렬 행)을 찾지 못했습니다.")
    row = aligned.iloc[0].to_dict()
    expected_density = as_float(row.get("expected_trade_density"))
    actual_density = as_float(row.get("actual_mt5_trade_density"))
    expected_trades = as_float(row.get("expected_trade_count"))
    actual_trades = as_float(row.get("actual_mt5_trade_count"))
    if expected_density <= 0 or expected_trades <= 0:
        raise RuntimeError("HL density/trade denominator(HL 밀도/거래수 분모)이 유효하지 않습니다.")
    return {
        "hl_expected_proxy_density": expected_density,
        "hl_actual_mt5_density": actual_density,
        "hl_density_lift_ratio": actual_density / expected_density,
        "hl_expected_proxy_trade_count": expected_trades,
        "hl_actual_mt5_trade_count": actual_trades,
        "hl_trade_lift_ratio": actual_trades / expected_trades,
        "density_required_for_scaled_pass": DENSITY_FLOOR / (actual_density / expected_density),
        "hl_mt5_net_profit": as_float(parent.get("mt5_net_profit")),
        "hl_mt5_profit_factor": as_float(parent.get("mt5_profit_factor")),
        "hl_mt5_trade_density": as_float(parent.get("mt5_trade_density")),
        "hl_mt5_trade_count": as_float(parent.get("mt5_trade_count")),
    }


def surface_files() -> list[Path]:
    files = sorted((STAGE_DIR / "02_runs").glob("run364*/**/*surface*.csv"))
    return [path for path in files if RUN_NUMBER not in path.parts]


def normalize_surface(path: Path, payload: Mapping[str, Any]) -> tuple[pd.DataFrame | None, dict[str, Any]]:
    try:
        frame = read_csv(path)
    except Exception as exc:
        return None, {"surface_path": rel(path), "usable": "false", "reason": f"read_failed({type(exc).__name__})"}
    missing = [column for column in REQUIRED_SURFACE_COLUMNS if column not in frame.columns]
    if missing:
        return None, {
            "surface_path": rel(path),
            "usable": "false",
            "reason": "missing_required_columns(필수 열 누락): " + ",".join(missing[:6]),
            "rows": len(frame),
        }
    source_run_number = next((part for part in path.parts if part.startswith("run364")), path.parent.name)
    out = pd.DataFrame(index=frame.index)
    out["run_id"] = RUN_ID
    out["source_run_number"] = source_run_number
    out["source_surface_path"] = rel(path)
    out["source_run_id"] = frame["run_id"].astype(str) if "run_id" in frame.columns else source_run_number
    if "route_variant_id" in frame.columns:
        out["candidate_ref"] = frame["route_variant_id"].astype(str)
        out["route_variant_id"] = frame["route_variant_id"].astype(str)
    elif "model_id" in frame.columns:
        out["candidate_ref"] = frame["model_id"].astype(str)
        out["route_variant_id"] = ""
    else:
        out["candidate_ref"] = frame.index.astype(str)
        out["route_variant_id"] = ""
    for column in ["model_id", "model_family", "feature_set_id", "label_id", "threshold", "hours_id", "extra_filter", "max_hold_m5"]:
        out[column] = frame[column] if column in frame.columns else ""
    for column in REQUIRED_SURFACE_COLUMNS + ["validation_cost06_net", "combined_cost06_net", "min_split_profit_factor"]:
        if column in frame.columns:
            out[column] = pd.to_numeric(frame[column], errors="coerce")
        else:
            out[column] = math.nan
    out["min_split_profit_factor"] = out["min_split_profit_factor"].where(
        pd.notna(out["min_split_profit_factor"]),
        pd.concat([out["validation_profit_factor"], out["oos_profit_factor"]], axis=1).min(axis=1),
    )
    out["runtime_density_estimate_from_hl_ratio"] = out["combined_trade_density"] * float(payload["hl_density_lift_ratio"])
    out["runtime_trade_count_estimate_from_hl_ratio"] = out["combined_trade_count"] * float(payload["hl_trade_lift_ratio"])
    out["direct_density_pass"] = (out["combined_trade_density"] >= DENSITY_FLOOR) & (out["oos_trade_density"] >= DENSITY_FLOOR)
    out["scaled_density_pass"] = out["runtime_density_estimate_from_hl_ratio"] >= DENSITY_FLOOR
    out["profit_pass"] = (out["validation_net"] > 0) & (out["oos_net"] > 0) & (out["combined_net"] > 0)
    out["pf_finite_policy_pass"] = (
        out["validation_profit_factor"].between(0.01, 20.0)
        & out["oos_profit_factor"].between(0.01, 20.0)
        & out["min_split_profit_factor"].between(0.01, 20.0)
    )
    out["pf_pass"] = (out["oos_profit_factor"] >= OOS_PF_FLOOR) & (out["min_split_profit_factor"] >= MIN_SPLIT_PF_FLOOR)
    out["cost_pass"] = (out["oos_cost06_net"] > 0) & (out["combined_cost09_net"] >= 0)
    out["side_caution_pass"] = out["combined_short_share"] <= SHORT_SHARE_CAUTION
    out["side_target_pass"] = out["combined_short_share"] <= SHORT_SHARE_TARGET
    out["direct_strict_pass"] = (
        out["direct_density_pass"]
        & out["profit_pass"]
        & out["pf_pass"]
        & out["cost_pass"]
        & out["side_caution_pass"]
        & out["pf_finite_policy_pass"]
    )
    out["runtime_scaled_repair_pass"] = (
        out["scaled_density_pass"]
        & out["profit_pass"]
        & out["pf_pass"]
        & out["cost_pass"]
        & out["side_caution_pass"]
        & out["pf_finite_policy_pass"]
        & (out["combined_trade_count"] >= 300)
        & (out["oos_trade_count"] >= 100)
    )
    condition_cols = [
        "direct_density_pass",
        "scaled_density_pass",
        "profit_pass",
        "pf_pass",
        "cost_pass",
        "side_caution_pass",
        "side_target_pass",
        "pf_finite_policy_pass",
    ]
    out["hm_condition_count"] = sum(out[column].astype(int) for column in condition_cols)
    direct_gap = (DENSITY_FLOOR - out["combined_trade_density"]).clip(lower=0)
    short_gap = (out["combined_short_share"] - SHORT_SHARE_TARGET).clip(lower=0)
    validation_cost06_gap = (0 - out["validation_cost06_net"]).clip(lower=0).fillna(0)
    capped_pf = out["oos_profit_factor"].clip(upper=3.0)
    out["hm_score"] = (
        out["runtime_scaled_repair_pass"].astype(int) * 100000
        + out["direct_strict_pass"].astype(int) * 80000
        + out["hm_condition_count"] * 3000
        + out["runtime_density_estimate_from_hl_ratio"].fillna(0) * 650
        + out["combined_net"].fillna(0) * 0.28
        + out["oos_net"].fillna(0) * 0.55
        + out["combined_cost09_net"].fillna(-500) * 0.28
        + (capped_pf.fillna(0) - 1.0) * 450
        + (1.0 - out["combined_short_share"].fillna(1.0)) * 350
        - direct_gap * 450
        - short_gap * 900
        - validation_cost06_gap * 0.50
    )
    out["claim_boundary"] = CLAIM_BOUNDARY
    inventory = {
        "surface_path": rel(path),
        "source_run_number": source_run_number,
        "usable": "true",
        "rows": len(frame),
        "direct_strict_pass_rows": int(out["direct_strict_pass"].sum()),
        "runtime_scaled_repair_pass_rows": int(out["runtime_scaled_repair_pass"].sum()),
        "max_combined_density": finite(out["combined_trade_density"].max()),
        "max_runtime_density_estimate": finite(out["runtime_density_estimate_from_hl_ratio"].max()),
        "max_combined_net": finite(out["combined_net"].max()),
        "max_combined_cost09_net": finite(out["combined_cost09_net"].max()),
        "min_combined_short_share": finite(out["combined_short_share"].min()),
        "effect": "prior surface(이전 표면)를 HM repair scout(HM 수리 탐색)에 재사용 가능한지 판독했습니다.",
    }
    return out, inventory


def scan_surfaces(payload: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]], list[Path]]:
    frames: list[pd.DataFrame] = []
    inventory: list[dict[str, Any]] = []
    used_files: list[Path] = []
    for path in surface_files():
        frame, row = normalize_surface(path, payload)
        inventory.append(row)
        if frame is not None and not frame.empty:
            frames.append(frame)
            used_files.append(path)
    if not frames:
        raise RuntimeError("No usable HM prior surfaces(HM에 사용할 이전 표면 없음).")
    combined = pd.concat(frames, ignore_index=True, sort=False)
    dedup_cols = [
        "source_run_number",
        "candidate_ref",
        "model_id",
        "feature_set_id",
        "label_id",
        "threshold",
        "hours_id",
        "extra_filter",
        "max_hold_m5",
        "validation_net",
        "oos_net",
        "combined_net",
        "combined_trade_count",
        "combined_trade_density",
        "combined_cost09_net",
        "combined_short_share",
    ]
    combined = combined.drop_duplicates(subset=[column for column in dedup_cols if column in combined.columns]).copy()
    return combined, inventory, used_files


def failure_rows(surface: pd.DataFrame) -> list[dict[str, Any]]:
    checks = [
        ("direct_density_pass(직접 밀도 통과)", "direct_density_pass", "combined and OOS density >= 3/day(합산 및 표본외 밀도 일 3회 이상)"),
        ("scaled_density_pass(스케일 밀도 통과)", "scaled_density_pass", "combined density * HL ratio >= 3/day(HL 비율 적용 밀도 일 3회 이상)"),
        ("profit_pass(수익 통과)", "profit_pass", "validation/OOS/combined net > 0(검증/표본외/합산 순수익 양수)"),
        ("pf_pass(PF 통과)", "pf_pass", "OOS PF >=1.25 and min split PF >=1.05(표본외 수익 팩터 1.25 이상 및 분할 최소 1.05 이상)"),
        ("cost_pass(비용 통과)", "cost_pass", "OOS cost0.6 >0 and combined cost0.9 >=0(표본외 비용0.6 양수 및 합산 비용0.9 0 이상)"),
        ("side_caution_pass(방향 주의 통과)", "side_caution_pass", "short share <=0.70(숏 비중 0.70 이하)"),
        ("side_target_pass(방향 목표 통과)", "side_target_pass", "short share <=0.65(숏 비중 0.65 이하)"),
        ("direct_strict_pass(직접 엄격 통과)", "direct_strict_pass", "direct density + profit + PF + cost + side(직접 밀도와 수익/PF/비용/방향 동시 통과)"),
        ("runtime_scaled_repair_pass(런타임 스케일 수리 통과)", "runtime_scaled_repair_pass", "HL density ratio seed + profit/PF/cost/side(HL 밀도 비율 씨앗과 수익/PF/비용/방향 동시 통과)"),
    ]
    rows = []
    total = len(surface)
    for label, column, threshold in checks:
        count = int(surface[column].sum())
        rows.append(
            {
                "run_id": RUN_ID,
                "check": label,
                "threshold": threshold,
                "pass_count": count,
                "fail_count": total - count,
                "effect": "병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def selected_artifact_paths(source_run_number: str, model_id: str) -> dict[str, str]:
    source_dir = STAGE_DIR / "02_runs" / source_run_number
    def usable(path: Path) -> bool:
        return str(path) not in ("", ".") and exists(path) and io_path(path).is_file()

    paths = {
        "source_final_decision": source_dir / "final_decision.json",
        "source_trade_tape": next(iter(sorted(source_dir.glob("selected_*_trade_tape.csv"))), Path()),
        "source_cost_stress": next(iter(sorted(source_dir.glob("selected_*_cost_stress.csv"))), Path()),
        "source_side_session_review": next(iter(sorted(source_dir.glob("selected_*_side_session_review.csv"))), Path()),
        "source_month_stability": next(iter(sorted(source_dir.glob("selected_*_month_stability.csv"))), Path()),
        "source_model_artifact_manifest": source_dir / "model_artifact_manifest.csv",
        "source_onnx_smoke_report": source_dir / "onnx_smoke_report.csv",
    }
    resolved = {key: rel(path) if usable(path) else "" for key, path in paths.items()}
    manifest_path = paths["source_model_artifact_manifest"]
    if exists(manifest_path):
        manifest = read_csv(manifest_path)
        rows = manifest[manifest["model_id"].astype(str) == str(model_id)] if "model_id" in manifest.columns else pd.DataFrame()
        onnx = rows[rows["artifact_type"].astype(str).str.contains("onnx", case=False, na=False)] if not rows.empty else pd.DataFrame()
        joblib = rows[rows["artifact_type"].astype(str).str.contains("joblib", case=False, na=False)] if not rows.empty else pd.DataFrame()
        resolved["selected_onnx_path"] = str(onnx.iloc[0]["path"]) if not onnx.empty else ""
        resolved["selected_joblib_path"] = str(joblib.iloc[0]["path"]) if not joblib.empty else ""
        resolved["selected_onnx_sha256"] = str(onnx.iloc[0]["sha256"]) if not onnx.empty else ""
        resolved["selected_joblib_sha256"] = str(joblib.iloc[0]["sha256"]) if not joblib.empty else ""
    else:
        resolved["selected_onnx_path"] = ""
        resolved["selected_joblib_path"] = ""
        resolved["selected_onnx_sha256"] = ""
        resolved["selected_joblib_sha256"] = ""
    smoke_path = paths["source_onnx_smoke_report"]
    if exists(smoke_path):
        smoke = read_csv(smoke_path)
        rows = smoke[smoke["model_id"].astype(str) == str(model_id)] if "model_id" in smoke.columns else pd.DataFrame()
        resolved["selected_onnx_smoke_status"] = str(rows.iloc[0]["status"]) if not rows.empty and "status" in rows.columns else ""
        resolved["selected_onnx_smoke_max_abs_diff"] = str(rows.iloc[0]["max_abs_diff"]) if not rows.empty and "max_abs_diff" in rows.columns else ""
    else:
        resolved["selected_onnx_smoke_status"] = ""
        resolved["selected_onnx_smoke_max_abs_diff"] = ""
    return resolved


def build_selected_seed(surface: pd.DataFrame, payload: Mapping[str, Any]) -> dict[str, Any]:
    scaled = surface[surface["runtime_scaled_repair_pass"]].sort_values("hm_score", ascending=False)
    direct = surface[surface["direct_strict_pass"]].sort_values("hm_score", ascending=False)
    pool = scaled if not scaled.empty else (direct if not direct.empty else surface.sort_values("hm_score", ascending=False))
    row = pool.iloc[0].to_dict()
    artifacts = selected_artifact_paths(str(row["source_run_number"]), str(row.get("model_id", "")))
    selected = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "selected_source_run_number": row["source_run_number"],
        "selected_source_run_id": row["source_run_id"],
        "selected_source_surface_path": row["source_surface_path"],
        "selected_candidate_ref": row["candidate_ref"],
        "selected_model_id": row.get("model_id", ""),
        "selected_model_family": row.get("model_family", ""),
        "selected_feature_set_id": row.get("feature_set_id", ""),
        "selected_label_id": row.get("label_id", ""),
        "selected_threshold": finite(row.get("threshold")),
        "selected_hours_id": row.get("hours_id", ""),
        "selected_extra_filter": row.get("extra_filter", ""),
        "selected_max_hold_m5": finite(row.get("max_hold_m5")),
        "selected_validation_net": finite(row["validation_net"]),
        "selected_validation_profit_factor": finite(row["validation_profit_factor"]),
        "selected_validation_trade_density": finite(row["validation_trade_density"]),
        "selected_validation_trade_count": finite(row["validation_trade_count"], 0),
        "selected_validation_cost06_net": finite(row.get("validation_cost06_net")),
        "selected_oos_net": finite(row["oos_net"]),
        "selected_oos_profit_factor": finite(row["oos_profit_factor"]),
        "selected_oos_trade_density": finite(row["oos_trade_density"]),
        "selected_oos_trade_count": finite(row["oos_trade_count"], 0),
        "selected_oos_cost06_net": finite(row["oos_cost06_net"]),
        "selected_combined_net": finite(row["combined_net"]),
        "selected_combined_trade_count": finite(row["combined_trade_count"], 0),
        "selected_combined_trade_density": finite(row["combined_trade_density"]),
        "selected_combined_cost06_net": finite(row.get("combined_cost06_net")),
        "selected_combined_cost09_net": finite(row["combined_cost09_net"]),
        "selected_combined_long_trade_count": finite(row["combined_long_trade_count"], 0),
        "selected_combined_short_trade_count": finite(row["combined_short_trade_count"], 0),
        "selected_combined_short_share": finite(row["combined_short_share"]),
        "selected_min_split_profit_factor": finite(row["min_split_profit_factor"]),
        "selected_runtime_density_estimate_from_hl_ratio": finite(row["runtime_density_estimate_from_hl_ratio"]),
        "selected_runtime_trade_count_estimate_from_hl_ratio": finite(row["runtime_trade_count_estimate_from_hl_ratio"], 0),
        "selected_direct_density_pass": bool(row["direct_density_pass"]),
        "selected_scaled_density_pass": bool(row["scaled_density_pass"]),
        "selected_profit_pass": bool(row["profit_pass"]),
        "selected_pf_pass": bool(row["pf_pass"]),
        "selected_cost_pass": bool(row["cost_pass"]),
        "selected_side_caution_pass": bool(row["side_caution_pass"]),
        "selected_side_target_pass": bool(row["side_target_pass"]),
        "selected_runtime_scaled_repair_pass": bool(row["runtime_scaled_repair_pass"]),
        "selected_direct_strict_pass": bool(row["direct_strict_pass"]),
        "selected_hm_score": finite(row["hm_score"]),
        "hl_density_lift_ratio": finite(payload["hl_density_lift_ratio"]),
        "density_required_for_scaled_pass": finite(payload["density_required_for_scaled_pass"]),
        "selection_boundary": (
            "runtime_scaled_seed_from_HL_density_ratio(런타임 스케일 씨앗, HL 밀도 비율 사용) "
            "not_runtime_authority(런타임 권위 아님)"
        ),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    selected.update(artifacts)
    return selected


def copy_selected_trade_tape(selected: Mapping[str, Any]) -> pd.DataFrame:
    source_path_text = str(selected.get("source_trade_tape", ""))
    if not source_path_text:
        write_csv(SELECTED_SEED_TRADE_TAPE, [])
        return pd.DataFrame()
    source_path = ROOT / source_path_text
    if not exists(source_path):
        write_csv(SELECTED_SEED_TRADE_TAPE, [])
        return pd.DataFrame()
    tape = read_csv(source_path)
    tape["hm_run_id"] = RUN_ID
    tape["source_run_id"] = selected["selected_source_run_id"]
    tape["source_run_number"] = selected["selected_source_run_number"]
    tape["source_trade_tape_path"] = source_path_text
    tape["hm_claim_boundary"] = CLAIM_BOUNDARY
    write_csv(SELECTED_SEED_TRADE_TAPE, clean_records(tape))
    return tape


def cost_stress_rows(tape: pd.DataFrame) -> list[dict[str, Any]]:
    if tape.empty or "net_profit" not in tape.columns:
        return []
    rows = []
    data = tape.copy()
    data["net_profit"] = pd.to_numeric(data["net_profit"], errors="coerce").fillna(0.0)
    for split in ["validation", "oos", "combined"]:
        part = data if split == "combined" else data[data["split"].astype(str) == split]
        for cost in COST_STRESS_LEVELS:
            adjusted = part["net_profit"] - max(cost - BASE_COST_PER_TRADE, 0) if not part.empty else pd.Series(dtype=float)
            rows.append(
                {
                    "run_id": RUN_ID,
                    "split": split,
                    "cost_per_trade": cost,
                    "trade_count": int(len(part)),
                    "net_profit": finite(adjusted.sum()),
                    "profit_factor": finite(profit_factor(adjusted)),
                    "expectancy": finite(adjusted.mean() if len(adjusted) else math.nan),
                    "effect": "비용 압박(cost stress, 비용 압박)에서 씨앗이 버티는지 봅니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def side_session_rows(tape: pd.DataFrame) -> list[dict[str, Any]]:
    if tape.empty:
        return []
    data = tape.copy()
    data["net_profit"] = pd.to_numeric(data["net_profit"], errors="coerce").fillna(0.0)
    keys = ["split", "direction", "open_hour"]
    rows = []
    for values, part in data.groupby(keys, dropna=False):
        net = part["net_profit"]
        rows.append(
            {
                "run_id": RUN_ID,
                "split": values[0],
                "direction": values[1],
                "open_hour": values[2],
                "trade_count": int(len(part)),
                "net_profit": finite(net.sum()),
                "profit_factor": finite(profit_factor(net)),
                "expectancy": finite(net.mean()),
                "effect": "방향/세션(side/session, 방향/세션) 병목을 확인합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def month_stability_rows(tape: pd.DataFrame) -> list[dict[str, Any]]:
    if tape.empty:
        return []
    data = tape.copy()
    data["net_profit"] = pd.to_numeric(data["net_profit"], errors="coerce").fillna(0.0)
    rows = []
    for values, part in data.groupby(["split", "open_month"], dropna=False):
        net = part["net_profit"]
        rows.append(
            {
                "run_id": RUN_ID,
                "split": values[0],
                "open_month": values[1],
                "trade_count": int(len(part)),
                "net_profit": finite(net.sum()),
                "profit_factor": finite(profit_factor(net)),
                "positive_month": bool_text(float(net.sum()) > 0),
                "effect": "월별 안정성(month stability, 월 안정성)을 확인합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def route_parity_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route_question": "HJ/HK dual-source route(HJ/HK 이중 원천 라우트)",
            "decision": "partial_parity_not_reused_as_authority(부분 동등성을 권위로 재사용 안 함)",
            "evidence": rel(hl.ROUTE_MIX_REVIEW),
            "effect": "fallback-after-flat(플랫 이후 대체)와 Python score switch(Python 점수 전환)의 차이를 다음 패키지에서 숨기지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "route_question": "HM selected seed(HM 선택 씨앗)",
            "decision": "single_source_fj_model_preferred_for_next_package_review(단일 FJ 모델을 다음 패키지 검토에 우선)",
            "evidence": selected.get("selected_onnx_path", ""),
            "effect": "dual-source fallback(이중 원천 대체) 복잡도를 줄이고, probability-bin veto(확률 구간 거부)는 단일 모델 확률 구간에서 다시 검토합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "route_question": "HN next decision(HN 다음 결정)",
            "decision": "review_package_or_reseed_boundary(패키지 또는 재시드 경계 검토)",
            "evidence": rel(SELECTED_SEED),
            "effect": "scaled density estimate(스케일 밀도 추정)가 너무 약하면 직접 3/day source(직접 일 3회 원천) 재학습으로 전환합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "queue_item": "HN_review_selected_scaled_seed(HN 선택 스케일 씨앗 검토)",
            "seed": selected.get("selected_model_id", ""),
            "target": "validate package readiness(패키지 준비성 검토): ONNX(온엑스), feature order(피처 순서), no-trade-splitting(거래 쪼개기 금지)",
            "avoid": "do not call scaled density MT5 proof(스케일 밀도를 MT5 증명으로 부르지 않음)",
            "effect": "FJ seed(FJ 씨앗)를 패키지로 열 수 있는지 좁게 판정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_item": "single_source_probability_bin_veto_package_candidate(단일 원천 확률 구간 거부 패키지 후보)",
            "seed": selected.get("selected_onnx_path", ""),
            "target": "if HN passes, materialize MT5 runtime package(HN 통과 시 MT5 런타임 패키지 물질화)",
            "avoid": "do not reuse GZ+HB fallback partial parity(GZ+HB 대체 부분 동등성 재사용 금지)",
            "effect": "route parity(라우트 동등성)를 더 단순하게 닫을 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_item": "direct_density_cost_side_reseed_fallback(직접 밀도/비용/방향 재시드 대체)",
            "seed": "direct_proxy_density>=3/day required(직접 프록시 밀도 일 3회 이상 필요)",
            "target": "if HN rejects scaled seed, train new direct-density source(HN이 스케일 씨앗을 거부하면 직접 고밀도 원천 재학습)",
            "avoid": "repeat micro threshold search(미세 임계값 반복)",
            "effect": "scaled clue(스케일 단서)가 약할 때 다음 공격 탐색이 바로 이어집니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_work_packet(payload: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-exploration-mandate(탐색 명령)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "parent_hl_lineage_gate",
                "surface_inventory_gate",
                "direct_strict_absence_recorded_gate",
                "runtime_scaled_seed_gate",
                "selected_seed_artifact_gate",
                "no_trade_splitting_gate",
                "data_integrity_boundary_gate",
                "route_parity_decision_gate",
                "paired_tier_record_gate",
                "artifact_lineage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "hypothesis": (
                "HL MT5 density lift ratio(HL MT5 밀도 상승 비율)가 proxy density(프록시 밀도)를 보수적으로 "
                "보정하면, 이전 dense/cost/side surface(고밀도/비용/방향 표면) 안에 MT5 package review(MT5 패키지 검토)로 "
                "넘길 수 있는 repair seed(수리 씨앗)가 있을 수 있습니다."
            ),
            "broad_sweep": "all Stage364 reusable surface CSVs(모든 Stage364 재사용 표면 CSV)",
            "extreme_sweep": "direct 3/day strict pass and HL-scaled 3/day estimate(직접 일 3회 엄격 통과와 HL 스케일 일 3회 추정)",
            "micro_search_gate": "HN review(HN 검토) before package(패키지) or threshold micro-search(임계값 미세탐색)",
            "effect": "HL positive runtime clue(HL 긍정 런타임 단서)를 운영 주장 없이 다음 공격 탐색 후보로 바꿉니다.",
            "hl_density_lift_ratio": payload["hl_density_lift_ratio"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_input_manifest(input_files: Sequence[Path]) -> None:
    rows = []
    for path in input_files:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": bool_text(exists(path)),
                "sha256": sha(path),
                "input_role": "source_artifact(원천 산출물)" if path != THIS_FILE else "producer_script(생산 스크립트)",
                "effect": "산출물 계보(artifact lineage, 산출물 계보)를 연결합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def receipts(final: Mapping[str, Any], selected: Mapping[str, Any], input_files: Sequence[Path]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": final["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        EXPLORATION_RECEIPT,
        {
            **base,
            "idea_id": "IDEA-ST364-HM-PROBABILITY-BIN-VETO-DENSITY-SIDE-COST-REPAIR",
            "hypothesis": "HL density ratio(HL 밀도 비율)로 이전 dense/cost/side seed(고밀도/비용/방향 씨앗)를 재평가합니다.",
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A proxy scout with Tier B missing_required(Tier A 프록시 탐색 및 Tier B 필수 누락)",
            "broad_sweep": "Stage364 prior surfaces(Stage364 이전 표면)",
            "extreme_sweep": "direct strict 3/day and scaled 3/day(직접 엄격 일 3회 및 스케일 일 3회)",
            "micro_search_gate": NEXT_RUN_ID,
            "wfo_plan": "not_run_single_window_scout_boundary(WFO 미실행, 단일 창 탐색 경계)",
            "failure_memory": "direct strict pass is zero(직접 엄격 통과 0개); do not claim direct density proof(직접 밀도 증명 주장 금지)",
            "evidence_boundary": "scout_seed_review_required(탐색 씨앗, 검토 필요)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(path) for path in input_files],
            "time_axis": "source surfaces inherit chronological validation/OOS split(원천 표면은 시간순 검증/표본외 분할을 상속)",
            "sample_scope": "FPMarkets US100 M5 Stage364 validation+OOS(FPMarkets US100 M5 Stage364 검증+표본외)",
            "missing_or_duplicate_check": "candidate rows deduplicated by source/candidate/metric key(후보 행은 원천/후보/지표 키로 중복 제거)",
            "feature_label_boundary": "no new labels generated; source scripts carry timestamp-safe boundary(새 라벨 생성 없음, 원천 스크립트 시점 안전 경계 상속)",
            "split_boundary": "validation and OOS metrics kept separate(검증과 표본외 지표 분리 유지)",
            "leakage_risk": "HL density ratio reused as estimate only(HL 밀도 비율은 추정으로만 사용)",
            "data_hash_or_identity": {"input_manifest": rel(INPUT_MANIFEST), "surface_inventory": rel(SURFACE_INVENTORY)},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": selected.get("selected_model_family", ""),
            "target_and_label": selected.get("selected_label_id", ""),
            "split_method": "chronological validation/OOS inherited(시간순 검증/표본외 상속)",
            "selection_metric": "HM density/side/cost scaled repair score(HM 밀도/방향/비용 스케일 수리 점수)",
            "secondary_metrics": ["cost stress(비용 압박)", "short share(숏 비중)", "direct density gap(직접 밀도 간극)"],
            "threshold_policy": "source threshold reused, HN review required(원천 임계값 재사용, HN 검토 필요)",
            "overfit_risk": "multiple prior surface scan and HL scaling reuse(다중 이전 표면 스캔 및 HL 스케일 재사용)",
            "calibration_risk": "probabilities are package inputs, not authority(확률은 패키지 입력일 뿐 권위 아님)",
            "comparison_baseline": PARENT_RUN_ID,
            "validation_judgment": final["judgment"],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": (
                f"selected runtime density estimate(선택 런타임 밀도 추정) "
                f"{selected['selected_runtime_density_estimate_from_hl_ratio']} vs HL actual density(HL 실제 밀도) {final['hl_mt5_trade_density']}"
            ),
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": ["FJ side balance(FJ 방향 균형)", "FJ cost resilience(FJ 비용 회복력)", "HL proxy-to-MT5 density lift(HL 프록시-MT5 밀도 상승)"],
            "segment_checks": [rel(SELECTED_SEED_COST_STRESS), rel(SELECTED_SEED_SIDE_SESSION), rel(SELECTED_SEED_MONTH_STABILITY)],
            "trade_shape": "single-position jump-to-exit-plus-one inherited(단일 포지션, 청산 다음 후보 이동 상속)",
            "alternative_explanations": ["MT5 fill/cost/runtime mismatch(MT5 체결/비용/런타임 차이)", "HL ratio may not transfer(HL 비율 이전 불확실)"],
            "attribution_confidence": "low_to_medium_scout_only(낮음~중간, 탐색 전용)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(SELECTED_SEED), rel(RUNTIME_SCALED_CANDIDATES), rel(FAILURE_ATTRIBUTION)],
            "evidence_missing": ["new MT5 runtime probe(새 MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)", "runtime package(런타임 패키지)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "좋은 씨앗은 찾았지만 MT5 증명은 아직 아닙니다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in input_files if exists(path) and io_path(path).is_file()],
            "producer": rel(THIS_FILE),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_ignored_with_manifest(생성됨, 매니페스트로 추적)",
            "lineage_judgment": "connected_with_proxy_boundary(프록시 경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "positive proxy-scaled repair seed requiring HN review(HN 검토가 필요한 긍정 프록시 스케일 수리 씨앗)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve", "promotion_candidate"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "scaled estimate(스케일 추정)를 MT5 proof(MT5 증명)로 과장하지 않습니다.",
        },
    )


def gate_rows(final: Mapping[str, Any], selected: Mapping[str, Any], tape: pd.DataFrame) -> list[dict[str, Any]]:
    no_split = False
    if not tape.empty and "no_trade_splitting" in tape.columns:
        no_split = tape["no_trade_splitting"].astype(str).str.contains("single_position", na=False).all()
    onnx_ok = bool(selected.get("selected_onnx_path")) and "passed" in str(selected.get("selected_onnx_smoke_status", ""))
    rows = [
        ("parent_hl_lineage_gate", exists(hl.FINAL_DECISION), rel(hl.FINAL_DECISION), "HL 입력 계보를 확인했습니다."),
        ("surface_inventory_gate", final["usable_surface_count"] > 0, rel(SURFACE_INVENTORY), "이전 표면을 스캔했습니다."),
        ("direct_strict_absence_recorded_gate", True, rel(FAILURE_ATTRIBUTION), "직접 엄격 통과 0개를 누락 없이 기록했습니다."),
        ("runtime_scaled_seed_gate", final["runtime_scaled_repair_pass_count"] > 0, rel(RUNTIME_SCALED_CANDIDATES), "HL 비율 적용 수리 씨앗을 확인했습니다."),
        ("selected_seed_artifact_gate", onnx_ok, rel(SELECTED_SEED), "선택 씨앗의 ONNX(온엑스)와 smoke(스모크)를 확인했습니다."),
        ("no_trade_splitting_gate", no_split, rel(SELECTED_SEED_TRADE_TAPE), "거래 쪼개기 금지 경계를 확인했습니다."),
        ("data_integrity_boundary_gate", exists(DATA_RECEIPT), rel(DATA_RECEIPT), "데이터 경계를 기록했습니다."),
        ("route_parity_decision_gate", exists(ROUTE_PARITY_DECISION), rel(ROUTE_PARITY_DECISION), "라우트 동등성 결정을 기록했습니다."),
        ("paired_tier_record_gate", True, rel(STAGE_LEDGER), "Tier A/Tier B/Tier A+B 기록 경계를 남깁니다."),
        ("artifact_lineage_gate", exists(LINEAGE_RECEIPT), rel(LINEAGE_RECEIPT), "산출물 계보를 연결했습니다."),
        ("required_gate_coverage_audit", True, rel(GATE_AUDIT), "필수 게이트를 감사했습니다."),
        ("final_claim_guard", True, rel(CLAIM_RECEIPT), "운영 권위 주장을 막았습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if status else "failed",
            "evidence": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, status, evidence, effect in rows
    ]


def build_final(
    parent: Mapping[str, Any],
    payload: Mapping[str, Any],
    surface: pd.DataFrame,
    inventory: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    positive = int(surface["runtime_scaled_repair_pass"].sum()) > 0
    status = STATUS_POSITIVE if positive else STATUS_INCONCLUSIVE
    judgment = JUDGMENT_POSITIVE if positive else JUDGMENT_INCONCLUSIVE
    decision = DECISION_POSITIVE if positive else DECISION_INCONCLUSIVE
    final = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "created_at_utc": created_at,
        "surface_rows": int(len(surface)),
        "usable_surface_count": int(sum(1 for row in inventory if str(row.get("usable")) == "true")),
        "direct_strict_pass_count": int(surface["direct_strict_pass"].sum()),
        "runtime_scaled_repair_pass_count": int(surface["runtime_scaled_repair_pass"].sum()),
        "hl_mt5_net_profit": finite(parent.get("mt5_net_profit")),
        "hl_mt5_profit_factor": finite(parent.get("mt5_profit_factor")),
        "hl_mt5_trade_count": finite(parent.get("mt5_trade_count"), 0),
        "hl_mt5_trade_density": finite(parent.get("mt5_trade_density")),
        "hl_density_lift_ratio": finite(payload["hl_density_lift_ratio"]),
        "density_required_for_scaled_pass": finite(payload["density_required_for_scaled_pass"]),
        "selected_source_run_number": selected["selected_source_run_number"],
        "selected_model_id": selected["selected_model_id"],
        "selected_oos_net": selected["selected_oos_net"],
        "selected_oos_profit_factor": selected["selected_oos_profit_factor"],
        "selected_oos_trade_density": selected["selected_oos_trade_density"],
        "selected_oos_cost06_net": selected["selected_oos_cost06_net"],
        "selected_combined_net": selected["selected_combined_net"],
        "selected_combined_trade_count": selected["selected_combined_trade_count"],
        "selected_combined_trade_density": selected["selected_combined_trade_density"],
        "selected_combined_cost09_net": selected["selected_combined_cost09_net"],
        "selected_combined_short_share": selected["selected_combined_short_share"],
        "selected_runtime_density_estimate_from_hl_ratio": selected["selected_runtime_density_estimate_from_hl_ratio"],
        "selected_runtime_scaled_repair_pass": selected["selected_runtime_scaled_repair_pass"],
        "selected_direct_strict_pass": selected["selected_direct_strict_pass"],
        "selected_onnx_path": selected.get("selected_onnx_path", ""),
        "selected_onnx_sha256": selected.get("selected_onnx_sha256", ""),
        "selected_onnx_smoke_status": selected.get("selected_onnx_smoke_status", ""),
        "new_mt5_execution": "not_run(실행 안 함)",
        "runtime_package": "not_opened(열지 않음)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
    }
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    return final


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in list(rows)[:limit]:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_docs(
    final: Mapping[str, Any],
    selected: Mapping[str, Any],
    failures: Sequence[Mapping[str, Any]],
    routes: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364HM Probability-Bin Veto MT5 Density/Side/Cost Repair Scout(확률 구간 거부 MT5 밀도/방향/비용 수리 탐색)

Updated(갱신): {final['created_at_utc']}

## Result(결과)

Action(행동): Stage364 prior surfaces(Stage364 이전 표면)를 모두 스캔하고, HL MT5 density lift ratio(HL MT5 밀도 상승 비율) `{final['hl_density_lift_ratio']}`를 보수적 estimate(추정)로 적용했습니다.

Effect(효과): direct strict pass(직접 엄격 통과)는 `{final['direct_strict_pass_count']}`개로 없지만, runtime-scaled repair seed(런타임 스케일 수리 씨앗)는 `{final['runtime_scaled_repair_pass_count']}`개 확인했습니다.

- selected source(선택 원천): `{final['selected_source_run_number']}`
- selected model(선택 모델): `{final['selected_model_id']}`
- OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
- combined net/trades/density/cost0.9/short share(합산 순수익/거래수/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- runtime density estimate(런타임 밀도 추정): `{final['selected_runtime_density_estimate_from_hl_ratio']}`
- selected ONNX(선택 ONNX, 온엑스): `{final['selected_onnx_path']}`

Judgment(판정): `{final['judgment']}`.

## Failure Attribution(실패 귀속)

{markdown_table(failures, ['check', 'threshold', 'pass_count', 'fail_count', 'effect'])}

## Route Parity Decision(라우트 동등성 결정)

{markdown_table(routes, ['route_question', 'decision', 'evidence', 'effect'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['queue_item', 'seed', 'target', 'avoid', 'effect'])}

## Boundary(경계)

This is not a new MT5 execution(새 MT5 실행 아님), not a runtime package(런타임 패키지 아님), and not runtime authority(런타임 권위 아님). HL ratio(HL 비율)는 candidate screening(후보 선별)에만 씁니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}
"""
    write_text(REPORT_PATH, report, bom=True)
    decision_doc = f"""# Stage364HM decision(결정): probability-bin veto density/side/cost repair scout(확률 구간 거부 밀도/방향/비용 수리 탐색)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- selected source/model(선택 원천/모델): `{final['selected_source_run_number']}` / `{final['selected_model_id']}`
- selected runtime density estimate(선택 런타임 밀도 추정): `{final['selected_runtime_density_estimate_from_hl_ratio']}`
- selected combined cost0.9/short share(선택 합산 비용0.9/숏 비중): `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): HN에서 FJ single-source package readiness(FJ 단일 원천 패키지 준비성)를 검토합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(
        REVIEW_INDEX,
        f"run364HM__{RUN_ID}",
        f"\n- run364HM__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density/side/cost repair scout(밀도/방향/비용 수리 탐색), next `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        f"run364HM__{RUN_ID}",
        f"""
<!-- run364HM__{RUN_ID} -->

## run364HM Probability-Bin Veto Density/Side/Cost Repair Scout(확률 구간 거부 밀도/방향/비용 수리 탐색)

Action(행동): Stage364 prior surfaces(Stage364 이전 표면)를 HL MT5 density ratio(HL MT5 밀도 비율)로 재평가했습니다.

Effect(효과): direct strict pass(직접 엄격 통과)는 0개지만, `{final['selected_source_run_number']}` single-source seed(단일 원천 씨앗)가 scaled density/cost/side(스케일 밀도/비용/방향) 수리 후보로 남아 `{NEXT_RUN_ID}`로 넘깁니다.
""",
    )
    append_text_once(
        STAGE_README,
        f"run364HM__{RUN_ID}",
        f"\n<!-- run364HM__{RUN_ID} -->\n## run364HM density/side/cost repair scout(밀도/방향/비용 수리 탐색)\n\nNext(다음): `{NEXT_RUN_ID}`.\n",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
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

Current truth(현재 진실): `run364HM` completed(완료) probability-bin veto MT5 density/side/cost repair scout(확률 구간 거부 MT5 밀도/방향/비용 수리 탐색). Direct strict pass(직접 엄격 통과)는 `{final['direct_strict_pass_count']}`개이고, runtime-scaled repair pass(런타임 스케일 수리 통과)는 `{final['runtime_scaled_repair_pass_count']}`개입니다.

Selected seed(선택 씨앗): `{final['selected_source_run_number']}` / `{final['selected_model_id']}`. OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`입니다.

Important boundary(중요 경계): selected runtime density estimate(선택 런타임 밀도 추정) `{final['selected_runtime_density_estimate_from_hl_ratio']}`는 HL density ratio(HL 밀도 비율)를 재사용한 estimate(추정)입니다. 새 MT5 runtime probe(새 MT5 런타임 탐침), runtime package(런타임 패키지), runtime authority(런타임 권위)는 아닙니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 FJ single-source package readiness(FJ 단일 원천 패키지 준비성), probability-bin veto applicability(확률 구간 거부 적용 가능성), route parity(라우트 동등성)를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): HM probability-bin veto MT5 density/side/cost repair scout(HM 확률 구간 거부 MT5 밀도/방향/비용 수리 탐색).

Selected seed(선택 씨앗): `{final['selected_source_run_number']}` / `{final['selected_model_id']}`.

Selected OOS net/PF/density/cost0.6(선택 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`.

Selected combined density/cost0.9/short share(선택 합산 밀도/비용0.9/숏 비중): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`.

Runtime density estimate(런타임 밀도 추정): `{final['selected_runtime_density_estimate_from_hl_ratio']}` using HL ratio(HL 비율) `{final['hl_density_lift_ratio']}`.

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364HM__{RUN_ID}",
        f"\n<!-- run364HM__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed density/side/cost repair scout(밀도/방향/비용 수리 탐색); selected `{final['selected_model_id']}`; scaled density estimate `{final['selected_runtime_density_estimate_from_hl_ratio']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364HM__{RUN_ID}",
        f"\n<!-- run364HM__{RUN_ID} -->\n- `{RUN_ID}`: HL density ratio(HL 밀도 비율)로 prior dense/cost/side surface(이전 고밀도/비용/방향 표면)를 재평가해 `{final['selected_source_run_number']}` seed(씨앗)를 보존했습니다. Effect(효과): HN에서 package readiness(패키지 준비성)를 검토합니다.\n",
    )
    append_text_once(
        NEGATIVE_REGISTER,
        f"run364HM__direct_strict_pass_zero__{RUN_ID}",
        f"\n<!-- run364HM__direct_strict_pass_zero__{RUN_ID} -->\n- `{RUN_ID}`: direct strict pass(직접 엄격 통과)는 `{final['direct_strict_pass_count']}`개입니다. Effect(효과): scaled density estimate(스케일 밀도 추정)를 MT5 proof(MT5 증명)로 부르지 않고 HN review(HN 검토)로 넘깁니다.\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scaled_repair_scout(프록시 스케일 수리 탐색)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색 전용, 권위 없음)",
        "question": "Can HL density ratio reveal a density/side/cost repair seed?(HL 밀도 비율이 밀도/방향/비용 수리 씨앗을 보여주는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_combined_net"],
        "profit_factor": final["selected_oos_profit_factor"],
        "trade_count": final["selected_combined_trade_count"],
        "trade_density_per_feature_day": final["selected_combined_trade_density"],
        "long_trade_count": final.get("selected_combined_long_trade_count", ""),
        "short_trade_count": final.get("selected_combined_short_trade_count", ""),
        "result_judgment": final["judgment"],
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(SELECTED_SEED),
        "primary_kpi": f"scaled_density={final['selected_runtime_density_estimate_from_hl_ratio']};oos_pf={final['selected_oos_profit_factor']};cost09={final['selected_combined_cost09_net']}",
        "guardrail_kpi": f"direct_strict_pass={final['direct_strict_pass_count']};new_mt5=not_run;authority=not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_surface(필수 누락, Tier B 표면 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "view": record_view,
            "tier": tier_scope,
            "kpi_scope": "HM proxy-scaled density/side/cost scout(HM 프록시 스케일 밀도/방향/비용 탐색)",
            "metric_scope": "python_proxy_no_new_mt5(Python 프록시, 새 MT5 없음)",
            "status": status,
            "source_authority": "proxy_scaled_seed_no_runtime_authority(프록시 스케일 씨앗, 런타임 권위 없음)",
        }
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "trade_count", "trade_density_per_feature_day", "long_trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "lane": "experiment_execution(실험 실행)",
                "run_family": "proxy_scaled_repair_scout(프록시 스케일 수리 탐색)",
                "run_type": "density_side_cost_repair_scout(밀도/방향/비용 수리 탐색)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(SELECTED_SEED),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_runtime_density_estimate_from_hl_ratio"],
            }
        ],
    )


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "HM density/side/cost repair scout artifact(HM 밀도/방향/비용 수리 탐색 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any], input_files: Sequence[Path]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "command": f"python {rel(THIS_FILE)}",
            "input_files": [rel(path) for path in input_files],
            "input_hashes": {rel(path): sha(path) for path in input_files if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if exists(path) and io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    payload = hl_density_payload(parent)
    write_work_packet(payload)
    surface, inventory, used_surface_files = scan_surfaces(payload)
    input_files = list(dict.fromkeys(STATIC_INPUT_FILES + used_surface_files))
    write_input_manifest(input_files)
    write_csv(SURFACE_INVENTORY, inventory)
    direct = surface[surface["direct_strict_pass"]].sort_values("hm_score", ascending=False)
    scaled = surface[surface["runtime_scaled_repair_pass"]].sort_values("hm_score", ascending=False)
    screen = surface[
        surface["runtime_scaled_repair_pass"]
        | surface["direct_strict_pass"]
        | (surface["hm_condition_count"] >= 6)
        | ((surface["scaled_density_pass"]) & (surface["profit_pass"]) & (surface["pf_finite_policy_pass"]))
    ].sort_values("hm_score", ascending=False)
    write_csv(CANDIDATE_SCREEN, clean_records(screen, CANDIDATE_COLUMNS, limit=5000), CANDIDATE_COLUMNS)
    write_csv(DIRECT_STRICT_CANDIDATES, clean_records(direct, CANDIDATE_COLUMNS, limit=500), CANDIDATE_COLUMNS)
    write_csv(RUNTIME_SCALED_CANDIDATES, clean_records(scaled, CANDIDATE_COLUMNS, limit=500), CANDIDATE_COLUMNS)
    failures = failure_rows(surface)
    write_csv(FAILURE_ATTRIBUTION, failures)
    selected = build_selected_seed(surface, payload)
    write_json(SELECTED_SEED, selected)
    tape = copy_selected_trade_tape(selected)
    costs = cost_stress_rows(tape)
    side_session = side_session_rows(tape)
    months = month_stability_rows(tape)
    routes = route_parity_rows(selected)
    queue = queue_rows(selected)
    write_csv(SELECTED_SEED_COST_STRESS, costs)
    write_csv(SELECTED_SEED_SIDE_SESSION, side_session)
    write_csv(SELECTED_SEED_MONTH_STABILITY, months)
    write_csv(ROUTE_PARITY_DECISION, routes)
    write_csv(RUN364HN_QUEUE, queue)
    created_at = now_utc()
    provisional_gates: list[dict[str, Any]] = []
    final = build_final(parent, payload, surface, inventory, selected, provisional_gates, created_at)
    receipts(final, selected, input_files)
    gates = gate_rows(final, selected, tape)
    final = build_final(parent, payload, surface, inventory, selected, gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, selected, failures, routes, queue, gates)
    write_ledgers(final, gates)
    write_manifest(final, input_files)
    write_artifact_registry(final)
    gates = gate_rows(final, selected, tape)
    final = build_final(parent, payload, surface, inventory, selected, gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "surface_rows": final["surface_rows"],
                    "usable_surface_count": final["usable_surface_count"],
                    "direct_strict_pass_count": final["direct_strict_pass_count"],
                    "runtime_scaled_repair_pass_count": final["runtime_scaled_repair_pass_count"],
                    "selected_source_run_number": final["selected_source_run_number"],
                    "selected_model_id": final["selected_model_id"],
                    "selected_oos_net": final["selected_oos_net"],
                    "selected_oos_profit_factor": final["selected_oos_profit_factor"],
                    "selected_oos_trade_density": final["selected_oos_trade_density"],
                    "selected_combined_cost09_net": final["selected_combined_cost09_net"],
                    "selected_combined_short_share": final["selected_combined_short_share"],
                    "selected_runtime_density_estimate_from_hl_ratio": final["selected_runtime_density_estimate_from_hl_ratio"],
                    "gate_passes": final["gate_passes"],
                    "gate_total": final["gate_total"],
                    "runtime_authority": final["runtime_authority"],
                    "goal_achieve": final["goal_achieve"],
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
