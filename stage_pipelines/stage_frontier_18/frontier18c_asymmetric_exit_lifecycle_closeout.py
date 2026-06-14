from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402


TODAY = "2026-06-14"
STAGE_ID = "stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout"
RUN_ID = "frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier18C"
PARENT_RUN_ID = "frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1"
NEXT_RUN_ID = "frontier19A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_negative_memory_asymmetric_exit_lifecycle_no_proxy_survivor_no_authority"
JUDGMENT = "negative_memory(부정 기억)"
CLAIM_BOUNDARY = (
    "negative_memory_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_BLOCKER = (
    "no_forward_clue_rows_0_0_0_and_no_runtime_handoff_candidate_under_pre_registered_profile_lock"
    "(전진 단서 0/0/0이고 사전 등록 프로필 고정 아래 런타임 인계 후보 없음)"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
F18B_RUN_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
REVIEW_DIR = STAGE_ROOT / "03_reviews"
SELECTED_DIR = STAGE_ROOT / "04_selected"
SPEC_DIR = STAGE_ROOT / "00_spec"
GROK_CLOSEOUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier18_stage_closeout/small_review")

F18B_FINAL = F18B_RUN_ROOT / "final_decision.json"
F18B_SUMMARY = F18B_RUN_ROOT / "candidate_summary.csv"
F18B_PARITY = F18B_RUN_ROOT / "onnx_parity.csv"
F18B_TRADE_LOG = F18B_RUN_ROOT / "trade_log.csv"
F18B_REPORT = REVIEW_DIR / f"{PARENT_RUN_ID}_report.md"
F18A_REPORT = REVIEW_DIR / "frontier18A_stage_open_asymmetric_exit_lifecycle_profit_lock_onnx_scout_v1_report.md"
GROK_OUTPUT = GROK_CLOSEOUT / "clean_output.md"
GROK_METADATA = GROK_CLOSEOUT / "metadata.json"

REPORT_PATH = REVIEW_DIR / f"{RUN_ID}_report.md"
CLOSEOUT_SUMMARY = RUN_ROOT / "closeout_summary.json"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
DECISION_DOC = Path("docs/decisions") / f"{TODAY}_stage_frontier_18_asymmetric_exit_lifecycle_closeout_negative_memory.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_GATE_AUDIT_MD = REVIEW_DIR / "required_gate_coverage_audit.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
README_PATH = STAGE_ROOT / "README.md"
ARTIFACT_REGISTRY = Path("docs/registers/artifact_registry.csv")


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    evidence = load_and_verify_evidence()
    final = build_final(created_at, evidence)
    write_outputs(final, evidence)
    update_docs_and_registers(final, evidence)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "negative_memory": final["negative_memory"],
                    "preserved_clue": final["preserved_clue"],
                    "runtime_probe_blocker": final["runtime_probe_blocker"],
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_LEDGER, f03b.ALPHA_LEDGER)


def load_and_verify_evidence() -> dict[str, Any]:
    f18b = read_json(F18B_FINAL)
    summary = pd.read_csv(io_path(F18B_SUMMARY), encoding="utf-8-sig")
    parity = pd.read_csv(io_path(F18B_PARITY), encoding="utf-8-sig")
    grok_text = read_text(GROK_OUTPUT)
    grok_meta = read_json(GROK_METADATA)
    best = dict(f18b.get("best_candidate_row", {}))
    checks = {
        "f18b_status_no_forward_clue": f18b.get("status") == "asymmetric_exit_lifecycle_no_forward_clue_no_authority",
        "f18b_zero_strict_seed_preserved": (
            int(f18b.get("strict_scout_clue_rows", -1)) == 0
            and int(f18b.get("seed_surface_rows", -1)) == 0
            and int(f18b.get("preserved_clue_rows", -1)) == 0
        ),
        "candidate_rows_9": int(len(summary)) == 9,
        "summary_all_failed_forward_clues": not bool(
            summary[["strict_scout_clue_pass", "seed_surface_pass", "preserved_clue_pass"]].astype(bool).any().any()
        ),
        "onnx_parity_all_passed": bool(parity["parity_passed"].astype(bool).all()),
        "best_oos_pf_below_seed_floor": float(best.get("oos_profit_factor", 999.0)) < 1.2,
        "best_oos_density_above_goal_band": float(best.get("oos_trades_per_day", 0.0)) > 10.0,
        "negative_subperiod_fraction_high": float(best.get("validation_oos_negative_subperiod_fraction", 0.0)) > 0.35,
        "grok_closeout_success": bool(grok_meta.get("success")) and not bool(grok_meta.get("timed_out")),
        "grok_closeout_accepted": "accepted" in grok_text.lower(),
        "runtime_blocker_phrase_in_grok": "no_forward_clue_rows_0_0_0" in grok_text,
    }
    if not all(checks.values()):
        raise RuntimeError("F18C closeout evidence check failed: " + json.dumps(checks, ensure_ascii=False))
    return {
        "f18b_final": f18b,
        "best": best,
        "candidate_summary_rows": summary.to_dict("records"),
        "parity_rows": parity.to_dict("records"),
        "grok_closeout_classification": "accepted(수용)",
        "checks": checks,
    }


