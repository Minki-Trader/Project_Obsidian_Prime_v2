from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_70 import frontier70b_label_regime_asymmetric_value_proxy_scout as f70b


STAGE_ID = f70b.STAGE_ID
RUN_ID = "frontier70C_label_regime_stability_repair_proxy_scout_v1"
PARENT_RUN_ID = f70b.RUN_ID
IDEA_ID = f70b.IDEA_ID
NEXT_RUN_IF_SIGNAL = "frontier70D_pre_mt5_grok_label_regime_stability_seed_review_v1"
NEXT_RUN_IF_NO_SIGNAL = "frontier70D_gap_analysis_or_closeout_decision_v1"
CLAIM_BOUNDARY = (
    "proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f70b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f70b.REVIEWS_ROOT
SELECTED_ROOT = f70b.SELECTED_ROOT
F70B_REPORT = REVIEWS_ROOT / "frontier70B_label_regime_asymmetric_value_proxy_scout_report.md"
F70B_SUMMARY = REVIEWS_ROOT / "f70b_proxy_candidate_summary_review.csv"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = f70b.read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def required_artifacts() -> list[Path]:
    return [F70B_REPORT, F70B_SUMMARY, f70b.F70A_AXIS_CONTRACT, f70b.MODEL_INPUT, f70b.RAW_US100]


def repair_label_specs() -> list[f70b.LabelSpec]:
    specs: list[f70b.LabelSpec] = []
    focused = [
        ("trend_quality", 12, (0.70, 0.80), (0.08, 0.12), (0.40, 0.55)),
        ("trend_quality", 18, (0.85, 0.95), (0.08, 0.12), (0.40, 0.55)),
        ("chop_reversion", 18, (0.85, 0.95), (0.08, 0.12), (0.40,)),
        ("vol_expansion", 18, (0.85, 0.95), (0.08, 0.12), (0.40,)),
        ("neutral", 12, (0.70, 0.80), (0.08,), (0.40,)),
    ]
    for mode, horizon, tps, edges, penalties in focused:
        for tp in tps:
            for edge in edges:
                for penalty in penalties:
                    specs.append(
                        f70b.LabelSpec(
                            label_id=f"repair_{mode}_h{horizon}_tp{int(tp*100):02d}_edge{int(edge*100):02d}_pen{int(penalty*100):02d}",
                            horizon_bars=horizon,
                            base_tp_atr=tp,
                            min_edge_atr=edge,
                            penalty=penalty,
                            regime_mode=mode,
                        )
                    )
    return specs


def repair_model_specs() -> list[f70b.ModelSpec]:
    base = f70b.model_specs()
    return [
        base[0],
        f70b.ModelSpec(
            "small_mlp_l2_v1",
            "small_nn(작은 신경망)",
            "hypothesis_carrier(가설 운반)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                StandardScaler(),
                MLPClassifier(
                    hidden_layer_sizes=(12,),
                    activation="relu",
                    alpha=0.02,
                    batch_size=512,
                    learning_rate_init=0.002,
                    max_iter=120,
                    early_stopping=True,
                    n_iter_no_change=8,
                    random_state=70,
                ),
            ),
        ),
        base[1],
    ]


def repair_selection_specs() -> list[f70b.SelectionSpec]:
    return [
        f70b.SelectionSpec("all_q50", "all", 0.50),
        f70b.SelectionSpec("all_q60", "all", 0.60),
        f70b.SelectionSpec("cash_q50", "cash", 0.50),
        f70b.SelectionSpec("trend_q50", "trend", 0.50),
        f70b.SelectionSpec("chop_q50", "chop", 0.50),
        f70b.SelectionSpec("vol_expansion_q50", "vol_expansion", 0.50),
    ]


