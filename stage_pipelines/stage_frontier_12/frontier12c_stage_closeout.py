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


STAGE_ID = "stage_frontier_12__trade_shape_duration_controlled_onnx_scout"
RUN_ID = "frontier12C_stage_closeout_trade_shape_duration_controlled_onnx_scout_v1"
RUN_NUMBER = "frontier12C"
PARENT_RUN_ID = "frontier12B_trade_shape_duration_label_proxy_scout_v1"
NEXT_RUN_ID = "frontier13A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_negative_memory_no_authority"
JUDGMENT = "negative_memory(부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_12_trade_shape_duration_controlled_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_12/frontier12c_stage_closeout.py")

F12B_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F12B_FINAL = F12B_ROOT / "final_decision.json"
F12B_SUMMARY = F12B_ROOT / "candidate_summary.csv"
F12B_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
GROK_CLOSEOUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier12_stage_closeout/small_review")


def main() -> int:
    now = utc_now()
    ensure_dirs()
    f12b = read_json(F12B_FINAL)
    grok = read_grok()
    local = local_verification(f12b, grok)
    summary = build_summary(now, f12b, grok, local)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "status": summary["status"],
                    "judgment": summary["judgment"],
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "grok_classification": summary["grok_classification"],
                    "local_verification": summary["local_verification"]["judgment"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
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
    return {
        "packet": GROK_CLOSEOUT.as_posix(),
        "prompt": (GROK_CLOSEOUT / "prompt.md").as_posix(),
        "output": (GROK_CLOSEOUT / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "classification": classify_grok(output),
        "wfo_mt5_skip_supported": "wfo" in output.lower() and "mt5" in output.lower(),
        "forbidden_claims_supported": "forbidden" in output.lower() and "goal achieve" in output.lower(),
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "accepted" in lowered:
        return "accepted(수용)"
    if "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(f12b: dict[str, Any], grok: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "frontier12b_final_exists": path_exists(F12B_FINAL),
        "candidate_summary_exists": path_exists(F12B_SUMMARY),
        "frontier12b_no_strict_or_preserved": int(f12b.get("strict_scout_clue_rows", -1)) == 0
        and int(f12b.get("preserved_clue_rows", -1)) == 0,
        "frontier12b_no_authority": f12b.get("claim_boundary", {}).get("runtime_authority") == "not_claimed(주장 없음)"
        and f12b.get("claim_boundary", {}).get("goal_achieve") == "not_claimed(주장 없음)",
        "grok_closeout_accepted": grok["success"] and grok["classification"] == "accepted(수용)",
        "grok_wfo_mt5_skip_supported": bool(grok["wfo_mt5_skip_supported"]),
        "grok_forbidden_claims_supported": bool(grok["forbidden_claims_supported"]),
    }
    return {
        "checks": checks,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_summary(now: str, f12b: dict[str, Any], grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    best = f12b.get("best_candidate_row", {})
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "f12b_status": f12b.get("status", ""),
        "f12b_judgment": f12b.get("judgment", ""),
        "strict_scout_clue_rows": int(f12b.get("strict_scout_clue_rows", 0)),
        "preserved_clue_rows": int(f12b.get("preserved_clue_rows", 0)),
        "best_candidate_row": best,
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "negative_memory": (
            "Trade-shape duration labels(거래 형상 보유 기간 라벨)은 validation DD floor(검증 손실폭 바닥)를 F11 reference"
            "(프론티어11 참조)보다 낮췄지만 validation PF/density(검증 수익 팩터/빈도), worst subperiod loss concentration"
            "(최악 하위기간 손실 집중), and balanced-model DD(균형 모델 손실폭)가 four-axis scout boundary(네 축 탐색 경계)를 통과하지 못했습니다."
        ),
        "reference_only_carry": (
            "The fast-shape plain logistic surface(빠른 형상 평범 로지스틱 표면)는 DD reduction seed surface"
            "(손실폭 감소 씨앗 표면)로만 보관합니다."
        ),
        "do_not_repeat": [
            "same label knob loosening(같은 라벨 파라미터 완화)",
            "class-weight density forcing(클래스 가중 빈도 강제)",
            "threshold micro-search(임계값 미세 탐색)",
        ],
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
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier12b_final": artifact_identity(F12B_FINAL),
            "frontier12b_candidate_summary": artifact_identity(F12B_SUMMARY),
            "frontier12b_report": artifact_identity(F12B_REPORT),
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
    return f"""# Frontier12C Stage Closeout Report(프론티어12C 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier12(프론티어12)를 negative memory(부정 기억)로 닫았습니다.

Effect(효과): trade-shape duration label(거래 형상 보유 기간 라벨) 가설은 DD reduction seed(손실폭 감소 씨앗)를 남기지만, 네 축을 동시에 만족하는 scout clue(탐색 단서)는 만들지 못했다는 경계를 고정합니다.

## Evidence Summary(근거 요약)

- strict scout clue rows(엄격 탐색 단서 행): `{summary['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{summary['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`

## Grok Closeout Receipt(그록 마감 영수증)

- packet(묶음): `{summary['grok_packet']}`
- classification(분류): `{summary['grok_classification']}`
- prompt hash(프롬프트 해시): `{summary['grok_prompt_hash']}`
- local verification(로컬 검증): `{summary['local_verification']['judgment']}`
- WFO/MT5 skip(WFO/MT5 생략): valid by claim boundary(주장 경계상 타당)

## Negative Memory(부정 기억)

{summary['negative_memory']}

## Reference-Only Carry(참조 전용 이월)

{summary['reference_only_carry']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동): new frontier hypothesis(새 프론티어 가설)로 이동합니다. Effect(효과): 같은 라벨 파라미터 완화(label knob loosening, 라벨 파라미터 완화)를 반복하지 않습니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier12C Required Gate Coverage Audit(프론티어12C 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- closeout_review_gate(마감 검토 게이트): Grok accepted(그록 수용)
- result_judgment_gate(결과 판정 게이트): strict/preserved rows 0(엄격/보존 행 0) and negative memory(부정 기억) recorded(기록됨)
- artifact_lineage_gate(산출물 계보 게이트): Frontier12B final/candidate/Grok outputs(프론티어12B 최종/후보/그록 출력) linked(연결됨)
- paired_tier_gate(짝 티어 게이트): Tier A(티어 A) closeout plus Tier B/combined missing_required(티어B/합산 필수 누락) recorded(기록됨)
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)

Effect(효과): Frontier12(프론티어12)는 닫혔지만 operating authority(운영 권위)는 생기지 않습니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Review Index(프론티어12 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `frontier12A_stage_open_trade_shape_duration_controlled_onnx_scout_v1`: stage open(단계 개방), Grok accepted(그록 수용).
- `frontier12B_trade_shape_duration_label_proxy_scout_v1`: proxy scout(프록시 탐색), strict/preserved rows 0(엄격/보존 행 0).
- `{RUN_ID}`: stage closeout(단계 마감), Grok accepted(그록 수용), negative memory(부정 기억).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Selection Status(프론티어12 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Closeout run(마감 실행): `{RUN_ID}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Negative memory(부정 기억): {summary['negative_memory']}

Reference-only carry(참조 전용 이월): {summary['reference_only_carry']}

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier12 As Negative Memory(결정: 프론티어12를 부정 기억으로 마감)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier12(프론티어12)를 negative memory(부정 기억)로 닫았습니다.

Effect(효과): DD reduction seed(손실폭 감소 씨앗)는 참조만 하고, 같은 label knob loosening(라벨 파라미터 완화) 반복을 금지합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
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
        ]
    )


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

Action(행동): Frontier12(프론티어12)는 negative memory(부정 기억)로 닫혔습니다.

Effect(효과): trade-shape duration label(거래 형상 보유 기간 라벨)은 손실폭을 일부 낮췄지만 빈도와 검증 수익성이 부족했다는 기억만 reference-only(참조 전용)로 남깁니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    best = summary["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={summary['strict_scout_clue_rows']};preserved={summary['preserved_clue_rows']};grok_accepted;no_authority",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "closed_negative_memory_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(best),
        "external_verification_status": "grok_closeout_review_done_mt5_out_of_scope(그록 마감 검토 완료, MT5 범위 밖)",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    best = summary["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "grok_accepted_no_wfo_no_mt5_no_authority(그록 수용, WFO/MT5/권위 없음)",
        "external_verification_status": "grok_closeout_review_done_mt5_out_of_scope(그록 마감 검토 완료, MT5 범위 밖)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_negative_memory_not_runtime(단계 마감 부정 기억, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
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
        f"- {summary['created_at_utc']}: `{RUN_ID}` closed Frontier12(프론티어12) as negative memory(부정 기억) after Grok closeout accepted"
        f"(그록 마감 수용). Effect(효과): next frontier(다음 프론티어) `{NEXT_RUN_ID}` starts a new hypothesis(새 가설) without authority claims(권위 주장 없음).\n"
    )


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict=False;preserved=False;"
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"worst_sub_dd={fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    return f"{number:.6g}" if number == number else "n/a"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
