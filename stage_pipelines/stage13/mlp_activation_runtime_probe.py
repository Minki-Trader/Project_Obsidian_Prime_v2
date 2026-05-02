from __future__ import annotations

import argparse
import json
import re
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from pandas.errors import ParserWarning

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    execute_prepared_run,
)
from foundation.models.mlp_activation import activation_drift, activation_scope_gap, activation_summary
from foundation.models.mlp_characteristics import MlpVariantSpec, fit_mlp_variant
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage13.mlp_handoff_support import (
    Stage13HandoffConfig,
    copy_runtime_inputs,
    export_feature_matrices,
    load_context,
    make_no_trade_attempts,
    materialize_models,
    rel,
)


STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04C"
RUN_ID = "run04C_mlp_activation_runtime_probe_v1"
PACKET_ID = "stage13_run04C_mlp_activation_runtime_probe_packet_v1"
EXPLORATION_LABEL = "stage13_MLPActivation__RuntimeProbabilityProxy"
MODEL_FAMILY = "sklearn_mlpclassifier_activation_probe"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_run_baseline_seed_or_reference"
BOUNDARY = "activation_runtime_probe_not_alpha_quality_not_promotion_not_runtime_authority"
NO_TRADE_THRESHOLD = 1.01
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 9
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04C_mlp_activation_runtime_probe_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run04C_mlp_activation_runtime_probe_plan.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_activation_runtime_probe.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
STAGE_BRIEF_PATH = STAGE_ROOT / "00_spec/stage_brief.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_bom(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def activation_probe_spec() -> MlpVariantSpec:
    return MlpVariantSpec(
        variant_id="activation_probe_relu64_l2",
        idea_id="relu_hidden_activation_shape",
        description="Single-hidden-layer ReLU MLP used to inspect dead units, sparsity, and high-activation concentration.",
        hidden_layer_sizes=(64,),
        activation="relu",
        alpha=0.001,
        learning_rate_init=0.001,
        max_iter=110,
        n_iter_no_change=10,
        validation_fraction=0.12,
        random_state=1503,
    )


def write_activation_artifacts(
    *,
    tier_a_activation: Mapping[str, Any],
    tier_b_activation: Mapping[str, Any],
) -> dict[str, Any]:
    root = RUN_ROOT / "activation"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_summary = tier_a_activation["summary"]
    tier_b_summary = tier_b_activation["summary"]
    drift = pd.concat([activation_drift(tier_a_summary), activation_drift(tier_b_summary)], ignore_index=True)
    gap = activation_scope_gap(tier_a_summary, tier_b_summary)
    artifacts: dict[str, Any] = {}
    frames = {
        "tier_a_activation_summary": tier_a_summary,
        "tier_b_activation_summary": tier_b_summary,
        "tier_a_unit_stats": tier_a_activation["unit_stats"],
        "tier_b_unit_stats": tier_b_activation["unit_stats"],
        "activation_drift": drift,
        "tier_activation_gap": gap,
    }
    for name, frame in frames.items():
        path = root / f"{name}.csv"
        frame.to_csv(io_path(path), index=False, encoding="utf-8")
        artifacts[name] = {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}
    summary_payload = {
        "tier_a": tier_a_activation["payload"],
        "tier_b": tier_b_activation["payload"],
        "drift": drift.to_dict(orient="records"),
        "tier_gap": gap.to_dict(orient="records"),
        "metric_boundary": "hidden_activation_structure_only_not_model_quality",
    }
    summary_path = root / "activation_summary.json"
    write_json(summary_path, summary_payload)
    artifacts["activation_summary"] = {"path": rel(summary_path), "rows": 1, "sha256": sha256_file_lf_normalized(summary_path)}
    return {"artifacts": artifacts, "payload": summary_payload}


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "blocked_materialize_only_no_mt5_execution",
        }
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
            "judgment": "blocked_activation_runtime_probe",
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = "inconclusive_activation_runtime_probe_completed" if completed else "blocked_activation_runtime_probe"
    return result


def _truthy_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin({"true", "1", "yes"})


