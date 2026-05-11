from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    ledger_pairs,
    upsert_csv_rows,
)
from foundation.mt5.runtime_artifacts import write_json
from stage_pipelines.stage10 import logreg_mt5_scout
from stage_pipelines.stage56 import dense_tier_a_engine_grid as grid


STAGE_ID = grid.STAGE_ID
RUN_NUMBER = "run50C"
PARENT_RUN_ID = "run50C_logreg_bracket_micro_grid_v1"
PACKET_ID = "stage56_run50C_logreg_bracket_micro_grid_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__LogRegBracketMicroGrid"
STAGE_ROOT = grid.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run50C_logreg_bracket_micro_grid.md"
RESULTS_CSV_PATH = STAGE_ROOT / "03_reviews" / "run50C_logreg_bracket_micro_grid_summary.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")


BRACKET_VARIANTS: tuple[grid.DenseVariant, ...] = (
    grid.DenseVariant("d35h07", 0.35, 0.35, 0.0, 7),
    grid.DenseVariant("d36h08", 0.36, 0.36, 0.0, 8),
    grid.DenseVariant("d37h09", 0.37, 0.37, 0.0, 9),
    grid.DenseVariant("d38h10", 0.38, 0.38, 0.0, 10),
    grid.DenseVariant("d39h11", 0.39, 0.39, 0.0, 11),
)

SUMMARY_COLUMNS = (
    "variant_id",
    "run_id",
    "external_verification_status",
    "threshold_id",
    "max_hold_bars",
    "tier_a_validation_closed_trades",
    "tier_a_validation_trades_per_day",
    "tier_a_validation_net_profit",
    "tier_a_validation_profit_factor",
    "tier_a_oos_closed_trades",
    "tier_a_oos_trades_per_day",
    "tier_a_oos_net_profit",
    "tier_a_oos_profit_factor",
    "tier_b_validation_closed_trades",
    "tier_b_validation_net_profit",
    "tier_b_validation_profit_factor",
    "tier_b_oos_closed_trades",
    "tier_b_oos_net_profit",
    "tier_b_oos_profit_factor",
    "routed_validation_closed_trades",
    "routed_validation_trades_per_day",
    "routed_validation_net_profit",
    "routed_validation_profit_factor",
    "routed_validation_b_fallback_bars",
    "routed_oos_closed_trades",
    "routed_oos_trades_per_day",
    "routed_oos_net_profit",
    "routed_oos_profit_factor",
    "routed_oos_b_fallback_bars",
    "routed_oos_max_drawdown",
    "judgment",
    "summary_path",
)


def _configure_grid_globals() -> None:
    grid.RUN_NUMBER = RUN_NUMBER
    grid.PARENT_RUN_ID = PARENT_RUN_ID
    grid.PACKET_ID = PACKET_ID
    grid.EXPLORATION_LABEL = EXPLORATION_LABEL
    grid.RUN_ROOT = RUN_ROOT
    grid.REPORT_PATH = REPORT_PATH
    grid.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    grid.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    grid.DEFAULT_VARIANTS = BRACKET_VARIANTS


def _float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _status_completed(summary: Mapping[str, Any], result: Mapping[str, Any]) -> bool:
    status = str(summary.get("external_verification_status") or result.get("external_verification_status") or "")
    return status == "completed"


def _routed_judgment(row: Mapping[str, Any]) -> str:
    validation_density = _float(row.get("routed_validation_trades_per_day"))
    oos_density = _float(row.get("routed_oos_trades_per_day"))
    validation_pf = _float(row.get("routed_validation_profit_factor"))
    oos_pf = _float(row.get("routed_oos_profit_factor"))
    validation_net = _float(row.get("routed_validation_net_profit"))
    oos_net = _float(row.get("routed_oos_net_profit"))
    if None in (validation_density, oos_density, validation_pf, oos_pf, validation_net, oos_net):
        return "blocked_or_unverified_no_mt5_routed_closed_trade_density"
    if validation_net <= 0.0 or oos_net <= 0.0:
        return "routed_quality_failed_runtime_probe_only"
    if validation_density >= 5.0 and oos_density >= 5.0 and validation_pf >= 1.10 and oos_pf >= 1.10:
        return "strong_routed_dense_engine_candidate_runtime_probe_only"
    if validation_density >= 3.0 and oos_density >= 3.0 and validation_pf >= 1.05 and oos_pf >= 1.05:
        return "weak_routed_dense_engine_candidate_runtime_probe_only"
    if validation_density <= 2.0 or oos_density <= 2.0:
        return "routed_density_target_failed_runtime_probe_only"
    return "routed_density_or_quality_inconclusive_runtime_probe_only"


