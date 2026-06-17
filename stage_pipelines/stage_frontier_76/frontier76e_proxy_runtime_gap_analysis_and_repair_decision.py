from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from stage_pipelines.stage_frontier_76 import frontier76b_axis_ablation_proxy_scout as f76b


STAGE_ID = f76b.STAGE_ID
RUN_ID = "frontier76E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = "frontier76D_mt5_axis_ablation_runtime_probe_v1"
NEXT_RUN_ID = "frontier76F_lifecycle_aware_density_repair_proxy_v1"
STATUS = "gap_analysis_completed_lifecycle_repair_proxy_required_no_authority"
JUDGMENT = "runtime_probe_gap_traced_to_same_direction_hold_compression_no_authority"
CLAIM_BOUNDARY = (
    "gap_analysis_and_repair_decision_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
F76D_RECEIPT = REVIEW_DIR / "f76d_runtime_receipt.csv"
F76D_SUMMARY = REVIEW_DIR / "f76d_summary.json"
GAP_ROWS_PATH = REVIEW_DIR / "f76e_proxy_runtime_gap_rows.csv"
SUMMARY_PATH = REVIEW_DIR / "f76e_gap_analysis_summary.json"
REPORT_PATH = REVIEW_DIR / "frontier76E_proxy_runtime_gap_analysis_and_repair_decision_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f76e.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if not rows:
        io_path(path).write_text("", encoding="utf-8-sig")
        return
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def telemetry_gap_counts(telemetry_path: str) -> dict[str, Any]:
    path = Path(telemetry_path)
    if not path.exists():
        return {
            "telemetry_exists": False,
            "cycle_rows": 0,
            "long_decision_count": 0,
            "long_order_attempted_count": 0,
            "hold_same_direction_count": 0,
            "hold_existing_count": 0,
            "open_long_count": 0,
            "close_max_hold_count": 0,
        }
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get("record_type") == "cycle"]
    exec_counts = Counter(row.get("exec_action", "") for row in rows)
    long_rows = [row for row in rows if row.get("decision") == "long"]
    long_attempted = [row for row in long_rows if row.get("order_attempted") == "true"]
    return {
        "telemetry_exists": True,
        "cycle_rows": len(rows),
        "long_decision_count": len(long_rows),
        "long_order_attempted_count": len(long_attempted),
        "hold_same_direction_count": exec_counts.get("hold_same_direction", 0),
        "hold_existing_count": exec_counts.get("hold_existing", 0),
        "open_long_count": exec_counts.get("open_long", 0),
        "close_max_hold_count": exec_counts.get("close_max_hold", 0),
    }


def build_gap_rows() -> list[dict[str, Any]]:
    rows = []
    for receipt in read_csv(F76D_RECEIPT):
        telemetry = telemetry_gap_counts(receipt.get("telemetry_path", ""))
        signal_count = as_int(receipt.get("signal_count"))
        order_attempt_count = as_int(receipt.get("order_attempt_count"))
        trade_count = as_int(receipt.get("trade_count"))
        proxy_tpd = as_float(receipt.get("proxy_trades_per_day"))
        runtime_tpd = as_float(receipt.get("trades_per_day"))
        proxy_pf = as_float(receipt.get("proxy_profit_factor"))
        runtime_pf = as_float(receipt.get("profit_factor"))
        proxy_dd = as_float(receipt.get("proxy_dd_percent"))
        runtime_dd = as_float(receipt.get("max_drawdown_percent"))
        row = {
            "split": receipt.get("split", ""),
            "period": f"{receipt.get('test_period_start', '')}..{receipt.get('test_period_end', '')}",
            "proxy_signal_count": signal_count,
            "runtime_signal_count": as_int(receipt.get("signal_count")),
            "order_attempt_count": order_attempt_count,
            "round_trip_trade_count": trade_count,
            "signal_to_order_ratio": order_attempt_count / signal_count if signal_count else 0.0,
            "signal_to_round_trip_ratio": trade_count / signal_count if signal_count else 0.0,
            "proxy_trades_per_day": proxy_tpd,
            "runtime_trades_per_day": runtime_tpd,
            "trades_per_day_delta": runtime_tpd - proxy_tpd,
            "proxy_profit_factor": proxy_pf,
            "runtime_profit_factor": runtime_pf,
            "profit_factor_delta": runtime_pf - proxy_pf,
            "proxy_dd_percent": proxy_dd,
            "runtime_dd_percent": runtime_dd,
            "drawdown_delta": runtime_dd - proxy_dd,
            "hold_same_direction_count": telemetry["hold_same_direction_count"],
            "hold_same_direction_share_of_signals": telemetry["hold_same_direction_count"] / signal_count if signal_count else 0.0,
            "hold_existing_count": telemetry["hold_existing_count"],
            "open_long_count": telemetry["open_long_count"],
            "close_max_hold_count": telemetry["close_max_hold_count"],
            "telemetry_exists": telemetry["telemetry_exists"],
            "primary_gap_cause": "same_direction_hold_compression_after_signal_parity",
        }
        rows.append(row)
    return rows


