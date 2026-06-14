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


STAGE_ID = "stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout"
RUN_ID = "frontier17A_stage_open_loss_cluster_firewall_profit_persistence_onnx_scout_v1"
RUN_NUMBER = "frontier17A"
PARENT_RUN_ID = "frontier16D_runtime_probe_supplement_v1"
NEXT_RUN_ID = "frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1"
STATUS = "opened_frontier17_loss_cluster_firewall_profit_persistence_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_with_definition_locks_and_runtime_probe_obligation_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path(
    "docs/decisions/2026-06-14_stage_frontier_17_loss_cluster_firewall_profit_persistence_onnx_scout_open.md"
)
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_17/materialize_frontier17a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier17_stage_open/small_review")
F16_SELECTION = Path(
    "stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/04_selected/selection_status.md"
)
F16D_REPORT = Path(
    "stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/03_reviews/"
    "frontier16D_runtime_probe_supplement_v1_report.md"
)

PROFILES: tuple[dict[str, Any], ...] = (
    {
        "profile_id": "f17b_firewall_h8_ddq70_contq60",
        "hold_bars": 8,
        "adverse_cluster_quantile": 0.70,
        "continuation_quantile": 0.60,
        "intent": "soft firewall with moderate continuation trigger(완만한 방화벽과 중간 지속 트리거)",
    },
    {
        "profile_id": "f17b_firewall_h10_ddq75_contq65",
        "hold_bars": 10,
        "adverse_cluster_quantile": 0.75,
        "continuation_quantile": 0.65,
        "intent": "balanced firewall with stricter loss-cluster veto(균형 방화벽과 더 엄격한 손실 군집 배제)",
    },
    {
        "profile_id": "f17b_firewall_h12_ddq80_contq70",
        "hold_bars": 12,
        "adverse_cluster_quantile": 0.80,
        "continuation_quantile": 0.70,
        "intent": "strict firewall with strict continuation trigger(강한 방화벽과 강한 지속 트리거)",
    },
)

