from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import alpha_run_ledgers  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    ledger_pairs,
    upsert_csv_rows,
)
from foundation.models.baseline_training import LABEL_ORDER, load_feature_order, validate_model_input_frame  # noqa: E402
from foundation.pipelines import run_stage10_logreg_mt5_scout as mt5  # noqa: E402


STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
SOURCE_RUN_ID = "run03D_et_standalone_batch20_v1"
SOURCE_VARIANT_ID = "v11_base_leaf20_q85"
RUN_ID = "run03E_et_batch20_top_v11_mt5_probe_v1"
RUN_NUMBER = "run03E"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesBatch20TopV11MT5Probe"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
COMMON_RUN_ROOT = f"Project_Obsidian_Prime_v2/stage12/{RUN_ID}"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
DEFAULT_MODEL_INPUT_PATH = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = ROOT.parents[1] / "Profiles" / "Tester"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
EA_TESTER_SET_NAME = "ObsidianPrimeV2_RuntimeProbeEA.set"
TIER_A = "Tier A"
TIER_B = "Tier B"
TIER_AB = "Tier A+B"


def io(path: Path) -> Path:
    return mt5._io_path(path)


def path_exists(path: Path) -> bool:
    return mt5._path_exists(path)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(json.dumps(mt5._json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def read_text(path: Path) -> str:
    return io(path).read_text(encoding="utf-8-sig")


def sha256_file(path: Path) -> str:
    return mt5.sha256_file(path)


def load_source_variant() -> dict[str, Any]:
    results_path = SOURCE_RUN_ROOT / "results/variant_results.csv"
    summary_path = SOURCE_RUN_ROOT / "summary.json"
    if not path_exists(results_path):
        raise FileNotFoundError(results_path)
    summary = json.loads(read_text(summary_path))
    if summary.get("standalone_boundary", {}).get("stage10_11_inheritance") is not False:
        raise RuntimeError("RUN03D is not marked stage10_11_inheritance=false.")
    if summary.get("standalone_boundary", {}).get("stage10_11_baseline") is not False:
        raise RuntimeError("RUN03D is not marked stage10_11_baseline=false.")
    rows = pd.read_csv(io(results_path))
    selected = rows.loc[rows["variant_id"].astype(str).eq(SOURCE_VARIANT_ID)]
    if selected.empty:
        raise RuntimeError(f"Missing source variant: {SOURCE_VARIANT_ID}")
    row = selected.iloc[0].to_dict()
    row["model_params"] = json.loads(str(row["model_params_json"]))
    return row


def split_date_range(frame: pd.DataFrame, split_name: str) -> tuple[str, str]:
    split = frame.loc[frame["split"].astype(str).eq(split_name)]
    if split.empty:
        raise RuntimeError(f"Split is empty: {split_name}")
    timestamps = pd.to_datetime(split["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def probability_matrix(model: ExtraTreesClassifier, values: np.ndarray) -> np.ndarray:
    raw = model.predict_proba(values)
    probs = np.zeros((len(values), 3), dtype=float)
    for idx, klass in enumerate(model.classes_):
        probs[:, [0, 1, 2].index(int(klass))] = raw[:, idx]
    return probs


def decision_frame(frame: pd.DataFrame, probs: np.ndarray, threshold: float, split_label: str) -> pd.DataFrame:
    p_short = probs[:, 0]
    p_flat = probs[:, 1]
    p_long = probs[:, 2]
    predicted_direction = np.where(p_short >= p_long, 0, 2)
    nonflat_conf = np.maximum(p_short, p_long)
    pass_gate = nonflat_conf >= threshold
    decision = np.full(len(frame), 1, dtype="int64")
    decision[pass_gate] = predicted_direction[pass_gate]
    labels = frame["label_class"].astype("int64").to_numpy()
    signals = decision != 1
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": split_label,
            "label_class": labels,
            "p_short": p_short,
            "p_flat": p_flat,
            "p_long": p_long,
            "threshold": threshold,
            "decision_class": decision,
            "decision_label": pd.Series(decision).map({0: "short", 1: "flat", 2: "long"}).to_numpy(),
            "is_signal": signals,
            "directional_correct": signals & (decision == labels),
        }
    )


def signal_metrics(decisions: pd.DataFrame) -> dict[str, Any]:
    signals = decisions.loc[decisions["is_signal"]]
    return {
        "rows": int(len(decisions)),
        "signal_count": int(len(signals)),
        "short_count": int((signals["decision_class"] == 0).sum()),
        "long_count": int((signals["decision_class"] == 2).sum()),
        "signal_coverage": float(len(signals) / len(decisions)) if len(decisions) else None,
        "directional_correct_count": int(signals["directional_correct"].sum()) if len(signals) else 0,
        "directional_hit_rate": float(signals["directional_correct"].mean()) if len(signals) else None,
    }


def common_ref(*parts: str) -> str:
    return "/".join([COMMON_RUN_ROOT, *parts])


def tester_profile_ini_name(split_name: str) -> str:
    split_code = "v" if split_name == "validation_is" else "o"
    return f"opv2_{RUN_NUMBER}_ta_{split_code}.ini"


def format_mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def materialize_tester_set_file(parameters: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    io(output_path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run_stage12_batch20_top_mt5_probe.py"]
    for key, value in parameters.items():
        lines.append(f"{key}={format_mt5_value(value)}")
    io(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": output_path.as_posix(), "sha256": sha256_file(output_path), "format": "mt5_set"}


def materialize_attempt(
    *,
    run_output_root: Path,
    split_name: str,
    local_onnx_path: Path,
    local_feature_matrix_path: Path,
    rule: mt5.ThresholdRule,
    feature_count: int,
    feature_order_hash: str,
    from_date: str,
    to_date: str,
    max_hold_bars: int,
) -> dict[str, Any]:
    stem = f"tier_a_only_{split_name}"
    common_model = common_ref("models", local_onnx_path.name)
    common_matrix = common_ref("features", local_feature_matrix_path.name)
    common_telemetry = common_ref("telemetry", f"{stem}_telemetry.csv")
    common_summary = common_ref("telemetry", f"{stem}_summary.csv")
    set_path = run_output_root / "mt5" / f"{stem}.set"
    ini_path = run_output_root / "mt5" / f"{stem}.ini"
    set_payload = materialize_tester_set_file(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": TIER_A,
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": split_name,
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpModelPath": common_model,
            "InpModelId": f"{RUN_ID}_{SOURCE_VARIANT_ID}",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_matrix,
            "InpFeatureCount": feature_count,
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFallbackEnabled": "false",
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": rule.short_threshold,
            "InpLongThreshold": rule.long_threshold,
            "InpMinMargin": rule.min_margin,
            "InpInvertSignal": "false",
            "InpFallbackShortThreshold": rule.short_threshold,
            "InpFallbackLongThreshold": rule.long_threshold,
            "InpFallbackMinMargin": rule.min_margin,
            "InpFallbackInvertSignal": "false",
            "InpAllowTrading": "true",
            "InpFixedLot": 0.1,
            "InpMaxHoldBars": int(max_hold_bars),
            "InpMaxConcurrentPositions": 1,
            "InpFeatureOrderHash": feature_order_hash,
            "InpMagic": 1203005,
        },
        set_path,
    )
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{stem}"
    ini_payload = mt5.materialize_tester_ini_file(
        mt5.TesterMaterializationConfig(
            from_date=from_date,
            to_date=to_date,
            report=report_name,
            shutdown_terminal=1,
        ),
        ini_path,
        set_file_path=Path(EA_TESTER_SET_NAME),
    )
    return {
        "tier": TIER_A,
        "split": split_name,
        "attempt_role": "tier_only_total",
        "record_view_prefix": "mt5_tier_a_only",
        "set": set_payload,
        "ini": ini_payload,
        "common_model_path": common_model,
        "common_feature_matrix_path": common_matrix,
        "common_telemetry_path": common_telemetry,
        "common_summary_path": common_summary,
        "local_feature_matrix_path": local_feature_matrix_path.as_posix(),
        "threshold_rule": mt5.threshold_rule_payload(rule),
        "max_hold_bars": int(max_hold_bars),
        "source_run": SOURCE_RUN_ID,
        "source_variant": SOURCE_VARIANT_ID,
        "standalone_scope": True,
        "stage10_11_inheritance": False,
    }


def metric_by_view(records: Sequence[Mapping[str, Any]], view: str, metric: str) -> Any:
    for record in records:
        if str(record.get("record_view")) == view:
            metrics = record.get("metrics", {})
            return metrics.get(metric) if isinstance(metrics, Mapping) else None
    return None


def view_status(records: Sequence[Mapping[str, Any]], view: str) -> str:
    for record in records:
        if str(record.get("record_view")) == view:
            return str(record.get("status"))
    return "missing"


def metric_text(records: Sequence[Mapping[str, Any]], view: str, metric: str) -> str:
    value = metric_by_view(records, view, metric)
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "blocked_or_missing(차단 또는 누락)"
    return str(value)


def boundary_rows(summary_path: Path) -> list[dict[str, Any]]:
    return [
        {
            "ledger_row_id": f"{RUN_ID}__mt5_tier_b_separate_boundary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_tier_b_separate_boundary",
            "parent_run_id": RUN_ID,
            "record_view": "mt5_tier_b_separate_boundary",
            "tier_scope": TIER_B,
            "kpi_scope": "paired_tier_record_boundary",
            "scoreboard_lane": "runtime_probe",
            "status": "not_produced",
            "judgment": "out_of_scope_by_claim_standalone_tier_a_only",
            "path": rel(summary_path),
            "primary_kpi": "missing_required=out_of_scope_by_claim",
            "guardrail_kpi": "reason=run03d_top_variant_mt5_probe_is_tier_a_only",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Tier B separate(Tier B 분리)는 RUN03E 주장 범위 밖(out_of_scope_by_claim)이다.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__mt5_tier_ab_combined_boundary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_tier_ab_combined_boundary",
            "parent_run_id": RUN_ID,
            "record_view": "mt5_tier_ab_combined_boundary",
            "tier_scope": TIER_AB,
            "kpi_scope": "paired_tier_record_boundary",
            "scoreboard_lane": "runtime_probe",
            "status": "not_produced",
            "judgment": "out_of_scope_by_claim_standalone_tier_a_only",
            "path": rel(summary_path),
            "primary_kpi": "missing_required=out_of_scope_by_claim",
            "guardrail_kpi": "reason=no_tier_b_fallback_or_combined_total_claim",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Tier A+B combined(Tier A+B 합산)는 RUN03E 주장 범위 밖(out_of_scope_by_claim)이다.",
        },
    ]


def blocked_rows(execution_results: Sequence[Mapping[str, Any]], run_output_root: Path, external_status: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in execution_results:
        if result.get("status") == "completed":
            continue
        split = str(result.get("split"))
        view = f"{result.get('record_view_prefix', 'mt5_tier_a_only')}_{split}"
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": RUN_ID,
                "record_view": view,
                "tier_scope": TIER_A,
                "kpi_scope": "trading_risk_execution",
                "scoreboard_lane": "runtime_probe",
                "status": "blocked",
                "judgment": "blocked_run03d_top_variant_mt5_runtime_probe",
                "path": rel(run_output_root / "kpi_record.json"),
                "primary_kpi": ledger_pairs((("returncode", result.get("returncode")), ("status", result.get("status")))),
                "guardrail_kpi": ledger_pairs((("source_run", SOURCE_RUN_ID), ("source_variant", SOURCE_VARIANT_ID))),
                "external_verification_status": external_status,
                "notes": "RUN03E MT5 runtime probe(MT5 런타임 탐침)가 실행됐지만 완료 근거가 부족하다.",
            }
        )
    return rows


def registry_notes(external_status: str, records: Sequence[Mapping[str, Any]]) -> str:
    return ledger_pairs(
        (
            ("source_run", SOURCE_RUN_ID),
            ("source_variant", SOURCE_VARIANT_ID),
            ("standalone_scope", True),
            ("stage10_11_inheritance", False),
            ("comparison_baseline", None),
            ("validation_net_profit", metric_by_view(records, "mt5_tier_a_only_validation_is", "net_profit")),
            ("validation_pf", metric_by_view(records, "mt5_tier_a_only_validation_is", "profit_factor")),
            ("validation_trades", metric_by_view(records, "mt5_tier_a_only_validation_is", "trade_count")),
            ("oos_net_profit", metric_by_view(records, "mt5_tier_a_only_oos", "net_profit")),
            ("oos_pf", metric_by_view(records, "mt5_tier_a_only_oos", "profit_factor")),
            ("oos_trades", metric_by_view(records, "mt5_tier_a_only_oos", "trade_count")),
            ("external_verification", external_status),
            ("boundary", "runtime_probe_only"),
        )
    )


def update_ledgers(run_output_root: Path, mt5_records: Sequence[Mapping[str, Any]], execution_results: Sequence[Mapping[str, Any]], external_status: str, summary_path: Path) -> dict[str, Any]:
    rows = alpha_run_ledgers.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=mt5_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
        tier_b=TIER_B,
    )
    rows.extend(blocked_rows(execution_results, run_output_root, external_status))
    rows.extend(boundary_rows(summary_path))
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "standalone_batch20_top_mt5_runtime_probe",
                "status": "reviewed" if external_status == "completed" else "blocked",
                "judgment": "inconclusive_run03d_top_variant_mt5_runtime_probe_completed"
                if external_status == "completed"
                else "blocked_run03d_top_variant_mt5_runtime_probe",
                "path": rel(run_output_root),
                "notes": registry_notes(external_status, mt5_records),
            }
        ],
        key="run_id",
    )
    return {"stage_run_ledger": stage_payload, "project_alpha_run_ledger": project_payload, "run_registry": registry_payload}


