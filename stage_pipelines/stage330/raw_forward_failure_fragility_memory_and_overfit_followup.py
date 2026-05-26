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
STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN_NUMBER = "run330G"
RUN_ID = "run330G_raw_forward_failure_fragility_memory_and_overfit_followup_v1"
PARENT_RUN_ID = "run330F_raw_forward_mt5_kpi_regime_cost_curve_review_v1"
STATUS = "completed_failure_fragility_memory_stage330_closed_no_selection"
JUDGMENT = "negative_memory_and_preserved_clues_no_forward_pass_no_goal_achieve"
DECISION = "stage330_closed_no_selection_forward_safe_rebuild_clues_preserved_stage331_open"
NEXT_STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
NEXT_RUN_ID = "run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1"
NEXT_ACTION = NEXT_RUN_ID
CLAIM_BOUNDARY = (
    "research_development_only_failure_memory_and_overfit_followup_no_threshold_retuning_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
NEXT_STAGE_BOUNDARY = (
    "research_development_only_cross_horizon_cost_curve_parity_probe_no_threshold_retuning_"
    "no_candidate_selection_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN330F_DIR = STAGE_DIR / "02_runs" / "run330F"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUTS_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_RUNS_DIR = NEXT_STAGE_DIR / "02_runs"
NEXT_REVIEWS_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330G_failure_fragility_memory.md"
NEXT_STAGE_DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage331_open_cross_horizon_cost_curve_parity_probe.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
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
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
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
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
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


def load_decision() -> dict[str, Any]:
    return json.loads(io_path(RUN330F_DIR / "final_forward_decision.json").read_text(encoding="utf-8"))


def cost_lookup(cost: pd.DataFrame) -> dict[tuple[str, float], Mapping[str, Any]]:
    lookup: dict[tuple[str, float], Mapping[str, Any]] = {}
    for _, row in cost.iterrows():
        attempt = str(row["attempt_name"])
        extra = float(row["extra_cost_per_round_trip_account_ccy"])
        lookup[(attempt, extra)] = row.to_dict()
    return lookup


def first_row(frame: pd.DataFrame, **filters: Any) -> Mapping[str, Any]:
    mask = pd.Series([True] * len(frame))
    for column, value in filters.items():
        mask &= frame[column].astype(str).eq(str(value))
    matched = frame.loc[mask]
    return {} if matched.empty else matched.iloc[0].to_dict()


def build_pressure_rows() -> list[dict[str, Any]]:
    kpi = read_csv(RUN330F_DIR / "forward_mt5_kpi_report.csv")
    cost = read_csv(RUN330F_DIR / "cost_stress_report.csv")
    curve = read_csv(RUN330F_DIR / "curve_pocket_report.csv")
    direction = read_csv(RUN330F_DIR / "long_short_attribution_report.csv")
    underwater = read_csv(RUN330F_DIR / "underwater_stretch_report.csv")
    db = read_csv(RUN330F_DIR / "db_attribution_report.csv")
    decision = load_decision()
    fragile = set(decision.get("fragility_flags", []))
    watchlist = set(decision.get("watchlist_not_selection", []))
    costs = cost_lookup(cost)
    rows: list[dict[str, Any]] = []
    for _, kpi_row in kpi.iterrows():
        attempt = str(kpi_row["attempt_name"])
        artifact = str(kpi_row["artifact_slug"])
        one_cost = costs.get((attempt, 1.0), {})
        two_cost = costs.get((attempt, 2.0), {})
        surviving_costs = [
            float(row["extra_cost_per_round_trip_account_ccy"])
            for _, row in cost.loc[cost["attempt_name"].astype(str).eq(attempt)].iterrows()
            if str(row["survives_pf_gt_1"]).lower() == "true"
        ]
        worst_curve = first_row(curve, attempt_name=attempt, chunk_type="rolling_worst_net")
        under = first_row(underwater, attempt_name=attempt)
        buy = first_row(direction, attempt_name=attempt, direction="buy")
        sell = first_row(direction, attempt_name=attempt, direction="sell")
        db_row = first_row(db, attempt_name=attempt)
        trade_count = to_float(kpi_row.get("trade_count")) or 0.0
        underwater_count = to_float(under.get("max_underwater_trade_count")) or 0.0
        underwater_ratio = underwater_count / trade_count if trade_count else None
        flags: list[str] = []
        score = 0
        pf = to_float(kpi_row.get("profit_factor")) or 0.0
        net = to_float(kpi_row.get("net_profit")) or 0.0
        dd_pct = to_float(kpi_row.get("equity_dd_percent")) or 0.0
        trades_per_day = to_float(kpi_row.get("trades_per_day")) or 0.0
        worst_net = to_float(worst_curve.get("net_profit")) or 0.0
        sell_net = to_float(sell.get("net_profit")) or 0.0
        sell_pf = to_float(sell.get("profit_factor")) or 0.0
        long_trades = to_float(kpi_row.get("long_trade_count")) or 0.0
        short_trades = to_float(kpi_row.get("short_trade_count")) or 0.0
        long_share = long_trades / trade_count if trade_count else None
        if net <= 25:
            flags.append("net_too_small_for_forward_robustness")
            score += 2
        if pf <= 1.05:
            flags.append("pf_near_flat")
            score += 3
        elif pf < 1.2:
            flags.append("pf_low_margin")
            score += 2
        if dd_pct > 20:
            flags.append("dd_percent_high")
            score += 2
        if trades_per_day < 4:
            flags.append("trade_density_below_us100_review_band")
            score += 1
        if str(one_cost.get("survives_pf_gt_1")).lower() != "true":
            flags.append("fails_plus1_cost_stress")
            score += 3
        if str(two_cost.get("survives_pf_gt_1")).lower() != "true":
            flags.append("fails_plus2_cost_stress")
            score += 1
        if worst_net < -50:
            flags.append("deep_rolling_curve_pocket")
            score += 2
        if underwater_ratio is not None and underwater_ratio > 0.50:
            flags.append("long_underwater_stretch")
            score += 2
        if sell_net < 0 or sell_pf < 1.0:
            flags.append("short_side_drag")
            score += 1
        if long_share is not None and long_share > 0.80:
            flags.append("long_side_concentration")
            score += 1
        if str(db_row.get("status", "")).lower() == "out_of_scope_by_claim":
            flags.append("db_source_missing_for_cp322a_attribution")
            score += 1
        if attempt in fragile:
            flags.append("run330f_fragility_flag")
            score += 2
        if attempt in watchlist:
            flags.append("watchlist_not_selection")
        level = "high" if score >= 8 else "medium" if score >= 5 else "low"
        rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": artifact,
                "candidate_id": kpi_row.get("candidate_id"),
                "feature_set_id": kpi_row.get("feature_set_id"),
                "model_id": kpi_row.get("model_id"),
                "net_profit": net,
                "profit_factor": pf,
                "trades_per_day": trades_per_day,
                "equity_dd_percent": dd_pct,
                "recovery_factor": to_float(kpi_row.get("recovery_factor")),
                "cost_1_net": to_float(one_cost.get("net_profit_after_cost")),
                "cost_1_pf": to_float(one_cost.get("profit_factor_after_cost")),
                "cost_1_survives": str(one_cost.get("survives_pf_gt_1")).lower() == "true",
                "cost_2_survives": str(two_cost.get("survives_pf_gt_1")).lower() == "true",
                "max_surviving_extra_cost": max(surviving_costs) if surviving_costs else None,
                "worst_rolling_net": worst_net,
                "worst_rolling_start": worst_curve.get("start_time"),
                "worst_rolling_end": worst_curve.get("end_time"),
                "max_underwater_trade_count": int(underwater_count),
                "underwater_trade_ratio": underwater_ratio,
                "buy_net": to_float(buy.get("net_profit")),
                "sell_net": sell_net,
                "sell_pf": sell_pf,
                "long_trade_share": long_share,
                "db_source_status": db_row.get("status"),
                "overfit_pressure_score": score,
                "overfit_pressure_level": level,
                "pressure_flags": ";".join(flags),
                "claim_effect": "research-only pressure evidence; no threshold, rule, or lot retuning",
            }
        )
    return rows


