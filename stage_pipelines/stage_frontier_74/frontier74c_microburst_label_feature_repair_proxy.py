from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_74 import frontier74b_microburst_turnover_raw_label_and_proxy_scout as base


STAGE_ID = "stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path"
RUN_ID = "frontier74C_microburst_label_feature_repair_proxy_v1"
PARENT_RUN_ID = "frontier74B_microburst_turnover_raw_label_and_proxy_scout_v1"
NEXT_PRE_MT5_RUN_ID = "frontier74D_pre_mt5_grok_microburst_clean_value_runtime_probe_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier74D_microburst_risk_session_repair_or_closeout_v1"
STATUS = "proxy_repair_completed_no_authority"
CLAIM_BOUNDARY = (
    "proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F74B_MANIFEST = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F74B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f74b_summary.json"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"

TARGET_TPD_VALUES = [9.0, 12.0, 15.0, 18.0]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, lines: Sequence[str]) -> None:
    write_text(path, "\n".join(lines))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        rows = [{"empty": "true"}]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.rstrip())


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
        raise FileNotFoundError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def required_inputs() -> list[Path]:
    return [F74B_MANIFEST, F74B_SUMMARY, ALPHA_LEDGER, RUN_REGISTRY, base.FWD12_INPUT, base.FWD12_FEATURE_ORDER, base.RAW_US100]


def repair_axes() -> list[base.AxisSpec]:
    axes: list[base.AxisSpec] = []
    for horizon, target, stop in ((3, 0.45, 0.25), (6, 0.70, 0.35), (9, 1.00, 0.45)):
        axes.append(base.AxisSpec(f"clean_value_h{horizon}_long", horizon, "long(롱)", 1, target, stop))
        axes.append(base.AxisSpec(f"clean_value_h{horizon}_short", horizon, "short(숏)", -1, target, stop))
    return axes


def label_modes(frame: Any, path: Mapping[str, np.ndarray], axis: base.AxisSpec) -> dict[str, np.ndarray]:
    finite = np.isfinite(path["pnl"])
    train = frame["split"].astype(str).eq("train").to_numpy(dtype=bool) & finite
    fast_limit = max(1, int(math.ceil(axis.horizon_bars * 0.67)))
    clean = (
        path["hit"]
        & (~path["adverse_first"])
        & (path["first_touch_bar"] > 0)
        & (path["first_touch_bar"] <= fast_limit)
        & (path["pnl"] > 0)
    )
    train_clean_pnl = path["pnl"][train & clean]
    q60 = float(np.quantile(train_clean_pnl, 0.60)) if len(train_clean_pnl) else 0.0
    train_all_pnl = path["pnl"][train]
    q70 = float(np.quantile(train_all_pnl[np.isfinite(train_all_pnl)], 0.70)) if len(train_all_pnl) else 0.0
    return {
        "clean_fast_touch": clean.astype(float),
        "clean_value_q60": (clean & (path["pnl"] >= q60)).astype(float),
        "net_edge_q70": ((path["pnl"] >= q70) & finite).astype(float),
    }