def run_repair(created_at: str) -> dict[str, Any]:
    frame = f70b.load_frames()
    features = f70b.feature_sets(frame)
    models = repair_model_specs()
    selections = repair_selection_specs()
    kpi_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    balance_rows: list[dict[str, Any]] = []
    bucket_rows: list[dict[str, Any]] = []

    for label_spec in repair_label_specs():
        frame = f70b.add_future_path(frame, label_spec.horizon_bars)
        label = f70b.build_labels(frame, label_spec)
        balance_rows.extend(f70b.class_counts(frame, label, label_spec))
        train_mask = frame["split"].astype(str).eq("train").to_numpy()
        if label.loc[train_mask].nunique() < 2:
            continue
        for feature_set in features:
            x_train = frame.loc[train_mask, feature_set.columns]
            y_train = label.loc[train_mask]
            for model_spec in models:
                model = model_spec.build()
                try:
                    model.fit(x_train, y_train)
                except Exception as exc:
                    candidate_rows.append(
                        {
                            "candidate_id": f"fit_failed_{f70b.stable_id([label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, str(exc)])}",
                            "label_id": label_spec.label_id,
                            "feature_set_id": feature_set.feature_set_id,
                            "model_id": model_spec.model_id,
                            "status": "fit_failed",
                            "error": str(exc)[:200],
                        }
                    )
                    continue
                side, score = f70b.side_scores(model, frame.loc[:, feature_set.columns])
                for selection in selections:
                    train_sel_mask = train_mask & f70b.mask_for(frame, selection.mask_name)
                    train_scores = score[train_sel_mask]
                    train_scores = train_scores[np.isfinite(train_scores)]
                    if len(train_scores) < 20:
                        continue
                    threshold = float(np.quantile(train_scores, selection.threshold_quantile))
                    split_rows = f70b.evaluate_selection(frame, side, score, label_spec, selection, threshold)
                    candidate_id = "f70c_" + f70b.stable_id([label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, selection.selection_id])
                    by_split = {row["split"]: row for row in split_rows}
                    val = by_split.get("validation", {})
                    oos = by_split.get("oos", {})
                    summary = {
                        "candidate_id": candidate_id,
                        "label_id": label_spec.label_id,
                        "horizon_bars": label_spec.horizon_bars,
                        "regime_mode": label_spec.regime_mode,
                        "feature_set_id": feature_set.feature_set_id,
                        "feature_count": len(feature_set.columns),
                        "model_id": model_spec.model_id,
                        "model_family": model_spec.model_family,
                        "model_role": model_spec.model_role,
                        "selection_id": selection.selection_id,
                        "mask_name": selection.mask_name,
                        "threshold_quantile": selection.threshold_quantile,
                        "threshold": threshold,
                        "validation_net": val.get("net", 0.0),
                        "validation_pf": val.get("pf", 0.0),
                        "validation_dd_pct": val.get("dd_pct", 0.0),
                        "validation_trades": val.get("trades", 0),
                        "validation_trades_per_day": val.get("trades_per_day", 0.0),
                        "oos_net": oos.get("net", 0.0),
                        "oos_pf": oos.get("pf", 0.0),
                        "oos_dd_pct": oos.get("dd_pct", 0.0),
                        "oos_trades": oos.get("trades", 0),
                        "oos_trades_per_day": oos.get("trades_per_day", 0.0),
                    }
                    summary["joint_soft"] = bool(
                        summary["validation_net"] > 0
                        and summary["oos_net"] > 0
                        and summary["validation_pf"] >= 1.20
                        and summary["oos_pf"] >= 1.20
                        and summary["validation_dd_pct"] <= 10.0
                        and summary["oos_dd_pct"] <= 10.0
                        and summary["validation_trades_per_day"] >= 0.80
                        and summary["oos_trades_per_day"] >= 0.80
                    )
                    summary["final_like"] = bool(
                        summary["validation_pf"] >= 2.0
                        and summary["oos_pf"] >= 2.0
                        and 5.0 <= summary["validation_trades_per_day"] <= 10.0
                        and 5.0 <= summary["oos_trades_per_day"] <= 10.0
                        and summary["validation_dd_pct"] < 10.0
                        and summary["oos_dd_pct"] < 10.0
                    )
                    candidate_rows.append(summary)
                    for row in split_rows:
                        kpi_rows.append({"candidate_id": candidate_id, **summary, **{f"split_{k}": v for k, v in row.items()}})
                    if summary["joint_soft"] or summary["final_like"]:
                        bucket_rows.extend(f70b.bucket_kpi(frame, side, score, label_spec, selection, threshold, candidate_id))

    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row.get("final_like")),
            bool(row.get("joint_soft")),
            float(row.get("validation_pf") or 0) + float(row.get("oos_pf") or 0),
            float(row.get("validation_trades_per_day") or 0) + float(row.get("oos_trades_per_day") or 0),
            float(row.get("oos_pf") or 0),
        ),
        reverse=True,
    )
    meaningful = [row for row in ranked if row.get("joint_soft")]
    final_like = [row for row in ranked if row.get("final_like")]
    status = "completed_proxy_repair_meaningful_signal_no_authority" if meaningful else "completed_proxy_repair_no_meaningful_signal_no_authority"
    judgment = "proxy_repair_seed_surface_no_authority" if meaningful else "proxy_repair_inconclusive_closeout_or_new_axis_required_no_authority"
    return {
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "next_run_id": NEXT_RUN_IF_SIGNAL if meaningful else NEXT_RUN_IF_NO_SIGNAL,
        "candidate_summaries": ranked,
        "candidate_kpi_rows": kpi_rows,
        "class_balance_rows": balance_rows,
        "bucket_kpi_rows": bucket_rows,
        "meaningful_candidates": meaningful,
        "final_like_candidates": final_like,
        "top_candidates": ranked[:12],
        "frame_rows": int(len(frame)),
    }


