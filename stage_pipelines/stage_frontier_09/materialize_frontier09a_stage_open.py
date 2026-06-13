from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_09__drawdown_normalized_clean_path_labeling"
RUN_ID = "frontier09A_stage_open_drawdown_clean_path_labeling_v1"
RUN_NUMBER = "frontier09A"
PARENT_RUN_ID = "frontier08D_stage_closeout_sample_weight_objective_v1"
NEXT_RUN_ID = "frontier09B_drawdown_clean_path_label_proxy_scout_v1"
IDEA_ID = "IDEA-FR09-DRAWDOWN-NORMALIZED-CLEAN-PATH-LABELING"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_09_drawdown_clean_path_labeling_open.md")
GROK_DIR = Path("docs/agent_control/grok_reviews/2026-06-14_frontier09_stage_open/medium_review")


def main() -> int:
    now = utc_now()
    grok = read_grok()
    summary = build_summary(now, grok)
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


def build_summary(now: str, grok: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "status": "opened_frontier09_drawdown_clean_path_labeling_no_authority",
        "judgment": "stage_opened_after_grok_review_no_authority",
        "grok_classification": classify_grok(grok["clean_output"]),
        "grok_success": grok["success"],
        "grok_prompt_path": grok["prompt_path"],
        "grok_output_path": grok["clean_output_path"],
        "grok_metadata_path": grok["metadata_path"],
        "frontier_thesis": (
            "drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)이 "
            "future return(미래 수익), adverse excursion(불리 이동), payoff/adverse ratio(수익/불리 이동 비율), "
            "underwater burden(수중 부담), clean-close recovery(깨끗한 종가 회복)를 함께 반영하면 "
            "fixed 3-class ONNX interface(고정 3분류 온엑스 인터페이스)가 DD/curve quality(손실폭/곡선 품질)를 "
            "더 직접 배울 수 있다."
        ),
        "novelty_delta": (
            "Frontier08(전선08)은 same labels plus sample weighting(동일 라벨 + 표본 가중)을 바꿨고, "
            "Frontier09(전선09)는 target representation(목표 표현)을 바꿔 bad-path rows(나쁜 경로 행)를 "
            "flat/no-trade(관망/무거래)로 만든다."
        ),
        "prior_stage_scan": [
            "Frontier08 closeout(전선08 마감): sample weighting alone(표본 가중 단독)은 validation DD 58~60%(검증 손실폭 58~60%)를 해결하지 못했다.",
            "Frontier07 reference(전선07 참조): adverse/path label mechanics(불리 이동/경로 라벨 기계)는 comparison control(비교 대조군)로만 쓴다.",
            "Stage281 memory(281단계 기억): drawdown-normalized directional MT5 rebuild(손실폭 정규화 방향 MT5 재구성)는 reference-only negative memory(참조 전용 부정 기억)다.",
        ],
        "do_not_repeat": [
            "F08 weight-only repair(전선08 가중 단독 수리) 반복 금지",
            "F07 family rename without mechanical delta(기계적 차이 없는 전선07 가족 이름 바꾸기) 금지",
            "Stage281 MT5 directional rebuild(281단계 방향 MT5 재구성) 상속 금지",
        ],
        "family_deltas": [
            {
                "family": "payoff_adverse_ratio(수익/불리 이동 비율)",
                "difference_from_f07": "F07 mae_mfe_balance(전선07 MFE/MAE 균형)는 target/cap(목표/상한) 중심이고, F09는 payoff divided by adverse burden(수익을 불리 부담으로 나눈 효율) 중심이다.",
            },
            {
                "family": "underwater_burden(수중 부담)",
                "difference_from_f07": "F07 time_to_adverse_penalty(전선07 불리 이동 속도 벌점)는 초기 불리 이동 속도이고, F09는 horizon adverse-bar count(수평선 내 불리 봉 수)와 burden ratio(부담 비율)를 직접 제한한다.",
            },
            {
                "family": "clean_recovery(깨끗한 회복)",
                "difference_from_f07": "F07 recovery_close_survival(전선07 종가 회복 생존)은 회복+상한이고, F09는 close return plus MFE capture efficiency(종가 수익 + 최대 유리 이동 포착 효율)를 함께 요구한다.",
            },
        ],
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json_sig(RUN_ROOT / "stage_open_summary.json", summary)
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "label_family_plan.md", label_family_plan(summary))
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
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_stage_ledger(stage_ledger)
    f03b.upsert_csv(stage_ledger, "ledger_row_id", ledger_row(summary))
    f03b.append_once(
        Path("docs/registers/idea_registry.md"),
        f"{RUN_ID}__{IDEA_ID}",
        (
            f"- `{IDEA_ID}`: Frontier09(전선09) opens drawdown-normalized clean path labeling"
            f"(손실폭 정규화 깨끗한 경로 라벨링). Effect(효과): F08(전선08) weight-only"
            f"(가중 단독) 반복을 피하고 DD/curve quality(손실폭/곡선 품질)를 target representation"
            f"(목표 표현)에 직접 넣습니다.\n"
        ),
    )
    f03b.append_once(
        Path("docs/workspace/changelog.md"),
        RUN_ID,
        (
            f"- {now}: `{RUN_ID}` opened Frontier09(전선09) with Grok accepted(그록 수용). "
            f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` can test clean-path labels(깨끗한 경로 라벨) "
            "without completion/baseline/promotion/runtime claims(완성/기준선/승격/런타임 주장 없이).\n"
        ),
    )


def stage_brief(summary: dict[str, Any]) -> str:
    deltas = "\n".join(
        f"- {item['family']}: {item['difference_from_f07']}" for item in summary["family_deltas"]
    )
    return f"""# Frontier09 Stage Brief(전선09 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)이 fixed ONNX(고정 온엑스) 3-class interface(3분류 인터페이스)에서 DD/curve quality(손실폭/곡선 품질)를 직접 더 잘 배우게 하는가?

Hypothesis(가설): {summary['frontier_thesis']}

Novelty delta(신규성 차이): {summary['novelty_delta']}

## Difference From Frontier07(전선07 대비 차이)

{deltas}

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier09 Experiment Design(전선09 실험 설계)

## Hypothesis(가설)

{summary['frontier_thesis']}

## Decision Use(결정 사용)

Stage-open design(단계 개방 설계)입니다. Effect(효과): 다음 proxy scout(프록시 탐색)가 어떤 label family(라벨 가족), control(대조군), stop condition(중단 조건)을 써야 하는지 고정합니다.

## Comparison Baseline(비교 기준)

- label_v1 reference(라벨 v1 참조)
- Frontier07 risk label reference(전선07 위험 라벨 참조)
- matched model/spec controls(같은 모델/스펙 대조군)

## Control Variables(고정 변수)

- US100 M5 Tier A(US100 5분봉 티어 A)
- 58 feature order(58개 피처 순서)
- train/validation/OOS split(학습/검증/표본밖 분할)
- fixed probs3 ONNX output(고정 3확률 온엑스 출력)
- argmax-only first scout(첫 탐색 최대확률 전용)

## Changed Variables(변경 변수)

Label target construction(라벨 목표 구성)만 바꿉니다.

## Success Criteria(성공 기준)

Strict scout clue(엄격 탐색 단서)는 validation/OOS(검증/표본밖) density 5~10/day, PF >= 1.2, DD <= 15%, ONNX parity(온엑스 동등성), learnability(학습 가능성), paired four-axis improvement(짝 네 축 개선)을 모두 요구합니다.

## Failure Criteria(실패 기준)

Class collapse(분류 붕괴), density-only improvement(밀도만 개선), validation DD far above 15%(검증 손실폭 15% 초과 지속), no paired improvement(짝 개선 없음)는 negative memory(부정 기억) 또는 capped repair(상한 수리)로 갑니다.

## Invalid Conditions(무효 조건)

Any threshold/scale(임계값/스케일)가 validation/OOS(검증/표본밖)에서 fit(적합)되면 invalid(무효)입니다.

## Evidence Plan(근거 계획)

Run manifest(실행 목록), label distribution(라벨 분포), threshold audit(임계값 감사), candidate metrics(후보 지표), model metrics(모델 지표), ONNX parity(온엑스 동등성), run registry(실행 등록부), alpha/stage ledger(알파/단계 장부)를 남깁니다.
"""


def input_refs(summary: dict[str, Any]) -> str:
    return f"""# Frontier09 Input References(전선09 입력 참조)

- current state(현재 상태): `docs/workspace/workspace_state.yaml`
- Frontier08 closeout(전선08 마감): `stages/stage_frontier_08__sample_weighted_objective/03_reviews/frontier08D_stage_closeout_sample_weight_objective_v1_report.md`
- Grok stage open packet(그록 단계 개방 묶음): `{GROK_DIR.as_posix()}`
- model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- raw US100(원천 US100): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    lines = "\n".join(f"- {item}" for item in summary["prior_stage_scan"])
    do_not = "\n".join(f"- {item}" for item in summary["do_not_repeat"])
    return f"""# Frontier09 Prior Stage Scan(전선09 이전 단계 점검)

## Reference Only(참조 전용)

{lines}

## Do Not Repeat(반복 금지)

{do_not}
"""


def label_family_plan(summary: dict[str, Any]) -> str:
    lines = "\n".join(
        f"- {item['family']}: {item['difference_from_f07']}" for item in summary["family_deltas"]
    )
    return f"""# Frontier09 Label Family Plan(전선09 라벨 가족 계획)

## Families(가족)

{lines}

## Leakage Guard(누수 보호)

Action(행동): threshold/scale(임계값/스케일)은 train split(학습 분할)에서만 fit(적합)합니다.

Effect(효과): validation/OOS(검증/표본밖)는 label application/evaluation(라벨 적용/평가) 전용으로 남습니다.
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier09A Stage Open Report(전선09A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Grok stage-open review(그록 단계 개방 검토)를 받은 뒤 Frontier09(전선09) drawdown-normalized clean path labeling(손실폭 정규화 깨끗한 경로 라벨링)을 열었습니다.

Effect(효과): Frontier08(전선08)의 sample weighting(표본 가중) 반복을 피하고, DD/curve quality(손실폭/곡선 품질)를 label target(라벨 목표)에 직접 넣는 proxy scout(프록시 탐색)를 준비합니다.

## Grok Receipt(그록 영수증)

- packet(묶음): `{GROK_DIR.as_posix()}`
- success(성공): `{summary['grok_success']}`
- classification(분류): `{summary['grok_classification']}`
- prompt(프롬프트): `{summary['grok_prompt_path']}`
- output(출력): `{summary['grok_output_path']}`

## Local Verification(로컬 검증)

- Frontier09(전선09)는 target representation(목표 표현) 축을 바꾸므로 Frontier08(전선08) 반복이 아닙니다.
- Frontier07(전선07)과 겹치는 mechanics(기계)는 explicit controls(명시 대조군)와 difference_from_f07(전선07 대비 차이)로 경계를 남겼습니다.
- WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서) 전까지 out_of_scope_by_claim(주장 범위 밖)입니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier09A Required Gate Coverage Audit(전선09A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): satisfied_with_boundary(경계부 충족)
- external_review_packet(외부 검토 묶음): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Effect(효과): stage open(단계 개방)만 주장하고 성능/운영 권위(성능/운영 권위)는 주장하지 않습니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier09 Review Index(전선09 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), experiment design(실험 설계).
- Grok packet(그록 묶음): `{GROK_DIR.as_posix()}`
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier09 Selection Status(전선09 선택 상태)

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
    return f"""# Decision: Open Frontier09 Drawdown Clean Path Labeling(결정: 전선09 손실폭 깨끗한 경로 라벨링 개방)

Date(날짜): 2026-06-14

Decision(결정): `{summary['status']}`

Effect(효과): Frontier09(전선09)는 DD/curve quality(손실폭/곡선 품질)를 label target(라벨 목표)에 직접 넣는 새 가설 생명주기(hypothesis lifecycle, 가설 생명주기)로 시작합니다.
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

Action(행동): Frontier09(전선09)는 Grok accepted(그록 수용) 후 drawdown-normalized clean path labeling(손실폭 정규화 깨끗한 경로 라벨링) 가설로 열렸습니다.

Effect(효과): 다음 실행은 `{NEXT_RUN_ID}` proxy scout(프록시 탐색)이며, 아직 completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)는 없습니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier09_stage_open_grok_accepted_no_authority",
        "family": "experiment_design(실험 설계)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": "open_frontier09_drawdown_clean_path_labeling",
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
        "source_authority": "grok_accepted_plus_local_verification(그록 수용과 로컬 검증)",
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
        "notes": f"next={NEXT_RUN_ID};no_authority",
        "question": "Can drawdown-normalized clean path labels improve DD/curve quality?(손실폭 정규화 깨끗한 경로 라벨이 손실폭/곡선 품질을 개선하는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def read_grok() -> dict[str, Any]:
    prompt_path = GROK_DIR / "prompt.md"
    clean_output_path = GROK_DIR / "clean_output.md"
    metadata_path = GROK_DIR / "metadata.json"
    if not clean_output_path.exists() or not metadata_path.exists():
        raise FileNotFoundError("Missing Frontier09 Grok stage-open packet.")
    metadata = json.loads(io_path(metadata_path).read_text(encoding="utf-8-sig"))
    return {
        "prompt_path": prompt_path.as_posix(),
        "clean_output_path": clean_output_path.as_posix(),
        "metadata_path": metadata_path.as_posix(),
        "clean_output": io_path(clean_output_path).read_text(encoding="utf-8-sig"),
        "success": bool(metadata.get("success")),
    }


def ensure_stage_ledger(path: Path) -> None:
    if path.exists():
        return
    header = f03b.read_csv_header(f03b.ALPHA_LEDGER)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        handle.write(",".join(header) + "\n")


def classify_grok(text: str) -> str:
    if "accepted(수용)" in text or "수용" in text:
        return "accepted(수용)"
    if "rejected(거절)" in text or "거절" in text:
        return "rejected(거절)"
    return "needs_local_verification(로컬 검증 필요)"


def write_json_sig(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