def label_density_rows(frame: Any, modes_by_axis: Mapping[str, Mapping[str, np.ndarray]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis in repair_axes():
        for mode_id, y in modes_by_axis[axis.axis_id].items():
            finite = np.isfinite(y)
            for split in ("train", "validation", "oos"):
                split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool) & finite
                hit_mask = split_mask & (y >= 0.5)
                days = base.split_days(frame.loc[split_mask, "timestamp"])
                rows.append(
                    {
                        "axis_id": axis.axis_id,
                        "label_mode": mode_id,
                        "split": split,
                        "side": axis.side,
                        "horizon_bars": axis.horizon_bars,
                        "target_atr": axis.target_atr,
                        "stop_atr": axis.stop_atr,
                        "label_count": int(hit_mask.sum()),
                        "label_rate": float(hit_mask.sum() / max(split_mask.sum(), 1)),
                        "label_trades_day": float(hit_mask.sum() / days),
                    }
                )
    return rows


def run_repair() -> dict[str, Any]:
    frame = base.load_frame()
    raw = base.load_raw()
    positions = base.align_raw(frame, raw)
    axes = repair_axes()
    paths = {axis.axis_id: base.compute_axis_path(frame, raw, positions, axis) for axis in axes}
    modes_by_axis = {axis.axis_id: label_modes(frame, paths[axis.axis_id], axis) for axis in axes}
    density_rows = label_density_rows(frame, modes_by_axis)
    feature_groups = base.feature_bundles(base.feature_order())
    feature_groups = {key: value for key, value in feature_groups.items() if key in {"micro_path_core", "session_micro_path", "core_no_external"}}
    factories_all = base.model_factories()
    factories = {key: factories_all[key] for key in ("logistic_l2", "hist_gbm")}
    thresholds = base.gate_thresholds(frame)
    gate_ids = ["all", "cash_mid_late", "vol_adx_active"]
    candidates: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    selected_cache: dict[str, tuple[np.ndarray, Mapping[str, np.ndarray], base.AxisSpec, np.ndarray]] = {}
    for axis in axes:
        path = paths[axis.axis_id]
        for mode_id, y in modes_by_axis[axis.axis_id].items():
            y = y.astype(float)
            y[~np.isfinite(path["pnl"])] = np.nan
            for bundle_id, features in feature_groups.items():
                for gate_id in gate_ids:
                    gate = base.gate_mask(frame, gate_id, thresholds)
                    for model_id, factory in factories.items():
                        try:
                            scores, fit_meta = base.train_scores(frame, features, y, gate, factory)
                        except Exception as exc:  # noqa: BLE001 - recorded as repair failure evidence.
                            failures.append(
                                {
                                    "axis_id": axis.axis_id,
                                    "label_mode": mode_id,
                                    "feature_bundle": bundle_id,
                                    "gate_id": gate_id,
                                    "model_id": model_id,
                                    "reason": str(exc),
                                }
                            )
                            continue
                        for target_tpd in TARGET_TPD_VALUES:
                            row = {
                                "candidate_id": f"f74c_{len(candidates):04d}",
                                "axis_id": axis.axis_id,
                                "label_mode": mode_id,
                                "side": axis.side,
                                "horizon_bars": axis.horizon_bars,
                                "target_atr": axis.target_atr,
                                "stop_atr": axis.stop_atr,
                                "feature_bundle": bundle_id,
                                "feature_count": len(features),
                                "gate_id": gate_id,
                                "model_id": model_id,
                                "target_trades_day": target_tpd,
                                **fit_meta,
                            }
                            row.update(base.evaluate_candidate(frame, positions, scores, path, gate, axis, target_tpd))
                            row["scout_clue"] = base.is_scout(row)
                            row["meaningful_candidate"] = base.is_meaningful(row)
                            row["final_like_reference_only"] = base.is_final_like(row)
                            candidates.append(row)
                            selected_cache[row["candidate_id"]] = (scores, path, axis, gate)
    ranked = sorted(
        candidates,
        key=lambda row: (
            bool(row["meaningful_candidate"]),
            bool(row["scout_clue"]),
            row["validation_profit_factor"],
            row["oos_profit_factor"],
            row["validation_net_profit"] + row["oos_net_profit"],
            -row["validation_max_drawdown_percent"],
            -row["oos_max_drawdown_percent"],
        ),
        reverse=True,
    )
    best = ranked[0] if ranked else {}
    selected = base.selected_trade_rows(frame, positions, selected_cache, best)
    return {
        "density_rows": density_rows,
        "candidate_rows": candidates,
        "failure_rows": failures,
        "ranked_rows": ranked,
        "best": best,
        "selected_rows": selected,
    }


def next_action(summary: Mapping[str, Any]) -> tuple[str, str]:
    if int(summary["meaningful_candidate_count"]) > 0:
        return NEXT_PRE_MT5_RUN_ID, "meaningful_proxy_repair_pre_mt5_grok_required(의미 프록시 수리, MT5 전 Grok 필요)"
    if int(summary["scout_clue_count"]) > 0:
        return NEXT_PRE_MT5_RUN_ID, "scout_clue_proxy_repair_pre_mt5_grok_required(탐색 단서 프록시 수리, MT5 전 Grok 필요)"
    return NEXT_REPAIR_OR_CLOSEOUT_RUN_ID, "repair_no_scout_clue_needs_risk_session_decision(수리 후 탐색 단서 없음, 위험/세션 결정 필요)"


def report_lines(created_at: str, summary: Mapping[str, Any], best: Mapping[str, Any], next_run: str) -> list[str]:
    best_line = "none(없음)"
    if best:
        best_line = (
            f"`{best['candidate_id']}` {best['axis_id']} {best['label_mode']} {best['model_id']} "
            f"validation/OOS PF(검증/표본외 수익 팩터) `{best['validation_profit_factor']:.4f}/{best['oos_profit_factor']:.4f}`, "
            f"DD(손실폭) `{best['validation_max_drawdown_percent']:.4f}/{best['oos_max_drawdown_percent']:.4f}`, "
            f"tpd(일거래) `{best['validation_trades_day']:.4f}/{best['oos_trades_day']:.4f}`"
        )
    return [
        "# Frontier74C Clean/Value Label Repair Proxy(F74C 깨끗한/가치 라벨 수리 프록시)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        f"- next_run_id(다음 실행 ID): `{next_run}`",
        "",
        "## Repair Hypothesis(수리 가설)",
        "",
        "F74B first-touch label(선도달 라벨)은 dense(조밀)했지만 validation drawdown(검증 손실폭)이 컸다. F74C는 adverse-first(불리 선도달), slow touch(느린 도달), low-value touch(낮은 가치 도달)를 라벨에서 제거해 signal quality(신호 품질)를 높일 수 있는지 시험했다.",
        "",
        "## KPI Summary(KPI 요약)",
        "",
        f"- candidate_rows(후보 행): `{summary['candidate_count']}`",
        f"- failure_rows(실패 행): `{summary['failure_count']}`",
        f"- scout_clue_count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary['meaningful_candidate_count']}`",
        f"- final_like_reference_only(최종 유사 참조 전용): `{summary['final_like_reference_only_count']}`",
        f"- best_candidate(최선 후보): {best_line}",
        "",
        "## Attribution(귀속)",
        "",
        "observed_change(관찰 변화): label density(라벨 밀도)는 여전히 충분하지만, validation/OOS paired KPI(검증/표본외 쌍 KPI)가 scout clue(탐색 단서)를 만들지 못하면 target/stop structure(익절/손절 구조)나 session/risk segmentation(세션/위험 분할)이 다음 수리 대상이다.",
        "",
        "Boundary(경계): proxy repair only(프록시 수리 전용). MT5 Runtime Probe(MT5 런타임 탐침)는 아직 실행하지 않았고 권위 주장도 없다.",
    ]


def gate_audit_lines(created_at: str, summary: Mapping[str, Any], next_reason: str) -> list[str]:
    return [
        "# F74C Required Gate Coverage Audit(F74C 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        "| repair novelty(수리 신규성) | `pass(통과)` | label/target changed(라벨/목표 변경): clean_fast_touch, clean_value_q60, net_edge_q70. |",
        "| proxy KPI measurement(프록시 KPI 측정) | `pass(통과)` | candidates(후보) recorded(기록됨). |",
        f"| next action routing(다음 행동 배치) | `{next_reason}` | pre-MT5 only if scout clue exists(탐색 단서가 있을 때만 MT5 전 검토). |",
        "| final claim guard(최종 주장 보호) | `pass(통과)` | no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). |",
    ]


def update_ledgers(created_at: str, summary: Mapping[str, Any], best: Mapping[str, Any], next_run: str, judgment: str) -> None:
    report = REVIEWS_ROOT / "frontier74C_microburst_label_feature_repair_proxy_report.md"
    manifest = RUN_ROOT / "run_manifest.json"
    audit = REVIEWS_ROOT / "required_gate_coverage_audit_f74c.md"
    row = {
        "ledger_row_id": f"{RUN_ID}__proxy_repair",
        "row_id": f"{RUN_ID}__proxy_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "clean_value_label_repair(깨끗한 가치 라벨 수리)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "view": "proxy_repair(프록시 수리)",
        "tier": "Tier A separate(티어 A 분리)",
        "kpi_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "metric_scope": "proxy_repair(프록시 수리)",
        "scoreboard_lane": "trade_shape(거래 형태)",
        "lane": "proxy_repair(프록시 수리)",
        "family": "experiment_execution(실험 실행)",
        "status": STATUS,
        "result_status": STATUS,
        "judgment": judgment,
        "result_judgment": judgment,
        "path": rel(report),
        "report_path": rel(report),
        "primary_report": rel(report),
        "primary_artifact": rel(manifest),
        "output_path": rel(manifest),
        "result_path": rel(report),
        "primary_kpi": f"candidates={summary['candidate_count']};scout={summary['scout_clue_count']};meaningful={summary['meaningful_candidate_count']}",
        "guardrail_kpi": f"final_like={summary['final_like_reference_only_count']};failures={summary['failure_count']}",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(MT5는 다음 검증 범위)",
        "notes": "F74C clean/value label repair proxy; no authority(F74C 깨끗한/가치 라벨 수리 프록시, 권위 없음).",
        "run_number": "frontier74C",
        "date": created_at[:10],
        "run_date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "next_action": next_run,
        "rows": summary["candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_rows": summary["candidate_count"],
        "positive_proxy_rows": summary["scout_clue_count"],
        "best_model_id": best.get("candidate_id", ""),
        "best_proxy_net": best.get("oos_net_profit", ""),
        "net_profit": best.get("oos_net_profit", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_max_drawdown_percent", ""),
        "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trade_density": best.get("oos_trades_day", ""),
        "expectancy": best.get("oos_expectancy", ""),
        "recovery_factor": best.get("oos_recovery_factor", ""),
        "feature_count": best.get("feature_count", ""),
        "candidate_model_id": best.get("candidate_id", ""),
        "created_at_utc": created_at,
        "required_gate_audit": rel(audit),
        "gate_audit_path": rel(audit),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_proxy_repair(전선 프록시 수리)",
        "run_type": "clean_value_microburst_label_repair(깨끗한 가치 마이크로버스트 라벨 수리)",
        "input_run_id": PARENT_RUN_ID,
        "question": "Can clean/value labels repair F74B proxy failure?(깨끗한/가치 라벨이 F74B 프록시 실패를 수리할 수 있나?)",
        "evidence_boundary": "proxy_repair_only_no_runtime(프록시 수리 전용, 런타임 없음)",
    }
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers(judgment: str, summary: Mapping[str, Any], best: Mapping[str, Any], next_run: str) -> None:
    marker = "<!-- frontier74C_clean_value_label_repair_proxy_v1 -->"
    best_text = "none(없음)"
    if best:
        best_text = (
            f"{best.get('candidate_id')} validation/OOS PF/DD/tpd(검증/표본외 수익 팩터/손실폭/일거래) "
            f"{best.get('validation_profit_factor')}/{best.get('oos_profit_factor')}/"
            f"{best.get('validation_max_drawdown_percent')}/{best.get('oos_max_drawdown_percent')}/"
            f"{best.get('validation_trades_day')}/{best.get('oos_trades_day')}"
        )
    block = f"""<!-- frontier74C_clean_value_label_repair_proxy_v1 -->
- `{RUN_ID}` executed clean/value microburst label repair proxy(깨끗한/가치 마이크로버스트 라벨 수리 프록시). Result(결과): `{judgment}`. Candidates(후보) `{summary['candidate_count']}`, scout clues(탐색 단서) `{summary['scout_clue_count']}`, meaningful candidates(의미 후보) `{summary['meaningful_candidate_count']}`. Best(최선): {best_text}. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state(created_at: str, judgment: str, next_run: str) -> None:
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {next_run}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {judgment}",
        f"next_run_id: {next_run}",
        "runtime_probe_status: f74_proxy_repair_completed_runtime_probe_pending_if_signal",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f73_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F74C clean/value label repair proxy(깨끗한/가치 라벨 수리 프록시)를 실행했다."',
        '  - "Effect(효과): F74B의 조밀하지만 약한 선도달 라벨을 품질/가치 라벨로 재구성했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    write_text(WORKSPACE_STATE, "\n".join(lines))
    write_md(
        SELECTED_ROOT / "selection_status.md",
        [
            "# F74 Selection Status(F74 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{next_run}`",
            f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
            f"- status(상태): `{STATUS}`",
            f"- judgment(판정): `{judgment}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            f"- next_action(다음 행동): `{next_run}`",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`",
        ],
    )
    write_md(
        CURRENT_WORKING_STATE,
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {created_at}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            f"Current run(현재 실행): `{next_run}`",
            f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F74C clean/value label repair proxy(깨끗한/가치 라벨 수리 프록시)를 실행했다.",
            "",
            f"Effect(효과): 다음 실행을 `{next_run}`로 설정했다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F74C required material missing: {missing}")
    created_at = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    result = run_repair()
    candidates = result["candidate_rows"]
    ranked = result["ranked_rows"]
    best = result["best"]
    meaningful_count = sum(1 for row in candidates if row.get("meaningful_candidate"))
    scout_count = sum(1 for row in candidates if row.get("scout_clue"))
    final_like_count = sum(1 for row in candidates if row.get("final_like_reference_only"))
    judgment = (
        "proxy_repair_meaningful_candidate_pre_mt5_required_no_authority"
        if meaningful_count
        else ("proxy_repair_scout_clue_pre_mt5_required_no_authority" if scout_count else "proxy_repair_no_scout_clue_risk_session_decision_required_no_authority")
    )
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": judgment,
        "candidate_count": len(candidates),
        "failure_count": len(result["failure_rows"]),
        "scout_clue_count": scout_count,
        "meaningful_candidate_count": meaningful_count,
        "final_like_reference_only_count": final_like_count,
        "best_candidate": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    next_run, next_reason = next_action(summary)
    summary["next_run_id"] = next_run
    summary["next_reason"] = next_reason

    write_csv(RUN_ROOT / "f74c_label_density_table.csv", result["density_rows"])
    write_csv(RUN_ROOT / "f74c_candidate_results.csv", candidates)
    write_csv(RUN_ROOT / "f74c_candidate_results_ranked_top50.csv", ranked[:50])
    write_csv(RUN_ROOT / "f74c_failure_rows.csv", result["failure_rows"] or [{"reason": "none"}])
    write_csv(RUN_ROOT / "f74c_selected_trades_top_candidate.csv", result["selected_rows"] or [{"empty": "true"}])
    write_json(RUN_ROOT / "f74c_summary.json", summary)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": next_run,
            "status": STATUS,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "external_verification_status": "out_of_scope_by_claim_proxy_only(MT5는 다음 검증 범위)",
        },
    )
    write_csv(REVIEWS_ROOT / "f74c_label_density_table.csv", result["density_rows"])
    write_csv(REVIEWS_ROOT / "f74c_candidate_results_ranked_top50.csv", ranked[:50])
    write_csv(REVIEWS_ROOT / "f74c_split_summary_best_candidate.csv", base.split_summary_rows(candidates, best))
    write_json(REVIEWS_ROOT / "f74c_summary.json", summary)
    write_md(REVIEWS_ROOT / "frontier74C_microburst_label_feature_repair_proxy_report.md", report_lines(created_at, summary, best, next_run))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f74c.md", gate_audit_lines(created_at, summary, next_reason))

    update_ledgers(created_at, summary, best, next_run, judgment)
    update_registers(judgment, summary, best, next_run)
    update_state(created_at, judgment, next_run)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