def build_final(created_at: str, evidence: Mapping[str, Any]) -> dict[str, Any]:
    best = dict(evidence["best"])
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "best_candidate_row": best,
        "negative_memory": (
            "asymmetric_exit_lifecycle_profit_lock_failed_pf_density_smoothness_under_pre_registered_profiles"
            "(사전 등록 프로필 아래 비대칭 청산 생명주기 수익 잠금은 PF/빈도/매끄러움에서 실패)"
        ),
        "preserved_clue": (
            "low_dd_lifecycle_shapes_preserved_as_dd_containment_clue_only"
            "(낮은 손실폭 생명주기 모양은 손실폭 억제 단서로만 보존)"
        ),
        "runtime_probe_blocker": RUNTIME_BLOCKER,
        "runtime_probe_observation": (
            "not_run_exact_blocker_recorded_no_runtime_handoff_candidate"
            "(미실행, 런타임 인계 후보 없음이라는 정확한 차단 사유 기록)"
        ),
        "grok_closeout_classification": evidence["grok_closeout_classification"],
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "closeout_paths": {
            "report": REPORT_PATH.as_posix(),
            "closeout_summary": CLOSEOUT_SUMMARY.as_posix(),
            "gate_audit": GATE_AUDIT.as_posix(),
            "f18b_candidate_summary": F18B_SUMMARY.as_posix(),
            "grok_closeout": GROK_OUTPUT.as_posix(),
        },
    }


def write_outputs(final: Mapping[str, Any], evidence: Mapping[str, Any]) -> None:
    gate_rows = gate_audit_rows(final, evidence)
    write_csv(GATE_AUDIT, gate_rows)
    write_json(CLOSEOUT_SUMMARY, final)
    write_json(RUN_MANIFEST, run_manifest(final, gate_rows, evidence))


def gate_audit_rows(final: Mapping[str, Any], evidence: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "f18b_proxy_boundary(F18B 프록시 경계)",
            "status": "failed_forward_clue_0_0_0(전진 단서 0/0/0 실패)",
            "evidence_path": F18B_SUMMARY.as_posix(),
            "effect": "strict/seed/preserved rows(엄격/씨앗/보존 행)가 모두 0이라 비싼 검증으로 넘기지 않습니다.",
        },
        {
            "gate_name": "onnx_parity_gate(ONNX 동등성 게이트)",
            "status": "passed_all_models(모든 모델 통과)",
            "evidence_path": F18B_PARITY.as_posix(),
            "effect": "실패 원인이 ONNX 변환 문제가 아니라 lifecycle economics(생명주기 경제성)임을 분리합니다.",
        },
        {
            "gate_name": "repair_legality_gate(수리 합법성 게이트)",
            "status": "blocked_inside_hypothesis(가설 내부 차단)",
            "evidence_path": GROK_OUTPUT.as_posix(),
            "effect": "validation/OOS 뒤 생명주기 파라미터 조정은 사전 등록 3프로필 고정을 위반합니다.",
        },
        {
            "gate_name": "runtime_probe_obligation_gate(런타임 탐침 의무 게이트)",
            "status": "exact_blocker_recorded(정확한 차단 사유 기록)",
            "evidence_path": CLOSEOUT_SUMMARY.as_posix(),
            "effect": RUNTIME_BLOCKER,
        },
        {
            "gate_name": "grok_closeout_review(Grok 마감 검토)",
            "status": "accepted_with_local_verification(로컬 검증 포함 수용)",
            "evidence_path": GROK_OUTPUT.as_posix(),
            "effect": "Grok은 negative memory closeout(부정 기억 마감)과 MT5 exact blocker(정확한 MT5 차단 사유)를 수용했습니다.",
        },
        {
            "gate_name": "claim_boundary_guard(주장 경계 보호)",
            "status": "passed_no_authority_claim(권위 주장 없음 통과)",
            "evidence_path": CLOSEOUT_SUMMARY.as_posix(),
            "effect": "completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 주장하지 않습니다.",
        },
    ]


