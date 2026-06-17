from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_71 import frontier71b_economics_native_proxy_scout as f71b


STAGE_ID = f71b.STAGE_ID
RUN_ID = "frontier71C_economics_native_repair_recombine_proxy_v1"
PARENT_RUN_ID = f71b.RUN_ID
NEXT_RUN_IF_SCOUT = "frontier71D_pre_mt5_grok_runtime_probe_economics_native_scout_v1"
NEXT_RUN_IF_NO_SCOUT = "frontier71D_mandatory_probe_or_closeout_logic_review_v1"
CLAIM_BOUNDARY = f71b.CLAIM_BOUNDARY

STAGE_ROOT = f71b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f71b.REVIEWS_ROOT

F71B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f71b_proxy_summary.json"
F71B_CANDIDATES = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f71b_candidate_summary.csv"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
SUMMARY_JSON = RUN_ROOT / "f71c_repair_summary.json"
CANDIDATE_CSV = RUN_ROOT / "f71c_repair_candidate_summary.csv"
KPI_CSV = RUN_ROOT / "f71c_repair_kpi_by_split.csv"
FRACTURE_CSV = RUN_ROOT / "f71c_repair_density_lift_fracture.csv"
TIER_CSV = RUN_ROOT / "f71c_tier_record_status.csv"
ENTRY_CSV = RUN_ROOT / "f71c_scout_entry_rows.csv"

REPORT = REVIEWS_ROOT / "frontier71C_economics_native_repair_recombine_proxy_report.md"
CANDIDATE_REVIEW_CSV = REVIEWS_ROOT / "f71c_repair_candidate_summary_review.csv"
KPI_REVIEW_CSV = REVIEWS_ROOT / "f71c_repair_kpi_by_split_review.csv"
FRACTURE_REVIEW_CSV = REVIEWS_ROOT / "f71c_repair_density_lift_fracture_review.csv"
TIER_REVIEW_CSV = REVIEWS_ROOT / "f71c_tier_record_status_review.csv"
GATE_AUDIT = REVIEWS_ROOT / "required_gate_coverage_audit_f71c.md"


@dataclass(frozen=True)
class RepairSelection:
    selection_id: str
    mask_name: str
    threshold_quantile: float
    entry_gap_bars: int


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repair_label_specs() -> list[f71b.LabelSpec]:
    rows = [
        ("density_h12_fast", 12, 0.70, 0.42, "first_hit_net", 0.08, 0.40, 0.10),
        ("density_h12_guard", 12, 0.75, 0.45, "dd_guarded", 0.08, 0.55, 0.06),
        ("density_h15_bal", 15, 0.85, 0.50, "path_balanced", 0.09, 0.48, 0.18),
        ("density_h15_guard", 15, 0.90, 0.52, "dd_guarded", 0.09, 0.62, 0.06),
        ("f71b_h18_retest", 18, 1.05, 0.70, "first_hit_net", 0.12, 0.55, 0.10),
        ("h18_tighter_dd", 18, 0.95, 0.55, "dd_guarded", 0.10, 0.68, 0.05),
        ("h18_path_bal", 18, 0.98, 0.62, "path_balanced", 0.10, 0.52, 0.20),
        ("h24_slow_guard", 24, 0.90, 0.48, "dd_guarded", 0.08, 0.72, 0.04),
    ]
    return [
        f71b.LabelSpec(
            label_id=f"repair_{name}_{mode}_h{h}_tp{int(tp*100)}_sl{int(sl*100)}",
            horizon_bars=h,
            tp_atr=tp,
            sl_atr=sl,
            utility_mode=mode,
            min_edge_atr=edge,
            adverse_penalty=penalty,
            close_weight=close_weight,
        )
        for name, h, tp, sl, mode, edge, penalty, close_weight in rows
    ]


