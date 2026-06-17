from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd"
RUN_ID = "frontier71A_stage_open_economics_native_label_selection_hypothesis_design_v1"
PARENT_RUN_ID = "five_stage_retrospective_after_f70_closeout_v1"
NEXT_RUN_ID = "frontier71B_economics_native_proxy_scout_v1"
STATUS = "stage_open_plan_only_local_anchors_completed_no_authority"
JUDGMENT = "economics_native_pivot_needs_proxy_execution_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_plan_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SPEC_ROOT = STAGE_ROOT / "00_spec"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f71_stage_open_economics_native_label_selection"
GROK_PROMPT = GROK_PACKET / "prompts/f71_stage_open_economics_native_label_selection_prompt.md"
GROK_CLEAN = GROK_PACKET / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET / "outputs/metadata.json"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
F70_CLOSEOUT = ROOT / "stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/03_reviews/stage_closeout_report.md"
F70_NEGATIVE = ROOT / "docs/registers/negative_result_register.md"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
STAGE_BRIEF = SPEC_ROOT / "stage_brief.md"
OPEN_REPORT = REVIEWS_ROOT / "frontier71A_stage_open_economics_native_label_selection_report.md"
LOCAL_VERIFICATION = REVIEWS_ROOT / "f71a_local_verification.json"
JOINT_GATE_CONTRACT = REVIEWS_ROOT / "f71a_joint_gate_contract.csv"
LABEL_SPEC = REVIEWS_ROOT / "f71a_label_economics_spec.json"
ANTI_REPEAT_DENYLIST = REVIEWS_ROOT / "f71a_anti_repeat_denylist.csv"
PHASE_PLAN = REVIEWS_ROOT / "f71a_phase_plan.csv"
GROK_RECEIPT = REVIEWS_ROOT / "grok_stage_open_receipt.md"
GATE_AUDIT = REVIEWS_ROOT / "required_gate_coverage_audit_f71a.md"
STAGE_LEDGER = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


JOINT_GATE_ROWS = [
    {
        "gate_name": "scout_clue(탐색 단서)",
        "validation_requirement": "net_profit>0;profit_factor>=1.10;drawdown<=15;trades_day>=1.0",
        "oos_requirement": "net_profit>0;profit_factor>=1.10;drawdown<=15;trades_day>=1.0",
        "effect": "keeps weak but directional economics for repair(약하지만 방향 있는 경제성을 수리 대상으로 보존)",
    },
    {
        "gate_name": "meaningful_candidate(의미 후보)",
        "validation_requirement": "profit_factor>=1.20;drawdown<=10;trades_day>=3.0",
        "oos_requirement": "profit_factor>=1.20;drawdown<=10;trades_day>=3.0",
        "effect": "allows MT5 Runtime Probe after proxy signal(프록시 신호 뒤 MT5 런타임 탐침 허용)",
    },
    {
        "gate_name": "density_lift_fracture_test(밀도 상승 균열 시험)",
        "validation_requirement": "candidate remains PF>=1.10 and DD<=12 when selected density is lifted by threshold relaxation or bucket expansion",
        "oos_requirement": "candidate remains PF>=1.10 and DD<=12 when selected density is lifted by threshold relaxation or bucket expansion",
        "effect": "blocks sparse-PF false wins(희소 수익 팩터 허위 승리 차단)",
    },
    {
        "gate_name": "final_like_reference_only(최종 유사 참조 전용)",
        "validation_requirement": "profit_factor>=2.0;drawdown<=10;5<=trades_day<=10;smooth_equity_proxy=true",
        "oos_requirement": "profit_factor>=2.0;drawdown<=10;5<=trades_day<=10;smooth_equity_proxy=true",
        "effect": "reference only until final completion review(최종 완성 검토 전까지 참조 전용)",
    },
]

