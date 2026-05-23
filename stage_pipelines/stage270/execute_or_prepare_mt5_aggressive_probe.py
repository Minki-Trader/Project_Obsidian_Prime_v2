from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    attempt_summary_rows,
    clear_runtime_outputs,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_ID = "270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe"
RUN_ID = "run270C_aggressive_probe_mt5_signal_replay_v1"
RUN_NUMBER = "run270C"
SOURCE_RUN_ID = "run270B_aggressive_probe_payload_materialization_v1"
PARENT_RUN_ID = "run270A_aggressive_upside_probe_design_v1"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
EXPLORATION_LABEL = "stage270_Model__AggressiveNonFilterSignalReplay"
SIGNAL_COLUMN = "run270c_long_only_signal"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage270/run270C_aggressive_probe"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN270B = STAGE_ROOT / "02_runs" / "run270B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REPORT_PATH = REVIEWS / "run270C_report.md"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"

MT5_QUEUE = RUN270B / "mt5_probe_queue.csv"
RUN270B_MANIFEST = RUN270B / "run_manifest.json"
RUN270B_PAYLOAD_MANIFEST = RUN270B / "probe_payload_manifest.csv"
RUN270B_REPORT = REVIEWS / "run270B_report.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
REVIEW_INDEX = REVIEWS / "review_index.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def safe_name(value: str, limit: int = 64) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def short_variant_token(variant_id: str) -> str:
    match = re.search(r"(q\d+)", variant_id)
    return match.group(1) if match else safe_name(variant_id, 16).lower()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding=encoding,
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})


def split_dates(frame: pd.DataFrame) -> tuple[str, str]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    if timestamps.empty:
        raise RuntimeError("empty split frame")
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def load_queue_rows() -> list[dict[str, str]]:
    if not path_exists(MT5_QUEUE):
        raise FileNotFoundError(MT5_QUEUE)
    return list(read_csv_rows(MT5_QUEUE))