def repair_feature_sets(frame: pd.DataFrame) -> list[f71b.FeatureSet]:
    keep = {"econ_core_price_v1", "econ_no_macro_v1", "econ_macro_context_v1", "econ_risk_path_v1"}
    return [item for item in f71b.feature_sets(frame) if item.feature_set_id in keep]


def repair_model_specs() -> list[f71b.ModelSpec]:
    return [
        f71b.ModelSpec(
            "extratrees_dense_leaf45_depth9_v1",
            "extra_trees_density_repair(엑스트라트리스 밀도 수리)",
            "density_repair(밀도 수리)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                ExtraTreesClassifier(
                    n_estimators=72,
                    max_depth=9,
                    min_samples_leaf=45,
                    max_features="sqrt",
                    class_weight="balanced",
                    random_state=711,
                    n_jobs=1,
                ),
            ),
        ),
        f71b.ModelSpec(
            "extratrees_leaf70_depth8_v1",
            "extra_trees_quality_repair(엑스트라트리스 품질 수리)",
            "quality_repair(품질 수리)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                ExtraTreesClassifier(
                    n_estimators=72,
                    max_depth=8,
                    min_samples_leaf=70,
                    max_features="sqrt",
                    class_weight="balanced",
                    random_state=712,
                    n_jobs=1,
                ),
            ),
        ),
        f71b.ModelSpec(
            "histgb_density_leaf16_v1",
            "hist_gradient_boosting_density(히스토그램 부스팅 밀도)",
            "nonlinear_density_repair(비선형 밀도 수리)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                HistGradientBoostingClassifier(
                    max_iter=72,
                    max_leaf_nodes=16,
                    learning_rate=0.06,
                    l2_regularization=0.05,
                    random_state=713,
                ),
            ),
        ),
    ]


def repair_selections() -> list[RepairSelection]:
    specs: list[RepairSelection] = []
    for mask in ("all", "cash", "vol_expansion", "trend", "early_late"):
        for quantile in (0.20, 0.30, 0.40):
            gap = 6 if quantile <= 0.30 else 9
            specs.append(RepairSelection(f"{mask}_q{int(quantile*100)}_gap{gap}", mask, quantile, gap))
    return specs


def selected_mask(frame: pd.DataFrame, score: np.ndarray, spec: RepairSelection, threshold: float) -> np.ndarray:
    active = (score >= threshold) & f71b.mask_for(frame, spec.mask_name)
    selected = set(f71b.non_overlap_indices(active, spec.entry_gap_bars))
    return np.array([idx in selected for idx in range(len(frame))], dtype=bool)


def threshold(score: np.ndarray, train_mask: np.ndarray, mask: np.ndarray, quantile: float) -> float | None:
    values = score[train_mask & mask]
    values = values[np.isfinite(values)]
    if len(values) < 80:
        return None
    return float(np.quantile(values, quantile))


def f71b_context() -> dict[str, Any]:
    summary = json.loads(io_path(F71B_SUMMARY).read_text(encoding="utf-8"))
    candidates = pd.read_csv(io_path(F71B_CANDIDATES))
    scout_count = int(candidates["scout_clue"].astype(str).str.lower().eq("true").sum())
    top = candidates.iloc[0].to_dict() if len(candidates) else {}
    return {"summary": summary, "scout_count": scout_count, "top": top}


def gate_flags(summary: Mapping[str, Any]) -> dict[str, bool]:
    return f71b.gate_flags(summary)


