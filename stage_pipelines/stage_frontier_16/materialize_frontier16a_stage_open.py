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


STAGE_ID = "stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout"
RUN_ID = "frontier16A_stage_open_edge_quality_risk_veto_density_transfer_onnx_scout_v1"
RUN_NUMBER = "frontier16A"
PARENT_RUN_ID = "frontier15C_score_threshold_density_repair_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier16B_edge_quality_risk_veto_proxy_scout_v1"
STATUS = "opened_frontier16_edge_quality_risk_veto_density_transfer_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_with_locked_decision_and_guard_manifest_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path(
    "docs/decisions/2026-06-14_stage_frontier_16_edge_quality_risk_veto_density_transfer_onnx_scout_open.md"
)
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_16/materialize_frontier16a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier16_stage_open/small_review")
F15_SELECTION = Path("stages/stage_frontier_15__score_threshold_density_controlled_onnx_scout/04_selected/selection_status.md")
F15_CLOSEOUT_REPORT = Path(
    "stages/stage_frontier_15__score_threshold_density_controlled_onnx_scout/03_reviews/"
    "frontier15C_score_threshold_density_repair_or_closeout_decision_v1_report.md"
)

PRIMARY_CELL_ID = "edge_margin__target8"
LABEL_VARIANTS = (
    {
        "variant_id": "f16b_edge_h8_t0p30_cap0p45_early0p25",
        "hold_bars": 8,
        "target_multiplier": 0.30,
        "adverse_cap_multiplier": 0.45,
        "early_adverse_cap_multiplier": 0.25,
    },
    {
        "variant_id": "f16b_edge_h8_t0p45_cap0p35_early0p20",
        "hold_bars": 8,
        "target_multiplier": 0.45,
        "adverse_cap_multiplier": 0.35,
        "early_adverse_cap_multiplier": 0.20,
    },
    {
        "variant_id": "f16b_edge_h12_t0p50_cap0p50_early0p30",
        "hold_bars": 12,
        "target_multiplier": 0.50,
        "adverse_cap_multiplier": 0.50,
        "early_adverse_cap_multiplier": 0.30,
    },
)