def load_payload(queue_row: Mapping[str, str]) -> pd.DataFrame:
    payload_path = ROOT / str(queue_row["payload_path"])
    frame = pd.read_parquet(io_path(payload_path)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame[SIGNAL_COLUMN] = pd.to_numeric(frame["variant_decision_flag"], errors="coerce").fillna(0).astype("int8")
    return frame


def export_feature_matrices(queue_rows: Sequence[Mapping[str, str]]) -> tuple[dict[str, Any], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    feature_exports: dict[str, Any] = {}
    split_frames: dict[str, pd.DataFrame] = {}
    supply_rows: list[dict[str, Any]] = []
    for queue_row in queue_rows:
        variant_id = queue_row["variant_id"]
        token = short_variant_token(variant_id)
        payload = load_payload(queue_row)
        for tier_view, tier_token, tier_label in (
            ("Tier A separate", "tier_a", mt5.TIER_A),
            ("Tier B separate", "tier_b", mt5.TIER_B),
        ):
            tier_frame = payload.loc[payload["tier_view"].astype(str).eq(tier_view)].copy()
            for source_split, runtime_split, split_token in (
                ("validation", "validation_is", "val"),
                ("oos", "oos", "oos"),
            ):
                split_frame = tier_frame.loc[tier_frame["split"].astype(str).eq(source_split)].copy()
                split_frame["tier_label"] = tier_label
                split_frame["runtime_split"] = runtime_split
                key = f"{variant_id}__{tier_token}__{runtime_split}"
                out_path = FEATURE_DIR / f"{token}_{tier_token}_{split_token}_signal.csv"
                feature_exports[key] = mt5.export_mt5_feature_matrix_csv(
                    split_frame,
                    (SIGNAL_COLUMN,),
                    out_path,
                    metadata_columns=(
                        "symbol",
                        "split",
                        "tier_view",
                        "tier_label",
                        "variant_id",
                        "variant_role",
                        "candidate_decision_score",
                        "reward_skew_score",
                        "weak_context_cost",
                        "failure_zone_cut_flag",
                        "support_identity_match_flag",
                    ),
                )
                split_frames[key] = split_frame
                supply_rows.append(
                    {
                        "variant_id": variant_id,
                        "queue_role": queue_row.get("queue_role", ""),
                        "tier_scope": tier_label,
                        "split": runtime_split,
                        "rows": int(len(split_frame)),
                        "signal_count": int(split_frame[SIGNAL_COLUMN].sum()),
                        "signal_rate": round(float(split_frame[SIGNAL_COLUMN].mean()) if len(split_frame) else 0.0, 8),
                        "feature_matrix_path": rel(out_path),
                        "feature_matrix_hash": feature_exports[key]["sha256"],
                    }
                )
    return feature_exports, split_frames, supply_rows


def route_coverage_from_supply(supply_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_split: dict[str, dict[str, int]] = {}
    for split in ("validation", "oos"):
        runtime_split = "validation_is" if split == "validation" else split
        tier_a_rows = sum(int(row["rows"]) for row in supply_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_A)
        tier_b_rows = sum(int(row["rows"]) for row in supply_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_B)
        by_split[split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "no_tier_labelable_rows": 0,
        }
    return {
        "by_split": by_split,
        "tier_b_fallback_by_split_subtype": {"validation": {"Tier B structural separate": by_split["validation"]["tier_b_fallback_rows"]}, "oos": {"Tier B structural separate": by_split["oos"]["tier_b_fallback_rows"]}},
        "no_tier_by_split": {"validation": 0, "oos": 0},
    }


def copy_runtime_inputs(feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common_files_root: Path) -> list[dict[str, Any]]:
    copied = []
    model_path = ROOT / str(model_artifact["path"])
    copied.append(copy_to_common(model_path, f"{COMMON_ROOT}/models/{model_path.name}", common_files_root))
    for export in feature_exports.values():
        local = ROOT / str(export["path"])
        copied.append(copy_to_common(local, f"{COMMON_ROOT}/features/{local.name}", common_files_root))
    return copied


def build_attempts(
    queue_rows: Sequence[Mapping[str, str]],
    feature_exports: Mapping[str, Any],
    split_frames: Mapping[str, pd.DataFrame],
    model_artifact: Mapping[str, Any],
    *,
    tier_scopes: set[str],
    limit: int | None = None,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    feature_hash = ordered_hash((SIGNAL_COLUMN,))
    for queue_row in queue_rows:
        variant_id = queue_row["variant_id"]
        token = short_variant_token(variant_id)
        for tier_token, tier_label in (("tier_a", mt5.TIER_A), ("tier_b", mt5.TIER_B)):
            if tier_token not in tier_scopes:
                continue
            for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
                key = f"{variant_id}__{tier_token}__{runtime_split}"
                frame = split_frames[key]
                from_date, to_date = split_dates(frame)
                feature_name = Path(str(feature_exports[key]["path"])).name
                attempt = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=270,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"{token}_{tier_token}_{split_token}",
                    tier=tier_label,
                    split=runtime_split,
                    model_path=f"{COMMON_ROOT}/models/{model_name}",
                    model_id=f"{RUN_ID}_{token}_{tier_token}_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{COMMON_ROOT}/features/{feature_name}",
                    feature_count=1,
                    feature_order_hash=feature_hash,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier=tier_token,
                    attempt_role="tier_only_total",
                    record_view_prefix=f"mt5_{token}_{tier_token}",
                    max_hold_bars=12,
                    common_root=COMMON_ROOT,
                    close_on_flat_signal=False,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values={
                        "InpEntryTransitionOnly": False,
                        "InpReentryCooldownBars": 0,
                        "InpSameDirectionReentryCooldownBars": 0,
                    },
                )
                attempt["variant_id"] = variant_id
                attempt["queue_role"] = queue_row.get("queue_role", "")
                attempt["signal_policy"] = "variant_decision_flag 1 -> long; 0 -> flat; no short side in Stage270 payload"
                attempts.append(attempt)
                if limit is not None and len(attempts) >= limit:
                    return attempts
    return attempts


def execute_prepared(
    prepared: Mapping[str, Any],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
    runtime_timeout_seconds: int,
) -> dict[str, Any]:
    attempts = list(prepared["attempts"])
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, RUN_ROOT / "mt5/mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            result = mt5.run_mt5_tester(
                terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=tester_profile_root / f"opv2_s270c_{attempt['attempt_name']}.ini",
                timeout_seconds=timeout_seconds,
            )
            result.update(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "variant_id": attempt.get("variant_id"),
                    "queue_role": attempt.get("queue_role"),
                    "tier": attempt.get("tier"),
                    "split": attempt.get("split"),
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "signal_policy": attempt.get("signal_policy"),
                    "ini_path": attempt.get("ini", {}).get("path"),
                    "set_path": attempt.get("set", {}).get("path"),
                }
            )
            result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                common_files_root,
                attempt,
                timeout_seconds=runtime_timeout_seconds,
                poll_seconds=2.0,
            )
            if result["runtime_outputs"].get("status") != "completed":
                result["status"] = "blocked"
            execution_results.append(result)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, prepared["route_coverage"])
    return {
        **dict(prepared),
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
    }


