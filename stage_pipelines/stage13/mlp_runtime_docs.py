from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any, Mapping

from foundation.control_plane.ledger import io_path
from foundation.control_plane.mt5_tier_balance_completion import ROOT


STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_ID = "run04A_mlp_characteristic_runtime_probe_v1"
BOUNDARY = "runtime_probe_mlp_characteristic_not_alpha_quality_not_promotion_not_runtime_authority"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
STAGE_BRIEF_PATH = STAGE_ROOT / "00_spec/stage_brief.md"
INPUT_REFERENCES_PATH = STAGE_ROOT / "01_inputs/input_references.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run04A_mlp_characteristic_runtime_probe_plan.md"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04A_mlp_characteristic_runtime_probe_packet.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_characteristic_runtime_probe_open.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_text_bom(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def current_branch() -> str:
    try:
        return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def write_stage13_docs(summary: Mapping[str, Any], result: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    status = str(summary["external_verification_status"])
    run_status = "reviewed_runtime_probe_completed" if status == "completed" else "blocked_runtime_probe_attempted"
    write_text_bom(PLAN_PATH, plan_text())
    write_text_bom(REVIEW_PATH, result_summary_markdown(summary, result))
    write_text_bom(STAGE_BRIEF_PATH, stage_brief_text(status))
    write_text_bom(INPUT_REFERENCES_PATH, input_references_text())
    write_text_bom(SELECTION_STATUS_PATH, selection_status_text(summary, selected, run_status))
    write_text_bom(REVIEW_INDEX_PATH, review_index_text(summary))
    write_text_bom(DECISION_PATH, decision_text(summary))
    sync_changelog(summary)
    sync_workspace_state(summary)
    sync_current_working_state(summary)


def plan_text() -> str:
    return "\n".join(
        [
            "# RUN04A MLP Characteristic Runtime Probe Plan",
            "",
            "- run_id(실행 ID): `run04A_mlp_characteristic_runtime_probe_v1`",
            "- purpose(목적): MLP model(다층 퍼셉트론 모델)의 얕은 특성 탐색과 좁은 MT5 runtime probe(MT5 런타임 탐침)를 함께 본다.",
            "- independence(독립성): Stage10/11/12(10/11/12단계) run(실행)을 baseline(기준선), seed(씨앗), reference(참고)로 쓰지 않는다.",
            "- depth(깊이): coarse characteristic scout(거친 특성 탐색)만 수행한다.",
            "- MT5 view(MT5 보기): Tier A used(Tier A 사용), Tier B fallback used(Tier B 대체 사용), actual routed total(실제 라우팅 전체)을 기록한다.",
            "",
            "효과(effect, 효과): 첫 작업에서 Python-only(파이썬만) 판독으로 끝내지 않고, Strategy Tester(전략 테스터) 반응까지 좁게 확인한다.",
        ]
    )


def result_summary_markdown(summary: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- selected variant(선택 변형): `{summary['selected_variant_id']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| view(보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래 수) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        lines.append(
            "| {view} | {split} | {net} | {pf} | {dd} | {trades} |".format(
                view=record.get("record_view"),
                split=record.get("split"),
                net=metrics.get("net_profit"),
                pf=metrics.get("profit_factor"),
                dd=metrics.get("max_drawdown_amount"),
                trades=metrics.get("trade_count"),
            )
        )
    if summary.get("failure"):
        lines.extend(["", f"- failure(실패): `{summary['failure']}`"])
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 결과는 MLP model(다층 퍼셉트론 모델)의 얕은 runtime_probe(런타임 탐침)이다.",
            "alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 만들지 않는다.",
        ]
    )
    return "\n".join(lines)


def stage_brief_text(status: str) -> str:
    return "\n".join(
        [
            "# Stage 13 MLP Training Effect",
            "",
            "## Question(질문)",
            "",
            "Stage 13(13단계)는 MLPClassifier(다층 퍼셉트론 분류기)의 학습 특성이 FPMarkets US100 M5(FPMarkets US100 5분봉) 입력에서 어떻게 드러나는지 얕게 확인한다.",
            "",
            "효과(effect, 효과): Logistic Regression(로지스틱 회귀), LightGBM(라이트GBM), ExtraTrees(엑스트라 트리)를 반복하지 않고 neural network style model(신경망 방식 모델)의 학습 효과(training effect, 학습 효과)를 분리해서 본다.",
            "",
            "## Scope(범위)",
            "",
            "- model family(모델 계열): `sklearn_mlpclassifier_multiclass(사이킷런 다층 퍼셉트론 다중분류)`",
            "- dataset(데이터셋): Stage 04(4단계)의 58 feature(58개 피처) model input(모델 입력)",
            "- label(라벨): 첫 기본 fwd12(60분) label/split(라벨/분할)",
            "- inheritance(계승): Stage10/11/12(10/11/12단계) run(실행)을 baseline(기준선), seed surface(씨앗 표면), reference surface(참고 표면)로 쓰지 않는다.",
            "",
            "## Exploration Style(탐색 방식)",
            "",
            "Stage 13(13단계)는 deep search(깊은 탐색) 단계가 아니다.",
            "",
            "효과(effect, 효과): Stage12(12단계)처럼 변형을 깊게 파지 않고, hidden layer shape(은닉층 모양), activation(활성화 함수), regularization(정규화), scaling sensitivity(스케일링 민감도), convergence behavior(수렴 행동), probability shape(확률 모양)만 먼저 본다.",
            "",
            "## First Scout Runtime Requirement(첫 탐색 런타임 요구)",
            "",
            "첫 scout(탐색)는 Python structural scout(파이썬 구조 탐색)와 narrow MT5 runtime probe(좁은 MT5 런타임 탐침)를 같이 본다.",
            "",
            "효과(effect, 효과): MLP model(다층 퍼셉트론 모델)이 Python(파이썬) 지표에서만 그럴듯한지, Strategy Tester(전략 테스터) 현실 반응에서도 최소 관찰 가치가 있는지 같은 packet(작업 묶음) 안에서 확인한다.",
            "",
            "## Current Boundary(현재 경계)",
            "",
            f"- first run status(첫 실행 상태): `{status}`",
            "- claim boundary(주장 경계): `runtime_probe_only(런타임 탐침만)`",
            "- forbidden claims(금지 주장): alpha quality(알파 품질), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)",
        ]
    )


def input_references_text() -> str:
    return "\n".join(
        [
            "# Stage 13 Input References",
            "",
            "- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`",
            "- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`",
            "- training summary(학습 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json`",
            "- Tier B policy(Tier B 정책): `foundation/control_plane/tier_context_materialization.py`",
            "- MT5 runtime EA(MT5 런타임 EA): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`",
            "",
            "효과(effect, 효과): Stage13(13단계)는 Stage10/11/12(10/11/12단계) 실행 산출물을 시작점으로 쓰지 않고, 닫힌 기반 입력과 공통 MT5(메타트레이더5) 런타임 인계만 사용한다.",
        ]
    )


def selection_status_text(summary: Mapping[str, Any], selected: Mapping[str, Any], run_status: str) -> str:
    return "\n".join(
        [
            "# Stage 13 Selection Status",
            "",
            "## Current Read(현재 판독)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- status(상태): `{run_status}`",
            "- proposed model family(제안 모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
            "- exploration depth(탐색 깊이): `coarse_characteristic_scout_only(거친 특성 탐색만)`",
            "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
            f"- current run(현재 실행): `{RUN_ID}`",
            f"- selected scout variant(선택 탐색 변형): `{selected['variant_id']}`",
            "- selected operating reference(선택 운영 기준): `none(없음)`",
            "- selected promotion candidate(선택 승격 후보): `none(없음)`",
            "- selected baseline(선택 기준선): `none(없음)`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "",
            "## Boundary(경계)",
            "",
            "이 상태는 runtime_probe(런타임 탐침)만 뜻한다.",
            "",
            "효과(effect, 효과): MT5(메타트레이더5) 결과가 양수여도 alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)를 만들지 않는다.",
        ]
    )


def review_index_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Stage 13 Review Index",
            "",
            f"- `run04A_mlp_characteristic_runtime_probe_v1`: `{summary['judgment']}`",
            f"- report(보고서): `{rel(REVIEW_PATH)}`",
            f"- manifest(실행 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`",
            f"- kpi record(KPI 기록): `{rel(RUN_ROOT / 'kpi_record.json')}`",
            f"- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`",
            "",
            "효과(effect, 효과): Stage13(13단계)의 첫 근거 위치를 한 곳에서 찾게 한다.",
        ]
    )


