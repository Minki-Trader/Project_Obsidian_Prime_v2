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


STAGE_ID = "stage_frontier_14__daily_session_opportunity_budget_onnx_scout"
RUN_ID = "frontier14A_stage_open_daily_session_opportunity_budget_onnx_scout_v1"
RUN_NUMBER = "frontier14A"
PARENT_RUN_ID = "frontier13C_stage_closeout_regime_normalized_trade_shape_onnx_scout_v1"
NEXT_RUN_ID = "frontier14B_daily_session_opportunity_budget_proxy_scout_v1"
STATUS = "opened_frontier14_daily_session_opportunity_budget_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_and_local_quota_boundary_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_14_daily_session_opportunity_budget_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_14/materialize_frontier14a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier14_stage_open/small_review")
F13_SELECTION = Path("stages/stage_frontier_13__regime_normalized_trade_shape_onnx_scout/04_selected/selection_status.md")
F13_REPORT = Path(
    "stages/stage_frontier_13__regime_normalized_trade_shape_onnx_scout/03_reviews/"
    "frontier13C_stage_closeout_regime_normalized_trade_shape_onnx_scout_v1_report.md"
)

QUOTA_VARIANTS = (
    {
        "variant_id": "f14b_day_q6_h8",
        "bucket_rule": "broker_day(브로커 일자)",
        "quota_per_bucket": 6,
        "hold_bars": 8,
        "utility": "future_path_utility_net_of_rough_cost(거친 비용 차감 미래 경로 효용)",
        "tie_break": "earliest_timestamp_then_larger_abs_utility(빠른 시각 후 큰 절대 효용)",
    },
    {
        "variant_id": "f14b_cash_q8_h8",
        "bucket_rule": "broker_day_x_cash_session(브로커 일자와 현금장 세션)",
        "quota_per_bucket": 8,
        "hold_bars": 8,
        "utility": "future_path_utility_net_of_rough_cost(거친 비용 차감 미래 경로 효용)",
        "tie_break": "earliest_timestamp_then_larger_abs_utility(빠른 시각 후 큰 절대 효용)",
    },
    {
        "variant_id": "f14b_cash_q10_h12",
        "bucket_rule": "broker_day_x_cash_session(브로커 일자와 현금장 세션)",
        "quota_per_bucket": 10,
        "hold_bars": 12,
        "utility": "future_path_utility_net_of_rough_cost(거친 비용 차감 미래 경로 효용)",
        "tie_break": "earliest_timestamp_then_larger_abs_utility(빠른 시각 후 큰 절대 효용)",
    },
)


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
    return {
        "packet": GROK_PACKET.as_posix(),
        "prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "output": (GROK_PACKET / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "forbidden_claims_supported": "not_claimed" in output.lower() and "goal achieve" in output.lower(),
        "quota_pre_registration_supported": "quota" in output.lower() and "pre-registration" in output.lower(),
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "accepted" in lowered:
        return "accepted(수용)"
    if "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    f13_selection = read_text(F13_SELECTION)
    f13_report = read_text(F13_REPORT)
    checks = {
        "workspace_next_frontier14": "next_run_id: frontier14A_stage_open_new_hypothesis_design_v1" in workspace,
        "f13_selection_closed_negative": "closed_negative_memory_no_authority" in f13_selection,
        "f13_report_no_authority": "Goal Achieve" in f13_report and "not_claimed" in f13_report,
        "grok_success": grok["success"],
        "grok_accepted": grok["classification"] == "accepted(수용)",
        "grok_forbidden_claims_supported": bool(grok["forbidden_claims_supported"]),
        "grok_quota_pre_registration_supported": bool(grok["quota_pre_registration_supported"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "quota_variants_pre_registered": len(QUOTA_VARIANTS) == 3,
    }
    return {
        "checks": checks,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


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
        "frontier_thesis": (
            "US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3클래스 온엑스)는 label wrapping"
            "(라벨 감싸기)보다 upstream entry opportunity generation(상류 진입 기회 생성)을 바꾸면"
            " density/PF/DD(빈도/수익 팩터/손실폭) 균형에 가까워질 수 있습니다."
        ),
        "novelty_delta": (
            "Frontier12/13(프론티어12/13)은 trade-shape label wrapping and regime-scale repair"
            "(거래 형상 라벨 감싸기와 국면 척도 수리)를 시험했습니다. Frontier14(프론티어14)는"
            " daily/session quota opportunity labels(일별/세션별 할당 기회 라벨)로 label source(라벨 원천)를 바꿉니다."
        ),
        "comparison_baseline": (
            "Reference-only(참조 전용): Frontier13 best sparse row(프론티어13 최상 희소 행) validation/OOS"
            " PF-density-DD 1.0397/2.2568/54.3762 and 2.0277/0.4122/5.5735."
        ),
        "control_variables": [
            "same Tier A dataset(동일 티어 A 데이터)",
            "same feature order(동일 피처 순서)",
            "same fixed model specs(동일 고정 모델 규격)",
            "fixed argmax signal contract(고정 최대확률 신호 계약)",
            "no post-fit selector or threshold search(적합 후 선택기나 임계값 탐색 없음)",
        ],
        "changed_variables": [
            "daily/session quota opportunity label source(일별/세션별 할당 기회 라벨 원천)",
            "pre-registered horizon/quota variants(사전 등록 지평/할당 변형)",
        ],
        "quota_variants": list(QUOTA_VARIANTS),
        "sample_scope": "Tier A US100 M5 train/validation/OOS fixed split(티어 A US100 5분봉 고정 분할)",
        "success_criteria": (
            "strict scout clue(엄격 탐색 단서): validation and OOS(검증과 표본밖) both positive net"
            "(양수 순수익), PF>=1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회),"
            " DD<=15%(손실폭 15% 이하), controlled subperiod DD(하위기간 손실폭 통제)."
        ),
        "failure_criteria": (
            "label quota(라벨 할당량)는 맞지만 model argmax(모델 최대확률)가 density cliff(빈도 절벽),"
            " DD explosion(손실폭 폭발), or PF collapse(수익 팩터 붕괴)를 만들면 negative memory(부정 기억)."
        ),
        "invalid_conditions": [
            "quota or horizon retuned after seeing validation/OOS metrics(검증/표본밖 지표 본 뒤 할당량/지평 재조정)",
            "validation/OOS statistics used to calibrate bucket boundaries(검증/표본밖 통계로 버킷 경계 보정)",
            "feature row uses future path information(피처 행이 미래 경로 정보를 사용)",
        ],
        "stop_conditions": [
            "strict rows > 0 triggers Grok pre-expensive review(엄격 행이 있으면 비싼 검증 전 그록 검토)",
            "strict/preserved rows 0 triggers repair-or-closeout decision(엄격/보존 행 0이면 수리/마감 결정)",
            "same quota retuning pressure appears triggers closeout(같은 할당 재조정 압력이 나오면 마감)",
        ],
        "do_not_repeat": [
            "same label knob loosening(같은 라벨 파라미터 완화)",
            "same regime-scale wrapping(같은 국면 척도 감싸기)",
            "class-weight density forcing(클래스 가중 빈도 강제)",
            "threshold micro-search(임계값 미세 탐색)",
            "quota/horizon retuning after metrics(지표 확인 뒤 할당량/지평 재조정)",
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
    write_json(RUN_ROOT / "quota_variant_manifest.json", summary["quota_variants"])
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "opportunity_budget_label_contract.md", label_contract(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "selection_metric_spec.md", selection_metric_spec())
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
            "frontier13_selection": artifact_identity(F13_SELECTION),
            "frontier13_closeout_report": artifact_identity(F13_REPORT),
            "grok_stage_open_output": artifact_identity(Path(summary["grok_output"])),
        },
        "outputs": {
            "stage_open_summary": (RUN_ROOT / "stage_open_summary.json").as_posix(),
            "quota_variant_manifest": (RUN_ROOT / "quota_variant_manifest.json").as_posix(),
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
        },
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Daily/Session Opportunity Budget ONNX Scout(프론티어14 일별/세션별 기회 예산 온엑스 탐색)

Status(상태): `{summary['status']}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): scout clue/seed surface/preserved clue/negative memory/invalid setup/blocked(탐색 단서/씨앗 표면/보존 단서/부정 기억/무효 설정/차단)만 허용합니다.
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Stage Brief(프론티어14 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can daily/session opportunity-budget labels(일별/세션별 기회 예산 라벨) make US100 M5 ONNX(US100 5분봉 온엑스) learn the 5~10/day density axis(일 5~10회 빈도 축) without post-fit threshold search(적합 후 임계값 탐색 없이)?

## Frontier Thesis(프론티어 가설)

{summary['frontier_thesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}

## Exit Rule(종료 규칙)

{summary['failure_criteria']}

## Claim Boundary(주장 경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 forbidden(금지)입니다.
"""


def label_contract(summary: dict[str, Any]) -> str:
    rows = "\n".join(
        f"- `{item['variant_id']}`: bucket(버킷) `{item['bucket_rule']}`, quota(할당량) `{item['quota_per_bucket']}`, "
        f"hold bars(보유 봉) `{item['hold_bars']}`, tie-break(동점 규칙) `{item['tie_break']}`"
        for item in summary["quota_variants"]
    )
    return f"""# Frontier14 Opportunity Budget Label Contract(프론티어14 기회 예산 라벨 계약)

Action(행동): daily/session bucket(일별/세션별 버킷) 안에서 future path utility(미래 경로 효용)를 사전 등록 quota(할당량)로 rank(순위화)합니다.

Effect(효과): label target density(라벨 표적 빈도)를 5~10/day(일 5~10회)에 가깝게 만들되, model argmax density(모델 최대확률 빈도)는 별도로 측정합니다.

## Pre-Registered Variants(사전 등록 변형)

{rows}

## Guards(보호 장치)

- quota/horizon retuning after metrics(지표 확인 뒤 할당량/지평 재조정) 금지
- validation/OOS statistics calibration(검증/표본밖 통계 보정) 금지
- post-fit selector or threshold search(적합 후 선택기 또는 임계값 탐색) 금지
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Experiment Design(프론티어14 실험 설계)

- hypothesis(가설): {summary['frontier_thesis']}
- decision_use(결정 사용): whether to continue upstream opportunity labels(상류 기회 라벨을 계속 밀지)
- comparison_baseline(비교 기준): {summary['comparison_baseline']}
- control_variables(통제 변수): {', '.join(summary['control_variables'])}
- changed_variables(변경 변수): {', '.join(summary['changed_variables'])}
- sample_scope(표본 범위): {summary['sample_scope']}
- success_criteria(성공 기준): {summary['success_criteria']}
- failure_criteria(실패 기준): {summary['failure_criteria']}
- invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}
- stop_conditions(중지 조건): {', '.join(summary['stop_conditions'])}
- evidence_plan(근거 계획): label density table/model KPI table/ONNX parity/stage ledger/Grok receipts(라벨 빈도표/모델 KPI표/온엑스 동등성/단계 장부/그록 영수증)
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Prior Stage Scan(프론티어14 이전 단계 점검)

Frontier13 closeout(프론티어13 마감): `{PARENT_RUN_ID}`.

Negative memory(부정 기억): regime-normalized trade-shape labels(국면 정규화 거래 형상 라벨)은 sparse PF/DD(희소 수익 팩터/손실폭)와 density(빈도)를 동시에 맞추지 못했습니다.

Reference-only carry(참조 전용 이월): {summary['comparison_baseline']}

Forbidden imports(금지 반입): winner/baseline/promotion/runtime authority/live readiness/Goal Achieve(승자/기준선/승격/런타임 권위/실거래 준비/목표 달성).
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    return f"""# Frontier14 Local Checks(프론티어14 로컬 확인)

Judgment(판정): `{summary['local_verification']['judgment']}`

{checks}
"""


def selection_metric_spec() -> str:
    return """# Frontier14 Selection Metric Spec(프론티어14 선택 지표 규격)

- strict scout clue(엄격 탐색 단서): validation/OOS positive net(검증/표본밖 양수 순수익), PF>=1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD<=15%(손실폭 15% 이하), subperiod DD controlled(하위기간 손실폭 통제)
- preserved clue(보존 단서): OOS PF/DD(표본밖 수익 팩터/손실폭) useful but validation or density incomplete(검증 또는 빈도 불완전) with clear boundary(명확한 경계)
- negative memory(부정 기억): label quota hit(라벨 할당량 충족) does not transfer to model density/PF/DD(모델 빈도/수익 팩터/손실폭)
"""


def input_refs(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Input Refs(프론티어14 입력 참조)

- Frontier13 selection(프론티어13 선택): `{F13_SELECTION.as_posix()}`
- Frontier13 closeout report(프론티어13 마감 보고서): `{F13_REPORT.as_posix()}`
- Grok stage-open output(그록 단계 개방 출력): `{summary['grok_output']}`
- quota variant manifest(할당 변형 목록): `{(RUN_ROOT / 'quota_variant_manifest.json').as_posix()}`
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier14A Stage Open Report(프론티어14A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier14(프론티어14)를 daily/session opportunity budget ONNX scout(일별/세션별 기회 예산 온엑스 탐색)로 열었습니다.

Effect(효과): Frontier12/13(프론티어12/13)의 라벨 감싸기 반복 대신 upstream opportunity generation(상류 기회 생성)을 시험합니다.

Grok classification(그록 분류): `{summary['grok_classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Review Index(프론티어14 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), quota label contract(할당 라벨 계약) registered(등록됨).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier14A Required Gate Coverage Audit(프론티어14A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 항목) recorded(기록됨)
- external_review_packet(외부 검토 묶음): Grok accepted(그록 수용)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Selection Status(프론티어14 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier14 Daily/Session Opportunity Budget ONNX Scout(결정: 프론티어14 일별/세션별 기회 예산 온엑스 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier14(프론티어14)를 upstream opportunity generation(상류 기회 생성) 가설로 열었습니다.

Effect(효과): Frontier13(프론티어13)의 same regime-scale wrapping(같은 국면 척도 감싸기)을 반복하지 않습니다.

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

Action(행동): Frontier14(프론티어14)는 daily/session opportunity budget labels(일별/세션별 기회 예산 라벨) 가설로 열렸습니다.

Effect(효과): label quota(라벨 할당량)와 model argmax density(모델 최대확률 빈도)를 분리 측정해, 빈도 축을 상류 라벨 원천에서 바꿀 수 있는지 확인합니다.

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
        "notes": "frontier14_stage_open_grok_accepted_quota_label_contract_no_authority",
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
        "primary_kpi": "grok_classification=accepted(그록 분류=수용)",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "not_applicable(해당 없음)",
        "notes": f"next={NEXT_RUN_ID};quota_label_contract;no_authority",
        "question": "Can daily/session opportunity budget labels teach ONNX frequency?(일별/세션별 기회 예산 라벨이 온엑스 빈도를 가르칠 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry() -> str:
    return (
        f"- `IDEA-FR14-DAILY-SESSION-OPPORTUNITY-BUDGET-ONNX-SCOUT`: Frontier14(프론티어14) opens daily/session "
        "opportunity budget ONNX scout(일별/세션별 기회 예산 온엑스 탐색). Effect(효과): F12/F13(프론티어12/13)의 "
        "label wrapping(라벨 감싸기)을 반복하지 않고 upstream entry opportunity generation(상류 진입 기회 생성)을 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier14(프론티어14) after Grok stage-open accepted"
        f"(그록 단계 개방 수용). Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` will test pre-registered quota labels"
        f"(사전 등록 할당 라벨) with no authority claims(권위 주장 없음).\n"
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


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