def classify_status(result: Mapping[str, Any]) -> tuple[str, str, str, str]:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if not attempts or not kpis:
        return (
            "blocked_aggressive_probe_mt5_signal_replay_no_kpi",
            "blocked_runtime_probe_missing_mt5_execution",
            "blocked",
            "repair_runtime_signal_replay_probe_before_candidate_judgment",
        )
    if completed_exec == len(attempts) and len(kpis) == len(attempts):
        return (
            "completed_aggressive_probe_mt5_signal_replay_no_candidate_selection",
            "runtime_probe_completed_inconclusive_no_candidate_selection",
            "completed",
            "run270D_balance_time_slice_trade_quality_review",
        )
    return (
        "partial_aggressive_probe_mt5_signal_replay_no_candidate_selection",
        "runtime_probe_partial_inconclusive_no_candidate_selection",
        "blocked",
        "run270D_balance_time_slice_trade_quality_review_with_runtime_gaps",
    )


def metric_value(record: Mapping[str, Any], name: str) -> Any:
    return dict(record.get("metrics", {})).get(name)


def kpi_summary_rows(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for record in records:
        report = dict(record.get("report", {}))
        html = dict(report.get("html_report", {})) if isinstance(report.get("html_report"), Mapping) else {}
        rows.append(
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "status": record.get("status"),
                "route_role": record.get("route_role"),
                "net_profit": metric_value(record, "net_profit"),
                "profit_factor": metric_value(record, "profit_factor"),
                "trade_count": metric_value(record, "trade_count"),
                "win_rate_percent": metric_value(record, "win_rate_percent"),
                "max_drawdown_amount": metric_value(record, "max_drawdown_amount"),
                "max_drawdown_percent": metric_value(record, "max_drawdown_percent"),
                "expectancy": metric_value(record, "expectancy"),
                "fill_count": metric_value(record, "fill_count"),
                "reject_count": metric_value(record, "reject_count"),
                "skip_count": metric_value(record, "skip_count"),
                "feature_ready_count": metric_value(record, "feature_ready_count"),
                "model_ok_count": metric_value(record, "model_ok_count"),
                "report_path": html.get("path", ""),
            }
        )
    return rows


def forensics_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    reports_by_attempt = {record.get("attempt_name"): record for record in result.get("strategy_tester_reports", [])}
    rows = []
    for attempt in result.get("attempts", []):
        execution = next((item for item in result.get("execution_results", []) if item.get("attempt_name") == attempt.get("attempt_name")), {})
        report = reports_by_attempt.get(attempt.get("attempt_name"), {})
        metrics = dict(report.get("metrics", {})) if isinstance(report, Mapping) else {}
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name"),
                "variant_id": attempt.get("variant_id"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "tester_status": execution.get("status", "not_attempted"),
                "runtime_status": dict(execution.get("runtime_outputs", {})).get("status", "missing"),
                "report_status": report.get("status", "missing") if isinstance(report, Mapping) else "missing",
                "terminal_returncode": execution.get("returncode"),
                "report_name": report.get("report_name", "") if isinstance(report, Mapping) else "",
                "report_path": dict(report.get("html_report", {})).get("path", "") if isinstance(report.get("html_report"), Mapping) else "",
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "deposit": "500",
                "leverage": "1:100",
                "symbol": "US100",
                "timeframe": "M5",
                "model": "Every tick based on real ticks or tester model=4",
                "cost_boundary": "strategy_tester_report_costs_only_no_cost_edge_claim",
                "set_path": attempt.get("set", {}).get("path"),
                "ini_path": attempt.get("ini", {}).get("path"),
            }
        )
    return rows


