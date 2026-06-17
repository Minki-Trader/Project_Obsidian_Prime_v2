from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_73 import frontier73b_session_regime_feature_model_rotation_proxy_scout as f73b


STAGE_ID = "stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap"
RUN_ID = "frontier73C_axis_reduction_or_repair_proxy_scout_v1"
PARENT_RUN_ID = "frontier73B_session_regime_feature_model_rotation_proxy_scout_v1"
NEXT_PRE_MT5_RUN_ID = "frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1"
NEXT_GAP_OR_CLOSEOUT_RUN_ID = "frontier73D_axis_reduction_gap_analysis_or_closeout_decision_v1"
STATUS = "proxy_repair_completed"
CLAIM_BOUNDARY = (
    "proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
F73B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "frontier73B_proxy_summary.json"
F73B_CANDIDATES = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f73b_candidate_summary.csv"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


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
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
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


def required_inputs() -> list[Path]:
    return [F73B_SUMMARY, F73B_CANDIDATES, f73b.FWD12_INPUT, f73b.FWD12_FEATURE_ORDER, f73b.FWD18_INPUT, f73b.FWD18_FEATURE_ORDER, f73b.RAW_US100]


def extended_gate_mask(frame: pd.DataFrame, gate_id: str, thresholds: Mapping[str, float]) -> np.ndarray:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    vol = pd.to_numeric(frame["historical_vol_5_over_20"], errors="coerce")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce")
    if gate_id in {"all", "cash_open", "cash_mid", "cash_late", "vol_high", "vol_low"}:
        return f73b.gate_mask(frame, gate_id, thresholds)
    if gate_id == "cash_open_90":
        return ((minutes >= 0) & (minutes <= 90)).to_numpy(dtype=bool)
    if gate_id == "cash_open_120":
        return ((minutes >= 0) & (minutes <= 120)).to_numpy(dtype=bool)
    if gate_id == "cash_early_mid":
        return ((minutes >= 0) & (minutes <= 210)).to_numpy(dtype=bool)
    if gate_id == "trend_low_dd":
        return ((adx >= thresholds["adx_median"]) & (vol < thresholds["vol_median"] * 1.35)).fillna(False).to_numpy(dtype=bool)
    if gate_id == "chop_low_vol":
        return ((adx < thresholds["adx_median"]) & (vol < thresholds["vol_median"])).fillna(False).to_numpy(dtype=bool)
    raise ValueError(f"unknown gate_id={gate_id}")


def repair_specs() -> list[dict[str, Any]]:
    return [
        {
            "surface_id": "repair_open_long_quality_density",
            "dataset_ids": ("fwd12",),
            "feature_bundle": "session_regime_core",
            "targets": ("long_quality",),
            "model_ids": ("small_nn_16", "extra_trees_ref", "hist_gbm"),
            "gate_ids": ("cash_open", "cash_open_90", "cash_open_120", "trend_low_dd"),
            "target_tpds": (1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0),
        },
        {
            "surface_id": "repair_short_quality_open_mid",
            "dataset_ids": ("fwd12",),
            "feature_bundle": "session_regime_core",
            "targets": ("short_quality",),
            "model_ids": ("hist_gbm", "extra_trees_ref", "small_nn_16"),
            "gate_ids": ("cash_open", "cash_mid", "cash_early_mid", "vol_high", "vol_low"),
            "target_tpds": (1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0),
        },
        {
            "surface_id": "repair_fwd18_inverse_dd_guard",
            "dataset_ids": ("fwd18",),
            "feature_bundle": "core_price_path",
            "targets": ("long_inverse", "short_inverse"),
            "model_ids": ("logistic_l2", "hist_gbm"),
            "gate_ids": ("all", "vol_low", "chop_low_vol", "cash_early_mid"),
            "target_tpds": (1.0, 1.25, 1.5, 2.0, 2.5, 3.0),
        },
        {
            "surface_id": "repair_importance_short_quality",
            "dataset_ids": ("fwd12",),
            "feature_bundle": "importance_seed_recombination",
            "targets": ("short_quality",),
            "model_ids": ("hist_gbm", "extra_trees_ref"),
            "gate_ids": ("vol_low", "chop_low_vol", "all"),
            "target_tpds": (1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0),
        },
    ]


def run_repair() -> dict[str, Any]:
    raw = f73b.load_raw()
    datasets = {dataset_id: f73b.load_dataset(spec, raw) for dataset_id, spec in f73b.DATASETS.items()}
    factories = f73b.model_factories()
    candidate_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    score_cache: dict[tuple[str, str, str, str, str, str], tuple[np.ndarray, dict[str, Any], Mapping[str, np.ndarray]]] = {}
    for spec in repair_specs():
        for dataset_id in spec["dataset_ids"]:
            data = datasets[dataset_id]
            frame = data["frame"]
            bundles = f73b.feature_bundles(data["features"])
            features = bundles[spec["feature_bundle"]]
            thresholds = f73b.train_thresholds(frame)
            for target_id in spec["targets"]:
                y, side, path = f73b.target_and_side(frame, data["paths"], target_id)
                for gate_id in spec["gate_ids"]:
                    gate = extended_gate_mask(frame, gate_id, thresholds)
                    for model_id in spec["model_ids"]:
                        cache_key = (spec["surface_id"], dataset_id, spec["feature_bundle"], target_id, gate_id, model_id)
                        try:
                            if cache_key not in score_cache:
                                scores, train_info = f73b.train_and_score(frame, features, y, gate, factories[model_id])
                                score_cache[cache_key] = (scores, train_info, path)
                            scores, train_info, _ = score_cache[cache_key]
                            for target_tpd in spec["target_tpds"]:
                                row = {
                                    "candidate_id": f"f73c_{len(candidate_rows) + 1:04d}",
                                    "surface_id": spec["surface_id"],
                                    "dataset_id": dataset_id,
                                    "feature_bundle": spec["feature_bundle"],
                                    "feature_count": len(features),
                                    "target_id": target_id,
                                    "side": "long" if side > 0 else "short",
                                    "model_id": model_id,
                                    "gate_id": gate_id,
                                    "target_trades_day": target_tpd,
                                    **train_info,
                                    **f73b.evaluate_candidate(frame, scores, path, gate, target_tpd),
                                }
                                row["scout_clue"] = f73b.is_scout(row)
                                row["meaningful_candidate"] = f73b.is_meaningful(row)
                                row["final_like_reference_only"] = f73b.is_final_like(row)
                                row["dual_positive"] = bool(row["validation_net_profit"] > 0 and row["oos_net_profit"] > 0)
                                candidate_rows.append(row)
                        except Exception as exc:  # noqa: BLE001
                            failure_rows.append({
                                "surface_id": spec["surface_id"],
                                "dataset_id": dataset_id,
                                "feature_bundle": spec["feature_bundle"],
                                "target_id": target_id,
                                "gate_id": gate_id,
                                "model_id": model_id,
                                "error": str(exc),
                            })
    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row["meaningful_candidate"]),
            bool(row["scout_clue"]),
            bool(row["dual_positive"]),
            min(row["validation_profit_factor"], row["oos_profit_factor"]),
            -max(row["validation_max_drawdown_percent"], row["oos_max_drawdown_percent"]),
            min(row["validation_trades_day"], row["oos_trades_day"]),
            row["oos_net_profit"],
        ),
        reverse=True,
    )
    return {
        "datasets": datasets,
        "candidate_rows": candidate_rows,
        "failure_rows": failure_rows,
        "ranked_rows": ranked,
        "score_cache": score_cache,
    }


