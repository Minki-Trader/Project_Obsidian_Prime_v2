from __future__ import annotations

import csv
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import prepare_timestamp_context_onnx_runtime_probe_without_db as pkg  # noqa: E402
from stage_pipelines.stage364 import execute_timestamp_context_onnx_mt5_runtime_probe_without_db as probe  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364H"
RUN_ID = "run364H_review_timestamp_context_onnx_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = probe.RUN_ID
NEXT_RUN_ID = "run364I_design_runtime_failure_repair_offensive_queue_without_db_v1"

STATUS = "completed_stage364H_runtime_probe_reviewed_failure_memory_and_offensive_repair_queue_opened_no_authority"
JUDGMENT = "valid_negative_mt5_kpi_overlap_parity_positive_clue_sparse_runtime_tape_trade_shape_failure_no_authority"
DECISION = "stage364H_open_run364I_design_runtime_failure_repair_offensive_queue_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run364G"
PARENT_SUMMARY = PARENT_RUN_DIR / "timestamp_context_onnx_mt5_probe_summary.csv"
PARENT_EXECUTION = PARENT_RUN_DIR / "mt5_execution_result.json"
PARENT_REPORT_RECORDS = PARENT_RUN_DIR / "strategy_tester_report_records.json"
PARENT_DIFF = PARENT_RUN_DIR / "proxy_mt5_runtime_difference.csv"
PARENT_TELEMETRY = (
    PARENT_RUN_DIR
    / "runtime_telemetry"
    / "run364F_rf_depth3_balanced_density_3_0_keep_long_p3_telemetry.csv"
)
PARENT_RUNTIME_SUMMARY = (
    PARENT_RUN_DIR
    / "runtime_telemetry"
    / "run364F_rf_depth3_balanced_density_3_0_keep_long_p3_summary.csv"
)
PARENT_FINAL = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATES = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"

EXPECTED_TAPE = STAGE_DIR / "02_runs" / "run364F" / "expected_probability_tapes" / "timestamp_context_expected_probability_tape.csv"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
TRADE_ATTRIBUTION = RUN_DIR / "closed_trade_attribution.csv"
MONTHLY_ATTRIBUTION = RUN_DIR / "monthly_trade_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_trade_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_trade_attribution.csv"
SIGNAL_DENSITY_ATTRIBUTION = RUN_DIR / "signal_density_attribution.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_PROBE_QUEUE = RUN_DIR / "run364I_offensive_repair_design_queue.csv"
KPI_EVIDENCE_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364H_timestamp_context_onnx_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364H_timestamp_context_onnx_mt5_runtime_probe_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

OUTPUT_FILES = [
    INPUT_MANIFEST,
    TRADE_ATTRIBUTION,
    MONTHLY_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    SIGNAL_DENSITY_ATTRIBUTION,
    REVIEW_FINDINGS,
    FAILURE_MEMORY,
    NEXT_PROBE_QUEUE,
    KPI_EVIDENCE_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path | str) -> str:
    return pkg.tr.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha256_file(path)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.write_csv(path, rows)


def write_text(path: Path, text: str) -> None:
    pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows)


def append_registry_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_registry_rows(path, key_fields, rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    _, rows = pkg.tr.read_csv_rows(path)
    return rows


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR]:
        os.makedirs(io(path), exist_ok=True)


def validate_parent() -> dict[str, Any]:
    parent = read_json(PARENT_FINAL)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    gates = read_csv_rows(PARENT_GATES)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent run364G gates are not all passed")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent made forbidden runtime/goal claim")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    inputs = [
        PARENT_FINAL,
        PARENT_GATES,
        PARENT_SUMMARY,
        PARENT_EXECUTION,
        PARENT_REPORT_RECORDS,
        PARENT_DIFF,
        PARENT_TELEMETRY,
        PARENT_RUNTIME_SUMMARY,
        EXPECTED_TAPE,
    ]
    return [
        {
            "run_id": RUN_ID,
            "input_role": path.stem,
            "path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) else "",
            "effect": "review input(검토 입력)을 고정해 run364G 판독 재현성을 보존한다.",
        }
        for path in inputs
    ]