def write_reports(run_output_root: Path, source_variant: Mapping[str, Any], python_metrics: Mapping[str, Any], onnx_parity: Mapping[str, Any], records: Sequence[Mapping[str, Any]], external_status: str) -> None:
    validation_view = "mt5_tier_a_only_validation_is"
    oos_view = "mt5_tier_a_only_oos"
    judgment = (
        "inconclusive_run03d_top_variant_mt5_runtime_probe_completed"
        if external_status == "completed"
        else "blocked_run03d_top_variant_mt5_runtime_probe"
    )
    result = f"""# {RUN_NUMBER} RUN03D Top Variant MT5 Probe(상위 변형 MT5 검증)

## Boundary(경계)

- run(실행): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- source variant(원천 변형): `{SOURCE_VARIANT_ID}`
- standalone boundary(단독 경계): Stage10/11(10/11단계) inheritance(계승)와 baseline(기준선)은 사용하지 않았다.
- external verification(외부 검증): `{external_status}`
- judgment(판정): `{judgment}`
- effect(효과): RUN03D(실행 03D) 최고 변형을 MT5(`MetaTrader 5`, 메타트레이더5) 런타임으로 확인하되, alpha quality(알파 품질)나 operating promotion(운영 승격)으로 말하지 않는다.

## Python Replay(파이썬 재현)

| split(분할) | signals(신호) | hit rate(적중률) |
|---|---:|---:|
| validation(검증) | {python_metrics['validation']['signal_count']} | {python_metrics['validation']['directional_hit_rate']} |
| OOS(표본외) | {python_metrics['oos']['signal_count']} | {python_metrics['oos']['directional_hit_rate']} |

## MT5 Strategy Tester(MT5 전략 테스터)

| split(분할) | status(상태) | net profit(순손익) | PF(수익팩터) | trades(거래) | max DD(최대 손실) |
|---|---|---:|---:|---:|---:|
| validation(검증) | {view_status(records, validation_view)} | {metric_text(records, validation_view, 'net_profit')} | {metric_text(records, validation_view, 'profit_factor')} | {metric_text(records, validation_view, 'trade_count')} | {metric_text(records, validation_view, 'max_drawdown_amount')} |
| OOS(표본외) | {view_status(records, oos_view)} | {metric_text(records, oos_view, 'net_profit')} | {metric_text(records, oos_view, 'profit_factor')} | {metric_text(records, oos_view, 'trade_count')} | {metric_text(records, oos_view, 'max_drawdown_amount')} |

## Runtime Parity(런타임 동등성)

- ONNX parity(ONNX 동등성): `{onnx_parity.get('passed')}`
- max abs diff(최대 절대 차이): `{onnx_parity.get('max_abs_diff')}`
- threshold(임계값): `{source_variant['threshold']}`
- effect(효과): Python probability(파이썬 확률)와 MT5 model handoff(모델 인계)가 같은 확률 표면을 쓰는지 확인한다.
"""
    packet = f"""# {RUN_NUMBER} review packet(검토 묶음)

## Result(결과)

`{RUN_ID}`는 RUN03D(실행 03D) top variant(상위 변형) `{SOURCE_VARIANT_ID}`의 MT5 runtime_probe(MT5 런타임 탐침)다.

## Evidence(근거)

- result summary(결과 요약): `{rel(run_output_root / 'reports/result_summary.md')}`
- manifest(실행 목록): `{rel(run_output_root / 'run_manifest.json')}`
- KPI record(KPI 기록): `{rel(run_output_root / 'kpi_record.json')}`
- source variant result(원천 변형 결과): `{rel(SOURCE_RUN_ROOT / 'results/variant_results.csv')}`

## Judgment(판정)

`{judgment}`. effect(효과): MT5 검증은 붙었지만 runtime_probe(런타임 탐침) 경계 안에서만 해석한다.
"""
    write_text(run_output_root / "reports/result_summary.md", result)
    write_text(STAGE_ROOT / f"03_reviews/{RUN_NUMBER}_batch20_top_mt5_probe_packet.md", packet)


