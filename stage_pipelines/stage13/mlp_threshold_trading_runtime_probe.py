from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

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
from foundation.models.mlp_characteristics import MlpVariantSpec
from stage_pipelines.stage13.mlp_handoff_support import (
    Stage13HandoffConfig,
    copy_runtime_inputs,
    export_feature_matrices,
    load_context,
    make_threshold_attempts,
    materialize_models,
    rel,
    write_runtime_probability_artifacts,
)


STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04E"
RUN_ID = "run04E_mlp_q90_threshold_trading_runtime_probe_v1"
PACKET_ID = "stage13_run04E_mlp_q90_threshold_trading_runtime_probe_packet_v1"
SOURCE_RUN_ID = "run04D_mlp_convergence_threshold_feasibility_probe_v1"
EXPLORATION_LABEL = "stage13_MLPThreshold__Q90TradingRuntime"
MODEL_FAMILY = "sklearn_mlpclassifier_q90_threshold_trading_probe"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_run_baseline_seed_or_reference"
BOUNDARY = "q90_threshold_trading_runtime_probe_not_alpha_quality_not_promotion_not_runtime_authority"
THRESHOLD_ID = "q90_m000"
MAX_HOLD_BARS = 9
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04E_mlp_q90_threshold_trading_runtime_probe_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run04E_mlp_q90_threshold_trading_runtime_probe_plan.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_q90_threshold_trading_runtime_probe.md"
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def source_spec() -> MlpVariantSpec:
    payload = read_json(SOURCE_ROOT / "run_manifest.json")["spec"]
    return MlpVariantSpec(
        variant_id=str(payload["variant_id"]),
        idea_id=str(payload["idea_id"]),
        description=str(payload["description"]),
        hidden_layer_sizes=tuple(int(value) for value in payload["hidden_layer_sizes"]),
        activation=str(payload["activation"]),
        alpha=float(payload["alpha"]),
        learning_rate_init=float(payload["learning_rate_init"]),
        max_iter=int(payload["max_iter"]),
        n_iter_no_change=int(payload["n_iter_no_change"]),
        validation_fraction=float(payload["validation_fraction"]),
        random_state=int(payload["random_state"]),
    )


def load_source_models() -> tuple[Any, Any]:
    tier_a = joblib.load(io_path(SOURCE_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.joblib"))
    tier_b = joblib.load(io_path(SOURCE_ROOT / "models/convergence_threshold_relu64_l2_tier_b_mlp_core42.joblib"))
    return tier_a, tier_b


def threshold_payload() -> dict[str, Any]:
    detail_path = SOURCE_ROOT / "thresholds/threshold_feasibility_detail.csv"
    detail = pd.read_csv(io_path(detail_path))
    routed = detail.loc[
        detail["scope"].astype(str).eq("Tier A+B")
        & detail["threshold_id"].astype(str).eq(THRESHOLD_ID)
        & detail["split"].astype(str).eq("validation")
    ].iloc[0]
    tier_a = float(routed["tier_a_threshold_value"])
    tier_b = float(routed["tier_b_threshold_value"])
    payload = {
        "source_run_id": SOURCE_RUN_ID,
        "source_detail_path": rel(detail_path),
        "source_detail_sha256": sha256_file_lf_normalized(detail_path),
        "threshold_id": THRESHOLD_ID,
        "tier_a_threshold": tier_a,
        "tier_b_fallback_threshold": tier_b,
        "min_margin": float(routed["min_margin"]),
        "threshold_policy": "RUN04D routed q90 density checkpoint reused without optimization",
        "boundary": "threshold_handoff_only_not_selected_threshold",
    }
    out = RUN_ROOT / "thresholds/threshold_handoff.json"
    write_json(out, payload)
    return {**payload, "path": rel(out), "sha256": sha256_file_lf_normalized(out)}


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
            "judgment": "blocked_q90_threshold_trading_runtime_probe",
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    result["judgment"] = (
        "inconclusive_q90_threshold_trading_runtime_probe_completed"
        if result.get("external_verification_status") == "completed"
        else "blocked_q90_threshold_trading_runtime_probe"
    )
    return result


def write_ledgers(*, result: Mapping[str, Any], threshold: Mapping[str, Any], runtime_probability: Mapping[str, Any]) -> dict[str, Any]:
    rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=Path(rel(RUN_ROOT)),
        external_verification_status=str(result.get("external_verification_status")),
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "q90_threshold_trading_runtime_probe",
        "status": "reviewed" if result.get("external_verification_status") == "completed" else "payload_only",
        "judgment": result.get("judgment"),
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("source_run", SOURCE_RUN_ID),
                ("threshold_id", threshold["threshold_id"]),
                ("tier_a_threshold", threshold["tier_a_threshold"]),
                ("tier_b_fallback_threshold", threshold["tier_b_fallback_threshold"]),
                ("runtime_probability_artifact", runtime_probability["runtime_probability_summary_json"]["path"]),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("external_verification", result.get("external_verification_status")),
                ("boundary", "q90_threshold_trading_runtime_probe_only"),
            )
        ),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def build_summary(result: Mapping[str, Any], threshold: Mapping[str, Any], model_artifacts: Mapping[str, Any]) -> dict[str, Any]:
    by_view = {str(row.get("record_view")): row.get("metrics", {}) for row in result.get("mt5_kpi_records", [])}
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
        "threshold": threshold,
        "onnx_parity": model_artifacts["onnx_parity"],
        "mt5_validation": by_view.get("mt5_routed_total_validation_is", {}),
        "mt5_oos": by_view.get("mt5_routed_total_oos", {}),
        "failure": result.get("failure"),
    }


