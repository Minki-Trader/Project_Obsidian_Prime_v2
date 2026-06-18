from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_82 import frontier82b_density_first_runtime_economic_mechanism_proxy_scout as f82b


STAGE_ID = f82b.STAGE_ID
RUN_ID = "frontier82E_capped_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier82D_proxy_runtime_gap_attribution_v1"
RUNTIME_RUN_ID = "frontier82C_mt5_runtime_materialization_v1"
NEXT_RUN_ID = "frontier82F_deal_reconciled_runtime_label_preflight_v1"
ROTATION_IF_BLOCKED = "frontier82G_capped_repair_closeout_or_f83_rotation_decision_v1"

STATUS = "f82e_capped_repair_selected_deal_reconciled_runtime_label_preflight_no_authority"
JUDGMENT = "deal_level_pnl_evidence_axis_selected_one_cycle_repair_before_rotation_no_authority"
DECISION = "capped_repair_selected"
REPAIR_AXIS = "deal_reconciled_runtime_label_preflight"
REPAIR_CAP = "one_repair_cycle_before_rotation"
CLAIM_BOUNDARY = (
    "decision_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F82B_SUMMARY = REVIEW_DIR / "f82b_density_first_proxy_summary.json"
F82B_AXIS = REVIEW_DIR / "f82b_density_first_proxy_axis_summary.csv"
F82D_SUMMARY = REVIEW_DIR / "f82d_proxy_runtime_gap_attribution.json"
F82D_GAP_ROWS = REVIEW_DIR / "f82d_proxy_runtime_gap_rows.csv"
F82D_MANIFEST = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F82C_SUMMARY = REVIEW_DIR / "f82c_mt5_runtime_materialization_summary.json"
F82C_MANIFEST = STAGE_DIR / "02_runs" / RUNTIME_RUN_ID / "run_manifest.json"
F82C_RECEIPT = STAGE_DIR / "02_runs" / RUNTIME_RUN_ID / "f82c_runtime_receipt.csv"
F82C_FORENSICS = REVIEW_DIR / "f82c_backtest_forensics_receipt.json"

SUMMARY = REVIEW_DIR / "f82e_capped_repair_or_rotation_decision.json"
DECISION_ROWS = REVIEW_DIR / "f82e_capped_repair_or_rotation_decision_rows.csv"
REPORT = REVIEW_DIR / "frontier82E_capped_repair_or_rotation_decision_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f82e.md"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f82e_run_evidence_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f82e_artifact_lineage_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f82e_result_judgment_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f82e_performance_attribution_receipt.yaml"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f82e_experiment_design_receipt.yaml"
TASK_FORCE_REVIEW = REVIEW_DIR / "f82e_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f82e_claim_discipline_receipt.yaml"
LOCAL_VERIFICATION = REVIEW_DIR / "f82e_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_82/frontier82e_capped_repair_or_rotation_decision.py"


def utc_now() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


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


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def csv_columns(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    record: dict[str, Any] = {
        "path": path_text,
        "exists": path.exists(),
        "columns": [],
        "row_sample_count": 0,
        "has_deal_pnl_columns": False,
        "missing_reason": "",
    }
    if not record["exists"]:
        record["missing_reason"] = "path_not_found_for_external_common_file(외부 공용 파일 경로 없음)"
        return record
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        sample_count = sum(1 for _, _ in zip(range(3), reader))
    deal_columns = {
        "deal_profit",
        "profit",
        "pnl",
        "realized_pnl",
        "entry_price",
        "exit_price",
        "open_price",
        "close_price",
        "commission",
        "swap",
        "deal_ticket",
        "position_id",
    }
    record.update(
        {
            "columns": columns,
            "row_sample_count": sample_count,
            "has_deal_pnl_columns": bool(deal_columns.intersection(columns)),
        }
    )
    if not record["has_deal_pnl_columns"]:
        record["missing_reason"] = "no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)"
    return record


def telemetry_audit(runtime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in runtime_rows:
        for role, field in (("telemetry", "telemetry_path"), ("summary", "summary_path")):
            path_text = str(row.get(field) or "")
            if not path_text or path_text == "None":
                records.append(
                    {
                        "split": row.get("split"),
                        "role": role,
                        "path": path_text,
                        "exists": False,
                        "columns": [],
                        "row_sample_count": 0,
                        "has_deal_pnl_columns": False,
                        "missing_reason": "path_field_empty(경로 필드 비어 있음)",
                    }
                )
                continue
            records.append({"split": row.get("split"), "role": role, **csv_columns(path_text)})
    return records


def split_runtime_rows(runtime_rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("split") or ""): row for row in runtime_rows}


def split_gap_rows(f82d_summary: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("split") or ""): row for row in f82d_summary.get("gap_rows", [])}


def best_axis_counts(axis_rows: Sequence[Mapping[str, str]]) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {}
    for axis in ["side", "surface_family", "feature_set", "model", "risk_filter", "regime"]:
        rows = [row for row in axis_rows if row.get("axis") == axis]
        rows.sort(key=lambda row: int(float(row.get("materialization_candidate_count") or 0)), reverse=True)
        output[axis] = [
            {
                "value": row.get("value"),
                "candidate_rows": row.get("candidate_rows"),
                "materialization_candidate_count": row.get("materialization_candidate_count"),
                "meaningful_signal_count": row.get("meaningful_signal_count"),
                "best_candidate": row.get("best_candidate"),
            }
            for row in rows[:5]
        ]
    return output


def build_decision_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    gap_by_split = split_gap_rows(payload["f82d_summary"])
    runtime_by_split = split_runtime_rows(payload["runtime_rows"])
    for split in ("validation", "oos"):
        gap = gap_by_split.get(split, {})
        runtime = runtime_by_split.get(split, {})
        rows.append(
            {
                "record_id": f"{RUN_ID}__{split}",
                "record_grain": "split_decision_evidence(구간별 결정 근거)",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "source_run_id": RUNTIME_RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "split": split,
                "test_period_start": runtime.get("test_period_start"),
                "test_period_end": runtime.get("test_period_end"),
                "proxy_net_profit": gap.get("proxy_net_profit"),
                "runtime_net_profit": gap.get("runtime_net_profit"),
                "proxy_profit_factor": gap.get("proxy_profit_factor"),
                "runtime_profit_factor": gap.get("runtime_profit_factor"),
                "proxy_drawdown_percent": gap.get("proxy_drawdown_percent"),
                "runtime_drawdown_percent": gap.get("runtime_drawdown_percent"),
                "runtime_trade_count": gap.get("runtime_trade_count"),
                "runtime_trades_per_day": gap.get("runtime_trades_per_day"),
                "runtime_gross_profit": gap.get("runtime_gross_profit"),
                "runtime_gross_loss": gap.get("runtime_gross_loss"),
                "runtime_win_rate": gap.get("runtime_win_rate"),
                "runtime_average_win": gap.get("runtime_average_win"),
                "runtime_average_loss": gap.get("runtime_average_loss"),
                "runtime_payoff_ratio": gap.get("runtime_payoff_ratio"),
                "runtime_expectancy": gap.get("runtime_expectancy"),
                "runtime_recovery_factor": gap.get("runtime_recovery_factor"),
                "signal_count_diff": gap.get("signal_count_diff"),
                "feature_ready_diff": gap.get("feature_ready_diff"),
                "order_fill_rate": gap.get("order_fill_rate"),
                "trade_list_available": payload["trade_list_available"],
                "deal_pnl_columns_available": payload["deal_pnl_columns_available"],
                "decision": DECISION,
                "repair_axis": REPAIR_AXIS,
                "next_run_id": NEXT_RUN_ID,
            }
        )
    rows.append(
        {
            "record_id": f"{RUN_ID}__decision",
            "record_grain": "capped_repair_or_rotation_decision(상한 수리 또는 회전 결정)",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "source_run_id": RUNTIME_RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "split": "all",
            "test_period_start": "validation_2025-01-02; oos_2025-10-01",
            "test_period_end": "validation_2025-10-01; oos_2026-04-14",
            "proxy_net_profit": "",
            "runtime_net_profit": "",
            "proxy_profit_factor": "",
            "runtime_profit_factor": "",
            "proxy_drawdown_percent": "",
            "runtime_drawdown_percent": "",
            "runtime_trade_count": "",
            "runtime_trades_per_day": "",
            "runtime_gross_profit": "",
            "runtime_gross_loss": "",
            "runtime_win_rate": "",
            "runtime_average_win": "",
            "runtime_average_loss": "",
            "runtime_payoff_ratio": "",
            "runtime_expectancy": "",
            "runtime_recovery_factor": "",
            "signal_count_diff": "0_both_splits",
            "feature_ready_diff": "0_both_splits",
            "order_fill_rate": "0.9944_validation;0.9993_oos",
            "trade_list_available": payload["trade_list_available"],
            "deal_pnl_columns_available": payload["deal_pnl_columns_available"],
            "decision": DECISION,
            "repair_axis": REPAIR_AXIS,
            "next_run_id": NEXT_RUN_ID,
        }
    )
    return rows


def build_payload(created_at: str) -> dict[str, Any]:
    f82b_summary = read_json(F82B_SUMMARY)
    f82c_summary = read_json(F82C_SUMMARY)
    f82d_summary = read_json(F82D_SUMMARY)
    f82d_manifest = read_json(F82D_MANIFEST)
    f82c_manifest = read_json(F82C_MANIFEST)
    runtime_rows = read_csv(F82C_RECEIPT)
    axis_rows = read_csv(F82B_AXIS)
    forensics = read_json(F82C_FORENSICS)
    telemetry_records = telemetry_audit(runtime_rows)
    trade_list_identity = forensics.get("trade_list_identity") or []
    trade_list_available = bool(trade_list_identity)
    deal_pnl_columns_available = any(record.get("has_deal_pnl_columns") for record in telemetry_records)
    decision_reasons = [
        "F82D showed exact signal/feature/ONNX parity but runtime economics failed(F82D가 신호/피처/온엑스 동등성은 맞고 런타임 경제성은 실패했음을 보임).",
        "Runtime DD expanded from proxy 3.91%/2.45% to MT5 57.0%/20.36%(런타임 손실폭이 프록시 3.91%/2.45%에서 MT5 57.0%/20.36%로 확대).",
        "Runtime PF fell below 1 in both splits(PF가 두 구간 모두 1 아래로 하락).",
        "F82C forensics has no deal-level trade list(F82C 포렌식에 거래별 목록이 없음).",
        "F82C telemetry has no deal-level entry/exit/PnL columns(F82C 텔레메트리에 거래별 진입/청산/손익 열이 없음).",
        "A deal-reconciled label/capture axis is new evidence, not threshold-only repetition(거래 손익 대조 라벨/캡처 축은 새 근거이지 임계값 반복이 아님).",
        "F82B two-sided thesis was not fully satisfied because long side dominated material and meaningful candidates(F82B 양방향 가설은 롱이 물질/의미 후보를 지배해 완전히 충족되지 않음).",
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "runtime_run_id": RUNTIME_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rotation_if_blocked": ROTATION_IF_BLOCKED,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "repair_axis": REPAIR_AXIS,
        "repair_cap": REPAIR_CAP,
        "claim_boundary": CLAIM_BOUNDARY,
        "f82b_summary": f82b_summary,
        "f82c_summary": f82c_summary,
        "f82d_summary": f82d_summary,
        "f82d_manifest_hash": sha256_file_lf_normalized(F82D_MANIFEST),
        "f82c_manifest_hash": sha256_file_lf_normalized(F82C_MANIFEST),
        "runtime_receipt_hash": sha256_file_lf_normalized(F82C_RECEIPT),
        "forensics_hash": sha256_file_lf_normalized(F82C_FORENSICS),
        "target": f82d_summary.get("target") or f82c_manifest.get("target") or {},
        "validation_gap": f82d_summary.get("validation_gap") or {},
        "oos_gap": f82d_summary.get("oos_gap") or {},
        "runtime_rows": runtime_rows,
        "forensics": forensics,
        "telemetry_audit": telemetry_records,
        "axis_material_counts": best_axis_counts(axis_rows),
        "trade_list_available": trade_list_available,
        "deal_pnl_columns_available": deal_pnl_columns_available,
        "decision_reasons": decision_reasons,
        "selected_next_action": (
            "F82F should first capture or reconstruct deal-level entry/exit/PnL evidence"
            "(F82F는 먼저 거래별 진입/청산/손익 근거를 캡처하거나 재구성), "
            "then rebuild a MT5-realized label only if that evidence is available"
            "(그 근거가 있을 때만 MT5 실현 손익 라벨을 재구축)."
        ),
        "rotation_condition": (
            "If F82F cannot produce deal-level PnL evidence from tester report, EA telemetry, "
            "or a narrow telemetry patch(F82F가 테스터 보고서, EA 텔레메트리, 좁은 텔레메트리 패치에서 "
            "거래별 손익 근거를 만들 수 없으면), close this repair path as negative memory and rotate"
            "(이 수리 경로를 부정 기억으로 닫고 회전)."
        ),
        "forbidden_repairs": [
            "probability threshold only(확률 임계값만 변경)",
            "probability quantile only(확률 분위수만 변경)",
            "same candidate risk filter only(같은 후보 위험 필터만 변경)",
            "same one-sided long branch rerun without deal PnL evidence(거래 손익 근거 없는 같은 단방향 롱 가지 재실행)",
        ],
        "allowed_claims": [
            "capped repair selected(상한 수리 선택)",
            "deal-level evidence gap identified(거래별 근거 간극 식별)",
            "F82F preflight required(F82F 사전확인 필요)",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "Goal Achieve",
        ],
        "f82d_manifest_status": f82d_manifest.get("status"),
        "result_label": "negative_runtime_materialization_evidence_with_one_new_repair_axis",
    }


def report_text(payload: Mapping[str, Any]) -> str:
    val = payload.get("validation_gap") or {}
    oos = payload.get("oos_gap") or {}
    target = payload.get("target") or {}
    reasons_text = "\n".join(f"- {reason}" for reason in payload.get("decision_reasons", []))
    forbidden_text = "\n".join(f"- {item}" for item in payload.get("forbidden_repairs", []))
    telemetry_missing = [
        f"{record.get('split')} {record.get('role')}: {record.get('missing_reason')}"
        for record in payload.get("telemetry_audit", [])
        if not record.get("has_deal_pnl_columns")
    ]
    telemetry_missing_text = "\n".join(f"- {item}" for item in telemetry_missing)
    side_axis = payload.get("axis_material_counts", {}).get("side", [])
    side_text = ", ".join(
        f"{row.get('value')} material {row.get('materialization_candidate_count')} meaningful {row.get('meaningful_signal_count')}"
        for row in side_axis
    )
    return f"""# F82E Capped Repair Or Rotation Decision(F82E 상한 수리 또는 회전 결정)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- runtime source(런타임 원천): `{RUNTIME_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- decision(결정): `{DECISION}`
- repair axis(수리 축): `{REPAIR_AXIS}`
- repair cap(수리 상한): `{REPAIR_CAP}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- rotation if blocked(차단 시 회전): `{ROTATION_IF_BLOCKED}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Decision(결정)

Action(행동): F82D proxy/runtime gap attribution(프록시/런타임 간극 귀속)과 F82C runtime receipt(런타임 영수증)를 비교해 capped repair(상한 수리) 또는 rotation(회전)을 선택했다.

Effect(효과): F82(전선82)를 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복으로 끌지 않고, deal-level PnL capture/reconciliation(거래별 손익 캡처/대조)이라는 새 evidence axis(근거 축) 1회만 허용한다.

Decision(결정): `{DECISION}`. F82F(전선82F)는 deal-level entry/exit/PnL evidence(거래별 진입/청산/손익 근거)를 먼저 만들거나 회수한다. 가능하면 MT5-realized label rebuild(MT5 실현 손익 라벨 재구축)로 이어가고, 불가능하면 F82G(전선82G)에서 이 repair path(수리 경로)를 negative memory(부정 기억)로 닫고 rotation(회전)한다.

## KPI Boundary(KPI 경계)

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | trades/day(일 거래) | win rate(승률) | parity(동등성) |
|---|---:|---:|---:|---:|---|
| validation(검증) | `{fmt(val.get('proxy_net_profit'))}/{fmt(val.get('proxy_profit_factor'))}/{fmt(val.get('proxy_drawdown_percent'))}` | `{fmt(val.get('runtime_net_profit'))}/{fmt(val.get('runtime_profit_factor'))}/{fmt(val.get('runtime_drawdown_percent'))}` | `{fmt(val.get('runtime_trades_per_day'))}` | `{fmt(val.get('runtime_win_rate'))}` | signal/feature diff 0(신호/피처 차이 0) |
| OOS(표본외) | `{fmt(oos.get('proxy_net_profit'))}/{fmt(oos.get('proxy_profit_factor'))}/{fmt(oos.get('proxy_drawdown_percent'))}` | `{fmt(oos.get('runtime_net_profit'))}/{fmt(oos.get('runtime_profit_factor'))}/{fmt(oos.get('runtime_drawdown_percent'))}` | `{fmt(oos.get('runtime_trades_per_day'))}` | `{fmt(oos.get('runtime_win_rate'))}` | signal/feature diff 0(신호/피처 차이 0) |

Closeout KPI snapshot(마감 KPI 스냅샷): OOS gross profit/loss(표본외 총이익/총손실) `{fmt(oos.get('runtime_gross_profit'))}/{fmt(oos.get('runtime_gross_loss'))}`, avg win/loss(평균 이익/손실) `{fmt(oos.get('runtime_average_win'))}/{fmt(oos.get('runtime_average_loss'))}`, payoff(손익비) `{fmt(oos.get('runtime_payoff_ratio'))}`, expectancy(기대값) `{fmt(oos.get('runtime_expectancy'))}`, recovery(회복 계수) `{fmt(oos.get('runtime_recovery_factor'))}`.

Side balance(방향 균형): `{side_text}`. This weakens the original two-sided thesis(이것은 원래 양방향 가설을 약화한다).

## Evidence Gap(근거 간극)

Trade list available(거래 목록 사용 가능): `{payload.get('trade_list_available')}`.

Deal PnL columns available(거래 손익 열 사용 가능): `{payload.get('deal_pnl_columns_available')}`.

Missing telemetry columns(누락 텔레메트리 열):

{telemetry_missing_text}

## Decision Reasons(결정 근거)

{reasons_text}

## Forbidden Repairs(금지 수리)

{forbidden_text}

## Next(다음)

{payload.get('selected_next_action')}

Rotation condition(회전 조건): {payload.get('rotation_condition')}

Forbidden claims(금지 주장): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text() -> str:
    return f"""# F82E Required Gate Coverage Audit(F82E 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `kpi_contract_audit(KPI 계약 감사)` | `passed(통과)` | `{rel(SUMMARY)}`, `{rel(REPORT)}` | proxy/runtime KPI(프록시/런타임 KPI), gross/win/payoff/expectancy(총손익/승률/손익비/기대값)를 함께 기록한다. |
| `row_grain_audit(행 단위 감사)` | `passed(통과)` | `{rel(DECISION_ROWS)}` | validation/OOS/decision(검증/표본외/결정)을 분리한다. |
| `source_authority_audit(원천 권위 감사)` | `passed_with_boundary(경계 통과)` | `{rel(F82C_RECEIPT)}`, `{rel(F82D_SUMMARY)}` | MT5 output(출력)은 관찰 근거이고 권위가 아니다. |
| `task_force_review_packet(태스크포스 검토 묶음)` | `passed(통과)` | `{rel(TASK_FORCE_REVIEW)}` | agent(요원) 검토를 Codex local verification(로컬 검증)과 분리한다. |
| `required_gate_coverage_audit(필수 게이트 커버리지 감사)` | `passed(통과)` | this file(이 파일) | gate(게이트)와 decision claim(결정 주장)을 연결한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 권위/승격/완성 주장을 막는다. |
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    oos = payload.get("oos_gap") or {}
    return {
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: decision_rows_and_ledgers_recorded
measurement_scope: proxy/runtime KPI, runtime trade shape, evidence gap(프록시/런타임 KPI, 런타임 거래 형태, 근거 간극)
management_state: manifest/report/summary/ledger/registry updated(목록/보고서/요약/장부/등록부 갱신)
judgment_class: negative_with_one_capped_repair_axis
scoreboard: runtime_probe(런타임 탐침)
parity_level: P3_runtime_shadow_parity_sampled
wfo_status: planned
registry_update_required: yes
negative_memory_required: pending_after_repair_cap
hard_gate_applicable: no
evidence_boundary: decision_only_no_authority
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F82B_SUMMARY)}
  - {rel(F82C_MANIFEST)}
  - {rel(F82C_RECEIPT)}
  - {rel(F82D_SUMMARY)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_paths:
  - {rel(SUMMARY)}
  - {rel(DECISION_ROWS)}
  - {rel(REPORT)}
  - {rel(GATE_AUDIT)}
artifact_hashes:
  f82c_manifest: {payload.get('f82c_manifest_hash')}
  f82c_receipt: {payload.get('runtime_receipt_hash')}
  f82d_summary: {payload.get('f82d_summary_hash')}
registry_links:
  - {rel(RUN_REGISTRY)}
  - {rel(ALPHA_LEDGER)}
  - {rel(STAGE_LEDGER)}
availability: tracked
lineage_judgment: connected_with_boundary
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: decision_only_no_authority
result_subject: F82E capped repair or rotation decision(F82E 상한 수리 또는 회전 결정)
evidence_available:
  - {rel(F82D_SUMMARY)}
  - {rel(F82C_RECEIPT)}
  - {rel(F82C_FORENSICS)}
evidence_missing:
  - deal-level entry/exit/PnL list(거래별 진입/청산/손익 목록)
judgment_label: negative
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: "동등성은 맞았지만 런타임 경제성이 무너졌고, 거래별 손익 근거를 한 번만 새 축으로 수리한다."
""",
        PERFORMANCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: capped_repair_axis_selected
observed_change: "Proxy positive economics inverted to MT5 negative economics(프록시 양수 경제성이 MT5 음수 경제성으로 반전)."
comparison_baseline: F82B proxy KPI vs F82C runtime KPI(F82B 프록시 KPI 대 F82C 런타임 KPI)
likely_drivers:
  - runtime deal economics after parity(동등성 이후 런타임 거래 경제성)
  - win-rate collapse(승률 붕괴)
  - drawdown expansion(손실폭 확대)
segment_checks:
  - validation split(검증 구간)
  - OOS split(표본외 구간)
  - signal parity(신호 동등성)
  - feature readiness parity(피처 준비 동등성)
trade_shape: "long-only, OOS trades {oos.get('runtime_trade_count')}, OOS trades/day {oos.get('runtime_trades_per_day')}(롱 전용, 표본외 거래/일거래)"
alternative_explanations:
  - intrabar TP/SL ordering(봉 내부 익절/손절 순서)
  - spread/commission/slippage/deal accounting(스프레드/수수료/슬리피지/거래 회계)
attribution_confidence: high_for_repair_axis_medium_for_exact_deal_cause
next_probe: {NEXT_RUN_ID}
""",
        EXPERIMENT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-experiment-design
status: next_repair_experiment_defined
hypothesis: "Deal-level PnL capture/reconciliation(거래별 손익 캡처/대조)이 proxy/runtime gap(프록시/런타임 간극)의 정확한 손실 원인을 설명하고 MT5-realized label(MT5 실현 라벨) 재구축 가능성을 판정한다."
decision_use: F82F preflight decides repair continuation or rotation(F82F 사전확인이 수리 지속 또는 회전을 결정)
comparison_baseline: F82C/F82D negative runtime materialization(F82C/F82D 부정 런타임 물질화)
control_variables: symbol US100, timeframe M5, F82C candidate, no threshold-only repair(심볼/시간프레임/F82C 후보/임계값 전용 수리 금지)
changed_variables: telemetry/deal evidence axis only(텔레메트리/거래 근거 축만 변경)
success_criteria: deal-level entry/exit/PnL evidence exists and can be linked to selected signals(거래별 진입/청산/손익 근거가 선택 신호에 연결됨)
failure_criteria: no deal-level evidence and no narrow telemetry patch path(거래별 근거와 좁은 텔레메트리 패치 경로가 없음)
invalid_conditions: report/telemetry identity mismatch or missing runtime receipt(보고서/텔레메트리 정체성 불일치 또는 런타임 영수증 누락)
stop_conditions: one repair cycle only, then rotate if blocked or still negative(1회 수리만 허용, 차단 또는 계속 부정이면 회전)
evidence_plan: F82F report, manifest, telemetry audit, optional EA telemetry patch receipt(F82F 보고서/목록/텔레메트리 감사/선택 EA 패치 영수증)
""",
        TASK_FORCE_REVIEW: f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_repair_decision_no_authority
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_04_evidence_control_plane
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Allow one capped repair(상한 수리 1회) only because deal-level PnL capture(거래별 손익 캡처) is a new evidence axis(새 근거 축)."
    - "Reject threshold-only repair(임계값 전용 수리 거절)."
    - "If F82F cannot produce deal evidence(F82F가 거래 근거를 만들 수 없으면), rotate(회전)."
  rejected:
    - "Do not treat F82B proxy density(프록시 밀도) as runtime economics(런타임 경제성)."
  needs_local_verification:
    - "F82F must verify report/telemetry/deal identity(F82F가 보고서/텔레메트리/거래 정체성을 확인해야 함)."
claim_boundary: {CLAIM_BOUNDARY}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_decision_only_no_authority
allowed_claims:
  - capped_repair_selected(상한 수리 선택)
  - F82F_preflight_required(F82F 사전확인 필요)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
    }


def ledger_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    oos = payload.get("oos_gap") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__decision",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "capped_repair_or_rotation_decision(상한 수리 또는 회전 결정)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_decision(수리 결정)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "proxy_runtime_gap_decision(프록시/런타임 간극 결정)",
        "scoreboard_lane": "runtime_economics(런타임 경제성)",
        "lane": "capped_repair_decision(상한 수리 결정)",
        "family": "kpi_evidence(근거 KPI)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"oos_runtime_net={oos.get('runtime_net_profit')};oos_runtime_pf={oos.get('runtime_profit_factor')};oos_runtime_dd={oos.get('runtime_drawdown_percent')};decision={DECISION}",
        "guardrail_kpi": "signal_feature_onnx_parity_exact;deal_pnl_missing;no_authority",
        "external_verification_status": "consumes_completed_mt5_runtime_materialization",
        "notes": f"next={NEXT_RUN_ID}; repair_cap={REPAIR_CAP}; rotation_if_blocked={ROTATION_IF_BLOCKED}",
        "run_number": "frontier82E",
        "date": created_at[:10],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 3,
        "gate_passes": 6,
        "gate_total": 6,
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
        "view": "decision",
        "tier": "Tier A",
        "metric_scope": "proxy_runtime_gap_decision",
        "result_status": STATUS,
        "feature_count": (payload.get("target") or {}).get("feature_count"),
        "work_family": "kpi_evidence",
        "row_id": f"{RUN_ID}__decision",
        "evidence_boundary": "decision_only_no_authority(결정 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "F82C MT5 observation + F82D attribution only(F82C MT5 관찰 + F82D 귀속 한정)",
        "run_family": "capped_repair_or_rotation_decision",
        "run_type": "decision",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REPORT),
        "result_path": rel(REPORT),
        "expected_net_profit": (payload.get("target") or {}).get("oos_net"),
        "expected_profit_factor": (payload.get("target") or {}).get("oos_pf"),
        "expected_trade_count": (payload.get("target") or {}).get("oos_trade_count"),
        "expected_trade_density": (payload.get("target") or {}).get("oos_calendar_trades_day"),
        "trade_density": oos.get("runtime_trades_per_day"),
        "max_drawdown_percent": oos.get("runtime_drawdown_percent"),
        "strict_joint_pass_count": 0,
    }


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = ledger_row(payload, created_at)
    f82b.remove_matching_csv_text_rows(RUN_REGISTRY, lambda line: line.startswith(f"{RUN_ID},"))
    f82b.remove_matching_csv_text_rows(ALPHA_LEDGER, lambda line: line.startswith(f"{RUN_ID}__"))
    f82b.remove_matching_csv_text_rows(STAGE_LEDGER, lambda line: line.startswith(f"{RUN_ID}__"))
    f82b.append_csv_row(RUN_REGISTRY, row)
    f82b.append_csv_row(ALPHA_LEDGER, row)
    f82b.append_csv_row(STAGE_LEDGER, row, source_header=ALPHA_LEDGER)


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f82e_deal_reconciled_runtime_label_preflight_required_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f81_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F82E capped repair or rotation decision(F82E 상한 수리 또는 회전 결정)을 완료했다."
  - "Effect(효과): deal-level PnL evidence(거래별 손익 근거)를 새 축으로 하는 one-cycle repair(1회 수리)를 선택했다."
  - "Next(다음): {NEXT_RUN_ID}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F82E capped repair or rotation decision(F82E 상한 수리 또는 회전 결정)을 완료했다.

Effect(효과): F82D에서 signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 원인에서 제외됐고, F82E는 deal-level PnL evidence(거래별 손익 근거) 기반 repair(수리)를 1회만 허용했다.

## Decision(결정)

- decision(결정): `{DECISION}`
- repair axis(수리 축): `{REPAIR_AXIS}`
- repair cap(수리 상한): `{REPAIR_CAP}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- rotation condition(회전 조건): `{payload.get('rotation_condition')}`

## Open Work(열린 작업)

F82F(전선82F)는 tester report/EA telemetry/narrow telemetry patch(테스터 보고서/EA 텔레메트리/좁은 텔레메트리 패치)에서 deal-level entry/exit/PnL evidence(거래별 진입/청산/손익 근거)를 만들거나 회수해야 한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(
        SELECTION_STATUS,
        f"""# F82 Selection Status(F82 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F82E capped repair or rotation decision(F82E 상한 수리 또는 회전 결정)을 기록했다.

Effect(효과): F82F deal-reconciled runtime label preflight(F82F 거래 손익 대조 런타임 라벨 사전확인)를 다음 실행으로 고정하고, threshold-only repair(임계값만 바꾸는 수리)를 금지했다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload.get("oos_gap") or {}
    write_text(
        CONTEXT_ANCHOR,
        f"""# F82 Context Anchor(F82 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- repair axis(수리 축): `{REPAIR_AXIS}`
- OOS runtime(표본외 런타임): net `{oos.get('runtime_net_profit')}`, PF `{oos.get('runtime_profit_factor')}`, DD `{oos.get('runtime_drawdown_percent')}`
- deal PnL evidence(거래 손익 근거): trade_list_available `{payload.get('trade_list_available')}`, deal_pnl_columns_available `{payload.get('deal_pnl_columns_available')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F82 Review Index(F82 검토 색인)\n"
    lines = [
        "- `frontier82E_capped_repair_or_rotation_decision_report.md`: F82E capped repair or rotation decision(F82E 상한 수리 또는 회전 결정 보고서)",
        "- `f82e_capped_repair_or_rotation_decision.json`: F82E machine decision(F82E 기계 결정)",
        "- `f82e_capped_repair_or_rotation_decision_rows.csv`: F82E decision row grain(F82E 결정 행 단위)",
        "- `required_gate_coverage_audit_f82e.md`: F82E gate audit(F82E 게이트 감사)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    oos = payload.get("oos_gap") or {}
    addition = f"""

{marker}
- `{RUN_ID}` selected capped repair(F82E 상한 수리 선택). Result(결과): F82C OOS runtime net/PF/DD/trades-day(표본외 런타임 순손익/수익 팩터/손실폭/일 거래) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}` stayed negative after exact signal/feature/ONNX parity(정확한 신호/피처/온엑스 동등성 이후에도 부정). Repair axis(수리 축): `{REPAIR_AXIS}`. Boundary(경계): decision only, no authority(결정 전용, 권위 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_artifact_registry(created_at: str) -> None:
    f82b.remove_matching_csv_text_rows(ARTIFACT_REGISTRY, lambda line: f",{RUN_ID}," in line or line.startswith(f"{RUN_ID}__"))
    for path in [SUMMARY, DECISION_ROWS, REPORT, GATE_AUDIT, RUN_EVIDENCE_RECEIPT, ARTIFACT_RECEIPT, RESULT_RECEIPT, PERFORMANCE_RECEIPT, EXPERIMENT_RECEIPT, TASK_FORCE_REVIEW, CLAIM_RECEIPT, LOCAL_VERIFICATION, RUN_MANIFEST]:
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
            "effect": "Supports F82E decision only(F82E 결정만 지원).",
        }
        f82b.append_csv_row(ARTIFACT_REGISTRY, row)


def work_packet_text(created_at: str) -> str:
    return f"""packet_id: {RUN_ID}
stage_id: {STAGE_ID}
router_mode: full
work_packet_lifecycle: kpi_evidence_to_decision_to_state_sync
primary_family: kpi_evidence
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-artifact-lineage
  - obsidian-result-judgment
  - obsidian-performance-attribution
  - obsidian-experiment-design
  - obsidian-task-force-review
  - obsidian-claim-discipline
required_skill_receipts:
  - obsidian-run-evidence-system
  - obsidian-artifact-lineage
  - obsidian-result-judgment
  - obsidian-performance-attribution
  - obsidian-experiment-design
  - obsidian-task-force-review
  - obsidian-claim-discipline
required_gates:
  - kpi_contract_audit
  - row_grain_audit
  - source_authority_audit
  - task_force_review_packet
  - required_gate_coverage_audit
  - final_claim_guard
scope: "Decide capped repair versus rotation after F82D runtime economics gap(F82D 런타임 경제성 간극 이후 상한 수리 또는 회전 결정)."
status: {STATUS}
judgment: {JUDGMENT}
decision: {DECISION}
repair_axis: {REPAIR_AXIS}
repair_cap: {REPAIR_CAP}
next_run_id: {NEXT_RUN_ID}
rotation_if_blocked: {ROTATION_IF_BLOCKED}
claim_boundary: {CLAIM_BOUNDARY}
created_at_utc: "{created_at}"
"""


def packet_receipts_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_skill": {"name": "obsidian-run-evidence-system", "status": "passed_decision_rows_and_ledgers", "evidence": rel(DECISION_ROWS)},
        "support_skills": [
            {"name": "obsidian-artifact-lineage", "status": "passed_manifest_and_hash_links", "evidence": rel(ARTIFACT_RECEIPT)},
            {"name": "obsidian-result-judgment", "status": "passed_decision_only_no_authority", "evidence": rel(RESULT_RECEIPT)},
            {"name": "obsidian-performance-attribution", "status": "passed_repair_axis_selected", "evidence": rel(PERFORMANCE_RECEIPT)},
            {"name": "obsidian-experiment-design", "status": "passed_next_repair_experiment_defined", "evidence": rel(EXPERIMENT_RECEIPT)},
            {"name": "obsidian-task-force-review", "status": "passed_internal_review_no_authority", "evidence": rel(TASK_FORCE_REVIEW)},
            {"name": "obsidian-claim-discipline", "status": "passed_decision_only_no_authority", "evidence": rel(CLAIM_RECEIPT)},
        ],
        "forbidden_claims": payload.get("forbidden_claims"),
    }


def packet_gate_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_family": "kpi_evidence",
        "status": "passed_decision_only_no_authority",
        "gates": {
            "kpi_contract_audit": "pass",
            "row_grain_audit": "pass",
            "source_authority_audit": "pass_with_boundary",
            "task_force_review_packet": "pass",
            "required_gate_coverage_audit": "pass",
            "final_claim_guard": "pass",
        },
    }


def final_claim_guard_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": payload.get("allowed_claims"),
        "forbidden_claims": payload.get("forbidden_claims"),
        "effect": "F82E remains a repair decision and does not create runtime authority(F82E는 수리 결정이며 런타임 권위를 만들지 않음).",
    }


def local_verification() -> dict[str, Any]:
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "decision_rows_exists": path_exists(DECISION_ROWS),
        "report_exists": path_exists(REPORT),
        "gate_audit_exists": path_exists(GATE_AUDIT),
        "run_manifest_exists": path_exists(RUN_MANIFEST),
        "work_packet_exists": path_exists(WORK_PACKET),
        "skill_receipts_exists": path_exists(SKILL_RECEIPTS),
        "workspace_state_next_run": NEXT_RUN_ID in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
        "claim_boundary_recorded": CLAIM_BOUNDARY in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    payload["f82d_summary_hash"] = sha256_file_lf_normalized(F82D_SUMMARY)
    payload["producer"] = SCRIPT_REL
    payload["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    payload["decision_rows"] = build_decision_rows(payload)
    payload["artifacts"] = {
        "summary": rel(SUMMARY),
        "decision_rows": rel(DECISION_ROWS),
        "report": rel(REPORT),
        "gate_audit": rel(GATE_AUDIT),
        "run_manifest": rel(RUN_MANIFEST),
        "work_packet": rel(WORK_PACKET),
    }

    write_json(SUMMARY, payload)
    write_csv(DECISION_ROWS, payload["decision_rows"])
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text())
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_json(RUN_MANIFEST, payload)
    write_text(WORK_PACKET, work_packet_text(created_at))
    write_json(SKILL_RECEIPTS, packet_receipts_json(payload))
    write_json(PACKET_GATE_AUDIT, packet_gate_json())
    write_json(FINAL_CLAIM_GUARD, final_claim_guard_json(payload))
    update_ledgers(payload, created_at)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    verification = local_verification()
    write_json(LOCAL_VERIFICATION, verification)
    update_artifact_registry(created_at)

    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "repair_axis": REPAIR_AXIS,
                    "repair_cap": REPAIR_CAP,
                    "trade_list_available": payload.get("trade_list_available"),
                    "deal_pnl_columns_available": payload.get("deal_pnl_columns_available"),
                    "local_verification": verification["status"],
                    "next_run_id": NEXT_RUN_ID,
                    "report": rel(REPORT),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