def update_selection_status(source_variant: Mapping[str, Any], records: Sequence[Mapping[str, Any]], external_status: str) -> None:
    path = STAGE_ROOT / "04_selected/selection_status.md"
    text = read_text(path) if path_exists(path) else f"# {STAGE_ID} selection status(선택 상태)\n"
    block = f"""

## {RUN_NUMBER} RUN03D top MT5 read(RUN03D 상위 변형 MT5 판독)

- run(실행): `{RUN_ID}`
- source variant(원천 변형): `{SOURCE_VARIANT_ID}`
- external verification(외부 검증): `{external_status}`
- validation net/PF(검증 순손익/수익팩터): `{metric_text(records, 'mt5_tier_a_only_validation_is', 'net_profit')}` / `{metric_text(records, 'mt5_tier_a_only_validation_is', 'profit_factor')}`
- OOS net/PF(표본외 순손익/수익팩터): `{metric_text(records, 'mt5_tier_a_only_oos', 'net_profit')}` / `{metric_text(records, 'mt5_tier_a_only_oos', 'profit_factor')}`
- judgment(판정): `inconclusive_run03d_top_variant_mt5_runtime_probe_completed`
- effect(효과): RUN03D 대표 변형은 MT5 검증을 받았지만, 운영 승격이나 알파 품질 주장은 아니다.
"""
    pattern = re.compile(rf"\n## {RUN_NUMBER} RUN03D top MT5 read\(RUN03D 상위 변형 MT5 판독\).*?(?=\n## |\Z)", re.S)
    text = pattern.sub(block.rstrip(), text) if pattern.search(text) else text.rstrip() + block
    write_text(path, text.rstrip() + "\n")


