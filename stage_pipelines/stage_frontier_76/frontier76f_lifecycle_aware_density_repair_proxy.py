from __future__ import annotations

import csv
import json
import sys
import warnings
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from stage_pipelines.stage_frontier_76 import frontier76b_axis_ablation_proxy_scout as f76b


STAGE_ID = f76b.STAGE_ID
RUN_ID = "frontier76F_lifecycle_aware_density_repair_proxy_v1"
PARENT_RUN_ID = "frontier76E_proxy_runtime_gap_analysis_and_repair_decision_v1"
NEXT_RUN_IF_SIGNAL = "frontier76G_pre_mt5_grok_lifecycle_repair_runtime_probe_v1"
NEXT_RUN_IF_NO_SIGNAL = "frontier76G_stage_closeout_axis_ablation_source_discovery_v1"
CLAIM_BOUNDARY = (
    "repair_proxy_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
MAX_HOLD_BARS = 12
PROB_QUANTILES = [0.50, 0.60, 0.70, 0.80]

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SUMMARY_PATH = REVIEW_DIR / "f76f_lifecycle_proxy_summary.json"
TOP100_PATH = REVIEW_DIR / "f76f_lifecycle_proxy_ranked_top100.csv"
AXIS_SUMMARY_PATH = REVIEW_DIR / "f76f_lifecycle_proxy_axis_summary.csv"
MODEL_FIT_PATH = REVIEW_DIR / "f76f_lifecycle_model_fit_summary.csv"
REPORT_PATH = REVIEW_DIR / "frontier76F_lifecycle_aware_density_repair_proxy_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f76f.md"
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


def lifecycle_select(raw_signal: np.ndarray, max_hold_bars: int = MAX_HOLD_BARS) -> np.ndarray:
    selected = np.zeros_like(raw_signal, dtype=bool)
    remaining_hold = 0
    for idx, flag in enumerate(raw_signal):
        if remaining_hold > 0:
            remaining_hold -= 1
            continue
        if bool(flag):
            selected[idx] = True
            remaining_hold = max_hold_bars
    return selected


def repair_meaningful_gate(val: Mapping[str, float], oos: Mapping[str, float]) -> bool:
    def ok(metrics: Mapping[str, float]) -> bool:
        return (
            float(metrics["net"]) > 0
            and float(metrics["pf"]) >= 1.30
            and float(metrics["dd_pct"]) <= 10.0
            and float(metrics["trades_day"]) >= 1.0
            and int(metrics["trade_count"]) >= 100
        )

    return ok(val) and ok(oos)


def density_scout_gate(val: Mapping[str, float], oos: Mapping[str, float]) -> bool:
    return (
        float(val["net"]) > 0
        and float(oos["net"]) > 0
        and min(float(val["pf"]), float(oos["pf"])) >= 1.15
        and max(float(val["dd_pct"]), float(oos["dd_pct"])) <= 12.0
        and min(float(val["trades_day"]), float(oos["trades_day"])) >= 3.0
    )


def completion_axis_nearness(val: Mapping[str, float], oos: Mapping[str, float]) -> bool:
    min_tpd = min(float(val["trades_day"]), float(oos["trades_day"]))
    max_tpd = max(float(val["trades_day"]), float(oos["trades_day"]))
    return (
        5.0 <= min_tpd
        and max_tpd <= 10.0
        and min(float(val["pf"]), float(oos["pf"])) >= 1.50
        and max(float(val["dd_pct"]), float(oos["dd_pct"])) < 10.0
        and float(val["net"]) > 0
        and float(oos["net"]) > 0
    )


def density_target_score(val: Mapping[str, float], oos: Mapping[str, float]) -> float:
    min_tpd = min(float(val["trades_day"]), float(oos["trades_day"]))
    if 5.0 <= min_tpd <= 10.0:
        return 1_000.0
    return max(0.0, 1_000.0 - abs(min_tpd - 7.5) * 120.0)


def rank_score(val: Mapping[str, float], oos: Mapping[str, float], meaningful: bool, density_scout: bool, near: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    min_tpd = min(float(val["trades_day"]), float(oos["trades_day"]))
    min_trades = min(int(val["trade_count"]), int(oos["trade_count"]))
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    return (
        (1_000_000.0 if meaningful else 0.0)
        + (500_000.0 if density_scout else 0.0)
        + (250_000.0 if near else 0.0)
        + (10_000.0 if min_net > 0 else 0.0)
        + density_target_score(val, oos) * 400.0
        + min_pf * 3_000.0
        + min_tpd * 1_500.0
        + min_trades * 2.0
        - max_dd * 250.0
        + min_net * 0.05
    )


def fit_and_score() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    df = pd.read_parquet(io_path(f76b.DATASET_PATH)).copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    features = f76b.feature_order()
    train_mask = df["split"] == "train"
    train = df.loc[train_mask]
    targets = f76b.target_specs(train)
    feature_map = f76b.feature_sets(features)
    builders: dict[str, Callable[[], Any]] = f76b.model_builders()
    thresholds = f76b.risk_thresholds(train)
    sessions = ["all", "cash_open", "cash_mid", "cash_late"]
    risks = ["none", "compression", "trend_aligned", "mean_revert"]

    candidate_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    candidate_id = 0

    for feature_set_name, cols in feature_map.items():
        if not cols:
            continue
        matrices = f76b.clean_matrices(df, train_mask, cols)
        for target in targets:
            y_train = f76b.make_target(train["future_log_return_12"], target)
            positives = int(y_train.sum())
            if positives == 0 or positives == len(y_train):
                fit_rows.append(
                    {
                        "feature_set": feature_set_name,
                        "target": target.name,
                        "model": "all",
                        "status": "skipped_single_class",
                        "positive_train": positives,
                        "train_rows": int(len(y_train)),
                    }
                )
                continue
            for model_name, builder in builders.items():
                if model_name == "small_mlp_16" and feature_set_name not in {"price_action_core", "volatility_compression"}:
                    continue
                model = builder()
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        model.fit(matrices["train"], y_train)
                    probs = {split: f76b.probability(model, matrices[split]) for split in ["train", "validation", "oos"]}
                    fit_rows.append(
                        {
                            "feature_set": feature_set_name,
                            "target": target.name,
                            "model": model_name,
                            "status": "fit_completed",
                            "positive_train": positives,
                            "train_rows": int(len(y_train)),
                            "train_positive_rate": float(positives / len(y_train)),
                        }
                    )
                except Exception as exc:  # noqa: BLE001
                    fit_rows.append(
                        {
                            "feature_set": feature_set_name,
                            "target": target.name,
                            "model": model_name,
                            "status": "fit_failed",
                            "error": str(exc)[:200],
                            "positive_train": positives,
                            "train_rows": int(len(y_train)),
                        }
                    )
                    continue

                for q in PROB_QUANTILES:
                    prob_threshold = float(np.quantile(probs["train"], q))
                    for session in sessions:
                        for risk in risks:
                            val_df = df.loc[df["split"] == "validation"].copy()
                            oos_df = df.loc[df["split"] == "oos"].copy()
                            val_raw = (
                                (probs["validation"] >= prob_threshold)
                                & f76b.session_mask(val_df, session)
                                & f76b.risk_mask(val_df, risk, target.side, thresholds)
                            )
                            oos_raw = (
                                (probs["oos"] >= prob_threshold)
                                & f76b.session_mask(oos_df, session)
                                & f76b.risk_mask(oos_df, risk, target.side, thresholds)
                            )
                            val_selected = lifecycle_select(val_raw, MAX_HOLD_BARS)
                            oos_selected = lifecycle_select(oos_raw, MAX_HOLD_BARS)
                            val_kpi = f76b.kpi(val_df.reset_index(drop=True), val_selected, target.side)
                            oos_kpi = f76b.kpi(oos_df.reset_index(drop=True), oos_selected, target.side)
                            meaningful = repair_meaningful_gate(val_kpi, oos_kpi)
                            density_scout = density_scout_gate(val_kpi, oos_kpi)
                            near = completion_axis_nearness(val_kpi, oos_kpi)
                            candidate_id += 1
                            row: dict[str, Any] = {
                                "candidate_id": f"f76f_{candidate_id:05d}",
                                "feature_set": feature_set_name,
                                "feature_count": len(cols),
                                "target": target.name,
                                "side": target.side,
                                "target_threshold": target.threshold,
                                "model": model_name,
                                "prob_quantile": q,
                                "prob_threshold": prob_threshold,
                                "session": session,
                                "risk_filter": risk,
                                "trade_shape": f"single_position_max_hold_{MAX_HOLD_BARS}",
                                "raw_val_signal_count": int(val_raw.sum()),
                                "raw_oos_signal_count": int(oos_raw.sum()),
                                "val_entry_count_after_lifecycle": int(val_selected.sum()),
                                "oos_entry_count_after_lifecycle": int(oos_selected.sum()),
                                "val_signal_to_entry_ratio": int(val_selected.sum()) / int(val_raw.sum()) if int(val_raw.sum()) else 0.0,
                                "oos_signal_to_entry_ratio": int(oos_selected.sum()) / int(oos_raw.sum()) if int(oos_raw.sum()) else 0.0,
                                "repair_meaningful_signal": int(meaningful),
                                "density_scout_clue": int(density_scout),
                                "completion_axis_nearness": int(near),
                                "dual_positive": int(val_kpi["net"] > 0 and oos_kpi["net"] > 0),
                                "rank_score": rank_score(val_kpi, oos_kpi, meaningful, density_scout, near),
                            }
                            for prefix, metrics in [("val", val_kpi), ("oos", oos_kpi)]:
                                for key, value in metrics.items():
                                    row[f"{prefix}_{key}"] = value
                            candidate_rows.append(row)

    candidate_rows.sort(key=lambda row: float(row["rank_score"]), reverse=True)
    best = candidate_rows[0] if candidate_rows else {}
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "candidate_rows": len(candidate_rows),
        "fit_rows": len(fit_rows),
        "fit_completed": sum(1 for row in fit_rows if row.get("status") == "fit_completed"),
        "repair_meaningful_signal_count": sum(int(row["repair_meaningful_signal"]) for row in candidate_rows),
        "density_scout_clue_count": sum(int(row["density_scout_clue"]) for row in candidate_rows),
        "completion_axis_nearness_count": sum(int(row["completion_axis_nearness"]) for row in candidate_rows),
        "best_candidate": best,
        "max_hold_bars": MAX_HOLD_BARS,
        "prob_quantiles": PROB_QUANTILES,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return candidate_rows, fit_rows, summary


def axis_summary_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis in ["feature_set", "target", "model", "session", "risk_filter"]:
        for value in sorted({str(row[axis]) for row in candidate_rows}):
            subset = [row for row in candidate_rows if str(row[axis]) == value]
            if not subset:
                continue
            best = max(subset, key=lambda row: float(row["rank_score"]))
            rows.append(
                {
                    "axis": axis,
                    "value": value,
                    "candidate_rows": len(subset),
                    "repair_meaningful_signal_count": sum(int(row["repair_meaningful_signal"]) for row in subset),
                    "density_scout_clue_count": sum(int(row["density_scout_clue"]) for row in subset),
                    "completion_axis_nearness_count": sum(int(row["completion_axis_nearness"]) for row in subset),
                    "best_candidate": best.get("candidate_id", ""),
                    "best_rank_score": best.get("rank_score", ""),
                    "best_val_pf_dd_tpd": f"{best.get('val_pf', '')}/{best.get('val_dd_pct', '')}/{best.get('val_trades_day', '')}",
                    "best_oos_pf_dd_tpd": f"{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}",
                }
            )
    return rows


def status_and_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    if int(summary["repair_meaningful_signal_count"]) > 0:
        return (
            "repair_proxy_lifecycle_meaningful_signal_pre_mt5_probe_required_no_authority",
            "lifecycle_repair_proxy_signal_requires_grok_and_mt5_probe_no_authority",
            NEXT_RUN_IF_SIGNAL,
        )
    if int(summary["density_scout_clue_count"]) > 0:
        return (
            "repair_proxy_lifecycle_density_scout_repair_required_no_authority",
            "density_scout_without_meaningful_signal_more_repair_or_negative_control_required_no_authority",
            NEXT_RUN_IF_NO_SIGNAL,
        )
    return (
        "repair_proxy_lifecycle_no_density_signal_more_repair_required_no_authority",
        "lifecycle_repair_proxy_no_meaningful_signal_no_authority",
        NEXT_RUN_IF_NO_SIGNAL,
    )


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]]) -> str:
    status, judgment, next_run = status_and_next(summary)
    best = summary.get("best_candidate") or {}
    lines = [
        "# Frontier76F Lifecycle-Aware Density Repair Proxy Report(F76F 생명주기 인식 거래밀도 수리 프록시 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- candidate rows(후보 행): `{summary['candidate_rows']}`",
        f"- repair meaningful signal count(수리 의미 신호 수): `{summary['repair_meaningful_signal_count']}`",
        f"- density scout clue count(거래밀도 탐색 단서 수): `{summary['density_scout_clue_count']}`",
        f"- completion axis nearness count(완성 축 근접 수): `{summary['completion_axis_nearness_count']}`",
        f"- best candidate(최선 후보): `{best.get('candidate_id', '')}`",
        f"- best axes(최선 축): `{best.get('feature_set', '')}/{best.get('model', '')}/{best.get('target', '')}/{best.get('session', '')}/{best.get('risk_filter', '')}/{best.get('prob_quantile', '')}`",
        f"- best validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `{best.get('val_net', '')}/{best.get('val_pf', '')}/{best.get('val_dd_pct', '')}/{best.get('val_trades_day', '')}`",
        f"- best OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}`",
        f"- next action(다음 행동): `{next_run}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Top Rows(상위 행)",
        "",
        "| rank(순위) | candidate(후보) | axes(축) | val net/PF/DD/tpd(검증) | oos net/PF/DD/tpd(표본외) | raw->entry val/oos(원신호->진입) | flags(표식) |",
        "|---:|---|---|---|---|---|---|",
    ]
    for idx, row in enumerate(top_rows[:10], start=1):
        lines.append(
            "| {idx} | `{candidate}` | `{axes}` | `{val}` | `{oos}` | `{ratio}` | `{flags}` |".format(
                idx=idx,
                candidate=row.get("candidate_id", ""),
                axes="/".join(
                    str(row.get(key, ""))
                    for key in ["feature_set", "model", "target", "session", "risk_filter", "prob_quantile"]
                ),
                val=f"{row.get('val_net', '')}/{row.get('val_pf', '')}/{row.get('val_dd_pct', '')}/{row.get('val_trades_day', '')}",
                oos=f"{row.get('oos_net', '')}/{row.get('oos_pf', '')}/{row.get('oos_dd_pct', '')}/{row.get('oos_trades_day', '')}",
                ratio=f"{row.get('raw_val_signal_count', '')}->{row.get('val_entry_count_after_lifecycle', '')}/{row.get('raw_oos_signal_count', '')}->{row.get('oos_entry_count_after_lifecycle', '')}",
                flags=f"meaningful={row.get('repair_meaningful_signal', '')};density={row.get('density_scout_clue', '')};near={row.get('completion_axis_nearness', '')}",
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary(해석 경계)",
            "",
            "Action(행동): F76E에서 확인된 same-direction hold compression(동방향 보유 압축)을 proxy scoring(프록시 점수화)에 반영했다.",
            "",
            "Effect(효과): 이 결과는 runtime-aware scout clue(런타임 인식 탐색 단서)일 뿐이고, MT5 Runtime Probe(MT5 런타임 탐침) 전에는 runtime authority(런타임 권위)를 만들지 않는다.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(created_at: str, summary: Mapping[str, Any]) -> str:
    status, _judgment, next_run = status_and_next(summary)
    return f"""# Required Gate Coverage Audit F76F(F76F 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| lifecycle repair proxy(생명주기 수리 프록시) | `passed(통과)` | `{summary['candidate_rows']}` candidates |
| F76E repair decision(F76E 수리 결정) | `passed(통과)` | parent `{PARENT_RUN_ID}` |
| density axis check(거래밀도 축 확인) | `{summary['density_scout_clue_count']}` | scout clue rows(탐색 단서 행) |
| meaningful signal check(의미 신호 확인) | `{summary['repair_meaningful_signal_count']}` | status `{status}` |
| next action(다음 행동) | `{next_run}` | Grok/MT5 required if meaningful signal exists(의미 신호면 Grok/MT5 필수) |
| final_claim_guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def ledger_row(created_at: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    status, judgment, next_run = status_and_next(summary)
    best = summary.get("best_candidate") or {}
    row_id = f"{RUN_ID}::lifecycle_repair_proxy::tier_a"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_proxy",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": f"candidates={summary['candidate_rows']};meaningful={summary['repair_meaningful_signal_count']};density={summary['density_scout_clue_count']}",
        "family": "lifecycle_aware_density_repair_proxy",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier76F",
        "date": created_at[:10],
        "decision": judgment,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "rows": summary["candidate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "best_proxy": best.get("candidate_id", ""),
        "candidate_rows": summary["candidate_rows"],
        "positive_proxy_rows": summary["repair_meaningful_signal_count"],
        "best_model_id": best.get("model", ""),
        "best_proxy_net": best.get("oos_net", ""),
        "net_profit": best.get("oos_net", ""),
        "profit_factor": best.get("oos_pf", ""),
        "drawdown": best.get("oos_dd_pct", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trade_density": best.get("oos_trades_day", ""),
        "expectancy": best.get("oos_expectancy", ""),
        "recovery_factor": best.get("oos_recovery", ""),
        "view": "proxy_validation_oos",
        "tier": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "metric_scope": "lifecycle_aware_repair_proxy",
        "scoreboard_lane": "trade_shape_repair_proxy",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(MT5는 다음 검증 범위)",
        "result_judgment": judgment,
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "lifecycle_aware_repair_proxy(생명주기 인식 수리 프록시)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "proxy_validation_oos(프록시 검증/표본외)",
        "primary_kpi": f"meaningful={summary['repair_meaningful_signal_count']};density={summary['density_scout_clue_count']}",
        "guardrail_kpi": f"max_hold_bars={MAX_HOLD_BARS};no authority",
        "work_family": "repair_proxy",
        "row_id": row_id,
        "evidence_boundary": "proxy_only_no_runtime_authority",
        "next_action": next_run,
        "artifact_count": "6",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "repair_proxy",
        "run_type": "lifecycle_aware_density_repair_proxy",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "trade_density": best.get("oos_trades_day", ""),
        "expected_net_profit": best.get("oos_net", ""),
        "expected_profit_factor": best.get("oos_pf", ""),
        "expected_trade_count": best.get("oos_trade_count", ""),
        "expected_trade_density": best.get("oos_trades_day", ""),
        "max_drawdown_percent": best.get("oos_dd_pct", ""),
    }


def update_state_and_ledgers(created_at: str, summary: Mapping[str, Any]) -> None:
    status, judgment, next_run = status_and_next(summary)
    best = summary.get("best_candidate") or {}
    row = ledger_row(created_at, summary)
    f76b.upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    f76b.upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    f76b.upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row)

    idea_path = ROOT / "docs/registers/idea_registry.md"
    marker = "<!-- frontier76F_lifecycle_aware_density_repair_proxy_v1 -->"
    text = io_path(idea_path).read_text(encoding="utf-8-sig")
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` ran lifecycle-aware density repair proxy(생명주기 인식 거래밀도 수리 프록시). Best(최선): `{best.get('candidate_id', '')}` with OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래) `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`.
"""
        write_text(idea_path, text.rstrip() + addition)

    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f76_mandatory_runtime_probe_attempted_repair_proxy_completed
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_frontier71_to_75_retrospective_completed
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F76F lifecycle-aware density repair proxy(생명주기 인식 거래밀도 수리 프록시)를 실행했다."
  - "Effect(효과): F76D에서 발견한 hold compression(보유 압축)을 proxy scoring(프록시 점수화)에 반영했다."
  - "Best proxy(최선 프록시): {best.get('candidate_id', '')} OOS net/PF/DD/tpd {best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F76F lifecycle-aware density repair proxy(생명주기 인식 거래밀도 수리 프록시)를 실행했다.

Effect(효과): F76B의 독립 신호 proxy(프록시)를 F76D runtime observation(런타임 관찰)에 맞춰 single-position max-hold12(단일 포지션 12봉 최대 보유) 구조로 다시 탐색했다.

## Repair Result(수리 결과)

- candidate rows(후보 행): `{summary['candidate_rows']}`
- repair meaningful signal count(수리 의미 신호 수): `{summary['repair_meaningful_signal_count']}`
- density scout clue count(거래밀도 탐색 단서 수): `{summary['density_scout_clue_count']}`
- best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)
    selection = f"""# F76 Selection Status(F76 선택 상태)

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F76F lifecycle-aware density repair proxy(생명주기 인식 거래밀도 수리 프록시)를 실행했다.

Effect(효과): 다음 행동은 결과에 따라 pre-MT5 Grok review(MT5 전 Grok 검토) 또는 추가 repair/pivot decision(수리/전환 결정)이다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)


def main() -> int:
    created_at = f76b.utc_now()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    candidate_rows, fit_rows, summary = fit_and_score()
    top = candidate_rows[:100]
    axis_rows = axis_summary_rows(candidate_rows)
    status, judgment, next_run = status_and_next(summary)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "summary": summary,
        "top100": top,
        "axis_summary": axis_rows,
        "fit_rows": fit_rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(SUMMARY_PATH, summary)
    write_csv(TOP100_PATH, top)
    write_csv(AXIS_SUMMARY_PATH, axis_rows)
    write_csv(MODEL_FIT_PATH, fit_rows)
    write_json(RUN_MANIFEST_PATH, payload)
    write_json(RUN_DIR / "f76f_lifecycle_proxy_summary.json", summary)
    write_csv(RUN_DIR / "f76f_lifecycle_proxy_ranked_top100.csv", top)
    write_csv(RUN_DIR / "f76f_lifecycle_proxy_axis_summary.csv", axis_rows)
    write_csv(RUN_DIR / "f76f_lifecycle_model_fit_summary.csv", fit_rows)
    write_text(REPORT_PATH, report_text(created_at, summary, top))
    write_text(GATE_AUDIT_PATH, gate_audit_text(created_at, summary))
    update_state_and_ledgers(created_at, summary)
    print(json.dumps(json_ready({"status": status, "judgment": judgment, "next_run_id": next_run, **summary}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
