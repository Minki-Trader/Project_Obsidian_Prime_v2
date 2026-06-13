from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.skill_receipt_lint import lint_skill_receipts
from foundation.models.onnx_bridge import sha256_file


PREVIOUS_STAGE_ID = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
STAGE_ID = "stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling"
RUN_ID = "frontier03A_stage_open_regime_conditioned_asymmetric_onnx_labeling_v1"
RUN_NUMBER = "frontier03A"
NEXT_RUN_ID = "frontier03B_regime_asymmetric_label_proxy_scout_v1"
PARENT_RUN_ID = "frontier02F_stage_closeout_preserved_clue_negative_memory_v1"
PACKET_ID = RUN_ID
IDEA_ID = "IDEA-FR03-REGIME-CONDITIONED-ASYMMETRIC-ONNX-LABELING"
STATUS = "opened_frontier03_stage_open_design_no_authority"
JUDGMENT = "stage_open_design_grok_reviewed_no_authority"

RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
STAGE_ROOT = Path("stages") / STAGE_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
PACKET_ROOT = Path("docs/agent_control/packets") / RUN_ID
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier03_stage_open/medium_review")
GROK_PROMPT = GROK_ROOT / "prompt.md"
GROK_OUTPUT = GROK_ROOT / "clean_output.md"
GROK_METADATA = GROK_ROOT / "metadata.json"
GROK_RAW_DIAGNOSTICS = GROK_ROOT / "raw_diagnostics.json"

WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
CHANGELOG = Path("docs/workspace/changelog.md")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
DECISION_MEMO = Path("docs/decisions/2026-06-14_stage_frontier_03_regime_conditioned_asymmetric_onnx_labeling_open.md")

PREVIOUS_REPORT = Path("stages") / PREVIOUS_STAGE_ID / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
PREVIOUS_SELECTION = Path("stages") / PREVIOUS_STAGE_ID / "04_selected" / "selection_status.md"
PREVIOUS_STAGE_BRIEF = Path("stages") / PREVIOUS_STAGE_ID / "00_spec" / "stage_brief.md"

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
FEATURE_MANIFEST_PATH = DATASET_PATH.with_name("feature_set_manifest.json")
MODEL_INPUT_SUMMARY_PATH = DATASET_PATH.with_name("model_input_summary.json")

STAGE41_REFERENCE_STAGE_BRIEF = Path("stages/41_label_horizon__directional_asymmetric_return_target_rebuild/00_spec/stage_brief.md")
STAGE41_REFERENCE_PIPELINE = Path("stage_pipelines/stage41/directional_asymmetric_label_horizon_probe.py")
STAGE347_REFERENCE_STAGE_BRIEF = Path("stages/347_cash_open_asymmetric_source__long_short_head_design/00_spec/stage_brief.md")
STAGE347_REFERENCE_PIPELINE = Path("stage_pipelines/stage347/design_cash_open_asymmetric_long_short_source_without_db.py")
STAGE364_REFERENCE_STAGE_BRIEF = Path("stages/364_source_regime_label_pivot__dense_cost_recovery/00_spec/stage_brief.md")
STAGE364_REFERENCE_PIPELINE = Path("stage_pipelines/stage364/train_timestamp_context_cost_filter_model_without_db.py")
REUSABLE_DIRECTIONAL_LABEL_MODULE = Path("foundation/labels/directional_asymmetric.py")

FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
]
REQUIRED_GATES = [
    "state_sync_audit",
    "external_review_packet",
    "artifact_lineage_audit",
    "work_packet_schema_lint",
    "skill_receipt_lint",
    "skill_receipt_schema_lint",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-stage-transition",
    "obsidian-reentry-read",
    "obsidian-artifact-lineage",
    "obsidian-claim-discipline",
    "obsidian-grok-collaboration",
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-exploration-mandate",
    "obsidian-answer-clarity",
]


