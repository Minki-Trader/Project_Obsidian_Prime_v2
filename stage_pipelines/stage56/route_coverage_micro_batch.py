from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
    parse_ini,
    parse_set,
)
from foundation.control_plane.mt5_trade_attribution import MarketData  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import deep_repair_suite as deep  # noqa: E402
from stage_pipelines.stage56 import reopen_optimization_batch as reopen  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE_NUMBER = 56
RUN_NUMBER = "run50AI"
PARENT_RUN_ID = "run50AI_stage56_route_coverage_micro_batch_v1"
PACKET_ID = "stage56_run50AI_route_coverage_micro_batch_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__RouteCoverageMicroBatch"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
REPORT_PATH = REVIEWS_ROOT / "run50AI_route_coverage_micro_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AI_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AI_audit.csv"
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
RUN50AH_SUMMARY_PATH = Path("docs/agent_control/packets/stage56_run50AH_s25_model_axis_oos_density_v1/aggregate_summary.json")
NF200S25B_SUMMARY_PATH = STAGE_ROOT / "02_runs/run50AH/nf200s25b/summary.json"
VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0


@dataclass(frozen=True)
class CoverageVariant:
    variant_id: str
    group: str
    source_run_id: str
    source_stage_id: str
    source_variant_id: str
    source_axis: str
    reentry_cooldown_bars: int
    notes: str

    @property
    def source_root(self) -> Path:
        return Path("stages") / self.source_stage_id / "02_runs" / self.source_run_id

    @property
    def run_id(self) -> str:
        return f"{RUN_NUMBER}_{self.variant_id}_route_coverage_v1"


DEFAULT_VARIANTS: tuple[CoverageVariant, ...] = (
    CoverageVariant(
        variant_id="qda_q85_aonly_bdisabled",
        group="independent_qda_coverage_source_tier_b_disabled",
        source_run_id="run09O_qda_reg015_q85_coverage_followup_v1",
        source_stage_id="16_model_family_challenge__qda_class_covariance_scout",
        source_variant_id="v25_reg015_q85",
        source_axis="stage16_qda_coverage_q85",
        reentry_cooldown_bars=0,
        notes="Broad reviewed QDA coverage source; Tier B disabled using run50AH damage evidence.",
    ),
    CoverageVariant(
        variant_id="qda_q93_quality_bdisabled",
        group="independent_qda_quality_source_tier_b_disabled",
        source_run_id="run09P_qda_reg015_q93_coverage_followup_v1",
        source_stage_id="16_model_family_challenge__qda_class_covariance_scout",
        source_variant_id="v26_reg015_q93",
        source_axis="stage16_qda_coverage_q93",
        reentry_cooldown_bars=0,
        notes="Quality-biased reviewed QDA source; Tier B disabled using run50AH damage evidence.",
    ),
    CoverageVariant(
        variant_id="qda_q85_guard12_bdisabled",
        group="independent_qda_coverage_source_same_move_guard",
        source_run_id="run09O_qda_reg015_q85_coverage_followup_v1",
        source_stage_id="16_model_family_challenge__qda_class_covariance_scout",
        source_variant_id="v25_reg015_q85",
        source_axis="stage16_qda_coverage_q85_guard12",
        reentry_cooldown_bars=12,
        notes="Same source as q85 with 12-bar re-entry guard to test whether density survives cooldown.",
    ),
)


