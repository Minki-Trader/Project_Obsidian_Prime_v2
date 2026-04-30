from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


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
from foundation.alpha import scout_runner as mt5  # noqa: E402


STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
SOURCE_RUN_ID = "run03B_et_standalone_fwd12_v1"
RUN_ID = "run03C_et_standalone_mt5_runtime_probe_v1"
RUN_NUMBER = "run03C"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesStandaloneMT5Probe"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
THRESHOLD_METHOD = "standalone_validation_nonflat_confidence_q90"
COMMON_RUN_ROOT = f"Project_Obsidian_Prime_v2/stage12/{RUN_ID}"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
DEFAULT_MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
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


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def io(path: Path) -> Path:
    return mt5._io_path(path)


def path_exists(path: Path) -> bool:
    return mt5._path_exists(path)


def sha256_file(path: Path) -> str:
    return mt5.sha256_file(path)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(json.dumps(mt5._json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = False) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def require_standalone_source(summary: Mapping[str, Any], threshold_rule: Mapping[str, Any]) -> None:
    if summary.get("run_id") != SOURCE_RUN_ID:
        raise RuntimeError(f"Unexpected source run: {summary.get('run_id')}")
    if summary.get("standalone_scope") is not True:
        raise RuntimeError("RUN03B source is not marked standalone_scope=true.")
    if summary.get("stage10_11_inheritance") is not False:
        raise RuntimeError("RUN03B source is not marked stage10_11_inheritance=false.")
    if threshold_rule.get("inherited_from_stage10_or_stage11") is not False:
        raise RuntimeError("RUN03B threshold rule is not marked independent from Stage 10/11.")


def format_mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def materialize_tester_set_file(parameters: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    io(output_path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run_stage12_extratrees_standalone_mt5_probe.py"]
    for key, value in parameters.items():
        lines.append(f"{key}={format_mt5_value(value)}")
    io(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "mt5_set",
        "parameter_count": int(len(parameters)),
    }


def common_ref(*parts: str) -> str:
    return "/".join([COMMON_RUN_ROOT, *parts])


def tester_profile_ini_name(split_name: str) -> str:
    split_code = "v" if split_name == "validation_is" else "o"
    return f"opv2_{RUN_NUMBER}_ta_{split_code}.ini"


def materialize_stage12_mt5_attempt(
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
            "InpModelId": f"{RUN_ID}_tier_a_standalone",
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
            "InpMagic": 1203001,
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
        "standalone_scope": True,
        "stage10_11_inheritance": False,
    }


def split_date_range(frame: pd.DataFrame, split_name: str) -> tuple[str, str]:
    split = frame.loc[frame["split"].astype(str).eq(split_name)]
    if split.empty:
        raise RuntimeError(f"Split is empty: {split_name}")
    timestamps = pd.to_datetime(split["timestamp"], utc=True)
    from_date = timestamps.min().strftime("%Y.%m.%d")
    to_date = (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")
    return from_date, to_date


def decision_metrics(frame: pd.DataFrame, probabilities: np.ndarray, threshold: float) -> dict[str, Any]:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    short_ok = (p_short >= threshold) & (p_short >= p_flat) & (p_short >= p_long)
    long_ok = (p_long >= threshold) & (p_long >= p_flat) & (p_long >= p_short)
    decision = np.full(len(frame), 1, dtype="int64")
    decision[short_ok] = 0
    decision[long_ok] = 2
    labels = frame["label_class"].astype("int64").to_numpy()
    signals = np.isin(decision, [0, 2])
    directional_correct = signals & (decision == labels)
    return {
        "rows": int(len(frame)),
        "signal_count": int(signals.sum()),
        "short_count": int((decision == 0).sum()),
        "long_count": int((decision == 2).sum()),
        "signal_coverage": float(signals.mean()) if len(frame) else None,
        "directional_correct_count": int(directional_correct.sum()),
        "directional_hit_rate": float(directional_correct[signals].mean()) if bool(signals.any()) else None,
    }


def build_runtime_decision_frame(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    threshold: float,
    split_label: str,
) -> pd.DataFrame:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    short_ok = (p_short >= threshold) & (p_short >= p_flat) & (p_short >= p_long)
    long_ok = (p_long >= threshold) & (p_long >= p_flat) & (p_long >= p_short)
    decision = np.full(len(frame), 1, dtype="int64")
    decision[short_ok] = 0
    decision[long_ok] = 2
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": split_label,
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "p_short": p_short,
            "p_flat": p_flat,
            "p_long": p_long,
            "decision_class": decision,
            "decision_label": pd.Series(decision).map({0: "short", 1: "flat", 2: "long"}).to_numpy(),
        }
    )


def mt5_metric_by_view(records: Sequence[Mapping[str, Any]], view: str, metric: str) -> Any:
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


def build_blocked_mt5_ledger_rows(
    *,
    execution_results: Sequence[Mapping[str, Any]],
    run_output_root: Path,
    external_status: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in execution_results:
        if result.get("status") == "completed":
            continue
        split = str(result.get("split"))
        view = f"{result.get('record_view_prefix', 'mt5_tier_a_only')}_{split}"
        runtime_outputs = result.get("runtime_outputs", {})
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
                "judgment": "blocked_standalone_extratrees_mt5_runtime_probe",
                "path": (run_output_root / "kpi_record.json").as_posix(),
                "primary_kpi": ledger_pairs(
                    (
                        ("returncode", result.get("returncode")),
                        ("runtime_status", runtime_outputs.get("status") if isinstance(runtime_outputs, Mapping) else None),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("stage10_11_inheritance", False),
                        ("source_run", SOURCE_RUN_ID),
                        ("blocker", result.get("blocker") or (runtime_outputs.get("last_summary", {}) if isinstance(runtime_outputs, Mapping) else {})),
                    )
                ),
                "external_verification_status": external_status,
                "notes": "Stage 12 standalone ExtraTrees MT5 attempt was made, but runtime evidence did not complete.",
            }
        )
    return rows


def boundary_ledger_rows(summary_path: Path) -> list[dict[str, Any]]:
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
            "path": summary_path.as_posix(),
            "primary_kpi": "missing_required=out_of_scope_by_claim",
            "guardrail_kpi": "reason=standalone_mt5_tier_a_only_no_partial_context_fallback_claim",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Required paired-tier record is present as boundary; Tier B was not used in this standalone MT5 probe.",
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
            "path": summary_path.as_posix(),
            "primary_kpi": "missing_required=out_of_scope_by_claim",
            "guardrail_kpi": "reason=no_tier_b_fallback_or_routed_total_claim_in_standalone_run",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Required combined record is present as boundary; no synthetic combined result is claimed.",
        },
    ]


