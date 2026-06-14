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
STAGE_ID = "stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout"
RUN_ID = "frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier17D"
PARENT_RUN_ID = "frontier17C_loss_cluster_firewall_runtime_probe_v1"
SOURCE_PROXY_RUN_ID = "frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1"
NEXT_RUN_ID = "frontier18A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_negative_memory_loss_cluster_firewall_runtime_economics_failed_no_authority"
JUDGMENT = "negative_memory(부정 기억)"
CLAIM_BOUNDARY = (
    "negative_memory_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_ROOT / "03_reviews"
SELECTED_DIR = STAGE_ROOT / "04_selected"
SPEC_DIR = STAGE_ROOT / "00_spec"
F17B_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_PROXY_RUN_ID
F17C_RUN_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
GROK_CLOSEOUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier17_closeout/small_review")

F17B_FINAL = F17B_RUN_ROOT / "final_decision.json"
F17B_REPORT = REVIEW_DIR / f"{SOURCE_PROXY_RUN_ID}_report.md"
F17C_FINAL = F17C_RUN_ROOT / "final_decision.json"
F17C_SUMMARY = F17C_RUN_ROOT / "mt5_runtime_probe_summary.csv"
F17C_SIGNAL_DIFF = F17C_RUN_ROOT / "runtime_signal_expected_vs_mt5_summary.csv"
F17C_REPORT = REVIEW_DIR / f"{PARENT_RUN_ID}_report.md"
GROK_OUTPUT = GROK_CLOSEOUT / "clean_output.md"

REPORT_PATH = REVIEW_DIR / f"{RUN_ID}_report.md"
CLOSEOUT_SUMMARY = RUN_ROOT / "closeout_summary.json"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
DECISION_DOC = Path("docs/decisions") / f"{TODAY}_frontier17d_closeout_negative_memory.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_GATE_AUDIT_MD = REVIEW_DIR / "required_gate_coverage_audit.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
ARTIFACT_REGISTRY = Path("docs/registers/artifact_registry.csv")


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    evidence = load_and_verify_evidence()
    final = build_final(created_at, evidence)
    write_outputs(final, evidence)
    update_docs_and_registers(final, evidence)
    print(json.dumps(json_ready({
        "run_id": RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "negative_memory": final["negative_memory"],
        "preserved_clue": final["preserved_clue"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_LEDGER, f03b.ALPHA_LEDGER)


def load_and_verify_evidence() -> dict[str, Any]:
    f17b = read_json(F17B_FINAL)
    f17c = read_json(F17C_FINAL)
    runtime = pd.read_csv(io_path(F17C_SUMMARY), encoding="utf-8-sig")
    signal_diff = pd.read_csv(io_path(F17C_SIGNAL_DIFF), encoding="utf-8-sig")
    grok_text = read_text(GROK_OUTPUT)

    best = dict(f17b.get("best_candidate_row", {}))
    checks = {
        "f17b_preserved_only": f17b.get("status") == "loss_cluster_firewall_preserved_clue_no_authority",
        "f17c_runtime_completed": f17c.get("status") == "runtime_probe_observation_completed_signal_matched_no_authority",
        "grok_closeout_accepted": "accepted" in grok_text.lower(),
        "runtime_two_rows": len(runtime) == 2,
        "signal_parity_all_matched": bool(signal_diff["usable_for_runtime_signal_parity"].astype(bool).all()),
        "oos_pf_below_one": float(runtime.loc[runtime["split"].astype(str).eq("oos"), "profit_factor"].iloc[0]) < 1.0,
        "max_dd_over_35": float(runtime["max_drawdown_percent"].max()) >= 35.0,
    }
    if not all(checks.values()):
        raise RuntimeError("F17D closeout evidence check failed(F17D 마감 근거 확인 실패): " + json.dumps(checks, ensure_ascii=False))

    return {
        "f17b_final": f17b,
        "f17c_final": f17c,
        "best": best,
        "runtime_rows": runtime.to_dict("records"),
        "signal_diff_rows": signal_diff.to_dict("records"),
        "grok_closeout_classification": "accepted(수용)",
        "checks": checks,
    }


def build_final(created_at: str, evidence: Mapping[str, Any]) -> dict[str, Any]:
    best = dict(evidence["best"])
    runtime_rows = list(evidence["runtime_rows"])
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "best_candidate_row": best,
        "negative_memory": (
            "loss_cluster_firewall_profit_persistence_failed_native_mt5_economics_and_dd"
            "(손실 군집 방화벽 수익 지속 가설은 MT5 실행 경제성과 손실폭에서 실패)"
        ),
        "preserved_clue": (
            "runtime_veto_tape_handoff_preserved_for_future_closed_bar_veto_runtime_probe"
            "(종료봉 차단 런타임 탐침을 위한 런타임 차단 테이프 인계 단서 보존)"
        ),
        "runtime_probe_observation": runtime_observation_text(runtime_rows),
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
            "f17c_runtime_summary": F17C_SUMMARY.as_posix(),
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
            "gate_name": "f17b_proxy_boundary(전선17B 프록시 경계)",
            "status": "passed_preserved_only(보존 단서 전용 통과)",
            "evidence_path": F17B_REPORT.as_posix(),
            "effect": "F17B proxy(프록시)는 preserved clue(보존 단서)였고 authority(권위)는 없었습니다.",
        },
        {
            "gate_name": "f17c_runtime_probe_observation(전선17C 런타임 탐침 관찰)",
            "status": "passed_runtime_completed_signal_matched(런타임 완료 및 신호 일치 통과)",
            "evidence_path": F17C_SUMMARY.as_posix(),
            "effect": "MT5 runtime probe(MT5 런타임 탐침)는 2/2 완료됐고 signal diff(신호 차이)는 0입니다.",
        },
        {
            "gate_name": "economic_failure_judgment(경제성 실패 판정)",
            "status": "failed_goal_axes_recorded(목표 축 실패 기록)",
            "evidence_path": F17C_SUMMARY.as_posix(),
            "effect": "OOS PF 0.92와 DD 47.50%로 completion candidate(완성 후보)가 아님을 기록합니다.",
        },
        {
            "gate_name": "grok_closeout_review(그록 마감 검토)",
            "status": "accepted_with_local_verification(로컬 검증 포함 수용)",
            "evidence_path": GROK_OUTPUT.as_posix(),
            "effect": "Grok(그록)은 추가 repair(수리)보다 negative memory(부정 기억) closeout(마감)을 권했습니다.",
        },
        {
            "gate_name": "claim_boundary_guard(주장 경계 보호)",
            "status": "passed_no_authority_claim(권위 주장 없음 통과)",
            "evidence_path": CLOSEOUT_SUMMARY.as_posix(),
            "effect": "completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 주장하지 않습니다.",
        },
    ]


def run_manifest(final: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]], evidence: Mapping[str, Any]) -> dict[str, Any]:
    output_paths = [REPORT_PATH, CLOSEOUT_SUMMARY, GATE_AUDIT, DECISION_DOC, F17C_SUMMARY, F17C_SIGNAL_DIFF, GROK_OUTPUT]
    return {
        **dict(final),
        "script_path": Path(__file__).as_posix(),
        "script_sha256": sha256_file(Path(__file__)),
        "gate_rows": gate_rows,
        "local_verification": evidence["checks"],
        "artifacts": [artifact_identity(path) for path in output_paths],
    }


def update_docs_and_registers(final: Mapping[str, Any], evidence: Mapping[str, Any]) -> None:
    write_text_sig(REPORT_PATH, report_text(final, evidence))
    write_text_sig(REVIEW_INDEX, review_index_text(final))
    write_text_sig(STAGE_GATE_AUDIT_MD, stage_gate_audit_text(final))
    write_text_sig(SELECTION_STATUS, selection_status_text(final))
    write_text_sig(DECISION_DOC, decision_text(final))
    append_stage_brief(final)
    write_text_sig(f03b.WORKSPACE_STATE, workspace_state_text(final))
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_LEDGER, "ledger_row_id", row)
    append_csv_io(ARTIFACT_REGISTRY, [artifact_registry_row(final, name, path) for name, path in {
        "closeout_summary": CLOSEOUT_SUMMARY,
        "report": REPORT_PATH,
        "run_manifest": RUN_MANIFEST,
        "gate_audit": GATE_AUDIT,
    }.items()])
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(f03b.NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def report_text(final: Mapping[str, Any], evidence: Mapping[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier17D Closeout(전선17D 마감)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): F17B proxy(프록시)와 F17C MT5 runtime probe(MT5 런타임 탐침)를 근거로 Frontier17(전선17)을 negative memory(부정 기억)로 닫았습니다.

Effect(효과): loss-cluster firewall profit persistence(손실 군집 방화벽 수익 지속) 가설은 닫고, RuntimeVetoTape(런타임 차단 테이프) handoff clue(인계 단서)만 보존합니다.

## Evidence(근거)

- best candidate(최선 후보): `{best.get('candidate_id')}`
- F17B proxy validation(검증): PF {fmt(best.get('validation_profit_factor'))}, density(밀도) {fmt(best.get('validation_trades_per_day'))}/day, DD {fmt(best.get('validation_dd_risk_percent'))}%
- F17B proxy OOS(표본밖): PF {fmt(best.get('oos_profit_factor'))}, density(밀도) {fmt(best.get('oos_trades_per_day'))}/day, DD {fmt(best.get('oos_dd_risk_percent'))}%
- F17C runtime observation(런타임 관찰): {final['runtime_probe_observation']}
- Grok closeout(그록 마감): `{final['grok_closeout_classification']}`

## Closeout(마감)

Negative memory(부정 기억): `{final['negative_memory']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier17 Review Index(전선17 검토 색인)

Updated(갱신): {final['created_at_utc']}

Closed run(마감 실행): `{RUN_ID}`

Status(상태): `{final['status']}`

Reports(보고서): `{F17B_REPORT.as_posix()}`, `{F17C_REPORT.as_posix()}`, `{REPORT_PATH.as_posix()}`
"""


def stage_gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier17 Required Gate Coverage Audit(전선17 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

## Covered Gates(충족한 게이트)

- Grok closeout review(그록 마감 검토): `accepted(수용)`, evidence(근거) `{GROK_OUTPUT.as_posix()}`
- proxy boundary(프록시 경계): F17B preserved clue only(보존 단서 전용), evidence(근거) `{F17B_REPORT.as_posix()}`
- MT5 runtime probe(런타임 탐침): F17C completed 2/2 and signal diff 0(2/2 완료 및 신호 차이 0), evidence(근거) `{F17C_SUMMARY.as_posix()}`
- result judgment(결과 판정): negative memory(부정 기억), evidence(근거) `{REPORT_PATH.as_posix()}`
- claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) not_claimed(주장 없음)

## Missing By Scope(범위상 누락)

- Tier B separate(티어 B 분리): missing_required(필수 누락)
- Tier A+B combined(티어 A+B 합산): missing_required(필수 누락)
- WFO/stress(워크포워드/스트레스): not_run_by_closeout(마감 판단상 미실행)

Effect(효과): Frontier17(전선17)은 runtime handoff clue(런타임 인계 단서)를 보존하지만 alpha hypothesis(알파 가설)는 MT5 economics/DD(MT5 경제성/손실폭) 실패로 닫습니다.
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier17 Selection Status(전선17 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Closeout(마감): `{final['judgment']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Next action(다음 행동): `{final['next_run_id']}`
"""


def decision_text(final: Mapping[str, Any]) -> str:
    return f"""# Decision: Frontier17 Closeout(결정: 전선17 마감)

Date(날짜): {final['created_at_utc']}

Decision(결정): `{final['status']}`

Action(행동): Frontier17(전선17)을 negative memory(부정 기억)로 닫았습니다.

Effect(효과): runtime handoff clue(런타임 인계 단서)는 보존하고 alpha hypothesis(알파 가설)는 MT5 economics/DD(MT5 경제성/손실폭) 실패로 넘기지 않습니다.

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

## Frontier17D Closeout(전선17D 마감)

Updated(갱신): {final['created_at_utc']}

Action(행동): F17(전선17)을 negative memory(부정 기억)로 닫았습니다.

Effect(효과): runtime veto tape handoff(런타임 차단 테이프 인계)는 보존하고, loss-cluster firewall alpha(손실 군집 방화벽 알파)는 MT5 PF/DD 실패로 반복하지 않습니다.
"""
    write_text_sig(STAGE_BRIEF, text)


def workspace_state_text(final: Mapping[str, Any]) -> str:
    return "\n".join([
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
    ])


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

Action(행동): Frontier17(전선17)은 negative memory(부정 기억)로 닫혔습니다.

Effect(효과): MT5 runtime probe(런타임 탐침)는 stage(단계) 안에서 완료됐고, 다음 frontier(전선)는 새 hypothesis(가설)로 시작해야 합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": final["runtime_probe_observation"],
        "family": "result_judgment(결과 판정)",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "attempt_count": 1,
        "runtime_completed_rows": 2,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": final["runtime_probe_observation"],
        "external_verification_status": "mt5_runtime_probe_completed(MT5 런타임 탐침 완료)",
        "result_path": REPORT_PATH.as_posix(),
        "gate_audit_path": GATE_AUDIT.as_posix(),
    }


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_authority_no_goal_claim(권위/목표 주장 없음)",
        "external_verification_status": "mt5_runtime_probe_completed(MT5 런타임 탐침 완료)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__negative_memory_closeout",
            "subrun_id": f"{RUN_ID}__negative_memory_closeout",
            "record_view": "Frontier17 closeout(전선17 마감)",
            "tier_scope": "Tier A runtime plus Tier B missing_required(티어 A 런타임 및 티어 B 필수 누락)",
            "kpi_scope": "negative_memory_closeout(부정 기억 마감)",
            "primary_kpi": final["runtime_probe_observation"],
            "notes": "F17C signal parity matched but MT5 economics/DD failed(F17C 신호 동등성은 일치했지만 MT5 경제성/손실폭 실패)",
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
        "notes": "Frontier17 closeout negative memory(전선17 부정 기억 마감)",
        "artifact_path": path.as_posix(),
        "effect": "negative memory closeout evidence(부정 기억 마감 근거)를 연결합니다.",
    }


def changelog_entry(final: Mapping[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier17(전선17) as negative memory(부정 기억). "
        f"Effect(효과): runtime handoff clue(런타임 인계 단서)는 보존하고 next run(다음 실행)은 `{NEXT_RUN_ID}`입니다.\n"
    )


def idea_registry_entry(final: Mapping[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: loss-cluster firewall profit persistence(손실 군집 방화벽 수익 지속) closed as negative memory(부정 기억). "
        "Effect(효과): native MT5 economics/DD(MT5 실행 경제성/손실폭) 실패를 반복 금지 단서로 남깁니다.\n"
    )


def negative_register_entry(final: Mapping[str, Any]) -> str:
    return f"""<!-- {RUN_ID} -->
## {RUN_ID} Frontier17 Negative Memory(전선17 부정 기억)

- judgment(판정): `{final['judgment']}`
- negative memory(부정 기억): `{final['negative_memory']}`
- preserved clue(보존 단서): `{final['preserved_clue']}`
- runtime observation(런타임 관찰): {final['runtime_probe_observation']}
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
- report(보고서): `{REPORT_PATH.as_posix()}`
"""


def runtime_observation_text(rows: Sequence[Mapping[str, Any]]) -> str:
    parts = []
    for row in rows:
        parts.append(
            f"{row.get('split')}: PF={fmt(row.get('profit_factor'))}, DD={fmt(row.get('max_drawdown_percent'))}%, "
            f"trades={fmt(row.get('trade_count'))}, signal_diff={row.get('signal_count_diff')}"
        )
    return " | ".join(parts)


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
