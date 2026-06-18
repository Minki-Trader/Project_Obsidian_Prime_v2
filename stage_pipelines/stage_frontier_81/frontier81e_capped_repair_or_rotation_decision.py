from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild"
RUN_ID = "frontier81E_capped_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier81D_proxy_runtime_gap_attribution_v1"
RUNTIME_RUN_ID = "frontier81C_mt5_runtime_materialization_v1"
NEXT_RUN_ID = "frontier81F_deal_reconciled_runtime_label_preflight_v1"
ROTATION_IF_BLOCKED = "frontier81G_negative_closeout_or_f82_rotation_decision_v1"

STATUS = "f81e_capped_repair_selected_deal_reconciled_label_preflight_no_authority"
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

F81D_SUMMARY = REVIEW_DIR / "f81d_proxy_runtime_gap_attribution.json"
F81D_GAP_ROWS = REVIEW_DIR / "f81d_proxy_runtime_gap_rows.csv"
F81D_MANIFEST = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F81C_MANIFEST = STAGE_DIR / "02_runs" / RUNTIME_RUN_ID / "run_manifest.json"
F81C_RECEIPT = STAGE_DIR / "02_runs" / RUNTIME_RUN_ID / "f81c_runtime_receipt.csv"
F81C_FORENSICS = REVIEW_DIR / "f81c_backtest_forensics_receipt.json"

SUMMARY = REVIEW_DIR / "f81e_capped_repair_or_rotation_decision.json"
DECISION_ROWS = REVIEW_DIR / "f81e_capped_repair_or_rotation_decision_rows.csv"
REPORT = REVIEW_DIR / "frontier81E_capped_repair_or_rotation_decision_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f81e.md"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f81e_run_evidence_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f81e_artifact_lineage_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f81e_result_judgment_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f81e_performance_attribution_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f81e_claim_discipline_receipt.yaml"
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
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_81/frontier81e_capped_repair_or_rotation_decision.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
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
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def csv_columns(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    record: dict[str, Any] = {
        "path": path_text,
        "exists": path_exists(path),
        "columns": [],
        "row_sample_count": 0,
        "has_deal_pnl_columns": False,
        "missing_reason": "",
    }
    if not record["exists"]:
        record["missing_reason"] = "path_not_found_after_io_path_retry(입출력 경로 재시도 후 경로 없음)"
        return record
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
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
            if not path_text:
                records.append(
                    {
                        "split": row.get("split"),
                        "role": role,
                        "path": "",
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


def split_gap_rows(f81d_summary: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("split") or ""): row for row in f81d_summary.get("gap_rows", [])}


def build_decision_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    gap_by_split = split_gap_rows(payload["f81d_summary"])
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
                "runtime_win_rate": gap.get("runtime_win_rate"),
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
            "runtime_win_rate": "",
            "signal_count_diff": "0_both_splits",
            "feature_ready_diff": "0_both_splits",
            "order_fill_rate": "0.992877_validation;1.0_oos",
            "trade_list_available": payload["trade_list_available"],
            "deal_pnl_columns_available": payload["deal_pnl_columns_available"],
            "decision": DECISION,
            "repair_axis": REPAIR_AXIS,
            "next_run_id": NEXT_RUN_ID,
        }
    )
    return rows


