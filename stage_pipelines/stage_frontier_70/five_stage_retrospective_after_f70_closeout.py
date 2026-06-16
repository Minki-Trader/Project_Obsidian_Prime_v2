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


RUN_ID = "five_stage_retrospective_after_f70_closeout_v1"
PACKET_ID = "frontier66_to_70_five_stage_retrospective_v1"
STAGE_ID = "five_stage_retrospective_frontier66_to_70"
PARENT_RUN_ID = "frontier70F_stage_closeout_regime_specific_asymmetric_value_exit_model_rotation_v1"
NEXT_RUN_ID = "frontier71A_stage_open_economics_native_label_selection_hypothesis_design_v1"
STATUS = "completed_five_stage_retrospective_no_authority"
JUDGMENT = "direction_delta_and_repair_priority_delta_only_no_authority"
CLAIM_BOUNDARY = (
    "retrospective_direction_delta_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_frontier66_to_70_five_stage_retrospective"
PROMPT = PACKET_ROOT / "prompts/frontier66_to_70_five_stage_retrospective_prompt.md"
CLEAN_OUTPUT = PACKET_ROOT / "outputs/clean_output.md"
METADATA = PACKET_ROOT / "outputs/metadata.json"
RAW_DIAGNOSTICS = PACKET_ROOT / "outputs/raw_diagnostics.json"

BOUNDED_EVIDENCE = PACKET_ROOT / "bounded_evidence_table.csv"
ADVICE_CLASSIFICATION = PACKET_ROOT / "advice_classification.json"
RETROSPECTIVE_REPORT = PACKET_ROOT / "retrospective_report.md"
RECEIPT = PACKET_ROOT / "receipt.md"
LOCAL_VERIFICATION = PACKET_ROOT / "local_verification.md"
NEXT_OPEN_BLOCK_CHECK = PACKET_ROOT / "next_stage_open_block_check.md"
RUN_MANIFEST = PACKET_ROOT / "run_manifest.json"

RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


STAGE_ROWS: list[dict[str, Any]] = [
    {
        "stage_id": "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "hypothesis": "runtime_probe_backfill_gap_audit(런타임 탐침 보강과 간극 감사)",
        "proxy_kpi": "net_sum=2793.80;best_pf=2.18;trades_total=24284;target_density_rows=0/64",
        "mt5_runtime_probe_kpi": "max_dd=60.81;dd_gt10_rows=60/64;pf_ge2_rows=1/64",
        "proxy_runtime_gap_cause": "signal_count_parity_not_runtime_economics(신호 수 동등성이 런타임 경제성이 아님)",
        "closeout_label": "closed_preserved_clue_signal_parity_negative_memory_runtime_economics_gap_no_authority",
        "preserved_clue": "signal_parity_diagnostic_layer(신호 동등성 진단 계층)",
        "negative_memory": "dd_inflation_repeats_across_backfill(보강 전반 손실폭 팽창 반복)",
        "systemic_repeat": "parity_not_economics(동등성은 경제성이 아님)",
        "next_action": "frontier67_dd_basis_crosswalk(F67 손실폭 기준 대조)",
        "report_path": "stages/stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk",
        "hypothesis": "count_parity_not_pnl_parity_crosswalk(거래 수 동등성과 손익 동등성 대조)",
        "proxy_kpi": "crosswalk_probe_with_count_alignment(거래 수 정렬 대조 탐침)",
        "mt5_runtime_probe_kpi": "net=2.31;pf=1.00;dd=30.58;trades_day=1.3282;signal_diff=0;feature_diff=0;swap=-14.24",
        "proxy_runtime_gap_cause": "order_deal_swap_dd_basis_after_parity(동등성 뒤 주문/체결/스왑/손실폭 기준)",
        "closeout_label": "preserved_clue_negative_memory_no_authority",
        "preserved_clue": "bridge_metrics_necessary_not_sufficient(연결 지표는 필요하지만 충분하지 않음)",
        "negative_memory": "runtime_economics_can_erase_proxy_meaning(런타임 경제성이 프록시 의미를 지움)",
        "systemic_repeat": "count_aligned_runtime_not_edge(거래 수 정렬은 우위가 아님)",
        "next_action": "frontier68_lifecycle_economics_proxy_design(F68 생명주기 경제성 프록시 설계)",
        "report_path": "stages/stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout",
        "hypothesis": "runtime_native_lifecycle_economics_proxy(런타임 네이티브 생명주기 경제성 프록시)",
        "proxy_kpi": "best_f68j_oos_net=68.24;pf=1.04;dd=13.76;trades_day=6.6923;validation_pf=0.94;validation_dd=38.55",
        "mt5_runtime_probe_kpi": "signal_diff=0;feature_diff=0;signature_collapse=false(서명 붕괴 없음)",
        "proxy_runtime_gap_cause": "unit_corrected_atr_avoids_signature_collapse_but_not_pf_dd(단위 보정 ATR은 서명 붕괴만 피함)",
        "closeout_label": "preserved_clue_negative_memory_no_authority",
        "preserved_clue": "unit_corrected_atr_telemetry_and_exact_parity(단위 보정 ATR 기록과 정확 동등성)",
        "negative_memory": "risk_envelope_alone_not_edge(위험 봉투만으로는 우위가 아님)",
        "systemic_repeat": "risk_only_repair_not_economics(위험 전용 수리는 경제성이 아님)",
        "next_action": "frontier69_axis_rotation(F69 축 전환)",
        "report_path": "stages/stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory",
        "hypothesis": "event_first_first_hit_opportunity(이벤트 우선 최초 도달 기회)",
        "proxy_kpi": "sparse_oos_pf=2.94;sparse_oos_tpd=0.0359;dense_oos_pf=1.19;dense_oos_tpd=1.3385;final_like=0;joint_soft=0",
        "mt5_runtime_probe_kpi": "exact_probability_signal_feature_parity_and_runtime_veto_tape(정확 확률/신호/피처 동등성과 런타임 차단 테이프)",
        "proxy_runtime_gap_cause": "sparse_pf_collapses_when_density_lifted(밀도 상승 때 희소 수익 팩터 붕괴)",
        "closeout_label": "preserved_clue_negative_memory_no_authority",
        "preserved_clue": "onnx_probability_signal_feature_parity_and_veto_tape(온엑스/확률/신호/피처 동등성과 차단 테이프)",
        "negative_memory": "threshold_cooldown_daily_quota_repair_failed(임계값/쿨다운/일 할당 수리 실패)",
        "systemic_repeat": "density_lift_destroys_sparse_pf(밀도 상승이 희소 수익 팩터를 깨뜨림)",
        "next_action": "frontier70_label_model_regime_rotation(F70 라벨/모델/장세 전환)",
        "report_path": "stages/stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation",
        "hypothesis": "regime_specific_asymmetric_value_exit_model_rotation(장세별 비대칭 가치/청산 모델 전환)",
        "proxy_kpi": "f70b_candidates=420;f70c_candidates=936;meaningful=0;final_like=0;reference_proxy_oos_pf=1.5657;reference_proxy_oos_tpd=0.8907",
        "mt5_runtime_probe_kpi": "f70e_reference_oos_net=68.00;pf=1.29;dd=5.61;tpd=0.8923;small_nn_oos_pf=1.02;small_nn_oos_dd=10.56;signal_feature_diff=0",
        "proxy_runtime_gap_cause": "selected_entry_tape_repaired_lifecycle_gap_remaining_economics_gap(선택 진입 테이프가 생명주기 간극 수리, 경제성 간극 남음)",
        "closeout_label": "preserved_clue_negative_memory_no_authority",
        "preserved_clue": "selected_entry_tape_aligns_runtime_trade_count(선택 진입 테이프가 런타임 거래 수를 맞춤)",
        "negative_memory": "same_label_model_surface_does_not_create_density_or_pf(같은 라벨/모델 표면은 밀도나 수익 팩터를 만들지 못함)",
        "systemic_repeat": "same_surface_tape_repair_not_edge(같은 표면 테이프 수리는 우위가 아님)",
        "next_action": "five_stage_retrospective_before_next_frontier_open(다음 전선 개방 전 5단계 중간 검토)",
        "report_path": "stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/03_reviews/stage_closeout_report.md",
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


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        return
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{key: json_ready(row.get(key, "")) for key in fieldnames} for row in rows])


def read_csv_header(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or [])


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def classify_advice(clean_text: str) -> dict[str, Any]:
    accepted = "advice_classification** | **accepted**" in clean_text or "Classification:** **accepted" in clean_text
    return {
        "advice_classification": "accepted(수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "direction_delta": "economics_native_model_label_selection(경제성 네이티브 모델/라벨/선택)",
        "repair_priority_delta": "proxy_economics_joint_gate_first_runtime_probe_second(프록시 경제성 공동 게이트 우선, 런타임 탐침은 이후)",
        "accepted": [
            "parity_not_economics_negative_memory(동등성은 경제성이 아님 부정 기억)",
            "selected_entry_tape_preserved_clue_only(선택 진입 테이프는 보존 단서일 뿐)",
            "economics_first_next_frontier_direction(경제성 우선 다음 전선 방향)",
            "deprioritize_same_surface_tape_threshold_risk_loops(같은 표면 테이프/임계값/위험 반복 낮춤)",
        ]
        if accepted
        else [],
        "rejected": ["none(없음)"] if accepted else ["unverified_stage_open(검증 없는 단계 개방)"],
        "needs_local_verification": [
            "kpi_rows_and_hashes(핵심 성과 지표 행과 해시)",
            "register_reset_after_packet(묶음 뒤 등록부 재설정)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Frontier66-F70 Five-Stage Retrospective(전선66-F70 5단계 중간 검토)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Packet ID(묶음 ID): `{PACKET_ID}`",
        f"Status(상태): `{STATUS}`",
        f"Judgment(판정): `{JUDGMENT}`",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Bounded Evidence Table(제한 근거표)",
        "",
        "| stage id(단계 ID) | hypothesis(가설) | proxy KPI(프록시 KPI) | MT5 runtime probe KPI(MT5 런타임 탐침 KPI) | gap cause(간극 원인) | closeout label(마감 라벨) | preserved clue(보존 단서) | negative memory(부정 기억) | systemic repeat(시스템성 반복) | next action(다음 행동) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in STAGE_ROWS:
        lines.append(
            f"| `{row['stage_id']}` | `{row['hypothesis']}` | `{row['proxy_kpi']}` | `{row['mt5_runtime_probe_kpi']}` | `{row['proxy_runtime_gap_cause']}` | `{row['closeout_label']}` | `{row['preserved_clue']}` | `{row['negative_memory']}` | `{row['systemic_repeat']}` | `{row['next_action']}` |"
        )
    lines.extend(
        [
            "",
            "## Grok Synthesis(그록 종합)",
            "",
            f"- advice_classification(조언 분류): `{summary['classification']['advice_classification']}`.",
            f"- direction_delta(방향 변화): `{summary['classification']['direction_delta']}`.",
            f"- repair_priority_delta(수리 우선순위 변화): `{summary['classification']['repair_priority_delta']}`.",
            "",
            "## Codex Local Verification(Codex 로컬 검증)",
            "",
            "- closeout reports(마감 보고서): F66-F70 paths(경로) exist(존재) checked from local filesystem(로컬 파일시스템).",
            "- Grok output(그록 출력): wrapper(래퍼) success(성공), timeout false(시간 제한 없음), prompt/output hashes(프롬프트/출력 해시) recorded(기록).",
            "- register reset(등록부 재설정): this packet(묶음) updates `docs/registers/five_stage_retrospective_register.yaml` to not_due(아직 아님) for the next frontier open(다음 전선 개방).",
            "",
            "## Direction Delta(방향 변화)",
            "",
            "- Next frontier(다음 전선)는 economics-native model/label/selection(경제성 네이티브 모델/라벨/선택)을 주제로 시작한다.",
            "- Bridge parity(연결 동등성)는 preserved diagnostic tooling(보존 진단 도구)로 낮추고 primary discovery(주 탐색)는 economic edge(경제 우위)에 둔다.",
            "- Any positive proxy(긍정 프록시)는 sparse-vs-dense fracture test(희소/밀집 균열 시험)를 먼저 통과해야 한다.",
            "",
            "## Repair Priority Delta(수리 우선순위 변화)",
            "",
            "- Prioritize(우선): meaningful-candidate funnel(의미 후보 깔때기), joint density/PF/DD proxy gate(밀도/PF/DD 공동 프록시 게이트), economics-native labels(경제성 네이티브 라벨).",
            "- Deprioritize(낮춤): same-surface tape/threshold/cooldown/risk-only loops(같은 표면 테이프/임계값/쿨다운/위험 전용 반복).",
            "- Runtime probe(런타임 탐침)는 새 frontier(새 전선)에서도 필수지만, 목적은 parity 재증명이 아니라 economics transfer(경제성 이전) 확인이다.",
            "",
            "## Do Not Repeat(반복 금지)",
            "",
            "- Do not treat count parity(거래 수 동등성), signal parity(신호 동등성), or selected-entry tape alignment(선택 진입 테이프 정렬) as edge proof(우위 증명).",
            "- Do not promote sparse PF(희소 수익 팩터) without density-lift survival(밀도 상승 생존).",
            "- Do not open F71 as more F70 variants(F70 변형 추가) on the same label/model surface(같은 라벨/모델 표면).",
            "",
            "## Next Stage Open Block Check(다음 단계 개방 차단 점검)",
            "",
            "- before packet(묶음 전): `due_after_f70_closeout(도래, F70 마감 뒤)`.",
            "- after packet(묶음 뒤): `not_due_after_retrospective_completed(중간 검토 완료 후 아직 아님)`.",
            f"- next_run(다음 실행): `{NEXT_RUN_ID}`.",
        ]
    )
    return lines


def receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# Frontier66-F70 Retrospective Receipt(전선66-F70 중간 검토 영수증)",
        "",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- created_at_utc(생성 시각): `{utc_now()}`",
        "- trigger_reason(트리거 이유): F70 closeout made five frontier closeouts since last retrospective(F70 마감으로 이전 중간 검토 뒤 5개 전선 마감 도달).",
        f"- bounded_evidence_table(제한 근거표): `{rel(BOUNDED_EVIDENCE)}`.",
        f"- prompt_identity(프롬프트 정체성): `{rel(PROMPT)}`, sha256 `{summary['prompt_hash']}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(CLEAN_OUTPUT)}`, sha256 `{summary['clean_output_hash']}`.",
        f"- advice_classification(조언 분류): `{summary['classification']['advice_classification']}`.",
        f"- accepted(수용): `{'; '.join(summary['classification']['accepted'])}`.",
        f"- rejected(거절): `{'; '.join(summary['classification']['rejected'])}`.",
        f"- needs_local_verification(로컬 검증 필요): `{'; '.join(summary['classification']['needs_local_verification'])}`.",
        f"- final_codex_direction(최종 Codex 방향): `{summary['classification']['direction_delta']}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def local_verification_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Local Verification(로컬 검증)",
        "",
        f"- created_at_utc(생성 시각): `{utc_now()}`",
        f"- prompt_hash(프롬프트 해시): `{summary['prompt_hash']}`",
        f"- clean_output_hash(정리 출력 해시): `{summary['clean_output_hash']}`",
        f"- metadata_path(메타데이터 경로): `{rel(METADATA)}`",
        f"- raw_diagnostics_path(원본 진단 경로): `{rel(RAW_DIAGNOSTICS)}`",
        "",
        "| artifact(산출물) | status(상태) | effect(효과) |",
        "|---|---|---|",
    ]
    for row in STAGE_ROWS:
        path = ROOT / row["report_path"]
        status = "exists(존재)" if path_exists(path) else "missing(누락)"
        lines.append(f"| `{row['report_path']}` | `{status}` | closeout evidence identity(마감 근거 정체성) |")
    lines.extend(
        [
            f"| `{rel(RETROSPECTIVE_REGISTER)}` | `updated(갱신)` | next frontier open block cleared after packet(묶음 뒤 다음 전선 개방 차단 해제) |",
            f"| `{rel(BOUNDED_EVIDENCE)}` | `written(기록)` | bounded evidence table durable(제한 근거표 지속화) |",
        ]
    )
    return lines


def next_open_block_lines() -> list[str]:
    return [
        "# Next Stage Open Block Check(다음 단계 개방 차단 점검)",
        "",
        f"- checked_at_utc(점검 시각): `{utc_now()}`",
        "- before(이전): `due_after_f70_closeout(도래, F70 마감 뒤)`.",
        "- action(행동): ran Frontier66-F70 five-stage retrospective(전선66-F70 5단계 중간 검토 실행).",
        "- effect(효과): next frontier open(다음 전선 개방) gate(게이트)를 `not_due_after_retrospective_completed(중간 검토 완료 후 아직 아님)`로 되돌린다.",
        f"- next_run(다음 실행): `{NEXT_RUN_ID}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def update_register() -> None:
    lines = [
        "version: five_stage_retrospective_register_v1",
        "source_of_truth: docs/registers/five_stage_retrospective_register.yaml",
        'purpose: "Track five-stage Grok retrospective(5단계 Grok 중간 검토) cadence without relying on Codex memory(코덱스 기억)."',
        "adopted_at_utc: '2026-06-16T12:05:00Z'",
        "adopted_during_stage_id: stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "cadence:",
        '  primary_trigger: "closing_frontier_number % 5 == 0"',
        '  fallback_trigger: "len(closed_frontier_ids_since_last_retrospective) >= 5"',
        "  next_open_block: true",
        '  scope_rule: "Use latest five canonical frontier closeout stage ids with closeout receipts, not numeric NN-4..NN alone."',
        "required_outputs:",
        "  - five_stage_retrospective_packet",
        "  - bounded_evidence_table",
        "  - grok_receipt",
        "  - codex_local_verification",
        "  - advice_classification",
        "  - compact_retrospective_report",
        "  - next_stage_open_block_check",
        "required_row_fields:",
        "  - stage_id",
        "  - hypothesis",
        "  - proxy_kpi",
        "  - mt5_runtime_probe_kpi",
        "  - proxy_runtime_gap_cause",
        "  - closeout_label",
        "  - preserved_clue",
        "  - negative_memory",
        "  - systemic_repeat",
        "  - next_action",
        "claim_boundary:",
        "  allowed:",
        "    - direction_delta",
        "    - repair_priority_delta",
        "  forbidden:",
        "    - completion",
        "    - baseline",
        "    - promotion",
        "    - runtime_authority",
        "    - live_readiness",
        "    - goal_achieve",
        "",
        "state:",
        f"  last_completed_packet_id: {PACKET_ID}",
        "  last_completed_at_frontier: 70",
        "  last_completed_stage_ids:",
    ]
    lines.extend(f"    - {row['stage_id']}" for row in STAGE_ROWS)
    lines.extend(
        [
            f"  last_completed_at_utc: '{utc_now()}'",
            "  closed_frontier_ids_since_last_retrospective: []",
            "  closeouts_since_last: 0",
            "  next_numeric_trigger_frontier: 75",
            "  current_due_status: not_due_after_retrospective_completed",
            '  note: "F66-F70 retrospective(중간 검토)가 완료되어 다음 frontier open(전선 개방) 차단은 해제됐다. 다음 numeric trigger(숫자 트리거)는 F75 closeout(마감)이다."',
        ]
    )
    io_path(RETROSPECTIVE_REGISTER).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def ledger_row() -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "five_stage_retrospective(5단계 중간 검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RETROSPECTIVE_REPORT),
        "notes": "F66-F70 retrospective closed with direction_delta and repair_priority_delta only.",
        "family": "five_stage_retrospective(5단계 중간 검토)",
        "primary_report": rel(RETROSPECTIVE_REPORT),
        "run_number": "retrospective_f66_f70",
        "date": "2026-06-17",
        "decision": "clear_next_frontier_open_block_after_retrospective",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(STAGE_ROWS),
        "gate_passes": 7,
        "gate_total": 7,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RETROSPECTIVE_REPORT),
        "run_date": "2026-06-17",
        "primary_artifact": rel(RUN_MANIFEST),
        "result_status": STATUS,
        "view": "five_stage_retrospective(5단계 중간 검토)",
        "tier": "not_applicable_cross_stage_retrospective(단계 간 중간 검토라 해당 없음)",
        "metric_scope": "cross_stage_synthesis(단계 간 종합)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "retrospective(중간 검토)",
        "external_verification_status": "grok_review_completed_local_verification_recorded(그록 검토 완료, 로컬 검증 기록)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(RETROSPECTIVE_REPORT),
        "gate_audit_path": rel(NEXT_OPEN_BLOCK_CHECK),
        "created_at": utc_now(),
        "ledger_row_id": f"{RUN_ID}__retrospective",
        "subrun_id": "retrospective(중간 검토)",
        "record_view": "retrospective(중간 검토)",
        "tier_scope": "not_applicable_cross_stage_retrospective",
        "kpi_scope": "f66_f70_closeout_synthesis(F66-F70 마감 종합)",
        "primary_kpi": "direction_delta=economics_native_model_label_selection;repair_priority_delta=proxy_economics_joint_gate_first",
        "guardrail_kpi": "no completion/baseline/promotion/runtime authority/live readiness/goal achieve",
        "work_family": "five_stage_retrospective(5단계 중간 검토)",
        "row_id": f"{RUN_ID}__retrospective",
        "evidence_boundary": "direction_delta_only_no_authority(방향 변화만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "What should F66-F70 change in the next frontier direction?(F66-F70은 다음 전선 방향을 어떻게 바꿔야 하나?)",
        "artifact_count": 7,
        "created_at_utc": utc_now(),
        "required_gate_audit": rel(NEXT_OPEN_BLOCK_CHECK),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "five_stage_retrospective(5단계 중간 검토)",
        "run_type": "retrospective(중간 검토)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(RETROSPECTIVE_REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "bounded_grok_review_and_local_verification(제한 그록 검토와 로컬 검증)",
    }


def update_ledgers() -> None:
    row = ledger_row()
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)


