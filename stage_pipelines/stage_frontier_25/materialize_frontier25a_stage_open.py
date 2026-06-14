from __future__ import annotations

import csv
import hashlib
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
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_24 import frontier24d_stage_closeout as f24d


STAGE_ID = "stage_frontier_25__bridge_archetype_preselection_onnx_scout"
RUN_ID = "frontier25A_stage_open_bridge_archetype_preselection_hypothesis_design_v1"
RUN_NUMBER = "frontier25A"
PARENT_RUN_ID = f24d.RUN_ID
NEXT_RUN_ID = "frontier25B_bridge_archetype_preselection_proxy_scout_v1"
STATUS = "opened_frontier25_bridge_archetype_preselection_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_dd_headroom_first_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_25/materialize_frontier25a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier25_stage_open/small_review")

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_25_bridge_archetype_preselection_onnx_scout_open.md")

F24_SELECTION = Path("stages/stage_frontier_24__density_bridge_payoff_pockets_onnx_scout/04_selected/selection_status.md")
F24_PRESERVED = Path("stages/stage_frontier_24__density_bridge_payoff_pockets_onnx_scout/04_selected/preserved_clue.md")
F24_NEGATIVE = Path("stages/stage_frontier_24__density_bridge_payoff_pockets_onnx_scout/04_selected/negative_memory.md")
F24_CLOSEOUT = (
    Path("stages/stage_frontier_24__density_bridge_payoff_pockets_onnx_scout/03_reviews")
    / f"{f24d.RUN_ID}_report.md"
)
F24_STAGE_LEDGER = Path("stages/stage_frontier_24__density_bridge_payoff_pockets_onnx_scout/03_reviews/stage_run_ledger.csv")

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "changed_variable": "dd_headroom_first_bridge_archetype_preselection",
    "forbidden_primary_path": "density_first_bridge_score_or_posthoc_dd_repair_as_primary_proxy",
    "structural_unit": "same_side_pair_or_triple_entry_time_or_union",
    "duplicate_trade_rule": "one_trade_per_timestamp_when_multiple_pockets_fire",
    "opposite_side_rule": "do_not_mix_long_and_short_inside_one_archetype",
    "archetype_score_contract": (
        "train-only score includes per-pocket train DD cap, bridge train DD headroom to 18%, "
        "equity_trend_r2, overlap ratio, min unique contribution, family diversity, and 5-10/day density"
    ),
    "non_repeat_proof": "compare top10 micro_id keys against Frontier24B top10 and require DD-headroom lift if overlap exists",
    "no_repair_in_frontier25b": "F25B must test preselection only; capped repair is not allowed in the primary proxy path",
    "no_lifecycle_until_seed": "no lifecycle repair until a seed or handoff worthy proxy exists",
    "no_onnx_until_handoff": "no model training or ONNX branch until handoff candidate exists",
}

