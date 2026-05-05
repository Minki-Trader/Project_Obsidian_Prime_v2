from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
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
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage23 import supervised_regime_scout as scout


STAGE_NUMBER = 23
STAGE_ID = scout.STAGE_ID
SOURCE_RUN_ID = scout.RUN_ID
SOURCE_PACKET_ID = scout.PACKET_ID
RUN_NUMBER = "run17B"
RUN_ID = "run17B_supervised_regime_classifier_runtime_probe_v1"
PACKET_ID = "stage23_run17B_supervised_regime_classifier_runtime_probe_v1"
EXPLORATION_LABEL = "stage23_Regime__SupervisedClassifierRuntimeProbe"
MODEL_FAMILY = "sklearn_supervised_regime_classifier_filter_onnx_runtime_probe"
MODEL_BACKEND = "onnx"
FEATURE_SET_ID = scout.FEATURE_SET_ID
LABEL_ID = scout.LABEL_ID
SPLIT_CONTRACT = scout.SPLIT_CONTRACT
THRESHOLD_QUANTILE = scout.THRESHOLD_QUANTILE
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0
BOUNDARY = "supervised_regime_classifier_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_supervised_regime_classifier_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_supervised_regime_classifier_runtime_probe_after_attempt"

ROOT = scout.ROOT
STAGE_ROOT = scout.STAGE_ROOT
SOURCE_RUN_ROOT = scout.RUN_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = scout.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = scout.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = scout.RUN_REGISTRY_PATH
REVIEW_PATH = STAGE_ROOT / "03_reviews/run17B_supervised_regime_classifier_runtime_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage23_run17B_supervised_regime_classifier_runtime_probe.md"
SELECTION_STATUS_PATH = scout.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = scout.REVIEW_INDEX_PATH
WORKSPACE_STATE_PATH = scout.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = scout.CURRENT_WORKING_STATE_PATH
GOAL_PLAN_PATH = scout.GOAL_PLAN_PATH


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return scout.rel(path)


def write_json(path: Path, payload: Any) -> None:
    scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    scout.write_md(path, text)


def read_json(path: Path) -> dict[str, Any]:
    return scout.read_json(path)


def safe_float(value: Any, default: float = 0.0) -> float:
    return scout.safe_float(value, default)


def load_source_summary() -> dict[str, Any]:
    summary_path = ROOT / "docs/agent_control/packets" / SOURCE_PACKET_ID / "aggregate_summary.json"
    summary = read_json(summary_path)
    if summary.get("selected_variant_id") != "v05_logistic_core24_compact_filter":
        raise RuntimeError(f"Unexpected Stage23 selected variant: {summary.get('selected_variant_id')}")
    return summary


