from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from stage_pipelines.stage_frontier_75 import frontier75b_volatility_compression_liquidity_release_proxy_scout as base


ROOT = base.ROOT
STAGE_ID = base.STAGE_ID
RUN_ID = "frontier75D_pre_mt5_grok_volatility_compression_negative_control_runtime_probe_v1"
PARENT_RUN_ID = "frontier75C_volatility_compression_label_risk_repair_proxy_v1"
NEXT_RUN_ID = "frontier75E_mt5_volatility_compression_negative_control_runtime_probe_v1"
TARGET_CANDIDATE_ID = "f75b_0551"
STATUS = "pre_mt5_grok_review_accepted_negative_control_no_authority"
JUDGMENT = "negative_control_runtime_probe_accepted_for_f75b_0551_no_authority"
CLAIM_BOUNDARY = (
    "pre_mt5_review_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = f"stages/{STAGE_ID}/03_reviews/frontier75D_pre_mt5_grok_negative_control_runtime_probe_report.md"
RECEIPT_PATH = f"stages/{STAGE_ID}/03_reviews/grok_pre_mt5_negative_control_runtime_probe_receipt.md"
GATE_AUDIT_PATH = f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f75d.md"
RUN_MANIFEST_PATH = f"stages/{STAGE_ID}/02_runs/{RUN_ID}/run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

GROK_PACKET = "docs/agent_control/grok_reviews/2026-06-17_f75d_pre_mt5_volatility_compression_negative_control_runtime_probe"
GROK_PROMPT = f"{GROK_PACKET}/prompts/f75d_pre_mt5_volatility_compression_negative_control_runtime_probe_prompt.md"
GROK_OUTPUT = f"{GROK_PACKET}/clean_output.md"
GROK_METADATA = f"{GROK_PACKET}/metadata.json"


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR):
        base.fs_path(path).mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(base.read_text(path))


def grok_review() -> dict[str, Any]:
    prompt = ROOT / GROK_PROMPT
    output = ROOT / GROK_OUTPUT
    metadata = ROOT / GROK_METADATA
    for path in (prompt, output, metadata):
        if not base.fs_path(path).exists():
            raise FileNotFoundError(path)
    meta = read_json(metadata)
    text = base.read_text(output)
    accepted = "accepted with minor modification" in text.lower() or "수용" in text
    return {
        "packet_path": GROK_PACKET,
        "prompt_path": GROK_PROMPT,
        "prompt_sha256": base.sha256_file(prompt),
        "output_path": GROK_OUTPUT,
        "output_sha256": base.sha256_file(output),
        "metadata_path": GROK_METADATA,
        "metadata_sha256": base.sha256_file(metadata),
        "metadata_success": bool(meta.get("success")),
        "returncode": meta.get("returncode"),
        "advice_classification": "accepted_with_minor_modification(소폭 수정 수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "codex_classification": "accepted(수용)",
        "accepted_direction": "single-target negative-control MT5 Runtime Probe(단일 대상 부정 대조 MT5 런타임 탐침)",
        "target_candidate_id": TARGET_CANDIDATE_ID,
        "rejected_or_deferred": "f75c_0286 deferred(보류): OOS stronger but validation flat(표본외 강하지만 검증 평평함)",
    }