def registry_notes(external_status: str, mt5_kpi_records: Sequence[Mapping[str, Any]]) -> str:
    return ledger_pairs(
        (
            ("source_run", SOURCE_RUN_ID),
            ("standalone_scope", True),
            ("stage10_11_inheritance", False),
            ("comparison_baseline", None),
            ("threshold_method", THRESHOLD_METHOD),
            ("validation_net_profit", mt5_metric_by_view(mt5_kpi_records, "mt5_tier_a_only_validation_is", "net_profit")),
            ("validation_pf", mt5_metric_by_view(mt5_kpi_records, "mt5_tier_a_only_validation_is", "profit_factor")),
            ("validation_trades", mt5_metric_by_view(mt5_kpi_records, "mt5_tier_a_only_validation_is", "trade_count")),
            ("oos_net_profit", mt5_metric_by_view(mt5_kpi_records, "mt5_tier_a_only_oos", "net_profit")),
            ("oos_pf", mt5_metric_by_view(mt5_kpi_records, "mt5_tier_a_only_oos", "profit_factor")),
            ("oos_trades", mt5_metric_by_view(mt5_kpi_records, "mt5_tier_a_only_oos", "trade_count")),
            ("external_verification", external_status),
            ("boundary", "runtime_probe_only"),
        )
    )


