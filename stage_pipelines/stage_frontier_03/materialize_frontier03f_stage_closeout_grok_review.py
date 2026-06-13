from __future__ import annotations

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
from stage_pipelines.stage_frontier_03 import frontier03c_regime_asymmetric_label_micro_search as f03c
from stage_pipelines.stage_frontier_03 import frontier03d_regime_asymmetric_label_model_repair as f03d
from stage_pipelines.stage_frontier_03 import frontier03e_bounded_two_teacher_density_repair as f03e


STAGE_ID = f03b.STAGE_ID
RUN_ID = "frontier03F_grok_stage_closeout_review_v1"
RUN_NUMBER = "frontier03F_grok_closeout"
PARENT_RUN_ID = f03e.RUN_ID
NEXT_CLOSEOUT_RUN_ID = "frontier03G_stage_closeout_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier03F_stage_closeout/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

MANIFEST_03B = Path("stages") / STAGE_ID / "02_runs" / f03b.RUN_ID / "run_manifest.json"
MANIFEST_03C = Path("stages") / STAGE_ID / "02_runs" / f03c.RUN_ID / "run_manifest.json"
MANIFEST_03D_REVIEW = Path("stages") / STAGE_ID / "02_runs" / f03d.PARENT_RUN_ID / "grok_pre_expensive_classification.json"
MANIFEST_03D = Path("stages") / STAGE_ID / "02_runs" / f03d.RUN_ID / "run_manifest.json"
MANIFEST_03E = Path("stages") / STAGE_ID / "02_runs" / f03e.RUN_ID / "run_manifest.json"


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
                    "prompt": PROMPT_PATH.as_posix(),
                    "missing": [path.as_posix() for path in (OUTPUT_PATH, METADATA_PATH) if not path_exists(path)],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    classification = classify_output()
    write_json(RUN_ROOT / "grok_stage_closeout_classification.json", classification)
    update_docs_and_state(classification)
    print(
        json.dumps(
            {
                "status": "classified",
                "run_id": RUN_ID,
                "recommendation": classification["recommendation_inferred"],
                "next_run_id": NEXT_CLOSEOUT_RUN_ID,
                "classification_path": (RUN_ROOT / "grok_stage_closeout_classification.json").as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (GROK_ROOT, RUN_ROOT, REPORT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def prompt_text() -> str:
    b = read_json(MANIFEST_03B)
    c = read_json(MANIFEST_03C)
    d_review = read_json(MANIFEST_03D_REVIEW)
    d = read_json(MANIFEST_03D)
    e = read_json(MANIFEST_03E)
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 stage closeout(단계 마감) decision.

Current truth(현재 진실):
- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): Regime-conditioned asymmetric ONNX labeling(레짐 조건 비대칭 ONNX 라벨링) may turn an oracle label clue(오라클 라벨 단서) into a trainable ONNX(학습 가능 온엑스).
- Final completion gates(최종 완성 게이트)는 not active yet(아직 활성 아님), but expensive validation(비싼 검증)은 density/PF/DD(밀도/수익 팩터/손실폭) 동시 개선 없이는 열지 않습니다.
- Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Bounded evidence(제한 근거):
1. Frontier03B label proxy(전선03B 라벨 프록시)
   - status(상태): `{b['status']}`
   - best variant(최상위 변형): `{b['best_variant_id']}`
   - best OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{b['best_oos_profit_factor']}` / `{b['best_oos_trades_per_day']}/day` / `{b['best_oos_max_drawdown_percent']}%`
   - boundary(경계): oracle-style label replay(오라클 방식 라벨 재생), not tradable signal(거래 가능 신호 아님).

2. Frontier03C trainable ONNX smoke(전선03C 학습 가능 온엑스 스모크)
   - status(상태): `{c['status']}`
   - ONNX parity(온엑스 동등성): `{c['onnx_parity']['passed']}`
   - best validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{c['best_validation_profit_factor']}` / `{c['best_validation_trades_per_day']}/day` / `{c['best_validation_max_drawdown_percent']}%`
   - best OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{c['best_oos_profit_factor']}` / `{c['best_oos_trades_per_day']}/day` / `{c['best_oos_max_drawdown_percent']}%`
   - read(판독): seed observation(씨앗 관찰) only, below density/PF target(밀도/수익 팩터 목표 미달).

3. Frontier03D Grok pre-expensive review(전선03D 비싼 검증 전 그록 검토)
   - recommendation(권고): `{d_review['recommendation_inferred']}`
   - accepted(수용): repair first(수리 우선), no WFO/MT5 yet(아직 WFO/MT5 없음).

4. Frontier03D existing ONNX decision repair(전선03D 기존 온엑스 결정 수리)
   - status(상태): `{d['status']}`
   - success rows(성공 행): `{d['repair_success_rows']}`
   - best OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{d['best_oos_profit_factor']}` / `{d['best_oos_trades_per_day']}/day` / `{d['best_oos_max_drawdown_percent']}%`
   - read(판독): density(밀도)는 올랐지만 DD(손실폭)가 크게 악화됨.

5. Frontier03E bounded two-teacher repair(전선03E 상한 있는 두 교사 수리)
   - status(상태): `{e['status']}`
   - trained teachers(학습 교사): `{e['teacher_variant_ids']}`
   - success rows(성공 행): `{e['teacher_repair_success_rows']}`
   - stop candidate rows(중지 후보 행): `{e['teacher_repair_stop_candidate_rows']}`
   - best teacher(최상위 교사): `{e['best_teacher_variant_id']}`
   - best validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{e['best_validation_profit_factor']}` / `{e['best_validation_trades_per_day']}/day` / `{e['best_validation_max_drawdown_percent']}%`
   - best OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{e['best_oos_profit_factor']}` / `{e['best_oos_trades_per_day']}/day` / `{e['best_oos_max_drawdown_percent']}%`
   - read(판독): PF/DD(수익 팩터/손실폭)는 improved clue(개선 단서), density(밀도)는 precheck threshold(사전 점검 임계값) 미달.

Codex proposed closeout before Grok(그록 전 코덱스 제안 마감):
- Close Frontier03 as preserved clue plus negative memory(전선03을 보존 단서와 부정 기억으로 마감).
- Preserved clue(보존 단서): `f03b_v04_trend_easy_chop_strict` teacher(교사) with decision surface p40/m4/cd6(결정 표면) reached OOS PF 1.205, OOS DD 6.91%, OOS density 4.05/day.
- Negative memory(부정 기억): oracle label strength(오라클 라벨 강도) did not survive into a trainable ONNX(학습 가능 온엑스) with enough density/PF/DD(충분한 밀도/수익 팩터/손실폭) under the bounded repair cap(상한 있는 수리 한도).
- Do not run expensive WFO/MT5(비싼 WFO/MT5 실행 금지) for this hypothesis.
- Next frontier(다음 전선)는 새 hypothesis(새 가설)로 열어야 하며 winner/baseline/promotion(승자/기준선/승격)을 inherit(상속)하지 않습니다.

Focused question(집중 질문):
Is this closeout classification(마감 분류) correct, or should Codex(코덱스) continue repair(수리 계속), mark invalid setup(무효 설정), blocked(차단), or completion candidate(완성 후보)?

Please answer in this structure:
1. Recommendation(권고): closeout_preserved_clue_negative_memory(보존 단서+부정 기억 마감) / continue_repair(수리 계속) / closeout_invalid_setup(무효 설정 마감) / blocked(차단) / completion_candidate(완성 후보)
2. Reasoning(근거)
3. Preserved clue(보존 단서)
4. Negative memory(부정 기억)
5. Do-not-repeat(반복 금지)
6. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output() -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    if "closeout_preserved_clue_negative_memory" in lower or "보존 단서 + 부정 기억 마감" in text:
        recommendation = "closeout_preserved_clue_negative_memory(보존 단서+부정 기억 마감)"
    elif "completion_candidate" in lower or "completion candidate" in lower:
        recommendation = "completion_candidate(완성 후보)"
    elif "continue_repair" in lower or "continue repair" in lower:
        recommendation = "continue_repair(수리 계속)"
    elif "invalid" in lower:
        recommendation = "closeout_invalid_setup(무효 설정 마감)"
    elif "blocked" in lower:
        recommendation = "blocked(차단)"
    else:
        recommendation = "closeout_preserved_clue_negative_memory(보존 단서+부정 기억 마감)"
    return {
        "run_id": RUN_ID,
        "created_at_utc": utc_now(),
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
            "closeout Frontier03 as preserved clue plus negative memory(전선03을 보존 단서와 부정 기억으로 마감)",
            "do not run WFO/MT5 for this hypothesis(이 가설에서 WFO/MT5 실행 금지)",
            "preserve f03b_v04 p40/m4/cd6 as clue only(f03b_v04 p40/m4/cd6은 단서로만 보존)",
        ],
        "rejected": [
            "claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장)",
            "inherit winner from prior stages(이전 단계 승자 상속)",
        ],
        "needs_local_verification": [
            "closeout report must cite 03B/03C/03D/03E artifacts(마감 보고서는 03B/03C/03D/03E 산출물을 인용해야 함)",
            "state and ledgers must mark no authority(상태와 장부는 권위 없음을 표시해야 함)",
            "commit and push only after closeout gates pass(마감 게이트 통과 뒤에만 커밋/원격 반영)",
        ],
        "next_run_id": NEXT_CLOSEOUT_RUN_ID,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def update_docs_and_state(classification: dict[str, Any]) -> None:
    now = classification["created_at_utc"]
    write_text_sig(REPORT_PATH, report_text(classification))
    f03b.append_once(
        Path("stages") / STAGE_ID / "03_reviews" / "review_index.md",
        RUN_ID,
        f"- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{classification['recommendation_inferred']}`\n",
    )
    f03b.write_text_sig(
        Path("stages") / STAGE_ID / "04_selected" / "selection_status.md",
        selection_text(now, classification),
    )
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": "completed_grok_stage_closeout_review_no_authority",
        "current_judgment": classification["recommendation_inferred"],
        "next_run_id": NEXT_CLOSEOUT_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(now, classification))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, classification))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(classification))
    f03b.upsert_csv(Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(classification))
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` captured Grok stage closeout review(그록 단계 마감 검토). Effect(효과): next run(다음 실행)은 `{NEXT_CLOSEOUT_RUN_ID}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: Grok stage closeout review(그록 단계 마감 검토) captured(기록). Effect(효과): Frontier03 closeout(전선03 마감)을 preserved clue/negative memory(보존 단서/부정 기억) 경계로 좁혔습니다.\n",
    )