def run_repair(created_at: str) -> dict[str, Any]:
    previous = f71b_context()
    frame = f71b.load_frame()
    train_mask = f71b.split_mask(frame, "train")
    labels = repair_label_specs()
    features = repair_feature_sets(frame)
    models = repair_model_specs()
    selections = repair_selections()
    candidate_rows: list[dict[str, Any]] = []
    kpi_rows: list[dict[str, Any]] = []
    fracture_rows: list[dict[str, Any]] = []
    entry_rows: list[dict[str, Any]] = []

    for label_spec in labels:
        label, long_profit, short_profit, best_utility = f71b.build_label(frame, label_spec)
        y_train = label.loc[train_mask]
        directional = int(np.count_nonzero(y_train.to_numpy() != 0))
        if y_train.nunique() < 2 or directional < 150:
            continue
        weights = f71b.sample_weight(frame, label, best_utility)[train_mask]
        for feature_set in features:
            x_train = frame.loc[train_mask, feature_set.columns]
            x_all = frame.loc[:, feature_set.columns]
            for model_spec in models:
                model = model_spec.build()
                try:
                    f71b.fit_model(model, x_train, y_train, weights)
                    side, score = f71b.side_scores(model, x_all)
                except Exception as exc:
                    candidate_rows.append(
                        {
                            "candidate_id": "f71c_fit_failed_" + f71b.stable_id([label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, str(exc)]),
                            "status": "fit_failed(학습 실패)",
                            "error": str(exc)[:200],
                        }
                    )
                    continue
                for selection in selections:
                    mask = f71b.mask_for(frame, selection.mask_name)
                    th = threshold(score, train_mask, mask, selection.threshold_quantile)
                    if th is None:
                        continue
                    candidate_id = "f71c_" + f71b.stable_id([label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, selection.selection_id])
                    sel_mask = selected_mask(frame, score, selection, th)
                    split_rows = f71b.evaluate_splits(frame, sel_mask, side, long_profit, short_profit)
                    by_split = {row["split"]: row for row in split_rows}
                    val = by_split.get("validation", {})
                    oos = by_split.get("oos", {})
                    relaxed_q = max(0.10, selection.threshold_quantile - 0.10)
                    relaxed_gap = max(4, selection.entry_gap_bars - 2)
                    rth = threshold(score, train_mask, mask, relaxed_q)
                    rval: dict[str, Any] = {}
                    roos: dict[str, Any] = {}
                    if rth is not None:
                        rsel = selected_mask(frame, score, RepairSelection(selection.selection_id + "_relaxed", selection.mask_name, relaxed_q, relaxed_gap), rth)
                        relaxed_rows = f71b.evaluate_splits(frame, rsel, side, long_profit, short_profit)
                        relaxed_by_split = {row["split"]: row for row in relaxed_rows}
                        rval = relaxed_by_split.get("validation", {})
                        roos = relaxed_by_split.get("oos", {})
                    fracture_pass = bool(
                        rval.get("profit_factor", 0.0) >= 1.10
                        and roos.get("profit_factor", 0.0) >= 1.10
                        and rval.get("max_drawdown_percent", 999.0) <= 12.0
                        and roos.get("max_drawdown_percent", 999.0) <= 12.0
                    )
                    summary = {
                        "candidate_id": candidate_id,
                        "label_id": label_spec.label_id,
                        "horizon_bars": label_spec.horizon_bars,
                        "tp_atr": label_spec.tp_atr,
                        "sl_atr": label_spec.sl_atr,
                        "feature_set_id": feature_set.feature_set_id,
                        "feature_count": len(feature_set.columns),
                        "model_id": model_spec.model_id,
                        "model_family": model_spec.model_family,
                        "selection_id": selection.selection_id,
                        "mask_name": selection.mask_name,
                        "entry_gap_bars": selection.entry_gap_bars,
                        "threshold_quantile": selection.threshold_quantile,
                        "threshold": th,
                        "density_lift_fracture_pass": fracture_pass,
                        "validation_net_profit": val.get("net_profit", 0.0),
                        "validation_gross_profit": val.get("gross_profit", 0.0),
                        "validation_gross_loss": val.get("gross_loss", 0.0),
                        "validation_profit_factor": val.get("profit_factor", 0.0),
                        "validation_max_drawdown_percent": val.get("max_drawdown_percent", 0.0),
                        "validation_trade_count": val.get("trade_count", 0),
                        "validation_trades_day": val.get("trades_day", 0.0),
                        "validation_win_rate": val.get("win_rate", 0.0),
                        "validation_expectancy": val.get("expectancy", 0.0),
                        "validation_recovery_factor": val.get("recovery_factor", 0.0),
                        "validation_smooth_equity_proxy": val.get("smooth_equity_proxy", False),
                        "oos_net_profit": oos.get("net_profit", 0.0),
                        "oos_gross_profit": oos.get("gross_profit", 0.0),
                        "oos_gross_loss": oos.get("gross_loss", 0.0),
                        "oos_profit_factor": oos.get("profit_factor", 0.0),
                        "oos_max_drawdown_percent": oos.get("max_drawdown_percent", 0.0),
                        "oos_trade_count": oos.get("trade_count", 0),
                        "oos_trades_day": oos.get("trades_day", 0.0),
                        "oos_win_rate": oos.get("win_rate", 0.0),
                        "oos_expectancy": oos.get("expectancy", 0.0),
                        "oos_recovery_factor": oos.get("recovery_factor", 0.0),
                        "oos_smooth_equity_proxy": oos.get("smooth_equity_proxy", False),
                    }
                    flags = gate_flags(summary)
                    summary.update(flags)
                    summary["meaningful_with_fracture"] = bool(flags["meaningful_candidate"] and fracture_pass)
                    candidate_rows.append(summary)
                    for row in split_rows:
                        kpi_rows.append(
                            {
                                "candidate_id": candidate_id,
                                "label_id": label_spec.label_id,
                                "feature_set_id": feature_set.feature_set_id,
                                "model_id": model_spec.model_id,
                                "selection_id": selection.selection_id,
                                "split": row["split"],
                                **{key: value for key, value in row.items() if key != "split"},
                            }
                        )
                    fracture_rows.append(
                        {
                            "candidate_id": candidate_id,
                            "selection_id": selection.selection_id,
                            "relaxed_quantile": relaxed_q,
                            "relaxed_entry_gap_bars": relaxed_gap,
                            "validation_profit_factor": rval.get("profit_factor", 0.0),
                            "validation_max_drawdown_percent": rval.get("max_drawdown_percent", 0.0),
                            "validation_trades_day": rval.get("trades_day", 0.0),
                            "oos_profit_factor": roos.get("profit_factor", 0.0),
                            "oos_max_drawdown_percent": roos.get("max_drawdown_percent", 0.0),
                            "oos_trades_day": roos.get("trades_day", 0.0),
                            "fracture_pass": fracture_pass,
                        }
                    )
                    if flags["scout_clue"] or flags["meaningful_candidate"]:
                        entry_rows.extend(f71b.entry_rows(frame, candidate_id, sel_mask, side, score, long_profit, short_profit, limit=5000))

    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row.get("final_like_reference_only")),
            bool(row.get("meaningful_with_fracture")),
            bool(row.get("meaningful_candidate")),
            bool(row.get("scout_clue")),
            min(float(row.get("validation_trades_day") or 0.0), float(row.get("oos_trades_day") or 0.0)),
            float(row.get("oos_profit_factor") or 0.0),
            float(row.get("validation_profit_factor") or 0.0),
            float(row.get("oos_net_profit") or 0.0),
        ),
        reverse=True,
    )
    scout = [row for row in ranked if row.get("scout_clue")]
    meaningful = [row for row in ranked if row.get("meaningful_candidate")]
    meaningful_fracture = [row for row in ranked if row.get("meaningful_with_fracture")]
    final_like = [row for row in ranked if row.get("final_like_reference_only")]
    any_scout = bool(scout) or previous["scout_count"] > 0
    status = "completed_repair_meaningful_candidate_no_authority" if meaningful else (
        "completed_repair_scout_clue_runtime_probe_required_no_authority" if any_scout else "completed_repair_no_scout_logic_review_required_no_authority"
    )
    judgment = "repair_found_meaningful_candidate_needs_grok_then_mt5_probe_no_authority" if meaningful else (
        "repair_kept_scout_clue_but_density_goal_not_met_probe_required_no_authority" if any_scout else "repair_failed_no_scout_clue_logic_review_no_authority"
    )
    next_run = NEXT_RUN_IF_SCOUT if any_scout else NEXT_RUN_IF_NO_SCOUT
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_count": len([row for row in candidate_rows if not str(row.get("status", "")).startswith("fit_failed")]),
        "fit_failed_count": len([row for row in candidate_rows if str(row.get("status", "")).startswith("fit_failed")]),
        "scout_clue_count": len(scout),
        "meaningful_candidate_count": len(meaningful),
        "meaningful_with_fracture_count": len(meaningful_fracture),
        "final_like_reference_only_count": len(final_like),
        "previous_scout_clue_count": previous["scout_count"],
        "previous_top_candidate": previous["top"].get("candidate_id", ""),
        "top_candidates": ranked[:15],
        "candidate_rows": ranked,
        "kpi_rows": kpi_rows,
        "fracture_rows": fracture_rows,
        "entry_rows": entry_rows,
    }


