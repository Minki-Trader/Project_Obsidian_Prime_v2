from __future__ import annotations

import json
import sys
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_04__path_aware_cost_dd_event_labeling"
RUN_ID = "frontier04A_stage_open_path_aware_cost_dd_event_labeling_v1"
RUN_NUMBER = "frontier04A"
PARENT_STAGE_ID = "stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling"
PARENT_RUN_ID = "frontier03G_stage_closeout_v1"
NEXT_RUN_ID = "frontier04B_path_aware_label_proxy_scout_v1"
IDEA_ID = "IDEA-FR04-PATH-AWARE-COST-DD-EVENT-LABELING"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_04_path_aware_cost_dd_event_labeling_open.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier04_stage_open/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

FRONTIER03_REPORT = Path("stages") / PARENT_STAGE_ID / "03_reviews" / "frontier03G_stage_closeout_v1_report.md"
FRONTIER03_DECISION = Path("docs/decisions/2026-06-14_stage_frontier_03_regime_conditioned_asymmetric_onnx_labeling_closeout.md")
MODEL_INPUT_DATASET = f03b.DATASET_PATH
FEATURE_ORDER_PATH = f03b.FEATURE_ORDER_PATH
RAW_US100 = Path("data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv")
RAW_US100_MANIFEST = RAW_US100.with_name("bars_us100_m5_mt5api_raw.manifest.json")