def telemetry_probability_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for execution in result.get("execution_results", []):
        runtime = execution.get("runtime_outputs", {})
        telemetry_path = runtime.get("telemetry_path")
        if not telemetry_path or not Path(str(telemetry_path)).exists():
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ParserWarning)
            frame = pd.read_csv(io_path(Path(str(telemetry_path))), index_col=False)
        cycle = frame.loc[frame["record_type"].astype(str).eq("cycle")].copy()
        if "feature_ready" in cycle:
            cycle = cycle.loc[_truthy_series(cycle["feature_ready"])]
        if "model_ok" in cycle:
            cycle = cycle.loc[_truthy_series(cycle["model_ok"])]
        probs = cycle.loc[:, ["p_short", "p_flat", "p_long"]].apply(pd.to_numeric, errors="coerce").dropna()
        if probs.empty:
            continue
        values = probs.to_numpy(dtype="float64", copy=False)
        clipped = np.clip(values, 1e-12, 1.0)
        entropy = -(clipped * np.log(clipped)).sum(axis=1)
        rows.append(
            {
                "attempt_name": execution.get("attempt_name"),
                "split": execution.get("split"),
                "tier": execution.get("tier"),
                "route_role": execution.get("attempt_role"),
                "rows": int(len(probs)),
                "mean_p_short": float(probs["p_short"].mean()),
                "mean_p_flat": float(probs["p_flat"].mean()),
                "mean_p_long": float(probs["p_long"].mean()),
                "mean_entropy": float(entropy.mean()),
                "mean_max_probability": float(values.max(axis=1).mean()),
                "row_sum_max_abs_error": float(np.abs(values.sum(axis=1) - 1.0).max()),
                "telemetry_path": str(telemetry_path),
            }
        )
    return rows


def write_runtime_probability_artifacts(result: Mapping[str, Any]) -> dict[str, Any]:
    rows = telemetry_probability_rows(result)
    root = RUN_ROOT / "runtime_probability"
    io_path(root).mkdir(parents=True, exist_ok=True)
    csv_path = root / "runtime_probability_summary.csv"
    json_path = root / "runtime_probability_summary.json"
    frame = pd.DataFrame(rows)
    frame.to_csv(io_path(csv_path), index=False, encoding="utf-8")
    payload = {"rows": rows, "boundary": "runtime_probability_proxy_only_not_hidden_activation_export"}
    write_json(json_path, payload)
    return {
        "runtime_probability_summary_csv": {"path": rel(csv_path), "rows": len(rows), "sha256": sha256_file_lf_normalized(csv_path)},
        "runtime_probability_summary_json": {"path": rel(json_path), "rows": len(rows), "sha256": sha256_file_lf_normalized(json_path)},
        "payload": payload,
    }


def activation_ledger_rows(activation_payload: Mapping[str, Any], activation_artifacts: Mapping[str, Any]) -> list[dict[str, Any]]:
    layer_rows = activation_payload["tier_a"]["layers"] + activation_payload["tier_b"]["layers"]
    selected = [row for row in layer_rows if row.get("split") in {"validation", "oos"} and int(row.get("layer_index", 0)) == 1]
    rows: list[dict[str, Any]] = []
    for row in selected:
        scope = str(row["scope"]).lower().replace(" ", "_")
        split = str(row["split"])
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__python_activation_{scope}_{split}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"python_activation_{scope}_{split}",
                "parent_run_id": RUN_ID,
                "record_view": f"python_activation_{scope}_{split}",
                "tier_scope": row["scope"],
                "kpi_scope": "hidden_activation_structure",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": "inconclusive_hidden_activation_structure",
                "path": activation_artifacts["activation_summary"]["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", row.get("rows")),
                        ("dead_units", row.get("dead_unit_count")),
                        ("near_dead_units", row.get("near_dead_unit_count")),
                        ("zero_rate_mean", row.get("zero_rate_mean")),
                        ("active_units_row_mean", row.get("active_units_row_mean")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("high_activation_rate_mean", row.get("high_activation_rate_mean")),
                        ("pre_activation_abs_p95", row.get("pre_activation_abs_p95")),
                        ("boundary", "activation_structure_only"),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": "Python hidden activation structure; not trading evidence or model quality.",
            }
        )
    return rows


