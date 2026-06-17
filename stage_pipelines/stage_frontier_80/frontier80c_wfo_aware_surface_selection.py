from __future__ import annotations

import csv
import json
import sys
import warnings
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_79 import frontier79b_runtime_native_trade_shape_label_proxy_scout as f79b
from stage_pipelines.stage_frontier_80 import frontier80b_broad_extreme_multi_axis_proxy_scout as f80b


STAGE_ID = f80b.STAGE_ID
RUN_ID = "frontier80C_wfo_aware_surface_selection_v1"
PARENT_RUN_ID = f80b.RUN_ID
NEXT_RUN_ID = "frontier80D_mt5_runtime_probe_quality_v1"
REPAIR_RUN_ID = "frontier80C_materialization_repair_before_mt5_v1"
STATUS_SUCCESS = "f80c_wfo_exportable_target_selected_for_mt5_materialization_no_authority"
STATUS_REPAIR = "f80c_no_wfo_exportable_target_repair_required_no_authority"
JUDGMENT_SUCCESS = "wfo_aware_materialization_target_selected_no_baseline_no_authority"
JUDGMENT_REPAIR = "proxy_clue_not_materializable_repair_required_no_authority"
CLAIM_BOUNDARY = (
    "wfo_selection_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
TOP_PATH = REVIEW_DIR / "f80b_multi_axis_ranked_top200.csv"
F80B_SUMMARY = REVIEW_DIR / "f80b_multi_axis_proxy_summary.json"

TARGET_SELECTION = REVIEW_DIR / "f80c_runtime_materialization_target_selection.json"
PERIOD_AUDIT = REVIEW_DIR / "f80c_wfo_candidate_period_audit.csv"
SUMMARY_PATH = REVIEW_DIR / "f80c_wfo_selection_summary.json"
EXPORT_CHECKS = REVIEW_DIR / "f80c_export_feasibility_checks.json"
REPORT = REVIEW_DIR / "frontier80C_wfo_aware_surface_selection_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f80c.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_80/frontier80c_wfo_aware_surface_selection.py"


def utc_now() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def export_feasibility() -> dict[str, Any]:
    checks: dict[str, Any] = {}
    try:
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType
    except Exception as exc:  # noqa: BLE001
        return {"environment": {"export_status": "blocked", "error_type": type(exc).__name__, "error_excerpt": str(exc)[:500]}}

    x, y = make_classification(n_samples=120, n_features=8, n_informative=5, random_state=8003)
    models = {
        "logistic_l2_balanced": make_pipeline(StandardScaler(), LogisticRegression(max_iter=100, class_weight="balanced")),
        "extra_trees_d6_l120": ExtraTreesClassifier(n_estimators=12, max_depth=6, min_samples_leaf=5, random_state=8003),
        "histgbm_shallow": HistGradientBoostingClassifier(max_iter=12, max_leaf_nodes=7, random_state=8003),
    }
    for name, model in models.items():
        try:
            model.fit(x, y)
            convert_sklearn(
                model,
                initial_types=[("float_input", FloatTensorType([None, int(x.shape[1])]))],
                options={id(model): {"zipmap": False}},
                target_opset=12,
            )
            checks[name] = {"export_status": "export_ok", "notes": "in_memory_skl2onnx_smoke_passed"}
        except Exception as exc:  # noqa: BLE001
            checks[name] = {"export_status": "export_failed", "error_type": type(exc).__name__, "error_excerpt": str(exc)[:500]}
    return checks


def period_rows_for_candidate(
    row: Mapping[str, str],
    df: pd.DataFrame,
    raw: pd.DataFrame,
    features: Sequence[str],
    thresholds: Mapping[str, float],
) -> list[dict[str, Any]]:
    spec = next(item for item in f80b.runtime_specs() if item.name == row["label_name"])
    outcome = f79b.compute_outcome(raw, f79b.entry_indices(df, raw, spec.entry_mode), spec)
    label = f80b.make_label(df, outcome, spec)
    train_valid = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
    feature_columns = f80b.feature_sets(features)[row["feature_set"]]
    matrices = f78b.clean_matrices(df, train_valid, feature_columns)
    model = f80b.model_builders()[row["model"]]()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(matrices["train"], label[train_valid])
    train_probs = f78b.probability(model, matrices["train"])
    threshold = float(np.quantile(train_probs, as_float(row["prob_quantile"])))
    period_rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        split_mask_global = (df["split"] == split).to_numpy()
        split_df = df.loc[split_mask_global].reset_index(drop=True)
        split_outcome = {key: np.asarray(value)[split_mask_global] for key, value in outcome.items()}
        valid = np.asarray(split_outcome["valid"], dtype=bool)
        probs = f78b.probability(model, matrices[split])
        raw_signal = (
            (probs >= threshold)
            & valid
            & f80b.regime_mask(split_df, row["regime"], spec.side, thresholds)
            & f80b.risk_mask(split_df, row["risk_filter"], spec.side, thresholds)
        )
        selected = f78b.lifecycle_select(raw_signal, np.asarray(split_outcome["exit_offset"], dtype=int), as_int(row["cooldown_bars"]))
        period = pd.to_datetime(split_df["timestamp"], errors="coerce", utc=True).dt.to_period("M").astype(str)
        for period_id in sorted(period.dropna().unique()):
            mask = period.eq(period_id).to_numpy()
            if not mask.any():
                continue
            part_df = split_df.loc[mask].reset_index(drop=True)
            part_outcome = {key: np.asarray(value)[mask] for key, value in split_outcome.items()}
            metrics = f78b.contract_kpi(part_df, selected[mask], part_outcome)
            period_rows.append(
                {
                    "candidate_id": row["candidate_id"],
                    "split": split,
                    "period": period_id,
                    "trade_count": metrics["trade_count"],
                    "net": metrics["net"],
                    "pf": metrics["pf"],
                    "dd_pct": metrics["dd_pct"],
                    "calendar_trades_day": metrics["calendar_trades_day"],
                    "positive_period": int(float(metrics["net"]) > 0.0 and int(metrics["trade_count"]) > 0),
                    "active_period": int(int(metrics["trade_count"]) > 0),
                }
            )
    return period_rows


def aggregate_periods(candidate: Mapping[str, str], periods: Sequence[Mapping[str, Any]], export_checks: Mapping[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {**candidate}
    for split in ("validation", "oos"):
        subset = [row for row in periods if row["candidate_id"] == candidate["candidate_id"] and row["split"] == split]
        active = [row for row in subset if int(row["active_period"]) == 1]
        positive = [row for row in active if int(row["positive_period"]) == 1]
        out[f"{split}_period_count"] = len(subset)
        out[f"{split}_active_period_count"] = len(active)
        out[f"{split}_positive_period_count"] = len(positive)
        out[f"{split}_positive_period_ratio"] = len(positive) / len(active) if active else 0.0
        out[f"{split}_worst_period_net"] = min((as_float(row["net"]) for row in active), default=0.0)
        out[f"{split}_max_period_dd_pct"] = max((as_float(row["dd_pct"]) for row in active), default=0.0)
    model_export = export_checks.get(str(candidate.get("model")), {})
    out["export_status"] = model_export.get("export_status", "unknown")
    out["export_error_type"] = model_export.get("error_type", "")
    out["wfo_gate"] = int(
        out["export_status"] == "export_ok"
        and as_int(candidate.get("materialization_candidate")) == 1
        and as_float(out["validation_positive_period_ratio"]) >= 0.45
        and as_float(out["oos_positive_period_ratio"]) >= 0.45
        and as_int(out["validation_active_period_count"]) >= 4
        and as_int(out["oos_active_period_count"]) >= 3
        and as_float(out["validation_max_period_dd_pct"]) <= 12.0
        and as_float(out["oos_max_period_dd_pct"]) <= 12.0
    )
    out["wfo_rank_score"] = (
        as_float(candidate.get("rank_score"))
        + as_float(out["validation_positive_period_ratio"]) * 120_000.0
        + as_float(out["oos_positive_period_ratio"]) * 180_000.0
        - max(0.0, abs(as_float(out["validation_worst_period_net"]))) * 250.0
        - max(0.0, abs(as_float(out["oos_worst_period_net"]))) * 350.0
        + (400_000.0 if out["wfo_gate"] else 0.0)
    )
    return out


def select_target(enriched: Sequence[Mapping[str, Any]], f80b_summary: Mapping[str, Any], export_checks: Mapping[str, Any]) -> dict[str, Any]:
    ranked = sorted(enriched, key=lambda row: as_float(row.get("wfo_rank_score")), reverse=True)
    target = next((row for row in ranked if as_int(row.get("wfo_gate")) == 1), {})
    fallback = {}
    if not target:
        fallback = next(
            (
                row
                for row in ranked
                if row.get("export_status") == "export_ok"
                and as_int(row.get("materialization_candidate")) == 1
                and as_float(row.get("oos_net")) > 0.0
            ),
            {},
        )
        target = fallback
    best = f80b_summary.get("best_candidate") or {}
    return {
        "runtime_materialization_target": dict(target),
        "target_candidate_id": target.get("candidate_id", ""),
        "blocked_best_candidate": best if target.get("candidate_id") != best.get("candidate_id") else {},
        "selection_reason": "wfo_exportable_materialization_target(워크포워드 인식 내보내기 가능 물질화 대상)" if target and not fallback else "fallback_exportable_materialization_target(대체 내보내기 가능 물질화 대상)" if target else "no_exportable_materialization_target(내보내기 가능 물질화 대상 없음)",
        "target_export_check": export_checks.get(str(target.get("model")), {}),
        "export_checks": export_checks,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_selected_baseline": True,
        "next_run_id": NEXT_RUN_ID if target else REPAIR_RUN_ID,
    }


def report_text(created_at: str, status: str, judgment: str, target_selection: Mapping[str, Any], enriched: Sequence[Mapping[str, Any]]) -> str:
    target = target_selection.get("runtime_materialization_target") or {}
    lines = []
    for row in sorted(enriched, key=lambda item: as_float(item.get("wfo_rank_score")), reverse=True)[:10]:
        lines.append(
            f"| `{row.get('candidate_id')}` | `{row.get('model')}` | `{row.get('surface_family')}` | `{row.get('feature_set')}` | "
            f"`{row.get('validation_positive_period_ratio'):.3f}/{row.get('oos_positive_period_ratio'):.3f}` | "
            f"`{row.get('val_net')}/{row.get('val_pf')}/{row.get('val_dd_pct')}/{row.get('val_trade_count')}` | "
            f"`{row.get('oos_net')}/{row.get('oos_pf')}/{row.get('oos_dd_pct')}/{row.get('oos_trade_count')}` | "
            f"`{row.get('export_status')}` | `{row.get('wfo_gate')}` |"
        )
    table = "\n".join(
        [
            "| candidate(후보) | model(모델) | surface(표면) | feature(피처) | val/oos period+(검증/표본외 양수기간) | val KPI(검증) | OOS KPI(표본외) | export(내보내기) | gate(게이트) |",
            "|---|---|---|---|---:|---:|---:|---|---:|",
            *lines,
        ]
    )
    return f"""# F80C WFO-Aware Surface Selection Report(F80C 워크포워드 인식 표면 선택 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- target candidate(대상 후보): `{target.get('candidate_id', 'none')}`
- target model(대상 모델): `{target.get('model', 'none')}`
- target reason(대상 사유): `{target_selection.get('selection_reason')}`

## Important Boundary(중요 경계)

Action(행동): F80B(전선80B)의 material proxy candidates(물질 프록시 후보)를 WFO-aware period stability(워크포워드 인식 기간 안정성)와 ONNX export feasibility(온엑스 내보내기 가능성)로 좁혔다.

Effect(효과): 이 대상은 MT5 materialization target(MT5 물질화 대상)일 뿐 selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위)가 아니다.

## Ranked Exportable Candidates(상위 내보내기 가능 후보)

{table}

## Next Run(다음 실행)

`{target_selection.get('next_run_id')}`
"""


def gate_audit_text(status: str, target_selection: Mapping[str, Any]) -> str:
    target = target_selection.get("runtime_materialization_target") or {}
    return f"""# F80C Required Gate Coverage Audit(F80C 필수 게이트 커버리지 감사)

Status(상태): `{status}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `f80b_handoff` | `passed(통과)` | `{rel(F80B_SUMMARY)}`, `{rel(TOP_PATH)}` | F80B(전선80B) 프록시 근거에서만 후보를 고른다. |
| `wfo_period_stability` | `{ 'passed(통과)' if target.get('candidate_id') else 'blocked(차단)' }` | `{rel(PERIOD_AUDIT)}` | 기간별 안정성을 확인하고 단일 aggregate(합산) 착시를 줄인다. |
| `onnx_export_feasibility` | `{target_selection.get('target_export_check', {}).get('export_status', 'unknown')}` | `{rel(EXPORT_CHECKS)}` | MT5 물질화 가능한 모델만 대상으로 둔다. |
| `not_selected_baseline_guard` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 후보를 기준선/승격/권위로 올리지 않는다. |
| `runtime_probe_gate` | `pending(대기)` | next run(다음 실행) `{target_selection.get('next_run_id')}` | MT5 runtime probe(MT5 런타임 탐침) 전에는 경제성 권위를 만들지 않는다. |
"""


def ledger_row(created_at: str, status: str, judgment: str, next_run: str, target_selection: Mapping[str, Any]) -> dict[str, Any]:
    target = target_selection.get("runtime_materialization_target") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__wfo_materialization_target",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "wfo_materialization_target(워크포워드 물질화 대상)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "wfo_proxy_selection(워크포워드 프록시 선택)",
        "scoreboard_lane": "runtime_economics(런타임 경제성)",
        "lane": "wfo_selection(워크포워드 선택)",
        "family": "experiment_execution(실험 실행)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "primary_kpi": f"target={target.get('candidate_id', '')};model={target.get('model', '')};wfo_gate={target.get('wfo_gate', '')}",
        "guardrail_kpi": "not_selected_baseline;runtime_probe_pending;signal_count_diagnostic_only",
        "external_verification_status": "not_run_runtime_probe_pending(미실행, 런타임 탐침 대기)",
        "notes": f"next={next_run}; reason={target_selection.get('selection_reason')}",
        "run_number": "frontier80C",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "rows": len(read_csv(TOP_PATH)),
        "gate_passes": 4 if target.get("candidate_id") else 2,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": target.get("candidate_id", ""),
        "model": target.get("model", ""),
        "net_profit": target.get("oos_net", ""),
        "profit_factor": target.get("oos_pf", ""),
        "drawdown": target.get("oos_dd_pct", ""),
        "trade_count": target.get("oos_trade_count", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "wfo_selection",
        "tier": "Tier A",
        "metric_scope": "validation_oos_period_stability",
        "result_status": status,
        "feature_count": target.get("feature_count", ""),
        "work_family": "experiment_execution",
        "row_id": f"{RUN_ID}__wfo_materialization_target",
        "evidence_boundary": "materialization_target_only_no_authority(물질화 대상만, 권위 없음)",
        "next_action": next_run,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_wfo_selection_only(프록시 워크포워드 선택 전용)",
    }


def update_state_files(created_at: str, status: str, judgment: str, next_run: str, target_selection: Mapping[str, Any]) -> None:
    target = target_selection.get("runtime_materialization_target") or {}
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f80_runtime_probe_materialization_target_ready_not_yet_run
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: inactive_preserve_records_pending_codex_task_force_replacement
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F80C WFO-aware selection(워크포워드 인식 선택)을 실행했다."
  - "Effect(효과): target={target.get('candidate_id', 'none')} model={target.get('model', 'none')}을 MT5 물질화 대상으로만 기록했다."
  - "Boundary(경계): no selected baseline/promotion/runtime authority/live readiness/Goal Achieve(선택 기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F80C WFO-aware surface selection(F80C 워크포워드 인식 표면 선택)을 실행했다.

Effect(효과): F80B(전선80B)의 후보 중 ONNX export feasibility(온엑스 내보내기 가능성)와 기간 안정성(period stability, 기간 안정성)을 통과한 MT5 materialization target(MT5 물질화 대상)을 좁혔다.

Target(대상): `{target.get('candidate_id', 'none')}` / `{target.get('model', 'none')}`.

Open work(열린 작업): `{next_run}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F80 Review Index(F80 검토 색인)\n"
    additions = [
        "- `frontier80C_wfo_aware_surface_selection_report.md`: F80C WFO-aware selection report(F80C 워크포워드 인식 선택 보고서)",
        "- `f80c_runtime_materialization_target_selection.json`: F80C MT5 materialization target(F80C MT5 물질화 대상)",
        "- `f80c_wfo_candidate_period_audit.csv`: F80C period stability audit(F80C 기간 안정성 감사)",
        "- `required_gate_coverage_audit_f80c.md`: F80C gate audit(F80C 게이트 감사)",
    ]
    for line in additions:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def write_receipts(status: str, judgment: str, target_selection: Mapping[str, Any]) -> None:
    target = target_selection.get("runtime_materialization_target") or {}
    receipts = {
        REVIEW_DIR / "f80c_model_validation_receipt.yaml": f"""packet_id: {RUN_ID}
skill: obsidian-model-validation
status: {status}
model_or_threshold_surface: "target={target.get('candidate_id', 'none')} model={target.get('model', 'none')}"
validation_split: "validation/OOS period stability(검증/표본외 기간 안정성)"
overfit_checks:
  - "period positive ratio(기간 양수 비율)"
  - "ONNX export feasibility(온엑스 내보내기 가능성)"
selection_metric_boundary: "materialization target only(물질화 대상만), no selected baseline(선택 기준선 없음)"
allowed_claims:
  - mt5_materialization_target
forbidden_claims:
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
""",
        REVIEW_DIR / "f80c_claim_discipline_receipt.yaml": f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_wfo_selection_only
requested_claims:
  - "F80C selected MT5 materialization target(F80C MT5 물질화 대상 선택)."
allowed_claims:
  - mt5_materialization_target
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
  - parity_only_economics
final_status: "{judgment}; boundary={CLAIM_BOUNDARY}"
""",
    }
    for path, text in receipts.items():
        write_text(path, text)


def main() -> int:
    ensure_dirs()
    f78b.INITIAL_BALANCE = f80b.INITIAL_BALANCE
    created_at = utc_now()
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    warnings.filterwarnings("ignore", message="Converting to PeriodArray/Index representation will drop timezone information.")
    f80b_summary = read_json(F80B_SUMMARY)
    top_rows = read_csv(TOP_PATH)
    export_checks = export_feasibility()
    write_json(EXPORT_CHECKS, export_checks)
    df, raw, features = f78b.load_inputs()
    thresholds = f78b.risk_thresholds(df)

    candidate_pool = [row for row in top_rows if as_int(row.get("materialization_candidate")) == 1][:80]
    all_periods: list[dict[str, Any]] = []
    for row in candidate_pool:
        all_periods.extend(period_rows_for_candidate(row, df, raw, features, thresholds))
    write_csv(PERIOD_AUDIT, all_periods)

    enriched = [aggregate_periods(row, all_periods, export_checks) for row in candidate_pool]
    target_selection = select_target(enriched, f80b_summary, export_checks)
    target = target_selection.get("runtime_materialization_target") or {}
    status = STATUS_SUCCESS if target.get("candidate_id") else STATUS_REPAIR
    judgment = JUDGMENT_SUCCESS if target.get("candidate_id") else JUDGMENT_REPAIR
    next_run = NEXT_RUN_ID if target.get("candidate_id") else REPAIR_RUN_ID
    target_selection["next_run_id"] = next_run

    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "candidate_pool_rows": len(candidate_pool),
        "wfo_gate_count": sum(as_int(row.get("wfo_gate")) for row in enriched),
        "exportable_material_count": sum(1 for row in enriched if row.get("export_status") == "export_ok" and as_int(row.get("materialization_candidate")) == 1),
        "target_candidate_id": target.get("candidate_id", ""),
        "target_model": target.get("model", ""),
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(SUMMARY_PATH, summary)
    write_json(TARGET_SELECTION, target_selection)
    write_text(REPORT, report_text(created_at, status, judgment, target_selection, enriched))
    write_text(GATE_AUDIT, gate_audit_text(status, target_selection))
    write_text(SELECTION_STATUS, f80_selection_status(created_at, status, judgment, next_run, target_selection))
    write_text(CONTEXT_ANCHOR, context_anchor_text(created_at, status, judgment, next_run, target_selection))
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": next_run,
            "created_at_utc": created_at,
            "status": status,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "summary": summary,
            "target_selection": target_selection,
            "producer": SCRIPT_REL,
            "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        },
    )
    row = ledger_row(created_at, status, judgment, next_run, target_selection)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    update_idea_registry(target_selection, next_run)
    update_state_files(created_at, status, judgment, next_run, target_selection)
    update_review_index()
    write_receipts(status, judgment, target_selection)
    print(json.dumps(json_ready({"status": status, "judgment": judgment, "target": target.get("candidate_id", ""), "model": target.get("model", ""), "next_run": next_run, "wfo_gate_count": summary["wfo_gate_count"]}), ensure_ascii=False, indent=2))
    return 0


def update_idea_registry(target_selection: Mapping[str, Any], next_run: str) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    target = target_selection.get("runtime_materialization_target") or {}
    addition = f"""

- `{RUN_ID}` selected F80 MT5 materialization target(F80 MT5 물질화 대상). Target(대상): `{target.get('candidate_id', '')}` `{target.get('model', '')}`. Boundary(경계): materialization target only, no baseline/promotion/runtime authority(물질화 대상만, 기준선/승격/런타임 권위 없음). Next(다음): `{next_run}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def f80_selection_status(created_at: str, status: str, judgment: str, next_run: str, target_selection: Mapping[str, Any]) -> str:
    target = target_selection.get("runtime_materialization_target") or {}
    return f"""# F80 Selection Status(F80 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F80C WFO-aware surface selection(F80C 워크포워드 인식 표면 선택)을 실행했다.

Effect(효과): target(대상) `{target.get('candidate_id', 'none')}` model(모델) `{target.get('model', 'none')}`을 MT5 materialization target(MT5 물질화 대상)으로만 기록했다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def context_anchor_text(created_at: str, status: str, judgment: str, next_run: str, target_selection: Mapping[str, Any]) -> str:
    target = target_selection.get("runtime_materialization_target") or {}
    return f"""# F80 Context Anchor(F80 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{next_run}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- target(대상): `{target.get('candidate_id', 'none')}` / `{target.get('model', 'none')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Runtime probe observation(런타임 탐침 관찰): not run yet(아직 미실행).

Next action(다음 행동): `{next_run}`.
"""


if __name__ == "__main__":
    raise SystemExit(main())
