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


STAGE_ID = "stage_frontier_15__score_threshold_density_controlled_onnx_scout"
RUN_ID = "frontier15C_score_threshold_density_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier15C"
PARENT_RUN_ID = "frontier15B_score_threshold_density_controlled_proxy_scout_v1"
NEXT_RUN_ID = "frontier16A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_negative_memory_with_preserved_density_transfer_clue_no_authority"
JUDGMENT = "negative_memory_with_preserved_density_transfer_clue(부정 기억 + 빈도 전이 보존 단서)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_15_score_threshold_density_controlled_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_15/frontier15c_stage_closeout.py")
GROK_CLOSEOUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier15_closeout/small_review_answer_only")
IDEA_MARKER = RUN_ID
NEGATIVE_MARKER = f"{RUN_ID}__score_threshold_edge_quality_negative_memory"

F15B_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F15B_FINAL = F15B_ROOT / "final_decision.json"
F15B_SUMMARY = F15B_ROOT / "candidate_summary.csv"
F15B_THRESHOLD = F15B_ROOT / "threshold_manifest.csv"
F15B_GAP = F15B_ROOT / "label_model_density_gap.csv"
F15B_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
PRIMARY_CELL_ID = "edge_margin__target8"


def main() -> int:
    now = utc_now()
    ensure_dirs()
    f15b = read_json(F15B_FINAL)
    candidates = read_csv_rows(F15B_SUMMARY)
    thresholds = read_csv_rows(F15B_THRESHOLD)
    density_gap = read_csv_rows(F15B_GAP)
    grok = read_grok()
    local = local_verification(f15b, grok, candidates, thresholds, density_gap)
    summary = build_summary(now, f15b, grok, local, candidates, thresholds, density_gap)
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
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
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
        "density_transfer_supported": "density" in lowered and "transfer" in lowered or "빈도 전이" in output,
        "next_frontier_supported": "next frontier" in lowered or "다음 프론티어" in output,
        "forbidden_claims_supported": "not_claimed" in lowered and "goal achieve" in lowered,
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "classification: accepted" in lowered:
        return "accepted(수용)"
    if "classification: rejected" in lowered:
        return "rejected(거절)"
    if "classification: needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(
    f15b: dict[str, Any],
    grok: dict[str, Any],
    candidates: list[dict[str, str]],
    thresholds: list[dict[str, str]],
    density_gap: list[dict[str, str]],
) -> dict[str, Any]:
    strict_count = sum(parse_bool(row.get("strict_scout_clue_pass")) for row in candidates)
    secondary_count = sum(parse_bool(row.get("secondary_strict_like_pass")) for row in candidates)
    preserved_count = sum(parse_bool(row.get("preserved_clue_pass")) for row in candidates)
    primary_rows = [row for row in candidates if parse_bool(row.get("is_primary_cell"))]
    exact_threshold_density = all(
        close_float(row.get("actual_train_selected_density_per_day"), row.get("target_density_per_day"), tolerance=1e-12)
        for row in thresholds
    )
    transfer = density_transfer_summary(density_gap)
    checks = {
        "frontier15b_final_exists": path_exists(F15B_FINAL),
        "frontier15b_candidate_summary_exists": path_exists(F15B_SUMMARY),
        "frontier15b_threshold_manifest_exists": path_exists(F15B_THRESHOLD),
        "frontier15b_density_gap_exists": path_exists(F15B_GAP),
        "frontier15b_report_exists": path_exists(F15B_REPORT),
        "candidate_row_count_81": len(candidates) == 81,
        "threshold_row_count_81": len(thresholds) == 81,
        "score_cell_count_9": len({row.get("cell_id") for row in thresholds}) == 9,
        "primary_cell_identity": {row.get("cell_id") for row in primary_rows} == {PRIMARY_CELL_ID},
        "strict_recount_zero": strict_count == 0,
        "secondary_recount_zero": secondary_count == 0,
        "preserved_recount_zero": preserved_count == 0,
        "final_counts_match_recount": int(f15b.get("primary_strict_scout_clue_rows", -1)) == strict_count
        and int(f15b.get("secondary_strict_like_rows", -1)) == secondary_count
        and int(f15b.get("preserved_clue_rows", -1)) == preserved_count,
        "train_threshold_density_exact": exact_threshold_density,
        "primary_density_transfers_near_target": 5.0 <= transfer["primary_validation_mean"] <= 10.0
        and 5.0 <= transfer["primary_oos_mean"] <= 10.0,
        "frontier15b_no_authority": f15b.get("claim_boundary", {}).get("runtime_authority") == "not_claimed(주장 없음)"
        and f15b.get("claim_boundary", {}).get("goal_achieve") == "not_claimed(주장 없음)",
        "grok_closeout_accepted": grok["success"] and grok["classification"] == "accepted(수용)",
        "grok_negative_memory_supported": bool(grok["negative_memory_supported"]),
        "grok_density_transfer_supported": bool(grok["density_transfer_supported"]),
        "grok_next_frontier_supported": bool(grok["next_frontier_supported"]),
        "grok_forbidden_claims_supported": bool(grok["forbidden_claims_supported"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "strict_recount": strict_count,
        "secondary_recount": secondary_count,
        "preserved_recount": preserved_count,
        "density_transfer_summary": transfer,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def density_transfer_summary(density_gap: list[dict[str, str]]) -> dict[str, Any]:
    df = pd.DataFrame(density_gap)
    if df.empty:
        return {
            "primary_validation_mean": 0.0,
            "primary_oos_mean": 0.0,
            "all_cell_train_exact_note": "missing(누락)",
        }
    df["model_trades_per_day_num"] = pd.to_numeric(df["model_trades_per_day"], errors="coerce")
    primary = df[df["cell_id"].eq(PRIMARY_CELL_ID)]
    return {
        "primary_validation_mean": float(primary[primary["split"].eq("validation")]["model_trades_per_day_num"].mean()),
        "primary_oos_mean": float(primary[primary["split"].eq("oos")]["model_trades_per_day_num"].mean()),
        "all_cells_validation_mean": float(df[df["split"].eq("validation")]["model_trades_per_day_num"].mean()),
        "all_cells_oos_mean": float(df[df["split"].eq("oos")]["model_trades_per_day_num"].mean()),
    }


def build_summary(
    now: str,
    f15b: dict[str, Any],
    grok: dict[str, Any],
    local: dict[str, Any],
    candidates: list[dict[str, str]],
    thresholds: list[dict[str, str]],
    density_gap: list[dict[str, str]],
) -> dict[str, Any]:
    best = f15b.get("best_candidate_row", {})
    primary = f15b.get("best_primary_cell_row", {})
    transfer = local["density_transfer_summary"]
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "f15b_status": f15b.get("status", ""),
        "candidate_row_count": len(candidates),
        "threshold_row_count": len(thresholds),
        "primary_strict_scout_clue_rows": local["strict_recount"],
        "secondary_strict_like_rows": local["secondary_recount"],
        "row_level_preserved_clue_rows": local["preserved_recount"],
        "mechanism_level_preserved_clue": (
            "train-only score thresholds(학습 전용 점수 임계값)는 density target(빈도 목표)을 validation/OOS"
            "(검증/표본밖) 주변으로 transfer(전이)할 수 있다. This is calibration-only(보정 전용) and not edge"
            "(엣지) or authority(권위)."
        ),
        "negative_memory": (
            "Probability score threshold(확률 점수 임계값) alone(단독) did not jointly deliver edge quality/PF/DD/"
            "subperiod stability(엣지 품질/수익 팩터/손실폭/하위기간 안정성). Best overall row(전체 최고 행)는 "
            f"validation/OOS PF-density-DD(검증/표본밖 수익 팩터-빈도-손실폭) {fmt(best.get('validation_profit_factor'))}/"
            f"{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk_percent'))}% and "
            f"{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk_percent'))}% only."
        ),
        "best_candidate_row": best,
        "best_primary_cell_row": primary,
        "density_transfer_summary": transfer,
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "do_not_repeat": [
            "same 9-cell score-threshold grid expansion(같은 9칸 점수 임계값 격자 확장)",
            "validation/OOS-guided threshold filtering(검증/표본밖 유도 임계값 필터링)",
            "F14 quota/horizon retuning(F14 할당/보유기간 재조정)",
            "claiming density transfer as edge(빈도 전이를 엣지로 주장)",
        ],
        "next_frontier_direction": (
            "new hypothesis required for edge quality/risk stability(엣지 품질/위험 안정성을 위한 새 가설 필요). "
            "Density transfer(빈도 전이)는 input clue(입력 단서)로만 carry(이월)한다."
        ),
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
    f03b.append_once(f03b.IDEA_REGISTRY, IDEA_MARKER, idea_registry_entry(summary))
    f03b.append_once(f03b.NEGATIVE_RESULT_REGISTER, NEGATIVE_MARKER, negative_register_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier15b_final": artifact_identity(F15B_FINAL),
            "frontier15b_candidate_summary": artifact_identity(F15B_SUMMARY),
            "frontier15b_threshold_manifest": artifact_identity(F15B_THRESHOLD),
            "frontier15b_density_gap": artifact_identity(F15B_GAP),
            "frontier15b_report": artifact_identity(F15B_REPORT),
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
    primary = summary["best_primary_cell_row"]
    transfer = summary["density_transfer_summary"]
    return f"""# Frontier15C Stage Closeout Report(프론티어15C 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier15(프론티어15)를 negative memory with preserved density-transfer clue(부정 기억 + 빈도 전이 보존 단서)로 닫았습니다.

Effect(효과): score threshold(점수 임계값)이 density(빈도)는 통제하지만 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 만들지 못했다는 경계를 고정하고, 다음 frontier(프론티어)는 새 가설로 시작합니다.

## Evidence Summary(근거 요약)

- candidate rows(후보 행): `{summary['candidate_row_count']}`
- primary strict rows(1순위 엄격 행): `{summary['primary_strict_scout_clue_rows']}`
- secondary strict-like rows(보조 엄격 유사 행): `{summary['secondary_strict_like_rows']}`
- row-level preserved clue rows(행 단위 보존 단서 행): `{summary['row_level_preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- best validation PF/density/DD(최고 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- best OOS PF/density/DD(최고 표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- best primary cell(최고 1순위 칸): `{primary.get('candidate_id', 'none')}`
- primary validation/OOS PF-density-DD(1순위 검증/표본밖 수익 팩터-빈도-손실폭): `{fmt(primary.get('validation_profit_factor'))}` / `{fmt(primary.get('validation_trades_per_day'))}` / `{fmt(primary.get('validation_dd_risk_percent'))}%` and `{fmt(primary.get('oos_profit_factor'))}` / `{fmt(primary.get('oos_trades_per_day'))}` / `{fmt(primary.get('oos_dd_risk_percent'))}%`

## Preserved Clue(보존 단서)

{summary['mechanism_level_preserved_clue']}

Primary cell density transfer(1순위 칸 빈도 전이): validation mean(검증 평균) `{fmt(transfer['primary_validation_mean'])}/day`, OOS mean(표본밖 평균) `{fmt(transfer['primary_oos_mean'])}/day`.

## Negative Memory(부정 기억)

{summary['negative_memory']}

## Grok Closeout Receipt(그록 마감 영수증)

- packet(묶음): `{summary['grok_packet']}`
- classification(분류): `{summary['grok_classification']}`
- prompt hash(프롬프트 해시): `{summary['grok_prompt_hash']}`
- local verification(로컬 검증): `{summary['local_verification']['judgment']}`

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동): 새 frontier hypothesis(프론티어 가설)로 edge quality/risk stability(엣지 품질/위험 안정성)를 다시 설계합니다. Effect(효과): density transfer(빈도 전이)를 edge(엣지)로 과장하지 않고 입력 단서로만 씁니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier15C Required Gate Coverage Audit(프론티어15C 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- closeout_review_gate(마감 검토 게이트): Grok accepted(그록 수용), local verification(로컬 검증) `{summary['local_verification']['judgment']}`
- result_judgment_gate(결과 판정 게이트): primary strict rows(1순위 엄격 행) 0, secondary strict-like rows(보조 엄격 유사 행) 0, row-level preserved rows(행 단위 보존 행) 0
- preserved_clue_boundary(보존 단서 경계): density-transfer mechanism only(빈도 전이 메커니즘만), no edge/authority claim(엣지/권위 주장 없음)
- paired_tier_gate(짝 티어 게이트): Tier A(티어 A) closeout plus Tier B/combined missing_required(티어 B/합산 필수 누락) recorded(기록됨)
- external_verification_gate(외부 검증 게이트): WFO/MT5(워크포워드/메타트레이더5)는 out_of_scope_by_claim(주장 범위 밖)
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Review Index(프론티어15 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `frontier15A_stage_open_score_threshold_density_controlled_onnx_scout_v1`: stage open(단계 개방), Grok accepted(그록 수용), 9-cell grid(9칸 격자) registered(등록됨).
- `{PARENT_RUN_ID}`: proxy scout(프록시 탐색), primary strict rows(1순위 엄격 행) 0, secondary strict-like rows(보조 엄격 유사 행) 0, row-level preserved rows(행 단위 보존 행) 0.
- `{RUN_ID}`: stage closeout(단계 마감), Grok accepted(그록 수용), negative memory plus narrow density-transfer clue(부정 기억 + 좁은 빈도 전이 단서).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier15 Selection Status(프론티어15 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Closeout run(마감 실행): `{RUN_ID}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Mechanism-level preserved clue(메커니즘 단위 보존 단서): {summary['mechanism_level_preserved_clue']}

Negative memory(부정 기억): {summary['negative_memory']}

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier15 As Negative Memory With Density-Transfer Clue(결정: 프론티어15를 부정 기억 + 빈도 전이 단서로 마감)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier15(프론티어15)를 `{summary['judgment']}`로 닫았습니다.

Effect(효과): score threshold(점수 임계값) 방식은 density target(빈도 목표)을 옮기는 데 쓸 수 있지만, edge quality/PF/DD/smoothness(엣지 품질/수익 팩터/손실폭/매끄러움)는 새 가설이 필요합니다.

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

Action(행동): Frontier15(프론티어15)는 negative memory with preserved density-transfer clue(부정 기억 + 빈도 전이 보존 단서)로 마감되었습니다.

Effect(효과): train-only score threshold(학습 전용 점수 임계값)는 빈도 목표를 옮길 수 있지만, PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 같이 만들지는 못했다는 경계를 고정합니다.

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
        "notes": f"primary_strict=0;secondary_strict_like=0;row_preserved=0;grok_accepted;no_authority",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "closed_negative_memory_density_transfer_clue_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(summary["best_candidate_row"], summary["best_primary_cell_row"]),
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
            "kpi_scope": "stage_closeout_negative_memory_density_transfer_clue_not_runtime(단계 마감 부정 기억 + 빈도 전이 단서, 런타임 아님)",
            "primary_kpi": primary_kpi_text(summary["best_candidate_row"], summary["best_primary_cell_row"]),
            "notes": f"next={NEXT_RUN_ID};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 짝 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)",
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


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` closed Frontier15(프론티어15) as negative memory with density-transfer clue"
        f"(부정 기억 + 빈도 전이 단서) after Grok closeout accepted(그록 마감 수용). Effect(효과): next frontier(다음 프론티어)"
        f" `{NEXT_RUN_ID}` starts a new hypothesis(새 가설) without authority claims(권위 주장 없음).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: Frontier15(프론티어15) closed as negative_memory_with_preserved_density_transfer_clue"
        "(부정 기억 + 빈도 전이 보존 단서). Effect(효과): train-only score threshold(학습 전용 점수 임계값)는 "
        "density transfer(빈도 전이) 단서로만 남기고, edge/PF/DD/smoothness(엣지/수익 팩터/손실폭/매끄러움)는 새 가설로 넘깁니다.\n"
    )


def negative_register_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{NEGATIVE_MARKER}`: Probability score threshold(확률 점수 임계값) alone(단독) did not create joint edge quality/PF/DD/"
        "subperiod stability(엣지 품질/수익 팩터/손실폭/하위기간 안정성). Effect(효과): 같은 9-cell threshold grid(9칸 임계값 격자) "
        "확장이나 validation-guided filtering(검증 유도 필터링)을 반복하지 않습니다. Reopen condition(재개 조건): 새 edge-quality/risk mechanism"
        "(엣지 품질/위험 메커니즘)이 density transfer(빈도 전이)를 입력 단서로만 사용할 때.\n"
    )


def primary_kpi_text(best: dict[str, Any], primary: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"best_val_pf={fmt(best.get('validation_profit_factor'))};"
        f"best_val_density={fmt(best.get('validation_trades_per_day'))};"
        f"best_val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"best_oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"best_oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"best_oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"primary={primary.get('candidate_id', 'none')};"
        f"primary_val_pf={fmt(primary.get('validation_profit_factor'))};"
        f"primary_oos_pf={fmt(primary.get('oos_profit_factor'))}"
    )


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


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return math.nan
    return number


def close_float(left: Any, right: Any, *, tolerance: float) -> bool:
    lnum = as_float(left)
    rnum = as_float(right)
    if not math.isfinite(lnum) or not math.isfinite(rnum):
        return False
    return abs(lnum - rnum) <= tolerance


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def fmt(value: Any) -> str:
    number = as_float(value)
    if not math.isfinite(number):
        return "n/a"
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