def update_ledgers_and_registry(
    *,
    run_output_root: Path,
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    external_status: str,
    summary_path: Path,
) -> dict[str, Any]:
    rows = alpha_run_ledgers.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
        tier_b=TIER_B,
    )
    rows.extend(
        build_blocked_mt5_ledger_rows(
            execution_results=execution_results,
            run_output_root=run_output_root,
            external_status=external_status,
        )
    )
    rows.extend(boundary_ledger_rows(summary_path))
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "standalone_mt5_runtime_probe",
                "status": "reviewed" if external_status == "completed" else "blocked",
                "judgment": (
                    "inconclusive_standalone_extratrees_mt5_runtime_probe_completed"
                    if external_status == "completed"
                    else "blocked_standalone_extratrees_mt5_runtime_probe"
                ),
                "path": rel(run_output_root),
                "notes": registry_notes(external_status, mt5_kpi_records),
            }
        ],
        key="run_id",
    )
    return {
        "stage_run_ledger": stage_payload,
        "project_alpha_run_ledger": project_payload,
        "run_registry": registry_payload,
    }


def metric_text(records: Sequence[Mapping[str, Any]], view: str, metric: str) -> str:
    value = mt5_metric_by_view(records, view, metric)
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "blocked_or_missing(차단 또는 누락)"
    return str(value)