def build_failure_memory_rows(pressure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in pressure_rows:
        attempt = str(row["attempt_name"])
        artifact = str(row["artifact_slug"])
        flags = str(row["pressure_flags"])
        level = str(row["overfit_pressure_level"])
        watchlist = "watchlist_not_selection" in flags
        if watchlist and level in {"low", "medium"}:
            memory_class = "preserved_clue_not_selection"
            salvage = "raw-forward 양수와 비교적 나은 PF는 다음 cross-horizon(교차 기간) 검증 입력으로 보존한다."
        elif watchlist:
            memory_class = "fragile_preserved_clue_not_selection"
            salvage = "watchlist(관찰 목록)이지만 비용/곡선/방향 취약성 때문에 선택하지 않는다."
        else:
            memory_class = "negative_memory"
            salvage = "같은 feature/model(피처/모델) 조합을 좁게 반복하지 않는 실패 기억으로 보존한다."
        if "balanced" in str(row.get("model_id")):
            do_not_repeat = "class_weight balanced(균형 가중치)만 반복해서 같은 표면을 다시 만들지 않는다."
            reopen = "새 feature source(피처 원천)나 cost-aware validation(비용 인식 검증)이 있을 때만 재개한다."
        elif artifact.startswith("u42"):
            do_not_repeat = "US100-only technical(US100 단독 기술) 고밀도 표면을 threshold(임계값)만 바꿔 반복하지 않는다."
            reopen = "방향/비용/수중 구간을 동시에 줄이는 새 구조가 있을 때만 재개한다."
        else:
            do_not_repeat = "forward raw 양수만 보고 lot(수량)이나 threshold(임계값)를 맞추는 수리를 하지 않는다."
            reopen = "cross-horizon(교차 기간), cost stress(비용 압박), curve pocket(곡선 포켓)이 동시에 약해질 때만 재개한다."
        rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": artifact,
                "memory_class": memory_class,
                "hypothesis": "forward-safe non-identity ONNX(전진 안전 비정체성 온엑스)가 raw-forward(원본 전진)에서도 비용/곡선/방향 압박을 견디는가",
                "variants_tried": row.get("candidate_id"),
                "failed_boundary": flags,
                "why_failed": summarize_failure(row),
                "salvage_value": salvage,
                "do_not_repeat": do_not_repeat,
                "reopen_condition": reopen,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summarize_failure(row: Mapping[str, Any]) -> str:
    parts: list[str] = []
    if not row.get("cost_1_survives"):
        parts.append("+1.0 cost stress(비용 압박)에서 PF>1 유지 실패")
    if (to_float(row.get("worst_rolling_net")) or 0.0) < -50:
        parts.append("rolling worst pocket(롤링 최악 포켓)이 -50 아래")
    if (to_float(row.get("underwater_trade_ratio")) or 0.0) > 0.5:
        parts.append("underwater stretch(수중 구간)가 전체 거래의 절반 초과")
    if (to_float(row.get("sell_net")) or 0.0) < 0:
        parts.append("short side(숏 방향)가 손실")
    if (to_float(row.get("trades_per_day")) or 0.0) < 4:
        parts.append("US100 review band(검토 거래 밀도)보다 낮은 거래수")
    if not parts:
        parts.append("양수 단서는 있으나 D/B source(D/B 원천)와 장기 cost/curve 검증이 빠짐")
    return "; ".join(parts)


def build_followup_queue(pressure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    watchlist = [row["attempt_name"] for row in pressure_rows if "watchlist_not_selection" in str(row["pressure_flags"])]
    high = [row["attempt_name"] for row in pressure_rows if row["overfit_pressure_level"] == "high"]
    return [
        {
            "queue_id": NEXT_RUN_ID,
            "stage_id": NEXT_STAGE_ID,
            "purpose": "cross-horizon/cost/curve/parity guard design(교차 기간/비용/곡선/동등성 방어 설계)",
            "inputs": "run330F reports; run330G failure memory; raw-forward MT5 telemetry",
            "must_hold_fixed": "no threshold retuning; no lot optimization; no D/B invention; no live/deployment claim",
            "watchlist_inputs": ";".join(str(item) for item in watchlist),
            "negative_memory_inputs": ";".join(str(item) for item in high),
            "expected_output": "stage331A design packet and no-retune verification queue",
            "status": "planned_next",
        },
        {
            "queue_id": "run331B_materialize_no_retune_replay_and_resampling_controls_v1",
            "stage_id": NEXT_STAGE_ID,
            "purpose": "materialize no-retune replay controls(무재튜닝 재생 대조군 물질화)",
            "inputs": "stage331A design packet",
            "must_hold_fixed": "fixed candidate identities and fixed cost/curve criteria",
            "watchlist_inputs": ";".join(str(item) for item in watchlist),
            "negative_memory_inputs": ";".join(str(item) for item in high),
            "expected_output": "chunked forward replays, cost curves, direction-split robustness tables",
            "status": "planned_after_stage331A",
        },
        {
            "queue_id": "run331C_runtime_replay_or_block_cross_horizon_probe_v1",
            "stage_id": NEXT_STAGE_ID,
            "purpose": "runtime replay or block(런타임 재생 또는 차단)",
            "inputs": "stage331B materialized controls",
            "must_hold_fixed": "tester identity and runtime handoff parity receipts required",
            "watchlist_inputs": ";".join(str(item) for item in watchlist),
            "negative_memory_inputs": ";".join(str(item) for item in high),
            "expected_output": "MT5 evidence or explicit runtime/data block",
            "status": "planned_after_stage331B",
        },
    ]


def build_decision_payload(pressure_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    high = [str(row["attempt_name"]) for row in pressure_rows if row["overfit_pressure_level"] == "high"]
    medium = [str(row["attempt_name"]) for row in pressure_rows if row["overfit_pressure_level"] == "medium"]
    preserved = [str(row["attempt_name"]) for row in pressure_rows if "watchlist_not_selection" in str(row["pressure_flags"])]
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "selected_candidate": "none",
        "stage330_status": "closed_no_selection",
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "high_pressure_attempts": high,
        "medium_pressure_attempts": medium,
        "preserved_clues_not_selection": preserved,
        "reason": "run330F raw-forward MT5 evidence is real but cost, curve pocket, direction, and D/B-source gaps keep the result research-only.",
        "next_action": NEXT_ACTION,
    }


def write_outputs(generated_at_utc: str) -> list[Path]:
    for directory in [RUN_DIR, REVIEWS_DIR, SELECTED_DIR, NEXT_SPEC_DIR, NEXT_INPUTS_DIR, NEXT_RUNS_DIR, NEXT_REVIEWS_DIR, NEXT_SELECTED_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    pressure_rows = build_pressure_rows()
    memory_rows = build_failure_memory_rows(pressure_rows)
    queue_rows = build_followup_queue(pressure_rows)
    decision = build_decision_payload(pressure_rows)
    artifacts: list[Path] = []
    artifacts.append(write_csv(RUN_DIR / "overfit_pressure_matrix.csv", [
        "attempt_name", "artifact_slug", "candidate_id", "feature_set_id", "model_id",
        "net_profit", "profit_factor", "trades_per_day", "equity_dd_percent", "recovery_factor",
        "cost_1_net", "cost_1_pf", "cost_1_survives", "cost_2_survives", "max_surviving_extra_cost",
        "worst_rolling_net", "worst_rolling_start", "worst_rolling_end",
        "max_underwater_trade_count", "underwater_trade_ratio", "buy_net", "sell_net", "sell_pf",
        "long_trade_share", "db_source_status", "overfit_pressure_score", "overfit_pressure_level",
        "pressure_flags", "claim_effect",
    ], pressure_rows))
    artifacts.append(write_csv(RUN_DIR / "failure_memory_report.csv", [
        "attempt_name", "artifact_slug", "memory_class", "hypothesis", "variants_tried",
        "failed_boundary", "why_failed", "salvage_value", "do_not_repeat", "reopen_condition", "claim_boundary",
    ], memory_rows))
    artifacts.append(write_csv(RUN_DIR / "followup_experiment_queue.csv", [
        "queue_id", "stage_id", "purpose", "inputs", "must_hold_fixed", "watchlist_inputs",
        "negative_memory_inputs", "expected_output", "status",
    ], queue_rows))
    artifacts.append(write_json(RUN_DIR / "stage330_closeout_decision.json", decision))
    artifacts.append(write_json(RUN_DIR / "stage331_open_receipt.json", {
        "opened_by": RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage331_status": "open_planned",
        "claim_boundary": NEXT_STAGE_BOUNDARY,
        "reason": "Stage330 produced preserved clues but no robust forward pass; Stage331 must test cross-horizon cost/curve/parity without retuning.",
    }))
    artifacts.append(write_json(RUN_DIR / "model_validation_receipt.json", {
        "status": "completed",
        "evidence": rel(artifacts[0]),
        "judgment": "overfit pressure remains unresolved",
        "claim_boundary": CLAIM_BOUNDARY,
    }))
    artifacts.append(write_json(RUN_DIR / "result_judgment_receipt.json", {
        "result_subject": RUN_ID,
        "evidence_available": [rel(artifacts[0]), rel(artifacts[1]), rel(artifacts[2])],
        "evidence_missing": ["cross-horizon MT5 replay", "D/B source handoff attribution", "longer horizon cost/curve verification"],
        "judgment_label": "negative_memory_and_preserved_clues",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
    }))
    artifacts.append(write_csv(RUN_DIR / "result_judgment.csv", [
        "run_id", "status", "judgment", "decision", "forward_passed", "forward_failed", "goal_achieve", "selected_candidate", "next_action", "claim_boundary",
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
    artifacts.extend(write_reports(pressure_rows, memory_rows, queue_rows, decision))
    artifacts.extend(create_next_stage_files())
    artifacts.append(update_stage330_selection(decision))
    artifacts.extend(update_current_truth(decision))
    artifacts.append(update_negative_register(pressure_rows, memory_rows))
    update_registers(generated_at_utc, decision, artifacts)
    return artifacts


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "model_validation(모델 검증)",
            "status": "completed_unresolved_overfit_pressure",
            "evidence_path": rel(RUN_DIR / "overfit_pressure_matrix.csv"),
            "effect": "cost/curve/direction/D-B source(비용/곡선/방향/D-B 원천) 압력을 한 표로 묶어 선택 후보 주장을 막는다.",
        },
        {
            "gate_name": "exploration_failure_memory(탐색 실패 기억)",
            "status": "completed",
            "evidence_path": rel(RUN_DIR / "failure_memory_report.csv"),
            "effect": "negative memory(부정 기억)와 preserved clue(보존 단서)를 분리해 같은 과적합 수리를 반복하지 않는다.",
        },
        {
            "gate_name": "result_judgment(결과 판정)",
            "status": "passed_no_goal_achieve",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "effect": "Forward Passed/Failed(전진 통과/실패), selected candidate(선택 후보), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
        {
            "gate_name": "stage_transition(단계 전환)",
            "status": "completed_research_handoff_only",
            "evidence_path": rel(RUN_DIR / "stage331_open_receipt.json"),
            "effect": "Stage331(331단계)을 연구 검증 질문으로 열며 operating reference(운영 기준)를 만들지 않는다.",
        },
        {
            "gate_name": "artifact_lineage(산출물 계보)",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "effect": "run330F MT5 분석에서 run330G 실패 기억과 Stage331 입력으로 이어지는 경로를 연결한다.",
        },
    ]


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        RUN330F_DIR / "forward_mt5_kpi_report.csv",
        RUN330F_DIR / "cost_stress_report.csv",
        RUN330F_DIR / "curve_pocket_report.csv",
        RUN330F_DIR / "long_short_attribution_report.csv",
        RUN330F_DIR / "underwater_stretch_report.csv",
        RUN330F_DIR / "db_attribution_report.csv",
        RUN330F_DIR / "final_forward_decision.json",
    ]
    all_paths = list(dict.fromkeys([*artifacts, Path(__file__)]))
    return {
        "generated_at_utc": generated_at_utc,
        "source_inputs": [rel(path) for path in inputs],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_paths if path.exists()],
        "artifact_hashes": {rel(path): sha256_file(path) for path in all_paths if path.exists() and path.is_file()},
        "lineage_judgment": "connected_with_failure_memory_and_stage331_research_handoff",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_reports(
    pressure_rows: Sequence[Mapping[str, Any]],
    memory_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    decision: Mapping[str, Any],
) -> list[Path]:
    pressure_table = "\n".join([
        "| attempt(시도) | level(수준) | score(점수) | PF(수익 팩터) | cost+1 PF(비용+1 수익 팩터) | worst pocket(최악 포켓) | flags(표시) |",
        "|---|---|---:|---:|---:|---:|---|",
        *[
            f"| {row['attempt_name']} | {row['overfit_pressure_level']} | {row['overfit_pressure_score']} | {csv_value(row['profit_factor'])} | {csv_value(row['cost_1_pf'])} | {csv_value(row['worst_rolling_net'])} | {row['pressure_flags']} |"
            for row in sorted(pressure_rows, key=lambda item: int(item["overfit_pressure_score"]), reverse=True)
        ],
    ])
    memory_counts: dict[str, int] = {}
    for row in memory_rows:
        memory_counts[str(row["memory_class"])] = memory_counts.get(str(row["memory_class"]), 0) + 1
    queue_table = "\n".join([
        "| queue(대기열) | stage(단계) | purpose(목적) | status(상태) |",
        "|---|---|---|---|",
        *[f"| {row['queue_id']} | {row['stage_id']} | {row['purpose']} | {row['status']} |" for row in queue_rows],
    ])
    report = write_md(
        REVIEWS_DIR / "run330G_failure_fragility_memory_and_overfit_followup.md",
        f"""
# run330G Failure Fragility Memory and Overfit Follow-up(330G 실패 취약성 기억 및 과적합 후속)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- decision(결정): `{decision['decision']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Pressure Matrix(압력 표)

{pressure_table}

## Failure Memory(실패 기억)

- memory_counts(기억 수): `{json.dumps(memory_counts, ensure_ascii=False, sort_keys=True)}`
- preserved_clues_not_selection(선택 아닌 보존 단서): `{', '.join(decision['preserved_clues_not_selection']) or 'none'}`
- high_pressure_attempts(높은 압력 시도): `{', '.join(decision['high_pressure_attempts']) or 'none'}`
- effect(효과): raw-forward(원본 전진) 양수 후보도 비용, 곡선 포켓, 방향, D/B source(D/B 원천) 압력이 남으면 선택 후보가 아니다.

## Follow-up Queue(후속 대기열)

{queue_table}
""",
    )
    decision_doc = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage330G Failure Fragility Memory Decision(330G 실패 취약성 기억 결정)

- decision(결정): `{decision['decision']}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- stage330_status(330단계 상태): `{decision['stage330_status']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): Stage330(330단계)은 연구 단서와 실패 기억을 남기고 닫으며, Stage331(331단계)은 retuning(재튜닝) 없이 cross-horizon/cost/curve/parity(교차 기간/비용/곡선/동등성)를 확인한다.
""",
    )
    final_report = write_md(
        REVIEWS_DIR / "final_stage330G_decision_report.md",
        f"""
# Final Stage330G Decision Report(최종 330G 결정 보고서)

Stage330(330단계)은 `closed_no_selection(선택 없이 종료)`로 닫는다.

- raw_forward_mt5_evidence(원본 전진 MT5 근거): `available`
- preserved_clues_not_selection(선택 아닌 보존 단서): `{', '.join(decision['preserved_clues_not_selection']) or 'none'}`
- negative_or_high_pressure_memory(부정 또는 높은 압력 기억): `{', '.join(decision['high_pressure_attempts']) or 'none'}`
- selected_candidate(선택 후보): `none`
- operating_reference(운영 기준): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

Effect(효과): 좋은 숫자 일부를 성공으로 포장하지 않고, 과적합 방지 검증을 Stage331(331단계)로 넘긴다.
""",
    )
    next_stage_doc = write_md(
        NEXT_STAGE_DECISION_DOC,
        f"""
# 2026-05-26 Stage331 Open Decision(331단계 개방 결정)

- opened_by(개방 실행): `{RUN_ID}`
- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- status(상태): `open_planned`
- active_question(활성 질문): Stage330(330단계)의 보존 단서가 cross-horizon/cost/curve/parity(교차 기간/비용/곡선/동등성) 압박에서도 살아남는가?
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`
- effect(효과): Stage331(331단계)은 후보 수리나 임계값 조정이 아니라, 선택 전 검증 구조를 먼저 만든다.
""",
    )
    return [report, decision_doc, final_report, next_stage_doc]


def create_next_stage_files() -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(write_md(
        NEXT_SPEC_DIR / "stage_brief.md",
        f"""
# Stage331 Cross-Horizon Cost Curve Parity Probe(331단계 교차 기간 비용 곡선 동등성 탐침)

- active_question(활성 질문): Stage330(330단계)의 preserved clue(보존 단서)가 retuning(재튜닝) 없이 교차 기간, 비용 압박, 곡선 포켓, 런타임 동등성에서 버티는가?
- source_stage(원천 단계): `{STAGE_ID}`
- opened_by(개방 실행): `{RUN_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`

Effect(효과): run330F의 raw-forward(원본 전진) 양수 결과를 곧장 고치거나 선택하지 않고, 과적합 방지 검증을 먼저 설계한다.
""",
    ))
    artifacts.append(write_md(
        NEXT_INPUTS_DIR / "input_refs.md",
        f"""
# Stage331 Input References(331단계 입력 참조)

- run330F KPI(핵심 성과 지표): `stages/{STAGE_ID}/02_runs/run330F/forward_mt5_kpi_report.csv`
- run330F cost stress(비용 압박): `stages/{STAGE_ID}/02_runs/run330F/cost_stress_report.csv`
- run330F curve pocket(곡선 포켓): `stages/{STAGE_ID}/02_runs/run330F/curve_pocket_report.csv`
- run330G pressure matrix(압력 표): `stages/{STAGE_ID}/02_runs/run330G/overfit_pressure_matrix.csv`
- run330G failure memory(실패 기억): `stages/{STAGE_ID}/02_runs/run330G/failure_memory_report.csv`
- run330G follow-up queue(후속 대기열): `stages/{STAGE_ID}/02_runs/run330G/followup_experiment_queue.csv`

Effect(효과): 입력은 research handoff(연구 인계)이며 selected candidate(선택 후보)가 아니다.
""",
    ))
    artifacts.append(write_csv(
        NEXT_REVIEWS_DIR / "stage_run_ledger.csv",
        ["row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes", "decision"],
        [],
    ))
    artifacts.append(write_md(
        NEXT_SELECTED_DIR / "selection_status.md",
        f"""
# Stage331 Selection Status(331단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{STAGE_ID}`
- source_stage_status(원천 단계 상태): `closed_no_selection`
- preserved_clues_not_selection(선택 아닌 보존 단서): `c56_plain_rf, m48_plain_rf`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage331(331단계)은 후보 선택이 아니라 cross-horizon/cost/curve/parity(교차 기간/비용/곡선/동등성) 검증 설계부터 시작한다.
""",
    ))
    return artifacts


def update_stage330_selection(decision: Mapping[str, Any]) -> Path:
    return write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage330 Selection Status(330단계 선택 상태)

- stage_status(단계 상태): `closed_no_selection`
- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- research_onnx_status(연구 온엑스 상태): `failure_fragility_memory_completed_no_selection`
- latest_runtime_probe(최신 런타임 탐침): `run330E_mt5_runtime_probe_or_block_v1`
- latest_forward_review(최신 전진 검토): `{PARENT_RUN_ID}`
- latest_failure_memory(최신 실패 기억): `{RUN_ID}`
- preserved_clues_not_selection(선택 아닌 보존 단서): `{', '.join(decision['preserved_clues_not_selection']) or 'none'}`
- high_pressure_attempts(높은 압력 시도): `{', '.join(decision['high_pressure_attempts']) or 'none'}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): Stage330(330단계)은 일부 양수 단서를 보존하지만 선택 후보 없이 닫는다.
""",
    )


def update_current_truth(decision: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage331(331단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): Stage330(330단계)의 보존 단서를 선택하지 않고 cross-horizon/cost/curve/parity(교차 기간/비용/곡선/동등성) 검증 설계로 넘긴다.\n"
        "- >-\n"
        f"  Stage330(330단계) run330G(330G 실행)는 `{decision['status']}`로 Stage330(330단계)을 선택 없이 닫았다. Effect(효과): failure memory(실패 기억)와 preserved clues(보존 단서)를 남겼지만 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage331(331단계)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": f"- source_stage(원천 단계): `{STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `cross_horizon_cost_curve_parity_probe`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": "- status(상태): `open_planned`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run330G_summary(330G 요약): failure/fragility memory and overfit follow-up(실패/취약성 기억 및 과적합 후속)을 `{decision['status']}`로 닫았다. "
        "Effect(효과): `c56_plain_rf`, `m48_plain_rf`는 preserved clue(보존 단서)일 뿐이고, Stage331(331단계)의 교차 기간/비용/곡선/동등성 검증으로 넘긴다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run330G_summary(330G 요약)")
    stage331_summary = (
        f"- stage331_open_summary(331단계 개방 요약): `{NEXT_STAGE_ID}`를 open_planned(열림 계획)로 열었다. "
        "Effect(효과): 후보 수리보다 먼저 no-retune(무재튜닝) 검증 구조를 만든다."
    )
    current_text = insert_after_line(current_text, "- run330G_summary(", stage331_summary, "stage331_open_summary(331단계 개방 요약)")
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    append_if_missing(
        CHANGELOG,
        "Stage330G Failure Fragility Memory",
        f"""
## 2026-05-26 - Stage330G Failure Fragility Memory(330G 실패 취약성 기억)

- run330G(330G 실행): run330F(330F 실행)의 raw-forward MT5(원본 전진 MT5) 결과를 overfit pressure(과적합 압력), failure memory(실패 기억), follow-up queue(후속 대기열)로 분해했다.
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- effect(효과): Stage330(330단계)은 선택 후보 없이 닫고 Stage331(331단계)을 연구 검증 질문으로 열었다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_negative_register(pressure_rows: Sequence[Mapping[str, Any]], memory_rows: Sequence[Mapping[str, Any]]) -> Path:
    high = [str(row["attempt_name"]) for row in pressure_rows if row["overfit_pressure_level"] == "high"]
    preserved = [str(row["attempt_name"]) for row in pressure_rows if "watchlist_not_selection" in str(row["pressure_flags"])]
    memory_count = len(memory_rows)
    return append_if_missing(
        NEGATIVE_REGISTER,
        f"{RUN_ID} Stage330 failure memory",
        f"""
## {RUN_ID} Stage330 failure memory(330단계 실패 기억)

- failed_or_high_pressure_profiles(실패 또는 높은 압력 프로필): `{', '.join(high) or 'none'}`
- preserved_clues_not_selection(선택 아닌 보존 단서): `{', '.join(preserved) or 'none'}`
- memory_rows(기억 행): `{memory_count}`
- failure_boundary(실패 경계): raw-forward MT5(원본 전진 MT5) 양수 결과만으로는 cost stress(비용 압박), curve pocket(곡선 포켓), direction attribution(방향 귀속), D/B source(D/B 원천) 공백을 닫지 못했다.
- do_not_repeat(반복 금지): forward(전진) 양수 후보에 threshold(임계값), lot(수량), balanced/plain(균형/일반)만 좁게 맞추는 수리를 반복하지 않는다.
- reopen_condition(재개 조건): cross-horizon(교차 기간), cost stress(비용 압박), curve pocket(곡선 포켓), runtime parity(런타임 동등성)가 같은 no-retune(무재튜닝) 기준에서 동시에 약해질 때만 재개한다.
""",
    )


def update_registers(generated_at_utc: str, decision: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run330G_failure_fragility_memory_and_overfit_followup.md"
    upsert_csv(RUN_REGISTRY, ["run_id"], [{
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "model_validation_failure_memory",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(report_path),
        "notes": f"stage330_closed_no_selection;next_stage={NEXT_STAGE_ID};goal_achieve_not_claimed.",
    }])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [{
        "ledger_row_id": f"{RUN_ID}__failure_memory",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "failure_memory_and_stage_handoff",
        "tier_scope": "raw_forward_runtime_probe_total",
        "kpi_scope": "overfit_pressure_cost_curve_direction",
        "scoreboard_lane": "model_validation",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(report_path),
        "primary_kpi": "overfit_pressure_matrix",
        "guardrail_kpi": "failure_memory;followup_queue;stage331_open_receipt",
        "external_verification_status": "uses_completed_run330E_run330F_mt5_evidence",
        "notes": f"decision={decision['decision']};next_action={NEXT_ACTION}.",
    }])
    upsert_csv(STAGE_LEDGER, ["row_id"], [{
        "row_id": f"{RUN_ID}__failure_memory",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "failure_memory_and_stage_handoff(실패 기억 및 단계 인계)",
        "tier_scope": "raw_forward_runtime_probe_total(원본 전진 런타임 탐침 전체)",
        "scoreboard": "overfit_pressure_cost_curve_direction(과적합 압력/비용/곡선/방향)",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "evidence_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report_path),
        "notes": "stage330_closed_no_selection;goal_achieve_not_claimed.",
        "decision": decision["decision"],
    }])
    artifact_rows = []
    for path in artifacts:
        if path.exists() and path.is_file():
            artifact_rows.append({
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage330G_failure_memory_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID if str(path).find(NEXT_STAGE_ID) == -1 else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "failure memory and research handoff artifact; no operating claim.",
            })
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage330G raw-forward failure memory and overfit follow-up.")
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
        "next_stage_id": NEXT_STAGE_ID,
        "next_action": NEXT_ACTION,
        "artifact_count": len(artifacts),
        "goal_achieve": "not_claimed",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
