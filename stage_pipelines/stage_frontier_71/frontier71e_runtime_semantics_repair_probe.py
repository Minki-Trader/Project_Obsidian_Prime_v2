from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_71 import frontier71b_economics_native_proxy_scout as f71b
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
)


STAGE_ID = f71b.STAGE_ID
RUN_ID = "frontier71E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = f71d.RUN_ID
SOURCE_PROXY_RUN_ID = f71b.RUN_ID
NEXT_RUN_ID = "frontier71F_stage_closeout_economics_native_label_selection_v1"
PRIMARY_CANDIDATE_ID = f71d.PRIMARY_CANDIDATE_ID
REPAIR_QUANTILE = 0.40
REPAIR_SELECTION_ID = "runtime_compatible_edge_margin_q40"
REPAIR_AXIS_ID = "f71e_edge_margin_q40_runtime_semantics_repair"
REPAIR_ROLE = "runtime_semantics_repair_edge_margin_q40_grok_accepted"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier71E_runtime_semantics_repair"
CLAIM_BOUNDARY = (
    "runtime_semantics_repair_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f71b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f71b.REVIEWS_ROOT
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
GROK_PACKET_ROOT = Path("docs/agent_control/grok_reviews/2026-06-17_f71e_pre_runtime_semantics_repair")
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f71e_pre_runtime_semantics_repair_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

F71D_RECEIPT = STAGE_ROOT / "02_runs" / f71d.RUN_ID / "f71d_runtime_probe_receipt.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F71E runtime semantics repair probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(f71d.ROOT).as_posix()


def configure_f71d_globals() -> None:
    f71d.RUN_ID = RUN_ID
    f71d.PARENT_RUN_ID = PARENT_RUN_ID
    f71d.NEXT_RUN_ID = NEXT_RUN_ID
    f71d.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    f71d.RUN_ROOT = RUN_ROOT
    f71d.MODEL_ROOT = MODEL_ROOT
    f71d.FEATURE_ROOT = FEATURE_ROOT
    f71d.VETO_ROOT = VETO_ROOT
    f71d.MT5_ROOT = MT5_ROOT
    f71d.COMMON_RUN_ROOT = COMMON_RUN_ROOT
    f71d.GROK_PACKET_ROOT = f71d.ROOT / GROK_PACKET_ROOT
    f71d.GROK_PROMPT = f71d.ROOT / GROK_PROMPT
    f71d.GROK_CLEAN = f71d.ROOT / GROK_CLEAN
    f71d.GROK_METADATA = f71d.ROOT / GROK_METADATA


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    f71d.write_csv(path, rows, columns)


def write_md(path: Path, lines: Sequence[str]) -> None:
    f71d.write_md(path, lines)


def class_probabilities(context: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    model = context["model"]
    proba = model.predict_proba(context["frame"].loc[:, context["feature_columns"]])
    classes = list(model.classes_)
    short = proba[:, classes.index(-1)] if -1 in classes else np.zeros(len(proba))
    flat = proba[:, classes.index(0)] if 0 in classes else np.zeros(len(proba))
    long = proba[:, classes.index(1)] if 1 in classes else np.zeros(len(proba))
    return short.astype(float), flat.astype(float), long.astype(float)


def edge_margin_context() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    base = f71d.build_context()
    frame = base["frame"]
    short, flat, long = class_probabilities(base)
    side = np.where(long >= short, 1, -1).astype(int)
    edge = (np.maximum(long, short) - flat).astype(float)
    train_mask = f71b.split_mask(frame, "train")
    selection_mask = f71b.mask_for(frame, base["axis"].mask_name)
    threshold = f71b.threshold_from_train(edge, train_mask, selection_mask, REPAIR_QUANTILE)
    if threshold is None:
        raise RuntimeError("edge margin repair threshold unavailable")
    axis = replace(
        base["axis"],
        axis_id=REPAIR_AXIS_ID,
        role=REPAIR_ROLE,
        selection_id=REPAIR_SELECTION_ID,
        threshold_quantile=REPAIR_QUANTILE,
        threshold=float(threshold),
    )
    selection = f71b.SelectionSpec(axis.selection_id, axis.mask_name, axis.threshold_quantile)
    selected = f71b.selected_mask_from_threshold(frame, edge, selection, base["label_spec"].horizon_bars, float(threshold))
    split_rows = f71b.evaluate_splits(frame, selected, side, base["long_profit"], base["short_profit"])
    repaired = dict(base)
    repaired.update(
        {
            "axis": axis,
            "side": side,
            "score": edge,
            "selected": selected,
            "proxy_kpi_by_split": {row["split"]: row for row in split_rows},
            "feature_order_hash": ordered_hash(base["feature_columns"]),
        }
    )
    return repaired, repair_sweep_rows(base)


def flatten_split_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for row in rows:
        split = str(row["split"])
        for key, value in row.items():
            if key != "split":
                flat[f"{split}_{key}"] = value
    return flat


def repair_sweep_rows(base: Mapping[str, Any]) -> list[dict[str, Any]]:
    frame = base["frame"]
    short, flat, long = class_probabilities(base)
    side = np.where(long >= short, 1, -1).astype(int)
    edge = np.maximum(long, short) - flat
    train_mask = f71b.split_mask(frame, "train")
    selection_mask = f71b.mask_for(frame, base["axis"].mask_name)
    rows: list[dict[str, Any]] = []
    for quantile in (0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70):
        threshold = f71b.threshold_from_train(edge, train_mask, selection_mask, quantile)
        if threshold is None:
            continue
        spec = f71b.SelectionSpec(f"runtime_compatible_edge_margin_q{int(quantile * 100):02d}", base["axis"].mask_name, quantile)
        selected = f71b.selected_mask_from_threshold(frame, edge, spec, base["label_spec"].horizon_bars, threshold)
        kpi = flatten_split_rows(f71b.evaluate_splits(frame, selected, side, base["long_profit"], base["short_profit"]))
        summary = {
            "run_id": RUN_ID,
            "candidate_id": PRIMARY_CANDIDATE_ID,
            "repair_id": spec.selection_id,
            "score_name": "edge_margin",
            "threshold_quantile": quantile,
            "threshold": float(threshold),
            "selected_total": int(selected.sum()),
            **kpi,
        }
        flags = f71b.gate_flags(summary)
        summary.update(flags)
        rows.append(summary)
    return rows


def f71d_gap_observation_rows() -> list[dict[str, Any]]:
    if not path_exists(F71D_RECEIPT):
        return [
            {
                "run_id": RUN_ID,
                "source_run_id": f71d.RUN_ID,
                "gap_observation": "missing_f71d_receipt",
                "effect": "repair evidence incomplete",
            }
        ]
    receipt = pd.read_csv(io_path(F71D_RECEIPT))
    rows: list[dict[str, Any]] = []
    for _, row in receipt.iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "split": row.get("split"),
                "expected_signal_count": row.get("expected_signal_count"),
                "runtime_signal_count": row.get("signal_count"),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
                "gap_cause_summary": row.get("gap_cause_summary"),
                "local_gap_cause": "threshold_semantics_mismatch_custom_score_vs_ea_edge_margin",
                "effect": "repair uses EA-compatible edge margin selection",
            }
        )
    return rows


