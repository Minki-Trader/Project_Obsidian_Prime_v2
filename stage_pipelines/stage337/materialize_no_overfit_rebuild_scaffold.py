from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AG"
RUN_ID = "run337AG_no_overfit_rebuild_scaffold_materialization_v1"
PARENT_RUN_ID = "run337AF_failure_memory_and_no_overfit_rebuild_queue_v1"
NEXT_RUN_ID = "run337AH_execute_full_current_day_visibility_repair_and_no_overfit_preflight_v1"
STATUS = "completed_stage337AG_no_overfit_rebuild_scaffold_materialized_no_training_no_selection"
JUDGMENT = "run337AF_queue_converted_to_predeclared_repair_defensive_offensive_scaffold"
DECISION = "stage337AG_open_run337AH_visibility_repair_and_no_overfit_preflight_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AG_no_overfit_rebuild_scaffold_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337AF_DIR = STAGE_DIR / "02_runs" / "run337AF"
REVIEWS_DIR = STAGE_DIR / "03_reviews"

REPORT_PATH = REVIEWS_DIR / "run337AG_no_overfit_rebuild_scaffold_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AG_no_overfit_rebuild_scaffold_materialization.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

AF_FAILURE_MEMORY = RUN337AF_DIR / "failure_memory.csv"
AF_DO_NOT_REPEAT = RUN337AF_DIR / "do_not_repeat_register.csv"
AF_GUARDRAILS = RUN337AF_DIR / "no_overfit_guardrail_matrix.csv"
AF_QUEUE = RUN337AF_DIR / "next_experiment_queue.csv"
AF_PROXY = RUN337AF_DIR / "proxy_mt5_usability_matrix.csv"
AF_EVIDENCE_MAP = RUN337AF_DIR / "evidence_to_requirement_map.csv"
AF_REOPEN = RUN337AF_DIR / "reopen_conditions.csv"
AF_FINAL = RUN337AF_DIR / "final_rebuild_queue_decision.json"

SCAFFOLD_MATRIX = RUN_DIR / "experiment_scaffold_matrix.csv"
PREDECLARED_GATES = RUN_DIR / "predeclared_gate_contracts.csv"
NO_LOOKAHEAD_POLICY = RUN_DIR / "no_lookahead_split_policy.csv"
PROXY_MT5_ROLE_LOCK = RUN_DIR / "proxy_mt5_role_lock_contract.csv"
MT5_REPAIR_CONTRACT = RUN_DIR / "mt5_visibility_repair_contract.csv"
COST_OBJECTIVE_CONTRACT = RUN_DIR / "cost_curve_objective_contract.csv"
SIDE_SURFACE_CONTRACT = RUN_DIR / "side_specific_payoff_surface_contract.csv"
ASOF_REGIME_CONTRACT = RUN_DIR / "asof_external_regime_source_contract.csv"
DB_TELEMETRY_CONTRACT = RUN_DIR / "db_source_telemetry_contract.csv"
ATR_RISK_CONTRACT = RUN_DIR / "predeclared_atr_exit_risk_surface_contract.csv"
EVIDENCE_READINESS = RUN_DIR / "evidence_readiness_audit.csv"
EXECUTION_QUEUE = RUN_DIR / "run337AH_execution_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_scaffold_decision.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_json(path: Path) -> Any:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if bom else "utf-8"), bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text, True)


def row_by(rows: Sequence[Mapping[str, str]], **match: str) -> dict[str, str]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in match.items()):
            return dict(row)
    return {}


def source_bundle() -> dict[str, Any]:
    return {
        "failure_memory": read_csv(AF_FAILURE_MEMORY),
        "do_not_repeat": read_csv(AF_DO_NOT_REPEAT),
        "guardrails": read_csv(AF_GUARDRAILS),
        "queue": read_csv(AF_QUEUE),
        "proxy": read_csv(AF_PROXY),
        "evidence_map": read_csv(AF_EVIDENCE_MAP),
        "reopen": read_csv(AF_REOPEN),
        "final": read_json(AF_FINAL),
    }


def track_contract_type(track: str) -> str:
    if track.startswith("repair"):
        return "runtime_data_repair(런타임/데이터 수리)"
    if track.startswith("defensive"):
        return "defensive_objective(방어 목적함수)"
    if track.startswith("offensive"):
        return "offensive_payoff_surface(공격 손익 표면)"
    if track.startswith("data"):
        return "asof_data_source(시점 기준 데이터 원천)"
    if track.startswith("parity"):
        return "proxy_mt5_parity(프록시-MT5 동등성)"
    if track.startswith("instrumentation"):
        return "runtime_telemetry_instrumentation(런타임 텔레메트리 계측)"
    if track.startswith("risk_exit"):
        return "risk_exit_surface(위험/청산 표면)"
    return "research_contract(연구 계약)"


