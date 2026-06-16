from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64b_loss_cluster_hazard_proxy_scout as f64b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64c_handoff_verification as f64c  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64d_handoff_adapter_repair as f64d  # noqa: E402
from stage_pipelines.stage_frontier_64 import run_frontier64_runtime_probe as f64e  # noqa: E402


STAGE_ID = f64b.STAGE_ID
RUN_ID = "frontier64F_stage_closeout_loss_cluster_hazard_v1"
RUN_NUMBER = "frontier64F"
PARENT_RUN_ID = f64e.RUN_ID
NEXT_STAGE_ID = "stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure"
NEXT_RUN_ID = "frontier65A_stage_open_runtime_semantics_pf_source_after_hazard_gate_failure_v1"

STAGE_ROOT = f64b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "stage_closeout_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / "grok_stage_closeout_receipt.md"
F64E_FINAL = STAGE_ROOT / "02_runs" / f64e.RUN_ID / "final_decision.json"
F64B_FINAL = STAGE_ROOT / "02_runs" / f64b.RUN_ID / "final_decision.json"
F64D_FINAL = STAGE_ROOT / "02_runs" / f64d.RUN_ID / "handoff_adapter_repair.json"
GROK_PACKET_ROOT = Path("docs/agent_control/grok_reviews/2026-06-16_frontier64_stage_closeout_review/small_review")
GROK_PROMPT = GROK_PACKET_ROOT / "prompt.md"
GROK_CLEAN_OUTPUT = GROK_PACKET_ROOT / "clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "metadata.json"