ANTI_REPEAT_ROWS = [
    {
        "deny_item": "f70_same_macro_regime_surface(F70 같은 거시/장세 표면)",
        "reject_if": "lead axis is regime filter or macro feature rank without new economics label",
        "effect": "prevents same-surface drift(같은 표면 표류 방지)",
    },
    {
        "deny_item": "post_hoc_tape_threshold_cooldown_quota(사후 테이프/임계값/쿨다운/할당)",
        "reject_if": "repair only changes throttling after old label scores",
        "effect": "forces change in what is selected(무엇을 선택하는지 변경 강제)",
    },
    {
        "deny_item": "sparse_pf_without_density_lift(밀도 상승 없는 희소 수익 팩터)",
        "reject_if": "PF looks high but trades/day is below meaningful gate and fracture test is absent",
        "effect": "blocks F69-style false clue(전선69식 허위 단서 차단)",
    },
    {
        "deny_item": "runtime_probe_as_discovery(탐색용 런타임 탐침)",
        "reject_if": "MT5 is used before proxy has scout_clue or meaningful_candidate evidence",
        "effect": "keeps runtime probe as transfer check(런타임 탐침을 이전 확인으로 유지)",
    },
    {
        "deny_item": "model_bakeoff_without_label_shift(라벨 변화 없는 모델 대결)",
        "reject_if": "model family changes but target and selection objective are old",
        "effect": "prevents feature/model churn(피처/모델 소모전 방지)",
    },
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        return
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: json_ready(row.get(field, "")) for field in fieldnames} for row in rows])


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def classify_grok(clean: str) -> dict[str, Any]:
    return {
        "classification": "needs_local_verification(로컬 검증 필요)" if "needs_local_verification" in clean else "accepted(수용)",
        "accepted": [
            "pivot_accepted_in_principle(전환 원칙상 수용)",
            "lead_pair_label_target_then_selection_objective(주도 쌍은 라벨/목표 다음 선택 목표)",
            "reject_same_surface_throttle_repeat(같은 표면 제한 반복 거절)",
        ],
        "needs_local_verification": [
            "joint_density_pf_dd_gate(밀도/수익 팩터/손실폭 공동 게이트)",
            "label_economics_spec(라벨 경제성 명세)",
            "anti_f70_denylist(F70 반복 금지 목록)",
            "retrospective_register_not_due(중간 검토 등록부 아직 아님)",
        ],
        "rejected": ["execution_open_without_local_anchors(로컬 고정점 없는 실행 개방)"],
    }


def label_spec() -> dict[str, Any]:
    return {
        "label_family": "economics_native_lifecycle_outcome(경제성 네이티브 생명주기 결과)",
        "lead_axis": "label_target_then_selection_objective(라벨/목표 다음 선택 목표)",
        "candidate_horizons_bars": [6, 12, 18, 24],
        "economic_components": [
            "realized_pnl_after_cost_slippage_swap(비용/슬리피지/스왑 뒤 실현 손익)",
            "mfe_mae_balance(최대 유리/불리 움직임 균형)",
            "adverse_path_stress(불리 경로 압박)",
            "hold_time_penalty(보유 시간 페널티)",
            "drawdown_contribution(손실폭 기여)",
        ],
        "selection_score_candidates": [
            "expected_net_contribution(예상 순수익 기여)",
            "pf_contribution_bucket(수익 팩터 기여 구간)",
            "dd_penalty_adjusted_edge(손실폭 페널티 보정 우위)",
            "density_band_utility(밀도 구간 효용)",
        ],
        "tier_recording": ["Tier A separate(티어 A 분리)", "Tier B separate(티어 B 분리)", "Tier A+B combined(티어 A+B 합산)"],
        "forbidden": [
            "old_direction_or_first_hit_label_without_economics(경제성 없는 기존 방향/최초 도달 라벨)",
            "post_hoc_quota_as_economics(사후 할당을 경제성으로 부르기)",
        ],
    }