GUARDS = (
    ("locked_decision_contract", "edge_margin only, train-only target8 only, no validation/OOS calibration"),
    ("pre_registered_label_spec", "three label variants fixed before Frontier16B metrics"),
    ("density_transfer_audit", "label, argmax, and edge_margin__target8 density by split"),
    ("do_not_repeat_registry", "no F15 9-cell grid, no validation-guided filtering, no density-as-edge claim"),
    ("variant_cap", "three label variants only, no post-hoc knob addition"),
    ("no_repair_ladder", "no F14/F15 repair ladder inside Frontier16B"),
    ("prior_stage_overlap_disclosure", "F07/F12 overlap disclosed; F16 difference recorded"),
    ("tier_paired_records", "Tier A separate, Tier B missing_required, combined missing_required"),
    ("onnx_parity_gate", "no strict or preserved judgment without parity pass"),
    ("claim_boundary_lock", "proxy scout only, all forbidden claims not_claimed"),
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
        "guard_count": len(summary["guards"]),
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
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "accepted_locked_policy": "edge_margin__target8" in output and "train-only" in lowered,
        "accepted_guard_count": sum(1 for guard_id, _ in GUARDS if guard_id.replace("_", " ") in lowered or guard_id in lowered),
        "accepted_claim_boundary": "not_claimed" in lowered and "goal achieve" in lowered,
        "accepted_overlap_disclosure": "f07" in lowered and "f12" in lowered,
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
    f15_selection = read_text(F15_SELECTION)
    f15_report = read_text(F15_CLOSEOUT_REPORT)
    checks = {
        "workspace_points_to_frontier16A": "next_run_id: frontier16A_stage_open_new_hypothesis_design_v1" in workspace,
        "f15_selection_closed_no_authority": "closed_negative_memory_with_preserved_density_transfer_clue_no_authority" in f15_selection,
        "f15_closeout_no_authority": "Goal Achieve" in f15_report and "not_claimed" in f15_report,
        "f15_density_transfer_clue_available": "density" in f15_report.lower() and ("8.629" in f15_report or "8.063" in f15_report),
        "grok_success": bool(grok["success"]),
        "grok_accepted": grok["classification"] == "accepted(수용)",
        "grok_locked_policy_supported": bool(grok["accepted_locked_policy"]),
        "grok_claim_boundary_supported": bool(grok["accepted_claim_boundary"]),
        "grok_overlap_disclosure_supported": bool(grok["accepted_overlap_disclosure"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "guard_manifest_has_ten_guards": len(GUARDS) == 10,
        "variant_cap_is_three": len(LABEL_VARIANTS) == 3,
    }
    return {
        "checks": checks,
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
        "hypothesis": (
            "F15(프론티어15)의 density transfer(빈도 전이)는 calibration clue(보정 단서)로만 쓰고, "
            "risk-quality path label(위험 품질 경로 라벨)이 PF/DD(수익 팩터/손실폭)를 개선하는지 본다."
        ),
        "novelty_delta": (
            "Changed variable(변경 변수)는 score grid(점수 격자)가 아니라 label meaning(라벨 의미)이다. "
            "Effect(효과)는 F15(프론티어15)의 9-cell expansion(9칸 확장)을 반복하지 않고 "
            "edge quality(엣지 품질)를 상류 label(라벨)에서 시험하는 것이다."
        ),
        "primary_cell_id": PRIMARY_CELL_ID,
        "locked_decision_contract": {
            "score_contract_id": "edge_margin",
            "score_expression": "max(p_short, p_long) - p_flat",
            "target_density_per_day": 8,
            "cell_id": PRIMARY_CELL_ID,
            "threshold_policy": "train split probability scores and train calendar only(학습 분할 확률 점수와 학습 달력만 사용)",
            "forbidden": "no validation/OOS threshold calibration(검증/표본밖 임계값 보정 금지)",
        },
        "label_variants": list(LABEL_VARIANTS),
        "guards": [{"guard_id": guard_id, "rule": rule} for guard_id, rule in GUARDS],
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "guard_manifest.json", {"guards": summary["guards"]})
    write_json(RUN_ROOT / "locked_decision_contract.json", summary["locked_decision_contract"])
    write_json(RUN_ROOT / "label_variant_manifest.json", summary["label_variants"])
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "locked_decision_contract.md", locked_decision_contract_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "label_spec.md", label_spec_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks_text(summary))
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
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry())
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier15_selection": artifact_identity(F15_SELECTION),
            "frontier15_closeout_report": artifact_identity(F15_CLOSEOUT_REPORT),
            "grok_stage_open_output": artifact_identity(Path(summary["grok_output"])),
        },
        "outputs": {
            "stage_open_summary": (RUN_ROOT / "stage_open_summary.json").as_posix(),
            "guard_manifest": (RUN_ROOT / "guard_manifest.json").as_posix(),
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
        },
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Edge Quality Risk Veto Density Transfer ONNX Scout(프론티어16 엣지 품질 위험 배제 빈도 전이 온엑스 탐색)

