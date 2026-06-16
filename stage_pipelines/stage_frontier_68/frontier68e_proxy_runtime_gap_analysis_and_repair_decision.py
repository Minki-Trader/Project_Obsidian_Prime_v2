from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

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


RUN_ID = "frontier68E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = "frontier68D_mt5_runtime_probe_candidate_axis_materialization_v1"
NEXT_RUN_ID = "frontier68F_near_four_axis_onnx_runtime_repair_probe_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"

F68D_RECEIPT = REVIEWS_ROOT / "frontier68D_runtime_probe_receipt_review.csv"
F68D_GAP = REVIEWS_ROOT / "frontier68D_gap_classification_review.csv"
F68B_SUMMARY = REVIEWS_ROOT / "f68b_proxy_candidate_summary_review.csv"
F68D_REPORT = REVIEWS_ROOT / "frontier68D_mt5_runtime_probe_report.md"

CLAIM_BOUNDARY = (
    "gap_analysis_repair_queue_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

REPAIR_CANDIDATE_IDS = {
    "f68b_0872ddc6192f": {
        "repair_id": "repair01_no_mega_cooldown6_near_four_axis",
        "priority": 1,
        "repair_family": "feature_set_trade_shape_recombination(피처 묶음/거래 형태 재조합)",
        "repair_hypothesis": (
            "Removing mega/top3 features and increasing same-axis spacing can compress runtime DD "
            "while preserving enough ONNX-exportable ExtraTrees density to test in MT5."
        ),
        "repair_effect": (
            "F68D density runtime failure is moved from count parity to DD/PF repair; "
            "F68D PF sparse failure is moved toward higher density."
        ),
        "next_probe": NEXT_RUN_ID,
    },
    "f68b_0f012336cfaf": {
        "repair_id": "repair02_session_regime_no_mega_duplicate_check",
        "priority": 2,
        "repair_family": "feature_set_duplicate_or_regime_check(피처 묶음 중복/장세 확인)",
        "repair_hypothesis": (
            "The session_regime_no_mega surface duplicates the no_mega KPI read in F68B; "
            "keep it as a duplicate-surface check unless feature hash proves it differs."
        ),
        "repair_effect": "Prevents treating two equivalent proxy rows as independent evidence.",
        "next_probe": "hold_after_repair01_hash_check(수리01 해시 확인 뒤 보류)",
    },
}


def main() -> int:
    created_at = utc_now()
    ensure_dirs()
    receipt_rows = read_csv_rows(F68D_RECEIPT)
    gap_rows = read_csv_rows(F68D_GAP)
    summary_rows = read_csv_rows(F68B_SUMMARY)
    selected_repairs = build_repair_queue(summary_rows, receipt_rows, gap_rows)
    attribution = build_attribution(receipt_rows, gap_rows, selected_repairs)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": "completed_gap_analysis_repair_queue_no_authority(간극 분석 및 수리 대기열 완료, 권위 없음)",
        "judgment": "runtime_probe_negative_repairable_seed_surface_no_authority(런타임 탐침 부정, 수리 가능한 씨앗 표면, 권위 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "observed_change": attribution["observed_change"],
        "comparison_baseline": attribution["comparison_baseline"],
        "likely_drivers": attribution["likely_drivers"],
        "segment_checks": attribution["segment_checks"],
        "trade_shape": attribution["trade_shape"],
        "alternative_explanations": attribution["alternative_explanations"],
        "attribution_confidence": attribution["attribution_confidence"],
        "next_probe": attribution["next_probe"],
        "repair_queue": selected_repairs,
        "source_paths": {
            "f68d_receipt": rel(F68D_RECEIPT),
            "f68d_gap": rel(F68D_GAP),
            "f68b_summary": rel(F68B_SUMMARY),
            "f68d_report": rel(F68D_REPORT),
        },
    }
    write_outputs(payload)
    update_state_and_ledgers(payload)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REVIEWS_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


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