def runtime_parity_receipt(result: Mapping[str, Any], status: str) -> list[dict[str, Any]]:
    completed = sum(1 for item in result.get("execution_results", []) if item.get("status") == "completed")
    attempts = len(result.get("attempts", []))
    return [
        {
            "field": "research_path",
            "status": "connected",
            "value": rel(RUN270B),
            "effect": "run270B(270B 실행) payload(페이로드)를 signal replay(신호 재생) feature matrix(피처 행렬)로 바꿨다.",
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "field": "runtime_path",
            "status": "connected" if attempts else "blocked",
            "value": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
            "effect": "기존 RuntimeProbeEA(런타임 탐침 EA)와 ebm_table(EBM 표) backend(백엔드)를 사용했다.",
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "field": "known_differences",
            "status": "bounded",
            "value": "Stage270 payload has binary entry only; runtime replay maps 1 to long and 0 to flat; no short-side claim.",
            "effect": "방향성이 없는 payload(페이로드)를 과장하지 않고 long-only(롱 전용) 탐침으로 제한한다.",
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "field": "parity_check",
            "status": "completed" if completed == attempts and attempts else "blocked_or_partial",
            "value": f"attempts_completed={completed}/{attempts};kpi_records={len(result.get('mt5_kpi_records', []))};status={status}",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)이 KPI(핵심 성과 지표)로 이어졌는지 확인한다.",
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "field": "parity_identity",
            "status": "recorded",
            "value": rel(RUN_ROOT / "run_manifest.json"),
            "effect": "model table(모델 표), feature matrix(피처 행렬), set/ini(설정/초기화) 경로와 hash(해시)를 목록에 남겼다.",
            "runtime_claim_boundary": "runtime_probe",
        },
    ]


def result_judgment_rows(status: str, judgment: str, next_action: str) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run270C aggressive probe MT5 signal replay(270C 공격형 탐침 MT5 신호 재생)",
            "evidence_available": "feature matrices, discrete signal score table, MT5 compile/run attempt, tester reports and KPI rows if produced",
            "evidence_missing": "balance/equity curve review, time-slice KPI, trade-quality review, Adapter package, ONNX export/parity",
            "judgment_label": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "이번 실행은 후보 선택이 아니라 공격형 분기가 MT5 런타임에서 거래 결과로 이어지는지 보는 탐침이다.",
        }
    ]


def artifact_rows(paths: Sequence[Path], created_at: str) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        rows.append(
            {
                "artifact_id": f"stage270_run270C_{safe_name(rel(path), 96)}",
                "artifact_type": "run270C_artifact",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "run270C aggressive probe MT5 signal replay artifact.",
            }
        )
    return rows


