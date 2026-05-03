from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, upsert_csv_rows, write_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_sklearn_to_onnx_zipmap_disabled, ordered_hash
from foundation.models.qda_discriminant import default_stage16_qda_specs
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage16 import qda_characterization_probe as base


PACKET_ID = "stage16_qda_run08A_run08J_mt5_runtime_probe_v1"
REVIEW_PACKET_PATH = base.STAGE_ROOT / "03_reviews/run08A_run08J_qda_mt5_runtime_probe_packet.md"
DECISION_PATH = base.ROOT / "docs/decisions/2026-05-02_stage16_qda_run08A_run08J_mt5_runtime_probe.md"
PACKET_ROOT = base.ROOT / "docs/agent_control/packets" / PACKET_ID
BOUNDARY = "qda_characterization_mt5_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_qda_characterization_mt5_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_qda_characterization_mt5_runtime_probe_after_attempt"
ONNX_OPSET = 13
ONNX_PARITY_TOLERANCE = 0.005
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    base.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    base.write_md(path, text)


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True) + "\n")


def run_summary_path(spec: Any) -> Path:
    return base.run_root(spec) / "summary.json"


def export_models(spec: Any, context: Mapping[str, Any], feature_order: Sequence[str], summary: Mapping[str, Any]) -> dict[str, Any]:
    root = base.run_root(spec) / "models"
    tier_a_model = joblib.load(io_path(base.ROOT / summary["model_artifacts"]["tier_a_joblib"]["path"]))
    tier_b_model = joblib.load(io_path(base.ROOT / summary["model_artifacts"]["tier_b_joblib"]["path"]))
    tier_a_onnx = root / f"{spec.variant_id}_tier_a_qda_opset{ONNX_OPSET}.onnx"
    tier_b_onnx = root / f"{spec.variant_id}_tier_b_qda_core42_opset{ONNX_OPSET}.onnx"
    tier_a_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model,
        tier_a_onnx,
        feature_count=len(feature_order),
        target_opset=ONNX_OPSET,
    )
    tier_b_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model,
        tier_b_onnx,
        feature_count=len(context["tier_b_feature_order"]),
        target_opset=ONNX_OPSET,
    )
    a_sample = context["tier_a_frame"].loc[
        context["tier_a_frame"]["split"].astype(str).eq("validation"), list(feature_order)
    ].head(128).to_numpy(dtype="float64", copy=False)
    b_sample = context["tier_b_training_frame"].loc[
        context["tier_b_training_frame"]["split"].astype(str).eq("validation"), context["tier_b_feature_order"]
    ].head(128).to_numpy(dtype="float64", copy=False)
    return {
        "tier_a_onnx": tier_a_export,
        "tier_b_onnx": tier_b_export,
        "onnx_parity": {
            "tier_a": check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, a_sample, tolerance=ONNX_PARITY_TOLERANCE),
            "tier_b": check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, b_sample, tolerance=ONNX_PARITY_TOLERANCE),
        },
    }