def decision_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-02 Stage 13 MLP Runtime Probe Open",
            "",
            "- decision(결정): Stage13(13단계)을 MLPClassifier(다층 퍼셉트론 분류기) 독립 탐색으로 연다.",
            f"- first run(첫 실행): `{RUN_ID}`",
            "- scope(범위): coarse characteristic scout(거친 특성 탐색) + narrow MT5 runtime probe(좁은 MT5 런타임 탐침)",
            "- independence(독립성): Stage10/11/12(10/11/12단계) run(실행)을 baseline(기준선), seed(씨앗), reference(참고)로 쓰지 않는다.",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "",
            "효과(effect, 효과): Stage13(13단계)는 주제 전환(topic pivot, 주제 전환)으로 열렸고, 운영 기준(operating reference, 운영 기준)은 만들지 않는다.",
        ]
    )


def sync_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    line = (
        f"- 2026-05-02: `{RUN_ID}` {summary['external_verification_status']}. "
        "Stage13(13단계) MLPClassifier(다층 퍼셉트론 분류기) coarse characteristic scout(거친 특성 탐색)와 narrow MT5 runtime_probe(좁은 MT5 런타임 탐침)를 실행했다. "
        "Effect(효과): Stage10/11/12(10/11/12단계) run(실행)을 baseline(기준선), seed(씨앗), reference(참고)로 쓰지 않고 MLP(다층 퍼셉트론) 특성만 독립적으로 기록한다."
    )
    if RUN_ID in text:
        text = re.sub(
            rf"- 2026-05-02: `{RUN_ID}` [^.]+\. Stage13",
            f"- 2026-05-02: `{RUN_ID}` {summary['external_verification_status']}. Stage13",
            text,
            count=1,
        )
        write_text_bom(CHANGELOG_PATH, text)
        return
    text = text.replace("## 2026-05-02\n\n", "## 2026-05-02\n\n" + line + "\n")
    write_text_bom(CHANGELOG_PATH, text)


