from __future__ import annotations

import json
import math
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
from stage_pipelines.stage_frontier_03 import frontier03c_regime_asymmetric_label_micro_search as f03c
from stage_pipelines.stage_frontier_03 import frontier03d_regime_asymmetric_label_model_repair as f03d
from stage_pipelines.stage_frontier_03 import frontier03e_bounded_two_teacher_density_repair as f03e
from stage_pipelines.stage_frontier_03 import materialize_frontier03f_stage_closeout_grok_review as f03f


STAGE_ID = f03b.STAGE_ID
RUN_ID = "frontier03G_stage_closeout_v1"
RUN_NUMBER = "frontier03G_closeout"
PARENT_RUN_ID = f03f.RUN_ID
NEXT_RUN_ID = "frontier04A_stage_open_new_hypothesis_design_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_03_regime_conditioned_asymmetric_onnx_labeling_closeout.md")

MANIFEST_03B = Path("stages") / STAGE_ID / "02_runs" / f03b.RUN_ID / "run_manifest.json"
MANIFEST_03C = Path("stages") / STAGE_ID / "02_runs" / f03c.RUN_ID / "run_manifest.json"
MANIFEST_03D = Path("stages") / STAGE_ID / "02_runs" / f03d.RUN_ID / "run_manifest.json"
MANIFEST_03E = Path("stages") / STAGE_ID / "02_runs" / f03e.RUN_ID / "run_manifest.json"
CLASSIFICATION_03F = Path("stages") / STAGE_ID / "02_runs" / f03f.RUN_ID / "grok_stage_closeout_classification.json"


def main() -> int:
    ensure_dirs()
    now = utc_now()
    evidence = load_evidence()
    closeout = build_closeout(now, evidence)
    gate = build_gate_audit(now, closeout, evidence)
    write_outputs(closeout, gate)
    update_docs_and_state(now, closeout, gate)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": closeout["status"],
                "judgment": closeout["judgment"],
                "stage_closeout_class": closeout["stage_closeout_class"],
                "gate_status": gate["status"],
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REPORT_PATH.parent, DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_evidence() -> dict[str, Any]:
    required = [MANIFEST_03B, MANIFEST_03C, MANIFEST_03D, MANIFEST_03E, CLASSIFICATION_03F]
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing closeout evidence(마감 근거 누락): {missing}")
    return {
        "frontier03b": read_json(MANIFEST_03B),
        "frontier03c": read_json(MANIFEST_03C),
        "frontier03d": read_json(MANIFEST_03D),
        "frontier03e": read_json(MANIFEST_03E),
        "frontier03f_grok": read_json(CLASSIFICATION_03F),
    }