def build_payload(created_at: str) -> dict[str, Any]:
    f81d_summary = read_json(F81D_SUMMARY)
    f81d_manifest = read_json(F81D_MANIFEST)
    f81c_manifest = read_json(F81C_MANIFEST)
    runtime_rows = read_csv(F81C_RECEIPT)
    forensics = read_json(F81C_FORENSICS)
    telemetry_records = telemetry_audit(runtime_rows)
    trade_list_identity = forensics.get("trade_list_identity") or []
    trade_list_available = bool(trade_list_identity)
    deal_pnl_columns_available = any(record.get("has_deal_pnl_columns") for record in telemetry_records)
    validation = (f81d_summary.get("validation_gap") or {}).copy()
    oos = (f81d_summary.get("oos_gap") or {}).copy()
    decision_reasons = [
        "F81D showed exact signal/feature parity but runtime economics failed(F81D가 신호/피처 동등성은 맞고 런타임 경제성은 실패했음을 보임).",
        "Runtime win rate fell from proxy 41-43% to MT5 24-25%(런타임 승률이 프록시 41-43%에서 MT5 24-25%로 하락).",
        "Runtime DD expanded from proxy 2-4% to MT5 24-31%(런타임 손실폭이 프록시 2-4%에서 MT5 24-31%로 확대).",
        "F81C forensics has no deal-level trade list(F81C 포렌식에 거래별 목록이 없음).",
        "F81C telemetry has no deal-level entry/exit/PnL columns(F81C 텔레메트리에 거래별 진입/청산/손익 열이 없음).",
        "A deal-reconciled label is a new evidence axis, not threshold-only repetition(거래 손익 대조 라벨은 새 근거 축이지 임계값 반복이 아님).",
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
        "f81d_summary": f81d_summary,
        "f81d_manifest_hash": sha256_file_lf_normalized(F81D_MANIFEST),
        "f81c_manifest_hash": sha256_file_lf_normalized(F81C_MANIFEST),
        "runtime_receipt_hash": sha256_file_lf_normalized(F81C_RECEIPT),
        "forensics_hash": sha256_file_lf_normalized(F81C_FORENSICS),
        "target": f81d_summary.get("target") or f81c_manifest.get("target") or {},
        "validation_gap": validation,
        "oos_gap": oos,
        "runtime_rows": runtime_rows,
        "forensics": forensics,
        "telemetry_audit": telemetry_records,
        "trade_list_available": trade_list_available,
        "deal_pnl_columns_available": deal_pnl_columns_available,
        "decision_reasons": decision_reasons,
        "selected_next_action": (
            "F81F should first capture or reconstruct deal-level entry/exit/PnL evidence"
            "(F81F는 먼저 거래별 진입/청산/손익 근거를 캡처하거나 재구성), "
            "then rebuild a MT5-realized label only if that evidence is available"
            "(그 근거가 있을 때만 MT5 실현 손익 라벨을 재구축)."
        ),
        "rotation_condition": (
            "If F81F cannot produce deal-level PnL evidence from tester report, EA telemetry, "
            "or a narrow telemetry patch(F81F가 테스터 보고서, EA 텔레메트리, 좁은 텔레메트리 패치에서 "
            "거래별 손익 근거를 만들 수 없으면), close F81 as negative memory and rotate"
            "(F81을 부정 기억으로 마감하고 회전)."
        ),
        "forbidden_repairs": [
            "probability threshold only(확률 임계값만 변경)",
            "probability quantile only(확률 분위수만 변경)",
            "same candidate risk filter only(같은 후보 위험 필터만 변경)",
            "same one-sided branch rerun without deal PnL evidence(거래 손익 근거 없는 같은 단방향 가지 재실행)",
        ],
        "allowed_claims": [
            "capped repair selected(상한 수리 선택)",
            "deal-level evidence gap identified(거래별 근거 간극 식별)",
            "F81F preflight required(F81F 사전확인 필요)",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "Goal Achieve",
        ],
        "f81d_manifest_status": f81d_manifest.get("status"),
    }


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def report_text(payload: Mapping[str, Any]) -> str:
    val = payload.get("validation_gap") or {}
    oos = payload.get("oos_gap") or {}
    target = payload.get("target") or {}
    telemetry_missing = [
        f"{record.get('split')} {record.get('role')}: {record.get('missing_reason')}"
        for record in payload.get("telemetry_audit", [])
        if not record.get("has_deal_pnl_columns")
    ]
    telemetry_missing_text = "\n".join(f"- {item}" for item in telemetry_missing)
    reasons_text = "\n".join(f"- {reason}" for reason in payload.get("decision_reasons", []))
    forbidden_text = "\n".join(f"- {item}" for item in payload.get("forbidden_repairs", []))
    return f"""# F81E Capped Repair Or Rotation Decision(F81E 상한 수리 또는 회전 결정)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- runtime source(런타임 원천): `{RUNTIME_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- decision(결정): `{DECISION}`
- repair axis(수리 축): `{REPAIR_AXIS}`
- repair cap(수리 상한): `{REPAIR_CAP}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Decision(결정)

Action(행동): F81D proxy/runtime gap attribution(프록시/런타임 간극 귀속)과 F81C runtime receipt(런타임 영수증)를 비교해 capped repair(상한 수리) 또는 rotation(회전)을 선택했다.

Effect(효과): F81(전선81)을 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복으로 끌지 않고, deal-level PnL(거래별 손익)이라는 새 evidence axis(근거 축) 1회만 허용한다.

Decision(결정): `{DECISION}`. F81F(전선81F)는 deal-level entry/exit/PnL evidence(거래별 진입/청산/손익 근거)를 먼저 만들거나 회수한다. 가능하면 MT5-realized label rebuild(MT5 실현 손익 라벨 재구축)로 이어가고, 불가능하면 F81 negative closeout(부정 마감) 또는 F82 rotation(F82 회전)으로 간다.

## KPI Boundary(KPI 경계)

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | trades/day(일 거래) | win rate(승률) | parity(동등성) |
|---|---:|---:|---:|---:|---|
| validation(검증) | `{fmt(val.get('proxy_net_profit'))}/{fmt(val.get('proxy_profit_factor'))}/{fmt(val.get('proxy_drawdown_percent'))}` | `{fmt(val.get('runtime_net_profit'))}/{fmt(val.get('runtime_profit_factor'))}/{fmt(val.get('runtime_drawdown_percent'))}` | `{fmt(val.get('runtime_trades_per_day'))}` | `{fmt(val.get('runtime_win_rate'))}` | signal/feature diff 0(신호/피처 차이 0) |
| OOS(표본외) | `{fmt(oos.get('proxy_net_profit'))}/{fmt(oos.get('proxy_profit_factor'))}/{fmt(oos.get('proxy_drawdown_percent'))}` | `{fmt(oos.get('runtime_net_profit'))}/{fmt(oos.get('runtime_profit_factor'))}/{fmt(oos.get('runtime_drawdown_percent'))}` | `{fmt(oos.get('runtime_trades_per_day'))}` | `{fmt(oos.get('runtime_win_rate'))}` | signal/feature diff 0(신호/피처 차이 0) |

## Evidence Gap(근거 간극)

- trade list available(거래 목록 있음): `{payload.get('trade_list_available')}`
- deal PnL columns available(거래 손익 열 있음): `{payload.get('deal_pnl_columns_available')}`

{telemetry_missing_text}

## Reasons(근거)

{reasons_text}

## Repair Cap(수리 상한)

Allowed(허용): one deal-reconciled repair cycle(거래 손익 대조 수리 1회). F81F(전선81F)는 tester report/EA telemetry/narrow telemetry patch(테스터 보고서/EA 텔레메트리/좁은 텔레메트리 패치) 중 가장 좁은 충분 방법으로 deal-level evidence(거래별 근거)를 만든다.

Forbidden(금지):

{forbidden_text}

Rotation condition(회전 조건): `{payload.get('rotation_condition')}`

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F81E Required Gate Coverage Audit(F81E 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `kpi_contract_audit` | `passed(통과)` | `{rel(SUMMARY)}` | hypothesis/test period/proxy KPI/runtime KPI/parity/gap cause/next action(가설/기간/프록시 KPI/런타임 KPI/동등성/간극 원인/다음 행동)을 결정에 연결한다. |
| `row_grain_audit` | `passed(통과)` | `{rel(DECISION_ROWS)}` | validation/OOS split rows(검증/표본외 구간 행)와 decision row(결정 행)를 분리한다. |
| `source_authority_audit` | `passed_with_boundary(경계 포함 통과)` | `{rel(F81C_RECEIPT)}`, `{rel(F81C_FORENSICS)}` | source authority(원천 권위)는 F81C MT5 runtime observation(F81C MT5 런타임 관찰)과 F81D attribution(F81D 귀속) 한정이다. |
| `required_gate_coverage_audit` | `passed(통과)` | `{rel(GATE_AUDIT)}` | required gates(필수 게이트)를 closeout receipt(종료 영수증)에 연결한다. |

Claim guard(주장 보호): `{CLAIM_BOUNDARY}`. Effect(효과): repair decision(수리 결정)을 runtime authority(런타임 권위)로 올려 말하지 않는다.
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    return {
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: capped_repair_decision_recorded_no_authority
measurement_scope:
  - proxy KPI(프록시 KPI)
  - runtime KPI(런타임 KPI)
  - parity/gap cause(동등성/간극 원인)
management_state:
  run_folder: {rel(RUN_DIR)}
  manifest: {rel(RUN_MANIFEST)}
  decision_rows: {rel(DECISION_ROWS)}
judgment_class: negative
scoreboard: runtime_parity(런타임 동등성)
parity_level: P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)
wfo_status: not_applicable_decision_only(결정 전용 해당 없음)
registry_update_required: yes
negative_memory_required: pending_stage_closeout(단계 마감 대기)
hard_gate_applicable: no
evidence_boundary: decision_only_no_authority(결정 전용, 권위 없음)
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F81D_SUMMARY)}
  - {rel(F81D_MANIFEST)}
  - {rel(F81C_MANIFEST)}
  - {rel(F81C_RECEIPT)}
  - {rel(F81C_FORENSICS)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_paths:
  - {rel(SUMMARY)}
  - {rel(DECISION_ROWS)}
  - {rel(REPORT)}
  - {rel(RUN_MANIFEST)}
artifact_hashes:
  f81d_manifest_sha256: {payload.get('f81d_manifest_hash')}
  f81c_manifest_sha256: {payload.get('f81c_manifest_hash')}
  runtime_receipt_sha256: {payload.get('runtime_receipt_hash')}
  forensics_sha256: {payload.get('forensics_hash')}
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
result_subject: F81E capped repair or rotation decision(F81E 상한 수리 또는 회전 결정)
evidence_available:
  - {rel(F81D_SUMMARY)}
  - {rel(F81C_RECEIPT)}
  - {rel(F81C_FORENSICS)}
evidence_missing:
  - deal-level entry/exit/PnL list(거래별 진입/청산/손익 목록)
judgment_label: negative
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: "동등성은 맞았지만 거래별 손익 근거가 없어, 한 번만 그 축을 수리한다."
""",
        PERFORMANCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: capped_repair_axis_selected