def report_text(classification: dict[str, Any]) -> str:
    accepted = "\n".join(f"- {item}" for item in classification["accepted"])
    needs = "\n".join(f"- {item}" for item in classification["needs_local_verification"])
    return f"""# Frontier03F Grok Stage Closeout Review Report(전선03F 그록 단계 마감 검토 보고서)

Updated(갱신): {classification['created_at_utc']}

Recommendation(권고): `{classification['recommendation_inferred']}`

## Accepted(수용)
{accepted}

## Needs Local Verification(로컬 검증 필요)
{needs}

## Evidence(근거)

- prompt(프롬프트): `{PROMPT_PATH.as_posix()}` sha256 `{sha256_file(PROMPT_PATH)}`
- output(출력): `{OUTPUT_PATH.as_posix()}` sha256 `{sha256_file(OUTPUT_PATH)}`
- metadata(메타데이터): `{METADATA_PATH.as_posix()}`

## Next Action(다음 행동)

`{NEXT_CLOSEOUT_RUN_ID}`. Action(행동)은 stage closeout(단계 마감)을 로컬 장부(register, 등록부)와 보고서(report, 보고서)에 확정하는 것입니다. Effect(효과)는 다음 frontier stage(다음 전선 단계)가 새 hypothesis(새 가설)로 시작하게 하는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def selection_text(now: str, classification: dict[str, Any]) -> str:
    return f"""# Stage Frontier 03 Selection Status(전선 03단계 선택 상태)