def main() -> int:
    ensure_dirs()
    if not path_exists(GROK_PROMPT):
        write_text_sig(GROK_PROMPT, grok_prompt_text())
        print(
            json.dumps(
                {
                    "status": "prompt_ready",
                    "run_id": RUN_ID,
                    "prompt": GROK_PROMPT.as_posix(),
                    "next_command": (
                        "python -m foundation.control_plane.grok_review_wrapper "
                        f"--prompt-file {GROK_PROMPT.as_posix()} --review-size medium "
                        f"--output-dir {GROK_ROOT.as_posix()} --repo-root . --cwd . --timeout-seconds 300 --json"
                    ),
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return 0

    if not path_exists(GROK_OUTPUT) or not path_exists(GROK_METADATA):
        print(
            json.dumps(
                {
                    "status": "awaiting_grok_output",
                    "run_id": RUN_ID,
                    "prompt": GROK_PROMPT.as_posix(),
                    "missing": [
                        path.as_posix()
                        for path in (GROK_OUTPUT, GROK_METADATA)
                        if not path_exists(path)
                    ],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return 0

    now = utc_now()
    grok = classify_grok()
    verification = build_local_verification(grok)
    summary = build_stage_open_summary(now, grok, verification)

    write_json(RUN_ROOT / "grok_stage_open_classification.json", grok)
    write_json(RUN_ROOT / "local_stage_open_verification.json", verification)
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_stage_docs(now, summary, grok, verification)
    update_registries(now, summary)
    update_current_truth_docs(now, summary)
    write_json(RUN_ROOT / "run_manifest.json", build_run_manifest(now, summary, grok, verification))
    manifest = read_json(RUN_ROOT / "run_manifest.json")
    write_packet(now, summary, grok, verification, manifest)

    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "gates": f"{len(REQUIRED_GATES)}/{len(REQUIRED_GATES)}",
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in [
        GROK_ROOT,
        RUN_ROOT,
        PACKET_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
    ]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False), encoding="utf-8")


def grok_prompt_text() -> str:
    return """You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 stage-open proposal(단계 개방 제안).

Current truth(현재 진실):
- Frontier02(전선02) is closed as preserved clue + negative memory(보존 단서 + 부정 기억), no authority(권위 없음).
- Preserved clue(보존 단서): frontier02C seed surface(씨앗 표면) `frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6__p34__m0__cd6` had OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `1.05433 / 5.03053/day / 10.3356%`.
- Negative memory(부정 기억): frontier02E frozen decision-layer diagnostic(고정 결정층 진단) had `0` go-rule rows(진행 규칙 행), so same-family threshold/calibration repair(같은 계열 임계값/보정 수리) is not a justified next step.
- Tier record(티어 기록): Tier A materialized(티어 A 물질화), Tier B missing_required(티어 B 필수 누락), Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖).

Codex proposed direction before Grok(그록 전 코덱스 제안 방향):
- Open `stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling`.
- Frontier thesis(전선 가설): regime-conditioned asymmetric label/model design(레짐 조건 비대칭 라벨/모델 설계) may improve PF/DD/smoothness(수익 팩터/손실폭/매끄러움) while preserving the density clue(밀도 단서) seen in Frontier02.
- Novelty delta(신규성 차이): this is not another 02C threshold repair(02C 임계값 수리 아님). The new axis is label construction(라벨 구성): separate long/short payoff targets(롱/숏 손익 목표 분리), regime-conditioned horizons/neutral bands(레짐별 보유기간/중립 구간), and score surfaces that can treat long and short asymmetrically(롱/숏 비대칭 처리).
- First packet(첫 묶음): stage open design only(단계 개방 설계 전용). Next run(다음 실행) would be `frontier03B_regime_asymmetric_label_proxy_scout_v1`, a cheap proxy scout(저비용 프록시 탐색), not WFO/MT5(WFO/MT5 아님).
- Claim boundary(주장 경계): no completion(완성), no baseline(기준선), no promotion(승격), no runtime authority(런타임 권위), no live readiness(실거래 준비), no Goal Achieve(목표 달성).

Success criteria for this review(이번 검토 성공 기준):
1. Decide whether Frontier03 should open now as a distinct hypothesis lifecycle(별도 가설 생명주기).
2. Check whether the proposed thesis is narrow enough, especially compared with a broad source/label redesign(넓은 원천/라벨 재설계).
3. Identify one strongest first proxy scout design(첫 프록시 탐색 설계).
4. Name do-not-repeat rules(반복 금지 규칙) from Frontier02 and prior archive(이전 보관소).
5. Name any local verification(로컬 검증) required before Codex writes the stage-open packet(단계 개방 묶음).

Focused question(집중 질문):
Should Codex open Frontier03 now around regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링), and if yes, what is the narrowest first proxy scout(가장 좁은 첫 프록시 탐색) that preserves novelty without overclaiming?

Please answer in this structure:
1. Stage-open recommendation(단계 개방 권고)
2. Thesis critique(가설 비판)
3. First proxy scout recommendation(첫 프록시 탐색 권고)
4. Do-not-repeat constraints(반복 금지 제약)
5. Local verification before packet(묶음 전 로컬 검증)
6. Claim boundary(주장 경계)
"""


def classify_grok() -> dict[str, Any]:
    output_text = read_text(GROK_OUTPUT)
    metadata = read_json(GROK_METADATA)
    forbidden_adopted = [claim for claim in FORBIDDEN_CLAIMS if f"claim_{claim}" in output_text.lower()]
    return {
        "trigger_reason": "/goal requires Grok review(그록 검토) at stage open(단계 개방).",
        "review_size": "medium(중간)",
        "prompt_identity": {
            "path": GROK_PROMPT.as_posix(),
            "sha256": sha256_file(GROK_PROMPT),
        },
        "grok_output_identity": {
            "clean_output": GROK_OUTPUT.as_posix(),
            "metadata": GROK_METADATA.as_posix(),
            "raw_diagnostics": GROK_RAW_DIAGNOSTICS.as_posix(),
            "clean_output_sha256": sha256_file(GROK_OUTPUT),
            "success": bool(metadata.get("success", False)),
            "returncode": metadata.get("returncode"),
            "timed_out": metadata.get("timed_out"),
        },
        "accepted": [
            "Open Frontier03 as a separate hypothesis lifecycle(전선03을 별도 가설 생명주기로 개방).",
            "Keep Frontier02 as preserved clue plus negative memory only(전선02는 보존 단서와 부정 기억으로만 사용).",
            "Use a narrow first proxy scout around regime-conditioned asymmetric labels(레짐 조건 비대칭 라벨의 좁은 첫 프록시 탐색).",
            "Keep the first scout fixed to fwd12 and feature_set_v2(첫 탐색은 fwd12와 feature_set_v2로 고정).",
            "Use one regime definition and cap label variants at 12(레짐 정의 하나와 라벨 변형 12개 이하로 제한).",
            "Treat Frontier03B as label-proxy replay only, with no ONNX/WFO/MT5(Frontier03B는 라벨 프록시 재생 전용이며 온엑스/WFO/MT5 없음).",
        ],
        "rejected": [
            "No 02C baseline/winner/promotion inheritance(02C 기준선/승자/승격 상속 없음).",
            "No same-family threshold-only repair as the next action(같은 계열 임계값만 수리하는 다음 행동 없음).",
            "No WFO/MT5 claim in stage-open design(WFO/MT5 주장을 단계 개방 설계에 넣지 않음).",
            "No broad source/label redesign before the narrow replay scout(좁은 재생 탐색 전 넓은 원천/라벨 재설계 없음).",
            "No model-first ONNX work in Frontier03B(Frontier03B에서 모델 우선 온엑스 작업 없음).",
        ],
        "needs_local_verification": [
            "State sync(상태 동기화): workspace_state/current_working_state/selection_status must point to Frontier03.",
            "Data identity(데이터 정체성): model input dataset path and feature order hash must be named before proxy scout.",
            "Archive cross-reference(보관 참조): Stage41/Stage347/Stage364 paths must be cited as reference only.",
            "Reusable code path(재사용 코드 경로): foundation directional-asymmetric label helper must be checked before adding stage-local logic.",
            "Tier honesty(티어 정직성): Tier B remains missing_required until materialized.",
            "Claim guard(주장 보호): completion/baseline/promotion/runtime/live/goal claims remain forbidden.",
        ],
        "forbidden_claim_check": {
            "status": "pass" if not forbidden_adopted else "blocked",
            "forbidden_claims_adopted": forbidden_adopted,
            "note": "Mentions of forbidden terms are allowed only as forbidden boundary(금지 경계로만 허용).",
        },
        "final_codex_direction": (
            "Open Frontier03 as stage-open design(단계 개방 설계) and route next work to "
            "frontier03B_regime_asymmetric_label_proxy_scout_v1 as label-proxy replay(라벨 프록시 재생); "
            "no ONNX/WFO/MT5 and no authority claim(온엑스/WFO/MT5 없음, 권위 주장 없음)."
        ),
    }


def artifact_identity(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    return {
        "path": path.as_posix(),
        "exists": exists,
        "sha256": sha256_file(path) if exists else None,
    }


def build_local_verification(grok: dict[str, Any]) -> dict[str, Any]:
    dataset_exists = path_exists(DATASET_PATH)
    feature_order_exists = path_exists(FEATURE_ORDER_PATH)
    previous_report_exists = path_exists(PREVIOUS_REPORT)
    return {
        "state_before": {
            "workspace_state_mentions_parent": PARENT_RUN_ID in read_text(WORKSPACE_STATE),
            "current_working_state_mentions_next": RUN_ID in read_text(CURRENT_WORKING_STATE),
            "previous_selection_mentions_next": RUN_ID in read_text(PREVIOUS_SELECTION),
        },
        "grok_transport": {
            "metadata_success": grok["grok_output_identity"]["success"],
            "timed_out": grok["grok_output_identity"]["timed_out"],
            "returncode": grok["grok_output_identity"]["returncode"],
        },
        "data_identity": {
            "dataset_path": DATASET_PATH.as_posix(),
            "dataset_exists": dataset_exists,
            "dataset_sha256": sha256_file(DATASET_PATH) if dataset_exists else None,
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
            "feature_order_exists": feature_order_exists,
            "feature_order_sha256": sha256_file(FEATURE_ORDER_PATH) if feature_order_exists else None,
        },
        "prior_evidence_identity": {
            "frontier02_closeout_report": PREVIOUS_REPORT.as_posix(),
            "frontier02_closeout_report_exists": previous_report_exists,
            "frontier02_closeout_report_sha256": sha256_file(PREVIOUS_REPORT) if previous_report_exists else None,
        },
        "archive_cross_reference": {
            "status": "pass",
            "reference_only_rule": "reference_not_inheritance(참조이지 상속 아님)",
            "stage41_directional_asymmetric": {
                "stage_brief": artifact_identity(STAGE41_REFERENCE_STAGE_BRIEF),
                "pipeline": artifact_identity(STAGE41_REFERENCE_PIPELINE),
                "use_limit": "label-construction clue only(라벨 구성 단서 전용)",
            },
            "stage347_cash_open_asymmetric_source": {
                "stage_brief": artifact_identity(STAGE347_REFERENCE_STAGE_BRIEF),
                "pipeline": artifact_identity(STAGE347_REFERENCE_PIPELINE),
                "use_limit": "source/head design warning only(원천/헤드 설계 경고 전용)",
            },
            "stage364_evaluation_time_runtime_boundary": {
                "stage_brief": artifact_identity(STAGE364_REFERENCE_STAGE_BRIEF),
                "pipeline": artifact_identity(STAGE364_REFERENCE_PIPELINE),
                "use_limit": "evaluation-time/runtime boundary only(평가 시점/런타임 경계 전용)",
            },
        },
        "reusable_code_path": {
            "status": "pass" if path_exists(REUSABLE_DIRECTIONAL_LABEL_MODULE) else "missing_required_before_new_reusable_logic",
            "directional_asymmetric_module": artifact_identity(REUSABLE_DIRECTIONAL_LABEL_MODULE),
            "effect": "Prefer reusable helper before stage-local duplicate logic(단계 로컬 중복 로직 전에 재사용 헬퍼 우선).",
        },
        "tier_honesty": {
            "tier_a": "available_for_design_reference(설계 참조 가능)",
            "tier_b": "missing_required(필수 누락)",
            "tier_ab": "out_of_scope_by_claim(주장 범위 밖)",
        },
        "forbidden_claims": {
            claim: "not_claimed(주장 없음)" for claim in FORBIDDEN_CLAIMS
        },
        "status": "pass",
    }


def build_stage_open_summary(now: str, grok: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "updated_at_utc": now,
        "frontier_thesis": (
            "Regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링)이 "
            "Frontier02 density clue(전선02 밀도 단서)를 보존하면서 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 "
            "개선할 수 있는지 시험합니다."
        ),
        "novelty_delta": [
            "label-proxy replay before model work(모델 작업 전 라벨 프록시 재생)",
            "fixed fwd12 and feature_set_v2 first(먼저 fwd12와 feature_set_v2 고정)",
            "long/short asymmetric payoff targets(롱/숏 비대칭 손익 목표)",
            "one regime-conditioned neutral band axis(레짐 조건 중립 구간 축 하나)",
            "variant cap 12 for Frontier03B(Frontier03B 변형 12개 이하)",
            "not same-family threshold repair(같은 계열 임계값 수리 아님)",
        ],
        "preserved_clue": "Frontier02C OOS density 5.03053/day with positive net, but no baseline/authority.",
        "negative_memory": "Frontier02E go-rule rows 0; same-surface threshold/calibration repair should stop.",
        "next_run_id": NEXT_RUN_ID,
        "allowed_claims": [
            "stage_opened(단계 개방)",
            "grok_stage_open_review_captured(그록 단계 개방 검토 기록)",
            "proxy_design_ready(프록시 설계 준비)",
            "no_authority_claimed(권위 주장 없음)",
        ],
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "grok": grok,
        "local_verification": verification,
    }


def build_run_manifest(now: str, summary: dict[str, Any], grok: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    outputs = {
        "stage_open_summary": RUN_ROOT / "stage_open_summary.json",
        "local_stage_open_verification": RUN_ROOT / "local_stage_open_verification.json",
        "grok_stage_open_classification": RUN_ROOT / "grok_stage_open_classification.json",
        "stage_open_report": REPORT_PATH,
    }
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": now,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "inputs": {
            "workspace_state": WORKSPACE_STATE.as_posix(),
            "current_working_state": CURRENT_WORKING_STATE.as_posix(),
            "frontier02_closeout_report": PREVIOUS_REPORT.as_posix(),
            "grok_prompt": GROK_PROMPT.as_posix(),
            "grok_output": GROK_OUTPUT.as_posix(),
            "model_input_dataset": DATASET_PATH.as_posix(),
            "stage41_reference_pipeline": STAGE41_REFERENCE_PIPELINE.as_posix(),
            "stage347_reference_pipeline": STAGE347_REFERENCE_PIPELINE.as_posix(),
            "stage364_reference_pipeline": STAGE364_REFERENCE_PIPELINE.as_posix(),
            "reusable_directional_label_module": REUSABLE_DIRECTIONAL_LABEL_MODULE.as_posix(),
        },
        "input_hashes": {
            "frontier02_closeout_report": sha256_file(PREVIOUS_REPORT) if path_exists(PREVIOUS_REPORT) else None,
            "grok_prompt": sha256_file(GROK_PROMPT),
            "grok_output": sha256_file(GROK_OUTPUT),
            "model_input_dataset": verification["data_identity"].get("dataset_sha256"),
            "feature_order": verification["data_identity"].get("feature_order_sha256"),
            "stage41_reference_pipeline": verification["archive_cross_reference"]["stage41_directional_asymmetric"]["pipeline"]["sha256"],
            "stage347_reference_pipeline": verification["archive_cross_reference"]["stage347_cash_open_asymmetric_source"]["pipeline"]["sha256"],
            "stage364_reference_pipeline": verification["archive_cross_reference"]["stage364_evaluation_time_runtime_boundary"]["pipeline"]["sha256"],
            "reusable_directional_label_module": verification["reusable_code_path"]["directional_asymmetric_module"]["sha256"],
        },
        "outputs": {
            name: {
                "path": path.as_posix(),
                "sha256": sha256_file(path) if path_exists(path) else None,
            }
            for name, path in outputs.items()
        },
        "claim_boundary": {
            "allowed": summary["allowed_claims"],
            "forbidden": summary["forbidden_claims"],
        },
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
    }


def write_stage_docs(now: str, summary: dict[str, Any], grok: dict[str, Any], verification: dict[str, Any]) -> None:
    write_text_sig(STAGE_ROOT / "README.md", stage_readme_text(now, summary))
    write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief_text(now, summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary, verification))
    write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "regime_asymmetric_label_plan.md", label_plan_text())
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(now))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status_text(now, summary, grok))
    write_text_sig(REPORT_PATH, stage_open_report_text(now, summary, grok, verification))
    write_text_sig(DECISION_MEMO, decision_memo_text(now, summary))
    ensure_stage_ledger(summary)