def write_ledgers(
    *,
    result: Mapping[str, Any],
    activation_payload: Mapping[str, Any],
    activation_artifacts: Mapping[str, Any],
    runtime_probability_artifacts: Mapping[str, Any],
    context: Mapping[str, Any],
) -> dict[str, Any]:
    rows = activation_ledger_rows(activation_payload, activation_artifacts)
    rows.extend(
        build_mt5_alpha_ledger_rows(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            mt5_kpi_records=result.get("mt5_kpi_records", []),
            run_output_root=Path(rel(RUN_ROOT)),
            external_verification_status=str(result.get("external_verification_status")),
        )
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "activation_runtime_probe",
        "status": "reviewed" if result.get("external_verification_status") == "completed" else "payload_only",
        "judgment": result.get("judgment"),
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("activation_artifact", activation_artifacts["activation_summary"]["path"]),
                ("runtime_probability_artifact", runtime_probability_artifacts["runtime_probability_summary_json"]["path"]),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("no_trade_threshold", NO_TRADE_THRESHOLD),
                ("tier_b_fallback_rows", context["tier_b_context_summary"].get("tier_b_fallback_rows")),
                ("external_verification", result.get("external_verification_status")),
                ("boundary", "activation_runtime_probe_only"),
            )
        ),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def metric_by_view(records: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(record.get("record_view")): record.get("metrics", {}) for record in records}


def _layer_lookup(payload: Mapping[str, Any], scope: str, split: str) -> Mapping[str, Any]:
    for row in payload[scope]["layers"]:
        if row.get("split") == split and int(row.get("layer_index", 0)) == 1:
            return row
    return {}


def build_summary(
    *,
    result: Mapping[str, Any],
    activation_payload: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    runtime_probability_artifacts: Mapping[str, Any],
) -> dict[str, Any]:
    by_view = metric_by_view(result.get("mt5_kpi_records", []))
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
        "no_trade_threshold": NO_TRADE_THRESHOLD,
        "spec": model_artifacts["spec"],
        "onnx_parity": model_artifacts["onnx_parity"],
        "tier_a_validation_activation": _layer_lookup(activation_payload, "tier_a", "validation"),
        "tier_a_oos_activation": _layer_lookup(activation_payload, "tier_a", "oos"),
        "tier_b_validation_activation": _layer_lookup(activation_payload, "tier_b", "validation"),
        "tier_b_oos_activation": _layer_lookup(activation_payload, "tier_b", "oos"),
        "mt5_handoff_validation": by_view.get("mt5_routed_total_validation_is", {}),
        "mt5_handoff_oos": by_view.get("mt5_routed_total_oos", {}),
        "runtime_probability_summary": runtime_probability_artifacts["payload"],
        "failure": result.get("failure"),
    }


def report_markdown(summary: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        f"- no_trade_threshold(무거래 임계값): `{NO_TRADE_THRESHOLD}`",
        "",
        "## Activation Behavior(활성화 동작)",
        "",
        "| scope(범위) | split(분할) | dead units(죽은 유닛) | near-dead units(준죽은 유닛) | zero rate mean(0 비율 평균) | active units mean(활성 유닛 평균) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for key, label in (
        ("tier_a_validation_activation", "Tier A validation"),
        ("tier_a_oos_activation", "Tier A OOS"),
        ("tier_b_validation_activation", "Tier B validation"),
        ("tier_b_oos_activation", "Tier B OOS"),
    ):
        row = summary.get(key, {})
        lines.append(
            f"| {label} | {row.get('split')} | {row.get('dead_unit_count')} | {row.get('near_dead_unit_count')} | {row.get('zero_rate_mean')} | {row.get('active_units_row_mean')} |"
        )
    lines.extend(
        [
            "",
            "## MT5 Runtime Proxy(MT5 런타임 대리값)",
            "",
            "| view(보기) | split(분할) | feature_ready(피처 준비) | model_ok(모델 정상) | trades(거래) |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        lines.append(
            f"| {record.get('record_view')} | {record.get('split')} | {metrics.get('feature_ready_count')} | {metrics.get('model_ok_count')} | {metrics.get('trade_count')} |"
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이번 실행은 MLP(다층 퍼셉트론)의 hidden activation(은닉 활성화) 구조와 MT5(메타트레이더5) probability proxy(확률 대리값) 인계만 확인한다.",
            "alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
        ]
    )
    return "\n".join(lines)


