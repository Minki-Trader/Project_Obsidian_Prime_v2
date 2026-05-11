from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.alpha import scout_runner as alpha_scout_runner  # noqa: E402
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, ledger_pairs, upsert_csv_rows  # noqa: E402
from foundation.mt5.runtime_artifacts import write_json  # noqa: E402
from stage_pipelines.stage10 import logreg_mt5_scout as logreg_scout  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE_NUMBER = 56
RUN_NUMBER = "run50B"
PARENT_RUN_ID = "run50B_tier_a_dense_engine_grid_v1"
PACKET_ID = "stage56_run50B_tier_a_dense_engine_grid_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__TierADenseLogRegGrid"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run50B_tier_a_dense_engine_grid.md"
RESULTS_CSV_PATH = STAGE_ROOT / "03_reviews" / "run50B_tier_a_dense_engine_grid_summary.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0


@dataclass(frozen=True)
class DenseVariant:
    variant_id: str
    short_threshold: float
    long_threshold: float
    min_margin: float
    max_hold_bars: int

    @property
    def run_id(self) -> str:
        return f"{RUN_NUMBER}_{self.variant_id}_logreg_dense_v1"

    @property
    def threshold_id(self) -> str:
        margin_bp = int(round(self.min_margin * 1000))
        return (
            f"stage56_{self.variant_id}_"
            f"s{self.short_threshold:.2f}_l{self.long_threshold:.2f}_m{margin_bp:03d}"
        )