def write_stage12_docs(
    *,
    external_status: str,
    threshold: float,
    python_metrics: Mapping[str, Any],
    onnx_parity: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any] | None,
    run_output_root: Path,
    summary_path: Path,
) -> None:
    validation_view = "mt5_tier_a_only_validation_is"
    oos_view = "mt5_tier_a_only_oos"
    judgment = (
        "inconclusive_standalone_extratrees_mt5_runtime_probe_completed"
        if external_status == "completed"
        else "blocked_standalone_extratrees_mt5_runtime_probe"
    )
    result_summary = f"""# RUN03C Standalone ExtraTrees MT5 Runtime Probe(단독 엑스트라 트리 MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- source model run(원천 모델 실행): `{SOURCE_RUN_ID}`
- standalone scope(단독 범위): `true(참)`
- Stage 10/11 inheritance(Stage 10/11 계승): `false(아님)`
- comparison baseline(비교 기준선): `none(없음)`
- threshold method(임계값 방식): `{THRESHOLD_METHOD}`
- nonflat threshold(비평탄 임계값): `{threshold}`
- ONNX parity(온닉스 동등성): `{onnx_parity.get('passed')}`
- external verification status(외부 검증 상태): `{external_status}`

## Python Replay(파이썬 재현)

| split(분할) | signals(신호) | hit rate(적중률) |
|---|---:|---:|
| validation(검증) | `{python_metrics['validation']['signal_count']}` | `{python_metrics['validation']['directional_hit_rate']}` |
| OOS(표본외) | `{python_metrics['oos']['signal_count']}` | `{python_metrics['oos']['directional_hit_rate']}` |

## MT5 Strategy Tester(MT5 전략 테스터)

| split(분할) | status(상태) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max drawdown(최대 손실) |
|---|---|---:|---:|---:|---:|
| validation(검증) | `{view_status(mt5_kpi_records, validation_view)}` | `{metric_text(mt5_kpi_records, validation_view, 'net_profit')}` | `{metric_text(mt5_kpi_records, validation_view, 'profit_factor')}` | `{metric_text(mt5_kpi_records, validation_view, 'trade_count')}` | `{metric_text(mt5_kpi_records, validation_view, 'max_drawdown_amount')}` |
| OOS(표본외) | `{view_status(mt5_kpi_records, oos_view)}` | `{metric_text(mt5_kpi_records, oos_view, 'net_profit')}` | `{metric_text(mt5_kpi_records, oos_view, 'profit_factor')}` | `{metric_text(mt5_kpi_records, oos_view, 'trade_count')}` | `{metric_text(mt5_kpi_records, oos_view, 'max_drawdown_amount')}` |

## Judgment(판정)

`{judgment}`

효과(effect, 효과): 이 실행은 Stage 12(12단계) 단독 ExtraTrees(엑스트라 트리)를 MT5 runtime_probe(런타임 탐침)로 본 것이다. alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 주장하지 않는다.
"""
    packet = f"""# RUN03C Standalone MT5 Runtime Probe Packet(단독 MT5 런타임 탐침 묶음)

## Intake(인입)

- active stage(활성 단계): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- model family(모델 계열): `{MODEL_FAMILY}`
- standalone guardrail(단독 가드레일): Stage 10/11(10/11단계) threshold/session/context/model surface(임계값/세션/문맥/모델 표면) 미사용

## Evidence(근거)

- ONNX parity passed(온닉스 동등성 통과): `{onnx_parity.get('passed')}`
- MetaEditor compile status(메타에디터 컴파일 상태): `{(compile_payload or {}).get('status')}`
- MT5 external status(MT5 외부 상태): `{external_status}`
- manifest(목록): `{rel(run_output_root / 'run_manifest.json')}`
- KPI record(핵심 성과 지표 기록): `{rel(run_output_root / 'kpi_record.json')}`
- summary(요약): `{rel(summary_path)}`

## Boundary(경계)

Tier A-only(Tier A 단독) standalone runtime_probe(단독 런타임 탐침)이다. Tier B(티어 B)와 Tier A+B combined(Tier A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)` 경계 행으로 남겼다.

효과(effect, 효과): Stage 12(12단계)의 단독 모델 실행 효과를 보되, 라우팅(routing, 라우팅)이나 과거 기준선(baseline, 기준선)을 섞지 않는다.
"""
    selection = f"""# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_standalone_mt5_runtime_probe_open(단독 MT5 런타임 탐침 활성)`
- current run(현재 실행): `{RUN_ID}`
- source Python run(원천 파이썬 실행): `{SOURCE_RUN_ID}`
- current model family(현재 모델 계열): `{MODEL_FAMILY}`
- comparison baseline(비교 기준선): `none(없음)`
- Stage 10/11 inheritance(Stage 10/11 계승): `false(아님)`
- external verification status(외부 검증 상태): `{external_status}`

## RUN03B Standalone Source(RUN03B 단독 원천)

- validation signals(검증 신호): `{python_metrics['validation']['signal_count']}`
- validation hit rate(검증 적중률): `{python_metrics['validation']['directional_hit_rate']}`
- OOS signals(표본외 신호): `{python_metrics['oos']['signal_count']}`
- OOS hit rate(표본외 적중률): `{python_metrics['oos']['directional_hit_rate']}`

## RUN03C MT5 Probe(RUN03C MT5 탐침)

- validation net/PF(검증 순수익/수익 팩터): `{metric_text(mt5_kpi_records, validation_view, 'net_profit')}` / `{metric_text(mt5_kpi_records, validation_view, 'profit_factor')}`
- OOS net/PF(표본외 순수익/수익 팩터): `{metric_text(mt5_kpi_records, oos_view, 'net_profit')}` / `{metric_text(mt5_kpi_records, oos_view, 'profit_factor')}`

효과(effect, 효과): Stage 12(12단계)는 단독 실험으로 유지되고, RUN03C(실행 03C)가 MT5 연결 근거를 담당한다.
"""
    write_text(run_output_root / "reports/result_summary.md", result_summary, bom=True)
    write_text(STAGE_ROOT / "03_reviews/run03C_standalone_mt5_runtime_probe_packet.md", packet, bom=True)
    write_text(STAGE_ROOT / "04_selected/selection_status.md", selection, bom=True)


