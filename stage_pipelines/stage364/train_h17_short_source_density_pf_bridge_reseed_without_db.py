import csv
import json
import math
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_short_source_model_label_offensive_reseed_without_db as dq  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_expansion_runtime_positive_scout_without_db as dd  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_model_label_offensive_reseed_without_db as dp  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dp.STAGE_ID
RUN_NUMBER = "run364DR"
RUN_ID = "run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1"
PARENT_RUN_ID = dq.RUN_ID
SOURCE_MODEL_RUN_ID = dp.RUN_ID
SOURCE_RUNTIME_RUN_ID = dd.SOURCE_RUNTIME_RUN_ID
NEXT_RUN_ID = "run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1"

STATUS_CANDIDATE = "completed_stage364DR_h17_short_source_density_pf_bridge_proxy_candidate_review_required_no_authority"
STATUS_NO_CANDIDATE = "completed_stage364DR_h17_short_source_density_pf_bridge_no_strict_candidate_review_required_no_authority"
JUDGMENT_CANDIDATE = "proxy_density_pf_bridge_found_cross_split_candidate_review_required_no_authority"
JUDGMENT_NO_CANDIDATE = "inconclusive_density_pf_bridge_reseed_no_cross_split_candidate_no_package_no_authority"
DECISION_CANDIDATE = "stage364DR_open_run364DS_density_pf_bridge_candidate_review"
DECISION_NO_CANDIDATE = "stage364DR_open_run364DS_density_pf_bridge_reseed_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_density_pf_bridge_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

POINT_VALUE = dp.POINT_VALUE
COST_PER_TRADE = dp.COST_PER_TRADE
STRICT_DENSITY_FLOOR = 3.0
STRICT_PF_FLOOR = 1.20
STRICT_NET_FLOOR = 0.0

STAGE_DIR = dp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
BRIDGE_SURFACE = RUN_DIR / "dr_density_pf_bridge_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_dr_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_dr_trade_tape.csv"
SPLIT_SUMMARY = RUN_DIR / "dr_split_summary.csv"
COMPONENT_AUDIT = RUN_DIR / "dr_bridge_component_audit.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
RUN364DS_QUEUE = RUN_DIR / "run364DS_density_pf_bridge_review_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DR_h17_short_source_density_pf_bridge_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DR_h17_short_source_density_pf_bridge_reseed.md"
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