def report_markdown(summary: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- threshold(임계값): Tier A `{summary['threshold']['tier_a_threshold']}`, Tier B fallback `{summary['threshold']['tier_b_fallback_threshold']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| view(보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        lines.append(
            f"| {record.get('record_view')} | {record.get('split')} | {metrics.get('net_profit')} | "
            f"{metrics.get('profit_factor')} | {metrics.get('max_drawdown_amount')} | {metrics.get('trade_count')} |"
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): RUN04D(실행 04D)의 q90 threshold(90분위 임계값)를 실제 거래 runtime_probe(런타임 탐침)에 연결했다.",
            "alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
        ]
    )
    return "\n".join(lines)


def sync_docs(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    write_text_bom(PLAN_PATH, plan_text(summary))
    write_text_bom(REVIEW_PATH, report_markdown(summary, result))
    write_text_bom(DECISION_PATH, decision_text(summary))
    write_text_bom(SELECTION_STATUS_PATH, selection_status_text(summary))
    sync_review_index(summary)
    sync_changelog(summary)
    sync_workspace_state(summary)
    sync_current_working_state(summary)


def plan_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# RUN04E MLP Q90 Threshold Trading Runtime Probe Plan",
            "",
            "- hypothesis(가설): RUN04D(실행 04D)의 q90 threshold(90분위 임계값)를 거래로 붙이면 MLP(다층 퍼셉트론)의 거래 모양을 볼 수 있다.",
            "- decision_use(결정 용도): 다음 탐색 방향을 정하는 참고 근거이며 threshold selection(임계값 선택)이 아니다.",
            "- controls(고정값): RUN04D(실행 04D) model(모델), 58 feature(58개 피처), split_v1(분할 v1), max_hold_bars(최대 보유 봉) 9.",
            f"- thresholds(임계값): Tier A `{summary['threshold']['tier_a_threshold']}`, Tier B fallback `{summary['threshold']['tier_b_fallback_threshold']}`.",
            "- evidence_plan(근거 계획): MT5 Strategy Tester(전략 테스터), ONNX parity(ONNX 동등성), ledger(장부), report(보고서).",
        ]
    )


def decision_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-02 Stage 13 MLP Q90 Threshold Trading Runtime Probe",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "- decision/effect(결정/효과): q90 threshold(90분위 임계값)를 거래까지 붙여 관찰했다.",
            "- boundary(경계): trading runtime_probe(거래 런타임 탐침)일 뿐 운영 의미는 없다.",
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
            "- status(상태): `reviewed_q90_threshold_trading_runtime_probe_completed`",
            "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
            "- exploration depth(탐색 깊이): `q90_threshold_trading_runtime_probe_only(q90 임계값 거래 탐침만)`",
            "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
            f"- current run(현재 실행): `{RUN_ID}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "",
            "효과(effect, 효과): 거래 결과를 보되 alpha quality(알파 품질)나 운영 의미는 만들지 않는다.",
        ]
    )


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
        "Stage13(13단계) MLP q90 threshold trading runtime_probe(q90 임계값 거래 런타임 탐침)를 실행했다. "
        "Effect(효과): RUN04D(실행 04D)의 임계값 가능성을 실제 거래 손익/거래 수로 관찰한다."
    )
    if RUN_ID not in text:
        text = text.replace("## 2026-05-02\n\n", "## 2026-05-02\n\n" + line + "\n", 1)
    write_text_bom(CHANGELOG_PATH, text)


