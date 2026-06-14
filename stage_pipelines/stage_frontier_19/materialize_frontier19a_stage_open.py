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


STAGE_ID = "stage_frontier_19__boosted_backbone_no_repair_stack_onnx_scout"
RUN_ID = "frontier19A_stage_open_boosted_backbone_no_repair_stack_onnx_scout_v1"
RUN_NUMBER = "frontier19A"
PARENT_RUN_ID = "frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1"
STATUS = "opened_frontier19_boosted_backbone_no_repair_stack_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_adjusted_review_with_backbone_only_locks_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_19_boosted_backbone_no_repair_stack_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_19/materialize_frontier19a_stage_open.py")

GROK_INITIAL_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier19_stage_open/small_review")
GROK_ADJUSTED_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier19_stage_open/small_review_adjusted")

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

F18_SELECTION = Path("stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/04_selected/selection_status.md")
F11_SELECTION = Path("stages/stage_frontier_11__subperiod_stability_first_onnx_scout/04_selected/selection_status.md")
ARCHIVE_XGB_STAGE = Path("stages/17_model_family_challenge__xgboost_regularized_boosting_scout")
ARCHIVE_CAT_STAGE = Path("stages/18_model_family_challenge__catboost_ordered_boosting_scout")
XGB_HELPER = Path("foundation/models/xgboost_boosting.py")
CAT_HELPER = Path("foundation/models/catboost_ordered.py")
ONNX_BRIDGE = Path("foundation/models/onnx_bridge.py")
EA_ENTRYPOINT = Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")


MODEL_VARIANTS: tuple[dict[str, Any], ...] = (
    {
        "variant_id": "f19b_xgb_depth2_l2_backbone_control",
        "family": "xgboost(XGBoost, 엑스지부스트)",
        "source_helper": XGB_HELPER.as_posix(),
        "basis": "v01_depth2_l2_subsample",
        "role": "shallow_regularized_backbone_control(얕은 정규화 백본 대조군)",
    },
    {
        "variant_id": "f19b_xgb_depth3_balanced_l2_backbone",
        "family": "xgboost(XGBoost, 엑스지부스트)",
        "source_helper": XGB_HELPER.as_posix(),
        "basis": "v02_depth3_balanced_l2",
        "role": "balanced_depth_regularized_backbone(균형 깊이 정규화 백본)",
    },
    {
        "variant_id": "f19b_cat_ordered_depth3_backbone",
        "family": "catboost(CatBoost, 캣부스트)",
        "source_helper": CAT_HELPER.as_posix(),
        "basis": "v01_ordered_depth3_bayesian",
        "role": "ordered_boosting_backbone(순서 부스팅 백본)",
    },
    {
        "variant_id": "f19b_cat_plain_depth3_backbone_control",
        "family": "catboost(CatBoost, 캣부스트)",
        "source_helper": CAT_HELPER.as_posix(),
        "basis": "v05_plain_depth3_control",
        "role": "plain_boosting_backbone_control(일반 부스팅 백본 대조군)",
    },
)

LOCKS: tuple[dict[str, str], ...] = (
    {
        "lock_id": "primary_variable_backbone_only",
        "rule": "Only model backbone variants change(모델 백본 변형만 변경). No threshold/veto/firewall/lifecycle/quota repair(임계값/배제/방화벽/생명주기/쿼터 수리 없음).",
    },
    {
        "lock_id": "variant_cap_max_four",
        "rule": "Exactly four variants are fixed before Frontier19B metrics(전선19B 지표 전 변형 4개 고정).",
    },
    {
        "lock_id": "stability_audit_not_selector",
        "rule": "Subperiod stability is audit/tie-break only(하위기간 안정성은 감사/동률 처리 전용). It cannot select or mutate validation/OOS outcomes(검증/표본외 결과 선택/변경 금지).",
    },
    {
        "lock_id": "single_execution_surface",
        "rule": "Use one fixed entry/exit surface(단일 진입/청산 표면). No lifecycle sweep(생명주기 스윕 없음), no daily quota(일일 쿼터 없음), no threshold search(임계값 탐색 없음).",
    },
    {
        "lock_id": "archive_reference_only",
        "rule": "Stage17/18 archive XGBoost/CatBoost runs are reference only(17/18단계 보관소 부스팅 실행은 참조 전용). No selected variant, threshold, hold, baseline, or handoff is inherited(선택 변형/임계값/보유/기준선/인계 상속 없음).",
    },
    {
        "lock_id": "runtime_probe_before_closeout",
        "rule": "Before closeout run a narrow MT5 runtime probe if a handoff candidate exists, otherwise record exact blocker(마감 전 인계 후보가 있으면 좁은 MT5 런타임 탐침, 없으면 정확한 차단 사유 기록).",
    },
    {
        "lock_id": "claim_boundary_lock",
        "rule": "Only scout clue/seed surface/runtime probe observation/preserved clue/negative memory/invalid setup/blocked may be claimed(탐색 단서/씨앗 표면/런타임 탐침 관찰/보존 단서/부정 기억/무효 설정/차단만 주장 가능).",
    },
)

