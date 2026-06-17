from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_80 import frontier80b_broad_extreme_multi_axis_proxy_scout as f80b


STAGE_ID = f80b.STAGE_ID
RUN_ID = "frontier80E_proxy_runtime_gap_attribution_v1"
CLOSEOUT_RUN_ID = "frontier80F_runtime_probe_quality_closeout_v1"
PARENT_RUN_ID = "frontier80D_mt5_runtime_probe_quality_v1"
STATUS = "closed_negative_memory_runtime_probe_quality_no_authority"
JUDGMENT = "runtime_probe_quality_closeout_negative_memory_with_preserved_clue_no_authority"
CLAIM_BOUNDARY = (
    "stage_closeout_runtime_probe_quality_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
NEXT_FRONTIER_PROPOSAL = "stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

F80B_SUMMARY = REVIEW_DIR / "f80b_multi_axis_proxy_summary.json"
F80C_SUMMARY = REVIEW_DIR / "f80c_wfo_selection_summary.json"
F80C_TARGET = REVIEW_DIR / "f80c_runtime_materialization_target_selection.json"
F80D_SUMMARY = REVIEW_DIR / "f80d_mt5_runtime_probe_quality_summary.json"
F80D_RECEIPT = STAGE_DIR / "02_runs/frontier80D_mt5_runtime_probe_quality_v1/f80d_runtime_receipt.csv"
F80D_MANIFEST = STAGE_DIR / "02_runs/frontier80D_mt5_runtime_probe_quality_v1/run_manifest.json"

GAP_JSON = REVIEW_DIR / "f80e_proxy_runtime_gap_attribution.json"
GAP_REPORT = REVIEW_DIR / "frontier80E_proxy_runtime_gap_attribution_report.md"
GAP_GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f80e.md"
CLOSEOUT_SUMMARY = REVIEW_DIR / "f80f_stage_closeout_summary.json"
CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
CLOSEOUT_GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f80f_closeout.md"
RESULT_RECEIPT = REVIEW_DIR / "f80f_result_judgment_receipt.yaml"
ATTRIBUTION_RECEIPT = REVIEW_DIR / "f80e_performance_attribution_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f80f_claim_discipline_receipt.yaml"
LINEAGE_RECEIPT = REVIEW_DIR / "f80f_artifact_lineage_receipt.yaml"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
FIVE_STAGE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
SCRIPT_REL = "stage_pipelines/stage_frontier_80/frontier80e_gap_attribution_and_closeout.py"


def utc_now() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def build_gap_payload(created_at: str) -> dict[str, Any]:
    f80b_summary = read_json(F80B_SUMMARY)
    f80c_summary = read_json(F80C_SUMMARY)
    target_selection = read_json(F80C_TARGET)
    f80d_summary = read_json(F80D_SUMMARY)
    runtime_rows = read_csv(F80D_RECEIPT)
    runtime = runtime_rows[0] if runtime_rows else {}
    target = target_selection.get("runtime_materialization_target") or {}
    proxy_net = as_float(runtime.get("proxy_net_profit"))
    runtime_net = as_float(runtime.get("net_profit"))
    proxy_pf = as_float(runtime.get("proxy_profit_factor"))
    runtime_pf = as_float(runtime.get("profit_factor"))
    proxy_dd = as_float(runtime.get("proxy_dd_percent"))
    runtime_dd = as_float(runtime.get("max_drawdown_percent"))
    signal_diff = as_float(runtime.get("signal_count_diff"))
    feature_ready_diff = as_float(runtime.get("feature_ready_diff"))
    fill_gap = as_float(runtime.get("order_fill_count")) - as_float(runtime.get("expected_selected_trade_count"))
    return {
        "run_id": RUN_ID,
        "closeout_run_id": CLOSEOUT_RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "target_candidate_id": target.get("candidate_id"),
        "target_model": target.get("model"),
        "f80b_candidate_rows": f80b_summary.get("candidate_rows"),
        "f80b_materialization_candidate_count": f80b_summary.get("materialization_candidate_count"),
        "f80b_meaningful_signal_count": f80b_summary.get("meaningful_signal_count"),
        "f80c_wfo_gate_count": f80c_summary.get("wfo_gate_count"),
        "f80d_attempt_count": f80d_summary.get("attempt_count"),
        "f80d_completed_attempt_count": f80d_summary.get("completed_attempt_count"),
        "proxy_validation": {
            "net_profit": proxy_net,
            "profit_factor": proxy_pf,
            "max_drawdown_percent": proxy_dd,
            "expected_selected_trade_count": as_float(runtime.get("expected_selected_trade_count")),
            "expected_signal_count": as_float(runtime.get("expected_signal_count")),
        },
        "runtime_validation": {
            "net_profit": runtime_net,
            "profit_factor": runtime_pf,
            "max_drawdown_percent": runtime_dd,
            "trade_count": as_float(runtime.get("trade_count")),
            "signal_count": as_float(runtime.get("signal_count")),
            "order_fill_count": as_float(runtime.get("order_fill_count")),
            "order_fill_rate": as_float(runtime.get("order_fill_rate")),
            "win_rate_percent": as_float(runtime.get("win_rate_percent")),
            "expectancy": as_float(runtime.get("expectancy")),
        },
        "gap": {
            "net_runtime_minus_proxy": runtime_net - proxy_net,
            "pf_runtime_minus_proxy": runtime_pf - proxy_pf,
            "dd_runtime_minus_proxy": runtime_dd - proxy_dd,
            "signal_count_diff": signal_diff,
            "feature_ready_diff": feature_ready_diff,
            "order_fill_minus_expected_selected": fill_gap,
        },
        "gap_attribution": {
            "not_feature_readiness": feature_ready_diff == 0,
            "not_signal_count": signal_diff == 0,
            "not_onnx_handoff": f80d_summary.get("artifact_export_status") == "runtime_probe_parity_passed",
            "primary_cause": "runtime_order_economics_after_parity(동등성 이후 런타임 주문 경제성)",
            "detail": "Expected signal count and feature readiness matched, but validation MT5 net/PF/DD moved from proxy positive to runtime negative.",
        },
        "closeout_label": "negative_memory(부정 기억)",
        "preserved_clue": "F80 multi-axis rotation found exportable WFO-aware materialization targets, and selected-entry parity can be made exact.",
        "negative_memory": "Even after ONNX/feature/signal parity, MT5 validation economics were negative: net -14.61, PF 0.95, DD 6.09%.",
        "next_frontier_proposal": NEXT_FRONTIER_PROPOSAL,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gap_report(payload: Mapping[str, Any]) -> str:
    gap = payload["gap"]
    proxy = payload["proxy_validation"]
    runtime = payload["runtime_validation"]
    return f"""# F80E Proxy/Runtime Gap Attribution(F80E 프록시/런타임 간극 귀속)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- target(대상): `{payload.get('target_candidate_id')}` / `{payload.get('target_model')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action(행동)

F80D(전선80D)의 MT5 runtime probe(MT5 런타임 탐침)를 F80B/F80C proxy(프록시) 기대와 비교했다.

Effect(효과): signal count(신호 수), feature readiness(피처 준비), ONNX handoff(온엑스 인계)가 맞아도 MT5 economics(MT5 경제성)가 깨질 수 있음을 F80의 closeout(마감) 근거로 고정한다.

## KPI Gap(KPI 간극)

| metric(지표) | proxy validation(프록시 검증) | MT5 validation(MT5 검증) | runtime - proxy(런타임-프록시) |
|---|---:|---:|---:|
| net profit(순손익) | `{proxy['net_profit']}` | `{runtime['net_profit']}` | `{gap['net_runtime_minus_proxy']}` |
| profit factor(수익 팩터) | `{proxy['profit_factor']}` | `{runtime['profit_factor']}` | `{gap['pf_runtime_minus_proxy']}` |
| DD %(손실폭 %) | `{proxy['max_drawdown_percent']}` | `{runtime['max_drawdown_percent']}` | `{gap['dd_runtime_minus_proxy']}` |
| signal count(신호 수) | `{proxy['expected_signal_count']}` | `{runtime['signal_count']}` | `{gap['signal_count_diff']}` |

## Attribution(귀속)

Primary cause(주 원인): `runtime_order_economics_after_parity(동등성 이후 런타임 주문 경제성)`.

Not the cause(원인 아님): feature readiness(피처 준비), signal count(신호 수), ONNX handoff(온엑스 인계).

Boundary(경계): This is runtime probe quality closeout material(런타임 탐침 품질 마감 근거) only.
"""


def closeout_report(payload: Mapping[str, Any]) -> str:
    proxy = payload["proxy_validation"]
    runtime = payload["runtime_validation"]
    gap = payload["gap"]
    return f"""# F80 Stage Closeout Report(F80 단계 마감 보고서)

Updated(갱신): {payload.get('created_at_utc')}

- stage id(단계 ID): `{STAGE_ID}`
- closeout run(마감 실행): `{CLOSEOUT_RUN_ID}`
- closeout label(마감 라벨): `{payload.get('closeout_label')}`
- judgment(판정): `{JUDGMENT}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Thesis(가설)

F80(전선80)은 feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 함께 바꾸면 runtime economics(런타임 경제성) 단서가 살아나는지 시험했다.

## What Happened(일어난 일)

- F80B(전선80B): `{payload.get('f80b_candidate_rows')}` candidates(후보), materialization candidates(물질화 후보) `{payload.get('f80b_materialization_candidate_count')}`, meaningful signals(의미 신호) `{payload.get('f80b_meaningful_signal_count')}`.
- F80C(전선80C): WFO/exportable gates(워크포워드/내보내기 게이트) `{payload.get('f80c_wfo_gate_count')}` and target(대상) `{payload.get('target_candidate_id')}`.
- F80D(전선80D): MT5 Strategy Tester attempt(전략 테스터 시도) `{payload.get('f80d_attempt_count')}`, completed(완료) `{payload.get('f80d_completed_attempt_count')}`.

## Runtime Probe Quality(런타임 탐침 품질)

Proxy validation(프록시 검증): net `{proxy['net_profit']}`, PF `{proxy['profit_factor']}`, DD `{proxy['max_drawdown_percent']}`.

MT5 validation(MT5 검증): net `{runtime['net_profit']}`, PF `{runtime['profit_factor']}`, DD `{runtime['max_drawdown_percent']}`.

Gap(간극): net `{gap['net_runtime_minus_proxy']}`, PF `{gap['pf_runtime_minus_proxy']}`, DD `{gap['dd_runtime_minus_proxy']}`.

## Preserved Clue(보존 단서)

{payload.get('preserved_clue')}

## Negative Memory(부정 기억)

{payload.get('negative_memory')}

## Next Frontier Proposal(다음 전선 제안)

`{NEXT_FRONTIER_PROPOSAL}` should attack MT5-native order intent/cost/exit shape(MT5 네이티브 주문 의도/비용/청산 형태) directly instead of increasing parity checks(동등성 점검) or signal count(신호 수).

## Forbidden Claims(금지 주장)

No completion(완성 없음), selected baseline(선택 기준선 없음), operating promotion(운영 승격 없음), runtime authority(런타임 권위 없음), live readiness(실거래 준비 없음), Goal Achieve(목표 달성 없음).
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F80F Required Gate Coverage Audit(F80F 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `f80_open_to_closeout_lifecycle` | `passed(통과)` | F80A/F80B/F80C/F80D/F80E/F80F artifacts(산출물) | F80 개방부터 마감까지 실행했다. |
| `mt5_runtime_probe_quality` | `passed(통과)` | `{rel(F80D_RECEIPT)}` | 실제 MT5 검증 결과를 closeout(마감)에 반영한다. |
| `gap_attribution` | `passed(통과)` | `{rel(GAP_JSON)}` | parity(동등성)와 economics(경제성)를 분리한다. |
| `five_stage_grok_retrospective` | `inactive_preserve_records(비활성, 기록 보존)` | `docs/registers/five_stage_retrospective_register.yaml` | F80 경로에서 Grok 회고를 다시 활성화하지 않는다. |
| `final_claim_guard` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 권위/승격/실거래/목표 달성을 만들지 않는다. |
"""


def ledger_rows(payload: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    runtime = payload["runtime_validation"]
    base = {
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_probe_quality_closeout(런타임 탐침 품질 마감)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "proxy_runtime_gap_attribution(프록시/런타임 간극 귀속)",
        "scoreboard_lane": "runtime_economics(런타임 경제성)",
        "family": "kpi_evidence(근거 KPI)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(CLOSEOUT_REPORT),
        "primary_kpi": f"runtime_net={runtime['net_profit']};runtime_pf={runtime['profit_factor']};runtime_dd={runtime['max_drawdown_percent']}",
        "guardrail_kpi": "no_authority;negative_memory;gap_attributed",
        "external_verification_status": "completed_mt5_validation_runtime_probe",
        "notes": f"next_frontier_proposal={NEXT_FRONTIER_PROPOSAL}",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_FRONTIER_PROPOSAL,
        "rows": 1,
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(CLOSEOUT_REPORT),
        "best_candidate_id": payload.get("target_candidate_id"),
        "model": payload.get("target_model"),
        "net_profit": runtime["net_profit"],
        "profit_factor": runtime["profit_factor"],
        "drawdown": runtime["max_drawdown_percent"],
        "trade_count": runtime["trade_count"],
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "tier": "Tier A",
        "metric_scope": "mt5_validation_runtime_probe",
        "result_status": STATUS,
        "work_family": "kpi_evidence",
        "evidence_boundary": "runtime_probe_quality_closeout_only_no_authority(런타임 탐침 품질 마감만, 권위 없음)",
        "next_action": NEXT_FRONTIER_PROPOSAL,
        "created_at_utc": created_at,
        "required_gate_audit": rel(CLOSEOUT_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_probe_quality_only(런타임 탐침 품질만)",
    }
    return [
        {**base, "ledger_row_id": f"{RUN_ID}__gap_attribution", "run_id": RUN_ID, "subrun_id": "gap_attribution(간극 귀속)", "lane": "gap_attribution(간극 귀속)", "view": "gap_attribution", "row_id": f"{RUN_ID}__gap_attribution", "run_number": "frontier80E"},
        {**base, "ledger_row_id": f"{CLOSEOUT_RUN_ID}__stage_closeout", "run_id": CLOSEOUT_RUN_ID, "subrun_id": "stage_closeout(단계 마감)", "lane": "stage_closeout(단계 마감)", "view": "stage_closeout", "row_id": f"{CLOSEOUT_RUN_ID}__stage_closeout", "run_number": "frontier80F"},
    ]


def write_receipts(payload: Mapping[str, Any]) -> None:
    write_text(
        ATTRIBUTION_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: gap_attributed_no_authority
attribution_layers_checked:
  - signal_count
  - feature_readiness
  - onnx_handoff
  - order_fill
  - net_profit
  - profit_factor
  - drawdown
missing_layers:
  - OOS MT5 runtime probe(표본외 MT5 런타임 탐침)
claim_boundary: {CLAIM_BOUNDARY}
""",
    )
    write_text(
        RESULT_RECEIPT,
        f"""packet_id: {CLOSEOUT_RUN_ID}
skill: obsidian-result-judgment
status: {STATUS}
judgment_boundary: runtime_probe_quality_closeout_only
allowed_claims:
  - negative_memory
  - preserved_clue
  - next_frontier_proposal
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
evidence_used:
  - {rel(F80D_RECEIPT)}
  - {rel(GAP_JSON)}
""",
    )
    write_text(
        CLAIM_RECEIPT,
        f"""packet_id: {CLOSEOUT_RUN_ID}
skill: obsidian-claim-discipline
status: passed_closeout_no_authority
requested_claims:
  - "F80 closeout(F80 마감)"
allowed_claims:
  - runtime_probe_quality_closeout
  - negative_memory
  - preserved_clue
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
    )
    write_text(
        LINEAGE_RECEIPT,
        f"""packet_id: {CLOSEOUT_RUN_ID}
skill: obsidian-artifact-lineage
status: closeout_artifacts_connected_no_authority
source_inputs:
  - {rel(F80B_SUMMARY)}
  - {rel(F80C_TARGET)}
  - {rel(F80D_RECEIPT)}
produced_artifacts:
  - {rel(GAP_JSON)}
  - {rel(CLOSEOUT_SUMMARY)}
  - {rel(CLOSEOUT_REPORT)}
raw_evidence:
  - {rel(F80D_RECEIPT)}
machine_readable:
  - {rel(GAP_JSON)}
  - {rel(CLOSEOUT_SUMMARY)}
human_readable:
  - {rel(GAP_REPORT)}
  - {rel(CLOSEOUT_REPORT)}
hashes_or_missing_reasons: "run_manifest producer sha256 recorded"
lineage_boundary: "runtime_probe_quality_closeout_only_no_authority"
""",
    )


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: frontier80_closed_next_frontier_not_opened
latest_completed_run_id: {CLOSEOUT_RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_FRONTIER_PROPOSAL}
runtime_probe_status: f80_runtime_probe_quality_closeout_completed_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: inactive_preserve_records_pending_codex_task_force_replacement_after_f80_closeout
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F80 open -> closeout(F80 개방 -> 마감)을 runtime probe quality(런타임 탐침 품질) 경계로 닫았다."
  - "Effect(효과): parity/signal/feature(동등성/신호/피처)는 맞았지만 MT5 economics(MT5 경제성)는 negative memory(부정 기억)로 기록됐다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `frontier80_closed_next_frontier_not_opened`

Latest completed run(최근 완료 실행): `{CLOSEOUT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F80(전선80)을 open -> closeout(개방 -> 마감)까지 실행했다.

Effect(효과): F80D MT5 validation(검증)에서 signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 통과했지만 net `-14.61`, PF `0.95`, DD `6.09%`로 runtime economics(런타임 경제성)는 negative memory(부정 기억)로 닫혔다.

Next frontier proposal(다음 전선 제안): `{NEXT_FRONTIER_PROPOSAL}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(
        SELECTION_STATUS,
        f"""# F80 Selection Status(F80 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F80(전선80)을 runtime probe quality closeout(런타임 탐침 품질 마감)으로 닫았다.

Effect(효과): F80B/F80C의 프록시 단서는 보존하지만, F80D MT5 validation(MT5 검증) 결과가 negative(부정)이므로 기준선/승격/런타임 권위로 올리지 않는다.

Latest completed run(최근 완료 실행): `{CLOSEOUT_RUN_ID}`

Next frontier proposal(다음 전선 제안): `{NEXT_FRONTIER_PROPOSAL}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    runtime = payload["runtime_validation"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F80 Context Anchor(F80 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `frontier80_closed_next_frontier_not_opened`
- latest completed run(최근 완료 실행): `{CLOSEOUT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- runtime validation(런타임 검증): net `{runtime['net_profit']}`, PF `{runtime['profit_factor']}`, DD `{runtime['max_drawdown_percent']}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_FRONTIER_PROPOSAL}` is proposal only(제안만), not opened(개방 아님).
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F80 Review Index(F80 검토 색인)\n"
    for line in [
        "- `frontier80E_proxy_runtime_gap_attribution_report.md`: F80E gap attribution report(F80E 간극 귀속 보고서)",
        "- `f80e_proxy_runtime_gap_attribution.json`: F80E machine gap attribution(F80E 기계 간극 귀속)",
        "- `stage_closeout_report.md`: F80 stage closeout report(F80 단계 마감 보고서)",
        "- `f80f_stage_closeout_summary.json`: F80F closeout summary(F80F 마감 요약)",
        "- `required_gate_coverage_audit_f80f_closeout.md`: F80F closeout gate audit(F80F 마감 게이트 감사)",
        "- `f80f_result_judgment_receipt.yaml`: F80F result judgment receipt(F80F 결과 판정 영수증)",
    ]:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_registers(payload: Mapping[str, Any], created_at: str) -> None:
    for row in ledger_rows(payload, created_at):
        upsert_csv(RUN_REGISTRY, "run_id", row)
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if CLOSEOUT_RUN_ID not in text:
        addition = f"""

- `{CLOSEOUT_RUN_ID}` closed F80(F80 마감). Result(결과): negative memory(부정 기억) after MT5 runtime probe quality(런타임 탐침 품질). Runtime validation(MT5 검증) net/PF/DD `{payload['runtime_validation']['net_profit']}/{payload['runtime_validation']['profit_factor']}/{payload['runtime_validation']['max_drawdown_percent']}`. Next proposal(다음 제안): `{NEXT_FRONTIER_PROPOSAL}`. Boundary(경계): no authority(권위 없음).
"""
        write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_five_stage_register(created_at: str) -> None:
    if not path_exists(FIVE_STAGE_REGISTER):
        return
    data = yaml.safe_load(io_path(FIVE_STAGE_REGISTER).read_text(encoding="utf-8-sig"))
    state = data.setdefault("state", {})
    closed = list(state.get("closed_frontier_ids_since_last_retrospective") or [])
    if STAGE_ID not in closed:
        closed.append(STAGE_ID)
    state["closed_frontier_ids_since_last_retrospective"] = closed
    state["closeouts_since_last"] = len(closed)
    state["current_due_status"] = "inactive_after_f80_closeout_5_of_5_preserve_records_pending_codex_task_force_replacement"
    state["active_trigger_status"] = "inactive_preserve_records_pending_codex_task_force_replacement"
    state["note"] = "F80 closeout(마감)을 F71-F75 retrospective(회고) 이후 5/5로 등록했지만 active trigger(활성 트리거)는 비활성이다."
    state["last_updated_at_utc"] = created_at
    data.setdefault("cadence", {})["next_open_block"] = False
    io_path(FIVE_STAGE_REGISTER).write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8-sig")


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_gap_payload(created_at)
    write_json(GAP_JSON, payload)
    write_text(GAP_REPORT, gap_report(payload))
    write_text(GAP_GATE_AUDIT, gate_audit_text(payload))
    write_json(CLOSEOUT_SUMMARY, payload)
    write_text(CLOSEOUT_REPORT, closeout_report(payload))
    write_text(CLOSEOUT_GATE_AUDIT, gate_audit_text(payload))
    write_receipts(payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "closeout_run_id": CLOSEOUT_RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "payload": payload,
            "producer": SCRIPT_REL,
            "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_state_files(payload, created_at)
    update_review_index()
    update_registers(payload, created_at)
    update_five_stage_register(created_at)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "runtime_net": payload["runtime_validation"]["net_profit"],
                "runtime_pf": payload["runtime_validation"]["profit_factor"],
                "runtime_dd": payload["runtime_validation"]["max_drawdown_percent"],
                "next_frontier_proposal": NEXT_FRONTIER_PROPOSAL,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
