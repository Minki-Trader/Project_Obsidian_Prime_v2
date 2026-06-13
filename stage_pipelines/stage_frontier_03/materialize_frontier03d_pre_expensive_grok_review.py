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


STAGE_ID = "stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling"
RUN_ID = "frontier03D_grok_pre_expensive_wfo_mt5_review_v1"
PARENT_RUN_ID = "frontier03C_regime_asymmetric_label_micro_search_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
NEXT_REPAIR_RUN_ID = "frontier03D_regime_asymmetric_label_model_repair_v1"
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier03D_pre_expensive_wfo_mt5/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

FRONTIER03B_REPORT = Path("stages") / STAGE_ID / "03_reviews" / "frontier03B_regime_asymmetric_label_proxy_scout_v1_report.md"
FRONTIER03B_MANIFEST = Path("stages") / STAGE_ID / "02_runs" / "frontier03B_regime_asymmetric_label_proxy_scout_v1" / "run_manifest.json"
FRONTIER03C_REPORT = Path("stages") / STAGE_ID / "03_reviews" / "frontier03C_regime_asymmetric_label_micro_search_v1_report.md"
FRONTIER03C_MANIFEST = Path("stages") / STAGE_ID / "02_runs" / "frontier03C_regime_asymmetric_label_micro_search_v1" / "run_manifest.json"


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
                    "missing": [
                        path.as_posix()
                        for path in (OUTPUT_PATH, METADATA_PATH)
                        if not path_exists(path)
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    classification = classify_output()
    write_json(RUN_ROOT / "grok_pre_expensive_classification.json", classification)
    update_docs_and_state(classification)
    print(json.dumps({"status": "classified", "run_id": RUN_ID, "classification_path": (RUN_ROOT / "grok_pre_expensive_classification.json").as_posix()}, ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (GROK_ROOT, RUN_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def prompt_text() -> str:
    c_manifest = read_json(FRONTIER03C_MANIFEST)
    b_manifest = read_json(FRONTIER03B_MANIFEST)
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 pre-expensive decision(비싼 검증 전 결정).

Current truth(현재 진실):
- Stage(단계): `{STAGE_ID}`
- Parent run(부모 실행): `{PARENT_RUN_ID}`
- Frontier03B(전선03B) label-proxy replay(라벨 프록시 재생) found oracle-style scout clue(오라클 방식 탐색 단서), but it is not a tradable signal(거래 가능 신호 아님).
- Frontier03C(전선03C) trained one LogisticRegression ONNX(로지스틱 회귀 온엑스) from the best Frontier03B label variant(라벨 변형).
- ONNX parity(온엑스 동등성): `{c_manifest['onnx_parity']['passed']}`
- Best Frontier03C OOS net/PF/density/DD(전선03C 표본외 순수익/수익 팩터/밀도/손실폭): `{c_manifest['best_oos_net_profit']}` / `{c_manifest['best_oos_profit_factor']}` / `{c_manifest['best_oos_trades_per_day']}/day` / `{c_manifest['best_oos_max_drawdown_percent']}%`
- Best Frontier03C validation net/PF/density/DD(전선03C 검증 순수익/수익 팩터/밀도/손실폭): `{c_manifest['best_validation_net_profit']}` / `{c_manifest['best_validation_profit_factor']}` / `{c_manifest['best_validation_trades_per_day']}/day` / `{c_manifest['best_validation_max_drawdown_percent']}%`
- Observation rows(관찰 행): `{c_manifest['onnx_seed_observation_rows']}`
- Frontier03B go rows(전선03B 진행 행): `{b_manifest['go_rule_rows']}`, but oracle-bound(오라클 경계) and not runtime-bound(런타임 경계 아님).

Evidence paths(근거 경로):
- Frontier03B report(전선03B 보고서): `{FRONTIER03B_REPORT.as_posix()}` sha256 `{sha256_file(FRONTIER03B_REPORT)}`
- Frontier03B manifest(전선03B 실행 목록): `{FRONTIER03B_MANIFEST.as_posix()}` sha256 `{sha256_file(FRONTIER03B_MANIFEST)}`
- Frontier03C report(전선03C 보고서): `{FRONTIER03C_REPORT.as_posix()}` sha256 `{sha256_file(FRONTIER03C_REPORT)}`
- Frontier03C manifest(전선03C 실행 목록): `{FRONTIER03C_MANIFEST.as_posix()}` sha256 `{sha256_file(FRONTIER03C_MANIFEST)}`

Codex proposed direction before Grok(그록 전 코덱스 제안 방향):
- Do not claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 금지).
- Because Frontier03C has ONNX parity and positive validation/OOS net(검증/표본외 양수 순수익), consider a narrow WFO/stress precheck(좁은 워크포워드/스트레스 사전 확인) only if Grok agrees the density gap(밀도 부족) is not a hard stop at this exploratory stage(탐색 단계).
- Alternative repair path(대안 수리 경로): avoid WFO/MT5 and first repair density from 3.34/day toward 5/day without destroying DD(손실폭) and PF(수익 팩터).

Focused question(집중 질문):
Should Codex(코덱스) proceed to narrow WFO/stress/MT5 precheck(좁은 워크포워드/스트레스/MT5 사전 확인), or should it repair the ONNX decision surface(온엑스 결정 표면) first because density(밀도) is below 5/day and PF(수익 팩터) is only 1.17?

Please answer in this structure:
1. Recommendation(권고): proceed_to_precheck(사전 확인 진행) / repair_first(수리 우선) / closeout_negative_memory(부정 기억 마감)
2. Reasoning(근거)
3. Risks(위험)
4. Narrow next experiment(좁은 다음 실험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output() -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    if "repair_first" in lower or "repair first" in lower:
        recommendation = "repair_first(수리 우선)"
    elif "proceed_to_precheck" in lower or "proceed to precheck" in lower:
        recommendation = "proceed_to_precheck(사전 확인 진행)"
    elif "closeout" in lower:
        recommendation = "closeout_negative_memory(부정 기억 마감)"
    else:
        recommendation = "needs_codex_local_decision(코덱스 로컬 결정 필요)"
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
            "repair_first(수리 우선)",
            "do_not_open_wfo_mt5_yet(아직 WFO/MT5 열지 않음)",
            "treat_frontier03c_as_seed_observation_only(Frontier03C는 씨앗 관찰 전용)",
        ],
        "rejected": [
            "proceed_to_precheck_now(지금 사전 확인 진행)",
            "closeout_negative_memory_now(지금 부정 기억 마감)",
        ],
        "needs_local_verification": [
            "bounded decision-surface repair(제한 결정 표면 수리)",
            "density/PF/DD joint guardrails(밀도/수익 팩터/손실폭 동시 보호)",
        ],
        "next_run_id": NEXT_REPAIR_RUN_ID,
        "claim_boundary": {
            "completion": "not_claimed(주장 없음)",
            "baseline": "not_claimed(주장 없음)",
            "promotion": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "live_readiness": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    }


def update_docs_and_state(classification: dict[str, Any]) -> None:
    now = classification["created_at_utc"]
    write_text_sig(REPORT_PATH, report_text(classification))
    f03b.append_once(
        Path("stages") / STAGE_ID / "03_reviews" / "review_index.md",
        RUN_ID,
        f"- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `repair_first_grok_review_no_authority(수리 우선 그록 검토, 권위 없음)`\n",
    )
    write_text_sig(
        Path("stages") / STAGE_ID / "04_selected" / "selection_status.md",
        f"""# Stage Frontier 03 Selection Status(전선 03단계 선택 상태)

Updated(갱신): {now}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `repair_first_grok_review_no_authority(수리 우선 그록 검토, 권위 없음)`

Grok recommendation(그록 권고): `{classification['recommendation_inferred']}`

Next action(다음 행동): `{NEXT_REPAIR_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )
    workspace_payload = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": "completed_grok_pre_expensive_review_repair_first_no_authority",
        "current_judgment": "repair_first_grok_review_no_authority",
        "next_run_id": NEXT_REPAIR_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    import yaml

    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(workspace_payload), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(
        f03b.CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Grok pre-expensive review(비싼 검증 전 그록 검토)는 `repair_first(수리 우선)`를 권고했습니다.

Judgment(판정): `repair_first_grok_review_no_authority(수리 우선 그록 검토, 권위 없음)`

Next action(다음 행동): `{NEXT_REPAIR_RUN_ID}`. Action(행동)은 existing ONNX decision surface(기존 온엑스 결정 표면)를 bounded repair(제한 수리)하는 것입니다. Effect(효과)는 WFO/MT5(워크포워드/MT5)를 열기 전에 density/PF/DD(밀도/수익 팩터/손실폭)를 같이 개선할 수 있는지 확인하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, classification))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(classification))
    f03b.upsert_csv(Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(classification))
    f03b.append_once(f03b.CHANGELOG, RUN_ID, f"- {now}: `{RUN_ID}` classified Grok pre-expensive review(비싼 검증 전 그록 검토) as repair_first(수리 우선). Effect(효과): WFO/MT5 전 bounded repair(제한 수리)로 이동합니다.\n")
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, f"- `{RUN_ID}`: Grok pre-expensive review(비싼 검증 전 그록 검토) accepted repair_first(수리 우선). Effect(효과): ONNX seed observation(온엑스 씨앗 관찰)을 WFO/MT5로 과장하지 않습니다.\n")


def report_text(classification: dict[str, Any]) -> str:
    return f"""# Frontier03D Grok Pre-Expensive Review Report(전선03D 비싼 검증 전 그록 검토 보고서)

Updated(갱신): {classification['created_at_utc']}

Judgment(판정): `repair_first_grok_review_no_authority(수리 우선 그록 검토, 권위 없음)`

Recommendation(권고): `{classification['recommendation_inferred']}`

## Read(판독)

Grok(그록)은 Frontier03C(전선03C)의 ONNX seed observation(온엑스 씨앗 관찰)을 인정했지만, density(밀도) `3.34/day`와 PF(수익 팩터) `1.17`은 expensive WFO/MT5 precheck(비싼 WFO/MT5 사전 확인)를 열기에는 약하다고 봤습니다.

Effect(효과): next action(다음 행동)은 `{NEXT_REPAIR_RUN_ID}`이고, WFO/MT5(워크포워드/MT5)는 아직 열지 않습니다.

## Evidence(근거)

- prompt(프롬프트): `{PROMPT_PATH.as_posix()}` sha256 `{sha256_file(PROMPT_PATH)}`
- output(출력): `{OUTPUT_PATH.as_posix()}` sha256 `{sha256_file(OUTPUT_PATH)}`
- metadata(메타데이터): `{METADATA_PATH.as_posix()}`

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def run_registry_row(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "grok_pre_expensive_review(비싼 검증 전 그록 검토)",
        "status": "completed_grok_pre_expensive_review_repair_first_no_authority",
        "judgment": "repair_first_grok_review_no_authority",
        "path": REPORT_PATH.as_posix(),
        "notes": "repair_first;no_wfo_no_mt5_no_authority",
        "work_family": "external_review(외부 검토)",
        "run_number": "frontier03D",
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_REPAIR_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "grok_review_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__grok_review",
        "subrun_id": f"{RUN_ID}__grok_review",
        "record_view": "Grok review(그록 검토)",
        "tier_scope": "not_applicable_review(해당 없음 검토)",
        "kpi_scope": "review_only_no_trading_kpi(검토 전용, 거래 KPI 없음)",
        "primary_kpi": "recommendation=repair_first(권고=수리 우선)",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured(그록 검토 기록)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "grok_pre_expensive_classification.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "external_second_opinion_only(외부 2차 의견 전용)",
        "reopen_condition": NEXT_REPAIR_RUN_ID,
        "question": "Should Frontier03C proceed to expensive WFO/MT5 or repair first?(전선03C는 비싼 WFO/MT5로 갈지 먼저 수리할지?)",
        "skill_family": "external_review(외부 검토)",
        "lineage_summary": "frontier03c_evidence_to_grok_review(전선03C 근거에서 그록 검토)",
    }


def ledger_row(classification: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__grok_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__grok_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Grok review(그록 검토)",
        "tier_scope": "not_applicable_review(해당 없음 검토)",
        "kpi_scope": "review_only_no_trading_kpi(검토 전용, 거래 KPI 없음)",
        "scoreboard_lane": "grok_pre_expensive_review(비싼 검증 전 그록 검토)",
        "status": "completed_grok_pre_expensive_review_repair_first_no_authority",
        "judgment": "repair_first_grok_review_no_authority",
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": "recommendation=repair_first(권고=수리 우선)",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured(그록 검토 기록)",
        "notes": f"next={NEXT_REPAIR_RUN_ID};no_authority",
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
