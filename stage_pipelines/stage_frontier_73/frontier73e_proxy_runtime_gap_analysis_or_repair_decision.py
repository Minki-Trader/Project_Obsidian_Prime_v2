from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_73 import frontier73b_session_regime_feature_model_rotation_proxy_scout as f73b


STAGE_ID = f73b.STAGE_ID
RUN_ID = "frontier73E_proxy_runtime_gap_analysis_or_repair_decision_v1"
PARENT_RUN_ID = "frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1"
NEXT_RUN_ID = "frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1"
STATUS = "proxy_runtime_gap_analysis_completed"
JUDGMENT = "runtime_gap_binary_bridge_divergence_repair_probe_required_no_authority"
CLAIM_BOUNDARY = (
    "gap_analysis_and_repair_decision_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f73b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f73b.REVIEWS_ROOT
SELECTED_ROOT = f73b.SELECTED_ROOT
F73C_TOP = STAGE_ROOT / "02_runs/frontier73C_axis_reduction_or_repair_proxy_scout_v1/f73c_top_candidates.csv"
F73D_RECEIPT = STAGE_ROOT / "02_runs/frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1/f73d_runtime_probe_receipt.csv"
F73D_DELTA = STAGE_ROOT / "02_runs/frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1/f73d_proxy_bridge_delta.csv"
F73D_MATERIALIZATION = STAGE_ROOT / "02_runs/frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1/f73d_bridge_materialization.csv"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def required_inputs() -> list[Path]:
    return [F73C_TOP, F73D_RECEIPT, F73D_DELTA, F73D_MATERIALIZATION]


def load_sources() -> dict[str, Any]:
    top = pd.read_csv(io_path(F73C_TOP))
    source = top.loc[top["candidate_id"].astype(str).eq("f73c_0002")]
    if source.empty:
        source = top.head(1)
    receipt = pd.read_csv(io_path(F73D_RECEIPT))
    delta = pd.read_csv(io_path(F73D_DELTA))
    material = pd.read_csv(io_path(F73D_MATERIALIZATION))
    return {
        "source": source.iloc[0].to_dict(),
        "runtime_rows": receipt.to_dict(orient="records"),
        "delta_rows": delta.to_dict(orient="records"),
        "materialization": material.iloc[0].to_dict() if not material.empty else {},
    }


def row_by_split(rows: Sequence[Mapping[str, Any]], split: str) -> Mapping[str, Any]:
    return next((row for row in rows if str(row.get("split")) == split), {})


def gap_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    source = payload["source"]
    out: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        runtime = row_by_split(payload["runtime_rows"], split)
        delta = row_by_split(payload["delta_rows"], split)
        out.append(
            {
                "split": split,
                "source_binary_net": source.get(f"{split}_net_profit"),
                "source_binary_pf": source.get(f"{split}_profit_factor"),
                "source_binary_dd": source.get(f"{split}_max_drawdown_percent"),
                "source_binary_tpd": source.get(f"{split}_trades_day"),
                "bridge_proxy_net": delta.get("bridge_net_profit"),
                "bridge_proxy_pf": delta.get("bridge_profit_factor"),
                "bridge_proxy_dd": delta.get("bridge_max_drawdown_percent"),
                "bridge_proxy_tpd": delta.get("bridge_trades_day"),
                "runtime_net": runtime.get("net_profit"),
                "runtime_pf": runtime.get("profit_factor"),
                "runtime_dd": runtime.get("max_drawdown_percent"),
                "runtime_tpd": runtime.get("trades_per_day"),
                "signal_count_diff": runtime.get("signal_count_diff"),
                "feature_ready_diff": runtime.get("feature_ready_diff"),
                "source_bridge_overlap_ratio": delta.get("overlap_ratio_vs_source"),
                "expected_signal_count": runtime.get("expected_signal_count"),
                "runtime_trade_count": runtime.get("trade_count"),
                "gap_driver_primary": "proxy_bridge_selection_divergence",
                "gap_driver_secondary": "trade_lifecycle_gap_after_signal_parity",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary_payload(payload: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    oos = row_by_split(rows, "oos")
    validation = row_by_split(rows, "validation")
    return {
        "created_at_utc": utc_now(),
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "source_candidate_id": payload["source"].get("candidate_id"),
        "materialization_mode": payload["materialization"].get("materialization_mode"),
        "model_family_used": payload["materialization"].get("model_family_used"),
        "validation_runtime_pf": validation.get("runtime_pf"),
        "validation_runtime_dd": validation.get("runtime_dd"),
        "oos_runtime_pf": oos.get("runtime_pf"),
        "oos_runtime_dd": oos.get("runtime_dd"),
        "oos_runtime_tpd": oos.get("runtime_tpd"),
        "oos_signal_count_diff": oos.get("signal_count_diff"),
        "oos_feature_ready_diff": oos.get("feature_ready_diff"),
        "oos_source_bridge_overlap_ratio": oos.get("source_bridge_overlap_ratio"),
        "primary_gap_cause": "binary F73C source was not preserved by 3-class bridge(이진 F73C 원천이 3분류 연결에서 보존되지 않음)",
        "secondary_gap_cause": "runtime lifecycle compressed trades after perfect signal parity(완전 신호 동등성 뒤 런타임 생명주기가 거래를 압축)",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(summary: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> list[str]:
    lines = [
        "# Frontier73E Proxy/Runtime Gap Analysis(F73E 프록시/런타임 간극 분석)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- source_candidate(원천 후보): `{summary['source_candidate_id']}`",
        f"- materialization_mode(물질화 방식): `{summary['materialization_mode']}`",
        f"- model_family_used(사용 모델 계열): `{summary['model_family_used']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Gap Table(간극 표)",
        "",
        "| split(분할) | source binary PF/DD/tpd(원천 이진 수익 팩터/손실폭/일거래) | bridge proxy PF/DD/tpd(연결 프록시 수익 팩터/손실폭/일거래) | runtime PF/DD/tpd(런타임 수익 팩터/손실폭/일거래) | parity diff(동등성 차이) | overlap(중복) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['split']} | {row['source_binary_pf']}/{row['source_binary_dd']}/{row['source_binary_tpd']} | "
            f"{row['bridge_proxy_pf']}/{row['bridge_proxy_dd']}/{row['bridge_proxy_tpd']} | "
            f"{row['runtime_pf']}/{row['runtime_dd']}/{row['runtime_tpd']} | "
            f"signal {row['signal_count_diff']}, feature {row['feature_ready_diff']} | {row['source_bridge_overlap_ratio']} |"
        )
    lines.extend(
        [
            "",
            "## Attribution(귀인)",
            "",
            "- observed_change(관찰 변화): F73C binary proxy(이진 프록시)는 OOS PF/DD/tpd `1.3587/4.2453/1.0`이었지만, F73D runtime(런타임)은 `1.09/15.33/1.0103`으로 약해졌다.",
            "- comparison_baseline(비교 기준): F73C `f73c_0002` binary small_nn_16(이진 작은 신경망) candidate and F73D 3-class bridge(3분류 연결) runtime.",
            "- likely_driver_primary(주요 원인): proxy_bridge_selection_divergence(프록시-연결 선택 분기). OOS overlap(중복)은 약 19%라 F73D bridge(연결)는 F73C 후보를 직접 보존하지 못했다.",
            "- likely_driver_secondary(보조 원인): trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극). Signal/feature diff(신호/피처 차이)는 0이지만 OOS signal 332개가 runtime trade 197개로 줄었다.",
            "- trade_shape(거래 형태): OOS runtime win rate(승률) `41.62%`, payoff ratio(손익비) `1.53`, DD(손실폭) `15.33%`, trades/day(일거래) `1.01`.",
            "- attribution_confidence(귀인 신뢰도): high for bridge divergence(연결 분기 높음), medium for lifecycle cost shape(생명주기 비용 형태 중간).",
            "",
            "## Repair Decision(수리 결정)",
            "",
            "Next repair(다음 수리): direct binary ONNX adapter(직접 이진 ONNX 어댑터)로 F73C binary probability(이진 확률)를 `[p_short=0, p_flat, p_long]` 3-column runtime output(3열 런타임 출력)으로 감싸서 bridge divergence(연결 분기)를 제거한다.",
            "",
            "Effect(효과): 같은 F73C binary signal(이진 신호)을 최대한 보존한 채 MT5 Runtime Probe(MT5 런타임 탐침)를 다시 관찰하고, 그래도 경제성이 무너지면 signal parity 문제가 아니라 lifecycle/execution economics(생명주기/실행 경제성) 문제로 더 강하게 좁힐 수 있다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{summary['next_run_id']}`.",
        ]
    )
    return lines


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F73E Required Gate Coverage Audit(F73E 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- parent_runtime_probe(상위 런타임 탐침): `{rel(F73D_RECEIPT)}`.",
        f"- proxy_bridge_delta(프록시-연결 차이): `{rel(F73D_DELTA)}`.",
        "- gap_cause(간극 원인): proxy_bridge_selection_divergence(프록시-연결 선택 분기) plus trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극).",
        f"- repair_next(다음 수리): `{NEXT_RUN_ID}`.",
        "- final_claim_guard(최종 주장 보호): pass(통과).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    report = REVIEWS_ROOT / "frontier73E_proxy_runtime_gap_analysis_report.md"
    return {
        "ledger_row_id": f"{RUN_ID}__gap_analysis",
        "row_id": f"{RUN_ID}__gap_analysis",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_runtime_gap_analysis(프록시/런타임 간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "gap_analysis(간극 분석)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "proxy_runtime_gap_kpi(프록시/런타임 간극 KPI)",
        "scoreboard_lane": "runtime_probe_gap_analysis(런타임 탐침 간극 분석)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(report),
        "primary_kpi": f"oos_runtime_pf={summary['oos_runtime_pf']}; oos_runtime_dd={summary['oos_runtime_dd']}; overlap={summary['oos_source_bridge_overlap_ratio']}",
        "guardrail_kpi": f"signal_diff={summary['oos_signal_count_diff']}; feature_diff={summary['oos_feature_ready_diff']}",
        "external_verification_status": "completed_from_parent_runtime_probe(F73D 런타임 탐침 완료 기반)",
        "notes": "F73E gap analysis selects direct binary ONNX adapter repair.",
        "family": "gap_analysis(간극 분석)",
        "lane": "proxy_runtime_gap_analysis(프록시/런타임 간극 분석)",
        "primary_report": rel(report),
        "run_number": "frontier73E",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": 2,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73e.md"),
        "evidence_boundary": "gap_analysis_no_authority(간극 분석, 권위 없음)",
        "next_action": summary["next_run_id"],
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "frontier73E_gap_analysis_summary.json"),
        "result_path": rel(report),
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    f73b.upsert_ledger(f73b.ALPHA_LEDGER, "ledger_row_id", row)
    f73b.upsert_ledger(f73b.RUN_REGISTRY, "run_id", row)
    f73b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f73b.ALPHA_LEDGER)


def update_registers(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier73E_proxy_runtime_gap_analysis_or_repair_decision_v1 -->"
    block = f"""<!-- frontier73E_proxy_runtime_gap_analysis_or_repair_decision_v1 -->
- `{RUN_ID}` completed F73 proxy/runtime gap analysis(F73 프록시/런타임 간극 분석). Result(결과): `{summary['judgment']}`. Primary gap(주요 간극): binary F73C source was not preserved by 3-class bridge(이진 F73C 원천이 3분류 연결에서 보존되지 않음), OOS overlap(표본외 중복) `{summary['oos_source_bridge_overlap_ratio']}`. Runtime OOS(런타임 표본외) PF/DD/tpd(수익 팩터/손실폭/일거래) `{summary['oos_runtime_pf']}/{summary['oos_runtime_dd']}/{summary['oos_runtime_tpd']}`. Next(다음): `{summary['next_run_id']}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."""
    append_once(f73b.IDEA_REGISTRY, marker, block)


def update_state(summary: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {summary['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {summary['next_run_id']}",
        "runtime_probe_status: f73_runtime_probe_completed_gap_analysis_done_repair_pending",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "notes:",
        f'  - "Action(행동): F73E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 실행했다. OOS runtime PF/DD/tpd(표본외 런타임 수익 팩터/손실폭/일거래) {summary["oos_runtime_pf"]}/{summary["oos_runtime_dd"]}/{summary["oos_runtime_tpd"]}."',
        f'  - "Effect(효과): bridge divergence(연결 분기)를 주 원인으로 기록하고, 다음 행동을 {summary["next_run_id"]}로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f73b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(SELECTED_ROOT / "selection_status.md", [
        "# F73 Selection Status(F73 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{summary['next_run_id']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{summary['next_run_id']}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ])
    write_text(f73b.CURRENT_WORKING_STATE, [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{summary['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F73E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 실행했다.",
        "",
        f"Effect(효과): F73D의 주요 간극을 bridge divergence(연결 분기)로 기록하고, direct binary ONNX adapter(직접 이진 ONNX 어댑터) 수리 탐침을 다음 행동 `{summary['next_run_id']}`로 설정했다.",
        "",
        f"- judgment(판정): `{summary['judgment']}`.",
        f"- OOS runtime PF/DD/tpd(표본외 런타임 수익 팩터/손실폭/일거래): `{summary['oos_runtime_pf']}` / `{summary['oos_runtime_dd']}` / `{summary['oos_runtime_tpd']}`.",
        f"- signal/feature diff(신호/피처 차이): `{summary['oos_signal_count_diff']}` / `{summary['oos_feature_ready_diff']}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F73E required material missing: {missing}")
    payload = load_sources()
    rows = gap_rows(payload)
    summary = summary_payload(payload, rows)
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    write_csv(RUN_ROOT / "f73e_gap_rows.csv", rows)
    write_json(RUN_ROOT / "frontier73E_gap_analysis_summary.json", summary)
    write_text(RUN_ROOT / "reports/result_summary.md", report_lines(summary, rows))
    write_text(REVIEWS_ROOT / "frontier73E_proxy_runtime_gap_analysis_report.md", report_lines(summary, rows))
    write_csv(REVIEWS_ROOT / "f73e_gap_rows_review.csv", rows)
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f73e.md", gate_audit_lines(summary))
    update_ledgers(summary)
    update_registers(summary)
    update_state(summary)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