def write_report(result: Mapping[str, Any], status: str, judgment: str, next_action: str) -> None:
    kpi_rows = kpi_summary_rows(result.get("mt5_kpi_records", []))
    best_lines = []
    for row in kpi_rows[:24]:
        best_lines.append(
            "| `{record_view}` | `{tier_scope}` | `{split}` | {net_profit} | {profit_factor} | {trade_count} | `{status}` |".format(
                **{key: row.get(key, "") for key in ("record_view", "tier_scope", "split", "net_profit", "profit_factor", "trade_count", "status")}
            )
        )
    if not best_lines:
        best_lines.append("| missing(누락) | missing(누락) | missing(누락) |  |  |  | `no_kpi_records` |")
    write_md(
        REPORT_PATH,
        f"""# Stage270 Run270C Aggressive Probe MT5 Signal Replay(270단계 270C 공격형 탐침 MT5 신호 재생)

- status(상태): `{status}`
- run(실행): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- attempts(시도): `{len(result.get('execution_results', []))}/{len(result.get('attempts', []))}`
- KPI records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`
- judgment(판정): `{judgment}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`

## Plain Result(쉬운 결과)

run270C(270C 실행)는 run270B(270B 실행)의 `variant_decision_flag`를 one-feature EBM table(단일 피처 EBM 표)로 바꿔 MT5(`MetaTrader 5`, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA)에 넣었다.
효과(effect, 효과): 공격형 branch(분기)가 Python payload(파이썬 페이로드)에만 머물지 않고 Strategy Tester(전략 테스터) 시도와 KPI(핵심 성과 지표) 경계까지 이동한다.

## Runtime Boundary(런타임 경계)

- signal policy(신호 정책): `variant_decision_flag=1`은 long(롱), `0`은 flat(무포지션)으로 재생한다.
- known difference(알려진 차이): Stage270(270단계) payload(페이로드)는 short side(숏 방향)를 갖고 있지 않다.
- effect(효과): 이 결과는 long-only runtime probe(롱 전용 런타임 탐침)이며 최종 candidate package(후보 패키지)나 ONNX readiness(온엑스 준비)를 만들지 않는다.

## KPI Preview(KPI 미리보기)

| record_view(기록 보기) | tier(티어) | split(분할) | net_profit(순손익) | PF(수익 팩터) | trades(거래 수) | status(상태) |
|---|---|---|---:|---:|---:|---|
{chr(10).join(best_lines)}

## Required Gate Coverage(필수 게이트 커버리지)

- runtime_evidence_gate(런타임 근거 게이트): `{ 'passed' if result.get('mt5_kpi_records') else 'blocked' }`
- scope_completion_gate(범위 완료 게이트): `{ 'passed' if result.get('attempts') else 'blocked' }`
- kpi_contract_audit(KPI 계약 감사): `{ 'passed' if result.get('mt5_kpi_records') else 'blocked' }`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): `{ 'passed' if result.get('mt5_kpi_records') else 'blocked' }`
- final_claim_guard(최종 주장 가드): `passed_no_selected_candidate_no_onnx_no_goal_achieve`

## Boundary(경계)

This run(이 실행)은 deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
""",
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    selection = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        (
            "run270C(270C 실행)는 run270B(270B 실행)의 binary signal(이진 신호)을 one-feature EBM table(단일 피처 EBM 표)로 바꿔 "
            "MT5(MetaTrader 5, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA)에서 실행했다.\n"
            f"효과(effect, 효과): attempts(시도) `{attempt_count}`개와 KPI records(KPI 기록) `{kpi_count}`개를 만들었지만, "
            "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 주장하지 않는다."
        ),
    )
    selection = append_once(
        selection,
        "run270C_report(270C 보고)",
        f"- run270C_report(270C 보고): `{rel(REPORT_PATH)}`\n- run270C_kpi_summary(270C KPI 요약): `{rel(RUN_ROOT / 'mt5_kpi_summary.csv')}`",
    )
    write_md(SELECTED, selection)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    run270c_summary = f"- run270C_summary(270C 요약): run270C(270C 실행)는 aggressive probe(공격형 탐침) signal replay(신호 재생)를 MT5(MetaTrader 5, 메타트레이더5)로 시도했다. Effect(효과): attempts(시도) `{attempt_count}`개와 KPI records(KPI 기록) `{kpi_count}`개를 남겼고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    current = replace_line_prefix(current, "- run270C_summary(270C 요약):", run270c_summary)
    write_md(CURRENT_STATE, current)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run270C_report(270C 보고)",
        f"- run270C_report(270C 보고): `{rel(REPORT_PATH)}`\n- run270C_manifest(270C 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`\n- run270C_runtime_parity_receipt(270C 런타임 동등성 영수증): `{rel(RUN_ROOT / 'runtime_parity_receipt.csv')}`",
    )
    write_md(REVIEW_INDEX, review)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage270(270단계) run270C(270C 실행) aggressive probe MT5 signal replay(공격형 탐침 MT5 신호 재생) `{RUN_ID}`. "
        f"Effect(효과): attempts(시도) `{attempt_count}`개와 KPI records(KPI 기록) `{kpi_count}`개를 만들었거나 시도했으며, "
        "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        "run270C_aggressive_probe_mt5_signal_replay_v1",
        f"## 2026-05-23 run270C aggressive probe MT5 signal replay(270C 공격형 탐침 MT5 신호 재생)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): MT5(MetaTrader 5, 메타트레이더5) runtime probe(런타임 탐침)를 시도하고 KPI records(KPI 기록) `{kpi_count}`개를 남겼다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def upsert_ledgers(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> None:
    report = rel(REPORT_PATH)
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_backtest_aggressive_probe_signal_replay",
        "status": status,
        "judgment": judgment,
        "path": report,
        "notes": f"kpi_records={len(result.get('mt5_kpi_records', []))};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}.",
    }
    upsert_csv_rows(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")

    project_rows = []
    stage_rows = []
    records = list(result.get("mt5_kpi_records", []))
    if not records:
        records = [
            {
                "record_view": "mt5_signal_replay_missing",
                "tier_scope": "Tier A/Tier B",
                "split": "validation_oos",
                "status": "blocked",
                "metrics": {},
                "report": {},
            }
        ]
    for record in records:
        view = str(record.get("record_view"))
        metrics = dict(record.get("metrics", {}))
        html = dict(dict(record.get("report", {})).get("html_report", {})) if isinstance(dict(record.get("report", {})).get("html_report", {}), Mapping) else {}
        project_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": view,
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "mt5_runtime_signal_replay_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", status),
                "judgment": judgment,
                "path": html.get("path") or report,
                "primary_kpi": f"net_profit={metrics.get('net_profit')};profit_factor={metrics.get('profit_factor')};trade_count={metrics.get('trade_count')}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;signal_policy=long_only_binary_replay",
                "external_verification_status": external_status,
                "notes": f"next_action={next_action};runtime_authority=not_claimed.",
            }
        )
        stage_rows.append(
            {
                "row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": view,
                "tier_scope": record.get("tier_scope", ""),
                "scoreboard": "runtime_probe",
                "status": record.get("status", status),
                "judgment": judgment,
                "evidence_boundary": "runtime_probe_no_candidate_selection",
                "report_path": report,
                "notes": f"external_verification_status={external_status};selected_candidate=none;onnx_readiness=not_claimed.",
            }
        )
    project_existing = [row for row in read_csv_rows(ALPHA_LEDGER) if str(row.get("run_id", "")).strip() != RUN_ID]
    write_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, [*project_existing, *project_rows])
    stage_columns = list(stage_rows[0].keys())
    stage_existing = [row for row in read_csv_rows(STAGE_LEDGER) if str(row.get("run_id", "")).strip() != RUN_ID]
    write_csv_rows(STAGE_LEDGER, stage_columns, [*stage_existing, *stage_rows])