DEFAULT_VARIANTS: tuple[DenseVariant, ...] = (
    DenseVariant("d34h06", 0.34, 0.34, 0.0, 6),
    DenseVariant("d36h06", 0.36, 0.36, 0.0, 6),
    DenseVariant("d38h09", 0.38, 0.38, 0.0, 9),
    DenseVariant("d40h12", 0.40, 0.40, 0.0, 12),
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _configure_stage56_identity(variant: DenseVariant, run_output_root: Path) -> None:
    common_run_root = f"Project_Obsidian_Prime_v2/stage56/{PARENT_RUN_ID}/{variant.variant_id}"
    logreg_scout.STAGE_ID = STAGE_ID
    logreg_scout.RUN_NUMBER = RUN_NUMBER
    logreg_scout.RUN_ID = variant.run_id
    logreg_scout.EXPLORATION_LABEL = f"{EXPLORATION_LABEL}__{variant.variant_id}"
    logreg_scout.DEFAULT_RUN_OUTPUT_ROOT = run_output_root
    logreg_scout.STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    logreg_scout.COMMON_RUN_ROOT = common_run_root
    alpha_scout_runner.configure_run_identity(
        run_number=RUN_NUMBER,
        run_id=variant.run_id,
        exploration_label=logreg_scout.EXPLORATION_LABEL,
        common_run_root=common_run_root,
        stage_id=STAGE_ID,
    )

    def build_stage56_context(
        *,
        run_output_root: Path,
        common_files_root: Path,
        terminal_data_root: Path,
        tester_profile_root: Path,
    ) -> alpha_scout_runner.ScoutRunContext:
        return alpha_scout_runner.build_run_context(
            stage_id=STAGE_ID,
            stage_number=STAGE_NUMBER,
            run_number=RUN_NUMBER,
            run_id=variant.run_id,
            exploration_label=logreg_scout.EXPLORATION_LABEL,
            output_root=run_output_root,
            common_run_root=common_run_root,
            common_files_root=common_files_root,
            terminal_data_root=terminal_data_root,
            tester_profile_root=tester_profile_root,
        )

    logreg_scout.build_scout_context = build_stage56_context


def _run_variant(
    variant: DenseVariant,
    *,
    attempt_mt5: bool,
    routed_fallback_enabled: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    force: bool,
) -> dict[str, Any]:
    run_output_root = RUN_ROOT / variant.variant_id
    summary_path = run_output_root / "summary.json"
    if summary_path.exists() and not force:
        return {
            "status": "skipped_existing",
            "variant_id": variant.variant_id,
            "run_id": variant.run_id,
            "summary_path": summary_path.as_posix(),
        }

    _configure_stage56_identity(variant, run_output_root)
    rule = logreg_scout.threshold_rule_from_values(
        threshold_id=variant.threshold_id,
        short_threshold=variant.short_threshold,
        long_threshold=variant.long_threshold,
        min_margin=variant.min_margin,
    )
    return logreg_scout.run_stage10_logreg_mt5_scout(
        model_input_path=logreg_scout.DEFAULT_MODEL_INPUT_PATH,
        feature_order_path=logreg_scout.DEFAULT_FEATURE_ORDER_PATH,
        tier_b_model_input_path=logreg_scout.DEFAULT_TIER_B_MODEL_INPUT_PATH,
        tier_b_feature_order_path=logreg_scout.DEFAULT_TIER_B_FEATURE_ORDER_PATH,
        raw_root=logreg_scout.DEFAULT_RAW_ROOT,
        training_summary_path=logreg_scout.DEFAULT_TRAINING_SUMMARY_PATH,
        stage07_model_path=logreg_scout.DEFAULT_STAGE07_MODEL_PATH,
        run_output_root=run_output_root,
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
        max_hold_bars=variant.max_hold_bars,
        tier_a_threshold_rule=rule,
        tier_b_threshold_rule=rule,
        routed_fallback_enabled=routed_fallback_enabled,
        attempt_mt5=attempt_mt5,
        terminal_path=terminal_path,
        metaeditor_path=metaeditor_path,
    )


def _record_by_view(summary: Mapping[str, Any], record_view: str) -> Mapping[str, Any]:
    for record in summary.get("mt5_kpi_records", []):
        if str(record.get("record_view")) == record_view:
            return record
    return {}


def _metric(summary: Mapping[str, Any], record_view: str, metric: str) -> Any:
    record = _record_by_view(summary, record_view)
    metrics = record.get("metrics", {}) if isinstance(record, Mapping) else {}
    return metrics.get(metric) if isinstance(metrics, Mapping) else None


def _per_day(trades: Any, days: float) -> float | None:
    if trades is None:
        return None
    try:
        return float(trades) / days
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def _judgment(validation_trades_per_day: float | None, oos_trades_per_day: float | None, validation_pf: Any, oos_pf: Any) -> str:
    if validation_trades_per_day is None or oos_trades_per_day is None:
        return "blocked_or_unverified_no_mt5_closed_trade_density"
    try:
        validation_pf_float = float(validation_pf)
        oos_pf_float = float(oos_pf)
    except (TypeError, ValueError):
        validation_pf_float = 0.0
        oos_pf_float = 0.0
    if validation_trades_per_day >= 5.0 and oos_trades_per_day >= 5.0 and validation_pf_float >= 1.10 and oos_pf_float >= 1.10:
        return "strong_dense_engine_candidate_runtime_probe_only"
    if validation_trades_per_day >= 3.0 and oos_trades_per_day >= 3.0 and validation_pf_float >= 1.05 and oos_pf_float >= 1.05:
        return "weak_dense_engine_candidate_runtime_probe_only"
    if validation_trades_per_day <= 2.0 or oos_trades_per_day <= 2.0:
        return "density_target_failed_runtime_probe_only"
    return "density_or_quality_inconclusive_runtime_probe_only"


def _summary_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        summary_path = Path(str(result.get("summary_path") or "")) if result.get("summary_path") else None
        summary = _read_json(summary_path) if summary_path and summary_path.exists() else {}
        variant_id = str(result.get("variant_id") or Path(str(result.get("run_output_root", ""))).name)
        run_id = str(result.get("run_id") or summary.get("run_id") or "")
        threshold = summary.get("selected_threshold", {}) if isinstance(summary, Mapping) else {}
        validation_trades = _metric(summary, "mt5_tier_a_only_validation_is", "trade_count")
        oos_trades = _metric(summary, "mt5_tier_a_only_oos", "trade_count")
        validation_per_day = _per_day(validation_trades, VALIDATION_DAYS)
        oos_per_day = _per_day(oos_trades, OOS_DAYS)
        validation_pf = _metric(summary, "mt5_tier_a_only_validation_is", "profit_factor")
        oos_pf = _metric(summary, "mt5_tier_a_only_oos", "profit_factor")
        row = {
            "variant_id": variant_id,
            "run_id": run_id,
            "external_verification_status": summary.get("external_verification_status", result.get("external_verification_status", "")),
            "threshold_id": threshold.get("threshold_id", result.get("threshold_id", "")) if isinstance(threshold, Mapping) else "",
            "max_hold_bars": threshold.get("max_hold_bars", "") if isinstance(threshold, Mapping) else "",
            "validation_closed_trades": validation_trades,
            "validation_trades_per_day": "" if validation_per_day is None else f"{validation_per_day:.6f}",
            "validation_net_profit": _metric(summary, "mt5_tier_a_only_validation_is", "net_profit"),
            "validation_profit_factor": validation_pf,
            "oos_closed_trades": oos_trades,
            "oos_trades_per_day": "" if oos_per_day is None else f"{oos_per_day:.6f}",
            "oos_net_profit": _metric(summary, "mt5_tier_a_only_oos", "net_profit"),
            "oos_profit_factor": oos_pf,
            "tier_b_validation_closed_trades": _metric(summary, "mt5_tier_b_fallback_only_validation_is", "trade_count"),
            "tier_b_oos_closed_trades": _metric(summary, "mt5_tier_b_fallback_only_oos", "trade_count"),
            "routed_validation_closed_trades": _metric(summary, "mt5_routed_total_validation_is", "trade_count"),
            "routed_oos_closed_trades": _metric(summary, "mt5_routed_total_oos", "trade_count"),
            "judgment": _judgment(validation_per_day, oos_per_day, validation_pf, oos_pf),
            "summary_path": str(summary_path.as_posix()) if summary_path else "",
        }
        rows.append(row)
    return rows


def _best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    verified = [row for row in rows if row.get("external_verification_status") == "completed"]
    if not verified:
        return None

    def score(row: Mapping[str, Any]) -> tuple[float, float, float]:
        try:
            density = min(float(row.get("validation_trades_per_day") or 0.0), float(row.get("oos_trades_per_day") or 0.0))
            pf_floor = min(float(row.get("validation_profit_factor") or 0.0), float(row.get("oos_profit_factor") or 0.0))
            net = float(row.get("validation_net_profit") or 0.0) + float(row.get("oos_net_profit") or 0.0)
        except (TypeError, ValueError):
            return (0.0, 0.0, 0.0)
        return (density, pf_floor, net)

    return max(verified, key=score)


def _write_report(rows: Sequence[Mapping[str, Any]], *, attempt_mt5: bool, routed_fallback_enabled: bool) -> None:
    best = _best_row(rows)
    candidate_line = "`none`"
    if best is not None:
        candidate_line = f"`{best.get('variant_id')}` / `{best.get('judgment')}`"
    lines = [
        "# Run50B Tier A Dense Engine Grid(50B 실행 Tier A 두꺼운 엔진 격자)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`",
        "- model_family(모델군): `LogReg(로지스틱 회귀)` Stage07 full-context Tier A model(Stage07 전체 문맥 Tier A 모델)",
        f"- mt5_attempted(MT5 시도): `{bool(attempt_mt5)}`",
        f"- routed_fallback_enabled(라우팅 대체 활성): `{bool(routed_fallback_enabled)}`",
        f"- best_current_read(현재 최선 판독): {candidate_line}",
        "- boundary(주장 경계): `runtime_probe_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`",
        "",
        "## Design(설계)",
        "",
        "- hypothesis(가설): Stage07 LogReg(로지스틱 회귀) Tier A 모델의 threshold(임계값)를 낮추면 MT5 closed trades(닫힌 거래) 밀도가 Stage56 최소 검토선에 접근할 수 있다.",
        "- decision_use(결정 용도): selected_research_baseline(선택 연구 기준선) 후보가 있는지 보기 위한 1차 격자다.",
        "- comparison_baseline(비교 기준): run50A 기존 근거 감사에서 가장 촘촘했던 QDA 후보와 Stage55 routed adapter(라우팅 어댑터) 후보.",
        "- controls(통제): 같은 데이터 분할, 같은 Stage07 Tier A 모델, 같은 MT5 EA(전문가 자문), 같은 US100 M5 계약을 쓴다.",
        "- changed_variables(변경 변수): Tier A short/long threshold(숏/롱 임계값)와 max_hold_bars(최대 보유 봉 수)만 바꾼다.",
        "",
        "## Results(결과)",
        "",
        "| variant(변형) | validation trades/day(검증 거래/일) | OOS trades/day(표본외 거래/일) | validation PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | judgment(판정) |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {vpd} | {opd} | {vpf} | {opf} | `{judgment}` |".format(
                variant=row.get("variant_id", ""),
                vpd=row.get("validation_trades_per_day", ""),
                opd=row.get("oos_trades_per_day", ""),
                vpf=row.get("validation_profit_factor", ""),
                opf=row.get("oos_profit_factor", ""),
                judgment=row.get("judgment", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "이 보고서는 research baseline selection(연구 기준선 선택) 안의 runtime probe(런타임 탐침)만 말한다.",
            "live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)는 주장하지 않는다.",
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8-sig")


def _write_parent_registry_row(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = _best_row(rows)
    status = "reviewed" if any(row.get("external_verification_status") == "completed" for row in rows) else "blocked"
    judgment = "reviewed_completed_tier_a_dense_engine_grid_runtime_probe_only" if status == "reviewed" else "blocked_no_completed_mt5_runtime_probe"
    notes = ledger_pairs(
        (
            ("variant_count", len(rows)),
            ("best_variant", None if best is None else best.get("variant_id")),
            ("best_judgment", None if best is None else best.get("judgment")),
            ("boundary", "research_baseline_selection_only_no_operating_claim"),
        )
    )
    return upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage56_dense_tier_a_engine_grid",
                "status": status,
                "judgment": judgment,
                "path": REPORT_PATH.as_posix(),
                "notes": notes,
            }
        ],
        key="run_id",
    )


def _write_aggregate_summary(results: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]], registry_payload: Mapping[str, Any]) -> None:
    best = _best_row(rows)
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "reviewed_runtime_probe_completed" if best is not None else "blocked_or_payload_only",
        "judgment": None if best is None else best.get("judgment"),
        "best_variant": None if best is None else dict(best),
        "variant_rows": [dict(row) for row in rows],
        "variant_payloads": [dict(result) for result in results],
        "artifacts": {
            "report_path": REPORT_PATH.as_posix(),
            "results_csv_path": RESULTS_CSV_PATH.as_posix(),
            "run_registry_payload": dict(registry_payload),
        },
        "boundary": "research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference",
    }
    write_json(AGGREGATE_SUMMARY_PATH, payload)