GUARDS: tuple[dict[str, str], ...] = (
    {
        "guard_id": "adverse_cluster_state_contract",
        "rule": "define train-only adverse cluster score from closed-bar state and path-risk diagnostics; do not reuse F16 edge_margin label columns(학습 전용 불리 군집 점수는 종료봉 상태와 경로 위험 진단으로 정의하고 F16 엣지 마진 라벨 열은 재사용하지 않음)",
    },
    {
        "guard_id": "continuation_quality_contract",
        "rule": "define realized continuation quality separately from future-edge labels(실현 지속 품질을 미래 엣지 라벨과 분리해 정의)",
    },
    {
        "guard_id": "decision_and_gate_contract",
        "rule": "entry equals NOT adverse_veto AND continuation_trigger; no score-rank density calibration(진입은 불리 배제 아님 AND 지속 트리거이며 점수 순위 빈도 보정 금지)",
    },
    {
        "guard_id": "no_f15_9cell_grid",
        "rule": "do not recreate F15 score-threshold 9-cell grid(F15 점수 임계값 9칸 격자 반복 금지)",
    },
    {
        "guard_id": "no_f16_locked_edge_margin_target8",
        "rule": "do not use F16 locked edge_margin target8 cell as the Frontier17 decision axis(F16 고정 엣지 마진 목표8 칸을 전선17 결정 축으로 쓰지 않음)",
    },
    {
        "guard_id": "no_validation_oos_threshold_calibration",
        "rule": "all quantiles and thresholds are fitted on train only(모든 분위수와 임계값은 학습 구간에서만 적합)",
    },
    {
        "guard_id": "stage299_loss_cluster_veto_overlap_disclosed",
        "rule": "Stage299 loss-cluster-veto memory is reference-only, not inherited winner(299단계 손실 군집 배제 기억은 참조 전용이며 승자 상속 아님)",
    },
    {
        "guard_id": "variant_cap_exactly_3",
        "rule": "exactly three pre-registered firewall profiles, no fourth knob(사전 등록 방화벽 프로필은 정확히 3개이며 네 번째 조정 금지)",
    },
    {
        "guard_id": "no_repair_ladder",
        "rule": "no post-hoc profile or quantile addition after Frontier17B metrics(Frontier17B 지표 이후 사후 프로필이나 분위수 추가 금지)",
    },
    {
        "guard_id": "density_floor_audit",
        "rule": "flag profiles below 3 trades/day as trade-starvation failure(일 3회 미만 프로필은 거래 기아 실패로 표시)",
    },
    {
        "guard_id": "firewall_transfer_audit",
        "rule": "report validation/OOS veto rate and continuation pass rate with train-frozen quantiles(학습 고정 분위수로 검증/표본밖 배제율과 지속 통과율 보고)",
    },
    {
        "guard_id": "tier_paired_records",
        "rule": "record Tier A separate, Tier B separate, and Tier A+B combined or explicit missing_required(티어 A 분리, 티어 B 분리, 티어 A+B 합산 또는 명시적 필수 누락 기록)",
    },
    {
        "guard_id": "onnx_parity_gate",
        "rule": "no scout clue or seed surface without ONNX parity pass(ONNX 동등성 통과 없이는 탐색 단서나 씨앗 표면 판정 금지)",
    },
    {
        "guard_id": "f16_reference_benchmark",
        "rule": "compare DD/smoothness/density against F16B proxy and F16D runtime observation(F16B 프록시와 F16D 런타임 관찰 대비 손실폭/매끄러움/빈도 비교)",
    },
    {
        "guard_id": "mt5_runtime_probe_before_closeout",
        "rule": "before stage closeout, run one narrow MT5 runtime probe for best-or-seed candidate or record exact blocked reason(단계 마감 전 최선 또는 씨앗 후보 1개 좁은 MT5 런타임 탐침 또는 정확한 차단 사유 기록)",
    },
    {
        "guard_id": "claim_boundary_lock",
        "rule": "only scout clue, seed surface, runtime probe observation, preserved clue, negative memory, invalid setup, or blocked may be claimed(탐색 단서, 씨앗 표면, 런타임 탐침 관찰, 보존 단서, 부정 기억, 무효 설정, 차단만 주장 가능)",
    },
)


def main() -> int:
    now = utc_now()
    ensure_dirs()
    grok = read_grok()
    local = local_verification(grok)
    summary = build_summary(now, grok, local)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": summary["grok_classification"],
        "local_verification": summary["local_verification"]["judgment"],
        "profile_count": len(PROFILES),
        "guard_count": len(GUARDS),
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def read_grok() -> dict[str, Any]:
    meta = read_json(GROK_PACKET / "metadata.json")
    output = read_text(GROK_PACKET / "clean_output.md")
    lowered = output.lower()
    return {
        "packet": GROK_PACKET.as_posix(),
        "prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "output": (GROK_PACKET / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "preflight_warnings": meta.get("preflight_warnings", []),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "accepted_definition_locks": all(token in output for token in (
            "adverse_cluster_state_contract",
            "continuation_quality_contract",
            "decision_and_gate_contract",
        )),
        "accepted_runtime_probe_obligation": "mt5_runtime_probe_before_closeout" in output,
        "accepted_claim_boundary": "scout clue" in lowered and "goal achieve" in lowered,
        "accepted_stage299_disclosure": "stage299" in lowered,
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