def plan_text() -> str:
    return "\n".join(
        [
            "# RUN04C MLP Activation Runtime Probe Plan",
            "",
            "- hypothesis(가설): ReLU MLP(렐루 다층 퍼셉트론)가 Tier A/B(티어 A/B)와 validation/OOS(검증/표본외)에서 dead unit(죽은 유닛), sparsity(희소성), high activation(높은 활성화) 차이를 보일 수 있다.",
            "- decision_use/comparison(결정 용도/비교): train split(학습 분할)과 Tier A/B(티어 A/B) 구조 단서만 보며 Stage10/11/12(10/11/12단계)는 기준선이 아니다.",
            "- controls(고정값): 58 feature(58개 피처), fwd12 label(60분 라벨), split_v1(분할 v1), no-trade threshold(무거래 임계값) 1.01.",
            "- changed_variables(변경 변수): 관찰 대상이 probability surface(확률 표면)에서 hidden activation(은닉 활성화)으로 바뀐다.",
            "- evidence_plan(근거 계획): activation CSV/JSON(활성화 CSV/JSON), ONNX parity(ONNX 동등성), MT5 Strategy Tester(전략 테스터) 무거래 인계, ledgers(장부).",
        ]
    )


def decision_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-02 Stage 13 MLP Activation Runtime Probe",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "- decision/effect(결정/효과): RUN04C(실행 04C)는 activation behavior(활성화 동작)만 기록하고 RUN04A/B(실행 04A/B)와 겹치지 않는다.",
            "- boundary(경계): activation_runtime_probe_only(활성화 런타임 탐침만)",
        ]
    )


def stage_brief_text() -> str:
    return "\n".join(
        [
            "# Stage 13 MLP Training Effect",
            "",
            "Stage13(13단계)은 MLPClassifier(다층 퍼셉트론 분류기)를 독립 주제로 얕게 탐색한다.",
            "",
            "- independence(독립성): Stage10/11/12(10/11/12단계) run(실행)을 baseline(기준선), seed(씨앗), reference(참고)로 쓰지 않는다.",
            "- depth/runtime boundary(깊이/런타임 경계): MLP(다층 퍼셉트론) 구조와 MT5(메타트레이더5) 좁은 probe(탐침)만 본다.",
            "효과(effect, 효과): 모델 계열 특성만 분리하고 운영 의미를 만들지 않는다.",
        ]
    )


def selection_status_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Stage 13 Selection Status",
            "",
            "## Current Read(현재 판독)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            "- status/depth(상태/깊이): `reviewed_activation_runtime_probe_completed(활성화 런타임 탐침 완료)`",
            "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
            "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
            f"- current run(현재 실행): `{RUN_ID}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "",
            "효과(effect, 효과): MLP(다층 퍼셉트론)의 내부 활성화와 MT5(메타트레이더5) 확률 대리값 인계만 확인한다.",
        ]
    )


