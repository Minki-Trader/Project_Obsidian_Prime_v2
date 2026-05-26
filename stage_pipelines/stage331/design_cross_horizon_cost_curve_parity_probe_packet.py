from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
RUN_NUMBER = "run331A"
RUN_ID = "run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1"
PARENT_RUN_ID = "run330G_raw_forward_failure_fragility_memory_and_overfit_followup_v1"
SOURCE_STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
STATUS = "completed_cross_horizon_cost_curve_parity_probe_design_no_selection"
JUDGMENT = "experiment_design_completed_research_only_no_goal_achieve"
DECISION = "stage331A_design_packet_completed_materialization_next_no_candidate_selection"
NEXT_ACTION = "run331B_materialize_no_retune_replay_and_resampling_controls_v1"
CLAIM_BOUNDARY = (
    "research_development_only_cross_horizon_cost_curve_parity_design_no_threshold_retuning_"
    "no_candidate_selection_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN330F_DIR = SOURCE_STAGE_DIR / "02_runs" / "run330F"
RUN330G_DIR = SOURCE_STAGE_DIR / "02_runs" / "run330G"
RUN330E_DIR = SOURCE_STAGE_DIR / "02_runs" / "run330E"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage331A_cross_horizon_cost_curve_parity_design.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def to_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return "\n".join(lines[: index + 1] + [block] + lines[index + 1 :]) + "\n"
    return text.rstrip() + "\n" + block + "\n"


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def load_inputs() -> dict[str, pd.DataFrame]:
    return {
        "pressure": read_csv(RUN330G_DIR / "overfit_pressure_matrix.csv"),
        "memory": read_csv(RUN330G_DIR / "failure_memory_report.csv"),
        "kpi": read_csv(RUN330F_DIR / "forward_mt5_kpi_report.csv"),
        "cost": read_csv(RUN330F_DIR / "cost_stress_report.csv"),
        "curve": read_csv(RUN330F_DIR / "curve_pocket_report.csv"),
        "direction": read_csv(RUN330F_DIR / "long_short_attribution_report.csv"),
        "trades": read_csv(RUN330F_DIR / "trade_level_records.csv"),
    }


def build_experiment_design(frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    trades = frames["trades"].copy()
    trades["open_time"] = pd.to_datetime(trades["open_time"], errors="coerce")
    trades["close_time"] = pd.to_datetime(trades["close_time"], errors="coerce")
    start = trades["open_time"].min()
    end = trades["close_time"].max()
    return {
        "run_id": RUN_ID,
        "hypothesis": "Stage330 preserved clues(보존 단서)는 retuning(재튜닝) 없이 cross-horizon/cost/curve/parity(교차 기간/비용/곡선/동등성) 압박을 견뎌야 다음 물질화로 갈 수 있다.",
        "decision_use": "run331B materialization(331B 물질화) 범위와 차단 조건을 정한다; candidate selection(후보 선택)에는 쓰지 않는다.",
        "comparison_baseline": "run330F raw-forward full-window MT5 result(원본 전진 전체 창 MT5 결과) and run330G high-pressure negative controls(높은 압력 부정 대조군)",
        "control_variables": [
            "candidate identity(후보 정체성)",
            "ONNX model(온엑스 모델)",
            "feature order(피처 순서)",
            "score threshold(점수 임계값)",
            "risk/lot/ATR SLTP logic(위험/수량/ATR 손절익절 로직)",
            "runtime handoff fields(런타임 인계 필드)",
        ],
        "changed_variables": [
            "evaluation slice only(평가 절편만 변경)",
            "cost stress ladder only(비용 압박 사다리만 변경)",
            "curve pocket partition only(곡선 포켓 분할만 변경)",
            "parity evidence requirement only(동등성 근거 요구만 변경)",
        ],
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "runtime_scope": "run330E/run330F raw-forward MT5 evidence",
            "start": None if pd.isna(start) else start.strftime("%Y-%m-%d %H:%M:%S"),
            "end": None if pd.isna(end) else end.strftime("%Y-%m-%d %H:%M:%S"),
            "trade_rows": int(trades.shape[0]),
            "attempts": sorted(frames["pressure"]["attempt_name"].astype(str).unique()),
        },
        "success_criteria": [
            "all planned views materialize without tuning(계획된 모든 보기 무튜닝 물질화)",
            "preserved clues retain interpretable cost/curve/direction evidence(보존 단서가 비용/곡선/방향 근거를 유지)",
            "runtime parity handoff paths are explicit(런타임 동등성 인계 경로가 명시됨)",
        ],
        "failure_criteria": [
            "preserved clue fails cost+1 and curve pocket together(보존 단서가 비용+1과 곡선 포켓을 함께 실패)",
            "cross-horizon slice reverses the full-window read(교차 기간 절편이 전체 창 판독을 뒤집음)",
            "D/B source or runtime parity remains untraceable for claims needing it(D/B 원천 또는 런타임 동등성 추적 불가)",
        ],
        "invalid_conditions": [
            "missing run330F or run330G artifacts(run330F 또는 run330G 산출물 누락)",
            "timestamp parse failure(타임스탬프 파싱 실패)",
            "candidate id mismatch across reports(보고서 간 후보 ID 불일치)",
            "any threshold/lot/rule retuning(임계값/수량/규칙 재튜닝 발생)",
        ],
        "stop_conditions": [
            "input artifact missing means block before materialization(입력 산출물 누락 시 물질화 전 차단)",
            "less than two horizon views per preserved clue means downgrade claim(보존 단서별 기간 보기 2개 미만이면 주장 하향)",
            "runtime handoff mismatch means runtime replay blocked(런타임 인계 불일치 시 런타임 재생 차단)",
        ],
        "evidence_plan": [
            "candidate_probe_matrix.csv",
            "cross_horizon_partition_plan.csv",
            "cost_curve_probe_plan.csv",
            "runtime_parity_handoff_plan.csv",
            "run331B materialized no-retune controls",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def role_for(row: Mapping[str, Any], memory: pd.DataFrame) -> str:
    attempt = str(row["attempt_name"])
    memory_row = memory.loc[memory["attempt_name"].astype(str).eq(attempt)]
    if not memory_row.empty:
        klass = str(memory_row.iloc[0]["memory_class"])
        if klass == "preserved_clue_not_selection":
            return "preserved_clue_not_selection"
    level = str(row["overfit_pressure_level"])
    if level == "high":
        return "negative_control_high_pressure"
    if level == "medium":
        return "fragility_control_medium_pressure"
    return "exploratory_control_low_pressure"


def build_candidate_matrix(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    pressure = frames["pressure"]
    memory = frames["memory"]
    rows: list[dict[str, Any]] = []
    for _, row in pressure.sort_values(["overfit_pressure_level", "attempt_name"]).iterrows():
        role = role_for(row, memory)
        required_views = [
            "full_forward",
            "month_split",
            "halves",
            "rolling_worst_pocket",
            "cost_ladder",
            "long_short_split",
            "runtime_parity_handoff",
        ]
        if role.startswith("preserved"):
            materialization_priority = "P1_preserved_clue"
            next_condition = "must survive no-retune cross-horizon and cost/curve evidence to remain a clue"
        elif "high" in role:
            materialization_priority = "P3_negative_control"
            next_condition = "used to prove the guard catches known fragile surfaces"
        else:
            materialization_priority = "P2_fragility_control"
            next_condition = "used to separate medium fragility from preserved clue behavior"
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "artifact_slug": row["artifact_slug"],
                "candidate_id": row["candidate_id"],
                "role": role,
                "materialization_priority": materialization_priority,
                "overfit_pressure_level": row["overfit_pressure_level"],
                "overfit_pressure_score": row["overfit_pressure_score"],
                "required_views": ";".join(required_views),
                "must_not_change": "threshold;lot;risk_logic;feature_order;ONNX;runtime_handoff",
                "next_condition": next_condition,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_horizon_plan(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    trades = frames["trades"].copy()
    trades["close_time"] = pd.to_datetime(trades["close_time"], errors="coerce")
    rows: list[dict[str, Any]] = []
    start = trades["close_time"].min()
    end = trades["close_time"].max()
    if pd.notna(start) and pd.notna(end):
        midpoint = start + (end - start) / 2
        rows.extend(
            [
                horizon_row("full_forward", "full raw-forward evidence(전체 원본 전진 근거)", start, end, trades, inclusive_end=True),
                horizon_row("first_half", "first half by close time(종료 시간 기준 전반)", start, midpoint, trades),
                horizon_row("second_half", "second half by close time(종료 시간 기준 후반)", midpoint, end, trades, inclusive_end=True),
            ]
        )
    for month, group in trades.dropna(subset=["close_time"]).groupby(trades["close_time"].dt.strftime("%Y-%m")):
        rows.append(horizon_row(f"month_{month}", f"calendar month(달력 월) {month}", group["close_time"].min(), group["close_time"].max(), trades, inclusive_end=True))
    curve = frames["curve"]
    worst = curve.loc[curve["chunk_type"].astype(str).eq("rolling_worst_net")]
    for _, row in worst.iterrows():
        rows.append(
            {
                "horizon_id": f"worst_pocket_{row['attempt_name']}",
                "description": "attempt-specific rolling worst pocket(시도별 롤링 최악 포켓)",
                "start_time": row.get("start_time"),
                "end_time": row.get("end_time"),
                "source_attempt": row.get("attempt_name"),
                "trade_rows_in_scope": row.get("trade_count"),
                "purpose": "stress known curve pocket without retuning(알려진 곡선 포켓을 무재튜닝 압박)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def horizon_row(horizon_id: str, description: str, start: pd.Timestamp, end: pd.Timestamp, trades: pd.DataFrame, inclusive_end: bool = False) -> dict[str, Any]:
    if inclusive_end:
        mask = (trades["close_time"] >= start) & (trades["close_time"] <= end)
    else:
        mask = (trades["close_time"] >= start) & (trades["close_time"] < end)
    return {
        "horizon_id": horizon_id,
        "description": description,
        "start_time": start,
        "end_time": end,
        "source_attempt": "all",
        "trade_rows_in_scope": int(mask.sum()),
        "purpose": "cross-horizon robustness read(교차 기간 강건성 판독)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_cost_plan(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    cost = frames["cost"]
    kpi = frames["kpi"]
    pressure = frames["pressure"]
    rows: list[dict[str, Any]] = []
    levels = sorted(float(value) for value in cost["extra_cost_per_round_trip_account_ccy"].unique())
    for _, row in pressure.iterrows():
        attempt = str(row["attempt_name"])
        base = kpi.loc[kpi["attempt_name"].astype(str).eq(attempt)].iloc[0].to_dict()
        for level in levels:
            cost_row = cost.loc[
                cost["attempt_name"].astype(str).eq(attempt)
                & cost["extra_cost_per_round_trip_account_ccy"].astype(float).eq(level)
            ].iloc[0].to_dict()
            rows.append(
                {
                    "attempt_name": attempt,
                    "artifact_slug": row["artifact_slug"],
                    "cost_level": level,
                    "base_profit_factor": base.get("profit_factor"),
                    "base_net_profit": base.get("net_profit"),
                    "expected_input_net_after_cost": cost_row.get("net_profit_after_cost"),
                    "expected_input_pf_after_cost": cost_row.get("profit_factor_after_cost"),
                    "probe_use": "verify cost curve monotonicity and survival margin(비용 곡선 단조성과 생존 여유 검증)",
                    "must_not_optimize": "lot;threshold;entry_filter;exit_rule",
                }
            )
    return rows


def build_runtime_parity_plan(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in candidate_rows:
        attempt = str(row["attempt_name"])
        rows.append(
            {
                "attempt_name": attempt,
                "research_path": rel(RUN330F_DIR / "trade_level_records.csv"),
                "runtime_path": rel(RUN330E_DIR / "mt5" / "reports"),
                "telemetry_path": rel(RUN330E_DIR / "runtime_telemetry" / f"{attempt}_telemetry.csv"),
                "shared_contract": "candidate_id;feature_order;fixed_threshold;risk_lot_ATR;bar_time",
                "known_differences": "D/B source is out_of_scope_by_claim(D/B 원천은 주장 범위 밖)",
                "parity_check_required": "report hash, telemetry row count, trade count, timestamp range",
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "block_condition": "missing telemetry or report identity mismatch",
            }
        )
    return rows


def build_materialization_queue(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    preserved = [row for row in candidate_rows if str(row["role"]).startswith("preserved")]
    controls = [row for row in candidate_rows if not str(row["role"]).startswith("preserved")]
    return [
        {
            "queue_id": NEXT_ACTION,
            "stage_id": STAGE_ID,
            "purpose": "materialize no-retune replay/resampling controls(무재튜닝 재생/재표본 대조군 물질화)",
            "primary_inputs": ";".join(str(row["attempt_name"]) for row in preserved),
            "control_inputs": ";".join(str(row["attempt_name"]) for row in controls),
            "required_outputs": "partitioned trades;cost ladders;curve pockets;runtime parity receipts",
            "blocked_if": "input mismatch, missing runtime telemetry, or retuning request",
            "status": "planned_next",
        },
        {
            "queue_id": "run331C_runtime_replay_or_block_cross_horizon_probe_v1",
            "stage_id": STAGE_ID,
            "purpose": "runtime replay or block(런타임 재생 또는 차단)",
            "primary_inputs": ";".join(str(row["attempt_name"]) for row in preserved),
            "control_inputs": ";".join(str(row["attempt_name"]) for row in controls),
            "required_outputs": "MT5 evidence or explicit data/runtime block",
            "blocked_if": "tester profile, broker session, or handoff parity cannot be reproduced",
            "status": "planned_after_run331B",
        },
    ]


def build_decision_payload(candidate_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    preserved = [str(row["attempt_name"]) for row in candidate_rows if str(row["role"]).startswith("preserved")]
    controls = [str(row["attempt_name"]) for row in candidate_rows if not str(row["role"]).startswith("preserved")]
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "selected_candidate": "none",
        "preserved_clues_not_selection": preserved,
        "negative_or_fragility_controls": controls,
        "next_action": NEXT_ACTION,
        "reason": "run331A only designs no-retune verification; it does not select, tune, or promote any ONNX.",
    }


def write_outputs(generated_at_utc: str) -> list[Path]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    SELECTED_DIR.mkdir(parents=True, exist_ok=True)
    frames = load_inputs()
    design = build_experiment_design(frames)
    candidate_rows = build_candidate_matrix(frames)
    horizon_rows = build_horizon_plan(frames)
    cost_rows = build_cost_plan(frames)
    parity_rows = build_runtime_parity_plan(candidate_rows)
    queue_rows = build_materialization_queue(candidate_rows)
    decision = build_decision_payload(candidate_rows)

    artifacts: list[Path] = []
    artifacts.append(write_json(RUN_DIR / "experiment_design_spec.json", design))
    artifacts.append(write_csv(RUN_DIR / "candidate_probe_matrix.csv", [
        "attempt_name", "artifact_slug", "candidate_id", "role", "materialization_priority",
        "overfit_pressure_level", "overfit_pressure_score", "required_views", "must_not_change",
        "next_condition", "claim_boundary",
    ], candidate_rows))
    artifacts.append(write_csv(RUN_DIR / "cross_horizon_partition_plan.csv", [
        "horizon_id", "description", "start_time", "end_time", "source_attempt",
        "trade_rows_in_scope", "purpose", "claim_boundary",
    ], horizon_rows))
    artifacts.append(write_csv(RUN_DIR / "cost_curve_probe_plan.csv", [
        "attempt_name", "artifact_slug", "cost_level", "base_profit_factor", "base_net_profit",
        "expected_input_net_after_cost", "expected_input_pf_after_cost", "probe_use", "must_not_optimize",
    ], cost_rows))
    artifacts.append(write_csv(RUN_DIR / "runtime_parity_handoff_plan.csv", [
        "attempt_name", "research_path", "runtime_path", "telemetry_path", "shared_contract",
        "known_differences", "parity_check_required", "runtime_claim_boundary", "block_condition",
    ], parity_rows))
    artifacts.append(write_csv(RUN_DIR / "materialization_queue.csv", [
        "queue_id", "stage_id", "purpose", "primary_inputs", "control_inputs",
        "required_outputs", "blocked_if", "status",
    ], queue_rows))
    artifacts.append(write_json(RUN_DIR / "model_validation_receipt.json", {
        "model_family": "Stage330 forward-safe non-identity ONNX clue set",
        "target_and_label": "fixed Stage330 score/signal behavior, no new label",
        "split_method": "runtime raw-forward plus planned cross-horizon slices",
        "selection_metric": "none_no_selection",
        "secondary_metrics": ["cost ladder", "curve pocket", "direction split", "runtime parity"],
        "threshold_policy": "fixed_no_retune",
        "overfit_risk": "single forward window and preserved-clue selection pressure",
        "calibration_risk": "scores are used as fixed decision surface, not probability claims",
        "comparison_baseline": "run330F full-window MT5 and run330G pressure matrix",
        "validation_judgment": "exploratory_design_only",
        "claim_boundary": CLAIM_BOUNDARY,
    }))
    artifacts.append(write_json(RUN_DIR / "runtime_parity_receipt.json", {
        "research_path": rel(RUN_DIR / "candidate_probe_matrix.csv"),
        "runtime_path": rel(RUN330E_DIR / "mt5"),
        "shared_contract": "fixed candidate identity, feature order, threshold, risk/lot/ATR and bar time",
        "known_differences": "D/B attribution remains out_of_scope_by_claim until source tags exist",
        "parity_check": "planned for run331B/run331C, not claimed by design run",
        "parity_identity": rel(RUN_DIR / "runtime_parity_handoff_plan.csv"),
        "runtime_claim_boundary": "research-only runtime_probe planning",
    }))
    artifacts.append(write_json(RUN_DIR / "result_judgment_receipt.json", {
        "result_subject": RUN_ID,
        "evidence_available": [rel(path) for path in artifacts[:6]],
        "evidence_missing": ["materialized replay controls", "fresh runtime replay", "final forward decision"],
        "judgment_label": "exploratory_design",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_ACTION,
        "user_explanation_hook": "검증 설계를 만든 것이며 후보 선택이 아니다.",
    }))
    artifacts.append(write_csv(RUN_DIR / "result_judgment.csv", [
        "run_id", "status", "judgment", "decision", "forward_passed", "forward_failed",
        "goal_achieve", "selected_candidate", "next_action", "claim_boundary",
    ], [{**decision, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY}]))
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", [
        "gate_name", "status", "evidence_path", "effect",
    ], gate_rows()))
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    artifacts.append(write_json(RUN_DIR / "run_manifest.json", {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "generated_at_utc": generated_at_utc,
        **decision,
        "claim_boundary": CLAIM_BOUNDARY,
    }))
    artifacts.extend(write_reports(design, candidate_rows, horizon_rows, queue_rows, decision))
    artifacts.append(update_selection_status(decision))
    artifacts.extend(update_current_truth(decision))
    update_registers(generated_at_utc, decision, artifacts)
    return artifacts


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "experiment_design(실험 설계)",
            "status": "completed",
            "evidence_path": rel(RUN_DIR / "experiment_design_spec.json"),
            "effect": "hypothesis/comparison/controls/scope/criteria(가설/비교/고정/범위/기준)를 고정한다.",
        },
        {
            "gate_name": "model_validation(모델 검증)",
            "status": "completed_design_only",
            "evidence_path": rel(RUN_DIR / "model_validation_receipt.json"),
            "effect": "threshold retuning(임계값 재튜닝) 없이 과적합 압력 검증 기준을 정한다.",
        },
        {
            "gate_name": "runtime_parity(런타임 동등성)",
            "status": "planned_not_claimed",
            "evidence_path": rel(RUN_DIR / "runtime_parity_handoff_plan.csv"),
            "effect": "런타임 권위가 아니라 다음 재생에서 확인할 handoff(인계) 조건을 적는다.",
        },
        {
            "gate_name": "result_judgment(결과 판정)",
            "status": "passed_no_goal_achieve",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "effect": "Forward Passed/Failed(전진 통과/실패), 선택 후보, Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
        {
            "gate_name": "artifact_lineage(산출물 계보)",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "effect": "run330F/run330G 근거에서 run331A 설계 산출물로 이어지는 경로를 연결한다.",
        },
    ]


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        RUN330G_DIR / "overfit_pressure_matrix.csv",
        RUN330G_DIR / "failure_memory_report.csv",
        RUN330G_DIR / "followup_experiment_queue.csv",
        RUN330F_DIR / "forward_mt5_kpi_report.csv",
        RUN330F_DIR / "cost_stress_report.csv",
        RUN330F_DIR / "curve_pocket_report.csv",
        RUN330F_DIR / "trade_level_records.csv",
        RUN330E_DIR / "runtime_telemetry",
    ]
    all_paths = list(dict.fromkeys([*artifacts, Path(__file__)]))
    return {
        "generated_at_utc": generated_at_utc,
        "source_inputs": [rel(path) for path in inputs],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in all_paths if path.exists()],
        "artifact_hashes": {rel(path): sha256_file(path) for path in all_paths if path.exists() and path.is_file()},
        "lineage_judgment": "connected_with_stage331A_design_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_reports(
    design: Mapping[str, Any],
    candidate_rows: Sequence[Mapping[str, Any]],
    horizon_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    decision: Mapping[str, Any],
) -> list[Path]:
    candidate_table = "\n".join([
        "| attempt(시도) | role(역할) | priority(우선순위) | pressure(압력) | next condition(다음 조건) |",
        "|---|---|---|---:|---|",
        *[
            f"| {row['attempt_name']} | {row['role']} | {row['materialization_priority']} | {row['overfit_pressure_score']} | {row['next_condition']} |"
            for row in candidate_rows
        ],
    ])
    horizon_table = "\n".join([
        "| horizon(기간) | start(시작) | end(종료) | rows(행) | purpose(목적) |",
        "|---|---|---|---:|---|",
        *[
            f"| {row['horizon_id']} | {csv_value(row['start_time'])} | {csv_value(row['end_time'])} | {row['trade_rows_in_scope']} | {row['purpose']} |"
            for row in horizon_rows[:12]
        ],
    ])
    queue_table = "\n".join([
        "| queue(대기열) | purpose(목적) | status(상태) |",
        "|---|---|---|",
        *[f"| {row['queue_id']} | {row['purpose']} | {row['status']} |" for row in queue_rows],
    ])
    report = write_md(
        REVIEWS_DIR / "run331A_cross_horizon_cost_curve_parity_design.md",
        f"""
# run331A Cross-Horizon Cost Curve Parity Design(331A 교차 기간 비용 곡선 동등성 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Experiment Design(실험 설계)

- hypothesis(가설): {design['hypothesis']}
- decision_use(결정 사용): {design['decision_use']}
- sample_scope(표본 범위): `{json.dumps(design['sample_scope'], ensure_ascii=False, sort_keys=True)}`

## Candidate Matrix(후보 행렬)

{candidate_table}

## Horizon Plan(기간 계획)

{horizon_table}

## Next Queue(다음 대기열)

{queue_table}
""",
    )
    decision_doc = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage331A Cross-Horizon Cost Curve Parity Design Decision(331A 교차 기간 비용 곡선 동등성 설계 결정)

- decision(결정): `{decision['decision']}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- preserved_clues_not_selection(선택 아닌 보존 단서): `{', '.join(decision['preserved_clues_not_selection']) or 'none'}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): 검증 설계는 완료했지만 materialized replay(물질화 재생)와 runtime replay(런타임 재생)는 아직 없으므로 성공/실패 판정을 닫지 않는다.
""",
    )
    return [report, decision_doc]


def update_selection_status(decision: Mapping[str, Any]) -> Path:
    return write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage331 Selection Status(331단계 선택 상태)

- stage_status(단계 상태): `open_in_progress`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_stage_status(원천 단계 상태): `closed_no_selection`
- latest_design(최신 설계): `{RUN_ID}`
- preserved_clues_not_selection(선택 아닌 보존 단서): `{', '.join(decision['preserved_clues_not_selection']) or 'none'}`
- negative_or_fragility_controls(부정 또는 취약성 대조군): `{', '.join(decision['negative_or_fragility_controls']) or 'none'}`
- current_run(현재 실행): `{NEXT_ACTION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): run331A는 검증 설계이며 후보 선택이나 운영 주장은 없다.
""",
    )


def update_current_truth(decision: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_ACTION}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus = (
        "- >-\n"
        f"  Stage331(331단계) run331A(331A 실행)는 `{decision['status']}`로 cross-horizon/cost/curve/parity design(교차 기간/비용/곡선/동등성 설계)을 완료했다. Effect(효과): 보존 단서를 선택하지 않고 run331B(331B 실행)의 no-retune materialization(무재튜닝 물질화)으로 넘긴다.\n"
    )
    if "Stage331(331단계) run331A(331A 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v2`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_ACTION}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `no_retune_cross_horizon_cost_curve_parity_materialization`",
        "- status(": f"- status(상태): `{decision['status']}`",
        "- decision(": f"- decision(판정): `{decision['judgment']}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run331A_summary(331A 요약): cross-horizon/cost/curve/parity design(교차 기간/비용/곡선/동등성 설계)을 `{decision['status']}`로 닫았다. "
        "Effect(효과): `c56_plain_rf`, `m48_plain_rf`는 선택 후보가 아니라 run331B(331B 실행)의 no-retune(무재튜닝) 검증 입력이다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run331A_summary(331A 요약)")
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    append_if_missing(
        CHANGELOG,
        "Stage331A Cross-Horizon Cost Curve Parity Design",
        f"""
## 2026-05-26 - Stage331A Cross-Horizon Cost Curve Parity Design(331A 교차 기간 비용 곡선 동등성 설계)

- run331A(331A 실행): Stage330(330단계)의 preserved clue(보존 단서)와 negative control(부정 대조군)을 no-retune(무재튜닝) 검증 설계로 묶었다.
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): 후보 선택 없이 run331B(331B 실행)의 물질화 대기열만 만든다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, decision: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run331A_cross_horizon_cost_curve_parity_design.md"
    upsert_csv(RUN_REGISTRY, ["run_id"], [{
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "experiment_design",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(report_path),
        "notes": "cross_horizon_cost_curve_parity_design;no_selection;goal_achieve_not_claimed.",
    }])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [{
        "ledger_row_id": f"{RUN_ID}__experiment_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "experiment_design",
        "tier_scope": "raw_forward_runtime_probe_total",
        "kpi_scope": "cross_horizon_cost_curve_parity_design",
        "scoreboard_lane": "experiment_design",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(report_path),
        "primary_kpi": "candidate_probe_matrix",
        "guardrail_kpi": "runtime_parity_plan;cost_curve_plan;horizon_plan",
        "external_verification_status": "out_of_scope_by_claim_design_only",
        "notes": f"decision={decision['decision']};next_action={NEXT_ACTION}.",
    }])
    upsert_csv(STAGE_LEDGER, ["row_id"], [{
        "row_id": f"{RUN_ID}__experiment_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "cross_horizon_cost_curve_parity_design(교차 기간 비용 곡선 동등성 설계)",
        "tier_scope": "raw_forward_runtime_probe_total(원본 전진 런타임 탐침 전체)",
        "scoreboard": "experiment_design_model_validation_runtime_parity(실험 설계/모델 검증/런타임 동등성)",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "evidence_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report_path),
        "notes": "no_candidate_selected;goal_achieve_not_claimed.",
        "decision": decision["decision"],
    }])
    artifact_rows = []
    for path in artifacts:
        if path.exists() and path.is_file():
            artifact_rows.append({
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage331A_design_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "cross-horizon cost/curve/parity design artifact; no operating claim.",
            })
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage331A cross-horizon cost/curve/parity design packet.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(json.dumps({
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "artifact_count": len(artifacts),
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