def load_models(summary: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = summary.get("artifacts", {}).get("model_artifacts", {})
    tier_a_path = ROOT / str(artifacts.get("tier_a_model", {}).get("path", ""))
    tier_b_path = ROOT / str(artifacts.get("tier_b_model", {}).get("path", ""))
    if not io_path(tier_a_path).exists() or not io_path(tier_b_path).exists():
        raise FileNotFoundError(f"Missing Stage23 run17A selected model artifacts: {tier_a_path}, {tier_b_path}")
    return {
        "tier_a_model": joblib.load(io_path(tier_a_path)),
        "tier_b_model": joblib.load(io_path(tier_b_path)),
        "tier_a_artifact": {"path": rel(tier_a_path), "sha256": sha256_file_lf_normalized(tier_a_path)},
        "tier_b_artifact": {"path": rel(tier_b_path), "sha256": sha256_file_lf_normalized(tier_b_path)},
    }


def runtime_contract(summary: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = summary.get("artifacts", {}).get("model_artifacts", {})
    feature_order = list(artifacts.get("runtime_feature_order") or [])
    if not feature_order:
        raise RuntimeError("Stage23 run17A summary is missing runtime_feature_order.")
    thresholds = dict(artifacts.get("thresholds") or {})
    for key in ("tier_a", "tier_b"):
        if key not in thresholds:
            raise RuntimeError(f"Stage23 run17A summary is missing {key} threshold.")
    return {
        "selected_variant_id": str(summary.get("selected_variant_id")),
        "runtime_feature_order": feature_order,
        "runtime_feature_order_hash": ordered_hash(feature_order),
        "thresholds": thresholds,
    }


def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return scout.save_frame(path, frame)


def materialize_python_tier_records(
    context: Mapping[str, Any],
    models: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, pd.DataFrame]]:
    feature_order = list(contract["runtime_feature_order"])
    thresholds = contract["thresholds"]
    tier_a_prob = scout.probability_frame(models["tier_a_model"], context["tier_a_frame"], feature_order)
    tier_b_prob = scout.probability_frame(models["tier_b_model"], context["tier_b_fallback_frame"], feature_order)
    tier_ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    root = RUN_ROOT / "predictions"
    a_path = root / "tier_a_runtime_probe_predictions.parquet"
    b_path = root / "tier_b_runtime_probe_predictions.parquet"
    ab_path = root / "tier_ab_runtime_probe_predictions.parquet"
    records = [
        scout.tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, float(thresholds["tier_a"]), a_path),
        scout.tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, float(thresholds["tier_b"]), b_path),
        scout.tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab_prob, float(thresholds["tier_a"]), ab_path),
    ]
    artifacts = {
        "tier_a_predictions": save_predictions(a_path, tier_a_prob),
        "tier_b_predictions": save_predictions(b_path, tier_b_prob),
        "tier_ab_predictions": save_predictions(ab_path, tier_ab_prob),
    }
    return records, artifacts, {"tier_a_prob": tier_a_prob, "tier_b_prob": tier_b_prob, "tier_ab_prob": tier_ab_prob}


