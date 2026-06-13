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


STAGE_ID = "stage_frontier_04__path_aware_cost_dd_event_labeling"
RUN_ID = "frontier04C_grok_pre_trainable_transfer_review_v1"
RUN_NUMBER = "frontier04C"
PARENT_RUN_ID = "frontier04B_path_aware_label_proxy_scout_v1"
NEXT_PROCEED_RUN_ID = "frontier04D_trainable_path_label_onnx_probe_v1"
NEXT_REPAIR_RUN_ID = "frontier04D_path_label_proxy_repair_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier04D_stage_closeout_negative_memory_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier04_pre_trainable_transfer/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F04B_RUN_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F04B_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
F04B_MANIFEST = F04B_RUN_ROOT / "run_manifest.json"
F04B_TOP = F04B_RUN_ROOT / "top.csv"
F04B_SUMMARY = F04B_RUN_ROOT / "summary.csv"
F04B_INTEGRITY = F04B_RUN_ROOT / "integrity.json"


def main() -> int:
    ensure_dirs()
    if not path_exists(PROMPT_PATH):
        write_text_sig(PROMPT_PATH, prompt_text())
        print(json.dumps({
            "status": "prompt_ready",
            "run_id": RUN_ID,
            "prompt": PROMPT_PATH.as_posix(),
            "next_command": (
                "python -m foundation.control_plane.grok_review_wrapper "
                f"--prompt-file {PROMPT_PATH.as_posix()} --review-size medium "
                f"--output-dir {GROK_ROOT.as_posix()} --repo-root . --cwd . --timeout-seconds 300 --json"
            ),
        }, ensure_ascii=False, indent=2))
        return 0
    if not path_exists(OUTPUT_PATH) or not path_exists(METADATA_PATH):
        print(json.dumps({
            "status": "awaiting_grok_output",
            "run_id": RUN_ID,
            "missing": [path.as_posix() for path in (OUTPUT_PATH, METADATA_PATH) if not path_exists(path)],
        }, ensure_ascii=False, indent=2))
        return 0
    now = utc_now()
    classification = classify_output(now)
    final = build_final(now, classification)
    write_outputs(final, classification)
    update_registries(final)
    print(json.dumps({
        "status": "grok_pre_trainable_review_materialized",
        "run_id": RUN_ID,
        "recommendation": classification["recommendation_inferred"],
        "next_run_id": final["next_run_id"],
    }, ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (GROK_ROOT, RUN_ROOT, REPORT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def prompt_text() -> str:
    top = read_top_row()
    integrity = read_json(F04B_INTEGRITY)
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Frontier04C pre-trainable-transfer gate(전선04C 학습 가능 전달 전 게이트).

Current truth(현재 진실):
- Stage(단계): `{STAGE_ID}`
- Parent run(부모 실행): `{PARENT_RUN_ID}`
- Parent judgment(부모 판정): seed_surface(씨앗 표면), no authority(권위 없음)
- Best path row(최상위 경로 행): `{top.get('variant_id')}`
- Validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{top.get('validation_profit_factor')}` / `{top.get('validation_trades_per_day')}/day` / `{top.get('validation_dd_risk_percent')}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{top.get('oos_profit_factor')}` / `{top.get('oos_trades_per_day')}/day` / `{top.get('oos_dd_risk_percent')}%`
- Joint pass(동시 통과): `{top.get('validation_oos_joint_pass')}`
- Integrity judgment(무결성 판정): `{integrity.get('integrity_judgment')}`
- Alignment(정렬): missing raw matches(원천 매칭 누락) `{integrity.get('missing_or_duplicate_check', {}).get('missing_raw_matches')}`, raw duplicate close keys(원천 중복 종가 키) `{integrity.get('missing_or_duplicate_check', {}).get('raw_duplicate_close_keys')}`, missing future paths(미래 경로 누락) `{integrity.get('missing_or_duplicate_check', {}).get('missing_future_paths')}`
- Time boundary(시간 경계): timezone remains unresolved(시간대는 미해결), so no direct UTC/session claim(직접 UTC/세션 주장 없음)
- Label boundary(라벨 경계): future OHLC after t+1 only(t+1 이후 미래 OHLC만 사용), no feature_set_v2 columns in label construction(라벨 생성에 피처 컬럼 없음)
- Known weakness(알려진 약점): path label is still an oracle proxy(경로 라벨은 여전히 오라클 프록시); high PF may be proxy inflation(높은 수익 팩터는 프록시 과장일 수 있음)

Bounded evidence(제한 근거):
- Frontier04B report(전선04B 보고서): `{F04B_REPORT.as_posix()}` sha256 `{sha256_file(F04B_REPORT)}`
- Frontier04B manifest(전선04B 실행 목록): `{F04B_MANIFEST.as_posix()}` sha256 `{sha256_file(F04B_MANIFEST)}`
- Frontier04B top rows(전선04B 상위 행): `{F04B_TOP.as_posix()}` sha256 `{sha256_file(F04B_TOP)}`
- Frontier04B summary(전선04B 요약): `{F04B_SUMMARY.as_posix()}` sha256 `{sha256_file(F04B_SUMMARY)}`
- Frontier04B integrity(전선04B 무결성): `{F04B_INTEGRITY.as_posix()}` sha256 `{sha256_file(F04B_INTEGRITY)}`
- Stage355 precedent(Stage355 선례): `stage_pipelines/stage355/materialize_density_recovery_label_inputs_without_db.py:first_barrier_labels`

Proposed Codex direction before Grok(그록 전 코덱스 제안 방향):
- Do not claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 금지).
- If accepted, run `{NEXT_PROCEED_RUN_ID}` as a narrow trainable ONNX transfer probe(좁은 학습 가능 온엑스 전달 탐침): train a small fixed-grid model from the path labels, keep feature_set_v2 fixed, no WFO/MT5, and compare validation/OOS against the proxy clue.
- If rejected, route to `{NEXT_REPAIR_RUN_ID}` or `{NEXT_CLOSEOUT_RUN_ID}` without threshold-only broad sweeps(넓은 임계값 전용 반복 없음).

Focused question(집중 질문):
Should Codex proceed to a narrow trainable ONNX transfer probe(좁은 학습 가능 온엑스 전달 탐침) from this seed surface(씨앗 표면), revise the proxy first(프록시 먼저 수정), close as negative memory(부정 기억 마감), or block(차단)?

Please answer in this structure:
1. Recommendation(권고): proceed_to_trainable_probe(학습 가능 탐침 진행) / revise_proxy(프록시 수정) / close_negative_memory(부정 기억 마감) / blocked(차단)
2. Reasoning(근거)
3. Required bounds for the next run(다음 실행 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        (lower.find("proceed_to_trainable_probe"), "proceed_to_trainable_probe(학습 가능 탐침 진행)"),
        (lower.find("revise_proxy"), "revise_proxy(프록시 수정)"),
        (lower.find("close_negative_memory"), "close_negative_memory(부정 기억 마감)"),
        (lower.find("blocked"), "blocked(차단)"),
    ]
    seen = [(pos, label) for pos, label in choices if pos >= 0]
    recommendation = min(seen, default=(0, "revise_proxy(프록시 수정)"))[1]
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
        "accepted": [],
        "rejected": [],
        "needs_local_verification": [
            "Codex must verify any Grok advice against local artifacts before action(코덱스는 그록 조언을 로컬 산출물로 재검증 후 행동)",
            "No WFO/MT5 until trainable transfer has local evidence(학습 가능 전달 로컬 근거 전 WFO/MT5 없음)",
        ],
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def build_final(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    recommendation = classification["recommendation_inferred"]
    if recommendation.startswith("proceed_to_trainable_probe"):
        next_run = NEXT_PROCEED_RUN_ID
        judgment = "external_review_accepts_trainable_probe_with_bounds(외부 검토가 경계부 학습 탐침을 수용)"
        status = "grok_review_accepts_next_probe_no_authority"
    elif recommendation.startswith("close_negative_memory"):
        next_run = NEXT_CLOSEOUT_RUN_ID
        judgment = "external_review_recommends_negative_memory_close(외부 검토가 부정 기억 마감을 권고)"
        status = "grok_review_recommends_closeout_no_authority"
    elif recommendation.startswith("blocked"):
        next_run = NEXT_REPAIR_RUN_ID
        judgment = "external_review_blocked_needs_local_repair(외부 검토 차단, 로컬 수리 필요)"
        status = "grok_review_blocked_no_authority"
    else:
        next_run = NEXT_REPAIR_RUN_ID
        judgment = "external_review_recommends_proxy_revision(외부 검토가 프록시 수정을 권고)"
        status = "grok_review_recommends_revision_no_authority"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": status,
        "judgment": judgment,
        "recommendation": recommendation,
        "next_run_id": next_run,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], classification: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "classification.json", classification)
    write_json(RUN_ROOT / "run_manifest.json", {
        **final,
        "script_path": "stage_pipelines/stage_frontier_04/frontier04c_grok_pre_trainable_transfer_review.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_04/frontier04c_grok_pre_trainable_transfer_review.py")),
        "outputs": {
            "classification": {"path": (RUN_ROOT / "classification.json").as_posix(), "sha256": sha256_file(RUN_ROOT / "classification.json")},
            "report": {"path": REPORT_PATH.as_posix()},
        },
        "grok_prompt": {"path": PROMPT_PATH.as_posix(), "sha256": sha256_file(PROMPT_PATH)},
        "grok_output": {"path": OUTPUT_PATH.as_posix(), "sha256": sha256_file(OUTPUT_PATH)},
    })
    write_text_sig(REPORT_PATH, report_text(final, classification))


def report_text(final: dict[str, Any], classification: dict[str, Any]) -> str:
    return f"""# Frontier04C Grok Pre-Trainable Transfer Review(전선04C 그록 학습 가능 전달 전 검토)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Grok recommendation(그록 권고): `{classification['recommendation_inferred']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier04B(전선04B) seed surface(씨앗 표면)를 Grok(그록)에 제한 근거로 보냈습니다.

Effect(효과): proxy oracle(프록시 오라클)을 trainable ONNX(학습 가능 온엑스)나 WFO/MT5(워크포워드/메타트레이더5) 주장으로 자동 승격하지 않고, 다음 실행 경계를 외부 비판과 로컬 재검증에 묶었습니다.

## Next Action(다음 행동)

`{final['next_run_id']}`.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def update_registries(final: dict[str, Any]) -> None:
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": final["status"],
        "current_judgment": final["judgment"],
        "next_run_id": final["next_run_id"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": final["created_at_utc"],
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final))
    row = ledger_row(final)
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n",
    )


def current_state_text(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier04C(전선04C)는 Grok pre-trainable-transfer review(그록 학습 가능 전달 전 검토)를 기록했습니다.

Judgment(판정): `{final['judgment']}`

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 Grok(그록) 권고를 로컬 검증한 경계 안에서 다음 탐색 실행으로 옮기는 것입니다. Effect(효과)는 proxy clue(프록시 단서)를 운영 의미(operating meaning, 운영 의미)로 과장하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "grok_review(그록 검토)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"recommendation={final['recommendation']};next={final['next_run_id']};no_authority",
        "work_family": "external_review(외부 검토)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": "0",
        "claim_boundary": "grok_review_only_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__grok_review",
        "subrun_id": f"{RUN_ID}__grok_review",
        "record_view": "external_review(외부 검토)",
        "tier_scope": "not_applicable_review(검토에는 해당 없음)",
        "kpi_scope": "review_only_no_trading_kpi(검토 전용, 거래 KPI 없음)",
        "primary_kpi": f"recommendation={final['recommendation']}",
        "guardrail_kpi": "no_model_training_no_onnx_no_wfo_no_mt5_no_authority(모델 학습/온엑스/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "run_manifest.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "external_review_only(외부 검토 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Should Frontier04B seed surface move to trainable ONNX probe?(전선04B 씨앗 표면을 학습 가능 온엑스 탐침으로 넘겨도 되는가?)",
        "skill_family": "grok_collaboration(그록 협업)",
        "lineage_summary": "frontier04b_proxy_to_pre_trainable_grok_gate(전선04B 프록시에서 학습 전 그록 게이트)",
    }


def ledger_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__grok_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__grok_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "external_review(외부 검토)",
        "tier_scope": "not_applicable_review(검토에는 해당 없음)",
        "kpi_scope": "review_only_no_trading_kpi(검토 전용, 거래 KPI 없음)",
        "scoreboard_lane": "grok_review(그록 검토)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"recommendation={final['recommendation']}",
        "guardrail_kpi": "no_model_training_no_onnx_no_wfo_no_mt5_no_authority(모델 학습/온엑스/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "notes": f"next={final['next_run_id']};no_authority",
    }


def read_top_row() -> dict[str, str]:
    with io_path(F04B_TOP).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