def write_outputs(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str, created_at: str) -> list[Path]:
    output_paths = [
        RUN_ROOT / "execution_result.json",
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        RUN_ROOT / "mt5_kpi_summary.csv",
        RUN_ROOT / "attempt_summary.csv",
        RUN_ROOT / "backtest_forensics.csv",
        RUN_ROOT / "runtime_parity_receipt.csv",
        RUN_ROOT / "result_judgment.csv",
        RUN_ROOT / "artifact_lineage_receipt.json",
        RUN_ROOT / "lineage.json",
        REPORT_PATH,
    ]
    write_json(RUN_ROOT / "execution_result.json", result, bom=True)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "producer": "stage_pipelines/stage270/execute_or_prepare_mt5_aggressive_probe.py",
        "entry_command": "python stage_pipelines/stage270/execute_or_prepare_mt5_aggressive_probe.py",
        "attempt_count": len(result.get("attempts", [])),
        "execution_result_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage270_variant_decision_flag_signal_replay",
        "signal_policy": "variant_decision_flag 1 -> long; 0 -> flat; no short-side claim",
        "known_differences": ["binary entry payload has no short side", "Tier B is separate structural replay, not fallback routing authority"],
        "compile": result.get("compile", {}),
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "next_action": next_action,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest, bom=True)
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "kpi_scope": "mt5_runtime_signal_replay_probe",
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "external_verification_status": external_status,
            "judgment": judgment,
            "boundary": BOUNDARY,
        },
        bom=True,
    )
    write_csv(RUN_ROOT / "mt5_kpi_summary.csv", kpi_summary_rows(result.get("mt5_kpi_records", [])))
    write_csv(RUN_ROOT / "attempt_summary.csv", attempt_summary_rows([result]))
    write_csv(RUN_ROOT / "backtest_forensics.csv", forensics_rows(result))
    write_csv(RUN_ROOT / "runtime_parity_receipt.csv", runtime_parity_receipt(result, status))
    write_csv(RUN_ROOT / "result_judgment.csv", result_judgment_rows(status, judgment, next_action))
    lineage_payload = {
        "source_inputs": [rel(MT5_QUEUE), rel(RUN270B_MANIFEST), rel(RUN270B_PAYLOAD_MANIFEST), rel(RUN270B_REPORT)],
        "producer": "stage_pipelines/stage270/execute_or_prepare_mt5_aggressive_probe.py",
        "consumer": [next_action, "docs/registers/run_registry.csv", "docs/registers/alpha_run_ledger.csv", "docs/registers/artifact_registry.csv"],
        "artifact_paths": [rel(path) for path in output_paths],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary" if result.get("attempts") else "blocked",
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "artifact_lineage_receipt.json", lineage_payload, bom=True)
    write_json(RUN_ROOT / "lineage.json", lineage_payload, bom=True)
    write_report(result, status, judgment, next_action)

    final_paths = [path for path in output_paths if path_exists(path)]
    lineage_payload["artifact_hashes"] = {rel(path): sha256_file_lf_normalized(path) for path in final_paths if io_path(path).is_file()}
    write_json(RUN_ROOT / "artifact_lineage_receipt.json", lineage_payload, bom=True)
    write_json(RUN_ROOT / "lineage.json", lineage_payload, bom=True)
    output_paths.extend([*FEATURE_DIR.glob("*.csv"), *MODEL_DIR.glob("*.csv"), *MT5_DIR.glob("*.set"), *MT5_DIR.glob("*.ini"), *MT5_DIR.glob("reports/*"), MT5_DIR / "mt5_compile.log"])
    final_paths = [path for path in output_paths if path_exists(path) and io_path(path).is_file()]
    upsert_csv_rows(ARTIFACT_REGISTRY, ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"], artifact_rows(final_paths, created_at), key="artifact_id")
    return final_paths


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)
    queue_rows = load_queue_rows()
    feature_exports, split_frames, supply_rows = export_feature_matrices(queue_rows)
    write_csv(RUN_ROOT / "runtime_supply_matrix.csv", supply_rows)
    model_artifact = export_single_discrete_signal_score_table(
        MODEL_DIR / "stage270_run270C_discrete_long_signal_score_table.csv",
        feature_order=(SIGNAL_COLUMN,),
    )
    tier_scopes = {item.strip().lower() for item in str(args.tier_scopes).split(",") if item.strip()}
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    attempts = build_attempts(queue_rows, feature_exports, split_frames, model_artifact, tier_scopes=tier_scopes, limit=args.limit)
    route_coverage = route_coverage_from_supply(supply_rows)
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": 270,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "common_copies": common_copies,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "runtime_supply_matrix": supply_rows,
        "route_coverage": route_coverage,
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage270_variant_decision_flag_signal_replay",
        "label_id": "not_applicable_precomputed_decision_signal",
        "split_contract": "Stage270 run270B payload split labels validation and oos",
        "stage_inheritance": "Stage267 prior evidence only; Stage269 seed; no selected baseline",
        "claim_boundary": BOUNDARY,
    }
    if args.materialize_only:
        result = {
            **prepared,
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }
    else:
        result = execute_prepared(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
            runtime_timeout_seconds=int(args.runtime_timeout_seconds),
        )
    status, judgment, external_status, next_action = classify_status(result)
    result = {
        **result,
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "created_at_utc": created_at,
    }
    write_outputs(result, status, judgment, external_status, next_action, created_at)
    upsert_ledgers(result, status, judgment, external_status, next_action)
    update_docs(status, judgment, next_action, len(result.get("mt5_kpi_records", [])), len(result.get("attempts", [])))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute or prepare Stage270 aggressive probe MT5 signal replay.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--tier-scopes", default="tier_a,tier_b")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    result = run(parse_args(argv or sys.argv[1:]))
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "judgment": result["judgment"],
                "external_verification_status": result["external_verification_status"],
                "attempt_count": len(result.get("attempts", [])),
                "execution_result_count": len(result.get("execution_results", [])),
                "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
                "selected_candidate": result.get("selected_candidate"),
                "onnx_readiness": result.get("onnx_readiness"),
                "goal_achieve": result.get("goal_achieve"),
                "next_action": result.get("next_action"),
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