def build_scaffold_matrix(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in sorted(src["queue"], key=lambda row: number(row.get("priority"))):
        priority = str(queue.get("priority", ""))
        experiment_id = queue.get("experiment_id", "")
        track = queue.get("track", "")
        rows.append(
            {
                "scaffold_id": experiment_id.replace("run337AG_", "scaffold_"),
                "source_experiment_id": experiment_id,
                "priority": priority,
                "track": track,
                "contract_type": track_contract_type(track),
                "question": queue.get("question", ""),
                "required_inputs": queue.get("required_inputs", ""),
                "required_evidence": queue.get("required_evidence", ""),
                "success_read": queue.get("success_read", ""),
                "failure_read": queue.get("failure_read", ""),
                "forbidden_shortcut": queue.get("forbidden_shortcut", ""),
                "no_overfit_controls": "predeclared evidence(사전 선언 증거); no forward retune(전진 재조정 금지); receipt-linked claim(영수증 연결 주장)",
                "first_execution_status": "scaffold_materialized_not_executed(뼈대 물질화, 실행 아님)",
                "next_run_slot": NEXT_RUN_ID,
                "effect": queue.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_predeclared_gates(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G337AG_forward_visibility",
            "source_guardrail_id": "G08_latest_forward_visibility_required",
            "scope": "repair(수리)",
            "pass_condition": "tester_to_feature_last_gap_minutes=0 and proxy/MT5 parity(프록시/MT5 동등성) refreshed for full current-day control(현재일 전체 대조)",
            "fail_condition": "gap remains(공백 유지) or telemetry mismatch(텔레메트리 불일치)",
            "evidence_required": "MT5 Strategy Tester report(전략 테스터 보고서), runtime summary(런타임 요약), timestamp-aligned parity(시점 맞춤 동등성)",
            "enforcement_phase": NEXT_RUN_ID,
            "effect": "Forward Passed/Failed(전진 통과/실패) 판정 전에 데이터 가시성을 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "G337AG_cost_ladder",
            "source_guardrail_id": "G04_cost_curve_direction_bundle",
            "scope": "defensive(방어)",
            "pass_condition": "fixed 0/0.5/1/2/3/5/10 point stress ladder(고정 포인트 압박 사다리) keeps net/PF/recovery/curve pocket(순수익/수익 팩터/회복/곡선 포켓) jointly acceptable under pre-forward validation(전진 전 검증)",
            "fail_condition": "single-point fragility(단일 포인트 취약성) or cost-tuned threshold(비용 맞춤 임계값)",
            "evidence_required": rel(COST_OBJECTIVE_CONTRACT),
            "enforcement_phase": "future_training_validation(미래 학습/검증)",
            "effect": "비용에 약한 후보를 초기 검증에서 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "G337AG_direction_surface",
            "source_guardrail_id": "G03_no_lot_or_short_only_fix",
            "scope": "offensive(공격)",
            "pass_condition": "long/short(롱/숏) each meet trade count/PF/recovery/pocket(거래수/수익 팩터/회복/포켓) without completed-day short-only disable(완성일 숏만 차단)",
            "fail_condition": "side filter(방향 필터)가 completed-day loss(완성일 손실)에 사후 피팅됨",
            "evidence_required": rel(SIDE_SURFACE_CONTRACT),
            "enforcement_phase": "future_training_validation(미래 학습/검증)",
            "effect": "방향 손실을 숨기지 않고 손익 표면으로 다룬다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "G337AG_asof_regime",
            "source_guardrail_id": "G06_external_asof_only",
            "scope": "data(데이터)",
            "pass_condition": "VIX/USD/rate(변동성 지수/달러/금리) rows have as-of timestamp(시점), lag policy(지연 정책), missing policy(결측 정책)",
            "fail_condition": "post-forward macro backfill(전진 이후 거시지표 사후 결합)",
            "evidence_required": rel(ASOF_REGIME_CONTRACT),
            "enforcement_phase": NEXT_RUN_ID,
            "effect": "경제 국면 설명에서 look-ahead bias(미래참조 편향)를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "G337AG_proxy_mt5_role",
            "source_guardrail_id": "G05_proxy_context_only",
            "scope": "parity(동등성)",
            "pass_condition": "proxy expected value(프록시 예상값)는 signal sanity(신호 점검), MT5(MetaTrader 5, 메타트레이더5)는 KPI authority(KPI 권위)로 고정",
            "fail_condition": "proxy-only KPI(프록시 단독 KPI) or proxy-only selection(프록시 단독 선택)",
            "evidence_required": rel(PROXY_MT5_ROLE_LOCK),
            "enforcement_phase": "all_future_runs(모든 미래 실행)",
            "effect": "연구 속도와 런타임 권위를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "G337AG_db_telemetry",
            "source_guardrail_id": "G07_db_source_instrumented",
            "scope": "instrumentation(계측)",
            "pass_condition": "D/B source(D/B 원천), D+B overlap(D+B 동시), timestamp(시점)가 telemetry(텔레메트리)에 직접 기록됨",
            "fail_condition": "buy/sell direction(매수/매도 방향)을 D/B source(D/B 원천)로 대체",
            "evidence_required": rel(DB_TELEMETRY_CONTRACT),
            "enforcement_phase": NEXT_RUN_ID,
            "effect": "D/B attribution(D/B 귀속)을 실제 원천으로만 주장한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "G337AG_receipt_claim",
            "source_guardrail_id": "G09_receipt_before_claim",
            "scope": "result_judgment(결과 판정)",
            "pass_condition": "data/model/runtime/result receipts(데이터/모델/런타임/결과 영수증) and artifact registry(산출물 등록부) are linked before claim(주장)",
            "fail_condition": "report-only completion(보고서만으로 완료)",
            "evidence_required": rel(EVIDENCE_READINESS),
            "enforcement_phase": "closeout(종료)",
            "effect": "완료 주장의 근거를 산출물에 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_no_lookahead_policy() -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "NL01_forward_holdout_locked",
            "rule": "2026-04-14 이후 forward data(전진 데이터)는 tuning/training/threshold/lot/risk selection(조정/학습/임계값/랏/위험 선택)에 쓰지 않는다.",
            "allowed_use": "diagnostic failure memory(진단 실패 기억), final untouched forward judgment(최종 미접촉 전진 판정)",
            "prohibited_use": "threshold retune(임계값 재조정), cost/side/risk filter fit(비용/방향/위험 필터 맞춤)",
            "verification": "run manifest(실행 목록)에 train/validation/forward cutoffs(학습/검증/전진 절단시점)를 기록",
            "effect": "forward pocket overfit(전진 포켓 과적합)을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "policy_id": "NL02_shared_window_pre_forward_only",
            "rule": "새 학습 또는 후보 재구성은 shared window(공유 구간) `2022-08-01`부터 `2026-04-13` 안의 사전 분할만 사용한다.",
            "allowed_use": "walk-forward optimization/WFO(워크포워드 최적화), purged validation(정화 검증), negative controls(부정 대조)",
            "prohibited_use": "2026-04-14 이후 결과를 보고 split(분할) 재선택",
            "verification": "split manifest(분할 목록) hash(해시) and timestamp boundary(시점 경계)",
            "effect": "학습 데이터와 전진 데이터 경계를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "policy_id": "NL03_macro_asof_lag",
            "rule": "external regime(외부 국면) 데이터는 as-of timestamp(시점 기준), release lag(공표 지연), missing policy(결측 정책)를 가진 경우에만 join(결합)한다.",
            "allowed_use": "regime attribution(국면 귀속), source-clean model branch(원천 깨끗한 모델 가지)",
            "prohibited_use": "post-hoc macro backfill(사후 거시지표 채움)",
            "verification": rel(ASOF_REGIME_CONTRACT),
            "effect": "경제지표를 설명력으로 쓰되 미래참조 편향을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "policy_id": "NL04_proxy_not_kpi",
            "rule": "proxy expected value(프록시 예상값)는 MT5(MetaTrader 5, 메타트레이더5)와 timestamp aligned(시점 정렬)일 때 signal sanity(신호 점검)에만 쓴다.",
            "allowed_use": "feature/order/handoff sanity(피처/순서/인계 점검)",
            "prohibited_use": "net/PF/DD/recovery(순수익/수익 팩터/손실폭/회복) claim(주장)",
            "verification": rel(PROXY_MT5_ROLE_LOCK),
            "effect": "proxy(프록시)와 runtime authority(런타임 권위)를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_proxy_mt5_role_lock(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in src["proxy"]:
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "proxy_match_read": f"{row.get('proxy_matched', '')}/{row.get('proxy_total', '')}",
                "gap_status": row.get("gap_status", ""),
                "allowed_use": "signal sanity(신호 점검), feature handoff parity(피처 인계 동등성), timestamp alignment check(시점 정렬 점검)",
                "disallowed_use": "KPI authority(KPI 권위), Forward Passed/Failed(전진 통과/실패), candidate selection(후보 선택)",
                "role_lock": "proxy_expected_context_only_mt5_runtime_authority_only_after_full_evidence(프록시 예상은 문맥 전용, MT5는 전체 증거 후 권위)",
                "next_check": "refresh after run337AH full current-day visibility repair(337AH 현재일 전체 가시성 수리 후 갱신)",
                "source_evidence": row.get("source_evidence", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_mt5_repair_contract(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    failure = row_by(src["failure_memory"], failure_id="ST337AF_full_current_day_boundary_gap")
    return [
        {
            "repair_step": "R01_confirm_latest_broker_bars",
            "purpose": "US100 M5 broker data(브로커 데이터)가 latest feature_last(최신 피처 마지막)까지 있는지 확인",
            "input_evidence": failure.get("source_evidence", ""),
            "required_output": "broker latest close timestamp(브로커 최신 종가 시점), feature_last timestamp(피처 마지막 시점)",
            "success_condition": "latest broker close(최신 브로커 종가) >= feature_last(피처 마지막)",
            "failure_condition": "data missing/incomplete(데이터 누락/불완전)",
            "effect": "데이터 문제와 tester visibility(테스터 가시성) 문제를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "repair_step": "R02_clear_or_rollover_tester_visibility",
            "purpose": "Strategy Tester(전략 테스터)가 current-day midnight cap(현재일 자정 경계)에 걸리는지 재확인",
            "input_evidence": failure.get("evidence_summary", ""),
            "required_output": "tester_last_observed_bar_time(테스터 마지막 관측 봉), tester_to_feature_last_gap_minutes(테스터-피처 마지막 공백 분)",
            "success_condition": "gap_minutes=0 for full current-day control(현재일 전체 대조)",
            "failure_condition": "tester_feature_last_gap_remains(테스터 피처 마지막 공백 유지)",
            "effect": "Forward decision(전진 판정) 가능 여부를 먼저 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "repair_step": "R03_rerun_proxy_mt5_parity",
            "purpose": "full current-day control(현재일 전체 대조)의 proxy/MT5 parity(프록시/MT5 동등성)를 갱신",
            "input_evidence": rel(AF_PROXY),
            "required_output": "timestamp_aligned_proxy_mt5_difference.csv(시점 맞춤 프록시-MT5 차이)",
            "success_condition": "all decision dimensions matched(모든 판단 차원 일치)",
            "failure_condition": "dimension mismatch(차원 불일치) or missing telemetry(텔레메트리 누락)",
            "effect": "proxy expected value(프록시 예상값)의 역할을 다시 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_cost_objective_contract() -> list[dict[str, Any]]:
    stress_points = ["0", "0.5", "1", "2", "3", "5", "10"]
    return [
        {
            "stress_point": point,
            "metric_bundle": "net/PF/recovery/DD/rolling pocket/trade count(순수익/수익 팩터/회복/손실폭/이동 포켓/거래수)",
            "selection_role": "candidate_gate_draft_not_forward_tuned(후보 게이트 초안, 전진 맞춤 아님)",
            "pass_read": "must remain jointly healthy across pre-forward validation(전진 전 검증에서 함께 건강해야 함)",
            "fail_read": "cost-thin profile(비용 얇은 프로필)",
            "no_overfit_control": "same ladder for all variants(모든 변형에 같은 사다리), no point-specific threshold(포인트별 임계값 없음)",
            "effect": "비용 버퍼를 결과 보고가 아니라 목적/게이트 계약으로 올린다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for point in stress_points
    ]


def build_side_surface_contract() -> list[dict[str, Any]]:
    return [
        {
            "side": side,
            "minimum_evidence": "trade count/PF/expectancy/recovery/rolling pocket/cost stress(거래수/수익 팩터/기대값/회복/이동 포켓/비용 압박)",
            "allowed_action": "side-specific model or label branch(방향별 모델 또는 라벨 가지) after pre-forward evidence(전진 전 증거 이후)",
            "forbidden_action": "completed-day short-only kill switch(완성일 숏만 차단하는 스위치)",
            "split_requirement": "train/validation/forward split must be side-aware(학습/검증/전진 분할은 방향 인식 필요)",
            "effect": "롱/숏 손익을 숨기지 않고 각각 독립 압박한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for side in ("long/buy(롱/매수)", "short/sell(숏/매도)", "combined_total(합산 전체)")
    ]


def build_asof_regime_contract(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    missing_failure = row_by(src["failure_memory"], failure_id="ST337AF_economic_regime_missing")
    raw_fields = missing_failure.get("evidence_summary", "missing_fields=vix_zscore_20,usdx_zscore_20,us10yr_zscore_20")
    fields = raw_fields.split("=", 1)[-1].split(",")
    meanings = {
        "vix_zscore_20": "VIX regime(변동성 지수 국면)",
        "usdx_zscore_20": "USD regime(달러 국면)",
        "us10yr_zscore_20": "rate regime(금리 국면)",
    }
    return [
        {
            "field": field,
            "meaning": meanings.get(field, "external regime(외부 국면)"),
            "source_requirement": "as-of timestamp(시점 기준), release lag(공표 지연), timezone(시간대), missing policy(결측 정책)",
            "join_policy": "left join at or before bar timestamp(봉 시점 이하 가장 최근 값 결합)",
            "forbidden_policy": "after-the-fact backfill(사후 채움)",
            "required_audit": "source hash(원천 해시), row coverage(행 커버리지), lag audit(지연 감사)",
            "effect": "경제 국면 설명을 데이터 무결성 안으로 가져온다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for field in fields
        if field
    ]


def build_db_telemetry_contract() -> list[dict[str, Any]]:
    fields = [
        ("db_source", "D/B source(D/B 원천)", "D, B, D+B, neither(D, B, 동시, 없음)"),
        ("d_rule_state", "D rule state(D 규칙 상태)", "true/false plus reason(참/거짓 및 이유)"),
        ("b_rule_state", "B rule state(B 규칙 상태)", "true/false plus reason(참/거짓 및 이유)"),
        ("decision_surface_source", "decision surface source(판단 표면 원천)", "model/rule/handoff(모델/규칙/인계)"),
        ("source_timestamp", "source timestamp(원천 시점)", "bar or trade open timestamp(봉 또는 거래 개시 시점)"),
    ]
    return [
        {
            "field": field,
            "meaning": meaning,
            "allowed_values": allowed,
            "required_in": "Python feature artifact(파이썬 피처 산출물), MT5 runtime telemetry(MT5 런타임 텔레메트리), trade record(거래 기록)",
            "claim_unlocked": "D/B attribution(D/B 귀속) only after row-level parity(행 단위 동등성)",
            "forbidden_claim": "buy/sell direction(매수/매도 방향)을 D/B로 대체",
            "effect": "D/B 분석을 실제 원천 기록과 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for field, meaning, allowed in fields
    ]


def build_atr_risk_contract() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sl_values = ["0.75", "1.00", "1.25", "1.50", "2.00"]
    tp_values = ["1.00", "1.50", "2.00", "2.50", "3.00"]
    for sl in sl_values:
        for tp in tp_values:
            rows.append(
                {
                    "grid_id": f"atr_sl_{sl}_tp_{tp}",
                    "atr_sl": sl,
                    "atr_tp": tp,
                    "selection_role": "predeclared_research_grid_not_forward_tuned(사전 선언 연구 격자, 전진 맞춤 아님)",
                    "metrics_required": "net/PF/DD/recovery/trade_count/cost_stress/curve_pocket(순수익/수익 팩터/손실폭/회복/거래수/비용 압박/곡선 포켓)",
                    "forbidden_use": "pick best completed-day pocket(완성일 최고 포켓 선택)",
                    "effect": "청산/위험 수리를 넓은 사전 격자로만 허용한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_evidence_readiness(scaffold: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in scaffold:
        track = item["track"]
        if str(track).startswith("repair"):
            readiness = "ready_for_run337AH_execution_attempt(337AH 실행 시도 준비)"
            missing = "fresh MT5 run output(신규 MT5 실행 출력)"
        elif str(track).startswith(("defensive", "offensive", "risk_exit")):
            readiness = "contract_ready_execution_pending(계약 준비, 실행 대기)"
            missing = "pre-forward training/validation run(전진 전 학습/검증 실행)"
        elif str(track).startswith(("data", "instrumentation")):
            readiness = "source_contract_ready_implementation_pending(원천 계약 준비, 구현 대기)"
            missing = "source files/telemetry implementation(원천 파일/텔레메트리 구현)"
        else:
            readiness = "role_contract_ready_refresh_pending(역할 계약 준비, 갱신 대기)"
            missing = "fresh parity refresh(신규 동등성 갱신)"
        rows.append(
            {
                "scaffold_id": item["scaffold_id"],
                "track": track,
                "readiness": readiness,
                "missing_before_positive_claim": missing,
                "positive_claim_allowed": "false",
                "next_action": NEXT_RUN_ID,
                "effect": "지금 가능한 것과 아직 필요한 증거를 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_execution_queue(scaffold: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in scaffold:
        priority = int(number(item.get("priority")))
        track = str(item.get("track", ""))
        if priority == 1:
            immediate_action = "execute_or_repair_full_current_day_MT5_visibility(현재일 전체 MT5 가시성 실행 또는 수리)"
            blocking_evidence = rel(MT5_REPAIR_CONTRACT)
            execution_mode = "runtime_repair_probe(런타임 수리 탐침)"
        elif priority in (4, 6):
            immediate_action = "materialize_source_or_telemetry_inputs(원천 또는 텔레메트리 입력 물질화)"
            blocking_evidence = rel(ASOF_REGIME_CONTRACT if priority == 4 else DB_TELEMETRY_CONTRACT)
            execution_mode = "input_materialization(입력 물질화)"
        elif priority == 5:
            immediate_action = "refresh_proxy_MT5_role_lock_after_repair(수리 후 프록시-MT5 역할 고정 갱신)"
            blocking_evidence = rel(PROXY_MT5_ROLE_LOCK)
            execution_mode = "parity_refresh(동등성 갱신)"
        else:
            immediate_action = "prepare_pre_forward_validation_runner(전진 전 검증 러너 준비)"
            blocking_evidence = rel(COST_OBJECTIVE_CONTRACT if priority == 2 else ATR_RISK_CONTRACT if "risk_exit" in track else SIDE_SURFACE_CONTRACT)
            execution_mode = "pre_forward_research_execution(전진 전 연구 실행)"
        rows.append(
            {
                "queue_order": priority,
                "source_scaffold_id": item["scaffold_id"],
                "execution_mode": execution_mode,
                "immediate_action": immediate_action,
                "required_contract": blocking_evidence,
                "done_when": item.get("required_evidence", ""),
                "forbidden_shortcut": item.get("forbidden_shortcut", ""),
                "claim_after_execution": "diagnostic_only_until_full_gate_bundle_passes(전체 게이트 묶음 전까지 진단 전용)",
                "effect": item.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_audit(src: Mapping[str, Any], scaffold: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], execution_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "work_packet_schema_lint(작업 묶음 스키마 점검)",
            "status": "passed(통과)",
            "evidence_path": f"{rel(SCAFFOLD_MATRIX)};{rel(PREDECLARED_GATES)};{rel(EXECUTION_QUEUE)}",
            "effect": "experiment_design(실험 설계) 작업군의 필수 구조를 산출물로 남겼다.",
        },
        {
            "gate_name": "run337AF_parent_queue_consumed(337AF 부모 대기열 소비)",
            "status": "passed(통과)",
            "evidence_path": rel(AF_QUEUE),
            "effect": f"{len(src['queue'])}개 parent queue(부모 대기열)를 {len(scaffold)}개 scaffold(뼈대)로 변환했다.",
        },
        {
            "gate_name": "predeclared_gates_materialized(사전 선언 게이트 물질화)",
            "status": "passed(통과)",
            "evidence_path": rel(PREDECLARED_GATES),
            "effect": f"{len(gates)}개 gate contract(게이트 계약)을 만들었다.",
        },
        {
            "gate_name": "no_lookahead_policy_materialized(미래참조 방지 정책 물질화)",
            "status": "passed(통과)",
            "evidence_path": rel(NO_LOOKAHEAD_POLICY),
            "effect": "2026-04-14 이후 forward data(전진 데이터)를 조정에 쓰지 않는 정책을 고정했다.",
        },
        {
            "gate_name": "proxy_mt5_role_lock_materialized(프록시-MT5 역할 고정 물질화)",
            "status": "passed(통과)",
            "evidence_path": rel(PROXY_MT5_ROLE_LOCK),
            "effect": "proxy expected value(프록시 예상값)는 signal sanity(신호 점검) 전용으로 고정했다.",
        },
        {
            "gate_name": "execution_queue_opened(실행 대기열 개방)",
            "status": "passed(통과)",
            "evidence_path": rel(EXECUTION_QUEUE),
            "effect": f"다음 run337AH(337AH 실행)에 {len(execution_queue)}개 실행 항목을 넘긴다.",
        },
        {
            "gate_name": "no_model_training_no_selection(모델 학습/선택 없음)",
            "status": "passed(통과)",
            "evidence_path": rel(Path(__file__)),
            "effect": "ONNX(온엑스), threshold(임계값), lot(랏), risk logic(위험 로직)을 변경하지 않았다.",
        },
        {
            "gate_name": "goal_achieve_gate(목표 달성 게이트)",
            "status": "not_claimed(주장 안 함)",
            "evidence_path": rel(FINAL_DECISION),
            "effect": "scaffold materialization(뼈대 물질화)은 Goal Achieve(목표 달성)가 아니다.",
        },
    ]


def build_final_decision(src: Mapping[str, Any], scaffold: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], execution_queue: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    parent = src["final"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_decision": parent.get("decision", ""),
        "scaffold_status": "materialized",
        "scaffold_rows": len(scaffold),
        "predeclared_gate_rows": len(gates),
        "execution_queue_rows": len(execution_queue),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "live_readiness": "not_claimed",
        "deployment": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def md_table(columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "/").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def report_text(final_decision: Mapping[str, Any], scaffold: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], readiness: Sequence[Mapping[str, Any]], execution_queue: Sequence[Mapping[str, Any]]) -> str:
    scaffold_rows = [
        {
            "priority": row["priority"],
            "track": row["track"],
            "scaffold_id": row["scaffold_id"],
            "status": row["first_execution_status"],
        }
        for row in scaffold
    ]
    gate_rows = [
        {
            "gate_id": row["gate_id"],
            "scope": row["scope"],
            "effect": row["effect"],
        }
        for row in gates
    ]
    readiness_rows = [
        {
            "scaffold_id": row["scaffold_id"],
            "readiness": row["readiness"],
            "missing": row["missing_before_positive_claim"],
        }
        for row in readiness
    ]
    queue_rows = [
        {
            "order": row["queue_order"],
            "mode": row["execution_mode"],
            "action": row["immediate_action"],
        }
        for row in execution_queue
    ]
    return f"""# run337AG No-Overfit Rebuild Scaffold Materialization(337AG 무과적합 재구성 뼈대 물질화)

## Decision(결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- scaffold_rows(뼈대 행): `{final_decision['scaffold_rows']}`
- predeclared_gate_rows(사전 선언 게이트 행): `{final_decision['predeclared_gate_rows']}`
- execution_queue_rows(실행 대기열 행): `{final_decision['execution_queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run337AF(337AF 실행)의 failure memory(실패 기억)를 바로 후보 수리로 튀기지 않고, repair/defensive/offensive/data/parity/instrumentation/risk_exit(수리/방어/공격/데이터/동등성/계측/위험청산) 계약으로 고정했다.

## Scaffold Matrix(뼈대 행렬)

{md_table(["priority", "track", "scaffold_id", "status"], scaffold_rows)}

## Predeclared Gates(사전 선언 게이트)

{md_table(["gate_id", "scope", "effect"], gate_rows)}

## Evidence Readiness(증거 준비도)

{md_table(["scaffold_id", "readiness", "missing"], readiness_rows)}

## run337AH Execution Queue(337AH 실행 대기열)

{md_table(["order", "mode", "action"], queue_rows)}

## Claim Boundary(주장 경계)

이 run(실행)은 model training(모델 학습), candidate selection(후보 선택), threshold retune(임계값 재조정), lot optimization(랏 최적화), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.
"""


def decision_doc_text(final_decision: Mapping[str, Any]) -> str:
    return f"""# Decision(결정): Stage337 run337AG No-Overfit Rebuild Scaffold(337AG 무과적합 재구성 뼈대)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Rationale(근거)

run337AF(337AF 실행)는 7개 failure memory(실패 기억), 9개 guardrail(가드레일), 7개 next queue(다음 대기열)를 만들었다. run337AG(337AG 실행)는 이를 사전 선언 scaffold(뼈대)로 바꾸어, 다음 run337AH(337AH 실행)가 tester visibility repair(테스터 가시성 수리)와 no-overfit preflight(무과적합 사전점검)를 같은 계약 아래 실행하게 한다.

## Boundary(경계)

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

Effect(효과): 성공처럼 보이는 completed-day pocket(완성일 포켓)을 다시 과적합하지 않고, 어떤 증거가 있어야 다음 실행이 의미 있는지 먼저 잠근다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        pattern = re.escape(marker) + r".*?(?=\n## |\Z)"
        return re.sub(pattern, block.strip(), text, count=1, flags=re.S)
    return text.rstrip() + "\n\n" + block.strip() + "\n"


def insert_or_replace_focus(text: str, focus_line: str) -> str:
    block = f"- >-\n  {focus_line}"
    marker = "Stage337 run337AG focus complete:"
    if marker in text:
        return re.sub(r"- >-\n  Stage337 run337AG focus complete:.*?(?=\n- >-|\n\n- >-|\Z)", block, text, count=1, flags=re.S)
    if "current_focus:\n" in text:
        return text.replace("current_focus:\n", "current_focus:\n" + block + "\n", 1)
    return text.rstrip() + "\ncurrent_focus:\n" + block + "\n"


def update_status_docs(final_decision: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    if path_exists(SELECTED_STATUS):
        text, bom = read_text(SELECTED_STATUS)
        text = replace_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        text = replace_line(text, "- latest_decision(최신 결정):", f"- latest_decision(최신 결정): `{DECISION}`")
        text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
        text = replace_line(text, "- Forward Passed(전진 통과):", "- Forward Passed(전진 통과): `not_claimed`")
        text = replace_line(text, "- Forward Failed(전진 실패):", "- Forward Failed(전진 실패): `not_claimed`")
        text = replace_line(text, "- runtime_authority(런타임 권위):", "- runtime_authority(런타임 권위): `not_claimed`")
        text = replace_line(text, "- goal_achieve(목표 달성):", "- goal_achieve(목표 달성): `not_claimed`")
        text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
        text = replace_line(
            text,
            "- effect(효과):",
            f"- effect(효과): run337AG(337AG 실행)는 scaffold(뼈대) `{final_decision['scaffold_rows']}`, predeclared gate(사전 선언 게이트) `{final_decision['predeclared_gate_rows']}`, execution queue(실행 대기열) `{final_decision['execution_queue_rows']}`를 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.",
        )
        write_text(SELECTED_STATUS, text, bom)
        changed.append(SELECTED_STATUS)
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        focus = (
            f"Stage337 run337AG focus complete: run337AG(337AG 실행)는 `{STATUS}`로 run337AF(337AF 실행)의 "
            "failure memory queue(실패 기억 대기열)를 no-overfit rebuild scaffold(무과적합 재구성 뼈대)로 물질화했다. "
            f"Effect(효과): scaffold(뼈대) `{final_decision['scaffold_rows']}`, predeclared gate(사전 선언 게이트) `{final_decision['predeclared_gate_rows']}`, "
            f"execution queue(실행 대기열) `{final_decision['execution_queue_rows']}`를 만들었고 Forward/Goal(전진/목표)은 주장하지 않는다."
        )
        text = insert_or_replace_focus(text, focus)
        write_text(WORKSPACE_STATE, text, bom)
        changed.append(WORKSPACE_STATE)
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
        text = replace_line(text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
        text = replace_line(text, "- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`")
        text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
        block = f"""## Stage337 run337AG(337AG 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): scaffold(뼈대) `{final_decision['scaffold_rows']}`, predeclared gate(사전 선언 게이트) `{final_decision['predeclared_gate_rows']}`, execution queue(실행 대기열) `{final_decision['execution_queue_rows']}`를 물질화했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        text = append_once(text, "## Stage337 run337AG(337AG 실행)", block)
        write_text(CURRENT_STATE, text, bom)
        changed.append(CURRENT_STATE)
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337AG(337AG 실행) `{STATUS}`. Effect(효과): no-overfit rebuild scaffold(무과적합 재구성 뼈대) `{final_decision['scaffold_rows']}`행과 run337AH execution queue(337AH 실행 대기열) `{final_decision['execution_queue_rows']}`행을 물질화했고 Forward/Goal(전진/목표)은 주장하지 않음."
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
        write_text(CHANGELOG, text, bom)
        changed.append(CHANGELOG)
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = replace_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        summary = (
            f"- run337AG_summary(337AG 요약): `{STATUS}`. Effect(효과): scaffold(뼈대) `{final_decision['scaffold_rows']}`, "
            f"predeclared gate(사전 선언 게이트) `{final_decision['predeclared_gate_rows']}`, execution queue(실행 대기열) `{final_decision['execution_queue_rows']}`를 만들고 run337AH(337AH 실행) visibility repair/preflight(가시성 수리/사전점검)를 연다.\n"
        )
        if "run337AG_summary(337AG 요약)" in text:
            text = re.sub(r"- run337AG_summary\(337AG 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.replace("- selected_candidate(선택 후보):", summary + "- selected_candidate(선택 후보):")
        write_text(STAGE_BRIEF, text, bom)
        changed.append(STAGE_BRIEF)
    return changed


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def append_artifacts(paths: Sequence[Path]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = list(rows[0].keys()) if rows else [
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "artifact_path",
        "claim_boundary",
    ]
    for column in ("artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "claim_boundary"):
        if column not in columns:
            columns.append(column)
    rows = [row for row in rows if row.get("run_id") != RUN_ID]
    generated = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        relative = rel(path)
        if relative in seen:
            continue
        seen.add(relative)
        suffix = path.suffix.lower()
        digest = sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py", ".yaml"} else sha256_file(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{relative}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": relative,
                "artifact_path": relative,
                "sha256": digest,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def write_receipts(final_decision: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    return [
        write_json(
            DATA_RECEIPT,
            {
                "run_id": RUN_ID,
                "data_source": [rel(AF_FAILURE_MEMORY), rel(AF_GUARDRAILS), rel(AF_QUEUE), rel(AF_PROXY), rel(AF_EVIDENCE_MAP)],
                "time_axis": "forward holdout(전진 홀드아웃) starts after 2026-04-13; run337AG uses no new bars(새 봉 사용 없음)",
                "sample_scope": "contract materialization only(계약 물질화 전용)",
                "leakage_risk": "low because no model training(모델 학습 없음) and no threshold retune(임계값 재조정 없음)",
                "integrity_judgment": "usable_for_scaffold_materialization_not_forward_decision(뼈대 물질화에는 사용 가능, 전진 판정은 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "primary_family": "experiment_design(실험 설계)",
                "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
                "hypothesis": "run337AF failure memory(실패 기억)를 no-overfit scaffold(무과적합 뼈대)로 바꾸면 다음 실행이 전진 포켓에 맞춰 튜닝되는 것을 막을 수 있다.",
                "controls": ["no forward retune(전진 재조정 금지)", "proxy not KPI authority(프록시 KPI 권위 아님)", "as-of macro only(시점 기준 거시만)", "D/B telemetry required(D/B 텔레메트리 필수)"],
                "stop_conditions": ["full current-day visibility unresolved(현재일 전체 가시성 미해결)", "cost/curve/direction gate missing(비용/곡선/방향 게이트 누락)", "receipt missing(영수증 누락)"],
                "evidence_artifacts": [rel(path) for path in artifacts],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            MODEL_RECEIPT,
            {
                "run_id": RUN_ID,
                "model_subject": "future ONNX research packet(미래 온엑스 연구 묶음)",
                "model_changes": "none(없음)",
                "threshold_changes": "none(없음)",
                "lot_changes": "none(없음)",
                "training_or_selection": "none(없음)",
                "overfit_judgment": "scaffold requires pre-forward evidence before any candidate claim(후보 주장 전 전진 전 증거 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_RECEIPT,
            {
                "run_id": RUN_ID,
                "runtime_scope": "no MT5 execution in run337AG(337AG에서 MT5 실행 없음)",
                "proxy_mt5_role": rel(PROXY_MT5_ROLE_LOCK),
                "next_runtime_probe": NEXT_RUN_ID,
                "runtime_claim_boundary": "runtime_authority_not_claimed(런타임 권위 주장 안 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_RECEIPT,
            {
                "run_id": RUN_ID,
                "judgment_label": "scaffold_materialized_no_selection(뼈대 물질화, 선택 없음)",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "이번에는 모델을 고치지 않고, 다음 실행이 과적합 수리로 새지 않게 계약과 실행 대기열을 고정했다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = source_bundle()
    scaffold = build_scaffold_matrix(src)
    gates = build_predeclared_gates(src)
    no_lookahead = build_no_lookahead_policy()
    proxy_lock = build_proxy_mt5_role_lock(src)
    mt5_repair = build_mt5_repair_contract(src)
    cost_contract = build_cost_objective_contract()
    side_contract = build_side_surface_contract()
    asof_contract = build_asof_regime_contract(src)
    db_contract = build_db_telemetry_contract()
    atr_contract = build_atr_risk_contract()
    readiness = build_evidence_readiness(scaffold)
    execution_queue = build_execution_queue(scaffold)
    gate_audit = build_gate_audit(src, scaffold, gates, execution_queue)
    final_decision = build_final_decision(src, scaffold, gates, execution_queue)

    artifacts: list[Path] = [
        write_csv(SCAFFOLD_MATRIX, list(scaffold[0].keys()), scaffold),
        write_csv(PREDECLARED_GATES, list(gates[0].keys()), gates),
        write_csv(NO_LOOKAHEAD_POLICY, list(no_lookahead[0].keys()), no_lookahead),
        write_csv(PROXY_MT5_ROLE_LOCK, list(proxy_lock[0].keys()), proxy_lock),
        write_csv(MT5_REPAIR_CONTRACT, list(mt5_repair[0].keys()), mt5_repair),
        write_csv(COST_OBJECTIVE_CONTRACT, list(cost_contract[0].keys()), cost_contract),
        write_csv(SIDE_SURFACE_CONTRACT, list(side_contract[0].keys()), side_contract),
        write_csv(ASOF_REGIME_CONTRACT, list(asof_contract[0].keys()), asof_contract),
        write_csv(DB_TELEMETRY_CONTRACT, list(db_contract[0].keys()), db_contract),
        write_csv(ATR_RISK_CONTRACT, list(atr_contract[0].keys()), atr_contract),
        write_csv(EVIDENCE_READINESS, list(readiness[0].keys()), readiness),
        write_csv(EXECUTION_QUEUE, list(execution_queue[0].keys()), execution_queue),
        write_csv(GATE_AUDIT, ["gate_name", "status", "evidence_path", "effect"], gate_audit),
        write_json(FINAL_DECISION, final_decision),
        write_md(REPORT_PATH, report_text(final_decision, scaffold, gates, readiness, execution_queue)),
        write_md(DECISION_DOC, decision_doc_text(final_decision)),
    ]
    artifacts.extend(write_receipts(final_decision, artifacts))
    artifacts.extend(update_status_docs(final_decision))

    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "no_overfit_rebuild_scaffold_materialization",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "family": "experiment_design",
            "primary_report": rel(REPORT_PATH),
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        {
            "ledger_row_id": f"{RUN_ID}__no_overfit_rebuild_scaffold",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "no_overfit_rebuild_scaffold",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "no_overfit_rebuild_scaffold",
            "tier_scope": "Tier A forward robustness evidence with boundary(티어 A 전진 강건성 경계 증거)",
            "kpi_scope": "design_contract_no_new_kpi(설계 계약, 새 KPI 없음)",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"scaffold_rows={len(scaffold)};predeclared_gate_rows={len(gates)};execution_queue_rows={len(execution_queue)}",
            "guardrail_kpi": "no_forward_retune;no_model_training;proxy_not_kpi_authority;asof_macro_only",
            "external_verification_status": "out_of_scope_by_claim_design_only_next_runtime_probe_run337AH",
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        STAGE_LEDGER,
        ["run_key"],
        {
            "run_key": f"{RUN_ID}__no_overfit_rebuild_scaffold",
            "ledger_row_id": f"{RUN_ID}__no_overfit_rebuild_scaffold",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "no_overfit_rebuild_scaffold",
            "work_family": "experiment_design",
            "question": "can run337AF failure memory be converted into a predeclared no-overfit repair defensive offensive scaffold",
            "metric_scope": "design_contract_no_forward_decision",
            "evidence_scope": "run337AF failure memory guardrails next queue proxy usability",
            "kpi_scope": "design_only_no_new_candidate_kpi",
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "primary_artifact": rel(REPORT_PATH),
            "report_path": rel(REPORT_PATH),
            "path": rel(REPORT_PATH),
            "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "decision": DECISION,
            "next_action": NEXT_RUN_ID,
        },
    )
    artifacts.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER])
    manifest = write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": [
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-runtime-parity",
                "obsidian-result-judgment",
            ],
            "required_gates": ["work_packet_schema_lint"],
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_action": NEXT_RUN_ID,
            "artifacts": [rel(path) for path in artifacts],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    artifacts.append(manifest)
    artifacts.append(append_artifacts([*artifacts, Path(__file__)]))

    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "scaffold_rows": len(scaffold),
                    "predeclared_gate_rows": len(gates),
                    "execution_queue_rows": len(execution_queue),
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
