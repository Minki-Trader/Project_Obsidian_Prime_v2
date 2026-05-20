from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267D_adapter_p2_materialization as run267d_materializer
from stage_pipelines.stage267 import run267D_adapter_p2_review as run267d_review


STAGE_ID = input_probe.STAGE_ID
RUN_ID = "run267E_stage267_adapter_p2_followup_design_v1"
RUN_NUMBER = "run267E"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY
STAGE_ROOT = input_probe.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "adapter_p2_followup_design"
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

INPUT_DESIGN_PATH = run267d_materializer.DESIGN_MATRIX_PATH
INPUT_REVIEW_PATH = run267d_review.CANDIDATE_AXIS_REVIEW_PATH
INPUT_NEGATIVE_SLICE_PATH = run267d_review.NEGATIVE_SLICE_PATH

FOLLOWUP_MATRIX_PATH = DESIGN_ROOT / "followup_matrix.csv"
FEATURE_MANIFEST_PATH = DESIGN_ROOT / "feature_manifest.csv"
RUNTIME_CONTRACT_PATH = DESIGN_ROOT / "contract.csv"
ATTEMPT_MANIFEST_PATH = DESIGN_ROOT / "attempts.csv"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267E_p2_followup.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267E_adapter_p2_followup_materialization.py")
OLD_REPORT_REL = (
    "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/"
    "stage267_run267E_adapter_p2_followup_materialization_report.md"
)

STATUS = "run267E_adapter_p2_followup_materialized_execution_pending"
NEXT_ACTION = "run267E_execute_atrcomp_monday_guard_mt5_batch"
PERIOD_LABEL = input_probe.PERIOD_LABEL
COMMON_ROOT = "OPV2/s267e/run267E_adapter_p2_followup"
SOURCE_SIGNAL_COLUMN = input_probe.SOURCE_SIGNAL_COLUMN


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_runtime_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def to_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def to_int(value: Any) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"missing replacement text: {old}")
    return text.replace(old, new, 1)


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def normalize_report_path(text: str) -> str:
    return text.replace(OLD_REPORT_REL, rel(REPORT_PATH))


def common_path(path_text: str) -> Path:
    return COMMON_FILES_ROOT_DEFAULT / Path(path_text)


def is_monday_bar(bar_time_server: str) -> bool:
    try:
        timestamp = datetime.strptime(bar_time_server, "%Y.%m.%d %H:%M:%S")
    except ValueError:
        return False
    return timestamp.weekday() == 0


def source_signal(row: Mapping[str, Any]) -> int:
    try:
        return int(round(float(row.get(SOURCE_SIGNAL_COLUMN) or 0.0)))
    except (TypeError, ValueError):
        return 0


def transform_no_monday(source: Path, destination: Path) -> dict[str, Any]:
    rows = read_csv(source)
    if not rows:
        raise RuntimeError(f"empty source feature file: {source}")
    columns = list(rows[0].keys())
    if SOURCE_SIGNAL_COLUMN not in columns:
        raise RuntimeError(f"missing source signal column: {source}")

    transformed: list[dict[str, Any]] = []
    total_signal_rows = 0
    long_signal_rows = 0
    short_signal_rows = 0
    blocked_rows = 0
    blocked_signal_rows = 0
    blocked_long_signal_rows = 0
    blocked_short_signal_rows = 0
    for row in rows:
        current = dict(row)
        signal = source_signal(row)
        if signal != 0:
            total_signal_rows += 1
            if signal > 0:
                long_signal_rows += 1
            else:
                short_signal_rows += 1
        if is_monday_bar(str(row.get("bar_time_server", ""))):
            blocked_rows += 1
            if signal != 0:
                blocked_signal_rows += 1
                if signal > 0:
                    blocked_long_signal_rows += 1
                else:
                    blocked_short_signal_rows += 1
            current[SOURCE_SIGNAL_COLUMN] = "0"
        transformed.append(current)

    write_runtime_csv(destination, transformed, columns)
    kept_signal_rows = total_signal_rows - blocked_signal_rows
    return {
        "source_feature_file": rel(source),
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "feature_order": ";".join(columns[1:]),
        "feature_order_hash": input_probe.ordered_hash(tuple(columns[1:])),
        "rows": len(rows),
        "total_signal_rows": total_signal_rows,
        "long_signal_rows": long_signal_rows,
        "short_signal_rows": short_signal_rows,
        "blocked_rows": blocked_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "blocked_long_signal_rows": blocked_long_signal_rows,
        "blocked_short_signal_rows": blocked_short_signal_rows,
        "kept_signal_rows": kept_signal_rows,
        "signal_retention": kept_signal_rows / total_signal_rows if total_signal_rows else None,
    }