def build_summary(gap_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    worst_tpd_gap = min((as_float(row.get("trades_per_day_delta")) for row in gap_rows), default=0.0)
    max_hold_share = max((as_float(row.get("hold_same_direction_share_of_signals")) for row in gap_rows), default=0.0)
    max_runtime_dd = max((as_float(row.get("runtime_dd_percent")) for row in gap_rows), default=0.0)
    min_runtime_pf = min((as_float(row.get("runtime_profit_factor")) for row in gap_rows), default=0.0)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "gap_rows": len(gap_rows),
        "primary_gap_cause": "same_direction_hold_compression_after_signal_parity",
        "worst_trades_per_day_delta": worst_tpd_gap,
        "max_hold_same_direction_share": max_hold_share,
        "max_runtime_dd_percent": max_runtime_dd,
        "min_runtime_profit_factor": min_runtime_pf,
        "repair_decision": "frontier76F_lifecycle_aware_density_repair_proxy",
        "repair_axes": [
            "trade_shape_lifecycle_proxy_single_position_max_hold12",
            "session_threshold_recombination_for_density",
            "feature_target_model_axis_reuse_from_f76b_without_runtime_authority",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_text(created_at: str, gap_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> str:
    lines = [
        "# Frontier76E Proxy/Runtime Gap Analysis and Repair Decision(F76E 프록시/런타임 간극 분석 및 수리 결정)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- primary gap cause(주 간극 원인): `{summary['primary_gap_cause']}`",
        f"- next action(다음 행동): `{NEXT_RUN_ID}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Gap Rows(간극 행)",
        "",
        "| split(분할) | signal(신호) | orders(주문) | trades(거래) | order/signal(주문/신호) | hold_same_direction(동방향 보유) | proxy tpd(프록시 일거래) | runtime tpd(런타임 일거래) | proxy PF(프록시 수익 팩터) | runtime PF(런타임 수익 팩터) | proxy DD%(프록시 손실폭) | runtime DD%(런타임 손실폭) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in gap_rows:
        lines.append(
            "| `{split}` | `{signal}` | `{orders}` | `{trades}` | `{ratio:.4f}` | `{hold}` | `{proxy_tpd}` | `{runtime_tpd}` | `{proxy_pf}` | `{runtime_pf}` | `{proxy_dd}` | `{runtime_dd}` |".format(
                split=row.get("split", ""),
                signal=row.get("proxy_signal_count", ""),
                orders=row.get("order_attempt_count", ""),
                trades=row.get("round_trip_trade_count", ""),
                ratio=as_float(row.get("signal_to_order_ratio")),
                hold=row.get("hold_same_direction_count", ""),
                proxy_tpd=row.get("proxy_trades_per_day", ""),
                runtime_tpd=row.get("runtime_trades_per_day", ""),
                proxy_pf=row.get("proxy_profit_factor", ""),
                runtime_pf=row.get("runtime_profit_factor", ""),
                proxy_dd=row.get("proxy_dd_percent", ""),
                runtime_dd=row.get("runtime_dd_percent", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Repair Decision(수리 결정)",
            "",
            "Action(행동): F76F에서 lifecycle-aware proxy(생명주기 인식 프록시)를 새로 실행한다.",
            "",
            "Effect(효과): 독립 신호마다 거래로 계산하던 F76B proxy(프록시)를 런타임처럼 single-position max-hold12(단일 포지션 12봉 최대 보유) 구조로 다시 점수화한다.",
            "",
            "Repair axes(수리 축):",
            "",
            "- feature set/model/target(피처 묶음/모델/목표)은 F76B 축을 재사용한다.",
            "- session/threshold(세션/임계값)는 density(거래 밀도)를 위해 다시 넓힌다.",
            "- runtime claim(런타임 주장)은 만들지 않고, 의미 신호가 생기면 Grok review(Grok 검토) 뒤 MT5 Runtime Probe(MT5 런타임 탐침)로 보낸다.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(created_at: str, summary: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit F76E(F76E 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F76D runtime evidence(F76D 런타임 근거) | `passed(통과)` | `{rel(F76D_RECEIPT)}` |
| telemetry gap analysis(텔레메트리 간극 분석) | `passed(통과)` | hold_same_direction share max `{summary['max_hold_same_direction_share']}` |
| repair decision(수리 결정) | `passed(통과)` | `{NEXT_RUN_ID}` |
| final_claim_guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def ledger_row(created_at: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    row_id = f"{RUN_ID}::gap_analysis::tier_a"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_runtime_gap_analysis",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"primary_gap={summary['primary_gap_cause']};next={NEXT_RUN_ID}",
        "family": "runtime_gap_repair_decision",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier76E",
        "date": created_at[:10],
        "decision": "lifecycle_aware_repair_proxy_required_no_authority",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "external_verification_status": "completed_from_f76d_runtime_probe(F76D 런타임 탐침 기반 완료)",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "proxy_runtime_gap_analysis(프록시/런타임 간극 분석)",
        "record_view": "gap_analysis_and_repair_decision(간극 분석 및 수리 결정)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "runtime_probe_gap_kpi(런타임 탐침 간극 KPI)",
        "primary_kpi": f"max_hold_same_direction_share={summary['max_hold_same_direction_share']}",
        "guardrail_kpi": "no authority;repair proxy next",
        "work_family": "runtime_gap_analysis_and_repair",
        "row_id": row_id,
        "evidence_boundary": "runtime_probe_observation_gap_analysis_only",
        "next_action": NEXT_RUN_ID,
        "artifact_count": "4",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_gap_analysis_and_repair",
        "run_type": "gap_analysis",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }


def update_state_and_ledgers(created_at: str, summary: Mapping[str, Any]) -> None:
    row = ledger_row(created_at, summary)
    f76b.upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    f76b.upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    f76b.upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row)

    idea_path = ROOT / "docs/registers/idea_registry.md"
    marker = "<!-- frontier76E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->"
    text = io_path(idea_path).read_text(encoding="utf-8-sig")
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` traced F76D proxy/runtime gap(프록시/런타임 간극) to same-direction hold compression(동방향 보유 압축). Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
        write_text(idea_path, text.rstrip() + addition)

    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f76_mandatory_runtime_probe_attempted_gap_analysis_completed
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_frontier71_to_75_retrospective_completed
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F76E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 기록했다."
  - "Effect(효과): F76F lifecycle-aware repair proxy(생명주기 인식 수리 프록시)를 다음 실행으로 고정했다."
  - "Primary gap(주 간극): same_direction_hold_compression_after_signal_parity."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F76E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다.

Effect(효과): F76D에서 signal parity(신호 동등성)는 맞았지만, same-direction hold compression(동방향 보유 압축)이 runtime trades/day(런타임 일거래)를 압축한 것으로 기록했다.

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- repair focus(수리 초점): lifecycle-aware proxy(생명주기 인식 프록시), session/threshold recombination(세션/임계값 재조합)
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)
    selection = f"""# F76 Selection Status(F76 선택 상태)

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F76E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다.

Effect(효과): 다음 실행은 F76F lifecycle-aware density repair proxy(생명주기 인식 거래밀도 수리 프록시)다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)


def main() -> int:
    created_at = f76b.utc_now()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    f76d_summary = read_json(F76D_SUMMARY)
    gap_rows = build_gap_rows()
    summary = build_summary(gap_rows)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "f76d_summary": f76d_summary,
        "gap_rows": gap_rows,
        "summary": summary,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(GAP_ROWS_PATH, gap_rows)
    write_json(SUMMARY_PATH, summary)
    write_json(RUN_DIR / "run_manifest.json", payload)
    write_csv(RUN_DIR / "f76e_proxy_runtime_gap_rows.csv", gap_rows)
    write_json(RUN_DIR / "f76e_gap_analysis_summary.json", summary)
    write_text(REPORT_PATH, report_text(created_at, gap_rows, summary))
    write_text(GATE_AUDIT_PATH, gate_audit_text(created_at, summary))
    update_state_and_ledgers(created_at, summary)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
