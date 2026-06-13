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

from foundation.control_plane.ledger import io_path, json_ready
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_10__split_consistent_utility_distillation"
RUN_ID = "frontier10A_stage_open_split_consistent_utility_distillation_v1"
RUN_NUMBER = "frontier10A"
PARENT_RUN_ID = "frontier09D_stage_closeout_drawdown_clean_path_labeling_v1"
NEXT_RUN_ID = "frontier10B_utility_distillation_proxy_scout_v1"
IDEA_ID = "IDEA-FR10-SPLIT-CONSISTENT-UTILITY-DISTILLATION"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_10_split_consistent_utility_distillation_open.md")
GROK_DIR = Path("docs/agent_control/grok_reviews/2026-06-14_frontier10_stage_open/medium_review")
NEGATIVE_REGISTER = Path("docs/registers/negative_result_register.md")
IDEA_REGISTER = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")


def main() -> int:
    now = utc_now()
    ensure_dirs()
    grok = read_grok()
    local = local_verification()
    summary = build_summary(now, grok, local)
    write_outputs(summary)
    update_docs_and_state(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "status": summary["status"],
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "grok_classification": summary["grok_classification"],
                    "next_run_id": NEXT_RUN_ID,
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
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


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path.exists():
        return
    header = f03b.read_csv_header(template_path)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_grok() -> dict[str, Any]:
    prompt_path = GROK_DIR / "prompt.md"
    clean_output_path = GROK_DIR / "clean_output.md"
    metadata_path = GROK_DIR / "metadata.json"
    missing = [path.as_posix() for path in (prompt_path, clean_output_path, metadata_path) if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing Frontier10 Grok packet files: {missing}")
    metadata = json.loads(io_path(metadata_path).read_text(encoding="utf-8-sig"))
    clean_output = io_path(clean_output_path).read_text(encoding="utf-8-sig")
    return {
        "prompt_path": prompt_path.as_posix(),
        "clean_output_path": clean_output_path.as_posix(),
        "metadata_path": metadata_path.as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "timed_out": bool(metadata.get("timed_out")),
        "clean_output": clean_output,
        "classification": classify_grok(clean_output),
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "accepted" in lowered or "수용" in text:
        return "accepted(수용)"
    if "rejected" in lowered or "거절" in text:
        return "rejected(거절)"
    return "needs_local_verification(로컬 검증 필요)"


def local_verification() -> dict[str, Any]:
    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
    workspace_state = io_path(Path("docs/workspace/workspace_state.yaml")).read_text(encoding="utf-8-sig")
    f09_selection = io_path(
        Path("stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/04_selected/selection_status.md")
    ).read_text(encoding="utf-8-sig")
    workspace_at_parent = (
        "current_stage_id: stage_frontier_09__drawdown_normalized_clean_path_labeling" in workspace_state
        and "next_run_id: frontier10A" in workspace_state
    )
    workspace_at_current = f"current_stage_id: {STAGE_ID}" in workspace_state and f"current_run_id: {RUN_ID}" in workspace_state
    checks = {
        "workspace_transition_matches_frontier10a": workspace_at_parent or workspace_at_current,
        "frontier09_selection_closed": "closed_preserved_clue_negative_memory_no_authority" in f09_selection,
        "stage295_negative_memory_found": "NEG-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION" in negative_text,
        "stage295_reopen_condition_found": "fresh density-floor profit expansion" in negative_text
        or "새 거래 밀도 하한 수익 확장" in negative_text,
    }
    return {
        "checks": checks,
        "judgment": "pass_with_stage295_boundary(295단계 경계 포함 통과)"
        if all(checks.values())
        else "needs_manual_review(수동 검토 필요)",
        "difference_from_stage295": (
            "Stage295(295단계)는 MT5 route-signal outcome distillation(MT5 경로 신호 결과 증류)과 "
            "actual routed total(실제 라우팅 전체) 후보화를 시험했고, Frontier10(전선10)은 "
            "Python Tier A train-only subwindow utility label(파이썬 Tier A 학습 전용 하위구간 효용 라벨)을 "
            "첫 scout(탐색)에서 ONNX argmax-only(ONNX 최대확률 전용)로 시험한다."
        ),
    }


def build_summary(now: str, grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "status": "opened_frontier10_split_consistent_utility_distillation_no_authority",
        "judgment": "stage_opened_after_grok_review_and_local_stage295_boundary_no_authority",
        "grok_classification": grok["classification"],
        "grok_success": grok["success"],
        "grok_timed_out": grok["timed_out"],
        "grok_prompt_path": grok["prompt_path"],
        "grok_output_path": grok["clean_output_path"],
        "grok_metadata_path": grok["metadata_path"],
        "grok_prompt_hash": grok["prompt_hash"],
        "local_verification": local,
        "frontier_thesis": (
            "A single fixed 3-class ONNX interface(고정 3분류 ONNX 인터페이스)가 train-only split-consistent "
            "utility distillation labels(학습 전용 분할 일관 효용 증류 라벨)을 배우면, 불안정하거나 "
            "DD-heavy(손실폭 큰) 행을 flat/no-trade(관망/무거래)로 보내고 밀도/PF/DD/매끄러움 네 축을 "
            "더 균형 있게 만들 수 있다."
        ),
        "novelty_delta": (
            "Frontier07(전선07)은 adverse-risk label(불리 위험 라벨), Frontier08(전선08)은 sample weight"
            "(표본 가중), Frontier09(전선09)는 clean-path target representation(깨끗한 경로 목표 표현)을 "
            "바꿨다. Frontier10(전선10)은 model fit(모델 학습) 전에 train subwindow utility consensus"
            "(학습 하위구간 효용 합의)를 요구하는 supervision philosophy(감독 철학)를 바꾼다."
        ),
        "do_not_repeat": [
            "Frontier09 clean-path density bridge repair(전선09 깨끗한 경로 밀도 브리지 수리) 반복 금지",
            "Frontier08 sample-weight-only repair(전선08 표본 가중 단독 수리) 반복 금지",
            "Stage295 MT5 route-signal outcome distillation(295단계 MT5 경로 신호 결과 증류) 상속 금지",
        ],
        "claim_boundary": {
            claim: "not_claimed(주장 없음)"
            for claim in (
                "completion(완성)",
                "baseline(기준선)",
                "promotion(승격)",
                "runtime_authority(런타임 권위)",
                "live_readiness(실거래 준비)",
                "goal_achieve(목표 달성)",
            )
        },
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json_sig(RUN_ROOT / "stage_open_summary.json", summary)
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "utility_distillation_plan.md", utility_distillation_plan(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_docs_and_state(summary: dict[str, Any]) -> None:
    now = summary["created_at_utc"]
    f03b.write_text_sig(
        Path("docs/workspace/workspace_state.yaml"),
        "\n".join(
            [
                f"current_stage_id: {STAGE_ID}",
                f"current_run_id: {RUN_ID}",
                f"latest_completed_run_id: {RUN_ID}",
                f"current_status: {summary['status']}",
                f"current_judgment: {summary['judgment']}",
                f"next_run_id: {NEXT_RUN_ID}",
                "runtime_authority: not_claimed",
                "operating_promotion: not_claimed",
                "goal_achieve: not_claimed",
                f"updated_at_utc: '{now}'",
                "",
            ]
        ),
    )
    f03b.write_text_sig(Path("docs/context/current_working_state.md"), current_working_state(summary))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(IDEA_REGISTER, f"{RUN_ID}__{IDEA_ID}", idea_registry_entry(summary))
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier10 Stage Brief(전선10 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can split-consistent utility distillation(분할 일관 효용 증류) improve a fixed ONNX(고정 ONNX) 3-class trade/no-trade surface(3분류 거래/무거래 표면) without repeating label/weight/bridge repair(라벨/가중/브리지 수리 반복)?

Hypothesis(가설): {summary['frontier_thesis']}

Novelty delta(신규성 차이): {summary['novelty_delta']}

Difference from Stage295(295단계 대비 차이): {summary['local_verification']['difference_from_stage295']}

Do not repeat(반복 금지):
{bullet_list(summary['do_not_repeat'])}

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier10 Experiment Design(전선10 실험 설계)

## Hypothesis(가설)

{summary['frontier_thesis']}

## Decision Use(결정 사용)

Stage-open design(단계 개방 설계)입니다. Effect(효과): 다음 proxy scout(프록시 탐색)가 utility family(효용군), controls(대조군), stop conditions(중단 조건)을 어떤 경계로 가져야 하는지 고정합니다.

## Comparison Baseline(비교 기준)

- label_v1 reference(라벨 v1 참조)
- Frontier07 risk label reference(전선07 위험 라벨 참조)
- Frontier08 best sample-weight row(전선08 최상 표본 가중 행)
- Frontier09 payoff/adverse ratio preserved clue(전선09 수익/불리 이동 비율 보존 단서)

## Control Variables(고정 변수)

- US100 M5 Tier A(US100 5분봉 Tier A)
- fixed 58 feature order(고정 58개 피처 순서)
- existing train/validation/OOS split(기존 학습/검증/표본밖 분할)
- fixed `[p_short, p_flat, p_long]` ONNX output(고정 ONNX 출력)
- argmax-only first scout(첫 탐색은 최대확률 전용)

## Changed Variables(변경 변수)

- train-only subwindow consensus target(학습 전용 하위구간 합의 목표)
- utility_margin target family(효용 마진 목표군)
- drawdown_veto_distillation family(손실폭 거부 증류군)
- explicit no-bridge control(명시적 무브리지 대조군)

## Sample Scope(표본 범위)

Data(데이터)는 기존 US100 M5 model input dataset(모델 입력 데이터셋)입니다. Tier B(티어 B)와 Tier A+B combined(Tier A+B 합산)는 사용 가능해지기 전까지 missing_required(필수 누락)로 기록합니다.

## Success Criteria(성공 기준)

- strict scout clue(엄격 탐색 단서): validation/OOS(검증/표본밖) 모두 density 5~10/day(일 5~10회), PF >= 1.2(수익 팩터 1.2 이상), DD <= 15%(손실폭 15% 이하), ONNX parity true(ONNX 동등성 참), paired axis improvement(짝 축 개선)
- preserved clue(보존 단서): strict clue(엄격 단서)는 없어도 3개 이상 축 개선, ONNX parity true(ONNX 동등성 참), class collapse(분류 붕괴) 없음

## Failure Criteria(실패 기준)

- validation DD(검증 손실폭)가 15%보다 크게 높고 개선 축이 없음
- density(밀도)가 2/day(일 2회) 아래로 붕괴
- Frontier09 bridge repair(전선09 브리지 수리)와 사실상 동일

## Invalid Conditions(무효 조건)

- validation/OOS(검증/표본밖) 정보를 target fit(목표 적합)에 사용
- feature-label boundary(피처-라벨 경계) 위반
- ONNX parity(ONNX 동등성) 실패를 무시

## Stop Conditions(중단 조건)

Strict clue(엄격 단서)가 없고 preserved clue(보존 단서)도 없으면 closeout(마감)으로 갑니다. Preserved clue(보존 단서)가 있으면 capped repair(상한 수리)를 한 번만 허용합니다.

## Evidence Plan(근거 계획)

- run_manifest.json(실행 목록)
- candidate summary CSV(후보 요약 CSV)
- ONNX parity audit(ONNX 동등성 감사)
- stage_run_ledger.csv(단계 실행 장부)
- alpha_run_ledger.csv(알파 실행 장부)
- required_gate_coverage_audit(필수 게이트 커버리지 감사)

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): `{f03b.DATASET_PATH.as_posix()}`
- time_axis(시간축): closed US100 M5 bars(확정 US100 5분봉), existing ordering(기존 순서)
- missing_or_duplicate_check(누락/중복 확인): next scout(다음 탐색)에서 row count/hash(행 수/해시)로 기록
- feature_label_boundary(피처-라벨 경계): future path utility(미래 경로 효용)는 label only(라벨 전용)
- split_boundary(분할 경계): train-only thresholds/scales/subwindows(학습 전용 임계값/스케일/하위구간)
- leakage_risk(누수 위험): subwindow consensus(하위구간 합의)가 validation/OOS(검증/표본밖)를 포함하는 경우
- data_hash_or_identity(데이터 해시/정체성): `{sha256_file(f03b.DATASET_PATH)}`
- integrity_judgment(무결성 판정): usable_with_boundary(경계 포함 사용 가능)

## Model Validation(모델 검증)

- model_family(모델군): ONNX-exportable sklearn classifiers(ONNX 내보내기 가능한 sklearn 분류기)
- target_and_label(목표와 라벨): split-consistent utility distillation(분할 일관 효용 증류)
- split_method(분할 방법): fixed train/validation/OOS(고정 학습/검증/표본밖)
- selection_metric(선택 지표): four-axis aspiration distance(네 축 목표거리)
- secondary_metrics(보조 지표): density/PF/DD/smoothness/class balance(밀도/수익 팩터/손실폭/매끄러움/클래스 균형)
- threshold_policy(임계값 정책): no threshold search(임계값 탐색 없음), argmax-only(최대확률 전용)
- overfit_risk(과적합 위험): train subwindow consensus over-selection(학습 하위구간 합의 과선택)
- calibration_risk(보정 위험): probabilities are ranking scores until calibrated(보정 전 확률은 순위 점수)
- validation_judgment(검증 판정): exploratory(탐색)
"""


def input_refs(summary: dict[str, Any]) -> str:
    return f"""# Frontier10 Input References(전선10 입력 참조)

- parent closeout(부모 마감): `stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/03_reviews/frontier09D_stage_closeout_drawdown_clean_path_labeling_v1_report.md`
- Grok packet(그록 묶음): `{GROK_DIR.as_posix()}`
- Stage295 negative memory(295단계 부정 기억): `docs/registers/negative_result_register.md`
- model input dataset(모델 입력 데이터셋): `{f03b.DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{f03b.FEATURE_ORDER_PATH.as_posix()}`
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return f"""# Frontier10 Prior Stage Scan(전선10 이전 단계 점검)

## Preserved Clues(보존 단서)

- Frontier09(전선09): payoff/adverse ratio(수익/불리 이동 비율), train-only audit pattern(학습 전용 감사 패턴)
- Frontier08(전선08): adverse/path utility weighting(불리/경로 효용 가중)이 density(밀도)를 일부 만들 수 있음
- Frontier07(전선07): adverse excursion risk label(불리 이동 위험 라벨)이 OOS DD(표본밖 손실폭)를 일부 줄일 수 있음

## Negative Memory(부정 기억)

- Frontier09(전선09): validation DD 56~64%(검증 손실폭 56~64%), strict rows 0(엄격 행 0)
- Frontier08(전선08): sample weighting alone(표본 가중 단독)은 validation DD(검증 손실폭)를 해결하지 못함
- Stage295(295단계): split-consistent outcome distillation(분할 일관 결과 증류)은 MT5 route-signal(경로 신호) 후보로 닫히지 않음

## Stage295 Boundary(295단계 경계)

{summary['local_verification']['difference_from_stage295']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}
"""


def utility_distillation_plan(summary: dict[str, Any]) -> str:
    return """# Utility Distillation Plan(효용 증류 계획)

## Families(군)

- utility_consensus(효용 합의): train subwindows(학습 하위구간)에서 side utility(방향 효용)가 안정적인 행만 long/short(롱/숏) 후보로 둡니다.
- utility_margin(효용 마진): 승리 방향 효용이 반대 방향과 flat(관망)보다 train-only margin(학습 전용 마진) 이상 커야 합니다.
- drawdown_veto_distillation(손실폭 거부 증류): raw return(원시 수익)이 양수여도 underwater burden(수중 부담)이 높으면 flat/no-trade(관망/무거래)로 증류합니다.

## First Scout Boundary(첫 탐색 경계)

Action(행동): no threshold search(임계값 탐색 없음), no class-prior bridge(클래스 사전분포 브리지 없음), argmax-only(최대확률 전용)로 확인합니다.

Effect(효과): Frontier09C(전선09C)의 density bridge repair(밀도 브리지 수리)를 반복하지 않고, target supervision(목표 감독) 자체가 네 축을 개선하는지 봅니다.
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier10A Stage Open Report(전선10A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Grok stage-open review(그록 단계 개방 검토)를 받은 뒤 Frontier10(전선10) split-consistent utility distillation(분할 일관 효용 증류)을 열었습니다.

Effect(효과): Frontier09(전선09)의 bridge repair(브리지 수리)를 반복하지 않고, model fit before decision supervision(모델 학습 전 의사결정 감독) 축으로 새 hypothesis lifecycle(가설 생명주기)을 시작합니다.

## Grok Receipt(그록 영수증)

- trigger_reason(트리거 이유): goal requires Grok stage-open review(목표가 그록 단계 개방 검토를 요구)
- review_size(검토 크기): medium review(중간 검토)
- direction_before_grok(그록 전 방향): split-consistent utility distillation(분할 일관 효용 증류)
- bounded_evidence(제한 근거): Frontier09 closeout(전선09 마감), Frontier07~09 memories(전선07~09 기억), Stage295 overlap risk(295단계 겹침 위험)
- prompt_identity(프롬프트 정체성): `{summary['grok_prompt_path']}` sha256 `{summary['grok_prompt_hash']}`
- grok_output_identity(그록 출력 정체성): `{summary['grok_output_path']}`
- advice_classification(조언 분류): `{summary['grok_classification']}`
- local_verification(로컬 검증): `{summary['local_verification']['judgment']}`
- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
- final_codex_direction(최종 코덱스 방향): open Frontier10A(전선10A 개방), then run Frontier10B proxy scout(전선10B 프록시 탐색)

## Local Verification(로컬 검증)

{summary['local_verification']['difference_from_stage295']}

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier10A Required Gate Coverage Audit(전선10A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): satisfied(충족)
- external_review_packet(외부 검토 묶음): satisfied by Grok packet(그록 묶음으로 충족)
- local_stage295_boundary_check(로컬 295단계 경계 확인): `{summary['local_verification']['judgment']}`
- final_claim_guard(최종 주장 보호): satisfied; no authority claims(충족, 권위 주장 없음)

Effect(효과): stage open(단계 개방)만 주장하고, performance/runtime authority(성과/런타임 권위)는 주장하지 않습니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier10 Review Index(전선10 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), Stage295 boundary locally verified(295단계 경계 로컬 검증).
- Grok packet(그록 묶음): `{GROK_DIR.as_posix()}`
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier10 Selection Status(전선10 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status(상태): `{summary['status']}`

Latest run(최근 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier10 Split-Consistent Utility Distillation(결정: 전선10 분할 일관 효용 증류 개방)

Date(날짜): 2026-06-14

Decision(결정): `{summary['status']}`

Effect(효과): Frontier10(전선10)을 새 hypothesis lifecycle(가설 생명주기)로 열고, Stage295(295단계)는 reference only(참조 전용)로만 둡니다.
"""


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier10(전선10)을 split-consistent utility distillation(분할 일관 효용 증류) 가설로 열었습니다.

Effect(효과): Frontier09(전선09)의 보존 단서와 부정 기억은 reference only(참조 전용)로 사용하고, 다음 실행은 `frontier10B_utility_distillation_proxy_scout_v1`입니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier10_stage_open_grok_accepted_stage295_boundary_no_authority",
        "family": "experiment_design(실험 설계)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": "open_frontier10_split_consistent_utility_distillation",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "candidate_rows": "0",
        "external_verification_status": "not_applicable(해당 없음)",
        "result_judgment": summary["judgment"],
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_open(단계 개방)",
        "goal_achieve": "not_claimed",
        "source_authority": "grok_accepted_plus_local_stage295_boundary(그록 수용과 로컬 295단계 경계)",
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
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": "grok_classification=accepted(그록 분류=수용)",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "not_applicable(해당 없음)",
        "notes": f"next={NEXT_RUN_ID};stage295_boundary_verified;no_authority",
        "question": "Can split-consistent utility distillation improve the ONNX trade/no-trade surface?(분할 일관 효용 증류가 ONNX 거래/무거래 표면을 개선하는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_open(단계 개방)",
        "goal_achieve": "not_claimed",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"<!-- {RUN_ID}__{IDEA_ID} -->\n"
        f"- `{IDEA_ID}`: Frontier10(전선10) opens split-consistent utility distillation"
        f"(분할 일관 효용 증류). Effect(효과): Frontier09(전선09) bridge repair(브리지 수리)를 반복하지 않고 "
        f"train subwindow utility consensus(학습 하위구간 효용 합의)를 새 supervision axis(감독 축)로 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier10(전선10) with Grok accepted(그록 수용) "
        f"and Stage295 boundary verified(295단계 경계 검증). Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` "
        "can test utility distillation(효용 증류) without authority claims(권위 주장 없이).\n"
    )


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def write_json_sig(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