def _summary_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        summary_path = Path(str(result.get("summary_path") or "")) if result.get("summary_path") else None
        summary = grid._read_json(summary_path) if summary_path and summary_path.exists() else {}
        variant_id = str(result.get("variant_id") or Path(str(result.get("run_output_root", ""))).name)
        run_id = str(result.get("run_id") or summary.get("run_id") or "")
        threshold = summary.get("selected_threshold", {}) if isinstance(summary, Mapping) else {}

        tier_a_validation_trades = grid._metric(summary, "mt5_tier_a_only_validation_is", "trade_count")
        tier_a_oos_trades = grid._metric(summary, "mt5_tier_a_only_oos", "trade_count")
        routed_validation_trades = grid._metric(summary, "mt5_routed_total_validation_is", "trade_count")
        routed_oos_trades = grid._metric(summary, "mt5_routed_total_oos", "trade_count")
        tier_a_validation_per_day = grid._per_day(tier_a_validation_trades, grid.VALIDATION_DAYS)
        tier_a_oos_per_day = grid._per_day(tier_a_oos_trades, grid.OOS_DAYS)
        routed_validation_per_day = grid._per_day(routed_validation_trades, grid.VALIDATION_DAYS)
        routed_oos_per_day = grid._per_day(routed_oos_trades, grid.OOS_DAYS)

        row = {
            "variant_id": variant_id,
            "run_id": run_id,
            "external_verification_status": summary.get("external_verification_status", result.get("external_verification_status", "")),
            "threshold_id": threshold.get("threshold_id", result.get("threshold_id", "")) if isinstance(threshold, Mapping) else "",
            "max_hold_bars": threshold.get("max_hold_bars", "") if isinstance(threshold, Mapping) else "",
            "tier_a_validation_closed_trades": tier_a_validation_trades,
            "tier_a_validation_trades_per_day": "" if tier_a_validation_per_day is None else f"{tier_a_validation_per_day:.6f}",
            "tier_a_validation_net_profit": grid._metric(summary, "mt5_tier_a_only_validation_is", "net_profit"),
            "tier_a_validation_profit_factor": grid._metric(summary, "mt5_tier_a_only_validation_is", "profit_factor"),
            "tier_a_oos_closed_trades": tier_a_oos_trades,
            "tier_a_oos_trades_per_day": "" if tier_a_oos_per_day is None else f"{tier_a_oos_per_day:.6f}",
            "tier_a_oos_net_profit": grid._metric(summary, "mt5_tier_a_only_oos", "net_profit"),
            "tier_a_oos_profit_factor": grid._metric(summary, "mt5_tier_a_only_oos", "profit_factor"),
            "tier_b_validation_closed_trades": grid._metric(summary, "mt5_tier_b_fallback_only_validation_is", "trade_count"),
            "tier_b_validation_net_profit": grid._metric(summary, "mt5_tier_b_fallback_only_validation_is", "net_profit"),
            "tier_b_validation_profit_factor": grid._metric(summary, "mt5_tier_b_fallback_only_validation_is", "profit_factor"),
            "tier_b_oos_closed_trades": grid._metric(summary, "mt5_tier_b_fallback_only_oos", "trade_count"),
            "tier_b_oos_net_profit": grid._metric(summary, "mt5_tier_b_fallback_only_oos", "net_profit"),
            "tier_b_oos_profit_factor": grid._metric(summary, "mt5_tier_b_fallback_only_oos", "profit_factor"),
            "routed_validation_closed_trades": routed_validation_trades,
            "routed_validation_trades_per_day": "" if routed_validation_per_day is None else f"{routed_validation_per_day:.6f}",
            "routed_validation_net_profit": grid._metric(summary, "mt5_routed_total_validation_is", "net_profit"),
            "routed_validation_profit_factor": grid._metric(summary, "mt5_routed_total_validation_is", "profit_factor"),
            "routed_validation_b_fallback_bars": grid._metric(summary, "mt5_routed_total_validation_is", "tier_b_fallback_used_count"),
            "routed_oos_closed_trades": routed_oos_trades,
            "routed_oos_trades_per_day": "" if routed_oos_per_day is None else f"{routed_oos_per_day:.6f}",
            "routed_oos_net_profit": grid._metric(summary, "mt5_routed_total_oos", "net_profit"),
            "routed_oos_profit_factor": grid._metric(summary, "mt5_routed_total_oos", "profit_factor"),
            "routed_oos_b_fallback_bars": grid._metric(summary, "mt5_routed_total_oos", "tier_b_fallback_used_count"),
            "routed_oos_max_drawdown": grid._metric(summary, "mt5_routed_total_oos", "max_drawdown_amount"),
            "summary_path": str(summary_path.as_posix()) if summary_path else "",
        }
        row["judgment"] = _routed_judgment(row) if _status_completed(summary, result) else "blocked_or_unverified_no_mt5_runtime_probe"
        rows.append(row)
    return rows