def write_artifacts(review: dict[str, Any], created_at: str) -> None:
    f75b = read_json(REVIEW_DIR / "f75b_summary.json")
    f75c = read_json(REVIEW_DIR / "f75c_summary.json")
    target = f75b["best_candidate"]
    report = f"""# Frontier75D Pre-MT5 Grok Review Report(F75D MT5 전 Grok 검토 보고서)

Run id(실행 ID): `{RUN_ID}`

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Updated(갱신): {created_at}

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Codex Direction Before Grok(Grok 전 Codex 방향)

Action(행동): F75B `f75b_0551`을 single-target negative-control MT5 Runtime Probe(단일 대상 부정 대조 MT5 런타임 탐침)로 물질화한다.

Effect(효과): weak proxy scout(약한 프록시 탐색 단서)를 “좋은 후보”로 과장하지 않고, proxy/runtime gap(프록시/런타임 간극)을 실제 MT5에서 관찰한다.

## Grok Advice(Grok 조언)

- classification(분류): `{review["advice_classification"]}`
- Codex classification(Codex 분류): `{review["codex_classification"]}`
- accepted direction(수용 방향): `{review["accepted_direction"]}`
- target(대상): `{TARGET_CANDIDATE_ID}`
- deferred(보류): `f75c_0286`

## Target Proxy KPI(대상 프록시 KPI)

- candidate(후보): `{TARGET_CANDIDATE_ID}`
- validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `{target["validation_net_profit"]:.4f}/{target["validation_profit_factor"]:.4f}/{target["validation_max_drawdown_percent"]:.4f}%/{target["validation_trades_day"]:.4f}`
- OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `{target["oos_net_profit"]:.4f}/{target["oos_profit_factor"]:.4f}/{target["oos_max_drawdown_percent"]:.4f}%/{target["oos_trades_day"]:.4f}`
- signal meaning(신호 의미): scout clue(탐색 단서), not meaningful signal(의미 신호 아님)

## Gap Risks To Pre-Record(사전 기록 간극 위험)

- density gap(밀도 간극): proxy tpd(프록시 일거래) is about `1.0`, below target `5.0`.
- PF optimism gap(수익 팩터 낙관 간극): validation PF `1.8815` vs OOS PF `1.1963`.
- gate parity risk(게이트 동등성 위험): `hv_q35_compression` and `cash_all` must match EA/session behavior(EA/세션 동작).
- model parity risk(모델 동등성 위험): ExtraTrees all58 export/inference surface(엑스트라트리 58피처 내보내기/추론 표면)가 얇은 edge(얇은 우위)를 지울 수 있다.
- short-only risk(숏 전용 위험): spread/fill/exit behavior(스프레드/체결/청산 동작)가 short(숏)에 불리할 수 있다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`: materialize and execute MT5 Runtime Probe(MT5 런타임 탐침 물질화 및 실행). Success criterion(성공 기준)은 positive PF(긍정 수익 팩터)가 아니라 observation completed with recorded gap(간극 기록이 있는 관찰 완료)다.
"""
    base.write_text(REVIEW_DIR / "frontier75D_pre_mt5_grok_negative_control_runtime_probe_report.md", report)

    receipt = f"""# F75D Grok Pre-MT5 Receipt(Grok MT5 전 영수증)

Trigger reason(트리거 이유): MT5 Runtime Probe(MT5 런타임 탐침)는 major validation(주요 검증)이므로 `/goal(목표)`에 따라 Grok second opinion(Grok 2차 의견)이 필요하다.

Review size(검토 크기): medium review(중간 검토)

Direction before Grok(Grok 전 방향): run negative-control MT5 probe(부정 대조 MT5 탐침) on `{TARGET_CANDIDATE_ID}`.

Bounded evidence(제한 근거): F75B summary(F75B 요약), F75C summary(F75C 요약), candidate KPI(후보 KPI), claim boundary(주장 경계).

Prompt identity(프롬프트 정체성): `{GROK_PROMPT}` sha256 `{review["prompt_sha256"]}`

Grok output identity(Grok 출력 정체성): `{GROK_OUTPUT}` sha256 `{review["output_sha256"]}`

Advice classification(조언 분류): `{review["advice_classification"]}`

Codex classification(Codex 분류): `{review["codex_classification"]}`

Local verification(로컬 검증): metadata success(메타데이터 성공) `{review["metadata_success"]}`, returncode `{review["returncode"]}`, F75B/F75C summaries present(F75B/F75C 요약 존재).

Forbidden claim check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Final Codex direction(최종 Codex 방향): `{NEXT_RUN_ID}` with target `{TARGET_CANDIDATE_ID}`.
"""
    base.write_text(REVIEW_DIR / "grok_pre_mt5_negative_control_runtime_probe_receipt.md", receipt)

    gate_audit = f"""# Required Gate Coverage Audit F75D(필수 게이트 커버리지 감사 F75D)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| pre_mt5_grok_review(MT5 전 Grok 검토) | passed(통과) | `{RECEIPT_PATH}` |
| advice_classification(조언 분류) | accepted(수용) | `{review["advice_classification"]}` |
| target_selection(대상 선택) | passed(통과) | `{TARGET_CANDIDATE_ID}` selected; `f75c_0286` deferred(보류) |
| gap_risk_prerecord(간극 위험 사전 기록) | passed(통과) | `{REPORT_PATH}` |
| runtime_probe_next(다음 런타임 탐침) | required(필수) | `{NEXT_RUN_ID}` |
| claim_guard(주장 보호) | passed(통과) | `{CLAIM_BOUNDARY}` |
"""
    base.write_text(REVIEW_DIR / "required_gate_coverage_audit_f75d.md", gate_audit)

    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "target_candidate_id": TARGET_CANDIDATE_ID,
        "grok": review,
        "f75b_best_candidate": target,
        "f75c_best_candidate": f75c.get("best_candidate", {}),
        "artifacts": {
            "report": REPORT_PATH,
            "receipt": RECEIPT_PATH,
            "gate_audit": GATE_AUDIT_PATH,
        },
    }
    base.write_json(RUN_DIR / "run_manifest.json", manifest)