def update_current_truth(source_variant: Mapping[str, Any], records: Sequence[Mapping[str, Any]], external_status: str, summary_path: Path) -> None:
    workspace_path = ROOT / "docs/workspace/workspace_state.yaml"
    workspace = read_text(workspace_path)
    stage12_block = f"""stage12_model_family_challenge:
  stage_id: "{STAGE_ID}"
  status: "active_standalone_batch20_top_mt5_probe_completed"
  lane: "standalone_batch20_top_mt5_runtime_probe"
  current_run_id: "{RUN_ID}"
  current_run_label: "{EXPLORATION_LABEL}"
  current_status: "reviewed"
  current_summary:
    boundary: "Stage12 standalone(단독); no Stage10/11 inheritance(10/11단계 비계승) or baseline(기준선)"
    latest_python_package: "{SOURCE_RUN_ID}"
    latest_mt5_runtime_probe: "{RUN_ID}"
    source_variant: "{SOURCE_VARIANT_ID}"
    python_validation_hit_rate: {float(source_variant['validation_hit_rate']):.12f}
    python_oos_hit_rate: {float(source_variant['oos_hit_rate']):.12f}
    validation_net_profit: {json.dumps(metric_by_view(records, 'mt5_tier_a_only_validation_is', 'net_profit'))}
    validation_profit_factor: {json.dumps(metric_by_view(records, 'mt5_tier_a_only_validation_is', 'profit_factor'))}
    validation_trades: {json.dumps(metric_by_view(records, 'mt5_tier_a_only_validation_is', 'trade_count'))}
    oos_net_profit: {json.dumps(metric_by_view(records, 'mt5_tier_a_only_oos', 'net_profit'))}
    oos_profit_factor: {json.dumps(metric_by_view(records, 'mt5_tier_a_only_oos', 'profit_factor'))}
    oos_trades: {json.dumps(metric_by_view(records, 'mt5_tier_a_only_oos', 'trade_count'))}
    package_judgment: "inconclusive_run03d_top_variant_mt5_runtime_probe_completed"
    external_verification: "{external_status}"
    result_summary_path: "{rel(RUN_ROOT / 'reports/result_summary.md')}"
    summary_path: "{rel(summary_path)}"
    next_action: "Review whether v16/v09/v13(변형 후보) deserve separate MT5 probes(MT5 탐침)"
"""
    workspace = re.sub(r"stage12_model_family_challenge:\n.*?(?=\nopen_items:)", stage12_block, workspace, flags=re.S)
    if "Stage 12 RUN03E" not in workspace:
        workspace = workspace.replace(
            '  - "Stage 12 RUN03D completed standalone(단독) batch20(20개 묶음) Python structural scout(파이썬 구조 탐색); package judgment(패키지 판정) is inconclusive(불충분)"',
            '  - "Stage 12 RUN03D completed standalone(단독) batch20(20개 묶음) Python structural scout(파이썬 구조 탐색); package judgment(패키지 판정) is inconclusive(불충분)"\n'
            '  - "Stage 12 RUN03E completed MT5 runtime_probe(MT5 런타임 탐침) for RUN03D top variant(상위 변형) v11_base_leaf20_q85"',
        )
    write_text(workspace_path, workspace)

    current_path = ROOT / "docs/context/current_working_state.md"
    current = read_text(current_path)
    stage12_md = f"""## 현재 Stage 12 상태(Current Stage 12 State, 현재 Stage 12 상태)

- 활성 단계(active stage, 활성 단계): `12_model_family_challenge__extratrees_training_effect`.
- 현재 실행(current run, 현재 실행): `{RUN_ID}`.
- 독립 경계(standalone boundary, 독립 경계): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력은 사용하지 않는다.
- 최신 Python 패키지(latest Python package, 최신 파이썬 패키지): `{SOURCE_RUN_ID}`.
- 최신 MT5 런타임 탐침(latest MT5 runtime probe, 최신 MT5 런타임 탐침): `{RUN_ID}`.
- 검증 대상(target, 대상): `{SOURCE_VARIANT_ID}`.
- Python 검증/표본외 적중(Python validation/OOS hit, 파이썬 검증/표본외 적중): `{float(source_variant['validation_hit_rate']):.6f}` / `{float(source_variant['oos_hit_rate']):.6f}`.
- MT5 검증 net/PF(MT5 validation net/PF, MT5 검증 순손익/수익팩터): `{metric_text(records, 'mt5_tier_a_only_validation_is', 'net_profit')}` / `{metric_text(records, 'mt5_tier_a_only_validation_is', 'profit_factor')}`.
- MT5 표본외 net/PF(MT5 OOS net/PF, MT5 표본외 순손익/수익팩터): `{metric_text(records, 'mt5_tier_a_only_oos', 'net_profit')}` / `{metric_text(records, 'mt5_tier_a_only_oos', 'profit_factor')}`.
- 판정(judgment, 판정): `inconclusive_run03d_top_variant_mt5_runtime_probe_completed`.
- 효과(effect, 효과): RUN03D 대표 변형까지 MT5 외부 검증을 붙였지만, runtime_probe(런타임 탐침)일 뿐 alpha quality(알파 품질)나 operating promotion(운영 승격)은 아니다.
"""
    current = re.sub(
        r"## 현재 Stage 12 상태\(Current Stage 12 State, 현재 Stage 12 상태\).*?(?=\n## 현재 경계)",
        stage12_md,
        current,
        flags=re.S,
    )
    write_text(current_path, current)

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = read_text(changelog_path)
    entry = (
        f"\n- 2026-04-28: `{RUN_ID}` completed(완료). RUN03D top variant(상위 변형) `{SOURCE_VARIANT_ID}` "
        f"MT5 runtime_probe(MT5 런타임 탐침), validation/OOS net(검증/표본외 순손익) "
        f"`{metric_text(records, 'mt5_tier_a_only_validation_is', 'net_profit')}` / "
        f"`{metric_text(records, 'mt5_tier_a_only_oos', 'net_profit')}`, external verification(외부 검증) `{external_status}`.\n"
    )
    pattern = re.compile(rf"\n- 2026-04-28: `{RUN_ID}` completed\(완료\).*?(?=\n- |\Z)", re.S)
    changelog = pattern.sub(entry.rstrip(), changelog) if pattern.search(changelog) else changelog.rstrip() + entry
    write_text(changelog_path, changelog.rstrip() + "\n")


