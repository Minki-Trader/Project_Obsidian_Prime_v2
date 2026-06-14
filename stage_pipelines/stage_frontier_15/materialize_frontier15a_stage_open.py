from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_15__score_threshold_density_controlled_onnx_scout"
RUN_ID = "frontier15A_stage_open_score_threshold_density_controlled_onnx_scout_v1"
RUN_NUMBER = "frontier15A"
PARENT_RUN_ID = "frontier14D_stage_closeout_daily_session_opportunity_budget_onnx_scout_v1"
NEXT_RUN_ID = "frontier15B_score_threshold_density_controlled_proxy_scout_v1"
STATUS = "opened_frontier15_score_threshold_density_controlled_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_and_score_contract_boundary_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_15_score_threshold_density_controlled_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_15/materialize_frontier15a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier15_stage_open/small_review")
F14_SELECTION = Path("stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/04_selected/selection_status.md")
F14_CLOSEOUT_REPORT = Path(
    "stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/03_reviews/"
    "frontier14D_stage_closeout_daily_session_opportunity_budget_onnx_scout_v1_report.md"
)

PRIMARY_CELL_ID = "edge_margin__target8"
SCORE_CONTRACTS = (
    {
        "score_contract_id": "edge_margin",
        "score_expression": "max(p_short, p_long) - p_flat",
        "korean_expression": "매수/매도 확률 중 큰 값에서 flat(플랫, 무거래) 확률을 뺀 값",
        "decision_meaning": "model confidence over flat(무거래 대비 모델 확신)",
    },
    {
        "score_contract_id": "side_gap",
        "score_expression": "abs(p_long - p_short)",
        "korean_expression": "long(롱, 매수) 확률과 short(숏, 매도) 확률의 절대 차이",
        "decision_meaning": "directional separation(방향 분리도)",
    },
    {
        "score_contract_id": "utility_tilt",
        "score_expression": "max(p_short, p_long) - 0.5 * p_flat",
        "korean_expression": "매수/매도 확률 중 큰 값에서 flat(플랫, 무거래) 확률 절반을 뺀 값",
        "decision_meaning": "milder flat penalty(완만한 무거래 벌점)",
    },
)
DENSITY_TARGETS = (5, 8, 10)