def repair_signal_status(receipts: Sequence[Mapping[str, Any]]) -> str:
    if not receipts:
        return "not_observed"
    diffs = [abs(int(row.get("signal_count_diff") or 0)) for row in receipts]
    expected = [max(int(row.get("expected_signal_count") or 0), 1) for row in receipts]
    max_ratio = max(diff / exp for diff, exp in zip(diffs, expected, strict=False))
    return "signal_parity_repaired" if max_ratio <= 0.05 else "signal_gap_remaining"


def best_receipt(receipts: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    oos = [row for row in receipts if row.get("split") == "oos"]
    return oos[0] if oos else (receipts[0] if receipts else {})


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt") or [])
    best = best_receipt(receipts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "candidate_id": PRIMARY_CANDIDATE_ID,
        "repair_axis_id": REPAIR_AXIS_ID,
        "repair_threshold_quantile": REPAIR_QUANTILE,
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": sum(1 for row in receipts if row.get("tester_status") == "completed"),
        "runtime_receipt_rows": len(receipts),
        "signal_status": repair_signal_status(receipts),
        "best_runtime_net_profit": best.get("net_profit"),
        "best_runtime_profit_factor": best.get("profit_factor"),
        "best_runtime_drawdown_percent": best.get("max_drawdown_percent"),
        "best_runtime_trades_per_day": best.get("trades_per_day"),
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    receipts = list(payload.get("runtime_receipt") or [])
    best = best_receipt(receipts)
    lines = [
        "# Frontier71E Proxy/Runtime Gap Analysis and Repair(F71E 프록시/런타임 간극 분석 및 수리)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- candidate(후보): `{PRIMARY_CANDIDATE_ID}`",
        f"- repair(수리): `{REPAIR_AXIS_ID}` / `{REPAIR_SELECTION_ID}`",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Gap Cause(간극 원인)",
        "",
        "- F71D ONNX parity(온엑스 동등성) and feature readiness(피처 준비)는 통과했다.",
        "- F71D telemetry(런타임 기록)는 `edge_margin_not_met(엣지 마진 미달)`가 지배했다.",
        "- Local diagnosis(로컬 진단): F71B proxy score(프록시 점수)는 custom score(맞춤 점수)였고 EA decision(전문가 자문 결정)은 edge margin(엣지 마진)이어서 threshold semantics mismatch(임계값 의미 불일치)가 생겼다.",
        "",
        "## Grok Review(그록 검토)",
        "",
        f"- prompt(프롬프트): `{GROK_PROMPT.as_posix()}`",
        f"- output(출력): `{GROK_CLEAN.as_posix()}`",
        "- classification(분류): `accepted_edge_margin_q40_single_repair_probe_needs_local_verification(엣지 마진 q40 단일 수리 탐침 수용, 로컬 검증 필요)`",
        "",
        "## Runtime Repair KPI(런타임 수리 핵심 성과 지표)",
        "",
        "| split(분할) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | expected signals(예상 신호) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in receipts:
        lines.append(
            f"| `{row.get('split')}` | `{f71b.fmt(row.get('net_profit'))}` | `{f71b.fmt(row.get('profit_factor'))}` | "
            f"`{f71b.fmt(row.get('max_drawdown_percent'))}` | `{f71b.fmt(row.get('trade_count'))}` | "
            f"`{f71b.fmt(row.get('trades_per_day'))}` | `{f71b.fmt(row.get('expected_signal_count'))}` | "
            f"`{f71b.fmt(row.get('signal_count_diff'))}` | `{f71b.fmt(row.get('feature_ready_diff'))}` | `{row.get('gap_cause_summary')}` |"
        )
    lines.extend(
        [
            "",
            "## Runtime Parity Boundary(런타임 동등성 경계)",
            "",
            f"- research_path(연구 경로): `{rel(Path(__file__))}`",
            "- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` plus generated `.set/.ini` files(생성 설정 파일).",
            "- shared_contract(공유 계약): ONNX output order `[p_short,p_flat,p_long]`, feature order hash(피처 순서 해시), edge_margin decision(엣지 마진 결정), RuntimeVetoTape selected-entry mask(선택 진입 차단 테이프).",
            "- known_differences(알려진 차이): this is a repair probe(수리 탐침), not the original F71B custom-score proxy(맞춤 점수 프록시).",
            f"- parity_check(동등성 점검): `{repair_signal_status(receipts)}`.",
            "- runtime_claim_boundary(런타임 주장 경계): runtime_probe(런타임 탐침), no runtime authority(런타임 권위 없음).",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`",
        ]
    )
    if best:
        lines.extend(
            [
                "",
                "## Best Runtime Observation(최선 런타임 관찰)",
                "",
                f"- net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(best.get('net_profit'))}` / `{f71b.fmt(best.get('profit_factor'))}` / `{f71b.fmt(best.get('max_drawdown_percent'))}` / `{f71b.fmt(best.get('trades_per_day'))}`.",
            ]
        )
    return lines


def grok_receipt_lines(created_at: str) -> list[str]:
    return [
        "# F71E Grok Receipt(F71E 그록 영수증)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "- trigger_reason(트리거 이유): runtime semantics repair probe(런타임 의미 수리 탐침) 전 검토.",
        "- review_size(검토 크기): medium review(중간 검토).",
        "- direction_before_grok(그록 전 방향): F71D signal count gap(신호 수 간극)을 custom score vs EA edge margin threshold mismatch(맞춤 점수와 EA 엣지 마진 임계값 불일치)로 보고 q40 repair(수리)를 제안.",
        f"- prompt_identity(프롬프트 정체성): `{GROK_PROMPT.as_posix()}`.",
        f"- grok_output_identity(그록 출력 정체성): `{GROK_CLEAN.as_posix()}`.",
        "- advice_classification(조언 분류): accepted(수용) q40 single MT5 repair probe(단일 MT5 수리 탐침); needs_local_verification(로컬 검증 필요) q40 materialization/parity(물질화/동등성).",
        "- local_verification(로컬 검증): F71E script(스크립트)가 q40 ONNX parity(온엑스 동등성), signal count parity(신호 수 동등성), MT5 output(MT5 출력)을 기록한다.",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        "- final_codex_direction(최종 Codex 방향): run F71E edge_margin q40 repair probe(F71E 엣지 마진 q40 수리 탐침 실행).",
    ]


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    return [
        "# F71E Required Gate Coverage Audit(F71E 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- MT5 runtime repair probe(MT5 런타임 수리 탐침): attempts(시도) `{summary['attempt_count']}`, completed(완료) `{summary['completed_attempt_count']}`.",
        f"- signal_status(신호 상태): `{summary['signal_status']}`.",
        f"- Grok review(그록 검토): `{GROK_CLEAN.as_posix()}`.",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`.",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`.",
    ]


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(RUN_ROOT / "frontier71E_runtime_semantics_repair_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier71E_runtime_semantics_repair_summary.json", build_summary(payload))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload, created_at))
    write_csv(RUN_ROOT / "f71e_proxy_repair_sweep.csv", payload.get("proxy_repair_sweep", []))
    write_csv(RUN_ROOT / "f71e_f71d_gap_observation.csv", payload.get("f71d_gap_observation", []))
    write_csv(RUN_ROOT / "f71e_candidate_axis_materialization.csv", payload.get("artifact_rows", []))
    write_csv(RUN_ROOT / "f71e_onnx_probability_parity.csv", payload.get("probability_parity", []))
    write_csv(RUN_ROOT / "f71e_onnx_signal_parity.csv", payload.get("signal_parity", []))
    write_csv(RUN_ROOT / "f71e_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_csv(RUN_ROOT / "f71e_gap_classification.csv", payload.get("gap_classification", []), f71d.GAP_COLUMNS)
    write_csv(REVIEWS_ROOT / "f71e_proxy_repair_sweep_review.csv", payload.get("proxy_repair_sweep", []))
    write_csv(REVIEWS_ROOT / "f71e_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "f71e_gap_classification_review.csv", payload.get("gap_classification", []), f71d.GAP_COLUMNS)
    write_md(REVIEWS_ROOT / "frontier71E_proxy_runtime_gap_analysis_and_repair_decision_report.md", report_lines(payload, created_at))
    write_md(REVIEWS_ROOT / "f71e_pre_runtime_repair_grok_receipt.md", grok_receipt_lines(created_at))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f71e.md", gate_audit_lines(payload, created_at))


def run_manifest(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "created_at_utc": created_at,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "producer": "stage_pipelines/stage_frontier_71/frontier71e_runtime_semantics_repair_probe.py",
        "grok_packet": {"prompt": GROK_PROMPT.as_posix(), "clean_output": GROK_CLEAN.as_posix(), "metadata": GROK_METADATA.as_posix()},
        "candidate_id": PRIMARY_CANDIDATE_ID,
        "repair_axis_id": REPAIR_AXIS_ID,
        "artifact_rows": payload.get("artifact_rows", []),
        "attempts": payload.get("attempts", []),
        "summary": build_summary(payload),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def registry_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    summary = build_summary(payload)
    best = best_receipt(list(payload.get("runtime_receipt") or []))
    report = REVIEWS_ROOT / "frontier71E_proxy_runtime_gap_analysis_and_repair_decision_report.md"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_semantics_repair(런타임 의미 수리)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(report),
        "notes": f"edge_margin_q40;completed={summary['completed_attempt_count']};signal_status={summary['signal_status']}",
        "family": "proxy_runtime_gap_analysis_and_repair(프록시/런타임 간극 분석 및 수리)",
        "primary_report": rel(report),
        "run_number": "frontier71E",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("runtime_receipt", [])),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "best_net_profit": best.get("net_profit"),
        "best_profit_factor": best.get("profit_factor"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "candidate_model_id": PRIMARY_CANDIDATE_ID,
        "net_profit": best.get("net_profit"),
        "profit_factor": best.get("profit_factor"),
        "drawdown": best.get("max_drawdown_percent"),
        "trade_count": best.get("trade_count"),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Semantics Repair(MT5 런타임 의미 수리)",
        "tier": "Tier A",
        "metric_scope": "runtime_repair_kpi(런타임 수리 KPI)",
        "scoreboard_lane": "runtime_repair(런타임 수리)",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(report),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f71e.md"),
        "created_at": created_at,
        "ledger_row_id": f"{RUN_ID}__runtime_semantics_repair",
        "subrun_id": "runtime_semantics_repair(런타임 의미 수리)",
        "record_view": "MT5 Runtime Semantics Repair(MT5 런타임 의미 수리)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_repair_kpi(런타임 수리 KPI)",
        "primary_kpi": f"best_pf={f71b.fmt(best.get('profit_factor'))};best_dd={f71b.fmt(best.get('max_drawdown_percent'))};tpd={f71b.fmt(best.get('trades_per_day'))}",
        "guardrail_kpi": f"signal_status={summary['signal_status']};feature_diff={f71b.fmt(best.get('feature_ready_diff'))}",
        "row_id": f"{RUN_ID}__runtime_semantics_repair",
        "evidence_boundary": "runtime_repair_observation_no_authority(런타임 수리 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can EA-compatible edge margin repair F71D signal count collapse?(EA 호환 엣지 마진이 F71D 신호 수 붕괴를 고칠 수 있나?)",
        "artifact_count": 12,
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f71e.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_runtime_repair(전선 런타임 수리)",
        "run_type": "runtime_semantics_repair(런타임 의미 수리)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT),
        "result_path": rel(report),
        "goal_achieve": "not_claimed",
        "source_authority": "F71D runtime probe + F71E Grok review(F71D 런타임 탐침 + F71E 그록 검토)",
        "trade_density": best.get("trades_per_day"),
        "max_drawdown_percent": best.get("max_drawdown_percent"),
    }


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = registry_row(payload, created_at)
    f71b.upsert_ledger(f71b.RUN_REGISTRY, "run_id", row)
    f71b.upsert_ledger(f71b.ALPHA_LEDGER, "ledger_row_id", row)
    f71b.upsert_ledger(f71b.STAGE_LEDGER, "ledger_row_id", row, source_header=f71b.ALPHA_LEDGER)


def append_idea(payload: Mapping[str, Any]) -> None:
    marker = "<!-- frontier71E_runtime_semantics_repair_probe_v1 -->"
    best = best_receipt(list(payload.get("runtime_receipt") or []))
    block = f"""
{marker}
- `{RUN_ID}` executed(실행): F71D signal count gap(신호 수 간극)을 threshold semantics mismatch(임계값 의미 불일치)로 진단하고, `edge_margin q40(엣지 마진 q40)` runtime semantics repair(런타임 의미 수리)를 MT5 Runtime Probe(MT5 런타임 탐침)로 실행했다. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(best.get('net_profit'))}/{f71b.fmt(best.get('profit_factor'))}/{f71b.fmt(best.get('max_drawdown_percent'))}/{f71b.fmt(best.get('trades_per_day'))}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier71E_proxy_runtime_gap_analysis_and_repair_decision_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    f71b.append_once(f71b.IDEA_REGISTRY, marker, block)


def write_state(payload: Mapping[str, Any], created_at: str) -> None:
    best = best_receipt(list(payload.get("runtime_receipt") or []))
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_retrospective_completed",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F71E runtime semantics repair(런타임 의미 수리)를 실행했다."',
        f'  - "Effect(효과): best runtime PF={f71b.fmt(best.get("profit_factor"))}, DD={f71b.fmt(best.get("max_drawdown_percent"))}, trades/day={f71b.fmt(best.get("trades_per_day"))}; next는 stage closeout review(단계 마감 검토) 또는 추가 수리 판단이다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f71b.WORKSPACE_STATE).write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")
    write_md(
        f71b.CURRENT_WORKING_STATE,
        [
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
            "Action(행동): F71E runtime semantics repair(런타임 의미 수리)를 실행했다.",
            "",
            "Effect(효과): F71D signal count gap(신호 수 간극)을 EA-compatible edge margin selection(EA 호환 엣지 마진 선택)으로 수리했는지 MT5에서 관찰했다.",
            "",
            f"- candidate(후보): `{PRIMARY_CANDIDATE_ID}`.",
            f"- repair(수리): `{REPAIR_AXIS_ID}`.",
            f"- best runtime net/PF/DD/trades_day(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(best.get('net_profit'))}` / `{f71b.fmt(best.get('profit_factor'))}` / `{f71b.fmt(best.get('max_drawdown_percent'))}` / `{f71b.fmt(best.get('trades_per_day'))}`.",
            f"- next action(다음 행동): `{NEXT_RUN_ID}`.",
            f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
        ],
    )
    write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        [
            "# F71 Selection Status(F71 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
            f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
            f"- status(상태): `{payload.get('status')}`",
            f"- judgment(판정): `{payload.get('judgment')}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            f"- current_boundary(현재 경계): `{CLAIM_BOUNDARY}`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        ],
    )


def main() -> int:
    args = parse_args()
    configure_f71d_globals()
    f71d.ensure_dirs()
    created_at = utc_now()
    if not path_exists(f71d.ROOT / GROK_CLEAN) or not path_exists(f71d.ROOT / GROK_METADATA):
        raise RuntimeError("missing F71E Grok review(F71E 그록 검토 누락)")
    context, sweep_rows = edge_margin_context()
    artifact, probability_rows, signal_rows = f71d.materialize_context(context, Path(args.common_files_root))
    attempts = f71d.build_attempts(context, artifact) if artifact.get("export_status") == "exported_selected_entry_tape_parity_passed" else []
    compile_payload = f71d.compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = f71d.execute_attempts(args, attempts, compile_payload)
        reports = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_ROOT,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution_results, reports)
    runtime_receipt = f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    gaps = f71d.gap_rows(runtime_receipt)
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    signal_status = repair_signal_status(runtime_receipt)
    if args.execute and completed:
        status = "completed_runtime_semantics_repair_observation_no_authority"
        judgment = (
            "runtime_semantics_signal_parity_repaired_economics_gap_remaining_no_authority"
            if signal_status == "signal_parity_repaired"
            else "runtime_semantics_repair_completed_signal_gap_remaining_no_authority"
        )
    elif args.execute:
        status = "blocked_runtime_semantics_repair_attempted_no_authority"
        judgment = "runtime_semantics_repair_blocked_no_authority"
    else:
        status = "materialized_runtime_semantics_repair_pending_mt5_no_authority"
        judgment = "runtime_semantics_repair_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "proxy_repair_sweep": sweep_rows,
        "f71d_gap_observation": f71d_gap_observation_rows(),
        "artifact_rows": [artifact],
        "probability_parity": probability_rows,
        "signal_parity": signal_rows,
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "gap_classification": gaps,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_outputs(payload, created_at)
    update_ledgers(payload, created_at)
    append_idea(payload)
    write_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