def sync_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    branch = current_branch()
    text = re.sub(r"^active_branch: .*$", f"active_branch: {branch}", text, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {STAGE_ID}", text, flags=re.MULTILINE)
    text = re.sub(
        r"^(  status: ).*$",
        r"\1stage01_closed_stage02_closed_stage03_closed_stage04_closed_stage05_closed_stage06_closed_stage07_closed_stage08_closed_stage09_closed_stage10_closed_stage11_closed_stage12_reviewed_closed_stage13_active_run04A_mlp_runtime_probe",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^(  status: stage04_closed_stage05_closed_stage06_closed_stage07_closed_stage08_closed_stage09_closed_stage10_closed_stage11_closed_stage12_reviewed_closed_no_next_stage_opened)$",
        "  status: stage04_closed_stage05_closed_stage06_closed_stage07_closed_stage08_closed_stage09_closed_stage10_closed_stage11_closed_stage12_reviewed_closed_stage13_active",
        text,
        flags=re.MULTILINE,
    )
    focus_line = "- treat Stage 13 as independent MLPClassifier(다층 퍼셉트론 분류기) coarse characteristic runtime_probe(거친 특성 런타임 탐침), not a baseline(기준선) or promotion(승격)"
    if focus_line not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    stage13_block = (
        "    stage13:\n"
        f"      stage_id: {STAGE_ID}\n"
        "      ownership: independent MLPClassifier coarse characteristic scout plus narrow MT5 runtime_probe\n"
        "      status: active_run04A_mlp_characteristic_runtime_probe\n"
    )
    if "    stage13:" not in text:
        text = text.replace(
            "    stage12:\n      stage_id: 12_model_family_challenge__extratrees_training_effect\n      ownership: standalone ExtraTrees model-family training effect without Stage 10/11 inheritance\n      status: reviewed_closed_no_next_stage_opened\n",
            "    stage12:\n      stage_id: 12_model_family_challenge__extratrees_training_effect\n      ownership: standalone ExtraTrees model-family training effect without Stage 10/11 inheritance\n      status: reviewed_closed_no_next_stage_opened\n" + stage13_block,
            1,
        )
    top_block = (
        "stage13_mlp_characteristic_runtime_probe:\n"
        f"  run_id: {RUN_ID}\n"
        f"  status: {summary['external_verification_status']}\n"
        f"  judgment: {summary['judgment']}\n"
        f"  selected_variant_id: {summary['selected_variant_id']}\n"
        "  boundary: runtime_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
        f"  report_path: {rel(REVIEW_PATH)}\n"
    )
    if "stage13_mlp_characteristic_runtime_probe:" not in text:
        text = text.replace("stage01_raw_m5_inventory:\n", top_block + "stage01_raw_m5_inventory:\n", 1)
    write_text_bom(WORKSPACE_STATE_PATH, text)


def sync_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_WORKING_STATE_PATH)
    branch = current_branch()
    text = re.sub(
        r"^- active_stage: .*$",
        f"- active_stage: `{STAGE_ID}(13단계 MLP 학습 효과)`",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^- active_branch: .*$",
        f"- active_branch: `{branch}(Stage13 브랜치)`",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^- current run\(현재 실행\): .*$",
        f"- current run(현재 실행): `{RUN_ID}`",
        text,
        flags=re.MULTILINE,
    )
    latest = "\n".join(
        [
            "## Latest Stage 13 Update(최신 Stage 13 업데이트)",
            "",
            f"Stage13(13단계)은 MLPClassifier(다층 퍼셉트론 분류기) 독립 탐색으로 열렸다. 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, 외부 검증 상태(external verification status, 외부 검증 상태)는 `{summary['external_verification_status']}`다.",
            "",
            "효과(effect, 효과): Stage10/11/12(10/11/12단계) 실행을 기준선(baseline, 기준선), 씨앗(seed, 씨앗), 참고(reference, 참고)로 쓰지 않고, MLP(다층 퍼셉트론)의 얕은 특성과 MT5(메타트레이더5) 런타임 반응만 기록한다.",
            "",
        ]
    )
    pattern = r"## Latest Stage 13 Update\(최신 Stage 13 업데이트\)\n.*?(?=## 쉬운 설명\(Plain Read, 쉬운 설명\))"
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, latest, text, flags=re.DOTALL)
    else:
        text = text.replace("## 쉬운 설명(Plain Read, 쉬운 설명)\n", latest + "## 쉬운 설명(Plain Read, 쉬운 설명)\n", 1)
    write_text_bom(CURRENT_WORKING_STATE_PATH, text)