def update_current_truth_docs(
    *,
    external_status: str,
    threshold: float,
    python_metrics: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    run_output_root: Path,
    summary_path: Path,
) -> None:
    validation_view = "mt5_tier_a_only_validation_is"
    oos_view = "mt5_tier_a_only_oos"
    workspace_path = ROOT / "docs/workspace/workspace_state.yaml"
    workspace_text = io(workspace_path).read_text(encoding="utf-8-sig")
    workspace_text = workspace_text.replace('updated_on: "2026-04-27"', 'updated_on: "2026-04-28"')
    workspace_text = workspace_text.replace(
        '"treat Stage 12 as active standalone ExtraTrees model-family experiment; RUN03A is invalid_for_standalone_scope and RUN03B is the current standalone Python structural scout"',
        '"treat Stage 12 as active standalone(단독) ExtraTrees(엑스트라 트리) MT5 runtime_probe(런타임 탐침); RUN03A is invalid_for_standalone_scope(단독 범위 무효), RUN03B is source Python scout(원천 파이썬 탐침), and RUN03C is current MT5 probe(현재 MT5 탐침)"',
    )
    stage12_block = f"""stage12_model_family_challenge:
  stage_id: "{STAGE_ID}"
  status: "active_standalone_mt5_runtime_probe_open"
  lane: "standalone_mt5_runtime_probe"
  current_run_id: "{RUN_ID}"
  current_run_number: "{RUN_NUMBER}"
  current_run_status: "{'reviewed' if external_status == 'completed' else 'blocked'}"
  current_run_judgment: "{'inconclusive_standalone_extratrees_mt5_runtime_probe_completed' if external_status == 'completed' else 'blocked_standalone_extratrees_mt5_runtime_probe'}"
  current_run_external_verification_status: "{external_status}"
  source_python_run_id: "{SOURCE_RUN_ID}"
  current_run_model_family: "{MODEL_FAMILY}"
  standalone_scope: true
  stage10_11_inheritance: false
  comparison_baseline: null
  scope_correction:
    run_id: "run03A_extratrees_fwd18_inverse_context_scout_v1"
    status: "invalid_for_standalone_scope"
    judgment: "invalid_scope_mismatch_for_requested_standalone_stage12"
    reason: "RUN03A reused Stage 10/11 comparison and Stage 11 context surface, so it is not standalone Stage 12 evidence"
  experiment_controls:
    model_input_dataset_id: "{MODEL_INPUT_DATASET_ID}"
    feature_set_id: "{FEATURE_SET_ID}"
    label_id: "label_v1_fwd12_m5_logret_train_q33_3class"
    threshold_method: "{THRESHOLD_METHOD}"
    nonflat_confidence_threshold: {threshold}
    stage10_threshold_used: false
    stage10_session_slice_used: false
    stage11_lightgbm_surface_used: false
    stage11_fwd18_inverse_context_used: false
  run03b_signal_read:
    tier_a_rows: 46650
    tier_a_signals: 3273
    validation_signals: {python_metrics['validation']['signal_count']}
    validation_directional_hit_rate: {python_metrics['validation']['directional_hit_rate']}
    oos_signals: {python_metrics['oos']['signal_count']}
    oos_directional_hit_rate: {python_metrics['oos']['directional_hit_rate']}
    tier_b_record: "out_of_scope_by_claim_standalone_tier_a_only"
    tier_ab_record: "out_of_scope_by_claim_standalone_tier_a_only"
  run03c_mt5_read:
    validation_status: "{view_status(mt5_kpi_records, validation_view)}"
    validation_net_profit: {json.dumps(mt5_metric_by_view(mt5_kpi_records, validation_view, 'net_profit'))}
    validation_profit_factor: {json.dumps(mt5_metric_by_view(mt5_kpi_records, validation_view, 'profit_factor'))}
    validation_trades: {json.dumps(mt5_metric_by_view(mt5_kpi_records, validation_view, 'trade_count'))}
    oos_status: "{view_status(mt5_kpi_records, oos_view)}"
    oos_net_profit: {json.dumps(mt5_metric_by_view(mt5_kpi_records, oos_view, 'net_profit'))}
    oos_profit_factor: {json.dumps(mt5_metric_by_view(mt5_kpi_records, oos_view, 'profit_factor'))}
    oos_trades: {json.dumps(mt5_metric_by_view(mt5_kpi_records, oos_view, 'trade_count'))}
  run03b_read: "ExtraTrees standalone run produced usable signal density but weak validation and OOS directional hit rates; keep as inconclusive Python structural evidence"
  run03c_read: "Stage 12 standalone ExtraTrees MT5 runtime_probe is {'completed but only runtime_probe evidence' if external_status == 'completed' else 'blocked after external verification attempt'}"
  boundary: "Standalone MT5 runtime_probe only; no alpha quality, no live readiness, no operating promotion"
  stage_brief_path: "stages/12_model_family_challenge__extratrees_training_effect/00_spec/stage_brief.md"
  input_references_path: "stages/12_model_family_challenge__extratrees_training_effect/01_inputs/input_references.md"
  run_manifest_path: "{rel(run_output_root / 'run_manifest.json')}"
  kpi_record_path: "{rel(run_output_root / 'kpi_record.json')}"
  summary_path: "{rel(summary_path)}"
  result_summary_path: "{rel(run_output_root / 'reports/result_summary.md')}"
  run_packet_path: "stages/12_model_family_challenge__extratrees_training_effect/03_reviews/run03C_standalone_mt5_runtime_probe_packet.md"
  scope_correction_path: "stages/12_model_family_challenge__extratrees_training_effect/03_reviews/run03A_scope_correction.md"
  selection_status_path: "stages/12_model_family_challenge__extratrees_training_effect/04_selected/selection_status.md"
"""
    workspace_text = re.sub(
        r"stage12_model_family_challenge:\n.*?\nopen_items:",
        stage12_block + "open_items:",
        workspace_text,
        flags=re.S,
    )
    if "Stage 12 RUN03C" not in workspace_text:
        workspace_text = workspace_text.replace(
            '  - "Stage 12 RUN03B has stage10_11_inheritance=false and is the current standalone run"',
            '  - "Stage 12 RUN03B has stage10_11_inheritance=false and is the source standalone Python run"\n'
            '  - "Stage 12 RUN03C is the current standalone MT5 runtime_probe run"',
        )
    write_text(workspace_path, workspace_text)

    current_path = ROOT / "docs/context/current_working_state.md"
    current_text = io(current_path).read_text(encoding="utf-8-sig")
    current_text = current_text.replace("- updated_on: `2026-04-27`", "- updated_on: `2026-04-28`")
    stage12_md = f"""## 현재 Stage 12 상태(Current Stage 12 State, 현재 Stage 12 상태)

- status(상태): `active_standalone_mt5_runtime_probe_open(단독 MT5 런타임 탐침 활성)`
- current run(현재 실행): `RUN03C(실행 03C)` `{RUN_ID}`
- source Python run(원천 파이썬 실행): `RUN03B(실행 03B)` `{SOURCE_RUN_ID}`
- model family(모델 계열): `ExtraTreesClassifier(엑스트라 트리 분류기)`
- comparison baseline(비교 기준선): `none(없음)`
- standalone input(단독 입력): fwd12(60분) canonical foundation label/split(정식 기반 라벨/분할), 58 feature(58개 피처) MT5 price-proxy model input(MT5 가격 대리 모델 입력)
- non-inheritance guardrail(비계승 가드레일): Stage 10/11(10/11단계) threshold/session/context/model surface(임계값/세션/문맥/모델 표면) 미사용
- external verification status(외부 검증 상태): `{external_status}`

RUN03A(실행 03A)는 Stage 10/11(10/11단계) 비교와 Stage 11(11단계) 문맥 표면을 썼기 때문에 `invalid_for_standalone_scope(단독 범위 무효)`로 낮췄다.

RUN03B(실행 03B)는 Python structural scout(파이썬 구조 탐침) 원천 모델이고, RUN03C(실행 03C)는 그 단독 모델을 MT5 runtime_probe(MT5 런타임 탐침)로 연결한 실행이다.

| split(분할) | Python signals(파이썬 신호) | Python hit rate(파이썬 적중률) | MT5 net/PF(MT5 순수익/수익 팩터) | MT5 trades(MT5 거래 수) |
|---|---:|---:|---:|---:|
| validation(검증) | `{python_metrics['validation']['signal_count']}` | `{python_metrics['validation']['directional_hit_rate']}` | `{metric_text(mt5_kpi_records, validation_view, 'net_profit')}` / `{metric_text(mt5_kpi_records, validation_view, 'profit_factor')}` | `{metric_text(mt5_kpi_records, validation_view, 'trade_count')}` |
| OOS(표본외) | `{python_metrics['oos']['signal_count']}` | `{python_metrics['oos']['directional_hit_rate']}` | `{metric_text(mt5_kpi_records, oos_view, 'net_profit')}` / `{metric_text(mt5_kpi_records, oos_view, 'profit_factor')}` | `{metric_text(mt5_kpi_records, oos_view, 'trade_count')}` |

효과(effect, 효과): Stage 12(12단계)는 단독 ExtraTrees(엑스트라 트리) 실험으로 유지하면서 MT5 Strategy Tester(MT5 전략 테스터) 거래/위험/실행 KPI(핵심 성과 지표)를 보기 시작했다.
"""
    current_text = re.sub(
        r"## 현재 Stage 12 상태\(Current Stage 12 State, 현재 Stage 12 상태\)\n.*?\n## 현재 경계",
        stage12_md + "\n## 현재 경계",
        current_text,
        flags=re.S,
    )
    current_text = current_text.replace(
        "Stage 12(12단계) `RUN03B(실행 03B)`는 ExtraTrees(엑스트라 트리) standalone Python structural scout(단독 파이썬 구조 탐침)이다.",
        "Stage 12(12단계) `RUN03B(실행 03B)`는 ExtraTrees(엑스트라 트리) standalone Python structural scout(단독 파이썬 구조 탐침)이고, `RUN03C(실행 03C)`는 그 모델의 standalone MT5 runtime_probe(단독 MT5 런타임 탐침)이다.",
    )
    current_text = current_text.replace(
        "- Stage 12(12단계)는 열려 있고, `RUN03B(실행 03B)` ExtraTrees(엑스트라 트리)가 현재 standalone structural scout(단독 구조 탐침)이다.",
        "- Stage 12(12단계)는 열려 있고, `RUN03C(실행 03C)` ExtraTrees(엑스트라 트리)가 현재 standalone MT5 runtime_probe(단독 MT5 런타임 탐침)이다.",
    )
    current_text = current_text.replace(
        "- Stage 12(12단계) `RUN03B(실행 03B)` ExtraTrees standalone Python structural scout(엑스트라 트리 단독 파이썬 구조 탐침)를 MT5 runtime evidence(MT5 런타임 근거), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장",
        "- Stage 12(12단계) `RUN03B(실행 03B)` ExtraTrees standalone Python structural scout(엑스트라 트리 단독 파이썬 구조 탐침)를 MT5 runtime evidence(MT5 런타임 근거)로 읽는 주장\n"
        "- Stage 12(12단계) `RUN03C(실행 03C)` standalone MT5 runtime_probe(단독 MT5 런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장",
    )
    write_text(current_path, current_text, bom=True)

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog_text = io(changelog_path).read_text(encoding="utf-8-sig")
    bullet = (
        f"- Stage 12(12단계) `RUN03C(실행 03C)` `{RUN_ID}`를 standalone ExtraTrees MT5 runtime_probe"
        f"(단독 엑스트라 트리 MT5 런타임 탐침)로 실행했다. 효과(effect, 효과)는 RUN03B(실행 03B) 단독 모델을 "
        f"ONNX(온닉스), MT5 feature matrix(MT5 피처 행렬), Strategy Tester(전략 테스터) 근거로 연결하되 "
        f"Stage 10/11(10/11단계) threshold/session/context/baseline(임계값/세션/문맥/기준선)을 쓰지 않게 하는 것이다. "
        f"외부 검증 상태(external verification status, 외부 검증 상태)는 `{external_status}`다.\n"
    )
    if "## 2026-04-28" not in changelog_text:
        changelog_text = changelog_text.replace("# Workspace Changelog\n", "# Workspace Changelog\n\n## 2026-04-28\n\n" + bullet)
    elif RUN_ID not in changelog_text:
        changelog_text = changelog_text.replace("## 2026-04-28\n\n", "## 2026-04-28\n\n" + bullet)
    write_text(changelog_path, changelog_text, bom=True)
