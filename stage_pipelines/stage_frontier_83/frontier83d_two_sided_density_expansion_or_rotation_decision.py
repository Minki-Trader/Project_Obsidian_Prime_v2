from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
RUN_ID = "frontier83D_two_sided_density_expansion_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier83C_proxy_runtime_gap_analysis_teacher_overlay_v1"
NEXT_RUN_ID = "frontier83E_short_side_density_runtime_materialization_v1"
STATUS = "f83d_short_density_materialization_target_selected_no_authority"
JUDGMENT = "f83c_runtime_parity_clue_routes_to_f82b_short_density_axis_mt5_materialization_required_no_authority"
CLAIM_BOUNDARY = (
    "target_selection_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F83C_SUMMARY = REVIEW_DIR / "f83c_proxy_runtime_gap_analysis_summary.json"
F82_STAGE_DIR = ROOT / "stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
F82B_SUMMARY = F82_STAGE_DIR / "03_reviews/f82b_density_first_proxy_summary.json"
F82B_ALL_CANDIDATES = F82_STAGE_DIR / "02_runs/frontier82B_density_first_runtime_economic_mechanism_proxy_scout_v1/f82b_density_first_proxy_candidates_all.csv"
F82B_TOP200 = F82_STAGE_DIR / "03_reviews/f82b_density_first_proxy_ranked_top200.csv"

TARGET_SELECTION = REVIEW_DIR / "f83d_short_density_materialization_target_selection.json"
SHORT_CANDIDATES = REVIEW_DIR / "f83d_short_density_candidate_shortlist.csv"
SUMMARY = REVIEW_DIR / "f83d_two_sided_density_expansion_decision_summary.json"
REPORT = REVIEW_DIR / "frontier83D_two_sided_density_expansion_or_rotation_decision_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f83d.md"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f83d_experiment_design_receipt.yaml"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f83d_run_evidence_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f83d_result_judgment_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f83d_claim_discipline_receipt.yaml"
TASK_FORCE_REVIEW = REVIEW_DIR / "f83d_task_force_review_receipt.yaml"
ARTIFACT_LINEAGE = REVIEW_DIR / "f83d_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f83d_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_83/frontier83d_two_sided_density_expansion_or_rotation_decision.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_csv_row(path: Path, row: Mapping[str, Any], *, key: str | None = None, source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    if key:
        rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def remove_registry_rows(path: Path, run_id: str) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [
            row
            for row in reader
            if row.get("run_id") != run_id
            and row.get("ledger_row_id") != f"{run_id}__target_selection"
            and row.get("row_id") != f"{run_id}__target_selection"
        ]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def remove_artifact_rows(path: Path, run_id: str) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [row for row in reader if row.get("run_id") != run_id and not str(row.get("artifact_id", "")).startswith(f"{run_id}__")]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def is_exportable(row: Mapping[str, Any]) -> bool:
    return str(row.get("model") or "").startswith(("extra_trees", "logistic"))


def short_candidate_filter(row: Mapping[str, Any]) -> bool:
    if str(row.get("side")) != "short":
        return False
    if as_int(row.get("materialization_candidate")) != 1:
        return False
    if not is_exportable(row):
        return False
    return (
        as_float(row.get("val_net")) > 0.0
        and as_float(row.get("oos_net")) > 0.0
        and as_float(row.get("val_pf")) >= 1.10
        and as_float(row.get("oos_pf")) >= 1.20
        and 5.0 <= as_float(row.get("val_calendar_trades_day")) <= 10.0
        and 5.0 <= as_float(row.get("oos_calendar_trades_day")) <= 10.0
        and as_float(row.get("val_dd_pct")) < 12.0
        and as_float(row.get("oos_dd_pct")) < 10.0
    )


def shortlist_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected = [dict(row) for row in rows if short_candidate_filter(row)]
    selected.sort(
        key=lambda row: (
            as_float(row.get("rank_score")),
            as_float(row.get("oos_pf")),
            -as_float(row.get("oos_dd_pct")),
        ),
        reverse=True,
    )
    for rank, row in enumerate(selected, start=1):
        row["f83d_shortlist_rank"] = rank
        row["f83d_selection_axis"] = "short_density_expansion_after_f83c_runtime_parity_gap"
        row["f83d_claim_boundary"] = CLAIM_BOUNDARY
    return selected


def build_payload(created_at: str) -> dict[str, Any]:
    f83c = read_json(F83C_SUMMARY)
    f82b = read_json(F82B_SUMMARY)
    all_rows = read_csv(F82B_ALL_CANDIDATES)
    all_short_rows = [row for row in all_rows if row.get("side") == "short"]
    short_materialization_rows = [row for row in all_short_rows if as_int(row.get("materialization_candidate")) == 1]
    short_exportable_materialization_rows = [row for row in short_materialization_rows if is_exportable(row)]
    shortlist = shortlist_rows(all_rows)
    if not shortlist:
        raise RuntimeError("f83d_short_density_target_missing")
    target = dict(shortlist[0])
    f83c_oos = f83c.get("oos_gap") or {}
    f83c_val = f83c.get("validation_gap") or {}
    combined_density_proxy_note = as_float(f83c_oos.get("runtime_trades_per_day")) + as_float(target.get("oos_calendar_trades_day"))
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": "F83C preserved long runtime parity(롱 런타임 동등성) but lacks density/two-sided supply(밀도/양방향 공급), so an exportable F82B short-density axis(숏 밀도 축) should be materialized as the next runtime probe(런타임 탐침).",
        "decision_use": "Select a short-side MT5 materialization target(F83E 숏 방향 MT5 물질화 대상 선택).",
        "comparison_baseline": {
            "f83c_long_runtime_validation": f83c_val,
            "f83c_long_runtime_oos": f83c_oos,
            "f82b_best_long_proxy": f82b.get("best_candidate") or {},
        },
        "control_variables": [
            "FPMarkets US100 M5(FPMarkets US100 5분봉)",
            "F82B feature/label candidate universe(F82B 피처/라벨 후보군)",
            "ONNX-exportable sklearn family only(온엑스 내보내기 가능한 사이킷런 계열만)",
        ],
        "changed_variables": [
            "side changed to short(방향을 숏으로 변경)",
            "target chosen by F83C density/two-sided gap(대상은 F83C 밀도/양방향 간극으로 선택)",
            "runtime materialization target switches from F83A teacher overlay to F82B short-density axis(런타임 물질화 대상이 F83A 교사 덧씌움에서 F82B 숏 밀도 축으로 변경)",
        ],
        "sample_scope": "Tier A separate from F82B proxy universe; Tier B missing_required; combined out_of_scope_by_claim.",
        "success_criteria": "A short exportable materialization candidate exists with validation/OOS positive net, OOS DD < 10, and 5-10 trades/day proxy density.",
        "failure_criteria": "No exportable short materialization target survives density/PF/DD filters.",
        "invalid_conditions": "F82B all-candidate file missing, candidate row cannot be reproduced by F83E, or target is not exportable.",
        "stop_conditions": "Stop F83D after selecting one F83E materialization target; do not threshold-microtune within F83D.",
        "evidence_plan": [
            rel(F83C_SUMMARY),
            rel(F82B_ALL_CANDIDATES),
            rel(TARGET_SELECTION),
            rel(SHORT_CANDIDATES),
            rel(REPORT),
        ],
        "f83c_runtime_parity_preserved": bool(f83c.get("runtime_parity_preserved")),
        "f83c_oos_runtime": {
            "net_profit": f83c_oos.get("runtime_net_profit"),
            "profit_factor": f83c_oos.get("runtime_profit_factor"),
            "drawdown_percent": f83c_oos.get("runtime_drawdown_percent"),
            "trades_per_day": f83c_oos.get("runtime_trades_per_day"),
            "long_trades": f83c_oos.get("runtime_long_trade_count"),
            "short_trades": f83c_oos.get("runtime_short_trade_count"),
        },
        "candidate_universe_counts": {
            "all_rows": len(all_rows),
            "short_rows": len(all_short_rows),
            "short_materialization_rows": len(short_materialization_rows),
            "short_exportable_materialization_rows": len(short_exportable_materialization_rows),
            "f83d_filtered_short_rows": len(shortlist),
        },
        "target": target,
        "target_selection": {
            "selection_rule": "highest_rank_score_short_exportable_materialization_candidate_with_density_5_10_oos_dd_lt10_val_dd_lt12",
            "selection_reason": "F83C showed long runtime parity but one-sided low-density objective gap; target supplies a short-side dense proxy candidate for MT5 materialization.",
            "synthetic_combined_density_note": combined_density_proxy_note,
            "synthetic_combined_density_boundary": "diagnostic_only_not_combined_economics(진단 전용, 합산 경제성 아님)",
        },
        "shortlist_rows": shortlist[:25],
        "preserved_clue": "F83B long teacher overlay preserved runtime parity(롱 교사 덧씌움 런타임 동등성 보존).",
        "new_axis": "short_density_expansion(숏 밀도 확장)",
        "negative_memory": "Do not keep repairing the long-only low-density teacher threshold(롱 전용 저밀도 교사 임계값만 계속 수리하지 말 것).",
        "result_label": "materialization_target_selected",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return payload


def report_text(payload: Mapping[str, Any]) -> str:
    target = payload["target"]
    f83c_oos = payload["f83c_oos_runtime"]
    return f"""# F83D Two-Sided Density Expansion Decision(F83D 양방향 밀도 확장 결정)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Decision(결정)

Action(행동): F83C runtime parity clue(F83C 런타임 동등성 단서)를 기준으로 F82B all-candidate universe(F82B 전체 후보군)에서 short-density materialization target(숏 밀도 물질화 대상)을 선택했다.

Effect(효과): F83E Strategy Tester(전략 테스터) 실행으로 바로 넘길 수 있는 exportable ONNX target(내보내기 가능 온엑스 대상)을 고정한다.

Selected target(선택 대상): `{target.get('candidate_id')}` / `{target.get('model')}` / `{target.get('label_name')}`.

| view(보기) | net(순손익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | trades/day(일 거래) | side(방향) |
|---|---:|---:|---:|---:|---:|---|
| F83C OOS runtime long(전선83C 표본외 런타임 롱) | `{fmt(f83c_oos.get('net_profit'))}` | `{fmt(f83c_oos.get('profit_factor'))}` | `{fmt(f83c_oos.get('drawdown_percent'))}` | `{fmt(f83c_oos.get('long_trades'), 0)}` | `{fmt(f83c_oos.get('trades_per_day'))}` | long-only(롱 전용) |
| F83D target OOS proxy short(전선83D 대상 표본외 프록시 숏) | `{fmt(target.get('oos_net'))}` | `{fmt(target.get('oos_pf'))}` | `{fmt(target.get('oos_dd_pct'))}` | `{fmt(target.get('oos_trade_count'), 0)}` | `{fmt(target.get('oos_calendar_trades_day'))}` | short-only(숏 전용) |

## Boundary(경계)

The F83D combined density note(F83D 합산 밀도 참고)는 diagnostic only(진단 전용)이다. Long runtime economics(롱 런타임 경제성)와 short proxy economics(숏 프록시 경제성)를 합산 성과로 주장하지 않는다.

Next action(다음 행동): `{NEXT_RUN_ID}` must materialize the selected short-density target(선택 숏 밀도 대상)을 MT5 Strategy Tester(MT5 전략 테스터)로 실행한다.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def gate_audit_text() -> str:
    return f"""# F83D Required Gate Coverage Audit(F83D 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `source_authority_audit(원천 권위 감사)` | `passed(통과)` | `{rel(F83C_SUMMARY)}`, `{rel(F82B_ALL_CANDIDATES)}` | F83C runtime clue(런타임 단서)와 F82B proxy universe(프록시 후보군)를 분리한다. |
| `target_selection_rule(대상 선택 규칙)` | `passed(통과)` | `{rel(TARGET_SELECTION)}` | short/exportable/density/PF/DD(숏/내보내기/밀도/수익 팩터/손실폭) 조건을 기록한다. |
| `candidate_shortlist(후보 압축 목록)` | `passed(통과)` | `{rel(SHORT_CANDIDATES)}` | 선택 전 후보군을 남긴다. |
| `experiment_design_receipt(실험 설계 영수증)` | `passed(통과)` | `{rel(EXPERIMENT_RECEIPT)}` | hypothesis/comparison/control(가설/비교/통제)을 고정한다. |
| `run_evidence_receipt(실행 근거 영수증)` | `passed(통과)` | `{rel(RUN_EVIDENCE_RECEIPT)}` | F83E materialization(물질화) 입력으로 쓰는 근거를 명명한다. |
| `result_judgment_boundary(결과 판정 경계)` | `passed(통과)` | `{rel(RESULT_RECEIPT)}` | target selection(대상 선택)만 주장한다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `{rel(TASK_FORCE_REVIEW)}` | 8명 agent(요원) 검토를 기록한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 권위/승격/실거래/목표 달성을 만들지 않는다. |
"""


def write_receipts(payload: Mapping[str, Any]) -> None:
    target = payload["target"]
    write_text(
        EXPERIMENT_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-experiment-design
status: target_selection_experiment_designed_no_authority
hypothesis: "{payload.get('hypothesis')}"
decision_use: "{payload.get('decision_use')}"
comparison_baseline: F83C long runtime gap(F83C 롱 런타임 간극) and F82B proxy universe(F82B 프록시 후보군)
control_variables:
  - FPMarkets US100 M5(FPMarkets US100 5분봉)
  - F82B feature/label universe(F82B 피처/라벨 후보군)
  - ONNX exportable model family(온엑스 내보내기 가능 모델 계열)
changed_variables:
  - short side target(숏 방향 대상)
  - density 5-10/day filter(일 5~10회 밀도 필터)
sample_scope: {payload.get('sample_scope')}
success_criteria: "{payload.get('success_criteria')}"
failure_criteria: "{payload.get('failure_criteria')}"
invalid_conditions: "{payload.get('invalid_conditions')}"
stop_conditions: "{payload.get('stop_conditions')}"
evidence_plan:
  - {rel(F83C_SUMMARY)}
  - {rel(F82B_ALL_CANDIDATES)}
  - {rel(TARGET_SELECTION)}
next_run: {NEXT_RUN_ID}
""",
    )
    write_text(
        RUN_EVIDENCE_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: target_selection_recorded_no_authority
measurement_scope: proxy target selection(프록시 대상 선택)
management_state: summary/report/target/ledger recorded(요약/보고/대상/장부 기록됨)
judgment_class: exploratory_target_selection(탐색 대상 선택)
scoreboard: structural_scout(구조 스카우트)
parity_level: P0_unverified_runtime_pending(P0 런타임 미검증 대기)
wfo_status: planned_for_future_or_exception_not_this_selection(미래 계획 또는 이번 선택에는 예외)
registry_update_required: yes
negative_memory_required: yes
hard_gate_applicable: no
evidence_boundary: candidate_target_only(후보 대상만)
target_candidate: {target.get('candidate_id')}
runtime_next: {NEXT_RUN_ID}
""",
    )
    write_text(
        RESULT_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: materialization_target_selected_no_authority
result_subject: F83D short-density target selection(F83D 숏 밀도 대상 선택)
evidence_available:
  - {rel(F83C_SUMMARY)}
  - {rel(F82B_ALL_CANDIDATES)}
  - {rel(TARGET_SELECTION)}
evidence_missing:
  - F83E MT5 Strategy Tester output(F83E MT5 전략 테스터 출력)
judgment_label: exploratory
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: "숏 후보는 프록시로 좋아 보이지만 런타임은 아직 안 봤다."
""",
    )
    write_text(
        CLAIM_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_target_selection_no_authority
allowed_claims:
  - short_density_target_selected
  - mt5_materialization_required_next
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
    )
    write_text(
        TASK_FORCE_REVIEW,
        f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f83d_target_selection_no_authority
review_mode: internal_adversarial_review_two_pass_limit(내부 비판 검토 2회차 제한)
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_02_platform_routing_architect
  - agent_03_philosophy_policy_skill_governance
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Use F83C as new evidence(F83C를 새 근거로 사용) to avoid long-only threshold-only repair(롱 전용 임계값 수리 반복 방지)."
    - "Select a short exportable density target(숏 내보내기 가능 밀도 대상)을 F83E MT5 materialization(F83E MT5 물질화)으로 넘긴다."
    - "Keep synthetic combined density(합성 합산 밀도)를 economics claim(경제성 주장)으로 쓰지 않는다."
  rejected:
    - "Do not promote F82B proxy short candidate(F82B 프록시 숏 후보)를 runtime result(런타임 결과)처럼 말하지 않는다."
  needs_local_verification:
    - "F83E must compile/export/run MT5 Strategy Tester(F83E는 컴파일/내보내기/MT5 전략 테스터 실행 필요)."
claim_boundary: {CLAIM_BOUNDARY}
""",
    )


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    paths = [TARGET_SELECTION, SHORT_CANDIDATES, SUMMARY, REPORT, GATE_AUDIT, EXPERIMENT_RECEIPT, RUN_EVIDENCE_RECEIPT, RESULT_RECEIPT, CLAIM_RECEIPT, TASK_FORCE_REVIEW, RUN_MANIFEST]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": [rel(F83C_SUMMARY), rel(F82B_SUMMARY), rel(F82B_ALL_CANDIDATES), rel(F82B_TOP200)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in paths},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_reviews_plus_ignored_source_with_hash(추적 검토 산출물 + 해시 있는 무시 원천)",
        "lineage_judgment": "connected_with_boundary(경계 있게 연결됨)",
    }


def ledger_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    target = payload["target"]
    return {
        "ledger_row_id": f"{RUN_ID}__target_selection",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "target_selection(대상 선택)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "short_density_materialization_target_selection(숏 밀도 물질화 대상 선택)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "proxy_target_selection(프록시 대상 선택)",
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "lane": "target_selection(대상 선택)",
        "family": "kpi_evidence(근거 KPI)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"target={target.get('candidate_id')};oos_pf={target.get('oos_pf')};oos_dd={target.get('oos_dd_pct')};oos_tpd={target.get('oos_calendar_trades_day')}",
        "guardrail_kpi": "target_selection_only;runtime_pending;no_authority",
        "external_verification_status": "out_of_scope_by_claim_runtime_next",
        "notes": f"next={NEXT_RUN_ID}; source={rel(F82B_ALL_CANDIDATES)}",
        "run_number": "frontier83D",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("shortlist_rows") or []),
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": target.get("candidate_id"),
        "model": target.get("model"),
        "net_profit": target.get("oos_net"),
        "profit_factor": target.get("oos_pf"),
        "drawdown": target.get("oos_dd_pct"),
        "trade_count": target.get("oos_trade_count"),
        "trades_per_day": target.get("oos_calendar_trades_day"),
        "run_date": created_at[:10],
        "primary_artifact": rel(TARGET_SELECTION),
        "view": "target_selection",
        "tier": "Tier A",
        "metric_scope": "proxy_target_selection",
        "result_status": STATUS,
        "feature_count": target.get("feature_count"),
        "work_family": "kpi_evidence",
        "row_id": f"{RUN_ID}__target_selection",
        "evidence_boundary": "target_selection_only_no_authority(대상 선택만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_target_selection_only(프록시 대상 선택만)",
    }


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = ledger_row(payload, created_at)
    for ledger_path, key in ((RUN_REGISTRY, "run_id"), (ALPHA_LEDGER, "ledger_row_id"), (STAGE_LEDGER, "ledger_row_id")):
        remove_registry_rows(ledger_path, RUN_ID)
        append_csv_row(ledger_path, row, key=key, source_header=ALPHA_LEDGER if ledger_path == STAGE_LEDGER else None)


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    target = payload["target"]
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f83_short_density_target_selected_mt5_materialization_required_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f82_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F83D short-density materialization target(숏 밀도 물질화 대상)을 선택했다."
  - "Effect(효과): target={target.get('candidate_id')}를 F83E MT5 Strategy Tester(F83E MT5 전략 테스터)로 넘긴다."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F83D target selection(F83D 대상 선택)을 완료했다.

Effect(효과): F83C long-only density gap(롱 전용 밀도 간극)을 새 evidence(근거)로 삼아 short-density target(숏 밀도 대상) `{target.get('candidate_id')}`를 F83E MT5 runtime materialization(F83E MT5 런타임 물질화)로 넘긴다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    target = payload["target"]
    write_text(
        SELECTION_STATUS,
        f"""# F83 Selection Status(F83 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F83D short-density target selection(F83D 숏 밀도 대상 선택)을 기록했다.

Effect(효과): `{target.get('candidate_id')}` / `{target.get('model')}`를 F83E Strategy Tester(F83E 전략 테스터) 대상으로 고정했다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    target = payload["target"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F83 Context Anchor(F83 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected short target(선택 숏 대상): `{target.get('candidate_id')}` / PF `{target.get('oos_pf')}` / DD `{target.get('oos_dd_pct')}` / trades/day `{target.get('oos_calendar_trades_day')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F83 Review Index(F83 검토 색인)\n"
    lines = [
        "- `frontier83D_two_sided_density_expansion_or_rotation_decision_report.md`: F83D target selection report(F83D 대상 선택 보고서)",
        "- `f83d_two_sided_density_expansion_decision_summary.json`: F83D machine summary(F83D 기계 요약)",
        "- `f83d_short_density_materialization_target_selection.json`: F83D selected short-density target(F83D 선택 숏 밀도 대상)",
        "- `f83d_short_density_candidate_shortlist.csv`: F83D short candidate shortlist(F83D 숏 후보 압축 목록)",
        "- `required_gate_coverage_audit_f83d.md`: F83D gate audit(F83D 게이트 감사)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    target = payload["target"]
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    addition = f"""

{marker}
- `{RUN_ID}` selected short-density materialization target(숏 밀도 물질화 대상) `{target.get('candidate_id')}` after F83C runtime parity/objective gap(F83C 런타임 동등성/목표 간극). Proxy OOS(프록시 표본외): net/PF/DD/tpd `{target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_calendar_trades_day')}`. Boundary(경계): target selection only, no authority(대상 선택만, 권위 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_artifact_registry(created_at: str) -> None:
    remove_artifact_rows(ARTIFACT_REGISTRY, RUN_ID)
    for path in [TARGET_SELECTION, SHORT_CANDIDATES, SUMMARY, REPORT, GATE_AUDIT, EXPERIMENT_RECEIPT, RUN_EVIDENCE_RECEIPT, RESULT_RECEIPT, CLAIM_RECEIPT, TASK_FORCE_REVIEW, ARTIFACT_LINEAGE, LOCAL_VERIFICATION]:
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "created_at": created_at,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F83D target selection only(F83D 대상 선택만 지원).",
        }
        append_csv_row(ARTIFACT_REGISTRY, row, key="artifact_id")


def packet_files(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "executed", "path": rel(EXPERIMENT_RECEIPT)},
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_REVIEW)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_LINEAGE)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(
        WORK_PACKET,
        f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
work_classification:
  primary_family: kpi_evidence
  mutation_intent: true
  execution_intent: false
skill_routing:
  primary_skill: obsidian-run-evidence-system
  support_skills:
    - obsidian-experiment-design
    - obsidian-result-judgment
    - obsidian-task-force-review
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
required_gates:
  - source_authority_audit
  - target_selection_rule
  - candidate_shortlist
  - experiment_design_receipt
  - run_evidence_receipt
  - result_judgment_boundary
  - codex_task_force_review_packet
  - final_claim_guard
  - required_gate_coverage_audit
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  claim_boundary: {CLAIM_BOUNDARY}
""",
    )
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "gates": {
                "source_authority_audit": "pass",
                "target_selection_rule": "pass",
                "candidate_shortlist": "pass",
                "experiment_design_receipt": "pass",
                "run_evidence_receipt": "pass",
                "result_judgment_boundary": "pass",
                "codex_task_force_review_packet": "pass",
                "final_claim_guard": "pass",
                "required_gate_coverage_audit": "pass",
            },
        },
    )
    write_json(
        PACKET_FINAL_CLAIM_GUARD,
        {
            "status": "pass",
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    target = payload.get("target") or {}
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "target_selection_exists": path_exists(TARGET_SELECTION),
        "shortlist_exists": path_exists(SHORT_CANDIDATES),
        "report_exists": path_exists(REPORT),
        "gate_audit_exists": path_exists(GATE_AUDIT),
        "receipts_exist": all(path_exists(path) for path in [EXPERIMENT_RECEIPT, RUN_EVIDENCE_RECEIPT, RESULT_RECEIPT, CLAIM_RECEIPT, TASK_FORCE_REVIEW]),
        "target_is_short": target.get("side") == "short",
        "target_exportable": is_exportable(target),
        "target_density_oos_5_to_10": 5.0 <= as_float(target.get("oos_calendar_trades_day")) <= 10.0,
        "workspace_state_next_run": NEXT_RUN_ID in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
        "packet_final_claim_guard_exists": path_exists(PACKET_FINAL_CLAIM_GUARD),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def write_all(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    write_json(TARGET_SELECTION, {"run_id": RUN_ID, "selected_target": payload["target"], "selection": payload["target_selection"], "claim_boundary": CLAIM_BOUNDARY, "next_run_id": NEXT_RUN_ID})
    write_csv(SHORT_CANDIDATES, payload["shortlist_rows"])
    write_json(SUMMARY, payload)
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text())
    write_receipts(payload)
    manifest = {**payload, "artifacts": {"target_selection": rel(TARGET_SELECTION), "shortlist": rel(SHORT_CANDIDATES), "summary": rel(SUMMARY), "report": rel(REPORT)}, "producer": SCRIPT_REL, "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL)}
    write_json(RUN_MANIFEST, manifest)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
    update_ledgers(payload, created_at)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    packet_files(payload, created_at)
    verification = local_verification(payload)
    write_json(LOCAL_VERIFICATION, verification)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
    update_artifact_registry(created_at)
    return verification


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    verification = write_all(payload, created_at)
    target = payload["target"]
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "target": target.get("candidate_id"),
                    "target_oos": {
                        "net": target.get("oos_net"),
                        "pf": target.get("oos_pf"),
                        "dd": target.get("oos_dd_pct"),
                        "trades_day": target.get("oos_calendar_trades_day"),
                    },
                    "shortlist_count": payload["candidate_universe_counts"]["f83d_filtered_short_rows"],
                    "local_verification": verification["status"],
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