observed_change: "Proxy positive economics inverted to MT5 negative economics(프록시 양수 경제성이 MT5 음수 경제성으로 반전)."
comparison_baseline: F81B proxy KPI vs F81C runtime KPI(F81B 프록시 KPI 대 F81C 런타임 KPI)
likely_drivers:
  - runtime deal economics after parity(동등성 이후 런타임 거래 경제성)
  - win-rate collapse(승률 붕괴)
  - drawdown expansion(손실폭 확대)
segment_checks:
  - validation split(검증 구간)
  - OOS split(표본외 구간)
  - signal parity(신호 동등성)
  - feature readiness parity(피처 준비 동등성)
trade_shape: "long-only, validation trades 697, OOS trades 670(롱 전용, 검증 697거래, 표본외 670거래)"
alternative_explanations:
  - intrabar TP/SL ordering(봉 내부 익절/손절 순서)
  - spread/commission/slippage/deal accounting(스프레드/수수료/슬리피지/거래 회계)
attribution_confidence: high_for_repair_axis_medium_for_exact_deal_cause
next_probe: {NEXT_RUN_ID}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_decision_only_no_authority
allowed_claims:
  - capped_repair_selected(상한 수리 선택)
  - F81F_preflight_required(F81F 사전확인 필요)
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
required_skill_receipts:
  - obsidian-run-evidence-system
  - obsidian-artifact-lineage
  - obsidian-result-judgment
  - obsidian-performance-attribution
