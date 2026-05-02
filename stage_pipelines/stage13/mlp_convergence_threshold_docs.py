from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from foundation.control_plane.ledger import io_path
from foundation.control_plane.mt5_tier_balance_completion import ROOT
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage13.mlp_handoff_support import rel


STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_ID = "run04D_mlp_convergence_threshold_feasibility_probe_v1"
PACKET_ID = "stage13_run04D_mlp_convergence_threshold_feasibility_probe_packet_v1"
BOUNDARY = "convergence_threshold_feasibility_probe_not_alpha_quality_not_promotion_not_runtime_authority"
REPRESENTATIVE_THRESHOLD_ID = "q90_m000"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04D_mlp_convergence_threshold_feasibility_probe_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run04D_mlp_convergence_threshold_feasibility_probe_plan.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_convergence_threshold_feasibility_probe.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
STAGE_BRIEF_PATH = STAGE_ROOT / "00_spec/stage_brief.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"


def write_text_bom(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def report_markdown(summary: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        f"- representative threshold(대표 임계값): `{REPRESENTATIVE_THRESHOLD_ID}`",
        "",
        "## Convergence(수렴)",
        "",
        "| scope(범위) | n_iter(반복) | max_iter(최대 반복) | loss first(초기 손실) | loss last(마지막 손실) | validation best(검증 최고) | label(라벨) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for scope in (mt5.TIER_A, mt5.TIER_B):
        row = summary["convergence"].get(scope, {})
        lines.append(
            f"| {scope} | {row.get('n_iter')} | {row.get('max_iter')} | {fmt(row.get('loss_first'))} | "
            f"{fmt(row.get('loss_last'))} | {fmt(row.get('validation_score_best'))} | {row.get('convergence_label')} |"
        )
    lines.extend(
        [
            "",
            "## Threshold Feasibility(임계값 가능성)",
            "",
            "| scope(범위) | validation signals(검증 신호) | validation coverage(검증 비율) | OOS signals(표본외 신호) | OOS coverage(표본외 비율) | density label(밀도 라벨) |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for scope in (mt5.TIER_A, mt5.TIER_B, mt5.TIER_AB):
        row = summary["representative_thresholds"].get(scope, {})
        lines.append(
            f"| {scope} | {row.get('validation_signal_count')} | {fmt(row.get('validation_signal_coverage'))} | "
            f"{row.get('oos_signal_count')} | {fmt(row.get('oos_signal_coverage'))} | {row.get('density_label')} |"
        )
    lines.extend(
        [
            "",
            "## MT5 No-Trade Handoff(MT5 무거래 인계)",
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
            f"| {record.get('record_view')} | {record.get('split')} | {metrics.get('feature_ready_count')} | "
            f"{metrics.get('model_ok_count')} | {metrics.get('trade_count')} |"
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이번 실행(run, 실행)은 MLP(다층 퍼셉트론)의 수렴 곡선과 확률 임계값 밀도를 함께 본다.",
            "alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
        ]
    )
    return "\n".join(lines)


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


def work_packet_markdown(summary: Mapping[str, Any], created_at: str) -> str:
    return "\n".join(
        [
            f"# {PACKET_ID}",
            "",
            f"- created_at_utc(생성 UTC): `{created_at}`",
            "- primary_family(주 작업군): `runtime_backtest(런타임 백테스트)`",
            "- primary_skill(주 스킬): `obsidian-model-validation(모델 검증)`",
            "- support_skills(보조 스킬): `experiment-design/runtime-parity/data-integrity/backtest-forensics/artifact-lineage(실험 설계/런타임 동등성/데이터 무결성/백테스트 포렌식/산출물 계보)`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "효과(effect, 효과): convergence(수렴)와 threshold feasibility(임계값 가능성)를 같은 work packet(작업 묶음)에서 닫는다.",
        ]
    )


def plan_text() -> str:
    return "\n".join(
        [
            "# RUN04D MLP Convergence + Threshold Feasibility Plan",
            "",
            "- hypothesis(가설): MLPClassifier(다층 퍼셉트론 분류기)는 loss curve(손실 곡선), validation score(검증 점수), probability density(확률 밀도)에서 특성이 보일 수 있다.",
            "- decision_use(결정 용도): 다음 trading runtime handoff(거래 런타임 인계)를 열기 전에 threshold density(임계값 밀도)가 너무 마르거나 넘치는지 확인한다.",
            "- comparison_baseline(비교 기준): Stage10/11/12(10/11/12단계) run(실행)을 쓰지 않고 Tier A/B(티어 A/B) 내부 표본만 비교한다.",
            "- controls(고정값): 58 feature(58개 피처), fwd12 label(60분 라벨), split_v1(분할 v1), no-trade threshold(무거래 임계값) 1.01.",
            "- changed_variables(변경값): 관찰 대상만 convergence(수렴)와 threshold feasibility(임계값 가능성)로 바꾼다.",
            "- evidence_plan(근거 계획): convergence CSV/JSON(수렴 CSV/JSON), threshold CSV/JSON(임계값 CSV/JSON), ONNX parity(ONNX 동등성), MT5 Strategy Tester(전략 테스터) 무거래 인계, ledger(장부).",
        ]
    )


def decision_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-02 Stage 13 MLP Convergence Threshold Feasibility Probe",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "- decision/effect(결정/효과): 1번 convergence(수렴)와 2번 threshold feasibility(임계값 가능성)를 한 run(실행)으로 닫았다.",
            "- boundary(경계): threshold selection(임계값 선택)이나 trading runtime authority(거래 런타임 권위)가 아니다.",
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
            "- depth(깊이): 깊은 최적화가 아니라 MLP(다층 퍼셉트론) 특성이 잘 보이는 구조만 확인한다.",
            "- current focus(현재 초점): convergence(수렴), threshold feasibility(임계값 가능성), MT5 no-trade handoff(MT5 무거래 인계).",
            "",
            "효과(effect, 효과): 다음 기준선 선택 전까지 모델 계열의 특성을 분리해서 보고, 운영 의미를 만들지 않는다.",
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
            "- status(상태): `reviewed_convergence_threshold_feasibility_probe_completed`",
            "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
            "- exploration depth(탐색 깊이): `convergence_threshold_feasibility_probe_only(수렴/임계값 가능성 탐침만)`",
            "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
            f"- current run(현재 실행): `{RUN_ID}`",
            "- selected operating reference(선택 운영 기준): `none(없음)`",
            "- selected promotion candidate(선택 승격 후보): `none(없음)`",
            "- selected baseline(선택 기준선): `none(없음)`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "",
            "효과(effect, 효과): MLP(다층 퍼셉트론)의 수렴과 임계값 밀도만 확인하고, 운영 의미는 만들지 않는다.",
        ]
    )


def sync_review_index(summary: Mapping[str, Any]) -> None:
    text = "\n".join(
        [
            "# Stage 13 Review Index",
            "",
            "- `run04A_mlp_characteristic_runtime_probe_v1`: `inconclusive_mlp_characteristic_runtime_probe_completed`",
            "- `run04B_mlp_input_geometry_runtime_handoff_probe_v1`: `inconclusive_input_geometry_runtime_handoff_probe_completed`",
            "- `run04C_mlp_activation_runtime_probe_v1`: `inconclusive_activation_runtime_probe_completed`",
            f"- `{RUN_ID}`: `{summary['judgment']}`, report(보고서) `{rel(REVIEW_PATH)}`",
            "",
            "효과(effect, 효과): Stage13(13단계)의 실행 근거 위치를 한 곳에서 찾게 한다.",
        ]
    )
    write_text_bom(REVIEW_INDEX_PATH, text)


def sync_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    text = text.replace("`run04B_mlp_input_geometry_runtime_handoff_probe_v1` blocked.", "`run04B_mlp_input_geometry_runtime_handoff_probe_v1` completed.")
    text = text.replace("`run04C_mlp_activation_runtime_probe_v1` blocked.", "`run04C_mlp_activation_runtime_probe_v1` completed.")
    line = (
        f"- 2026-05-02: `{RUN_ID}` {summary['external_verification_status']}. "
        "Stage13(13단계) MLP convergence(수렴)와 threshold feasibility(임계값 가능성)를 한 run(실행)으로 확인했다. "
        "Effect(효과): 다음 거래 런타임 인계 전에 확률 밀도와 MT5 no-trade handoff(MT5 무거래 인계)를 분리해서 확인한다."
    )
    if RUN_ID not in text:
        text = text.replace("## 2026-05-02\n\n", "## 2026-05-02\n\n" + line + "\n", 1)
    write_text_bom(CHANGELOG_PATH, text)


def sync_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {STAGE_ID}", text, flags=re.MULTILINE)
    text = text.replace("stage13_active_run04C_mlp_activation_runtime_probe", "stage13_active_run04D_mlp_convergence_threshold_feasibility_probe")
    text = text.replace("active_run04C_mlp_activation_runtime_probe", "active_run04D_mlp_convergence_threshold_feasibility_probe")
    block = (
        "stage13_mlp_convergence_threshold_feasibility_probe:\n"
        f"  run_id: {RUN_ID}\n"
        f"  status: {summary['external_verification_status']}\n"
        f"  judgment: {summary['judgment']}\n"
        "  boundary: convergence_threshold_feasibility_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
        f"  report_path: {rel(REVIEW_PATH)}\n"
    )
    text = _replace_or_insert_block(text, "stage13_mlp_convergence_threshold_feasibility_probe", block)
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
            "효과(effect, 효과): MLP(다층 퍼셉트론)의 convergence(수렴), threshold feasibility(임계값 가능성), MT5 no-trade handoff(MT5 무거래 인계)를 한 묶음으로 확인했다.",
            "",
        ]
    )
    text = replace_section(text, "## Latest Stage 13 Update", "## 쉬운 설명", latest)
    stage_section = "\n".join(
        [
            "## 현재 단계(Current Stage, 현재 단계)",
            "",
            f"`{STAGE_ID}`",
            "",
            "Stage13(13단계)의 질문(question, 질문)은 Stage10/11/12(10/11/12단계)를 계승하지 않고 MLPClassifier(다층 퍼셉트론 분류기)의 학습 특성만 얕게 보는 것이다.",
            "",
            "효과(effect, 효과): 이번 상태는 convergence(수렴)와 threshold feasibility(임계값 가능성)를 확인했지만 baseline(기준선), alpha quality(알파 품질), runtime authority(런타임 권위)는 만들지 않는다.",
            "",
        ]
    )
    text = replace_section(text, "## 현재 단계(Current Stage, 현재 단계)", "## 탐색 원칙", stage_section)
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


def fmt(value: Any) -> str:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return "NA"
    if pd.isna(numeric):
        return "NA"
    return f"{numeric:.6g}"
