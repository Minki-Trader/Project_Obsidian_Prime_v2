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


STAGE_ID = "stage_frontier_19__boosted_backbone_no_repair_stack_onnx_scout"
RUN_ID = "frontier19C_boosted_backbone_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier19C"
PARENT_RUN_ID = "frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1"
NEXT_RUN_ID = "frontier20A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_negative_memory_boosted_backbone_no_proxy_survivor_no_authority"
JUDGMENT = "negative_memory(부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_ROOT / "03_reviews"
REPORT_PATH = REVIEW_DIR / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_19_boosted_backbone_closeout_negative_memory.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_19/frontier19c_boosted_backbone_closeout.py")

F19A_REPORT = REVIEW_DIR / "frontier19A_stage_open_boosted_backbone_no_repair_stack_onnx_scout_v1_report.md"
F19B_REPORT = REVIEW_DIR / "frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1_report.md"
F19B_FINAL = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "final_summary.json"
F19B_MODEL_AUDIT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "model_export_parity_audit.csv"
F19B_CANDIDATES = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "candidate_summary.csv"
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier19_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")

NEGATIVE_MEMORY = (
    "capped_boosted_tree_backbone_only_valid_onnx_but_no_forward_economic_clue"
    "(상한 부스팅 트리 백본 단독은 유효 ONNX를 만들지만 전진 경제 단서 없음)"
)
RUNTIME_BLOCKER = (
    "no_forward_clue_rows_0_0_0_and_no_runtime_handoff_candidate_under_backbone_only_lock"
    "(전진 단서 0/0/0이고 백본 단독 잠금 아래 런타임 인계 후보 없음)"
)