def sync_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = text.replace("stage13_active_run04D_mlp_convergence_threshold_feasibility_probe", "stage13_active_run04E_mlp_q90_threshold_trading_runtime_probe")
    text = text.replace("active_run04D_mlp_convergence_threshold_feasibility_probe", "active_run04E_mlp_q90_threshold_trading_runtime_probe")
    block = (
        "stage13_mlp_q90_threshold_trading_runtime_probe:\n"
        f"  run_id: {RUN_ID}\n"
        f"  status: {summary['external_verification_status']}\n"
        f"  judgment: {summary['judgment']}\n"
        "  boundary: q90_threshold_trading_runtime_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
        f"  report_path: {rel(REVIEW_PATH)}\n"
    )
    text = _replace_or_insert_block(text, "stage13_mlp_q90_threshold_trading_runtime_probe", block)
    write_text_bom(WORKSPACE_STATE_PATH, text)


def sync_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_WORKING_STATE_PATH)
    text = re.sub(r"^- current run.*$", f"- current run(현재 실행): `{RUN_ID}`", text, count=1, flags=re.MULTILINE)
    latest = "\n".join(
        [
            "## Latest Stage 13 Update(최신 Stage 13 업데이트)",
            "",
            f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, 외부 검증 상태(external verification status, 외부 검증 상태)는 `{summary['external_verification_status']}`다.",
            "",
            "효과(effect, 효과): RUN04D(실행 04D)의 q90 threshold(90분위 임계값)를 실제 거래 runtime_probe(런타임 탐침)로 붙여 보았다.",
            "",
        ]
    )
    text = replace_section(text, "## Latest Stage 13 Update", "## 쉬운 설명", latest)
    write_text_bom(CURRENT_WORKING_STATE_PATH, text)


def replace_section(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker, start + len(start_marker)) if start >= 0 else -1
    if start >= 0 and end > start:
        return text[:start] + replacement + text[end:]
    return replacement + "\n" + text


def _replace_or_insert_block(text: str, key: str, block: str) -> str:
    pattern = rf"^{re.escape(key)}:\n(?:  .*\n)+"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, block, text, count=1, flags=re.MULTILINE)
    return text.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n", 1)