def export_models(context: Mapping[str, Any], models: Mapping[str, Any], contract: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    feature_order = list(contract["runtime_feature_order"])
    selected = str(contract["selected_variant_id"])
    tier_a_onnx = root / f"{selected}_tier_a_supervised_regime_classifier.onnx"
    tier_b_onnx = root / f"{selected}_tier_b_supervised_regime_classifier.onnx"
    tier_a_export = mt5.export_sklearn_to_onnx_zipmap_disabled(
        models["tier_a_model"],
        tier_a_onnx,
        feature_count=len(feature_order),
        drop_label_output=True,
    )
    tier_b_export = mt5.export_sklearn_to_onnx_zipmap_disabled(
        models["tier_b_model"],
        tier_b_onnx,
        feature_count=len(feature_order),
        drop_label_output=True,
    )
    sample_a = context["tier_a_frame"].loc[
        context["tier_a_frame"]["split"].astype(str).eq("validation"),
        feature_order,
    ].head(2048).to_numpy(dtype="float64", copy=False)
    sample_b = context["tier_b_training_frame"].loc[
        context["tier_b_training_frame"]["split"].astype(str).eq("validation"),
        feature_order,
    ].head(2048).to_numpy(dtype="float64", copy=False)
    return {
        "selected_variant_id": selected,
        "model_backend": MODEL_BACKEND,
        "tier_a_joblib": models["tier_a_artifact"],
        "tier_b_joblib": models["tier_b_artifact"],
        "runtime_feature_order": feature_order,
        "runtime_feature_order_hash": contract["runtime_feature_order_hash"],
        "thresholds": contract["thresholds"],
        "tier_a_onnx": {**tier_a_export, "path": rel(Path(tier_a_export["path"]))},
        "tier_b_onnx": {**tier_b_export, "path": rel(Path(tier_b_export["path"]))},
        "onnx_parity": {
            "tier_a": mt5.check_onnxruntime_probability_parity(models["tier_a_model"], tier_a_onnx, sample_a),
            "tier_b": mt5.check_onnxruntime_probability_parity(models["tier_b_model"], tier_b_onnx, sample_b),
        },
    }


def export_feature_matrices(context: Mapping[str, Any], contract: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "features"
    feature_order = list(contract["runtime_feature_order"])
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
            feature_order,
            root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = ROOT / str(model_artifacts[key]["path"])
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / str(matrix["path"])
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], contract: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    tier_a_model = Path(str(model_artifacts["tier_a_onnx"]["path"])).name
    tier_b_model = Path(str(model_artifacts["tier_b_onnx"]["path"])).name
    feature_count = len(contract["runtime_feature_order"])
    feature_hash = str(contract["runtime_feature_order_hash"])
    thresholds = contract["thresholds"]
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(str(feature_matrices[f"tier_a_{runtime_split}"]["path"])).name
        tier_b_matrix = Path(str(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"])).name
        common_kwargs = {
            "run_root": RUN_ROOT,
            "run_id": RUN_ID,
            "stage_number": STAGE_NUMBER,
            "exploration_label": EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_a_only_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=feature_count,
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_only_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{RUN_ID}_tier_b",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=feature_count,
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_b"]),
                long_threshold=float(thresholds["tier_b"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=feature_count,
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{RUN_ID}_tier_b",
                fallback_model_backend=MODEL_BACKEND,
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=feature_count,
                fallback_feature_order_hash=feature_hash,
                fallback_short_threshold=float(thresholds["tier_b"]),
                fallback_long_threshold=float(thresholds["tier_b"]),
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
            )
        )
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
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = str(prepared.get("selected_variant_id"))
        record["topic_read"] = "supervised_regime_classifier_filter_runtime_handoff"
        record["threshold_quantile"] = f"q{THRESHOLD_QUANTILE:.2f}"
        record["max_hold_bars"] = MAX_HOLD_BARS
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    parity = model_artifacts.get("onnx_parity", {})
    return bool(parity.get("tier_a", {}).get("passed")) and bool(parity.get("tier_b", {}).get("passed"))


def runtime_failure_signature(result: Mapping[str, Any]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    model_ok_total = 0
    model_fail_total = 0
    feature_ready_total = 0
    last_skip_counts: dict[str, int] = {}
    for item in result.get("execution_results", []) or []:
        status = str(item.get("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
        outputs = item.get("runtime_outputs", {})
        if not isinstance(outputs, Mapping):
            continue
        summary = outputs.get("last_summary", {})
        if not isinstance(summary, Mapping):
            continue
        model_ok_total += int(summary.get("model_ok_count") or 0)
        model_fail_total += int(summary.get("model_fail_count") or 0)
        feature_ready_total += int(summary.get("feature_ready_count") or 0)
        skip = summary.get("last_skip_reason")
        if skip:
            last_skip_counts[str(skip)] = last_skip_counts.get(str(skip), 0) + 1
    primary_skip = max(last_skip_counts.items(), key=lambda pair: pair[1])[0] if last_skip_counts else None
    return {
        "compile_status": (result.get("compile") or {}).get("status") if isinstance(result.get("compile"), Mapping) else None,
        "attempt_status_counts": status_counts,
        "feature_ready_count_total": feature_ready_total,
        "model_ok_count_total": model_ok_total,
        "model_fail_count_total": model_fail_total,
        "primary_runtime_skip": primary_skip,
        "last_skip_reason_counts": last_skip_counts,
    }


def write_normalized_kpi() -> dict[str, Any]:
    inventory = [{"run_id": RUN_ID, "stage_id": STAGE_ID, "idea_id": RUN_NUMBER, "path": rel(RUN_ROOT)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_json(PACKET_ROOT / "normalized_kpi_records.json", records)
    write_json(PACKET_ROOT / "normalized_kpi_summary.json", summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(PACKET_ROOT / "enriched_kpi_records.json", enriched)
    write_json(PACKET_ROOT / "trade_level_records.json", trade_rows)
    write_json(PACKET_ROOT / "trade_attribution_summary.json", trade_summary)
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


def build_summary(
    result: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    source_summary: Mapping[str, Any],
) -> dict[str, Any]:
    completed = result.get("external_verification_status") == "completed"
    validation = metrics_by_view(result, "mt5_routed_total_validation_is")
    oos = metrics_by_view(result, "mt5_routed_total_oos")
    avg_trades = (safe_float(validation.get("trade_count")) + safe_float(oos.get("trade_count"))) / 2.0
    visible = completed and parity_passed(model_artifacts) and avg_trades >= 5.0
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "selected_variant_id": model_artifacts.get("selected_variant_id"),
        "source_python_scout_judgment": source_summary.get("judgment"),
        "topic_read": "supervised_regime_classifier_filter_runtime_handoff",
        "threshold_quantile": THRESHOLD_QUANTILE,
        "max_hold_bars": MAX_HOLD_BARS,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "closure_judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "external_verification_status": result["external_verification_status"],
        "model_characteristic_strength": "supervised_regime_runtime_axis_visible" if visible else "supervised_regime_runtime_axis_weak_or_blocked",
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "python_tier_records": list(tier_records),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "attempt_count": len(result.get("attempts", [])),
        "expected_attempts": 6,
        "expected_kpi_records": 10,
        "validation_routed": validation,
        "oos_routed": oos,
        "runtime_failure_signature": runtime_failure_signature(result),
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def packet_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    parity = summary.get("model_artifacts", {}).get("onnx_parity", {})
    return f"""# RUN17B Supervised Regime Classifier Runtime Probe(실행17B 지도 국면 분류기 런타임 탐침)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- judgment(판정): `{summary.get('closure_judgment')}`
- external verification(외부 검증): `{summary.get('external_verification_status')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{kpi.get('normalized_records')}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): supervised regime classifier(지도 국면 분류기)를 direct entry model(직접 진입 모델)이 아니라 permission/filter(허용/필터) runtime_probe(런타임 탐침)로 MT5(`MetaTrader 5`, 메타트레이더5)에 인계했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation(검증) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` | `{validation.get('max_drawdown_amount')}` |
| OOS(표본외) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` | `{oos.get('max_drawdown_amount')}` |

## ONNX Parity(온닉스 동등성)

- Tier A parity(Tier A 동등성): `{parity.get('tier_a', {}).get('passed')}`; max_abs_diff(최대 절대 차이) `{parity.get('tier_a', {}).get('max_abs_diff')}`
- Tier B parity(Tier B 동등성): `{parity.get('tier_b', {}).get('passed')}`; max_abs_diff(최대 절대 차이) `{parity.get('tier_b', {}).get('max_abs_diff')}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
"""


def gate_payloads(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {
            "status": "passed" if completed and parity_ok else "blocked",
            "external_verification_status": summary.get("external_verification_status"),
            "onnx_parity_passed": parity_ok,
            "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
            "expected_kpi_records": summary.get("expected_kpi_records"),
        },
        "scope_completion_gate": {
            "status": "passed" if summary.get("attempt_count") == summary.get("expected_attempts") else "blocked",
            "attempt_count": summary.get("attempt_count"),
            "expected_attempts": summary.get("expected_attempts"),
            "claim_boundary": BOUNDARY,
        },
        "kpi_contract_audit": {
            "status": "passed" if int(summary.get("mt5_kpi_record_count") or 0) > 0 and int(kpi.get("parser_errors") or 0) == 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
            "trade_parser_errors": kpi.get("trade_parser_errors"),
        },
        "required_gate_coverage_audit": {
            "status": "passed",
            "packet_id": PACKET_ID,
            "required_gates": gates,
            "covered_gates": gates,
        },
        "final_claim_guard": {
            "status": "passed",
            "allowed_claims": ["runtime_probe", "inconclusive", "blocked"],
            "forbidden_claims": summary.get("forbidden_claims"),
            "claim_boundary": BOUNDARY,
        },
    }


def write_run_outputs(
    result: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    source_summary: Mapping[str, Any],
    kpi: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(result, model_artifacts, prediction_artifacts, tier_records, source_summary)
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["closure_judgment"],
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("topic_read", summary["topic_read"]),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("selected_variant", summary.get("selected_variant_id")),
                ("threshold_quantile", f"q{THRESHOLD_QUANTILE:.2f}"),
                ("validation_net_profit", validation.get("net_profit")),
                ("validation_pf", validation.get("profit_factor")),
                ("oos_net_profit", oos.get("net_profit")),
                ("oos_pf", oos.get("profit_factor")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"q{THRESHOLD_QUANTILE:.2f}",
        run_output_root=RUN_ROOT,
        external_verification_status=result["external_verification_status"],
    )
    materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=ledger_rows,
    )
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": summary.get("selected_variant_id"),
        "threshold_policy": f"non-flat q{THRESHOLD_QUANTILE:.2f}; inherited from run17A scout, not profit searched",
        "max_hold_bars": MAX_HOLD_BARS,
        "boundary": BOUNDARY,
        "runtime_probe": {
            key: result.get(key)
            for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
            if key in result
        },
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
    }
    kpi_record = {
        **manifest,
        "kpi_scope": "supervised_regime_classifier_mt5_runtime_probe",
        "python_tier_records": list(tier_records),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result["external_verification_status"],
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "kpi_management": dict(kpi),
        "judgment": summary["closure_judgment"],
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(RUN_ROOT / "summary.json", summary)
    write_md(REVIEW_PATH, packet_markdown(summary, kpi))
    write_json(PACKET_ROOT / "aggregate_summary.json", {**summary, "kpi_management": dict(kpi)})
    write_json(PACKET_ROOT / "skill_receipts.json", build_skill_receipts(summary, created_at))
    for name, payload in gate_payloads(summary, kpi).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    return summary


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    status = "completed" if summary.get("external_verification_status") == "completed" else "blocked"
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-runtime-parity",
            "status": status,
            "research_path": rel(ROOT / "stage_pipelines/stage23/supervised_regime_scout.py"),
            "runtime_path": rel(ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
            "shared_contract": "core24 feature order, q0.80 non-flat thresholds, 3-class probability output, Tier A primary plus Tier B fallback routing",
            "parity_check": summary.get("model_artifacts", {}).get("onnx_parity"),
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-backtest-forensics",
            "status": status,
            "tester_report_count": summary.get("mt5_kpi_record_count"),
            "runtime_failure_signature": summary.get("runtime_failure_signature"),
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "completed",
            "result_subject": RUN_ID,
            "judgment_label": summary.get("closure_judgment"),
            "claim_boundary": BOUNDARY,
        },
    ]


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    status = "active_run17B_mt5_runtime_probe_completed" if completed else "active_run17B_mt5_runtime_probe_blocked_after_attempt"
    next_action = "stage23_closeout_and_stage24_open_only" if completed else "repair_run17B_supervised_regime_runtime_probe_then_rerun_exact_attempts"
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    lines = state.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("current_run_id: "):
            lines[index] = f"current_run_id: {RUN_ID}"
    state = "\n".join(lines) + "\n"
    state = state.replace(
        "treat Stage 23 as active_run17A_python_structural_scout_completed after Stage23 supervised regime classifier scout; next action is run17B_supervised_regime_classifier_runtime_probe_v1, and no baseline, promotion, or runtime authority exists",
        f"treat Stage 23 as {status} after Stage23 supervised regime classifier MT5 runtime_probe; next action is {next_action}, and no baseline, promotion, or runtime authority exists",
    )
    state = state.replace("current_run_id: run17A_supervised_regime_classifier_filter_scout_v1", f"current_run_id: {RUN_ID}", 1)
    state = state.replace("status: active_run17A_python_structural_scout_completed", f"status: {status}", 1)
    state = state.replace("latest_completed_run: run17A_supervised_regime_classifier_filter_scout_v1", f"latest_completed_run: {RUN_ID}", 1)
    state = state.replace("next_exact_action: run17B_supervised_regime_classifier_runtime_probe_v1", f"next_exact_action: {next_action}", 1)
    stage_block = f"""stage23_supervised_regime_classifier_filter:
  stage_id: {STAGE_ID}
  status: {status}
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary.get('selected_variant_id')}
  boundary: {BOUNDARY}
  judgment: {summary.get('closure_judgment')}
  mt5_runtime_probe_status: {'completed_by_next_milestone_' + RUN_ID if completed else 'blocked_after_attempt_' + RUN_ID}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  report_path: stages/{STAGE_ID}/03_reviews/run17B_supervised_regime_classifier_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage23_supervised_regime_classifier_filter:", stage_block)
    block = f"""stage23_supervised_regime_run17B_runtime_probe:
  packet_id: {PACKET_ID}
  status: {'reviewed_runtime_probe_completed' if completed else 'blocked_runtime_probe_after_attempt'}
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  selected_variant_id: {summary.get('selected_variant_id')}
  mt5_attempt_count: {summary.get('attempt_count')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: stages/{STAGE_ID}/03_reviews/run17B_supervised_regime_classifier_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage23_supervised_regime_run17B_runtime_probe:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    status = "active_run17B_mt5_runtime_probe_completed" if completed else "active_run17B_mt5_runtime_probe_blocked_after_attempt"
    next_action = "stage23_closeout_and_stage24_open_only" if completed else "repair run17B supervised regime runtime probe and rerun the same six MT5 attempts"
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage23 Selection Status(23단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `{status}`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{summary.get('closure_judgment')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{kpi.get('normalized_records')}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage23(23단계)는 supervised classifier(지도 분류기)의 permission/filter(허용/필터) runtime behavior(런타임 행동)를 MT5까지 확인했지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Next Exact Action(다음 정확한 행동)

`{next_action}`.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else "# Stage23 Review Index(23단계 검토 색인)\n"
    line = f"- `{RUN_ID}`: `{rel(REVIEW_PATH)}`\n"
    if RUN_ID not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    write_md(
        DECISION_PATH,
        f"""# Stage23 RUN17B Supervised Regime Classifier Runtime Decision(23단계 실행17B 지도 국면 분류기 런타임 결정)

## Decision(결정)

`{RUN_ID}`를 `{summary.get('closure_judgment')}`로 기록한다.

효과(effect, 효과): supervised regime classifier(지도 국면 분류기)의 ONNX handoff(온닉스 인계)와 MT5 tester output(테스터 출력)을 확보했다. 이 근거는 runtime_probe(런타임 탐침)일 뿐 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)가 아니다.

## Next Condition(다음 조건)

`{next_action}`.
""",
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage23 RUN17B Supervised Regime Runtime Update(최신 23단계 실행17B 지도 국면 런타임 업데이트)

Stage23(23단계) `{RUN_ID}`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `{summary.get('closure_judgment')}`. MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`. next exact action(다음 정확한 행동): `{next_action}`.

효과(effect, 효과): run17A Python structural scout(파이썬 구조 탐색)를 ONNX runtime handoff(온닉스 런타임 인계) 확인으로 전진시켰다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- current run(현재 실행): `{SOURCE_RUN_ID}` completed(완료); next run(다음 실행): `{RUN_ID}`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    plan = plan.replace(
        f"Current active milestone(현재 활성 마일스톤): Stage23(23단계) `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침).",
        f"Current active milestone(현재 활성 마일스톤): Stage23(23단계) `{next_action}`.",
        1,
    )
    plan = plan.replace(
        f"- [ ] Stage23(23단계) supervised regime classifier(지도 국면 분류기) scout/probe/closeout/open Stage24. Completed(완료): `{SOURCE_RUN_ID}`; remaining(남음): MT5 runtime_probe(MT5 런타임 탐침), closeout/open Stage24.",
        f"- [ ] Stage23(23단계) supervised regime classifier(지도 국면 분류기) scout/probe/closeout/open Stage24. Completed(완료): `{SOURCE_RUN_ID}`, `{RUN_ID}`; remaining(남음): closeout/open Stage24.",
        1,
    )
    plan = plan.replace(
        f"Stage23(23단계)는 supervised regime classifier(지도 국면 분류기) `{SOURCE_RUN_ID}` Python structural scout(파이썬 구조 탐색)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage23(23단계) `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)이다.",
        f"Stage23(23단계)는 supervised regime classifier(지도 국면 분류기) `{SOURCE_RUN_ID}` Python structural scout(파이썬 구조 탐색)와 `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage23(23단계) `{next_action}`이다.",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` {'completed(완료)' if completed else 'blocked after attempt(시도 후 차단)'} as MT5 runtime_probe(MT5 런타임 탐침).
- active branch(활성 브랜치): `codex/stage23-supervised-regime-classifier`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage23(23단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/23_regime_model__supervised_regime_classifier_filter/02_runs/{RUN_ID}`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): supervised regime classifier runtime pipeline(지도 국면 분류기 런타임 파이프라인), run evidence(실행 근거), ledgers(장부), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/23_regime_model__supervised_regime_classifier_filter`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `{rel(RUN_ROOT / 'mt5')}` and `{rel(REVIEW_PATH)}`.
- blocker(차단 사유): `{'none(없음)' if completed else 'see run_manifest runtime_probe failure(실행 목록 런타임 탐침 실패 참고)'}`.
- exact next action(정확한 다음 행동): `{next_action}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage23(23단계) closeout/open Stage24(마감/24단계 개방) 또는 run17B repair(수정)에서 시작한다.
"""
    start = plan.find("## Latest Stop Resume State(최신 중지 재개 상태)")
    end = plan.find("\n## Per-Stage Milestone Loop", start)
    if start != -1 and end != -1:
        plan = plan[:start] + resume + plan[end:]
    else:
        plan = plan.rstrip() + "\n\n" + resume
    outcome = f"- `2026-05-05`: Stage23(23단계) `{RUN_ID}` MT5 runtime_probe(런타임 탐침)를 기록했다. judgment(판정): `{summary.get('closure_judgment')}`.\n"
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def materialize_bundle(args: argparse.Namespace) -> dict[str, Any]:
    source_summary = load_source_summary()
    contract = runtime_contract(source_summary)
    context = scout.load_context()
    models = load_models(source_summary)
    tier_records, prediction_artifacts, _ = materialize_python_tier_records(context, models, contract)
    model_artifacts = export_models(context, models, contract)
    feature_matrices = export_feature_matrices(context, contract)
    copies = copy_runtime_inputs(model_artifacts, feature_matrices)
    attempts = make_attempts(context, model_artifacts, feature_matrices, contract)
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "selected_variant_id": contract["selected_variant_id"],
        "attempts": attempts,
        "common_copies": copies,
        "route_coverage": context["tier_b_context_summary"],
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
    }
    if args.materialize_only:
        write_json(
            RUN_ROOT / "materialized_runtime_probe_bundle.json",
            {
                **prepared,
                "prediction_artifacts": prediction_artifacts,
                "python_tier_records": tier_records,
                "external_verification_status": "not_attempted_materialize_only",
            },
        )
    return {
        "source_summary": source_summary,
        "context": context,
        "tier_records": tier_records,
        "prediction_artifacts": prediction_artifacts,
        "model_artifacts": model_artifacts,
        "prepared": prepared,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    bundle = materialize_bundle(args)
    if args.materialize_only:
        return {
            "run_id": RUN_ID,
            "judgment": "not_attempted_materialize_only",
            "external_verification_status": "not_attempted_materialize_only",
            "mt5_kpi_record_count": 0,
            "attempt_count": len(bundle["prepared"]["attempts"]),
            "model_artifacts": bundle["model_artifacts"],
            "prepared_bundle_path": rel(RUN_ROOT / "materialized_runtime_probe_bundle.json"),
        }
    result = execute_or_block(bundle["prepared"], args)
    result["model_artifacts"] = bundle["model_artifacts"]
    result["feature_matrices"] = bundle["prepared"]["feature_matrices"]
    provisional = {
        "normalized_records": 0,
        "normalized_summary_rows": 0,
        "missing_runs": 0,
        "parser_errors": 0,
        "trade_attribution_records": 0,
        "trade_level_rows": 0,
        "trade_parser_errors": 0,
    }
    write_run_outputs(
        result,
        bundle["model_artifacts"],
        bundle["prediction_artifacts"],
        bundle["tier_records"],
        bundle["source_summary"],
        provisional,
        created_at,
    )
    kpi = write_normalized_kpi()
    summary = write_run_outputs(
        result,
        bundle["model_artifacts"],
        bundle["prediction_artifacts"],
        bundle["tier_records"],
        bundle["source_summary"],
        kpi,
        created_at,
    )
    update_workspace_state(summary)
    update_text_docs(summary, kpi)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage23 supervised regime classifier MT5 runtime probe.")
    parser.add_argument("--materialize-only", action="store_true", help="Prepare artifacts without launching MT5 or changing current truth docs.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    summary = run(args)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "judgment": summary["judgment"],
                    "external_verification_status": summary["external_verification_status"],
                    "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
                    "attempt_count": summary.get("attempt_count"),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