def local_verification(clean: str) -> dict[str, Any]:
    retrospective_text = io_path(RETROSPECTIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(RETROSPECTIVE_REGISTER) else ""
    f70_text = io_path(F70_CLOSEOUT).read_text(encoding="utf-8-sig") if path_exists(F70_CLOSEOUT) else ""
    return {
        "grok_classification": classify_grok(clean),
        "retrospective_register_not_due": "current_due_status: not_due_after_retrospective_completed" in retrospective_text,
        "f70_closeout_exists": path_exists(F70_CLOSEOUT),
        "f70_negative_memory_mentions_same_surface": "same_label_model_surface" in f70_text or "같은 F70 라벨/모델 축" in f70_text,
        "negative_result_register_exists": path_exists(F70_NEGATIVE),
        "joint_gate_rows": len(JOINT_GATE_ROWS),
        "anti_repeat_rows": len(ANTI_REPEAT_ROWS),
        "label_spec_version": "economics_native_lifecycle_outcome_v1",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def phase_plan_rows() -> list[dict[str, str]]:
    return [
        {"phase": "F71A", "action": "stage_open_local_anchor(단계 개방 로컬 고정)", "effect": "materialize joint gate and label economics spec(공동 게이트와 라벨 경제성 명세 물질화)", "next": "F71B"},
        {"phase": "F71B", "action": "economics_native_proxy_scout(경제성 네이티브 프록시 탐색)", "effect": "search broad label/feature/model/trade/risk surface(넓은 라벨/피처/모델/거래/위험 표면 탐색)", "next": "F71C_or_F71D"},
        {"phase": "F71C", "action": "repair_recombine_if_signal(신호가 있으면 수리/재조합)", "effect": "change what is selected, not only throttling(제한만이 아니라 선택 대상을 변경)", "next": "F71D"},
        {"phase": "F71D", "action": "mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침)", "effect": "check economics transfer after proxy signal(프록시 신호 뒤 경제성 이전 확인)", "next": "F71E"},
        {"phase": "F71E", "action": "gap_analysis_repair_closeout(간극 분석/수리/마감)", "effect": "record preserved clue or negative memory honestly(보존 단서 또는 부정 기억 정직 기록)", "next": "closeout"},
    ]


def report_lines(payload: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Frontier71A Stage Open(F71A 단계 개방)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Stage ID(단계 ID): `{STAGE_ID}`",
        f"Run ID(실행 ID): `{RUN_ID}`",
        f"Status(상태): `{STATUS}`",
        f"Judgment(판정): `{JUDGMENT}`",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis(가설)",
        "",
        "An economics-native label/selection objective(경제성 네이티브 라벨/선택 목표), trained to select entries that survive a joint density/PF/DD gate(밀도/수익 팩터/손실폭 공동 게이트), may produce more meaningful candidates(의미 후보) than F68-F70 bridge/risk/tape repairs(연결/위험/테이프 수리).",
        "",
        "Effect(효과): F71 changes what is selected(무엇을 선택하는지) rather than only how entries are throttled(진입을 어떻게 제한하는지).",
        "",
        "## Local Verification(로컬 검증)",
        "",
        f"- retrospective register(중간 검토 등록부) not due(아직 아님): `{payload['local_verification']['retrospective_register_not_due']}`.",
        f"- F70 closeout(마감) exists(존재): `{payload['local_verification']['f70_closeout_exists']}`.",
        f"- joint gate rows(공동 게이트 행): `{payload['local_verification']['joint_gate_rows']}`.",
        f"- anti-repeat denylist rows(반복 금지 행): `{payload['local_verification']['anti_repeat_rows']}`.",
        "",
        "## Grok Review(그록 검토)",
        "",
        f"- classification(분류): `{payload['grok']['classification']['classification']}`.",
        f"- prompt(프롬프트): `{rel(GROK_PROMPT)}`, sha256 `{file_hash(GROK_PROMPT)}`.",
        f"- output(출력): `{rel(GROK_CLEAN)}`, sha256 `{file_hash(GROK_CLEAN)}`.",
        "- Codex action(Codex 행동): accepted pivot in principle(원칙상 전환 수용), and materialized local anchors(로컬 고정점 물질화).",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`.",
        "",
        "Effect(효과): F71B can run proxy scout(프록시 탐색) only against this joint gate(공동 게이트), label spec(라벨 명세), and denylist(거부 목록).",
    ]
    return lines


def receipt_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F71 Stage Open Grok Receipt(F71 단계 개방 그록 영수증)",
        "",
        f"- created_at_utc(생성): `{utc_now()}`",
        "- trigger_reason(트리거 이유): F71 stage open(단계 개방) after F66-F70 retrospective(중간 검토).",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{file_hash(GROK_PROMPT)}`.",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{file_hash(GROK_CLEAN)}`.",
        f"- classification(분류): `{payload['grok']['classification']['classification']}`.",
        f"- accepted(수용): `{'; '.join(payload['grok']['classification']['accepted'])}`.",
        f"- rejected(거절): `{'; '.join(payload['grok']['classification']['rejected'])}`.",
        f"- needs_local_verification(로컬 검증 필요): `{'; '.join(payload['grok']['classification']['needs_local_verification'])}`.",
        f"- final_codex_direction(최종 Codex 방향): `{NEXT_RUN_ID}` with local anchors(로컬 고정점 포함).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def gate_audit_lines() -> list[str]:
    return [
        "# Required Gate Coverage Audit F71A(필수 게이트 커버리지 감사 F71A)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| retrospective due check(중간 검토 도래 점검) | passed(통과) | `{rel(RETROSPECTIVE_REGISTER)}` | F71 개방 차단 없음 |",
        f"| Grok stage open review(그록 단계 개방 검토) | passed_with_local_verification(로컬 검증 포함 통과) | `{rel(GROK_RECEIPT)}` | F71 전환 과장 방지 |",
        f"| joint gate contract(공동 게이트 계약) | passed(통과) | `{rel(JOINT_GATE_CONTRACT)}` | economics-native proxy(경제성 네이티브 프록시) 측정 가능 |",
        f"| label economics spec(라벨 경제성 명세) | passed(통과) | `{rel(LABEL_SPEC)}` | 기존 라벨 재사용 방지 |",
        f"| anti-repeat denylist(반복 금지 목록) | passed(통과) | `{rel(ANTI_REPEAT_DENYLIST)}` | F70 같은 표면 반복 차단 |",
        f"| claim boundary(주장 경계) | passed(통과) | `{CLAIM_BOUNDARY}` | 금지 주장 없음 |",
    ]


def stage_brief_lines() -> list[str]:
    return [
        "# Frontier71 Brief(F71 개요)",
        "",
        f"Stage ID(단계 ID): `{STAGE_ID}`",
        "",
        "Core question(핵심 질문): Can economics-native labels and selection objectives(경제성 네이티브 라벨과 선택 목표) create meaningful candidates(의미 후보) under joint density/PF/DD constraints(밀도/수익 팩터/손실폭 공동 조건)?",
        "",
        "Boundary(경계): exploration only(탐색만), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
    ]


def ledger_row() -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(OPEN_REPORT),
        "notes": "F71 opened as plan-only economics-native label/selection pivot with local anchors.",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(OPEN_REPORT),
        "run_number": "frontier71A",
        "date": "2026-06-17",
        "decision": "open_f71_economics_native_label_selection",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(OPEN_REPORT),
        "run_date": "2026-06-17",
        "primary_artifact": rel(RUN_MANIFEST),
        "result_status": STATUS,
        "attempt_count": 0,
        "view": "stage_open(단계 개방)",
        "tier": "not_applicable_stage_open(단계 개방 해당 없음)",
        "metric_scope": "plan_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_open(단계 개방)",
        "external_verification_status": "grok_review_completed_local_anchors_materialized(그록 검토 완료, 로컬 고정점 물질화)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(OPEN_REPORT),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": utc_now(),
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "subrun_id": "stage_open(단계 개방)",
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open",
        "kpi_scope": "plan_only_no_trading_kpi(계획 전용)",
        "primary_kpi": "joint_gate_rows=4;anti_repeat_rows=5;label_spec=economics_native_lifecycle_outcome_v1",
        "guardrail_kpi": "no F70 same-surface repeat; runtime probe remains mandatory later",
        "work_family": "experiment_design(실험 설계)",
        "row_id": f"{RUN_ID}__stage_open",
        "evidence_boundary": "plan_only_no_authority(계획 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can economics-native label/selection create meaningful candidates?(경제성 네이티브 라벨/선택이 의미 후보를 만들 수 있나?)",
        "artifact_count": 8,
        "created_at_utc": utc_now(),
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "stage_open(단계 개방)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(OPEN_REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "F66-F70 retrospective and F71 Grok stage-open review(F66-F70 중간 검토와 F71 그록 단계 개방 검토)",
    }


def update_ledgers() -> None:
    row = ledger_row()
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def append_idea() -> None:
    marker = "<!-- frontier71A_stage_open_economics_native_label_selection -->"
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else ""
    if marker in text:
        return
    block = f"""
{marker}
- `{RUN_ID}` opens Frontier71(전선71) as economics-native label/selection exploration(경제성 네이티브 라벨/선택 탐색). Effect(효과): F66-F70 bridge parity clues(연결 동등성 단서)를 보조 도구로 낮추고, what-to-select(무엇을 선택할지)를 joint density/PF/DD gate(밀도/수익 팩터/손실폭 공동 게이트)로 다시 정의한다. Evidence(근거): `{rel(OPEN_REPORT)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    io_path(IDEA_REGISTRY).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def write_state_files() -> None:
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_retrospective_completed",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "Action(행동): F71A stage open(단계 개방)을 economics-native label/selection(경제성 네이티브 라벨/선택)으로 물질화했다."',
        '  - "Effect(효과): F71B proxy scout(프록시 탐색)는 공동 게이트, 라벨 경제성 명세, F70 반복 금지 목록을 기준으로 실행된다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")
    lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F71A stage open(단계 개방)을 완료했다.",
        "",
        "Effect(효과): 다음 실행은 economics-native proxy scout(경제성 네이티브 프록시 탐색)이고, F70 반복 금지 목록과 joint gate(공동 게이트)가 로컬 근거로 고정됐다.",
        "",
        f"- stage(단계): `{STAGE_ID}`.",
        "- lead axis(주도 축): `label/target -> selection objective(라벨/목표 -> 선택 목표)`.",
        f"- next action(다음 행동): `{NEXT_RUN_ID}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(CURRENT_WORKING_STATE, lines)


def main() -> int:
    required = [GROK_PROMPT, GROK_CLEAN, GROK_METADATA, RETROSPECTIVE_REGISTER, F70_CLOSEOUT]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing F71A evidence: {missing}")
    clean = io_path(GROK_CLEAN).read_text(encoding="utf-8-sig")
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "grok": {"classification": classify_grok(clean), "prompt_hash": file_hash(GROK_PROMPT), "clean_hash": file_hash(GROK_CLEAN)},
        "local_verification": local_verification(clean),
        "label_spec": label_spec(),
        "joint_gate_rows": JOINT_GATE_ROWS,
        "anti_repeat_rows": ANTI_REPEAT_ROWS,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": utc_now(),
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "inputs": {"grok_prompt": rel(GROK_PROMPT), "grok_clean": rel(GROK_CLEAN), "retrospective_register": rel(RETROSPECTIVE_REGISTER), "f70_closeout": rel(F70_CLOSEOUT)},
        "outputs": {"open_report": rel(OPEN_REPORT), "joint_gate_contract": rel(JOINT_GATE_CONTRACT), "label_spec": rel(LABEL_SPEC), "anti_repeat_denylist": rel(ANTI_REPEAT_DENYLIST)},
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(LOCAL_VERIFICATION, payload["local_verification"])
    write_json(LABEL_SPEC, payload["label_spec"])
    write_csv(JOINT_GATE_CONTRACT, JOINT_GATE_ROWS)
    write_csv(ANTI_REPEAT_DENYLIST, ANTI_REPEAT_ROWS)
    write_csv(PHASE_PLAN, phase_plan_rows())
    write_md(STAGE_BRIEF, stage_brief_lines())
    write_md(OPEN_REPORT, report_lines(payload))
    write_md(GROK_RECEIPT, receipt_lines(payload))
    write_md(GATE_AUDIT, gate_audit_lines())
    update_ledgers()
    append_idea()
    write_state_files()
    print(json.dumps(json_ready({"status": STATUS, "judgment": JUDGMENT, "next_run_id": NEXT_RUN_ID}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
