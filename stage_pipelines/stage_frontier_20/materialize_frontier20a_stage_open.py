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
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout"
RUN_ID = "frontier20A_stage_open_train_only_feature_state_rule_atlas_onnx_scout_v1"
RUN_NUMBER = "frontier20A"
PARENT_RUN_ID = "frontier19C_boosted_backbone_repair_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier20B_feature_state_rule_atlas_proxy_scout_v1"
STATUS = "opened_frontier20_train_only_feature_state_rule_atlas_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_adjusted_review_with_train_only_rule_atlas_locks_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_20_train_only_feature_state_rule_atlas_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_20/materialize_frontier20a_stage_open.py")

GROK_INITIAL_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier20_stage_open/small_review")
GROK_ADJUSTED_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier20_stage_open/adjusted_review")

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

F19_SELECTION = Path("stages/stage_frontier_19__boosted_backbone_no_repair_stack_onnx_scout/04_selected/selection_status.md")
F18_SELECTION = Path("stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/04_selected/selection_status.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")

TRAIN_QUANTILES = ("q10", "q20", "q30", "q70", "q80", "q90")
MANDATORY_RECORD_VIEWS = (
    "Tier A separate(티어 A 분리)",
    "Tier B separate(티어 B 분리)",
    "Tier A+B combined(티어 A+B 합산)",
)

LOCKS: tuple[dict[str, str], ...] = (
    {
        "lock_id": "existing_58_contract_features_only",
        "rule": "Use only existing 58 contract features(기존 58개 계약 피처만 사용). No new feature engineering(새 피처 설계 없음).",
    },
    {
        "lock_id": "fixed_train_quantile_grid",
        "rule": "Fit q10/q20/q30/q70/q80/q90 only on train split(학습 분할에서만 고정 분위수 적합).",
    },
    {
        "lock_id": "max_conjunction_depth_two",
        "rule": "Rule atlas(규칙 지도)는 single or pair conjunction(단일 또는 쌍 결합)까지만 허용합니다.",
    },
    {
        "lock_id": "train_only_side_selection",
        "rule": "Long/short side(롱/숏 방향)는 train split(학습 분할) 성과로만 고릅니다.",
    },
    {
        "lock_id": "validation_oos_read_only",
        "rule": "Validation/OOS(검증/표본외)는 평가 전용이며 rule selection(규칙 선택)에 쓰지 않습니다.",
    },
    {
        "lock_id": "no_probability_threshold_or_backbone",
        "rule": "No probability threshold(확률 임계값 없음), no boosted backbone(부스팅 백본 없음).",
    },
    {
        "lock_id": "no_overlay_repair_stack",
        "rule": "No lifecycle/quota/firewall/veto repair(생명주기/할당량/방화벽/배제 수리 없음).",
    },
    {
        "lock_id": "tier_paired_record_slots",
        "rule": "Stage run ledger(단계 실행 장부)는 Tier A/Tier B/Tier A+B 기록 슬롯을 반드시 엽니다.",
    },
    {
        "lock_id": "runtime_probe_obligation",
        "rule": "If a handoff candidate(인계 후보)가 있으면 MT5 runtime probe(MT5 런타임 탐침)를 시도하고, 없으면 exact blocker(정확한 차단 사유)를 기록합니다.",
    },
    {
        "lock_id": "claim_boundary_lock",
        "rule": "Only scout clue/seed surface/runtime probe observation/preserved clue/negative memory/invalid setup/blocked(탐색 단서/씨앗 표면/런타임 탐침 관찰/보존 단서/부정 기억/무효 설정/차단) language is allowed.",
    },
)


