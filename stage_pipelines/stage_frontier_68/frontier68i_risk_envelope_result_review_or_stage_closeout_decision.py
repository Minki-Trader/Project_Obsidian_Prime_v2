from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
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


RUN_ID = "frontier68I_risk_envelope_result_review_or_stage_closeout_decision_v1"
PARENT_RUN_ID = "frontier68H_atr_sltp_risk_envelope_runtime_repair_probe_v1"
NEXT_RUN_ID = "frontier68J_unit_corrected_atr_runtime_repair_probe_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
F68H_RUN_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID

F68H_EXECUTION = F68H_RUN_ROOT / "frontier68H_atr_sltp_runtime_repair_execution_result.json"
F68H_COMPARISON = REVIEWS_ROOT / "frontier68H_comparison_vs_f68f_review.csv"
F68H_RECEIPT = REVIEWS_ROOT / "frontier68H_runtime_probe_receipt_review.csv"
F68F_RECEIPT = REVIEWS_ROOT / "frontier68F_runtime_probe_receipt_review.csv"

CLAIM_BOUNDARY = (
    "risk_envelope_result_review_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


def main() -> int:
    created_at = utc_now()
    ensure_dirs()
    execution = json.loads(io_path(F68H_EXECUTION).read_text(encoding="utf-8"))
    comparison_rows = read_csv_rows(F68H_COMPARISON)
    receipt_rows = read_csv_rows(F68H_RECEIPT)
    f68f_rows = read_csv_rows(F68F_RECEIPT)
    effective_rows = build_effective_sltp_rows(execution)
    signature_rows = build_signature_rows(comparison_rows)
    decision = decide(comparison_rows, effective_rows, signature_rows)
    next_variants = build_next_variants(execution)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": "completed_risk_envelope_result_review_no_authority(위험 봉투 결과 검토 완료, 권위 없음)",
        "judgment": decision["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "f68h_status": execution.get("status"),
        "f68h_judgment": execution.get("judgment"),
        "f68f_baseline": f68f_rows,
        "f68h_receipts": receipt_rows,
        "comparison_vs_f68f": comparison_rows,
        "effective_sltp": effective_rows,
        "signature_collapse": signature_rows,
        "decision": decision,
        "next_variants": next_variants,
        "source_paths": {
            "f68h_execution": rel(F68H_EXECUTION),
            "f68h_comparison": rel(F68H_COMPARISON),
            "f68h_receipt": rel(F68H_RECEIPT),
            "f68f_receipt": rel(F68F_RECEIPT),
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


def telemetry_order_sltp_summary(path: Path) -> dict[str, Any]:
    atr_values: list[float] = []
    sl_values: list[float] = []
    tp_values: list[float] = []
    with io_path(path).open("r", encoding="utf-8", errors="replace", newline="") as handle:
        for row in csv.DictReader(handle):
            if str(row.get("order_attempted")).strip().lower() not in {"true", "1"}:
                continue
            atr = as_float(row.get("atr_points"))
            sl = as_float(row.get("open_sl_points"))
            tp = as_float(row.get("open_tp_points"))
            if atr is not None and sl is not None and tp is not None:
                atr_values.append(atr)
                sl_values.append(sl)
                tp_values.append(tp)
    return {
        "order_rows": len(sl_values),
        "atr_min": min(atr_values) if atr_values else "",
        "atr_max": max(atr_values) if atr_values else "",
        "open_sl_min": min(sl_values) if sl_values else "",
        "open_sl_max": max(sl_values) if sl_values else "",
        "open_tp_min": min(tp_values) if tp_values else "",
        "open_tp_max": max(tp_values) if tp_values else "",
        "open_sl_unique_count": len(set(sl_values)),
        "open_tp_unique_count": len(set(tp_values)),
        "open_sl_unique_values": ";".join(fmt(v) for v in sorted(set(sl_values))[:8]),
        "open_tp_unique_values": ";".join(fmt(v) for v in sorted(set(tp_values))[:8]),
    }


def build_effective_sltp_rows(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in execution.get("execution_results", []):
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        telemetry_path = runtime.get("telemetry_path")
        attempt_name = str(result.get("attempt_name") or "")
        if not telemetry_path:
            continue
        summary = telemetry_order_sltp_summary(Path(str(telemetry_path)))
        variant_id = attempt_name.replace("f68h_", "").replace("_validation", "").replace("_oos", "")
        rows.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant_id,
                "split": result.get("split"),
                **summary,
                "effective_collapse": summary.get("open_sl_unique_values") == "180" and summary.get("open_tp_unique_values") == "260",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_signature_rows(comparison_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    by_sig: dict[tuple[str, str], list[str]] = defaultdict(list)
    metric_keys = (
        "net_profit",
        "profit_factor",
        "drawdown_percent",
        "trades_per_day",
        "trade_count",
        "win_rate_percent",
        "average_win",
        "average_loss",
        "payoff_ratio",
    )
    for row in comparison_rows:
        signature = "|".join(str(row.get(key, "")) for key in metric_keys)
        signature_hash = hashlib.sha256(signature.encode("utf-8")).hexdigest()[:12]
        by_sig[(str(row.get("split")), signature_hash)].append(str(row.get("variant_id")))
    rows: list[dict[str, Any]] = []
    for (split, signature_hash), variants in sorted(by_sig.items()):
        rows.append(
            {
                "split": split,
                "signature_hash": signature_hash,
                "variant_count": len(variants),
                "variants": ";".join(sorted(variants)),
                "collapsed_all_three": len(set(variants)) == 3,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def decide(
    comparison_rows: Sequence[Mapping[str, str]],
    effective_rows: Sequence[Mapping[str, Any]],
    signature_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    all_effectively_capped = bool(effective_rows) and all(bool(row.get("effective_collapse")) for row in effective_rows)
    all_signatures_collapsed = sum(1 for row in signature_rows if row.get("collapsed_all_three")) == 2
    negative_kpi = all((as_float(row.get("profit_factor")) or 0.0) < 1.0 for row in comparison_rows)
    if all_effectively_capped and all_signatures_collapsed:
        judgment = (
            "invalid_variant_differentiation_negative_capped_atr_observation_no_authority"
            "(변형 구분 무효, 상한 캡 평균진폭 관찰 부정, 권위 없음)"
        )
        label = "invalid setup plus negative observation(무효 설정 + 부정 관찰)"
    elif negative_kpi:
        judgment = "negative_risk_envelope_probe_no_authority(부정 위험 봉투 탐침, 권위 없음)"
        label = "negative memory(부정 기억)"
    else:
        judgment = "inconclusive_risk_envelope_probe_no_authority(불충분 위험 봉투 탐침, 권위 없음)"
        label = "inconclusive(불충분)"
    return {
        "judgment": judgment,
        "closeout_label": label,
        "main_cause": "F68H variants used different .set multipliers but all effective orders clamped to open_sl=180 and open_tp=260, so variant differentiation collapsed.",
        "negative_memory": "Do not repeat F52-style 40/180 and 60/260 ATR point caps on F68F ONNX; they over-activate exits, increase density, worsen PF, and expand DD.",
        "preserved_clue": "Telemetry ATR points are available and show unit scale; a future ATR probe must use unit-corrected caps or uncapped multiplier semantics.",
        "next_action": NEXT_RUN_ID,
    }


def build_next_variants(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "uncapped_atr03_tp05_re0_sd6",
            "role": "unit_scale_low_pressure",
            "atr_stop_multiplier": 0.3,
            "atr_take_profit_multiplier": 0.5,
            "atr_min_stop_points": 0.0,
            "atr_max_stop_points": 0.0,
            "atr_min_take_profit_points": 0.0,
            "atr_max_take_profit_points": 0.0,
            "reentry_cooldown_bars": 0,
            "same_direction_reentry_cooldown_bars": 6,
            "effect": "Tests ATR unit semantics without max-cap collapse while preserving F68F reentry policy.",
        },
        {
            "variant_id": "uncapped_atr06_tp10_re0_sd6",
            "role": "unit_scale_mid_pressure",
            "atr_stop_multiplier": 0.6,
            "atr_take_profit_multiplier": 1.0,
            "atr_min_stop_points": 0.0,
            "atr_max_stop_points": 0.0,
            "atr_min_take_profit_points": 0.0,
            "atr_max_take_profit_points": 0.0,
            "reentry_cooldown_bars": 0,
            "same_direction_reentry_cooldown_bars": 6,
            "effect": "Tests whether actual ATR multiplier scale can reduce DD without the F68H forced 180/260 stop shape.",
        },
        {
            "variant_id": "uncapped_atr10_tp16_re0_sd6",
            "role": "unit_scale_wide_pressure",
            "atr_stop_multiplier": 1.0,
            "atr_take_profit_multiplier": 1.6,
            "atr_min_stop_points": 0.0,
            "atr_max_stop_points": 0.0,
            "atr_min_take_profit_points": 0.0,
            "atr_max_take_profit_points": 0.0,
            "reentry_cooldown_bars": 0,
            "same_direction_reentry_cooldown_bars": 6,
            "effect": "Tests wider ATR semantics as a control against returning to no-SLTP F68F behavior.",
        },
    ]


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "f68i_risk_envelope_result_review.json", payload)
    write_csv(RUN_ROOT / "f68i_effective_atr_sltp_summary.csv", payload["effective_sltp"])
    write_csv(RUN_ROOT / "f68i_signature_collapse.csv", payload["signature_collapse"])
    write_csv(RUN_ROOT / "f68i_next_unit_corrected_atr_variants.csv", payload["next_variants"])
    write_csv(REVIEWS_ROOT / "frontier68I_effective_atr_sltp_summary_review.csv", payload["effective_sltp"])
    write_csv(REVIEWS_ROOT / "frontier68I_signature_collapse_review.csv", payload["signature_collapse"])
    write_csv(REVIEWS_ROOT / "frontier68I_next_unit_corrected_atr_variants_review.csv", payload["next_variants"])
    write_md(REVIEWS_ROOT / "frontier68I_risk_envelope_result_review_report.md", report_lines(payload))
    write_md(REVIEWS_ROOT / "frontier68I_gate_audit.md", gate_audit_lines(payload))
    write_review_index()


def report_lines(payload: Mapping[str, Any]) -> list[str]:
    lines = [
        "# F68I Risk Envelope Result Review(F68I 위험 봉투 결과 검토)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68H ATR SL/TP runtime probe(F68H 평균진폭 손절/익절 런타임 탐침)를 KPI(핵심 성과 지표), effective SL/TP(실효 손절/익절), signature collapse(서명 붕괴)로 검토했다.",
        "",
        "Effect(효과): 세 변형이 실제로는 모두 open_sl=180/open_tp=260(개시 손절/익절 180/260)으로 접혔다는 원인을 분리해, 같은 캡 수리를 반복하지 않게 했다.",
        "",
        f"- status(상태): `{payload['status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        f"- closeout label(마감 라벨): `{payload['decision']['closeout_label']}`",
        "",
        "## F68H KPI Summary(F68H 핵심 성과 지표 요약)",
        "",
        "| split(분할) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | variants(변형) |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in payload["signature_collapse"]:
        sample = next((r for r in payload["comparison_vs_f68f"] if r.get("split") == row["split"]), {})
        lines.append(
            "| `{split}` | `{net}` | `{pf}` | `{dd}` | `{tpd}` | `{variants}` |".format(
                split=row["split"],
                net=fmt(sample.get("net_profit")),
                pf=fmt(sample.get("profit_factor")),
                dd=fmt(sample.get("drawdown_percent")),
                tpd=fmt(sample.get("trades_per_day")),
                variants=row["variants"],
            )
        )
    lines.extend(
        [
            "",
            "## Effective SL/TP(실효 손절/익절)",
            "",
            "| attempt(시도) | ATR min/max(평균진폭 최소/최대) | SL unique(손절 고유값) | TP unique(익절 고유값) | collapsed(붕괴) |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in payload["effective_sltp"]:
        lines.append(
            "| `{attempt}` | `{amin}..{amax}` | `{sl}` | `{tp}` | `{collapsed}` |".format(
                attempt=row["attempt_name"],
                amin=fmt(row["atr_min"]),
                amax=fmt(row["atr_max"]),
                sl=row["open_sl_unique_values"],
                tp=row["open_tp_unique_values"],
                collapsed=row["effective_collapse"],
            )
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- main cause(주요 원인): {payload['decision']['main_cause']}",
            f"- negative memory(부정 기억): {payload['decision']['negative_memory']}",
            f"- preserved clue(보존 단서): {payload['decision']['preserved_clue']}",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}` should test unit-corrected ATR semantics(단위 보정 평균진폭 의미)를 쓰되, Grok review(Grok 검토)를 먼저 실행해야 한다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F68I Gate Audit(F68I 게이트 감사)",
        "",
        f"- F68H execution result(F68H 실행 결과): `{io_path(F68H_EXECUTION).exists()}`.",
        f"- F68H comparison(F68H 비교): `{io_path(F68H_COMPARISON).exists()}`.",
        f"- effective SL/TP rows(실효 손절/익절 행): `{len(payload['effective_sltp'])}`.",
        f"- signature collapse rows(서명 붕괴 행): `{len(payload['signature_collapse'])}`.",
        "- MT5 Runtime Probe(MT5 런타임 탐침): `completed_in_F68H(F68H에서 완료)`.",
        "- Grok before next MT5 probe(다음 MT5 탐침 전 Grok): `required_for_F68J(F68J 필수)`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_review_index() -> None:
    index_path = REVIEWS_ROOT / "review_index.md"
    existing = io_path(index_path).read_text(encoding="utf-8-sig") if io_path(index_path).exists() else ""
    additions = [
        "- `frontier68I_risk_envelope_result_review_report.md`: F68I risk envelope result review(F68I 위험 봉투 결과 검토)",
        "- `frontier68I_effective_atr_sltp_summary_review.csv`: effective ATR SL/TP summary(실효 평균진폭 손절/익절 요약)",
        "- `frontier68I_signature_collapse_review.csv`: F68H signature collapse review(F68H 서명 붕괴 검토)",
        "- `frontier68I_next_unit_corrected_atr_variants_review.csv`: F68J unit-corrected ATR variants(F68J 단위 보정 평균진폭 변형)",
    ]
    lines = existing.rstrip().splitlines() if existing else ["# Review Index(검토 색인)", ""]
    for line in additions:
        if line not in lines:
            lines.append(line)
    lines.append(f"Next action(다음 행동): `{NEXT_RUN_ID}`")
    write_md(index_path, lines)


def update_state_and_ledgers(payload: Mapping[str, Any]) -> None:
    oos = next((row for row in payload["comparison_vs_f68f"] if row.get("split") == "oos"), {})
    row = {
        "ledger_row_id": f"{RUN_ID}__risk_envelope_result_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "risk_envelope_result_review(위험 봉투 결과 검토)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "f68h_effective_sltp_and_signature_review(F68H 실효 손절익절 및 서명 검토)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "risk_envelope_result_and_next_repair(위험 봉투 결과 및 다음 수리)",
        "scoreboard_lane": "diagnostic_special(진단 특수)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68I_risk_envelope_result_review_report.md",
        "primary_kpi": f"oos_pf={fmt(oos.get('profit_factor'))};oos_dd={fmt(oos.get('drawdown_percent'))};oos_tpd={fmt(oos.get('trades_per_day'))}",
        "guardrail_kpi": "effective_sl=180;effective_tp=260;variant_signature_collapse=true;next_grok_required",
        "external_verification_status": "completed_for_review_next_probe_pending(검토 완료, 다음 탐침 대기)",
        "notes": "F68I records F68H as invalid variant differentiation plus negative capped ATR observation.",
        "date": payload["created_at_utc"][:10],
        "decision": "proceed_to_f68j_unit_corrected_atr_runtime_repair_probe",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier68I_risk_envelope_result_review_report.md",
        "result_judgment": payload["judgment"],
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_risk_envelope_result_review(전선 위험 봉투 결과 검토)",
        "run_type": "risk_envelope_result_review_or_stage_closeout_decision(위험 봉투 결과 검토 또는 단계 마감 결정)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68i_risk_envelope_result_review.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68I_risk_envelope_result_review_report.md",
        "source_authority": "f68h_mt5_runtime_probe_observation_no_authority(F68H MT5 런타임 탐침 관찰, 권위 없음)",
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
        "runtime_probe_status: f68h_reviewed_invalid_variant_differentiation_next_probe_required(F68H 검토, 변형 구분 무효, 다음 탐침 필요)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F68I action(행동): F68H effective ATR SL/TP(F68H 실효 평균진폭 손절/익절)와 signature collapse(서명 붕괴)를 검토했다."',
        '  - "Effect(효과): 세 변형이 모두 180/260 포인트로 접힌 것을 기록해 같은 cap repair(상한 수리) 반복을 막았다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}` 전 Grok review(그록 검토) 후 unit-corrected ATR probe(단위 보정 평균진폭 탐침)를 실행한다."',
        '  - "Boundary(경계): result review only(결과 검토 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
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
            "Action(행동): F68I risk envelope result review(F68I 위험 봉투 결과 검토)를 실행했다.",
            "",
            "Effect(효과): F68H의 세 ATR SL/TP 변형이 모두 open_sl=180/open_tp=260(개시 손절/익절 180/260)으로 접혀 variant differentiation(변형 구분)이 무효였음을 기록했다.",
            "",
            f"- F68I status(F68I 상태): `{payload['status']}`.",
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
            "- completed_action(완료 행동): F68I risk envelope result review(F68I 위험 봉투 결과 검토).",
            f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier68I_risk_envelope_result_review_report.md`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}` with Grok pre-probe review(그록 탐침 전 검토).",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
        ],
    )


def compact_status(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": payload["status"],
        "judgment": payload["judgment"],
        "effective_sltp_rows": len(payload["effective_sltp"]),
        "signature_collapse_rows": len(payload["signature_collapse"]),
        "next_run_id": payload["next_run_id"],
        "claim_boundary": payload["claim_boundary"],
    }


if __name__ == "__main__":
    raise SystemExit(main())
