from __future__ import annotations

import argparse
import csv
import json
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import json_ready  # noqa: E402
from foundation.control_plane.mt5_trade_attribution import MarketData  # noqa: E402
from stage_pipelines.stage56 import deep_repair_suite as deep  # noqa: E402
from stage_pipelines.stage56 import reopen_optimization_batch as reopen  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50F"
PARENT_RUN_ID = "run50F_stage56_cooldown_b_tight_repair_v1"
PACKET_ID = "stage56_run50F_cooldown_b_tight_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__CooldownBTightRepair"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
REPORT_PATH = REVIEWS_ROOT / "run50F_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50F_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50F_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")


@dataclass(frozen=True)
class CooldownVariant:
    variant_id: str
    group: str
    tier_a_short_threshold: float
    tier_a_long_threshold: float
    tier_a_min_margin: float
    tier_b_short_threshold: float
    tier_b_long_threshold: float
    tier_b_min_margin: float
    max_hold_bars: int
    reentry_cooldown_bars: int
    routed_fallback_enabled: bool = True
    session_slice_id: str | None = None
    tier_b_allowed_subtypes: tuple[str, ...] = ()
    notes: str = ""
    side_filter_id: str | None = None
    side_filter_enabled: bool = False
    tier_a_side_filter_feature_index: int = -1
    tier_b_side_filter_feature_index: int = -1
    block_short_feature_range: bool = False
    block_short_feature_min: float = 0.0
    block_short_feature_max: float = 0.0
    block_long_feature_range: bool = False
    block_long_feature_min: float = 0.0
    block_long_feature_max: float = 0.0

    @property
    def base_id(self) -> str:
        text = self.variant_id
        for marker in ("_c0", "_c1", "_c2", "_c3"):
            if marker in text:
                return text.split(marker, 1)[0]
        return text

    def to_deep_variant(self) -> deep.RepairVariant:
        return deep.RepairVariant(
            self.variant_id,
            self.group,
            self.tier_a_short_threshold,
            self.tier_a_long_threshold,
            self.tier_a_min_margin,
            self.tier_b_short_threshold,
            self.tier_b_long_threshold,
            self.tier_b_min_margin,
            self.max_hold_bars,
            session_slice_id=self.session_slice_id,
            tier_b_allowed_subtypes=self.tier_b_allowed_subtypes,
            notes=self.notes,
            side_filter_id=self.side_filter_id,
            side_filter_enabled=self.side_filter_enabled,
            tier_a_side_filter_feature_index=self.tier_a_side_filter_feature_index,
            tier_b_side_filter_feature_index=self.tier_b_side_filter_feature_index,
            block_short_feature_range=self.block_short_feature_range,
            block_short_feature_min=self.block_short_feature_min,
            block_short_feature_max=self.block_short_feature_max,
            block_long_feature_range=self.block_long_feature_range,
            block_long_feature_min=self.block_long_feature_min,
            block_long_feature_max=self.block_long_feature_max,
        )


DEFAULT_VARIANTS: tuple[CooldownVariant, ...] = (
    CooldownVariant("d330h06_b042_c1", "cooldown_b_tight", 0.330, 0.330, 0.0, 0.420, 0.420, 0.0, 6, 1, notes="lower A threshold with B042 and one-bar reentry cooldown"),
    CooldownVariant("d320h06_b042_c1", "cooldown_b_tight", 0.320, 0.320, 0.0, 0.420, 0.420, 0.0, 6, 1, notes="extra density pressure with B042 and one-bar cooldown"),
    CooldownVariant("d330h06_b045_c1", "cooldown_b_tight", 0.330, 0.330, 0.0, 0.450, 0.450, 0.0, 6, 1, notes="lower A threshold with stricter B045 and one-bar cooldown"),
    CooldownVariant("d320h06_b045_c1", "cooldown_b_tight", 0.320, 0.320, 0.0, 0.450, 0.450, 0.0, 6, 1, notes="extra density pressure with stricter B045 and one-bar cooldown"),
    CooldownVariant("d315h06_b045_c2", "cooldown_density_pressure", 0.315, 0.315, 0.0, 0.450, 0.450, 0.0, 6, 2, notes="two-bar cooldown survival pressure"),
    CooldownVariant("d305h06_b045_c2", "cooldown_density_pressure", 0.305, 0.305, 0.0, 0.450, 0.450, 0.0, 6, 2, notes="lower threshold to test whether cooldown density can recover"),
)