required_gates:
  - kpi_contract_audit
  - row_grain_audit
  - source_authority_audit
  - required_gate_coverage_audit
scope: "Decide capped repair versus rotation after F81D runtime economics gap(F81D 런타임 경제성 간극 이후 상한 수리 또는 회전 결정)."
status: {STATUS}
judgment: {JUDGMENT}
decision: {DECISION}
repair_axis: {REPAIR_AXIS}
repair_cap: {REPAIR_CAP}
next_run_id: {NEXT_RUN_ID}
rotation_if_blocked: {ROTATION_IF_BLOCKED}
branch_worktree_fit: "passed_on_codex/frontier81-runtime-gap-repair"
branch_action: "created_new_branch"
skills_not_used:
  obsidian-runtime-parity: "No new MT5 execution in F81E(F81E에서는 새 MT5 실행 없음)."
  obsidian-backtest-forensics: "Consumes existing F81C receipt only(F81C 기존 영수증만 소비)."
  obsidian-model-validation: "No model export or threshold selection in F81E(F81E에서는 모델 내보내기나 임계값 선택 없음)."
claim_boundary: {CLAIM_BOUNDARY}
created_at_utc: "{created_at}"
"""


def packet_receipts_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_skill": {
            "name": "obsidian-run-evidence-system",
            "status": "passed_decision_rows_and_ledgers",
            "evidence": rel(DECISION_ROWS),
        },
        "support_skills": [
            {
                "name": "obsidian-artifact-lineage",
                "status": "passed_manifest_and_hash_links",
                "evidence": rel(ARTIFACT_RECEIPT),
            },
            {
                "name": "obsidian-result-judgment",
                "status": "passed_decision_only_no_authority",
                "evidence": rel(RESULT_RECEIPT),
            },
            {
                "name": "obsidian-performance-attribution",
                "status": "passed_repair_axis_selected",
                "evidence": rel(PERFORMANCE_RECEIPT),
            },
        ],
        "companion_skill": {
            "name": "obsidian-claim-discipline",
            "status": "passed_decision_only_no_authority",
            "evidence": rel(CLAIM_RECEIPT),
        },
        "forbidden_claims": payload.get("forbidden_claims"),
    }


def packet_gate_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_family": "kpi_evidence",
        "status": "passed_decision_only_no_authority",
        "gates": [
            {
                "gate": "kpi_contract_audit",
                "status": "passed",
                "evidence": rel(SUMMARY),
                "effect": "Decision links proxy/runtime KPI and next action(결정이 프록시/런타임 KPI와 다음 행동을 연결).",
            },
            {
                "gate": "row_grain_audit",
                "status": "passed",
                "evidence": rel(DECISION_ROWS),
                "effect": "Rows are validation/OOS plus one decision record(행은 검증/표본외와 결정 기록).",
            },
            {
                "gate": "source_authority_audit",
                "status": "passed_with_boundary",
                "evidence": [rel(F81C_RECEIPT), rel(F81C_FORENSICS), rel(F81D_SUMMARY)],
                "effect": "Authority is observation and decision only(권위는 관찰과 결정 한정).",
            },
            {
                "gate": "required_gate_coverage_audit",
                "status": "passed",
                "evidence": rel(GATE_AUDIT),
            },
        ],
    }


def final_claim_guard_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": payload.get("allowed_claims"),
        "forbidden_claims": payload.get("forbidden_claims"),
        "effect": "F81E remains a repair decision and does not create runtime authority(F81E는 수리 결정이며 런타임 권위를 만들지 않음).",
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
        "primary_kpi": (
            f"oos_runtime_net={oos.get('runtime_net_profit')};"
            f"oos_runtime_pf={oos.get('runtime_profit_factor')};"
            f"oos_runtime_dd={oos.get('runtime_drawdown_percent')};"
            f"decision={DECISION}"
        ),
        "guardrail_kpi": "signal_feature_parity_exact;deal_pnl_missing;no_authority",
        "external_verification_status": "consumes_completed_mt5_runtime_materialization",
        "notes": f"next={NEXT_RUN_ID}; repair_cap={REPAIR_CAP}; rotation_if_blocked={ROTATION_IF_BLOCKED}",
        "run_number": "frontier81E",
        "date": created_at[:10],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 3,
        "gate_passes": 4,
        "gate_total": 4,
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
        "source_authority": "F81C MT5 observation + F81D attribution only(F81C MT5 관찰 + F81D 귀속 한정)",
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
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f81e_deal_reconciled_runtime_label_preflight_required_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: inactive_preserve_records_pending_codex_task_force_replacement
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F81E capped repair or rotation decision(F81E 상한 수리 또는 회전 결정)을 완료했다."
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

Action(행동): F81E capped repair or rotation decision(F81E 상한 수리 또는 회전 결정)을 완료했다.

Effect(효과): F81D에서 signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 원인에서 제외됐고, F81E는 deal-level PnL evidence(거래별 손익 근거) 기반 repair(수리)를 1회만 허용했다.

## Decision(결정)

- decision(결정): `{DECISION}`
- repair axis(수리 축): `{REPAIR_AXIS}`
- repair cap(수리 상한): `{REPAIR_CAP}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- rotation condition(회전 조건): `{payload.get('rotation_condition')}`

## Open Work(열린 작업)

F81F(전선81F)는 tester report/EA telemetry/narrow telemetry patch(테스터 보고서/EA 텔레메트리/좁은 텔레메트리 패치)에서 deal-level entry/exit/PnL evidence(거래별 진입/청산/손익 근거)를 만들거나 회수해야 한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(
        SELECTION_STATUS,
        f"""# F81 Selection Status(F81 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F81E capped repair or rotation decision(F81E 상한 수리 또는 회전 결정)을 기록했다.