def skill_receipts(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    status = "executed" if result.get("external_verification_status") == "completed" else "blocked"
    return {
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "receipts": [
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-experiment-design",
                "status": status,
                "hypothesis": "MLP hidden activation(은닉 활성화) 구조가 split/tier(분할/티어)별 차이를 보일 수 있다.",
                "baseline": "train split(학습 분할) only; no Stage10/11/12 baseline(기준선 없음)",
                "changed_variables": "observation target changed to activation behavior(활성화 동작)",
                "invalid_conditions": "missing activation artifact(활성화 산출물 누락) or missing MT5 handoff(인계 누락)",
                "evidence_plan": [rel(RUN_ROOT / "activation/activation_summary.json"), rel(RUN_ROOT / "run_manifest.json")],
            },
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-runtime-parity",
                "status": status,
                "python_artifact": rel(RUN_ROOT / "models/activation_probe_relu64_l2_tier_a_mlp_58.joblib"),
                "runtime_artifact": rel(RUN_ROOT / "models/activation_probe_relu64_l2_tier_a_mlp_58.onnx"),
                "compared_surface": "ONNX probability parity(확률 동등성) and MT5 no-trade probability proxy(무거래 확률 대리값)",
                "parity_level": "runtime_probe(런타임 탐침)",
                "tester_identity": "MT5 Strategy Tester(전략 테스터) US100 M5",
                "missing_evidence": ["none(없음)"],
                "allowed_claims": ["runtime_probe_completed"],
                "forbidden_claims": ["alpha_quality", "promotion", "runtime_authority"],
            },
            {"packet_id": PACKET_ID, "skill": "obsidian-data-integrity", "status": status, "data_sources_checked": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT], "time_axis_boundary": "Stage04/03 timestamp contract(시간축 계약)", "split_boundary": "train/validation/oos split_v1(학습/검증/표본외)", "leakage_checks": "reviewed model input reused(검토 입력 재사용)", "missing_data_boundary": "Tier B partial context fallback only(부분 문맥 대체만)"},
            {"packet_id": PACKET_ID, "skill": "obsidian-backtest-forensics", "status": status, "tester_report": rel(RUN_ROOT / "mt5/reports"), "tester_settings": rel(RUN_ROOT / "mt5"), "spread_commission_slippage": "tester settings only(테스터 설정만); no performance claim(성과 주장 없음)", "trade_list_identity": "zero-trade no-trade probe(무거래 탐침)", "forensic_gaps": ["none(없음)"]},
            {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": status, "source_inputs": [FEATURE_SET_ID, LABEL_ID], "produced_artifacts": [rel(RUN_ROOT / "activation/activation_summary.json"), rel(RUN_ROOT / "run_manifest.json")], "raw_evidence": [rel(RUN_ROOT / "runtime_probability/runtime_probability_summary.json")], "machine_readable": [rel(RUN_ROOT / "kpi_record.json")], "human_readable": [rel(REVIEW_PATH)], "hashes_or_missing_reasons": "hashes recorded(해시 기록됨)", "lineage_boundary": BOUNDARY},
        ],
    }


def sync_docs(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    write_text_bom(PLAN_PATH, plan_text())
    write_text_bom(REVIEW_PATH, report_markdown(summary, result))
    write_text_bom(DECISION_PATH, decision_text(summary))
    write_text_bom(STAGE_BRIEF_PATH, stage_brief_text())
    write_text_bom(SELECTION_STATUS_PATH, selection_status_text(summary))
    sync_review_index(summary)
    sync_changelog(summary)
    sync_workspace_state(summary)
    sync_current_working_state(summary)


def sync_review_index(summary: Mapping[str, Any]) -> None:
    text = read_text(REVIEW_INDEX_PATH) if REVIEW_INDEX_PATH.exists() else "# Stage 13 Review Index\n"
    line = f"- `{RUN_ID}`: `{summary['judgment']}`, report(보고서) `{rel(REVIEW_PATH)}`"
    if RUN_ID not in text:
        text = text.rstrip() + "\n" + line + "\n"
    write_text_bom(REVIEW_INDEX_PATH, text)


def sync_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    line = (
        f"- 2026-05-02: `{RUN_ID}` {summary['external_verification_status']}. "
        "Stage13(13단계) MLP activation runtime probe(MLP 활성화 런타임 탐침)를 실행했다. "
        "Effect(효과): hidden activation(은닉 활성화)과 MT5 probability proxy(MT5 확률 대리값) 인계만 확인했다."
    )
    if RUN_ID not in text:
        text = text.replace("## 2026-05-02\n\n", "## 2026-05-02\n\n" + line + "\n", 1)
    write_text_bom(CHANGELOG_PATH, text)


def _replace_or_insert_block(text: str, key: str, block: str) -> str:
    pattern = rf"^{re.escape(key)}:\n(?:  .*\n)+"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, block, text, count=1, flags=re.MULTILINE)
    return text.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n", 1)