def copy_model(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {
        "source_model_file": rel(source),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
    }


def review_by_pair() -> dict[tuple[str, str], dict[str, str]]:
    rows = {}
    for row in read_csv(INPUT_REVIEW_PATH):
        rows[(row.get("candidate_alias", ""), row.get("feature_axis", ""))] = row
    return rows


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def followup_decision(row: Mapping[str, str], review: Mapping[str, str]) -> tuple[str, str, str]:
    axis = row.get("axis", "")
    alias = row.get("candidate_alias", "")
    if axis == "atrcomp":
        return (
            "materialize_atrcomp_monday_guard",
            "attempt_planned",
            "run267D에서 atrcomp(ATR 압축 대체)는 순수익이 건설적이지만 Monday(월요일) 약점이 후보 전체에 반복되어 entry weekday guard(진입 요일 방어)를 실제 MT5(MetaTrader 5, 메타트레이더5) 재실행 묶음으로 확인한다.",
        )
    if axis == "late21":
        return (
            "carry_late21_as_adapter_control_reference",
            "design_only",
            "late21(후반 21시)은 DD(drawdown, 손실폭)가 상대적으로 낮아 Adapter prototype(어댑터 원형) 관찰축으로 유지하지만, 새 시도보다 run267D(267D 실행) 결과를 control reference(대조 참고)로 쓴다.",
        )
    if axis == "vlowadx":
        return (
            "hold_vlowadx_for_redesign_or_reject",
            "no_attempt",
            "vlowadx(낮은 변동성+ADX)는 2024-07(2024년 7월)과 chron_mid(중간 시간순 구간) DD(drawdown, 손실폭)가 커서 같은 변형 반복보다 구조 재설계 또는 탈락 검토로 보낸다.",
        )
    return (
        f"hold_{alias}_{axis}",
        "no_attempt",
        "알 수 없는 축이라 새 실행 없이 보류한다.",
    )


def build_attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "source_axis": attempt.get("source_axis"),
                "followup_variant": attempt.get("followup_variant"),
                "followup_action": attempt.get("followup_action"),
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def build_materialization() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    design_input = read_csv(INPUT_DESIGN_PATH)
    reviews = review_by_pair()
    specs = specs_by_alias()
    followup_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []

    atrcomp_index = 0
    for row in design_input:
        alias = row.get("candidate_alias", "")
        axis = row.get("axis", "")
        review = reviews.get((alias, axis), {})
        decision, execution_scope, reason = followup_decision(row, review)
        followup_variant = "atrcomp_monday_guard" if axis == "atrcomp" else axis
        row_base = {
            "candidate_alias": alias,
            "candidate_role": row.get("candidate_role"),
            "source_axis": axis,
            "role_scope": row.get("role_scope"),
            "followup_variant": followup_variant,
            "followup_decision": decision,
            "execution_scope": execution_scope,
            "decision_reason": reason,
            "run267d_net_profit": review.get("net_profit", ""),
            "run267d_profit_factor": review.get("profit_factor", ""),
            "run267d_trade_count": review.get("trade_count", ""),
            "run267d_equity_dd_percent": review.get("report_equity_drawdown_percent", ""),
            "weakest_month": review.get("weakest_month", ""),
            "weakest_month_net": review.get("weakest_month_net", ""),
            "weakest_hour_utc": review.get("weakest_hour_utc", ""),
            "weakest_hour_net": review.get("weakest_hour_net", ""),
            "weakest_chron_segment": review.get("weakest_chron_segment", ""),
            "weakest_chron_net": review.get("weakest_chron_net", ""),
            "source_feature_path": row.get("common_feature_path", ""),
            "source_model_path": row.get("common_model_path", ""),
            "followup_feature_path": "",
            "followup_model_path": "",
            "common_feature_path": "",
            "common_model_path": "",
            "total_signal_rows": "",
            "blocked_signal_rows": "",
            "kept_signal_rows": "",
            "signal_retention": "",
            "feature_order_hash": row.get("feature_order_hash", ""),
            "attempts_planned": 0,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        if axis != "atrcomp":
            followup_rows.append(row_base)
            continue

        atrcomp_index += 1
        spec = specs[alias]
        local_root = DESIGN_ROOT / "atrcomp_monday_guard" / alias
        source_feature = common_path(str(row.get("common_feature_path", "")))
        source_model = common_path(str(row.get("common_model_path", "")))
        feature_path = local_root / "features" / f"{alias}_atrcomp_nomonday.csv"
        model_path = local_root / "models" / f"{alias}_atrcomp_nomonday_model.csv"
        feature_meta = transform_no_monday(source_feature, feature_path)
        model_meta = copy_model(source_model, model_path)
        common_feature_path = f"{COMMON_ROOT}/atrmon/{alias}/features/{feature_path.name}"
        common_model_path = f"{COMMON_ROOT}/atrmon/{alias}/models/{model_path.name}"
        common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
        common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

        feature_row = {
            "candidate_alias": alias,
            "candidate_role": row.get("candidate_role"),
            "source_axis": axis,
            "followup_variant": followup_variant,
            "materialization_rule": "entry signal(진입 신호)을 source bar weekday(원천 봉 요일)가 Monday(월요일)이면 flat(무거래)으로 바꾼다.",
            "source_feature_file": feature_meta["source_feature_file"],
            "feature_file": feature_meta["feature_file"],
            "feature_sha256": feature_meta["feature_sha256"],
            "source_model_file": model_meta["source_model_file"],
            "model_file": model_meta["model_file"],
            "model_sha256": model_meta["model_sha256"],
            "common_feature_path": common_feature_path,
            "common_feature_sha256": common_feature["sha256"],
            "common_model_path": common_model_path,
            "common_model_sha256": common_model["sha256"],
            "feature_order": feature_meta["feature_order"],
            "feature_order_hash": feature_meta["feature_order_hash"],
            "rows": feature_meta["rows"],
            "total_signal_rows": feature_meta["total_signal_rows"],
            "blocked_signal_rows": feature_meta["blocked_signal_rows"],
            "blocked_long_signal_rows": feature_meta["blocked_long_signal_rows"],
            "blocked_short_signal_rows": feature_meta["blocked_short_signal_rows"],
            "kept_signal_rows": feature_meta["kept_signal_rows"],
            "signal_retention": feature_meta["signal_retention"],
        }
        feature_rows.append(feature_row)
        lineage_rows.extend(
            [
                {
                    "candidate_alias": alias,
                    "source_axis": axis,
                    "followup_variant": followup_variant,
                    "artifact_role": "feature_csv",
                    "source_path": feature_meta["source_feature_file"],
                    "run267e_path": feature_meta["feature_file"],
                    "common_path": common_feature_path,
                    "run267e_sha256": feature_meta["feature_sha256"],
                    "common_sha256": common_feature["sha256"],
                },
                {
                    "candidate_alias": alias,
                    "source_axis": axis,
                    "followup_variant": followup_variant,
                    "artifact_role": "model_csv",
                    "source_path": model_meta["source_model_file"],
                    "run267e_path": model_meta["model_file"],
                    "common_path": common_model_path,
                    "run267e_sha256": model_meta["model_sha256"],
                    "common_sha256": common_model["sha256"],
                },
            ]
        )
        row_base.update(
            {
                "followup_feature_path": feature_meta["feature_file"],
                "followup_model_path": model_meta["model_file"],
                "common_feature_path": common_feature_path,
                "common_model_path": common_model_path,
                "total_signal_rows": feature_meta["total_signal_rows"],
                "blocked_signal_rows": feature_meta["blocked_signal_rows"],
                "kept_signal_rows": feature_meta["kept_signal_rows"],
                "signal_retention": feature_meta["signal_retention"],
                "feature_order_hash": feature_meta["feature_order_hash"],
                "attempts_planned": 2,
            }
        )
        followup_rows.append(row_base)
        contract_rows.append(
            {
                "candidate_alias": alias,
                "source_axis": axis,
                "followup_variant": followup_variant,
                "shared_contract": "feature_order;thresholds;model_csv;MT5 runtime settings;2024 historical stress window",
                "feature_count": 3,
                "feature_order": feature_meta["feature_order"],
                "feature_order_hash": feature_meta["feature_order_hash"],
                "model_backend": "ebm_table",
                "short_threshold": spec.variant.short_threshold,
                "long_threshold": spec.variant.long_threshold,
                "min_margin": 0.0,
                "max_hold_bars": spec.variant.max_hold_bars,
                "close_on_flat_signal": spec.variant.close_on_flat_signal,
                "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
                "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
                "known_difference": "run267E blocks source-bar Monday entries for atrcomp only; run267D weakness was measured by trade close weekday, so this is a diagnostic guard rather than a proof of repair.",
                "runtime_claim_boundary": "research_only_runtime_execution_pending",
            }
        )
        for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_atrmon", "ta"),
                (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_atrmon", "rt"),
            ),
            start=1,
        ):
            magic = 26760000 + atrcomp_index * 100 + role_index
            payload = attempt_payload(
                run_root=DESIGN_ROOT,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label="stage267_AdapterP2Followup__atrmon",
                attempt_name=f"{alias}_atrmon_{attempt_token}_2024",
                tier=tier,
                split=PERIOD_LABEL,
                model_path=common_model_path,
                model_id=f"{RUN_ID}_{alias}_atrcomp_monday_guard_2024",
                model_backend="ebm_table",
                feature_path=common_feature_path,
                feature_count=3,
                feature_order_hash=str(feature_meta["feature_order_hash"]),
                short_threshold=spec.variant.short_threshold,
                long_threshold=spec.variant.long_threshold,
                min_margin=0.0,
                invert_signal=False,
                from_date="2024.01.02",
                to_date="2025.01.01",
                primary_active_tier="tier_a",
                attempt_role=attempt_role,
                record_view_prefix=prefix,
                max_hold_bars=spec.variant.max_hold_bars,
                common_root=f"{COMMON_ROOT}/atrmon/{alias}",
                fallback_enabled=False,
                close_on_flat_signal=spec.variant.close_on_flat_signal,
                reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                extra_set_values=input_probe.base_extra_set_values(spec, magic),
            )
            payload.update(
                {
                    "candidate_alias": alias,
                    "candidate_role": row.get("candidate_role"),
                    "source_axis": axis,
                    "followup_variant": followup_variant,
                    "followup_action": decision,
                    "execution_status": "not_executed",
                }
            )
            attempts.append(payload)
    return followup_rows, feature_rows, contract_rows, attempts, lineage_rows


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = [
        ("stage267_run267E_followup_matrix", "followup_matrix", FOLLOWUP_MATRIX_PATH, "Run267E follow-up decisions from run267D review."),
        ("stage267_run267E_feature_manifest", "feature_manifest", FEATURE_MANIFEST_PATH, "Run267E atrcomp Monday-guard feature/model manifest."),
        ("stage267_run267E_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267E runtime contract for planned MT5 attempts."),
        ("stage267_run267E_attempts", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267E planned MT5 set/ini attempts."),
        ("stage267_run267E_lineage", "lineage", LINEAGE_PATH, "Run267E artifact lineage."),
        ("stage267_run267E_result", "result", RESULT_PATH, "Run267E materialization result."),
        ("stage267_run267E_report", "report", REPORT_PATH, "Run267E materialization report."),
    ]
    rows = []
    for artifact_id, artifact_type, path, notes in artifacts:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def update_ledgers(created_at: str, followup_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267E_adapter_p2_followup_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "adapter_p2_followup_materialization",
            "tier_scope": "Tier A and Tier A+B historical 2024 atrcomp Monday-guard attempts planned",
            "scoreboard": "experiment_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "evidence_boundary": "feature_set_ini_materialization_only_no_mt5_kpi_yet_not_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"followup_rows={len(followup_rows)};attempts={len(attempts)};next_action={NEXT_ACTION}.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_adapter_p2_followup",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267E materialized atrcomp Monday-guard attempts; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": "stage267_run267E_adapter_p2_followup_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_p2_followup_materialization",
            "parent_run_id": run267d_materializer.RUN_ID,
            "record_view": "materialized_attempts",
            "tier_scope": "Tier A and Tier A+B historical 2024",
            "kpi_scope": "feature_set_ini_materialization",
            "scoreboard_lane": "adapter_p2_followup",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"followup_rows={len(followup_rows)};attempts={len(attempts)}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "mt5_execution_pending",
            "notes": "Run267E carries Stage58+ prior research into a concrete weak-slice follow-up, but no candidate selection is claimed.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )
    for artifact in artifact_rows(created_at):
        upsert_csv(
            ARTIFACT_REGISTRY_PATH,
            "artifact_id",
            artifact,
            ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        )


def update_current_truth_docs() -> None:
    report_line = f"- Stage267(267단계) run267E Adapter/P2 follow-up materialization(어댑터/2차 대체 후속 물질화): `{rel(REPORT_PATH)}`"

    state = normalize_report_path(io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig"))
    state = replace_once(state, "- current_run(현재 실행): `run267D_stage267_adapter_p2_materialization_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    state = replace_once(state, "- status(상태): `run267D_adapter_p2_mt5_review_completed`", f"- status(상태): `{STATUS}`")
    state = append_after(
        state,
        "- Stage267(267단계) run267D Adapter/P2 MT5 review(어댑터/2차 대체 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_mt5_review.md`",
        report_line,
    )
    state = replace_once(state, "- next_run(다음 실행): `run267D_stage267_adapter_p2_materialization_v1`", f"- next_run(다음 실행): `{RUN_ID}`")
    state = replace_once(
        state,
        "- action(행동): run267D(267D 실행)에서 late21(후반 21시) Adapter prototype(어댑터 원형)과 atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX) P2 replacement(2차 대체) 30개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행했다.",
        "- action(행동): run267E(267E 실행)에서 run267D(267D 실행) 검토의 atrcomp(ATR 압축 대체) Monday(월요일) 취약점을 MT5(MetaTrader 5, 메타트레이더5) attempt(시도) 10개로 물질화했다.",
    )
    state = replace_once(
        state,
        "- effect(효과): 선택 축이 설계 묶음에 머물지 않고 Strategy Tester(전략 테스터) KPI(핵심 성과 지표), report(보고서), forensics(포렌식) 근거로 넘어갔다.",
        "- effect(효과): Stage58(58단계) 이후 연구가 압축 피처(compressed feature, 압축 피처)로만 남지 않고, 후보군 공통 약점인 요일 취약성을 실제 재실행 가능한 feature/set/ini(피처/설정/초기화) 묶음으로 이어간다.",
    )
    state = replace_once(
        state,
        "- next_action(다음 행동): `run267E_design_adapter_p2_followup_from_run267D_review`. Effect(효과): run267D(267D 실행) 검토에서 보인 atrcomp(ATR 압축 대체) 건설적 축, late21(후반 21시) 어댑터 원형 관찰축, vlowadx(낮은 변동성+ADX) 손실폭 취약축을 다음 설계로 분리한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): atrcomp Monday guard(ATR 압축 월요일 방어)가 실제 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)에서 손실폭을 줄이는지, 아니면 단순 절단인지 확인한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, state)

    selection = normalize_report_path(io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig"))
    selection = replace_once(selection, "- stage_status(단계 상태): `run267D_adapter_p2_mt5_review_completed`", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_once(selection, "- current_run(현재 실행): `run267D_stage267_adapter_p2_materialization_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_once(selection, "- last_completed_run(마지막 완료 실행): `run267A_stage267_baseline_candidate_racing_protocol_v1`", f"- last_completed_run(마지막 완료 실행): `{run267d_materializer.RUN_ID}`")
    selection = append_after(
        selection,
        "- run267D_adapter_p2_mt5_review(267D 어댑터/2차 대체 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_mt5_review.md`",
        f"- run267E_adapter_p2_followup_materialization(267E 어댑터/2차 대체 후속 물질화): `{rel(REPORT_PATH)}`",
    )
    selection = replace_once(selection, "- next_action(다음 행동): `run267E_design_adapter_p2_followup_from_run267D_review`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_once(
        selection,
        "Run267D(267D 실행)는 Adapter/P2 MT5 execution(어댑터/2차 대체 MT5 실행)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 실행된 30개 KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 바탕으로 후속 설계를 분리하는 작업이다.",
        "Run267E(267E 실행)는 Adapter/P2 follow-up materialization(어댑터/2차 대체 후속 물질화)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 atrcomp Monday guard(ATR 압축 월요일 방어) 10개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해 실제 KPI(핵심 성과 지표)를 확인하는 작업이다.",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = normalize_report_path(io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig"))
    review = replace_once(review, "- status(상태): `run267D_adapter_p2_mt5_review_completed`", f"- status(상태): `{STATUS}`")
    review = replace_once(review, "- current_run(현재 실행): `run267D_stage267_adapter_p2_materialization_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_once(review, "- last_completed_run(마지막 완료 실행): `run267A_stage267_baseline_candidate_racing_protocol_v1`", f"- last_completed_run(마지막 완료 실행): `{run267d_materializer.RUN_ID}`")
    review = append_after(
        review,
        "- run267D_adapter_p2_mt5_review(267D 어댑터/2차 대체 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_mt5_review.md`",
        f"- run267E_adapter_p2_followup_materialization(267E 어댑터/2차 대체 후속 물질화): `{rel(REPORT_PATH)}`",
    )
    review = replace_once(
        review,
        "Run267D(267D 실행)는 Adapter/P2 MT5 execution(어댑터/2차 대체 MT5 실행)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267E_design_adapter_p2_followup_from_run267D_review`에서 다음 Adapter/P2(어댑터/2차 대체) 설계를 분리한다.",
        f"Run267E(267E 실행)는 Adapter/P2 follow-up materialization(어댑터/2차 대체 후속 물질화)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`에서 atrcomp Monday guard(ATR 압축 월요일 방어)를 실제 KPI(핵심 성과 지표)로 확인한다.",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = normalize_report_path(io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig"))
    workspace = replace_once(workspace, "current_run_id: run267D_stage267_adapter_p2_materialization_v1", f"current_run_id: {RUN_ID}")
    workspace = replace_once(
        workspace,
        "Stage267(267단계) run267D(267D 실행) Adapter/P2 MT5 review(어댑터/2차 대체 MT5 검토) `run267D_adapter_p2_mt5_review_completed`. Effect(효과): `30` attempts(시도)에서 `30` KPI records(핵심 성과 지표 기록)를 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "Stage267(267단계) run267E(267E 실행) Adapter/P2 follow-up materialization(어댑터/2차 대체 후속 물질화) `run267E_adapter_p2_followup_materialized_execution_pending`. Effect(효과): atrcomp Monday guard(ATR 압축 월요일 방어) 10개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace = replace_once(
        workspace,
        "Next action(다음 행동)는 `run267E_design_adapter_p2_followup_from_run267D_review`이다. Effect(효과): run267D(267D 실행) review(검토)에서 보인 atrcomp(ATR 압축 대체), late21(후반 21시), vlowadx(낮은 변동성+ADX)의 다른 약점을 다음 설계에서 분리한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): atrcomp Monday guard(ATR 압축 월요일 방어)가 실제 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)에서 덜 깨지는지 확인한다.",
    )
    workspace = replace_once(
        workspace,
        "Stage266(266단계) `266_adapter_research__late_segment_stability_repair_after_stage265_review` was superseded before run execution(실행 전 대체) by the user-directed long R&D racing goal(장기 연구개발 경주 목표), and Stage267(267단계) `267_adapter_research__baseline_candidate_racing_protocol` is active_run267D_adapter_p2_materialized_execution_pending(267D 어댑터/2차 대체 물질화 뒤 실행 대기 활성). Effect(효과): a single-candidate late-segment repair(단일 후보 후반 구간 수리) no longer drives the next work; the five-candidate research baseline pool(연구 기준 후보군)이 같은 조건에서 비교된다.",
        "Stage266(266단계) `266_adapter_research__late_segment_stability_repair_after_stage265_review` was superseded before run execution(실행 전 대체) by the user-directed long R&D racing goal(장기 연구개발 경주 목표), and Stage267(267단계) `267_adapter_research__baseline_candidate_racing_protocol` is active_run267E_adapter_p2_followup_materialized_execution_pending(267E 어댑터/2차 대체 후속 물질화 뒤 실행 대기 활성). Effect(효과): a single-candidate late-segment repair(단일 후보 후반 구간 수리) no longer drives the next work; the five-candidate research baseline pool(연구 기준 후보군)이 같은 조건에서 비교된다.",
    )
    workspace = replace_once(workspace, "  status: run267D_adapter_p2_mt5_review_completed", f"  status: {STATUS}")
    workspace = replace_once(workspace, "  current_run_id: run267D_stage267_adapter_p2_materialization_v1", f"  current_run_id: {RUN_ID}")
    workspace = replace_once(workspace, "  next_action: run267E_design_adapter_p2_followup_from_run267D_review", f"  next_action: {NEXT_ACTION}")
    workspace = append_after(
        workspace,
        "  historical_2024_balance_time_slice_review_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_balance_time_slice_review.md",
        f"  run267E_adapter_p2_followup_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(
    result: Mapping[str, Any],
    followup_rows: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
) -> str:
    materialized = [row for row in followup_rows if row.get("execution_scope") == "attempt_planned"]
    design_only = [row for row in followup_rows if row.get("execution_scope") != "attempt_planned"]
    lines = [
        "# Stage267 Run267E Adapter/P2 Follow-up Materialization(267단계 267E 어댑터/2차 대체 후속 물질화)",
        "",
        "- action(행동): run267D(267D 실행) review(검토)에서 나온 atrcomp(ATR 압축 대체) Monday(월요일) 약점을 entry weekday guard(진입 요일 방어) feature variant(피처 변형)로 물질화했다.",
        "- effect(효과): Stage58(58단계) 이후 연구가 압축 피처(compressed feature, 압축 피처)로만 남지 않고, 실제 MT5(MetaTrader 5, 메타트레이더5) 재실행 가능한 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 이어진다.",
        f"- followup_rows(후속 행): `{len(followup_rows)}`",
        f"- materialized_feature_variants(물질화 피처 변형): `{len(feature_rows)}`",
        f"- attempts_planned(계획 시도): `{result['attempt_count']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Stage58 Answer(58단계 질문 답)",
        "",
        "충분히 활용했다고 보기는 어렵다.",
        "",
        "- used(활용): Stage58(58단계) 이후 risk/ATR(위험/ATR), state/context(상태/문맥), rank/gate bucket(순위/게이트 구간)은 후속 후보의 재료로 남았다.",
        "- not enough(부족): 후보군 기준의 full ablation(전체 제거), similar replacement(유사 대체), 2024 stress(2024 압박), zoom equity review(확대 평가금 검토)는 뒤늦게 Stage267(267단계)에서 다시 열렸다.",
        "- practical read(실전 판독): 이전 연구는 버려진 것이 아니라 압축되어 있었고, 지금 goal(목표)에는 그 압축을 다시 풀어 공통 검증판으로 올리는 일이 필요하다.",
        "",
        "## Materialized Branch(물질화 분기)",
        "",
        "| candidate(후보) | source axis(원천 축) | run267D net(267D 순수익) | run267D PF(267D 수익 팩터) | DD%(손실폭) | blocked signals(차단 신호) | retention(유지율) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in materialized:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['source_axis']}` | {csv_value(row.get('run267d_net_profit'))} | {csv_value(row.get('run267d_profit_factor'))} | {csv_value(row.get('run267d_equity_dd_percent'))} | {csv_value(row.get('blocked_signal_rows'))} | {csv_value(row.get('signal_retention'))} |"
        )
    lines.extend(
        [
            "",
            "## Held Branches(보류 분기)",
            "",
            "| candidate(후보) | source axis(원천 축) | decision(판정) | effect(효과) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in design_only:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['source_axis']}` | `{row['followup_decision']}` | {row['decision_reason']} |"
        )
    lines.extend(
        [
            "",
            "## Experiment Design Receipt(실험 설계 기록)",
            "",
            "- hypothesis(가설): atrcomp(ATR 압축 대체)의 headline KPI(대표 핵심 성과 지표)는 건설적이지만 Monday(월요일) 약점이 공통으로 반복되므로, source-bar Monday(원천 봉 월요일) 진입을 막으면 DD(drawdown, 손실폭)가 줄어드는지 확인한다.",
            "- comparison(비교): run267D(267D 실행) atrcomp(ATR 압축 대체) 결과와 run267E(267E 실행) atrcomp Monday guard(ATR 압축 월요일 방어)를 candidate(후보)별로 비교한다.",
            "- control(통제): model CSV(모델 표), threshold(임계값), max hold(최대 보유), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), 2024 date window(2024 날짜 구간)는 유지한다.",
            "- changed variable(변경 변수): entry signal(진입 신호)만 Monday(월요일) source bar(원천 봉)에서 flat(무거래)으로 바꾼다.",
            "- invalid condition(무효 조건): 단순 거래 절단으로 순수익만 좋아지고 trade count(거래 수), curve shape(곡선 형태), DD(drawdown, 손실폭)가 불편하면 후보 개선으로 보지 않는다.",
            "- stop condition(중단 조건): 이 분기가 월요일 하나에 과적합하거나 손실을 다른 구간으로 밀면 repair loop(수리 반복)를 닫고 feature engineering(피처 엔지니어링) 또는 후보 탈락으로 넘긴다.",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준선): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- result_subject(결과 대상): `run267E_adapter_p2_followup_materialization`.",
            "- evidence_available(사용 가능 근거): run267D(267D 실행) review(검토), feature/model lineage(피처/모델 계보), set/ini manifest(설정/초기화 목록).",
            "- evidence_missing(빠진 근거): run267E(267E 실행) MT5(MetaTrader 5, 메타트레이더5) execution(실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice review(시간 구간 검토).",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def materialize() -> dict[str, Any]:
    created_at = utc_now()
    followup_rows, feature_rows, contract_rows, attempts, lineage_rows = build_materialization()
    result = {
        "status": STATUS,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "followup_rows": len(followup_rows),
        "feature_variant_count": len(feature_rows),
        "contract_rows": len(contract_rows),
        "attempt_count": len(attempts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "followup_matrix": rel(FOLLOWUP_MATRIX_PATH),
            "feature_manifest": rel(FEATURE_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        FOLLOWUP_MATRIX_PATH,
        followup_rows,
        (
            "candidate_alias",
            "candidate_role",
            "source_axis",
            "role_scope",
            "followup_variant",
            "followup_decision",
            "execution_scope",
            "decision_reason",
            "run267d_net_profit",
            "run267d_profit_factor",
            "run267d_trade_count",
            "run267d_equity_dd_percent",
            "weakest_month",
            "weakest_month_net",
            "weakest_hour_utc",
            "weakest_hour_net",
            "weakest_chron_segment",
            "weakest_chron_net",
            "source_feature_path",
            "source_model_path",
            "followup_feature_path",
            "followup_model_path",
            "common_feature_path",
            "common_model_path",
            "total_signal_rows",
            "blocked_signal_rows",
            "kept_signal_rows",
            "signal_retention",
            "feature_order_hash",
            "attempts_planned",
            "claim_boundary",
        ),
    )
    write_csv(
        FEATURE_MANIFEST_PATH,
        feature_rows,
        (
            "candidate_alias",
            "candidate_role",
            "source_axis",
            "followup_variant",
            "materialization_rule",
            "source_feature_file",
            "feature_file",
            "feature_sha256",
            "source_model_file",
            "model_file",
            "model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_order",
            "feature_order_hash",
            "rows",
            "total_signal_rows",
            "blocked_signal_rows",
            "blocked_long_signal_rows",
            "blocked_short_signal_rows",
            "kept_signal_rows",
            "signal_retention",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        contract_rows,
        (
            "candidate_alias",
            "source_axis",
            "followup_variant",
            "shared_contract",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "model_backend",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        build_attempt_rows(attempts),
        (
            "candidate_alias",
            "candidate_role",
            "source_axis",
            "followup_variant",
            "followup_action",
            "attempt_name",
            "tier",
            "split",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "fallback_enabled",
            "execution_status",
        ),
    )
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "inputs": {
                "run267d_design": rel(INPUT_DESIGN_PATH),
                "run267d_review": rel(INPUT_REVIEW_PATH),
                "run267d_negative_slices": rel(INPUT_NEGATIVE_SLICE_PATH),
            },
            "lineage": lineage_rows,
        },
    )
    write_json(RESULT_PATH, result | {"lineage_rows": len(lineage_rows)})
    write_md(REPORT_PATH, report_markdown(result, followup_rows, feature_rows))
    update_current_truth_docs()
    update_ledgers(created_at, followup_rows, attempts)
    return result


def main() -> int:
    result = materialize()
    print(
        json.dumps(
            {
                "status": result["status"],
                "followup_rows": result["followup_rows"],
                "feature_variant_count": result["feature_variant_count"],
                "attempt_count": result["attempt_count"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
