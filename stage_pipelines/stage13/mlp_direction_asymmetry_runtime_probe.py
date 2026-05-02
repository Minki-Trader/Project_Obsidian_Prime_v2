from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.mlp_characteristics import MlpVariantSpec
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage13.mlp_handoff_support import (
    Stage13HandoffConfig,
    copy_runtime_inputs,
    export_feature_matrices,
    load_context,
    materialize_models,
    rel,
    write_runtime_probability_artifacts,
)


STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04F"
RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
PACKET_ID = "stage13_run04F_mlp_direction_asymmetry_runtime_probe_packet_v1"
SOURCE_RUN_ID = "run04E_mlp_q90_threshold_trading_runtime_probe_v1"
THRESHOLD_SOURCE_RUN_ID = "run04D_mlp_convergence_threshold_feasibility_probe_v1"
EXPLORATION_LABEL = "stage13_MLPDirection__TierALongShortAsymmetry"
MODEL_FAMILY = "sklearn_mlpclassifier_direction_asymmetry_probe"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_run_baseline_seed_or_reference"
BOUNDARY = "direction_asymmetry_runtime_probe_not_alpha_quality_not_promotion_not_runtime_authority"
THRESHOLD_ID = "q90_m000"
NO_SIGNAL_THRESHOLD = 1.01
MAX_HOLD_BARS = 9
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04F_mlp_direction_asymmetry_runtime_probe_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run04F_mlp_direction_asymmetry_runtime_probe_plan.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_direction_asymmetry_runtime_probe.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
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
    source = read_json(SOURCE_ROOT / "thresholds/threshold_handoff.json")
    out = {
        "source_run_id": SOURCE_RUN_ID,
        "threshold_source_run_id": THRESHOLD_SOURCE_RUN_ID,
        "threshold_id": THRESHOLD_ID,
        "tier_a_threshold": float(source["tier_a_threshold"]),
        "tier_b_fallback_threshold": float(source["tier_b_fallback_threshold"]),
        "no_signal_threshold": NO_SIGNAL_THRESHOLD,
        "min_margin": float(source["min_margin"]),
        "threshold_policy": "RUN04E q90 threshold reused for Tier A direction asymmetry without optimization",
        "boundary": "direction_asymmetry_only_not_selected_threshold",
    }
    path = RUN_ROOT / "thresholds/threshold_handoff.json"
    write_json(path, out)
    return {**out, "path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def make_direction_attempts(
    *,
    config: Stage13HandoffConfig,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    threshold: Mapping[str, Any],
) -> list[dict[str, Any]]:
    common = common_run_root(config.stage_number, config.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    specs = (
        ("tier_a_long_only", "long_only", NO_SIGNAL_THRESHOLD, float(threshold["tier_a_threshold"])),
        ("tier_a_short_only", "short_only", float(threshold["tier_a_threshold"]), NO_SIGNAL_THRESHOLD),
        ("tier_a_both_no_fallback", "both_no_fallback", float(threshold["tier_a_threshold"]), float(threshold["tier_a_threshold"])),
    )
    attempts: list[dict[str, Any]] = []
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": config.run_root,
            "run_id": config.run_id,
            "stage_number": config.stage_number,
            "exploration_label": config.exploration_label,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": config.max_hold_bars,
            "common_root": common,
        }
        for attempt_name, view_suffix, short_threshold, long_threshold in specs:
            attempts.append(
                attempt_payload(
                    **common_kwargs,
                    attempt_name=f"{attempt_name}_{runtime_split}",
                    tier=mt5.TIER_A,
                    model_path=f"{common}/models/{tier_a_model}",
                    model_id=f"{RUN_ID}_tier_a_{view_suffix}",
                    feature_path=f"{common}/features/{matrix}",
                    feature_count=len(context["tier_a_feature_order"]),
                    feature_order_hash=context["tier_a_feature_order_hash"],
                    short_threshold=short_threshold,
                    long_threshold=long_threshold,
                    min_margin=config.min_margin,
                    invert_signal=False,
                    primary_active_tier="tier_a",
                    attempt_role="tier_only_total",
                    record_view_prefix=f"mt5_tier_a_{view_suffix}",
                )
            )
    return attempts


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
            "judgment": "blocked_direction_asymmetry_runtime_probe",
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    result["judgment"] = (
        "inconclusive_direction_asymmetry_runtime_probe_completed"
        if result.get("external_verification_status") == "completed"
        else "blocked_direction_asymmetry_runtime_probe"
    )
    return result