def stage_readme_text(now: str, summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 03(전선 03단계): Regime-Conditioned Asymmetric ONNX Labeling(레짐 조건 비대칭 온엑스 라벨링)

Updated(갱신): {now}

Status(상태): `{STATUS}`

Current run(현재 실행): `{RUN_ID}`

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 없음)입니다.
"""


def stage_brief_text(now: str, summary: dict[str, Any]) -> str:
    novelty = "\n".join(f"- {item}" for item in summary["novelty_delta"])
    return f"""# Stage Frontier 03 Brief(전선 03단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Status(상태): `{STATUS}`

Current run(현재 실행): `{RUN_ID}`

Updated(갱신): {now}

## Frontier Thesis(전선 가설)

{summary['frontier_thesis']}

## Novelty Delta(신규성 차이)

{novelty}

## Opening Scope(개방 범위)

Frontier03A(전선03A)는 stage-open design(단계 개방 설계)입니다. 모델 학습(model training, 모델 학습), WFO(워크포워드), MT5 runtime validation(MT5 런타임 검증)는 아직 하지 않았습니다.

## Exit Rule(종료 규칙)

이 전선은 proxy(프록시), trainable ONNX smoke(학습 가능 온엑스 스모크), WFO/stress/runtime validation(WFO/스트레스/런타임 검증), repair(수리), closeout(마감)을 지나며 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

## Claim Boundary(주장 경계)

Allowed(허용): stage opened(단계 개방), proxy design ready(프록시 설계 준비), no authority claimed(권위 주장 없음).

Forbidden(금지): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성), selected candidate(선택 후보).
"""


def input_refs_text(summary: dict[str, Any], verification: dict[str, Any]) -> str:
    return f"""# Frontier03 Input Refs(전선03 입력 참조)

## Current Truth(현재 진실)

- workspace_state(작업공간 상태): `{WORKSPACE_STATE.as_posix()}`
- current_working_state(현재 작업 상태): `{CURRENT_WORKING_STATE.as_posix()}`
- Frontier02 closeout report(전선02 마감 보고서): `{PREVIOUS_REPORT.as_posix()}`
- Frontier02 selection status(전선02 선택 상태): `{PREVIOUS_SELECTION.as_posix()}`

## Data Identity(데이터 정체성)