def build_closeout(now: str, evidence: dict[str, Any]) -> dict[str, Any]:
    e = evidence["frontier03e"]
    d = evidence["frontier03d"]
    c = evidence["frontier03c"]
    b = evidence["frontier03b"]
    f = evidence["frontier03f_grok"]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": "closed_preserved_clue_plus_negative_memory_no_authority",
        "judgment": "stage_closed_preserved_clue_negative_memory_no_authority",
        "stage_closeout_class": "preserved_clue_plus_negative_memory(보존 단서+부정 기억)",
        "created_at_utc": now,
        "next_run_id": NEXT_RUN_ID,
        "grok_recommendation": f["recommendation_inferred"],
        "preserved_clue": {
            "teacher_variant_id": e["best_teacher_variant_id"],
            "candidate_id": e["best_candidate_id"],
            "side_mode": e["best_side_mode"],
            "threshold": e["best_probability_threshold"],
            "margin": e["best_probability_margin"],
            "cooldown_bars": e["best_cooldown_bars"],
            "oos_profit_factor": e["best_oos_profit_factor"],
            "oos_trades_per_day": e["best_oos_trades_per_day"],
            "oos_max_drawdown_percent": e["best_oos_max_drawdown_percent"],
            "validation_profit_factor": e["best_validation_profit_factor"],
            "validation_trades_per_day": e["best_validation_trades_per_day"],
            "validation_max_drawdown_percent": e["best_validation_max_drawdown_percent"],
            "meaning": "OOS PF/DD clue only; validation fold and density are insufficient(표본밖 PF/DD 단서일 뿐, 검증 구간과 밀도는 부족)",
        },
        "negative_memory": [
            "Oracle label replay strength did not transfer into sufficient trainable ONNX joint KPI(오라클 라벨 재생 강도가 충분한 학습 가능 온엑스 동시 KPI로 전달되지 않음).",
            "Decision-surface-only repair increased density but worsened DD sharply(결정 표면만 수리하면 밀도는 올라도 손실폭이 크게 악화됨).",
            "Two-teacher repair produced zero success rows under the precheck criteria(두 교사 수리는 사전 점검 기준 성공 행 0개).",
            "Validation fold remained weak even when OOS PF/DD improved(표본밖 PF/DD가 좋아져도 검증 구간은 약함).",
        ],
        "do_not_repeat": [
            "Do not repeat broad threshold/margin/cooldown sweeps on the same single teacher(같은 단일 교사에서 넓은 임계값/마진/쿨다운 스윕 반복 금지).",
            "Do not treat oracle PF 999 and DD 0 as trainable ONNX promise(오라클 PF 999와 DD 0을 학습 가능 온엑스 약속으로 해석 금지).",
            "Do not open WFO/MT5 for this hypothesis without joint KPI precheck eligibility(동시 KPI 사전 점검 적격 없이는 이 가설 WFO/MT5 금지).",
            "Do not inherit this clue as winner, baseline, promotion, or authority(이 단서를 승자/기준선/승격/권위로 상속 금지).",
        ],
        "frontier03b_best": {
            "variant_id": b["best_variant_id"],
            "oos_profit_factor": b["best_oos_profit_factor"],
            "oos_trades_per_day": b["best_oos_trades_per_day"],
            "oos_max_drawdown_percent": b["best_oos_max_drawdown_percent"],
            "boundary": "oracle_label_proxy_only(오라클 라벨 프록시 전용)",
        },
        "frontier03c_best": {
            "onnx_sha256": c["onnx_sha256"],
            "onnx_parity_passed": c["onnx_parity"]["passed"],
            "oos_profit_factor": c["best_oos_profit_factor"],
            "oos_trades_per_day": c["best_oos_trades_per_day"],
            "oos_max_drawdown_percent": c["best_oos_max_drawdown_percent"],
        },
        "frontier03d_best": {
            "repair_success_rows": d["repair_success_rows"],
            "oos_profit_factor": d["best_oos_profit_factor"],
            "oos_trades_per_day": d["best_oos_trades_per_day"],
            "oos_max_drawdown_percent": d["best_oos_max_drawdown_percent"],
        },
        "frontier03e_best": {
            "teacher_repair_success_rows": e["teacher_repair_success_rows"],
            "teacher_repair_stop_candidate_rows": e["teacher_repair_stop_candidate_rows"],
            "oos_profit_factor": e["best_oos_profit_factor"],
            "oos_trades_per_day": e["best_oos_trades_per_day"],
            "oos_max_drawdown_percent": e["best_oos_max_drawdown_percent"],
            "validation_profit_factor": e["best_validation_profit_factor"],
            "validation_trades_per_day": e["best_validation_trades_per_day"],
            "validation_max_drawdown_percent": e["best_validation_max_drawdown_percent"],
        },
        "artifacts": artifact_identities(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def artifact_identities() -> dict[str, dict[str, Any]]:
    paths = {
        "frontier03b_manifest": MANIFEST_03B,
        "frontier03c_manifest": MANIFEST_03C,
        "frontier03d_manifest": MANIFEST_03D,
        "frontier03e_manifest": MANIFEST_03E,
        "frontier03f_grok_classification": CLASSIFICATION_03F,
        "frontier03f_grok_output": f03f.OUTPUT_PATH,
    }
    return {
        name: {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else None}
        for name, path in paths.items()
    }


def build_gate_audit(now: str, closeout: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    forbidden_claims = ("completion", "baseline", "promotion", "runtime_authority", "live_readiness", "goal_achieve")
    e = evidence["frontier03e"]
    f = evidence["frontier03f_grok"]
    checks = {
        "grok_closeout_review_captured": bool(f.get("metadata_success")) and "closeout_preserved" in f.get("recommendation_inferred", ""),
        "bounded_repair_exhausted": int(e["teacher_repair_success_rows"]) == 0 and int(e["trained_models"]) == 2,
        "expensive_validation_not_opened": True,
        "preserved_clue_named": bool(closeout["preserved_clue"]["candidate_id"]),
        "negative_memory_named": len(closeout["negative_memory"]) >= 3,
        "forbidden_claims_not_claimed": all(value == "not_claimed(주장 없음)" for value in closeout["claim_boundary"].values()),
    }
    status = "pass" if all(checks.values()) else "blocked"
    return {
        "audit_name": "frontier03_stage_closeout_gate(전선03 단계 마감 게이트)",
        "status": status,
        "created_at_utc": now,
        "required_gates": [
            "grok_stage_closeout_review(그록 단계 마감 검토)",
            "bounded_repair_exhaustion(상한 수리 소진)",
            "artifact_lineage(산출물 계보)",
            "final_claim_guard(최종 주장 방지)",
            "state_sync_update(상태 동기화 갱신)",
        ],
        "checks": checks,
        "allowed_claims": [
            "stage_closed_preserved_clue_negative_memory(단계가 보존 단서+부정 기억으로 닫힘)",
            "no_authority(권위 없음)",
        ],
        "forbidden_claims": list(forbidden_claims),
    }


def write_outputs(closeout: dict[str, Any], gate: dict[str, Any]) -> None:
    paths = {
        "stage_closeout_summary": RUN_ROOT / "stage_closeout_summary.json",
        "closeout_gate_audit": RUN_ROOT / "closeout_gate_audit.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_json(paths["stage_closeout_summary"], closeout)
    write_json(paths["closeout_gate_audit"], gate)
    write_text_sig(REPORT_PATH, report_text(closeout, gate))
    write_text_sig(DECISION_PATH, decision_text(closeout))
    outputs = {
        "stage_closeout_summary": {"path": paths["stage_closeout_summary"].as_posix(), "sha256": sha256_file(paths["stage_closeout_summary"])},
        "closeout_gate_audit": {"path": paths["closeout_gate_audit"].as_posix(), "sha256": sha256_file(paths["closeout_gate_audit"])},
        "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
        "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
    }
    manifest = {
        **closeout,
        "script_path": "stage_pipelines/stage_frontier_03/materialize_frontier03g_stage_closeout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_03/materialize_frontier03g_stage_closeout.py")),
        "gate_audit": gate,
        "outputs": outputs,
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(paths["run_manifest"], manifest)


def update_docs_and_state(now: str, closeout: dict[str, Any], gate: dict[str, Any]) -> None:
    f03b.append_once(
        Path("stages") / STAGE_ID / "03_reviews" / "review_index.md",
        RUN_ID,
        f"- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{closeout['judgment']}`\n",
    )
    f03b.write_text_sig(Path("stages") / STAGE_ID / "04_selected" / "selection_status.md", selection_text(now, closeout, gate))
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": closeout["status"],
        "current_judgment": closeout["judgment"],
        "stage_closeout_class": closeout["stage_closeout_class"],
        "next_run_id": NEXT_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(now, closeout, gate))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, closeout, gate))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(closeout, gate))
    f03b.upsert_csv(Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(closeout, gate))
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` closed Frontier03(전선03 마감) as preserved clue plus negative memory(보존 단서+부정 기억). Effect(효과): next run(다음 실행)은 `{NEXT_RUN_ID}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: Frontier03(전선03) closeout(마감). Preserved clue(보존 단서)는 `{closeout['preserved_clue']['candidate_id']}`이고, negative memory(부정 기억)는 oracle-to-ONNX transfer gap(오라클에서 온엑스 전달 격차)입니다. Effect(효과): 다음 frontier(전선)는 reference only(참조 전용)로만 사용할 수 있습니다.\n",
    )