def scope_boundary_rows(threshold: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for scope in (mt5.TIER_B, mt5.TIER_AB):
        suffix = scope.lower().replace(" ", "_").replace("+", "b")
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__direction_scope_{suffix}_out_of_scope",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"direction_scope_{suffix}_out_of_scope",
                "parent_run_id": RUN_ID,
                "record_view": f"direction_scope_{suffix}_out_of_scope",
                "tier_scope": scope,
                "kpi_scope": "claim_scope_boundary",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": "out_of_scope_by_claim_direction_asymmetry",
                "path": threshold["path"],
                "primary_kpi": ledger_pairs((("threshold_id", threshold["threshold_id"]), ("source_run", SOURCE_RUN_ID))),
                "guardrail_kpi": ledger_pairs((("boundary", "tier_a_only_direction_asymmetry"),)),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": "RUN04F intentionally isolates Tier A direction; Tier B/routed damage was observed in RUN04E.",
            }
        )
    return rows


def write_ledgers(*, result: Mapping[str, Any], threshold: Mapping[str, Any], runtime_probability: Mapping[str, Any]) -> dict[str, Any]:
    rows = scope_boundary_rows(threshold)
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
        "lane": "direction_asymmetry_runtime_probe",
        "status": "reviewed" if result.get("external_verification_status") == "completed" else "payload_only",
        "judgment": result.get("judgment"),
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("source_run", SOURCE_RUN_ID),
                ("threshold_id", threshold["threshold_id"]),
                ("tier_a_threshold", threshold["tier_a_threshold"]),
                ("views", "tier_a_long_only;tier_a_short_only;tier_a_both_no_fallback"),
                ("runtime_probability_artifact", runtime_probability["runtime_probability_summary_json"]["path"]),
                ("external_verification", result.get("external_verification_status")),
                ("boundary", "direction_asymmetry_runtime_probe_only"),
            )
        ),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def build_summary(result: Mapping[str, Any], threshold: Mapping[str, Any], model_artifacts: Mapping[str, Any]) -> dict[str, Any]:
    by_view = {str(row.get("record_view")): row.get("metrics", {}) for row in result.get("mt5_kpi_records", [])}
    views = (
        "mt5_tier_a_long_only",
        "mt5_tier_a_short_only",
        "mt5_tier_a_both_no_fallback",
    )
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
        "views": {view: {"validation": by_view.get(f"{view}_validation_is", {}), "oos": by_view.get(f"{view}_oos", {})} for view in views},
        "failure": result.get("failure"),
    }