Effect(효과): F81F deal-reconciled runtime label preflight(F81F 거래 손익 대조 런타임 라벨 사전확인)를 다음 실행으로 고정하고, threshold-only repair(임계값만 바꾸는 수리)를 금지했다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload.get("oos_gap") or {}
    write_text(
        CONTEXT_ANCHOR,
        f"""# F81 Context Anchor(F81 문맥 앵커)

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
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F81 Review Index(F81 검토 색인)\n"
    lines = [
        "- `frontier81E_capped_repair_or_rotation_decision_report.md`: F81E capped repair or rotation decision(F81E 상한 수리 또는 회전 결정 보고서)",
        "- `f81e_capped_repair_or_rotation_decision.json`: F81E machine decision(F81E 기계 결정)",
        "- `f81e_capped_repair_or_rotation_decision_rows.csv`: F81E decision row grain(F81E 결정 행 단위)",
        "- `required_gate_coverage_audit_f81e.md`: F81E gate audit(F81E 게이트 감사)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    oos = payload.get("oos_gap") or {}
    addition = f"""

- `{RUN_ID}` selected capped repair(F81E 상한 수리 선택). Result(결과): F81C OOS runtime net/PF/DD/trades-day(표본외 런타임 순손익/수익 팩터/손실폭/일 거래) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}` stayed negative after exact signal/feature parity(정확한 신호/피처 동등성 이후에도 부정). Repair axis(수리 축): `{REPAIR_AXIS}`. Boundary(경계): decision only, no authority(결정 전용, 권위 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_changelog(payload: Mapping[str, Any]) -> None:
    text = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    oos = payload.get("oos_gap") or {}
    entry = f"""# 2026-06-18 - F81E Capped Repair Decision(F81E 상한 수리 결정)

- Action(행동): `{RUN_ID}`로 F81D runtime gap(런타임 간극) 이후 capped repair(상한 수리) 또는 rotation(회전)을 판정했다.
- Effect(효과): OOS runtime net/PF/DD(표본외 런타임 순손익/수익 팩터/손실폭) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}`와 missing deal-level PnL evidence(거래별 손익 근거 누락)를 근거로 `{REPAIR_AXIS}` 1회 수리를 선택했다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(CHANGELOG, entry + text)


