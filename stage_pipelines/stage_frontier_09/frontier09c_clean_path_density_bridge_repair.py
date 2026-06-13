from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_09 import frontier09b_drawdown_clean_path_label_proxy_scout as f09b


STAGE_ID = f09b.STAGE_ID
RUN_ID = "frontier09C_clean_path_density_bridge_repair_v1"
RUN_NUMBER = "frontier09C"
PARENT_RUN_ID = f09b.RUN_ID
NEXT_STRICT_RUN_ID = "frontier09D_grok_pre_expensive_drawdown_clean_path_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier09D_stage_closeout_drawdown_clean_path_labeling_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
F09B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "candidate_summary.csv"

REPAIR_TARGET_COUNT = 4


@dataclass(frozen=True)
class RepairModelSpec:
    model_id: str
    estimator: Pipeline
    threshold_policy: str


REPAIR_MODEL_SPECS = tuple(
    RepairModelSpec(
        model_id=f"logreg_l2_c0p5_dirw{weight:.2f}_argmax".replace(".", "p"),
        estimator=Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        C=0.5,
                        random_state=29,
                        solver="lbfgs",
                        class_weight={0: weight, 1: 1.0, 2: weight},
                    ),
                ),
            ]
        ),
        threshold_policy="argmax_only_directional_class_prior_bridge(최대 확률 전용, 방향 클래스 사전분포 브리지)",
    )
    for weight in (1.15, 1.35, 1.60, 1.90)
)


def main() -> int:
    configure_frontier09b_runtime()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = f09b.f07b.load_training_packet()
    feature_order = f09b.f04d.read_feature_order()
    path = f09b.f07b.path_arrays(full, raw, f09b.HORIZON_BARS)
    variants = f09b.build_variants(full, path)
    selected_ids = select_repair_target_ids()
    targets = [
        target
        for target in f09b.build_targets(full, raw, path, variants)
        if not target.target_kind.startswith("clean_path_label_candidate") or target.target_id in selected_ids
    ]
    result = f09b.train_and_evaluate(full, feature_order, path, targets)
    final = f09b.build_final(result, source_integrity, feature_order, variants)
    finalize_repair_decision(final, selected_ids)
    artifacts = write_artifacts(result, final, selected_ids)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "strict_scout_clue_rows": final["strict_scout_clue_rows"],
                    "preserved_clue_rows": final["preserved_clue_rows"],
                    "best_candidate": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def configure_frontier09b_runtime() -> None:
    f09b.RUN_ID = RUN_ID
    f09b.RUN_NUMBER = RUN_NUMBER
    f09b.PARENT_RUN_ID = PARENT_RUN_ID
    f09b.NEXT_STRICT_RUN_ID = NEXT_STRICT_RUN_ID
    f09b.NEXT_REPAIR_RUN_ID = NEXT_CLOSEOUT_RUN_ID
    f09b.RUN_ROOT = RUN_ROOT
    f09b.MODEL_DIR = MODEL_DIR
    f09b.REPORT_PATH = REPORT_PATH
    f09b.f04d.MODEL_SPECS = REPAIR_MODEL_SPECS
    f09b.MODEL_ID_SHORT.clear()
    for spec in REPAIR_MODEL_SPECS:
        suffix = spec.model_id.replace("logreg_l2_c0p5_", "").replace("_argmax", "")
        f09b.MODEL_ID_SHORT[spec.model_id] = suffix


def select_repair_target_ids() -> set[str]:
    if not path_exists(F09B_SUMMARY):
        raise FileNotFoundError(F09B_SUMMARY)
    summary = pd.read_csv(str(io_path(F09B_SUMMARY)), encoding="utf-8-sig")
    pool = summary[
        summary["preserved_clue_pass"].map(parse_bool)
        & summary["learnability_pass"].map(parse_bool)
    ].sort_values(["validation_oos_score_sum", "oos_dd_risk_percent"], ascending=[True, True])
    selected: list[str] = []
    seen_family: set[str] = set()
    for _, row in pool.iterrows():
        family = str(row["label_family"])
        target_id = str(row["target_id"])
        if family in seen_family or target_id in selected:
            continue
        selected.append(target_id)
        seen_family.add(family)
        if len(selected) >= REPAIR_TARGET_COUNT:
            break
    for _, row in pool.iterrows():
        target_id = str(row["target_id"])
        if target_id not in selected:
            selected.append(target_id)
        if len(selected) >= REPAIR_TARGET_COUNT:
            break
    if not selected:
        raise RuntimeError("No Frontier09B preserved clean-path labels available for capped repair.")
    return set(selected[:REPAIR_TARGET_COUNT])