def _best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    verified = [row for row in rows if row.get("external_verification_status") == "completed"]
    if not verified:
        return None

    def judgment_rank(row: Mapping[str, Any]) -> float:
        judgment = str(row.get("judgment") or "")
        if judgment.startswith("strong_"):
            return 3.0
        if judgment.startswith("weak_"):
            return 2.0
        if "inconclusive" in judgment:
            return 1.0
        return 0.0

    def score(row: Mapping[str, Any]) -> tuple[float, float, float, float, float]:
        density = min(_float(row.get("routed_validation_trades_per_day")) or 0.0, _float(row.get("routed_oos_trades_per_day")) or 0.0)
        pf_floor = min(_float(row.get("routed_validation_profit_factor")) or 0.0, _float(row.get("routed_oos_profit_factor")) or 0.0)
        net = (_float(row.get("routed_validation_net_profit")) or 0.0) + (_float(row.get("routed_oos_net_profit")) or 0.0)
        fallback = (_float(row.get("routed_validation_b_fallback_bars")) or 0.0) + (_float(row.get("routed_oos_b_fallback_bars")) or 0.0)
        return (judgment_rank(row), pf_floor, density, net, fallback)

    return max(verified, key=score)


def _write_report(rows: Sequence[Mapping[str, Any]], *, attempt_mt5: bool, routed_fallback_enabled: bool) -> None:
    best = _best_row(rows)
    best_line = "`none`" if best is None else f"`{best.get('variant_id')}` / `{best.get('judgment')}`"
    lines = [
        "# Run50C LogReg Bracket Micro-Grid(50C 실행 로지스틱 회귀 구간 미세 격자)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`",
        "- model_family(모델군): `LogReg(로지스틱 회귀)` Stage07 full-context Tier A model(Stage07 전체 문맥 Tier A 모델) plus Tier B fallback model(Tier B 대체 모델)",
        f"- mt5_attempted(MT5 시도): `{bool(attempt_mt5)}`",
        f"- routed_fallback_enabled(라우팅 대체 활성): `{bool(routed_fallback_enabled)}`",
        f"- best_current_read(현재 최선 판독): {best_line}",
        "- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`",
        "",
        "## Design(설계)",
        "",
        "- hypothesis(가설): run50B(50B 실행)의 d34h06 density frontier(밀도 경계)와 d40h12 quality frontier(품질 경계) 사이에 실제 A+B routed total(A+B 라우팅 전체) 약한 기준선 후보가 있을 수 있다.",
        "- decision_use(결정 용도): selected_research_baseline(선택 연구 기준선), baseline_candidate_only(기준선 후보 전용), no_dense_engine_found(두꺼운 엔진 없음) 중 최종 판정으로 갈 수 있는지 좁힌다.",
        "- controls(통제): 같은 split(분할), 같은 Stage07 LogReg(로지스틱 회귀), 같은 Tier B partial-context(부분 문맥), 같은 MT5 EA(전문가 자문), 같은 US100 M5 계약을 쓴다.",
        "- changed_variables(변경 변수): short/long threshold(숏/롱 임계값)와 max_hold_bars(최대 보유 봉 수)만 바꾼다.",
        "",
        "## Results(결과)",
        "",
        "| variant(변형) | A val/day(A 검증/일) | A OOS/day(A 표본외/일) | routed val/day(라우팅 검증/일) | routed OOS/day(라우팅 표본외/일) | routed val PF(라우팅 검증 수익 팩터) | routed OOS PF(라우팅 표본외 수익 팩터) | B val bars(B 검증 봉) | B OOS bars(B 표본외 봉) | judgment(판정) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {avd} | {aod} | {rvd} | {rod} | {rvpf} | {ropf} | {bvb} | {bob} | `{judgment}` |".format(
                variant=row.get("variant_id", ""),
                avd=row.get("tier_a_validation_trades_per_day", ""),
                aod=row.get("tier_a_oos_trades_per_day", ""),
                rvd=row.get("routed_validation_trades_per_day", ""),
                rod=row.get("routed_oos_trades_per_day", ""),
                rvpf=row.get("routed_validation_profit_factor", ""),
                ropf=row.get("routed_oos_profit_factor", ""),
                bvb=row.get("routed_validation_b_fallback_bars", ""),
                bob=row.get("routed_oos_b_fallback_bars", ""),
                judgment=row.get("judgment", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Read(판독)",
            "",
            "- 이 실행은 actual routed total(실제 라우팅 전체)을 synthetic sum(합성 합산)으로 만들지 않고, MT5 strategy tester(전략 테스터) 단일 계좌 경로에서 읽는다.",
            "- Tier B fallback(Tier B 대체)은 라우팅에서 실제 사용된 봉 수를 따로 기록한다. 효과는 Tier B 단독 성과와 라우팅 기여를 섞지 않게 하는 것이다.",
            "- live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)는 주장하지 않는다.",
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8-sig")


def _parent_status(rows: Sequence[Mapping[str, Any]]) -> str:
    return "reviewed" if any(row.get("external_verification_status") == "completed" for row in rows) else "blocked"


def _parent_judgment(rows: Sequence[Mapping[str, Any]]) -> str:
    if _parent_status(rows) != "reviewed":
        return "blocked_no_completed_mt5_runtime_probe"
    if any(str(row.get("judgment", "")).startswith(("strong_", "weak_")) for row in rows):
        return "reviewed_completed_logreg_bracket_micro_grid_dense_candidate_runtime_probe_only"
    return "reviewed_completed_logreg_bracket_micro_grid_no_selected_baseline_runtime_probe_only"


def _write_parent_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = _best_row(rows)
    primary_kpi = ledger_pairs(
        (
            ("best_variant", None if best is None else best.get("variant_id")),
            ("routed_validation_trades_per_day", None if best is None else best.get("routed_validation_trades_per_day")),
            ("routed_oos_trades_per_day", None if best is None else best.get("routed_oos_trades_per_day")),
            ("routed_validation_pf", None if best is None else best.get("routed_validation_profit_factor")),
            ("routed_oos_pf", None if best is None else best.get("routed_oos_profit_factor")),
        )
    )
    guardrail_kpi = ledger_pairs(
        (
            ("selected_research_baseline", "none"),
            ("live_readiness", "none"),
            ("runtime_authority", "none"),
            ("operating_promotion", "none"),
            ("operating_reference", "none"),
            ("actual_routed_not_synthetic", True),
        )
    )
    parent_row = {
        "ledger_row_id": f"{PARENT_RUN_ID}__stage56_bracket_micro_grid_parent",
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "subrun_id": "stage56_bracket_micro_grid_parent",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "run50C_bracket_micro_grid_parent",
        "tier_scope": "Tier A primary plus Tier B fallback",
        "kpi_scope": "stage56_logreg_bracket_micro_grid",
        "scoreboard_lane": "runtime_probe",
        "status": _parent_status(rows),
        "judgment": _parent_judgment(rows),
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": primary_kpi,
        "guardrail_kpi": guardrail_kpi,
        "external_verification_status": "completed" if _parent_status(rows) == "reviewed" else "blocked",
        "notes": "Run50C bracket micro-grid completed with actual MT5 closed-trade evidence; no operating claim.",
    }
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage56_logreg_bracket_micro_grid",
                "status": _parent_status(rows),
                "judgment": _parent_judgment(rows),
                "path": REPORT_PATH.as_posix(),
                "notes": ledger_pairs(
                    (
                        ("variant_count", len(rows)),
                        ("best_variant", None if best is None else best.get("variant_id")),
                        ("best_judgment", None if best is None else best.get("judgment")),
                        ("boundary", "research_baseline_selection_only_no_operating_claim"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    return {
        "stage_ledger_payload": stage_payload,
        "project_ledger_payload": project_payload,
        "run_registry_payload": registry_payload,
    }


def _write_aggregate_summary(results: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]], parent_payload: Mapping[str, Any]) -> None:
    best = _best_row(rows)
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "reviewed_runtime_probe_completed" if best is not None else "blocked_or_payload_only",
        "judgment": _parent_judgment(rows),
        "best_variant": None if best is None else dict(best),
        "variant_rows": [dict(row) for row in rows],
        "variant_payloads": [dict(result) for result in results],
        "artifacts": {
            "report_path": REPORT_PATH.as_posix(),
            "results_csv_path": RESULTS_CSV_PATH.as_posix(),
            "parent_payload": dict(parent_payload),
        },
        "boundary": "research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference",
    }
    write_json(AGGREGATE_SUMMARY_PATH, payload)


def _select_variants(selected_ids: Iterable[str] | None, max_variants: int | None) -> tuple[grid.DenseVariant, ...]:
    selected = list(BRACKET_VARIANTS)
    if selected_ids:
        wanted = set(selected_ids)
        selected = [variant for variant in selected if variant.variant_id in wanted]
        missing = sorted(wanted.difference(variant.variant_id for variant in selected))
        if missing:
            raise ValueError(f"Unknown variant ids: {missing}")
    if max_variants is not None:
        selected = selected[: int(max_variants)]
    if not selected:
        raise ValueError("At least one variant is required.")
    return tuple(selected)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Stage56 run50C LogReg bracket micro-grid.")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--routed-fallback", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--common-files-root", default=str(logreg_mt5_scout.DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(logreg_mt5_scout.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(logreg_mt5_scout.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _configure_grid_globals()
    args = parse_args(argv)
    variants = _select_variants(args.variant_id, args.max_variants)
    results: list[dict[str, Any]] = []
    for variant in variants:
        result = grid._run_variant(
            variant,
            attempt_mt5=bool(args.attempt_mt5),
            routed_fallback_enabled=bool(args.routed_fallback),
            common_files_root=Path(args.common_files_root),
            terminal_data_root=Path(args.terminal_data_root),
            tester_profile_root=Path(args.tester_profile_root),
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            force=bool(args.force),
        )
        result["variant_id"] = variant.variant_id
        result["variant_spec"] = {
            "short_threshold": variant.short_threshold,
            "long_threshold": variant.long_threshold,
            "min_margin": variant.min_margin,
            "max_hold_bars": variant.max_hold_bars,
        }
        results.append(result)

    rows = _summary_rows(results)
    grid._write_csv(RESULTS_CSV_PATH, rows, SUMMARY_COLUMNS)
    _write_report(rows, attempt_mt5=bool(args.attempt_mt5), routed_fallback_enabled=bool(args.routed_fallback))
    parent_payload = _write_parent_rows(rows)
    _write_aggregate_summary(results, rows, parent_payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "rows": rows,
                "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