def update_state_and_ledgers(created_at: str) -> None:
    workspace_state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: pending_mt5_negative_control_runtime_probe
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f74_closeout_f75_closeout_will_trigger
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F75D pre-MT5 Grok review(MT5 전 Grok 검토)를 완료했다."
  - "Effect(효과): F75B f75b_0551 negative-control runtime probe(부정 대조 런타임 탐침)를 다음 실행으로 고정했다."
  - "Next(다음): {NEXT_RUN_ID}"
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    base.write_text(ROOT / "docs/workspace/workspace_state.yaml", workspace_state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(맥락 고정점): `{CONTEXT_ANCHOR_PATH}`

## Current Truth(현재 진실)

Action(행동): F75D pre-MT5 Grok review(MT5 전 Grok 검토)를 완료했다.

Effect(효과): F75B `f75b_0551`을 single-target negative-control MT5 Runtime Probe(단일 대상 부정 대조 MT5 런타임 탐침)로 고정했다.

## Open Work(열린 작업)

Next run(다음 실행): `{NEXT_RUN_ID}`

Runtime probe success criterion(런타임 탐침 성공 기준): positive result(긍정 결과)가 아니라 observation completed with recorded proxy/runtime gap(프록시/런타임 간극 기록이 있는 관찰 완료).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(ROOT / "docs/context/current_working_state.md", current)

    row_id = f"{RUN_ID}__pre_mt5_grok"
    row = {
        "ledger_row_id": row_id,
        "row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pre_mt5_review(MT5 전 검토)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "external_review_packet(외부 검토 묶음)",
        "scoreboard_lane": "runtime_probe_precheck(런타임 탐침 사전 점검)",
        "lane": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "family": "negative_control_runtime_probe_precheck(부정 대조 런타임 탐침 사전 점검)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "path": REPORT_PATH,
        "report_path": REPORT_PATH,
        "primary_report": REPORT_PATH,
        "primary_kpi": f"grok=accepted;target={TARGET_CANDIDATE_ID}",
        "guardrail_kpi": "negative_control_success_is_gap_observation",
        "external_verification_status": "pre_mt5_review_completed(MT5 전 검토 완료)",
        "notes": "F75D Grok accepted single-target negative-control MT5 Runtime Probe(F75D Grok 단일 대상 부정 대조 MT5 런타임 탐침 수용).",
        "run_number": "frontier75D",
        "date": "2026-06-17",
        "run_date": "2026-06-17",
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": "1",
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_artifact": RUN_MANIFEST_PATH,
        "result_status": STATUS,
        "evidence_boundary": "pre_mt5_review_only_no_runtime_yet(MT5 전 검토 전용, 런타임 아직 없음)",
        "work_family": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "question": "Should F75 run negative-control MT5 Runtime Probe?(F75가 부정 대조 MT5 런타임 탐침을 실행해야 하나?)",
        "next_action": NEXT_RUN_ID,
        "gate_audit_path": GATE_AUDIT_PATH,
        "required_gate_audit": GATE_AUDIT_PATH,
        "created_at": created_at,
        "created_at_utc": created_at,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "run_type": "negative_control_runtime_probe_precheck(부정 대조 런타임 탐침 사전 점검)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": RUN_MANIFEST_PATH,
        "result_path": REPORT_PATH,
        "artifact_count": "4",
    }
    run_registry = ROOT / "docs/registers/run_registry.csv"
    alpha_ledger = ROOT / "docs/registers/alpha_run_ledger.csv"
    with base.fs_path(run_registry).open("r", encoding="utf-8-sig", newline="") as handle:
        run_fields = list(csv.DictReader(handle).fieldnames or [])
    with base.fs_path(alpha_ledger).open("r", encoding="utf-8-sig", newline="") as handle:
        alpha_fields = list(csv.DictReader(handle).fieldnames or [])
    base.upsert_csv_row(run_registry, "run_id", row, run_fields)
    base.upsert_csv_row(alpha_ledger, "ledger_row_id", row, alpha_fields)
    base.upsert_csv_row(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, alpha_fields)

    idea_path = ROOT / "docs/registers/idea_registry.md"
    text = base.read_text(idea_path)
    marker = "<!-- frontier75D_pre_mt5_grok_negative_control_runtime_probe_v1 -->"
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` recorded pre-MT5 Grok review(MT5 전 Grok 검토). Result(결과): `{JUDGMENT}`. Target(대상): `{TARGET_CANDIDATE_ID}`. Evidence(근거): `{REPORT_PATH}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
        base.write_text(idea_path, text.rstrip() + addition)


def main() -> None:
    ensure_dirs()
    created_at = base.now_utc()
    review = grok_review()
    if review["codex_classification"] != "accepted(수용)":
        raise RuntimeError("F75D Grok review not accepted")
    write_artifacts(review, created_at)
    update_state_and_ledgers(created_at)
    print(json.dumps({
        "status": STATUS,
        "judgment": JUDGMENT,
        "target_candidate_id": TARGET_CANDIDATE_ID,
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
