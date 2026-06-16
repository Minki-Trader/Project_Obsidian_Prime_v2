from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from stage_pipelines.stage_frontier_68.frontier68a_bridge_feasibility_and_label_design import (
    STAGE_ID,
    rel,
    upsert_ledger,
    write_csv,
    write_json,
    write_md,
)


RUN_ID = "frontier68G_repair_result_review_or_next_validation_v1"
PARENT_RUN_ID = "frontier68F_near_four_axis_onnx_runtime_repair_probe_v1"
NEXT_RUN_ID = "frontier68H_atr_sltp_risk_envelope_runtime_repair_probe_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"

F68D_RECEIPT = REVIEWS_ROOT / "frontier68D_runtime_probe_receipt_review.csv"
F68F_RECEIPT = REVIEWS_ROOT / "frontier68F_runtime_probe_receipt_review.csv"
F68F_GAP = REVIEWS_ROOT / "frontier68F_gap_classification_review.csv"
F68F_HANDOFF = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "frontier68F_handoff_intent.csv"
F68F_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "frontier68F_candidate_axis_summary.csv"
F52_POLICY = ROOT / "stages/stage_frontier_52__short_pf_edge_order_path_cost_recurrence_after_f51_runtime_memory/01_inputs/runtime_policy_manifest.json"

CLAIM_BOUNDARY = (
    "repair_result_review_and_next_runtime_repair_plan_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

NEXT_REPAIR_VARIANTS: tuple[dict[str, Any], ...] = (
    {
        "variant_id": "f52_atr08_tp12_re3_sd6",
        "role": "preserved_clue_atr_sltp_replay",
        "atr_stop_multiplier": 0.8,
        "atr_take_profit_multiplier": 1.2,
        "reentry_cooldown_bars": 3,
        "same_direction_reentry_cooldown_bars": 6,
        "hypothesis": "F52 ATR SL/TP envelope may compress F68F account DD without changing ONNX signals.",
    },
    {
        "variant_id": "tight_atr06_tp10_re3_sd6",
        "role": "dd_compression_pressure",
        "atr_stop_multiplier": 0.6,
        "atr_take_profit_multiplier": 1.0,
        "reentry_cooldown_bars": 3,
        "same_direction_reentry_cooldown_bars": 6,
        "hypothesis": "A tighter ATR stop may reduce DD below F68F, testing whether loss tails dominate the gap.",
    },
    {
        "variant_id": "wide_atr10_tp16_re3_sd6",
        "role": "pf_preservation_pressure",
        "atr_stop_multiplier": 1.0,
        "atr_take_profit_multiplier": 1.6,
        "reentry_cooldown_bars": 3,
        "same_direction_reentry_cooldown_bars": 6,
        "hypothesis": "A wider reward bracket may preserve OOS PF while still adding bounded stop discipline.",
    },
)


def main() -> int:
    created_at = utc_now()
    ensure_dirs()
    d_receipts = read_csv_rows(F68D_RECEIPT)
    f_receipts = read_csv_rows(F68F_RECEIPT)
    f_gaps = read_csv_rows(F68F_GAP)
    handoff = first_row(F68F_HANDOFF)
    summary = first_row(F68F_SUMMARY)
    comparisons = build_comparisons(d_receipts, f_receipts)
    target_status = build_target_status(f_receipts)
    next_variants = build_next_variants(handoff, summary)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": "completed_repair_result_review_next_runtime_repair_plan_no_authority(수리 결과 검토 및 다음 런타임 수리 계획 완료, 권위 없음)",
        "judgment": "preserved_clue_risk_envelope_repair_required_no_authority(보존 단서, 위험 봉투 수리 필요, 권위 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "f68f_handoff": handoff,
        "f68f_summary": summary,
        "target_status": target_status,
        "comparisons": comparisons,
        "gap_summary": summarize_gap(f_gaps),
        "next_repair_hypothesis": {
            "hypothesis": "Apply ATR SL/TP risk envelope to the exact F68F ONNX signal path.",
            "effect": "Separates DD compression from model/feature/signal changes after F68F proved exact signal and feature parity.",
            "grok_required_before_probe": True,
            "next_run_id": NEXT_RUN_ID,
        },
        "next_variants": next_variants,
        "source_paths": {
            "f68d_receipt": rel(F68D_RECEIPT),
            "f68f_receipt": rel(F68F_RECEIPT),
            "f68f_gap": rel(F68F_GAP),
            "f68f_handoff": rel(F68F_HANDOFF),
            "f68f_summary": rel(F68F_SUMMARY),
            "f52_policy": rel(F52_POLICY),
        },
    }
    write_outputs(payload)
    update_state_and_ledgers(payload)
    print(json.dumps(json_ready(compact_status(payload)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def ensure_dirs() -> None:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS_ROOT).mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def first_row(path: Path) -> dict[str, str]:
    rows = read_csv_rows(path)
    return rows[0] if rows else {}


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: Any) -> str:
    number = as_float(value)
    if number is None:
        return "" if value in (None, "") else str(value)
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.6f}".rstrip("0").rstrip(".")