def report_text(closeout: dict[str, Any], gate: dict[str, Any]) -> str:
    clue = closeout["preserved_clue"]
    negative = "\n".join(f"- {item}" for item in closeout["negative_memory"])
    repeat = "\n".join(f"- {item}" for item in closeout["do_not_repeat"])
    return f"""# Frontier03G Stage Closeout Report(전선03G 단계 마감 보고서)

Updated(갱신): {closeout['created_at_utc']}

Status(상태): `{closeout['status']}`

Judgment(판정): `{closeout['judgment']}`

Closeout class(마감 분류): `{closeout['stage_closeout_class']}`

Gate status(게이트 상태): `{gate['status']}`

## Preserved Clue(보존 단서)

- candidate(후보): `{clue['candidate_id']}`
- teacher(교사): `{clue['teacher_variant_id']}`
- surface(표면): threshold/margin/cooldown(임계값/마진/쿨다운) `{clue['threshold']}` / `{clue['margin']}` / `{clue['cooldown_bars']}`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(clue['oos_profit_factor'])}` / `{fmt(clue['oos_trades_per_day'])}/day` / `{fmt(clue['oos_max_drawdown_percent'])}%`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(clue['validation_profit_factor'])}` / `{fmt(clue['validation_trades_per_day'])}/day` / `{fmt(clue['validation_max_drawdown_percent'])}%`

Plain read(쉬운 판독): OOS PF/DD(표본밖 수익 팩터/손실폭)는 clue(단서)이지만 density(밀도)와 validation fold(검증 구간)가 부족해 precheck(사전 점검)로 가지 않습니다.

## Negative Memory(부정 기억)
{negative}

## Do Not Repeat(반복 금지)
{repeat}

## Grok Review(그록 검토)

Recommendation(권고): `{closeout['grok_recommendation']}`

Effect(효과): Grok(그록) 조언은 local verification(로컬 검증) 뒤 accepted(수용)되었고, WFO/MT5(워크포워드/메타트레이더5)는 열지 않습니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 새 frontier stage(전선 단계)를 새 hypothesis(가설)로 여는 것입니다. Effect(효과)는 Frontier03(전선03)의 clue(단서)를 reference only(참조 전용)로 보존하고 inheritance(상속)를 막는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def decision_text(closeout: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier03 Closeout(전선03 마감)

Date(날짜): 2026-06-14

Decision(결정): Frontier03(전선03)은 preserved clue plus negative memory(보존 단서+부정 기억)로 닫는다.

Reason(이유): bounded repair(상한 있는 수리) 안에서 success rows(성공 행)가 0개였고, Grok closeout review(그록 마감 검토)가 closeout(마감)을 수용했다.

Preserved clue(보존 단서): `{closeout['preserved_clue']['candidate_id']}`.

Boundary(경계): winner(승자), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def selection_text(now: str, closeout: dict[str, Any], gate: dict[str, Any]) -> str:
    return f"""# Stage Frontier 03 Selection Status(전선 03단계 선택 상태)