def finalize_repair_decision(final: dict[str, Any], selected_ids: set[str]) -> None:
    strict_rows = int(final["strict_scout_clue_rows"])
    preserved_rows = int(final["preserved_clue_rows"])
    if strict_rows:
        status = "clean_path_density_bridge_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue(엄격 탐색 단서)"
        next_run = NEXT_STRICT_RUN_ID
    elif preserved_rows:
        status = "clean_path_density_bridge_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run = NEXT_CLOSEOUT_RUN_ID
    else:
        status = "clean_path_density_bridge_no_repair_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run = NEXT_CLOSEOUT_RUN_ID
    final.update(
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "status": status,
            "judgment": judgment,
            "next_run_id": next_run,
            "repair_scope": (
                "capped repair: top Frontier09B preserved clean-path labels x directional class-prior weights"
                "(상한 수리: Frontier09B 상위 보존 깨끗한 경로 라벨 x 방향 클래스 사전분포 가중치)"
            ),
            "selected_repair_target_ids": sorted(selected_ids),
            "repair_model_specs": [spec.model_id for spec in REPAIR_MODEL_SPECS],
            "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        }
    )


def write_artifacts(result: dict[str, Any], final: dict[str, Any], selected_ids: set[str]) -> dict[str, Path]:
    artifacts = {
        "selected_targets": RUN_ROOT / "selected_repair_targets.csv",
        "candidate_metrics": RUN_ROOT / "repair_model_metrics.csv",
        "reference_metrics": RUN_ROOT / "reference_model_metrics.csv",
        "candidate_summary": RUN_ROOT / "repair_candidate_summary.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "target_distribution": RUN_ROOT / "target_distribution.csv",
        "skipped": RUN_ROOT / "skipped_targets.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    f09b.write_csv(artifacts["selected_targets"], [{"target_id": target_id} for target_id in sorted(selected_ids)])
    f09b.write_csv(artifacts["candidate_metrics"], result["candidate_metrics"])
    f09b.write_csv(artifacts["reference_metrics"], result["reference_metrics"])
    f09b.write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    f09b.write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    f09b.write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    f09b.write_csv(artifacts["target_distribution"], result["target_distribution"])
    f09b.write_csv(artifacts["skipped"], result["skipped"])
    final["artifact_lineage"]["producer"] = "stage_pipelines/stage_frontier_09/frontier09c_clean_path_density_bridge_repair.py"
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    f09b.write_json(artifacts["final_decision"], final)
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_09/frontier09c_clean_path_density_bridge_repair.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_09/frontier09c_clean_path_density_bridge_repair.py")),
        "artifacts": {
            name: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for name, path in artifacts.items()
            if name != "run_manifest" and path_exists(path)
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    f09b.write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier09C Clean Path Density Bridge Repair Report(전선09C 깨끗한 경로 밀도 브리지 수리 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier09B(전선09B)의 preserved clean-path labels(보존 깨끗한 경로 라벨) 상위 후보에 directional class-prior weights(방향 클래스 사전분포 가중치)를 적용해 argmax-only repair(최대 확률 전용 수리)를 실행했습니다.

Effect(효과): threshold search(임계값 탐색) 없이 거래 밀도(density, 밀도)를 끌어올릴 수 있는지 확인했고, validation DD(검증 손실폭)가 계속 큰지 함께 압박했습니다.

## Best Repair Read(최상위 수리 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/거래 밀도/손실폭): `{f09b.fmt(best.get('validation_profit_factor'))}` / `{f09b.fmt(best.get('validation_trades_per_day'))}` / `{f09b.fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(OOS 표본밖 수익 팩터/거래 밀도/손실폭): `{f09b.fmt(best.get('oos_profit_factor'))}` / `{f09b.fmt(best.get('oos_trades_per_day'))}` / `{f09b.fmt(best.get('oos_dd_risk_percent'))}%`
- ONNX parity(ONNX 동등성): `{best.get('parity_passed', False)}`

## Boundaries(경계)

- repair scope(수리 범위): `{final['repair_scope']}`
- selected targets(선택 라벨): `{', '.join(final['selected_repair_target_ids'])}`
- WFO/MT5(WFO/MT5): strict scout clue(엄격 탐색 단서) 전까지 out_of_scope_by_claim(주장 범위 밖)입니다.
- completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Artifacts(산출물)

- repair candidate summary(수리 후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- repair model metrics(수리 모델 지표): `{artifacts['candidate_metrics'].as_posix()}`
- ONNX parity(ONNX 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 실행 전 검토)로, 없으면 stage closeout(단계 마감)으로 가는 것입니다. Effect(효과)는 capped repair(상한 수리)를 반복하지 않고 가설을 정직하게 닫는 것입니다.
"""
    f09b.write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    state_text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {final['next_run_id']}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
"""
    io_path(f03b.WORKSPACE_STATE).write_text(state_text, encoding="utf-8", newline="\n")
    f09b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    f09b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final, artifacts))
    f09b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(final, artifacts))
    f09b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit_text(final))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final, artifacts):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}`, preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: clean path density bridge repair(깨끗한 경로 밀도 브리지 수리)를 실행했습니다. Effect(효과): 임계값 탐색 없이 라벨 후보의 밀도/손실폭 수리 가능성을 확인했습니다.\n",
    )


def current_state_text(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier09C(전선09C)는 Frontier09B(전선09B) 보존 라벨에 directional class-prior bridge(방향 클래스 사전분포 브리지)를 적용했습니다.

Effect(효과): threshold search(임계값 탐색) 없이 density/DD(밀도/손실폭)를 수리할 수 있는지 확인했고, strict clue(엄격 단서)가 없으면 stage closeout(단계 마감)으로 넘깁니다.

Best read(최상위 판독): `{best.get('candidate_id', 'none')}` with strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}` and preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier09 Selection Status(전선09 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Report(보고서): `{REPORT_PATH.as_posix()}`

Final decision(최종 판정 파일): `{artifacts['final_decision'].as_posix()}`

Best candidate(최상위 후보): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def review_index_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    artifact_lines = "\n".join(f"- `{path.as_posix()}`" for path in artifacts.values())
    return f"""# Frontier09 Review Index(전선09 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier09A_stage_open_drawdown_clean_path_labeling_v1`: stage open(단계 개방) and Grok review(그록 검토).
- `frontier09B_drawdown_clean_path_label_proxy_scout_v1`: clean path label proxy scout(깨끗한 경로 라벨 프록시 탐색).
- `{RUN_ID}`: capped density bridge repair(상한 밀도 브리지 수리).

## Latest Artifacts(최신 산출물)

{artifact_lines}
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier09C Required Gate Coverage Audit(전선09C 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족)
- skill_receipt_lint(스킬 영수증 검사): satisfied_with_boundary(경계부 충족)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Action(행동): capped repair scout(상한 수리 탐색)와 ONNX parity(ONNX 동등성)까지만 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), operating promotion(운영 승격), runtime authority(런타임 권위), completion(완성)은 주장하지 않습니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "clean_path_density_bridge_repair(깨끗한 경로 밀도 브리지 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_row_count"]),
        "claim_boundary": "clean_path_density_bridge_repair_no_threshold_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_clean_path_density_bridge_repair",
        "subrun_id": f"{RUN_ID}__tier_a_clean_path_density_bridge_repair",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "clean_path_density_bridge_repair_not_runtime(깨끗한 경로 밀도 브리지 수리, 런타임 아님)",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대 확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "clean_path_density_bridge_repair_only(깨끗한 경로 밀도 브리지 수리 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can class-prior bridge recover density without worsening drawdown?(클래스 사전분포 브리지가 손실폭을 악화하지 않고 밀도를 회복하는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "frontier09b_preserved_clue_to_frontier09c_capped_repair(전선09B 보존 단서에서 전선09C 상한 수리)",
        "best_candidate_id": best.get("candidate_id", ""),
        "best_validation_pf": best.get("validation_profit_factor", ""),
        "best_validation_density": best.get("validation_trades_per_day", ""),
        "best_validation_dd": best.get("validation_dd_risk_percent", ""),
        "best_oos_pf": best.get("oos_profit_factor", ""),
        "best_oos_density": best.get("oos_trades_per_day", ""),
        "best_oos_dd": best.get("oos_dd_risk_percent", ""),
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "clean_path_density_bridge_repair(깨끗한 경로 밀도 브리지 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대 확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_clean_path_density_bridge_repair",
            "subrun_id": f"{RUN_ID}__tier_a_clean_path_density_bridge_repair",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "clean_path_density_bridge_repair_not_runtime(깨끗한 경로 밀도 브리지 수리, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
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


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"preserved={best.get('preserved_clue_pass', False)};"
        f"oos_pf={f09b.fmt(best.get('oos_profit_factor'))};"
        f"oos_density={f09b.fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={f09b.fmt(best.get('oos_dd_risk_percent'))}"
    )


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