def tier_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    return [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A full-context model input(Tier A 전체 문맥 모델 입력)",
            "status": "completed_proxy_repair(프록시 수리 완료)",
            "judgment": result["judgment"],
            "net_profit": top.get("oos_net_profit", ""),
            "profit_factor": top.get("oos_profit_factor", ""),
            "drawdown": top.get("oos_max_drawdown_percent", ""),
            "trade_count": top.get("oos_trade_count", ""),
            "trades_day": top.get("oos_trades_day", ""),
            "notes": "F71C repair materialized Tier A only(F71C 수리는 Tier A만 물질화).",
        },
        {
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B partial-context sample(Tier B 부분 문맥 표본)",
            "status": "missing_required(필수 누락)",
            "judgment": "not_materialized_in_f71c_proxy_repair(F71C 프록시 수리에서 미물질화)",
            "notes": "Recorded as missing_required, not omitted(필수 누락으로 기록, 생략 아님).",
        },
        {
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "combined record(합산 기록)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "judgment": "no_synthetic_combined_claim_without_tier_b(Tier B 없이 합성 합산 주장 없음)",
            "notes": "No combined read because Tier B is not materialized(Tier B 미물질화로 합산 판독 없음).",
        },
    ]


def report_lines(result: Mapping[str, Any]) -> list[str]:
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    return [
        "# Frontier71C Economics-Native Repair/Recombine Proxy(F71C 경제성 네이티브 수리/재조합 프록시)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Repair Hypothesis(수리 가설)",
        "",
        "F71B found PF/DD scout clues(수익 팩터/손실폭 탐색 단서) but density(밀도)가 너무 낮았다. F71C changes label horizon(라벨 수평선), entry gap(진입 간격), feature recombination(피처 재조합), and tree density(트리 밀도) together.",
        "",
        "Effect(효과): this is not only threshold loosening(임계값 완화만이 아님); it changes selection semantics(선택 의미) and trade cadence(거래 리듬).",
        "",
        "## KPI Summary(KPI 요약)",
        "",
        f"- candidates tested(시험 후보): `{result['candidate_count']}`",
        f"- previous F71B scout clues(이전 F71B 탐색 단서): `{result['previous_scout_clue_count']}`",
        f"- F71C scout clues(F71C 탐색 단서): `{result['scout_clue_count']}`",
        f"- meaningful candidates(의미 후보): `{result['meaningful_candidate_count']}`",
        f"- meaningful with fracture(밀도 균열 통과 의미 후보): `{result['meaningful_with_fracture_count']}`",
        f"- final-like reference-only(최종 유사 참조 전용): `{result['final_like_reference_only_count']}`",
        "",
        "## Top Repair Row(상위 수리 행)",
        "",
        f"- candidate(후보): `{top.get('candidate_id', 'none')}`",
        f"- validation net/PF/DD/trades/day(검증 순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(top.get('validation_net_profit'))}` / `{f71b.fmt(top.get('validation_profit_factor'))}` / `{f71b.fmt(top.get('validation_max_drawdown_percent'))}` / `{f71b.fmt(top.get('validation_trades_day'))}`",
        f"- OOS net/PF/DD/trades/day(표본외 순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(top.get('oos_net_profit'))}` / `{f71b.fmt(top.get('oos_profit_factor'))}` / `{f71b.fmt(top.get('oos_max_drawdown_percent'))}` / `{f71b.fmt(top.get('oos_trades_day'))}`",
        f"- label/feature/model/selection(라벨/피처/모델/선택): `{top.get('label_id', '')}` / `{top.get('feature_set_id', '')}` / `{top.get('model_id', '')}` / `{top.get('selection_id', '')}`",
        "",
        "## Runtime Probe Position(런타임 탐침 위치)",
        "",
        f"- next action(다음 행동): `{result['next_run_id']}`",
        "- runtime probe KPI(런타임 탐침 KPI): pending(대기).",
        "- proxy/runtime gap(프록시/런타임 간극): pending until MT5 Runtime Probe(MT5 런타임 탐침 전까지 대기).",
    ]