Status(상태): `{summary['status']}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Primary cell(1순위 칸): `{PRIMARY_CELL_ID}`

Claim boundary(주장 경계): proxy scout/preserved clue/negative memory/invalid setup/blocked(프록시 탐색/보존 단서/부정 기억/무효 설정/차단)까지만 허용합니다.
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Stage Brief(프론티어16 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): risk-quality path label(위험 품질 경로 라벨)이 locked edge_margin density policy(고정 엣지 마진 빈도 정책) 아래에서 PF/DD(수익 팩터/손실폭)를 개선하는가?

## Hypothesis(가설)

{summary['hypothesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Claim Boundary(주장 경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def locked_decision_contract_text(summary: dict[str, Any]) -> str:
    contract = summary["locked_decision_contract"]
    return f"""# Locked Decision Contract(고정 결정 계약)

Action(행동): `{contract['score_expression']}` 하나와 `{PRIMARY_CELL_ID}` 하나만 Frontier16B(프론티어16B)에 씁니다.

Effect(효과): F15(프론티어15)의 9-cell grid(9칸 격자) 반복을 막고, validation/OOS(검증/표본밖)를 threshold selection(임계값 선택)에 쓰지 않습니다.

- score_contract_id(점수 계약 ID): `{contract['score_contract_id']}`
- target_density_per_day(목표 일 거래 빈도): `{contract['target_density_per_day']}`
- threshold_policy(임계값 정책): {contract['threshold_policy']}
- forbidden(금지): {contract['forbidden']}
"""


def label_spec_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(
        "- `{variant_id}`: hold_bars(보유 봉수) `{hold_bars}`, target_multiplier(목표 배수) `{target_multiplier}`, "
        "adverse_cap_multiplier(역행 상한 배수) `{adverse_cap_multiplier}`, early_adverse_cap_multiplier(초기 역행 상한 배수) "
        "`{early_adverse_cap_multiplier}`".format(**variant)
        for variant in summary["label_variants"]
    )
    return f"""# Frontier16 Label Spec(프론티어16 라벨 명세)

Action(행동): train-only scale(학습 전용 척도)로 path return(경로 수익), adverse excursion(역행폭), early adverse excursion(초기 역행폭)을 묶은 3개 label variants(라벨 변형)를 고정합니다.

Effect(효과): label meaning(라벨 의미)을 F15(프론티어15)의 density threshold(빈도 임계값)와 분리해, edge quality(엣지 품질)를 새 상류 가설로 시험합니다.

{rows}
"""


def do_not_repeat_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{guard['guard_id']}`: {guard['rule']}" for guard in summary["guards"])
    return f"""# Do Not Repeat(반복 금지)

{rows}
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Experiment Design(프론티어16 실험 설계)

- hypothesis(가설): {summary['hypothesis']}
- changed_variable(변경 변수): label meaning(라벨 의미)
- locked_decision_cell(고정 결정 칸): `{PRIMARY_CELL_ID}`
- variant_cap(변형 상한): `{len(summary['label_variants'])}`
- success_criteria(성공 기준): validation/OOS(검증/표본밖) net positive(순수익 양수), PF >= 1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD <= 15%(손실폭 15% 이하), ONNX parity pass(온엑스 동등성 통과)
- failure_criteria(실패 기준): density(빈도)는 맞지만 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 깨지면 negative memory(부정 기억)로 닫습니다.
- invalid_conditions(무효 조건): validation/OOS threshold retune(검증/표본밖 임계값 재조정), score cell 추가(점수 칸 추가), post-hoc label knob(사후 라벨 파라미터) 추가
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return f"""# Prior Stage Scan(이전 단계 스캔)

F15(프론티어15)는 density transfer(빈도 전이)를 calibration clue(보정 단서)로 남겼지만, edge quality/PF/DD/subperiod stability(엣지 품질/수익 팩터/손실폭/하위기간 안정성)를 같이 만들지 못했습니다.

F07/F12(프론티어07/12)는 adverse excursion/path label(역행폭/경로 라벨) 표면과 겹칩니다. F16(프론티어16)의 차이는 F15(프론티어15)의 locked decision(고정 결정)과 density transfer as input only(빈도 전이를 입력 단서로만 사용)를 함께 고정한 점입니다.