def run(args: argparse.Namespace) -> dict[str, Any]:
    mt5.configure_run_identity(
        run_number=RUN_NUMBER,
        run_id=RUN_ID,
        exploration_label=EXPLORATION_LABEL,
        common_run_root=COMMON_RUN_ROOT,
    )
    run_output_root = Path(args.run_output_root)
    for folder in ("models", "predictions", "mt5", "reports"):
        io(run_output_root / folder).mkdir(parents=True, exist_ok=True)
    io(STAGE_ROOT / "03_reviews").mkdir(parents=True, exist_ok=True)
    io(STAGE_ROOT / "04_selected").mkdir(parents=True, exist_ok=True)

    source_variant = load_source_variant()
    feature_order = load_feature_order(Path(args.feature_order_path))
    feature_hash = mt5.ordered_hash(feature_order)
    if feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {feature_hash} != {FEATURE_ORDER_HASH}")
    frame = pd.read_parquet(io(Path(args.model_input_path)))
    validate_model_input_frame(frame, feature_order)
    if "label_class" not in frame.columns:
        raise RuntimeError("model input is missing label_class")

    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    validation = frame.loc[frame["split"].astype(str).eq("validation")].copy()
    oos = frame.loc[frame["split"].astype(str).eq("oos")].copy()
    model = ExtraTreesClassifier(**source_variant["model_params"])
    model.fit(train.loc[:, feature_order].to_numpy(dtype="float64", copy=False), train["label_class"].astype("int64").to_numpy())
    if [int(value) for value in model.classes_] != [int(value) for value in LABEL_ORDER]:
        raise RuntimeError(f"Model class order mismatch: {model.classes_}")

    threshold = float(source_variant["threshold"])
    rule = mt5.threshold_rule_from_values(
        threshold_id=f"{SOURCE_VARIANT_ID}_q{float(source_variant['threshold_quantile']):.2f}",
        short_threshold=threshold,
        long_threshold=threshold,
        min_margin=float(source_variant["min_margin"]),
    )
    onnx_path = run_output_root / f"models/{SOURCE_VARIANT_ID}.onnx"
    onnx_export = mt5.export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=len(feature_order))
    parity_values = validation.loc[:, feature_order].to_numpy(dtype="float64", copy=False)[: max(1, min(args.parity_rows, len(validation)))]
    onnx_parity = mt5.check_onnxruntime_probability_parity(model, onnx_path, parity_values)

    validation_probs = probability_matrix(model, validation.loc[:, feature_order].to_numpy(dtype="float64", copy=False))
    oos_probs = probability_matrix(model, oos.loc[:, feature_order].to_numpy(dtype="float64", copy=False))
    validation_decisions = decision_frame(validation, validation_probs, threshold, "validation")
    oos_decisions = decision_frame(oos, oos_probs, threshold, "oos")
    python_metrics = {"validation": signal_metrics(validation_decisions), "oos": signal_metrics(oos_decisions)}
    runtime_decision_path = run_output_root / "predictions/runtime_decisions.parquet"
    pd.concat([validation_decisions, oos_decisions], ignore_index=True).to_parquet(io(runtime_decision_path), index=False)

    common_files_root = Path(args.common_files_root)
    terminal_data_root = Path(args.terminal_data_root)
    tester_profile_root = Path(args.tester_profile_root)
    common_copies = [mt5.copy_to_common_files(common_files_root, onnx_path, common_ref("models", onnx_path.name))]
    split_specs = {
        "validation_is": ("validation", validation, *split_date_range(frame, "validation")),
        "oos": ("oos", oos, *split_date_range(frame, "oos")),
    }
    attempts: list[dict[str, Any]] = []
    feature_matrices: dict[str, Any] = {}
    for split_label, (_source_split, split_frame, from_date, to_date) in split_specs.items():
        matrix_path = run_output_root / "mt5" / f"tier_a_only_{split_label}_feature_matrix.csv"
        matrix_payload = mt5.export_mt5_feature_matrix_csv(split_frame, feature_order, matrix_path)
        feature_matrices[split_label] = matrix_payload
        common_copies.append(mt5.copy_to_common_files(common_files_root, matrix_path, common_ref("features", matrix_path.name)))
        attempt = materialize_attempt(
            run_output_root=run_output_root,
            split_name=split_label,
            local_onnx_path=onnx_path,
            local_feature_matrix_path=matrix_path,
            rule=rule,
            feature_count=len(feature_order),
            feature_order_hash=feature_hash,
            from_date=from_date,
            to_date=to_date,
            max_hold_bars=args.max_hold_bars,
        )
        attempt["feature_matrix"] = matrix_payload
        attempts.append(attempt)

    compile_payload: dict[str, Any] | None = None
    execution_results: list[dict[str, Any]] = []
    if args.attempt_mt5:
        for attempt in attempts:
            for key in ("common_telemetry_path", "common_summary_path"):
                output = common_files_root / Path(str(attempt[key]))
                if path_exists(output):
                    io(output).unlink()
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = mt5.compile_mql5_ea(Path(args.metaeditor_path), mt5.EA_SOURCE_PATH, run_output_root / "mt5/mt5_compile.log")
        if compile_payload["status"] == "completed":
            for attempt in attempts:
                result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    Path(attempt["ini"]["path"]),
                    set_path=Path(attempt["set"]["path"]),
                    tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                    tester_profile_ini_path=tester_profile_root / tester_profile_ini_name(str(attempt["split"])),
                    timeout_seconds=args.mt5_timeout_seconds,
                )
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                result["attempt_role"] = attempt["attempt_role"]
                result["record_view_prefix"] = attempt["record_view_prefix"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=args.runtime_output_timeout_seconds)
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                execution_results.append(result)

    report_records = (
        mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=attempts,
        )
        if args.attempt_mt5
        else []
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    mt5_records = mt5.build_mt5_kpi_records(execution_results)
    route_coverage = {
        "by_split": {
            "validation": {"tier_a_primary_rows": int(len(validation)), "routed_labelable_rows": int(len(validation))},
            "oos": {"tier_a_primary_rows": int(len(oos)), "routed_labelable_rows": int(len(oos))},
        },
        "no_tier_by_split": {"validation": 0, "oos": 0},
        "tier_b_fallback_by_split_subtype": {},
    }
    mt5_records = mt5.enrich_mt5_kpi_records_with_route_coverage(mt5_records, route_coverage)
    runtime_completed = bool(args.attempt_mt5) and len(execution_results) == len(attempts) and all(result.get("status") == "completed" for result in execution_results)
    report_completed = len(mt5_records) >= len(attempts) and all(record.get("status") == "completed" for record in mt5_records)
    external_status = "completed" if runtime_completed and report_completed else "blocked" if args.attempt_mt5 else "out_of_scope_by_claim"
    judgment = "inconclusive_run03d_top_variant_mt5_runtime_probe_completed" if external_status == "completed" else "blocked_run03d_top_variant_mt5_runtime_probe"

    summary_path = run_output_root / "summary.json"
    ledger_payload = update_ledgers(run_output_root, mt5_records, execution_results, external_status, summary_path)
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "lane": "standalone_batch20_top_mt5_runtime_probe",
            "status": "reviewed" if external_status == "completed" else "blocked",
            "judgment": judgment,
        },
        "source": {
            "run_id": SOURCE_RUN_ID,
            "variant_id": SOURCE_VARIANT_ID,
            "variant_result_path": rel(SOURCE_RUN_ROOT / "results/variant_results.csv"),
            "stage10_11_inheritance": False,
            "stage10_11_baseline": False,
        },
        "model": {
            "family": MODEL_FAMILY,
            "params": source_variant["model_params"],
            "threshold": threshold,
            "threshold_quantile": source_variant["threshold_quantile"],
            "feature_count": len(feature_order),
            "feature_order_hash": feature_hash,
        },
        "python_metrics": python_metrics,
        "onnx_parity": onnx_parity,
        "mt5": {
            "attempted": bool(args.attempt_mt5),
            "external_verification_status": external_status,
            "compile": compile_payload,
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "kpi_records": mt5_records,
            "attempts": attempts,
            "tester_identity": {
                "symbol": "US100",
                "period": "M5",
                "model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "max_hold_bars": int(args.max_hold_bars),
            },
        },
        "artifacts": {
            "onnx": {"path": rel(onnx_path), "sha256": sha256_file(onnx_path), **onnx_export},
            "runtime_decisions": {"path": rel(runtime_decision_path), "sha256": sha256_file(runtime_decision_path)},
            "feature_matrices": feature_matrices,
            "common_copies": common_copies,
            "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        },
        "tier_records": {
            "tier_a_separate": "completed" if external_status == "completed" else external_status,
            "tier_b_separate": "out_of_scope_by_claim_standalone_tier_a_only",
            "tier_ab_combined": "out_of_scope_by_claim_standalone_tier_a_only",
        },
        "boundary": "runtime_probe_only_not_alpha_quality_not_live_readiness_not_operating_promotion",
    }
    kpi = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": SOURCE_VARIANT_ID,
        "python_metrics": python_metrics,
        "onnx_parity": onnx_parity,
        "mt5_records": mt5_records,
        "execution_results": execution_results,
        "external_verification_status": external_status,
        "judgment": judgment,
        "boundary": manifest["boundary"],
    }
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": SOURCE_VARIANT_ID,
        "status": "reviewed" if external_status == "completed" else "blocked",
        "judgment": judgment,
        "external_verification_status": external_status,
        "stage10_11_inheritance": False,
        "stage10_11_baseline": False,
        "python_metrics": python_metrics,
        "onnx_parity": onnx_parity,
        "mt5_kpi_records": mt5_records,
        "ledger_payload": ledger_payload,
        "manifest_path": rel(run_output_root / "run_manifest.json"),
        "kpi_record_path": rel(run_output_root / "kpi_record.json"),
        "result_summary_path": rel(run_output_root / "reports/result_summary.md"),
    }
    write_json(run_output_root / "run_manifest.json", manifest)
    write_json(run_output_root / "kpi_record.json", kpi)
    write_json(summary_path, summary)
    write_reports(run_output_root, source_variant, python_metrics, onnx_parity, mt5_records, external_status)
    update_selection_status(source_variant, mt5_records, external_status)
    update_current_truth(source_variant, mt5_records, external_status, summary_path)
    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": SOURCE_VARIANT_ID,
        "external_verification_status": external_status,
        "onnx_parity_passed": onnx_parity.get("passed"),
        "mt5_kpi_record_count": len(mt5_records),
        "summary_path": rel(summary_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MT5 probe for Stage12 RUN03D top ExtraTrees variant.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--run-output-root", default=str(RUN_ROOT))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    parser.add_argument("--max-hold-bars", type=int, default=12)
    parser.add_argument("--parity-rows", type=int, default=128)
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--mt5-timeout-seconds", type=int, default=300)
    parser.add_argument("--runtime-output-timeout-seconds", type=int, default=600)
    return parser.parse_args()


def main() -> int:
    payload = run(parse_args())
    print(json.dumps(mt5._json_ready(payload), ensure_ascii=False, indent=2))
    return 0 if payload.get("onnx_parity_passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