def gate_audit_lines(result: Mapping[str, Any]) -> list[str]:
    return [
        "# Required Gate Coverage Audit F71C(필수 게이트 커버리지 감사 F71C)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| F71B scout clue input(F71B 탐색 단서 입력) | passed(통과) | `{f71b.rel(F71B_SUMMARY)}` | repair source(수리 원천) 고정 |",
        f"| repair execution(수리 실행) | passed(통과) | `{f71b.rel(SUMMARY_JSON)}` | density repair(밀도 수리) 물질화 |",
        f"| Tier paired records(티어 쌍 기록) | passed_with_missing_required(필수 누락 포함 통과) | `{f71b.rel(TIER_CSV)}` | Tier B 미물질화 숨김 방지 |",
        f"| MT5 runtime probe(MT5 런타임 탐침) | pending(대기) | next `{result['next_run_id']}` | mandatory probe(필수 탐침)로 이동 |",
        f"| forbidden claim guard(금지 주장 보호) | passed(통과) | `{CLAIM_BOUNDARY}` | 금지 주장 없음 |",
    ]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    f71b.write_csv(path, rows)


def write_outputs(result: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "inputs": {"f71b_summary": f71b.rel(F71B_SUMMARY), "f71b_candidates": f71b.rel(F71B_CANDIDATES)},
        "outputs": {"summary": f71b.rel(SUMMARY_JSON), "candidates": f71b.rel(CANDIDATE_CSV), "report": f71b.rel(REPORT)},
        "claim_boundary": CLAIM_BOUNDARY,
    }
    f71b.write_json(RUN_MANIFEST, manifest)
    summary = {key: value for key, value in result.items() if key not in {"candidate_rows", "kpi_rows", "fracture_rows", "entry_rows"}}
    f71b.write_json(SUMMARY_JSON, summary)
    write_csv(CANDIDATE_CSV, result["candidate_rows"])
    write_csv(KPI_CSV, result["kpi_rows"])
    write_csv(FRACTURE_CSV, result["fracture_rows"])
    write_csv(TIER_CSV, tier_rows(result))
    write_csv(ENTRY_CSV, result["entry_rows"])
    write_csv(CANDIDATE_REVIEW_CSV, result["candidate_rows"])
    write_csv(KPI_REVIEW_CSV, result["kpi_rows"])
    write_csv(FRACTURE_REVIEW_CSV, result["fracture_rows"])
    write_csv(TIER_REVIEW_CSV, tier_rows(result))
    f71b.write_md(REPORT, report_lines(result))
    f71b.write_md(GATE_AUDIT, gate_audit_lines(result))