def report_lines(result: Mapping[str, Any]) -> list[str]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    return [
        "# F70C Label-Regime Stability Repair Proxy Scout(F70C 라벨-장세 안정성 수리 프록시 탐색)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "## Hypothesis(가설)",
        "",
        "F70B positive-both but weak-PF strata(F70B 양쪽 양수이나 약한 수익 팩터 층)를 label parameter and model carrier(라벨 파라미터와 모델 운반체)로 좁히면 split instability(분할 불안정)를 줄일 수 있다.",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): trend/chop/volatility label strata(추세/횡보/변동성 라벨 층), small NN(작은 신경망), and fixed low quantile selection(고정 낮은 분위수 선택)을 시험했다.",
        "",
        "Effect(효과): F69식 threshold/cooldown/daily quota rescue(임계값/쿨다운/일별 할당 구제)가 아니라 label stability repair(라벨 안정성 수리)의 가능성을 확인했다.",
        "",
        "## KPI Summary(KPI 요약)",
        "",
        f"- candidate rows(후보 행): `{len(result['candidate_summaries'])}`.",
        f"- meaningful joint-soft candidates(의미 있는 공동 완화 후보): `{len(result['meaningful_candidates'])}`.",
        f"- final-like candidates(최종 조건 유사 후보): `{len(result['final_like_candidates'])}`.",
        f"- top candidate(상위 후보): `{best.get('candidate_id', 'none')}`.",
        f"- top validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래): `{f70b.fmt(best.get('validation_net'))}` / `{f70b.fmt(best.get('validation_pf'))}` / `{f70b.fmt(best.get('validation_dd_pct'))}` / `{f70b.fmt(best.get('validation_trades_per_day'))}`.",
        f"- top OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{f70b.fmt(best.get('oos_net'))}` / `{f70b.fmt(best.get('oos_pf'))}` / `{f70b.fmt(best.get('oos_dd_pct'))}` / `{f70b.fmt(best.get('oos_trades_per_day'))}`.",
        "",
        f"- next action(다음 행동): `{result['next_run_id']}`.",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def gate_audit_lines(result: Mapping[str, Any]) -> list[str]:
    return [
        "# F70C Required Gate Coverage Audit(F70C 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| parent_proxy(부모 프록시) | pass(통과) | `{f70b.rel(F70B_SUMMARY)}` | F70B failure shape(실패 모양)에서 수리 시작 |",
        f"| repair_scope(수리 범위) | pass(통과) | `{f70b.rel(RUN_ROOT / 'f70c_proxy_candidate_summary.csv')}` | 라벨 안정성 수리로 제한 |",
        f"| no_trade_shape_rescue(거래 형태 구제 없음) | pass(통과) | fixed selection specs(고정 선택 규격) | F69 반복 방지 |",
        "| MT5 runtime probe(MT5 런타임 탐침) | pending_if_meaningful_signal(의미 신호면 대기) | proxy-only boundary(프록시 전용 경계) | 런타임 주장 없음 |",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def tier_pair_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    return [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "status": "materialized_proxy_repair_kpi(프록시 수리 KPI 물질화)",
            "net_profit": best.get("oos_net", ""),
            "profit_factor": best.get("oos_pf", ""),
            "trade_count": best.get("oos_trades", ""),
            "trades_per_day": best.get("oos_trades_per_day", ""),
            "notes": "F70C primary sample remains Tier A full-context proxy input(F70C 주 표본은 티어 A 전체 문맥 프록시 입력)",
        },
        {"record_view": "Tier B separate(Tier B 분리)", "tier_scope": "Tier B", "status": "missing_required(필수 누락)", "net_profit": "", "profit_factor": "", "trade_count": "", "trades_per_day": "", "notes": "Tier B not materialized in F70C repair(Tier B는 F70C 수리에서 물질화하지 않음)"},
        {"record_view": "Tier A+B combined(Tier A+B 합산)", "tier_scope": "Tier A+B", "status": "out_of_scope_by_claim(주장 범위 밖)", "net_profit": "", "profit_factor": "", "trade_count": "", "trades_per_day": "", "notes": "No synthetic combined KPI claimed(합성 합산 KPI 주장 없음)"},
    ]


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": result["created_at_utc"],
        "producer": "stage_pipelines/stage_frontier_70/frontier70c_label_regime_stability_repair_proxy_scout.py",
        "status": result["status"],
        "judgment": result["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "artifacts": [
            f70b.rel(RUN_ROOT / "f70c_proxy_candidate_summary.csv"),
            f70b.rel(RUN_ROOT / "f70c_proxy_kpi_by_split.csv"),
            f70b.rel(REVIEWS_ROOT / "frontier70C_label_regime_stability_repair_proxy_scout_report.md"),
            f70b.rel(REVIEWS_ROOT / "required_gate_coverage_audit_f70c.md"),
        ],
        "next_run_id": result["next_run_id"],
    }