FINAL_STATUS = "closed_negative_memory_runtime_probe_quality_gap_no_authority(마감, 부정 기억, 런타임 탐침 품질 차이, 권위 없음)"
FINAL_JUDGMENT = "negative_memory_runtime_probe_quality_gap_no_authority(부정 기억, 런타임 탐침 품질 차이, 권위 없음)"


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    context = load_context()
    final = build_final(created_at, context)
    write_artifacts(final)
    write_reports(final)
    update_registries(final)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "grok_classification": final["grok_classification"],
                    "next_stage_id": final["next_stage_id"],
                    "next_run_id": final["next_run_id"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_context() -> dict[str, Any]:
    required = [F64B_FINAL, F64D_FINAL, F64E_FINAL, GROK_PROMPT, GROK_CLEAN_OUTPUT, GROK_METADATA]
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F64F closeout evidence missing(마감 근거 누락): {missing}")
    return {
        "f64b_final": read_json(F64B_FINAL),
        "f64d_final": read_json(F64D_FINAL),
        "f64e_final": read_json(F64E_FINAL),
        "grok_clean": read_text(GROK_CLEAN_OUTPUT),
        "grok_metadata": read_json(GROK_METADATA),
    }


def build_final(created_at: str, context: Mapping[str, Any]) -> dict[str, Any]:
    f64e_final = context["f64e_final"]
    runtime_rows = list(f64e_final.get("runtime_rows", []))
    gap_rows = list(f64e_final.get("proxy_runtime_gap_rows", []))
    val_runtime = row_by_split(runtime_rows, "validation_is")
    oos_runtime = row_by_split(runtime_rows, "oos")
    val_gap = row_by_split(gap_rows, "validation_is")
    oos_gap = row_by_split(gap_rows, "oos")
    grok_classification = classify_grok(context["grok_clean"])
    local_verification = local_verification_payload(grok_classification, runtime_rows, gap_rows)
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": FINAL_STATUS,
        "judgment": FINAL_JUDGMENT,
        "closeout_label": "negative_memory(부정 기억)",
        "f64b": context["f64b_final"],
        "f64d": context["f64d_final"],
        "f64e": f64e_final,
        "runtime_rows": runtime_rows,
        "proxy_runtime_gap_rows": gap_rows,
        "validation_runtime": val_runtime,
        "oos_runtime": oos_runtime,
        "validation_gap": val_gap,
        "oos_gap": oos_gap,
        "grok_classification": grok_classification,
        "grok_metadata": context["grok_metadata"],
        "grok_prompt": GROK_PROMPT.as_posix(),
        "grok_output": GROK_CLEAN_OUTPUT.as_posix(),
        "grok_receipt": GROK_RECEIPT_PATH.as_posix(),
        "local_verification": local_verification,
        "preserved_clues": preserved_clues(context),
        "negative_memory": negative_memory_text(),
        "do_not_repeat": do_not_repeat_text(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "root_cause_boundary": "runtime_semantics_gap_is_working_hypothesis_not_forensic_proof(런타임 의미 차이는 작업 가설이며 법의학적 증명은 아님)",
    }


def classify_grok(clean: str) -> str:
    lower = clean.lower()
    if "accepted" in lower and "needs_local_verification" in lower:
        return "accepted_with_root_cause_needs_local_verification(수용, 원인 세부는 로컬 검증 필요)"
    if "accepted" in lower:
        return "accepted(수용)"
    return "needs_local_verification(로컬 검증 필요)"


def local_verification_payload(classification: str, runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    feature_ready_clean = all(int_or_none(row.get("feature_ready_diff")) == 0 for row in completed)
    signal_diff_large = any(abs(int_or_none(row.get("signal_count_diff")) or 0) > 1000 for row in completed)
    pf_failed = any((float_or_none(row.get("profit_factor")) or 0.0) <= 1.0 for row in completed)
    dd_failed = any((float_or_none(row.get("max_drawdown_percent")) or 999.0) >= 10.0 for row in completed)
    density_plausible = all(5.0 <= (float_or_none(row.get("runtime_trades_per_day")) or -1.0) <= 10.0 for row in completed)
    gap_pf_collapse = any(abs(float_or_none(row.get("profit_factor_gap_mt5_minus_proxy")) or 0.0) >= 0.35 for row in gap_rows)
    return {
        "classification": classification,
        "completed_runtime_rows": len(completed),
        "feature_ready_diff_zero": feature_ready_clean,
        "large_signal_diff_present": signal_diff_large,
        "pf_failed": pf_failed,
        "dd_failed_somewhere": dd_failed,
        "density_in_goal_band": density_plausible,
        "proxy_runtime_pf_collapse": gap_pf_collapse,
        "accepted": bool(completed and feature_ready_clean and pf_failed and gap_pf_collapse),
        "root_cause_boundary": "accepted_as_working_hypothesis_only(작업 가설로만 수용)",
    }


def preserved_clues(context: Mapping[str, Any]) -> list[str]:
    f64b_final = context["f64b_final"]
    f64d_final = context["f64d_final"]
    return [
        f"F64B proxy(프록시)는 F63 four-axis beat rows(F63 네 축 동시 개선 행) `{f64b_final.get('f63_four_axis_beat_rows')}`와 preserved clue rows(보존 단서 행) `{f64b_final.get('preserved_clue_rows')}`를 만들었다.",
        f"F64D direction adapter ONNX(방향 어댑터 온엑스)+runtime veto tape(런타임 차단 테이프)는 selected adapter(선택 어댑터) `{f64d_final.get('selected_adapter_id')}`로 handoff mismatch(인계 불일치)를 좁혀 MT5 probe(MT5 탐침)까지 보낼 수 있었다.",
        "feature_ready_diff(피처 준비 차이)가 `0`이어도 PF/DD(수익 팩터/손실폭)가 MT5에서 무너질 수 있다는 runtime semantics gap(런타임 의미 차이) 단서를 보존한다.",
    ]


def negative_memory_text() -> str:
    return (
        "loss-cluster hazard admit/block(손실 군집 위험 허용/차단) plus simple symmetric direction entry(단순 대칭 방향 진입)는 "
        "proxy(프록시)와 local handoff repair(로컬 인계 수리)에서는 좋아 보여도 MT5 runtime economics(MT5 런타임 경제성)로 전이되지 않았다."
    )


def do_not_repeat_text() -> str:
    return (
        "Do not treat loss-cluster hazard admit/block(손실 군집 위험 허용/차단) plus simple symmetric direction entry(단순 대칭 방향 진입) "
        "as an independent PF source(독립 수익 팩터 원천) from proxy metrics(프록시 지표), ONNX parity(온엑스 동등성), "
        "or local handoff repair(로컬 인계 수리) alone. Require a narrow MT5 runtime probe(좁은 MT5 런타임 탐침) with explicit PF/DD gates(명시 수익 팩터/손실폭 게이트) "
        "before further work on the same surface(같은 표면). Do not stack more handoff/lifecycle adapter mutations(인계/생명주기 어댑터 변형) "
        "unless the next stage(다음 단계) introduces a new PF mechanism(새 수익 팩터 메커니즘), not another parity patch(동등성 패치)."
    )


def write_artifacts(final: Mapping[str, Any]) -> None:
    f64c.write_json(RUN_ROOT / "stage_closeout_decision.json", final)
    f64c.write_json(RUN_ROOT / "run_manifest.json", final)


def write_reports(final: Mapping[str, Any]) -> None:
    f03b.write_text_sig(REPORT_PATH, closeout_report_text(final))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text())
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status_text(final))
    f03b.write_json(STAGE_ROOT / "04_selected" / "selection_status.json", selection_status_json(final))
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state_text(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))