Updated(갱신): {now}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage status(단계 상태): `{closeout['status']}`

Judgment(판정): `{closeout['judgment']}`

Gate status(게이트 상태): `{gate['status']}`

Preserved clue(보존 단서): `{closeout['preserved_clue']['candidate_id']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def current_state_text(now: str, closeout: dict[str, Any], gate: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier03(전선03)은 preserved clue plus negative memory(보존 단서+부정 기억)로 닫혔습니다.

Judgment(판정): `{closeout['judgment']}`

Gate status(게이트 상태): `{gate['status']}`

Preserved clue(보존 단서): `{closeout['preserved_clue']['candidate_id']}` with OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `{fmt(closeout['preserved_clue']['oos_profit_factor'])}` / `{fmt(closeout['preserved_clue']['oos_trades_per_day'])}/day` / `{fmt(closeout['preserved_clue']['oos_max_drawdown_percent'])}%`.

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 새 frontier stage(전선 단계)를 새 hypothesis(가설)로 여는 것입니다. Effect(효과)는 Frontier03(전선03)을 reference only(참조 전용)로 남기고 winner/baseline/promotion(승자/기준선/승격) 상속을 막는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(now: str, closeout: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": closeout["status"],
        "judgment": closeout["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"closeout_class={closeout['stage_closeout_class']};gate={gate['status']};no_authority",
        "work_family": "stage_transition(단계 전환)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "stage_closed_preserved_clue_negative_memory_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "not_applicable_closeout(마감에는 해당 없음)",
        "kpi_scope": "closeout_summary_no_new_trades(마감 요약, 새 거래 없음)",
        "primary_kpi": f"preserved_oos_pf={fmt(closeout['preserved_clue']['oos_profit_factor'])};density={fmt(closeout['preserved_clue']['oos_trades_per_day'])};dd={fmt(closeout['preserved_clue']['oos_max_drawdown_percent'])}",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "stage_closeout_summary.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_reference_only(단계 마감, 참조 전용)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "How did Frontier03 close after capped repair?(상한 수리 뒤 전선03은 어떻게 닫혔는가?)",
        "skill_family": "stage_transition(단계 전환)",
        "lineage_summary": "frontier03b_to_03g_closeout(전선03B에서 03G 마감)",
    }


def ledger_row(closeout: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "not_applicable_closeout(마감에는 해당 없음)",
        "kpi_scope": "closeout_summary_no_new_trades(마감 요약, 새 거래 없음)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": closeout["status"],
        "judgment": closeout["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"preserved_oos_pf={fmt(closeout['preserved_clue']['oos_profit_factor'])};density={fmt(closeout['preserved_clue']['oos_trades_per_day'])};dd={fmt(closeout['preserved_clue']['oos_max_drawdown_percent'])}",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "notes": f"closeout_class={closeout['stage_closeout_class']};gate={gate['status']};next={NEXT_RUN_ID};no_authority",
    }


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def num(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    return f"{num(value):.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