def report_markdown(summary: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- threshold(임계값): Tier A `{summary['threshold']['tier_a_threshold']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| view(보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래) | long/short(롱/숏) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {})
        lines.append(
            f"| {record.get('record_view')} | {record.get('split')} | {metrics.get('net_profit')} | "
            f"{metrics.get('profit_factor')} | {metrics.get('max_drawdown_amount')} | {metrics.get('trade_count')} | "
            f"{metrics.get('long_trade_count')}/{metrics.get('short_trade_count')} |"
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): RUN04E(실행 04E)의 q90 threshold(90분위 임계값)를 Tier A(티어 A) 방향별로 분해했다.",
            "Tier B(티어 B)와 routed total(라우팅 전체)은 이번 주장 범위 밖(out_of_scope_by_claim, 주장 범위 밖)이다.",
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
            "# RUN04F MLP Direction Asymmetry Runtime Probe Plan",
            "",
            "- hypothesis(가설): RUN04E(실행 04E)의 손상은 Tier A(티어 A) 안에서도 long/short(롱/숏) 비대칭으로 설명될 수 있다.",
            "- decision_use(결정 용도): q90 threshold(q90 임계값)를 더 튜닝할지, 다른 MLP(다층 퍼셉트론) 가설로 갈지 정하는 참고 근거다.",
            "- comparison_baseline(비교 기준): 같은 모델/같은 threshold(임계값)에서 long-only(롱 전용), short-only(숏 전용), both no-fallback(양방향 대체 없음)을 비교한다.",
            "- controls(고정값): RUN04E(실행 04E) model(모델), Tier A feature matrix(Tier A 피처 행렬), q90 threshold(q90 임계값), max_hold_bars(최대 보유 봉) 9.",
            f"- threshold(임계값): `{summary['threshold']['tier_a_threshold']}`.",
            "- evidence_plan(근거 계획): MT5 Strategy Tester(전략 테스터), ONNX parity(ONNX 동등성), ledger(장부), report(보고서).",
        ]
    )


def decision_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-02 Stage 13 MLP Direction Asymmetry Runtime Probe",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "- decision/effect(결정/효과): RUN04E(실행 04E)의 거래 결과를 Tier A(티어 A) 방향별로 분해했다.",
            "- boundary(경계): direction asymmetry runtime_probe(방향 비대칭 런타임 탐침)일 뿐 운영 의미는 없다.",
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
            "- status(상태): `reviewed_direction_asymmetry_runtime_probe_completed`",
            "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
            "- exploration depth(탐색 깊이): `direction_asymmetry_runtime_probe_only(방향 비대칭 런타임 탐침만)`",
            "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
            f"- current run(현재 실행): `{RUN_ID}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "",
            "효과(effect, 효과): 방향별 거래 모양을 보되 alpha quality(알파 품질)나 운영 의미는 만들지 않는다.",
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
        "Stage13(13단계) MLP direction asymmetry runtime_probe(방향 비대칭 런타임 탐침)를 실행했다. "
        "Effect(효과): RUN04E(실행 04E)의 q90 threshold(q90 임계값)를 Tier A(티어 A) long/short(롱/숏)로 분해한다."
    )
    if RUN_ID not in text:
        text = text.replace("## 2026-05-02\n\n", "## 2026-05-02\n\n" + line + "\n", 1)
    write_text_bom(CHANGELOG_PATH, text)


