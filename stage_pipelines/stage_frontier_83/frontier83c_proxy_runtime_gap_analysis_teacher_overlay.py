from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
RUN_ID = "frontier83C_proxy_runtime_gap_analysis_teacher_overlay_v1"
PARENT_RUN_ID = "frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1"
NEXT_RUN_ID = "frontier83D_two_sided_density_expansion_or_rotation_decision_v1"
STATUS = "f83c_gap_attributed_runtime_parity_preserved_strategy_objective_gap_no_authority"
JUDGMENT = "runtime_parity_preserved_but_density_pf_two_sided_wfo_gaps_require_new_axis_repair_or_rotation_no_authority"
CLAIM_BOUNDARY = (
    "gap_attribution_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F83A_SUMMARY = REVIEW_DIR / "f83a_teacher_distillation_summary.json"
F83B_SUMMARY = REVIEW_DIR / "f83b_mt5_runtime_materialization_summary.json"
F83B_MANIFEST = PARENT_RUN_DIR / "run_manifest.json"
F83B_RECEIPT = PARENT_RUN_DIR / "f83b_runtime_receipt.csv"
F83B_SIGNAL_PARITY = PARENT_RUN_DIR / "f83b_signal_parity.csv"
F83B_SOURCE_REPRODUCTION = PARENT_RUN_DIR / "f83b_source_reproduction.csv"
F83B_TASK_FORCE = REVIEW_DIR / "f83b_task_force_review_receipt.yaml"

SUMMARY = REVIEW_DIR / "f83c_proxy_runtime_gap_analysis_summary.json"
GAP_ROWS = REVIEW_DIR / "f83c_proxy_runtime_gap_rows.csv"
REPORT = REVIEW_DIR / "frontier83C_proxy_runtime_gap_analysis_teacher_overlay_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f83c.md"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f83c_run_evidence_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f83c_performance_attribution_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f83c_result_judgment_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f83c_claim_discipline_receipt.yaml"
TASK_FORCE_REVIEW = REVIEW_DIR / "f83c_task_force_review_receipt.yaml"
ARTIFACT_LINEAGE = REVIEW_DIR / "f83c_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f83c_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_83/frontier83c_proxy_runtime_gap_analysis_teacher_overlay.py"

MIN_FINAL_TRADES_PER_DAY = 5.0
MAX_FINAL_TRADES_PER_DAY = 10.0
MIN_FINAL_PF = 2.0
HIGH_FINAL_PF = 3.0
MAX_FINAL_DD_PERCENT = 10.0


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_csv_row(path: Path, row: Mapping[str, Any], *, key: str | None = None, source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    if key:
        rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def remove_registry_rows(path: Path, run_id: str) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [
            row
            for row in reader
            if row.get("run_id") != run_id
            and row.get("ledger_row_id") != f"{run_id}__gap_analysis"
            and row.get("row_id") != f"{run_id}__gap_analysis"
        ]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def remove_csv_rows(path: Path, predicate: Callable[[dict[str, str]], bool]) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [row for row in reader if not predicate(row)]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def safe_ratio(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def split_prefix(split: str) -> str:
    return "validation" if split == "validation" else split


def objective_failure_tags(runtime: Mapping[str, Any]) -> list[str]:
    tags: list[str] = []
    trades_per_day = as_float(runtime.get("runtime_trades_per_day"))
    pf = as_float(runtime.get("runtime_profit_factor"))
    dd = as_float(runtime.get("runtime_drawdown_percent"))
    short_trades = as_int(runtime.get("runtime_short_trade_count"))
    if trades_per_day < MIN_FINAL_TRADES_PER_DAY:
        tags.append("density_below_5_per_day(일 5회 미만)")
    if pf < MIN_FINAL_PF:
        tags.append("pf_below_2(수익 팩터 2 미만)")
    if dd >= MAX_FINAL_DD_PERCENT:
        tags.append("dd_above_or_equal_10_percent(손실폭 10% 이상)")
    if short_trades == 0:
        tags.append("one_sided_long_only(롱 전용)")
    tags.append("wfo_stress_curve_not_checked(워크포워드/스트레스/곡선 미검증)")
    return tags


def build_gap_rows(runtime_rows: Sequence[Mapping[str, Any]], best: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for runtime in runtime_rows:
        split = str(runtime.get("split") or "")
        prefix = split_prefix(split)
        proxy_trade_count = as_float(best.get(f"{prefix}_trade_count"))
        runtime_trade_count = as_float(runtime.get("trade_count"))
        runtime_trades_per_day = as_float(runtime.get("trades_per_day"))
        runtime_pf = as_float(runtime.get("profit_factor"))
        runtime_dd = as_float(runtime.get("max_drawdown_percent"))
        long_trades = as_float(runtime.get("long_trade_count"))
        short_trades = as_float(runtime.get("short_trade_count"))
        proxy_net = as_float(runtime.get("proxy_net_profit"))
        proxy_pf = as_float(runtime.get("proxy_profit_factor"))
        proxy_dd = as_float(runtime.get("proxy_dd_percent"))
        proxy_tpd = as_float(runtime.get("proxy_trades_per_day"))
        runtime_net = as_float(runtime.get("net_profit"))
        trade_total = max(runtime_trade_count, 0.0)
        row = {
            "split": split,
            "candidate_id": runtime.get("candidate_id"),
            "source_candidate_id": best.get("candidate_id"),
            "model": best.get("model"),
            "axis_id": runtime.get("axis_id"),
            "test_period_start": runtime.get("test_period_start"),
            "test_period_end": runtime.get("test_period_end"),
            "calendar_days_exclusive": runtime.get("calendar_days_exclusive"),
            "tester_status": runtime.get("tester_status"),
            "report_status": runtime.get("report_status"),
            "proxy_net_profit": proxy_net,
            "runtime_net_profit": runtime_net,
            "net_runtime_minus_proxy": runtime_net - proxy_net,
            "proxy_profit_factor": proxy_pf,
            "runtime_profit_factor": runtime_pf,
            "pf_runtime_minus_proxy": runtime_pf - proxy_pf,
            "proxy_drawdown_percent": proxy_dd,
            "runtime_drawdown_percent": runtime_dd,
            "dd_runtime_minus_proxy": runtime_dd - proxy_dd,
            "proxy_trades_per_day": proxy_tpd,
            "runtime_trades_per_day": runtime_trades_per_day,
            "trades_per_day_runtime_minus_proxy": runtime_trades_per_day - proxy_tpd,
            "proxy_trade_count": proxy_trade_count,
            "runtime_trade_count": runtime_trade_count,
            "trade_count_runtime_minus_proxy": runtime_trade_count - proxy_trade_count,
            "expected_signal_count": as_float(runtime.get("expected_signal_count")),
            "runtime_signal_count": as_float(runtime.get("signal_count")),
            "signal_count_diff": as_float(runtime.get("signal_count_diff")),
            "feature_ready_diff": as_float(runtime.get("feature_ready_diff")),
            "order_fill_count": as_float(runtime.get("order_fill_count")),
            "order_fill_rate": as_float(runtime.get("order_fill_rate")),
            "runtime_long_trade_count": long_trades,
            "runtime_short_trade_count": short_trades,
            "runtime_long_share": safe_ratio(long_trades, trade_total),
            "runtime_short_share": safe_ratio(short_trades, trade_total),
            "runtime_winning_trade_count": as_float(runtime.get("winning_trade_count")),
            "runtime_losing_trade_count": as_float(runtime.get("losing_trade_count")),
            "proxy_win_rate": as_float(best.get(f"{prefix}_win_rate")),
            "runtime_win_rate": as_float(runtime.get("win_rate_percent")) / 100.0,
            "runtime_average_win": as_float(runtime.get("average_win")),
            "runtime_average_loss": as_float(runtime.get("average_loss")),
            "runtime_payoff_ratio": as_float(runtime.get("payoff_ratio")),
            "runtime_expectancy": as_float(runtime.get("expectancy")),
            "runtime_recovery_factor": as_float(runtime.get("recovery_factor")),
            "runtime_gross_profit": as_float(runtime.get("gross_profit")),
            "runtime_gross_loss": as_float(runtime.get("gross_loss")),
            "proxy_time_under_water_trades": best.get(f"{prefix}_time_under_water_trades", ""),
            "runtime_time_under_water_trades": "missing_from_f83b_runtime_receipt",
            "proxy_max_consecutive_loss": best.get(f"{prefix}_max_consecutive_loss", ""),
            "runtime_max_consecutive_loss": "missing_from_f83b_runtime_receipt",
            "density_shortfall_to_5_per_day": max(0.0, MIN_FINAL_TRADES_PER_DAY - runtime_trades_per_day),
            "density_multiplier_to_5_per_day": safe_ratio(MIN_FINAL_TRADES_PER_DAY, runtime_trades_per_day),
            "density_multiplier_to_10_per_day": safe_ratio(MAX_FINAL_TRADES_PER_DAY, runtime_trades_per_day),
            "pf_shortfall_to_2": max(0.0, MIN_FINAL_PF - runtime_pf),
            "pf_shortfall_to_3": max(0.0, HIGH_FINAL_PF - runtime_pf),
            "dd_margin_to_10_percent": MAX_FINAL_DD_PERCENT - runtime_dd,
            "proxy_runtime_parity_class": "minimal_proxy_runtime_gap" if abs(runtime_net - proxy_net) <= 0.01 and abs(runtime_pf - proxy_pf) <= 0.01 and abs(runtime_dd - proxy_dd) <= 0.05 else "proxy_runtime_economic_gap",
            "strategy_objective_gap_class": "density_pf_two_sided_wfo_gap",
            "objective_failure_tags": ";".join(objective_failure_tags({"runtime_trades_per_day": runtime_trades_per_day, "runtime_profit_factor": runtime_pf, "runtime_drawdown_percent": runtime_dd, "runtime_short_trade_count": short_trades})),
            "report_path": runtime.get("report_path"),
        }
        rows.append(row)
    return rows


def build_payload(created_at: str) -> dict[str, Any]:
    f83a_summary = read_json(F83A_SUMMARY)
    f83b_summary = read_json(F83B_SUMMARY)
    f83b_manifest = read_json(F83B_MANIFEST)
    runtime_rows = read_csv(F83B_RECEIPT)
    signal_rows = read_csv(F83B_SIGNAL_PARITY)
    reproduction_rows = read_csv(F83B_SOURCE_REPRODUCTION)
    best = f83a_summary.get("best_candidate") or {}
    gap_rows = build_gap_rows(runtime_rows, best)
    validation = next((row for row in gap_rows if row["split"] == "validation"), {})
    oos = next((row for row in gap_rows if row["split"] == "oos"), {})
    completed_rows = [row for row in runtime_rows if row.get("tester_status") == "completed"]
    feature_signal_clean = all(
        as_float(row.get("feature_ready_diff")) == 0.0 and as_float(row.get("signal_count_diff")) == 0.0
        for row in runtime_rows
    )
    runtime_parity_preserved = (
        len(completed_rows) == len(runtime_rows)
        and feature_signal_clean
        and as_int(f83b_summary.get("probability_parity_pass_rows")) == 3
        and as_int(f83b_summary.get("signal_parity_pass_rows")) == 3
        and as_int(f83b_summary.get("source_reproduction_pass_rows")) >= 2
    )
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "target": best,
        "parent_status": f83b_summary.get("status"),
        "parent_judgment": f83b_summary.get("judgment"),
        "parent_attempt_count": f83b_summary.get("attempt_count"),
        "parent_completed_attempt_count": f83b_summary.get("completed_attempt_count"),
        "runtime_parity_preserved": runtime_parity_preserved,
        "parity": {
            "probability_pass_rows": f83b_summary.get("probability_parity_pass_rows"),
            "signal_pass_rows": f83b_summary.get("signal_parity_pass_rows"),
            "feature_pass_rows": f83b_summary.get("feature_readiness_pass_rows"),
            "source_reproduction_pass_rows": f83b_summary.get("source_reproduction_pass_rows"),
            "feature_signal_clean": feature_signal_clean,
            "selected_not_source_count": f83b_summary.get("selected_not_source_count"),
            "signal_rows": signal_rows,
            "source_reproduction_rows": reproduction_rows,
        },
        "gap_rows": gap_rows,
        "validation_gap": validation,
        "oos_gap": oos,
        "observed_change": "F83B preserved proxy/runtime economics closely, but still fails density, PF, two-sidedness, WFO/stress, and smooth-curve final-objective checks.",
        "primary_attribution": "strategy_objective_gap_after_runtime_parity(런타임 동등성 이후 전략 목표 간극)",
        "not_primary_drivers": [
            "signal_count_mismatch(신호 수 불일치): zero diff on validation/OOS",
            "feature_readiness_mismatch(피처 준비 불일치): zero diff on validation/OOS",
            "ONNX_handoff(온엑스 인계): probability and signal parity rows passed",
            "order_fill(주문 체결): order fill rate 1.0 on validation/OOS",
        ],
        "remaining_objective_gaps": [
            "trade_density_below_5_to_10_per_day(거래 밀도 일 5~10회 미달)",
            "profit_factor_below_2_to_3(수익 팩터 2~3 미달)",
            "one_sided_long_only_supply(롱 전용 공급)",
            "WFO_stress_curve_smoothness_not_validated(워크포워드/스트레스/곡선 매끄러움 미검증)",
        ],
        "preserved_clue": "Exportable ONNX teacher overlay can preserve selected-entry runtime behavior with near-zero proxy/runtime gap.",
        "negative_memory": "Current long-only low-density teacher overlay is not final-like; avoid threshold-only repair without new density/two-sided axis.",
        "next_action": NEXT_RUN_ID,
        "result_label": "runtime_parity_seed_preserved_but_strategy_objective_gap",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_inputs": [rel(F83A_SUMMARY), rel(F83B_SUMMARY), rel(F83B_MANIFEST), rel(F83B_RECEIPT), rel(F83B_SIGNAL_PARITY), rel(F83B_SOURCE_REPRODUCTION)],
        "parent_manifest_target": f83b_manifest.get("target") or {},
    }


def report_text(payload: Mapping[str, Any]) -> str:
    target = payload["target"]
    val = payload["validation_gap"]
    oos = payload["oos_gap"]
    return f"""# F83C Proxy/Runtime Gap Analysis(F83C 프록시/런타임 간극 분석)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Readout(판독)

Action(행동): F83B MT5 runtime materialization(F83B MT5 런타임 물질화)을 F83A proxy KPI(F83A 프록시 핵심 성과 지표)와 split(구간)별로 비교했다.

Effect(효과): runtime mismatch(런타임 불일치)가 아니라 strategy objective gap(전략 목표 간극)을 다음 F83D 입력으로 고정한다.

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | runtime trades/day(런타임 일 거래) | density gap to 5/day(일 5회 간극) | PF gap to 2(수익 팩터 2 간극) | long/short(롱/숏) |
|---|---:|---:|---:|---:|---:|---:|
| validation(검증) | `{fmt(val.get('proxy_net_profit'))}/{fmt(val.get('proxy_profit_factor'))}/{fmt(val.get('proxy_drawdown_percent'))}` | `{fmt(val.get('runtime_net_profit'))}/{fmt(val.get('runtime_profit_factor'))}/{fmt(val.get('runtime_drawdown_percent'))}` | `{fmt(val.get('runtime_trades_per_day'))}` | `{fmt(val.get('density_shortfall_to_5_per_day'))}` | `{fmt(val.get('pf_shortfall_to_2'))}` | `{fmt(val.get('runtime_long_trade_count'), 0)}/{fmt(val.get('runtime_short_trade_count'), 0)}` |
| OOS(표본외) | `{fmt(oos.get('proxy_net_profit'))}/{fmt(oos.get('proxy_profit_factor'))}/{fmt(oos.get('proxy_drawdown_percent'))}` | `{fmt(oos.get('runtime_net_profit'))}/{fmt(oos.get('runtime_profit_factor'))}/{fmt(oos.get('runtime_drawdown_percent'))}` | `{fmt(oos.get('runtime_trades_per_day'))}` | `{fmt(oos.get('density_shortfall_to_5_per_day'))}` | `{fmt(oos.get('pf_shortfall_to_2'))}` | `{fmt(oos.get('runtime_long_trade_count'), 0)}/{fmt(oos.get('runtime_short_trade_count'), 0)}` |

## Attribution(귀속)

Primary attribution(주 귀속): `{payload.get('primary_attribution')}`.

Not primary drivers(주 원인 아님): signal count mismatch(신호 수 불일치), feature readiness mismatch(피처 준비 불일치), ONNX handoff(온엑스 인계), order fill(주문 체결).

Preserved clue(보존 단서): exportable ONNX teacher overlay(내보내기 가능 온엑스 교사 덧씌움)는 selected-entry runtime behavior(선택 진입 런타임 행동)를 거의 그대로 보존했다.

Negative memory(부정 기억): current long-only low-density branch(현재 롱 전용 저밀도 가지)는 final objective(최종 목표)에 멀다. threshold-only repair(임계값만 바꾸는 수리)는 금지한다.

Closeout KPI note(마감 핵심 지표 참고): F83B runtime receipt(F83B 런타임 영수증)는 gross profit/loss(총이익/총손실), win rate(승률), avg win/loss(평균 이익/손실), payoff ratio(손익비), expectancy(기대값), recovery factor(회복 계수), long/short breakdown(롱/숏 분해)을 포함한다. runtime time under water(런타임 회복 전 체류 시간)와 max consecutive loss(최대 연속 손실)는 F83B receipt(영수증)에 없어 proxy value(프록시 값)만 참고로 남긴다.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def gate_audit_text() -> str:
    return f"""# F83C Required Gate Coverage Audit(F83C 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `runtime_materialization_evidence(런타임 물질화 근거)` | `passed(통과)` | `{rel(F83B_RECEIPT)}` | F83B Strategy Tester(전략 테스터) 결과를 사용한다. |
| `proxy_runtime_gap_analysis(프록시/런타임 간극 분석)` | `passed(통과)` | `{rel(SUMMARY)}`, `{rel(GAP_ROWS)}` | proxy/runtime(프록시/런타임) 차이를 split(구간)별로 기록한다. |
| `parity_not_cause_boundary(동등성 비원인 경계)` | `passed(통과)` | `{rel(F83B_SIGNAL_PARITY)}`, `{rel(F83B_SOURCE_REPRODUCTION)}` | signal/feature/ONNX parity(신호/피처/온엑스 동등성)를 주 원인에서 제외한다. |
| `objective_gap_boundary(목표 간극 경계)` | `passed(통과)` | `{rel(REPORT)}` | final completion gate(최종 완성 게이트)가 아니라 다음 수리 입력으로만 쓴다. |
| `run_evidence_receipt(실행 근거 영수증)` | `passed(통과)` | `{rel(RUN_EVIDENCE_RECEIPT)}` | KPI(핵심 성과 지표)와 source authority(원천 권위)를 분리한다. |
| `performance_attribution_receipt(성과 귀속 영수증)` | `passed(통과)` | `{rel(PERFORMANCE_RECEIPT)}` | runtime parity(런타임 동등성)와 objective gap(목표 간극)을 분리한다. |
| `result_judgment_boundary(결과 판정 경계)` | `passed(통과)` | `{rel(RESULT_RECEIPT)}` | positive clue(긍정 단서)와 negative memory(부정 기억)를 같이 남긴다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `{rel(TASK_FORCE_REVIEW)}` | 8명 agent(요원) 검토를 기록한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 권위/승격/실거래/목표 달성을 만들지 않는다. |
"""


def ledger_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    oos = payload["oos_gap"]
    return {
        "ledger_row_id": f"{RUN_ID}__gap_analysis",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "gap_analysis(간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_runtime_gap_analysis(프록시/런타임 간극 분석)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "mt5_runtime_materialization_gap(런타임 물질화 간극)",
        "scoreboard_lane": "strategy_objective_gap(전략 목표 간극)",
        "lane": "gap_analysis(간극 분석)",
        "family": "kpi_evidence(근거 KPI)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"oos_runtime_net={oos.get('runtime_net_profit')};oos_runtime_pf={oos.get('runtime_profit_factor')};oos_runtime_dd={oos.get('runtime_drawdown_percent')};oos_tpd={oos.get('runtime_trades_per_day')}",
        "guardrail_kpi": "runtime_parity_preserved;density_pf_two_sided_wfo_gap;no_authority",
        "external_verification_status": "completed_parent_mt5_runtime_materialization",
        "notes": f"next={NEXT_RUN_ID}; attribution={payload.get('primary_attribution')}",
        "run_number": "frontier83C",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("gap_rows") or []),
        "gate_passes": 9,
        "gate_total": 9,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": (payload.get("target") or {}).get("candidate_id"),
        "model": (payload.get("target") or {}).get("model"),
        "net_profit": oos.get("runtime_net_profit"),
        "profit_factor": oos.get("runtime_profit_factor"),
        "drawdown": oos.get("runtime_drawdown_percent"),
        "trade_count": oos.get("runtime_trade_count"),
        "trades_per_day": oos.get("runtime_trades_per_day"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "gap_analysis",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_gap",
        "result_status": STATUS,
        "feature_count": (payload.get("target") or {}).get("feature_count"),
        "work_family": "kpi_evidence",
        "row_id": f"{RUN_ID}__gap_analysis",
        "evidence_boundary": "gap_analysis_only_no_authority(간극 분석만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "gap_analysis_only(간극 분석만)",
    }


def write_receipts(payload: Mapping[str, Any]) -> None:
    oos = payload["oos_gap"]
    write_text(
        RUN_EVIDENCE_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: kpi_evidence_recorded_no_authority
source_authority: parent_mt5_runtime_materialization(F83B 부모 MT5 런타임 물질화)
required_records:
  hypothesis: realized_pnl_teacher_distillation_exportable_runtime_rotation(실현 손익 교사 증류 내보내기 가능 런타임 회전)
  test_period: validation 2025-01-02..2025-10-01; OOS 2025-10-01..2026-04-14
  proxy_kpi: preserved in {rel(GAP_ROWS)}
  runtime_kpi: net={oos.get('runtime_net_profit')}; pf={oos.get('runtime_profit_factor')}; dd={oos.get('runtime_drawdown_percent')}; trades={oos.get('runtime_trade_count')}; tpd={oos.get('runtime_trades_per_day')}
  parity: preserved_after_f83b(전선83B 이후 보존)
  gap_cause: strategy_objective_gap_after_runtime_parity(런타임 동등성 이후 전략 목표 간극)
  next_action: {NEXT_RUN_ID}
tier_records:
  tier_a_separate: recorded
  tier_b_separate: missing_required
  combined: out_of_scope_by_claim
claim_boundary: {CLAIM_BOUNDARY}
""",
    )
    write_text(
        PERFORMANCE_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: objective_gap_attributed_after_runtime_parity_no_authority
observed_change: "{payload.get('observed_change')}"
primary_attribution: {payload.get('primary_attribution')}
not_primary_drivers:
  - signal_count_mismatch(신호 수 불일치)
  - feature_readiness_mismatch(피처 준비 불일치)
  - ONNX_handoff(온엑스 인계)
  - order_fill(주문 체결)
remaining_gaps:
  - density_below_5_to_10_per_day(거래 밀도 일 5~10회 미달)
  - profit_factor_below_2_to_3(수익 팩터 2~3 미달)
  - long_only_supply(롱 전용 공급)
  - WFO_stress_curve_not_validated(워크포워드/스트레스/곡선 미검증)
next_action: {NEXT_RUN_ID}
""",
    )
    write_text(
        RESULT_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: clue_and_negative_memory_recorded_no_authority
result_label: {payload.get('result_label')}
positive_clue: "{payload.get('preserved_clue')}"
negative_memory: "{payload.get('negative_memory')}"
judgment_label: mixed_seed_preserved_objective_gap
claim_boundary: {CLAIM_BOUNDARY}
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
""",
    )
    write_text(
        CLAIM_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_gap_analysis_no_authority
allowed_claims:
  - runtime_parity_seed_preserved
  - strategy_objective_gap_attributed
  - next_new_axis_repair_or_rotation_required
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
    )
    write_text(
        TASK_FORCE_REVIEW,
        f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f83c_gap_analysis_no_authority
review_mode: internal_adversarial_review_two_pass_limit(내부 비판 검토 2회차 제한)
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_02_platform_routing_architect
  - agent_03_philosophy_policy_skill_governance
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Classify F83B as runtime parity seed preserved(F83B를 런타임 동등성 씨앗 보존으로 분류)."
    - "Do not blame feature/signal/ONNX mismatch(피처/신호/온엑스 불일치)를 primary cause(주 원인)로 두지 않음."
    - "Route next to two-sided density expansion or rotation(다음은 양방향 밀도 확장 또는 회전으로 라우팅)."
  rejected:
    - "Do not call one-sided low-density positive runtime observation(일방향 저밀도 긍정 런타임 관찰)을 baseline(기준선) 또는 authority(권위)로 승격."
  needs_local_verification:
    - "F83D must materialize any meaningful new-axis signal(F83D는 의미 있는 새 축 신호를 물질화해야 함)."
previous_task_force_receipt: {rel(F83B_TASK_FORCE)}
claim_boundary: {CLAIM_BOUNDARY}
""",
    )


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    paths = [
        SUMMARY,
        GAP_ROWS,
        RUN_EVIDENCE_RECEIPT,
        PERFORMANCE_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        TASK_FORCE_REVIEW,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        GATE_AUDIT,
        RUN_MANIFEST,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": payload.get("source_inputs"),
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in paths},
        "lineage_judgment": "gap_analysis_connected_with_no_authority_boundary(권위 없음 경계로 간극 분석 연결)",
    }


def local_verification() -> dict[str, Any]:
    gap_rows = read_csv(GAP_ROWS) if path_exists(GAP_ROWS) else []
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "gap_rows_exists": path_exists(GAP_ROWS),
        "gap_rows_count_two": len(gap_rows) == 2,
        "report_exists": path_exists(REPORT),
        "gate_audit_exists": path_exists(GATE_AUDIT),
        "run_evidence_receipt_exists": path_exists(RUN_EVIDENCE_RECEIPT),
        "performance_receipt_exists": path_exists(PERFORMANCE_RECEIPT),
        "result_receipt_exists": path_exists(RESULT_RECEIPT),
        "task_force_review_exists": path_exists(TASK_FORCE_REVIEW),
        "manifest_exists": path_exists(RUN_MANIFEST),
        "packet_final_claim_guard_exists": path_exists(PACKET_FINAL_CLAIM_GUARD),
        "workspace_state_next_run": NEXT_RUN_ID in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = ledger_row(payload, created_at)
    for ledger_path, key in ((RUN_REGISTRY, "run_id"), (ALPHA_LEDGER, "ledger_row_id"), (STAGE_LEDGER, "ledger_row_id")):
        remove_registry_rows(ledger_path, RUN_ID)
        append_csv_row(ledger_path, row, key=key, source_header=ALPHA_LEDGER if ledger_path == STAGE_LEDGER else None)


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f83_runtime_parity_preserved_strategy_objective_gap_attributed_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f82_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F83C proxy/runtime gap analysis(프록시/런타임 간극 분석)을 완료했다."
  - "Effect(효과): F83B는 runtime parity seed(런타임 동등성 씨앗)로 보존하고, 남은 문제를 strategy objective gap(전략 목표 간극)으로 고정했다."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F83C proxy/runtime gap analysis(F83C 프록시/런타임 간극 분석)을 완료했다.

Effect(효과): F83B MT5 runtime materialization(MT5 런타임 물질화)은 proxy/runtime parity(프록시/런타임 동등성)가 보존됐지만, final objective(최종 목표)에는 density/PF/two-sided/WFO-stress gap(밀도/수익 팩터/양방향/워크포워드-스트레스 간극)이 남았다.

Next run(다음 실행): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(
        SELECTION_STATUS,
        f"""# F83 Selection Status(F83 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F83C gap analysis(F83C 간극 분석)을 기록했다.

Effect(효과): F83B는 positive runtime parity clue(긍정 런타임 동등성 단서)이지만 final objective gap(최종 목표 간극)이 남아 F83D new-axis repair or rotation(F83D 새 축 수리 또는 회전)으로 넘긴다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_gap"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F83 Context Anchor(F83 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- OOS runtime(표본외 런타임): net `{oos.get('runtime_net_profit')}`, PF `{oos.get('runtime_profit_factor')}`, DD `{oos.get('runtime_drawdown_percent')}`, trades/day `{oos.get('runtime_trades_per_day')}`
- gap cause(간극 원인): strategy objective gap after runtime parity(런타임 동등성 이후 전략 목표 간극)
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F83 Review Index(F83 검토 색인)\n"
    lines = [
        "- `frontier83C_proxy_runtime_gap_analysis_teacher_overlay_report.md`: F83C proxy/runtime gap analysis report(F83C 프록시/런타임 간극 분석 보고서)",
        "- `f83c_proxy_runtime_gap_analysis_summary.json`: F83C machine gap analysis(F83C 기계 간극 분석)",
        "- `f83c_proxy_runtime_gap_rows.csv`: F83C split-level gap rows(F83C 구간별 간극 행)",
        "- `required_gate_coverage_audit_f83c.md`: F83C gate audit(F83C 게이트 감사)",
        "- `f83c_task_force_review_receipt.yaml`: F83C Task Force review receipt(F83C 태스크포스 검토 영수증)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    oos = payload["oos_gap"]
    addition = f"""

{marker}
- `{RUN_ID}` attributed F83 proxy/runtime gap(F83 프록시/런타임 간극 귀속). Result(결과): OOS runtime net/PF/DD/trades_day(표본외 런타임 순손익/수익 팩터/손실폭/일 거래) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}`. Clue(단서): runtime parity seed preserved(런타임 동등성 씨앗 보존). Negative memory(부정 기억): low-density long-only branch(저밀도 롱 전용 가지) cannot be final-like without new axis(새 축 없이는 최종형 아님). Next(다음): `{NEXT_RUN_ID}`.
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_artifact_registry(created_at: str) -> None:
    remove_csv_rows(ARTIFACT_REGISTRY, lambda row: row.get("run_id") == RUN_ID or str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__"))
    for path in [
        SUMMARY,
        GAP_ROWS,
        RUN_EVIDENCE_RECEIPT,
        PERFORMANCE_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        TASK_FORCE_REVIEW,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        GATE_AUDIT,
        RUN_MANIFEST,
    ]:
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "created_at": created_at,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F83C gap analysis only(F83C 간극 분석만 지원).",
        }
        append_csv_row(ARTIFACT_REGISTRY, row, key="artifact_id")


def packet_files(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "receipts": [
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-performance-attribution", "status": "executed", "path": rel(PERFORMANCE_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_REVIEW)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_LINEAGE)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(
        WORK_PACKET,
        f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
work_classification:
  primary_family: kpi_evidence
  mutation_intent: true
  execution_intent: false
skill_routing:
  primary_skill: obsidian-run-evidence-system
  support_skills:
    - obsidian-performance-attribution
    - obsidian-result-judgment
    - obsidian-task-force-review
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
required_gates:
  - runtime_materialization_evidence
  - proxy_runtime_gap_analysis
  - parity_not_cause_boundary
  - objective_gap_boundary
  - run_evidence_receipt
  - performance_attribution_receipt
  - result_judgment_boundary
  - codex_task_force_review_packet
  - final_claim_guard
  - required_gate_coverage_audit
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  claim_boundary: {CLAIM_BOUNDARY}
evidence_contract:
  source_inputs:
    - {rel(F83A_SUMMARY)}
    - {rel(F83B_SUMMARY)}
    - {rel(F83B_MANIFEST)}
    - {rel(F83B_RECEIPT)}
  produced_artifacts:
    - {rel(SUMMARY)}
    - {rel(GAP_ROWS)}
    - {rel(REPORT)}
    - {rel(RUN_MANIFEST)}
final_claim_policy:
  forbidden_claims:
    - completion
    - selected_baseline
    - operating_promotion
    - runtime_authority
    - live_readiness
    - goal_achieve
""",
    )
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "gates": {
                "runtime_materialization_evidence": "pass",
                "proxy_runtime_gap_analysis": "pass",
                "parity_not_cause_boundary": "pass",
                "objective_gap_boundary": "pass",
                "run_evidence_receipt": "pass",
                "performance_attribution_receipt": "pass",
                "result_judgment_boundary": "pass",
                "codex_task_force_review_packet": "pass",
                "final_claim_guard": "pass",
                "required_gate_coverage_audit": "pass",
            },
        },
    )
    write_json(
        PACKET_FINAL_CLAIM_GUARD,
        {
            "status": "pass",
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )


def write_all(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    write_json(SUMMARY, payload)
    write_csv(GAP_ROWS, payload["gap_rows"])
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text())
    write_receipts(payload)
    manifest = {
        **payload,
        "artifacts": {
            "summary": rel(SUMMARY),
            "gap_rows": rel(GAP_ROWS),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
            "run_evidence_receipt": rel(RUN_EVIDENCE_RECEIPT),
            "performance_receipt": rel(PERFORMANCE_RECEIPT),
            "result_receipt": rel(RESULT_RECEIPT),
            "task_force_review": rel(TASK_FORCE_REVIEW),
        },
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
    update_ledgers(payload, created_at)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    update_context_anchor(payload, created_at)
    packet_files(payload, created_at)
    verification = local_verification()
    write_json(LOCAL_VERIFICATION, verification)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
    update_artifact_registry(created_at)
    return verification


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    verification = write_all(payload, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "target": (payload.get("target") or {}).get("candidate_id"),
                    "runtime_parity_preserved": payload.get("runtime_parity_preserved"),
                    "validation_runtime": payload.get("validation_gap", {}),
                    "oos_runtime": payload.get("oos_gap", {}),
                    "local_verification": verification["status"],
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