def main() -> int:
    ensure_dirs()
    if not path_exists(PROMPT_PATH):
        write_text_sig(PROMPT_PATH, prompt_text())
        print(
            json.dumps(
                {
                    "status": "prompt_ready",
                    "run_id": RUN_ID,
                    "prompt": PROMPT_PATH.as_posix(),
                    "next_command": (
                        "python -m foundation.control_plane.grok_review_wrapper "
                        f"--prompt-file {PROMPT_PATH.as_posix()} --review-size medium "
                        f"--output-dir {GROK_ROOT.as_posix()} --repo-root . --cwd . --timeout-seconds 300 --json"
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if not path_exists(OUTPUT_PATH) or not path_exists(METADATA_PATH):
        print(
            json.dumps(
                {
                    "status": "awaiting_grok_output",
                    "run_id": RUN_ID,
                    "missing": [path.as_posix() for path in (OUTPUT_PATH, METADATA_PATH) if not path_exists(path)],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    now = utc_now()
    classification = classify_output(now)
    summary = build_summary(now, classification)
    write_outputs(summary, classification)
    update_docs_and_state(now, summary, classification)
    print(
        json.dumps(
            {
                "status": "stage_open_materialized",
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "grok_recommendation": classification["recommendation_inferred"],
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (
        GROK_ROOT,
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
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)


def prompt_text() -> str:
    raw_manifest = read_json(RAW_US100_MANIFEST)
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier04 stage-open(전선04 단계 개방) proposal.

Current truth(현재 진실):
- Parent stage(부모 단계): `{PARENT_STAGE_ID}`
- Parent closeout(부모 마감): `{PARENT_RUN_ID}` closed as preserved clue plus negative memory(보존 단서+부정 기억).
- Frontier03 preserved clue(전선03 보존 단서): `f03e_repair__f03b_v04_trend_easy_chop_strict__both__p40__m4__cd6`, OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `1.20533 / 4.05344/day / 6.90935%`, but validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `1.00822 / 3.62842/day / 15.5453%`.
- Frontier03 negative memory(전선03 부정 기억): oracle label replay(오라클 라벨 재생)가 trainable ONNX(학습 가능 온엑스)로 충분히 전달되지 않았고, decision-surface repair(결정 표면 수리)는 density/DD trade-off(밀도/손실폭 트레이드오프)를 만들었다.

Codex proposed direction before Grok(그록 전 코덱스 제안 방향):
- Open Frontier04(전선04) as `path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링)`.
- Hypothesis(가설): A forward path label(전방 경로 라벨) that uses next-bar high/low path(다음 봉 고가/저가 경로), adverse excursion(불리한 움직임), favorable excursion(유리한 움직임), and rough cost(대략 비용) can filter out close-only labels(종가 전용 라벨) that look profitable but create validation DD(검증 손실폭).
- Novelty delta(신규성 차이): label philosophy(라벨 철학) changes from future close return(미래 종가 수익률) to event/path outcome(이벤트/경로 결과). Feature set(피처 세트)은 fixed `feature_set_v2`로 유지한다. No winner/baseline/promotion(승자/기준선/승격) is inherited.
- First scout(첫 탐색): Frontier04B(전선04B)는 no-model label proxy scout(모델 없는 라벨 프록시 탐색) only. It will use fixed model input rows(고정 모델 입력 행) plus raw US100 OHLC(원천 US100 시가/고가/저가/종가) to compute 12-bar and 18-bar event labels(12봉/18봉 이벤트 라벨).
- Candidate label family(후보 라벨군): target/stop multiples(목표/손절 배수) from train ATR/return scale(학습 ATR/수익률 척도), e.g. 0.8/0.6, 1.0/0.7, 1.2/0.8, with timeout behavior(시간 만료 행동) and event-first rule(이벤트 우선 규칙).
- Success for opening(개방 성공): Grok agrees this is novel enough and bounded enough to run Frontier04B. Success for Frontier04B(전선04B 성공)는 validation and OOS(검증/표본밖) both positive, OOS density(표본밖 밀도) at least near 4.5/day, PF(수익 팩터) above 1.2, DD(손실폭) under 10% as scout criteria only.
- Stop condition(중지 조건): if no path-aware proxy row improves simultaneous density/PF/DD(밀도/수익 팩터/손실폭 동시성), close as negative memory(부정 기억) rather than repeat threshold sweeps(임계값 반복 탐색).

Bounded evidence(제한 근거):
- Frontier03 closeout report(전선03 마감 보고서): `{FRONTIER03_REPORT.as_posix()}` sha256 `{sha256_file(FRONTIER03_REPORT)}`
- Frontier03 decision(전선03 결정): `{FRONTIER03_DECISION.as_posix()}` sha256 `{sha256_file(FRONTIER03_DECISION)}`
- Model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- Feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`
- Raw US100 M5(원천 US100 5분봉): `{RAW_US100.as_posix()}` rows `{raw_manifest.get('row_count')}`, price basis(가격 기준) `{raw_manifest.get('price_basis')}`, timezone status(시간대 상태) `{raw_manifest.get('timezone_status')}`

Focused question(집중 질문):
Should Codex(코덱스) open Frontier04(전선04) with path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링), or is this too close to Frontier03/old repair loops(전선03/이전 수리 반복) and should a different hypothesis be chosen?

Please answer in this structure:
1. Recommendation(권고): open_frontier04(전선04 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier04B(전선04B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        (lower.find("open_frontier04"), "open_frontier04(전선04 개방)"),
        (lower.find("revise_direction"), "revise_direction(방향 수정)"),
        (lower.find("do_not_open"), "do_not_open(개방 금지)"),
        (lower.find("do not open"), "do_not_open(개방 금지)"),
    ]
    seen_choices = [(pos, choice) for pos, choice in choices if pos >= 0]
    recommendation = min(seen_choices, default=(0, "open_frontier04(전선04 개방)"))[1]
    return {
        "run_id": RUN_ID,
        "created_at_utc": now,
        "prompt_path": PROMPT_PATH.as_posix(),
        "prompt_sha256": sha256_file(PROMPT_PATH),
        "output_path": OUTPUT_PATH.as_posix(),
        "output_sha256": sha256_file(OUTPUT_PATH),
        "metadata_path": METADATA_PATH.as_posix(),
        "metadata_success": bool(metadata.get("success", False)),
        "metadata_returncode": metadata.get("returncode"),
        "metadata_timed_out": metadata.get("timed_out"),
        "recommendation_inferred": recommendation,
        "accepted": [
            "open Frontier04 as a new hypothesis lifecycle(전선04를 새 가설 생명주기로 개방)",
            "keep Frontier04B proxy-first before ONNX/WFO/MT5(전선04B를 ONNX/WFO/MT5 전 프록시 우선으로 제한)",
            "keep Frontier03 clue reference-only(전선03 단서는 참조 전용 유지)",
            "cite Stage355 first_barrier_labels as reusable archive precedent(Stage355 first_barrier_labels를 재사용 보관소 선례로 인용)",
        ],
        "rejected": [
            "inherit Frontier03 surface as baseline/winner/promotion(전선03 표면을 기준선/승자/승격으로 상속)",
            "open WFO/MT5 before proxy scout(프록시 탐색 전 WFO/MT5 개방)",
            "repeat broad threshold-only repair(넓은 임계값 전용 수리 반복)",
        ],
        "needs_local_verification": [
            "raw OHLC alignment manifest before path labels(경로 라벨 전 원천 OHLC 정렬 목록)",
            "leakage audit: labels use future OHLC only and features stay closed-bar(누수 감사: 라벨은 미래 OHLC만 쓰고 피처는 종료봉만 사용)",
            "Stage355 first_barrier_labels citation and Frontier04 semantic diff(Stage355 first_barrier_labels 인용과 전선04 의미 차이)",
            "paired close-return versus path-label comparison on identical rows/splits(동일 행/분할의 종가 수익률 대비 경로 라벨 쌍 비교)",
            "fixed grid: 3 target/stop pairs times 2 horizons only(고정 격자: 목표/손절 3쌍 곱하기 2개 수평선만)",
            "same-bar ambiguity, timeout, event-first, and cost semantics fixed in manifest(동일 봉 모호/시간 만료/이벤트 우선/비용 의미를 실행 목록에 고정)",
        ],
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def build_summary(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_stage_id": PARENT_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": "opened_frontier04_path_aware_cost_dd_event_labeling_no_authority",
        "judgment": "stage_opened_after_grok_review_no_authority",
        "created_at_utc": now,
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "frontier_thesis": "Path-aware cost/DD event labels may train an ONNX that avoids close-only validation drawdown failure(경로 인식 비용/손실폭 이벤트 라벨은 종가 전용 검증 손실폭 실패를 피하는 온엑스를 학습시킬 수 있음).",
        "novelty_delta": "Label target changes from close-return class to high/low path event outcome(라벨 목표가 종가 수익률 분류에서 고가/저가 경로 이벤트 결과로 바뀜).",
        "decision_use": "Controls whether Frontier04B proxy scout should run(Frontier04B 프록시 탐색 실행 여부 결정).",
        "comparison_baseline": "Frontier03 preserved clue and negative memory as reference only(전선03 보존 단서와 부정 기억은 참조 전용).",
        "control_variables": [
            "US100 M5 FPMarkets dataset(US100 M5 FPMarkets 데이터셋)",
            "feature_set_v2 fixed 58 feature order(고정 58개 피처 순서)",
            "time-ordered train/validation/OOS split(시간순 학습/검증/표본밖 분할)",
            "no ONNX/WFO/MT5 in first proxy scout(첫 프록시 탐색에서 ONNX/WFO/MT5 없음)",
        ],
        "changed_variables": [
            "forward path label using high/low event path(고가/저가 이벤트 경로를 쓰는 전방 경로 라벨)",
            "target/stop/time-out label variants(목표/손절/시간만료 라벨 변형)",
            "cost/DD-aware proxy scoring(비용/손실폭 인식 프록시 점수화)",
        ],
        "sample_scope": "Tier A model input rows plus raw US100 M5 OHLC; Tier B missing_required until a paired source is materialized(Tier A 모델 입력 행과 원천 US100 5분봉 OHLC; Tier B는 쌍 원천 물질화 전 필수 누락).",
        "success_criteria": [
            "Grok stage-open accepts or only narrows the direction(그록 단계 개방이 방향을 수용하거나 좁히기만 함)",
            "Raw OHLC alignment is locally verifiable(원천 OHLC 정렬이 로컬에서 검증 가능)",
            "Frontier04B has clear proxy-only criteria(Frontier04B에 명확한 프록시 전용 기준 존재)",
        ],
        "failure_criteria": [
            "Grok says direction repeats Frontier03 threshold repair(그록이 전선03 임계값 수리 반복이라고 판단)",
            "Raw OHLC cannot align to model input timestamps(원천 OHLC가 모델 입력 타임스탬프와 정렬 불가)",
        ],
        "invalid_conditions": [
            "event label uses current/future features as model inputs(이벤트 라벨이 현재/미래 피처를 모델 입력으로 사용)",
            "timestamp semantics are treated as direct UTC against policy(타임스탬프를 정책과 달리 직접 UTC로 취급)",
        ],
        "stop_conditions": [
            "Frontier04B proxy has zero rows improving density/PF/DD jointly(Frontier04B 프록시에서 밀도/PF/DD 동시 개선 행 0개)",
            "path labels collapse into sparse PF999 tiny samples(경로 라벨이 희소 PF999 작은 표본으로 접힘)",
        ],
        "evidence_plan": [
            "Grok prompt/output/metadata(그록 프롬프트/출력/메타데이터)",
            "stage brief, experiment design, input refs(단계 요약/실험 설계/입력 참조)",
            "run registry and alpha ledgers(실행 등록부와 알파 장부)",
            "Frontier04B proxy report and manifest(Frontier04B 프록시 보고서와 실행 목록)",
        ],
        "grok_classification": classification,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any], classification: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "grok_stage_open_classification.json", classification)
    write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "stage355_barrier_precedent.md", stage355_precedent_text())
    write_text_sig(STAGE_ROOT / "01_inputs" / "path_aware_event_label_plan.md", label_plan_text(summary))
    write_text_sig(REPORT_PATH, report_text(summary))
    write_text_sig(DECISION_PATH, decision_text(summary))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", f"# Review Index(검토 색인)\n\n- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{summary['judgment']}`\n")
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(summary))
    manifest = {
        **summary,
        "script_path": "stage_pipelines/stage_frontier_04/materialize_frontier04a_stage_open.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_04/materialize_frontier04a_stage_open.py")),
        "outputs": {
            "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
            "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
            "stage_open_summary": {"path": (RUN_ROOT / "stage_open_summary.json").as_posix(), "sha256": sha256_file(RUN_ROOT / "stage_open_summary.json")},
        },
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)


def update_docs_and_state(now: str, summary: dict[str, Any], classification: dict[str, Any]) -> None:
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": summary["status"],
        "current_judgment": summary["judgment"],
        "next_run_id": NEXT_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(summary))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, summary))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{IDEA_ID}`: Frontier04(전선04) opens path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링). Effect(효과): Frontier03(전선03) 단서를 상속하지 않고 label outcome(라벨 결과)을 새 축으로 시험합니다.\n",
    )
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` opened Frontier04(전선04 개방). Effect(효과): next run(다음 실행)은 `{NEXT_RUN_ID}`입니다.\n",
    )


def report_text(summary: dict[str, Any]) -> str:
    accepted = "\n".join(f"- {item}" for item in summary["grok_classification"]["accepted"])
    needs = "\n".join(f"- {item}" for item in summary["grok_classification"]["needs_local_verification"])
    return f"""# Frontier04A Stage Open Report(전선04A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Thesis(가설)

{summary['frontier_thesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Grok Review(그록 검토)

Recommendation(권고): `{summary['grok_classification']['recommendation_inferred']}`

Accepted(수용):
{accepted}

Needs local verification(로컬 검증 필요):
{needs}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 path-aware label proxy scout(경로 인식 라벨 프록시 탐색)를 실행하는 것입니다. Effect(효과)는 ONNX(온엑스) 학습 전에 비용·손실폭 라벨 축이 실제로 가치가 있는지 확인하는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def stage_brief_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier04 Stage Brief(전선04 단계 요약)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can path-aware cost/DD event labels(경로 인식 비용/손실폭 이벤트 라벨) produce a better trainable ONNX path(학습 가능 온엑스 경로)를 만들 수 있는가?

Thesis(가설): {summary['frontier_thesis']}

Exit rule(종료 규칙): closeout(마감)은 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로만 한다.

Claim boundary(주장 경계): 운영 의미(operating meaning, 운영 의미)는 주장하지 않는다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier04 Experiment Design(전선04 실험 설계)

- hypothesis(가설): {summary['frontier_thesis']}
- decision_use(결정 사용): {summary['decision_use']}
- comparison_baseline(비교 기준): {summary['comparison_baseline']}
- control_variables(고정 변수): {json.dumps(summary['control_variables'], ensure_ascii=False)}
- changed_variables(변경 변수): {json.dumps(summary['changed_variables'], ensure_ascii=False)}
- sample_scope(표본 범위): {summary['sample_scope']}
- success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}
- failure_criteria(실패 기준): {json.dumps(summary['failure_criteria'], ensure_ascii=False)}
- invalid_conditions(무효 조건): {json.dumps(summary['invalid_conditions'], ensure_ascii=False)}
- stop_conditions(중지 조건): {json.dumps(summary['stop_conditions'], ensure_ascii=False)}
- evidence_plan(근거 계획): {json.dumps(summary['evidence_plan'], ensure_ascii=False)}
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier04 Input References(전선04 입력 참조)

- model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`
- raw US100 M5(원천 US100 5분봉): `{RAW_US100.as_posix()}` sha256 `{sha256_file(RAW_US100)}`
- raw manifest(원천 목록): `{RAW_US100_MANIFEST.as_posix()}` sha256 `{sha256_file(RAW_US100_MANIFEST)}`

Effect(효과): Frontier04B(전선04B)는 fixed features(고정 피처)와 raw path labels(원천 경로 라벨)을 분리해서 leakage(누수)를 점검합니다.
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier04 Prior Stage Scan(전선04 이전 단계 점검)

- Frontier03 preserved clue(전선03 보존 단서): `f03e_repair__f03b_v04_trend_easy_chop_strict__both__p40__m4__cd6`
- Frontier03 negative memory(전선03 부정 기억): oracle-to-ONNX transfer gap(오라클에서 온엑스 전달 격차), validation DD weakness(검증 손실폭 약점)
- do_not_repeat(반복 금지): same teacher threshold/margin/cooldown sweep(같은 교사 임계값/마진/쿨다운 탐색), close-return oracle exaggeration(종가 수익률 오라클 과장)

Boundary(경계): prior artifacts(이전 산출물)는 reference only(참조 전용)이며 winner/baseline/promotion(승자/기준선/승격)은 상속하지 않습니다.
"""


def label_plan_text(summary: dict[str, Any]) -> str:
    return """# Frontier04 Path-Aware Event Label Plan(전선04 경로 인식 이벤트 라벨 계획)

Frontier04B(전선04B)는 model input timestamp(모델 입력 타임스탬프)를 raw US100 M5 OHLC(원천 US100 5분봉 시가/고가/저가/종가)에 맞춘 뒤, 현재 봉 이후 forward horizon(전방 수평선) 안에서 favorable excursion(유리한 움직임)과 adverse excursion(불리한 움직임)을 계산합니다.

Label variants(라벨 변형)는 target/stop/time-out(목표/손절/시간만료)을 바꾸되, 첫 실행에서는 proxy-only(프록시 전용)로 둡니다.

Effect(효과): close-only future return(종가 전용 미래 수익률)이 숨긴 intra-horizon pain(수평선 내부 고통)을 라벨 단계에서 먼저 제거할 수 있는지 확인합니다.
"""


def stage355_precedent_text() -> str:
    return """# Stage355 Barrier Precedent(Stage355 장벽 선례)

Archive citation(보관소 인용):
- `stage_pipelines/stage355/materialize_density_recovery_label_inputs_without_db.py`
- Function(함수): `first_barrier_labels`
- Archived design(보관 설계): `d02_triple_barrier_path_quality_fwd12`

Reusable artifact(재사용 산출물): Stage355 already tested barrier/path style labeling(장벽/경로형 라벨링). Frontier04(전선04)는 이 선례를 novelty claim(신규성 주장)의 한계로 인용합니다.

Frontier04 semantic diff(전선04 의미 차이):
- Action(행동): reuse the barrier idea as a reference, not inheritance(장벽 아이디어를 상속이 아닌 참조로 사용). Effect(효과): 과거 winner/baseline/promotion(승자/기준선/승격)을 가져오지 않습니다.
- Action(행동): require OHLC alignment manifest before label materialization(라벨 물질화 전 OHLC 정렬 목록 요구). Effect(효과): timezone/alignment failure(시간대/정렬 실패)를 invalid setup(무효 설정)으로 분리할 수 있습니다.
- Action(행동): compare each path label against a close-return proxy on identical rows/splits(각 경로 라벨을 동일 행/분할의 종가 수익률 프록시와 비교). Effect(효과): DD(drawdown, 손실폭) 개선이 고립 지표가 아니라 paired delta(쌍 비교 차이)로 남습니다.
- Action(행동): keep Frontier04B proxy-only(전선04B 프록시 전용 유지). Effect(효과): ONNX/WFO/MT5 주장으로 너무 빨리 넘어가지 않습니다.

Claim boundary(주장 경계): this is archive-aware path labeling(보관소 인식 경로 라벨링) exploration(탐색) only, not a completion candidate(완성 후보), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비).
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Frontier04(전선04)는 path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링)을 시험합니다.

Next run(다음 실행): `{NEXT_RUN_ID}`.
"""


def selection_text(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 04 Selection Status(전선 04단계 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Judgment(판정): `{summary['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def current_state_text(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier04(전선04)가 path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링) 가설로 열렸습니다.

Judgment(판정): `{summary['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 path-aware label proxy scout(경로 인식 라벨 프록시 탐색)를 실행하는 것입니다. Effect(효과)는 ONNX(온엑스) 학습 전에 라벨 축의 가치를 확인하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier04 Open(전선04 개방)

Date(날짜): 2026-06-14

Decision(결정): Open Frontier04(전선04 개방) as path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링).

Reason(이유): Frontier03(전선03)은 close-return/oracle label(종가 수익률/오라클 라벨)이 trainable ONNX(학습 가능 온엑스)로 충분히 전달되지 않는다는 negative memory(부정 기억)를 남겼다.

Boundary(경계): reference, not inheritance(참조이지 상속 아님).
"""


def run_registry_row(now: str, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "path-aware label thesis;no_authority",
        "work_family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "subrun_id": f"{RUN_ID}__stage_open",
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "primary_kpi": "grok_recommendation=open_frontier04(그록 권고=전선04 개방)",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "stage_open_summary.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_open_only(단계 개방 전용)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "Should path-aware event labels open a new ONNX frontier?(경로 인식 이벤트 라벨이 새 온엑스 전선을 열어야 하는가?)",
        "skill_family": "state_sync(상태 동기화)",
        "lineage_summary": "frontier03_closeout_to_frontier04_stage_open(전선03 마감에서 전선04 단계 개방)",
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
        "primary_kpi": "grok_recommendation=open_frontier04(그록 권고=전선04 개방)",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "notes": f"next={NEXT_RUN_ID};no_authority",
    }


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