def ledger_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": result["status"],
        "judgment": result["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/frontier70C_label_regime_stability_repair_proxy_scout_report.md",
        "claim_boundary": CLAIM_BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_proxy_repair_only(프록시 수리 전용 주장 범위 밖)",
        "run_number": "frontier70C",
        "date": str(result["created_at_utc"])[:10],
        "run_date": str(result["created_at_utc"])[:10],
        "decision": "pre_mt5_grok_if_meaningful_signal_else_gap_or_closeout",
        "next_run_id": result["next_run_id"],
        "rows": len(result["candidate_summaries"]),
        "candidate_rows": len(result["candidate_summaries"]),
        "positive_proxy_rows": len(result["meaningful_candidates"]),
        "best_proxy": best.get("candidate_id", ""),
        "best_model_id": best.get("model_id", ""),
        "net_profit": f70b.fmt(best.get("oos_net")),
        "profit_factor": f70b.fmt(best.get("oos_pf")),
        "drawdown": f70b.fmt(best.get("oos_dd_pct")),
        "trade_count": f70b.fmt(best.get("oos_trades")),
        "trade_density": f70b.fmt(best.get("oos_trades_per_day")),
        "feature_count": best.get("feature_count", ""),
        "sample_rows": result["frame_rows"],
        "attempt_count": len(result["candidate_summaries"]),
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard": "structural_scout(구조 탐색)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "evidence_boundary": "proxy_repair_only_no_runtime_authority(프록시 수리 전용, 런타임 권위 없음)",
        "work_family": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_repair(프록시 수리)",
        "result_status": result["status"],
        "result_judgment": result["judgment"],
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier70C_label_regime_stability_repair_proxy_scout_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f70c.md",
        "created_at": result["created_at_utc"],
        "created_at_utc": result["created_at_utc"],
        "required_gate_audit": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f70c.md",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_repair_only_no_runtime(프록시 수리 전용, 런타임 없음)",
        "question": "Can label-regime stability repair reduce split instability?(라벨-장세 안정성 수리가 분할 불안정을 줄이는가)",
        "next_action": result["next_run_id"],
        "artifact_count": 10,
        "run_family": "frontier_proxy_repair(전선 프록시 수리)",
        "run_type": "label_regime_stability_repair_proxy_scout(라벨-장세 안정성 수리 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f70c_proxy_candidate_summary.csv",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier70C_label_regime_stability_repair_proxy_scout_report.md",
    }
    rows: list[dict[str, Any]] = []
    for tier in tier_pair_rows(result):
        row = dict(base)
        suffix = tier["record_view"].split("(")[0].strip().lower().replace(" ", "_").replace("+", "plus")
        row.update({"ledger_row_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "subrun_id": tier["record_view"], "record_view": tier["record_view"], "view": tier["record_view"], "tier_scope": tier["tier_scope"], "tier": tier["tier_scope"], "kpi_scope": "proxy_repair_kpi(프록시 수리 KPI)", "metric_scope": "validation_oos_proxy(검증/표본외 프록시)", "primary_kpi": f"net={tier['net_profit']};pf={tier['profit_factor']};trades_day={tier['trades_per_day']}", "guardrail_kpi": tier["notes"], "notes": tier["notes"]})
        if tier["tier_scope"] != "Tier A":
            row["status"] = tier["status"]
            row["judgment"] = "inconclusive_tier_pair_gap_named(티어 쌍 간극 이름 붙임)"
            row["net_profit"] = ""
            row["profit_factor"] = ""
            row["drawdown"] = ""
            row["trade_count"] = ""
            row["trade_density"] = ""
        rows.append(row)
    return rows


def write_outputs(result: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT, RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(RUN_ROOT / "f70c_proxy_candidate_summary.csv", list(result["candidate_summaries"]))
    write_csv(RUN_ROOT / "f70c_proxy_kpi_by_split.csv", list(result["candidate_kpi_rows"]))
    write_csv(RUN_ROOT / "f70c_label_balance.csv", list(result["class_balance_rows"]))
    write_csv(RUN_ROOT / "f70c_bucket_kpi.csv", list(result["bucket_kpi_rows"]))
    write_json(RUN_ROOT / "f70c_top_candidates.json", list(result["top_candidates"]))
    write_csv(RUN_ROOT / "f70c_tier_pair_status.csv", tier_pair_rows(result))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(result))
    write_md(RUN_ROOT / "reports/result_summary.md", report_lines(result))
    write_csv(REVIEWS_ROOT / "f70c_proxy_candidate_summary_review.csv", list(result["candidate_summaries"]))
    write_csv(REVIEWS_ROOT / "f70c_proxy_kpi_by_split_review.csv", list(result["candidate_kpi_rows"]))
    write_csv(REVIEWS_ROOT / "f70c_label_balance_review.csv", list(result["class_balance_rows"]))
    write_csv(REVIEWS_ROOT / "f70c_bucket_kpi_review.csv", list(result["bucket_kpi_rows"]))
    write_json(REVIEWS_ROOT / "f70c_top_candidates_review.json", list(result["top_candidates"]))
    write_csv(REVIEWS_ROOT / "f70c_tier_pair_status_review.csv", tier_pair_rows(result))
    write_md(REVIEWS_ROOT / "frontier70C_label_regime_stability_repair_proxy_scout_report.md", report_lines(result))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f70c.md", gate_audit_lines(result))
    append_once(REVIEWS_ROOT / "review_index.md", "<!-- frontier70C_label_regime_stability_repair_proxy_scout_v1 -->", """<!-- frontier70C_label_regime_stability_repair_proxy_scout_v1 -->
- `frontier70C_label_regime_stability_repair_proxy_scout_report.md`: F70C proxy repair report(F70C 프록시 수리 보고서)
- `f70c_proxy_candidate_summary_review.csv`: F70C candidate summary(F70C 후보 요약)
- `required_gate_coverage_audit_f70c.md`: F70C required gate audit(F70C 필수 게이트 감사)""")


def update_ledgers(result: Mapping[str, Any]) -> None:
    rows = ledger_rows(result)
    for row in rows:
        upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
        upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", rows[0])


def update_registers(result: Mapping[str, Any]) -> None:
    marker = "<!-- frontier70C_label_regime_stability_repair_proxy_scout_v1 -->"
    block = f"""<!-- frontier70C_label_regime_stability_repair_proxy_scout_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` executed label-regime stability repair proxy scout(라벨-장세 안정성 수리 프록시 탐색 실행). Result(결과): `{result['judgment']}`. Meaningful joint-soft candidates(의미 있는 공동 완화 후보): `{len(result['meaningful_candidates'])}`. Final-like candidates(최종 조건 유사 후보): `{len(result['final_like_candidates'])}`. Boundary(경계): proxy-repair only(프록시 수리 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{result['next_run_id']}`."""
    append_once(ROOT / "docs/registers/idea_registry.md", marker, block)


def update_state_files(result: Mapping[str, Any]) -> None:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {result['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {result['status']}",
        f"current_judgment: {result['judgment']}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {result['next_run_id']}",
        "runtime_probe_status: f70_mandatory_runtime_probe_pending_after_meaningful_proxy_signal_or_gap_decision(F70 의미 있는 프록시 신호 또는 간극 결정 뒤 필수 런타임 탐침 대기)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f69_closeout_4_of_5",
        f"updated_at_utc: '{result['created_at_utc']}'",
        "notes:",
        '  - "F70C action(행동): label-regime stability repair proxy scout(라벨-장세 안정성 수리 프록시 탐색)를 실행했다."',
        f'  - "Effect(효과): joint-soft candidates(공동 완화 후보) `{len(result["meaningful_candidates"])}`, final-like candidates(최종 조건 유사 후보) `{len(result["final_like_candidates"])}`를 기록했다."',
        f'  - "Top proxy clue(상위 프록시 단서): `{best.get("candidate_id", "none")}` OOS PF/trades_day/DD(표본외 수익 팩터/일거래/손실폭) `{f70b.fmt(best.get("oos_pf"))}/{f70b.fmt(best.get("oos_trades_per_day"))}/{f70b.fmt(best.get("oos_dd_pct"))}`."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    current = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{result['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F70C label-regime stability repair proxy scout(F70C 라벨-장세 안정성 수리 프록시 탐색)를 실행했다.",
        "",
        "Effect(효과): F70B의 split instability(분할 불안정)를 라벨 파라미터와 작은 신경망 모델 운반체로 수리해 봤다.",
        "",
        f"- status(상태): `{result['status']}`.",
        f"- judgment(판정): `{result['judgment']}`.",
        f"- candidate rows(후보 행): `{len(result['candidate_summaries'])}`.",
        f"- joint-soft candidates(공동 완화 후보): `{len(result['meaningful_candidates'])}`.",
        f"- final-like candidates(최종 조건 유사 후보): `{len(result['final_like_candidates'])}`.",
        f"- top candidate(상위 후보): `{best.get('candidate_id', 'none')}`.",
        f"- top OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{f70b.fmt(best.get('oos_net'))}` / `{f70b.fmt(best.get('oos_pf'))}` / `{f70b.fmt(best.get('oos_dd_pct'))}` / `{f70b.fmt(best.get('oos_trades_per_day'))}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current)
    selection = [
        "# F70 Selection Status(F70 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{result['next_run_id']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{result['next_run_id']}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(SELECTED_ROOT / "selection_status.md", selection)


def main() -> int:
    missing = [f70b.rel(path) for path in required_artifacts() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F70C required material missing: {missing}")
    result = run_repair(utc_now())
    write_outputs(result)
    update_ledgers(result)
    update_registers(result)
    update_state_files(result)
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    print(json.dumps(json_ready({
        "status": result["status"],
        "judgment": result["judgment"],
        "run_id": RUN_ID,
        "next_run_id": result["next_run_id"],
        "candidate_rows": len(result["candidate_summaries"]),
        "meaningful_candidates": len(result["meaningful_candidates"]),
        "final_like_candidates": len(result["final_like_candidates"]),
        "top_candidate": best.get("candidate_id", "none"),
        "top_oos_pf": best.get("oos_pf", ""),
        "top_oos_trades_per_day": best.get("oos_trades_per_day", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    import numpy as np

    raise SystemExit(main())