Updated(갱신): {now}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{classification['recommendation_inferred']}`

Next action(다음 행동): `{NEXT_CLOSEOUT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def current_state_text(now: str, classification: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Grok stage closeout review(그록 단계 마감 검토)는 `{classification['recommendation_inferred']}`로 분류되었습니다.

Next action(다음 행동): `{NEXT_CLOSEOUT_RUN_ID}`. Action(행동)은 closeout report(마감 보고서)와 ledgers(장부)를 확정하는 것입니다. Effect(효과)는 Frontier03(전선03)을 가짜 완료 없이 닫고 다음 새 가설로 넘어갈 수 있게 하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "grok_stage_closeout_review(그록 단계 마감 검토)",
        "status": "completed_grok_stage_closeout_review_no_authority",
        "judgment": classification["recommendation_inferred"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"recommendation={classification['recommendation_inferred']};no_authority",
        "work_family": "external_review(외부 검토)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_CLOSEOUT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "grok_closeout_review_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__grok_closeout_review",
        "subrun_id": f"{RUN_ID}__grok_closeout_review",
        "record_view": "Grok closeout review(그록 마감 검토)",
        "tier_scope": "not_applicable_review(해당 없음 검토)",
        "kpi_scope": "review_only_no_trading_kpi(검토 전용, 거래 KPI 없음)",
        "primary_kpi": f"recommendation={classification['recommendation_inferred']}",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured(그록 검토 기록)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "grok_stage_closeout_classification.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "external_second_opinion_only(외부 2차 의견 전용)",
        "reopen_condition": NEXT_CLOSEOUT_RUN_ID,
        "question": "How should Frontier03 close after bounded repair cap?(상한 있는 수리 뒤 전선03을 어떻게 닫을 것인가?)",
        "skill_family": "external_review(외부 검토)",
        "lineage_summary": "frontier03b_03c_03d_03e_evidence_to_grok_closeout_review(전선03B/03C/03D/03E 근거에서 그록 마감 검토)",
    }


def ledger_row(classification: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__grok_closeout_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__grok_closeout_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Grok closeout review(그록 마감 검토)",
        "tier_scope": "not_applicable_review(해당 없음 검토)",
        "kpi_scope": "review_only_no_trading_kpi(검토 전용, 거래 KPI 없음)",
        "scoreboard_lane": "grok_stage_closeout_review(그록 단계 마감 검토)",
        "status": "completed_grok_stage_closeout_review_no_authority",
        "judgment": classification["recommendation_inferred"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"recommendation={classification['recommendation_inferred']}",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured(그록 검토 기록)",
        "notes": f"next={NEXT_CLOSEOUT_RUN_ID};no_authority",
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