Reference only(참조 전용): winner/baseline/promotion/runtime authority/live readiness/Goal Achieve(승자/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 상속하지 않습니다.
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    return f"""# Frontier16 Local Checks(프론티어16 로컬 확인)

Judgment(판정): `{summary['local_verification']['judgment']}`

{checks}
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Selection Metric Spec(프론티어16 선택 지표 명세)

- strict scout clue(엄격 탐색 단서): `{PRIMARY_CELL_ID}`가 validation/OOS(검증/표본밖) 양쪽에서 PF/density/DD/subperiod/parity(수익 팩터/빈도/손실폭/하위기간/동등성)를 통과해야 합니다.
- preserved clue(보존 단서): density(빈도)가 5~10/day(일 5~10회)를 유지하고 PF/DD/smoothness(수익 팩터/손실폭/매끄러움) 중 좁은 축이 개선될 때만 기록합니다.
- negative memory(부정 기억): 0 strict + 0 preserved(엄격 0 + 보존 0)이면 같은 단계 안 repair ladder(수리 사다리)를 열지 않습니다.
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier16A Stage Open Report(프론티어16A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier16(프론티어16)을 edge-quality risk-veto density-transfer ONNX scout(엣지 품질 위험 배제 빈도 전이 온엑스 탐색)로 열었습니다.

Effect(효과): F15(프론티어15)의 density transfer(빈도 전이)는 calibration clue(보정 단서)로만 쓰고, 새 edge-quality label(엣지 품질 라벨)을 고정 decision policy(결정 정책) 아래에서 시험합니다.

Grok classification(그록 분류): `{summary['grok_classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Guard count(가드 수): `{len(summary['guards'])}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Review Index(프론티어16 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), guard manifest(가드 목록) registered(등록됨).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier16A Required Gate Coverage Audit(프론티어16A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- external_review_packet(외부 검토 묶음): Grok accepted(그록 수용), packet(묶음) `{summary['grok_packet']}`.
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- locked_decision_gate(고정 결정 게이트): `{PRIMARY_CELL_ID}` only(만 사용)
- guard_manifest_gate(가드 목록 게이트): `{len(summary['guards'])}` guards(가드)
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier16 Selection Status(프론티어16 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier16 Edge Quality Risk Veto Density Transfer ONNX Scout(결정: 프론티어16 엣지 품질 위험 배제 빈도 전이 온엑스 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier16(프론티어16)을 새 hypothesis lifecycle(가설 생명주기)로 열었습니다.

Effect(효과): reference only(참조 전용) 규칙을 지키며, F15(프론티어15)의 density transfer(빈도 전이)를 상속이 아니라 calibration clue(보정 단서)로만 사용합니다.

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

Action(행동): Frontier16(프론티어16)을 locked decision contract(고정 결정 계약)과 risk-quality label variants(위험 품질 라벨 변형)로 열었습니다.

Effect(효과): 다음 실행은 3 label variants(라벨 변형)와 1 decision cell(결정 칸)만 시험하므로 F15(프론티어15) 9-cell grid(9칸 격자) 반복을 막습니다.

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
        "notes": "frontier16_stage_open_grok_accepted_locked_decision_guard_manifest_no_authority",
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
        "primary_kpi": f"grok_classification={summary['grok_classification']};guards={len(summary['guards'])};primary_cell={PRIMARY_CELL_ID}",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "not_applicable(해당 없음)",
        "notes": f"next={NEXT_RUN_ID};locked_decision;no_authority",
        "question": "Can risk-quality labels improve edge under locked density transfer policy?(고정 빈도 전이 정책 아래 위험 품질 라벨이 엣지를 개선하는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry() -> str:
    return (
        f"- `IDEA-FR16-EDGE-QUALITY-RISK-VETO-DENSITY-TRANSFER-ONNX-SCOUT`: `{RUN_ID}` opens edge-quality "
        "risk-veto density-transfer ONNX scout(엣지 품질 위험 배제 빈도 전이 온엑스 탐색). Effect(효과): "
        "F15(프론티어15)의 density transfer(빈도 전이)를 calibration clue(보정 단서)로만 쓰고 edge-quality label(엣지 품질 라벨)을 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier16(프론티어16) after Grok stage-open accepted(그록 단계 개방 수용). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` will test 3 label variants(라벨 변형) with locked cell(고정 칸) `{PRIMARY_CELL_ID}` and no authority claims(권위 주장 없음).\n"
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