def sync_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {STAGE_ID}", text, flags=re.MULTILINE)
    text = re.sub(r"status: active_run04A_mlp_characteristic_runtime_probe", "status: active_run04C_mlp_activation_runtime_probe", text)
    text = text.replace("active_run04A_mlp_runtime_probe", "active_run04C_mlp_activation_runtime_probe")
    blocks = {
        "stage13_mlp_characteristic_runtime_probe": (
            "stage13_mlp_characteristic_runtime_probe:\n"
            "  run_id: run04A_mlp_characteristic_runtime_probe_v1\n"
            "  status: completed\n"
            "  judgment: inconclusive_mlp_characteristic_runtime_probe_completed\n"
            "  selected_variant_id: v02_wide_relu_l2\n"
            "  boundary: runtime_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
            "  report_path: stages/13_model_family_challenge__mlp_training_effect/03_reviews/run04A_mlp_characteristic_runtime_probe_packet.md\n"
        ),
        "stage13_mlp_input_geometry_runtime_handoff_probe": (
            "stage13_mlp_input_geometry_runtime_handoff_probe:\n"
            "  run_id: run04B_mlp_input_geometry_runtime_handoff_probe_v1\n"
            "  status: completed\n"
            "  judgment: inconclusive_input_geometry_runtime_handoff_probe_completed\n"
            "  boundary: runtime_handoff_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
            "  report_path: stages/13_model_family_challenge__mlp_training_effect/03_reviews/run04B_mlp_input_geometry_runtime_handoff_probe_packet.md\n"
        ),
        "stage13_mlp_activation_runtime_probe": (
            "stage13_mlp_activation_runtime_probe:\n"
            f"  run_id: {RUN_ID}\n"
            f"  status: {summary['external_verification_status']}\n"
            f"  judgment: {summary['judgment']}\n"
            "  boundary: activation_runtime_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
            f"  report_path: {rel(REVIEW_PATH)}\n"
        ),
    }
    for key, block in blocks.items():
        text = _replace_or_insert_block(text, key, block)
    write_text_bom(WORKSPACE_STATE_PATH, text)


def sync_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_WORKING_STATE_PATH)
    text = re.sub(r"^- current run\(현재 실행\): .*$", f"- current run(현재 실행): `{RUN_ID}`", text, flags=re.MULTILINE)
    latest = "\n".join(
        [
            "## Latest Stage 13 Update(최신 Stage 13 업데이트)",
            "",
            f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, 외부 검증 상태(external verification status, 외부 검증 상태)는 `{summary['external_verification_status']}`다.",
            "",
            "효과(effect, 효과): MLP(다층 퍼셉트론)의 hidden activation(은닉 활성화)과 MT5(메타트레이더5) probability proxy(확률 대리값) 인계만 확인했다.",
            "",
        ]
    )
    start = text.find("## Latest Stage 13 Update")
    end = text.find("## 쉬운 설명", start)
    if start >= 0 and end > start:
        text = text[:start] + latest + text[end:]
    else:
        text = text.replace("## 쉬운 설명", latest + "## 쉬운 설명", 1)
    write_text_bom(CURRENT_WORKING_STATE_PATH, text)


def write_run_files(
    *,
    created_at: str,
    context: Mapping[str, Any],
    spec: MlpVariantSpec,
    activation_payload: Mapping[str, Any],
    activation_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    prepared: Mapping[str, Any],
    result: Mapping[str, Any],
    runtime_probability_artifacts: Mapping[str, Any],
    ledgers: Mapping[str, Any],
) -> dict[str, Any]:
    summary = build_summary(
        result=result,
        activation_payload=activation_payload,
        model_artifacts=model_artifacts,
        runtime_probability_artifacts=runtime_probability_artifacts,
    )
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "boundary": BOUNDARY,
        "spec": spec.payload(),
        "activation_artifacts": activation_artifacts,
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
        "attempts": prepared["attempts"],
        "common_copies": prepared["common_copies"],
        "runtime_probability_artifacts": runtime_probability_artifacts,
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "failure": result.get("failure"),
    }
    kpi = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "activation_and_runtime_probability_proxy",
        "activation": activation_payload,
        "tier_b_context_summary": context["tier_b_context_summary"],
        "runtime_probability": runtime_probability_artifacts["payload"],
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result.get("external_verification_status"),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi)
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(PACKET_ROOT / "ledger_outputs.json", ledgers)
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(created_at, result))
    write_text_bom(RUN_ROOT / "reports/result_summary.md", report_markdown(summary, result))
    write_text_bom(PACKET_ROOT / "work_packet.md", work_packet_markdown(summary, created_at))
    sync_docs(summary, result)
    return summary