def by_key(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {str(row.get(key)): row for row in rows}


def build_repair_queue(
    summary_rows: list[dict[str, str]],
    receipt_rows: list[dict[str, str]],
    gap_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    summary_by_candidate = by_key(summary_rows, "candidate_id")
    density_oos = next((row for row in receipt_rows if row.get("axis_id") == "density_axis" and row.get("split") == "oos"), {})
    density_validation = next(
        (row for row in receipt_rows if row.get("axis_id") == "density_axis" and row.get("split") == "validation"),
        {},
    )
    pf_oos = next((row for row in receipt_rows if row.get("axis_id") == "pf_axis" and row.get("split") == "oos"), {})
    gap_classes = sorted({row.get("gap_class", "") for row in gap_rows if row.get("gap_class")})
    queue: list[dict[str, Any]] = []
    for candidate_id, spec in REPAIR_CANDIDATE_IDS.items():
        row = summary_by_candidate.get(candidate_id)
        if not row:
            queue.append(
                {
                    **spec,
                    "candidate_id": candidate_id,
                    "status": "missing_required_candidate_summary(필수 후보 요약 누락)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        queue.append(
            {
                **spec,
                "candidate_id": candidate_id,
                "status": "queued_for_repair_probe(수리 탐침 대기)",
                "target_id": row.get("target_id"),
                "feature_set_id": row.get("feature_set_id"),
                "model_id": row.get("model_id"),
                "threshold_quantile": row.get("threshold_quantile"),
                "cooldown_bars": row.get("cooldown_bars"),
                "side_policy": row.get("side_policy"),
                "exit_mode": row.get("exit_mode"),
                "proxy_validation_net": row.get("validation_net"),
                "proxy_validation_pf": row.get("validation_pf"),
                "proxy_validation_tpd": row.get("validation_tpd"),
                "proxy_validation_dd_pct": row.get("validation_dd_pct_proxy"),
                "proxy_oos_net": row.get("oos_net"),
                "proxy_oos_pf": row.get("oos_pf"),
                "proxy_oos_tpd": row.get("oos_tpd"),
                "proxy_oos_dd_pct": row.get("oos_dd_pct_proxy"),
                "runtime_gap_basis": {
                    "density_validation_pf": density_validation.get("profit_factor"),
                    "density_validation_dd_pct": density_validation.get("max_drawdown_percent"),
                    "density_oos_pf": density_oos.get("profit_factor"),
                    "density_oos_dd_pct": density_oos.get("max_drawdown_percent"),
                    "pf_oos_trades_per_day": pf_oos.get("trades_per_day"),
                    "gap_classes": gap_classes,
                },
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(queue, key=lambda row: int(row.get("priority") or 999))


def build_attribution(
    receipt_rows: list[dict[str, str]],
    gap_rows: list[dict[str, str]],
    repairs: list[dict[str, Any]],
) -> dict[str, Any]:
    density_validation = next(
        (row for row in receipt_rows if row.get("axis_id") == "density_axis" and row.get("split") == "validation"),
        {},
    )
    density_oos = next((row for row in receipt_rows if row.get("axis_id") == "density_axis" and row.get("split") == "oos"), {})
    pf_validation = next((row for row in receipt_rows if row.get("axis_id") == "pf_axis" and row.get("split") == "validation"), {})
    pf_oos = next((row for row in receipt_rows if row.get("axis_id") == "pf_axis" and row.get("split") == "oos"), {})
    exact_signal_gaps = [row for row in gap_rows if row.get("gap_class") == "signal_count_exact"]
    exact_feature_gaps = [row for row in gap_rows if row.get("gap_class") == "feature_ready_exact"]
    return {
        "observed_change": {
            "density_axis": {
                "validation_runtime_pf": density_validation.get("profit_factor"),
                "validation_runtime_dd_pct": density_validation.get("max_drawdown_percent"),
                "oos_runtime_pf": density_oos.get("profit_factor"),
                "oos_runtime_dd_pct": density_oos.get("max_drawdown_percent"),
                "oos_runtime_tpd": density_oos.get("trades_per_day"),
            },
            "pf_axis": {
                "validation_runtime_pf": pf_validation.get("profit_factor"),
                "validation_runtime_tpd": pf_validation.get("trades_per_day"),
                "oos_runtime_pf": pf_oos.get("profit_factor"),
                "oos_runtime_tpd": pf_oos.get("trades_per_day"),
            },
        },
        "comparison_baseline": "F68C proxy KPI and F68D MT5 Strategy Tester runtime receipt",
        "likely_drivers": [
            "signal/feature parity is not the failure driver because all four attempts have zero signal and feature diffs",
            "density_axis failure is runtime economics and account drawdown expansion",
            "pf_axis failure is signal scarcity and PF saturation in proxy accounting",
            "repair must alter feature set, trade spacing, or risk/exit shape rather than only relabel parity",
        ],
        "segment_checks": {
            "validation_oos": "checked",
            "axis_split": "checked_density_axis_and_pf_axis",
            "signal_count_parity_rows": len(exact_signal_gaps),
            "feature_readiness_parity_rows": len(exact_feature_gaps),
            "missing": "time-under-water and equity smoothness need future runtime report parsing",
        },
        "trade_shape": {
            "density_validation_trades": density_validation.get("trade_count"),
            "density_oos_trades": density_oos.get("trade_count"),
            "density_oos_long_short": f"{density_oos.get('long_trade_count')}/{density_oos.get('short_trade_count')}",
            "pf_validation_trades": pf_validation.get("trade_count"),
            "pf_oos_trades": pf_oos.get("trade_count"),
        },
        "alternative_explanations": [
            "proxy DD is normalized points and not account DD authority",
            "tester report includes deal/accounting effects that proxy only approximates",
            "close_on_flat runtime lifecycle can change realized holding shape versus proxy horizon",
        ],
        "attribution_confidence": "medium(중간)",
        "next_probe": {
            "run_id": NEXT_RUN_ID,
            "primary_repair_candidate": repairs[0].get("candidate_id") if repairs else "",
            "effect": "Export the ONNX-capable near-four-axis repair surface, then run MT5 before any stronger claim.",
        },
    }


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "f68e_gap_attribution.json", payload)
    write_csv(RUN_ROOT / "f68e_repair_queue.csv", payload["repair_queue"])
    write_csv(REVIEWS_ROOT / "f68e_repair_queue_review.csv", payload["repair_queue"])
    write_md(REVIEWS_ROOT / "frontier68E_proxy_runtime_gap_analysis_repair_decision_report.md", report_lines(payload))
    write_md(REVIEWS_ROOT / "frontier68E_gate_audit.md", gate_audit_lines(payload))
    write_review_index()


def report_lines(payload: Mapping[str, Any]) -> list[str]:
    lines = [
        "# F68E Proxy/Runtime Gap Analysis And Repair Decision(F68E 프록시/런타임 간극 분석 및 수리 결정)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68D MT5 Runtime Probe(MT5 런타임 탐침)와 F68B proxy table(프록시 표)을 함께 읽어 repair queue(수리 대기열)를 만들었다.",
        "",
        "Effect(효과): proxy/runtime alignment(프록시/런타임 정렬)을 핑계로 멈추지 않고, feature set/trade shape/model export(피처 묶음/거래 형태/모델 내보내기) 변경으로 이어지는 다음 실험을 고정했다.",
        "",
        "## Runtime Probe Observation(런타임 탐침 관찰)",
        "",
        "- density axis(밀도 축): signal/feature parity(신호/피처 동등성)는 맞았지만 validation PF/DD(검증 수익 팩터/손실폭)가 `0.91/71.13`, OOS PF/DD(표본외 수익 팩터/손실폭)가 `1.04/26.84`였다.",
        "- PF axis(수익 팩터 축): DD(손실폭)는 작았지만 OOS trades/day(표본외 일 거래)가 `0.005128`로 목표 밀도와 멀었다.",
        "- gap cause(간극 원인): 신호 수나 피처 준비 문제가 아니라 runtime economics/account DD/trade shape(런타임 경제성/계좌 손실폭/거래 형태) 문제다.",
        "",
        "## Repair Queue(수리 대기열)",
        "",
        "| priority(우선순위) | repair(수리) | candidate(후보) | proxy val PF/DD/TPD(프록시 검증) | proxy OOS PF/DD/TPD(프록시 표본외) | next(다음) |",
        "|---:|---|---|---:|---:|---|",
    ]
    for row in payload["repair_queue"]:
        lines.append(
            "| `{priority}` | `{repair}` | `{candidate}` | `{vpf}/{vdd}/{vtpd}` | `{opf}/{odd}/{otpd}` | `{next}` |".format(
                priority=row.get("priority"),
                repair=row.get("repair_id"),
                candidate=row.get("candidate_id"),
                vpf=fmt(row.get("proxy_validation_pf")),
                vdd=fmt(row.get("proxy_validation_dd_pct")),
                vtpd=fmt(row.get("proxy_validation_tpd")),
                opf=fmt(row.get("proxy_oos_pf")),
                odd=fmt(row.get("proxy_oos_dd_pct")),
                otpd=fmt(row.get("proxy_oos_tpd")),
                next=row.get("next_probe"),
            )
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): F68D runtime probe result(F68D 런타임 탐침 결과).",
            "- evidence_available(사용 가능 근거): F68D receipt/gap CSV(영수증/간극 표), MT5 reports(전략 테스터 보고서), F68B proxy summary(F68B 프록시 요약).",
            "- evidence_missing(빠진 근거): repair 후보의 ONNX export(ONNX 내보내기), MT5 runtime probe(MT5 런타임 탐침), WFO/stress(워크포워드/스트레스).",
            "- judgment_label(판정 라벨): negative runtime observation with repairable seed surface(부정 런타임 관찰, 수리 가능한 씨앗 표면).",
            f"- next_condition(다음 조건): `{NEXT_RUN_ID}`에서 pre-export Grok review(내보내기 전 그록 검토) 후 ONNX export(ONNX 내보내기)와 MT5 probe(MT5 탐침)를 실행한다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F68E Gate Audit(F68E 게이트 감사)",
        "",
        f"- F68D receipt exists(F68D 영수증 존재): `{io_path(F68D_RECEIPT).exists()}`.",
        f"- F68D gap table exists(F68D 간극 표 존재): `{io_path(F68D_GAP).exists()}`.",
        f"- F68B summary exists(F68B 요약 존재): `{io_path(F68B_SUMMARY).exists()}`.",
        f"- repair_queue_rows(수리 대기열 행): `{len(payload['repair_queue'])}`.",
        "- Grok before next major validation(다음 주요 검증 전 그록): `required_next_run(다음 실행 필수)`.",
        "- MT5 Runtime Probe(MT5 런타임 탐침): `completed_for_F68D; required_again_if_repair_proxy_export_materializes(F68D 완료, 수리 프록시 내보내기 물질화 시 재필수)`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_review_index() -> None:
    existing = io_path(REVIEWS_ROOT / "review_index.md").read_text(encoding="utf-8-sig")
    line = "- `frontier68E_proxy_runtime_gap_analysis_repair_decision_report.md`: F68E gap analysis and repair queue(F68E 간극 분석 및 수리 대기열)"
    if line not in existing:
        existing = existing.rstrip() + "\n" + line + f"\nNext action(다음 행동): `{NEXT_RUN_ID}`\n"
    write_md(REVIEWS_ROOT / "review_index.md", existing.splitlines())


def update_state_and_ledgers(payload: Mapping[str, Any]) -> None:
    primary = payload["repair_queue"][0] if payload["repair_queue"] else {}
    row = {
        "ledger_row_id": f"{RUN_ID}__gap_repair_queue",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "gap_analysis_repair_queue(간극 분석 수리 대기열)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_runtime_gap_repair_decision(프록시 런타임 간극 수리 결정)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "runtime_gap_attribution_and_repair_queue(런타임 간극 원인 분해 및 수리 대기열)",
        "scoreboard_lane": "diagnostic_special(진단 특수)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68E_proxy_runtime_gap_analysis_repair_decision_report.md",
        "primary_kpi": (
            f"primary_repair={primary.get('candidate_id', '')};"
            f"proxy_val_pf={fmt(primary.get('proxy_validation_pf'))};"
            f"proxy_oos_pf={fmt(primary.get('proxy_oos_pf'))};"
            f"proxy_val_tpd={fmt(primary.get('proxy_validation_tpd'))};"
            f"proxy_oos_tpd={fmt(primary.get('proxy_oos_tpd'))}"
        ),
        "guardrail_kpi": "f68d_signal_gap_rows=0;f68d_feature_gap_rows=0;next_grok_required_before_export",
        "external_verification_status": "completed_for_gap_inputs_next_probe_pending(간극 입력 검증 완료, 다음 탐침 대기)",
        "notes": "F68E attributes F68D failure to economics/DD/trade-shape, not signal or feature parity; repair queue created.",
        "date": payload["created_at_utc"][:10],
        "decision": "proceed_to_f68f_near_four_axis_onnx_runtime_repair_probe",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier68E_proxy_runtime_gap_analysis_repair_decision_report.md",
        "result_judgment": payload["judgment"],
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_gap_analysis_repair_queue(전선 간극 분석 수리 대기열)",
        "run_type": "gap_analysis_repair_decision(간극 분석 수리 결정)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68e_repair_queue.csv",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68E_proxy_runtime_gap_analysis_repair_decision_report.md",
        "source_authority": "f68d_mt5_runtime_probe_observation_no_authority(F68D MT5 런타임 탐침 관찰, 권위 없음)",
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
        "runtime_probe_status: f68d_completed_repair_probe_required_if_f68f_export_materializes(F68D 완료, F68F 내보내기 물질화 시 수리 탐침 필수)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F68E action(행동): F68D runtime probe(F68D 런타임 탐침)와 F68B proxy table(F68B 프록시 표)을 연결해 repair queue(수리 대기열)를 만들었다."',
        '  - "Effect(효과): signal/feature parity(신호/피처 동등성)가 아니라 runtime economics/DD/trade shape(런타임 경제성/손실폭/거래 형태)를 다음 수리 대상으로 좁혔다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 Grok review(그록 검토) 후 ONNX export(ONNX 내보내기)와 MT5 repair probe(MT5 수리 탐침)를 시도한다."',
        '  - "Boundary(경계): repair queue only(수리 대기열 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    cws = [
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
        "Action(행동): F68E proxy/runtime gap analysis and repair decision(F68E 프록시/런타임 간극 분석 및 수리 결정)을 실행했다.",
        "",
        "Effect(효과): F68D의 경제성 붕괴를 신호/피처 동등성 문제가 아니라 runtime economics/DD/trade shape(런타임 경제성/손실폭/거래 형태) 문제로 좁히고, 다음 ONNX repair probe(ONNX 수리 탐침) 대기열을 만들었다.",
        "",
        f"- F68E status(F68E 상태): `{payload['status']}`.",
        f"- repair_queue_rows(수리 대기열 행): `{len(payload['repair_queue'])}`.",
        f"- primary repair(주 수리): `{payload['repair_queue'][0]['candidate_id'] if payload['repair_queue'] else ''}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", cws)


def write_selection_status(payload: Mapping[str, Any]) -> None:
    lines = [
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
        f"- completed_action(완료 행동): F68E gap analysis/repair queue(F68E 간극 분석/수리 대기열) `{len(payload['repair_queue'])}` rows(행).",
        "- repair_primary(주 수리): `f68b_0872ddc6192f` near-four-axis ExtraTrees(네 축 근접 엑스트라트리스).",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier68E_proxy_runtime_gap_analysis_repair_decision_report.md`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}` pre-export Grok review, ONNX export, MT5 repair probe(내보내기 전 그록 검토, ONNX 내보내기, MT5 수리 탐침).",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", lines)


if __name__ == "__main__":
    raise SystemExit(main())