def closeout_report_text(final: Mapping[str, Any]) -> str:
    val = final["validation_runtime"]
    oos = final["oos_runtime"]
    vgap = final["validation_gap"]
    ogap = final["oos_gap"]
    lines = [
        "# F64F Stage Closeout(F64F 단계 마감)",
        "",
        f"Updated(갱신): {final['created_at_utc']}",
        "",
        f"Status(상태): `{final['status']}`",
        "",
        f"Judgment(판정): `{final['judgment']}`",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): F64 loss-cluster hazard admission source(손실 군집 위험 진입 허용 원천)를 proxy(프록시), handoff verification(인계 검증), capped repair(상한 수리), MT5 runtime probe(MT5 런타임 탐침), Grok closeout review(그록 마감 검토)까지 이어서 닫았다.",
        "",
        "Effect(효과): 좋은 proxy(프록시) 숫자가 MT5 runtime economics(MT5 런타임 경제성)에서 무너진 차이를 negative memory(부정 기억)로 고정하고, 다음 frontier stage(전선 단계)는 새 PF mechanism(새 수익 팩터 메커니즘)만 열게 한다.",
        "",
        "## Runtime Evidence(런타임 근거)",
        "",
        "| split(분할) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |",
        "|---|---:|---:|---:|---:|---:|",
        f"| validation_is(검증 내부) | {val.get('profit_factor')} | {val.get('max_drawdown_percent')} | {val.get('runtime_trades_per_day')} | {val.get('signal_count_diff')} | {val.get('feature_ready_diff')} |",
        f"| oos(표본외) | {oos.get('profit_factor')} | {oos.get('max_drawdown_percent')} | {oos.get('runtime_trades_per_day')} | {oos.get('signal_count_diff')} | {oos.get('feature_ready_diff')} |",
        "",
        "## Proxy-Runtime Gap(프록시-런타임 차이)",
        "",
        f"- validation_is PF gap(MT5 minus proxy, MT5-프록시): `{fmt(vgap.get('profit_factor_gap_mt5_minus_proxy'))}`; DD gap(손실폭 차이): `{fmt(vgap.get('dd_gap_mt5_minus_proxy'))}`.",
        f"- oos PF gap(MT5 minus proxy, MT5-프록시): `{fmt(ogap.get('profit_factor_gap_mt5_minus_proxy'))}`; DD gap(손실폭 차이): `{fmt(ogap.get('dd_gap_mt5_minus_proxy'))}`.",
        "",
        "## Grok Review(그록 검토)",
        "",
        f"- packet(패킷): `{GROK_PACKET_ROOT.as_posix()}`",
        f"- classification(분류): `{final['grok_classification']}`",
        f"- local verification(로컬 검증): `{final['local_verification']['accepted']}`",
        f"- root-cause boundary(원인 경계): `{final['root_cause_boundary']}`",
        "",
        "## Preserved Clues(보존 단서)",
        "",
    ]
    lines.extend(f"- {item}" for item in final["preserved_clues"])
    lines.extend(
        [
            "",
            "## Negative Memory(부정 기억)",
            "",
            final["negative_memory"],
            "",
            "## Do Not Repeat(반복 금지)",
            "",
            final["do_not_repeat"],
            "",
            "## Boundary(경계)",
            "",
            "Closeout(마감)은 negative memory(부정 기억)다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)이다.",
            "",
            f"Next stage(다음 단계): `{final['next_stage_id']}`.",
            f"Next run(다음 실행): `{final['next_run_id']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def grok_receipt_text(final: Mapping[str, Any]) -> str:
    metadata = final["grok_metadata"]
    return "\n".join(
        [
            "# F64 Grok Stage Closeout Receipt(F64 그록 단계 마감 영수증)",
            "",
            "- trigger_reason(트리거 이유): stage closeout requires Grok second opinion(단계 마감은 그록 2차 의견 필요).",
            "- review_size(검토 크기): `small review(소규모 검토)`.",
            "- direction_before_grok(그록 전 방향): close F64 as negative memory if MT5 PF/DD gap is valid(유효한 MT5 수익 팩터/손실폭 차이면 부정 기억으로 마감).",
            f"- prompt_identity(프롬프트 정체성): `{GROK_PROMPT.as_posix()}`, sha256 `{metadata.get('prompt_hash')}`.",
            f"- grok_output_identity(그록 출력 정체성): `{GROK_CLEAN_OUTPUT.as_posix()}`, sha256 `{sha256_file(GROK_CLEAN_OUTPUT)}`.",
            f"- advice_classification(조언 분류): `{final['grok_classification']}`.",
            f"- local_verification(로컬 검증): `{json.dumps(json_ready(final['local_verification']), ensure_ascii=False, sort_keys=True)}`.",
            "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
            f"- final_codex_direction(최종 코덱스 방향): `{final['judgment']}`로 닫고 `{final['next_run_id']}`는 새 PF mechanism(새 수익 팩터 메커니즘) 질문으로만 연다.",
            "",
        ]
    )


def review_index_text() -> str:
    return "\n".join(
        [
            "# F64 Review Index(F64 검토 색인)",
            "",
            "- `runA_report.md`: stage-open report(단계 개방 보고)",
            "- `runB_report.md`: proxy scout report(프록시 탐색 보고)",
            "- `handoff_verification_report.md`: F64C handoff verification(인계 검증)",
            "- `handoff_adapter_repair_report.md`: F64D handoff adapter repair(인계 어댑터 수리)",
            "- `runtime_probe_report.md`: F64E MT5 runtime probe(MT5 런타임 탐침)",
            "- `proxy_runtime_gap_report.md`: F64E proxy-runtime gap(프록시-런타임 차이)",
            "- `grok_stage_open_receipt.md`: Grok stage-open receipt(그록 단계 개방 영수증)",
            "- `grok_stage_closeout_receipt.md`: Grok closeout receipt(그록 마감 영수증)",
            "- `stage_closeout_report.md`: F64F closeout report(F64F 마감 보고)",
            "- `required_gate_coverage_audit.md`: required gate coverage audit(필수 게이트 커버리지 감사)",
            "- `stage_run_ledger.csv`: stage-local run ledger(단계 로컬 실행 장부)",
            "",
        ]
    )


def gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# F64 Required Gate Coverage Audit(F64 필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_completed(프록시 완료): `{f64b.RUN_ID}`
- pre_mt5_grok_review(비싼 MT5 전 그록 검토): `needs_local_verification(로컬 검증 필요)`
- local_handoff_verification(로컬 인계 검증): `blocked_handoff_adapter_mismatch(차단, 인계 어댑터 불일치)`
- capped_handoff_adapter_repair(상한 있는 인계 어댑터 수리): `{f64d.RUN_ID}`
- mt5_runtime_probe(MT5 런타임 탐침): `{PARENT_RUN_ID}` / `runtime_probe_observation_no_authority`
- proxy_runtime_gap(프록시-런타임 차이): `recorded(기록됨)`
- stage_closeout_grok_review(단계 마감 그록 검토): `{final['grok_classification']}`
- local_verification(로컬 검증): `accepted_negative_memory_with_root_cause_boundary(부정 기억 수용, 원인 경계 낮춤)`
- final_closeout_label(최종 마감 라벨): `{final['closeout_label']}`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# F64 Selection Status(F64 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- selected_proxy_candidate(선택 프록시 후보): `{final['f64e'].get('candidate_id')}`
- selected_direction_adapter(선택 방향 어댑터): `{final['f64e'].get('selected_adapter_id')}`
- runtime_probe_report(런타임 탐침 보고서): `{f64e.REPORT_PATH.as_posix()}`
- proxy_runtime_gap_report(프록시-런타임 차이 보고서): `{f64e.GAP_REPORT_PATH.as_posix()}`
- closeout_report(마감 보고서): `{REPORT_PATH.as_posix()}`
- grok_closeout_receipt(그록 마감 영수증): `{GROK_RECEIPT_PATH.as_posix()}`
- next_stage(다음 단계): `{final['next_stage_id']}`
- next_run(다음 실행): `{final['next_run_id']}`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def selection_status_json(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "closeout_label": final["closeout_label"],
        "selected_proxy_candidate": final["f64e"].get("candidate_id"),
        "selected_direction_adapter": final["f64e"].get("selected_adapter_id"),
        "runtime_probe_report": f64e.REPORT_PATH.as_posix(),
        "proxy_runtime_gap_report": f64e.GAP_REPORT_PATH.as_posix(),
        "closeout_report": REPORT_PATH.as_posix(),
        "grok_closeout_receipt": GROK_RECEIPT_PATH.as_posix(),
        "next_stage_id": final["next_stage_id"],
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["claim_boundary"],
    }


def workspace_state_text(final: Mapping[str, Any]) -> str:
    val = final["validation_runtime"]
    oos = final["oos_runtime"]
    return f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_stage_id: {final['next_stage_id']}
next_run_id: {final['next_run_id']}
runtime_probe_status: runtime_probe_observation_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
notes:
  - "F64F closeout(마감): negative_memory(부정 기억). validation_is PF={val.get('profit_factor')} DD={val.get('max_drawdown_percent')} trades/day={val.get('runtime_trades_per_day')}; OOS PF={oos.get('profit_factor')} DD={oos.get('max_drawdown_percent')} trades/day={oos.get('runtime_trades_per_day')}."
  - "Grok closeout review(그록 마감 검토)는 label(라벨)을 accepted(수용)했고 root cause(원인)는 working hypothesis(작업 가설)로 낮췄다."
  - "Next frontier(다음 전선)는 F64 adapter mutation(어댑터 변형) 반복이 아니라 new PF mechanism(새 수익 팩터 메커니즘) 질문이다."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음)."
"""


def current_working_state_text(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Frontier64(F64, 전선 64단계)는 stage closeout(단계 마감)까지 닫혔다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- closeout_label(마감 라벨): `{final['closeout_label']}`
- next_stage(다음 단계): `{final['next_stage_id']}`
- next_run(다음 실행): `{final['next_run_id']}`

Action(행동): F64B proxy(프록시), F64C handoff verification(인계 검증), F64D capped repair(상한 수리), F64E MT5 runtime probe(MT5 런타임 탐침), Grok closeout review(그록 마감 검토)를 하나의 hypothesis lifecycle(가설 생명주기)로 묶어 마감했다.

Effect(효과): loss-cluster hazard admit/block(손실 군집 위험 허용/차단) 표면은 proxy(프록시)만으로는 독립 PF source(독립 수익 팩터 원천)로 믿으면 안 된다는 negative memory(부정 기억)로 남았고, 다음 frontier(다음 전선)는 새 PF mechanism(새 수익 팩터 메커니즘)을 열어야 한다.

Claim boundary(주장 경계): closeout(마감)은 완료 후보가 아니라 negative memory(부정 기억)다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
"""


def update_registries(final: Mapping[str, Any]) -> None:
    patch_f64e_evidence_paths()
    f64c.upsert_csv(f03b.RUN_REGISTRY, "run_id", runtime_probe_run_registry_row(final))
    f64c.upsert_csv(f03b.RUN_REGISTRY, "run_id", closeout_run_registry_row(final))
    f64c.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", closeout_ledger_row(final))
    sync_stage_ledger_from_project()
    f64c.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    f64c.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_entry(final))
    f64c.append_once(f03b.NEGATIVE_RESULT_REGISTER, RUN_ID, negative_entry(final))