def write_state_files() -> None:
    state_lines = [
        "current_stage_id: stage_frontier_71__economics_native_label_selection_pending_open",
        "active_stage: stage_frontier_71__economics_native_label_selection_pending_open",
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
        '  - "Action(행동): F66-F70 five-stage retrospective(5단계 중간 검토)를 닫았다."',
        '  - "Effect(효과): 다음 전선은 economics-native label/selection(경제성 네이티브 라벨/선택) 방향으로 열 수 있지만, 아직 새 stage open(단계 개방)은 실행하지 않았다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")

    current_lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "Active stage(활성 단계): `stage_frontier_71__economics_native_label_selection_pending_open`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): Frontier66-F70 five-stage retrospective(전선66-F70 5단계 중간 검토)를 완료했다.",
        "",
        "Effect(효과): bridge parity(연결 동등성)는 보존 진단 도구로 낮추고, 다음 전선의 주 과제는 economics-native label/selection(경제성 네이티브 라벨/선택)으로 잡는다.",
        "",
        "- direction_delta(방향 변화): `economics_native_model_label_selection(경제성 네이티브 모델/라벨/선택)`.",
        "- repair_priority_delta(수리 우선순위 변화): `proxy_economics_joint_gate_first_runtime_probe_second(프록시 경제성 공동 게이트 우선, 런타임 탐침은 이후)`.",
        "- five-stage retrospective(5단계 중간 검토): `not_due_after_retrospective_completed(중간 검토 완료 후 아직 아님)`.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- retrospective report(중간 검토 보고서): `{rel(RETROSPECTIVE_REPORT)}`",
        f"- receipt(영수증): `{rel(RECEIPT)}`",
        f"- local verification(로컬 검증): `{rel(LOCAL_VERIFICATION)}`",
        f"- next open block check(다음 개방 차단 점검): `{rel(NEXT_OPEN_BLOCK_CHECK)}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(CURRENT_WORKING_STATE, current_lines)


def main() -> int:
    required = [PROMPT, CLEAN_OUTPUT, METADATA]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing retrospective evidence: {missing}")
    clean_text = io_path(CLEAN_OUTPUT).read_text(encoding="utf-8-sig")
    classification = classify_advice(clean_text)
    summary = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "covered_stage_ids": [row["stage_id"] for row in STAGE_ROWS],
        "prompt": rel(PROMPT),
        "clean_output": rel(CLEAN_OUTPUT),
        "metadata": rel(METADATA),
        "prompt_hash": file_hash(PROMPT),
        "clean_output_hash": file_hash(CLEAN_OUTPUT),
        "classification": classification,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": utc_now(),
    }
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
        "inputs": {
            "prompt": rel(PROMPT),
            "clean_output": rel(CLEAN_OUTPUT),
            "metadata": rel(METADATA),
            "raw_diagnostics": rel(RAW_DIAGNOSTICS),
        },
        "outputs": {
            "bounded_evidence": rel(BOUNDED_EVIDENCE),
            "advice_classification": rel(ADVICE_CLASSIFICATION),
            "retrospective_report": rel(RETROSPECTIVE_REPORT),
            "receipt": rel(RECEIPT),
            "local_verification": rel(LOCAL_VERIFICATION),
            "next_stage_open_block_check": rel(NEXT_OPEN_BLOCK_CHECK),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(BOUNDED_EVIDENCE, STAGE_ROWS)
    write_json(ADVICE_CLASSIFICATION, classification)
    write_json(RUN_MANIFEST, manifest)
    write_md(RETROSPECTIVE_REPORT, report_lines(summary))
    write_md(RECEIPT, receipt_lines(summary))
    write_md(LOCAL_VERIFICATION, local_verification_lines(summary))
    write_md(NEXT_OPEN_BLOCK_CHECK, next_open_block_lines())
    update_register()
    update_ledgers()
    write_state_files()
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "covered_stage_count": len(STAGE_ROWS),
                    "next_run_id": NEXT_RUN_ID,
                    "retrospective_due_status": "not_due_after_retrospective_completed",
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