def parse_report_trades(report_path: Path) -> pd.DataFrame:
    tables = pd.read_html(io(report_path), encoding="utf-16")
    deals = tables[1].iloc[138:271].copy()
    deals.columns = [
        "time",
        "deal",
        "symbol",
        "type",
        "direction",
        "volume",
        "price",
        "order",
        "commission",
        "swap",
        "profit",
        "balance",
        "comment",
    ]
    deals = deals[deals["time"].notna()].copy()
    for column in ["profit", "commission", "swap", "balance", "price"]:
        deals[column] = pd.to_numeric(deals[column], errors="coerce")
    deals["dt"] = pd.to_datetime(deals["time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    closed: list[dict[str, Any]] = []
    last_in: pd.Series | None = None
    for _, row in deals.iterrows():
        direction = str(row.get("direction", "")).lower()
        if direction == "in":
            last_in = row
        elif direction == "out" and last_in is not None:
            hold_minutes = math.nan
            if pd.notna(last_in["dt"]) and pd.notna(row["dt"]):
                hold_minutes = (row["dt"] - last_in["dt"]).total_seconds() / 60.0
            closed.append(
                {
                    "trade_index": len(closed) + 1,
                    "entry_time": last_in["time"],
                    "exit_time": row["time"],
                    "entry_hour": int(last_in["dt"].hour) if pd.notna(last_in["dt"]) else "",
                    "exit_hour": int(row["dt"].hour) if pd.notna(row["dt"]) else "",
                    "entry_month": last_in["dt"].strftime("%Y-%m") if pd.notna(last_in["dt"]) else "",
                    "exit_month": row["dt"].strftime("%Y-%m") if pd.notna(row["dt"]) else "",
                    "hold_minutes": hold_minutes,
                    "hold_days": hold_minutes / 1440.0 if math.isfinite(hold_minutes) else "",
                    "entry_price": last_in["price"],
                    "exit_price": row["price"],
                    "profit_before_swap": row["profit"],
                    "swap": row["swap"],
                    "net_after_swap": float(row["profit"]) + float(row["swap"] or 0.0),
                    "comment": row["comment"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            last_in = None
    return pd.DataFrame(closed)


def aggregate_trades(closed: pd.DataFrame, group_column: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped = closed.groupby(group_column, dropna=False, observed=True)
    for key, frame in grouped:
        profit = frame["profit_before_swap"].astype(float)
        net = frame["net_after_swap"].astype(float)
        rows.append(
            {
                group_column: str(key),
                "trades": int(len(frame)),
                "gross_profit_before_swap": round(float(profit[profit > 0].sum()), 6),
                "gross_loss_before_swap": round(float(profit[profit < 0].sum()), 6),
                "net_before_swap": round(float(profit.sum()), 6),
                "swap": round(float(frame["swap"].astype(float).sum()), 6),
                "net_after_swap": round(float(net.sum()), 6),
                "avg_net_after_swap": round(float(net.mean()), 6),
                "wins": int((profit > 0).sum()),
                "losses": int((profit < 0).sum()),
                "max_win": round(float(profit.max()), 6),
                "max_loss": round(float(profit.min()), 6),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def hold_bucket_rows(closed: pd.DataFrame) -> list[dict[str, Any]]:
    frame = closed.copy()
    bins = [0, 30, 60, 120, 240, 480, 1440, 10080]
    labels = ["0_30m", "30_60m", "60_120m", "120_240m", "240_480m", "480_1440m", "1440_10080m"]
    frame["hold_bucket"] = pd.cut(frame["hold_minutes"], bins=bins, labels=labels, right=False)
    return aggregate_trades(frame, "hold_bucket")


def signal_density_rows(summary: Mapping[str, Any], runtime_summary: Mapping[str, Any], expected: pd.DataFrame) -> list[dict[str, Any]]:
    first = pd.to_datetime(summary["first_ready_bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    last = pd.to_datetime(summary["last_ready_bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    calendar_days = max(1.0, (last - first).days + 1 if pd.notna(first) and pd.notna(last) else 1.0)
    business_days = max(1, len(pd.bdate_range(first.normalize(), last.normalize())) if pd.notna(first) and pd.notna(last) else 1)
    expected["dt"] = pd.to_datetime(expected["bar_time_server"], errors="coerce")
    oos = expected[expected["split"].astype(str).eq("oos")]
    validation = expected[expected["split"].astype(str).eq("validation")]
    return [
        {
            "scope": "mt5_oos_overlap_runtime(표본외 겹친 런타임)",
            "first_ready_bar_time": summary["first_ready_bar_time"],
            "last_ready_bar_time": summary["last_ready_bar_time"],
            "calendar_days": calendar_days,
            "business_days": business_days,
            "ready_model_rows": int(summary["ready_model_rows"]),
            "long_signal_rows": int(runtime_summary["long_count"]),
            "filled_orders": int(runtime_summary["order_fill_count"]),
            "closed_trades": int(summary["trade_count"]),
            "ready_rows_per_business_day": round(float(summary["ready_model_rows"]) / business_days, 6),
            "long_signals_per_business_day": round(float(runtime_summary["long_count"]) / business_days, 6),
            "closed_trades_per_business_day": round(float(summary["trade_count"]) / business_days, 6),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scope": "expected_validation_unvisited(미방문 검증 예상)",
            "first_ready_bar_time": validation["bar_time_server"].min(),
            "last_ready_bar_time": validation["bar_time_server"].max(),
            "calendar_days": "",
            "business_days": "",
            "ready_model_rows": int(len(validation)),
            "long_signal_rows": int(validation["ea_expected_signal"].astype(str).str.lower().eq("long").sum()),
            "filled_orders": "",
            "closed_trades": "",
            "ready_rows_per_business_day": "",
            "long_signals_per_business_day": "",
            "closed_trades_per_business_day": "",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scope": "expected_oos_visited(방문 표본외 예상)",
            "first_ready_bar_time": oos["bar_time_server"].min(),
            "last_ready_bar_time": oos["bar_time_server"].max(),
            "calendar_days": "",
            "business_days": "",
            "ready_model_rows": int(len(oos)),
            "long_signal_rows": int(oos["ea_expected_signal"].astype(str).str.lower().eq("long").sum()),
            "filled_orders": int(runtime_summary["order_fill_count"]),
            "closed_trades": int(summary["trade_count"]),
            "ready_rows_per_business_day": "",
            "long_signals_per_business_day": "",
            "closed_trades_per_business_day": "",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def review_findings(summary: Mapping[str, Any], runtime_summary: Mapping[str, Any], closed: pd.DataFrame, signal_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    dense = next(row for row in signal_rows if row["scope"].startswith("mt5_oos"))
    long_short_balance = "long_only_no_short(롱 전용, 숏 없음)"
    worst_month = max(aggregate_trades(closed, "exit_month"), key=lambda row: abs(float(row["net_after_swap"])))
    losing_months = [row["exit_month"] for row in aggregate_trades(closed, "exit_month") if float(row["net_after_swap"]) < 0]
    return [
        {
            "finding_id": "RF-ST364H-01",
            "finding_type": "positive_clue(긍정 단서)",
            "subject": "ONNX/MT5 runtime parity(ONNX/MT5 런타임 동등성)",
            "evidence": f"matched_rows={summary['matched_rows']};mismatch_rows={summary['mismatch_rows']};max_abs_probability_diff={summary['max_abs_probability_diff']}",
            "judgment": "runtime_probe_parity_overlap_passed_no_authority(겹친 구간 런타임 탐침 동등성 통과, 권위 없음)",
            "effect": "model output handoff(모델 출력 인계)는 다음 탐색에서 재사용할 수 있다.",
        },
        {
            "finding_id": "RF-ST364H-02",
            "finding_type": "negative_memory(부정 기억)",
            "subject": "MT5 KPI(MT5 핵심 성과)",
            "evidence": f"net_profit={summary['net_profit']};profit_factor={summary['profit_factor']};expectancy={summary['expectancy']};recovery_factor={summary['recovery_factor']};max_drawdown={summary['max_drawdown_amount']}",
            "judgment": "valid_negative_runtime_probe(유효한 부정 런타임 탐침)",
            "effect": "운영 후보나 목표 달성으로 올리지 않는다.",
        },
        {
            "finding_id": "RF-ST364H-03",
            "finding_type": "failure_driver(실패 원인)",
            "subject": "sparse runtime tape trade shape(희소 런타임 테이프 거래 형태)",
            "evidence": f"ready_rows={summary['ready_model_rows']};closed_trades={summary['trade_count']};closed_trades_per_business_day={dense['closed_trades_per_business_day']};feature_skip_count={runtime_summary['feature_skip_count']}",
            "judgment": "trade_density_requirement_failed(거래 밀도 요구 실패)",
            "effect": "다음 탐색은 threshold-only(임계값 전용)가 아니라 dense source/runtime exit semantics(고밀도 원천/런타임 청산 의미)를 바꿔야 한다.",
        },
        {
            "finding_id": "RF-ST364H-04",
            "finding_type": "failure_driver(실패 원인)",
            "subject": "multi-day hold drawdown(수일 보유 낙폭)",
            "evidence": f"entry_hour_18_net={float(closed[closed['entry_hour']==18]['net_after_swap'].sum()):.2f};losing_months={','.join(losing_months)};worst_month={worst_month['exit_month']}:{worst_month['net_after_swap']}",
            "judgment": "hold_shape_and_month_regime_fragile(보유 형태와 월 국면 취약)",
            "effect": "entry-hour/session/regime veto(진입 시간/세션/국면 제외)는 회수 단서지만 밀도 회복과 함께 시험해야 한다.",
        },
        {
            "finding_id": "RF-ST364H-05",
            "finding_type": "evidence_boundary(근거 경계)",
            "subject": "validation rows unvisited(검증 행 미방문)",
            "evidence": f"expected_rows={summary['expected_rows']};visited_expected_rows={summary['visited_expected_rows']};unvisited_expected_rows={summary['unvisited_expected_rows']}",
            "judgment": "overlap_parity_only_not_full_window_authority(겹친 구간 동등성 전용, 전체 창 권위 아님)",
            "effect": "validation+OOS 전체 런타임 주장으로 확장하지 않는다.",
        },
    ]


def failure_memory_rows(summary: Mapping[str, Any], signal_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    dense = next(row for row in signal_rows if row["scope"].startswith("mt5_oos"))
    return [
        {
            "failure_id": "FM-ST364H-SPARSE-RUNTIME-TAPE-NEGATIVE-MT5-KPI",
            "source_run": PARENT_RUN_ID,
            "hypothesis": "timestamp context ONNX cost-filter(시점 문맥 ONNX 비용 필터)가 dense cost recovery(고밀도 비용 회복)를 MT5에서 유지한다.",
            "failed_boundary": "runtime_probe(런타임 탐침)",
            "why_failed": (
                f"MT5 net_profit={summary['net_profit']}, PF={summary['profit_factor']}, expectancy={summary['expectancy']}, "
                f"closed_trades_per_business_day={dense['closed_trades_per_business_day']}로 수익성과 밀도가 동시에 실패했다."
            ),
            "salvage_value": (
                f"proxy-MT5 parity(프록시-MT5 동등성)는 matched_rows={summary['matched_rows']} mismatch_rows={summary['mismatch_rows']}로 통과했다. "
                "따라서 ONNX handoff(ONNX 인계)는 재사용 가능하다."
            ),
            "do_not_repeat": "same sparse event tape(같은 희소 이벤트 테이프)에 threshold-only tightening(임계값 전용 조임)만 반복하지 않는다.",
            "reopen_condition": "dense M5 source(고밀도 M5 원천), calendar-time exit(캘린더 시간 청산), 또는 session/regime router(세션/국면 라우터)가 trade/day 3+와 MT5 net positive(MT5 순수익 양수)를 동시에 만들 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def next_probe_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run364I_Q01_dense_m5_source_runtime_rebuild",
            "idea_id": "IDEA-ST364H-DENSE-M5-SOURCE-RUNTIME-REPAIR",
            "hypothesis": "event-only sparse tape(이벤트 전용 희소 테이프)를 dense closed-M5 source(고밀도 닫힌 M5 원천)로 바꾸면 trade/day 3+와 runtime exit quality(런타임 청산 품질)를 회복할 수 있다.",
            "variant_family": "offensive_source_rebuild(공격 원천 재구축)",
            "broad_sweep": "dense all-M5 rows, cash-open rows, NY overlap rows(전체 M5/현금장/뉴욕 겹침 행)",
            "extreme_sweep": "all-long dense control, flat-every-non-signal control(전체 롱 고밀도 대조/비신호 전부 flat 대조)",
            "success_gate": "MT5 probe or proxy prefilter(프록시 선별)에서 trade/day>=3, net_profit>0, PF>1.05, drawdown not catastrophic(낙폭 파국 없음)",
            "effect": "trade splitting(거래 쪼개기) 없이 신호 원천 밀도를 회복하는지 본다.",
            "boundary": "design_queue_only(설계 대기열 전용)",
        },
        {
            "queue_id": "run364I_Q02_calendar_exit_semantics_probe",
            "idea_id": "IDEA-ST364H-CALENDAR-EXIT-SEMANTICS",
            "hypothesis": "MaxHoldBars(최대 보유 봉)가 sparse feature-ready cycle(희소 피처 준비 주기)로 세어져 수일 보유가 생겼으므로, calendar M5 exit(캘린더 M5 청산)나 dense flat tape(고밀도 flat 테이프)가 손실 꼬리를 줄인다.",
            "variant_family": "repair_control(수리 대조)",
            "broad_sweep": "max_hold M5 6/12/24/48 bars, close_on_flat true, entry_transition_only true(닫힌 M5 보유/flat 청산/전환 진입)",
            "extreme_sweep": "same-day force flat, no max hold(당일 강제 flat/최대 보유 없음)",
            "success_gate": "net drawdown reduction(순수익 낙폭 축소) without density collapse(밀도 붕괴 없음)",
            "effect": "runtime semantics(런타임 의미) 실패인지 model edge(모델 우위) 실패인지 분리한다.",
            "boundary": "design_queue_only(설계 대기열 전용)",
        },
        {
            "queue_id": "run364I_Q03_session_regime_loss_veto",
            "idea_id": "IDEA-ST364H-SESSION-REGIME-LOSS-VETO",
            "hypothesis": "entry_hour 16/18 and 2025-11/2026-02/2026-03 loss clusters(손실 군집)을 session/regime veto(세션/국면 제외)로 줄이면 회복 계수가 개선된다.",
            "variant_family": "offensive_rule_stack(공격 규칙 묶음)",
            "broad_sweep": "hour veto, month/regime veto, volatility crash veto(시간/월국면/변동성 급락 제외)",
            "extreme_sweep": "19-21 only, no-18-hour, no-bad-month replay(19-21 전용/18시 제외/나쁜 월 제외 재생)",
            "success_gate": "PF/recovery improve(수익 팩터/회복 개선) while trade/day remains >=3 after dense source repair(고밀도 원천 수리 후 일 3회 유지)",
            "effect": "밀도 없이 손실 월만 자르는 방어 미세조정을 피한다.",
            "boundary": "design_queue_only(설계 대기열 전용)",
        },
    ]


def materialize_review() -> dict[str, Any]:
    parent_summary = pd.read_csv(io(PARENT_SUMMARY)).fillna("").iloc[0].to_dict()
    parent_summary["mismatch_rows"] = int(parent_summary.get("expected_missing_rows", 0) or 0) + int(
        parent_summary.get("hash_mismatch_rows", 0) or 0
    ) + int(parent_summary.get("probability_mismatch_rows", 0) or 0) + int(parent_summary.get("decision_mismatch_rows", 0) or 0)
    runtime_summary = pd.read_csv(io(PARENT_RUNTIME_SUMMARY)).fillna("").iloc[-1].to_dict()
    expected = pd.read_csv(io(EXPECTED_TAPE)).fillna("")
    report_records = read_json(PARENT_REPORT_RECORDS)
    report_path = Path(report_records[0]["html_report"]["path"])
    closed = parse_report_trades(report_path)
    write_csv(TRADE_ATTRIBUTION, closed.to_dict(orient="records"))
    write_csv(MONTHLY_ATTRIBUTION, aggregate_trades(closed, "exit_month"))
    write_csv(ENTRY_HOUR_ATTRIBUTION, aggregate_trades(closed, "entry_hour"))
    write_csv(HOLD_BUCKET_ATTRIBUTION, hold_bucket_rows(closed))
    signal_rows = signal_density_rows(parent_summary, runtime_summary, expected)
    write_csv(SIGNAL_DENSITY_ATTRIBUTION, signal_rows)
    findings = review_findings(parent_summary, runtime_summary, closed, signal_rows)
    write_csv(REVIEW_FINDINGS, findings)
    failure_rows = failure_memory_rows(parent_summary, signal_rows)
    write_csv(FAILURE_MEMORY, failure_rows)
    queue = next_probe_rows()
    write_csv(NEXT_PROBE_QUEUE, queue)
    mt5_density = next(row for row in signal_rows if row["scope"].startswith("mt5_oos"))
    return {
        "parent_summary": parent_summary,
        "runtime_summary": runtime_summary,
        "closed_trades": int(len(closed)),
        "net_after_swap": round(float(closed["net_after_swap"].sum()), 6),
        "monthly_negative_count": int(sum(1 for row in aggregate_trades(closed, "exit_month") if float(row["net_after_swap"]) < 0)),
        "entry_hour_18_net": round(float(closed[closed["entry_hour"] == 18]["net_after_swap"].sum()), 6),
        "closed_trades_per_business_day": mt5_density["closed_trades_per_business_day"],
        "long_signals_per_business_day": mt5_density["long_signals_per_business_day"],
        "findings_count": len(findings),
        "failure_memory_count": len(failure_rows),
        "next_probe_queue_count": len(queue),
    }


def gate_row(gate_id: str, status: str, evidence_path: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": rel(evidence_path),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden = all(
        final.get(key) == "not_claimed"
        for key in ["forward_passed", "forward_failed", "goal_achieve", "runtime_authority", "operating_promotion"]
    )
    return [
        gate_row("parent_364G_gates_passed", "passed" if final["parent_gate_passed"] else "failed", PARENT_GATES, "run364G(364G 실행) gate(게이트)를 이어받는다."),
        gate_row("mt5_summary_available", "passed" if exists(PARENT_SUMMARY) and exists(PARENT_REPORT_RECORDS) else "failed", PARENT_SUMMARY, "MT5 KPI(MT5 핵심 성과 지표) 근거를 확인한다."),
        gate_row("trade_attribution_materialized", "passed" if exists(TRADE_ATTRIBUTION) and final["closed_trades"] > 0 else "failed", TRADE_ATTRIBUTION, "closed trade(종료 거래)를 분해한다."),
        gate_row("performance_attribution_written", "passed" if exists(MONTHLY_ATTRIBUTION) and exists(ENTRY_HOUR_ATTRIBUTION) else "failed", MONTHLY_ATTRIBUTION, "월/시간 성과 귀속을 남긴다."),
        gate_row("failure_memory_recorded", "passed" if exists(FAILURE_MEMORY) and final["failure_memory_count"] > 0 else "failed", FAILURE_MEMORY, "부정 결과를 재사용 가능한 실패 기억으로 남긴다."),
        gate_row("next_probe_design_queue_written", "passed" if exists(NEXT_PROBE_QUEUE) and final["next_probe_queue_count"] >= 3 else "failed", NEXT_PROBE_QUEUE, "다음 공격 탐색 씨앗을 만든다."),
        gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", FINAL_DECISION, "운영 승격/런타임 권위/목표 달성을 주장하지 않는다."),
        gate_row("required_gate_coverage_audit_written", "passed", GATE_AUDIT, "필수 게이트 커버리지를 남긴다."),
    ]


def write_final(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    parent = summary["parent_summary"]
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_gate_passed": True,
        "external_verification_status": "out_of_scope_by_claim_review_of_completed_mt5_probe(완료 MT5 탐침 검토라 새 외부 검증 범위 밖)",
        "result_subject": "run364G timestamp context ONNX MT5 runtime probe(364G 시점 문맥 ONNX MT5 런타임 탐침)",
        "net_profit": parent["net_profit"],
        "profit_factor": parent["profit_factor"],
        "trade_count": parent["trade_count"],
        "expectancy": parent["expectancy"],
        "recovery_factor": parent["recovery_factor"],
        "max_drawdown_amount": parent["max_drawdown_amount"],
        "matched_rows": parent["matched_rows"],
        "mismatch_rows": parent["mismatch_rows"],
        "unvisited_expected_rows": parent["unvisited_expected_rows"],
        "closed_trades": summary["closed_trades"],
        "net_after_swap": summary["net_after_swap"],
        "monthly_negative_count": summary["monthly_negative_count"],
        "entry_hour_18_net": summary["entry_hour_18_net"],
        "closed_trades_per_business_day": summary["closed_trades_per_business_day"],
        "long_signals_per_business_day": summary["long_signals_per_business_day"],
        "findings_count": summary["findings_count"],
        "failure_memory_count": summary["failure_memory_count"],
        "next_probe_queue_count": summary["next_probe_queue_count"],
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(row["path"]) if isinstance(row.get("path"), Path) else row["path"] for row in input_manifest_rows()],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        KPI_EVIDENCE_RECEIPT,
        {
            **base,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "kpi_contract_audit": rel(REVIEW_FINDINGS),
            "row_grain_audit": "run/subrun/view(실행/하위 실행/보기)는 Tier A/Tier B/Tier A+B로 registry(등록부)에 기록한다.",
            "source_authority_audit": rel(PARENT_SUMMARY),
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "Python proxy positive(파이썬 프록시 양수) to MT5 negative(MT5 음수)",
            "comparison_baseline": rel(PARENT_SUMMARY),
            "likely_drivers": ["sparse runtime tape(희소 런타임 테이프)", "multi-day hold(수일 보유)", "bad months 2025-11/2026-02/2026-03(나쁜 월)"],
            "segment_checks": [rel(MONTHLY_ATTRIBUTION), rel(ENTRY_HOUR_ATTRIBUTION), rel(HOLD_BUCKET_ATTRIBUTION), rel(SIGNAL_DENSITY_ATTRIBUTION)],
            "trade_shape": rel(TRADE_ATTRIBUTION),
            "attribution_confidence": "medium(중간)",
            "next_probe": rel(NEXT_PROBE_QUEUE),
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": final["result_subject"],
            "evidence_available": [rel(PARENT_SUMMARY), rel(PARENT_REPORT_RECORDS), rel(REVIEW_FINDINGS)],
            "evidence_missing": "full validation runtime pass(전체 검증 구간 런타임 통과)는 없음; 642 expected rows(예상 행) 미방문.",
            "judgment_label": "negative(부정) with positive parity clue(동등성 긍정 단서)",
            "next_condition": "dense M5 source(고밀도 M5 원천) 또는 runtime exit repair(런타임 청산 수리)가 MT5 net/PF/density를 동시에 회복해야 한다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(PARENT_FINAL), rel(PARENT_SUMMARY), rel(PARENT_REPORT_RECORDS), rel(PARENT_DIFF)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "mt5_execution": "not_run_review_of_parent(새 실행 없음, 부모 검토)",
            "forward_passed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run364H Timestamp Context ONNX MT5 Probe Review(364H 시점 문맥 ONNX MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- MT5 net_profit(MT5 순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- expectancy(기대값): `{final['expectancy']}`
- recovery_factor(회복 계수): `{final['recovery_factor']}`
- trade_count(거래수): `{final['trade_count']}`
- closed_trades_per_business_day(영업일당 종료 거래): `{final['closed_trades_per_business_day']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- unvisited_expected_rows(미방문 예상 행): `{final['unvisited_expected_rows']}`

## Judgment(판정)

Action(행동): run364G(364G 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI(핵심 성과), trade shape(거래 형태), runtime parity(런타임 동등성)로 분해했다.
Effect(효과): ONNX handoff(ONNX 인계)는 재사용 가능한 positive clue(긍정 단서)이지만, MT5 수익 구조와 거래 밀도는 valid negative(유효한 부정)로 닫는다.

## Attribution(귀속)

- parity(동등성): proxy-MT5 matched(프록시-MT5 일치) `{final['matched_rows']}`, mismatch(불일치) `{final['mismatch_rows']}`.
- failure driver(실패 원인): sparse runtime tape(희소 런타임 테이프)가 feature_skip_count(피처 스킵 수)를 크게 만들고, max-hold(최대 보유)가 feature-ready cycle(피처 준비 주기) 기준으로 수일 보유를 만들었다.
- trade density(거래 밀도): closed_trades_per_business_day(영업일당 종료 거래) `{final['closed_trades_per_business_day']}`로 목표 `3+`에 미달한다.
- loss cluster(손실 군집): entry_hour 18(18시 진입) net(순손익) `{final['entry_hour_18_net']}`, negative months(음수 월) `{final['monthly_negative_count']}`개.

## Evidence(근거)

- findings(검토 발견): `{rel(REVIEW_FINDINGS)}`
- monthly attribution(월별 귀속): `{rel(MONTHLY_ATTRIBUTION)}`
- entry-hour attribution(진입 시간 귀속): `{rel(ENTRY_HOUR_ATTRIBUTION)}`
- hold-bucket attribution(보유 구간 귀속): `{rel(HOLD_BUCKET_ATTRIBUTION)}`
- signal density(신호 밀도): `{rel(SIGNAL_DENSITY_ATTRIBUTION)}`
- failure memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- next design queue(다음 설계 대기열): `{rel(NEXT_PROBE_QUEUE)}`

## Next(다음)

`{NEXT_RUN_ID}`는 Stage364(364단계) 안에서 dense M5 source(고밀도 M5 원천), calendar exit semantics(캘린더 청산 의미), session/regime veto(세션/국면 제외)를 넓게 설계한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""# {TODAY} Stage364H Decision(364H 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(REVIEW_FINDINGS)}`, `{rel(FAILURE_MEMORY)}`, `{rel(NEXT_PROBE_QUEUE)}`

Action(행동): run364G MT5 runtime probe(MT5 런타임 탐침)를 negative memory(부정 기억)와 offensive repair queue(공격 수리 대기열)로 정리했다.
Effect(효과): 같은 sparse tape threshold-only search(희소 테이프 임계값 전용 탐색)를 반복하지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run364H(364H 실행)는 run364G(364G 실행)를 valid negative runtime probe(유효한 부정 런타임 탐침)로 검토했고, run364I(364I 실행)는 Stage364(364단계) 안에서 dense source/runtime exit repair(고밀도 원천/런타임 청산 수리)를 설계한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage364 Selection Status(364단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- mt5_runtime_probe(MT5 런타임 탐침): `valid_negative_with_overlap_parity_clue(겹친 구간 동등성 단서가 있는 유효 부정)`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- net_profit(순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- trade_count(거래수): `{final['trade_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 동등성 단서를 운영 승격으로 오해하지 않고, 다음 공격 탐색으로 넘긴다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection)
    write_text(WORKSPACE_STATE, workspace)
    marker = RUN_ID
    append_text_once(REVIEW_INDEX, marker, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - MT5 probe review(MT5 탐침 검토) and offensive repair queue(공격 수리 대기열).")
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run364H MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): sparse runtime tape(희소 런타임 테이프) 실패를 다음 dense source/runtime exit repair(고밀도 원천/런타임 청산 수리)로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run364H MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- findings(검토 발견): `{rel(REVIEW_FINDINGS)}`
- effect(효과): ONNX parity clue(ONNX 동등성 단서)는 보존하고, MT5 KPI negative(MT5 KPI 부정)는 실패 기억으로 남긴다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        marker,
        f"""## {TODAY} run364H Timestamp Context ONNX MT5 Probe Review(364H 시점 문맥 ONNX MT5 탐침 검토)

- action(행동): run364G MT5 runtime probe(MT5 런타임 탐침)를 성과 귀속과 실패 기억으로 검토했다.
- effect(효과): next_run(다음 실행) `{NEXT_RUN_ID}`가 sparse tape threshold-only search(희소 테이프 임계값 전용 탐색)를 반복하지 않게 한다.
- boundary(경계): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 주장하지 않는다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST364H-DENSE-M5-SOURCE-RUNTIME-REPAIR",
        f"""## IDEA-ST364H-DENSE-M5-SOURCE-RUNTIME-REPAIR

- idea(아이디어): sparse event tape(희소 이벤트 테이프)를 dense M5 source(고밀도 M5 원천)와 calendar exit semantics(캘린더 청산 의미)로 수리한다.
- hypothesis(가설): ONNX handoff(ONNX 인계)는 맞으므로 signal source density(신호 원천 밀도)와 runtime exit(런타임 청산)를 바꾸면 trade/day(일별 거래수) 3+와 MT5 net positive(MT5 순수익 양수)를 다시 시험할 수 있다.
- evidence(근거): `{rel(REVIEW_FINDINGS)}`, `{rel(FAILURE_MEMORY)}`.
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        "FM-ST364H-SPARSE-RUNTIME-TAPE-NEGATIVE-MT5-KPI",
        f"""## 2026-06-02 FM-ST364H-SPARSE-RUNTIME-TAPE-NEGATIVE-MT5-KPI

- source_run(원천 실행): `{PARENT_RUN_ID}`
- failure(실패): MT5 net_profit(순수익) `{final['net_profit']}`, PF(수익 팩터) `{final['profit_factor']}`, trade_count(거래수) `{final['trade_count']}`, closed_trades_per_business_day(영업일당 종료 거래) `{final['closed_trades_per_business_day']}`.
- salvage_value(회수 가치): proxy-MT5 parity(프록시-MT5 동등성)는 matched_rows(일치 행) `{final['matched_rows']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`로 좋다.
- do_not_repeat(반복 금지): 같은 sparse event tape(희소 이벤트 테이프)의 threshold-only search(임계값 전용 탐색)를 반복하지 않는다.
- reopen_condition(재개 조건): dense M5 source(고밀도 M5 원천), calendar exit semantics(캘린더 청산 의미), session/regime router(세션/국면 라우터)가 trade/day 3+와 MT5 순수익 양수를 동시에 만들 때.
- evidence(근거): `{rel(FAILURE_MEMORY)}`.
""",
    )


def write_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "kpi_evidence(KPI 근거)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": final["external_verification_status"],
        "notes": "run364H reviews run364G MT5 runtime probe(run364H가 run364G MT5 런타임 탐침을 검토).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(REVIEW_FINDINGS),
        "result_status": JUDGMENT,
        "work_family": "kpi_evidence(KPI 근거)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": now_utc(),
        "lane": "runtime_probe_review(런타임 탐침 검토)",
        "family": "kpi_evidence(KPI 근거)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Why did runtime parity pass but MT5 KPI fail?(런타임 동등성은 통과했는데 MT5 KPI는 왜 실패했는가?)",
        "net_profit": final["net_profit"],
        "profit_factor": final["profit_factor"],
        "trade_count": final["trade_count"],
        "expectancy": final["expectancy"],
        "recovery_factor": final["recovery_factor"],
        "max_drawdown_amount": final["max_drawdown_amount"],
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "runtime_completed_rows": 1,
    }
    run_row = dict(base)
    run_row["subrun_id"] = ""
    append_registry_rows(RUN_REGISTRY, ["run_id"], [run_row])
    tier_rows = []
    for suffix, view, tier, status, primary_kpi, guardrail in [
        (
            "Tier_A",
            "Tier A separate(Tier A 분리)",
            "Tier A",
            JUDGMENT,
            f"net={final['net_profit']};pf={final['profit_factor']};trades={final['trade_count']};matched={final['matched_rows']};mismatch={final['mismatch_rows']}",
            "runtime_authority=not_claimed;operating_promotion=not_claimed;goal=not_claimed",
        ),
        (
            "Tier_B",
            "Tier B separate(Tier B 분리)",
            "Tier B",
            "out_of_scope_by_claim",
            "tier_b_runtime_component=out_of_scope_by_claim",
            "no Tier B fallback used in run364G(run364G에서 Tier B 대체 사용 없음)",
        ),
        (
            "Tier_AplusB",
            "Tier A+B combined(Tier A+B 합산)",
            "Tier A+B",
            "actual_routed_total_same_as_tier_a_no_tier_b_fallback",
            f"actual_routed_total_net={final['net_profit']};pf={final['profit_factor']};trades={final['trade_count']}",
            "combined result is same routed account, not synthetic sum(합산은 합성 합계가 아니라 같은 라우팅 계좌)",
        ),
    ]:
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "view": view,
                "tier_scope": tier,
                "tier": tier,
                "kpi_scope": "runtime_probe_review(런타임 탐침 검토)",
                "metric_scope": "runtime_probe_review(런타임 탐침 검토)",
                "result_status": status,
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
            }
        )
        tier_rows.append(row)
    append_registry_rows(PROJECT_LEDGER, ["run_id", "subrun_id"], tier_rows)
    append_registry_rows(STAGE_LEDGER, ["run_id", "subrun_id"], tier_rows)


def write_artifact_registry() -> None:
    rows = []
    for path in OUTPUT_FILES:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "notes": "run364H review artifact(검토 산출물).",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "path"], rows)


def main() -> None:
    ensure_dirs()
    validate_parent()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    summary = materialize_review()
    seed = {
        **summary,
        "parent_gate_passed": True,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
    }
    gates = make_gates(seed)
    write_csv(GATE_AUDIT, gates)
    final = write_final(summary, gates)
    write_receipts(final)
    write_docs(final)
    write_registers(final)
    write_artifact_registry()
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final(summary, gates)
    failed = [row for row in gates if row["status"] != "passed"]
    if failed:
        raise RuntimeError(f"run364H gates failed: {failed}")
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