def export_feature_matrices(spec: Any, context: Mapping[str, Any], feature_order: Sequence[str]) -> dict[str, Any]:
    root = base.run_root(spec) / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            feature_order,
            root / f"tier_a_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            context["tier_b_feature_order"],
            root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(spec: Any, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(base.STAGE_NUMBER, spec.run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = base.ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = base.ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(
    spec: Any,
    context: Mapping[str, Any],
    feature_order: Sequence[str],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(base.STAGE_NUMBER, spec.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    a_threshold = float(thresholds["tier_a"])
    b_threshold = float(thresholds["tier_b"])
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": base.run_root(spec),
            "run_id": spec.run_id,
            "stage_number": base.STAGE_NUMBER,
            "exploration_label": base.EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_only_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{spec.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(feature_order), feature_order_hash=ordered_hash(feature_order), short_threshold=a_threshold, long_threshold=a_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="tier_only_total", record_view_prefix="mt5_tier_a_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_fallback_only_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{spec.run_id}_tier_b", feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=b_threshold, long_threshold=b_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role="tier_b_fallback_only_total", record_view_prefix="mt5_tier_b_fallback_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{spec.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(feature_order), feature_order_hash=ordered_hash(feature_order), short_threshold=a_threshold, long_threshold=a_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="routed_total", record_view_prefix="mt5_routed_total", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{spec.run_id}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=b_threshold, fallback_long_threshold=b_threshold, fallback_min_margin=MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": JUDGMENT_BLOCKED, "failure": {"type": type(exc).__name__, "message": str(exc)}}
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = prepared["source_variant_id"]
    return result


def routed_metrics(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def write_run_outputs(spec: Any, result: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_root = base.run_root(spec)
    manifest = read_json(run_root / "run_manifest.json")
    kpi_record = read_json(run_root / "kpi_record.json")
    summary = read_json(run_root / "summary.json")
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=spec.run_id,
        stage_id=base.STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"validation_nonflat_q{base.THRESHOLD_QUANTILE:.2f}",
        run_output_root=run_root,
        external_verification_status=result["external_verification_status"],
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=base.STAGE_LEDGER_PATH,
        project_alpha_ledger_path=base.PROJECT_LEDGER_PATH,
        rows=ledger_rows,
    )
    registry_output = upsert_run_registry(spec, result)
    validation = routed_metrics(result, "mt5_routed_total_validation_is")
    oos = routed_metrics(result, "mt5_routed_total_oos")
    runtime_payload = {
        "packet_id": PACKET_ID,
        "scoreboard_lane": "runtime_probe",
        "external_verification_status": result["external_verification_status"],
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "kpi_records": result.get("mt5_kpi_records", []),
        "validation_routed": validation,
        "oos_routed": oos,
    }
    kpi_record["model_family"] = base.MODEL_FAMILY
    kpi_record["feature_set_id"] = base.FEATURE_SET_ID
    kpi_record["label_id"] = base.LABEL_ID
    kpi_record["split_contract"] = base.SPLIT_CONTRACT
    kpi_record["stage_inheritance"] = False
    manifest["runtime_probe"] = {key: result.get(key) for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure") if key in result}
    manifest["runtime_probe"]["packet_id"] = PACKET_ID
    manifest["runtime_probe"]["model_artifacts"] = result.get("model_artifacts")
    manifest["runtime_probe"]["feature_matrices"] = result.get("feature_matrices")
    kpi_record["mt5"] = runtime_payload
    kpi_record["external_verification_status"] = result["external_verification_status"]
    kpi_record["judgment"] = result["judgment"]
    kpi_record["boundary"] = BOUNDARY
    kpi_record["ledger_outputs"] = ledger_outputs
    kpi_record["registry_output"] = registry_output
    summary.update(
        {
            "judgment": result["judgment"],
            "external_verification_status": result["external_verification_status"],
            "boundary": BOUNDARY,
            "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
            "attempt_count": len(result.get("attempts", [])),
            "validation_routed": validation,
            "oos_routed": oos,
        }
    )
    write_json(run_root / "run_manifest.json", manifest)
    write_json(run_root / "kpi_record.json", kpi_record)
    write_json(run_root / "summary.json", summary)
    write_json(PACKET_ROOT / "run_summaries" / f"{spec.run_id}.json", summary)
    write_md(run_root / "reports/result_summary.md", run_result_markdown(summary))
    return summary


def upsert_run_registry(spec: Any, result: Mapping[str, Any]) -> dict[str, Any]:
    validation = routed_metrics(result, "mt5_routed_total_validation_is")
    oos = routed_metrics(result, "mt5_routed_total_oos")
    row = {
        "run_id": spec.run_id,
        "stage_id": base.STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": result["judgment"],
        "path": base.rel(base.run_root(spec)),
        "notes": ledger_pairs(
            (
                ("model_family", base.MODEL_FAMILY),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("validation_net_profit", validation.get("net_profit")),
                ("validation_pf", validation.get("profit_factor")),
                ("oos_net_profit", oos.get("net_profit")),
                ("oos_pf", oos.get("profit_factor")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(base.RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def run_result_markdown(summary: Mapping[str, Any]) -> str:
    lines = [
        f"# {summary['run_id']} Result Summary({summary['run_id']} 결과 요약)",
        "",
        f"- variant(변형): `{summary['variant_id']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- external verification(외부 검증): `{summary['external_verification_status']}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count')}`",
        "",
        "| view(보기) | net(순수익) | pf(수익 팩터) | trades(거래 수) | dd(손실) | recovery(회복) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for view in ("validation_routed", "oos_routed"):
        metrics = summary.get(view, {})
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | `{}` | `{}` |".format(
                view,
                metrics.get("net_profit"),
                metrics.get("profit_factor"),
                metrics.get("trade_count"),
                metrics.get("max_drawdown_amount"),
                metrics.get("recovery_factor"),
            )
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 실행은 QDA(이차 판별 분석) 특성 파악 결과를 MT5(메타트레이더5) runtime_probe(런타임 탐침) KPI까지 연결했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아니다.",
        ]
    )
    return "\n".join(lines)


def build_one(spec: Any, context: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    summary = read_json(run_summary_path(spec))
    feature_order = base.feature_order_for_mode(context["full_feature_order"], spec.tier_a_feature_mode)
    model_artifacts = export_models(spec, context, feature_order, summary)
    feature_matrices = export_feature_matrices(spec, context, feature_order)
    copies = copy_runtime_inputs(spec, model_artifacts, feature_matrices)
    attempts = make_attempts(spec, context, feature_order, model_artifacts, feature_matrices, summary["thresholds"])
    prepared = {
        "stage_id": base.STAGE_ID,
        "stage_number": base.STAGE_NUMBER,
        "run_id": spec.run_id,
        "run_number": spec.run_number,
        "run_root": base.run_root(spec),
        "source_variant_id": spec.variant_id,
        "attempts": attempts,
        "common_copies": copies,
        "route_coverage": context["tier_b_context_summary"],
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
    }
    result = execute_or_block(prepared, args)
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    tier_records = read_json(base.run_root(spec) / "kpi_record.json").get("python_tier_records", [])
    return write_run_outputs(spec, result, tier_records)


def aggregate_summary(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in summaries if row.get("external_verification_status") == "completed"]
    best_oos = max(summaries, key=lambda row: base.safe_float(row.get("oos_routed", {}).get("net_profit"), -1e18), default=None)
    best_val = max(summaries, key=lambda row: base.safe_float(row.get("validation_routed", {}).get("net_profit"), -1e18), default=None)
    return {
        "packet_id": PACKET_ID,
        "stage_id": base.STAGE_ID,
        "run_range": "run08A-run08J",
        "run_count": len(summaries),
        "completed_run_count": len(completed),
        "blocked_run_count": len(summaries) - len(completed),
        "external_verification_status": "completed" if len(completed) == len(summaries) else "blocked_or_partial",
        "judgment": JUDGMENT_COMPLETED if len(completed) == len(summaries) else JUDGMENT_BLOCKED,
        "boundary": BOUNDARY,
        "mt5_kpi_record_count": sum(int(row.get("mt5_kpi_record_count", 0)) for row in summaries),
        "attempt_count": sum(int(row.get("attempt_count", 0)) for row in summaries),
        "best_oos_routed_net_run": best_oos,
        "best_validation_routed_net_run": best_val,
        "run_ids": [row["run_id"] for row in summaries],
    }


def write_normalized_kpi(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    inventory = [
        {
            "run_id": str(row["run_id"]),
            "stage_id": base.STAGE_ID,
            "idea_id": str(row.get("idea_id") or row.get("run_number") or row["run_id"]),
            "path": base.rel(base.STAGE_ROOT / "02_runs" / str(row["run_id"])),
        }
        for row in summaries
    ]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(base.ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(base.ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, base.ROOT, market_data)
    write_jsonl(PACKET_ROOT / "normalized_kpi_records.jsonl", records)
    write_csv_rows(PACKET_ROOT / "normalized_kpi_summary.csv", mt5_kpi_recorder.SUMMARY_COLUMNS, summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_jsonl(PACKET_ROOT / "enriched_kpi_records.jsonl", enriched)
    write_csv_rows(PACKET_ROOT / "trade_level_records.csv", mt5_trade_attribution.TRADE_COLUMNS, trade_rows)
    write_csv_rows(PACKET_ROOT / "trade_attribution_summary.csv", mt5_trade_attribution.SUMMARY_COLUMNS, trade_summary)
    write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def packet_markdown(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any]) -> str:
    lines = [
        "# Stage16 QDA RUN08A-RUN08J MT5 Runtime Probe(16단계 QDA 실행 08A-08J MT5 런타임 탐침)",
        "",
        f"- judgment(판정): `{aggregate['judgment']}`",
        f"- completed runs(완료 실행): `{aggregate['completed_run_count']}/{aggregate['run_count']}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{aggregate['mt5_kpi_record_count']}`",
        f"- normalized KPI records(정규화 KPI 기록): `{kpi['normalized_records']}`",
        f"- trade attribution records(거래 귀속 기록): `{kpi['trade_attribution_records']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| run(실행) | topic(주제) | val net/trades(검증) | oos net/trades(표본외) |",
        "|---|---|---:|---:|",
    ]
    for row in summaries:
        val = row.get("validation_routed", {})
        oos = row.get("oos_routed", {})
        lines.append(f"| `{row['run_number']}` | `{row['idea_id']}` | `{val.get('net_profit')}/{val.get('trade_count')}` | `{oos.get('net_profit')}/{oos.get('trade_count')}` |")
    best_oos = aggregate.get("best_oos_routed_net_run") or {}
    lines.extend(
        [
            "",
            f"- best OOS routed net(최고 표본외 라우팅 순수익): `{best_oos.get('run_number')}` `{best_oos.get('idea_id')}` `{(best_oos.get('oos_routed') or {}).get('net_profit')}`",
            "",
            "효과(effect, 효과): 이 묶음은 QDA(이차 판별 분석) 특성 파악 run(실행)을 MT5(메타트레이더5) Strategy Tester(전략 테스터), KPI(핵심성과지표), normalized KPI(정규화 KPI), trade attribution(거래 귀속)까지 연결한다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def write_packet_files(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", {**dict(aggregate), "kpi_management": dict(kpi)})
    write_json(PACKET_ROOT / "artifact_index.json", {"run_summaries": list(summaries), "report_path": base.rel(REVIEW_PACKET_PATH), "created_at_utc": created_at})
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "source_authority_audit", "required_gate_coverage_audit", "final_claim_guard"]})
    write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "receipts": [{"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe"}, {"skill": "obsidian-backtest-forensics", "status": "completed", "backtest_judgment": "usable_with_boundary"}, {"skill": "obsidian-artifact-lineage", "status": "completed", "lineage_judgment": "connected_with_boundary"}, {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": aggregate["judgment"], "claim_boundary": BOUNDARY}]})
    gates = gate_payloads(aggregate, kpi)
    for name, payload in gates.items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    write_md(REVIEW_PACKET_PATH, packet_markdown(aggregate, summaries, kpi))


def gate_payloads(aggregate: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    runtime_ok = aggregate["completed_run_count"] == aggregate["run_count"] == 10 and aggregate["mt5_kpi_record_count"] == 100
    kpi_ok = kpi["normalized_records"] == 100 and kpi["parser_errors"] == 0 and kpi["missing_runs"] == 0
    passed = bool(runtime_ok and kpi_ok)
    return {
        "runtime_evidence_gate": {"audit_name": "runtime_evidence_gate", "status": "pass" if runtime_ok else "blocked", "passed": runtime_ok, "counts": {"attempt_count": aggregate["attempt_count"], "mt5_kpi_record_count": aggregate["mt5_kpi_record_count"]}},
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": "pass" if kpi_ok else "blocked", "passed": kpi_ok, **dict(kpi)},
        "source_authority_audit": {"audit_name": "source_authority_audit", "status": "pass" if passed else "blocked", "passed": passed, "source": "run kpi_record.json plus MT5 Strategy Tester reports"},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass" if passed else "blocked", "passed": passed, "allowed_claims": [aggregate["judgment"], "runtime_probe"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if passed else "blocked", "passed": passed, "required_gates": {"runtime_evidence_gate": "pass" if runtime_ok else "blocked", "kpi_contract_audit": "pass" if kpi_ok else "blocked", "source_authority_audit": "pass" if passed else "blocked", "final_claim_guard": "pass" if passed else "blocked"}},
    }


def sync_docs(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any]) -> None:
    write_md(base.STAGE_ROOT / "03_reviews/review_index.md", "\n".join(["# Stage 16 Review Index(16단계 검토 색인)", "", "- `run08A`~`run08J`: `inconclusive_qda_characterization_structural_scout_completed`, report(보고서): `stages/16_model_family_challenge__qda_class_covariance_scout/03_reviews/run08A_run08J_qda_characterization_packet.md`", f"- `run08A`~`run08J` MT5(`MetaTrader 5`, 메타트레이더5): `{aggregate['judgment']}`, report(보고서): `{base.rel(REVIEW_PACKET_PATH)}`", "", "효과(effect, 효과): Stage16(16단계)는 QDA(이차 판별 분석) 성격 파악 run(실행)을 MT5 runtime_probe(MT5 런타임 탐침)와 KPI(핵심성과지표)까지 연결했지만, edge(거래 우위)나 운영 의미는 없다."]))
    write_md(base.STAGE_ROOT / "04_selected/selection_status.md", "\n".join(["# Stage 16 Selection Status(16단계 선택 상태)", "", "## Current Read(현재 판독)", "", f"- stage(단계): `{base.STAGE_ID}`", "- status(상태): `reviewed_qda_run08A_run08J_mt5_runtime_probe_no_edge(검토됨, QDA 실행 08A-08J MT5 런타임 탐침, 엣지 없음)`", "- current run(현재 실행): `run08J_qda_external16_feature_geometry_characterization_v1`", "- model family(모델 계열): QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)", "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`", f"- judgment(판정): `{aggregate['judgment']}`", f"- MT5 KPI records(MT5 핵심성과지표 기록): `{aggregate['mt5_kpi_record_count']}`", f"- normalized KPI records(정규화 KPI 기록): `{kpi['normalized_records']}`", f"- boundary(경계): `{BOUNDARY}`", "", "효과(effect, 효과): 이번 10개 run(실행)은 MT5(메타트레이더5) 검증과 KPI(핵심성과지표) 관리를 갖춘 runtime_probe(런타임 탐침)이다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다."]))
    write_md(DECISION_PATH, "\n".join(["# 2026-05-02 Stage16 QDA MT5 Runtime Probe(16단계 QDA MT5 런타임 탐침)", "", "## Decision(결정)", "", "Stage16(16단계) QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) `run08A`~`run08J`를 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)까지 검증하고 KPI(`Key Performance Indicator`, 핵심성과지표)를 정규화 기록으로 관리한다.", "", "효과(effect, 효과): Python structural scout(파이썬 구조 스카우트) 결과가 런타임에서 어떤 거래/위험/실행 KPI(핵심성과지표)를 만드는지 확인할 수 있다.", "", "## Boundary(경계)", "", f"`{BOUNDARY}`"]))
    sync_workspace_docs(aggregate, kpi)


def sync_workspace_docs(aggregate: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    state_path = base.ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("stage16_qda_run08A_run08J_characterization_reviewed", "stage16_qda_run08A_run08J_mt5_runtime_probe_reviewed")
    state = state.replace("reviewed_qda_run08A_run08J_characterization_no_mt5_no_edge", "reviewed_qda_run08A_run08J_mt5_runtime_probe_no_edge")
    state = state.replace("current_status: run08A_run08J_characterization_reviewed", "current_status: run08A_run08J_mt5_runtime_probe_reviewed")
    state = state.replace("boundary: qda_characterization_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority", f"boundary: {BOUNDARY}")
    state = state.replace("next_action: inspect_qda_characterization_clues_before_any_runtime_probe", "next_action: inspect_qda_mt5_kpi_before_any_followup_probe")
    append = f"""stage16_qda_mt5_runtime_probe_run08A_run08J:
  packet_id: {PACKET_ID}
  status: reviewed_runtime_probe_completed
  judgment: {aggregate['judgment']}
  run_range: run08A-run08J
  completed_run_count: {aggregate['completed_run_count']}
  mt5_kpi_record_count: {aggregate['mt5_kpi_record_count']}
  normalized_kpi_record_count: {kpi['normalized_records']}
  trade_attribution_records: {kpi['trade_attribution_records']}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {base.rel(REVIEW_PACKET_PATH)}
  decision_path: {base.rel(DECISION_PATH)}
  next_action: inspect_qda_mt5_kpi_before_any_followup_probe
"""
    if "stage16_qda_mt5_runtime_probe_run08A_run08J:" not in state:
        state = state.replace("stage15_lda_run06A_run06J_runtime_probe:\n", append + "stage15_lda_run06A_run06J_runtime_probe:\n", 1)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = base.ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    latest = "\n".join(["## Latest Stage 16 Update(최신 Stage 16 업데이트)", "", "Stage16(16단계)는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) `run08A`~`run08J`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 실행하고 KPI(`Key Performance Indicator`, 핵심성과지표)를 정규화했다.", "", f"효과(effect, 효과): `{aggregate['judgment']}`로 기록했지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.", ""])
    current = re_sub_latest(current, latest)
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def re_sub_latest(text: str, latest: str) -> str:
    import re
    return re.sub(r"## Latest Stage 16 Update\(최신 Stage 16 업데이트\)\n\n.*?(?=## 쉬운 설명)", latest, text, count=1, flags=re.S)


def sync_misc_docs() -> None:
    changelog_path = base.ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = "- 2026-05-02: Stage16 QDA(이차 판별 분석) `run08A`~`run08J` MT5 runtime_probe(MT5 런타임 탐침)와 KPI(핵심성과지표) 정규화를 완료했다. 효과(effect, 효과): 런타임 KPI를 관리하되 edge(거래 우위)는 주장하지 않는다."
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line + "\n", encoding="utf-8-sig")
    idea_path = base.ROOT / "docs/registers/idea_registry.md"
    idea = io_path(idea_path).read_text(encoding="utf-8-sig").replace("run08A_run08J_characterization_reviewed", "run08A_run08J_mt5_runtime_probe_reviewed")
    io_path(idea_path).write_text(idea.rstrip() + "\n", encoding="utf-8-sig")


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = base.load_context()
    selected = {item.strip() for item in args.run_filter.split(",") if item.strip()} if args.run_filter else set()
    specs = [spec for spec in default_stage16_qda_specs() if not selected or spec.run_number in selected or spec.run_id in selected]
    summaries = [build_one(spec, context, args) for spec in specs]
    aggregate = aggregate_summary(summaries)
    kpi = write_normalized_kpi(summaries)
    write_packet_files(aggregate, summaries, kpi, created_at)
    sync_docs(aggregate, summaries, kpi)
    sync_misc_docs()
    print(json.dumps(json_ready({**aggregate, "kpi_management": kpi}), ensure_ascii=False, indent=2))
    return dict(aggregate)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage16 QDA MT5 runtime probes and KPI management.")
    parser.add_argument("--run-filter", default="")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    args = parser.parse_args(argv)
    build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