EXECUTION_SURFACE = {
    "decision_policy": "argmax_nonflat_control(최대확률 비중립 대조)",
    "threshold_policy": "no_validation_oos_threshold_search(검증/표본외 임계값 탐색 없음)",
    "exit_policy": "fixed_fwd12_proxy_then_single_runtime_surface_if_handoff_exists(프록시는 고정 fwd12, 인계 후보가 있으면 단일 런타임 표면)",
    "density_policy": "observe_density_no_daily_quota_repair(빈도 관찰, 일일 쿼터 수리 없음)",
    "stability_policy": "audit_and_tie_break_only(감사와 동률 처리 전용)",
}


def main() -> int:
    now = utc_now()
    ensure_dirs()
    normalize_grok_markdown()
    grok_initial = read_grok_packet(GROK_INITIAL_PACKET)
    grok_adjusted = read_grok_packet(GROK_ADJUSTED_PACKET)
    local = local_verification(grok_initial, grok_adjusted)
    summary = build_summary(now, grok_initial, grok_adjusted, local)
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
        "variant_count": len(MODEL_VARIANTS),
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
        "output_excerpt": output[:1200],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "classification" in lowered and "accepted" in lowered:
        return "accepted(수용)"
    if "classification" in lowered and "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(grok_initial: dict[str, Any], grok_adjusted: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    f18_selection = read_text(F18_SELECTION)
    f11_selection = read_text(F11_SELECTION)
    run_registry = read_text(RUN_REGISTRY)
    ea_text = read_text(EA_ENTRYPOINT)
    features = read_feature_order()
    checks = {
        "workspace_points_to_frontier19A": "next_run_id: frontier19A_stage_open_new_hypothesis_design_v1" in workspace,
        "f18_closed_negative_memory": "negative_memory(부정 기억)" in f18_selection and "runtime probe blocker" in f18_selection.lower(),
        "f11_negative_memory_confirmed": "negative_memory" in f11_selection.lower() and "subperiod" in f11_selection.lower(),
        "archive_xgb_stage_exists": path_exists(ARCHIVE_XGB_STAGE),
        "archive_catboost_stage_exists": path_exists(ARCHIVE_CAT_STAGE),
        "run_registry_xgb_archive_reference_found": "17_model_family_challenge__xgboost_regularized_boosting_scout" in run_registry,
        "run_registry_catboost_archive_reference_found": "18_model_family_challenge__catboost_ordered_boosting_scout" in run_registry,
        "xgb_helper_exists": path_exists(XGB_HELPER),
        "catboost_helper_exists": path_exists(CAT_HELPER),
        "onnx_export_helpers_exist": all(token in read_text(ONNX_BRIDGE) for token in ("export_xgboost_classifier_to_onnx", "export_catboost_classifier_to_onnx")),
        "feature_order_hash_matches_contract": ordered_hash(features) == EXPECTED_FEATURE_HASH,
        "model_variant_cap_is_four": len(MODEL_VARIANTS) == 4,
        "required_lock_ids_present": {
            "primary_variable_backbone_only",
            "variant_cap_max_four",
            "stability_audit_not_selector",
            "single_execution_surface",
            "archive_reference_only",
            "runtime_probe_before_closeout",
            "claim_boundary_lock",
        }.issubset({item["lock_id"] for item in LOCKS}),
        "ea_single_surface_inputs_available": all(token in ea_text for token in ("InpDecisionMode", "InpMaxHoldBars", "InpReverseOnOppositeSignal", "InpCloseOnFlatSignal")),
        "initial_grok_success": bool(grok_initial["success"]),
        "initial_grok_needs_local_verification": grok_initial["classification"] == "needs_local_verification(로컬 검증 필요)",
        "adjusted_grok_success": bool(grok_adjusted["success"]),
        "adjusted_grok_accepted": grok_adjusted["classification"] == "accepted(수용)",
        "grok_no_unexpected_top_level_artifacts": not grok_initial["unexpected_top_level_artifacts"] and not grok_adjusted["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_with_locks(잠금 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
        "feature_count": len(features),
        "feature_order_hash": ordered_hash(features),
    }


def build_summary(
    now: str,
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
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-grok-collaboration",
        ],
        "hypothesis": (
            "A capped boosted-tree backbone-only scout(상한 있는 부스팅 트리 백본 단독 탐색) under the fixed US100 M5 "
            "58-feature closed-bar ONNX contract(고정 US100 5분봉 58피처 닫힌 봉 ONNX 계약) can create a scout clue(탐색 단서) "
            "without reusing failed threshold/veto/firewall/lifecycle/quota/stability-selector repairs"
            "(실패한 임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리 재사용 없음)."
        ),
        "decision_use": "Open Frontier19A(전선19A 개방) and lock Frontier19B proxy scope(전선19B 프록시 범위 고정), not a completion or authority claim(완성 또는 권위 주장 아님).",
        "comparison_baseline": "F15~F18 recent negative memories and archive Stage17/18 model-family runs are reference only(최근 부정 기억과 17/18단계 모델 계열 실행은 참조 전용).",
        "control_variables": [
            "US100 M5 FPMarkets data contract(US100 5분봉 FPMarkets 데이터 계약)",
            "label_v1 fwd12 split discipline(label_v1 fwd12 분할 규율)",
            "58-feature order hash(58피처 순서 해시)",
            "fixed output schema [p_short,p_flat,p_long](고정 출력 스키마)",
            "single entry/exit surface(단일 진입/청산 표면)",
        ],
        "changed_variables": ["boosted-tree backbone variant(부스팅 트리 백본 변형)"],
        "sample_scope": "Tier A separate first(티어 A 분리 우선), Tier B/Tier A+B explicit missing_required if unavailable(티어 B/합산 불가 시 필수 누락 명시).",
        "success_criteria": {
            "scout_clue": "Validation/OOS PF moves toward 2+, density near 5~10/day, DD toward <=10~15%, and smoothness improves without repair stacking(검증/표본외 PF 2+ 방향, 빈도 5~10/day 근처, 손실폭 10~15% 방향, 수리 중첩 없이 매끄러움 개선).",
            "seed_surface": "One backbone improves a major axis without breaking the other three axes(한 백본이 다른 세 축을 깨지 않고 주요 축 하나를 개선).",
            "runtime_probe_observation": "If a handoff candidate exists, a narrow MT5 probe is attempted before closeout(인계 후보가 있으면 마감 전 좁은 MT5 탐침 시도).",
        },
        "failure_criteria": [
            "Boosted backbone repeats archive Stage17/18 inconclusive economics(부스팅 백본이 17/18단계 보관소의 불충분 경제성을 반복)",
            "Backbone-only path needs threshold/veto/lifecycle/quota repair to look usable(백본 단독 경로가 쓸만해 보이려면 임계값/배제/생명주기/쿼터 수리가 필요)",
            "ONNX parity fails for all pre-registered variants(사전 등록 변형 전체 ONNX 동등성 실패)",
        ],
        "invalid_conditions": [
            "Validation/OOS threshold search(검증/표본외 임계값 탐색)",
            "Subperiod stability as primary selector(하위기간 안정성을 1차 선택기로 사용)",
            "Archive selected variant, q-threshold, hold, or MT5 KPI inherited as baseline(보관소 선택 변형/분위 임계값/보유/MT5 KPI를 기준선으로 상속)",
            "Lifecycle sweep or daily quota repair inside Frontier19B(전선19B 안 생명주기 스윕 또는 일일 쿼터 수리)",
        ],
        "stop_conditions": [
            "Strict scout clue or seed surface found, then Grok before expensive WFO/MT5(엄격 탐색 단서 또는 씨앗 표면 발견 시 비싼 WFO/MT5 전 Grok 검토)",
            "No forward clue under locked variants, then repair/closeout decision(고정 변형 아래 전진 단서 없으면 수리/마감 결정)",
            "Runtime claim needed, then MT5 probe or exact blocker(런타임 주장이 필요하면 MT5 탐침 또는 정확한 차단 사유)",
        ],
        "evidence_plan": [
            "F19A stage-open summary and locks(전선19A 단계 개방 요약과 잠금)",
            "F19B model variant metrics by split(전선19B 모델 변형 분할별 지표)",
            "ONNX export and onnxruntime parity receipts(ONNX 내보내기와 런타임 동등성 영수증)",
            "Tier A/Tier B/Tier A+B ledger rows or missing_required(티어 A/B/합산 장부 행 또는 필수 누락)",
            "Runtime probe report or exact blocker before closeout(마감 전 런타임 탐침 보고 또는 정확한 차단 사유)",
        ],
        "model_variants": list(MODEL_VARIANTS),
        "execution_surface": dict(EXECUTION_SURFACE),
        "locks": list(LOCKS),
        "grok_initial": grok_initial,
        "grok_adjusted": grok_adjusted,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "model_variant_lock.json", {"variants": summary["model_variants"]})
    write_json(RUN_ROOT / "execution_surface_lock.json", summary["execution_surface"])
    write_json(RUN_ROOT / "guard_manifest.json", {"locks": summary["locks"]})
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "model_backbone_lock_spec.md", model_backbone_lock_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "selection_metric_spec.md", selection_metric_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": summary["status"],
        "judgment": summary["judgment"],
        "script": artifact_identity(SCRIPT_PATH),
        "report": artifact_identity(REPORT_PATH),
        "decision": {"path": DECISION_PATH.as_posix()},
        "inputs": {
            "dataset": artifact_identity(DATASET_PATH),
            "feature_order": artifact_identity(FEATURE_ORDER_PATH),
            "f18_selection": artifact_identity(F18_SELECTION),
            "f11_selection": artifact_identity(F11_SELECTION),
            "grok_initial": summary["grok_initial"],
            "grok_adjusted": summary["grok_adjusted"],
        },
        "outputs": {
            "stage_open_summary": (RUN_ROOT / "stage_open_summary.json").as_posix(),
            "model_variant_lock": (RUN_ROOT / "model_variant_lock.json").as_posix(),
            "execution_surface_lock": (RUN_ROOT / "execution_surface_lock.json").as_posix(),
            "guard_manifest": (RUN_ROOT / "guard_manifest.json").as_posix(),
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Boosted Backbone No Repair Stack ONNX Scout(전선19 부스팅 백본 수리 중첩 없는 ONNX 탐색)

Stage id(단계 ID): `{STAGE_ID}`

Status(상태): `{summary['status']}`

Action(행동): Frontier19(전선19)를 boosted backbone-only scout(부스팅 백본 단독 탐색)로 열었습니다.

Effect(효과): F15~F18(전선15~18)의 threshold/veto/firewall/lifecycle repair stack(임계값/배제/방화벽/생명주기 수리 중첩)을 반복하지 않고, 모델 백본(backbone, 백본) 하나만 1차 변수로 둡니다.

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Stage Brief(전선19 단계 개요)

Question(질문): boosted-tree backbone(부스팅 트리 백본)만 바꾸고 repair stack(수리 중첩)을 제거하면 US100 M5 ONNX(온엑스) 탐색 단서가 살아나는가?

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F19(전선19)의 novelty(신규성)는 model-family backbone(모델 계열 백본) 자체가 아니라, F15~F18(전선15~18)의 overlay repair(덧씌움 수리)를 제거하고 capped backbone-only(상한 있는 백본 단독)로 반증 가능하게 묶는 데 있습니다.

Exit rule(종료 규칙): hypothesis -> proxy -> WFO/stress/runtime validation -> repair -> closeout(가설 -> 프록시 -> WFO/스트레스/런타임 검증 -> 수리 -> 마감)을 지나 completion candidate/preserved clue/negative memory/invalid setup/blocked(완성 후보/보존 단서/부정 기억/무효 설정/차단) 중 하나로 닫습니다.
"""


def model_backbone_lock_spec(summary: dict[str, Any]) -> str:
    variants = "\n".join(
        f"- `{item['variant_id']}`: {item['family']}; basis(기반) `{item['basis']}`; role(역할) {item['role']}"
        for item in summary["model_variants"]
    )
    surface = "\n".join(f"- {key}: `{value}`" for key, value in summary["execution_surface"].items())
    return f"""# Frontier19 Model Backbone Lock Spec(전선19 모델 백본 잠금 명세)

Action(행동): Frontier19B(전선19B) 전에 model variants(모델 변형)와 execution surface(실행 표면)를 고정합니다.

Effect(효과): validation/OOS(검증/표본외) 결과를 본 뒤 threshold(임계값), lifecycle(생명주기), quota(쿼터), stability selector(안정성 선택기)를 추가하는 invalid setup(무효 설정)을 막습니다.

## Variants(변형)

{variants}

## Execution Surface(실행 표면)

{surface}
"""


def do_not_repeat_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{item['lock_id']}`: {item['rule']}" for item in summary["locks"])
    return f"""# Frontier19 Do Not Repeat(전선19 반복 금지)

{rows}
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return """# Frontier19 Selection Metric Spec(전선19 선택 지표 명세)

- scout clue(탐색 단서): validation/OOS(검증/표본외) PF, density, DD, smoothness(PF/빈도/손실폭/매끄러움)가 동시에 목표 방향으로 움직여야 합니다.
- seed surface(씨앗 표면): 한 축 개선이 다른 세 축을 심하게 깨지 않아야 합니다.
- tie-break(동률 처리): train-only subperiod stability audit(학습 전용 하위기간 안정성 감사)는 동률 처리만 가능하며, 1차 선택기로 쓰지 않습니다.
- runtime probe observation(런타임 탐침 관찰): 인계 후보가 있으면 MT5 runtime probe(MT5 런타임 탐침)를 시도하고, 없으면 exact blocker(정확한 차단 사유)를 남깁니다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Experiment Design(전선19 실험 설계)

- primary_family(주 작업군): `{summary['primary_family']}`
- primary_skill(주 스킬): `{summary['primary_skill']}`
- support_skills(보조 스킬): `{', '.join(summary['support_skills'])}`
- required_gates(필수 게이트): `work_packet_schema_lint`, `external_review_packet`, `backbone_variant_lock_gate`, `do_not_repeat_lock_gate`, `runtime_probe_obligation_gate`, `required_gate_coverage_audit`, `final_claim_guard`

hypothesis(가설): {summary['hypothesis']}

decision_use(결정 용도): {summary['decision_use']}

comparison_baseline(비교 기준): {summary['comparison_baseline']}

control_variables(통제 변수): {', '.join(summary['control_variables'])}

changed_variables(변경 변수): {', '.join(summary['changed_variables'])}

sample_scope(표본 범위): {summary['sample_scope']}

success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}

failure_criteria(실패 기준): {', '.join(summary['failure_criteria'])}

invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}

stop_conditions(중단 조건): {', '.join(summary['stop_conditions'])}

evidence_plan(근거 계획): {', '.join(summary['evidence_plan'])}
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    return """# Frontier19 Prior Stage Scan(전선19 이전 단계 스캔)

Frontier11 negative memory(전선11 부정 기억): subperiod stability-first selector(하위기간 안정성 우선 선택기)는 strict/preserved(엄격/보존) 단서 없이 닫혔습니다. Effect(효과): F19에서 stability(안정성)는 audit/tie-break(감사/동률 처리) 전용입니다.

Frontier15~18 negative memory(전선15~18 부정 기억): threshold/veto/firewall/lifecycle repair(임계값/배제/방화벽/생명주기 수리)는 반복하지 않습니다. Effect(효과): F19B는 backbone-only(백본 단독)로 시작합니다.

Archive Stage17/18 reference only(17/18단계 보관소 참조 전용): XGBoost/CatBoost(엑스지부스트/캣부스트) MT5 runtime probe(런타임 탐침)는 inconclusive(불충분)로 남아 있습니다. Effect(효과): export/parity lesson(내보내기/동등성 교훈)만 참고하고, selected variant(선택 변형), threshold(임계값), hold(보유), baseline(기준선), handoff(인계)는 상속하지 않습니다.
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    return f"""# Frontier19 Local Checks(전선19 로컬 확인)

Judgment(판정): `{summary['local_verification']['judgment']}`

Feature count(피처 수): `{summary['local_verification']['feature_count']}`

Feature order hash(피처 순서 해시): `{summary['local_verification']['feature_order_hash']}`

{checks}
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Input Refs(전선19 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- Frontier18 selection(전선18 선택 상태): `{F18_SELECTION.as_posix()}`
- Frontier11 selection(전선11 선택 상태): `{F11_SELECTION.as_posix()}`
- Grok initial review(그록 초기 검토): `{summary['grok_initial']['output']}`
- Grok adjusted review(그록 수정 검토): `{summary['grok_adjusted']['output']}`
- XGBoost helper(엑스지부스트 도우미): `{XGB_HELPER.as_posix()}`
- CatBoost helper(캣부스트 도우미): `{CAT_HELPER.as_posix()}`
- ONNX bridge(ONNX 연결): `{ONNX_BRIDGE.as_posix()}`
- EA entrypoint(EA 진입점): `{EA_ENTRYPOINT.as_posix()}`
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier19A Stage Open Report(전선19A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier19(전선19)를 boosted backbone no-repair-stack ONNX scout(부스팅 백본 수리 중첩 없는 ONNX 탐색)로 열었습니다.

Effect(효과): 최근 F15~F18(전선15~18)의 repair stack(수리 중첩) 실패를 반복하지 않고, pre-registered max 4 variants(사전 등록 최대 4개 변형)만 Frontier19B(전선19B)에서 시험하게 합니다.

Grok initial classification(그록 초기 분류): `{summary['grok_initial']['classification']}`

Grok adjusted classification(그록 수정 분류): `{summary['grok_adjusted']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Variant count(변형 수): `{len(summary['model_variants'])}`

Lock count(잠금 수): `{len(summary['locks'])}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Review Index(전선19 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok initial needs_local_verification(그록 초기 로컬 검증 필요), Grok adjusted accepted(그록 수정 수용), backbone-only locks(백본 단독 잠금), runtime probe obligation(런타임 탐침 의무) recorded(기록).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier19A Required Gate Coverage Audit(전선19A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_locks(잠금 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): hypothesis/controls/success/failure/invalid/stop/evidence(가설/통제/성공/실패/무효/중단/근거) recorded(기록).
- external_review_packet(외부 검토 묶음): Grok adjusted accepted(그록 수정 수용), packet(묶음) `{summary['grok_adjusted']['packet']}`.
- backbone_variant_lock_gate(백본 변형 잠금 게이트): 4 variants(변형 4개) fixed before Frontier19B metrics(전선19B 지표 전 고정).
- do_not_repeat_lock_gate(반복 금지 잠금 게이트): F11/F15~F18/Stage17~18(전선11/15~18/17~18단계) repeat risks(반복 위험) recorded(기록).
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): runtime probe or exact blocker before closeout(마감 전 런타임 탐침 또는 정확한 차단 사유) recorded(기록).
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier19 Selection Status(전선19 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier19 Boosted Backbone No Repair Stack ONNX Scout(결정: 전선19 부스팅 백본 수리 중첩 없는 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier19(전선19)를 capped backbone-only hypothesis lifecycle(상한 있는 백본 단독 가설 생명주기)로 열었습니다.

Effect(효과): F19B(전선19B)는 4개 model variants(모델 변형)만 시험하며, threshold/veto/firewall/lifecycle/quota/stability selector repair(임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리)를 추가하지 않습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(f03b.WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier19_stage_open_grok_adjusted_accepted_backbone_only_locks_no_authority",
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
        "primary_kpi": f"grok_adjusted={summary['grok_adjusted']['classification']};variants={len(MODEL_VARIANTS)};locks={len(LOCKS)}",
        "guardrail_kpi": "no_model_training_no_wfo_no_mt5_no_authority(모델 학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_required_before_closeout(그록 단계 개방 검토 완료, 마감 전 런타임 탐침 필요)",
        "notes": f"next={NEXT_RUN_ID};backbone_only_locks;no_authority",
        "question": "Can capped boosted-tree backbone-only scout create a forward clue without repair stacking?(상한 있는 부스팅 트리 백본 단독 탐색이 수리 중첩 없이 전진 단서를 만들 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR19-BOOSTED-BACKBONE-NO-REPAIR-STACK-ONNX-SCOUT`: `{RUN_ID}` opens backbone-only boosted-tree scout(백본 단독 부스팅 트리 탐색). "
        "Effect(효과): F15~F18 repair stack(수리 중첩)을 반복하지 않고 model backbone(모델 백본) 축만 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier19(전선19) after Grok adjusted accepted(그록 수정 수용). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` is locked to max 4 backbone variants(최대 4 백본 변형) with no repair stack(수리 중첩 없음).\n"
    )


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

Action(행동): Frontier19(전선19)를 boosted backbone no-repair-stack ONNX scout(부스팅 백본 수리 중첩 없는 ONNX 탐색)로 열었습니다.

Effect(효과): 다음 실행은 4 pre-registered backbone variants(사전 등록 백본 변형 4개)만 proxy(프록시)로 시험하며, threshold/veto/firewall/lifecycle/quota/stability selector repair(임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리)를 추가하지 않습니다.

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


def read_feature_order() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


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