def receipt_by_axis_split(rows: Sequence[Mapping[str, Any]], axis_id: str, split: str) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("axis_id") == axis_id and row.get("split") == split), {})


def f68f_split(rows: Sequence[Mapping[str, Any]], split: str) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("split") == split), {})


def delta(new: Any, old: Any) -> float | None:
    a = as_float(new)
    b = as_float(old)
    if a is None or b is None:
        return None
    return a - b


def build_comparisons(d_receipts: Sequence[Mapping[str, Any]], f_receipts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        d = receipt_by_axis_split(d_receipts, "density_axis", split)
        f = f68f_split(f_receipts, split)
        rows.append(
            {
                "comparison": "f68f_vs_f68d_density_axis",
                "split": split,
                "period": f"{f.get('test_period_start')}..{f.get('test_period_end')}",
                "f68d_net_profit": d.get("net_profit"),
                "f68f_net_profit": f.get("net_profit"),
                "net_profit_delta": fmt(delta(f.get("net_profit"), d.get("net_profit"))),
                "f68d_profit_factor": d.get("profit_factor"),
                "f68f_profit_factor": f.get("profit_factor"),
                "profit_factor_delta": fmt(delta(f.get("profit_factor"), d.get("profit_factor"))),
                "f68d_drawdown_percent": d.get("max_drawdown_percent"),
                "f68f_drawdown_percent": f.get("max_drawdown_percent"),
                "drawdown_percent_delta": fmt(delta(f.get("max_drawdown_percent"), d.get("max_drawdown_percent"))),
                "f68d_trades_per_day": d.get("trades_per_day"),
                "f68f_trades_per_day": f.get("trades_per_day"),
                "trades_per_day_delta": fmt(delta(f.get("trades_per_day"), d.get("trades_per_day"))),
                "signal_count_diff": f.get("signal_count_diff"),
                "feature_ready_diff": f.get("feature_ready_diff"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_target_status(f_receipts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in f_receipts:
        pf = as_float(row.get("profit_factor")) or 0.0
        dd = as_float(row.get("max_drawdown_percent")) or 999.0
        tpd = as_float(row.get("trades_per_day")) or 0.0
        rows.append(
            {
                "split": row.get("split"),
                "period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "drawdown_percent": row.get("max_drawdown_percent"),
                "trades_per_day": row.get("trades_per_day"),
                "density_axis_status": "near_lower_bound" if 4.5 <= tpd < 5.0 else "outside_target",
                "pf_axis_status": "below_final_target" if pf < 2.0 else "inside_final_target",
                "dd_axis_status": "above_final_target" if dd >= 10.0 else "inside_final_target",
                "curve_axis_status": "not_measured_in_f68f_receipt",
                "strict_joint_status": "not_passed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summarize_gap(gaps: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    classes = sorted({row.get("gap_class", "") for row in gaps if row.get("gap_class")})
    return {
        "gap_classes": classes,
        "signal_gap_rows": sum(1 for row in gaps if row.get("layer") == "signal_count_parity" and row.get("delta") not in {"0", "0.0"}),
        "feature_gap_rows": sum(1 for row in gaps if row.get("layer") == "feature_readiness" and row.get("delta") not in {"0", "0.0"}),
        "main_cause": "runtime economics, account DD, and trade/risk shape rather than signal or feature readiness",
    }


def build_next_variants(handoff: Mapping[str, str], summary: Mapping[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in NEXT_REPAIR_VARIANTS:
        rows.append(
            {
                **variant,
                "candidate_id": summary.get("candidate_id") or handoff.get("candidate_id"),
                "model_path_repo": handoff.get("model_path_repo"),
                "feature_csv_repo": handoff.get("feature_csv_repo"),
                "feature_order_hash": handoff.get("feature_order_hash"),
                "model_sha256": handoff.get("model_sha256"),
                "feature_count": handoff.get("feature_count"),
                "max_hold_bars": handoff.get("max_hold_bars"),
                "close_on_flat_signal": True,
                "reverse_on_opposite_signal": True,
                "atr_sltp_enabled": True,
                "atr_period": 14,
                "atr_min_stop_points": 40.0,
                "atr_max_stop_points": 180.0,
                "atr_min_take_profit_points": 60.0,
                "atr_max_take_profit_points": 260.0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "f68g_repair_result_review.json", payload)
    write_csv(RUN_ROOT / "f68g_f68f_vs_f68d_comparison.csv", payload["comparisons"])
    write_csv(RUN_ROOT / "f68g_target_status.csv", payload["target_status"])
    write_csv(RUN_ROOT / "f68g_next_repair_variants.csv", payload["next_variants"])
    write_csv(REVIEWS_ROOT / "frontier68G_f68f_vs_f68d_comparison_review.csv", payload["comparisons"])
    write_csv(REVIEWS_ROOT / "frontier68G_next_repair_variants_review.csv", payload["next_variants"])
    write_md(REVIEWS_ROOT / "frontier68G_repair_result_review_report.md", report_lines(payload))
    write_md(REVIEWS_ROOT / "frontier68G_gate_audit.md", gate_audit_lines(payload))
    write_review_index()


def report_lines(payload: Mapping[str, Any]) -> list[str]:
    lines = [
        "# F68G Repair Result Review(F68G 수리 결과 검토)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68F runtime repair probe(F68F 런타임 수리 탐침)를 F68D density axis(F68D 밀도 축)와 비교하고 다음 수리 가설을 정했다.",
        "",
        "Effect(효과): signal/feature parity(신호/피처 동등성)는 유지된 채 DD(drawdown, 손실폭)와 PF(profit factor, 수익 팩터)가 개선됐는지 분리하고, 다음 MT5 probe(MT5 탐침)를 risk envelope(위험 봉투) 수리로 좁혔다.",
        "",
        f"- status(상태): `{payload['status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        "",
        "## F68F vs F68D Runtime KPI(F68F 대 F68D 런타임 핵심 성과 지표)",
        "",
        "| split(분할) | F68F net(순수익) | net delta(순수익 차이) | F68F PF(수익 팩터) | PF delta(차이) | F68F DD%(손실폭) | DD delta(차이) | F68F trades/day(일 거래) | density delta(밀도 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["comparisons"]:
        lines.append(
            "| `{split}` | `{net}` | `{net_d}` | `{pf}` | `{pf_d}` | `{dd}` | `{dd_d}` | `{tpd}` | `{tpd_d}` |".format(
                split=row["split"],
                net=fmt(row["f68f_net_profit"]),
                net_d=fmt(row["net_profit_delta"]),
                pf=fmt(row["f68f_profit_factor"]),
                pf_d=fmt(row["profit_factor_delta"]),
                dd=fmt(row["f68f_drawdown_percent"]),
                dd_d=fmt(row["drawdown_percent_delta"]),
                tpd=fmt(row["f68f_trades_per_day"]),
                tpd_d=fmt(row["trades_per_day_delta"]),
            )
        )
    lines.extend(
        [
            "",
            "## Target Read(목표 판독)",
            "",
            "- scout clue(탐색 단서): F68F improved OOS net/PF/DD(F68F 표본외 순수익/수익 팩터/손실폭 개선) versus F68D density axis(F68D 밀도 축).",
            "- missing axis(빠진 축): validation/OOS DD(검증/표본외 손실폭)는 `10%` 위이고, PF(수익 팩터)는 final target(최종 목표) 아래다.",
            "- density note(거래 밀도 메모): OOS trades/day(표본외 일 거래)는 `4.779487`로 5/day 하한에 가깝지만 아직 미달이다.",
            "- parity note(동등성 메모): signal_count_diff/feature_ready_diff(신호 수/피처 준비 차이)는 `0`이다.",
            "",
            "## Next Runtime Repair(다음 런타임 수리)",
            "",
            "Hypothesis(가설): exact F68F ONNX signal path(정확한 F68F ONNX 신호 경로)에 ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투)를 붙이면 DD를 더 압축할 수 있다.",
            "",
            "| variant(변형) | role(역할) | ATR stop(손절) | ATR TP(익절) | reentry(재진입) | same-dir cooldown(동방향 쿨다운) |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in payload["next_variants"]:
        lines.append(
            "| `{variant}` | `{role}` | `{stop}` | `{tp}` | `{reentry}` | `{sd}` |".format(
                variant=row["variant_id"],
                role=row["role"],
                stop=row["atr_stop_multiplier"],
                tp=row["atr_take_profit_multiplier"],
                reentry=row["reentry_cooldown_bars"],
                sd=row["same_direction_reentry_cooldown_bars"],
            )
        )
    lines.extend(
        [
            "",
            "Next action(다음 행동): run Grok pre-probe review(Grok 탐침 전 검토) and then F68H MT5 Runtime Probe(F68H MT5 런타임 탐침).",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F68G Gate Audit(F68G 게이트 감사)",
        "",
        f"- F68D receipt(F68D 영수증): `{io_path(F68D_RECEIPT).exists()}`.",
        f"- F68F receipt(F68F 영수증): `{io_path(F68F_RECEIPT).exists()}`.",
        f"- F68F gap table(F68F 간극 표): `{io_path(F68F_GAP).exists()}`.",
        f"- F68F handoff(F68F 인계): `{io_path(F68F_HANDOFF).exists()}`.",
        f"- next variants(다음 변형 수): `{len(payload['next_variants'])}`.",
        "- Grok before F68H MT5 Runtime Probe(F68H MT5 런타임 탐침 전 Grok): `required`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_review_index() -> None:
    index_path = REVIEWS_ROOT / "review_index.md"
    existing = io_path(index_path).read_text(encoding="utf-8-sig") if io_path(index_path).exists() else ""
    additions = [
        "- `frontier68G_repair_result_review_report.md`: F68G repair result review and next ATR SL/TP runtime repair plan(F68G 수리 결과 검토 및 다음 평균진폭 손절/익절 런타임 수리 계획)",
        "- `frontier68G_f68f_vs_f68d_comparison_review.csv`: F68F versus F68D runtime KPI comparison(F68F 대 F68D 런타임 KPI 비교)",
        "- `frontier68G_next_repair_variants_review.csv`: F68H planned risk envelope variants(F68H 계획 위험 봉투 변형)",
    ]
    lines = existing.rstrip().splitlines() if existing else ["# Review Index(검토 색인)", ""]
    for line in additions:
        if line not in lines:
            lines.append(line)
    lines.append(f"Next action(다음 행동): `{NEXT_RUN_ID}`")
    write_md(index_path, lines)


def update_state_and_ledgers(payload: Mapping[str, Any]) -> None:
    oos = next((row for row in payload["target_status"] if row.get("split") == "oos"), {})
    row = {
        "ledger_row_id": f"{RUN_ID}__repair_result_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_result_review(수리 결과 검토)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "f68f_runtime_repair_result_review(F68F 런타임 수리 결과 검토)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "runtime_probe_comparison_and_next_repair_plan(런타임 탐침 비교 및 다음 수리 계획)",
        "scoreboard_lane": "diagnostic_special(진단 특수)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68G_repair_result_review_report.md",
        "primary_kpi": f"oos_pf={fmt(oos.get('profit_factor'))};oos_dd={fmt(oos.get('drawdown_percent'))};oos_tpd={fmt(oos.get('trades_per_day'))}",
        "guardrail_kpi": "f68f_signal_gap_rows=0;f68f_feature_gap_rows=0;grok_required_before_f68h",
        "external_verification_status": "completed_for_review_next_probe_pending(검토 완료, 다음 탐침 대기)",
        "notes": "F68G keeps F68F as preserved clue and routes next repair to ATR SL/TP risk envelope.",
        "date": payload["created_at_utc"][:10],
        "decision": "proceed_to_f68h_atr_sltp_risk_envelope_runtime_repair_probe",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier68G_repair_result_review_report.md",
        "result_judgment": payload["judgment"],
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_repair_review(전선 수리 검토)",
        "run_type": "repair_result_review_or_next_validation(수리 결과 검토 또는 다음 검증)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68g_repair_result_review.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68G_repair_result_review_report.md",
        "source_authority": "f68f_mt5_runtime_probe_observation_no_authority(F68F MT5 런타임 탐침 관찰, 권위 없음)",
    }
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    write_current_state(payload)
    write_selection_status(payload)


def write_current_state(payload: Mapping[str, Any]) -> None:
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload['status']}",
        f"current_judgment: {payload['judgment']}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68f_repair_runtime_probe_reviewed_next_probe_required(F68F 수리 런타임 탐침 검토, 다음 탐침 필요)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F68G action(행동): F68F runtime repair probe(F68F 런타임 수리 탐침)를 F68D density axis(F68D 밀도 축)와 비교했다."',
        '  - "Effect(효과): DD/PF 개선은 보존 단서로 남기고, 최종 목표 미달 축은 ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투) 수리로 넘겼다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}` 전 Grok review(그록 검토) 후 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다."',
        '  - "Boundary(경계): repair result review only(수리 결과 검토 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    write_md(
        ROOT / "docs/context/current_working_state.md",
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {payload['created_at_utc']}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            "",
            f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "",
            f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F68G repair result review(F68G 수리 결과 검토)를 실행했다.",
            "",
            "Effect(효과): F68F는 F68D보다 DD/PF/net(손실폭/수익 팩터/순수익)이 개선됐지만 final target(최종 목표)에는 부족하므로, 다음 MT5 probe(MT5 탐침)를 ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투) 수리로 고정했다.",
            "",
            f"- F68G status(F68G 상태): `{payload['status']}`.",
            f"- next_run(다음 실행): `{NEXT_RUN_ID}`.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def write_selection_status(payload: Mapping[str, Any]) -> None:
    write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        [
            "# F68 Selection Status(F68 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
            f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
            f"- status(상태): `{payload['status']}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            "- completed_action(완료 행동): F68G repair result review(F68G 수리 결과 검토).",
            f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier68G_repair_result_review_report.md`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}` with Grok pre-probe review(그록 탐침 전 검토).",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
        ],
    )


def compact_status(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": payload["status"],
        "judgment": payload["judgment"],
        "comparison_rows": len(payload["comparisons"]),
        "next_variant_rows": len(payload["next_variants"]),
        "next_run_id": payload["next_run_id"],
        "claim_boundary": payload["claim_boundary"],
    }


if __name__ == "__main__":
    raise SystemExit(main())