def registry_row(result: Mapping[str, Any]) -> dict[str, Any]:
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_repair(프록시 수리)",
        "status": result["status"],
        "judgment": result["judgment"],
        "path": f71b.rel(REPORT),
        "notes": f"candidates={result['candidate_count']};scout={result['scout_clue_count']};meaningful={result['meaningful_candidate_count']};previous_scout={result['previous_scout_clue_count']}",
        "family": "economics_native_repair_recombine(경제성 네이티브 수리/재조합)",
        "primary_report": f71b.rel(REPORT),
        "run_number": "frontier71C",
        "date": "2026-06-17",
        "decision": result["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": result["next_run_id"],
        "rows": result["candidate_count"],
        "gate_passes": result["scout_clue_count"],
        "gate_total": result["candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f71b.rel(REPORT),
        "candidate_rows": result["candidate_count"],
        "positive_proxy_rows": result["scout_clue_count"],
        "best_model_id": top.get("model_id", ""),
        "best_proxy_net": top.get("oos_net_profit", ""),
        "best_net_profit": top.get("oos_net_profit", ""),
        "best_profit_factor": top.get("oos_profit_factor", ""),
        "run_date": "2026-06-17",
        "primary_artifact": f71b.rel(RUN_MANIFEST),
        "candidate_model_id": top.get("candidate_id", ""),
        "net_profit": top.get("oos_net_profit", ""),
        "profit_factor": top.get("oos_profit_factor", ""),
        "drawdown": top.get("oos_max_drawdown_percent", ""),
        "trade_count": top.get("oos_trade_count", ""),
        "result_status": result["status"],
        "sample_rows": "",
        "expectancy": top.get("oos_expectancy", ""),
        "attempt_count": result["candidate_count"],
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 전용 주장 범위 밖)",
        "result_judgment": result["judgment"],
        "final_decision_path": f71b.rel(REPORT),
        "gate_audit_path": f71b.rel(GATE_AUDIT),
        "created_at": result["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_proxy_repair",
        "subrun_id": "proxy_repair(프록시 수리)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A full-context sample(Tier A 전체 문맥 표본)",
        "kpi_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "primary_kpi": f"best_oos_net={f71b.fmt(top.get('oos_net_profit'))};best_oos_pf={f71b.fmt(top.get('oos_profit_factor'))};best_oos_dd={f71b.fmt(top.get('oos_max_drawdown_percent'))};best_oos_tpd={f71b.fmt(top.get('oos_trades_day'))}",
        "guardrail_kpi": f"scout={result['scout_clue_count']};meaningful={result['meaningful_candidate_count']};fracture={result['meaningful_with_fracture_count']}",
        "row_id": f"{RUN_ID}__tier_a_proxy_repair",
        "evidence_boundary": "proxy_repair_only_no_authority(프록시 수리 전용, 권위 없음)",
        "next_action": result["next_run_id"],
        "question": "Can density repair lift F71B scout clue without losing PF/DD?(밀도 수리가 F71B 단서의 수익 팩터/손실폭을 잃지 않고 올릴 수 있나?)",
        "artifact_count": 8,
        "created_at_utc": result["created_at_utc"],
        "required_gate_audit": f71b.rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_proxy_repair(전선 프록시 수리)",
        "run_type": "proxy_repair(프록시 수리)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f71b.rel(RUN_ROOT),
        "result_path": f71b.rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "F71B scout clue(F71B 탐색 단서)",
        "trade_density": top.get("oos_trades_day", ""),
        "max_drawdown_percent": top.get("oos_max_drawdown_percent", ""),
        "strict_joint_pass_count": result["meaningful_candidate_count"],
    }


def ledger_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = registry_row(result)
    rows = []
    for idx, tier in enumerate(tier_rows(result), start=1):
        row = dict(base)
        row.update(tier)
        row["ledger_row_id"] = f"{RUN_ID}__tier_view_{idx}"
        row["row_id"] = row["ledger_row_id"]
        row["subrun_id"] = tier["record_view"]
        row["path"] = f71b.rel(TIER_CSV)
        rows.append(row)
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    f71b.upsert_ledger(f71b.RUN_REGISTRY, "run_id", registry_row(result))
    for row in ledger_rows(result):
        f71b.upsert_ledger(f71b.ALPHA_LEDGER, "ledger_row_id", row)
        f71b.upsert_ledger(f71b.STAGE_LEDGER, "ledger_row_id", row, source_header=f71b.ALPHA_LEDGER)


def append_idea(result: Mapping[str, Any]) -> None:
    marker = "<!-- frontier71C_economics_native_repair_recombine_proxy_v1 -->"
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    block = f"""
{marker}
- `{RUN_ID}` executed density repair/recombine proxy(밀도 수리/재조합 프록시). Result(결과): `{result['judgment']}`. F71C scout clue(탐색 단서) `{result['scout_clue_count']}`, meaningful candidate(의미 후보) `{result['meaningful_candidate_count']}`. Top OOS(상위 표본외) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{f71b.fmt(top.get('oos_net_profit'))}/{f71b.fmt(top.get('oos_profit_factor'))}/{f71b.fmt(top.get('oos_max_drawdown_percent'))}/{f71b.fmt(top.get('oos_trades_day'))}`. Evidence(근거): `{f71b.rel(REPORT)}`. Next(다음): `{result['next_run_id']}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    f71b.append_once(f71b.IDEA_REGISTRY, marker, block)


def write_state(result: Mapping[str, Any]) -> None:
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {result['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {result['status']}",
        f"current_judgment: {result['judgment']}",
        f"next_run_id: {result['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_retrospective_completed",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "Action(행동): F71C density repair/recombine proxy(밀도 수리/재조합 프록시)를 실행했다."',
        f'  - "Effect(효과): scout={result["scout_clue_count"]}, meaningful={result["meaningful_candidate_count"]}; next는 MT5 Runtime Probe 전 Grok 검토 또는 논리 검토로 고정된다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f71b.WORKSPACE_STATE).write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")
    lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{result['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F71C density repair/recombine proxy(밀도 수리/재조합 프록시)를 실행했다.",
        "",
        f"Effect(효과): F71B 단서의 밀도를 올리려 했고, F71C scout clue(탐색 단서) `{result['scout_clue_count']}`, meaningful candidate(의미 후보) `{result['meaningful_candidate_count']}`를 기록했다.",
        "",
        f"- top candidate(상위 후보): `{top.get('candidate_id', 'none')}`.",
        f"- validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(top.get('validation_net_profit'))}` / `{f71b.fmt(top.get('validation_profit_factor'))}` / `{f71b.fmt(top.get('validation_max_drawdown_percent'))}` / `{f71b.fmt(top.get('validation_trades_day'))}`.",
        f"- OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(top.get('oos_net_profit'))}` / `{f71b.fmt(top.get('oos_profit_factor'))}` / `{f71b.fmt(top.get('oos_max_drawdown_percent'))}` / `{f71b.fmt(top.get('oos_trades_day'))}`.",
        f"- next action(다음 행동): `{result['next_run_id']}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]
    f71b.write_md(f71b.CURRENT_WORKING_STATE, lines)


def main() -> int:
    missing = [f71b.rel(path) for path in [F71B_SUMMARY, F71B_CANDIDATES] if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing F71B artifact(F71B 산출물 누락): {missing}")
    result = run_repair(utc_now())
    write_outputs(result)
    update_ledgers(result)
    append_idea(result)
    write_state(result)
    print(
        json.dumps(
            json_ready(
                {
                    "status": result["status"],
                    "judgment": result["judgment"],
                    "candidate_count": result["candidate_count"],
                    "scout_clue_count": result["scout_clue_count"],
                    "meaningful_candidate_count": result["meaningful_candidate_count"],
                    "next_run_id": result["next_run_id"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