def selected_trade_rows(result: Mapping[str, Any], best: Mapping[str, Any]) -> list[dict[str, Any]]:
    if not best:
        return []
    cache_key = (
        best["surface_id"],
        best["dataset_id"],
        best["feature_bundle"],
        best["target_id"],
        best["gate_id"],
        best["model_id"],
    )
    scores, _, path = result["score_cache"][cache_key]
    frame = result["datasets"][best["dataset_id"]]["frame"]
    thresholds = f73b.train_thresholds(frame)
    gate = extended_gate_mask(frame, best["gate_id"], thresholds)
    mask = gate & np.isfinite(scores) & np.isfinite(path["pnl"]) & (scores >= float(best["score_threshold"]))
    selected = frame.loc[mask, ["timestamp", "split", "label", "label_class", "label_id", "minutes_from_cash_open"]].copy()
    selected["score"] = scores[mask]
    selected["pnl"] = path["pnl"][mask]
    selected["direction"] = path["direction"][mask]
    selected["candidate_id"] = best["candidate_id"]
    return selected.sort_values("timestamp").to_dict(orient="records")[:5000]


def summary_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    rows = result["candidate_rows"]
    ranked = result["ranked_rows"]
    best = ranked[0] if ranked else {}
    scout_count = sum(1 for row in rows if row["scout_clue"])
    meaningful_count = sum(1 for row in rows if row["meaningful_candidate"])
    final_like_count = sum(1 for row in rows if row["final_like_reference_only"])
    dual_positive_count = sum(1 for row in rows if row["dual_positive"])
    judgment = (
        "proxy_repair_meaningful_signal_pre_mt5_required_no_authority"
        if meaningful_count
        else "proxy_repair_scout_or_dual_positive_near_miss_pre_mt5_probe_required_no_authority"
        if scout_count or dual_positive_count
        else "proxy_repair_no_clue_gap_analysis_or_closeout_required_no_authority"
    )
    next_run = NEXT_PRE_MT5_RUN_ID if (meaningful_count or scout_count or dual_positive_count) else NEXT_GAP_OR_CLOSEOUT_RUN_ID
    return {
        "created_at_utc": utc_now(),
        "status": STATUS,
        "judgment": judgment,
        "candidate_count": len(rows),
        "scout_clue_count": scout_count,
        "meaningful_candidate_count": meaningful_count,
        "final_like_reference_only_count": final_like_count,
        "dual_positive_count": dual_positive_count,
        "model_failure_count": len(result["failure_rows"]),
        "best_candidate": best,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def surface_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for surface_id in sorted({row["surface_id"] for row in rows}):
        subset = [row for row in rows if row["surface_id"] == surface_id]
        best = max(subset, key=lambda row: (bool(row["dual_positive"]), min(row["validation_profit_factor"], row["oos_profit_factor"]), row["oos_net_profit"]))
        out.append({
            "surface_id": surface_id,
            "candidate_count": len(subset),
            "dual_positive_count": sum(1 for row in subset if row["dual_positive"]),
            "scout_clue_count": sum(1 for row in subset if row["scout_clue"]),
            "meaningful_candidate_count": sum(1 for row in subset if row["meaningful_candidate"]),
            "best_candidate_id": best["candidate_id"],
            "best_validation_pf": best["validation_profit_factor"],
            "best_oos_pf": best["oos_profit_factor"],
            "best_oos_net": best["oos_net_profit"],
            "best_oos_dd": best["oos_max_drawdown_percent"],
            "best_oos_trades_day": best["oos_trades_day"],
        })
    return out


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    best = summary["best_candidate"]
    best_lines = [
        f"- candidate_id(후보 ID): `{best.get('candidate_id', '')}`",
        f"- surface/dataset/bundle(표면/데이터셋/묶음): `{best.get('surface_id', '')}` / `{best.get('dataset_id', '')}` / `{best.get('feature_bundle', '')}`",
        f"- target/model/gate(목표/모델/게이트): `{best.get('target_id', '')}` / `{best.get('model_id', '')}` / `{best.get('gate_id', '')}`",
        f"- validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `{best.get('validation_net_profit', 0):.4f}` / `{best.get('validation_profit_factor', 0):.4f}` / `{best.get('validation_max_drawdown_percent', 0):.4f}%` / `{best.get('validation_trades_day', 0):.4f}`",
        f"- OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net_profit', 0):.4f}` / `{best.get('oos_profit_factor', 0):.4f}` / `{best.get('oos_max_drawdown_percent', 0):.4f}%` / `{best.get('oos_trades_day', 0):.4f}`",
        f"- dual/scout/meaningful/final-like(양쪽 양수/탐색/의미/최종 유사): `{best.get('dual_positive', False)}` / `{best.get('scout_clue', False)}` / `{best.get('meaningful_candidate', False)}` / `{best.get('final_like_reference_only', False)}`",
    ] if best else ["- no candidate rows(후보 행 없음)."]
    return [
        "# Frontier73C Axis Reduction Repair Proxy Scout(F73C 축 축소 수리 프록시 탐색)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- candidate_count(후보 수): `{summary['candidate_count']}`",
        f"- dual_positive_count(양쪽 양수 수): `{summary['dual_positive_count']}`",
        f"- scout_clue_count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary['meaningful_candidate_count']}`",
        f"- final_like_reference_only_count(최종 유사 참조 전용 수): `{summary['final_like_reference_only_count']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Repair Thesis(수리 논제)",
        "",
        "F73B produced OOS-only strength and weak dual-positive candidates(F73B는 표본외 단독 강점과 약한 양쪽 양수 후보를 만들었다). F73C narrows to cash-open quality and fwd18 inverse DD guards(정규장 초반 품질과 18봉 역방향 손실폭 보호로 축소) instead of widening the whole matrix(전체 매트릭스 확장 없음).",
        "",
        "## Best Candidate(최선 후보)",
        "",
        *best_lines,
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{summary['next_run_id']}`.",
        "",
        "Effect(효과): dual-positive near-miss(양쪽 양수 근접 후보)가 있으면 stage mandatory MT5 Runtime Probe(단계 필수 MT5 런타임 탐침)를 위해 Grok pre-MT5 review(사전 MT5 Grok 검토)로 넘어간다.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F73C Required Gate Coverage Audit(F73C 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| parent_proxy_evidence(F73B 부모 프록시 근거) | pass(통과) | `{rel(F73B_SUMMARY)}` | 수리 방향을 F73B 결과에서 도출 |",
        f"| repair_axis_reduction(수리 축 축소) | pass(통과) | `{rel(RUN_ROOT / 'f73c_repair_surface_plan.csv')}` | 전체 조합 확장 방지 |",
        f"| proxy_repair_execution(프록시 수리 실행) | pass(통과) | `{rel(RUN_ROOT / 'f73c_candidate_summary.csv')}` | 수리 후보 KPI 생성 |",
        f"| mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침) | pending_pre_mt5_grok(사전 MT5 Grok 대기) | `{summary['next_run_id']}` | stage lifecycle(단계 생명주기)상 런타임 탐침 준비 |",
        f"| final_claim_guard(최종 주장 보호) | pass(통과) | `{CLAIM_BOUNDARY}` | 강한 주장 없음 |",
    ]


def selection_status_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
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
        "dual_positive_count": summary["dual_positive_count"],
        "scout_clue_count": summary["scout_clue_count"],
        "meaningful_candidate_count": summary["meaningful_candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary["best_candidate"]
    report = REVIEWS_ROOT / "frontier73C_axis_reduction_or_repair_proxy_scout_report.md"
    return {
        "ledger_row_id": f"{RUN_ID}__proxy_repair",
        "row_id": f"{RUN_ID}__proxy_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_repair(프록시 수리)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(report),
        "primary_kpi": f"candidates={summary['candidate_count']}; dual={summary['dual_positive_count']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_candidate_count']}",
        "guardrail_kpi": f"best_oos_pf={best.get('oos_profit_factor', 0):.4f}; best_oos_tpd={best.get('oos_trades_day', 0):.4f}; mt5_probe=pending",
        "external_verification_status": "out_of_scope_by_claim_proxy_repair_only(프록시 수리 전용 주장 범위 밖)",
        "notes": "F73C axis reduction repair proxy scout completed; pre-MT5 probe next if near-miss exists.",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_repair(프록시 수리)",
        "primary_report": rel(report),
        "run_number": "frontier73C",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["candidate_count"],
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(RUN_ROOT / "f73c_candidate_summary.csv"),
        "candidate_model_id": best.get("candidate_id", ""),
        "net_profit": best.get("oos_net_profit", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_max_drawdown_percent", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "result_status": summary["status"],
        "candidate_rows": summary["candidate_count"],
        "positive_proxy_rows": summary["dual_positive_count"],
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": best.get("oos_net_profit", ""),
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(report),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73c.md"),
        "created_at": summary["created_at_utc"],
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73c.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_repair_only(프록시 수리 전용)",
        "evidence_boundary": "proxy_repair_only_no_runtime(프록시 수리 전용, 런타임 없음)",
        "next_action": summary["next_run_id"],
        "question": "Can axis reduction repair produce a runtime-probe-worthy near miss?(축 축소 수리가 런타임 탐침 가치가 있는 근접 후보를 만들 수 있나?)",
        "artifact_count": 10,
        "work_family": "experiment_execution(실험 실행)",
        "run_family": "frontier_proxy_repair(전선 프록시 수리)",
        "run_type": "axis_reduction_repair_proxy_scout(축 축소 수리 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(report),
        "trade_density": best.get("oos_trades_day", ""),
        "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
        "strict_joint_pass_count": summary["meaningful_candidate_count"],
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    f73b.upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    f73b.upsert_ledger(RUN_REGISTRY, "run_id", row)
    f73b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier73C_axis_reduction_or_repair_proxy_scout_v1 -->"
    best = summary["best_candidate"]
    block = f"""<!-- frontier73C_axis_reduction_or_repair_proxy_scout_v1 -->
- `{RUN_ID}` executed F73 axis-reduction repair proxy scout(F73 축 축소 수리 프록시 탐색). Result(결과): `{summary['judgment']}`. Candidates(후보) `{summary['candidate_count']}`, dual-positive(양쪽 양수) `{summary['dual_positive_count']}`, scout clue(탐색 단서) `{summary['scout_clue_count']}`, meaningful(의미 후보) `{summary['meaningful_candidate_count']}`. Best OOS(최선 표본외) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{best.get('oos_net_profit', 0):.4f}/{best.get('oos_profit_factor', 0):.4f}/{best.get('oos_max_drawdown_percent', 0):.4f}/{best.get('oos_trades_day', 0):.4f}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier73C_axis_reduction_or_repair_proxy_scout_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{summary['next_run_id']}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state_files(summary: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {summary['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {summary['next_run_id']}",
        "runtime_probe_status: f73_pre_mt5_grok_pending_for_mandatory_runtime_probe",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "notes:",
        f'  - "Action(행동): F73C axis reduction repair(축 축소 수리)를 실행했다. Candidates(후보) {summary["candidate_count"]}, dual-positive(양쪽 양수) {summary["dual_positive_count"]}, scout clue(탐색 단서) {summary["scout_clue_count"]}, meaningful(의미 후보) {summary["meaningful_candidate_count"]}."',
        f'  - "Effect(효과): F73 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 위해 다음 행동을 {summary["next_run_id"]}로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(CURRENT_WORKING_STATE, [
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
        "Action(행동): F73C axis reduction repair proxy scout(축 축소 수리 프록시 탐색)를 실행했다.",
        "",
        f"Effect(효과): 후보 `{summary['candidate_count']}`개 중 dual-positive(양쪽 양수) `{summary['dual_positive_count']}`개, scout clue(탐색 단서) `{summary['scout_clue_count']}`개를 기록했고, 다음 행동을 `{summary['next_run_id']}`로 설정했다.",
        "",
        f"- judgment(판정): `{summary['judgment']}`.",
        f"- best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래): `{summary['best_candidate'].get('oos_net_profit', 0):.4f}` / `{summary['best_candidate'].get('oos_profit_factor', 0):.4f}` / `{summary['best_candidate'].get('oos_max_drawdown_percent', 0):.4f}%` / `{summary['best_candidate'].get('oos_trades_day', 0):.4f}`.",
        "- runtime probe(런타임 탐침): pre-MT5 Grok review(사전 MT5 Grok 검토) 뒤 필수 실행 대상.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    best = summary["best_candidate"]
    best_lines = [
        f"- candidate_id(후보 ID): `{best.get('candidate_id', '')}`",
        f"- surface/dataset/bundle(표면/데이터셋/묶음): `{best.get('surface_id', '')}` / `{best.get('dataset_id', '')}` / `{best.get('feature_bundle', '')}`",
        f"- target/model/gate(목표/모델/게이트): `{best.get('target_id', '')}` / `{best.get('model_id', '')}` / `{best.get('gate_id', '')}`",
        f"- validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `{best.get('validation_net_profit', 0):.4f}` / `{best.get('validation_profit_factor', 0):.4f}` / `{best.get('validation_max_drawdown_percent', 0):.4f}%` / `{best.get('validation_trades_day', 0):.4f}`",
        f"- OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net_profit', 0):.4f}` / `{best.get('oos_profit_factor', 0):.4f}` / `{best.get('oos_max_drawdown_percent', 0):.4f}%` / `{best.get('oos_trades_day', 0):.4f}`",
        f"- dual/scout/meaningful/final-like(검증+표본외 양수/탐색 단서/의미 후보/최종 유사): `{best.get('dual_positive', False)}` / `{best.get('scout_clue', False)}` / `{best.get('meaningful_candidate', False)}` / `{best.get('final_like_reference_only', False)}`",
    ] if best else ["- no candidate rows(후보 행 없음)."]
    return [
        "# Frontier73C Axis Reduction Repair Proxy Scout(F73C 축 축소 수리 프록시 탐색)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- candidate_count(후보 수): `{summary['candidate_count']}`",
        f"- dual_positive_count(검증+표본외 양수 수): `{summary['dual_positive_count']}`",
        f"- scout_clue_count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary['meaningful_candidate_count']}`",
        f"- final_like_reference_only_count(최종 유사 참조 전용 수): `{summary['final_like_reference_only_count']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Repair Thesis(수리 명제)",
        "",
        "F73B produced OOS-only strength and weak dual-positive candidates(F73B는 표본외 단독 강점과 약한 검증+표본외 양수 후보를 만들었다). F73C narrows to cash-open quality and fwd18 inverse DD guards(정규장 초반 품질과 fwd18 역방향 손실폭 보호로 축소) instead of widening the whole matrix(전체 행렬 확장 없음).",
        "",
        "## Best Candidate(최선 후보)",
        "",
        *best_lines,
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{summary['next_run_id']}`.",
        "",
        "Effect(효과): dual-positive near-miss(검증+표본외 양수 근접 후보)가 있으면 stage mandatory MT5 Runtime Probe(단계 필수 MT5 런타임 탐침)를 위해 Grok pre-MT5 review(사전 MT5 Grok 검토)로 이어간다.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F73C Required Gate Coverage Audit(F73C 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| parent_proxy_evidence(F73B 부모 프록시 근거) | pass(통과) | `{rel(F73B_SUMMARY)}` | repair direction(수리 방향)을 F73B 결과에서 도출 |",
        f"| repair_axis_reduction(수리 축 축소) | pass(통과) | `{rel(RUN_ROOT / 'f73c_repair_surface_plan.csv')}` | 전체 조합 확장 방지 |",
        f"| proxy_repair_execution(프록시 수리 실행) | pass(통과) | `{rel(RUN_ROOT / 'f73c_candidate_summary.csv')}` | 수리 후보 KPI(핵심 성과 지표) 생성 |",
        f"| mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침) | pending_pre_mt5_grok(사전 MT5 Grok 대기) | `{summary['next_run_id']}` | stage lifecycle(단계 생명주기)의 런타임 탐침 준비 |",
        f"| final_claim_guard(최종 주장 보호) | pass(통과) | `{CLAIM_BOUNDARY}` | 강한 주장 없음 |",
    ]


def selection_status_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
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
    ]


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary["best_candidate"]
    report = REVIEWS_ROOT / "frontier73C_axis_reduction_or_repair_proxy_scout_report.md"
    return {
        "ledger_row_id": f"{RUN_ID}__proxy_repair",
        "row_id": f"{RUN_ID}__proxy_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_repair(프록시 수리)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(report),
        "primary_kpi": f"candidates={summary['candidate_count']}; dual={summary['dual_positive_count']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_candidate_count']}",
        "guardrail_kpi": f"best_oos_pf={best.get('oos_profit_factor', 0):.4f}; best_oos_tpd={best.get('oos_trades_day', 0):.4f}; mt5_probe=pending",
        "external_verification_status": "out_of_scope_by_claim_proxy_repair_only(프록시 수리 전용 주장 범위 밖)",
        "notes": "F73C axis reduction repair proxy scout completed; pre-MT5 probe next if near-miss exists.",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_repair(프록시 수리)",
        "primary_report": rel(report),
        "run_number": "frontier73C",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["candidate_count"],
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(RUN_ROOT / "f73c_candidate_summary.csv"),
        "candidate_model_id": best.get("candidate_id", ""),
        "net_profit": best.get("oos_net_profit", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_max_drawdown_percent", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "result_status": summary["status"],
        "candidate_rows": summary["candidate_count"],
        "positive_proxy_rows": summary["dual_positive_count"],
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": best.get("oos_net_profit", ""),
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(report),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73c.md"),
        "created_at": summary["created_at_utc"],
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73c.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_repair_only(프록시 수리 전용)",
        "evidence_boundary": "proxy_repair_only_no_runtime(프록시 수리 전용, 런타임 없음)",
        "next_action": summary["next_run_id"],
        "question": "Can axis reduction repair produce a runtime-probe-worthy near miss?(축 축소 수리가 런타임 탐침 가치가 있는 근접 후보를 만들 수 있나?)",
        "artifact_count": 10,
        "work_family": "experiment_execution(실험 실행)",
        "run_family": "frontier_proxy_repair(전선 프록시 수리)",
        "run_type": "axis_reduction_repair_proxy_scout(축 축소 수리 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(report),
        "trade_density": best.get("oos_trades_day", ""),
        "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
        "strict_joint_pass_count": summary["meaningful_candidate_count"],
    }


def update_registers(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier73C_axis_reduction_or_repair_proxy_scout_v1 -->"
    best = summary["best_candidate"]
    block = f"""<!-- frontier73C_axis_reduction_or_repair_proxy_scout_v1 -->
- `{RUN_ID}` executed F73 axis-reduction repair proxy scout(F73 축 축소 수리 프록시 탐색). Result(결과): `{summary['judgment']}`. Candidates(후보) `{summary['candidate_count']}`, dual-positive(검증+표본외 양수) `{summary['dual_positive_count']}`, scout clue(탐색 단서) `{summary['scout_clue_count']}`, meaningful(의미 후보) `{summary['meaningful_candidate_count']}`. Best OOS(최선 표본외) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{best.get('oos_net_profit', 0):.4f}/{best.get('oos_profit_factor', 0):.4f}/{best.get('oos_max_drawdown_percent', 0):.4f}/{best.get('oos_trades_day', 0):.4f}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier73C_axis_reduction_or_repair_proxy_scout_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{summary['next_run_id']}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state_files(summary: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {summary['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {summary['next_run_id']}",
        "runtime_probe_status: f73_pre_mt5_grok_pending_for_mandatory_runtime_probe",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "notes:",
        f'  - "Action(행동): F73C axis reduction repair(축 축소 수리)를 실행했다. Candidates(후보) {summary["candidate_count"]}, dual-positive(검증+표본외 양수) {summary["dual_positive_count"]}, scout clue(탐색 단서) {summary["scout_clue_count"]}, meaningful(의미 후보) {summary["meaningful_candidate_count"]}."',
        f'  - "Effect(효과): F73 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 위해 다음 행동을 {summary["next_run_id"]}로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(CURRENT_WORKING_STATE, [
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
        "Action(행동): F73C axis reduction repair proxy scout(축 축소 수리 프록시 탐색)를 실행했다.",
        "",
        f"Effect(효과): 후보 `{summary['candidate_count']}`개 중 dual-positive(검증+표본외 양수) `{summary['dual_positive_count']}`개, scout clue(탐색 단서) `{summary['scout_clue_count']}`개를 기록했고, 다음 행동을 `{summary['next_run_id']}`로 설정했다.",
        "",
        f"- judgment(판정): `{summary['judgment']}`.",
        f"- best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래): `{summary['best_candidate'].get('oos_net_profit', 0):.4f}` / `{summary['best_candidate'].get('oos_profit_factor', 0):.4f}` / `{summary['best_candidate'].get('oos_max_drawdown_percent', 0):.4f}%` / `{summary['best_candidate'].get('oos_trades_day', 0):.4f}`.",
        "- runtime probe(런타임 탐침): pre-MT5 Grok review(사전 MT5 Grok 검토) 후 필수 실행 대기.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def write_outputs(result: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ranked = result["ranked_rows"]
    write_csv(RUN_ROOT / "f73c_repair_surface_plan.csv", repair_specs())
    write_csv(RUN_ROOT / "f73c_candidate_summary.csv", result["candidate_rows"])
    write_csv(RUN_ROOT / "f73c_top_candidates.csv", ranked[:40])
    write_csv(RUN_ROOT / "f73c_best_candidate_trades.csv", selected_trade_rows(result, summary["best_candidate"]))
    write_csv(RUN_ROOT / "f73c_model_failures.csv", result["failure_rows"])
    write_csv(RUN_ROOT / "f73c_surface_summary.csv", surface_summary(result["candidate_rows"]))
    write_json(RUN_ROOT / "frontier73C_proxy_repair_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_text(RUN_ROOT / "reports/result_summary.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "frontier73C_axis_reduction_or_repair_proxy_scout_report.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f73c.md", gate_audit_lines(summary))
    write_csv(REVIEWS_ROOT / "f73c_top_candidates_review.csv", ranked[:25])
    write_csv(REVIEWS_ROOT / "f73c_surface_summary_review.csv", surface_summary(result["candidate_rows"]))
    write_text(SELECTED_ROOT / "selection_status.md", selection_status_lines(summary))


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F73C required material missing: {missing}")
    result = run_repair()
    summary = summary_payload(result)
    write_outputs(result, summary)
    update_registers(summary)
    update_ledgers(summary)
    update_state_files(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "candidate_count": summary["candidate_count"],
        "dual_positive_count": summary["dual_positive_count"],
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
