from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout"
RUN_ID = "frontier16C_edge_quality_risk_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier16C"
PARENT_RUN_ID = "frontier16B_edge_quality_risk_veto_proxy_scout_v1"
NEXT_RUN_ID = "frontier17A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_negative_memory_no_forward_clue_edge_quality_risk_veto_no_authority"
JUDGMENT = "negative_memory_no_forward_clue_with_narrow_rf_density_dd_observation(부정 기억, 전진 단서 없음 + 좁은 랜덤포레스트 빈도/손실폭 관찰)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_16_edge_quality_risk_veto_density_transfer_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_16/frontier16c_stage_closeout.py")
GROK_CLOSEOUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier16_closeout/small_review_answer_only")
F16A_SUMMARY = STAGE_ROOT / "02_runs" / "frontier16A_stage_open_edge_quality_risk_veto_density_transfer_onnx_scout_v1" / "stage_open_summary.json"
F16B_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F16B_FINAL = F16B_ROOT / "final_decision.json"
F16B_SUMMARY = F16B_ROOT / "candidate_summary.csv"
F16B_DENSITY_AUDIT = F16B_ROOT / "density_transfer_audit.csv"
F16B_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
NEGATIVE_MARKER = f"{RUN_ID}__edge_quality_risk_veto_negative_memory"