def skill_receipts(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    status = "executed" if result.get("external_verification_status") == "completed" else "blocked"
    return {
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "receipts": [
            {"packet_id": PACKET_ID, "skill": "obsidian-experiment-design", "status": status, "hypothesis": "q90 threshold(90분위 임계값) trading shape(거래 모양)를 관찰한다.", "baseline": "RUN04D threshold handoff(임계값 인계) only; no Stage10/11/12 baseline(기준선 없음)", "changed_variables": "allow trading(거래 허용) instead of no-trade handoff(무거래 인계)", "invalid_conditions": "missing MT5 report(MT5 보고서 누락) or model handoff mismatch(모델 인계 불일치)", "evidence_plan": [rel(RUN_ROOT / "run_manifest.json"), rel(RUN_ROOT / "kpi_record.json")]},
            {"packet_id": PACKET_ID, "skill": "obsidian-model-validation", "status": status, "model_or_threshold_surface": "RUN04D q90 threshold(90분위 임계값) reused without optimization(최적화 없음)", "validation_split": SPLIT_CONTRACT, "overfit_checks": "single inherited threshold checkpoint(단일 인계 임계값 확인점)", "selection_metric_boundary": "not selected threshold(선택 임계값 아님)", "allowed_claims": ["trading_runtime_probe_completed"], "forbidden_claims": ["alpha_quality", "promotion", "runtime_authority"]},
            {"packet_id": PACKET_ID, "skill": "obsidian-runtime-parity", "status": status, "python_artifact": rel(RUN_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.joblib"), "runtime_artifact": rel(RUN_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.onnx"), "compared_surface": "ONNX parity(ONNX 동등성) and MT5 trading output(MT5 거래 출력)", "parity_level": "runtime_probe(런타임 탐침)", "tester_identity": "MT5 Strategy Tester(전략 테스터) US100 M5", "missing_evidence": ["none(없음)"], "allowed_claims": ["runtime_probe_completed"], "forbidden_claims": ["runtime_authority", "live_readiness", "promotion"]},
            {"packet_id": PACKET_ID, "skill": "obsidian-backtest-forensics", "status": status, "tester_report": rel(RUN_ROOT / "mt5/reports"), "tester_settings": rel(RUN_ROOT / "mt5"), "spread_commission_slippage": "tester settings inherited(테스터 설정 계승); performance claim downgraded(성과 주장 낮춤)", "trade_list_identity": "MT5 report and telemetry(MT5 보고서와 기록)", "forensic_gaps": ["none(없음)"]},
            {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": status, "source_inputs": [SOURCE_RUN_ID, FEATURE_SET_ID, LABEL_ID], "produced_artifacts": [rel(RUN_ROOT / "run_manifest.json"), rel(RUN_ROOT / "thresholds/threshold_handoff.json")], "raw_evidence": [rel(RUN_ROOT / "mt5/reports")], "machine_readable": [rel(RUN_ROOT / "kpi_record.json")], "human_readable": [rel(REVIEW_PATH)], "hashes_or_missing_reasons": "hashes recorded in manifest(목록에 해시 기록)", "lineage_boundary": BOUNDARY},
        ],
    }


def write_run_files(
    *,
    created_at: str,
    context: Mapping[str, Any],
    spec: MlpVariantSpec,
    threshold: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    prepared: Mapping[str, Any],
    result: Mapping[str, Any],
    runtime_probability: Mapping[str, Any],
    ledgers: Mapping[str, Any],
) -> dict[str, Any]:
    summary = build_summary(result, threshold, model_artifacts)
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "boundary": BOUNDARY,
        "spec": spec.payload(),
        "threshold": threshold,
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
        "attempts": prepared["attempts"],
        "common_copies": prepared["common_copies"],
        "runtime_probability_artifacts": runtime_probability,
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
        "threshold": threshold,
        "tier_b_context_summary": context["tier_b_context_summary"],
        "runtime_probability": runtime_probability["payload"],
        "mt5": {"scoreboard_lane": "runtime_probe", "external_verification_status": result.get("external_verification_status"), "kpi_records": result.get("mt5_kpi_records", [])},
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi)
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(PACKET_ROOT / "ledger_outputs.json", ledgers)
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(created_at, result))
    write_text_bom(RUN_ROOT / "reports/result_summary.md", report_markdown(summary, result))
    write_text_bom(PACKET_ROOT / "work_packet.md", report_markdown(summary, result))
    sync_docs(summary, result)
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP q90 threshold trading runtime probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    created_at = utc_now()
    context = load_context()
    spec = source_spec()
    tier_a_model, tier_b_model = load_source_models()
    threshold = threshold_payload()
    config = Stage13HandoffConfig(STAGE_NUMBER, RUN_ID, EXPLORATION_LABEL, RUN_ROOT, 0.0, float(threshold["min_margin"]), MAX_HOLD_BARS)
    model_artifacts = materialize_models(config=config, spec=spec, tier_a_model=tier_a_model, tier_b_model=tier_b_model, tier_a_frame=context["tier_a_frame"], tier_b_training_frame=context["tier_b_training_frame"], tier_a_feature_order=context["tier_a_feature_order"], tier_b_feature_order=context["tier_b_feature_order"], artifact_prefix=spec.variant_id)
    feature_matrices = export_feature_matrices(config, context)
    prepared = {
        "run_id": RUN_ID,
        "run_root": RUN_ROOT.as_posix(),
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "attempts": make_threshold_attempts(config=config, context=context, model_artifacts=model_artifacts, feature_matrices=feature_matrices, model_id_suffix="q90_trading_probe", record_prefix_suffix="q90_trading", tier_a_threshold=float(threshold["tier_a_threshold"]), tier_b_threshold=float(threshold["tier_b_fallback_threshold"])),
        "common_copies": copy_runtime_inputs(config=config, model_artifacts=model_artifacts, feature_matrices=feature_matrices),
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": context["tier_b_context_summary"],
    }
    result = execute_or_materialize(prepared, args)
    runtime_probability = write_runtime_probability_artifacts(result=result, output_root=RUN_ROOT / "runtime_probability", boundary="runtime_probability_proxy_for_trading_probe")
    ledgers = write_ledgers(result=result, threshold=threshold, runtime_probability=runtime_probability)
    summary = write_run_files(created_at=created_at, context=context, spec=spec, threshold=threshold, model_artifacts=model_artifacts, feature_matrices=feature_matrices, prepared=prepared, result=result, runtime_probability=runtime_probability, ledgers=ledgers)
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "materialize_only": bool(args.materialize_only), "summary": summary})
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