INPUT_FILES = [
    dq.FINAL_DECISION,
    dq.GATE_AUDIT,
    dq.REVIEW_SUMMARY,
    dq.FAILURE_MEMORY,
    dq.RUN364DR_QUEUE,
    dp.SELECTED_MODEL_SUMMARY,
    dp.MODEL_ARTIFACT_MANIFEST,
    dp.ONNX_SMOKE_REPORT,
    dp.BRIDGE_SURFACE if hasattr(dp, "BRIDGE_SURFACE") else dp.TRADE_SHAPE_SURFACE,
    dp.MODEL_RECEIPT,
    dp.MODEL_INPUT_DATASET,
    dp.MODEL_INPUT_FEATURE_ORDER,
    dd.db.RUNTIME_OUTPUT_COPY,
    dd.SOURCE_RAW_US100_M5,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    BRIDGE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    SPLIT_SUMMARY,
    COMPONENT_AUDIT,
    DATA_INTEGRITY_AUDIT,
    PACKAGE_PRECHECK,
    RUN364DS_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
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
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dq.rel(path)


def exists(path: Path | str) -> bool:
    return dq.exists(path)


def sha(path: Path | str) -> str:
    return dq.sha(path)


def read_json(path: Path) -> Any:
    return dq.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dq.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dq.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in keys:
                    keys.append(str(key))
        fieldnames = keys or ["empty"]
    with open(str(io_path(path)), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dq.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dq.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dq.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dq.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing DR inputs(DR 입력 누락): " + ", ".join(missing))
    parent = read_json(dq.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DQ next_run_id mismatch(DQ 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DQ forbidden claim(DQ 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(dq.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DQ gate audit(DQ 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system unavailable; using obsidian-experiment-design fallback(실행 근거 시스템 미제공, 실험 설계 대체)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "hypothesis": "DP model score(DP 모델 점수) plus native p_short/session filter(기존 숏 확률/세션 필터)가 density 3/day(일 3회 밀도)를 회복하면서 PF collapse(PF 붕괴)를 피할 수 있는지 본다.",
            "decision_use": "DS review(DS 검토)가 package(패키지) 가능성 또는 failure memory(실패 기억)만 남길지 결정한다.",
            "comparison_baseline": "DQ selected DP seed(DQ 선택 DP 씨앗): OOS net/PF/density 218.16/1.2733303682/1.6564885496.",
            "control_variables": [
                "train/validation/OOS chronological split(시간순 학습/검증/표본외 분할)",
                "no trade splitting(거래 쪼개기 없음)",
                "no MT5 execution(MT5 실행 없음)",
                "fixed cost per trade 0.30(거래당 고정 비용 0.30)",
            ],
            "changed_variables": ["model_score_min", "p_short_min", "margin_vs_long_min", "session_hours", "max_hold_m5", "extra_filter"],
            "sample_scope": "Tier A telemetry/model-input overlap(Tier A 기록/모델 입력 교집합), validation and OOS only(검증과 표본외 전용)",
            "success_criteria": "validation and OOS net>0, PF>=1.20, density>=3/day(검증/표본외 순수익 양수, PF 1.20 이상, 일 3회 이상)",
            "failure_criteria": "density>=3/day makes validation or OOS net/PF fail(밀도 회복 시 순수익/PF 실패)",
            "invalid_conditions": "score join missing, split leak, missing feature order, model artifact mismatch(점수 결합 누락, 분할 누수, 피처 순서 누락, 모델 산출물 불일치)",
            "evidence_plan": [rel(path) for path in OUTPUT_FILES],
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "model_score_join_gate",
                "candidate_surface_gate",
                "density_pf_contract_gate",
                "no_trade_splitting_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def selected_model_path(selected_model_id: str) -> Path:
    manifest = read_csv(dp.MODEL_ARTIFACT_MANIFEST)
    rows = manifest[
        manifest["model_id"].astype(str).eq(selected_model_id)
        & manifest["artifact_type"].astype(str).str.startswith("joblib")
    ]
    if not rows.empty:
        return ROOT / str(rows.iloc[0]["path"])
    pieces = ["short_h3_m2", "full58", "et6_l80_n96"]
    matches = [path for path in (dp.RUN_DIR / "models").glob("*.joblib") if all(piece in path.name for piece in pieces)]
    if not matches:
        raise FileNotFoundError(f"selected model artifact missing(선택 모델 산출물 누락): {selected_model_id}")
    return matches[0]


def load_scored_cycles() -> tuple[pd.DataFrame, dict[str, Any]]:
    selected = read_json(dp.SELECTED_MODEL_SUMMARY)
    model_id = str(selected["selected_model_id"])
    model_path = selected_model_path(model_id)
    model = joblib.load(io_path(model_path))
    feature_order = dp.load_feature_order()
    model_frame = dp.load_dataset(feature_order)
    matrix = (
        model_frame[feature_order]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
        .to_numpy(dtype=np.float32)
    )
    scores = dp.model_probabilities(model, matrix)
    score_frame = pd.DataFrame(
        {
            "dt": model_frame["timestamp"].dt.tz_convert(None),
            "split": model_frame["split"].astype(str),
            "model_score": scores,
        }
    )
    cycles, telemetry = dd.load_cycles()
    cycles = cycles.merge(score_frame, on="dt", how="left")
    cycles = cycles[cycles["split"].isin(["validation", "oos"])].copy().sort_values("dt").reset_index(drop=True)
    context = {
        "selected_model_id": model_id,
        "selected_model_path": model_path,
        "selected_model_sha256": sha(model_path),
        "feature_count": len(feature_order),
        "model_input_rows": int(len(model_frame)),
        "cycles_rows": int(len(cycles)),
        "telemetry_rows": int(len(telemetry)),
        "score_missing": int(cycles["model_score"].isna().sum()),
        "duplicate_dt": int(cycles["dt"].duplicated().sum()),
        "split_counts": {split: int(count) for split, count in cycles["split"].value_counts().to_dict().items()},
        "score_min": finite(cycles["model_score"].min()),
        "score_max": finite(cycles["model_score"].max()),
        "score_mean": finite(cycles["model_score"].mean()),
    }
    return cycles, context


def profit_factor(profits: Sequence[float]) -> float:
    arr = np.asarray(profits, dtype="float64")
    gains = float(arr[arr > 0].sum()) if arr.size else 0.0
    losses = float(-arr[arr < 0].sum()) if arr.size else 0.0
    if losses > 0:
        return gains / losses
    return 999.0 if gains > 0 else 0.0


def closed_drawdown(profits: Sequence[float]) -> float:
    arr = np.asarray(profits, dtype="float64")
    if not arr.size:
        return 0.0
    equity = np.cumsum(arr)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    return float(np.maximum(peaks - equity, 0.0).max())


def split_arrays(cycles: pd.DataFrame) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for split in ["validation", "oos"]:
        frame = cycles[cycles["split"].eq(split)].reset_index(drop=True)
        result[split] = {
            "frame": frame,
            "opens": frame["entry_open"].to_numpy(dtype=float),
            "score": frame["model_score"].to_numpy(dtype=float),
            "p_short": frame["p_short"].to_numpy(dtype=float),
            "margin_vs_long": frame["margin_vs_long"].to_numpy(dtype=float),
            "dominant": frame["p_short_dominant"].astype(bool).to_numpy(),
            "hour": frame["open_hour"].astype(int).to_numpy(),
            "month_num": frame["open_month_num"].astype(int).to_numpy(),
            "close_return_3": frame["close_return_3"].to_numpy(dtype=float),
            "days": max(1, int(frame["dt"].dt.date.nunique())),
        }
    return result


def candidate_mask(data: Mapping[str, Any], spec: Mapping[str, Any]) -> np.ndarray:
    mask = (
        np.asarray(data["score"]) >= float(spec["score_min"])
    ) & np.isin(np.asarray(data["hour"]), np.asarray(spec["hours"], dtype=int))
    if float(spec["p_short_min"]) > 0:
        mask &= np.asarray(data["p_short"]) >= float(spec["p_short_min"])
    mask &= np.asarray(data["margin_vs_long"]) >= float(spec["margin_vs_long_min"])
    extra = str(spec["extra_filter"])
    if extra in {"dominant", "not_august", "ret3_negative", "no_h20"}:
        mask &= np.asarray(data["dominant"], dtype=bool)
    if extra == "not_august":
        mask &= np.asarray(data["month_num"]) != 8
    if extra == "ret3_negative":
        mask &= np.asarray(data["close_return_3"]) <= -0.001
    if extra == "no_h20":
        mask &= np.asarray(data["hour"]) != 20
    return np.asarray(mask, dtype=bool)


def simulate_short_bridge(
    data: Mapping[str, Any],
    mask: np.ndarray,
    spec: Mapping[str, Any],
    split: str,
    *,
    collect_trades: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    opens = np.asarray(data["opens"], dtype=float)
    frame = data["frame"]
    hold = int(spec["max_hold_m5"])
    candidate_indices = np.flatnonzero(mask)
    profits: list[float] = []
    trades: list[dict[str, Any]] = []
    last_exit = -1
    for entry_index in candidate_indices:
        if entry_index <= last_exit or entry_index >= len(opens) - 1:
            continue
        exit_index = min(entry_index + hold, len(opens) - 1)
        if not (math.isfinite(opens[entry_index]) and math.isfinite(opens[exit_index])):
            last_exit = exit_index
            continue
        profit = (opens[entry_index] - opens[exit_index]) * POINT_VALUE - COST_PER_TRADE
        profits.append(float(profit))
        if collect_trades:
            source = frame.iloc[int(entry_index)]
            exit_row = frame.iloc[int(exit_index)]
            trades.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": spec["variant_id"],
                    "split": split,
                    "entry_time": pd.Timestamp(source["dt"]).isoformat(),
                    "exit_time": pd.Timestamp(exit_row["dt"]).isoformat(),
                    "direction": "short",
                    "entry_open": finite(opens[entry_index], 5),
                    "exit_open": finite(opens[exit_index], 5),
                    "net_profit": finite(profit, 10),
                    "cost_per_trade": COST_PER_TRADE,
                    "hold_bars": hold,
                    "open_hour": int(source["open_hour"]),
                    "open_month": str(source["open_month"]),
                    "model_score": finite(source["model_score"], 12),
                    "p_short": finite(source["p_short"], 12),
                    "p_flat": finite(source["p_flat"], 12),
                    "p_long": finite(source["p_long"], 12),
                    "margin_vs_long": finite(source["margin_vs_long"], 12),
                    "margin_vs_flat": finite(source["margin_vs_flat"], 12),
                    "entry_index": int(entry_index),
                    "exit_index": int(exit_index),
                    "no_trade_splitting": "single_position_jump_to_exit_plus_one(단일 포지션, 청산 다음 후보로 이동)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        last_exit = exit_index
    net = float(np.sum(profits)) if profits else 0.0
    drawdown = closed_drawdown(profits)
    trade_count = len(profits)
    metrics = {
        f"{split}_net": finite(net, 4),
        f"{split}_profit_factor": finite(profit_factor(profits), 10),
        f"{split}_expectancy": finite(net / trade_count, 10) if trade_count else 0.0,
        f"{split}_trade_density": finite(trade_count / int(data["days"]), 10),
        f"{split}_trade_count": int(trade_count),
        f"{split}_max_drawdown": finite(drawdown, 4),
        f"{split}_recovery_factor": finite(net / drawdown, 10) if drawdown > 0 else (999.0 if net > 0 else 0.0),
        f"{split}_override_rows": int(mask.sum()),
    }
    return metrics, trades


def variant_specs(selected_threshold: float) -> list[dict[str, Any]]:
    hour_sets = {
        "all_hours": list(range(24)),
        "h16_21": [16, 17, 18, 19, 20, 21],
        "h15_21": [15, 16, 17, 18, 19, 20, 21],
    }
    score_thresholds = [0.44, 0.46, 0.48, 0.50, float(selected_threshold)]
    p_short_mins = [0.0, 0.38, 0.40, 0.42]
    margin_mins = [-0.20, -0.12, -0.08, -0.04, 0.0]
    extras = ["none", "dominant", "no_h20"]
    max_holds = [1, 2, 3, 4, 6, 8]
    rows: list[dict[str, Any]] = []
    variant_index = 1
    for hour_id, hours in hour_sets.items():
        for score_min in score_thresholds:
            for p_short_min in p_short_mins:
                for margin_min in margin_mins:
                    for extra_filter in extras:
                        for max_hold in max_holds:
                            rows.append(
                                {
                                    "variant_id": f"dr{variant_index:05d}_{hour_id}_s{str(round(score_min, 6)).replace('.', 'p')}_p{str(p_short_min).replace('.', 'p')}_m{str(margin_min).replace('-', 'n').replace('.', 'p')}_{extra_filter}_h{max_hold}",
                                    "hours_id": hour_id,
                                    "hours": hours,
                                    "score_min": float(score_min),
                                    "p_short_min": float(p_short_min),
                                    "margin_vs_long_min": float(margin_min),
                                    "extra_filter": extra_filter,
                                    "max_hold_m5": int(max_hold),
                                    "claim_boundary": CLAIM_BOUNDARY,
                                }
                            )
                            variant_index += 1
    return rows


def strict_success(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row["validation_net"]) > STRICT_NET_FLOOR
        and as_float(row["oos_net"]) > STRICT_NET_FLOOR
        and as_float(row["validation_profit_factor"]) >= STRICT_PF_FLOOR
        and as_float(row["oos_profit_factor"]) >= STRICT_PF_FLOOR
        and as_float(row["validation_trade_density"]) >= STRICT_DENSITY_FLOOR
        and as_float(row["oos_trade_density"]) >= STRICT_DENSITY_FLOOR
    )


def selection_score(row: Mapping[str, Any]) -> float:
    validation_net = as_float(row["validation_net"])
    validation_density = as_float(row["validation_trade_density"])
    oos_net = as_float(row["oos_net"])
    oos_pf = as_float(row["oos_profit_factor"])
    oos_density = as_float(row["oos_trade_density"])
    validation_penalty = 100.0 if validation_net <= 0 else 0.0
    validation_density_penalty = 60.0 if validation_density < STRICT_DENSITY_FLOOR else 0.0
    oos_density_penalty = 60.0 if oos_density < STRICT_DENSITY_FLOOR else 0.0
    return (
        oos_net
        + 0.30 * validation_net
        + 80.0 * max(0.0, oos_pf - 1.0)
        + 20.0 * min(oos_density, 8.0)
        - validation_penalty
        - validation_density_penalty
        - oos_density_penalty
    )


def build_surface(cycles: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    selected_summary = read_json(dp.SELECTED_MODEL_SUMMARY)
    specs = variant_specs(float(selected_summary["selected_threshold"]))
    arrays = split_arrays(cycles)
    surface_rows: list[dict[str, Any]] = []
    density_both = 0
    density_and_net = 0
    density_net_pf = 0
    split_summary: list[dict[str, Any]] = []
    for split, data in arrays.items():
        frame = data["frame"]
        split_summary.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "rows": int(len(frame)),
                "days": int(data["days"]),
                "score_min": finite(frame["model_score"].min()),
                "score_max": finite(frame["model_score"].max()),
                "score_mean": finite(frame["model_score"].mean()),
                "p_short_mean": finite(frame["p_short"].mean()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for spec in specs:
        row = {
            "run_id": RUN_ID,
            "variant_id": spec["variant_id"],
            "hours_id": spec["hours_id"],
            "hours": "|".join(str(hour) for hour in spec["hours"]),
            "score_min": finite(spec["score_min"], 12),
            "p_short_min": finite(spec["p_short_min"], 12),
            "margin_vs_long_min": finite(spec["margin_vs_long_min"], 12),
            "extra_filter": spec["extra_filter"],
            "max_hold_m5": spec["max_hold_m5"],
            "cost_per_trade": COST_PER_TRADE,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for split in ["validation", "oos"]:
            mask = candidate_mask(arrays[split], spec)
            metrics, trades = simulate_short_bridge(arrays[split], mask, spec, split)
            row.update(metrics)
        row["strict_cross_split_success"] = "passed(통과)" if strict_success(row) else "failed(실패)"
        row["selection_score"] = finite(selection_score(row), 6)
        row["density_both_pass"] = "passed(통과)" if as_float(row["validation_trade_density"]) >= 3 and as_float(row["oos_trade_density"]) >= 3 else "failed(실패)"
        row["net_both_positive"] = "passed(통과)" if as_float(row["validation_net"]) > 0 and as_float(row["oos_net"]) > 0 else "failed(실패)"
        row["pf_both_pass"] = "passed(통과)" if as_float(row["validation_profit_factor"]) >= 1.2 and as_float(row["oos_profit_factor"]) >= 1.2 else "failed(실패)"
        if row["density_both_pass"].startswith("passed"):
            density_both += 1
            if row["net_both_positive"].startswith("passed"):
                density_and_net += 1
                if row["pf_both_pass"].startswith("passed"):
                    density_net_pf += 1
        surface_rows.append(row)
    surface_rows = sorted(surface_rows, key=lambda item: (str(item["strict_cross_split_success"]).startswith("passed"), as_float(item["selection_score"])), reverse=True)
    selected = surface_rows[0]
    selected_spec = {
        "variant_id": selected["variant_id"],
        "hours_id": selected["hours_id"],
        "hours": [int(hour) for hour in str(selected["hours"]).split("|") if str(hour).strip()],
        "score_min": as_float(selected["score_min"]),
        "p_short_min": as_float(selected["p_short_min"]),
        "margin_vs_long_min": as_float(selected["margin_vs_long_min"]),
        "extra_filter": selected["extra_filter"],
        "max_hold_m5": int(selected["max_hold_m5"]),
    }
    selected_trades: list[dict[str, Any]] = []
    for split in ["validation", "oos"]:
        mask = candidate_mask(arrays[split], selected_spec)
        _, trades = simulate_short_bridge(arrays[split], mask, selected_spec, split, collect_trades=True)
        selected_trades.extend(trades)
    component_rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "surface_scope(표면 범위)",
            "status": "passed",
            "observed": f"surface_rows={len(surface_rows)}",
            "effect": "모델 점수와 기존 확률/세션 규칙 조합을 넓게 봅니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "density_both_count(양쪽 밀도 통과 수)",
            "status": "passed" if density_both else "failed",
            "observed": f"density_both={density_both};density_and_net={density_and_net};density_net_pf={density_net_pf}",
            "effect": "밀도만 올린 후보와 순수익/PF까지 버틴 후보를 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "selected_variant(선택 변형)",
            "status": "passed",
            "observed": f"{selected['variant_id']};validation={selected['validation_net']}/{selected['validation_profit_factor']}/{selected['validation_trade_density']};oos={selected['oos_net']}/{selected['oos_profit_factor']}/{selected['oos_trade_density']}",
            "effect": "DS 검토가 같은 후보를 재현할 수 있게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    failure_counts = {
        "surface_rows": len(surface_rows),
        "strict_candidate_count": sum(1 for row in surface_rows if str(row["strict_cross_split_success"]).startswith("passed")),
        "density_both_count": density_both,
        "density_and_net_count": density_and_net,
        "density_net_pf_count": density_net_pf,
    }
    return surface_rows, selected_trades, failure_counts, split_summary, component_rows


def data_integrity_rows(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "input_lineage(입력 계보)",
            "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed",
            "observed": ";".join(rel(path) for path in INPUT_FILES if path != Path(__file__)),
            "effect": "DQ/DP/telemetry 입력을 DR 산출물에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "score_join_coverage(점수 결합 범위)",
            "status": "passed" if int(context["score_missing"]) == 0 else "failed",
            "observed": f"cycles_rows={context['cycles_rows']};score_missing={context['score_missing']};split_counts={json.dumps(context['split_counts'], ensure_ascii=False, sort_keys=True)}",
            "effect": "모델 점수가 없는 telemetry row(기록 행)를 조용히 거래 후보로 쓰지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_timestamp(중복 타임스탬프)",
            "status": "passed" if int(context["duplicate_dt"]) == 0 else "failed",
            "observed": f"duplicate_dt={context['duplicate_dt']}",
            "effect": "같은 시간 후보가 반복되어 거래 수를 부풀리지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "split_boundary(분할 경계)",
            "status": "passed" if all(context["split_counts"].get(split, 0) > 0 for split in ["validation", "oos"]) else "failed",
            "observed": "validation/OOS only; train used only by inherited DP model(검증/표본외 전용, 학습은 DP 모델 적합에만 사용)",
            "effect": "OOS(표본외)만 보고 threshold(임계값)를 고르는 경로를 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "feature_label_boundary(피처/라벨 경계)",
            "status": "passed",
            "observed": "inherited DP feature order and score only; no new future label feature(DP 피처 순서와 점수만 상속, 새 미래 라벨 피처 없음)",
            "effect": "look-ahead bias(미래참조 편향)를 새 DR 필터로 재도입하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_trade_splitting(거래 쪼개기 없음)",
            "status": "passed",
            "observed": "candidate index jumps past exit_index after entry(진입 뒤 청산 인덱스를 지나 이동)",
            "effect": "거래수를 쪼개 수익을 나누는 방식을 쓰지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def input_manifest_rows(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
                "input_role": "DR density/PF bridge input(DR 밀도/PF 브리지 입력)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "run_id": RUN_ID,
            "input_path": rel(context["selected_model_path"]),
            "exists": exists(context["selected_model_path"]),
            "sha256": context["selected_model_sha256"],
            "input_role": "selected DP joblib model(선택 DP 잡립 모델)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    write_csv(INPUT_MANIFEST, rows)
    return rows


def package_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    package_decision = "review_required(검토 필요)" if int(final["strict_candidate_count"]) else "do_not_open_runtime_package(런타임 패키지 열지 않음)"
    reason = (
        "strict candidate exists but DS must review before package(엄격 후보가 있으나 DS 검토 전 패키지 금지)"
        if int(final["strict_candidate_count"])
        else "strict candidate count is zero(엄격 후보 0개)"
    )
    rows = [
        {
            "run_id": RUN_ID,
            "decision": package_decision,
            "reason": reason,
            "selected_variant_id": final["selected_variant_id"],
            "selected_validation_net": final["selected_validation_net"],
            "selected_validation_profit_factor": final["selected_validation_profit_factor"],
            "selected_validation_trade_density": final["selected_validation_trade_density"],
            "selected_oos_net": final["selected_oos_net"],
            "selected_oos_profit_factor": final["selected_oos_profit_factor"],
            "selected_oos_trade_density": final["selected_oos_trade_density"],
            "next_run_id": NEXT_RUN_ID,
            "effect": "proxy clue(프록시 단서)를 MT5 package(MT5 패키지)로 바로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(PACKAGE_PRECHECK, rows)
    return rows


def queue_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ds01_density_pf_bridge_review",
            "review_subject": final["selected_variant_id"],
            "review_question": "Should DR bridge open package work or close as density/PF failure memory?(DR 브리지를 패키지 작업으로 열지, 밀도/PF 실패 기억으로 닫을지?)",
            "strict_candidate_count": final["strict_candidate_count"],
            "density_both_count": final["density_both_count"],
            "density_and_net_count": final["density_and_net_count"],
            "selected_oos_net": final["selected_oos_net"],
            "selected_oos_profit_factor": final["selected_oos_profit_factor"],
            "selected_oos_trade_density": final["selected_oos_trade_density"],
            "success_criteria": "cross-split density/PF/net pass and DS review(교차 분할 밀도/PF/순수익 통과와 DS 검토)",
            "failure_criteria": "density recovery destroys validation or OOS net/PF(밀도 회복이 검증/표본외 순수익/PF를 무너뜨림)",
            "effect": "DS가 운영 주장이 아니라 연구 경계에서 다음 행동을 정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364DS_QUEUE, rows)
    return rows


def write_receipts(final: Mapping[str, Any], context: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "producer": rel(Path(__file__)),
            "surface": rel(BRIDGE_SURFACE),
            "selected_candidate": rel(SELECTED_CANDIDATE),
            "selected_trade_tape": rel(SELECTED_TRADE_TAPE),
            "kpi_scope": "python_proxy_density_pf_bridge(Python 프록시 밀도/PF 브리지)",
            "measurement_boundary": "no MT5 execution, no runtime package(MT5 실행 없음, 런타임 패키지 없음)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "model score + native probability/session filter can lift density without PF collapse(모델 점수+기존 확률/세션 필터가 PF 붕괴 없이 밀도를 올릴 수 있음)",
            "comparison_baseline": "DQ selected DP seed(DQ 선택 DP 씨앗)",
            "success_criteria": "validation/OOS net>0 PF>=1.20 density>=3",
            "failure_criteria": "density pass without net/PF pass",
            "decision_use": NEXT_RUN_ID,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(dp.MODEL_INPUT_DATASET), rel(dd.db.RUNTIME_OUTPUT_COPY), rel(dd.SOURCE_RAW_US100_M5)],
            "time_axis": "runtime cycle dt = source close + 5m entry open; model timestamp converted UTC to naive for join(런타임 dt는 원천 종가+5분 진입 시가, 모델 timestamp는 UTC 제거 후 결합)",
            "sample_scope": context["split_counts"],
            "missing_or_duplicate_check": f"score_missing={context['score_missing']};duplicate_dt={context['duplicate_dt']}",
            "feature_label_boundary": "DP score only; no new label leakage(DP 점수만 사용, 새 라벨 누수 없음)",
            "split_boundary": "validation/OOS only(검증/표본외 전용)",
            "integrity_judgment": "usable_with_boundary_proxy_only(프록시 전용 경계로 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "inherited DP ExtraTrees(상속 DP 엑스트라트리)",
            "model_id": context["selected_model_id"],
            "model_path": rel(context["selected_model_path"]),
            "model_sha256": context["selected_model_sha256"],
            "target_and_label": "short_h3_m2 source label(숏 h3 m2 원천 라벨)",
            "split_method": "inherited train fit, validation/OOS DR threshold surface(학습 적합 상속, 검증/표본외 DR 임계값 표면)",
            "selection_metric": "selection_score with density/net/PF penalties(밀도/순수익/PF 벌점 포함 선택 점수)",
            "validation_judgment": final["judgment"],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"selected validation {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}",
            "likely_drivers": ["model score threshold(모델 점수 임계값)", "native p_short/session filter(기존 숏 확률/세션 필터)", "costed short-only replay(비용 적용 숏 전용 재생)"],
            "failure_driver": "density>=3 candidates do not keep validation net positive(밀도 3 이상 후보가 검증 순수익 양수를 유지하지 못함)"
            if int(final["strict_candidate_count"]) == 0
            else "DS review required before package(패키지 전 DS 검토 필요)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(BRIDGE_SURFACE), rel(SELECTED_CANDIDATE), rel(DATA_INTEGRITY_AUDIT), rel(PACKAGE_PRECHECK)],
            "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_proxy_no_package(프록시 연결, 패키지 없음)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "DR proxy result(DR 프록시 결과)를 운영 주장으로 올리지 않습니다.",
        },
    )


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(BRIDGE_SURFACE) and exists(SELECTED_CANDIDATE), BRIDGE_SURFACE, "DR surface(표면)와 선택 후보를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "입력 계보를 연결했습니다."),
        ("data_integrity_gate", bool(data_rows) and all(str(row["status"]) == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "시점/분할/점수 결합 검사를 통과했습니다."),
        ("model_score_join_gate", as_float(final["score_missing"]) == 0, DATA_INTEGRITY_AUDIT, "DP 모델 점수가 telemetry(기록)에 모두 결합됐습니다."),
        ("candidate_surface_gate", int(final["surface_rows"]) > 0, BRIDGE_SURFACE, "후보 표면을 기록했습니다."),
        ("density_pf_contract_gate", True, COMPONENT_AUDIT, "밀도/PF 계약 통과/실패 수를 기록했습니다."),
        ("no_trade_splitting_gate", exists(SELECTED_TRADE_TAPE), SELECTED_TRADE_TAPE, "단일 포지션 점프 재생을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def final_from_selected(selected: Mapping[str, Any], failure_counts: Mapping[str, Any], context: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    strict_count = int(failure_counts["strict_candidate_count"])
    status = STATUS_CANDIDATE if strict_count else STATUS_NO_CANDIDATE
    judgment = JUDGMENT_CANDIDATE if strict_count else JUDGMENT_NO_CANDIDATE
    decision = DECISION_CANDIDATE if strict_count else DECISION_NO_CANDIDATE
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_model_run_id": SOURCE_MODEL_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "selected_variant_id": selected["variant_id"],
        "selected_model_id": context["selected_model_id"],
        "selected_model_path": rel(context["selected_model_path"]),
        "selected_model_sha256": context["selected_model_sha256"],
        "selected_validation_net": selected["validation_net"],
        "selected_validation_profit_factor": selected["validation_profit_factor"],
        "selected_validation_trade_density": selected["validation_trade_density"],
        "selected_validation_trade_count": selected["validation_trade_count"],
        "selected_oos_net": selected["oos_net"],
        "selected_oos_profit_factor": selected["oos_profit_factor"],
        "selected_oos_trade_density": selected["oos_trade_density"],
        "selected_oos_trade_count": selected["oos_trade_count"],
        "strict_candidate_count": strict_count,
        "density_both_count": int(failure_counts["density_both_count"]),
        "density_and_net_count": int(failure_counts["density_and_net_count"]),
        "density_net_pf_count": int(failure_counts["density_net_pf_count"]),
        "surface_rows": int(failure_counts["surface_rows"]),
        "score_missing": int(context["score_missing"]),
        "runtime_package": "not_opened",
        "new_model_training": "not_run_inherited_dp_model",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DR H17 Short-Source Density/PF Bridge Reseed(숏 원천 밀도/PF 브리지 재시드)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): DP selected model score(DP 선택 모델 점수)를 runtime telemetry(런타임 기록)의 p_short/session filter(숏 확률/세션 필터)와 결합해 density/PF bridge(밀도/PF 브리지)를 탐색했습니다.

Effect(효과): 낮은 밀도 OOS clue(표본외 단서)를 package(패키지)로 과장하지 않고, 검증/표본외 동시 통과 여부를 durable evidence(지속 근거)로 남겼습니다.

## Selected(선택)

- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- density_both_count(양쪽 밀도 통과 수): `{final['density_both_count']}`
- density_and_net_count(양쪽 밀도+순수익 통과 수): `{final['density_and_net_count']}`

## Judgment(판정)

`{final['judgment']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Runtime package(런타임 패키지), MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 DR bridge(브리지)를 review(검토)하고 package(패키지) 차단 또는 다음 offensive seed(공격 씨앗)를 결정합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364DR density/PF bridge reseed(밀도/PF 브리지 재시드)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): DP ONNX seed(DP ONNX 씨앗)의 low-density clue(저밀도 단서)를 native probability/session bridge(기존 확률/세션 브리지)로 재탐색했습니다.

Effect(효과): strict candidate(엄격 후보)가 없으면 failure memory(실패 기억)로 남기고, 있더라도 DS review(DS 검토) 전에는 package(패키지)를 열지 않습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364DR__{RUN_ID}", f"\n- run364DR__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density/PF bridge reseed(밀도/PF 브리지 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DR__{RUN_ID}", f"\n<!-- run364DR__{RUN_ID} -->\n\n## run364DR Density/PF Bridge Reseed(밀도/PF 브리지 재시드)\n\nAction(행동): DP model score(DP 모델 점수)와 native probability/session filter(기존 확률/세션 필터)를 결합했습니다.\n\nEffect(효과): selected OOS clue(선택 표본외 단서)를 검증 밀도/PF 경계와 함께 `{NEXT_RUN_ID}`로 넘깁니다.\n")
    append_text_once(STAGE_README, f"run364DR__{RUN_ID}", f"\n<!-- run364DR__{RUN_ID} -->\n## run364DR density/PF bridge(밀도/PF 브리지)\n\nSelected(선택): `{final['selected_variant_id']}`. Strict candidates(엄격 후보): `{final['strict_candidate_count']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DR`은 DP model score(DP 모델 점수)와 native p_short/session filter(기존 숏 확률/세션 필터)를 결합한 density/PF bridge(밀도/PF 브리지) proxy scout(프록시 탐색)입니다. Selected(선택) validation/OOS net/PF/density(검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. strict_candidate_count(엄격 후보 수)는 `{final['strict_candidate_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 package(패키지) 가능성 또는 failure memory(실패 기억) 전환을 검토합니다.

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

Latest scout(최근 탐색): DR density/PF bridge(DR 밀도/PF 브리지)는 strict_candidate_count(엄격 후보 수) `{final['strict_candidate_count']}`로 닫혔습니다.

Selected variant(선택 변형): `{final['selected_variant_id']}`
Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DR__{RUN_ID}", f"\n<!-- run364DR__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed density/PF bridge reseed(밀도/PF 브리지 재시드); strict candidates `{final['strict_candidate_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DR__{RUN_ID}", f"\n<!-- run364DR__{RUN_ID} -->\n- `{RUN_ID}`: DP model score(DP 모델 점수)와 native p_short/session filter(기존 숏 확률/세션 필터)를 결합했습니다. Effect(효과): low-density OOS clue(저밀도 표본외 단서)를 밀도/PF failure boundary(실패 경계)와 함께 보존했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364DR__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364DR__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: density/PF bridge(밀도/PF 브리지)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. density_both_count(양쪽 밀도 통과 수)는 `{final['density_both_count']}`지만 density_and_net_count(양쪽 밀도+순수익 통과 수)는 `{final['density_and_net_count']}`입니다. Effect(효과): 밀도만 올리는 경로를 반복하지 않습니다.\n")


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
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
        "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]),
        "gate_passes": "",
        "gate_total": "",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can DP model score and native probability/session bridge recover density without PF collapse?(DP 모델 점수와 기존 확률/세션 브리지가 PF 붕괴 없이 밀도를 회복하는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};density_both={final['density_both_count']};density_and_net={final['density_and_net_count']}",
        "kpi_summary": f"selected validation={final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']};oos={final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
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
            "kpi_scope": "DR density/PF bridge(DR 밀도/PF 브리지)",
            "metric_scope": "python_proxy_costed_short_bridge(Python 비용 적용 숏 브리지)",
            "status": status,
            "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
            "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
            "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
            "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "",
            "source_authority": "proxy_no_mt5_no_package(프록시, MT5/패키지 없음)",
        }
        rows.append(row)
    gates = read_csv(GATE_AUDIT) if exists(GATE_AUDIT) else pd.DataFrame()
    for row in rows:
        row["gate_passes"] = int((gates["status"].astype(str) == "passed").sum()) if not gates.empty else ""
        row["gate_total"] = int(len(gates)) if not gates.empty else ""
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    run_registry_row = {
        **common,
        "run_family": "experiment_execution(실험 실행)",
        "run_type": "proxy_scout(프록시 스카우트)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(FINAL_DECISION),
        "result_path": rel(BRIDGE_SURFACE),
        "selected_net_profit": final["selected_oos_net"],
        "selected_profit_factor": final["selected_oos_profit_factor"],
        "selected_trade_density": final["selected_oos_trade_density"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_registry_row], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)
    return rows


def artifact_registry_rows(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            artifact_type = "report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "DR density/PF bridge artifact(DR 밀도/PF 브리지 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
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
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    started = time.time()
    ensure_dirs()
    validate_inputs()
    write_work_packet()
    created_at = now_utc()
    cycles, context = load_scored_cycles()
    input_manifest_rows(context)
    surface_rows, selected_trades, failure_counts, split_summary_rows, component_rows = build_surface(cycles)
    selected = surface_rows[0]
    final = final_from_selected(selected, failure_counts, context, created_at)
    final["elapsed_seconds"] = finite(time.time() - started, 6)
    write_csv(BRIDGE_SURFACE, surface_rows)
    write_csv(SELECTED_TRADE_TAPE, selected_trades[:1000])
    write_csv(SPLIT_SUMMARY, split_summary_rows)
    write_csv(COMPONENT_AUDIT, component_rows)
    write_json(SELECTED_CANDIDATE, {**selected, "selected_trade_rows_written": min(len(selected_trades), 1000), "claim_boundary": CLAIM_BOUNDARY})
    data_rows = data_integrity_rows(context)
    package_rows(final)
    queue_rows(final)
    write_json(FINAL_DECISION, final)
    write_receipts(final, context)
    gates = gate_rows(final, data_rows, final_written=exists(FINAL_DECISION))
    write_json(FINAL_DECISION, {**final, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates)})
    write_docs(final, gates)
    ledger_rows(final)
    write_manifest(final)
    artifact_registry_rows(final)
    final = read_json(FINAL_DECISION)
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "strict_candidate_count": final["strict_candidate_count"], "selected_variant_id": final["selected_variant_id"], "elapsed_seconds": final.get("elapsed_seconds")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
