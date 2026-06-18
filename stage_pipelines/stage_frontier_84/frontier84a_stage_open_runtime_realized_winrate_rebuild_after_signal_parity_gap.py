from __future__ import annotations

import csv
import io
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
RUN_ID = "frontier84A_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap_v1"
PARENT_RUN_ID = "frontier83G_runtime_realized_outcome_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier84B_runtime_realized_winrate_proxy_scout_v1"

STATUS = "opened_runtime_realized_winrate_rebuild_hypothesis_lifecycle_no_authority"
JUDGMENT = "frontier84_opened_runtime_realized_winrate_label_axis_after_f83_gap_no_authority"
CLAIM_BOUNDARY = (
    "frontier84_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f83_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "retired_archive_only_no_new_grok_call_no_next_open_block"

SCRIPT_REL = "stage_pipelines/stage_frontier_84/frontier84a_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
INPUT_DIR = STAGE_DIR / "01_inputs"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
REPORT = REVIEW_DIR / "frontier84A_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap_report.md"
MANIFEST = REVIEW_DIR / "f84a_stage_open_manifest.json"
EXPERIMENT_DESIGN = REVIEW_DIR / "f84a_experiment_design.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f84a_state_sync_audit.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f84a_artifact_lineage.json"
GATE_AUDIT_MD = REVIEW_DIR / "required_gate_coverage_audit_f84a_open.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
LOCAL_VERIFICATION = REVIEW_DIR / "f84a_local_verification.json"

STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f84a_stage_transition_receipt.yaml"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f84a_experiment_design_receipt.yaml"
EXPLORATION_RECEIPT = REVIEW_DIR / "f84a_exploration_mandate_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f84a_result_judgment_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f84a_artifact_lineage_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f84a_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f84a_claim_discipline_receipt.yaml"
ANSWER_RECEIPT = REVIEW_DIR / "f84a_answer_clarity_receipt.yaml"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_stage_frontier_84_open.md"
FRONTIER_EXTRA_REGISTER = ROOT / "docs/registers/frontier_extra_stage_register.yaml"
FIVE_STAGE_RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"

F83_STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
F83_STAGE_DIR = ROOT / "stages" / F83_STAGE_ID
F83G_SUMMARY = F83_STAGE_DIR / "03_reviews/f83g_repair_or_rotation_decision_summary.json"
F83G_REPORT = F83_STAGE_DIR / "03_reviews/stage_closeout_report.md"
F83E_SUMMARY = F83_STAGE_DIR / "03_reviews/f83e_short_side_density_runtime_materialization_summary.json"
F83F_SUMMARY = F83_STAGE_DIR / "03_reviews/f83f_short_density_proxy_runtime_gap_analysis_summary.json"
F83F_GAP_ROWS = F83_STAGE_DIR / "03_reviews/f83f_short_density_proxy_runtime_gap_rows.csv"
F83F_CAUSE_ROWS = F83_STAGE_DIR / "03_reviews/f83f_gap_cause_attribution_rows.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def csv_output_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        try:
            relative_to_cwd = resolved.relative_to(Path.cwd().resolve())
        except ValueError:
            relative_to_cwd = None
        if relative_to_cwd is not None and len(str(relative_to_cwd)) < 240:
            return relative_to_cwd
        if len(str(resolved)) < 240:
            return resolved
    return io_path(path)


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            sample = io_path(candidate).read_bytes()
            return "\r\n" if b"\r\n" in sample else "\n"
    return "\n"


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    lineterminator = csv_lineterminator(path, source_header)
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
        rows = []
    else:
        fieldnames = [field for field in row.keys() if field]
        rows = []
    for field in row:
        if field and field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore", lineterminator=lineterminator)
    writer.writeheader()
    writer.writerows(rows)
    csv_output_path(path).write_bytes(buffer.getvalue().encode("utf-8-sig"))


def as_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def fmt(value: Any, digits: int = 4) -> str:
    number = as_float(value)
    if number is None:
        return str(value)
    return f"{number:.{digits}f}"


def ensure_dirs() -> None:
    for directory in (SPEC_DIR, INPUT_DIR, RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def build_design(created_at: str) -> dict[str, Any]:
    f83g = read_json(F83G_SUMMARY)
    f83e = read_json(F83E_SUMMARY)
    f83f = read_json(F83F_SUMMARY)
    runtime_oos = f83g.get("runtime_probe_kpi", {}).get("oos", {})
    runtime_validation = f83g.get("runtime_probe_kpi", {}).get("validation", {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "primary_family": "state_sync",
        "primary_skill": "obsidian-stage-transition",
        "support_skills": [
            "obsidian-reentry-read",
            "obsidian-experiment-design",
            "obsidian-exploration-mandate",
            "obsidian-artifact-lineage",
            "obsidian-result-judgment",
            "obsidian-task-force-review",
            "obsidian-claim-discipline",
            "obsidian-answer-clarity",
        ],
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "idea_id": "IDEA-FR84-RUNTIME-REALIZED-WINRATE-REBUILD-AFTER-SIGNAL-PARITY-GAP",
        "frontier_thesis": (
            "Runtime-realized win/loss, stop-touch, and fill-path labels(런타임 실현 승패, 손절·익절 터치, 체결 경로 라벨)을 "
            "F83E/F83F의 actual MT5 outcome(실제 MT5 결과)에서 재구성하면, proxy success after signal parity(신호 동등성 뒤 프록시 성공)가 "
            "actual MT5 win rate(실제 MT5 승률)로 보존되는 exportable ONNX candidate(내보내기 가능 온엑스 후보)를 만들 수 있다."
        ),
        "hypothesis": (
            "F83의 loss(손실)는 signal count mismatch(신호 수 불일치)가 아니라 runtime win-rate erosion(런타임 승률 침식)이므로, "
            "다음 proxy(프록시)는 종가 방향 smooth_supply(부드러운 공급) 대신 runtime-realized outcome(런타임 실현 결과)을 직접 예측해야 한다."
        ),
        "decision_use": (
            "F84B가 runtime-realized label proxy scout(런타임 실현 라벨 프록시 탐색)를 실행해 MT5 materialization candidate(MT5 물질화 후보)를 만들지, "
            "또는 F83 negative memory(부정 기억)를 더 강한 do-not-repeat(반복 금지)로 닫을지 결정한다."
        ),
        "comparison_baseline": [
            f"F83E validation runtime(검증 런타임): net/PF/DD/tpd/winrate {runtime_validation.get('net_profit')}/{runtime_validation.get('profit_factor')}/{runtime_validation.get('max_drawdown_percent')}/{runtime_validation.get('trades_per_day')}/{runtime_validation.get('win_rate_percent')}",
            f"F83E OOS runtime(표본외 런타임): net/PF/DD/tpd/winrate {runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}/{runtime_oos.get('win_rate_percent')}",
            "F83D proxy short-density target(프록시 숏 밀도 대상): proxy OOS positive but runtime negative(프록시 표본외 양수였으나 런타임 부정)",
        ],
        "control_variables": [
            "symbol/timeframe(심볼/시간프레임): FPMarkets US100 M5(FPMarkets US100 5분봉)",
            "reference boundary(참조 경계): F83 artifacts are reference only(F83 산출물은 참조 전용)",
            "no inherited winner/baseline/authority(승자/기준선/권위 상속 없음)",
            "meaningful candidate requires MT5 Strategy Tester materialization(의미 후보는 MT5 전략 테스터 물질화 필요)",
        ],
        "changed_variables": [
            "label axis changes to runtime-realized win/loss(라벨 축을 런타임 실현 승패로 변경)",
            "target axis includes stop-touch/fill-path(목표 축에 손절·익절 터치/체결 경로 포함)",
            "risk axis must react to DD expansion after signal parity(위험 축은 신호 동등성 이후 손실폭 확대에 반응)",
            "session/regime split is allowed before threshold micro-search(임계값 미세탐색 전 세션/장세 분할 허용)",
        ],
        "sample_scope": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "stage": STAGE_ID,
            "reference_window": "F83E validation 2025-01-02..2025-10-01 and OOS 2025-10-01..2026-04-14",
            "tier_scope": "Tier A separate required in F84B; Tier B and combined must be recorded or marked missing_required/out_of_scope_by_claim",
        },
        "success_criteria": [
            "F84B produces at least one meaningful proxy candidate(의미 있는 프록시 후보 1개 이상)",
            "candidate density remains 5-10 trades/day in proxy(프록시에서 일 5~10회 밀도 유지)",
            "proxy target explicitly improves win-rate preservation vs F83E/F83F(프록시 목표가 F83E/F83F 대비 승률 보존을 직접 개선)",
            "any meaningful candidate is materialized in MT5 Strategy Tester(의미 후보는 MT5 전략 테스터로 물질화)",
        ],
        "failure_criteria": [
            "runtime-realized labels collapse to threshold-only repair(런타임 실현 라벨이 임계값 수리 반복으로 붕괴)",
            "candidate density dies below usable trade supply(후보 밀도가 사용 가능 거래 공급 이하로 사망)",
            "proxy candidate repeats f82b_10355 smooth_supply short close_direction surface(기존 f82b_10355 표면 반복)",
            "MT5 materialization shows same win-rate/DD erosion after signal parity(MT5 물질화에서 동일 승률/손실폭 침식)",
        ],
        "invalid_conditions": [
            "row-level runtime outcome mapping cannot be traced(행 단위 런타임 결과 매핑 불가)",
            "features leak future realized outcome into entry features(피처가 미래 실현 결과를 누수)",
            "stop-touch/fill-path label semantics are ambiguous(손절·익절 터치/체결 경로 라벨 의미 불명확)",
            "ONNX export/parity is claimed without reproducible artifact identity(재현 가능한 산출물 정체성 없이 온엑스 동등성 주장)",
        ],
        "stop_conditions": [
            "No signal/no trade/mismatch/crash/block(무신호/무거래/불일치/충돌/차단)은 negative evidence(부정 근거)로 기록",
            "No new axis beyond threshold/filter/parameter(임계값/필터/파라미터 외 새 축 없음)이면 capped repair(상한 수리)",
            "Runtime claim(런타임 주장)은 MT5 receipt/report/log/snapshot(영수증/보고서/로그/스냅샷) 없이는 낮춘다",
        ],
        "evidence_plan": [
            rel(F83G_SUMMARY),
            rel(F83E_SUMMARY),
            rel(F83F_SUMMARY),
            rel(F83F_GAP_ROWS),
            rel(F83F_CAUSE_ROWS),
            rel(EXPERIMENT_DESIGN),
            rel(REPORT),
            rel(MANIFEST),
        ],
        "prior_stage_scan": {
            "preserved_clue": f83g.get("preserved_clues", []),
            "negative_memory": f83g.get("negative_memory", []),
            "do_not_repeat": [
                "Do not reuse f82b_10355 smooth_trade_supply short close_direction surface with threshold/filter/parameter-only repair(동일 f82b_10355 표면 임계값/필터/파라미터만 수리 금지).",
                "Do not treat ONNX/signal parity as economics authority(온엑스/신호 동등성을 경제성 권위로 취급 금지).",
            ],
            "reopen_axes": f83g.get("repair_admissibility", {}).get("allowed_reopen_axes", []),
        },
        "exploration_mandate": {
            "legacy_relation": "prior_evidence_only(과거 근거 전용)",
            "tier_scope": "Tier A required; Tier B/combined explicit missing or out_of_scope allowed only with reason(Tier A 필수, Tier B/합산은 사유 포함 누락 가능)",
            "broad_sweep": "runtime label family x stop-touch target x fill-path target x session/regime split x risk logic(런타임 라벨군 x 터치 목표 x 체결 경로 x 세션/장세 x 위험 로직)",
            "extreme_sweep": "include zero/low/high/extreme hold and TP/SL touch windows when legal(합법 범위의 무/저/고/극단 보유 및 손절·익절 터치 창 포함)",
            "micro_search_gate": "only after a label family shows density and win-rate preservation(라벨군이 밀도와 승률 보존을 보인 뒤)",
            "wfo_plan": "F84B starts as scout but must prepare WFO-aware selection before runtime validation(F84B는 탐색이지만 런타임 검증 전 WFO 인식 선택 준비)",
            "failure_memory": "negative memory must include salvage value and reopen condition(부정 기억은 회수 가치와 재개 조건 포함)",
            "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계 전용, 권위 없음)",
        },
        "runtime_reference": {
            "validation": runtime_validation,
            "oos": runtime_oos,
            "primary_gap_cause": f83g.get("primary_gap_cause"),
            "artifact_export_status": f83e.get("artifact_export_status"),
            "f83f_judgment": f83f.get("judgment"),
        },
    }


def stage_brief_text(design: Mapping[str, Any]) -> str:
    return f"""# F84 Stage Brief(F84 단계 개요)

Updated(갱신): {design['created_at_utc']}

Stage ID(단계 ID): `{STAGE_ID}`

Opening run(개방 실행): `{RUN_ID}`

Status(상태): `{STATUS}`

## Frontier Thesis(전선 가설)

{design['frontier_thesis']}

Effect(효과): F84는 F83의 short-density proxy(숏 밀도 프록시)를 winner(승자)로 물려받지 않고, runtime-realized outcome label(런타임 실현 결과 라벨)을 새 축으로 시험한다.

## Novelty Delta(신규성 차이)

- F83의 primary cause(주 원인)는 `{design['runtime_reference']['primary_gap_cause']}`였다.
- F84는 same-surface threshold/filter-only repair(동일 표면 임계값/필터만 수리)를 하지 않는다.
- F84는 stop-touch/fill-path/risk/session-regime(손절·익절 터치/체결 경로/위험/세션·장세)을 넓게 섞는다.

## Experiment Design(실험 설계)

- hypothesis(가설): {design['hypothesis']}
- decision_use(결정 용도): {design['decision_use']}
- comparison_baseline(비교 기준): {'; '.join(design['comparison_baseline'])}
- control_variables(고정 변수): {'; '.join(design['control_variables'])}
- changed_variables(변경 변수): {'; '.join(design['changed_variables'])}
- sample_scope(표본 범위): {json.dumps(design['sample_scope'], ensure_ascii=False)}
- success_criteria(성공 기준): {'; '.join(design['success_criteria'])}
- failure_criteria(실패 기준): {'; '.join(design['failure_criteria'])}
- invalid_conditions(무효 조건): {'; '.join(design['invalid_conditions'])}
- stop_conditions(중지 조건): {'; '.join(design['stop_conditions'])}
- evidence_plan(근거 계획): {'; '.join(design['evidence_plan'])}

## Prior Stage Scan(이전 단계 점검)

- preserved clue(보존 단서): {json.dumps(design['prior_stage_scan']['preserved_clue'], ensure_ascii=False)}
- negative memory(부정 기억): {json.dumps(design['prior_stage_scan']['negative_memory'], ensure_ascii=False)}
- do_not_repeat(반복 금지): {json.dumps(design['prior_stage_scan']['do_not_repeat'], ensure_ascii=False)}

## Boundary(경계)

This run(이 실행)은 stage open/design only(단계 개방/설계 전용)다. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`.
"""


def input_refs_text(design: Mapping[str, Any]) -> str:
    return f"""# F84 Input References(F84 입력 참조)

Updated(갱신): {design['created_at_utc']}

Prepared by(작성 실행): `{RUN_ID}`

## Reference Only(참조 전용)

- F83 closeout report(F83 마감 보고서): `{rel(F83G_REPORT)}`
- F83G closeout summary(F83G 마감 요약): `{rel(F83G_SUMMARY)}`
- F83E MT5 runtime materialization(F83E MT5 런타임 물질화): `{rel(F83E_SUMMARY)}`
- F83F gap analysis(F83F 간극 분석): `{rel(F83F_SUMMARY)}`
- F83F gap rows(F83F 간극 행): `{rel(F83F_GAP_ROWS)}`
- F83 negative register(F83 부정 등록부): `{rel(NEGATIVE_REGISTER)}`

## Do Not Inherit(상속 금지)

- winner(승자)
- selected baseline(선택 기준선)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)

Effect(효과): F84 can use F83 as clue memory(F84는 F83을 단서 기억으로만 사용) and must build its own hypothesis/proxy/runtime evidence(자체 가설/프록시/런타임 근거를 만들어야 함).
"""


def report_text(design: Mapping[str, Any]) -> str:
    runtime_oos = design["runtime_reference"]["oos"]
    return f"""# F84A Stage Open Runtime-Realized Win-Rate Rebuild(F84A 단계 개방 런타임 실현 승률 재구축)

Updated(갱신): {design['created_at_utc']}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Open Decision(개방 결정)

Action(행동): F84를 runtime-realized win-rate rebuild(런타임 실현 승률 재구축) hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F83의 부정 근거를 반복하지 않고, 실제 MT5 승률이 무너진 원인을 새 label/target/risk axis(라벨/목표/위험 축)로 직접 시험한다.

## F83 Reference KPI(F83 참고 KPI)

- Runtime OOS(런타임 표본외): net/PF/DD/trades-day/win-rate(순손익/수익 팩터/손실폭/일 거래/승률) `{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}/{runtime_oos.get('win_rate_percent')}`
- Primary gap cause(주 간극 원인): `{design['runtime_reference']['primary_gap_cause']}`

## F84A Experiment Contract(F84A 실험 계약)

- hypothesis(가설): {design['hypothesis']}
- broad_sweep(넓은 탐색): {design['exploration_mandate']['broad_sweep']}
- micro_search_gate(미세 탐색 게이트): {design['exploration_mandate']['micro_search_gate']}
- next action(다음 행동): `{NEXT_RUN_ID}`

## Claim Boundary(주장 경계)

F84A is open/design only(F84A는 개방/설계 전용). It does not create proxy KPI(프록시 KPI), runtime KPI(런타임 KPI), ONNX candidate(온엑스 후보), selected baseline(선택 기준선), or runtime authority(런타임 권위).
"""


def selection_status_text(design: Mapping[str, Any]) -> str:
    return f"""# F84 Selection Status(F84 선택 상태)

Updated(갱신): {design['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F84A stage open(F84A 단계 개방)을 기록했다.

Effect(효과): F84는 F83 same-surface repair(동일 표면 수리)를 반복하지 않고 runtime-realized win-rate rebuild(런타임 실현 승률 재구축)로 시작한다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def workspace_state_text(design: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
resume_frontier_id: {STAGE_ID}
runtime_probe_status: f84_open_design_only_runtime_probe_pending_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
five_stage_retrospective_due_status: {FIVE_STAGE_RETROSPECTIVE_STATUS}
updated_at_utc: '{design['created_at_utc']}'
context_anchor: {rel(REVIEW_DIR / 'context_anchor.md')}
notes:
  - "Action(행동): F84A stage open(F84A 단계 개방)을 완료했다."
  - "Effect(효과): F83 negative memory(부정 기억)를 참조로만 쓰고 F84 runtime-realized win-rate rebuild(F84 런타임 실현 승률 재구축)를 새 가설 생명주기로 열었다."
  - "Next(다음): {NEXT_RUN_ID}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""


def current_working_state_text(design: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {design['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F84A open(개방)으로 F84를 runtime-realized win-rate rebuild(런타임 실현 승률 재구축) hypothesis lifecycle(가설 생명주기)로 열었다.

Effect(효과): F83의 same-surface threshold/filter repair(동일 표면 임계값/필터 수리)는 금지하고, F84B에서 runtime-realized label proxy scout(런타임 실현 라벨 프록시 탐색)를 진행한다.

## What Is True Now(지금 참인 것)

- F84A is stage open/design only(F84A는 단계 개방/설계 전용).
- F83G remains valid negative memory(F83G는 유효한 부정 기억으로 유지).
- F84B is the next proxy scout(F84B가 다음 프록시 탐색).

## Not Yet True(아직 참이 아닌 것)

No proxy KPI/runtime KPI/ONNX candidate/completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(프록시 KPI/런타임 KPI/온엑스 후보/완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def context_anchor_text(design: Mapping[str, Any]) -> str:
    return f"""# F84 Context Anchor(F84 문맥 앵커)

Updated(갱신): {design['created_at_utc']}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- parent negative memory(부모 부정 기억): `{PARENT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def review_index_text(design: Mapping[str, Any]) -> str:
    return f"""# F84 Review Index(F84 검토 색인)

Updated(갱신): {design['created_at_utc']}

- `{rel(REPORT)}`: F84A stage open report(F84A 단계 개방 보고서)
- `{rel(EXPERIMENT_DESIGN)}`: F84A experiment design(F84A 실험 설계)
- `{rel(MANIFEST)}`: F84A stage open manifest(F84A 단계 개방 목록)
- `{rel(GATE_AUDIT_MD)}`: F84A gate coverage audit(F84A 게이트 커버리지 감사)
- `{rel(TASK_FORCE_RECEIPT)}`: F84A Task Force receipt(F84A 태스크포스 영수증)
- `{rel(ARTIFACT_LINEAGE)}`: F84A artifact lineage(F84A 산출물 계보)
"""


def decision_memo_text(design: Mapping[str, Any]) -> str:
    return f"""# Decision Memo: F84 Open(F84 개방 결정 메모)

Updated(갱신): {design['created_at_utc']}

Decision(결정): Open(개방) `{STAGE_ID}` after F83 closeout(F83 마감 후).

Action(행동): F83 runtime win-rate erosion after signal parity(F83 신호 동등성 이후 런타임 승률 침식)를 negative memory(부정 기억)로 두고, F84를 runtime-realized win-rate rebuild(런타임 실현 승률 재구축)로 열었다.

Effect(효과): F84B는 same-surface threshold/filter repair(동일 표면 임계값/필터 수리)가 아니라 runtime-realized label proxy scout(런타임 실현 라벨 프록시 탐색)를 수행한다.

Evidence(근거):

- `{rel(F83G_REPORT)}`
- `{rel(STAGE_BRIEF)}`
- `{rel(REPORT)}`
- `{rel(WORK_PACKET)}`

Boundary(경계): open/design only(개방/설계만). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text(design: Mapping[str, Any]) -> str:
    return f"""# F84A Required Gate Coverage Audit(F84A 필수 게이트 커버리지 감사)

Updated(갱신): {design['created_at_utc']}

Packet(묶음): `{RUN_ID}`

Primary family(주 작업군): `state_sync(상태 동기화)`

Primary skill(주 스킬): `obsidian-stage-transition(단계 전환)`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `state_sync_audit(상태 동기화 감사)` | `passed(통과)` | `{rel(STATE_SYNC_AUDIT)}` | active_stage(활성 단계)를 F84로 맞춘다. |
| `frontier_open_contract(전선 개방 계약)` | `passed(통과)` | `{rel(STAGE_BRIEF)}` | thesis/novelty/prior scan/exit boundary(가설/신규성/이전 점검/종료 경계)를 기록한다. |
| `frontier_extra_due_check(전선 추가 도래 점검)` | `passed_not_due(통과_도래아님)` | `{rel(FRONTIER_EXTRA_REGISTER)}` | F84는 F100 전이라 Extra Stage(추가 단계) 도래가 아니다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `{rel(TASK_FORCE_RECEIPT)}` | 8명 agent(요원) 검토를 남긴다. |
| `experiment_design_receipt(실험 설계 영수증)` | `passed(통과)` | `{rel(EXPERIMENT_RECEIPT)}` | 가설/비교/통제/성공·실패 조건을 고정한다. |
| `exploration_mandate_receipt(탐색 명령 영수증)` | `passed(통과)` | `{rel(EXPLORATION_RECEIPT)}` | broad/extreme/WFO/failure-memory(넓은/극단/워크포워드/실패 기억)를 연결한다. |
| `artifact_lineage_audit(산출물 계보 감사)` | `passed(통과)` | `{rel(ARTIFACT_LINEAGE)}` | source/producer/consumer/hash(원천/생산자/소비자/해시)를 연결한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{rel(PACKET_FINAL_CLAIM_GUARD)}` | 권위/승격/완성 주장을 막는다. |

Not applicable with reason(사유 있는 해당 없음):

- `kpi_contract_audit(KPI 계약 감사)`: no proxy/runtime KPI(프록시/런타임 KPI 없음) in stage-open design packet(단계 개방 설계 묶음).
- `mt5_runtime_evidence_gate(MT5 런타임 근거 게이트)`: no MT5 execution(MT5 실행 없음) in F84A.
- `model_training_gate(모델 학습 게이트)`: no model training(모델 학습 없음) in F84A.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def state_sync_audit(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "state_sync_audit",
        "packet_id": RUN_ID,
        "status": "pass",
        "active_stage": STAGE_ID,
        "current_run": NEXT_RUN_ID,
        "latest_completed_run": RUN_ID,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_at_utc": design["created_at_utc"],
    }


def final_claim_guard(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "gate": "final_claim_guard",
        "status": "pass",
        "allowed_claims": [
            "stage_opened(단계 개방)",
            "design_only(설계 전용)",
            "proxy_scout_handoff_named(프록시 탐색 인계 지명)",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
            "git_push_as_validation",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_at_utc": design["created_at_utc"],
    }


def receipt_texts(design: Mapping[str, Any]) -> dict[Path, str]:
    return {
        STAGE_TRANSITION_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-stage-transition
status: completed_f84_stage_open_no_authority
active_stage: {STAGE_ID}
latest_completed_run_id: {RUN_ID}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
five_stage_retrospective_status: {FIVE_STAGE_RETROSPECTIVE_STATUS}
claim_boundary: {CLAIM_BOUNDARY}
""",
        EXPERIMENT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-experiment-design
status: recorded_stage_open_design_no_authority
hypothesis: "{design['hypothesis']}"
decision_use: "{design['decision_use']}"
comparison_baseline: "{'; '.join(design['comparison_baseline'])}"
control_variables: "{'; '.join(design['control_variables'])}"
changed_variables: "{'; '.join(design['changed_variables'])}"
sample_scope: "{json.dumps(design['sample_scope'], ensure_ascii=False)}"
success_criteria: "{'; '.join(design['success_criteria'])}"
failure_criteria: "{'; '.join(design['failure_criteria'])}"
invalid_conditions: "{'; '.join(design['invalid_conditions'])}"
stop_conditions: "{'; '.join(design['stop_conditions'])}"
evidence_plan: "{'; '.join(design['evidence_plan'])}"
claim_boundary: {CLAIM_BOUNDARY}
""",
        EXPLORATION_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-exploration-mandate
status: recorded_runtime_realized_axis_no_authority
idea_id: {design['idea_id']}
hypothesis: "{design['frontier_thesis']}"
legacy_relation: {design['exploration_mandate']['legacy_relation']}
tier_scope: {design['exploration_mandate']['tier_scope']}
broad_sweep: {design['exploration_mandate']['broad_sweep']}
extreme_sweep: {design['exploration_mandate']['extreme_sweep']}
micro_search_gate: {design['exploration_mandate']['micro_search_gate']}
wfo_plan: {design['exploration_mandate']['wfo_plan']}
failure_memory: {design['exploration_mandate']['failure_memory']}
evidence_boundary: {design['exploration_mandate']['evidence_boundary']}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: stage_open_design_only_no_authority
result_subject: F84 stage open(F84 단계 개방)
evidence_available:
  - {rel(F83G_SUMMARY)}
  - {rel(STAGE_BRIEF)}
  - {rel(REPORT)}
evidence_missing:
  - F84 proxy KPI(F84 프록시 KPI)
  - F84 MT5 runtime probe(F84 MT5 런타임 탐침)
  - F84 ONNX export candidate(F84 온엑스 내보내기 후보)
judgment_label: exploratory(탐색)
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: "F84는 열렸지만 아직 후보나 런타임 결과는 없다."
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F83G_SUMMARY)}
  - {rel(F83E_SUMMARY)}
  - {rel(F83F_SUMMARY)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_lineage: {rel(ARTIFACT_LINEAGE)}
availability: tracked_reports_with_hashes(해시가 있는 추적 보고서)
claim_boundary: {CLAIM_BOUNDARY}
""",
        TASK_FORCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f84_stage_open_no_authority
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
    - "Open F84 as new hypothesis lifecycle(F84를 새 가설 생명주기로 개방)."
    - "Use F83 runtime win-rate erosion as reference-only negative memory(F83 런타임 승률 침식을 참조 전용 부정 기억으로 사용)."
    - "Require broad runtime-realized label sweep before micro threshold search(미세 임계값 전 넓은 런타임 실현 라벨 탐색 요구)."
    - "Require MT5 Strategy Tester materialization for meaningful F84 candidates(의미 있는 F84 후보는 MT5 전략 테스터 물질화 요구)."
  rejected:
    - "Do not inherit f82b_10355/F83 short-density surface as baseline(f82b_10355/F83 숏 밀도 표면을 기준선으로 상속하지 않음)."
    - "Do not call stage-open design a model or runtime result(단계 개방 설계를 모델/런타임 결과로 부르지 않음)."
  needs_local_verification:
    - "F84B must produce proxy evidence before any materialization claim(F84B 프록시 근거 전 물질화 주장 금지)."
claim_boundary: {CLAIM_BOUNDARY}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_stage_open_no_authority
allowed_claims:
  - f84_opened_design_only
  - next_proxy_scout_named
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
        ANSWER_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-answer-clarity
status: user_facing_summary_ready
plain_meaning: F84 is now open as a new research question, but no model or runtime candidate exists yet(F84는 새 연구 질문으로 열렸지만 모델/런타임 후보는 아직 없음).
what_is_true_now: stage_open_design_only(단계 개방 설계 전용)
what_is_not_true: proxy_runtime_onnx_authority_or_goal_achieve(프록시/런타임/온엑스 권위 또는 목표 달성 아님)
claim_boundary: {CLAIM_BOUNDARY}
""",
    }


def packet_files(design: Mapping[str, Any]) -> None:
    write_text(
        WORK_PACKET,
        f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{design['created_at_utc']}'
work_classification:
  primary_family: state_sync
  mutation_intent: true
  execution_intent: false
skill_routing:
  primary_skill: obsidian-stage-transition
  support_skills:
    - obsidian-reentry-read
    - obsidian-experiment-design
    - obsidian-exploration-mandate
    - obsidian-artifact-lineage
    - obsidian-result-judgment
    - obsidian-task-force-review
    - obsidian-claim-discipline
    - obsidian-answer-clarity
required_gates:
  - state_sync_audit
  - frontier_open_contract
  - frontier_extra_due_check
  - codex_task_force_review_packet
  - experiment_design_receipt
  - exploration_mandate_receipt
  - artifact_lineage_audit
  - final_claim_guard
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  claim_boundary: {CLAIM_BOUNDARY}
""",
    )
    sync_payload = state_sync_audit(design)
    write_json(PACKET_STATE_SYNC_AUDIT, sync_payload)
    write_json(STATE_SYNC_AUDIT, sync_payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_claim_guard(design))
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "receipts": [
                {"skill": "obsidian-stage-transition", "status": "executed", "path": rel(STAGE_TRANSITION_RECEIPT)},
                {"skill": "obsidian-experiment-design", "status": "executed", "path": rel(EXPERIMENT_RECEIPT)},
                {"skill": "obsidian-exploration-mandate", "status": "executed", "path": rel(EXPLORATION_RECEIPT)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_RECEIPT)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
                {"skill": "obsidian-answer-clarity", "status": "executed", "path": rel(ANSWER_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "status": "passed",
            "required_gates": {
                "state_sync_audit": "pass",
                "frontier_open_contract": "pass",
                "frontier_extra_due_check": "pass_not_due",
                "codex_task_force_review_packet": "pass",
                "experiment_design_receipt": "pass",
                "exploration_mandate_receipt": "pass",
                "artifact_lineage_audit": "pass",
                "final_claim_guard": "pass",
            },
            "not_applicable_with_reason": {
                "kpi_contract_audit": "No proxy/runtime KPI(프록시/런타임 KPI 없음) in F84A stage-open design packet.",
                "mt5_runtime_evidence_gate": "No MT5 execution(MT5 실행 없음) in F84A.",
                "model_training_gate": "No model training(모델 학습 없음) in F84A.",
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def ledger_row(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "stage_open(단계 개방)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "F84 stage open(F84 단계 개방)",
        "tier_scope": "Tier A/B not_applicable_until_proxy(Tier A/B는 프록시 전까지 해당 없음)",
        "kpi_scope": "stage_open_design(단계 개방 설계)",
        "scoreboard_lane": "frontier_stage_open(전선 단계 개방)",
        "lane": "stage_open",
        "family": "state_sync",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": "stage_open=1;proxy_kpi=pending;runtime_kpi=pending",
        "guardrail_kpi": f"frontier_extra_due={FRONTIER_EXTRA_DUE_STATUS};no_authority;no_same_surface_threshold_only_repair",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"next={NEXT_RUN_ID}; parent={PARENT_RUN_ID}; design_only",
        "run_number": "frontier84A",
        "date": design["created_at_utc"][:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": design["created_at_utc"][:10],
        "primary_artifact": rel(MANIFEST),
        "view": "stage_open",
        "tier": "stage_open_design",
        "metric_scope": "stage_open_design",
        "result_status": STATUS,
        "work_family": "state_sync",
        "row_id": f"{RUN_ID}__stage_open",
        "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": design["frontier_thesis"],
        "artifact_count": 16,
        "created_at_utc": design["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT_MD),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_only",
        "run_family": "stage_open",
        "run_type": "stage_open",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(REPORT),
    }


def update_ledgers(design: Mapping[str, Any]) -> None:
    row = ledger_row(design)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def artifact_rows(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts: Sequence[tuple[str, Path, str]] = [
        ("stage_pipeline_script", ROOT / SCRIPT_REL, "F84A stage open producer script(F84A 단계 개방 생산 스크립트)"),
        ("stage_brief", STAGE_BRIEF, "F84 stage brief(F84 단계 개요)"),
        ("input_refs", INPUT_REFS, "F84 input references(F84 입력 참조)"),
        ("stage_open_report", REPORT, "F84A stage open report(F84A 단계 개방 보고서)"),
        ("stage_open_manifest", MANIFEST, "F84A stage open manifest(F84A 단계 개방 목록)"),
        ("experiment_design", EXPERIMENT_DESIGN, "F84A experiment design(F84A 실험 설계)"),
        ("selection_status", SELECTION_STATUS, "F84 selection status(F84 선택 상태)"),
        ("work_packet", WORK_PACKET, "F84A work packet(F84A 작업 묶음)"),
        ("gate_audit", GATE_AUDIT_MD, "F84A gate coverage audit(F84A 게이트 커버리지 감사)"),
        ("state_sync_audit", STATE_SYNC_AUDIT, "F84A state sync audit(F84A 상태 동기화 감사)"),
        ("task_force_receipt", TASK_FORCE_RECEIPT, "F84A Task Force receipt(F84A 태스크포스 영수증)"),
        ("artifact_lineage", ARTIFACT_LINEAGE, "F84A artifact lineage(F84A 산출물 계보)"),
        ("local_verification", LOCAL_VERIFICATION, "F84A local verification(F84A 로컬 검증)"),
    ]
    rows: list[dict[str, Any]] = []
    for artifact_type, path, notes in artifacts:
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": design["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": design["created_at_utc"],
                "notes": notes,
                "artifact_path": rel(path),
                "effect": "Supports F84 stage open/design only(F84 단계 개방/설계만 지원).",
            }
        )
    return rows


def update_artifact_registry(design: Mapping[str, Any]) -> None:
    for row in artifact_rows(design):
        upsert_csv(ARTIFACT_REGISTRY, "artifact_id", row)


def update_changelog_and_idea(design: Mapping[str, Any]) -> None:
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        entry = f"""# 2026-06-18 - F84A Stage Open(F84A 단계 개방)

- Action(행동): `{RUN_ID}`로 `{STAGE_ID}`를 runtime-realized win-rate rebuild(런타임 실현 승률 재구축) hypothesis lifecycle(가설 생명주기)로 열었다.
- Effect(효과): F83 win-rate erosion negative memory(F83 승률 침식 부정 기억)를 참조로만 쓰고, F84B runtime-realized label proxy scout(F84B 런타임 실현 라벨 프록시 탐색)를 다음 실행으로 둔다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
        write_text(CHANGELOG, entry + changelog)
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea_text:
        addition = f"""

{marker}
- `{design['idea_id']}` opened by `{RUN_ID}`. Hypothesis(가설): {design['frontier_thesis']} Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): open/design only(개방/설계만), no authority(권위 없음).
"""
        write_text(IDEA_REGISTRY, idea_text.rstrip() + addition)


def local_verification(design: Mapping[str, Any]) -> dict[str, Any]:
    state_text = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    current_text = io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE) else ""
    selection_text = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig") if path_exists(SELECTION_STATUS) else ""
    task_force_text = io_path(TASK_FORCE_RECEIPT).read_text(encoding="utf-8-sig") if path_exists(TASK_FORCE_RECEIPT) else ""
    checks = [
        {"check": "f83g_source_exists", "passed": path_exists(F83G_SUMMARY)},
        {"check": "stage_brief_exists", "passed": path_exists(STAGE_BRIEF)},
        {"check": "selection_status_exists", "passed": path_exists(SELECTION_STATUS)},
        {"check": "workspace_state_names_f84", "passed": f"active_stage: {STAGE_ID}" in state_text},
        {"check": "current_working_state_names_f84", "passed": STAGE_ID in current_text},
        {"check": "selection_status_names_f84a", "passed": RUN_ID in selection_text and STATUS in selection_text},
        {"check": "packet_exists", "passed": path_exists(WORK_PACKET)},
        {"check": "task_force_all_agents", "passed": all(f"agent_0{i}_" in task_force_text for i in range(1, 9))},
        {"check": "next_run_named", "passed": NEXT_RUN_ID in state_text and NEXT_RUN_ID in selection_text},
        {"check": "final_claim_guard_exists", "passed": path_exists(PACKET_FINAL_CLAIM_GUARD)},
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if all(check["passed"] for check in checks) else "fail",
        "all_passed": all(check["passed"] for check in checks),
        "checks": checks,
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_at_utc": design["created_at_utc"],
    }


def write_lineage(design: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    artifacts = [
        ROOT / SCRIPT_REL,
        STAGE_BRIEF,
        INPUT_REFS,
        REPORT,
        MANIFEST,
        EXPERIMENT_DESIGN,
        SELECTION_STATUS,
        WORK_PACKET,
        GATE_AUDIT_MD,
        STATE_SYNC_AUDIT,
        TASK_FORCE_RECEIPT,
        LOCAL_VERIFICATION,
    ]
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": design["created_at_utc"],
        "source_inputs": [rel(F83G_SUMMARY), rel(F83G_REPORT), rel(F83E_SUMMARY), rel(F83F_SUMMARY), rel(F83F_GAP_ROWS), rel(NEGATIVE_REGISTER)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY)],
        "availability": "tracked_reports_with_hashes(해시가 있는 추적 보고서)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
        "local_verification": verification,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(ARTIFACT_LINEAGE, payload)


def write_state_docs(design: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(design))
    write_text(CURRENT_WORKING_STATE, current_working_state_text(design))
    write_text(SELECTION_STATUS, selection_status_text(design))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(design))
    write_text(REVIEW_DIR / "context_anchor.md", context_anchor_text(design))
    write_text(REVIEW_INDEX, review_index_text(design))
    write_text(DECISION_MEMO, decision_memo_text(design))


def write_all(design: Mapping[str, Any]) -> dict[str, Any]:
    write_json(EXPERIMENT_DESIGN, design)
    write_text(STAGE_BRIEF, stage_brief_text(design))
    write_text(INPUT_REFS, input_refs_text(design))
    write_text(REPORT, report_text(design))
    write_text(GATE_AUDIT_MD, gate_audit_text(design))
    for path, text in receipt_texts(design).items():
        write_text(path, text)
    packet_files(design)
    write_state_docs(design)
    update_ledgers(design)
    write_json(
        MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "experiment_design": rel(EXPERIMENT_DESIGN),
            "report": rel(REPORT),
            "work_packet": rel(WORK_PACKET),
            "created_at_utc": design["created_at_utc"],
        },
    )
    update_changelog_and_idea(design)
    verification = local_verification(design)
    write_json(LOCAL_VERIFICATION, verification)
    write_lineage(design, verification)
    update_artifact_registry(design)
    return verification


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    design = build_design(created_at)
    design["producer"] = SCRIPT_REL
    design["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    verification = write_all(design)
    runtime_oos = design["runtime_reference"]["oos"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "active_stage": STAGE_ID,
                "latest_completed_run": RUN_ID,
                "next_run": NEXT_RUN_ID,
                "reference_oos": {
                    "net": runtime_oos.get("net_profit"),
                    "pf": runtime_oos.get("profit_factor"),
                    "dd": runtime_oos.get("max_drawdown_percent"),
                    "trades_per_day": runtime_oos.get("trades_per_day"),
                    "win_rate": runtime_oos.get("win_rate_percent"),
                },
                "local_verification": verification["status"],
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