CRITERIA = {
    "scout_clue": {"pf": 1.10, "density_low": 5.0, "density_high": 10.0, "dd_cap": 25.0},
    "seed_surface": {"pf": 1.20, "density_low": 5.0, "density_high": 10.0, "dd_cap": 18.0},
    "handoff_candidate": {"pf": 1.50, "density_low": 5.0, "density_high": 10.0, "dd_cap": 12.0, "equity_trend_r2": 0.35},
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    feature_order = read_feature_order()
    grok = read_grok_packet()
    local = local_verification(feature_order, grok)
    if local["judgment"] != "pass_open_ready_with_dd_headroom_locks":
        raise RuntimeError(f"Frontier25A local verification failed: {json.dumps(local, ensure_ascii=False)}")
    summary = build_summary(created_at, feature_order, grok, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": grok["classification"],
        "local_verification": local["judgment"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs" / "active",
        STAGE_ROOT / "02_runs" / "archived",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_stage_ledger_header()


def ensure_stage_ledger_header() -> None:
    path = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(path):
        return
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_feature_order() -> list[str]:
    features = [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(features) != 58:
        raise ValueError(f"feature count mismatch: {len(features)}")
    return features


def read_grok_packet() -> dict[str, Any]:
    metadata = read_json(GROK_PACKET / "metadata.json")
    output = read_text(GROK_PACKET / "clean_output.md")
    return {
        "packet": GROK_PACKET.as_posix(),
        "prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "output": (GROK_PACKET / "clean_output.md").as_posix(),
        "metadata": (GROK_PACKET / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "output_excerpt": output[:2800],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)"
    if "acceptable_new_hypothesis" in lowered and "accepted" in lowered:
        return "accepted_acceptable_new_hypothesis(수용, 허용 가능한 새 가설)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    if "accepted" in lowered:
        return "accepted(수용)"
    return "classification_missing(분류 누락)"


def local_verification(feature_order: list[str], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f24_selection = read_text(F24_SELECTION)
    f24_preserved = read_text(F24_PRESERVED)
    f24_negative = read_text(F24_NEGATIVE)
    f24_closeout = read_text(F24_CLOSEOUT)
    f24_ledger = read_text(F24_STAGE_LEDGER)
    grok_text = read_text(GROK_PACKET / "clean_output.md")
    feature_hash = ordered_hash(feature_order)
    checks = {
        "workspace_current_stage_frontier24_closed": f"current_stage_id: {f24d.STAGE_ID}" in workspace
        and "closed_preserved_clue_negative_memory_density_bridge_dd_repair_scout_no_handoff" in workspace,
        "workspace_next_run_frontier25a": f"next_run_id: {RUN_ID}" in workspace,
        "f24_selection_no_authority": "no selected baseline" in f24_selection.lower()
        and "Runtime probe blocker" in f24_selection,
        "f24_preserved_bridge_scouts": all(anchor in f24_preserved for anchor in ("f24b_0174", "f24c_0105", "f24c_0163")),
        "f24_negative_reopen_archetype": "bridge archetype pre-selection" in f24_negative,
        "f24_closeout_metrics_anchors": all(anchor in f24_closeout for anchor in ("f24b_0174", "f24c_0105", "f24c_0163")),
        "f24_stage_ledger_seed_handoff_zero": "f24c_scout=3;seed=0;handoff=0" in f24_ledger,
        "feature_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepts_stage_open": grok["classification"] in {
            "accepted_acceptable_new_hypothesis(수용, 허용 가능한 새 가설)",
            "accepted(수용)",
            "needs_local_verification(로컬 검증 필요)",
        },
        "grok_locks_train_only": "Train-only selection" in grok_text or "train-only" in grok_text,
        "grok_locks_dd_headroom_first": "DD-headroom-first" in grok_text or "dd_headroom_first" in grok_text,
        "grok_blocks_repair_primary_path": "No repair in F25B" in grok_text or "no repair" in grok_text.lower(),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_open_ready_with_dd_headroom_locks" if all(checks.values()) else "needs_manual_review",
        "checks": checks,
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
    }


def build_summary(created_at: str, feature_order: list[str], grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "frontier_thesis": "DD-headroom-first bridge archetype pre-selection may find smoother 5-10/day OR-union entries before repair(손실폭 여유 우선 연결 원형 사전 선택이 수리 전에 더 매끄러운 일 5~10회 OR 합집합 진입을 찾을 수 있다)",
        "hypothesis": "F24 failed because it selected density first and repaired DD later; F25 flips the order and selects lower-risk bridge archetypes on train only(F24는 빈도 우선 선택 뒤 손실폭을 고쳤기 때문에 실패했고, F25는 학습 전용 낮은 위험 연결 원형을 먼저 고른다)",
        "decision_use": "decide whether headroom-first bridge construction deserves proxy repair, WFO, or runtime handoff consideration(손실폭 여유 우선 연결 구성이 프록시 수리/WFO/런타임 인계 검토 가치가 있는지 결정)",
        "comparison_baseline": "F24B density-first bridge and F24C post-hoc DD repair as reference-only, not baseline(F24B 빈도 우선 연결과 F24C 사후 손실폭 수리는 참조 전용이며 기준선 아님)",
        "control_variables": [
            "US100 M5 Tier A dataset(US100 5분봉 티어 A 데이터셋)",
            "feature_set_v2 58 features(피처 세트 v2 58개)",
            "fwd12 label horizon(fwd12 라벨 지평)",
            "same-side OR-union semantics(같은 방향 OR 합집합 의미)",
            "validation/OOS read-only(검증/표본외 읽기 전용)",
        ],
        "changed_variables": [
            "dd_headroom_first_preselection(손실폭 여유 우선 사전 선택)",
            "explicit F24B top10 non-repeat audit(F24B 상위10 반복 아님 감사)",
            "no primary repair in first proxy(첫 프록시 기본 경로 수리 없음)",
        ],
        "sample_scope": "Tier A US100 M5 model_input_dataset.parquet, train/validation/oos frozen split(티어 A US100 5분봉 고정 분할)",
        "success_criteria": {
            "scout": "validation and OOS PF>=1.10, density 5-10/day, max DD<=25%(검증/표본외 수익 팩터 1.10 이상, 일 5~10회, 최대 손실폭 25% 이하)",
            "seed": "PF>=1.20, density 5-10/day, max DD<=18%(수익 팩터 1.20 이상, 일 5~10회, 최대 손실폭 18% 이하)",
            "handoff": "PF>=1.50, density 5-10/day, max DD<=12%, smoothness proxy pass(수익 팩터 1.50 이상, 일 5~10회, 손실폭 12% 이하, 매끄러움 통과)",
        },
        "failure_criteria": [
            "no archetype passes train-only DD headroom filter(학습 전용 손실폭 여유 필터 통과 원형 없음)",
            "top rows repeat F24B keys without DD headroom lift(F24B 키 반복이며 손실폭 여유 개선 없음)",
            "all forward rows fail scout PF/DD/density(모든 전진 행이 탐색 수익 팩터/손실폭/빈도 실패)",
        ],
        "invalid_conditions": [
            "validation/OOS used in selection(검증/표본외 선택 사용)",
            "F25B applies capped repair as primary path(F25B가 상한 수리를 기본 경로로 적용)",
            "feature hash mismatch(피처 해시 불일치)",
        ],
        "stop_conditions": [
            "F25B has zero valid archetypes(F25B 유효 원형 0개)",
            "F25B is repeat without metric lift(F25B가 지표 개선 없는 반복)",
            "handoff rows >0 triggers Grok before expensive WFO/MT5(인계 행이 있으면 비싼 WFO/MT5 전 Grok 검토)",
            "no seed/handoff after capped repair closes as preserved clue or negative memory(상한 수리 뒤 씨앗/인계 없으면 보존 단서 또는 부정 기억으로 마감)",
        ],
        "locks": LOCKS,
        "criteria": CRITERIA,
        "grok": grok,
        "local_verification": local,
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "bridge_archetype_preselection_lock.json", {"locks": LOCKS, "criteria": CRITERIA})
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "bridge_archetype_preselection_lock_spec.md", lock_spec())
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index())
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_PACKET / "clean_output.md",
        F24_SELECTION,
        F24_PRESERVED,
        F24_NEGATIVE,
        F24_CLOSEOUT,
        RUN_ROOT / "stage_open_summary.json",
        REPORT_PATH,
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "feature_schema": {
            "feature_count": summary["feature_count"],
            "feature_order_hash": summary["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "rule_stack": {
            "entry": "same-side pair/triple OR-union bridge archetypes(같은 방향 쌍/삼중 OR 합집합 연결 원형)",
            "selection": "train-only DD-headroom-first preselection(학습 전용 손실폭 여유 우선 사전 선택)",
            "forbidden": "no validation selection, no F25B repair, no ONNX/MT5 before handoff(검증 선택 없음, F25B 수리 없음, 인계 전 ONNX/MT5 없음)",
        },
        "claim_boundary": summary["claim_boundary"],
    }


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier25_stage_open_grok_accepted_dd_headroom_first_contract_no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "guardrail_kpi": "dd_headroom_first_lock_no_model_training_no_wfo_no_mt5_no_authority(손실폭 여유 우선 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok={summary['grok']['classification']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "dd_headroom_first_lock_no_model_training_no_wfo_no_mt5_no_authority(손실폭 여유 우선 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};dd_headroom_first=true;no_authority",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(summary))


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
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
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier25(전선25)를 bridge archetype preselection ONNX scout(연결 원형 사전 선택 ONNX 탐색)로 열었습니다.

Effect(효과): F24(전선24)의 density-first bridge then DD repair(빈도 우선 연결 뒤 손실폭 수리)를 반복하지 않고, train-only DD-headroom-first preselection(학습 전용 손실폭 여유 우선 사전 선택)을 먼저 시험합니다.

Runtime/ONNX boundary(런타임/ONNX 경계): handoff candidate(인계 후보)가 나오기 전까지 MT5(메타트레이더5), WFO(워크포워드 최적화), ONNX(온엑스)는 열지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): train-only DD-headroom-first bridge archetype preselection(학습 전용 손실폭 여유 우선 연결 원형 사전 선택)이 F24(전선24)의 post-hoc DD repair(사후 손실폭 수리) 없이 더 좋은 scout/seed/handoff(탐색/씨앗/인계) 표면을 만드는지 시험합니다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier25 Stage Brief(전선25 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F25(전선25)는 F24B(전선24B)의 density-first bridge score(빈도 우선 연결 점수)를 단순 재가중하지 않습니다. changed variable(변경 변수)은 train-only DD-headroom-first bridge archetype preselection(학습 전용 손실폭 여유 우선 연결 원형 사전 선택)입니다.

OR-union semantics(OR 합집합 의미): 같은 timestamp(타임스탬프)에 여러 pocket(구간)이 켜져도 한 거래로 세며, long/short(롱/숏)는 한 archetype(원형) 안에서 섞지 않습니다.

Exit rule(종료 규칙): proxy(프록시), possible capped repair(가능한 상한 수리), closeout(마감)을 거쳐 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lock_spec() -> str:
    lines = ["# Frontier25 Bridge Archetype Preselection Lock Spec(전선25 연결 원형 사전 선택 잠금 명세)", ""]
    lines.append("Locks(잠금):")
    lines.extend(f"- {key}: {value}" for key, value in LOCKS.items())
    lines.append("")
    lines.append("Criteria(기준):")
    lines.append(json.dumps(CRITERIA, ensure_ascii=False, indent=2))
    lines.append("")
    return "\n".join(lines)


def do_not_repeat_text() -> str:
    return """# Frontier25 Do Not Repeat(전선25 반복 금지)

- Do not repeat F24B density-first bridge score as the primary ranking(F24B 빈도 우선 연결 점수를 기본 순위로 반복 금지).
- Do not apply F24C-style capped DD repair inside F25B(F25B 안에서 F24C식 상한 손실폭 수리 금지).
- Do not use validation/OOS DD headroom in selection(검증/표본외 손실폭 여유를 선택에 사용 금지).
- Do not count duplicate timestamp hits as multiple trades(중복 타임스탬프 신호를 여러 거래로 계산 금지).
- Do not export ONNX or run MT5 before handoff candidate(인계 후보 전 ONNX 내보내기 또는 MT5 실행 금지).
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier25 Experiment Design(전선25 실험 설계)

- hypothesis(가설): {summary['hypothesis']}
- decision_use(결정 사용처): {summary['decision_use']}
- comparison_baseline(비교 기준): {summary['comparison_baseline']}
- control_variables(통제 변수): {', '.join(summary['control_variables'])}
- changed_variables(변경 변수): {', '.join(summary['changed_variables'])}
- sample_scope(표본 범위): {summary['sample_scope']}
- success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}
- failure_criteria(실패 기준): {', '.join(summary['failure_criteria'])}
- invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}
- stop_conditions(중단 조건): {', '.join(summary['stop_conditions'])}
- evidence_plan(근거 계획): F25B run manifest(실행 목록), train-ranked archetype table(학습 순위 원형 표), F24B top-10 diff audit(F24B 상위10 차이 감사), split metrics(분할 지표), run registry(실행 등록부), stage ledger(단계 장부).
"""


def prior_stage_scan_text() -> str:
    return """# Frontier25 Prior Stage Scan(전선25 이전 단계 점검)

F24 preserved clue(전선24 보존 단서): `f24_density_bridge_dd_repaired_scout_pockets_reference_only(전선24 빈도 연결 손실폭 수리 탐색 구간 참조 전용)`.

- `f24b_0174`: high-density source(고빈도 원천) but validation DD 30%+(검증 손실폭 30% 이상).
- `f24c_0105`, `f24c_0106`, `f24c_0163`: capped DD repair scout clues(상한 손실폭 수리 탐색 단서), but no seed/handoff(씨앗/인계 없음).

F24 negative memory(전선24 부정 기억): OR-union bridge + single capped DD repair(OR 합집합 연결 + 단일 상한 손실폭 수리)는 seed/handoff(씨앗/인계)를 만들지 못했습니다.

Reference boundary(참조 경계): F24(전선24)는 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier25 Input References(전선25 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
- F24 closeout(전선24 마감): `{F24_CLOSEOUT.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier25 Review Index(전선25 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier25 Grok Stage Open Receipt(전선25 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 단계 개방 검토를 요구).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): bridge archetype preselection scout(연결 원형 사전 선택 탐색).

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Advice classification(조언 분류): `{summary['grok']['classification']}`.

Accepted advice(수용 조언): DD-headroom-first preselection(손실폭 여유 우선 사전 선택), train-only ranking(학습 전용 순위), no repair in F25B(F25B 수리 금지), unchanged gates(기존 게이트 유지), top-10 non-repeat proof(상위10 반복 아님 증명)를 잠급니다.

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 Codex 방향): F25B(전선25B)는 기존 F24 micro pocket(전선24 미세 구간)을 재구성하되, density-first(빈도 우선)가 아니라 DD-headroom-first(손실폭 여유 우선) 원형 점수로 평가합니다.
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier25 Local Verification(전선25 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier25 Required Gate Coverage Audit(전선25 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 필드) materialized(물질화)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- archetype_score_contract_gate(원형 점수 계약 게이트): DD-headroom-first formula(손실폭 여유 우선 공식) recorded(기록)
- non_repeat_gate(반복 방지 게이트): F25B must compare top10 keys against F24B(F25B는 F24B 상위10 키 비교 필수)
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier25A Stage Open Report(전선25A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier25(전선25)를 bridge archetype preselection ONNX scout(연결 원형 사전 선택 ONNX 탐색)로 열었습니다.

Effect(효과): F24(전선24)의 density-first bridge then capped DD repair(빈도 우선 연결 뒤 상한 손실폭 수리)를 반복하지 않고, train-only DD-headroom-first preselection(학습 전용 손실폭 여유 우선 사전 선택)을 첫 proxy(프록시)로 시험합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier25 Selection Status(전선25 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Status(상태): `{summary['status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier25 Bridge Archetype Preselection ONNX Scout(결정: 전선25 연결 원형 사전 선택 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): F25(전선25)를 train-only DD-headroom-first bridge archetype preselection(학습 전용 손실폭 여유 우선 연결 원형 사전 선택) 가설로 열었습니다.

Effect(효과): F24(전선24) 단서는 reference only(참조 전용)로 쓰고, winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier25(전선25) after Grok accepted review(그록 수용 검토). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` must test DD-headroom-first bridge archetype preselection(손실폭 여유 우선 연결 원형 사전 선택)을 시험합니다.\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR25-BRIDGE-ARCHETYPE-PRESELECTION-ONNX-SCOUT`: `{RUN_ID}` opens bridge archetype preselection scout(연결 원형 사전 선택 탐색). "
        "Effect(효과): F24 사후 손실폭 수리 반복 대신 train-only DD-headroom-first(학습 전용 손실폭 여유 우선) 구조 선택을 시험합니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing(누락)"}


def sha256_io(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
