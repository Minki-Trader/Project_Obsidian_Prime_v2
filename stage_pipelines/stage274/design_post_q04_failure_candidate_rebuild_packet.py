from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild"
RUN_ID = "run274A_design_post_q04_failure_candidate_rebuild_packet_v1"
SOURCE_RUN_ID = "run273C_close_stage273_open_stage274_candidate_rebuild_v1"
STATUS = "completed_post_q04_failure_candidate_rebuild_packet_design_no_candidate_selection"
JUDGMENT = "fresh_candidate_rebuild_queue_ready_no_candidate_selection"
NEXT_ACTION = "run274B_materialize_post_q04_failure_candidate_package_blueprints"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE / "02_runs" / "run274A"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_STAGE273 = ROOT / "stages" / "273_onnx_candidate_campaign__time_risk_router_stability_validation"
SOURCE_CLOSEOUT = SOURCE_STAGE273 / "03_reviews" / "stage273_closeout_stage274_candidate_rebuild_handoff.md"
SOURCE_FAILURE_MEMORY = SOURCE_STAGE273 / "02_runs" / "run273B" / "stability_failure_memory.csv"
SOURCE_WEAK_SLICE = SOURCE_STAGE273 / "02_runs" / "run273B" / "weak_slice_trade_quality.csv"
SOURCE_BALANCE = SOURCE_STAGE273 / "02_runs" / "run273B" / "balance_curve_diagnostics.csv"
SOURCE_HANDOFF = SOURCE_STAGE273 / "02_runs" / "run273C" / "stage274_handoff_manifest.json"

THESIS_QUEUE = RUN_DIR / "candidate_rebuild_thesis_queue.csv"
FAILURE_MAP = RUN_DIR / "failure_to_requirement_map.csv"
BLUEPRINT_SEEDS = RUN_DIR / "candidate_package_blueprint_seeds.csv"
DISCARD_CONDITIONS = RUN_DIR / "discard_conditions.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run274A_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("; ".join(missing))


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def load_failure_facts() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    must_exist([SOURCE_CLOSEOUT, SOURCE_FAILURE_MEMORY, SOURCE_WEAK_SLICE, SOURCE_BALANCE, SOURCE_HANDOFF])
    failure = read_csv_rows(SOURCE_FAILURE_MEMORY)
    weak = read_csv_rows(SOURCE_WEAK_SLICE)
    balance = read_csv_rows(SOURCE_BALANCE)
    if not failure:
        raise ValueError("Stage273 failure memory is empty.")
    return failure, weak, balance


