from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_72 import frontier72b_trade_shape_exit_distribution_proxy_scout as f72b


STAGE_ID = f72b.STAGE_ID
RUN_ID = "frontier72C_trade_shape_label_feature_repair_or_pre_mt5_decision_v1"
PARENT_RUN_ID = f72b.RUN_ID
NEXT_MT5_RUN_ID = "frontier72D_pre_mt5_grok_trade_shape_runtime_probe_v1"
NEXT_REPAIR_RUN_ID = "frontier72C2_capped_trade_shape_density_dd_repair_v1"
CLAIM_BOUNDARY = (
    "proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f72b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f72b.REVIEWS_ROOT
SELECTED_ROOT = f72b.SELECTED_ROOT

F72B_TOP = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f72b_top_candidates.csv"
F72B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "frontier72B_proxy_summary.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = f72b.read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def parse_shape(shape_id: str) -> f72b.TradeShape:
    side, hold, stop, target = shape_id.split("_")
    return f72b.TradeShape(
        hold_bars=int(hold[1:]),
        stop_atr=float(stop[2:]),
        target_atr=float(target[2:]),
        direction=1 if side == "long" else -1,
    )


def required_inputs() -> list[Path]:
    return [F72B_TOP, F72B_SUMMARY, f72b.MODEL_INPUT, f72b.FEATURE_ORDER, f72b.RAW_US100]


def repair_label(path: Mapping[str, np.ndarray], shape: f72b.TradeShape, variant: str) -> np.ndarray:
    pnl = path["pnl"]
    quality = path["quality"]
    mae = path["mae_ratio"]
    mfe = path["mfe_ratio"]
    tuw = path["tuw_ratio"]
    if variant == "strict_quality_012":
        label = (pnl > 0) & (quality > 0.12) & (mae <= shape.stop_atr * 0.85) & (tuw <= 0.55)
    elif variant == "mfe_mae_gap_040":
        label = (pnl > 0) & ((mfe - mae) >= 0.40) & (mae <= shape.stop_atr) & (tuw <= 0.65)
    elif variant == "early_survival_045":
        label = (pnl > 0) & (quality > 0.02) & (mae <= shape.stop_atr * 0.75) & (tuw <= 0.45)
    elif variant == "dd_guard_balanced":
        label = (pnl > 0) & (quality > 0.08) & (mae <= shape.stop_atr * 0.70) & (mfe >= shape.target_atr * 0.55)
    else:
        label = path["label"] > 0
    return label.astype(float)


def selected_shapes() -> list[f72b.TradeShape]:
    top = pd.read_csv(io_path(F72B_TOP))
    shape_ids = list(dict.fromkeys(top["shape_id"].head(8).tolist()))
    shapes = [parse_shape(shape_id) for shape_id in shape_ids]
    extras = [
        f72b.TradeShape(12, 0.9, 1.8, -1),
        f72b.TradeShape(24, 0.9, 1.8, -1),
        f72b.TradeShape(24, 1.2, 2.4, -1),
        f72b.TradeShape(12, 0.9, 1.2, 1),
    ]
    seen = {shape.shape_id for shape in shapes}
    for shape in extras:
        if shape.shape_id not in seen:
            shapes.append(shape)
            seen.add(shape.shape_id)
    return shapes[:12]


def evaluate_repair() -> dict[str, Any]:
    model = pd.read_parquet(io_path(f72b.MODEL_INPUT))
    model["timestamp"] = pd.to_datetime(model["timestamp"], utc=True)
    raw = pd.read_csv(io_path(f72b.RAW_US100)).sort_values("time_close_unix").reset_index(drop=True)
    positions = f72b.align_raw(model, raw)
    features = [line.strip() for line in f72b.read_text(f72b.FEATURE_ORDER).splitlines() if line.strip()]
    bundles = f72b.feature_bundles(features)
    factories = f72b.model_factories()
    model_ids = ["small_nn_16", "extra_trees_ref", "hist_additive_tree"]
    target_tpd_values = [1.5, 2.5, 3.5, 5.0]
    label_variants = ["strict_quality_012", "mfe_mae_gap_040", "early_survival_045", "dd_guard_balanced"]
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for shape in selected_shapes():
        path = f72b.compute_shape_path(model, raw, positions, shape)
        for label_variant in label_variants:
            y = repair_label(path, shape, label_variant)
            for bundle_id, bundle_features in bundles.items():
                for model_id in model_ids:
                    try:
                        scores, train_info = f72b.train_and_score(model, bundle_features, y, factories[model_id])
                    except Exception as exc:  # noqa: BLE001 - repair failure is evidence.
                        failures.append({
                            "shape_id": shape.shape_id,
                            "label_variant": label_variant,
                            "bundle_id": bundle_id,
                            "model_id": model_id,
                            "error": type(exc).__name__,
                            "message": str(exc)[:180],
                        })
                        continue
                    for target_tpd in target_tpd_values:
                        row = {
                            "candidate_id": f"f72c_{len(rows) + 1:04d}",
                            "shape_id": shape.shape_id,
                            "label_variant": label_variant,
                            "bundle_id": bundle_id,
                            "model_id": model_id,
                            "target_trades_day": target_tpd,
                            "feature_count": len(bundle_features),
                            **train_info,
                            **f72b.evaluate_candidate(model, scores, path, target_tpd),
                        }
                        row["scout_clue"] = f72b.is_scout(row)
                        row["meaningful_candidate"] = f72b.is_meaningful(row)
                        row["final_like_reference_only"] = (
                            row["meaningful_candidate"]
                            and row["validation_profit_factor"] >= 2.0
                            and row["oos_profit_factor"] >= 2.0
                            and 5.0 <= row["validation_trades_day"] <= 10.0
                            and 5.0 <= row["oos_trades_day"] <= 10.0
                        )
                        rows.append(row)
    ranked = sorted(
        rows,
        key=lambda row: (
            bool(row["meaningful_candidate"]),
            bool(row["scout_clue"]),
            row["oos_profit_factor"],
            row["oos_net_profit"],
            -abs(row["oos_trades_day"] - 5.0),
        ),
        reverse=True,
    )
    best = ranked[0] if ranked else {}
    selected_path = {}
    selected_scores = None
    if best:
        shape = parse_shape(best["shape_id"])
        selected_path = f72b.compute_shape_path(model, raw, positions, shape)
        y = repair_label(selected_path, shape, best["label_variant"])
        scores, _ = f72b.train_and_score(model, bundles[best["bundle_id"]], y, factories[best["model_id"]])
        selected_scores = scores
    return {
        "model": model,
        "candidate_rows": rows,
        "failure_rows": failures,
        "ranked_rows": ranked,
        "best": best,
        "selected_path": selected_path,
        "selected_scores": selected_scores,
    }


def summary_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    rows = result["candidate_rows"]
    best = result["best"]
    scout_count = sum(1 for row in rows if row["scout_clue"])
    meaningful_count = sum(1 for row in rows if row["meaningful_candidate"])
    final_like = sum(1 for row in rows if row["final_like_reference_only"])
    next_run = NEXT_MT5_RUN_ID if scout_count > 0 else NEXT_REPAIR_RUN_ID
    judgment = (
        "proxy_repair_preserved_scout_clue_pre_mt5_required_no_authority"
        if scout_count > 0 and meaningful_count == 0
        else "proxy_repair_meaningful_candidate_pre_mt5_required_no_authority"
        if meaningful_count > 0
        else "proxy_repair_zero_signal_capped_repair_required_no_authority"
    )
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "proxy_repair_completed",
        "judgment": judgment,
        "candidate_count": len(rows),
        "model_failure_count": len(result["failure_rows"]),
        "scout_clue_count": scout_count,
        "meaningful_candidate_count": meaningful_count,
        "final_like_reference_only_count": final_like,
        "best_candidate": best,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": utc_now(),
    }


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    best = summary["best_candidate"]
    return [
        "# Frontier72C Trade-Shape Label/Feature Repair(F72C 거래 형태 라벨/피처 수리)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- candidate_count(후보 수): `{summary['candidate_count']}`",
        f"- scout_clue_count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary['meaningful_candidate_count']}`",
        f"- final_like_reference_only_count(최종 유사 참조 전용 수): `{summary['final_like_reference_only_count']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Best Repair Candidate(최선 수리 후보)",
        "",
        f"- candidate_id(후보 ID): `{best.get('candidate_id', '')}`",
        f"- shape/label/model/bundle(형태/라벨/모델/묶음): `{best.get('shape_id', '')}` / `{best.get('label_variant', '')}` / `{best.get('model_id', '')}` / `{best.get('bundle_id', '')}`",
        f"- validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `{best.get('validation_net_profit', 0):.4f}` / `{best.get('validation_profit_factor', 0):.4f}` / `{best.get('validation_max_drawdown_percent', 0):.4f}%` / `{best.get('validation_trades_day', 0):.4f}`",
        f"- OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net_profit', 0):.4f}` / `{best.get('oos_profit_factor', 0):.4f}` / `{best.get('oos_max_drawdown_percent', 0):.4f}%` / `{best.get('oos_trades_day', 0):.4f}`",
        f"- scout/meaningful/final-like(탐색/의미/최종 유사): `{best.get('scout_clue', False)}` / `{best.get('meaningful_candidate', False)}` / `{best.get('final_like_reference_only', False)}`",
        "",
        "## Repair Interpretation(수리 해석)",
        "",
        "Effect(효과): F72C는 라벨 엄격도와 피처 묶음을 바꿔 F72B scout clue(탐색 단서)를 유지/확대할 수 있는지 본다. 이 결과는 아직 proxy-only(프록시 전용)이며 runtime probe(런타임 탐침)를 대체하지 않는다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{summary['next_run_id']}`.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F72C Required Gate Coverage Audit(F72C 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| parent_proxy(F72B 프록시) | pass(통과) | `{rel(F72B_SUMMARY)}` | F72B scout clue(탐색 단서)에서 수리 출발 |",
        f"| repair_not_same_threshold(동일 임계값 반복 아님) | pass(통과) | `{rel(RUN_ROOT / 'f72c_repair_candidate_summary.csv')}` | label_variant(라벨 변형)와 feature bundle(피처 묶음)을 변경 |",
        f"| proxy_repair_kpi(프록시 수리 KPI) | pass(통과) | `{rel(REVIEWS_ROOT / 'frontier72C_trade_shape_label_feature_repair_report.md')}` | 수리 KPI 기록 |",
        f"| mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침) | pending_next(다음 대기) | `{summary['next_run_id']}` | scout clue가 남으면 pre-MT5 Grok 후 탐침으로 이동 |",
        f"| final_claim_guard(최종 주장 보호) | pass(통과) | `{CLAIM_BOUNDARY}` | 금지 주장 없음 |",
    ]