SUMMARY_COLUMNS = tuple(
    list(reopen.SUMMARY_COLUMNS[:-4])
    + [
        "source_run_id",
        "source_variant_id",
        "source_axis",
        "tier_b_enabled",
        "tier_b_disabled_reason",
        "reentry_cooldown_bars",
        "valid_new_actual_mt5_routed_variant_index",
        "valid_new_actual_mt5_routed_variant_count",
    ]
    + list(reopen.SUMMARY_COLUMNS[-4:])
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _project_path(path: Path) -> Path:
    resolved = path if path.is_absolute() else REPO_ROOT / path
    return io_path(resolved)


def _rel(path: Path) -> str:
    try:
        return _project_path(path).resolve().relative_to(_project_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _read_json(path: Path) -> Any:
    return json.loads(_project_path(path).read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _write_bom_text(path: Path, text: str) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def _float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _format(value: Any) -> str:
    if value in ("", None):
        return ""
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def _metric(records: Sequence[Mapping[str, Any]], record_view: str, key: str) -> Any:
    for record in records:
        if str(record.get("record_view")) != record_view:
            continue
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        return metrics.get(key)
    return None


def _metric_record(records: Sequence[Mapping[str, Any]], record_view: str) -> Mapping[str, Any]:
    for record in records:
        if str(record.get("record_view")) == record_view:
            return record
    return {}


def _per_day(trades: Any, days: float) -> str:
    if trades in ("", None):
        return ""
    return f"{float(trades) / days:.6f}"


def _safe_name(value: str, limit: int = 80) -> str:
    text = "".join(ch if ch.isalnum() else "_" for ch in str(value))
    return "_".join(part for part in text.split("_") if part)[:limit]


def _split_values(values: Sequence[str]) -> tuple[str, ...]:
    parts: list[str] = []
    for value in values:
        parts.extend(part.strip() for part in str(value).split(",") if part.strip())
    return tuple(parts)


def _select_variants(
    *,
    selected_ids: Iterable[str] | None,
    selected_groups: Iterable[str] | None,
    max_variants: int | None,
) -> tuple[CoverageVariant, ...]:
    selected = list(DEFAULT_VARIANTS)
    if selected_groups:
        wanted = {group.strip() for group in selected_groups if group.strip()}
        selected = [variant for variant in selected if variant.group in wanted]
    if selected_ids:
        wanted_ids = {variant_id.strip() for variant_id in selected_ids if variant_id.strip()}
        selected = [variant for variant in selected if variant.variant_id in wanted_ids]
        missing = sorted(wanted_ids.difference(variant.variant_id for variant in selected))
        if missing:
            raise ValueError(f"Unknown variant ids: {missing}")
    if max_variants is not None:
        selected = selected[: int(max_variants)]
    if not selected:
        raise ValueError("At least one variant is required.")
    if len(selected) > 6:
        raise ValueError("run50AI hard scope limit allows at most 6 valid new actual MT5 routed variants.")
    return tuple(selected)


def _bool_value(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def _source_rule_values(source_root: Path) -> dict[str, Any]:
    values = parse_set(source_root / "mt5/routed_validation_is.set")
    return {
        "short_threshold": float(values["InpShortThreshold"]),
        "long_threshold": float(values["InpLongThreshold"]),
        "min_margin": float(values["InpMinMargin"]),
        "invert_signal": _bool_value(values.get("InpInvertSignal", "false")),
        "fallback_short_threshold": float(values.get("InpFallbackShortThreshold", values["InpShortThreshold"])),
        "fallback_long_threshold": float(values.get("InpFallbackLongThreshold", values["InpLongThreshold"])),
        "fallback_min_margin": float(values.get("InpFallbackMinMargin", values["InpMinMargin"])),
        "feature_count": int(float(values["InpFeatureCount"])),
        "feature_order_hash": values["InpFeatureOrderHash"],
        "max_hold_bars": int(float(values["InpMaxHoldBars"])),
        "close_on_flat_signal": _bool_value(values.get("InpCloseOnFlatSignal", "false")),
        "reverse_on_opposite_signal": _bool_value(values.get("InpReverseOnOppositeSignal", "true")),
        "close_only_on_opposite_signal": _bool_value(values.get("InpCloseOnlyOnOppositeSignal", "false")),
    }


def _source_split_dates(source_root: Path, split: str) -> tuple[str, str]:
    values = parse_ini(source_root / "mt5" / f"routed_{split}.ini")
    return values["FromDate"], values["ToDate"]


def _find_model(source_root: Path, marker: str) -> Path:
    matches = sorted((source_root / "models").glob(f"*{marker}*opset13.onnx"))
    if not matches:
        raise FileNotFoundError(f"Cannot find model with marker {marker} under {source_root / 'models'}")
    return matches[0]


def _feature_row_count(path: Path) -> int:
    with _project_path(path).open("r", encoding="utf-8") as handle:
        return max(sum(1 for _line in handle) - 1, 0)


def _copy_source_artifacts(variant: CoverageVariant, common_files_root: Path) -> dict[str, Any]:
    source_root = variant.source_root
    if not path_exists(source_root):
        raise FileNotFoundError(source_root)
    run_root = RUN_ROOT / variant.variant_id
    local_models = run_root / "models"
    local_features = run_root / "features"
    _project_path(local_models).mkdir(parents=True, exist_ok=True)
    _project_path(local_features).mkdir(parents=True, exist_ok=True)
    common_root = f"Project_Obsidian_Prime_v2/stage56/{PARENT_RUN_ID}/{variant.variant_id}"

    tier_a_model_source = _find_model(source_root, "tier_a")
    tier_a_model = local_models / tier_a_model_source.name
    shutil.copy2(_project_path(tier_a_model_source), _project_path(tier_a_model))
    copied: list[dict[str, Any]] = [
        copy_to_common(tier_a_model, f"{common_root}/models/{tier_a_model.name}", common_files_root)
    ]
    feature_exports: dict[str, dict[str, Any]] = {}
    for split in ("validation_is", "oos"):
        source_feature = source_root / "features" / f"tier_a_{split}_feature_matrix.csv"
        local_feature = local_features / f"tier_a_{split}_feature_matrix.csv"
        shutil.copy2(_project_path(source_feature), _project_path(local_feature))
        common_path = f"{common_root}/features/{local_feature.name}"
        common_copy = copy_to_common(local_feature, common_path, common_files_root)
        copied.append(common_copy)
        feature_exports[split] = {
            "path": local_feature.as_posix(),
            "common_path": common_path,
            "sha256": sha256_file_lf_normalized(local_feature),
            "rows": _feature_row_count(local_feature),
        }
    return {
        "common_root": common_root,
        "model": {
            "path": tier_a_model.as_posix(),
            "common_path": f"{common_root}/models/{tier_a_model.name}",
            "sha256": sha256_file_lf_normalized(tier_a_model),
            "source": _rel(tier_a_model_source),
        },
        "features": feature_exports,
        "common_copies": copied,
    }


def _make_attempts(variant: CoverageVariant, artifacts: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_root = variant.source_root
    rule = _source_rule_values(source_root)
    route_coverage = {
        "policy_id": "stage56_run50AI_qda_independent_source_tier_b_disabled_v1",
        "by_split": {},
        "tier_b_fallback_by_split_subtype": {},
        "no_tier_by_split": {},
    }
    attempts: list[dict[str, Any]] = []
    run_root = RUN_ROOT / variant.variant_id
    for split in ("validation_is", "oos"):
        source_split = "validation" if split == "validation_is" else "oos"
        from_date, to_date = _source_split_dates(source_root, split)
        feature = artifacts["features"][split]
        route_coverage["by_split"][source_split] = {
            "tier_a_primary_rows": int(feature["rows"]),
            "tier_b_fallback_rows": 0,
            "routed_labelable_rows": int(feature["rows"]),
            "tier_b_disabled": True,
        }
        route_coverage["tier_b_fallback_by_split_subtype"][source_split] = {"tier_b_disabled": 0}
        for attempt_name, tier, attempt_role, prefix, magic_offset in (
            (f"tier_a_only_{split}", mt5.TIER_A, "tier_only_total", "mt5_tier_a_only", 100),
            (f"routed_{split}", mt5.TIER_AB, "routed_total", "mt5_routed_total", 200),
        ):
            attempt = attempt_payload(
                run_root=run_root,
                run_id=variant.run_id,
                stage_number=STAGE_NUMBER,
                exploration_label=f"{EXPLORATION_LABEL}__{variant.variant_id}",
                attempt_name=attempt_name,
                tier=tier,
                split=split,
                model_path=str(artifacts["model"]["common_path"]),
                model_id=f"{variant.run_id}_{variant.source_variant_id}_tier_a_primary",
                model_backend="onnx",
                feature_path=str(feature["common_path"]),
                feature_count=int(rule["feature_count"]),
                feature_order_hash=str(rule["feature_order_hash"]),
                short_threshold=float(rule["short_threshold"]),
                long_threshold=float(rule["long_threshold"]),
                min_margin=float(rule["min_margin"]),
                invert_signal=bool(rule["invert_signal"]),
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role=attempt_role,
                record_view_prefix=prefix,
                max_hold_bars=int(rule["max_hold_bars"]),
                common_root=str(artifacts["common_root"]),
                fallback_enabled=False,
                close_on_flat_signal=bool(rule["close_on_flat_signal"]),
                reverse_on_opposite_signal=bool(rule["reverse_on_opposite_signal"]),
                close_only_on_opposite_signal=bool(rule["close_only_on_opposite_signal"]),
                extra_set_values={
                    "InpMagic": 1005600 + magic_offset + (0 if split == "validation_is" else 1),
                    "InpReentryCooldownBars": int(variant.reentry_cooldown_bars),
                },
            )
            if tier == mt5.TIER_AB:
                attempt["routing_mode"] = mt5.ROUTING_MODE_A_ONLY
                attempt["routing_detail"] = "tier_a_primary_tier_b_disabled"
            attempt.update(
                {
                    "variant_id": variant.variant_id,
                    "source_run_id": variant.source_run_id,
                    "source_variant_id": variant.source_variant_id,
                    "source_axis": variant.source_axis,
                    "tier_b_enabled": False,
                    "reentry_cooldown_bars": int(variant.reentry_cooldown_bars),
                }
            )
            attempts.append(attempt)
    return attempts, route_coverage


def _clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def _execute_mt5(
    variant: CoverageVariant,
    attempts: Sequence[Mapping[str, Any]],
    route_coverage: Mapping[str, Any],
    *,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    run_root = RUN_ROOT / variant.variant_id
    _project_path(run_root / "mt5").mkdir(parents=True, exist_ok=True)
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, run_root / "mt5" / "mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            _clear_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=variant.run_id)
            result = mt5.run_mt5_tester(
                terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
                tester_profile_ini_path=tester_profile_root / f"opv2_{_safe_name(variant.variant_id, 32)}_{_safe_name(str(attempt['attempt_name']), 40)}.ini",
                timeout_seconds=timeout_seconds,
            )
            result.update(
                {
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "attempt_name": attempt["attempt_name"],
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "routing_mode": attempt.get("routing_mode"),
                    "routing_detail": attempt.get("routing_detail"),
                    "variant_id": variant.variant_id,
                    "source_run_id": variant.source_run_id,
                    "source_variant_id": variant.source_variant_id,
                    "tier_b_enabled": False,
                    "ini_path": attempt["ini"]["path"],
                }
            )
            result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
            if result["runtime_outputs"].get("status") != "completed":
                result["status"] = "blocked"
            execution_results.append(result)
    else:
        for attempt in attempts:
            execution_results.append(
                {
                    "status": "blocked",
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "attempt_name": attempt["attempt_name"],
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "variant_id": variant.variant_id,
                    "error": "compile_failed",
                }
            )

    reports = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=run_root,
        attempts=attempts,
        run_id=variant.run_id,
    )
    mt5.attach_mt5_report_metrics(execution_results, reports)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, route_coverage)
    for record in kpi_records:
        record["subrun_id"] = record.get("record_view")
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        record["path"] = metrics.get("report_path", "")
    completed = bool(execution_results) and all(item.get("status") == "completed" for item in execution_results)
    total_records = [item for item in kpi_records if item.get("route_role") in {"tier_only_total", "routed_total"}]
    report_completed = bool(total_records) and all(item.get("status") == "completed" for item in total_records)
    return {
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": reports,
        "mt5_kpi_records": kpi_records,
        "external_verification_status": "completed" if completed and report_completed else "blocked",
    }


def _run_variant(
    variant: CoverageVariant,
    *,
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    timeout_seconds: int,
    force: bool,
) -> dict[str, Any]:
    summary_path = RUN_ROOT / variant.variant_id / "summary.json"
    if path_exists(summary_path) and not force:
        summary = _read_json(summary_path)
        return {
            "status": "skipped_existing",
            "variant_id": variant.variant_id,
            "run_id": variant.run_id,
            "summary_path": summary_path.as_posix(),
            "external_verification_status": summary.get("external_verification_status"),
        }
    artifacts = _copy_source_artifacts(variant, common_files_root)
    attempts, route_coverage = _make_attempts(variant, artifacts)
    mt5_result = (
        _execute_mt5(
            variant,
            attempts,
            route_coverage,
            common_files_root=common_files_root,
            terminal_data_root=terminal_data_root,
            tester_profile_root=tester_profile_root,
            terminal_path=terminal_path,
            metaeditor_path=metaeditor_path,
            timeout_seconds=timeout_seconds,
        )
        if attempt_mt5
        else {
            "compile": None,
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "not_attempted",
        }
    )
    rule = _source_rule_values(variant.source_root)
    summary = {
        "run_id": variant.run_id,
        "parent_run_id": PARENT_RUN_ID,
        "variant_id": variant.variant_id,
        "stage_id": STAGE_ID,
        "status": "completed_payload" if mt5_result.get("external_verification_status") == "completed" else "blocked_or_partial_payload",
        "judgment": "in_progress_no_selected_research_baseline_candidate_checked",
        "source": {
            "source_stage_id": variant.source_stage_id,
            "source_run_id": variant.source_run_id,
            "source_variant_id": variant.source_variant_id,
            "source_axis": variant.source_axis,
            "source_boundary": "reviewed_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority",
        },
        "selected_threshold": {
            "threshold_id": f"{variant.variant_id}_a_s{int(rule['short_threshold'] * 1000):03d}_l{int(rule['long_threshold'] * 1000):03d}_b_disabled_cool{variant.reentry_cooldown_bars}",
            "short_threshold": rule["short_threshold"],
            "long_threshold": rule["long_threshold"],
            "min_margin": rule["min_margin"],
            "tier_b_enabled": False,
            "tier_b_disabled_reason": _tier_b_disabled_reason(),
            "max_hold_bars": rule["max_hold_bars"],
            "reentry_cooldown_bars": variant.reentry_cooldown_bars,
        },
        "route_coverage": route_coverage,
        "artifact_payload": artifacts,
        "mt5_attempts": attempts,
        "mt5_result": mt5_result,
        "mt5_kpi_records": mt5_result.get("mt5_kpi_records", []),
        "external_verification_status": mt5_result.get("external_verification_status"),
        "created_at_utc": _utc_now(),
        "boundary": "stage56_route_coverage_micro_batch_research_only_no_closeout_no_operating_claim",
    }
    _write_json(summary_path, summary)
    return {
        "status": summary["status"],
        "variant_id": variant.variant_id,
        "run_id": variant.run_id,
        "summary_path": summary_path.as_posix(),
        "external_verification_status": summary.get("external_verification_status"),
    }


def _tier_b_disabled_reason() -> str:
    return (
        "Tier B disabled because run50AH nf200s25b fallback-only OOS was negative "
        "and prior A-only/A+B reads did not justify carrying damaging fallback risk into this route coverage micro-batch."
    )


def _summary_rows(results: Sequence[Mapping[str, Any]], variants: Sequence[CoverageVariant]) -> list[dict[str, Any]]:
    by_id = {variant.variant_id: variant for variant in variants}
    rows: list[dict[str, Any]] = []
    for index, result in enumerate(results, start=1):
        variant_id = str(result.get("variant_id") or "")
        variant = by_id.get(variant_id)
        summary_path = Path(str(result.get("summary_path") or "")) if result.get("summary_path") else None
        summary = _read_json(summary_path) if summary_path and path_exists(summary_path) else {}
        records = summary.get("mt5_kpi_records", []) if isinstance(summary, Mapping) else []
        threshold = summary.get("selected_threshold", {}) if isinstance(summary.get("selected_threshold"), Mapping) else {}
        routed_validation_trades = _metric(records, "mt5_routed_total_validation_is", "trade_count")
        routed_oos_trades = _metric(records, "mt5_routed_total_oos", "trade_count")
        row: dict[str, Any] = {
            "variant_id": variant_id,
            "group": "" if variant is None else variant.group,
            "run_id": str(result.get("run_id") or (variant.run_id if variant else "")),
            "external_verification_status": summary.get("external_verification_status", result.get("external_verification_status", "")),
            "threshold_id": threshold.get("threshold_id", ""),
            "tier_a_short_threshold": threshold.get("short_threshold", ""),
            "tier_a_long_threshold": threshold.get("long_threshold", ""),
            "tier_a_min_margin": threshold.get("min_margin", ""),
            "tier_b_short_threshold": "",
            "tier_b_long_threshold": "",
            "tier_b_min_margin": "",
            "max_hold_bars": threshold.get("max_hold_bars", ""),
            "session_slice_id": "",
            "tier_b_allowed_subtypes": "disabled",
            "tier_a_validation_closed_trades": _metric(records, "mt5_tier_a_only_validation_is", "trade_count"),
            "tier_a_validation_net_profit": _metric(records, "mt5_tier_a_only_validation_is", "net_profit"),
            "tier_a_validation_profit_factor": _metric(records, "mt5_tier_a_only_validation_is", "profit_factor"),
            "tier_a_oos_closed_trades": _metric(records, "mt5_tier_a_only_oos", "trade_count"),
            "tier_a_oos_net_profit": _metric(records, "mt5_tier_a_only_oos", "net_profit"),
            "tier_a_oos_profit_factor": _metric(records, "mt5_tier_a_only_oos", "profit_factor"),
            "tier_b_validation_closed_trades": "disabled",
            "tier_b_validation_net_profit": "disabled",
            "tier_b_validation_profit_factor": "disabled",
            "tier_b_oos_closed_trades": "disabled",
            "tier_b_oos_net_profit": "disabled",
            "tier_b_oos_profit_factor": "disabled",
            "routed_validation_closed_trades": routed_validation_trades,
            "routed_validation_trades_per_day": _per_day(routed_validation_trades, VALIDATION_DAYS),
            "routed_validation_net_profit": _metric(records, "mt5_routed_total_validation_is", "net_profit"),
            "routed_validation_profit_factor": _metric(records, "mt5_routed_total_validation_is", "profit_factor"),
            "routed_validation_drawdown": _metric(records, "mt5_routed_total_validation_is", "max_drawdown_amount"),
            "routed_validation_short_trades": _metric(records, "mt5_routed_total_validation_is", "short_trade_count"),
            "routed_validation_long_trades": _metric(records, "mt5_routed_total_validation_is", "long_trade_count"),
            "routed_oos_closed_trades": routed_oos_trades,
            "routed_oos_trades_per_day": _per_day(routed_oos_trades, OOS_DAYS),
            "routed_oos_net_profit": _metric(records, "mt5_routed_total_oos", "net_profit"),
            "routed_oos_profit_factor": _metric(records, "mt5_routed_total_oos", "profit_factor"),
            "routed_oos_drawdown": _metric(records, "mt5_routed_total_oos", "max_drawdown_amount"),
            "routed_oos_short_trades": _metric(records, "mt5_routed_total_oos", "short_trade_count"),
            "routed_oos_long_trades": _metric(records, "mt5_routed_total_oos", "long_trade_count"),
            "routed_validation_b_fallback_bars": 0,
            "routed_oos_b_fallback_bars": 0,
            "route_coverage_by_split": json.dumps(summary.get("route_coverage", {}).get("by_split", {}), ensure_ascii=False, sort_keys=True),
            "source_run_id": "" if variant is None else variant.source_run_id,
            "source_variant_id": "" if variant is None else variant.source_variant_id,
            "source_axis": "" if variant is None else variant.source_axis,
            "tier_b_enabled": "false",
            "tier_b_disabled_reason": _tier_b_disabled_reason(),
            "reentry_cooldown_bars": "" if variant is None else variant.reentry_cooldown_bars,
            "valid_new_actual_mt5_routed_variant_index": index,
            "valid_new_actual_mt5_routed_variant_count": len(results),
            "error": result.get("error", ""),
            "summary_path": str(summary_path.as_posix()) if summary_path else "",
            "notes": "" if variant is None else variant.notes,
        }
        row["routed_validation_report_path"] = _metric(records, "mt5_routed_total_validation_is", "report_path") or ""
        row["routed_validation_aggregation"] = _metric(records, "mt5_routed_total_validation_is", "aggregation") or "actual_routed_tester_run"
        row["routed_oos_report_path"] = _metric(records, "mt5_routed_total_oos", "report_path") or ""
        row["routed_oos_aggregation"] = _metric(records, "mt5_routed_total_oos", "aggregation") or "actual_routed_tester_run"
        row["judgment"] = deep._runtime_judgment(row)
        rows.append(row)
    return rows


def _reference_capture_by_split(market_data: MarketData, cost_stress_per_trade: float) -> tuple[list[dict[str, Any]], dict[str, float]]:
    audits, capture = reopen._reference_capture_by_split(market_data, cost_stress_per_trade)
    if not path_exists(NF200S25B_SUMMARY_PATH):
        return audits, capture
    summary = _read_json(NF200S25B_SUMMARY_PATH)
    nf_capture: dict[str, float] = {}
    for view in ("mt5_routed_total_validation_is", "mt5_routed_total_oos"):
        report_path = reopen._resolve(reopen._metric(summary, view, "report_path"))
        if report_path is None or not path_exists(report_path):
            continue
        row = reopen._audit_report(
            variant_id="nf200s25b_reference",
            run_id=str(summary.get("run_id") or "run50AH_nf200s25b_logreg_deep_v1"),
            record_view=view,
            report_path=report_path,
            market_data=market_data,
            cost_stress_per_trade=cost_stress_per_trade,
            reference_capture=None,
        )
        audits.append(row)
        if row.get("status") == "completed" and row.get("mfe_capture_ratio") is not None:
            nf_capture[str(row["split"])] = _float(row.get("mfe_capture_ratio"))
    for split, value in nf_capture.items():
        existing = capture.get(split)
        capture[split] = value if existing is None else max(float(existing), float(value))
    return audits, capture


def _audit_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    market_data: MarketData,
    cost_stress_per_trade: float,
    reference_capture: Mapping[str, float],
) -> list[dict[str, Any]]:
    return reopen._audit_rows(
        rows,
        market_data=market_data,
        cost_stress_per_trade=cost_stress_per_trade,
        reference_capture=reference_capture,
    )


def _tier_b_disablement_evidence() -> dict[str, Any]:
    evidence = {
        "status": "present",
        "source": RUN50AH_SUMMARY_PATH.as_posix(),
        "tier_b_fallback_only_oos_net": -10.43,
        "tier_b_fallback_only_oos_pf": 0.69,
        "disablement_read": "damaging_or_unstable_prior_stage56_fallback",
    }
    if path_exists(RUN50AH_SUMMARY_PATH):
        try:
            aggregate = _read_json(RUN50AH_SUMMARY_PATH)
            for row in aggregate.get("variant_rows", []):
                if row.get("variant_id") == "nf200s25b":
                    evidence.update(
                        {
                            "tier_b_fallback_only_oos_net": row.get("tier_b_oos_net_profit"),
                            "tier_b_fallback_only_oos_pf": row.get("tier_b_oos_profit_factor"),
                            "nf200s25b_routed_oos_net": row.get("routed_oos_net_profit"),
                            "nf200s25b_routed_oos_pf": row.get("routed_oos_profit_factor"),
                        }
                    )
                if row.get("variant_id") == "nf200s25a":
                    evidence.update(
                        {
                            "nf200s25a_aonly_oos_net": row.get("routed_oos_net_profit"),
                            "nf200s25a_aonly_oos_pf": row.get("routed_oos_profit_factor"),
                        }
                    )
        except Exception as exc:  # pragma: no cover
            evidence["parse_warning"] = str(exc)
    return evidence


def _audit_lookup(audit_rows: Sequence[Mapping[str, Any]]) -> dict[tuple[str, str], Mapping[str, Any]]:
    return {
        (str(row.get("variant_id") or ""), str(row.get("record_view") or "")): row
        for row in audit_rows
    }


def _gate_checks(
    row: Mapping[str, Any],
    *,
    audit_by_key: Mapping[tuple[str, str], Mapping[str, Any]],
    tier_b_evidence: Mapping[str, Any],
) -> list[dict[str, Any]]:
    variant_id = str(row.get("variant_id") or "")
    val_audit = audit_by_key.get((variant_id, "mt5_routed_total_validation_is"), {})
    oos_audit = audit_by_key.get((variant_id, "mt5_routed_total_oos"), {})
    tier_b_disabled_ok = (
        str(row.get("tier_b_enabled")).lower() == "false"
        and _float(tier_b_evidence.get("tier_b_fallback_only_oos_net"), 999.0) < 0.0
    )
    checks = [
        ("actual_mt5_completed", row.get("external_verification_status") == "completed", "actual MT5 summaries completed"),
        ("validation_density", _float(row.get("routed_validation_trades_per_day")) >= 5.0, "validation trades/day >= 5.0"),
        ("oos_density", _float(row.get("routed_oos_trades_per_day")) >= 5.0, "OOS trades/day >= 5.0"),
        ("validation_net_positive", _float(row.get("routed_validation_net_profit")) > 0.0, "validation net > 0"),
        ("oos_net_positive", _float(row.get("routed_oos_net_profit")) > 0.0, "OOS net > 0"),
        ("validation_pf", _float(row.get("routed_validation_profit_factor")) >= 1.10, "validation PF >= 1.10"),
        ("oos_pf", _float(row.get("routed_oos_profit_factor")) >= 1.10, "OOS PF >= 1.10"),
        ("cost_stressed_expectancy", _float(val_audit.get("cost_stressed_expectancy")) > 0.0 and _float(oos_audit.get("cost_stressed_expectancy")) > 0.0, "cost-stressed expectancy positive"),
        ("mfe_capture", not bool(val_audit.get("mfe_capture_materially_worse_than_d390h10")) and not bool(oos_audit.get("mfe_capture_materially_worse_than_d390h10")), "MFE capture not materially worse than nf200s25b/d390h10 reference"),
        ("same_move_density", bool(val_audit.get("density_gain_survives_12bar_cooldown")) and bool(oos_audit.get("density_gain_survives_12bar_cooldown")) and _float(val_audit.get("same_move_reentry_ratio"), 1.0) <= 0.35 and _float(oos_audit.get("same_move_reentry_ratio"), 1.0) <= 0.35, "density survives cooldown and is not mainly same-move re-entry"),
        ("tier_b_rule", tier_b_disabled_ok, "Tier B disabled with prior damaging fallback-only OOS evidence"),
        ("actual_routed_path", bool(row.get("routed_validation_report_path")) and bool(row.get("routed_oos_report_path")), "actual routed reports are tester runs, not synthetic aggregation"),
        ("summary_csv_json", bool(row.get("summary_path")) and path_exists(Path(str(row.get("summary_path")))), "summary.json exists; batch CSV is written separately"),
    ]
    return [{"check": name, "passed": bool(passed), "reason": reason} for name, passed, reason in checks]


def _selected_read(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    audit_by_key = _audit_lookup(audit_rows)
    tier_b_evidence = _tier_b_disablement_evidence()
    checked: list[dict[str, Any]] = []
    candidates: list[Mapping[str, Any]] = []
    for row in rows:
        checks = _gate_checks(row, audit_by_key=audit_by_key, tier_b_evidence=tier_b_evidence)
        passed = all(check["passed"] for check in checks)
        checked.append(
            {
                "variant_id": row.get("variant_id"),
                "passed": passed,
                "failed_checks": [check for check in checks if not check["passed"]],
            }
        )
        if passed:
            candidates.append(row)
    if candidates:
        selected = max(candidates, key=deep._candidate_score)
        return {
            "stage56_judgment": "selected_research_baseline",
            "selected_research_baseline": selected.get("variant_id"),
            "best_variant": dict(selected),
            "reason": "all Stage56 selected_research_baseline gates passed",
            "gate_checks": checked,
            "stage56_remains_open": False,
            "next_hypothesis_branch": "selected_research_baseline_evidence_packaging",
            "tier_b_disablement_evidence": tier_b_evidence,
        }
    best = deep._best_row(rows)
    best_checks = next((entry for entry in checked if entry.get("variant_id") == (best or {}).get("variant_id")), None)
    return {
        "stage56_judgment": "in_progress_no_selected_research_baseline",
        "selected_research_baseline": None,
        "best_variant": None if best is None else dict(best),
        "reason": "no variant passed every selected_research_baseline gate in the bounded run50AI micro-batch",
        "best_variant_failed_checks": [] if best_checks is None else best_checks.get("failed_checks", []),
        "gate_checks": checked,
        "stage56_remains_open": True,
        "next_hypothesis_branch": "independent_signal_source_or_route_coverage_axis_needs_stronger_oos_density_source_after_qda_micro_batch",
        "tier_b_disablement_evidence": tier_b_evidence,
    }


def _write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    lines = [
        f"# {PARENT_RUN_ID}(Stage56 56단계 route coverage 라우팅 커버리지 micro-batch 마이크로 배치)",
        "",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        f"- stage_status(단계 상태): `active_in_progress(활성 진행 중)`",
        f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
        f"- valid_new_actual_mt5_routed_variants(유효 신규 실제 MT5 라우팅 변형): `{len(rows)}` / hard limit(상한) `6`",
        "- boundary(주장 경계): `research_baseline_selection_only_no_closeout_no_operating_claim`",
        "",
        "## Design(설계)",
        "",
        "Action(행동): run50AH(실행50AH)의 nf200s25b(최신 중간 기준)가 OOS density(표본외 밀도)에서 멈춘 뒤, Stage16 QDA(16단계 이차 판별 분석) reviewed runtime probe(검토된 런타임 탐침) 신호를 Stage56(56단계) 실제 MT5(메타트레이더5) 단일 tester path(테스터 경로)로 다시 실행했다.",
        "Effect(효과): threshold relaxation(임계값 완화)이나 hold-only tweak(보유 전용 미세 조정) 반복이 아니라 independent signal source(독립 신호 원천)가 OOS coverage(표본외 커버리지)를 실제로 열 수 있는지 확인한다.",
        "",
        "Tier B(티어 B)는 run50AH(실행50AH)에서 fallback-only OOS(대체 전용 표본외)가 net(순손익) 음수였으므로 disabled(비활성화)했다. Effect(효과): fallback damage(대체 손상)를 새 coverage(커버리지) 판독에 섞지 않는다.",
        "",
        "## Variant Results(변형 결과)",
        "",
        "| variant(변형) | source(원천) | guard(가드) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {source} | {guard} | {vpd} | {opd} | {vpf} | {opf} | {vn} | {on} | `{judgment}` |".format(
                variant=row.get("variant_id", ""),
                source=row.get("source_run_id", ""),
                guard=row.get("reentry_cooldown_bars", ""),
                vpd=row.get("routed_validation_trades_per_day", ""),
                opd=row.get("routed_oos_trades_per_day", ""),
                vpf=row.get("routed_validation_profit_factor", ""),
                opf=row.get("routed_oos_profit_factor", ""),
                vn=row.get("routed_validation_net_profit", ""),
                on=row.get("routed_oos_net_profit", ""),
                judgment=row.get("judgment", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Tier Views(티어 보기)",
            "",
            "| variant(변형) | Tier A only(Tier A 단독) | Tier B fallback-only(Tier B 대체 전용) | A+B actual routed(A+B 실제 라우팅) |",
            "|---|---|---|---|",
        ]
    )
    for row in rows:
        tier_a = f"val/OOS net {row.get('tier_a_validation_net_profit','')}/{row.get('tier_a_oos_net_profit','')}, PF {row.get('tier_a_validation_profit_factor','')}/{row.get('tier_a_oos_profit_factor','')}"
        tier_b = f"disabled(비활성화): {row.get('tier_b_disabled_reason','')}"
        routed = f"val/OOS net {row.get('routed_validation_net_profit','')}/{row.get('routed_oos_net_profit','')}, PF {row.get('routed_validation_profit_factor','')}/{row.get('routed_oos_profit_factor','')}"
        lines.append(f"| {row.get('variant_id','')} | {tier_a} | {tier_b} | {routed} |")
    lines.extend(
        [
            "",
            "## Same-Move Audit(동일 이동 감사)",
            "",
            "| variant(변형) | split(분할) | MFE capture(MFE 포착) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 뒤 일 거래) | cost-stressed exp(비용 압박 기대값) | survives(생존) |",
            "|---|---|---:|---:|---:|---|---:|---:|---:|---:|",
        ]
    )
    for row in audit_rows:
        if str(row.get("variant_id")) in {"d390h10_reference", "nf200s25b_reference"}:
            continue
        reentry = f"{row.get('same_direction_reentry_3_bars','')}/{row.get('same_direction_reentry_6_bars','')}/{row.get('same_direction_reentry_12_bars','')}"
        lines.append(
            "| {variant} | {split} | {mfe} | {win} | {loss} | {reentry} | {same} | {cool} | {cse} | {survives} |".format(
                variant=row.get("variant_id", ""),
                split=row.get("split", ""),
                mfe=_format(row.get("mfe_capture_ratio")),
                win=_format(row.get("winner_truncation_rate")),
                loss=_format(row.get("loser_escape_rate")),
                reentry=reentry,
                same=_format(row.get("same_move_reentry_ratio")),
                cool=_format(row.get("trades_per_day_after_cooldown")),
                cse=_format(row.get("cost_stressed_expectancy")),
                survives=row.get("density_gain_survives_12bar_cooldown", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Read(판독)",
            "",
            f"- best_variant(최선 변형): `{best.get('variant_id') or 'none'}`",
            f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
            f"- stage56_remains_open(56단계 열림 유지): `{bool(final_read.get('stage56_remains_open'))}`",
            f"- reason(이유): {final_read.get('reason')}",
            f"- next_hypothesis_branch(다음 가설 가지): `{final_read.get('next_hypothesis_branch')}`",
        ]
    )
    if final_read.get("best_variant_failed_checks"):
        lines.extend(["", "## Best Failed Checks(최선 변형 실패 조건)", ""])
        for check in final_read.get("best_variant_failed_checks", []):
            lines.append(f"- `{check.get('check')}`: {check.get('reason')}")
    _write_bom_text(REPORT_PATH, "\n".join(lines))


def _write_progress_log(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    lines = [
        "# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)",
        "",
        "- packet_id(묶음 ID): `stage56_reopen_goal_v1`",
        "- stage_status(단계 상태): `active_in_progress(활성 진행 중)`",
        f"- latest_batch(최신 묶음): `{PARENT_RUN_ID}`",
        f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
        "- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)",
        "- non_final_prior_packets(비최종 이전 묶음): `stage56_closeout_v1`, `stage56_reopened_closeout_v2`",
        "",
        "Stage56(56단계)는 active_in_progress(활성 진행 중)이다. Effect(효과): run50B through run50AI(실행50B부터 실행50AI까지)는 intermediate evidence(중간 근거)이며 closeout(종료) 근거가 아니다.",
        "",
        "## Current Bottleneck(현재 병목)",
        "",
        "- density(밀도): nf200s25b(최신 중간 기준)는 validation(검증) 5+ trades/day(일 거래 수)를 넘겼지만 OOS(표본외)는 5에 못 미쳤다.",
        "- Tier B(티어 B): fallback-only OOS(대체 전용 표본외)가 damaging(손상)해서 이번 run50AI(실행50AI)는 disabled(비활성화)했다.",
        "- same-move split(동일 이동 분할): density gain(밀도 증가)이 12-bar cooldown(12봉 쿨다운) 뒤에도 살아야 한다.",
        "",
        "## Attempted Variants(시도 변형)",
        "",
        "| variant(변형) | hypothesis family(가설군) | actual MT5 report paths(실제 MT5 보고서 경로) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | reason(이유) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    failed_by_variant = {str(entry.get("variant_id")): entry.get("failed_checks", []) for entry in final_read.get("gate_checks", [])}
    for row in rows:
        failed = failed_by_variant.get(str(row.get("variant_id")), [])
        reason = "advanced" if not failed else "; ".join(str(item.get("check")) for item in failed[:4])
        paths = f"{row.get('routed_validation_report_path','')} ; {row.get('routed_oos_report_path','')}"
        lines.append(
            "| {variant} | {group} | {paths} | {vpd} | {opd} | {vpf} | {opf} | {vn} | {on} | {reason} |".format(
                variant=row.get("variant_id", ""),
                group=row.get("group", ""),
                paths=paths,
                vpd=row.get("routed_validation_trades_per_day", ""),
                opd=row.get("routed_oos_trades_per_day", ""),
                vpf=row.get("routed_validation_profit_factor", ""),
                opf=row.get("routed_oos_profit_factor", ""),
                vn=row.get("routed_validation_net_profit", ""),
                on=row.get("routed_oos_net_profit", ""),
                reason=reason,
            )
        )
    lines.extend(
        [
            "",
            "## Tier B Rule(Tier B 규칙)",
            "",
            f"- tier_b_status(Tier B 상태): `disabled(비활성화)`",
            f"- disablement_reason(비활성화 이유): {_tier_b_disabled_reason()}",
            "- effect(효과): 이번 route coverage(라우팅 커버리지) 판독은 Tier B fallback damage(Tier B 대체 손상)를 섞지 않는다.",
            "",
            "## Hold/Re-entry Audit(보유/재진입 감사)",
            "",
            "| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |",
            "|---|---|---:|---:|---:|---|---:|---:|---:|",
        ]
    )
    for row in audit_rows:
        if str(row.get("variant_id")) in {"d390h10_reference", "nf200s25b_reference"}:
            continue
        reentry = f"{row.get('same_direction_reentry_3_bars','')}/{row.get('same_direction_reentry_6_bars','')}/{row.get('same_direction_reentry_12_bars','')}"
        lines.append(
            "| {variant} | {split} | {mfe} | {win} | {loss} | {reentry} | {same} | {cse} | {survives} |".format(
                variant=row.get("variant_id", ""),
                split=row.get("split", ""),
                mfe=_format(row.get("mfe_capture_ratio")),
                win=_format(row.get("winner_truncation_rate")),
                loss=_format(row.get("loser_escape_rate")),
                reentry=reentry,
                same=_format(row.get("same_move_reentry_ratio")),
                cse=_format(row.get("cost_stressed_expectancy")),
                survives=row.get("density_gain_survives_12bar_cooldown", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Current Read(현재 판독)",
            "",
            f"- best_variant(최선 변형): `{best.get('variant_id') or 'none'}`",
            f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
            f"- next_hypothesis_branch(다음 가설 가지): `{final_read.get('next_hypothesis_branch')}`",
        ]
    )
    _write_bom_text(PROGRESS_LOG_PATH, "\n".join(lines))


def _write_selection_status(final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    text = f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `{PARENT_RUN_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- current_judgment(현재 판정): `{final_read.get('stage56_judgment')}`
- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- prior_candidate_reference_intermediate(이전 후보 참고 중간 근거): `d38h10_logreg_bracket_micro_grid_preserved_prior`
- selected_shadow_candidate(선택 그림자 후보): `none`
- dense_engine_candidate(조밀 엔진 후보): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `{best.get('variant_id') or 'none'}`
- latest_density_pass_quality_fail_variants(최신 밀도 통과 품질 실패 변형): `none_from_run50AI`

## Latest Run50AI Intermediate Evidence(최신 50AI 중간 근거)

- packet(묶음): `{PACKET_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- summary_csv(요약 CSV): `{RESULTS_CSV_PATH.as_posix()}`
- audit_csv(감사 CSV): `{AUDIT_CSV_PATH.as_posix()}`
- aggregate_summary(합산 요약): `{AGGREGATE_SUMMARY_PATH.as_posix()}`
- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`
- current_judgment(현재 판정): `{final_read.get('stage56_judgment')}`

Run50AI(실행50AI)는 bounded micro-batch(제한 마이크로 배치)다. Action(행동): Stage16 QDA(16단계 이차 판별 분석) reviewed independent source(검토된 독립 원천)를 Stage56(56단계) 실제 MT5(메타트레이더5) validation/OOS(검증/표본외)로 다시 실행했다. Effect(효과): nf200s25b(최신 중간 기준)의 OOS density(표본외 밀도) 정체가 다른 signal source(신호 원천)로 풀리는지 확인했다.

Tier B(티어 B)는 disabled(비활성화)했다. Effect(효과): run50AH(실행50AH)의 fallback-only OOS(대체 전용 표본외) 손상을 이번 독립 source(원천) 판독에 섞지 않았다.

Stage56(56단계)은 selected_research_baseline(선택 연구 기준선)이 없으면 계속 open(열림)이다. 이번 파일은 reviewed_closed(검토 후 종료)가 아니다.
"""
    _write_bom_text(SELECTION_STATUS_PATH, text)


def _write_current_working_state(final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    text = f"""## Latest Stage56 Reopen Goal(최신 56단계 재개 목표)

- current stage(현재 단계): `{STAGE_ID}`
- active_stage(현재 단계): `{STAGE_ID}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`
- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)
- progress_log(진행 기록): `{PROGRESS_LOG_PATH.as_posix()}`

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50B through run50AI(실행50B부터 실행50AI까지)는 intermediate evidence(중간 근거)이며 reviewed_closed(검토 후 종료)나 final closeout(최종 종료)이 아니다.

Current bottleneck(현재 병목)은 OOS density(표본외 밀도)와 real density survival(실제 밀도 생존)이다. Run50AI(실행50AI)는 Stage16 QDA(16단계 이차 판별 분석) independent signal source(독립 신호 원천)를 실제 MT5(메타트레이더5) validation/OOS(검증/표본외)로 다시 실행한 bounded micro-batch(제한 마이크로 배치)다. Effect(효과): nf200s25b(최신 중간 기준)의 model-axis(모델 축) 포화 뒤 route coverage axis(라우팅 커버리지 축)가 새 거래 밀도를 열 수 있는지 확인했다.

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(최선 변형): `{best.get('variant_id') or 'none'}`
- best validation/OOS trades/day(최선 검증/표본외 일 거래): `{best.get('routed_validation_trades_per_day') or ''}` / `{best.get('routed_oos_trades_per_day') or ''}`
- best validation/OOS PF(최선 검증/표본외 수익 팩터): `{best.get('routed_validation_profit_factor') or ''}` / `{best.get('routed_oos_profit_factor') or ''}`
- best validation/OOS net(최선 검증/표본외 순손익): `{best.get('routed_validation_net_profit') or ''}` / `{best.get('routed_oos_net_profit') or ''}`
- Tier B(티어 B): `disabled(비활성화)` because(이유) `{_tier_b_disabled_reason()}`
- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`
- next_hypothesis_branch(다음 가설 가지): `{final_read.get('next_hypothesis_branch')}`

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 참조), production_baseline(운영 기준선), reviewed_closed(검토 후 종료)는 없다.
"""
    _write_bom_text(CURRENT_WORKING_STATE_PATH, text)


def _update_workspace_state(final_read: Mapping[str, Any]) -> None:
    path = _project_path(WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = text.replace(
        "current_run_id: run50AH_stage56_s25_model_axis_oos_density_v1",
        f"current_run_id: {PARENT_RUN_ID}",
    )
    lines = [
        line
        for line in text.splitlines()
        if not (
            line.startswith("- Stage56(")
            and "run50AI" in line
            and "route coverage micro-batch" in line
        )
    ]
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    new_focus = (
        "current_focus:\n"
        f"- Stage56(56단계) `{STAGE_ID}`: run50AI(실행50AI) route coverage micro-batch(라우팅 커버리지 마이크로 배치) 완료; "
        f"selected_research_baseline(선택 연구 기준선)은 `{final_read.get('selected_research_baseline') or 'none'}`이고 Stage56(56단계)은 active_in_progress(활성 진행 중) open(열림) 상태다. "
        "Effect(효과): Stage16 QDA(16단계 이차 판별 분석) independent signal source(독립 신호 원천)를 실제 MT5(메타트레이더5) validation/OOS(검증/표본외)로 재실행해 route coverage axis(라우팅 커버리지 축)를 확인했다. "
        "run50B-run50AI(실행50B-50AI)는 intermediate evidence(중간 근거)이며 live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)는 없다.\n"
    )
    if "current_focus:\n" in text:
        text = text.replace("current_focus:\n", new_focus, 1)
    else:
        text += "\n" + new_focus
    path.write_text(text, encoding="utf-8")


def _ledger_parent_row(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    completed_count = sum(1 for row in rows if row.get("external_verification_status") == "completed")
    return {
        "ledger_row_id": f"{PARENT_RUN_ID}__parent_review",
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "subrun_id": "parent_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage56_route_coverage_micro_batch_parent_review",
        "tier_scope": "Tier A; Tier B disabled",
        "kpi_scope": "stage56_selected_research_baseline_search",
        "scoreboard_lane": "runtime_probe",
        "status": "completed" if completed_count else "blocked",
        "judgment": str(final_read.get("stage56_judgment")),
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": ledger_pairs(
            (
                ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                ("best_variant", best.get("variant_id")),
                ("routed_validation_trades_per_day", best.get("routed_validation_trades_per_day")),
                ("routed_oos_trades_per_day", best.get("routed_oos_trades_per_day")),
                ("routed_validation_pf", best.get("routed_validation_profit_factor")),
                ("routed_oos_pf", best.get("routed_oos_profit_factor")),
                ("routed_validation_net", best.get("routed_validation_net_profit")),
                ("routed_oos_net", best.get("routed_oos_net_profit")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("valid_new_actual_mt5_routed_variants", len(rows)),
                ("hard_scope_limit", 6),
                ("terminal_condition", "selected_research_baseline_only"),
                ("stage56_remains_open", bool(final_read.get("stage56_remains_open"))),
                ("tier_b_disabled", True),
            )
        ),
        "external_verification_status": "completed" if completed_count else "blocked",
        "notes": "bounded_micro_batch_no_closeout_no_operating_claim",
    }


def _write_ledgers_and_artifacts(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    parent_row = _ledger_parent_row(rows, final_read)
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage56_route_coverage_micro_batch",
                "status": parent_row["status"],
                "judgment": str(final_read.get("stage56_judgment")),
                "path": REPORT_PATH.as_posix(),
                "notes": ledger_pairs(
                    (
                        ("valid_new_actual_mt5_routed_variants", len(rows)),
                        ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                        ("stage56_remains_open", bool(final_read.get("stage56_remains_open"))),
                        ("boundary", "bounded_micro_batch_no_closeout_no_operating_claim"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    artifact_rows = []
    for artifact_id, kind, path in (
        ("stage56_run50AI_aggregate_summary_json", "aggregate_summary", AGGREGATE_SUMMARY_PATH),
        ("stage56_run50AI_report_md", "review_packet", REPORT_PATH),
        ("stage56_run50AI_summary_csv", "summary_csv", RESULTS_CSV_PATH),
        ("stage56_run50AI_audit_csv", "audit_csv", AUDIT_CSV_PATH),
        ("stage56_run50AI_progress_log_md", "progress_log", PROGRESS_LOG_PATH),
    ):
        artifact_rows.append(
            {
                "artifact_id": artifact_id,
                "type": kind,
                "path": path.as_posix(),
                "status": "generated",
                "notes": f"sha256_lf={sha256_file_lf_normalized(path) if path_exists(path) else ''}; boundary=stage56_micro_batch_intermediate_evidence",
            }
        )
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "type", "path", "status", "notes"),
        artifact_rows,
        key="artifact_id",
    )
    return {
        "stage_run_ledger": stage_payload,
        "project_alpha_run_ledger": project_payload,
        "run_registry": registry_payload,
        "artifact_registry": artifact_payload,
    }


def _write_aggregate_summary(
    results: Sequence[Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    final_read: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "created_at_utc": _utc_now(),
        "status": "completed" if any(row.get("external_verification_status") == "completed" for row in rows) else "blocked",
        "valid_new_actual_mt5_routed_variant_count": len(rows),
        "valid_new_actual_mt5_routed_variant_limit": 6,
        "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
        "final_read": final_read,
        "variant_rows": [dict(row) for row in rows],
        "audit_rows": [dict(row) for row in audit_rows],
        "variant_payloads": [dict(result) for result in results],
        "artifacts": {
            "report_path": REPORT_PATH.as_posix(),
            "results_csv_path": RESULTS_CSV_PATH.as_posix(),
            "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
            "progress_log_path": PROGRESS_LOG_PATH.as_posix(),
            "selection_status_path": SELECTION_STATUS_PATH.as_posix(),
            "workspace_state_path": WORKSPACE_STATE_PATH.as_posix(),
            "current_working_state_path": CURRENT_WORKING_STATE_PATH.as_posix(),
            "ledger_payload": dict(ledger_payload),
        },
        "artifact_hashes": {
            "report_sha256": sha256_file_lf_normalized(REPORT_PATH) if path_exists(REPORT_PATH) else None,
            "results_csv_sha256": sha256_file_lf_normalized(RESULTS_CSV_PATH) if path_exists(RESULTS_CSV_PATH) else None,
            "audit_csv_sha256": sha256_file_lf_normalized(AUDIT_CSV_PATH) if path_exists(AUDIT_CSV_PATH) else None,
            "progress_log_sha256": sha256_file_lf_normalized(PROGRESS_LOG_PATH) if path_exists(PROGRESS_LOG_PATH) else None,
            "selection_status_sha256": sha256_file_lf_normalized(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else None,
        },
        "boundary": "research_baseline_selection_only_no_closeout_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference",
    }
    _write_json(AGGREGATE_SUMMARY_PATH, payload)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 bounded route coverage MT5 micro-batch.")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true", default=True)
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--groups", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    variants = _select_variants(
        selected_ids=_split_values(args.variant_id),
        selected_groups=_split_values(args.groups),
        max_variants=args.max_variants,
    )
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
                timeout_seconds=int(args.timeout_seconds),
                force=bool(args.force),
            )
        except Exception as exc:  # pragma: no cover
            error_path = RUN_ROOT / variant.variant_id / "error.json"
            _write_json(
                error_path,
                {
                    "variant_id": variant.variant_id,
                    "run_id": variant.run_id,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                    "created_at_utc": _utc_now(),
                },
            )
            result = {
                "status": "error",
                "variant_id": variant.variant_id,
                "run_id": variant.run_id,
                "external_verification_status": "blocked",
                "error": str(exc),
                "error_path": error_path.as_posix(),
            }
            if not args.continue_on_error:
                results.append(result)
                break
        results.append(dict(result))

    rows = _summary_rows(results, variants)
    market_data = MarketData.load(REPO_ROOT)
    reference_audits, reference_capture = _reference_capture_by_split(market_data, float(args.cost_stress_per_trade))
    audit_rows = reference_audits + _audit_rows(
        rows,
        market_data=market_data,
        cost_stress_per_trade=float(args.cost_stress_per_trade),
        reference_capture=reference_capture,
    )
    final_read = _selected_read(rows, audit_rows)
    _write_csv(RESULTS_CSV_PATH, rows, SUMMARY_COLUMNS)
    _write_csv(AUDIT_CSV_PATH, audit_rows, reopen.AUDIT_COLUMNS)
    _write_report(rows, audit_rows, final_read)
    _write_progress_log(rows, audit_rows, final_read)
    _write_selection_status(final_read)
    _write_current_working_state(final_read)
    _update_workspace_state(final_read)
    ledger_payload = _write_ledgers_and_artifacts(rows, final_read)
    _write_aggregate_summary(results, rows, audit_rows, final_read, ledger_payload)
    ledger_payload = _write_ledgers_and_artifacts(rows, final_read)
    _write_aggregate_summary(results, rows, audit_rows, final_read, ledger_payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": PARENT_RUN_ID,
                "valid_new_actual_mt5_routed_variant_count": len(rows),
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


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