def _configure_globals() -> None:
    for module in (deep, reopen):
        module.RUN_NUMBER = RUN_NUMBER
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.PACKET_ID = PACKET_ID
        module.EXPLORATION_LABEL = EXPLORATION_LABEL
        module.RUN_ROOT = RUN_ROOT
        module.REPORT_PATH = REPORT_PATH
        module.RESULTS_CSV_PATH = RESULTS_CSV_PATH
        module.AUDIT_CSV_PATH = AUDIT_CSV_PATH
        module.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
        module.STAGE_RUN_LEDGER_PATH = STAGE_RUN_LEDGER_PATH
        module.PROJECT_ALPHA_LEDGER_PATH = PROJECT_ALPHA_LEDGER_PATH
        module.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    target = reopen._project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    target = reopen._project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _select_variants(
    *,
    selected_ids: Iterable[str] | None,
    selected_groups: Iterable[str] | None,
    max_variants: int | None,
) -> tuple[CooldownVariant, ...]:
    selected = list(DEFAULT_VARIANTS)
    if selected_groups:
        wanted_groups = {group.strip() for group in selected_groups if group.strip()}
        selected = [variant for variant in selected if variant.group in wanted_groups]
    if selected_ids:
        wanted = {variant_id.strip() for variant_id in selected_ids if variant_id.strip()}
        selected = [variant for variant in selected if variant.variant_id in wanted]
        missing = sorted(wanted.difference(variant.variant_id for variant in selected))
        if missing:
            raise ValueError(f"Unknown variant ids: {missing}")
    if max_variants is not None:
        selected = selected[: int(max_variants)]
    if not selected:
        raise ValueError("At least one variant is required.")
    return tuple(selected)


def _split_values(values: Sequence[str]) -> tuple[str, ...]:
    parts: list[str] = []
    for value in values:
        parts.extend(part.strip() for part in str(value).split(",") if part.strip())
    return tuple(parts)


def _run_variant(
    variant: CooldownVariant,
    *,
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    force: bool,
) -> dict[str, Any]:
    deep_variant = variant.to_deep_variant()
    result = deep._run_variant(
        deep_variant,
        attempt_mt5=attempt_mt5,
        routed_fallback_enabled=variant.routed_fallback_enabled,
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
        terminal_path=terminal_path,
        metaeditor_path=metaeditor_path,
        force=force,
        reentry_cooldown_bars=variant.reentry_cooldown_bars,
    )
    result["variant_id"] = variant.variant_id
    result["variant_spec"] = {
        "group": variant.group,
        "base_id": variant.base_id,
        "routed_fallback_enabled": variant.routed_fallback_enabled,
        "reentry_cooldown_bars": variant.reentry_cooldown_bars,
        "tier_a_short_threshold": variant.tier_a_short_threshold,
        "tier_a_long_threshold": variant.tier_a_long_threshold,
        "tier_a_min_margin": variant.tier_a_min_margin,
        "tier_b_short_threshold": variant.tier_b_short_threshold,
        "tier_b_long_threshold": variant.tier_b_long_threshold,
        "tier_b_min_margin": variant.tier_b_min_margin,
        "max_hold_bars": variant.max_hold_bars,
        "side_filter_id": variant.side_filter_id,
        "side_filter_enabled": variant.side_filter_enabled,
        "tier_a_side_filter_feature_index": variant.tier_a_side_filter_feature_index,
        "tier_b_side_filter_feature_index": variant.tier_b_side_filter_feature_index,
        "block_short_feature_range": variant.block_short_feature_range,
        "block_short_feature_min": variant.block_short_feature_min,
        "block_short_feature_max": variant.block_short_feature_max,
        "block_long_feature_range": variant.block_long_feature_range,
        "block_long_feature_min": variant.block_long_feature_min,
        "block_long_feature_max": variant.block_long_feature_max,
    }
    return result