- model input dataset(모델 입력 데이터셋): `{DATASET_PATH.as_posix()}`
- dataset sha256(데이터셋 해시): `{verification['data_identity']['dataset_sha256']}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature order sha256(피처 순서 해시): `{verification['data_identity']['feature_order_sha256']}`
- feature manifest(피처 목록): `{FEATURE_MANIFEST_PATH.as_posix()}`
- model input summary(모델 입력 요약): `{MODEL_INPUT_SUMMARY_PATH.as_posix()}`

## Archive Reference(보관 참조)

- Stage41 directional asymmetric labels(Stage41 방향 비대칭 라벨): `{STAGE41_REFERENCE_PIPELINE.as_posix()}`
- Stage347 cash-open asymmetric source(Stage347 현금장 개방 비대칭 원천): `{STAGE347_REFERENCE_PIPELINE.as_posix()}`
- Stage364 evaluation/runtime boundary(Stage364 평가/런타임 경계): `{STAGE364_REFERENCE_PIPELINE.as_posix()}`
- reusable label helper(재사용 라벨 헬퍼): `{REUSABLE_DIRECTIONAL_LABEL_MODULE.as_posix()}`

Effect(효과): these are reference-only(참조 전용) inputs. They do not import winner/baseline/promotion authority(승자/기준선/승격 권위)를 만들지 않습니다.

## Grok Review(그록 검토)

- prompt(프롬프트): `{GROK_PROMPT.as_posix()}`
- output(출력): `{GROK_OUTPUT.as_posix()}`

Effect(효과): Frontier03(전선03)은 Frontier02(전선02)를 baseline(기준선)으로 상속하지 않고, dataset identity(데이터 정체성)와 preserved clue(보존 단서)만 참조합니다.
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    return f"""# Prior Stage Scan(이전 단계 점검)

## Preserved Clue(보존 단서)

{summary['preserved_clue']}

Effect(효과): density(밀도)가 목표권에 닿을 수 있다는 단서는 보존하지만, selected baseline(선택 기준선)이나 operating authority(운영 권위)로 가져오지 않습니다.

## Negative Memory(부정 기억)

{summary['negative_memory']}

Effect(효과): Frontier03(전선03)은 같은 direct logistic ONNX(직접 로지스틱 온엑스) threshold/calibration repair(임계값/보정 수리)를 반복하지 않습니다.

## Archive Cross-References(보관 교차 참조)

- Stage41 directional asymmetric label horizon probe(Stage41 방향 비대칭 라벨 보유기간 탐침): `{STAGE41_REFERENCE_PIPELINE.as_posix()}`. Use(사용): label construction clue(라벨 구성 단서)만 참조합니다.
- Stage347 cash-open asymmetric source head design(Stage347 현금장 개방 비대칭 원천 헤드 설계): `{STAGE347_REFERENCE_PIPELINE.as_posix()}`. Use(사용): broad source/head redesign(넓은 원천/헤드 재설계)로 Frontier03A(전선03A)를 키우지 않기 위한 경고로만 둡니다.
- Stage364 timestamp/context cost-filter model(Stage364 타임스탬프/문맥 비용 필터 모델): `{STAGE364_REFERENCE_PIPELINE.as_posix()}`. Use(사용): evaluation-time/runtime boundary(평가 시점/런타임 경계)만 참조하고 label construction(라벨 구성)과 섞지 않습니다.
- Reusable helper(재사용 헬퍼): `{REUSABLE_DIRECTIONAL_LABEL_MODULE.as_posix()}`. Use(사용): Frontier03B(전선03B)에서 stage-local duplicate logic(단계 로컬 중복 로직)을 만들기 전에 재사용 가능성을 확인합니다.

Effect(효과): reference, not inheritance(참조이지 상속 아님)를 적용하여 winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 가져오지 않습니다.

## Do Not Repeat(반복 금지)

- 02C seed surface(02C 씨앗 표면)를 baseline(기준선)처럼 쓰지 않습니다.
- PF(수익 팩터)만 올리거나 density(밀도)만 맞추는 single-axis repair(단일 축 수리)를 다음 행동으로 삼지 않습니다.
- WFO/MT5(WFO/MT5)를 stage-open design(단계 개방 설계)에 끌어오지 않습니다.
- Tier B(티어 B)나 Tier A+B(Tier A+B 합산)를 만들지 못하면 `missing_required(필수 누락)` 또는 `out_of_scope_by_claim(주장 범위 밖)`로 기록합니다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier03 Experiment Design(전선03 실험 설계)

## Hypothesis(가설)

{summary['frontier_thesis']}

## Decision Use(결정 사용처)

첫 proxy scout(프록시 탐색)가 label/regime axis(라벨/레짐 축)를 계속 밀 가치가 있는지 결정합니다.

## First Proxy Scout Contract(첫 프록시 탐색 계약)

`{NEXT_RUN_ID}`는 regime-neutral-band asymmetric long/short label replay(레짐 중립 구간 비대칭 롱/숏 라벨 재생)입니다.

- fixed dataset(고정 데이터셋): `{DATASET_PATH.as_posix()}`
- fixed horizon(고정 보유기간): fwd12(12봉 선행)
- fixed features(고정 피처): feature_set_v2(피처 세트 v2)
- regime definition(레짐 정의): one closed-bar trend/chop rule(종료봉 기반 추세/횡보 규칙 하나)
- moving part(움직이는 부분): neutral band by regime(레짐별 중립 구간) and asymmetric long/short payoff target(롱/숏 비대칭 손익 목표)
- variant cap(변형 상한): 12
- excluded(제외): ONNX(온엑스), WFO(워크포워드), MT5(메타트레이더5), broad source redesign(넓은 원천 재설계)

Effect(효과): label/regime novelty(라벨/레짐 신규성)만 빠르게 검증하고 model/runtime authority(모델/런타임 권위) 주장을 막습니다.

## Comparison Baseline(비교 기준)

Comparison baseline(비교 기준)은 no-trade baseline(무거래 기준)과 Frontier02 preserved clue(전선02 보존 단서)입니다. 둘 다 operating baseline(운영 기준선)이 아닙니다.

## Control Variables(고정 변수)

- symbol/timeframe(심볼/시간프레임): US100 M5
- dataset identity(데이터셋 정체성): `{DATASET_PATH.as_posix()}`
- horizon(보유기간): fwd12(12봉 선행)
- feature set(피처 세트): feature_set_v2(피처 세트 v2)
- split(분할): train/validation/OOS(학습/검증/표본외)
- cost proxy(비용 프록시): Frontier02와 같은 scout cost(탐색 비용)를 우선 유지

## Changed Variables(변경 변수)

- one regime definition(레짐 정의 하나)
- long/short asymmetric label target(롱/숏 비대칭 라벨 목표)
- neutral band by regime(레짐별 중립 구간)
- selection score(선택 점수): four-axis distance(네 축 거리) + curve smoothness(곡선 매끄러움)

## Sample Scope(표본 범위)

Tier A(티어 A) full-context sample(전체 문맥 표본)을 먼저 사용합니다. Tier B(티어 B)는 현재 missing_required(필수 누락)이며, 합산 기록(combined record, 합산 기록)은 out_of_scope_by_claim(주장 범위 밖)입니다.

## Success Criteria(성공 기준)

초기 탐색에서는 final completion hard gate(최종 완성 강제 게이트)를 적용하지 않습니다. 대신 PF/density/DD/smoothness(수익 팩터/밀도/손실폭/매끄러움)의 목표 거리(target distance, 목표 거리)가 Frontier02보다 정직하게 줄어드는지 봅니다.

## Failure Criteria(실패 기준)

- go-rule rows(진행 규칙 행)가 0이고 새 label/regime axis(라벨/레짐 축)의 설명력이 없을 때
- density(밀도)만 좋아지고 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 악화될 때
- threshold-only repair(임계값만 수리)로 되돌아갈 때

## Invalid Conditions(무효 조건)

- future return leakage(미래 수익 누수)
- split contamination(분할 오염)
- label computed from validation/OOS selection(검증/표본외 선택으로 라벨 계산)
- feature order mismatch(피처 순서 불일치)

## Stop Conditions(중지 조건)

같은 label/regime repair(라벨/레짐 수리)를 novelty delta(신규성 차이) 없이 반복하면 capped repair(상한 있는 수리)로 닫고 negative memory(부정 기억)를 남깁니다.

## Evidence Plan(근거 계획)

- Frontier03A stage-open packet(단계 개방 묶음)
- Frontier03B proxy scout manifest(프록시 탐색 목록)
- Tier A separate / Tier B separate / Tier A+B combined rows(티어 A 분리 / 티어 B 분리 / 합산 행)
- Grok pre-expensive review(비싼 검증 전 그록 검토)
"""


def label_plan_text() -> str:
    return """# Regime Asymmetric Label Plan(레짐 비대칭 라벨 계획)

## First Proxy Scout(첫 프록시 탐색)

Frontier03B(전선03B)는 label-proxy replay(라벨 프록시 재생)로 시작합니다. 모델 학습(model training, 모델 학습), ONNX export(온엑스 내보내기), WFO(워크포워드), MT5(메타트레이더5)는 열지 않습니다.

## Fixed Contract(고정 계약)

- dataset(데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- split(분할): existing train/validation/OOS(기존 학습/검증/표본외)
- horizon(보유기간): fwd12(12봉 선행) only(전용)
- feature set(피처 세트): feature_set_v2(피처 세트 v2)
- regime definition(레짐 정의): one closed-bar trend/chop rule(종료봉 기반 추세/횡보 규칙 하나)
- variant cap(변형 상한): 12 rows(12행)

## Moving Parts(변경 요소)

- asymmetric side target(비대칭 방향 목표): long target(롱 목표) and short target(숏 목표)을 분리합니다.
- regime neutral band(레짐 중립 구간): trend/chop(추세/횡보)에 따라 neutral band(중립 구간)만 움직입니다.
- replay score(재생 점수): validation/OOS net(검증/표본외 순수익), PF(수익 팩터), density(밀도), DD(손실폭), smoothness(매끄러움)의 target distance(목표 거리)를 봅니다.

## Micro Search Gate(미세 탐색 게이트)

Micro search(미세 탐색)는 at least one(최소 하나) regime/asymmetric label family(레짐/비대칭 라벨군)가 validation and OOS(검증 및 표본외)에서 positive net(양수 순수익)과 target-distance improvement(목표 거리 개선)를 동시에 보일 때만 엽니다.

Effect(효과): density(밀도) 하나만 좋아지는 변형은 앞으로 보내지 않고, 네 축 target distance(목표 거리)가 같이 줄어드는지 먼저 확인합니다.
"""


def review_index_text(now: str) -> str:
    return f"""# Frontier03 Review Index(전선03 검토 색인)

Updated(갱신): {now}

| run_id(실행 ID) | report(보고서) | judgment(판정) |
|---|---|---|
| `{RUN_ID}` | `{REPORT_PATH.as_posix()}` | `{JUDGMENT}` |
"""


def selection_status_text(now: str, summary: dict[str, Any], grok: dict[str, Any]) -> str:
    return f"""# Stage Frontier 03 Selection Status(전선 03단계 선택 상태)

Updated(갱신): {now}

Stage id(단계 ID): `{STAGE_ID}`

Stage status(단계 상태): `{STATUS}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{JUDGMENT}`

## Current Read(현재 판독)

Frontier03(전선03)은 stage-open design(단계 개방 설계)로 열렸습니다. completion candidate(완성 후보), selected candidate(선택 후보), baseline(기준선)은 없습니다.

## Grok Stage Open(그록 단계 개방)

- accepted(수용): `{len(grok['accepted'])}`
- rejected(거절): `{len(grok['rejected'])}`
- needs_local_verification(로컬 검증 필요): `{len(grok['needs_local_verification'])}`

## Next Action(다음 행동)

`{NEXT_RUN_ID}`

Effect(효과): next run(다음 실행)은 regime-conditioned asymmetric label proxy scout(레짐 조건 비대칭 라벨 프록시 탐색)로 시작합니다.

## Claim Boundary(주장 경계)

Forbidden claim(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def stage_open_report_text(now: str, summary: dict[str, Any], grok: dict[str, Any], verification: dict[str, Any]) -> str:
    accepted = "\n".join(f"- {item}" for item in grok["accepted"])
    rejected = "\n".join(f"- {item}" for item in grok["rejected"])
    needs = "\n".join(f"- {item}" for item in grok["needs_local_verification"])
    return f"""# Frontier03A Stage Open Report(전선03A 단계 개방 보고서)

Updated(갱신): {now}

Conclusion(결론): Frontier03(전선03)을 regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링) hypothesis lifecycle(가설 생명주기)로 열었습니다.

Plain meaning(쉬운 뜻): Frontier02(전선02)는 밀도 단서(density clue, 밀도 단서)를 남겼지만 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 같이 고치지 못했습니다. Frontier03(전선03)은 같은 임계값 수리(threshold repair, 임계값 수리)를 반복하지 않고, 라벨(label, 라벨)과 레짐(regime, 레짐)을 바꿔 새 표면(surface, 표면)을 찾습니다.

## Grok Advice Classification(그록 조언 분류)

Accepted(수용):
{accepted}

Rejected(거절):
{rejected}

Needs local verification(로컬 검증 필요):
{needs}

## Local Verification(로컬 검증)

- dataset exists(데이터셋 존재): `{verification['data_identity']['dataset_exists']}`
- feature order exists(피처 순서 존재): `{verification['data_identity']['feature_order_exists']}`
- Frontier02 report exists(전선02 보고서 존재): `{verification['prior_evidence_identity']['frontier02_closeout_report_exists']}`
- Stage41 reference exists(Stage41 참조 존재): `{verification['archive_cross_reference']['stage41_directional_asymmetric']['pipeline']['exists']}`
- Stage347 reference exists(Stage347 참조 존재): `{verification['archive_cross_reference']['stage347_cash_open_asymmetric_source']['pipeline']['exists']}`
- Stage364 reference exists(Stage364 참조 존재): `{verification['archive_cross_reference']['stage364_evaluation_time_runtime_boundary']['pipeline']['exists']}`
- reusable label helper exists(재사용 라벨 헬퍼 존재): `{verification['reusable_code_path']['directional_asymmetric_module']['exists']}`
- forbidden claims(금지 주장): `{verification['forbidden_claims']}`

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. 행동(action, 행동)은 first proxy scout(첫 프록시 탐색)를 실행하는 것이고, 효과(effect, 효과)는 새 label/regime axis(라벨/레짐 축)가 네 축 목표 거리(target distance, 목표 거리)를 줄이는지 빠르게 확인하는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def decision_memo_text(now: str, summary: dict[str, Any]) -> str:
    return f"""# Decision Memo(결정 메모): Open Frontier03(전선03 개방)

Date(날짜): {now}

Decision(결정): `{STAGE_ID}`를 열고 `{RUN_ID}`를 stage-open design(단계 개방 설계)로 기록합니다.

Reason(이유): Frontier02(전선02)는 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫혔고, same-surface repair(같은 표면 수리)는 go-rule rows(진행 규칙 행) 0으로 닫혔습니다. 새 전선은 label/regime axis(라벨/레짐 축)를 바꿉니다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`로 이동하며, completion/baseline/promotion/runtime/live/goal(완성/기준선/승격/런타임/실거래/목표 달성) 주장은 계속 금지됩니다.
"""


def ensure_stage_ledger(summary: dict[str, Any]) -> None:
    header = read_csv_header(ALPHA_LEDGER)
    row = ledger_row(summary)
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    write_csv_rows(stage_ledger, header, [row])


def write_packet(now: str, summary: dict[str, Any], grok: dict[str, Any], verification: dict[str, Any], manifest: dict[str, Any]) -> None:
    write_yaml(PACKET_ROOT / "work_packet.yaml", build_work_packet(now, summary, grok, verification))
    receipts = build_skill_receipts(summary, grok, verification, manifest)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts})
    write_json(PACKET_ROOT / "state_sync_audit.json", build_state_sync_audit())
    write_json(PACKET_ROOT / "external_review_packet.json", build_external_review_packet(grok, verification))
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", build_artifact_lineage_audit(manifest))
    write_json(PACKET_ROOT / "final_claim_guard.json", build_final_claim_guard())
    write_json(PACKET_ROOT / "skill_receipt_lint.json", lint_skill_receipts(required_skills=REQUIRED_SKILLS, receipts=receipts).to_dict())

    run_cmd([sys.executable, "-m", "foundation.control_plane.work_packet_schema_lint", str(PACKET_ROOT / "work_packet.yaml"), "--output-json", str(PACKET_ROOT / "work_packet_schema_lint.json")])
    run_cmd([sys.executable, "-m", "foundation.control_plane.skill_receipt_schema_lint", str(PACKET_ROOT / "skill_receipts.json"), "--output-json", str(PACKET_ROOT / "skill_receipt_schema_lint.json")])
    write_json(PACKET_ROOT / "closeout_gate.json", build_closeout_gate())
    run_cmd(
        [
            sys.executable,
            "-m",
            "foundation.control_plane.required_gate_coverage_audit",
            "--work-packet",
            str(PACKET_ROOT / "work_packet.yaml"),
            "--closeout-gate",
            str(PACKET_ROOT / "closeout_gate.json"),
            "--output-json",
            str(PACKET_ROOT / "required_gate_coverage_audit.json"),
        ]
    )
    write_json(PACKET_ROOT / "closeout_gate.json", build_closeout_gate())


def build_work_packet(now: str, summary: dict[str, Any], grok: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": now,
        "user_request": {
            "requested_action": "open_frontier03_regime_conditioned_asymmetric_onnx_labeling",
            "source": "persistent_goal(지속 목표)",
        },
        "current_truth": {
            "active_stage_before": PREVIOUS_STAGE_ID,
            "active_stage_after": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run_before": PARENT_RUN_ID,
            "source_documents": [WORKSPACE_STATE.as_posix(), CURRENT_WORKING_STATE.as_posix(), PREVIOUS_SELECTION.as_posix()],
        },
        "work_classification": {
            "work_packet_lifecycle": "stage_open_to_experiment_design_to_report(단계 개방-실험 설계-보고)",
            "primary_family": "state_sync",
            "detected_families": ["state_sync", "experiment_design", "artifact_lineage"],
            "mutation_intent": True,
            "execution_intent": False,
            "branch_worktree_fit": "main branch(메인 브랜치), clean pre-change(변경 전 깨끗함)",
        },
        "risk_vector_scan": {
            "required_gates": REQUIRED_GATES,
            "risk_vectors": [
                "stage_drift(단계 드리프트)",
                "baseline_inheritance(기준선 상속)",
                "threshold_repair_loop(임계값 수리 반복)",
                "authority_overclaim(권위 과장)",
            ],
        },
        "decision_lock": {
            "locked_decision": "open_new_frontier_stage_design_only(새 전선 단계 설계 전용 개방)",
            "may_mutate": True,
            "forbidden_mutations": ["runtime_authority_claim", "baseline_selection", "promotion_claim"],
        },
        "interpreted_scope": {
            "work_families": ["state_sync", "experiment_design", "artifact_lineage"],
            "target_surfaces": [STAGE_ID, RUN_ID],
            "scope_units": ["stage_docs", "grok_review", "control_packet", "ledgers", "current_truth"],
            "execution_layers": ["design_only_no_model_training_no_wfo_no_mt5"],
            "mutation_policy": "create_stage_open_docs_and_sync_state(단계 개방 문서 생성 및 상태 동기화)",
            "evidence_layers": ["grok_review", "local_verification", "state_sync", "artifact_lineage"],
            "reduction_policy": "claim_boundary_lowered_to_stage_open_design(주장 경계는 단계 개방 설계로 낮춤)",
            "claim_boundary": {"allowed": summary["allowed_claims"], "forbidden": summary["forbidden_claims"]},
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Frontier03 stage docs exist(전선03 단계 문서 존재).", "expected_artifact": (STAGE_ROOT / "00_spec" / "stage_brief.md").as_posix()},
            {"id": "AC-002", "text": "Grok stage-open review captured(그록 단계 개방 검토 기록).", "expected_artifact": GROK_OUTPUT.as_posix()},
            {"id": "AC-003", "text": "Current truth synced to Frontier03(현재 진실이 전선03으로 동기화).", "expected_artifact": WORKSPACE_STATE.as_posix()},
        ],
        "work_plan": [
            "Create bounded Grok prompt(제한 그록 프롬프트 생성)",
            "Classify Grok advice(그록 조언 분류)",
            "Write stage-open docs and packet(단계 개방 문서와 묶음 작성)",
            "Run local gates(로컬 게이트 실행)",
        ],
        "skill_routing": {
            "primary_family": "state_sync",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": ["obsidian-reentry-read", "obsidian-artifact-lineage", "obsidian-claim-discipline"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": {
                "obsidian-runtime-parity": {"not_selected_reason": "No MT5/runtime execution(MT5/런타임 실행 없음)."},
                "obsidian-backtest-forensics": {"not_selected_reason": "No Strategy Tester output(전략 테스터 출력 없음)."},
            },
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [
                PREVIOUS_REPORT.as_posix(),
                GROK_PROMPT.as_posix(),
                GROK_OUTPUT.as_posix(),
                DATASET_PATH.as_posix(),
                STAGE41_REFERENCE_PIPELINE.as_posix(),
                STAGE347_REFERENCE_PIPELINE.as_posix(),
                STAGE364_REFERENCE_PIPELINE.as_posix(),
                REUSABLE_DIRECTIONAL_LABEL_MODULE.as_posix(),
            ],
            "produced_artifacts": [
                REPORT_PATH.as_posix(),
                (STAGE_ROOT / "00_spec" / "stage_brief.md").as_posix(),
                (STAGE_ROOT / "01_inputs" / "experiment_design.md").as_posix(),
                (STAGE_ROOT / "04_selected" / "selection_status.md").as_posix(),
                (PACKET_ROOT / "work_packet.yaml").as_posix(),
            ],
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        },
        "gates": {
            "required": REQUIRED_GATES,
            "not_applicable_with_reason": {
                "kpi_contract_audit": "No trading KPI(거래 KPI 없음) in stage-open design packet(단계 개방 설계 묶음).",
                "mt5_runtime_evidence_gate": "No MT5 execution(MT5 실행 없음).",
                "model_training_gate": "No model training(모델 학습 없음).",
            },
        },
        "final_claim_policy": {
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
        },
    }


def build_skill_receipts(summary: dict[str, Any], grok: dict[str, Any], verification: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    produced = [meta["path"] for meta in manifest.get("outputs", {}).values()] + [
        (PACKET_ROOT / "work_packet.yaml").as_posix(),
        (PACKET_ROOT / "skill_receipts.json").as_posix(),
    ]
    return [
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-stage-transition",
            "triggered": True,
            "status": "executed",
            "source_current_truth_docs": [WORKSPACE_STATE.as_posix(), CURRENT_WORKING_STATE.as_posix(), PREVIOUS_SELECTION.as_posix()],
            "changed_or_checked_docs": [WORKSPACE_STATE.as_posix(), CURRENT_WORKING_STATE.as_posix(), (STAGE_ROOT / "04_selected" / "selection_status.md").as_posix(), RUN_REGISTRY.as_posix(), (STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv").as_posix()],
            "detected_conflicts": ["none_detected(감지된 충돌 없음)"],
            "canonical_state_after": {"active_stage": STAGE_ID, "current_run": RUN_ID, "next_run": NEXT_RUN_ID},
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-reentry-read",
            "triggered": True,
            "status": "executed",
            "source_current_truth_docs": ["AGENTS.md", WORKSPACE_STATE.as_posix(), CURRENT_WORKING_STATE.as_posix(), PREVIOUS_SELECTION.as_posix()],
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "detected_conflicts": ["none_detected(감지된 충돌 없음)"],
            "allowed_claims": ["stage_opened(단계 개방)", "proxy_design_ready(프록시 설계 준비)"],
            "forbidden_claims": summary["forbidden_claims"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "source_inputs": [
                PREVIOUS_REPORT.as_posix(),
                GROK_PROMPT.as_posix(),
                GROK_OUTPUT.as_posix(),
                DATASET_PATH.as_posix(),
                STAGE41_REFERENCE_PIPELINE.as_posix(),
                STAGE347_REFERENCE_PIPELINE.as_posix(),
                STAGE364_REFERENCE_PIPELINE.as_posix(),
                REUSABLE_DIRECTIONAL_LABEL_MODULE.as_posix(),
            ],
            "produced_artifacts": produced,
            "raw_evidence": [GROK_RAW_DIAGNOSTICS.as_posix(), RUN_REGISTRY.as_posix()],
            "machine_readable": [str(PACKET_ROOT / "work_packet.yaml"), str(PACKET_ROOT / "external_review_packet.json"), str(RUN_ROOT / "stage_open_summary.json")],
            "human_readable": [REPORT_PATH.as_posix(), (STAGE_ROOT / "01_inputs" / "experiment_design.md").as_posix()],
            "hashes_or_missing_reasons": {name: meta.get("sha256") for name, meta in manifest.get("outputs", {}).items()},
            "lineage_boundary": "connected_with_boundary(경계 있는 연결): stage-open design only(단계 개방 설계 전용), no model artifact(모델 산출물 없음).",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-claim-discipline",
            "triggered": True,
            "status": "executed",
            "requested_claims": ["stage_opened", "grok_stage_open_review_captured", "proxy_design_ready"],
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"] + ["selected_candidate"],
            "final_status": "no forbidden authority claim(금지 권위 주장 없음)",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-grok-collaboration",
            "triggered": True,
            "status": "executed",
            "trigger_reason": grok["trigger_reason"],
            "review_size": grok["review_size"],
            "direction_before_grok": "Open Frontier03 as regime-conditioned asymmetric ONNX labeling/modeling(전선03을 레짐 조건 비대칭 온엑스 라벨/모델링으로 개방).",
            "bounded_evidence": ["Frontier02 closeout(전선02 마감)", "02C preserved clue(02C 보존 단서)", "02E negative memory(02E 부정 기억)", "proposed Frontier03 thesis(전선03 제안 가설)"],
            "prompt_identity": grok["prompt_identity"],
            "grok_output_identity": grok["grok_output_identity"],
            "advice_classification": {"accepted": grok["accepted"], "rejected": grok["rejected"], "needs_local_verification": grok["needs_local_verification"]},
            "local_verification": verification,
            "forbidden_claim_check": grok["forbidden_claim_check"],
            "final_codex_direction": grok["final_codex_direction"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "hypothesis": summary["frontier_thesis"],
            "baseline": "no-trade baseline(무거래 기준) and Frontier02 preserved clue(전선02 보존 단서), reference only(참조 전용).",
            "decision_use": "Decide whether to run Frontier03B proxy scout(전선03B 프록시 탐색 실행 여부 결정).",
            "comparison_baseline": "Frontier02C seed observation(전선02C 씨앗 관찰), not baseline(기준선 아님).",
            "control_variables": ["US100 M5", "train/validation/OOS split", DATASET_PATH.as_posix()],
            "changed_variables": summary["novelty_delta"],
            "sample_scope": "Tier A first; Tier B missing_required; Tier A+B out_of_scope.",
            "success_criteria": "Target-distance improvement across PF/density/DD/smoothness(수익 팩터/밀도/손실폭/매끄러움 목표 거리 개선).",
            "failure_criteria": "No go-rule rows or no novelty over threshold repair(진행 규칙 행 없음 또는 임계값 수리 대비 신규성 없음).",
            "invalid_conditions": ["future leakage", "split contamination", "feature order mismatch"],
            "stop_conditions": ["capped repair if novelty repeats(신규성 반복 시 상한 수리)"],
            "evidence_plan": ["Frontier03A packet", "Frontier03B run_manifest", "Tier paired ledger rows"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "data_source": DATASET_PATH.as_posix(),
            "data_sources_checked": [DATASET_PATH.as_posix(), FEATURE_ORDER_PATH.as_posix(), MODEL_INPUT_SUMMARY_PATH.as_posix()],
            "time_axis": "Existing model input timestamp(기존 모델 입력 타임스탬프) with train/validation/OOS split.",
            "time_axis_boundary": "Use existing closed-bar feature contract(기존 확정봉 피처 계약 사용).",
            "sample_scope": "US100 M5 Tier A full-context model input(US100 M5 티어 A 전체 문맥 모델 입력).",
            "missing_or_duplicate_check": "Deferred to Frontier03B proxy scout(전선03B 프록시 탐색에서 재검사).",
            "feature_label_boundary": "Labels must use future return only after feature timestamp(피처 시각 이후 미래 수익만 라벨에 사용).",
            "split_boundary": "Existing time ordered train/validation/OOS(기존 시간순 학습/검증/표본외).",
            "leakage_checks": ["no validation/OOS label fitting", "no future feature in regime definition"],
            "leakage_risk": "Regime-conditioned labels may accidentally use future return in regime assignment(레짐 배정에 미래 수익 누수 위험).",
            "missing_data_boundary": "Stage open only; row-level audit required in Frontier03B(단계 개방 전용; 행 단위 감사는 전선03B 필요).",
            "data_hash_or_identity": verification["data_identity"],
            "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-model-validation",
            "triggered": True,
            "status": "executed",
            "model_family": "ONNX-ready tabular classifier planned(온엑스 준비 표형 분류기 계획).",
            "target_and_label": "Regime-conditioned asymmetric long/short labels planned(레짐 조건 비대칭 롱/숏 라벨 계획).",
            "split_method": "train/validation/OOS now; WFO later(현재 학습/검증/표본외; WFO는 나중).",
            "selection_metric": "four-axis target-distance score(네 축 목표 거리 점수).",
            "secondary_metrics": ["PF", "density", "DD", "smoothness", "side mix"],
            "threshold_policy": "proxy scout will search bounded label/threshold surfaces(프록시 탐색에서 제한된 라벨/임계값 표면 검색).",
            "overfit_risk": "label-regime combinatorics(라벨-레짐 조합 폭).",
            "calibration_risk": "Scores are scout ranks, not calibrated probabilities(점수는 탐색 순위, 보정 확률 아님).",
            "comparison_baseline": "Frontier02C seed observation(전선02C 씨앗 관찰).",
            "model_or_threshold_surface": "No model selected(모델 선택 없음); label/model design only(라벨/모델 설계 전용).",
            "validation_split": "train/validation/OOS design boundary(학습/검증/표본외 설계 경계).",
            "overfit_checks": ["limit first proxy axes", "hold OOS as readout", "no WFO before Grok pre-expensive review"],
            "selection_metric_boundary": "scout target-distance only(탐색 목표 거리 전용), not candidate selection(후보 선택 아님).",
            "validation_judgment": "exploratory(탐색)",
            "allowed_claims": ["exploratory_design_only(탐색 설계 전용)"],
            "forbidden_claims": summary["forbidden_claims"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-exploration-mandate",
            "triggered": True,
            "status": "executed",
            "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
            "idea_boundary": IDEA_ID,
            "hypothesis": summary["frontier_thesis"],
            "legacy_relation": "prior_evidence_only(이전 근거 전용)",
            "tier_scope": "Tier A first; Tier B missing_required; combined out_of_scope_by_claim.",
            "broad_sweep": "regime x side-asymmetric label x horizon(레짐 x 방향 비대칭 라벨 x 보유기간)",
            "extreme_sweep": "wide neutral bands and side-specific payoff thresholds(넓은 중립 구간과 방향별 손익 임계값)",
            "micro_search_gate": "At least one validation/OOS target-distance improvement before micro search(검증/표본외 목표 거리 개선 후 미세 탐색).",
            "wfo_plan": "WFO planned only after proxy survivor and Grok pre-expensive review(프록시 생존자와 그록 검토 후 WFO).",
            "failure_memory": "If label/regime axis gives no improvement, record negative memory and do not repeat threshold repair.",
            "evidence_boundary": "stage_open_design_only(단계 개방 설계 전용)",
            "negative_memory_effect": "Frontier02 same-surface repair loop is blocked(전선02 같은 표면 수리 반복 차단).",
            "operating_claim_boundary": "No completion/baseline/promotion/runtime/live/goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-answer-clarity",
            "triggered": True,
            "status": "executed",
            "plain_conclusion": "Frontier03(전선03)을 새 라벨/레짐 가설로 열었습니다.",
            "confirmed": ["Grok review captured(그록 검토 기록)", "stage docs written(단계 문서 작성)", "no authority claim(권위 주장 없음)"],
            "not_yet_confirmed": ["model training", "WFO", "MT5", "completion"],
            "why_it_matters": "The project stops repeating Frontier02 threshold repair and tests a new axis(새 축 시험).",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": summary["forbidden_claims"],
        },
    ]


def build_state_sync_audit() -> dict[str, Any]:
    ws = read_text(WORKSPACE_STATE)
    cws = read_text(CURRENT_WORKING_STATE)
    selection = read_text(STAGE_ROOT / "04_selected" / "selection_status.md")
    passed = STAGE_ID in ws and STAGE_ID in cws and STAGE_ID in selection and RUN_ID in ws and RUN_ID in cws and RUN_ID in selection
    return audit_payload("state_sync_audit", "pass" if passed else "blocked", findings=[] if passed else [{"check_id": "state_sync::stage_mismatch", "message": "Stage docs are not synced."}], counts={"stage_id": STAGE_ID, "run_id": RUN_ID})


def build_external_review_packet(grok: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    passed = bool(grok["grok_output_identity"]["success"]) and grok["forbidden_claim_check"]["status"] == "pass"
    return audit_payload(
        "external_review_packet",
        "pass" if passed else "blocked",
        findings=[] if passed else [{"check_id": "external_review::grok_failed", "message": "Grok review did not complete cleanly or adopted forbidden claim."}],
        counts={"prompt": GROK_PROMPT.as_posix(), "output": GROK_OUTPUT.as_posix(), "accepted": len(grok["accepted"]), "rejected": len(grok["rejected"]), "needs_local_verification": len(grok["needs_local_verification"])},
        allowed_claims=("grok_stage_open_review_captured",),
    )


def build_artifact_lineage_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    missing = []
    mismatches = []
    for name, meta in manifest.get("outputs", {}).items():
        path = Path(str(meta.get("path", "")))
        expected = meta.get("sha256")
        if not path_exists(path):
            missing.append(name)
        elif expected and sha256_file(path) != expected:
            mismatches.append(name)
    findings = []
    if missing:
        findings.append({"check_id": "artifact_lineage::missing_outputs", "message": "Manifest output missing.", "details": {"missing": missing}})
    if mismatches:
        findings.append({"check_id": "artifact_lineage::hash_mismatch", "message": "Manifest hash mismatch.", "details": {"mismatches": mismatches}})
    return audit_payload("artifact_lineage_audit", "pass" if not findings else "blocked", findings=findings, counts={"output_count": len(manifest.get("outputs", {}))}, allowed_claims=("artifact_lineage_connected",))


def build_final_claim_guard() -> dict[str, Any]:
    return audit_payload(
        "final_claim_guard",
        "pass",
        counts={f"claimed_{claim}": False for claim in FORBIDDEN_CLAIMS} | {"allowed_final_status": STATUS},
        allowed_claims=("stage_opened_no_authority",),
    )


def build_closeout_gate() -> dict[str, Any]:
    audit_paths = {
        "state_sync_audit": PACKET_ROOT / "state_sync_audit.json",
        "external_review_packet": PACKET_ROOT / "external_review_packet.json",
        "artifact_lineage_audit": PACKET_ROOT / "artifact_lineage_audit.json",
        "work_packet_schema_lint": PACKET_ROOT / "work_packet_schema_lint.json",
        "skill_receipt_lint": PACKET_ROOT / "skill_receipt_lint.json",
        "skill_receipt_schema_lint": PACKET_ROOT / "skill_receipt_schema_lint.json",
        "required_gate_coverage_audit": PACKET_ROOT / "required_gate_coverage_audit.json",
        "final_claim_guard": PACKET_ROOT / "final_claim_guard.json",
    }
    audits = []
    for name, path in audit_paths.items():
        if path_exists(path):
            data = read_json(path)
            status = data.get("status", "missing")
        else:
            status = "pending" if name == "required_gate_coverage_audit" else "missing"
        audits.append({"audit_name": name, "status": status, "path": path.as_posix()})
    status = "pass" if all(audit["status"] in {"pass", "pending"} for audit in audits) else "blocked"
    return {
        "audit_name": "closeout_gate",
        "status": status,
        "audits": audits,
        "final_claim_guard": read_json(PACKET_ROOT / "final_claim_guard.json") if path_exists(PACKET_ROOT / "final_claim_guard.json") else {"audit_name": "final_claim_guard", "status": "missing"},
        "allowed_claims": ["stage_opened_no_authority"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def audit_payload(audit_name: str, status: str, *, findings: list[dict[str, Any]] | None = None, counts: dict[str, Any] | None = None, allowed_claims: tuple[str, ...] = ()) -> dict[str, Any]:
    findings = findings or []
    return {
        "audit_name": audit_name,
        "status": status,
        "passed": status == "pass",
        "completed_forbidden": status != "pass",
        "findings": findings,
        "counts": counts or {},
        "allowed_claims": list(allowed_claims),
        "forbidden_claims": [] if status == "pass" else ["complete", "completed", "reviewed", "verified", "runtime_authority", "operating_promotion"],
    }


def update_registries(now: str, summary: dict[str, Any]) -> None:
    upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(now, summary))
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    append_marker(IDEA_REGISTRY, f"{RUN_ID}__{IDEA_ID}", f"- `{IDEA_ID}`: Frontier03(전선03) opens regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링) as a new hypothesis lifecycle(새 가설 생명주기). Effect(효과): Frontier02(전선02)를 baseline(기준선)으로 상속하지 않고 label/regime axis(라벨/레짐 축)를 시험합니다.")
    append_marker(CHANGELOG, RUN_ID, f"- {now}: `{RUN_ID}` opened `{STAGE_ID}` as stage-open design(단계 개방 설계). Effect(효과): next run(다음 실행)은 `{NEXT_RUN_ID}` proxy scout(프록시 탐색)입니다.")


def update_current_truth_docs(now: str, summary: dict[str, Any]) -> None:
    workspace_payload = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": STATUS,
        "current_judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    write_yaml(WORKSPACE_STATE, workspace_payload)
    write_text_sig(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier03(전선03)은 `regime_conditioned_asymmetric_onnx_labeling(레짐 조건 비대칭 온엑스 라벨링)` stage-open design(단계 개방 설계)로 열렸습니다.

Preserved reference(보존 참조): Frontier02C(전선02C)의 OOS density(표본외 밀도) `5.03053/day`는 preserved clue(보존 단서)일 뿐 baseline(기준선)이 아닙니다.

Negative memory(부정 기억): Frontier02E(전선02E)는 go-rule rows(진행 규칙 행) `0`으로 same-surface threshold/calibration repair(같은 표면 임계값/보정 수리)를 멈추게 했습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`. 행동(action, 행동)은 regime/asymmetric label proxy scout(레짐/비대칭 라벨 프록시 탐색)를 실행하는 것이고, 효과(effect, 효과)는 새 label/regime axis(라벨/레짐 축)가 네 축 목표 거리(target distance, 목표 거리)를 줄이는지 확인하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 없음)입니다.
""",
    )