def _select_variants(selected_ids: Iterable[str] | None, max_variants: int | None) -> tuple[DenseVariant, ...]:
    selected = list(DEFAULT_VARIANTS)
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
    parser = argparse.ArgumentParser(description="Run the Stage56 Tier A dense LogReg MT5 grid.")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--routed-fallback", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--common-files-root", default=str(logreg_scout.DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(logreg_scout.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(logreg_scout.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    variants = _select_variants(args.variant_id, args.max_variants)
    results: list[dict[str, Any]] = []
    for variant in variants:
        result = _run_variant(
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
    _write_csv(
        RESULTS_CSV_PATH,
        rows,
        (
            "variant_id",
            "run_id",
            "external_verification_status",
            "threshold_id",
            "max_hold_bars",
            "validation_closed_trades",
            "validation_trades_per_day",
            "validation_net_profit",
            "validation_profit_factor",
            "oos_closed_trades",
            "oos_trades_per_day",
            "oos_net_profit",
            "oos_profit_factor",
            "tier_b_validation_closed_trades",
            "tier_b_oos_closed_trades",
            "routed_validation_closed_trades",
            "routed_oos_closed_trades",
            "judgment",
            "summary_path",
        ),
    )
    _write_report(rows, attempt_mt5=bool(args.attempt_mt5), routed_fallback_enabled=bool(args.routed_fallback))
    registry_payload = _write_parent_registry_row(rows)
    _write_aggregate_summary(results, rows, registry_payload)
    print(json.dumps({"status": "ok", "rows": rows, "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