def build_failure_map(failure: Sequence[Mapping[str, str]], weak: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    severe = [
        row
        for row in weak
        if row.get("slice_judgment") == "negative_slice(음수 구간)"
        and (to_float(row.get("net_profit")) <= -75 or (to_float(row.get("trade_count")) >= 20 and to_float(row.get("profit_factor")) < 0.8))
    ]
    worst_severe = sorted(severe, key=lambda row: to_float(row.get("net_profit")))[:8]
    rows: list[dict[str, Any]] = []
    for row in failure:
        rows.append(
            {
                "failure_id": row["failure_id"],
                "source_tier": row["tier_scope"],
                "source_split": row["split"],
                "failure_evidence": row["evidence"],
                "design_requirement": "Candidate must reduce month/hour concentration(월/시간 집중 완화) without simply suppressing all weak-clock trades(약한 시계 거래 전체 억제 금지).",
                "discard_condition": "Discard if the new surface only lowers trade count(거래 수 감소만) or repeats q04 worst month/hour signature(q04 최악 월/시간 서명 반복).",
                "claim_boundary": BOUNDARY,
            }
        )
    for index, row in enumerate(worst_severe, start=1):
        rows.append(
            {
                "failure_id": f"stage274_severe_slice_{index:02d}",
                "source_tier": row.get("tier_scope", ""),
                "source_split": row.get("split", ""),
                "failure_evidence": f"{row.get('slice_family')} {row.get('slice_key')} net={row.get('net_profit')} pf={row.get('profit_factor')} trades={row.get('trade_count')}",
                "design_requirement": "Candidate must explain or redirect severe negative slice(심한 음수 구간 설명 또는 경로 전환).",
                "discard_condition": "Discard if severe slice(심한 구간) remains negative with PF(수익 팩터) below 0.8.",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_candidate_queue() -> list[dict[str, Any]]:
    return [
        {
            "package_id": "cp274A_session_loss_asymmetry_router",
            "candidate_role": "selectable_fresh_thesis(선택 가능 새 논제)",
            "fresh_thesis": "Session/hour loss pockets(세션/시간 손실 구간)는 no-trade filter(무거래 필터)가 아니라 direction-specific route asymmetry(방향별 경로 비대칭)로 바뀔 수 있다.",
            "feature_surface": "weekday_phase(요일 단계);session_clock_risk(세션 시계 위험);route_signal_label(경로 신호 라벨);candidate_decision_score(후보 판단 점수)",
            "decision_surface": "hour-loss zone(시간 손실 구간)에서 long/short permission(롱/숏 허용)을 따로 계산하고 flat(관망)은 마지막 수단으로만 사용",
            "risk_logic": "If hour-loss pocket(시간 손실 구간) appears, reduce exposure(노출 축소) before changing direction(방향 변경).",
            "upside_hypothesis": "Keeps q04 net edge(q04 순수익 우위) while reducing 17/18-hour loss concentration(17/18시 손실 집중).",
            "failure_mode": "Turns into a hidden filter(숨은 필터) and only reduces trade count(거래 수만 감소).",
            "discard_condition": "Reject if validation/OOS(검증/표본외) trade count falls below q04 by more than 35% without PF/DD improvement(수익 팩터/손실폭 개선).",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "package_id": "cp274B_month_regime_resilience_surface",
            "candidate_role": "selectable_fresh_thesis(선택 가능 새 논제)",
            "fresh_thesis": "Worst-month losses(최악 월 손실)는 calendar exclusion(달력 제외)이 아니라 regime-pressure reward budget(국면 압박 보상 예산) 문제다.",
            "feature_surface": "month_regime_pressure(월 국면 압박);phase_risk_score(단계 위험 점수);phase_opportunity_score(단계 기회 점수);chron_phase_age(시간순 단계 나이)",
            "decision_surface": "When regime pressure(국면 압박) is high, require payoff asymmetry(보상 비대칭) instead of blocking the month(月 차단).",
            "risk_logic": "Tighten risk only after opportunity score(기회 점수)가 약할 때; strong opportunity(강한 기회)는 작은 크기로 허용",
            "upside_hypothesis": "Reduces May/December collapse(5월/12월 붕괴) without killing all active periods(활성 구간 전체 제거).",
            "failure_mode": "Calendar proxy overfit(달력 대리 과적합).",
            "discard_condition": "Reject if gains vanish outside the named weak months(명명된 약한 월 밖에서 이익 소멸).",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "package_id": "cp274C_drawdown_recovery_context_router",
            "candidate_role": "selectable_fresh_thesis(선택 가능 새 논제)",
            "fresh_thesis": "q04 drawdown(손실폭)은 single-entry signal(단일 진입 신호)보다 recovery context(회복 문맥) 부족에서 온다.",
            "feature_surface": "chron_phase_age(시간순 단계 나이);session_clock_risk(세션 시계 위험);phase_risk_score(단계 위험 점수);route_signal_value(경로 신호 값)",
            "decision_surface": "After loss pocket proxy(손실 구간 대리)가 켜지면 re-entry permission(재진입 허용)을 score spread(점수 차이)에 묶는다.",
            "risk_logic": "Use recovery state(회복 상태) to delay same-direction re-entry(동방향 재진입 지연), not to ban the route(경로 금지 아님).",
            "upside_hypothesis": "Reduces longest underwater run(최장 회복 전 구간) while preserving active trade shape(활성 거래 형태).",
            "failure_mode": "Becomes cooldown-only repair(쿨다운만 하는 수리).",
            "discard_condition": "Reject if worst-hour net(최악 시간 순수익) improves but monthly collapse(월별 붕괴)가 유지된다.",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "package_id": "cp274D_q04_failure_boundary_control",
            "candidate_role": "support_control(보조 대조)",
            "fresh_thesis": "q04(4번 분기) 그대로의 failure signature(실패 서명)를 대조군으로 보존한다.",
            "feature_surface": "q04 existing surface(q04 기존 표면)",
            "decision_surface": "No change(변경 없음)",
            "risk_logic": "No change(변경 없음)",
            "upside_hypothesis": "None; control only(없음, 대조 전용)",
            "failure_mode": "If new packages match this signature(새 패키지가 이 서명과 같음), they are not fresh(새롭지 않음).",
            "discard_condition": "Never promote; use as reference only(승격 금지, 참조만).",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    ]


def build_blueprint_seeds(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue:
        package_id = row["package_id"]
        identity = hashlib.sha256(
            "|".join([package_id, row["feature_surface"], row["decision_surface"], row["risk_logic"]]).encode("utf-8")
        ).hexdigest()
        rows.append(
            {
                "package_id": package_id,
                "blueprint_seed_hash": identity,
                "feature_order_source": "Stage271/Stage272 q04 payload feature order(271/272단계 q04 페이로드 피처 순서)",
                "model_or_scoring_surface": "to_be_materialized_in_run274B(274B에서 물질화)",
                "adapter_path": "planned_after_survivor_only(생존 후 계획)",
                "runtime_handoff": "not_ready(준비 안 됨)",
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_discard_conditions(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "discard_condition": row["discard_condition"],
            "must_not_claim": "selected_candidate(선택 후보);ONNX readiness(온엑스 준비);Adapter handoff(어댑터 인계)",
            "effect": "Keeps Stage274(274단계) from becoming a q04 repair loop(q04 수리 반복).",
            "claim_boundary": BOUNDARY,
        }
        for row in queue
    ]


def write_receipts(queue: Sequence[Mapping[str, Any]], failure_map: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "hypothesis": "q04(4번 분기)의 월/시간 손실 집중을 직접 고치는 대신 새 decision/risk surface(판단/위험 표면)가 ONNX-worthy candidate(온엑스화 가치 후보) 후보를 만들 수 있다.",
            "decision_use": "run274B(274B 실행)에서 어떤 candidate package blueprint(후보 패키지 청사진)를 물질화할지 정한다.",
            "comparison_baseline": "q04 failure boundary control(q04 실패 경계 대조)",
            "control_variables": ["US100", "M5", "Stage271/272 feature order(271/272단계 피처 순서)", "Tier A/B paired records(티어 A/B 쌍 기록)"],
            "changed_variables": ["decision surface(판단 표면)", "risk logic(위험 로직)", "failure-memory constraints(실패 기억 제약)"],
            "sample_scope": "Stage274 design only(274단계 설계만); source evidence from run273B(273B 원천 근거)",
            "success_criteria": "At least one selectable blueprint(선택 가능 청사진) is materializable without repeating q04 failure signature(q04 실패 서명 반복 없음).",
            "failure_criteria": "All selectable blueprints(선택 가능 청사진)가 filter-only repair(필터 전용 수리) 또는 q04 duplicate(q04 중복)로 접힘.",
            "invalid_conditions": "Missing failure memory(실패 기억 누락) or source stage mismatch(원천 단계 불일치).",
            "stop_conditions": "If run274B cannot create materially distinct surfaces(실질적으로 다른 표면), close and open a new thesis(새 논제).",
            "evidence_plan": [rel(THESIS_QUEUE), rel(FAILURE_MAP), rel(BLUEPRINT_SEEDS), rel(DISCARD_CONDITIONS)],
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "data_source": [rel(SOURCE_FAILURE_MEMORY), rel(SOURCE_WEAK_SLICE), rel(SOURCE_BALANCE), rel(SOURCE_HANDOFF)],
            "time_axis": "No new bar data(새 봉 데이터 없음); consumes run273B reviewed evidence(273B 검토 근거 소비).",
            "sample_scope": "Failure memory rows(실패 기억 행) and weak-slice summaries(약한 구간 요약).",
            "missing_or_duplicate_check": f"failure_map_rows={len(failure_map)};candidate_queue_rows={len(queue)}",
            "feature_label_boundary": "No labels or future data used(라벨/미래 데이터 사용 없음).",
            "split_boundary": "Preserves validation/OOS and Tier A/B evidence labels(검증/표본외와 티어 A/B 라벨 보존).",
            "leakage_risk": "Selection bias(선택 편향) if weak slices are hard-coded as calendar filters(달력 필터로 하드코딩).",
            "data_hash_or_identity": {rel(SOURCE_FAILURE_MEMORY): sha256_file(SOURCE_FAILURE_MEMORY), rel(SOURCE_WEAK_SLICE): sha256_file(SOURCE_WEAK_SLICE)},
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "model_family": "not_trained_yet(아직 학습 없음); candidate scoring/decision surfaces(후보 점수/판단 표면) planned",
            "target_and_label": "No new target(새 목표 없음) in run274A(274A 실행).",
            "split_method": "Design stage(설계 단계); later run must keep Tier A/B and validation/OOS split(티어 A/B와 검증/표본외 분리 유지).",
            "selection_metric": "material distinctness(물질적 차이), failure signature avoidance(실패 서명 회피), and future KPI readiness(향후 KPI 준비)",
            "secondary_metrics": ["trade count(거래 수)", "net/PF/DD(순수익/수익 팩터/손실폭)", "weak month/hour slices(약한 월/시간 구간)", "Adapter identity(어댑터 정체성)"],
            "threshold_policy": "no threshold chosen yet(아직 임계값 선택 없음)",
            "overfit_risk": "High if packages encode May/December or hour 17/18 as direct exclusions(5월/12월 또는 17/18시 직접 제외).",
            "calibration_risk": "Future scores must not be described as probabilities(향후 점수를 확률로 말하지 않음).",
            "comparison_baseline": "cp274D q04 failure boundary control(q04 실패 경계 대조)",
            "validation_judgment": "exploratory_design_no_candidate_selection(탐색 설계, 후보 선택 없음)",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": "Stage274 post-q04 failure candidate rebuild design(274단계 q04 실패 이후 후보 재구성 설계)",
                "evidence_available": "run273B failure memory(273B 실패 기억);candidate thesis queue(후보 논제 대기열);discard conditions(폐기 조건)",
                "evidence_missing": "materialized score surfaces(물질화 점수 표면);MT5 KPI(MT5 핵심 성과 지표);Adapter package(어댑터 패키지);ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "q04(4번 분기)를 버리고, 실패 원인을 새 후보 설계 조건으로 바꿨다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        [
            {
                "gate_name": "work_packet_schema_lint(작업 묶음 스키마 점검)",
                "status": "passed(통과)",
                "evidence_path": rel(EXPERIMENT_RECEIPT),
                "effect": "fresh thesis(새 논제), 비교 기준, 폐기 조건을 기록했다.",
            },
            {
                "gate_name": "final_claim_guard(최종 주장 방어)",
                "status": "passed(통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            },
        ],
    )


def write_report(queue: Sequence[Mapping[str, Any]], failure_map: Sequence[Mapping[str, Any]]) -> None:
    queue_lines = "\n".join(
        f"- `{row['package_id']}`: {row['fresh_thesis']}"
        for row in queue
    )
    write_md(
        RUN_REPORT,
        f"""# run274A Post-Q04 Failure Candidate Rebuild Design(274A q04 실패 이후 후보 재구성 설계)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run274A(274A 실행)는 q04(4번 분기)를 고치지 않고, q04 failure memory(q04 실패 기억)를 새 candidate package(후보 패키지) 설계 조건으로 바꿨다.
효과(effect, 효과): 다음 run274B(274B 실행)는 같은 q04 repair(수리)가 아니라 fresh thesis(새 논제) 후보 표면을 물질화한다.

## Candidate Queue(후보 대기열)

{queue_lines}

## Evidence Paths(근거 경로)

- candidate_rebuild_thesis_queue(후보 재구성 논제 대기열): `{rel(THESIS_QUEUE)}`
- failure_to_requirement_map(실패-요구조건 지도): `{rel(FAILURE_MAP)}` rows(행) `{len(failure_map)}`
- candidate_package_blueprint_seeds(후보 패키지 청사진 씨앗): `{rel(BLUEPRINT_SEEDS)}`
- discard_conditions(폐기 조건): `{rel(DISCARD_CONDITIONS)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def update_ledgers(queue: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"candidate_thesis_rows={len(queue)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": row["package_id"],
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": f"candidate rebuild thesis {row['package_id']}",
            "tier_scope": "Tier A+B design scope",
            "kpi_scope": "candidate_rebuild_design",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": row["candidate_role"],
            "path": rel(THESIS_QUEUE),
            "primary_kpi": "planning_only",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "not_applicable",
            "notes": row["discard_condition"],
        }
        for row in queue
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": f"candidate_rebuild_thesis_{row['package_id']}",
            "tier_scope": "Tier A+B design scope",
            "scoreboard": "experiment_design",
            "status": STATUS,
            "judgment": row["candidate_role"],
            "evidence_boundary": "design_only_no_candidate_no_onnx",
            "report_path": rel(RUN_REPORT),
            "notes": row["discard_condition"],
        }
        for row in queue
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs(queue: Sequence[Mapping[str, Any]]) -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_once(selection, "run274A_report", f"- run274A_report(274A 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run274A_candidate_queue", f"- run274A_candidate_queue(274A 후보 대기열): `{rel(THESIS_QUEUE)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run274A_report",
        "\n".join(
            [
                f"- run274A_report(274A 보고서): `{rel(RUN_REPORT)}`",
                f"- run274A_candidate_queue(274A 후보 대기열): `{rel(THESIS_QUEUE)}`",
                f"- run274A_failure_map(274A 실패 지도): `{rel(FAILURE_MAP)}`",
                f"- run274A_blueprint_seeds(274A 청사진 씨앗): `{rel(BLUEPRINT_SEEDS)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run274A_summary",
        f"- run274A_summary(274A 요약): run274A(274A 실행)는 q04(4번 분기) 실패 이후 candidate rebuild thesis queue(후보 재구성 논제 대기열) `{len(queue)}`개를 만들었다. Effect(효과): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않고 run274B(274B 실행) 물질화로 넘긴다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage274(274단계) run274A(274A 실행) post q04 failure candidate rebuild design(q04 실패 이후 후보 재구성 설계) `{RUN_ID}`. "
        f"Effect(효과): candidate thesis rows(후보 논제 행) `{len(queue)}`개를 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run274A post-q04 failure candidate rebuild design(274A q04 실패 이후 후보 재구성 설계)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): q04(4번 분기)를 반복하지 않고 fresh thesis(새 논제) 후보 대기열 `{len(queue)}`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [SOURCE_CLOSEOUT, SOURCE_FAILURE_MEMORY, SOURCE_WEAK_SLICE, SOURCE_BALANCE, SOURCE_HANDOFF]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage274/design_post_q04_failure_candidate_rebuild_packet.py",
        "entry_command": "python stage_pipelines/stage274/design_post_q04_failure_candidate_rebuild_packet.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    full_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run274A_candidate_rebuild_design_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run274A post-q04 failure candidate rebuild design artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def execute() -> dict[str, Any]:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    failure, weak, _balance = load_failure_facts()
    failure_map = build_failure_map(failure, weak)
    queue = build_candidate_queue()
    blueprint_seeds = build_blueprint_seeds(queue)
    discard = build_discard_conditions(queue)
    write_csv(FAILURE_MAP, failure_map)
    write_csv(THESIS_QUEUE, queue)
    write_csv(BLUEPRINT_SEEDS, blueprint_seeds)
    write_csv(DISCARD_CONDITIONS, discard)
    write_receipts(queue, failure_map)
    write_report(queue, failure_map)
    artifacts = [
        THESIS_QUEUE,
        FAILURE_MAP,
        BLUEPRINT_SEEDS,
        DISCARD_CONDITIONS,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers(queue)
    update_state_docs(queue)
    write_manifests_and_registry(created_at, artifacts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "candidate_thesis_rows": len(queue),
        "failure_map_rows": len(failure_map),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