def main() -> int:
    now = utc_now()
    ensure_dirs()
    grok = read_grok()
    local = local_verification(grok)
    summary = build_summary(now, grok, local)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": summary["grok_classification"],
        "local_verification": summary["local_verification"]["judgment"],
        "primary_cell_id": PRIMARY_CELL_ID,
        "score_cell_count": len(summary["score_cells"]),
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def read_grok() -> dict[str, Any]:
    meta = read_json(GROK_PACKET / "metadata.json")
    output = read_text(GROK_PACKET / "clean_output.md")
    lowered = output.lower()
    return {
        "packet": GROK_PACKET.as_posix(),
        "prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "output": (GROK_PACKET / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "accepted_runtime_representation_change": "runtime representation change" in lowered or "representation swap" in lowered,
        "accepted_nine_cell_guard": "9-cell" in lowered or "9" in lowered and "grid" in lowered,
        "accepted_argmax_baseline_guard": "argmax baseline" in lowered,
        "forbidden_claims_supported": "not_claimed" in lowered and "goal achieve" in lowered,
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "classification" in lowered and "accepted" in lowered:
        return "accepted(수용)"
    if "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    f14_selection = read_text(F14_SELECTION)
    f14_report = read_text(F14_CLOSEOUT_REPORT)
    checks = {
        "workspace_points_to_frontier15A": "next_run_id: frontier15A_stage_open_new_hypothesis_design_v1" in workspace,
        "f14_selection_closed_with_no_authority": "closed_preserved_clue_negative_memory_no_authority" in f14_selection,
        "f14_selection_points_to_frontier15A": "frontier15A_stage_open_new_hypothesis_design_v1" in f14_selection,
        "f14_report_no_authority": "Goal Achieve" in f14_report and "not_claimed" in f14_report,
        "grok_success": bool(grok["success"]),
        "grok_accepted": grok["classification"] == "accepted(수용)",
        "grok_runtime_representation_guard": bool(grok["accepted_runtime_representation_change"]),
        "grok_nine_cell_guard": bool(grok["accepted_nine_cell_guard"]),
        "grok_argmax_baseline_guard": bool(grok["accepted_argmax_baseline_guard"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "score_cells_frozen": len(score_cells()) == 9 and PRIMARY_CELL_ID in {cell["cell_id"] for cell in score_cells()},
    }
    return {
        "checks": checks,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def score_cells() -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    for contract in SCORE_CONTRACTS:
        for target in DENSITY_TARGETS:
            cell_id = f"{contract['score_contract_id']}__target{target}"
            cells.append({
                **contract,
                "target_density_per_day": target,
                "cell_id": cell_id,
                "is_primary_cell": cell_id == PRIMARY_CELL_ID,
                "threshold_fit_policy": (
                    "train probability scores plus train calendar only"
                    "(학습 확률 점수와 학습 달력만 사용)"
                ),
                "threshold_application_policy": (
                    "apply unchanged to validation/OOS(검증/표본밖에 변경 없이 적용)"
                ),
            })
    return cells


def build_summary(now: str, grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": (
            "F14(프론티어14)의 label-side density(라벨 쪽 빈도)는 올라갔지만 argmax signal"
            "(최대확률 신호)이 거래 빈도 절벽을 만들었다. F15(프론티어15)는 같은 초기 label family"
            "(라벨 계열)를 control(통제)로 두고, ONNX probability tensor(온엑스 확률 텐서)를 score surface"
            "(점수 표면)로 읽어 train-only density threshold(학습 전용 빈도 임계값) 계약을 시험한다."
        ),
        "novelty_delta": (
            "changed variable(변경 변수)은 label knob(라벨 손잡이)이 아니라 runtime decision contract"
            "(런타임 결정 계약)이다. 효과(effect, 효과)는 F14(프론티어14)의 quota retuning"
            "(할당 재조정), flat subset ladder(플랫 부분집합 사다리), class-weight forcing"
            "(클래스 가중치 강제), validation/OOS threshold calibration(검증/표본밖 임계값 보정)을 반복하지 않는 것이다."
        ),
        "primary_cell_id": PRIMARY_CELL_ID,
        "score_cells": score_cells(),
        "strict_selection_rule": (
            "strict scout clue(엄격 탐색 단서)는 primary cell(1순위 칸) "
            f"`{PRIMARY_CELL_ID}`만 forward trigger(전진 트리거)로 쓴다. 다른 cell(칸)이 좋아도 "
            "secondary preserved clue(보조 보존 단서)로만 기록한다."
        ),
        "required_rows": [
            "all 9 score-target cells reported(9개 점수-목표 칸 전부 보고)",
            "F14-matched argmax baseline row per variant/model/split(F14 대응 최대확률 기준행을 변형/모델/분할별 기록)",
            "label/model density split per split(라벨/모델 빈도 분리를 분할별 기록)",
            "train-only threshold manifest(학습 전용 임계값 목록)",
        ],
        "controls": [
            "same Tier A dataset(같은 티어 A 데이터셋)",
            "same feature order(같은 피처 순서)",
            "initial F14 opportunity labels only(초기 F14 기회 라벨만 사용)",
            "no quota/horizon retuning(할당/보유기간 재조정 없음)",
            "no validation/OOS threshold calibration(검증/표본밖 임계값 보정 없음)",
        ],
        "success_criteria": (
            "primary cell(1순위 칸)이 validation/OOS(검증/표본밖)에서 positive net(양수 순손익), "
            "PF >= 1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD <= 15%"
            "(손실폭 15% 이하), subperiod DD control(하위기간 손실폭 통제), ONNX parity"
            "(온엑스 동등성)를 동시에 만족하면 strict scout clue(엄격 탐색 단서)로 본다."
        ),
        "failure_criteria": (
            "train-only threshold(학습 전용 임계값)이 validation/OOS density(검증/표본밖 빈도)로 전이되지 않거나 "
            "PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 무너지면 negative memory(부정 기억) 또는 repair"
            "(수리) 후보로 기록한다."
        ),
        "invalid_conditions": [
            "validation/OOS PF/net/DD로 threshold(임계값)를 고르거나 바꾸는 경우",
            "결과를 본 뒤 score contract(점수 계약)나 target density(목표 빈도)를 추가하는 경우",
            "F14 label quota/horizon(라벨 할당/보유기간)을 다시 맞추는 경우",
        ],
        "stage_closeout_options": [
            "completion candidate(완성 후보)",
            "preserved clue(보존 단서)",
            "negative memory(부정 기억)",
            "invalid setup(무효 설정)",
            "blocked(차단)",
        ],
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "score_contract_manifest.json", {
        "primary_cell_id": PRIMARY_CELL_ID,
        "score_cells": summary["score_cells"],
        "strict_selection_rule": summary["strict_selection_rule"],
    })
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "score_threshold_signal_contract.md", score_contract_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "selection_metric_spec.md", selection_metric_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_state_and_registries(summary: dict[str, Any]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(summary))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry())
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier14_selection": artifact_identity(F14_SELECTION),
            "frontier14_closeout_report": artifact_identity(F14_CLOSEOUT_REPORT),
            "grok_stage_open_output": artifact_identity(Path(summary["grok_output"])),
        },
        "outputs": {
            "stage_open_summary": (RUN_ROOT / "stage_open_summary.json").as_posix(),
            "score_contract_manifest": (RUN_ROOT / "score_contract_manifest.json").as_posix(),
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
        },
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Score Threshold Density Controlled ONNX Scout(프론티어15 점수 임계값 빈도 통제 온엑스 탐색)

Status(상태): `{summary['status']}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Primary cell(1순위 칸): `{PRIMARY_CELL_ID}`

Claim boundary(주장 경계): scout clue/seed surface/preserved clue/negative memory/invalid setup/blocked(탐색 단서/씨앗 표면/보존 단서/부정 기억/무효 설정/차단)까지만 허용합니다.
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Stage Brief(프론티어15 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): ONNX probability tensor(온엑스 확률 텐서)를 score threshold signal contract(점수 임계값 신호 계약)로 읽으면 F14(프론티어14)의 argmax density cliff(최대확률 빈도 절벽)를 줄일 수 있는가?

## Hypothesis(가설)

{summary['hypothesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Strict Rule(엄격 규칙)

{summary['strict_selection_rule']}

## Claim Boundary(주장 경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def score_contract_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(
        f"- `{cell['cell_id']}`: `{cell['score_expression']}`, target density(목표 빈도) "
        f"`{cell['target_density_per_day']}/day`, primary(1순위) `{cell['is_primary_cell']}`"
        for cell in summary["score_cells"]
    )
    return f"""# Frontier15 Score Threshold Signal Contract(프론티어15 점수 임계값 신호 계약)

Action(행동): ONNX probability tensor(온엑스 확률 텐서)의 short/flat/long(숏/플랫/롱) 확률을 3개 score contract(점수 계약)로 바꾼 뒤, train-only threshold(학습 전용 임계값)로 거래 빈도를 맞춥니다.

Effect(효과): validation/OOS(검증/표본밖) 성과를 보고 threshold(임계값)를 고르지 않고, density transfer(빈도 전이)가 되는지만 확인합니다.

## Frozen Grid(고정 격자)

{rows}

## Required Baseline(필수 기준행)

F14-matched argmax baseline row(F14 대응 최대확률 기준행)를 every variant/model/split(모든 변형/모델/분할)에 기록합니다. Effect(효과): score threshold(점수 임계값)이 실제로 density cliff(빈도 절벽)를 고쳤는지 비교합니다.
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Experiment Design(프론티어15 실험 설계)

- hypothesis(가설): {summary['hypothesis']}
- changed_variable(변경 변수): runtime decision contract(런타임 결정 계약)
- primary_cell(1순위 칸): `{PRIMARY_CELL_ID}`
- controls(통제 변수): {', '.join(summary['controls'])}
- required_rows(필수 행): {', '.join(summary['required_rows'])}
- success_criteria(성공 기준): {summary['success_criteria']}
- failure_criteria(실패 기준): {summary['failure_criteria']}
- invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}
- evidence_plan(근거 계획): score contract manifest(점수 계약 목록), threshold manifest(임계값 목록), argmax baseline metrics(최대확률 기준 지표), model metrics(모델 지표), subperiod metrics(하위기간 지표), ONNX parity(온엑스 동등성)
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Prior Stage Scan(프론티어15 이전 단계 스캔)

Frontier14 closeout(프론티어14 마감): `{PARENT_RUN_ID}`.

Preserved clue(보존 단서): sparse cash-session q8 h8 plain logistic surface(희소 현금장 q8 h8 일반 로지스틱 표면)는 OOS(표본밖)에서 PF(수익 팩터)가 높고 DD(손실폭)가 낮았지만 density(빈도)가 부족했습니다.

Negative memory(부정 기억): label-side quota(라벨 쪽 할당)는 5~10/day(일 5~10회)에 가까웠지만 argmax model signal(최대확률 모델 신호)은 약 0.07~0.10/day(일 0.07~0.10회)로 무너졌습니다.

Reference only(참조 전용): F14(프론티어14)는 winner/baseline/promotion/runtime authority/live readiness/Goal Achieve(승자/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 넘기지 않습니다.
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    return f"""# Frontier15 Local Checks(프론티어15 로컬 확인)

Judgment(판정): `{summary['local_verification']['judgment']}`

{checks}
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Selection Metric Spec(프론티어15 선택 지표 명세)

- strict scout clue(엄격 탐색 단서): primary cell(1순위 칸) `{PRIMARY_CELL_ID}`가 validation/OOS(검증/표본밖) 양쪽에서 PF/density/DD/subperiod/parity(수익 팩터/빈도/손실폭/하위기간/동등성) 조건을 통과해야 합니다.
- preserved clue(보존 단서): non-primary cell(비 1순위 칸) 또는 일부 축만 좋은 row(행)는 다음 단계 전진 트리거가 아니라 clue(단서)로만 보존합니다.
- negative memory(부정 기억): train threshold(학습 임계값)가 validation/OOS(검증/표본밖) 빈도로 전이되지 않거나 PF/DD(수익 팩터/손실폭)가 무너지면 기록합니다.
"""


def input_refs(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Input Refs(프론티어15 입력 참조)

- Frontier14 selection(프론티어14 선택 상태): `{F14_SELECTION.as_posix()}`
- Frontier14 closeout report(프론티어14 마감 보고서): `{F14_CLOSEOUT_REPORT.as_posix()}`
- Grok stage-open output(그록 단계 개방 출력): `{summary['grok_output']}`
- score contract manifest(점수 계약 목록): `{(RUN_ROOT / 'score_contract_manifest.json').as_posix()}`
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier15A Stage Open Report(프론티어15A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier15(프론티어15)를 score threshold density controlled ONNX scout(점수 임계값 빈도 통제 온엑스 탐색)로 열었습니다.

Effect(효과): F14(프론티어14)의 argmax density cliff(최대확률 빈도 절벽)를 label retuning(라벨 재조정)이 아니라 decision contract(결정 계약) 변경으로 시험합니다.

Grok classification(그록 분류): `{summary['grok_classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Primary cell(1순위 칸): `{PRIMARY_CELL_ID}`

Score cells(점수 칸): `{len(summary['score_cells'])}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Review Index(프론티어15 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), 9-cell score grid(9칸 점수 격자) registered(등록됨).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier15A Required Gate Coverage Audit(프론티어15A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): hypothesis/controls/success/failure/invalid/stop boundary(가설/통제/성공/실패/무효/중지 경계) 기록됨.
- external_review_packet(외부 검토 묶음): Grok accepted(그록 수용), packet(묶음) `{summary['grok_packet']}`.
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Selection Status(프론티어15 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Primary cell(1순위 칸): `{PRIMARY_CELL_ID}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier15 Score Threshold Density Controlled ONNX Scout(결정: 프론티어15 점수 임계값 빈도 통제 온엑스 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier15(프론티어15)를 runtime decision contract(런타임 결정 계약) 가설로 열었습니다.

Effect(효과): F14(프론티어14)의 label family(라벨 계열)를 미세 조정하지 않고, probability score threshold(확률 점수 임계값)이 거래 빈도 축을 회복하는지 검증합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "",
    ])


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier15(프론티어15)는 ONNX probability tensor(온엑스 확률 텐서)를 score threshold signal contract(점수 임계값 신호 계약)로 읽는 가설로 열렸습니다.

Effect(효과): F14(프론티어14)에서 보인 argmax density cliff(최대확률 빈도 절벽)를 label retuning(라벨 재조정) 없이 검증할 수 있습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier15_stage_open_grok_accepted_score_threshold_contract_no_authority",
        "work_family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok_classification={summary['grok_classification']};primary_cell={PRIMARY_CELL_ID};score_cells=9",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "not_applicable(해당 없음)",
        "notes": f"next={NEXT_RUN_ID};score_threshold_contract;no_authority",
        "question": "Can ONNX probability score thresholds control density?(온엑스 확률 점수 임계값이 빈도를 통제할 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry() -> str:
    return (
        f"- `IDEA-FR15-SCORE-THRESHOLD-DENSITY-CONTROLLED-ONNX-SCOUT`: `{RUN_ID}` opens score threshold "
        "density controlled ONNX scout(점수 임계값 빈도 통제 온엑스 탐색). Effect(효과): F14(프론티어14)의 "
        "argmax density cliff(최대확률 빈도 절벽)를 runtime decision contract(런타임 결정 계약)로 검증합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier15(프론티어15) after Grok stage-open accepted"
        f"(그록 단계 개방 수용). Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` will test frozen 9-cell "
        f"score grid(고정 9칸 점수 격자) with primary cell(1순위 칸) `{PRIMARY_CELL_ID}` and no authority claims"
        "(권위 주장 없음).\n"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