def work_packet_markdown(summary: Mapping[str, Any], created_at: str) -> str:
    return "\n".join(
        [
            f"# {PACKET_ID}",
            "",
            f"- created_at_utc(생성 UTC): `{created_at}`",
            "- primary_family(주 작업군): `runtime_backtest(런타임 백테스트)`",
            "- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`",
            "- support_skills(보조 스킬): `experiment-design/data-integrity/backtest-forensics/artifact-lineage(실험 설계/데이터 무결성/백테스트 포렌식/산출물 계보)`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "효과(effect, 효과): hidden activation(은닉 활성화)과 MT5(메타트레이더5) probability proxy(확률 대리값)를 같은 작업 묶음으로 닫는다.",
        ]
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP hidden activation plus MT5 probability proxy probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)

    created_at = utc_now()
    config = Stage13HandoffConfig(
        stage_number=STAGE_NUMBER,
        run_id=RUN_ID,
        exploration_label=EXPLORATION_LABEL,
        run_root=RUN_ROOT,
        no_trade_threshold=NO_TRADE_THRESHOLD,
        min_margin=MIN_MARGIN,
        max_hold_bars=MAX_HOLD_BARS,
    )
    context = load_context()
    spec = activation_probe_spec()
    tier_a_model = fit_mlp_variant(context["tier_a_frame"], context["tier_a_feature_order"], spec)
    tier_b_model = fit_mlp_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_activation = activation_summary(
        model=tier_a_model,
        frame=context["tier_a_frame"],
        feature_order=context["tier_a_feature_order"],
        scope=mt5.TIER_A,
    )
    tier_b_activation = activation_summary(
        model=tier_b_model,
        frame=context["tier_b_training_frame"],
        feature_order=context["tier_b_feature_order"],
        scope=mt5.TIER_B,
    )
    activation_output = write_activation_artifacts(tier_a_activation=tier_a_activation, tier_b_activation=tier_b_activation)
    model_artifacts = materialize_models(
        config=config,
        spec=spec,
        tier_a_model=tier_a_model,
        tier_b_model=tier_b_model,
        tier_a_frame=context["tier_a_frame"],
        tier_b_training_frame=context["tier_b_training_frame"],
        tier_a_feature_order=context["tier_a_feature_order"],
        tier_b_feature_order=context["tier_b_feature_order"],
        artifact_prefix=spec.variant_id,
    )
    feature_matrices = export_feature_matrices(config, context)
    common_copies = copy_runtime_inputs(config=config, model_artifacts=model_artifacts, feature_matrices=feature_matrices)
    prepared = {
        "run_id": RUN_ID,
        "run_root": RUN_ROOT.as_posix(),
        "stage_id": STAGE_ID,
        "source_variant_id": spec.variant_id,
        "attempts": make_no_trade_attempts(
            config=config,
            context=context,
            model_artifacts=model_artifacts,
            feature_matrices=feature_matrices,
            model_id_suffix="activation_probe",
            record_prefix_suffix="activation_proxy",
        ),
        "common_copies": common_copies,
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": context["tier_b_context_summary"],
    }
    result = execute_or_materialize(prepared, args)
    runtime_probability_artifacts = write_runtime_probability_artifacts(result)
    ledgers = write_ledgers(
        result=result,
        activation_payload=activation_output["payload"],
        activation_artifacts=activation_output["artifacts"],
        runtime_probability_artifacts=runtime_probability_artifacts,
        context=context,
    )
    summary = write_run_files(
        created_at=created_at,
        context=context,
        spec=spec,
        activation_payload=activation_output["payload"],
        activation_artifacts=activation_output["artifacts"],
        model_artifacts=model_artifacts,
        feature_matrices=feature_matrices,
        prepared=prepared,
        result=result,
        runtime_probability_artifacts=runtime_probability_artifacts,
        ledgers=ledgers,
    )
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "materialize_only": bool(args.materialize_only), "summary": summary})
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