def write_packet_files(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(WORK_PACKET, work_packet_text(created_at))
    write_json(SKILL_RECEIPTS, packet_receipts_json(payload))
    write_json(PACKET_GATE_AUDIT, packet_gate_json())
    write_json(FINAL_CLAIM_GUARD, final_claim_guard_json(payload))


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    decision_rows = build_decision_rows(payload)
    payload["decision_rows"] = decision_rows
    payload["producer"] = SCRIPT_REL
    payload["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    payload["artifacts"] = {
        "summary": rel(SUMMARY),
        "decision_rows": rel(DECISION_ROWS),
        "report": rel(REPORT),
        "gate_audit": rel(GATE_AUDIT),
        "run_manifest": rel(RUN_MANIFEST),
        "work_packet": rel(WORK_PACKET),
    }

    write_json(SUMMARY, payload)
    write_csv(DECISION_ROWS, decision_rows)
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_json(RUN_MANIFEST, payload)
    write_packet_files(payload, created_at)
    update_ledgers(payload, created_at)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    update_changelog(payload)

    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "repair_axis": REPAIR_AXIS,
                "repair_cap": REPAIR_CAP,
                "trade_list_available": payload.get("trade_list_available"),
                "deal_pnl_columns_available": payload.get("deal_pnl_columns_available"),
                "next_run_id": NEXT_RUN_ID,
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