def selection_status_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F72 Selection Status(F72 선택 상태)",
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
    ]


def run_manifest(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": summary["next_run_id"],
        "status": summary["status"],
        "judgment": summary["judgment"],
        "candidate_count": summary["candidate_count"],
        "scout_clue_count": summary["scout_clue_count"],
        "meaningful_candidate_count": summary["meaningful_candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "artifacts": [
            rel(RUN_ROOT / "f72c_repair_candidate_summary.csv"),
            rel(RUN_ROOT / "f72c_top_repair_candidates.csv"),
            rel(REVIEWS_ROOT / "frontier72C_trade_shape_label_feature_repair_report.md"),
        ],
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    best = summary["best_candidate"]
    row = {
        **f72b.ledger_row(summary),
        "ledger_row_id": f"{RUN_ID}__proxy_repair",
        "row_id": f"{RUN_ID}__proxy_repair",
        "run_id": RUN_ID,
        "subrun_id": "proxy_repair(프록시 수리)",
        "parent_run_id": PARENT_RUN_ID,
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(REVIEWS_ROOT / "frontier72C_trade_shape_label_feature_repair_report.md"),
        "primary_kpi": f"candidates={summary['candidate_count']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_candidate_count']}",
        "guardrail_kpi": f"best_oos_pf={best.get('oos_profit_factor', 0):.4f}; best_oos_tpd={best.get('oos_trades_day', 0):.4f}; mt5_probe=pending_next",
        "run_number": "frontier72C",
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["candidate_count"],
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72c.md"),
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72c.md"),
        "primary_artifact": rel(RUN_ROOT / "f72c_repair_candidate_summary.csv"),
        "candidate_model_id": best.get("candidate_id", ""),
        "net_profit": best.get("oos_net_profit", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_max_drawdown_percent", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "best_model_id": best.get("model_id", ""),
        "result_path": rel(REVIEWS_ROOT / "frontier72C_trade_shape_label_feature_repair_report.md"),
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "claim_boundary": CLAIM_BOUNDARY,
        "evidence_boundary": "proxy_repair_only_no_runtime(프록시 수리 전용, 런타임 없음)",
        "work_family": "experiment_execution(실험 실행)",
        "run_type": "trade_shape_label_feature_repair(거래 형태 라벨/피처 수리)",
    }
    f72b.upsert_ledger(f72b.ALPHA_LEDGER, "ledger_row_id", row)
    f72b.upsert_ledger(f72b.RUN_REGISTRY, "run_id", row)
    f72b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f72b.ALPHA_LEDGER)


def update_registers(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier72C_trade_shape_label_feature_repair_or_pre_mt5_decision_v1 -->"
    best = summary["best_candidate"]
    block = f"""<!-- frontier72C_trade_shape_label_feature_repair_or_pre_mt5_decision_v1 -->
- `{RUN_ID}` executed F72 label/feature repair(F72 라벨/피처 수리). Result(결과): `{summary['judgment']}`. Candidates(후보) `{summary['candidate_count']}`, scout clue(탐색 단서) `{summary['scout_clue_count']}`, meaningful candidate(의미 후보) `{summary['meaningful_candidate_count']}`. Best OOS(최선 표본외) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{best.get('oos_net_profit', 0):.4f}/{best.get('oos_profit_factor', 0):.4f}/{best.get('oos_max_drawdown_percent', 0):.4f}/{best.get('oos_trades_day', 0):.4f}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier72C_trade_shape_label_feature_repair_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{summary['next_run_id']}`."""
    append_once(f72b.IDEA_REGISTRY, marker, block)


def update_state(summary: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {summary['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {summary['next_run_id']}",
        "runtime_probe_status: f72_mandatory_runtime_probe_pending_after_repair",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f71_closeout",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "notes:",
        f'  - "Action(행동): F72C label/feature repair(라벨/피처 수리)를 실행했다. Candidates(후보) {summary["candidate_count"]}, scout clue(탐색 단서) {summary["scout_clue_count"]}, meaningful(의미 후보) {summary["meaningful_candidate_count"]}."',
        f'  - "Effect(효과): scout clue(탐색 단서)가 남아 다음 행동을 {summary["next_run_id"]}로 설정했다. Runtime probe(런타임 탐침)는 아직 pending(대기)이다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f72b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    current = [
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
        "Action(행동): F72C label/feature repair(라벨/피처 수리)를 실행했다.",
        "",
        f"Effect(효과): 후보 `{summary['candidate_count']}`개 중 scout clue(탐색 단서) `{summary['scout_clue_count']}`개, meaningful candidate(의미 후보) `{summary['meaningful_candidate_count']}`개를 기록했고, 다음 행동을 `{summary['next_run_id']}`로 설정했다.",
        "",
        f"- judgment(판정): `{summary['judgment']}`.",
        f"- best OOS PF(최선 표본외 수익 팩터): `{summary['best_candidate'].get('oos_profit_factor', 0):.4f}`.",
        "- runtime probe(런타임 탐침): pending after pre-MT5 Grok(사전 MT5 Grok 뒤 대기).",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_text(f72b.CURRENT_WORKING_STATE, current)


def write_outputs(result: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ranked = result["ranked_rows"]
    write_csv(RUN_ROOT / "f72c_repair_candidate_summary.csv", result["candidate_rows"])
    write_csv(RUN_ROOT / "f72c_top_repair_candidates.csv", ranked[:25])
    write_csv(RUN_ROOT / "f72c_repair_model_failures.csv", result["failure_rows"])
    trade_rows = f72b.selected_trade_rows(result["model"], summary["best_candidate"], result["selected_path"], result["selected_scores"])
    write_csv(RUN_ROOT / "f72c_top_repair_candidate_trades.csv", trade_rows)
    write_json(RUN_ROOT / "frontier72C_repair_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_text(RUN_ROOT / "reports/result_summary.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "frontier72C_trade_shape_label_feature_repair_report.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f72c.md", gate_audit_lines(summary))
    write_text(SELECTED_ROOT / "selection_status.md", selection_status_lines(summary))


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F72C required material missing: {missing}")
    result = evaluate_repair()
    summary = summary_payload(result)
    write_outputs(result, summary)
    update_registers(summary)
    update_ledgers(summary)
    update_state(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "candidate_count": summary["candidate_count"],
        "scout_clue_count": summary["scout_clue_count"],
        "meaningful_candidate_count": summary["meaningful_candidate_count"],
        "next_run_id": summary["next_run_id"],
        "best_oos_net": summary["best_candidate"].get("oos_net_profit", 0),
        "best_oos_pf": summary["best_candidate"].get("oos_profit_factor", 0),
        "best_oos_dd": summary["best_candidate"].get("oos_max_drawdown_percent", 0),
        "best_oos_trades_day": summary["best_candidate"].get("oos_trades_day", 0),
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