def runtime_probe_run_registry_row(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = final["oos_runtime"]
    val = final["validation_runtime"]
    return {
        "run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_runtime_probe(엠티5 런타임 탐침)",
        "status": "runtime_probe_observation_no_authority",
        "judgment": FINAL_JUDGMENT,
        "path": f64e.REPORT_PATH.as_posix(),
        "notes": f"validation_pf={val.get('profit_factor')};validation_dd={val.get('max_drawdown_percent')};oos_pf={oos.get('profit_factor')};oos_dd={oos.get('max_drawdown_percent')};next={RUN_ID}",
        "family": "runtime_parity(런타임 동등성)",
        "primary_report": f64e.REPORT_PATH.as_posix(),
        "run_number": "frontier64E",
        "date": final["created_at_utc"][:10],
        "decision": FINAL_JUDGMENT,
        "parent_run_id": f64d.RUN_ID,
        "next_run_id": RUN_ID,
        "claim_boundary": "runtime_probe_observation_only_no_authority(런타임 탐침 관찰 전용, 권위 없음)",
        "report_path": f64e.REPORT_PATH.as_posix(),
        "profit_factor": oos.get("profit_factor", ""),
        "drawdown": oos.get("max_drawdown_percent", ""),
        "trade_count": oos.get("trade_count", ""),
        "view": "mt5_runtime_probe(엠티5 런타임 탐침)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "mt5_runtime_probe(엠티5 런타임 탐침)",
        "external_verification_status": "completed(완료)",
        "result_judgment": FINAL_JUDGMENT,
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_mt5_runtime_probe(전선 MT5 런타임 탐침)",
        "run_type": "mt5_runtime_probe(엠티5 런타임 탐침)",
        "output_path": (STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "final_decision.json").as_posix(),
        "result_path": (STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "final_decision.json").as_posix(),
        "selected_profit_factor": oos.get("profit_factor", ""),
        "selected_trade_density": oos.get("runtime_trades_per_day", ""),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
        "trade_density": oos.get("runtime_trades_per_day", ""),
        "max_drawdown_percent": oos.get("max_drawdown_percent", ""),
    }


def closeout_run_registry_row(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = final["oos_runtime"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"closeout=negative_memory;grok={final['grok_classification']};next={final['next_run_id']}",
        "family": "result_judgment(결과 판정)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": final["created_at_utc"][:10],
        "decision": final["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": "closed_negative_memory_no_completion_no_authority(부정 기억 마감, 완성/권위 없음)",
        "report_path": REPORT_PATH.as_posix(),
        "profit_factor": oos.get("profit_factor", ""),
        "drawdown": oos.get("max_drawdown_percent", ""),
        "trade_count": oos.get("trade_count", ""),
        "view": "stage_closeout(단계 마감)",
        "tier": "Tier A + missing_required records(티어 A + 필수 누락 기록)",
        "metric_scope": "stage_closeout_runtime_probe_summary(단계 마감 런타임 탐침 요약)",
        "external_verification_status": "completed(완료)",
        "result_judgment": final["judgment"],
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_stage_closeout(전선 단계 마감)",
        "run_type": "stage_closeout(단계 마감)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": (RUN_ROOT / "stage_closeout_decision.json").as_posix(),
        "result_path": (RUN_ROOT / "stage_closeout_decision.json").as_posix(),
        "selected_profit_factor": oos.get("profit_factor", ""),
        "selected_trade_density": oos.get("runtime_trades_per_day", ""),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
        "trade_density": oos.get("runtime_trades_per_day", ""),
        "max_drawdown_percent": oos.get("max_drawdown_percent", ""),
    }


def closeout_ledger_row(final: Mapping[str, Any]) -> dict[str, Any]:
    row = closeout_run_registry_row(final)
    row.update(
        {
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "subrun_id": f"{RUN_ID}__stage_closeout",
            "record_view": "stage_closeout(단계 마감)",
            "tier_scope": "Tier A separate + Tier B missing_required + Tier A+B missing_required(Tier A 분리 + Tier B 필수 누락 + 합산 필수 누락)",
            "kpi_scope": "runtime_probe_closeout(런타임 탐침 마감)",
            "scoreboard_lane": "result_judgment(결과 판정)",
            "primary_kpi": f"validation_pf={final['validation_runtime'].get('profit_factor')};oos_pf={final['oos_runtime'].get('profit_factor')};label=negative_memory",
            "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)",
            "external_verification_status": "completed(완료)",
        }
    )
    return row


def patch_f64e_evidence_paths() -> None:
    old_path = "stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/03_reviews/frontier64E_mt5_runtime_probe_loss_cluster_hazard_v1_report.md"
    new_path = f64e.REPORT_PATH.as_posix()
    patch_csv_field(f03b.ALPHA_LEDGER, "run_id", PARENT_RUN_ID, {"path": new_path, "report_path": new_path, "primary_report": new_path})
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(stage_ledger):
        patch_csv_field(stage_ledger, "run_id", PARENT_RUN_ID, {"path": new_path})
    del old_path


def sync_stage_ledger_from_project() -> None:
    header = read_csv_header(f03b.ALPHA_LEDGER)
    rows = [row for row in read_csv_rows(f03b.ALPHA_LEDGER) if row.get("stage_id") == STAGE_ID]
    write_csv_with_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", header, rows)


def patch_csv_field(path: Path, key: str, value: str, updates: Mapping[str, Any]) -> None:
    if not path_exists(path):
        return
    header = read_csv_header(path)
    rows = read_csv_rows(path)
    changed = False
    for row in rows:
        if row.get(key) == value:
            for field, new_value in updates.items():
                if field in header:
                    row[field] = f03b.stringify(new_value)
                    changed = True
    if changed:
        write_csv_with_header(path, header, rows)


def changelog_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {final['created_at_utc'][:10]} Frontier64F Stage Closeout(F64F 단계 마감)\n\n- action(행동): `{RUN_ID}`로 F64 loss-cluster hazard source(손실 군집 위험 원천)를 negative memory(부정 기억)로 마감했다.\n- effect(효과): MT5 PF/DD(수익 팩터/손실폭) 실패와 proxy-runtime gap(프록시-런타임 차이)을 고정하고 `{final['next_run_id']}`를 새 PF mechanism(새 수익 팩터 메커니즘) 질문으로 남겼다.\n- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.\n"


def idea_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_ID}\n\n- Stage(단계): `{STAGE_ID}`\n- Idea(아이디어): loss-cluster hazard admission source(손실 군집 위험 진입 허용 원천)가 independent PF source(독립 수익 팩터 원천)인지 시험했다.\n- Result(결과): `{final['judgment']}`\n- Evidence(근거): `{REPORT_PATH.as_posix()}` and `{f64e.GAP_REPORT_PATH.as_posix()}`.\n- Preserved clue(보존 단서): F64B proxy(프록시)와 F64D handoff repair(인계 수리)는 참조 단서로만 보존한다.\n- Next(다음): `{final['next_run_id']}` with new PF mechanism(새 수익 팩터 메커니즘).\n- Boundary(경계): no authority(권위 없음), no completion(완성 없음).\n"


def negative_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_ID}\n\n- Stage(단계): `{STAGE_ID}`\n- Negative memory(부정 기억): `{final['judgment']}`\n- Why failed(실패 이유): {final['negative_memory']}\n- Salvage value(회수 가치): F64B proxy clue(프록시 단서), F64D handoff-repair clue(인계 수리 단서), feature_ready_diff=0 with MT5 failure(피처 준비 차이 0인데 MT5 실패)를 보존한다.\n- Reopen condition(재개 조건): same surface(같은 표면)는 새 PF mechanism(새 수익 팩터 메커니즘)과 narrow MT5 runtime probe(좁은 MT5 런타임 탐침)를 함께 제시할 때만 재개한다.\n- Do-not-repeat(반복 금지): {final['do_not_repeat']}\n- Evidence(근거): `{REPORT_PATH.as_posix()}` and `{f64e.GAP_REPORT_PATH.as_posix()}`.\n- Boundary(경계): no authority(권위 없음), no completion(완성 없음).\n"


def row_by_split(rows: Sequence[Mapping[str, Any]], split: str) -> dict[str, Any]:
    for row in rows:
        if str(row.get("split")) == split:
            return dict(row)
    return {}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_csv_header(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv_with_header(path: Path, header: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(header), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: f03b.stringify(row.get(column, "")) for column in header})


def int_or_none(value: Any) -> int | None:
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return None


def float_or_none(value: Any) -> float | None:
    try:
        number = float(str(value))
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: Any) -> str:
    number = float_or_none(value)
    return f"{number:.6g}" if number is not None else "n/a"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