def sync_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = text.replace("stage13_active_run04E_mlp_q90_threshold_trading_runtime_probe", "stage13_active_run04F_mlp_direction_asymmetry_runtime_probe")
    text = text.replace("active_run04E_mlp_q90_threshold_trading_runtime_probe", "active_run04F_mlp_direction_asymmetry_runtime_probe")
    block = (
        "stage13_mlp_direction_asymmetry_runtime_probe:\n"
        f"  run_id: {RUN_ID}\n"
        f"  status: {summary['external_verification_status']}\n"
        f"  judgment: {summary['judgment']}\n"
        "  boundary: direction_asymmetry_runtime_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
        f"  report_path: {rel(REVIEW_PATH)}\n"
    )
    text = _replace_or_insert_block(text, "stage13_mlp_direction_asymmetry_runtime_probe", block)
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
            "효과(effect, 효과): q90 threshold(q90 임계값)를 Tier A(티어 A) long-only/short-only/both no-fallback(롱 전용/숏 전용/양방향 대체 없음)으로 나눠 봤다.",
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
            {"packet_id": PACKET_ID, "skill": "obsidian-experiment-design", "status": status, "hypothesis": "Tier A(티어 A) q90 threshold(q90 임계값)의 long/short(롱/숏) 비대칭을 관찰한다.", "baseline": "RUN04E q90 threshold trading probe(RUN04E q90 거래 탐침)", "changed_variables": "direction permission(방향 허용) only: long-only/short-only/both", "invalid_conditions": "missing MT5 report(MT5 보고서 누락) or direction thresholds not applied(방향 임계값 미적용)", "evidence_plan": [rel(RUN_ROOT / "run_manifest.json"), rel(RUN_ROOT / "kpi_record.json")]},
            {"packet_id": PACKET_ID, "skill": "obsidian-model-validation", "status": status, "model_or_threshold_surface": "RUN04E q90 threshold(q90 임계값) reused without optimization(최적화 없음)", "validation_split": SPLIT_CONTRACT, "overfit_checks": "post-hoc decomposition(사후 분해) only; no selection claim(선택 주장 없음)", "selection_metric_boundary": "not selected threshold or selected direction(선택 임계값/방향 아님)", "allowed_claims": ["direction_asymmetry_observed"], "forbidden_claims": ["alpha_quality", "promotion", "runtime_authority"]},
            {"packet_id": PACKET_ID, "skill": "obsidian-runtime-parity", "status": status, "python_artifact": rel(RUN_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.joblib"), "runtime_artifact": rel(RUN_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.onnx"), "compared_surface": "ONNX parity(ONNX 동등성) and MT5 direction-specific trading output(MT5 방향별 거래 출력)", "parity_level": "runtime_probe(런타임 탐침)", "tester_identity": "MT5 Strategy Tester(전략 테스터) US100 M5", "missing_evidence": ["none(없음)"], "allowed_claims": ["runtime_probe_completed"], "forbidden_claims": ["runtime_authority", "live_readiness", "promotion"]},
            {"packet_id": PACKET_ID, "skill": "obsidian-data-integrity", "status": status, "data_sources_checked": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT], "time_axis_boundary": "existing Stage04/03 timestamp contract(기존 시간축 계약)", "split_boundary": "validation/oos split_v1(검증/표본외 분할)", "leakage_checks": "no threshold re-fit(임계값 재적합 없음); direction permission only(방향 허용만)", "missing_data_boundary": "Tier B/Tier A+B out_of_scope_by_claim(주장 범위 밖)"},
            {"packet_id": PACKET_ID, "skill": "obsidian-backtest-forensics", "status": status, "tester_report": rel(RUN_ROOT / "mt5/reports"), "tester_settings": rel(RUN_ROOT / "mt5"), "spread_commission_slippage": "tester settings inherited(테스터 설정 계승); performance claim downgraded(성과 주장 낮춤)", "trade_list_identity": "MT5 report and telemetry(MT5 보고서와 기록)", "forensic_gaps": ["none(없음)"]},
            {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": status, "source_inputs": [SOURCE_RUN_ID, THRESHOLD_SOURCE_RUN_ID, FEATURE_SET_ID, LABEL_ID], "produced_artifacts": [rel(RUN_ROOT / "run_manifest.json"), rel(RUN_ROOT / "thresholds/threshold_handoff.json")], "raw_evidence": [rel(RUN_ROOT / "mt5/reports")], "machine_readable": [rel(RUN_ROOT / "kpi_record.json")], "human_readable": [rel(REVIEW_PATH)], "hashes_or_missing_reasons": "hashes recorded in manifest(목록에 해시 기록)", "lineage_boundary": BOUNDARY},
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
        "threshold_source_run_id": THRESHOLD_SOURCE_RUN_ID,
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
        "tier_b_context_boundary": "out_of_scope_by_claim",
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
    parser = argparse.ArgumentParser(description="Stage13 MLP direction asymmetry runtime probe.")
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
        "attempts": make_direction_attempts(config=config, context=context, model_artifacts=model_artifacts, feature_matrices=feature_matrices, threshold=threshold),
        "common_copies": copy_runtime_inputs(config=config, model_artifacts=model_artifacts, feature_matrices=feature_matrices),
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": context["tier_b_context_summary"],
    }
    result = execute_or_materialize(prepared, args)
    runtime_probability = write_runtime_probability_artifacts(result=result, output_root=RUN_ROOT / "runtime_probability", boundary="runtime_probability_proxy_for_direction_asymmetry_probe")
    ledgers = write_ledgers(result=result, threshold=threshold, runtime_probability=runtime_probability)
    summary = write_run_files(created_at=created_at, context=context, spec=spec, threshold=threshold, model_artifacts=model_artifacts, feature_matrices=feature_matrices, prepared=prepared, result=result, runtime_probability=runtime_probability, ledgers=ledgers)
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "materialize_only": bool(args.materialize_only), "summary": summary})
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