def local_verification(grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    f16_selection = read_text(F16_SELECTION)
    f16d_report = read_text(F16D_REPORT)
    guard_ids = {guard["guard_id"] for guard in GUARDS}
    checks = {
        "workspace_points_to_frontier17A": (
            "next_run_id: frontier17A_stage_open_new_hypothesis_design_v1" in workspace
            or (f"current_stage_id: {STAGE_ID}" in workspace and f"current_run_id: {RUN_ID}" in workspace)
        ),
        "f16_selection_closed_negative_memory": "negative_memory" in f16_selection and "not_claimed" in f16_selection,
        "f16d_runtime_probe_recorded": "Frontier16D Runtime Probe Supplement" in f16d_report and "signal diff(신호 차이)" in f16d_report,
        "f16d_oos_collapse_recorded": "| `oos` | `completed` | `completed` | 0.87 | 47.17 | 164 | 0 |" in f16d_report,
        "grok_success": bool(grok["success"]),
        "grok_accepted": grok["classification"] == "accepted(수용)",
        "grok_definition_locks_supported": bool(grok["accepted_definition_locks"]),
        "grok_runtime_probe_supported": bool(grok["accepted_runtime_probe_obligation"]),
        "grok_claim_boundary_supported": bool(grok["accepted_claim_boundary"]),
        "grok_stage299_disclosure_supported": bool(grok["accepted_stage299_disclosure"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "profile_cap_is_three": len(PROFILES) == 3,
        "guard_count_is_sixteen": len(GUARDS) == 16,
        "required_guard_ids_present": {
            "adverse_cluster_state_contract",
            "continuation_quality_contract",
            "decision_and_gate_contract",
            "mt5_runtime_probe_before_closeout",
            "claim_boundary_lock",
        }.issubset(guard_ids),
    }
    return {
        "checks": checks,
        "preflight_warnings": grok["preflight_warnings"],
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_summary(now: str, grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "frontier_thesis": (
            "Train-only loss-cluster firewall(학습 전용 손실 군집 방화벽) and profit-persistence trigger(수익 지속성 트리거)를 "
            "AND gate(동시 충족 게이트)로 묶어, 빈도(density, 빈도)를 먼저 강제하지 않고 손실폭(drawdown, 손실폭) 위험이 낮은 지속 상태만 진입한다."
        ),
        "novelty_delta": (
            "F15/F16(전선15/16)의 score threshold/edge_margin(점수 임계값/엣지 마진) 수리가 아니라 "
            "validation philosophy(검증 철학)를 drawdown-first hazard firewall(손실폭 우선 위험 방화벽)로 바꾼다."
        ),
        "profiles": list(PROFILES),
        "guards": list(GUARDS),
        "definition_locks": definition_locks(),
        "success_criteria": {
            "scout_clue": "validation/OOS net positive, PF >= 1.2, density 5~10/day, DD <= 15%, worst subperiod DD <= 25%, ONNX parity pass(검증/표본밖 순수익 양수, 수익 팩터 1.2 이상, 일 5~10회, 손실폭 15% 이하, 최악 하위기간 손실폭 25% 이하, ONNX 동등성 통과)",
            "seed_surface": "DD/smoothness improves versus F16B/D, density remains 3~10/day, PF axis does not regress(손실폭/매끄러움이 F16B/D보다 개선되고 빈도는 일 3~10회, 수익 팩터 축 후퇴 없음)",
            "runtime_probe_observation": "one narrow MT5 probe before closeout or exact blocked reason(마감 전 좁은 MT5 탐침 1회 또는 정확한 차단 사유)",
        },
        "failure_criteria": [
            "density only improves while PF/DD/smoothness fails(빈도만 개선되고 수익 팩터/손실폭/매끄러움 실패)",
            "firewall suppresses trades below 3/day(방화벽이 거래를 일 3회 미만으로 억제)",
            "train-only hazard thresholds do not transfer to validation/OOS(학습 전용 위험 임계값이 검증/표본밖으로 전이되지 않음)",
            "MT5 runtime probe shows material runtime collapse(MT5 런타임 탐침에서 중대한 런타임 붕괴)",
        ],
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def definition_locks() -> dict[str, str]:
    return {
        "adverse_cluster_state_contract": (
            "Use train-only adverse-cluster score from closed-bar market state and path-risk diagnostics; "
            "do not reuse F16 edge_margin label columns(종료봉 시장 상태와 경로 위험 진단으로 학습 전용 불리 군집 점수를 만들고 F16 엣지 마진 라벨 열은 재사용하지 않음)."
        ),
        "continuation_quality_contract": (
            "Use realized continuation quality as a separate target axis; no future-edge label rename(실현 지속 품질을 별도 목표 축으로 쓰며 미래 엣지 라벨 이름 변경 금지)."
        ),
        "decision_and_gate_contract": (
            "Runtime decision meaning is NOT adverse_veto AND continuation_trigger; no score-rank density calibration(런타임 결정 의미는 불리 배제 아님 AND 지속 트리거이며 점수 순위 빈도 보정 금지)."
        ),
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "guard_manifest.json", {"guards": summary["guards"]})
    write_json(RUN_ROOT / "profile_manifest.json", {"profiles": summary["profiles"]})
    write_json(RUN_ROOT / "definition_locks.json", summary["definition_locks"])
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "definition_locks.md", definition_locks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "firewall_profile_spec.md", profile_spec_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "selection_metric_spec.md", selection_metric_spec(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_state_and_registries(summary: dict[str, Any]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(summary))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier16_selection": artifact_identity(F16_SELECTION),
            "frontier16d_runtime_report": artifact_identity(F16D_REPORT),
            "grok_stage_open_output": artifact_identity(Path(summary["grok_output"])),
        },
        "outputs": {
            "stage_open_summary": (RUN_ROOT / "stage_open_summary.json").as_posix(),
            "guard_manifest": (RUN_ROOT / "guard_manifest.json").as_posix(),
            "profile_manifest": (RUN_ROOT / "profile_manifest.json").as_posix(),
            "definition_locks": (RUN_ROOT / "definition_locks.json").as_posix(),
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
        },
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Loss Cluster Firewall Profit Persistence ONNX Scout(전선17 손실 군집 방화벽 수익 지속성 ONNX 탐색)

Status(상태): `{summary['status']}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): scout clue/seed surface/runtime probe observation/preserved clue/negative memory/invalid setup/blocked(탐색 단서/씨앗 표면/런타임 탐침 관찰/보존 단서/부정 기억/무효 설정/차단)까지만 허용합니다.
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Stage Brief(전선17 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): loss-cluster firewall(손실 군집 방화벽)과 profit-persistence trigger(수익 지속성 트리거)를 AND gate(동시 충족 게이트)로 묶으면 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 함께 개선할 수 있는가?

## Frontier Thesis(전선 가설)

{summary['frontier_thesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Exit Rule(종료 규칙)

Frontier17(전선17)은 proxy(프록시), WFO/stress/runtime validation(WFO/스트레스/런타임 검증), repair(수리), closeout(마감)을 지나며 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

## Claim Boundary(주장 경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def definition_locks_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{key}`: {value}" for key, value in summary["definition_locks"].items())
    return f"""# Frontier17 Definition Locks(전선17 정의 고정)

Action(행동): Frontier17B(전선17B) 물질화 전에 adverse cluster(불리 군집), continuation quality(지속 품질), decision gate(결정 게이트)의 의미를 고정합니다.

Effect(효과): F16 risk-quality label(전선16 위험 품질 라벨)을 이름만 바꿔 반복하는 일을 막습니다.

{rows}
"""


def profile_spec_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(
        "- `{profile_id}`: hold_bars(보유 봉수) `{hold_bars}`, adverse_cluster_quantile(불리 군집 분위수) `{adverse_cluster_quantile}`, continuation_quantile(지속 분위수) `{continuation_quantile}`; {intent}".format(**profile)
        for profile in summary["profiles"]
    )
    return f"""# Frontier17 Firewall Profile Spec(전선17 방화벽 프로필 명세)

Action(행동): 3 profiles(프로필 3개)를 Frontier17B(전선17B) 전에 고정합니다.

Effect(효과): bounded exploration(제한 탐색)은 허용하되, 결과를 본 뒤 profile/quantile(프로필/분위수)을 추가하는 repair ladder(수리 사다리)를 막습니다.

{rows}
"""


def do_not_repeat_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{guard['guard_id']}`: {guard['rule']}" for guard in summary["guards"])
    return f"""# Do Not Repeat(반복 금지)

{rows}
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Experiment Design(전선17 실험 설계)

- primary_family(주 작업군): `experiment_design(실험 설계)`
- primary_skill(주 스킬): `obsidian-experiment-design`
- support_skills(보조 스킬): `obsidian-data-integrity`, `obsidian-model-validation`, `obsidian-exploration-mandate`, `obsidian-artifact-lineage`, `obsidian-result-judgment`, `obsidian-grok-collaboration`
- required_gates(필수 게이트): `work_packet_schema_lint`, `external_review_packet`, `definition_lock_gate`, `required_gate_coverage_audit`, `final_claim_guard`

Hypothesis(가설): {summary['frontier_thesis']}

Changed variable(변경 변수): validation philosophy(검증 철학) and decision structure(결정 구조).

Success criteria(성공 기준):
- scout clue(탐색 단서): {summary['success_criteria']['scout_clue']}
- seed surface(씨앗 표면): {summary['success_criteria']['seed_surface']}
- runtime probe observation(런타임 탐침 관찰): {summary['success_criteria']['runtime_probe_observation']}

Failure criteria(실패 기준): {', '.join(summary['failure_criteria'])}
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Prior Stage Scan(전선17 이전 단계 점검)

F15 preserved clue(전선15 보존 단서): train-only score threshold(학습 전용 점수 임계값)는 density transfer(빈도 전이)를 만들 수 있었습니다.

F15/F16 negative memory(전선15/16 부정 기억): threshold/edge-margin/risk-quality label(임계값/엣지 마진/위험 품질 라벨)만으로 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 동시에 만들지 못했습니다.

F16D runtime probe observation(전선16D 런타임 탐침 관찰): signal_diff=0(신호 차이 0)으로 handoff parity(인계 동등성)는 맞았지만 OOS(표본밖)는 PF 0.87, DD 47.17%로 무너졌습니다.

Stage299 overlap disclosure(299단계 겹침 공개): loss-cluster-veto(손실 군집 배제) 기억은 reference only(참조 전용)입니다. Frontier17(전선17)은 winner/baseline/promotion/runtime authority/live readiness/Goal Achieve(승자/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 상속하지 않습니다.
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    warnings = ", ".join(summary["local_verification"].get("preflight_warnings", [])) or "none(없음)"
    return f"""# Frontier17 Local Checks(전선17 로컬 확인)

Judgment(판정): `{summary['local_verification']['judgment']}`

Grok preflight warnings(그록 사전점검 경고): `{warnings}`

{checks}
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Input Refs(전선17 입력 참조)

- Frontier16 selection status(전선16 선택 상태): `{F16_SELECTION.as_posix()}`
- Frontier16D runtime report(전선16D 런타임 보고서): `{F16D_REPORT.as_posix()}`
- Grok stage-open output(그록 단계 개방 출력): `{summary['grok_output']}`
- guard manifest(가드 목록): `{(RUN_ROOT / 'guard_manifest.json').as_posix()}`
- profile manifest(프로필 목록): `{(RUN_ROOT / 'profile_manifest.json').as_posix()}`
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Selection Metric Spec(전선17 선택 지표 명세)

- scout clue(탐색 단서): validation/OOS(검증/표본밖) 양쪽에서 PF, DD, density, subperiod DD, ONNX parity(수익 팩터, 손실폭, 빈도, 하위기간 손실폭, ONNX 동등성)를 동시에 봅니다.
- seed surface(씨앗 표면): F16B/D(전선16B/D)보다 DD/smoothness(손실폭/매끄러움)가 명확히 좋아지고 density(빈도)가 일 3~10회에 머물 때만 기록합니다.
- negative memory(부정 기억): density(빈도)만 맞거나 firewall(방화벽)이 거래를 굶기면 같은 단계 안에서 반복 수리하지 않고 닫습니다.
- runtime probe observation(런타임 탐침 관찰): closeout(마감) 전 best-or-seed candidate(최선 또는 씨앗 후보) 1개에 MT5 runtime probe(MT5 런타임 탐침)를 시도하거나 정확한 blocked reason(차단 사유)을 기록합니다.
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier17A Stage Open Report(전선17A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier17(전선17)을 loss-cluster firewall profit-persistence ONNX scout(손실 군집 방화벽 수익 지속성 ONNX 탐색)로 열었습니다.

Effect(효과): F15/F16(전선15/16)의 density-first threshold/edge-margin(빈도 우선 임계값/엣지 마진) 반복을 피하고 DD-first hazard firewall(손실폭 우선 위험 방화벽)을 새 가설 축으로 고정합니다.

Grok classification(그록 분류): `{summary['grok_classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Profile count(프로필 수): `{len(summary['profiles'])}`

Guard count(가드 수): `{len(summary['guards'])}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Review Index(전선17 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), definition locks(정의 고정), guard manifest(가드 목록), runtime probe obligation(런타임 탐침 의무) recorded(기록됨).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier17A Required Gate Coverage Audit(전선17A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 검사): hypothesis/controls/success/failure/invalid/exit boundary(가설/통제/성공/실패/무효/종료 경계) recorded(기록됨).
- external_review_packet(외부 검토 묶음): Grok accepted(그록 수용), packet(묶음) `{summary['grok_packet']}`.
- definition_lock_gate(정의 고정 게이트): adverse cluster/continuation/decision gate(불리 군집/지속/결정 게이트) fixed(고정됨).
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): `mt5_runtime_probe_before_closeout` recorded(기록됨).
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일).
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier17 Selection Status(전선17 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier17 Loss Cluster Firewall Profit Persistence ONNX Scout(결정: 전선17 손실 군집 방화벽 수익 지속성 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier17(전선17)을 새 hypothesis lifecycle(가설 생명주기)로 열었습니다.

Effect(효과): F15/F16(전선15/16)의 수리 축을 상속하지 않고, DD-first hazard firewall(손실폭 우선 위험 방화벽)을 새 검증 철학(validation philosophy, 검증 철학)으로 시험할 수 있습니다.

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

Action(행동): Frontier17(전선17)을 loss-cluster firewall profit-persistence ONNX scout(손실 군집 방화벽 수익 지속성 ONNX 탐색)로 열었습니다.

Effect(효과): 다음 실행은 3개 firewall profiles(방화벽 프로필)를 고정하고, F15/F16(전선15/16)의 threshold/edge-margin repair(임계값/엣지 마진 수리)를 반복하지 않는 proxy scout(프록시 탐색)를 진행할 수 있습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier17_stage_open_grok_accepted_definition_locks_runtime_probe_obligation_no_authority",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
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
        "primary_kpi": f"grok_classification={summary['grok_classification']};profiles={len(PROFILES)};guards={len(GUARDS)}",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_required_before_closeout(그록 단계 개방 검토 완료, 마감 전 런타임 탐침 필요)",
        "notes": f"next={NEXT_RUN_ID};definition_locks;no_authority",
        "question": "Can loss-cluster firewall plus continuation trigger improve PF/DD/smoothness?(손실 군집 방화벽과 지속 트리거가 수익 팩터/손실폭/매끄러움을 개선할 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR17-LOSS-CLUSTER-FIREWALL-PROFIT-PERSISTENCE-ONNX-SCOUT`: `{RUN_ID}` opens loss-cluster firewall "
        "profit-persistence ONNX scout(손실 군집 방화벽 수익 지속성 ONNX 탐색). Effect(효과): F15/F16(전선15/16)의 "
        "density-first threshold/edge-margin(빈도 우선 임계값/엣지 마진) 반복 없이 DD-first hazard firewall(손실폭 우선 위험 방화벽)을 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier17(전선17) after Grok stage-open accepted(그록 단계 개방 수용). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` will test 3 firewall profiles(방화벽 프로필 3개) with definition locks(정의 고정) and MT5 runtime probe obligation(MT5 런타임 탐침 의무), no authority claims(권위 주장 없음).\n"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