def run_manifest(final: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]], evidence: Mapping[str, Any]) -> dict[str, Any]:
    output_paths = [
        REPORT_PATH,
        CLOSEOUT_SUMMARY,
        GATE_AUDIT,
        DECISION_DOC,
        F18B_SUMMARY,
        F18B_PARITY,
        F18B_TRADE_LOG,
        GROK_OUTPUT,
        GROK_METADATA,
    ]
    return {
        **dict(final),
        "script_path": Path(__file__).as_posix(),
        "script_sha256": sha256_file(Path(__file__)),
        "gate_rows": gate_rows,
        "local_verification": evidence["checks"],
        "artifacts": [artifact_identity(path) for path in output_paths],
    }


def update_docs_and_registers(final: Mapping[str, Any], evidence: Mapping[str, Any]) -> None:
    write_text_sig(REPORT_PATH, report_text(final))
    write_text_sig(REVIEW_INDEX, review_index_text(final))
    write_text_sig(STAGE_GATE_AUDIT_MD, stage_gate_audit_text(final))
    write_text_sig(SELECTION_STATUS, selection_status_text(final))
    write_text_sig(DECISION_DOC, decision_text(final))
    append_stage_brief(final)
    update_readme(final)
    write_text_sig(f03b.WORKSPACE_STATE, workspace_state_text(final))
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_LEDGER, "ledger_row_id", row)
    if path_exists(ARTIFACT_REGISTRY):
        append_csv_io(
            ARTIFACT_REGISTRY,
            [
                artifact_registry_row(final, name, path)
                for name, path in {
                    "closeout_summary": CLOSEOUT_SUMMARY,
                    "report": REPORT_PATH,
                    "run_manifest": RUN_MANIFEST,
                    "gate_audit": GATE_AUDIT,
                }.items()
            ],
        )
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(f03b.NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def report_text(final: Mapping[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier18C Closeout(전선18C 마감)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): F18B proxy(프록시)와 Grok closeout review(Grok 마감 검토)를 근거로 Frontier18(전선18)을 negative memory(부정 기억)로 닫았습니다.

Effect(효과): asymmetric exit lifecycle/profit lock(비대칭 청산 생명주기/수익 잠금) 가설을 같은 파라미터 수리로 반복하지 않고, 낮은 DD(drawdown, 손실폭) 형태만 참고 단서로 남깁니다.

## Evidence(근거)

- best candidate(최선 후보): `{best.get('candidate_id')}`
- validation PF/density/DD(검증 PF/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본외 PF/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- strict/seed/preserved(엄격/씨앗/보존): `0/0/0`
- ONNX parity(ONNX 동등성): all passed(모두 통과)
- Grok closeout(Grok 마감): `{final['grok_closeout_classification']}`

## Closeout(마감)

Negative memory(부정 기억): `{final['negative_memory']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier18 Review Index(전선18 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `frontier18A_stage_open_asymmetric_exit_lifecycle_profit_lock_onnx_scout_v1`: stage open(단계 개방), Grok accepted(Grok 수용), lifecycle profile locks(생명주기 프로필 고정).
- `{PARENT_RUN_ID}`: proxy scout(프록시 탐색), strict/seed/preserved(엄격/씨앗/보존) `0/0/0`.
- `{RUN_ID}`: closeout(마감), negative memory(부정 기억), exact runtime blocker(정확한 런타임 차단 사유).
- reports(보고서): `{F18A_REPORT.as_posix()}`, `{F18B_REPORT.as_posix()}`, `{REPORT_PATH.as_posix()}`
"""


def stage_gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier18 Required Gate Coverage Audit(전선18 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

## Covered Gates(충족 게이트)

- Grok stage open review(Grok 단계 개방 검토): accepted(수용), evidence(근거) `docs/agent_control/grok_reviews/2026-06-14_frontier18_stage_open/small_review/clean_output.md`
- Grok closeout review(Grok 마감 검토): accepted(수용), evidence(근거) `{GROK_OUTPUT.as_posix()}`
- proxy boundary(프록시 경계): F18B strict/seed/preserved(엄격/씨앗/보존) `0/0/0`, evidence(근거) `{F18B_SUMMARY.as_posix()}`
- ONNX parity(ONNX 동등성): all models passed(모든 모델 통과), evidence(근거) `{F18B_PARITY.as_posix()}`
- runtime probe obligation(런타임 탐침 의무): exact blocker(정확한 차단 사유) `{final['runtime_probe_blocker']}`
- result judgment(결과 판정): negative memory(부정 기억), evidence(근거) `{REPORT_PATH.as_posix()}`
- claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) not_claimed(주장 없음)

## Missing By Scope(범위상 누락)

- Tier B separate(티어 B 분리): missing_required(필수 누락)
- Tier A+B combined(티어 A+B 합산): missing_required(필수 누락)
- MT5 runtime probe(MT5 런타임 탐침): exact blocker recorded(정확한 차단 사유 기록)
- WFO/stress(워크포워드/스트레스): not_run_by_negative_proxy_closeout(부정 프록시 마감으로 미실행)

Effect(효과): Frontier18(전선18)은 낮은 DD 형태를 참고 단서로 남기지만, PF/빈도/매끄러움 실패 때문에 앞으로 보내지 않습니다.
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier18 Selection Status(전선18 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Closeout(마감): `{final['judgment']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`
"""


def decision_text(final: Mapping[str, Any]) -> str:
    return f"""# Decision: Frontier18 Closeout(결정: 전선18 마감)

Date(날짜): {final['created_at_utc']}

Decision(결정): `{final['status']}`

Action(행동): Frontier18(전선18)을 negative memory(부정 기억)로 닫았습니다.

Effect(효과): 사전 등록한 lifecycle profiles(생명주기 프로필) 안에서 PF/density/smoothness(PF/빈도/매끄러움)가 살아나지 않았음을 기록하고, 같은 수리 반복을 막습니다.

Next action(다음 행동): `{final['next_run_id']}`
"""


def append_stage_brief(final: Mapping[str, Any]) -> None:
    marker = f"<!-- {RUN_ID}__closeout -->"
    text = read_text(STAGE_BRIEF) if path_exists(STAGE_BRIEF) else f"# {STAGE_ID}\n"
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    text += f"""
{marker}

## Frontier18C Closeout(전선18C 마감)

Updated(갱신): {final['created_at_utc']}

Action(행동): F18(전선18)을 negative memory(부정 기억)로 닫았습니다.

Effect(효과): low-DD lifecycle shape(낮은 손실폭 생명주기 모양)은 참고만 하고, PF/density/smoothness(PF/빈도/매끄러움)가 부족한 asymmetric exit lifecycle(비대칭 청산 생명주기) 수리를 반복하지 않습니다.
"""
    write_text_sig(STAGE_BRIEF, text)


def update_readme(final: Mapping[str, Any]) -> None:
    text = f"""# Frontier18 Asymmetric Exit Lifecycle Profit Lock ONNX Scout(전선18 비대칭 청산 생명주기 수익 잠금 ONNX 탐색)

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Next run(다음 실행): `{final['next_run_id']}`

Effect(효과): 사전 등록 lifecycle profiles(생명주기 프로필) 3개는 PF/density/smoothness(PF/빈도/매끄러움)를 살리지 못해 negative memory(부정 기억)로 닫혔습니다.
"""
    write_text_sig(README_PATH, text)


def workspace_state_text(final: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            f"next_run_id: {final['next_run_id']}",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "",
        ]
    )


def current_working_state_text(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier18(전선18)은 negative memory(부정 기억)로 닫혔습니다.

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)는 생존 후보 부재로 exact blocker(정확한 차단 사유)를 기록했고, 다음 frontier(전선)는 새 hypothesis(가설)로 시작해야 합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: Mapping[str, Any]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict_seed_preserved=0_0_0;runtime_blocker={RUNTIME_BLOCKER}",
        "family": "result_judgment(결과 판정)",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "attempt_count": 1,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(best),
        "external_verification_status": "exact_blocker_no_mt5_runtime_probe(정확한 차단 사유, MT5 런타임 탐침 없음)",
        "result_path": REPORT_PATH.as_posix(),
        "gate_audit_path": GATE_AUDIT.as_posix(),
    }


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_authority_no_goal_claim(권위/목표 주장 없음)",
        "external_verification_status": "exact_blocker_no_mt5_runtime_probe(정확한 차단 사유, MT5 런타임 탐침 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__negative_memory_closeout",
            "subrun_id": f"{RUN_ID}__negative_memory_closeout",
            "record_view": "Frontier18 closeout(전선18 마감)",
            "tier_scope": "Tier A proxy plus Tier B missing_required(티어 A 프록시와 티어 B 필수 누락)",
            "kpi_scope": "negative_memory_closeout(부정 기억 마감)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"runtime_blocker={RUNTIME_BLOCKER};no_authority",
        }
    ]


def artifact_registry_row(final: Mapping[str, Any], artifact_type: str, path: Path) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "artifact_type": artifact_type,
        "path": path.as_posix(),
        "sha256": sha256_file(path) if path_exists(path) else "",
        "created_at": final["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "artifact_id": f"{RUN_ID}__{artifact_type}",
        "created_at_utc": final["created_at_utc"],
        "notes": "Frontier18 closeout negative memory(전선18 부정 기억 마감)",
        "artifact_path": path.as_posix(),
        "effect": "negative memory closeout evidence(부정 기억 마감 근거)를 연결합니다.",
    }


def changelog_entry(final: Mapping[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier18(전선18) as negative memory(부정 기억). "
        f"Effect(효과): runtime blocker(런타임 차단 사유) `{RUNTIME_BLOCKER}` recorded and next run(다음 실행) is `{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: Mapping[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: asymmetric exit lifecycle/profit lock(비대칭 청산 생명주기/수익 잠금) closed as negative memory(부정 기억). "
        "Effect(효과): same lifecycle parameter retuning(동일 생명주기 파라미터 재조정)을 반복하지 않습니다.\n"
    )


def negative_register_entry(final: Mapping[str, Any]) -> str:
    return f"""<!-- {RUN_ID} -->
## {RUN_ID} Frontier18 Negative Memory(전선18 부정 기억)

- judgment(판정): `{final['judgment']}`
- negative memory(부정 기억): `{final['negative_memory']}`
- preserved clue(보존 단서): `{final['preserved_clue']}`
- runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`
- best proxy(최선 프록시): {primary_kpi_text(final['best_candidate_row'])}
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
- report(보고서): `{REPORT_PATH.as_posix()}`
"""


def primary_kpi_text(best: Mapping[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"neg_subperiod={fmt(best.get('validation_oos_negative_subperiod_fraction'))};"
        "strict_seed_preserved=0_0_0"
    )


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [dict(row) for row in rows]
    if fieldnames is None:
        columns: list[str] = []
        for row in materialized:
            for key in row:
                if key not in columns:
                    columns.append(key)
        fieldnames = columns
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in materialized:
            writer.writerow({column: stringify(row.get(column, "")) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


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


def upsert_csv_io(path: Path, key: str, row: Mapping[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows.extend(dict(existing) for existing in csv.DictReader(handle))
    normalized = {column: stringify(row.get(column, "")) for column in header}
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
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def append_csv_io(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        return
    header = read_csv_header_io(path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        for row in rows:
            writer.writerow({column: stringify(row.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, Any]:
    return {
        "path": rel(path),
        "exists": path_exists(path),
        "sha256": sha256_file(path) if path_exists(path) else "",
    }


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else str(value)
    return str(value)


def fmt(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return ""
    return f"{number:.6g}"


def rel(path: Path | str) -> str:
    p = Path(path)
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    raise SystemExit(main())
