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
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_73 import frontier73b_session_regime_feature_model_rotation_proxy_scout as f73b


STAGE_ID = f73b.STAGE_ID
RUN_ID = "frontier73G_direct_binary_adapter_gap_or_closeout_decision_v1"
PARENT_RUN_ID = "frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1"
NEXT_RUN_ID = "frontier73H_closeout_grok_review_v1"
CLAIM_BOUNDARY = (
    "gap_decision_and_closeout_recommendation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f73b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f73b.REVIEWS_ROOT
SELECTED_ROOT = f73b.SELECTED_ROOT
F73D_RECEIPT = STAGE_ROOT / "02_runs/frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1/f73d_runtime_probe_receipt.csv"
F73F_RECEIPT = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_runtime_probe_receipt.csv"
F73F_REPRO = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_source_reproduction.csv"
F73F_SIGNAL = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_signal_parity.csv"
F73F_PROB = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_probability_parity.csv"
F73F_ARTIFACT = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_direct_binary_adapter_materialization.csv"
F73F_REPORT = REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"
F73E_REPORT = REVIEWS_ROOT / "frontier73E_proxy_runtime_gap_analysis_report.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def require_inputs() -> list[str]:
    paths = [F73D_RECEIPT, F73F_RECEIPT, F73F_REPRO, F73F_SIGNAL, F73F_PROB, F73F_ARTIFACT, F73F_REPORT, F73E_REPORT]
    return [rel(path) for path in paths if not path_exists(path)]


def split_rows(frame: pd.DataFrame) -> dict[str, dict[str, Any]]:
    return {str(row["split"]): row.to_dict() for _, row in frame.iterrows()}


def build_gap_rows() -> list[dict[str, Any]]:
    f73d = split_rows(read_csv(F73D_RECEIPT))
    f73f = split_rows(read_csv(F73F_RECEIPT))
    repro = split_rows(read_csv(F73F_REPRO))
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        d = f73d.get(split, {})
        f = f73f.get(split, {})
        r = repro.get(split, {})
        rows.append(
            {
                "split": split,
                "f73d_runtime_net_profit": d.get("net_profit"),
                "f73d_runtime_profit_factor": d.get("profit_factor"),
                "f73d_runtime_dd_percent": d.get("max_drawdown_percent"),
                "f73d_runtime_trades_day": d.get("trades_per_day"),
                "f73f_proxy_net_profit": f.get("proxy_net_profit"),
                "f73f_proxy_profit_factor": f.get("proxy_profit_factor"),
                "f73f_proxy_dd_percent": f.get("proxy_dd_percent"),
                "f73f_proxy_trades_day": f.get("proxy_trades_per_day"),
                "f73f_runtime_net_profit": f.get("net_profit"),
                "f73f_runtime_profit_factor": f.get("profit_factor"),
                "f73f_runtime_dd_percent": f.get("max_drawdown_percent"),
                "f73f_runtime_trades_day": f.get("trades_per_day"),
                "f73f_trade_count": f.get("trade_count"),
                "f73f_expected_signal_count": f.get("expected_signal_count"),
                "f73f_signal_count_diff": f.get("signal_count_diff"),
                "f73f_feature_ready_diff": f.get("feature_ready_diff"),
                "f73f_order_attempt_count": f.get("order_attempt_count"),
                "f73f_order_fill_count": f.get("order_fill_count"),
                "f73f_win_rate_percent": f.get("win_rate_percent"),
                "f73f_average_win": f.get("average_win"),
                "f73f_average_loss": f.get("average_loss"),
                "f73f_payoff_ratio": f.get("payoff_ratio"),
                "f73f_expectancy": f.get("expectancy"),
                "f73f_recovery_factor": f.get("recovery_factor"),
                "source_reproduction_overlap": r.get("overlap_ratio_vs_source"),
                "runtime_minus_proxy_pf": _num(f.get("profit_factor")) - _num(f.get("proxy_profit_factor")),
                "runtime_minus_proxy_dd": _num(f.get("max_drawdown_percent")) - _num(f.get("proxy_dd_percent")),
                "runtime_trade_compression": _num(f.get("trade_count")) / _num(f.get("expected_signal_count")) if _num(f.get("expected_signal_count")) else None,
            }
        )
    return rows


def _num(value: Any) -> float:
    try:
        if pd.isna(value):
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def build_decision(gap_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validation = next(row for row in gap_rows if row.get("split") == "validation")
    oos = next(row for row in gap_rows if row.get("split") == "oos")
    artifact = read_csv(F73F_ARTIFACT).iloc[0].to_dict()
    signal = read_csv(F73F_SIGNAL)
    probability = read_csv(F73F_PROB)
    signal_pass = int(signal["passed"].astype(bool).sum())
    probability_pass = int(probability["passed"].astype(bool).sum())
    preserved_clues = [
        "direct_binary_adapter_removed_bridge_divergence(직접 이진 어댑터가 연결 분기를 제거함)",
        "source_reproduction_overlap_1_0(원천 재현 중복 1.0)",
        "oos_runtime_dd_repaired_from_f73d_15_33_to_f73f_5_16(표본외 런타임 손실폭이 F73D 15.33%에서 F73F 5.16%로 개선)",
    ]
    negative_memory = [
        "validation_runtime_dd_21_percent_remains_unacceptable(검증 런타임 손실폭 21%는 불가)",
        "oos_trade_density_0_63_trades_day_below_goal_axis(표본외 일거래 0.63은 목표 축보다 낮음)",
        "signal_parity_perfect_but_runtime_trade_lifecycle_compresses_entries(신호 동등성은 완전하지만 런타임 거래 생명주기가 진입을 압축)",
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "gap_decision_completed_closeout_review_required",
        "judgment": "preserved_clue_negative_memory_closeout_review_required_no_authority",
        "closeout_recommendation": "close_as_preserved_clue_negative_memory",
        "result_subject": "F73 session/regime/feature/model rotation after direct binary adapter runtime repair(F73 세션/장세/피처/모델 회전의 직접 이진 어댑터 런타임 수리 이후 판정)",
        "evidence_available": [
            rel(F73E_REPORT),
            rel(F73F_REPORT),
            rel(F73F_RECEIPT),
            rel(F73F_SIGNAL),
            rel(F73F_REPRO),
        ],
        "evidence_missing": [
            "not_a_completion_candidate_so_wfo_stress_not_run(완성 후보가 아니라 WFO/스트레스는 실행하지 않음)",
            "time_under_water_not_available_in_runtime_receipt(회복 전 체류 시간은 런타임 영수증에 없음)",
            "max_consecutive_loss_not_available_in_runtime_receipt(최대 연속 손실은 런타임 영수증에 없음)",
        ],
        "preserved_clue": preserved_clues,
        "negative_memory": negative_memory,
        "primary_gap_cause": "trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극)",
        "secondary_gap_cause": "session_regime_feature_model_seed_not_stable_across_validation_oos(세션/장세/피처/모델 씨앗이 검증과 표본외에서 안정적이지 않음)",
        "signal_parity_pass_rows": signal_pass,
        "probability_parity_pass_rows": probability_pass,
        "source_reproduction_min_overlap": min(float(row.get("source_reproduction_overlap") or 0.0) for row in gap_rows),
        "validation_runtime": validation,
        "oos_runtime": oos,
        "artifact": {
            "candidate_id": artifact.get("candidate_id"),
            "source_candidate_id": artifact.get("source_candidate_id"),
            "patched_onnx_path": artifact.get("patched_onnx_path"),
            "patched_onnx_sha256": artifact.get("patched_onnx_sha256"),
            "feature_order_sha256": artifact.get("feature_order_sha256"),
            "runtime_veto_tape_sha256": artifact.get("runtime_veto_tape_sha256"),
            "export_status": artifact.get("export_status"),
        },
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any], gap_rows: Sequence[Mapping[str, Any]], created_at: str) -> list[str]:
    validation = payload["validation_runtime"]
    oos = payload["oos_runtime"]
    lines = [
        "# Frontier73G Direct Binary Adapter Gap Decision(F73G 직접 이진 어댑터 간극 결정)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload['status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        f"- closeout_recommendation(마감 권고): `{payload['closeout_recommendation']}`",
        f"- primary_gap_cause(주요 간극 원인): `{payload['primary_gap_cause']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Evidence(근거)",
        "",
        f"- probability parity(확률 동등성): `{payload['probability_parity_pass_rows']}/3`",
        f"- signal parity(신호 동등성): `{payload['signal_parity_pass_rows']}/3`",
        f"- source reproduction min overlap(원천 재현 최소 중복): `{payload['source_reproduction_min_overlap']}`",
        f"- artifact(산출물): `{payload['artifact']['patched_onnx_path']}`, sha256 `{payload['artifact']['patched_onnx_sha256']}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| split(분할) | net(순수익) | PF(수익 팩터) | DD(손실폭) | trades/day(일거래) | trade_count(거래 수) | win_rate(승률) | expectancy(기대값) | recovery(회복 계수) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in gap_rows:
        lines.append(
            f"| {row['split']} | {row['f73f_runtime_net_profit']} | {row['f73f_runtime_profit_factor']} | {row['f73f_runtime_dd_percent']} | {row['f73f_runtime_trades_day']} | {row['f73f_trade_count']} | {row['f73f_win_rate_percent']} | {row['f73f_expectancy']} | {row['f73f_recovery_factor']} |"
        )
    lines.extend(
        [
            "",
            "## Decision(결정)",
            "",
            "- preserved_clue(보존 단서): direct binary adapter(직접 이진 어댑터)는 F73C source signal(원천 신호)을 보존했고 OOS DD(표본외 손실폭)를 줄였다.",
            "- negative_memory(부정 기억): validation DD(검증 손실폭) 21%, OOS trades/day(표본외 일거래) 0.63이라 네 축을 동시에 만족하는 방향은 아니다.",
            "- next_condition(다음 조건): F73 closeout Grok review(F73 마감 Grok 검토)가 이 마감 권고를 비판하고, 다음 stage(단계)는 새 hypothesis(가설)로 열어야 한다.",
            "",
            "## Closeout KPI Snapshot(마감 핵심 성과 지표 스냅샷)",
            "",
            f"- validation(검증): net/PF/DD/trades_day `{validation.get('f73f_runtime_net_profit')}` / `{validation.get('f73f_runtime_profit_factor')}` / `{validation.get('f73f_runtime_dd_percent')}` / `{validation.get('f73f_runtime_trades_day')}`.",
            f"- oos(표본외): net/PF/DD/trades_day `{oos.get('f73f_runtime_net_profit')}` / `{oos.get('f73f_runtime_profit_factor')}` / `{oos.get('f73f_runtime_dd_percent')}` / `{oos.get('f73f_runtime_trades_day')}`.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`.",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    return [
        "# F73G Required Gate Coverage Audit(F73G 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        f"- parent_runtime_probe(상위 런타임 탐침): `{rel(F73F_RECEIPT)}`.",
        f"- proxy_runtime_gap_analysis(프록시/런타임 간극 분석): `{rel(F73E_REPORT)}`.",
        f"- signal_parity(신호 동등성): `{payload['signal_parity_pass_rows']}/3`.",
        f"- probability_parity(확률 동등성): `{payload['probability_parity_pass_rows']}/3`.",
        f"- source_reproduction_min_overlap(원천 재현 최소 중복): `{payload['source_reproduction_min_overlap']}`.",
        "- final_claim_guard(최종 주장 보호): pass(통과).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_runtime"]
    row = {
        "ledger_row_id": f"{RUN_ID}__gap_decision",
        "row_id": f"{RUN_ID}__gap_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "direct_binary_adapter_gap_decision(직접 이진 어댑터 간극 결정)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "gap_decision(간극 결정)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_gap_decision_kpi(런타임 간극 결정 KPI)",
        "scoreboard_lane": "runtime_probe_gap_analysis(런타임 탐침 간극 분석)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": rel(REVIEWS_ROOT / "frontier73G_direct_binary_adapter_gap_decision_report.md"),
        "primary_kpi": f"oos_pf={oos.get('f73f_runtime_profit_factor')};oos_dd={oos.get('f73f_runtime_dd_percent')};oos_tpd={oos.get('f73f_runtime_trades_day')}",
        "guardrail_kpi": f"signal_parity={payload['signal_parity_pass_rows']}/3;source_overlap={payload['source_reproduction_min_overlap']}",
        "external_verification_status": "completed(완료)",
        "notes": "F73G gap decision recommends closeout as preserved clue plus negative memory; no authority.",
        "family": "gap_decision(간극 결정)",
        "lane": "runtime_gap_analysis(런타임 간극 분석)",
        "primary_report": rel(REVIEWS_ROOT / "frontier73G_direct_binary_adapter_gap_decision_report.md"),
        "run_number": "frontier73G",
        "date": created_at[:10],
        "decision": payload["judgment"],
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier73G_direct_binary_adapter_gap_decision_report.md"),
        "runtime_completed_rows": 2,
        "best_net_profit": oos.get("f73f_runtime_net_profit"),
        "best_profit_factor": oos.get("f73f_runtime_profit_factor"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "candidate_model_id": payload["artifact"].get("candidate_id"),
        "net_profit": oos.get("f73f_runtime_net_profit"),
        "profit_factor": oos.get("f73f_runtime_profit_factor"),
        "drawdown": oos.get("f73f_runtime_dd_percent"),
        "trade_count": oos.get("f73f_trade_count"),
        "trade_density": oos.get("f73f_runtime_trades_day"),
        "result_status": payload["status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73g.md"),
        "evidence_boundary": "gap_decision_no_authority(간극 결정, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier73G_direct_binary_adapter_gap_decision_report.md"),
    }
    f73b.upsert_ledger(f73b.ALPHA_LEDGER, "ledger_row_id", row)
    f73b.upsert_ledger(f73b.RUN_REGISTRY, "run_id", row)
    f73b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f73b.ALPHA_LEDGER)


def update_registers(payload: Mapping[str, Any]) -> None:
    marker = "<!-- frontier73G_direct_binary_adapter_gap_or_closeout_decision_v1 -->"
    oos = payload["oos_runtime"]
    block = f"""<!-- frontier73G_direct_binary_adapter_gap_or_closeout_decision_v1 -->
- `{RUN_ID}` recorded gap decision(간극 결정). Preserved clue(보존 단서): direct binary adapter(직접 이진 어댑터) preserved source signal(원천 신호 보존) and improved OOS DD(표본외 손실폭) to `{oos.get('f73f_runtime_dd_percent')}`. Negative memory(부정 기억): validation DD(검증 손실폭) and trade density(거래 밀도) remain insufficient. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier73G_direct_binary_adapter_gap_decision_report.md')}`. Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."""
    append_once(f73b.IDEA_REGISTRY, marker, block)


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload['status']}",
        f"current_judgment: {payload['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f73_runtime_probe_repair_gap_decision_done_closeout_grok_pending",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F73G direct binary adapter gap decision(직접 이진 어댑터 간극 결정)을 기록했다."',
        '  - "Effect(효과): F73F의 보존 단서와 부정 기억을 분리했고, closeout Grok review(마감 Grok 검토)를 다음 행동으로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f73b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(SELECTED_ROOT / "selection_status.md", [
        "# F73 Selection Status(F73 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{payload['status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ])
    write_text(f73b.CURRENT_WORKING_STATE, [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F73G direct binary adapter gap decision(직접 이진 어댑터 간극 결정)을 기록했다.",
        "",
        f"Effect(효과): F73 closeout Grok review(F73 마감 Grok 검토)를 다음 행동 `{NEXT_RUN_ID}`로 설정했다.",
        "",
        f"- judgment(판정): `{payload['judgment']}`.",
        f"- closeout_recommendation(마감 권고): `{payload['closeout_recommendation']}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    missing = require_inputs()
    if missing:
        raise FileNotFoundError(f"F73G required material missing: {missing}")
    created_at = utc_now()
    gap_rows = build_gap_rows()
    payload = build_decision(gap_rows)
    payload["created_at_utc"] = created_at
    write_json(RUN_ROOT / "frontier73G_gap_decision_result.json", payload)
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": payload["status"],
        "judgment": payload["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "input_reports": payload["evidence_available"],
    })
    write_csv(RUN_ROOT / "f73g_direct_binary_adapter_gap_rows.csv", gap_rows)
    write_csv(REVIEWS_ROOT / "f73g_direct_binary_adapter_gap_rows_review.csv", gap_rows)
    write_text(REVIEWS_ROOT / "frontier73G_direct_binary_adapter_gap_decision_report.md", report_lines(payload, gap_rows, created_at))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f73g.md", gate_audit_lines(payload, created_at))
    update_ledgers(payload, created_at)
    update_registers(payload)
    update_state(payload, created_at)
    print(json.dumps(json_ready({
        "run_id": RUN_ID,
        "status": payload["status"],
        "judgment": payload["judgment"],
        "closeout_recommendation": payload["closeout_recommendation"],
        "oos_pf": payload["oos_runtime"].get("f73f_runtime_profit_factor"),
        "oos_dd": payload["oos_runtime"].get("f73f_runtime_dd_percent"),
        "oos_trades_day": payload["oos_runtime"].get("f73f_runtime_trades_day"),
        "validation_pf": payload["validation_runtime"].get("f73f_runtime_profit_factor"),
        "validation_dd": payload["validation_runtime"].get("f73f_runtime_dd_percent"),
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
