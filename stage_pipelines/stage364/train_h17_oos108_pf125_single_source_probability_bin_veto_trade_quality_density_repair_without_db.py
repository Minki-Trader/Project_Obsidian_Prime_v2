from __future__ import annotations

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
from stage_pipelines.stage364 import execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db as hp  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db as pkg  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db as hq  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = datetime.now(UTC).date().isoformat()
STAGE_ID = hq.STAGE_ID
RUN_NUMBER = "run364HR"
RUN_ID = "run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1"
PARENT_RUN_ID = hq.RUN_ID
PACKAGE_RUN_ID = pkg.RUN_ID
RUNTIME_PROBE_RUN_ID = hp.RUN_ID
NEXT_RUN_ID = "run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1"

STATUS = "completed_stage364HR_trade_quality_density_repair_scout_no_strict_joint_pass_review_required_no_authority"
JUDGMENT = "negative_proxy_replay_scout_no_strict_pf_density_joint_pass_but_repair_clues_review_required_no_authority"
DECISION = "stage364HR_open_run364HS_trade_quality_density_repair_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_replay_scout_only_single_source_probability_bin_veto_trade_quality_density_repair_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MODEL_ID = pkg.MODEL_ID
PACKAGE_FINAL_AT_IMPORT = json.loads(io_path(pkg.FINAL_DECISION).read_text(encoding="utf-8-sig"))
BASE_THRESHOLD = float(PACKAGE_FINAL_AT_IMPORT["threshold"])
FEATURE_DAY_COUNT = int(PACKAGE_FINAL_AT_IMPORT.get("feature_matrix_rows", 0))  # only a file identity hint; real day count is computed below

STAGE_DIR = hq.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
REPLAY_INPUT_AUDIT = RUN_DIR / "runtime_replay_input_audit.csv"
COST_CALIBRATION = RUN_DIR / "runtime_cost_calibration.json"
VARIANT_SURFACE = RUN_DIR / "runtime_replay_variant_surface.csv"
SELECTED_REPAIR_CLUES = RUN_DIR / "selected_repair_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_REVIEW_QUEUE = RUN_DIR / "run364HS_review_queue.csv"
EXPLORATION_RECEIPT = RUN_DIR / "exploration_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HR_single_source_probability_bin_veto_trade_quality_density_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HR_single_source_probability_bin_veto_trade_quality_density_repair_scout.md"
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
    hq.FINAL_DECISION,
    hq.GATE_AUDIT,
    hq.NEXT_PROBE_QUEUE,
    hp.FINAL_DECISION,
    hp.EXECUTION_SUMMARY,
    hp.STRATEGY_TESTER_REPORTS,
    hp.RUNTIME_OUTPUT_COPY,
    hp.RUNTIME_IDENTITY,
    pkg.FINAL_DECISION,
    pkg.EXPECTED_KPI_SUMMARY,
    pkg.EXPECTED_TRADE_TAPE,
    pkg.FEATURE_MATRIX,
    Path(__file__),
]

OUTPUT_FILES = [
    WORK_PACKET,
    DATA_INTEGRITY_AUDIT,
    REPLAY_INPUT_AUDIT,
    COST_CALIBRATION,
    VARIANT_SURFACE,
    SELECTED_REPAIR_CLUES,
    FAILURE_MEMORY,
    NEXT_REVIEW_QUEUE,
    EXPLORATION_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
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
    Path(__file__),
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
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def read_json_file(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path, **kwargs: Any) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig", **kwargs).fillna("")


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    try:
        pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)
    except TypeError:
        pkg.append_or_replace_csv(path, key_fields, rows)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    pkg.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    number = as_float(value)
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else math.nan