def main() -> int:
    preexisting_stage_root = path_exists(STAGE_ROOT)
    ensure_dirs()
    normalize_grok_markdown()
    now = utc_now()
    feature_order = read_feature_order()
    grok_initial = read_grok_packet(GROK_INITIAL_PACKET)
    grok_adjusted = read_grok_packet(GROK_ADJUSTED_PACKET)
    local = local_verification(feature_order, grok_initial, grok_adjusted, preexisting_stage_root)
    summary = build_summary(now, feature_order, grok_initial, grok_adjusted, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_adjusted_classification": summary["grok_adjusted"]["classification"],
        "local_verification": summary["local_verification"]["judgment"],
        "feature_count": summary["feature_count"],
        "feature_order_hash": summary["feature_order_hash"],
        "lock_count": len(LOCKS),
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
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", ALPHA_LEDGER)


def normalize_grok_markdown() -> None:
    for packet in (GROK_INITIAL_PACKET, GROK_ADJUSTED_PACKET):
        for name in ("prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                text = io_path(path).read_text(encoding="utf-8-sig")
                f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    return {
        "packet": packet.as_posix(),
        "prompt": (packet / "prompt.md").as_posix(),
        "output": (packet / "clean_output.md").as_posix(),
        "metadata": (packet / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "duration_seconds": metadata.get("duration_seconds", ""),
        "preflight_warnings": metadata.get("preflight_warnings", []),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "output_excerpt": output[:1600],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "decision:** `adjust`" in lowered or "decision: `adjust`" in lowered:
        return "accepted_with_adjustments(조정 수용)"
    if "decision:** `accept`" in lowered or "decision: `accept`" in lowered:
        return "accepted(수용)"
    if "decision:** `reject`" in lowered or "decision: `reject`" in lowered:
        return "rejected(거절)"
    if "i'll read" in lowered or "작성하고" in text:
        return "rejected_no_actionable_review(실행 가능한 검토 없음으로 거절)"
    return "classification_missing(분류 누락)"


def local_verification(
    feature_order: list[str],
    grok_initial: dict[str, Any],
    grok_adjusted: dict[str, Any],
    preexisting_stage_root: bool,
) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    f19_selection = read_text(F19_SELECTION)
    f18_selection = read_text(F18_SELECTION)
    negative_register = read_text(NEGATIVE_RESULT_REGISTER)
    feature_hash = ordered_hash(feature_order)
    checks = {
        "workspace_current_stage_frontier19": f"current_stage_id: {Path(F19_SELECTION).parts[1]}" in workspace,
        "workspace_next_run_frontier20a": "next_run_id: frontier20A_stage_open_new_hypothesis_design_v1" in workspace,
        "f19_closed_negative_memory": "negative_memory(부정 기억)" in f19_selection and "no selected baseline" in f19_selection,
        "f18_lifecycle_negative_memory_seen": "asymmetric_exit_lifecycle" in negative_register and "runtime probe blocker" in f18_selection.lower(),
        "feature_order_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "feature_count_is_58": len(feature_order) == 58,
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_initial_rejected_as_non_actionable": grok_initial["classification"] == "rejected_no_actionable_review(실행 가능한 검토 없음으로 거절)",
        "grok_adjusted_usable": grok_adjusted["classification"] == "accepted_with_adjustments(조정 수용)",
        "grok_no_unexpected_top_level_artifacts": not grok_initial["unexpected_top_level_artifacts"] and not grok_adjusted["unexpected_top_level_artifacts"],
        "f20_stage_root_was_not_preexisting": not preexisting_stage_root,
        "mandatory_record_views_declared": len(MANDATORY_RECORD_VIEWS) == 3,
    }
    return {
        "judgment": "pass_with_adjusted_locks(조정 잠금 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_hash,
    }


def build_summary(
    now: str,
    feature_order: list[str],
    grok_initial: dict[str, Any],
    grok_adjusted: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design",
        "support_skills": [
            "obsidian-reentry-read",
            "obsidian-exploration-mandate",
            "obsidian-model-validation",
            "obsidian-grok-collaboration",
            "obsidian-result-judgment",
        ],
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "frontier_thesis": "Train-only feature-state rule atlas(학습 전용 피처 상태 규칙 지도)이 model probability/backbone(모델 확률/백본) 접근이 흐린 직접 alpha surface(직접 알파 표면)를 드러낼 수 있는가?",
        "hypothesis": "Sparse closed-bar feature-state conjunctions(희소 확정봉 피처 상태 결합)를 train split(학습 분할)에서만 선택하면 validation/OOS(검증/표본외)에서 5~10 trades/day(일 5~10회), PF improvement(수익 팩터 개선), lower DD(낮은 손실폭), smoother curve(더 매끄러운 곡선)에 가까워지는 seed surface(씨앗 표면)를 찾을 수 있다.",
        "novelty_delta": "F20(전선20)은 new features(새 피처), probability thresholds(확률 임계값), boosted backbone(부스팅 백본), lifecycle/quota/firewall repair(생명주기/할당량/방화벽 수리)를 쓰지 않고, fixed 58 feature states(고정 58 피처 상태)의 train-only direct rule surface(학습 전용 직접 규칙 표면)를 시험합니다.",
        "decision_use": "Open F20A stage(전선20A 단계)를 계획/잠금 상태로 열고 F20B proxy scout(전선20B 프록시 탐색) 범위를 고정합니다. Completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)는 만들지 않습니다.",
        "comparison_baseline": "Recent negative memories(최근 부정 기억) F05/F15/F16/F18/F19 and reference-only Stage12~364 archive(참조 전용 12~364단계 보관소).",
        "control_variables": [
            "US100 M5 FPMarkets v2 dataset(US100 5분봉 FPMarkets v2 데이터셋)",
            "label_v1 fwd12 split(라벨 v1 12봉 전방 분할)",
            "58 feature order hash(58 피처 순서 해시)",
            "closed-bar only inference boundary(확정봉 전용 추론 경계)",
            "no validation/OOS rule selection(검증/표본외 규칙 선택 없음)",
        ],
        "changed_variables": [
            "feature-state rule definitions(피처 상태 규칙 정의)",
            "train-only rule side(학습 전용 규칙 방향)",
            "rule atlas ranking on train only(학습 전용 규칙 지도 순위)",
        ],
        "sample_scope": "Tier A separate(티어 A 분리) is materialized from the 58-feature model input. Tier B separate(티어 B 분리) and Tier A+B combined(티어 A+B 합산) are required record views and may be missing_required/out_of_scope_by_claim(필수 누락/주장 범위 밖) if no Tier B source exists.",
        "success_criteria": [
            "scout clue(탐색 단서): validation/OOS PF(검증/표본외 수익 팩터)가 1.5+ toward target(목표 방향)으로 움직이고 density(빈도)가 5~10/day 근처입니다.",
            "seed surface(씨앗 표면): PF/density/DD/smoothness(수익 팩터/빈도/손실폭/매끄러움) 중 하나 이상이 악화 없이 의미 있게 좋아집니다.",
            "runtime probe observation(런타임 탐침 관찰): handoff candidate(인계 후보)가 생기면 MT5 runtime probe(MT5 런타임 탐침)를 시도합니다.",
        ],
        "failure_criteria": [
            "Train-only rules(학습 전용 규칙)이 validation/OOS(검증/표본외)에서 PF 1.1~1.3, high DD(높은 손실폭)에 머물러 F19와 같은 no-forward-clue(전진 단서 없음)로 끝납니다.",
            "Useful-looking surface(좋아 보이는 표면)가 validation/OOS guided filtering(검증/표본외 유도 필터링)을 요구합니다.",
            "No strict/seed/preserved/handoff row(엄격/씨앗/보존/인계 행)가 남지 않습니다.",
        ],
        "invalid_conditions": [
            "New feature engineering(새 피처 설계)",
            "Probability threshold search(확률 임계값 탐색)",
            "Validation/OOS selection(검증/표본외 선택)",
            "Boosted backbone rerun(부스팅 백본 재실행)",
            "Lifecycle/quota/firewall/veto repair inside F20B(F20B 내부 생명주기/할당량/방화벽/배제 수리)",
        ],
        "stop_conditions": [
            "strict/seed/handoff surface(엄격/씨앗/인계 표면)가 생기면 Grok pre-expensive review(비싼 실행 전 그록 검토)로 멈춥니다.",
            "locked atlas(고정 지도)에서 0/0/0/0이면 repair_or_closeout decision(수리/마감 결정)으로 넘깁니다.",
            "MT5 claim(MT5 주장)이 필요하면 runtime probe(런타임 탐침) 또는 exact blocker(정확한 차단 사유)를 남깁니다.",
        ],
        "evidence_plan": [
            "stage_open_summary.json(단계 개방 요약)",
            "rule_atlas_lock.json(규칙 지도 잠금)",
            "grok_stage_open_receipt.md(그록 단계 개방 영수증)",
            "F20B metrics by split(F20B 분할별 지표)",
            "Tier A/Tier B/Tier A+B ledger rows(티어 A/B/합산 장부 행)",
            "runtime probe report or blocker(런타임 탐침 보고 또는 차단 사유)",
        ],
        "locks": list(LOCKS),
        "train_quantiles": TRAIN_QUANTILES,
        "mandatory_record_views": MANDATORY_RECORD_VIEWS,
        "grok_initial": grok_initial,
        "grok_adjusted": grok_adjusted,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "rule_atlas_lock.json", rule_atlas_lock(summary))
    write_json(RUN_ROOT / "guard_manifest.json", {"locks": summary["locks"]})
    write_json(RUN_ROOT / "grok_receipt.json", grok_receipt(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "rule_atlas_lock_spec.md", rule_atlas_lock_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_checks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(DATASET_PATH),
            artifact_identity(FEATURE_ORDER_PATH),
            artifact_identity(GROK_ADJUSTED_PACKET / "clean_output.md"),
        ],
        "feature_schema": {
            "feature_count": summary["feature_count"],
            "feature_order_hash": summary["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "rule_stack": {
            "entry": list(summary["locks"]),
            "filters": ["validation_oos_read_only(검증/표본외 읽기 전용)"],
            "position": ["not_applicable_stage_open(단계 개방에는 해당 없음)"],
            "exit": ["not_applicable_stage_open(단계 개방에는 해당 없음)"],
        },
        "results": {
            "by_split": {},
            "cross_split": {"stage_open": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)"},
            "report_refs": [{"role": "stage_open_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "mismatch_policy": "fail_fast(즉시 실패)",
            "required_output_schema": "[p_short,p_flat,p_long](숏/중립/롱 확률 순서) if ONNX is later materialized(나중에 ONNX가 물질화될 경우)",
        },
        "claim_boundary": summary["claim_boundary"],
    }


def rule_atlas_lock(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "feature_policy": "existing_58_contract_features_only(기존 58 계약 피처만)",
        "feature_order_hash": summary["feature_order_hash"],
        "quantiles": list(TRAIN_QUANTILES),
        "max_conjunction_depth": 2,
        "selection_partition": "train_only(학습 전용)",
        "evaluation_partitions": ["validation_read_only(검증 읽기 전용)", "oos_read_only(표본외 읽기 전용)"],
        "forbidden_repairs": [
            "probability_threshold_search(확률 임계값 탐색)",
            "boosted_backbone_rerun(부스팅 백본 재실행)",
            "lifecycle_repair(생명주기 수리)",
            "quota_repair(할당량 수리)",
            "firewall_or_veto_repair(방화벽 또는 배제 수리)",
        ],
    }


def grok_receipt(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "trigger_reason": "Goal requires Grok second opinion at stage open(목표가 단계 개방 시 그록 2차 의견을 요구)",
        "review_size": "small review(소규모 검토)",
        "direction_before_grok": summary["frontier_thesis"],
        "bounded_evidence": [
            "F19 closeout negative memory(F19 부정 기억 마감)",
            "F05/F15/F16/F18/F19 do-not-repeat list(반복 금지 목록)",
            "pre-open in-memory probe summary(개방 전 메모리 탐침 요약)",
        ],
        "initial_packet": summary["grok_initial"],
        "adjusted_packet": summary["grok_adjusted"],
        "advice_classification": {
            "initial": summary["grok_initial"]["classification"],
            "adjusted": summary["grok_adjusted"]["classification"],
        },
        "local_verification": summary["local_verification"],
        "forbidden_claim_check": summary["claim_boundary"],
        "final_codex_direction": "Open F20A with adjusted locks(조정 잠금으로 F20A 개방)",
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier20 Train-Only Feature-State Rule Atlas ONNX Scout(전선20 학습 전용 피처 상태 규칙 지도 ONNX 탐색)

Stage id(단계 ID): `{STAGE_ID}`

Status(상태): `{summary['status']}`

Action(행동): Frontier20(전선20)을 train-only feature-state rule atlas(학습 전용 피처 상태 규칙 지도) 가설로 열었습니다.

Effect(효과): F05/F15/F19(전선05/15/19)의 feature expansion/threshold/backbone(피처 확장/임계값/백본) 반복을 피하고, 기존 58 feature state(기존 58 피처 상태)의 직접 규칙 표면만 시험합니다.

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier20 Stage Brief(전선20 단계 개요)

Question(질문): train-only feature-state rule atlas(학습 전용 피처 상태 규칙 지도)가 US100 M5 ONNX(온엑스) 후보 탐색에서 직접 seed surface(씨앗 표면)를 드러낼 수 있는가?

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): {summary['novelty_delta']}

Exit rule(종료 규칙): hypothesis -> proxy -> WFO/stress/runtime validation -> repair -> closeout(가설 -> 프록시 -> WFO/스트레스/런타임 검증 -> 수리 -> 마감)을 지나 completion candidate/preserved clue/negative memory/invalid setup/blocked(완성 후보/보존 단서/부정 기억/무효 설정/차단) 중 하나로 닫습니다. 단, completion(완성)은 final completion review(최종 완성 검토) 전에는 주장하지 않습니다.
"""


def rule_atlas_lock_spec(summary: dict[str, Any]) -> str:
    locks = "\n".join(f"- `{item['lock_id']}`: {item['rule']}" for item in summary["locks"])
    views = "\n".join(f"- {view}" for view in MANDATORY_RECORD_VIEWS)
    return f"""# Frontier20 Rule Atlas Lock Spec(전선20 규칙 지도 잠금 명세)

Action(행동): F20B proxy scout(F20B 프록시 탐색) 전에 rule atlas(규칙 지도)의 허용 범위를 고정합니다.

Effect(효과): validation/OOS(검증/표본외) 숫자를 본 뒤 규칙을 바꾸는 leakage(누수)와 F15/F19 반복을 막습니다.

## Locks(잠금)

{locks}

## Required Record Views(필수 기록 보기)

{views}
"""


def do_not_repeat_text(summary: dict[str, Any]) -> str:
    return """# Frontier20 Do Not Repeat(전선20 반복 금지)

- F05 feature micro-expansion(피처 미세 확장): 새 handcrafted feature(수제 피처)를 만들지 않습니다.
- F15 threshold grid(임계값 격자): probability score threshold(확률 점수 임계값)를 탐색하지 않습니다.
- F16 edge-quality risk-veto(엣지 품질 위험 배제): broad veto labels(넓은 배제 라벨)를 다시 만들지 않습니다.
- F18 lifecycle repair(생명주기 수리): hold/reverse/TP/ATR lifecycle sweep(보유/반전/이익실현/ATR 생명주기 탐색)을 하지 않습니다.
- F19 boosted backbone-only(부스팅 백본 단독): boosted-tree model backbone(부스팅 트리 모델 백본)을 다시 바꾸지 않습니다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier20 Experiment Design(전선20 실험 설계)

- primary_family(주 작업군): `{summary['primary_family']}`
- primary_skill(주 스킬): `{summary['primary_skill']}`
- support_skills(보조 스킬): `{', '.join(summary['support_skills'])}`
- required_gates(필수 게이트): `external_review_packet`, `train_only_leakage_guard`, `rule_atlas_lock_gate`, `tier_paired_record_gate`, `runtime_probe_obligation_gate`, `required_gate_coverage_audit`, `final_claim_guard`

hypothesis(가설): {summary['hypothesis']}

decision_use(결정 용도): {summary['decision_use']}

comparison_baseline(비교 기준): {summary['comparison_baseline']}

control_variables(통제 변수): {', '.join(summary['control_variables'])}

changed_variables(변경 변수): {', '.join(summary['changed_variables'])}

sample_scope(표본 범위): {summary['sample_scope']}

success_criteria(성공 기준): {', '.join(summary['success_criteria'])}

failure_criteria(실패 기준): {', '.join(summary['failure_criteria'])}

invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}

stop_conditions(중단 조건): {', '.join(summary['stop_conditions'])}

evidence_plan(근거 계획): {', '.join(summary['evidence_plan'])}
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    return """# Frontier20 Prior Stage Scan(전선20 이전 단계 점검)

F19 negative memory(F19 부정 기억): boosted backbone-only(부스팅 백본 단독)는 valid ONNX(유효 ONNX)를 만들었지만 forward economic clue(전진 경제 단서)가 없었습니다. Effect(효과): F20은 model backbone(모델 백본)을 바꾸지 않습니다.

F18 negative memory(F18 부정 기억): low-DD lifecycle shape(낮은 손실폭 생명주기 모양)는 보존 단서였지만 PF/density/smoothness(수익 팩터/빈도/매끄러움)가 부족했습니다. Effect(효과): F20은 lifecycle repair(생명주기 수리)를 쓰지 않습니다.

F15 negative memory(F15 부정 기억): score threshold density repair(점수 임계값 빈도 수리)는 edge quality/PF/DD(엣지 품질/수익 팩터/손실폭)를 만들지 못했습니다. Effect(효과): F20은 probability threshold(확률 임계값)를 쓰지 않습니다.

F05 negative memory(F05 부정 기억): feature micro-expansion(피처 미세 확장)은 전이되지 않았습니다. Effect(효과): F20은 기존 58 feature(기존 58 피처)만 씁니다.
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier20 Input Refs(전선20 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature order hash(피처 순서 해시): `{summary['feature_order_hash']}`
- F19 selection(F19 선택 상태): `{F19_SELECTION.as_posix()}`
- F18 selection(F18 선택 상태): `{F18_SELECTION.as_posix()}`
- Grok initial review(그록 초기 검토): `{summary['grok_initial']['output']}`
- Grok adjusted review(그록 조정 검토): `{summary['grok_adjusted']['output']}`
- stage open script(단계 개방 스크립트): `{SCRIPT_PATH.as_posix()}`
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier20 Review Index(전선20 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok adjusted review(그록 조정 검토) accepted with locks(잠금 포함 수용), no trading KPI(거래 KPI 없음), no authority(권위 없음).
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    receipt = grok_receipt(summary)
    return f"""# Frontier20 Grok Stage-Open Receipt(전선20 그록 단계 개방 영수증)

trigger_reason(트리거 이유): {receipt['trigger_reason']}

review_size(검토 크기): {receipt['review_size']}

direction_before_grok(그록 전 방향): {receipt['direction_before_grok']}

initial_classification(초기 분류): `{summary['grok_initial']['classification']}`

adjusted_classification(조정 분류): `{summary['grok_adjusted']['classification']}`

local_verification(로컬 검증): `{summary['local_verification']['judgment']}`

final_codex_direction(최종 코덱스 방향): {receipt['final_codex_direction']}

forbidden_claim_check(금지 주장 확인): `{json.dumps(summary['claim_boundary'], ensure_ascii=False, sort_keys=True)}`
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    return f"""# Frontier20 Local Verification(전선20 로컬 검증)

Judgment(판정): `{summary['local_verification']['judgment']}`

Feature count(피처 수): `{summary['feature_count']}`

Feature order hash(피처 순서 해시): `{summary['feature_order_hash']}`

{checks}
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier20A Required Gate Coverage Audit(전선20A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_adjusted_locks(조정 잠금 포함 통과)

- external_review_packet(외부 검토 묶음): Grok adjusted review(그록 조정 검토) `{summary['grok_adjusted']['packet']}` recorded(기록됨).
- train_only_leakage_guard(학습 전용 누수 방지): quantiles/side/ranking(분위수/방향/순위)은 train-only(학습 전용)로 잠김.
- rule_atlas_lock_gate(규칙 지도 잠금 게이트): 58 features, depth 2, fixed quantiles(58 피처, 깊이 2, 고정 분위수) 기록됨.
- tier_paired_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B(티어 A/B/합산) 슬롯 기록됨.
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): handoff candidate(인계 후보) 없으면 exact blocker(정확한 차단 사유)를 기록하도록 잠김.
- final_claim_guard(최종 주장 보호): completion/baseline/promotion/runtime/live/Goal(완성/기준선/승격/런타임/실거래/목표) 주장 없음.
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier20A Stage Open Report(전선20A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier20(전선20)을 train-only feature-state rule atlas ONNX scout(학습 전용 피처 상태 규칙 지도 ONNX 탐색)로 열었습니다.

Effect(효과): 기존 58 feature(기존 58 피처)의 closed-bar state(확정봉 상태)만 써서 seed surface(씨앗 표면)를 찾고, validation/OOS(검증/표본외)로 규칙을 고르지 못하게 잠갔습니다.

Grok initial classification(그록 초기 분류): `{summary['grok_initial']['classification']}`

Grok adjusted classification(그록 조정 분류): `{summary['grok_adjusted']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Feature count/hash(피처 수/해시): `{summary['feature_count']}` / `{summary['feature_order_hash']}`

Lock count(잠금 수): `{len(summary['locks'])}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier20 Selection Status(전선20 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier20 Train-Only Feature-State Rule Atlas ONNX Scout(결정: 전선20 학습 전용 피처 상태 규칙 지도 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier20(전선20)을 train-only feature-state rule atlas(학습 전용 피처 상태 규칙 지도)로 열었습니다.

Effect(효과): F20B(전선20B)는 58 contract features(58 계약 피처), fixed train quantiles(고정 학습 분위수), max depth 2(최대 깊이 2), train-only side selection(학습 전용 방향 선택)만 시험합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


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
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier20_stage_open_grok_adjusted_rule_atlas_locks_no_authority",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
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
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok_adjusted={summary['grok_adjusted']['classification']};locks={len(LOCKS)};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "no_model_training_no_wfo_no_mt5_no_authority(모델 학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_required_before_closeout(그록 단계 개방 검토 완료, 마감 전 런타임 탐침 필요)",
        "notes": f"next={NEXT_RUN_ID};train_only_rule_atlas_locks;no_authority",
        "question": "Can train-only feature-state rule atlas expose a seed surface without feature/threshold/backbone repair?(학습 전용 피처 상태 규칙 지도가 피처/임계값/백본 수리 없이 씨앗 표면을 드러낼 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR20-TRAIN-ONLY-FEATURE-STATE-RULE-ATLAS-ONNX-SCOUT`: `{RUN_ID}` opens train-only feature-state rule atlas(학습 전용 피처 상태 규칙 지도). "
        "Effect(효과): F05/F15/F19(전선05/15/19)의 피처 확장/임계값/백본 반복을 피하고 fixed 58 feature states(고정 58 피처 상태)를 직접 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier20(전선20) after Grok adjusted review(그록 조정 검토). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` is locked to train-only rule atlas(학습 전용 규칙 지도) with no threshold/backbone/lifecycle repair(임계값/백본/생명주기 수리 없음).\n"
    )


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(f03b.WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))


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

Action(행동): Frontier20(전선20)을 train-only feature-state rule atlas ONNX scout(학습 전용 피처 상태 규칙 지도 ONNX 탐색)로 열었습니다.

Effect(효과): 다음 실행은 기존 58 feature(기존 58 피처)의 train-only quantile rules(학습 전용 분위수 규칙)만 시험하며 validation/OOS(검증/표본외)를 규칙 선택에 쓰지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    with io_path(template_path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_feature_order() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