def _augment_rows(rows: list[dict[str, Any]], variants: Sequence[CooldownVariant]) -> None:
    reopen._augment_rows(rows, variants)
    by_id = {variant.variant_id: variant for variant in variants}
    for row in rows:
        variant = by_id.get(str(row.get("variant_id") or ""))
        row["reentry_cooldown_bars"] = "" if variant is None else variant.reentry_cooldown_bars
        row["side_filter_id"] = "" if variant is None or variant.side_filter_id is None else variant.side_filter_id
        row["side_filter_enabled"] = "" if variant is None else variant.side_filter_enabled
        row["tier_a_side_filter_feature_index"] = "" if variant is None else variant.tier_a_side_filter_feature_index
        row["tier_b_side_filter_feature_index"] = "" if variant is None else variant.tier_b_side_filter_feature_index


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 cooldown-aware MT5 repair batch.")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true", default=True)
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--groups", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(deep.logreg_scout.DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(deep.logreg_scout.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(deep.logreg_scout.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _configure_globals()
    args = parse_args(argv)
    variants = _select_variants(
        selected_ids=_split_values(args.variant_id),
        selected_groups=_split_values(args.groups),
        max_variants=args.max_variants,
    )
    deep_variants = tuple(variant.to_deep_variant() for variant in variants)
    results: list[dict[str, Any]] = []
    for variant in variants:
        try:
            result = _run_variant(
                variant,
                attempt_mt5=bool(args.attempt_mt5),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
                force=bool(args.force),
            )
        except Exception as exc:  # pragma: no cover - long MT5 batches must keep evidence.
            error_path = RUN_ROOT / variant.variant_id / "error.json"
            _write_json(
                error_path,
                {
                    "variant_id": variant.variant_id,
                    "run_id": variant.to_deep_variant().run_id,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                    "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                },
            )
            result = {
                "status": "error",
                "variant_id": variant.variant_id,
                "run_id": variant.to_deep_variant().run_id,
                "external_verification_status": "blocked",
                "error": str(exc),
                "error_path": error_path.as_posix(),
            }
            if not args.continue_on_error:
                results.append(result)
                break
        results.append(dict(result))

    rows = deep._summary_rows(results, deep_variants)
    _augment_rows(rows, variants)
    market_data = MarketData.load(REPO_ROOT)
    reference_audits, reference_capture = reopen._reference_capture_by_split(
        market_data,
        float(args.cost_stress_per_trade),
    )
    audit_rows = reference_audits + reopen._audit_rows(
        rows,
        market_data=market_data,
        cost_stress_per_trade=float(args.cost_stress_per_trade),
        reference_capture=reference_capture,
    )
    final_read = reopen._selected_read(rows, audit_rows)
    _write_csv(RESULTS_CSV_PATH, rows, SUMMARY_COLUMNS)
    _write_csv(AUDIT_CSV_PATH, audit_rows, reopen.AUDIT_COLUMNS)
    reopen._write_report(rows, audit_rows, final_read, attempt_mt5=bool(args.attempt_mt5))
    reopen._write_progress_log(rows, audit_rows, final_read)
    ledger_payload = reopen._write_parent_rows(rows, final_read)
    reopen._write_aggregate_summary(results, rows, audit_rows, final_read, ledger_payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": PARENT_RUN_ID,
                "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
                "final_read": final_read.get("stage56_judgment"),
                "stage56_remains_open": bool(final_read.get("stage56_remains_open")),
                "results_csv_path": RESULTS_CSV_PATH.as_posix(),
                "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
                "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


SUMMARY_COLUMNS = tuple(
    list(reopen.SUMMARY_COLUMNS[:-4])
    + [
        "reentry_cooldown_bars",
        "side_filter_id",
        "side_filter_enabled",
        "tier_a_side_filter_feature_index",
        "tier_b_side_filter_feature_index",
    ]
    + list(reopen.SUMMARY_COLUMNS[-4:])
)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