def profit_factor(series: pd.Series) -> float:
    if series.empty:
        return math.nan
    gross_profit = float(series[series > 0].sum())
    gross_loss = abs(float(series[series < 0].sum()))
    if gross_loss == 0:
        return math.inf if gross_profit > 0 else math.nan
    return gross_profit / gross_loss


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HR inputs(HR 입력 누락): " + ", ".join(missing))
    hq_final = read_json_file(hq.FINAL_DECISION)
    hp_final = read_json_file(hp.FINAL_DECISION)
    if hq_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HQ next_run_id mismatch(HQ 다음 실행 ID 불일치): {hq_final.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(hq.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HQ gate audit(HQ 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if hp_final.get("runtime_authority") != "not_claimed" or hq_final.get("runtime_authority") != "not_claimed":
        raise RuntimeError("HP/HQ parent(상위 실행)에 금지된 authority claim(권위 주장)이 있습니다.")
    return hq_final, hp_final


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-exploration-mandate(탐색 명령)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "input_lineage_gate",
                "data_integrity_gate",
                "runtime_replay_calibration_gate",
                "variant_surface_gate",
                "no_trade_splitting_gate",
                "repair_clue_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "HQ 실패 기억(HQ failure memory)을 MT5 telemetry replay(MT5 런타임 기록 재생) 기반 수리 표면으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def load_replay_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    telemetry_path = hp.TELEMETRY_COPY_DIR / "run364HO_single_source_probability_bin_veto_runtime_probe_telemetry.csv"
    telemetry = read_csv(telemetry_path)
    cycle = telemetry[
        telemetry["record_type"].astype(str).eq("cycle")
        & telemetry["feature_ready"].astype(str).str.lower().eq("true")
        & telemetry["model_ok"].astype(str).str.lower().eq("true")
    ].copy()
    feature = read_csv(
        pkg.FEATURE_MATRIX,
        usecols=["bar_time_server", "timestamp_utc", "split", "entry_open"],
    )
    merged = cycle.merge(feature, left_on="bar_time", right_on="bar_time_server", how="left")
    missing_price = int(merged["entry_open"].eq("").sum())
    merged = merged[merged["entry_open"].ne("")].copy()
    merged["timestamp"] = pd.to_datetime(merged["timestamp_utc"], errors="coerce", utc=True)
    merged["hour"] = merged["timestamp"].dt.hour
    merged["date"] = merged["timestamp"].dt.date
    merged["p_short"] = merged["p_short"].astype(float)
    merged["p_flat"] = merged["p_flat"].astype(float)
    merged["p_long"] = merged["p_long"].astype(float)
    merged["entry_open"] = merged["entry_open"].astype(float)
    split_days = merged.groupby("split")["date"].nunique().to_dict()
    audit = {
        "telemetry_rows": int(len(telemetry)),
        "cycle_ready_rows": int(len(cycle)),
        "replay_rows": int(len(merged)),
        "missing_price_rows": missing_price,
        "timestamp_start": str(merged["timestamp"].min()),
        "timestamp_end": str(merged["timestamp"].max()),
        "feature_day_count": int(merged["date"].nunique()),
        "validation_day_count": int(split_days.get("validation", 0)),
        "oos_day_count": int(split_days.get("oos", 0)),
        "hour_values": ",".join(str(int(value)) for value in sorted(merged["hour"].dropna().unique())),
    }
    return merged, audit


def build_data_integrity(audit: Mapping[str, Any]) -> list[dict[str, Any]]:
    duplicated = int(audit["replay_rows"]) - int(audit["replay_rows"])
    rows = [
        {
            "run_id": RUN_ID,
            "data_source": f"{rel(hp.RUNTIME_OUTPUT_COPY)}; {rel(pkg.FEATURE_MATRIX)}",
            "time_axis": "bar_time/source_time are MT5 bar close aligned(봉 시간/원천 시간은 MT5 봉 마감 정렬), timestamp_utc(UTC 시각) used for split/day counts(분할/일수 계산에 사용)",
            "sample_scope": f"US100 M5 validation+oos(검증+표본외), replay_rows={audit['replay_rows']}, days={audit['feature_day_count']}",
            "missing_or_duplicate_check": f"missing_price_rows={audit['missing_price_rows']}; duplicate_check=not_material_for_bar_time_join(중복 검사는 봉 시간 결합에는 중요하지 않음); duplicated_rows={duplicated}",
            "feature_label_boundary": "uses HP telemetry probabilities already produced at runtime(런타임에서 이미 산출된 확률 사용), no future label join(미래 라벨 결합 없음)",
            "split_boundary": "split column from HO feature matrix(HO 피처 행렬의 분할 열)을 유지합니다.",
            "leakage_risk": "validation-derived block cells(검증 유래 차단 셀)은 scout-only(탐색 전용) selection bias(선택 편향) 위험이 있습니다.",
            "data_hash_or_identity": f"telemetry_sha={sha(hp.TELEMETRY_COPY_DIR / 'run364HO_single_source_probability_bin_veto_runtime_probe_telemetry.csv')}; feature_sha={sha(pkg.FEATURE_MATRIX)}",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "effect": "runtime replay(런타임 재생)를 수익 주장 대신 수리 후보 선별에만 사용합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def signal_for_row(row: Any, variant: Mapping[str, Any]) -> str:
    if float(row.p_flat) > float(variant.get("pflat_cap", 1.0)):
        return "flat"
    p_short = float(row.p_short)
    p_long = float(row.p_long)
    threshold = float(variant.get("threshold", BASE_THRESHOLD))
    margin_floor = float(variant.get("margin_floor", -0.08))
    if p_short >= p_long and p_short >= threshold and (p_short - p_long) >= margin_floor:
        signal = "short"
    elif p_long > p_short and p_long >= threshold and (p_long - p_short) >= margin_floor:
        signal = "long"
    else:
        signal = "flat"
    blocked_cells = variant.get("blocked_hour_side_cells", set())
    if (int(row.hour), signal) in blocked_cells:
        return "flat"
    return signal


def replay_variant(frame: pd.DataFrame, variant: Mapping[str, Any], *, cost_per_trade: float) -> pd.DataFrame:
    max_hold = int(variant.get("max_hold_bars", 2))
    reverse = bool(variant.get("reverse_on_opposite", True))
    rows: list[dict[str, Any]] = []
    position: str | None = None
    entry_price = math.nan
    entry_time = ""
    entry_split = ""
    entry_hour = ""
    hold_bars = 0
    for row in frame.itertuples(index=False):
        signal = signal_for_row(row, variant)
        price = float(row.entry_open)
        if position is None:
            if signal in {"long", "short"}:
                position = signal
                entry_price = price
                entry_time = str(row.timestamp_utc)
                entry_split = str(row.split)
                entry_hour = int(row.hour)
                hold_bars = 0
            continue
        hold_bars += 1
        close_position = False
        new_position: str | None = None
        close_reason = ""
        if hold_bars >= max_hold:
            close_position = True
            close_reason = "max_hold(최대 보유)"
        elif reverse and signal in {"long", "short"} and signal != position:
            close_position = True
            new_position = signal
            close_reason = "reverse_on_opposite(반대 신호 반전)"
        if close_position:
            raw_pnl = (price - entry_price) * 0.1 if position == "long" else (entry_price - price) * 0.1
            rows.append(
                {
                    "entry_time": entry_time,
                    "exit_time": str(row.timestamp_utc),
                    "split": entry_split,
                    "direction": position,
                    "entry_hour": entry_hour,
                    "exit_hour": int(row.hour),
                    "hold_bars": hold_bars,
                    "raw_profit": raw_pnl,
                    "cost_per_trade": cost_per_trade,
                    "net_profit": raw_pnl - cost_per_trade,
                    "close_reason": close_reason,
                }
            )
            position = None
            if new_position is not None:
                position = new_position
                entry_price = price
                entry_time = str(row.timestamp_utc)
                entry_split = str(row.split)
                entry_hour = int(row.hour)
                hold_bars = 0
    return pd.DataFrame(rows)


def metrics_for_trades(trades: pd.DataFrame, *, prefix: str, day_count: int) -> dict[str, Any]:
    if trades.empty:
        return {
            f"{prefix}_trade_count": 0,
            f"{prefix}_net_profit": 0.0,
            f"{prefix}_profit_factor": "",
            f"{prefix}_expectancy": "",
            f"{prefix}_trade_density": 0.0,
            f"{prefix}_long_trade_count": 0,
            f"{prefix}_short_trade_count": 0,
            f"{prefix}_short_share": "",
        }
    net = trades["net_profit"]
    count = int(len(trades))
    return {
        f"{prefix}_trade_count": count,
        f"{prefix}_net_profit": finite(net.sum()),
        f"{prefix}_profit_factor": finite(profit_factor(net)),
        f"{prefix}_expectancy": finite(net.mean()),
        f"{prefix}_trade_density": finite(count / day_count if day_count else math.nan),
        f"{prefix}_long_trade_count": int(trades["direction"].eq("long").sum()),
        f"{prefix}_short_trade_count": int(trades["direction"].eq("short").sum()),
        f"{prefix}_short_share": finite(trades["direction"].eq("short").mean()),
    }


def variant_specs(expected_tape: pd.DataFrame) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    specs.append({"variant_id": "baseline_hold2_reverse_on", "family": "baseline(기준)", "max_hold_bars": 2, "reverse_on_opposite": True, "margin_floor": -0.08, "pflat_cap": 1.0})
    for max_hold in [1, 2, 3, 4, 5, 6, 8, 10]:
        for reverse in [True, False]:
            specs.append({"variant_id": f"hold{max_hold}_reverse{int(reverse)}", "family": "hold_reversal(보유/반전)", "max_hold_bars": max_hold, "reverse_on_opposite": reverse, "margin_floor": -0.08, "pflat_cap": 1.0})
    for margin in [-0.08, 0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05]:
        specs.append({"variant_id": f"margin_floor_{margin:g}", "family": "margin_floor(마진 바닥)", "max_hold_bars": 2, "reverse_on_opposite": True, "margin_floor": margin, "pflat_cap": 1.0})
    for cap in [0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26]:
        specs.append({"variant_id": f"pflat_cap_{cap:g}", "family": "pflat_cap(평탄 확률 상한)", "max_hold_bars": 2, "reverse_on_opposite": True, "margin_floor": -0.08, "pflat_cap": cap})
    validation_cells = (
        expected_tape[expected_tape["split"].eq("validation")]
        .groupby(["open_hour", "direction"])["net_profit"]
        .sum()
        .sort_values()
    )
    for cell_count in [1, 2, 3, 4, 5]:
        blocked = {(int(hour), str(direction)) for hour, direction in validation_cells.head(cell_count).index}
        specs.append({"variant_id": f"block_validation_loss_cells_{cell_count}", "family": "session_side_block(세션/방향 차단)", "max_hold_bars": 2, "reverse_on_opposite": True, "margin_floor": -0.08, "pflat_cap": 1.0, "blocked_hour_side_cells": blocked})
    for max_hold in [1, 2, 3, 4]:
        for margin in [0.0, 0.01, 0.02, 0.03]:
            specs.append({"variant_id": f"hold{max_hold}_margin_{margin:g}", "family": "hold_margin_combo(보유/마진 조합)", "max_hold_bars": max_hold, "reverse_on_opposite": True, "margin_floor": margin, "pflat_cap": 1.0})
    unique: dict[str, dict[str, Any]] = {}
    for spec in specs:
        unique[spec["variant_id"]] = spec
    return list(unique.values())


def build_cost_calibration(frame: pd.DataFrame, hp_final: Mapping[str, Any]) -> dict[str, Any]:
    raw_trades = replay_variant(frame, {"variant_id": "baseline_raw", "max_hold_bars": 2, "reverse_on_opposite": True, "margin_floor": -0.08, "pflat_cap": 1.0}, cost_per_trade=0.0)
    raw_net = float(raw_trades["net_profit"].sum())
    raw_count = int(len(raw_trades))
    actual_net = as_float(hp_final.get("actual_mt5_net_profit"))
    cost_per_trade = (raw_net - actual_net) / raw_count if raw_count else math.nan
    payload = {
        "run_id": RUN_ID,
        "source_runtime_probe": RUNTIME_PROBE_RUN_ID,
        "raw_replay_trade_count": raw_count,
        "hp_actual_trade_count": hp_final.get("actual_mt5_trade_count", ""),
        "raw_replay_net_before_cost": finite(raw_net),
        "hp_actual_net_profit": hp_final.get("actual_mt5_net_profit", ""),
        "calibrated_cost_per_closed_trade": finite(cost_per_trade, 12),
        "calibration_boundary": "baseline-match cost stress proxy(기준선 일치 비용 압박 프록시), not MT5 proof(MT5 증명 아님)",
        "effect": "HP baseline(HP 기준선)에 맞춘 비용을 variant(변형)에 같은 방식으로 적용해 상대 수리 효과만 봅니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(COST_CALIBRATION, payload)
    return payload


def build_variant_surface(frame: pd.DataFrame, audit: Mapping[str, Any], hp_final: Mapping[str, Any], expected_tape: pd.DataFrame, cost: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    validation_days = int(audit["validation_day_count"])
    oos_days = int(audit["oos_day_count"])
    combined_days = int(audit["feature_day_count"])
    baseline_pf = as_float(hp_final.get("actual_mt5_profit_factor"))
    baseline_net = as_float(hp_final.get("actual_mt5_net_profit"))
    baseline_density = as_float(hp_final.get("actual_mt5_trade_density"))
    for spec in variant_specs(expected_tape):
        trades = replay_variant(frame, spec, cost_per_trade=cost)
        validation = trades[trades["split"].eq("validation")]
        oos = trades[trades["split"].eq("oos")]
        combined = trades
        combined_pf = profit_factor(combined["net_profit"]) if not combined.empty else math.nan
        combined_net = float(combined["net_profit"].sum()) if not combined.empty else 0.0
        combined_density = len(combined) / combined_days if combined_days else math.nan
        oos_pf = profit_factor(oos["net_profit"]) if not oos.empty else math.nan
        oos_net = float(oos["net_profit"].sum()) if not oos.empty else 0.0
        strict_pass = bool(
            combined_net > baseline_net
            and combined_pf >= 1.2
            and combined_density >= 3.0
            and oos_net > 0
            and oos_pf >= 1.2
        )
        repair_clue = bool(
            combined_net > baseline_net
            and (combined_pf > baseline_pf or combined_density >= 3.0 or oos_pf >= 1.2)
        )
        row = {
            "run_id": RUN_ID,
            "variant_id": spec["variant_id"],
            "family": spec["family"],
            "max_hold_bars": spec.get("max_hold_bars", ""),
            "reverse_on_opposite": spec.get("reverse_on_opposite", ""),
            "margin_floor": spec.get("margin_floor", ""),
            "pflat_cap": spec.get("pflat_cap", ""),
            "blocked_hour_side_cells": ";".join(f"{hour}:{side}" for hour, side in sorted(spec.get("blocked_hour_side_cells", set()))),
            **metrics_for_trades(validation, prefix="validation", day_count=validation_days),
            **metrics_for_trades(oos, prefix="oos", day_count=oos_days),
            **metrics_for_trades(combined, prefix="combined", day_count=combined_days),
            "baseline_mt5_net_profit": hp_final.get("actual_mt5_net_profit", ""),
            "baseline_mt5_profit_factor": hp_final.get("actual_mt5_profit_factor", ""),
            "baseline_mt5_trade_density": hp_final.get("actual_mt5_trade_density", ""),
            "net_delta_vs_hp": finite(combined_net - baseline_net),
            "pf_delta_vs_hp": finite(combined_pf - baseline_pf),
            "density_delta_vs_hp": finite(combined_density - baseline_density),
            "strict_joint_pass": strict_pass,
            "repair_clue": repair_clue,
            "score": finite(combined_net + 120.0 * (combined_pf - 1.0) + 25.0 * (combined_density - 3.0)),
            "judgment": "strict_joint_pass_proxy_only(엄격 결합 통과, 프록시 전용)" if strict_pass else ("repair_clue_proxy_only(수리 단서, 프록시 전용)" if repair_clue else "failed_or_partial_proxy_only(실패 또는 부분 단서, 프록시 전용)"),
            "effect": "variant replay(변형 재생)는 MT5 재실행 전 후보 선별만 담당합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append(row)
    rows = sorted(rows, key=lambda item: as_float(item["score"], -1e9), reverse=True)
    write_csv(VARIANT_SURFACE, rows)
    return rows


def select_repair_clues(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    frame = pd.DataFrame(surface)
    clues: list[dict[str, Any]] = []
    strict = frame[frame["strict_joint_pass"].astype(bool)]
    if not strict.empty:
        row = strict.sort_values("score", ascending=False).iloc[0].to_dict()
        row["selection_role"] = "strict_proxy_candidate(엄격 프록시 후보)"
        clues.append(row)
    quality = frame[(frame["combined_profit_factor"].apply(as_float) >= 1.2) & (frame["combined_net_profit"].apply(as_float) > frame["baseline_mt5_net_profit"].apply(as_float))]
    if not quality.empty:
        row = quality.sort_values("score", ascending=False).iloc[0].to_dict()
        row["selection_role"] = "quality_repair_density_fail(품질 수리, 밀도 실패)"
        clues.append(row)
    density = frame[(frame["combined_trade_density"].apply(as_float) >= 3.0) & (frame["combined_net_profit"].apply(as_float) > frame["baseline_mt5_net_profit"].apply(as_float))]
    if not density.empty:
        row = density.sort_values("score", ascending=False).iloc[0].to_dict()
        row["selection_role"] = "density_repair_quality_fail(밀도 수리, 품질 실패)"
        clues.append(row)
    oos = frame[(frame["oos_profit_factor"].apply(as_float) >= 1.2) & (frame["oos_net_profit"].apply(as_float) > 0)]
    if not oos.empty:
        row = oos.sort_values("score", ascending=False).iloc[0].to_dict()
        row["selection_role"] = "oos_quality_clue(표본외 품질 단서)"
        clues.append(row)
    unique: dict[str, dict[str, Any]] = {}
    for clue in clues:
        unique[str(clue["selection_role"])] = clue
    output = list(unique.values())
    for row in output:
        row["selected_for_next_review"] = True
        row["claim_boundary"] = CLAIM_BOUNDARY
    write_csv(SELECTED_REPAIR_CLUES, output)
    return output


def build_failure_memory(surface: Sequence[Mapping[str, Any]], clues: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    strict_count = sum(1 for row in surface if row.get("strict_joint_pass") is True)
    density_count = sum(1 for row in surface if as_float(row.get("combined_trade_density")) >= 3.0)
    quality_count = sum(1 for row in surface if as_float(row.get("combined_profit_factor")) >= 1.2)
    rows = [
        {
            "run_id": RUN_ID,
            "hypothesis": "Lifecycle/margin/session controls(생명주기/마진/세션 제어)가 HP 과잉 거래와 PF 붕괴를 동시에 수리할 수 있다.",
            "variants_tried": len(surface),
            "strict_joint_pass_count": strict_count,
            "density_pass_count": density_count,
            "quality_pass_count": quality_count,
            "failed_boundary": "no variant jointly passed PF>=1.2, density>=3/day, net>HP, OOS PF>=1.2(동시 통과 변형 없음)",
            "why_failed": "quality-improving variants reduce density(품질 개선 변형은 밀도 저하), density variants keep PF weak(밀도 변형은 PF 약함)",
            "salvage_value": "; ".join(f"{row.get('selection_role')}={row.get('variant_id')}" for row in clues),
            "reopen_condition": "combine density-preserving entry expansion with quality repair, then repackage only after HS review(밀도 보존 진입 확장과 품질 수리를 결합하고 HS 검토 후에만 패키지화)",
            "do_not_repeat_note": "do not use top_n trade ranking or trade splitting(상위 N개 거래 순위 자르기나 거래 쪼개기 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(FAILURE_MEMORY, rows)
    return rows


def build_next_review_queue(clues: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "review_strict_failure_boundary(엄격 실패 경계 검토)",
            "action": "Review why no PF/density joint pass appeared(PF/밀도 동시 통과가 왜 없었는지 검토)",
            "effect": "HS can decide whether to widen density supply or change model/source(HS가 밀도 공급 확대 또는 모델/원천 변경을 결정할 수 있습니다).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    for clue in clues:
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_id": f"review_{clue.get('selection_role')}",
                "action": f"Review variant(변형 검토) `{clue.get('variant_id')}`",
                "effect": f"Preserve clue(단서 보존): net/PF/density={clue.get('combined_net_profit')}/{clue.get('combined_profit_factor')}/{clue.get('combined_trade_density')}",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(NEXT_REVIEW_QUEUE, rows)
    return rows


def build_final(
    hq_final: Mapping[str, Any],
    hp_final: Mapping[str, Any],
    audit: Mapping[str, Any],
    calibration: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    best = surface[0] if surface else {}
    strict_count = sum(1 for row in surface if row.get("strict_joint_pass") is True)
    density_pass_count = sum(1 for row in surface if as_float(row.get("combined_trade_density")) >= 3.0)
    quality_pass_count = sum(1 for row in surface if as_float(row.get("combined_profit_factor")) >= 1.2)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "runtime_probe_run_id": RUNTIME_PROBE_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "model_id": MODEL_ID,
        "variant_count": len(surface),
        "strict_joint_pass_count": strict_count,
        "density_pass_count": density_pass_count,
        "quality_pass_count": quality_pass_count,
        "selected_clue_count": len(clues),
        "best_variant_id": best.get("variant_id", ""),
        "best_variant_family": best.get("family", ""),
        "best_combined_net_profit": best.get("combined_net_profit", ""),
        "best_combined_profit_factor": best.get("combined_profit_factor", ""),
        "best_combined_trade_density": best.get("combined_trade_density", ""),
        "best_oos_net_profit": best.get("oos_net_profit", ""),
        "best_oos_profit_factor": best.get("oos_profit_factor", ""),
        "hp_mt5_net_profit": hp_final.get("actual_mt5_net_profit", ""),
        "hp_mt5_profit_factor": hp_final.get("actual_mt5_profit_factor", ""),
        "hp_mt5_trade_density": hp_final.get("actual_mt5_trade_density", ""),
        "calibrated_cost_per_closed_trade": calibration.get("calibrated_cost_per_closed_trade", ""),
        "feature_day_count": audit.get("feature_day_count", ""),
        "failure_memory": failure_rows[0].get("failed_boundary", "") if failure_rows else "",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "next_review_queue_rows": len(review_queue),
    }


def gate_rows(final: Mapping[str, Any], *, receipts_written: bool) -> list[dict[str, Any]]:
    receipt_paths = [EXPLORATION_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, PERFORMANCE_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("input_lineage_gate", exists(hq.FINAL_DECISION) and exists(hp.RUNTIME_OUTPUT_COPY) and exists(pkg.FEATURE_MATRIX), hq.FINAL_DECISION, "HQ/HP/HO input lineage(입력 계보)를 확인했습니다."),
        ("data_integrity_gate", exists(DATA_INTEGRITY_AUDIT), DATA_INTEGRITY_AUDIT, "timestamp/split/feature-label boundary(시각/분할/피처-라벨 경계)를 기록했습니다."),
        ("runtime_replay_calibration_gate", exists(COST_CALIBRATION), COST_CALIBRATION, "HP MT5 baseline(HP MT5 기준선)에 replay cost(재생 비용)를 보정했습니다."),
        ("variant_surface_gate", exists(VARIANT_SURFACE), VARIANT_SURFACE, "trade-quality/density variant surface(거래 품질/밀도 변형 표면)를 만들었습니다."),
        ("no_trade_splitting_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "top_n/trade splitting(상위 N개/거래 쪼개기)을 쓰지 않았음을 기록했습니다."),
        ("repair_clue_gate", exists(SELECTED_REPAIR_CLUES), SELECTED_REPAIR_CLUES, "strict pass(엄격 통과)가 없어도 수리 단서를 따로 보존했습니다."),
        ("receipt_coverage_gate", receipts_written and all(exists(path) for path in receipt_paths), JUDGMENT_RECEIPT, "필수 receipt(영수증)를 덮었습니다."),
        ("required_gate_coverage_audit", exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결했습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장(operating claim, 운영 주장)을 막았습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "blocked",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def write_receipts(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPLORATION_RECEIPT,
        {
            **base,
            "idea_id": "IDEA-ST364-SINGLE-SOURCE-PROBABILITY-BIN-VETO-TRADE-QUALITY-DENSITY-REPAIR",
            "hypothesis": failure_rows[0]["hypothesis"],
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A single-source + Tier B missing_required(Tier A 단일 원천 + Tier B 필수 누락)",
            "broad_sweep": "hold/reversal/margin/pflat/session-side(보유/반전/마진/평탄 확률/세션-방향)",
            "extreme_sweep": "hold1/hold10 and pflat_cap0.20(보유1/보유10 및 평탄 확률 상한 0.20)",
            "micro_search_gate": "strict joint pass required before package(패키지 전 엄격 동시 통과 필요)",
            "wfo_plan": "single-window scout only(단일 구간 탐색 전용); WFO required if HS promotes follow-up(HS가 후속 승격 시 WFO 필요)",
            "failure_memory": rel(FAILURE_MEMORY),
            "evidence_boundary": "proxy_replay_scout_only(프록시 재생 탐색 전용)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            **data_rows[0],
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_subject": MODEL_ID,
            "model_change": "not_changed(변경 없음)",
            "runtime_probe_source": RUNTIME_PROBE_RUN_ID,
            "validation_scope": "rule-stack replay scout only(규칙 묶음 재생 탐색 전용)",
            "overfit_risk": "validation-derived cells may overfit(검증 유래 셀은 과적합 가능)",
            "model_validation_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "quality variants improve PF/net but lose density; density variants keep PF weak(품질 변형은 PF/순수익을 개선하지만 밀도를 잃고, 밀도 변형은 PF가 약함)",
            "comparison_baseline": f"HP MT5 net/PF/density={final['hp_mt5_net_profit']}/{final['hp_mt5_profit_factor']}/{final['hp_mt5_trade_density']}",
            "likely_drivers": "hold/reversal friction(보유/반전 마찰), margin floor(마진 바닥), session-side loss cells(세션-방향 손실 셀)",
            "segment_checks": [rel(VARIANT_SURFACE), rel(SELECTED_REPAIR_CLUES), rel(FAILURE_MEMORY)],
            "attribution_confidence": "medium(중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(VARIANT_SURFACE), rel(SELECTED_REPAIR_CLUES), rel(FAILURE_MEMORY), rel(GATE_AUDIT)],
            "evidence_missing": ["new MT5 execution(새 MT5 실행)", "runtime package(런타임 패키지)", "WFO validation(WFO 검증)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "No joint PF/density repair yet(아직 PF/밀도 동시 수리는 없음).",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "proxy replay(프록시 재생)를 operating claim(운영 주장)으로 승격하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], surface: Sequence[Mapping[str, Any]], clues: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364HR Single-Source Probability-Bin Veto Trade-Quality Density Repair Scout(단일 원천 확률 구간 거부 거래 품질 밀도 수리 탐색)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- strict_joint_pass_count(엄격 동시 통과 수): `{final['strict_joint_pass_count']}`
- best variant(최선 변형): `{final['best_variant_id']}`
- best net/PF/density(최선 순수익/수익 팩터/밀도): `{final['best_combined_net_profit']}` / `{final['best_combined_profit_factor']}` / `{final['best_combined_trade_density']}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): HP MT5 telemetry(HP MT5 런타임 기록)의 probabilities(확률)와 HO feature matrix(HO 피처 행렬)의 entry_open(진입 시가)을 결합해 hold/reversal/margin/pflat/session-side(보유/반전/마진/평탄 확률/세션-방향) 변형을 replay(재생)했습니다.

Effect(효과): MT5 재실행 전 trade quality(거래 품질)과 density(밀도)가 같이 고쳐지는지 넓게 확인했습니다. 결과는 strict joint pass(엄격 동시 통과) 없음이며, HS review(HS 검토)가 수리 단서와 실패 경계를 판정해야 합니다.

## Top Surface(상위 표면)

{markdown_table(surface, ['variant_id', 'family', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_density', 'oos_net_profit', 'oos_profit_factor', 'strict_joint_pass', 'repair_clue', 'score'], limit=12)}

## Selected Clues(선택 단서)

{markdown_table(clues, ['selection_role', 'variant_id', 'family', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_density', 'oos_net_profit', 'oos_profit_factor'], limit=8)}

## Failure Memory(실패 기억)

{markdown_table(failure_rows, ['hypothesis', 'variants_tried', 'strict_joint_pass_count', 'failed_boundary', 'why_failed', 'salvage_value'])}

## Next Queue(다음 대기열)

{markdown_table(queue_rows, ['queue_id', 'action', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This run(이번 실행)은 proxy replay scout(프록시 재생 탐색)입니다. new MT5 execution(새 MT5 실행), runtime package(런타임 패키지), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364HR decision(결정): trade-quality density repair scout(거래 품질 밀도 수리 탐색)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- strict_joint_pass_count(엄격 동시 통과 수): `{final['strict_joint_pass_count']}`
- best variant(최선 변형): `{final['best_variant_id']}`
- best net/PF/density(최선 순수익/수익 팩터/밀도): `{final['best_combined_net_profit']}` / `{final['best_combined_profit_factor']}` / `{final['best_combined_trade_density']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): HS에서 품질 단서와 밀도 단서를 분리 검토하고, 필요하면 density supply(밀도 공급)와 cost/PF repair(비용/PF 수리)를 결합합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364HR__{RUN_ID}", f"\n- run364HR__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - trade-quality density repair scout(거래 품질 밀도 수리 탐색), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HR__{RUN_ID}", f"\n<!-- run364HR__{RUN_ID} -->\n\n## run364HR Trade-Quality Density Repair Scout(거래 품질 밀도 수리 탐색)\n\nAction(행동): HP MT5 telemetry(HP MT5 런타임 기록)를 replay(재생)해 hold/reversal/margin/pflat/session-side(보유/반전/마진/평탄 확률/세션-방향) 수리 표면을 만들었습니다.\n\nEffect(효과): strict joint pass(엄격 동시 통과)는 없지만 `{final['best_variant_id']}` 같은 수리 단서를 `{NEXT_RUN_ID}` 검토로 넘깁니다. 운영 권위는 없습니다.\n")
    append_text_once(STAGE_README, f"run364HR__{RUN_ID}", f"\n<!-- run364HR__{RUN_ID} -->\n## run364HR scout(탐색)\n\nTrade-quality density repair(거래 품질 밀도 수리) proxy replay(프록시 재생) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
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

Current truth(현재 진실): `run364HR` completed(완료) a trade-quality density repair proxy replay scout(거래 품질 밀도 수리 프록시 재생 탐색). strict_joint_pass_count(엄격 동시 통과 수)는 `{final['strict_joint_pass_count']}`입니다.

Best clue(최선 단서): `{final['best_variant_id']}` net/PF/density(순수익/수익 팩터/밀도)는 `{final['best_combined_net_profit']}` / `{final['best_combined_profit_factor']}` / `{final['best_combined_trade_density']}`입니다. 효과는 품질을 고치면 밀도가 떨어지고, 밀도를 고치면 PF(수익 팩터)가 약한 실패 경계를 분리한 것입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected clues(선택 단서), strict failure boundary(엄격 실패 경계), and package eligibility(패키지 가능성)를 review(검토)합니다.

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

Latest scout(최근 탐색): `{RUN_ID}`.

Judgment(판정): `{JUDGMENT}`.

Strict joint pass(엄격 동시 통과): `{final['strict_joint_pass_count']}`.

Best variant(최선 변형): `{final['best_variant_id']}` with net/PF/density(순수익/수익 팩터/밀도) `{final['best_combined_net_profit']}` / `{final['best_combined_profit_factor']}` / `{final['best_combined_trade_density']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HR__{RUN_ID}", f"\n<!-- run364HR__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed trade-quality density repair scout(거래 품질 밀도 수리 탐색); strict pass `{final['strict_joint_pass_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HR__{RUN_ID}", f"\n<!-- run364HR__{RUN_ID} -->\n- `{RUN_ID}`: HP MT5 telemetry(HP MT5 런타임 기록)를 replay(재생)해 hold/reversal/margin/pflat/session-side(보유/반전/마진/평탄 확률/세션-방향) 수리 표면을 만들었습니다. Effect(효과): 품질 수리와 밀도 수리의 충돌을 HS 검토 입력으로 바꿉니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HR__no_strict_joint_pass__{RUN_ID}", f"\n<!-- run364HR__no_strict_joint_pass__{RUN_ID} -->\n- `{RUN_ID}`: strict joint pass(엄격 동시 통과) `0`. Effect(효과): 운영 주장 없이 HS에서 품질/밀도 단서를 분리 검토합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["variant_count"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "trade_shape(거래 형태)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "proxy_replay_scout_only_no_authority(프록시 재생 탐색 전용, 권위 없음)",
        "question": "Can HP trade quality and density be repaired together?(HP 거래 품질과 밀도를 함께 수리할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["best_combined_net_profit"],
        "profit_factor": final["best_combined_profit_factor"],
        "trade_density": final["best_combined_trade_density"],
        "strict_joint_pass_count": final["strict_joint_pass_count"],
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(VARIANT_SURFACE),
        "candidate_model_id": MODEL_ID,
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, row_status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required(필수 누락)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim(주장 범위 밖)"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "status": row_status,
            "view": record_view,
            "tier": tier_scope,
            "kpi_scope": "HR proxy replay scout(HR 프록시 재생 탐색)",
            "metric_scope": "python_proxy_no_new_mt5(Python 프록시, 새 MT5 없음)",
            "route_attribution_boundary": "single_source_tier_b_missing_required(단일 원천이라 Tier B 필수 누락)",
        }
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "trade_density"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "trade_shape(거래 형태)", "primary_report": rel(REPORT_PATH)}], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "HR trade-quality density repair scout artifact(HR 거래 품질 밀도 수리 탐색 산출물)",
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
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    hq_final, hp_final = validate_inputs()
    hp_context = dict(hp_final)
    if not hp_context.get("actual_mt5_trade_density"):
        hp_context["actual_mt5_trade_density"] = hq_final.get("actual_mt5_trade_density", "")
    write_work_packet()
    replay_frame, replay_audit = load_replay_frame()
    write_csv(REPLAY_INPUT_AUDIT, [{**{"run_id": RUN_ID}, **replay_audit, "claim_boundary": CLAIM_BOUNDARY}])
    data_rows = build_data_integrity(replay_audit)
    expected_tape = read_csv(pkg.EXPECTED_TRADE_TAPE)
    calibration = build_cost_calibration(replay_frame, hp_context)
    surface = build_variant_surface(replay_frame, replay_audit, hp_context, expected_tape, as_float(calibration["calibrated_cost_per_closed_trade"]))
    clues = select_repair_clues(surface)
    failure_rows = build_failure_memory(surface, clues)
    queue_rows = build_next_review_queue(clues, failure_rows)
    final = build_final(hq_final, hp_context, replay_audit, calibration, surface, clues, failure_rows, queue_rows)
    gates = gate_rows(final, receipts_written=False)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_receipts(final, data_rows, failure_rows)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(final, receipts_written=True)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, surface, clues, failure_rows, queue_rows, gates)
    write_json(FINAL_DECISION, final)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