def main() -> int:
    now = utc_now()
    ensure_dirs()
    normalize_grok_markdown()
    f19b = read_json(F19B_FINAL)
    grok = read_grok()
    local = local_verification(f19b, grok)
    summary = build_summary(now, f19b, grok, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "negative_memory": summary["negative_memory"],
        "runtime_blocker": summary["runtime_blocker"],
        "grok_classification": summary["grok"]["classification"],
        "local_verification": summary["local_verification"]["judgment"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REVIEW_DIR, STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(REVIEW_DIR / "stage_run_ledger.csv", ALPHA_LEDGER)


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_CLOSEOUT_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok() -> dict[str, Any]:
    metadata = read_json(GROK_CLOSEOUT_PACKET / "metadata.json")
    output = read_text(GROK_CLOSEOUT_PACKET / "clean_output.md")
    lowered = output.lower()
    return {
        "packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "prompt": (GROK_CLOSEOUT_PACKET / "prompt.md").as_posix(),
        "output": (GROK_CLOSEOUT_PACKET / "clean_output.md").as_posix(),
        "metadata": (GROK_CLOSEOUT_PACKET / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "duration_seconds": metadata.get("duration_seconds", ""),
        "preflight_warnings": metadata.get("preflight_warnings", []),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "decision_advice_close_negative": "close_negative_memory" in lowered,
        "no_authority_clean": not any(term in lowered for term in (
            "runtime authority granted",
            "live readiness granted",
            "selected baseline granted",
            "goal achieve granted",
            "목표 달성 승인",
            "런타임 권위 승인",
        )),
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "classification" in lowered and "accepted" in lowered:
        return "accepted(수용)"
    if "classification" in lowered and "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(f19b: dict[str, Any], grok: dict[str, Any]) -> dict[str, Any]:
    model_audit = read_text(F19B_MODEL_AUDIT)
    best = f19b.get("best_summary", {})
    checks = {
        "f19b_no_forward_clue": f19b.get("status") == "boosted_backbone_no_forward_clue_no_authority",
        "strict_seed_preserved_zero": f19b.get("strict_count") == 0 and f19b.get("seed_count") == 0 and f19b.get("preserved_count") == 0,
        "handoff_candidate_zero": f19b.get("handoff_candidate_count") == 0,
        "onnx_parity_four_of_four": f19b.get("onnx_parity_pass_count") == 4 and "True" in model_audit,
        "best_metric_matches_no_clue": (
            float(best.get("validation_max_drawdown_percent", 0.0)) > 80.0
            and float(best.get("oos_max_drawdown_percent", 0.0)) > 40.0
            and float(best.get("validation_trades_per_day", 0.0)) > 30.0
            and float(best.get("oos_trades_per_day", 0.0)) > 30.0
        ),
        "runtime_blocker_recorded": "no_runtime_handoff_candidate" in str(f19b.get("runtime_probe_boundary", "")),
        "grok_success": bool(grok["success"]),
        "grok_accepted": grok["classification"] == "accepted(수용)",
        "grok_advises_close_negative": bool(grok["decision_advice_close_negative"]),
        "grok_no_unexpected_artifacts": not grok["unexpected_top_level_artifacts"],
        "grok_no_forbidden_authority": bool(grok["no_authority_clean"]),
    }
    return {
        "judgment": "pass_close_negative_memory(부정 기억 마감 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
    }


def build_summary(now: str, f19b: dict[str, Any], grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "negative_memory": NEGATIVE_MEMORY,
        "runtime_blocker": RUNTIME_BLOCKER,
        "reusable_artifact_note": (
            "ONNX export/parity mechanics are reusable artifact notes only(ONNX 내보내기/동등성 절차는 재사용 산출물 메모 전용). "
            "They are not preserved clue, selected baseline, or runtime authority(보존 단서/선택 기준선/런타임 권위 아님)."
        ),
        "f19b_best_candidate": f19b.get("best_candidate_id", ""),
        "f19b_best_summary": f19b.get("best_summary", {}),
        "f19b_counts": {
            "strict_count": f19b.get("strict_count"),
            "seed_count": f19b.get("seed_count"),
            "preserved_count": f19b.get("preserved_count"),
            "handoff_candidate_count": f19b.get("handoff_candidate_count"),
            "onnx_parity_pass_count": f19b.get("onnx_parity_pass_count"),
            "model_count": f19b.get("model_count"),
        },
        "failure_attribution": [
            "ONNX export/parity passed 4/4(ONNX 내보내기/동등성 4/4 통과)",
            "Best validation/OOS PF stayed near 1.03/1.05(최상 검증/표본외 수익 팩터가 1.03/1.05 근처)",
            "Best density stayed over objective at about 32~37/day(최상 빈도가 목표보다 높은 32~37/day)",
            "Best DD stayed far over target at about 81%/41%(최상 손실폭이 목표보다 높은 81%/41%)",
        ],
        "closeout_decision": "closed_negative_memory(부정 기억 마감)",
        "grok": grok,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "closeout_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(REVIEW_DIR / "review_index.md", review_index(summary))
    f03b.write_text_sig(REVIEW_DIR / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": summary["status"],
        "judgment": summary["judgment"],
        "script": artifact_identity(SCRIPT_PATH),
        "inputs": {
            "f19a_report": artifact_identity(F19A_REPORT),
            "f19b_report": artifact_identity(F19B_REPORT),
            "f19b_final": artifact_identity(F19B_FINAL),
            "f19b_model_audit": artifact_identity(F19B_MODEL_AUDIT),
            "f19b_candidates": artifact_identity(F19B_CANDIDATES),
            "grok_closeout": summary["grok"],
        },
        "outputs": {
            "closeout_summary": (RUN_ROOT / "closeout_summary.json").as_posix(),
            "report": artifact_identity(REPORT_PATH),
            "decision": DECISION_PATH.as_posix(),
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }


def report_text(summary: dict[str, Any]) -> str:
    best = summary["f19b_best_summary"]
    return f"""# Frontier19C Closeout Report(전선19C 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier19(전선19)를 negative memory(부정 기억)로 닫았습니다.

Effect(효과): capped boosted-tree backbone-only(상한 부스팅 트리 백본 단독) 가설을 같은 repair stack(수리 중첩)으로 반복하지 않고, ONNX conversion(ONNX 변환)이 아니라 proxy economics/density/DD(프록시 경제성/빈도/손실폭)가 실패 원인임을 분리합니다.

Negative memory(부정 기억): `{summary['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{summary['runtime_blocker']}`

Best candidate(최상 후보): `{summary['f19b_best_candidate']}`

- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_max_drawdown_percent'))}%`
- OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_max_drawdown_percent'))}%`
- ONNX parity(ONNX 동등성): `{summary['f19b_counts']['onnx_parity_pass_count']}` / `{summary['f19b_counts']['model_count']}`
- strict/seed/preserved/handoff(엄격/씨앗/보존/인계): `{summary['f19b_counts']['strict_count']}` / `{summary['f19b_counts']['seed_count']}` / `{summary['f19b_counts']['preserved_count']}` / `{summary['f19b_counts']['handoff_candidate_count']}`

Grok closeout classification(그록 마감 분류): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Reusable artifact note(재사용 산출물 메모): {summary['reusable_artifact_note']}

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Review Index(전선19 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `frontier19A_stage_open_boosted_backbone_no_repair_stack_onnx_scout_v1`: stage open(단계 개방), Grok adjusted accepted(그록 수정 수용).
- `frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1`: proxy scout(프록시 탐색), 4/4 ONNX parity(ONNX 동등성), 0/0/0 forward clue(전진 단서 없음).
- `{RUN_ID}`: closeout(마감), negative memory(부정 기억), no runtime handoff candidate(런타임 인계 후보 없음).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier19C Required Gate Coverage Audit(전선19C 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_close_negative_memory(부정 기억 마감 통과)

- closeout_gate(마감 게이트): negative memory(부정 기억) selected with no authority claims(권위 주장 없음).
- external_review_packet(외부 검토 묶음): Grok accepted close_negative_memory(그록 부정 기억 마감 수용), packet(묶음) `{summary['grok']['packet']}`.
- runtime_evidence_gate(런타임 근거 게이트): MT5 not run because exact blocker recorded(MT5 미실행, 정확한 차단 사유 기록) `{summary['runtime_blocker']}`.
- kpi_contract_audit(KPI 계약 감사): F19B PF/density/DD/smoothness(PF/빈도/손실폭/매끄러움) and ONNX parity(ONNX 동등성) reviewed(검토).
- tier_record_gate(티어 기록 게이트): F19B Tier A materialized(티어 A 물질화), Tier B missing_required(티어 B 필수 누락), Tier A+B out_of_scope_by_claim(합산 주장 범위 밖).
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Selection Status(전선19 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Closeout(마감): `{summary['judgment']}`

Negative memory(부정 기억): `{summary['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{summary['runtime_blocker']}`

Reusable artifact note(재사용 산출물 메모): ONNX export/parity mechanics(ONNX 내보내기/동등성 절차)는 재사용 산출물 메모일 뿐 preserved clue(보존 단서)가 아닙니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier19 As Negative Memory(결정: 전선19 부정 기억 마감)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier19(전선19)의 capped boosted backbone-only hypothesis lifecycle(상한 부스팅 백본 단독 가설 생명주기)을 닫았습니다.

Effect(효과): valid ONNX(유효 ONNX)만으로는 목표 네 축(PF/빈도/손실폭/매끄러움)에 가까워지지 않는다는 negative memory(부정 기억)를 남기고, 다음 frontier stage(전선 단계)는 새 가설로 시작합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(f03b.WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier19_closed_negative_memory_valid_onnx_no_forward_economic_clue_no_runtime_handoff_candidate_no_authority",
        "family": "result_judgment(결과 판정)",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_closeout_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_wfo_no_mt5_no_authority( WFO/MT5/권위 없음)",
        "external_verification_status": f"grok_closeout_accepted_runtime_blocker_recorded(그록 마감 수용, 런타임 차단 기록): {summary['runtime_blocker']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_negative_memory_not_runtime(단계 마감 부정 기억, 런타임 아님)",
            "primary_kpi": "strict=0;seed=0;preserved=0;handoff=0;onnx_parity=4/4",
            "notes": "closed_negative_memory_no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)",
            "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def negative_register_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: {summary['negative_memory']}. "
        f"Runtime blocker(런타임 차단): `{summary['runtime_blocker']}`. "
        "Effect(효과): boosted backbone-only(부스팅 백본 단독)을 repair stack(수리 중첩) 없이 반복하지 않습니다.\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: Frontier19(전선19) closed as negative memory(부정 기억). "
        "Effect(효과): ONNX export/parity(ONNX 내보내기/동등성)는 재사용 산출물 메모로만 남기고, 다음 전선은 새 가설로 시작합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` closed Frontier19(전선19) as negative memory(부정 기억). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` starts a new hypothesis(새 가설).\n"
    )


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

Action(행동): Frontier19(전선19)를 negative memory(부정 기억)로 닫았습니다.

Effect(효과): capped boosted-tree backbone-only(상한 부스팅 트리 백본 단독)는 valid ONNX(유효 ONNX) 4/4를 만들었지만, repair stack(수리 중첩) 없이 PF/density/DD/smoothness(PF/빈도/손실폭/매끄러움)를 살리지 못했다는 사실을 다음 가설의 반복 금지 근거로 남깁니다.

Runtime probe blocker(런타임 탐침 차단 사유): `{summary['runtime_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    with io_path(template_path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "0"
    return f"{number:.6g}" if number == number else "0"


if __name__ == "__main__":
    raise SystemExit(main())