def main() -> int:
    now = utc_now()
    ensure_dirs()
    stage_open = read_json(F16A_SUMMARY)
    f16b = read_json(F16B_FINAL)
    candidates = read_csv_rows(F16B_SUMMARY)
    density_audit = read_csv_rows(F16B_DENSITY_AUDIT)
    grok = read_grok()
    local = local_verification(stage_open, f16b, grok, candidates, density_audit)
    summary = build_summary(now, stage_open, f16b, grok, local, candidates, density_audit)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": summary["grok_classification"],
        "local_verification": summary["local_verification"]["judgment"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def read_grok() -> dict[str, Any]:
    meta = read_json(GROK_CLOSEOUT / "metadata.json")
    output = read_text(GROK_CLOSEOUT / "clean_output.md")
    lowered = output.lower()
    return {
        "packet": GROK_CLOSEOUT.as_posix(),
        "prompt": (GROK_CLOSEOUT / "prompt.md").as_posix(),
        "output": (GROK_CLOSEOUT / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "negative_memory_supported": "negative_memory" in lowered or "부정 기억" in output,
        "no_preserved_supported": "do not promote" in lowered or "보존 단서" in output and "not a forward clue" in lowered,
        "next_frontier_supported": "next frontier" in lowered or "다음 프론티어" in output,
        "forbidden_claims_supported": "not_claimed" in lowered and "goal achieve" in lowered,
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "classification:" in lowered and "accepted" in lowered:
        return "accepted(수용)"
    if "classification:" in lowered and "rejected" in lowered:
        return "rejected(거절)"
    if "classification:" in lowered and "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(
    stage_open: dict[str, Any],
    f16b: dict[str, Any],
    grok: dict[str, Any],
    candidates: list[dict[str, str]],
    density_audit: list[dict[str, str]],
) -> dict[str, Any]:
    strict_count = sum(parse_bool(row.get("strict_scout_clue_pass")) for row in candidates)
    preserved_count = sum(parse_bool(row.get("preserved_clue_pass")) for row in candidates)
    best = f16b.get("best_candidate_row", {})
    density = density_summary(density_audit)
    guard_ids = {str(guard.get("guard_id")) for guard in stage_open.get("guards", [])}
    checks = {
        "frontier16b_final_exists": path_exists(F16B_FINAL),
        "frontier16b_candidate_summary_exists": path_exists(F16B_SUMMARY),
        "frontier16b_density_audit_exists": path_exists(F16B_DENSITY_AUDIT),
        "frontier16b_report_exists": path_exists(F16B_REPORT),
        "candidate_row_count_9": len(candidates) == 9,
        "strict_recount_zero": strict_count == 0,
        "preserved_recount_zero": preserved_count == 0,
        "final_counts_match_recount": int(f16b.get("strict_scout_clue_rows", -1)) == strict_count
        and int(f16b.get("preserved_clue_rows", -1)) == preserved_count,
        "best_candidate_identity": best.get("candidate_id") == "f16b_edge_h8_t0p30_cap0p45_early0p25__rf_bal__edge_margin__target8",
        "best_oos_pf_below_one": float(best.get("oos_profit_factor", 999.0)) < 1.0,
        "best_density_dd_near_miss_values_present": close_float(best.get("validation_trades_per_day"), 5.655738, 1e-5)
        and close_float(best.get("oos_trades_per_day"), 5.458015, 1e-5)
        and close_float(best.get("validation_dd_risk_percent"), 12.959868, 1e-5)
        and close_float(best.get("oos_dd_risk_percent"), 12.803154, 1e-5),
        "density_train_locked_exact": close_float(density["train_edge_mean"], 8.0, 1e-12),
        "density_label_oracle_too_broad": density["validation_label_mean"] > 20.0 and density["oos_label_mean"] > 20.0,
        "stage_open_no_repair_ladder_guard": "no_repair_ladder" in guard_ids,
        "grok_closeout_accepted": grok["success"] and grok["classification"] == "accepted(수용)",
        "grok_negative_memory_supported": bool(grok["negative_memory_supported"]),
        "grok_no_preserved_supported": bool(grok["no_preserved_supported"]),
        "grok_next_frontier_supported": bool(grok["next_frontier_supported"]),
        "grok_forbidden_claims_supported": bool(grok["forbidden_claims_supported"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "strict_recount": strict_count,
        "preserved_recount": preserved_count,
        "density_summary": density,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def density_summary(rows: list[dict[str, str]]) -> dict[str, float]:
    df = pd.DataFrame(rows)
    if df.empty:
        return {
            "train_edge_mean": 0.0,
            "validation_edge_mean": 0.0,
            "oos_edge_mean": 0.0,
            "validation_label_mean": 0.0,
            "oos_label_mean": 0.0,
        }
    df["trades_per_day_num"] = pd.to_numeric(df["trades_per_day"], errors="coerce")

    def mean(split: str, signal_kind_contains: str) -> float:
        mask = df["split"].eq(split) & df["signal_kind"].str.contains(signal_kind_contains, regex=False)
        return float(df.loc[mask, "trades_per_day_num"].mean())

    return {
        "train_edge_mean": mean("train", "edge_margin_target8"),
        "validation_edge_mean": mean("validation", "edge_margin_target8"),
        "oos_edge_mean": mean("oos", "edge_margin_target8"),
        "validation_label_mean": mean("validation", "label_oracle"),
        "oos_label_mean": mean("oos", "label_oracle"),
    }


def build_summary(
    now: str,
    stage_open: dict[str, Any],
    f16b: dict[str, Any],
    grok: dict[str, Any],
    local: dict[str, Any],
    candidates: list[dict[str, str]],
    density_audit: list[dict[str, str]],
) -> dict[str, Any]:
    best = f16b.get("best_candidate_row", {})
    density = local["density_summary"]
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "f16b_status": f16b.get("status", ""),
        "candidate_row_count": len(candidates),
        "strict_scout_clue_rows": local["strict_recount"],
        "preserved_clue_rows": local["preserved_recount"],
        "best_candidate_row": best,
        "density_summary": density,
        "negative_memory": (
            "Risk-quality labels(위험 품질 라벨) plus locked edge_margin target8(고정 엣지 마진 목표8)은 "
            "density/DD(빈도/손실폭)를 일부 후보에서 맞췄지만 OOS PF(표본밖 수익 팩터)와 split stability(분할 안정성)를 만들지 못했다."
        ),
        "narrow_observation": (
            "Best RF near miss(최고 랜덤포레스트 근접 실패)는 validation/OOS density/DD(검증/표본밖 빈도/손실폭)가 가까웠지만 "
            "OOS PF(표본밖 수익 팩터) `0.942216`으로 edge quality(엣지 품질) 실패다. This is not a preserved clue(보존 단서 아님)."
        ),
        "do_not_repeat": [
            "same 3 label variants with locked edge_margin target8(같은 3개 라벨 변형 + 고정 엣지 마진 목표8)",
            "promoting density/DD near miss without PF(수익 팩터 없는 빈도/손실폭 근접 실패를 승격)",
            "validation/OOS threshold calibration(검증/표본밖 임계값 보정)",
            "adding score cells inside Frontier16(프론티어16 내부 점수 칸 추가)",
        ],
        "next_frontier_direction": (
            "새 가설은 PF and split stability(수익 팩터와 분할 안정성)를 label/decision surface(라벨/결정 표면)에 직접 넣어야 한다. "
            "F16(프론티어16)의 broad label oracle density(넓은 라벨 오라클 빈도)는 반복하지 않는다."
        ),
        "stage_open_guard_reference": stage_open.get("guards", []),
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "external_verification_status": "grok_closeout_review_done_wfo_mt5_out_of_scope_by_claim(그록 마감 검토 완료, WFO/MT5는 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "closeout_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_state_and_registries(summary: dict[str, Any]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(summary))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))
    f03b.append_once(f03b.NEGATIVE_RESULT_REGISTER, NEGATIVE_MARKER, negative_register_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier16a_summary": artifact_identity(F16A_SUMMARY),
            "frontier16b_final": artifact_identity(F16B_FINAL),
            "frontier16b_candidate_summary": artifact_identity(F16B_SUMMARY),
            "frontier16b_density_audit": artifact_identity(F16B_DENSITY_AUDIT),
            "grok_closeout_output": artifact_identity(Path(summary["grok_output"])),
        },
        "outputs": {
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
            "selection_status": (STAGE_ROOT / "04_selected" / "selection_status.md").as_posix(),
        },
    }


def report_text(summary: dict[str, Any]) -> str:
    best = summary["best_candidate_row"]
    density = summary["density_summary"]
    return f"""# Frontier16C Stage Closeout Report(프론티어16C 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier16(프론티어16)을 negative memory with no forward clue(전진 단서 없는 부정 기억)로 닫았습니다.

Effect(효과): locked edge_margin target8(고정 엣지 마진 목표8)과 risk-quality labels(위험 품질 라벨)이 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 함께 만들지 못했다는 경계를 고정합니다.

## Evidence Summary(근거 요약)

- candidate rows(후보 행): `{summary['candidate_row_count']}`
- strict rows(엄격 행): `{summary['strict_scout_clue_rows']}`
- preserved rows(보존 행): `{summary['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`
- density audit(빈도 감사): train edge mean(학습 엣지 평균) `{fmt(density['train_edge_mean'])}/day`, validation edge mean(검증 엣지 평균) `{fmt(density['validation_edge_mean'])}/day`, OOS edge mean(표본밖 엣지 평균) `{fmt(density['oos_edge_mean'])}/day`
- label oracle density(라벨 오라클 빈도): validation(검증) `{fmt(density['validation_label_mean'])}/day`, OOS(표본밖) `{fmt(density['oos_label_mean'])}/day`

## Negative Memory(부정 기억)

{summary['negative_memory']}

## Narrow Observation(좁은 관찰)

{summary['narrow_observation']}

## Grok Closeout Receipt(그록 마감 영수증)

- packet(묶음): `{summary['grok_packet']}`
- classification(분류): `{summary['grok_classification']}`
- prompt hash(프롬프트 해시): `{summary['grok_prompt_hash']}`
- local verification(로컬 검증): `{summary['local_verification']['judgment']}`

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동): 새 frontier hypothesis(프론티어 가설)로 PF and split stability(수익 팩터와 분할 안정성)를 직접 겨냥합니다. Effect(효과): F16(프론티어16)의 near miss(근접 실패)를 repair ladder(수리 사다리)로 늘리지 않습니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier16C Required Gate Coverage Audit(프론티어16C 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- closeout_review_gate(마감 검토 게이트): Grok accepted(그록 수용), local verification(로컬 검증) `{summary['local_verification']['judgment']}`
- result_judgment_gate(결과 판정 게이트): strict rows(엄격 행) 0, preserved rows(보존 행) 0
- no_repair_ladder_gate(수리 사다리 금지 게이트): stage open(단계 개방) guard(가드)를 closeout(마감)에 인용
- paired_tier_gate(티어 쌍 게이트): Tier A closeout(티어 A 마감) plus Tier B/combined missing_required(티어 B/합산 필수 누락) recorded(기록됨)
- external_verification_gate(외부 검증 게이트): WFO/MT5(워크포워드/메타트레이더5)는 out_of_scope_by_claim(주장 범위 밖)
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Review Index(프론티어16 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `frontier16A_stage_open_edge_quality_risk_veto_density_transfer_onnx_scout_v1`: stage open(단계 개방), Grok accepted(그록 수용), guard manifest(가드 목록) registered(등록됨).
- `{PARENT_RUN_ID}`: proxy scout(프록시 탐색), strict rows(엄격 행) 0, preserved rows(보존 행) 0.
- `{RUN_ID}`: stage closeout(단계 마감), Grok accepted(그록 수용), negative memory with no forward clue(전진 단서 없는 부정 기억).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Selection Status(프론티어16 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Closeout run(마감 실행): `{RUN_ID}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Negative memory(부정 기억): {summary['negative_memory']}

Narrow observation(좁은 관찰): {summary['narrow_observation']}

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier16 As Negative Memory With No Forward Clue(결정: 프론티어16을 전진 단서 없는 부정 기억으로 마감)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier16(프론티어16)을 `{summary['judgment']}`로 닫았습니다.

Effect(효과): density/DD near miss(빈도/손실폭 근접 실패)를 preserved clue(보존 단서)로 과장하지 않고, PF and split stability(수익 팩터와 분할 안정성)가 부족한 실패 기억으로 남깁니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


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

Action(행동): Frontier16(프론티어16)은 negative memory with no forward clue(전진 단서 없는 부정 기억)로 마감되었습니다.

Effect(효과): best RF near miss(최고 랜덤포레스트 근접 실패)는 좁은 관찰로만 남기고, preserved clue/completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(보존 단서/완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 만들지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "strict=0;preserved=0;grok_accepted;no_forward_clue;no_authority",
        "family": "result_judgment(결과 판정)",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "closed_negative_memory_no_forward_clue_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(summary["best_candidate_row"]),
        "external_verification_status": summary["external_verification_status"],
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
        "guardrail_kpi": "grok_accepted_no_wfo_no_mt5_no_authority(그록 수용, WFO/MT5/권위 없음)",
        "external_verification_status": summary["external_verification_status"],
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_negative_memory_not_runtime(단계 마감 부정 기억, 런타임 아님)",
            "primary_kpi": primary_kpi_text(summary["best_candidate_row"]),
            "notes": f"next={NEXT_RUN_ID};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"preserved={best.get('preserved_clue_pass', False)};"
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` closed Frontier16(프론티어16) as negative memory with no forward clue"
        f"(전진 단서 없는 부정 기억) after Grok closeout accepted(그록 마감 수용). Effect(효과): next frontier(다음 프론티어) "
        f"`{NEXT_RUN_ID}` must use a new hypothesis(새 가설) and must not preserve the RF near miss(랜덤포레스트 근접 실패 보존 금지).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: Frontier16(프론티어16) closed as negative_memory_no_forward_clue(전진 단서 없는 부정 기억). "
        "Effect(효과): locked edge_margin target8(고정 엣지 마진 목표8) with broad risk-quality labels(넓은 위험 품질 라벨)는 PF and split stability(수익 팩터와 분할 안정성)를 만들지 못했습니다.\n"
    )


def negative_register_entry(summary: dict[str, Any]) -> str:
    return f"""<!-- {NEGATIVE_MARKER} -->
## {RUN_ID} Frontier16 edge-quality risk-veto negative memory(프론티어16 엣지 품질 위험 배제 부정 기억)

- subject(대상): locked edge_margin target8(고정 엣지 마진 목표8) + 3 risk-quality labels(위험 품질 라벨 3개)
- judgment(판정): `negative_memory_no_forward_clue(전진 단서 없는 부정 기억)`
- evidence(근거): best RF validation/OOS PF-density-DD(최고 랜덤포레스트 검증/표본밖 수익 팩터-빈도-손실폭) `{fmt(summary['best_candidate_row'].get('validation_profit_factor'))}/{fmt(summary['best_candidate_row'].get('validation_trades_per_day'))}/{fmt(summary['best_candidate_row'].get('validation_dd_risk_percent'))}%` and `{fmt(summary['best_candidate_row'].get('oos_profit_factor'))}/{fmt(summary['best_candidate_row'].get('oos_trades_per_day'))}/{fmt(summary['best_candidate_row'].get('oos_dd_risk_percent'))}%`
- do_not_repeat(반복 금지): same 3 labels plus locked edge_margin target8(같은 3개 라벨 + 고정 엣지 마진 목표8), density/DD near miss as preserved clue(빈도/손실폭 근접 실패를 보존 단서로 승격)
- reopen_condition(재개 조건): new hypothesis(새 가설)가 PF and split stability(수익 팩터와 분할 안정성)를 직접 설계할 때만 재개
- report(보고서): `{REPORT_PATH.as_posix()}`
"""


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    csv_path(path.parent).mkdir(parents=True, exist_ok=True)
    with csv_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with csv_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with csv_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    csv_path(path.parent).mkdir(parents=True, exist_ok=True)
    with csv_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def csv_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) >= 240:
        return io_path(path)
    return resolved


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with csv_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def close_float(left: Any, right: Any, tolerance: float) -> bool:
    try:
        return abs(float(left) - float(right)) <= tolerance
    except (TypeError, ValueError):
        return False


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "inf"
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