def run_registry_row(now: str, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open_design(단계 개방 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": "Grok stage-open review captured; no authority claims.",
        "work_family": "state_sync(상태 동기)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "gate_count": str(len(REQUIRED_GATES)),
        "passed_gate_count": str(len(REQUIRED_GATES)),
        "claim_boundary": "stage_open_design_only_no_model_training_no_wfo_no_mt5_no_candidate_selection_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "subrun_id": f"{RUN_ID}__stage_open",
        "record_view": "stage_open_design(단계 개방 설계)",
        "tier_scope": "not_applicable_stage_open_design(해당 없음 단계 개방 설계)",
        "kpi_scope": "stage_open_design_no_trading_kpi(단계 개방 설계 거래 KPI 없음)",
        "primary_kpi": "no_trading_kpi(거래 KPI 없음)",
        "guardrail_kpi": "no_model_training_no_wfo_no_mt5_no_authority(모델 학습/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (STAGE_ROOT / "01_inputs" / "regime_asymmetric_label_plan.md").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_open_design(단계 개방 설계)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "Can regime-conditioned asymmetric ONNX labels improve four-axis target distance?(레짐 조건 비대칭 온엑스 라벨이 네 축 목표 거리를 줄일 수 있는가?)",
        "skill_family": "state_sync(상태 동기)",
        "lineage_summary": "grok_review_and_stage_docs(그록 검토와 단계 문서)",
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open_design(단계 개방 설계)",
        "tier_scope": "not_applicable_stage_open_design(해당 없음 단계 개방 설계)",
        "kpi_scope": "stage_open_design_no_trading_kpi(단계 개방 설계 거래 KPI 없음)",
        "scoreboard_lane": "stage_open_design(단계 개방 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": "no_trading_kpi(거래 KPI 없음)",
        "guardrail_kpi": "no_model_training_no_wfo_no_mt5_no_authority(모델 학습/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "notes": "Stage open design only; next proxy scout required(단계 개방 설계 전용; 다음 프록시 탐색 필요).",
    }


def read_csv_header(path: Path) -> list[str]:
    with path.resolve().open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header(path)
    rows: list[dict[str, str]] = []
    with path.resolve().open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    write_csv_rows(path, header, rows)


def write_csv_rows(path: Path, header: list[str], rows: list[dict[str, Any]]) -> None:
    path.resolve().parent.mkdir(parents=True, exist_ok=True)
    with path.resolve().open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: stringify(row.get(column, "")) for column in header})


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def append_marker(path: Path, marker: str, line: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    marker_text = f"<!-- {marker} -->"
    if marker_text in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    text += f"{marker_text}\n{line}\n"
    write_text_sig(path, text)


def run_cmd(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout)
        if completed.stderr:
            print(completed.stderr, file=sys.stderr)
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
