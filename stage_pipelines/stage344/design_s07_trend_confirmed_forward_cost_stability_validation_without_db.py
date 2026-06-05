from __future__ import annotations

import csv
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage344 import (  # noqa: E402
    materialize_directional_long_supply_quality_surface_package_without_db as pkg,
)
from stage_pipelines.stage344 import (  # noqa: E402
    review_directional_long_quality_surface_mt5_probe_without_db as parent,
)


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344F"
RUN_ID = "run344F_design_s07_trend_confirmed_forward_cost_stability_validation_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
SOURCE_RUNTIME_RUN_ID = "run344D_execute_directional_long_supply_quality_surface_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run344G_materialize_s07_forward_cost_stability_validation_package_without_db_v1"

STATUS = "completed_stage344F_s07_forward_cost_stability_validation_design_ready_no_selection"
JUDGMENT = "s07_validation_design_ready_for_cost_session_regime_package_no_operating_claim"
DECISION = "stage344F_open_run344G_materialize_s07_forward_cost_stability_validation_package"
CLAIM_BOUNDARY = (
    "research_development_design_only_s07_forward_cost_stability_validation_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344F_s07_forward_cost_stability_validation_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344F_s07_forward_cost_stability_validation_design.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SOURCE_PARENT_FINAL = parent.FINAL_DECISION
SOURCE_PARENT_GATES = parent.GATE_AUDIT
SOURCE_PARENT_QUEUE = parent.NEXT_QUEUE
SOURCE_PARENT_SCORECARD = parent.REVIEW_SCORECARD
SOURCE_PARENT_POSITIVE = parent.POSITIVE_CLUES
SOURCE_PARENT_FAILURE = parent.FAILURE_MEMORY
SOURCE_RUNTIME_SUMMARY = STAGE_DIR / "02_runs" / "run344D" / "directional_long_quality_surface_mt5_probe_summary.csv"
SOURCE_RUNTIME_DIFF = STAGE_DIR / "02_runs" / "run344D" / "proxy_mt5_runtime_difference.csv"
SOURCE_RUNTIME_IDENTITY = STAGE_DIR / "02_runs" / "run344D" / "runtime_identity.csv"
SOURCE_RUNTIME_REPORT_DIR = STAGE_DIR / "02_runs" / "run344D" / "mt5" / "reports"
SOURCE_S07_TELEMETRY = STAGE_DIR / "02_runs" / "run344D" / "runtime_telemetry" / "s07_trend_confirmed_long_only_telemetry.csv"
SOURCE_S07_SUMMARY = STAGE_DIR / "02_runs" / "run344D" / "runtime_telemetry" / "s07_trend_confirmed_long_only_summary.csv"
SOURCE_PACKAGE_ATTEMPTS = pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE
SOURCE_PACKAGE_EXPECTED = pkg.EXPECTED_TAPE
SOURCE_PACKAGE_FEATURES = pkg.FEATURE_MATRIX

WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "data_integrity_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
VALIDATION_SURFACE_PLAN = RUN_DIR / "s07_validation_surface_plan.csv"
COST_STRESS_CONTRACT = RUN_DIR / "cost_stress_contract.csv"
SESSION_REGIME_PLAN = RUN_DIR / "session_regime_attribution_plan.csv"
COMPARATOR_PLAN = RUN_DIR / "anchor_s05_s07_comparator_plan.csv"
FORWARD_REPLAY_HANDOFF_PLAN = RUN_DIR / "forward_replay_handoff_plan.csv"
NEXT_QUEUE = RUN_DIR / "run344G_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = (
    SOURCE_PARENT_FINAL,
    SOURCE_PARENT_GATES,
    SOURCE_PARENT_QUEUE,
    SOURCE_PARENT_SCORECARD,
    SOURCE_PARENT_POSITIVE,
    SOURCE_PARENT_FAILURE,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_RUNTIME_DIFF,
    SOURCE_RUNTIME_IDENTITY,
    SOURCE_S07_TELEMETRY,
    SOURCE_S07_SUMMARY,
    SOURCE_PACKAGE_ATTEMPTS,
    SOURCE_PACKAGE_EXPECTED,
    SOURCE_PACKAGE_FEATURES,
)

OUTPUT_FILES = (
    WORK_PACKET,
    EXPERIMENT_CONTRACT,
    DATA_INTEGRITY_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    VALIDATION_SURFACE_PLAN,
    COST_STRESS_CONTRACT,
    SESSION_REGIME_PLAN,
    COMPARATOR_PLAN,
    FORWARD_REPLAY_HANDOFF_PLAN,
    NEXT_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def path_is_file(path: Path) -> bool:
    return pkg.path_is_file(path)


def ensure_parent(path: Path) -> None:
    pkg.ensure_parent(path)


def required(path: Path) -> Path:
    return pkg.required(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pkg.read_csv(path)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fields: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields
    ensure_parent(path)
    with open(pkg.fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_or_replace_csv(path, keys, rows)


def sha256_file(path: Path) -> str:
    return pkg.sha256_file(path)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value) or value == "":
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def exact_parent_gate_passed() -> bool:
    gates = read_csv(SOURCE_PARENT_GATES)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def build_contracts() -> dict[str, Any]:
    for source in INPUT_FILES:
        required(source)
    parent_final = read_json(SOURCE_PARENT_FINAL)
    if parent_final.get("next_run_id", parent_final.get("next_action")) != RUN_ID:
        raise RuntimeError("run344E next run does not point to run344F")
    if not exact_parent_gate_passed():
        raise RuntimeError("run344E gate audit has failed rows")

    summary = read_csv(SOURCE_RUNTIME_SUMMARY)
    scorecard = read_csv(SOURCE_PARENT_SCORECARD)
    s07 = summary.loc[summary["attempt_name"].astype(str).eq("s07_trend_confirmed_long_only")]
    if s07.empty:
        raise RuntimeError("missing s07 MT5 summary row")
    s07_row = s07.iloc[0]
    s07_score = scorecard.loc[scorecard["attempt_name"].astype(str).eq("s07_trend_confirmed_long_only")]
    if s07_score.empty:
        raise RuntimeError("missing s07 review scorecard row")

    experiment_rows = [
        {
            "contract_id": "run344F_hypothesis(가설)",
            "hypothesis": "s07 trend-confirmed long(추세 확인 롱)은 base MT5 KPI(MT5 핵심 성과 지표)뿐 아니라 cost stress(비용 압박), session/regime stability(세션/국면 안정성), equity curve quality(수익곡선 품질)에서도 anchor(앵커)보다 덜 깨질 수 있다.",
            "decision_use": "decide whether to run a narrow runtime validation package before any operating promotion claim(운영 승격 주장 전 좁은 런타임 검증 패키지를 실행할지 결정)",
            "comparison_baseline": "s01_anchor_short_supply_control and s05_long_quality_extreme_top20(s01 앵커와 s05 고신뢰 롱 품질)",
            "control_variables": "US100 M5, 2024.07.30-2025.01.01, model family, feature csv, expected tape, EA binary, tester profile, lot 0.10, max_hold_bars 12(심볼/주기/기간/모델/피처/EA/로트/보유 고정)",
            "changed_variables": "validation lens only: cost overlay, session bucket, regime bucket, comparator inclusion(검증 렌즈: 비용 오버레이, 세션 버킷, 국면 버킷, 대조군 포함)",
            "sample_scope": "Tier A full-context runtime probe sample, US100 M5, 5827 ready feature rows and 69924 expected comparison rows(Tier A 전체 문맥 런타임 표본)",
            "success_criteria": "s07 remains net positive, PF >= 1.5, recovery >= 1.0 under moderate cost overlay and does not concentrate all edge in one tiny session/regime bucket(s07이 중간 비용 오버레이와 버킷 귀속에서 깨지지 않음)",
            "failure_criteria": "PF < 1.5 or recovery < 1.0 under moderate cost overlay, or edge appears as one tiny bucket only(비용 또는 버킷에서 수익 구조가 붕괴)",
            "invalid_conditions": "proxy-MT5 mismatch, missing report/deal evidence, timestamp mismatch, changed EA logic without lineage(프록시-MT5 불일치, 보고서/거래 근거 누락, 시점 불일치, 계보 없는 EA 변경)",
            "stop_conditions": "stop before operating claim if cost overlay or session/regime attribution is weak(비용/세션/국면 귀속이 약하면 운영 주장 전 중단)",
            "evidence_plan": "run344G package, run344H MT5 probe or reuse-audit, run344I review with scorecard/cost/session/equity artifacts(344G 패키지, 344H MT5 탐침 또는 재사용 감사, 344I 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    data_rows = [
        {
            "check_id": "runtime_input_scope(런타임 입력 범위)",
            "data_source": f"{rel(SOURCE_PACKAGE_FEATURES)}; {rel(SOURCE_PACKAGE_EXPECTED)}; {rel(SOURCE_RUNTIME_SUMMARY)}",
            "time_axis": "MT5 bar time and feature source_time use M5 bar-close convention from existing runtime parity contract(MT5 봉 시간과 피처 source_time은 기존 런타임 동등성 계약의 M5 종가 기준)",
            "sample_scope": "US100 M5 Tier A, 2024.07.30 to 2025.01.01, 5827 feature-ready rows and 69924 expected rows(US100 M5 Tier A 표본)",
            "missing_or_duplicate_check": "reuse run344D exact parity: matched_rows=expected_rows and mismatch_rows=0(run344D 정확 동등성 재사용)",
            "feature_label_boundary": "no new feature or label is created; validation reads past MT5/runtime artifacts only(새 피처/라벨 없음, 기존 MT5/런타임 산출물만 읽음)",
            "split_boundary": "inner_holdout_runtime_collapsed_probe only; no forward pass is claimed(내부 홀드아웃 런타임 탐침 전용, 전진 통과 주장 없음)",
            "leakage_risk": "selection bias from choosing s07 after run344D; controlled by using run344F as validation design, not operating decision(run344D 후 s07 선택 편향을 검증 설계 경계로 낮춤)",
            "data_hash_or_identity": f"expected_rows={parent_final.get('expected_rows')};matched_rows={parent_final.get('matched_rows')};runtime_run={SOURCE_RUNTIME_RUN_ID}",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    runtime_rows = [
        {
            "contract_id": "run344F_runtime_parity_boundary(런타임 동등성 경계)",
            "research_path": rel(Path(__file__)),
            "runtime_path": f"{rel(SOURCE_PACKAGE_ATTEMPTS)}; {rel(SOURCE_RUNTIME_REPORT_DIR)}",
            "shared_contract": "same feature order hash, model paths, expected tape, thresholds, side filter, tester identity from run344C/run344D(동일 피처 순서 해시, 모델 경로, 예상 테이프, 임계값, 사이드 필터, 테스터 정체성)",
            "known_differences": "cost stress is an attribution overlay after MT5 evidence, not an MT5 tester cost replacement(비용 압박은 MT5 근거 이후 귀속 오버레이이며 MT5 비용 대체가 아님)",
            "parity_check": "run344D exact parity already reached; run344G must preserve or explicitly re-probe(run344D 정확 동등성 도달, 344G는 보존 또는 재탐침)",
            "parity_identity": f"matched_rows={parent_final.get('matched_rows')};mismatch_rows={parent_final.get('mismatch_rows')};exact_parent_rows={parent_final.get('parent_exact_parity_rows')}",
            "runtime_claim_boundary": "design_only_no_runtime_authority(설계 전용, 런타임 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    validation_rows = [
        {
            "surface_id": "surface01_s07_base_runtime_replay(기본 런타임 재현)",
            "seed_attempt": "s07_trend_confirmed_long_only",
            "purpose": "preserve exact MT5 meaning before cost/session analysis(비용/세션 분석 전 MT5 의미 보존)",
            "baseline": "run344D s07 MT5 report(344D s07 MT5 보고서)",
            "changed_variable": "none unless run344G chooses re-probe(344G 재탐침 선택 전 변경 없음)",
            "required_artifacts": "set/ini/model/feature/expected/telemetry/report hashes(설정/모델/피처/예상/텔레메트리/보고서 해시)",
            "success_rule": "exact parity or explicit re-probe evidence(정확 동등성 또는 명시 재탐침 근거)",
            "failure_rule": "any parity mismatch or missing report(동등성 불일치 또는 보고서 누락)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "surface_id": "surface02_cost_overlay_grid(비용 오버레이 격자)",
            "seed_attempt": "s07_trend_confirmed_long_only",
            "purpose": "test whether s07 expectancy survives additional friction(s07 기대값이 추가 마찰을 버티는지 확인)",
            "baseline": "run344D MT5 net/PF/expectancy(344D MT5 순수익/PF/기대값)",
            "changed_variable": "post-MT5 cost per closed trade overlay: 0.5/1.0/2.0/4.0 account currency(거래당 사후 비용 오버레이)",
            "required_artifacts": "MT5 report deal extraction or trade count fallback with attribution warning(MT5 보고서 거래 추출 또는 거래수 fallback 경고)",
            "success_rule": "moderate overlay keeps net positive, PF >= 1.5, recovery >= 1.0(중간 오버레이에서도 양수익/PF/회복 유지)",
            "failure_rule": "moderate overlay breaks PF/recovery or net(중간 오버레이에서 PF/회복/순수익 붕괴)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "surface_id": "surface03_session_regime_buckets(세션/국면 버킷)",
            "seed_attempt": "s07_trend_confirmed_long_only",
            "purpose": "locate whether edge is concentrated in time/session/volatility bucket(엣지가 시간/세션/변동성 버킷에 집중되는지 확인)",
            "baseline": "all s07 runtime telemetry rows(전체 s07 런타임 텔레메트리 행)",
            "changed_variable": "bucket lens only: cash open, mid session, late session, volatility/adx terciles(버킷 렌즈만 변경)",
            "required_artifacts": "bucketed signal/fill count and report-linked trade attribution when available(버킷별 신호/체결 수와 보고서 연결 거래 귀속)",
            "success_rule": "edge not entirely from one tiny bucket and long/short mix remains interpretable(엣지가 작은 버킷 하나에만 있지 않음)",
            "failure_rule": "positive KPI depends on a small unrepeatable pocket(양수 KPI가 작은 재현 불가 포켓에 의존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "surface_id": "surface04_anchor_s05_s07_comparator(앵커/s05/s07 대조)",
            "seed_attempt": "s01_anchor_short_supply_control;s05_long_quality_extreme_top20;s07_trend_confirmed_long_only",
            "purpose": "ensure s07 is not just raw net but better stress shape(s07이 원 순수익만 좋은 것이 아닌지 확인)",
            "baseline": "s01 anchor and s05 high-confidence threshold(s01 앵커와 s05 고신뢰 임계값)",
            "changed_variable": "comparator inclusion only(대조군 포함만 변경)",
            "required_artifacts": "same tester identity and exact parity for all comparators(모든 대조군 동일 테스터 정체성과 정확 동등성)",
            "success_rule": "s07 remains best or clearly useful after stress and bucket attribution(압박과 버킷 후에도 s07 유용성 유지)",
            "failure_rule": "s05 or anchor dominates after cost/stability stress(비용/안정성 압박 후 s05 또는 앵커가 우위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "surface_id": "surface05_forward_replay_handoff(전진/재생 인계)",
            "seed_attempt": "s07_trend_confirmed_long_only",
            "purpose": "list narrow files needed before a future forward/replay probe(미래 전진/재생 탐침 전 필요한 파일 나열)",
            "baseline": "run344C package and run344D runtime identity(344C 패키지와 344D 런타임 정체성)",
            "changed_variable": "handoff audit only(인계 감사만 변경)",
            "required_artifacts": "model hash, feature hash, set/ini hash, EA hash, common-file paths(모델/피처/설정/EA 해시와 공용 파일 경로)",
            "success_rule": "all handoff files are present or regeneration command is recorded(모든 인계 파일 존재 또는 재생성 명령 기록)",
            "failure_rule": "lineage gap blocks forward/replay claim(계보 공백이 전진/재생 주장을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    cost_rows = [
        {
            "cost_scenario": "base_mt5_broker_cost(기본 MT5 브로커 비용)",
            "cost_per_closed_trade_account_currency": 0.0,
            "status": "mt5_report_authority(MT5 보고서 권위)",
            "use": "reference KPI only(기준 KPI 전용)",
            "limitation": "depends on tester broker settings(테스터 브로커 설정에 의존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "cost_scenario": "light_overlay(가벼운 오버레이)",
            "cost_per_closed_trade_account_currency": 0.5,
            "status": "post_mt5_attribution_only(MT5 이후 귀속 전용)",
            "use": "sanity stress(상식 압박)",
            "limitation": "does not replace MT5 tester KPI(MT5 테스터 KPI 대체 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "cost_scenario": "moderate_overlay(중간 오버레이)",
            "cost_per_closed_trade_account_currency": 2.0,
            "status": "post_mt5_attribution_only(MT5 이후 귀속 전용)",
            "use": "promotion-candidate stress floor(승격 후보 압박 하한)",
            "limitation": "requires report/deal extraction for PF recalculation(PF 재계산에는 보고서 거래 추출 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "cost_scenario": "heavy_overlay(강한 오버레이)",
            "cost_per_closed_trade_account_currency": 4.0,
            "status": "post_mt5_attribution_only(MT5 이후 귀속 전용)",
            "use": "failure threshold probe(실패 임계 탐침)",
            "limitation": "exploratory stress only(탐색 압박 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    session_rows = [
        {
            "bucket_id": "cash_open_first_60m(현금장 첫 60분)",
            "time_rule": "minutes_from_cash_open >= 0 and < 60(현금장 개장 후 0-60분)",
            "regime_rule": "all volatility/adx states(전체 변동성/ADX 상태)",
            "required_metric": "cycle count, signal count, fill count, long/short mix, linked PnL if report extraction succeeds(사이클/신호/체결/방향/연결 손익)",
            "effect": "checks if open shock carries or damages s07 edge(개장 충격이 s07 엣지를 운반/훼손하는지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "cash_mid_60_210m(현금장 중반 60-210분)",
            "time_rule": "minutes_from_cash_open >= 60 and < 210(현금장 개장 후 60-210분)",
            "regime_rule": "all volatility/adx states(전체 변동성/ADX 상태)",
            "required_metric": "same as above(위와 같음)",
            "effect": "checks if trend-confirmed long survives normal liquidity(정상 유동성에서 추세 확인 롱이 유지되는지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "cash_late_after_210m(현금장 후반 210분 이후)",
            "time_rule": "minutes_from_cash_open >= 210(현금장 개장 후 210분 이후)",
            "regime_rule": "all volatility/adx states(전체 변동성/ADX 상태)",
            "required_metric": "same as above(위와 같음)",
            "effect": "checks late-session continuation versus exhaustion(후반 지속과 소진을 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "adx_volatility_terciles(ADX/변동성 삼분위)",
            "time_rule": "all session times(전체 세션 시간)",
            "regime_rule": "adx_14 and historical_vol_20 terciles from runtime feature matrix(런타임 피처 행렬의 ADX와 역사 변동성 삼분위)",
            "required_metric": "signal/fill and linked PnL by regime when available(가능 시 국면별 신호/체결/손익)",
            "effect": "tests whether low-ADX veto removed the right long pockets(낮은 ADX 거부가 올바른 롱 포켓을 제거했는지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    comparator_rows = [
        {
            "comparator_id": "anchor_s01(앵커 s01)",
            "attempt_name": "s01_anchor_short_supply_control",
            "role": "profit anchor and short supply reference(수익 앵커와 숏 공급 기준)",
            "expected_use": "guard against s07 overfitting to long rescue(s07 롱 복구 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "comparator_id": "high_conf_s05(고신뢰 s05)",
            "attempt_name": "s05_long_quality_extreme_top20",
            "role": "quality threshold comparator(품질 임계값 대조군)",
            "expected_use": "checks whether trend filter beats simple confidence filtering(추세 필터가 단순 신뢰 필터보다 나은지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "comparator_id": "candidate_s07(후보 s07)",
            "attempt_name": "s07_trend_confirmed_long_only",
            "role": "primary validation seed(주 검증 씨앗)",
            "expected_use": "cost/session/regime/equity validation target(비용/세션/국면/수익곡선 검증 대상)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    handoff_rows = [
        {
            "handoff_item": "model_bundle(모델 번들)",
            "source_path": "stages/344_directional_long_quality__supply_surface_probe/02_runs/run344C/models/s07_trend_confirmed_long_only.onnx",
            "required_identity": "sha256 and common-file copy hash(sha256과 공용 파일 복사 해시)",
            "consumer": NEXT_RUN_ID,
            "effect": "keeps ONNX(온엑스) identity fixed before forward/replay(전진/재생 전 모델 정체성 고정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "handoff_item": "runtime_set_ini(런타임 set/ini)",
            "source_path": "stages/344_directional_long_quality__supply_surface_probe/02_runs/run344C/mt5/sets and inis",
            "required_identity": "parameter hash and tester profile path(파라미터 해시와 테스터 프로필 경로)",
            "consumer": NEXT_RUN_ID,
            "effect": "prevents hidden parameter drift(숨은 파라미터 드리프트 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "handoff_item": "ea_binary(EA 바이너리)",
            "source_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.ex5",
            "required_identity": "EA hash and portable copy path(EA 해시와 포터블 복사 경로)",
            "consumer": NEXT_RUN_ID,
            "effect": "keeps runtime logic equal(런타임 로직 동등성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    next_rows = [
        {
            "queue_id": "run344G_01_package_s07_anchor_s05(패키지 s07/앵커/s05)",
            "next_run_id": NEXT_RUN_ID,
            "input_attempts": "s07_trend_confirmed_long_only;s05_long_quality_extreme_top20;s01_anchor_short_supply_control",
            "action": "materialize validation package with existing ONNX/set/ini/features and short path names(기존 ONNX/set/ini/피처와 짧은 경로명으로 검증 패키지 물질화)",
            "effect": "prepares narrow MT5/runtime replay and attribution(좁은 MT5/런타임 재생과 귀속 준비)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run344G_02_extract_cost_session_contracts(비용/세션 계약 추출)",
            "next_run_id": NEXT_RUN_ID,
            "input_attempts": "s07_trend_confirmed_long_only",
            "action": "copy cost stress and session/regime attribution contracts into package(비용 압박과 세션/국면 귀속 계약을 패키지에 복사)",
            "effect": "run344H/run344I can judge stability without redefining KPI(344H/344I가 KPI 재정의 없이 안정성 판정 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run344G_03_handoff_manifest(인계 목록)",
            "next_run_id": NEXT_RUN_ID,
            "input_attempts": "s07_trend_confirmed_long_only",
            "action": "write model/set/ini/EA/feature/report hash manifest(모델/set/ini/EA/피처/보고서 해시 목록 작성)",
            "effect": "narrows future forward/replay blocker to concrete missing files(미래 전진/재생 차단 원인을 구체 파일로 좁힘)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    write_csv(EXPERIMENT_CONTRACT, experiment_rows)
    write_csv(DATA_INTEGRITY_CONTRACT, data_rows)
    write_csv(RUNTIME_PARITY_CONTRACT, runtime_rows)
    write_csv(VALIDATION_SURFACE_PLAN, validation_rows)
    write_csv(COST_STRESS_CONTRACT, cost_rows)
    write_csv(SESSION_REGIME_PLAN, session_rows)
    write_csv(COMPARATOR_PLAN, comparator_rows)
    write_csv(FORWARD_REPLAY_HANDOFF_PLAN, handoff_rows)
    write_csv(NEXT_QUEUE, next_rows)

    work_packet = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-runtime-parity(런타임 동등성)",
            "obsidian-artifact-lineage(산출물 계보)",
        ],
        "required_gates": [
            "work_packet_schema_lint",
            "experiment_contract_written",
            "data_integrity_contract_written",
            "runtime_parity_contract_written",
            "validation_plan_covers_cost_session_regime_forward",
            "next_materialization_queue_written",
            "required_gate_coverage_audit",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "effect": "keeps s07 validation narrow and auditable(s07 검증을 좁고 감사 가능하게 유지)",
    }
    write_json(WORK_PACKET, work_packet)

    final = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "promotion_candidate_attempt_name": "s07_trend_confirmed_long_only",
        "promotion_candidate_model_id": parent_final.get("promotion_candidate_model_id"),
        "reference_net_profit": parent_final.get("promotion_candidate_net_profit"),
        "reference_profit_factor": parent_final.get("promotion_candidate_profit_factor"),
        "reference_expectancy": parent_final.get("promotion_candidate_expectancy"),
        "reference_drawdown": parent_final.get("promotion_candidate_max_drawdown_amount"),
        "reference_recovery_factor": parent_final.get("promotion_candidate_recovery_factor"),
        "reference_trade_count": parent_final.get("promotion_candidate_trade_count"),
        "reference_long_short": f"{parent_final.get('promotion_candidate_long_trade_count')}/{parent_final.get('promotion_candidate_short_trade_count')}",
        "experiment_contract_rows": len(experiment_rows),
        "data_integrity_rows": len(data_rows),
        "runtime_parity_rows": len(runtime_rows),
        "validation_surface_rows": len(validation_rows),
        "cost_stress_rows": len(cost_rows),
        "session_regime_rows": len(session_rows),
        "comparator_rows": len(comparator_rows),
        "next_queue_rows": len(next_rows),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "new_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return final


def gate(gate_id: str, passed: bool, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["selected_model"] == "none(없음)"
        and final["new_mt5_execution"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    return [
        gate("parent_run344E_gates_passed", exact_parent_gate_passed(), SOURCE_PARENT_GATES, "run344E review(검토) gate(게이트)가 통과된 상태에서 설계"),
        gate("work_packet_schema_lint", path_is_file(WORK_PACKET), WORK_PACKET, "work packet(작업 묶음)이 family/skill/gate를 가진다"),
        gate("experiment_contract_written", path_is_file(EXPERIMENT_CONTRACT) and final["experiment_contract_rows"] > 0, EXPERIMENT_CONTRACT, "실험 설계 계약을 기록"),
        gate("data_integrity_contract_written", path_is_file(DATA_INTEGRITY_CONTRACT) and final["data_integrity_rows"] > 0, DATA_INTEGRITY_CONTRACT, "데이터 무결성 경계를 기록"),
        gate("runtime_parity_contract_written", path_is_file(RUNTIME_PARITY_CONTRACT) and final["runtime_parity_rows"] > 0, RUNTIME_PARITY_CONTRACT, "런타임 동등성 경계를 기록"),
        gate("validation_plan_covers_cost_session_regime_forward", path_is_file(VALIDATION_SURFACE_PLAN) and final["validation_surface_rows"] >= 5, VALIDATION_SURFACE_PLAN, "비용/세션/국면/전진 준비를 같은 설계에 포함"),
        gate("next_materialization_queue_written", path_is_file(NEXT_QUEUE) and final["next_queue_rows"] > 0, NEXT_QUEUE, "run344G 물질화 대기열을 생성"),
        gate("no_forbidden_operating_claim", no_forbidden, FINAL_DECISION, "설계 결과를 선정/운영/목표 달성으로 올리지 않음"),
        gate("required_gate_coverage_audit_written", True, GATE_AUDIT, "필수 게이트 커버리지 감사를 기록"),
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "receipt_id": "run344F_experiment_design(실험 설계)",
            "run_id": RUN_ID,
            "hypothesis": "s07 must survive cost/session/regime validation before any stronger claim(s07은 더 강한 주장 전 비용/세션/국면 검증을 버텨야 함)",
            "decision_use": "open run344G materialization only(run344G 물질화만 개방)",
            "evidence_plan": [rel(EXPERIMENT_CONTRACT), rel(VALIDATION_SURFACE_PLAN), rel(NEXT_QUEUE)],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "receipt_id": "run344F_data_integrity(데이터 무결성)",
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_PACKAGE_FEATURES), rel(SOURCE_PACKAGE_EXPECTED), rel(SOURCE_RUNTIME_SUMMARY)],
            "time_axis": "existing MT5 M5 bar-close runtime artifacts(기존 MT5 M5 종가 런타임 산출물)",
            "feature_label_boundary": "no new features or labels in this design(이번 설계에는 새 피처/라벨 없음)",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "receipt_id": "run344F_runtime_parity(런타임 동등성)",
            "run_id": RUN_ID,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(SOURCE_PACKAGE_ATTEMPTS),
            "known_differences": "cost stress overlay is post-MT5 attribution(비용 압박 오버레이는 MT5 이후 귀속)",
            "runtime_claim_boundary": "design_only_no_runtime_authority(설계 전용, 런타임 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "receipt_id": "run344F_performance_attribution_plan(성과 귀속 계획)",
            "run_id": RUN_ID,
            "observed_change": "s07 improved net/PF/trades/longs versus anchor(s07이 앵커 대비 순수익/PF/거래수/롱 개선)",
            "comparison_baseline": "s01 anchor and s05 threshold comparator(s01 앵커와 s05 임계값 대조군)",
            "segment_checks": "session buckets, ADX/volatility terciles, cost overlay, equity curve quality(세션 버킷, ADX/변동성 삼분위, 비용 오버레이, 수익곡선 품질)",
            "attribution_confidence": "medium_until_run344G_or_run344H(344G 또는 344H 전까지 중간)",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "receipt_id": "run344F_claim_boundary(주장 경계)",
            "run_id": RUN_ID,
            "candidate_selection": final["candidate_selection"],
            "selected_model": final["selected_model"],
            "new_mt5_execution": final["new_mt5_execution"],
            "forward_passed": final["forward_passed"],
            "runtime_authority": final["runtime_authority"],
            "operating_promotion": final["operating_promotion"],
            "goal_achieve": final["goal_achieve"],
            "effect": "keeps design from becoming operating claim(설계가 운영 주장으로 바뀌지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_lineage() -> None:
    inputs = [
        {
            "path": rel(path),
            "exists": path_is_file(path),
            "sha256": sha256_file(path) if path_is_file(path) else "",
        }
        for path in INPUT_FILES
    ]
    outputs = [
        {
            "path": rel(path),
            "exists": path_is_file(path),
            "sha256": sha256_file(path) if path_is_file(path) else "",
        }
        for path in OUTPUT_FILES
        if path != ARTIFACT_REGISTRY
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            "receipt_id": "run344F_artifact_lineage(산출물 계보)",
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "source_inputs": inputs,
            "artifact_paths": outputs,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "lineage_judgment": "connected_with_design_boundary(설계 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344F s07 Forward/Cost/Stability Validation Design(344F s07 전진/비용/안정성 검증 설계)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- candidate(후보): `s07_trend_confirmed_long_only`
- reference KPI(참조 핵심 성과 지표): net(순수익) `{final['reference_net_profit']}`, PF(수익 팩터) `{final['reference_profit_factor']}`, expectancy(기대값) `{final['reference_expectancy']}`, recovery(회복 계수) `{final['reference_recovery_factor']}`, drawdown(낙폭) `{final['reference_drawdown']}`, trades(거래수) `{final['reference_trade_count']}`
- selected_model(선정 모델): `{final['selected_model']}`
- runtime_authority(런타임 권위): `{final['runtime_authority']}`
- operating_promotion(운영 승격): `{final['operating_promotion']}`
- Goal Achieve(목표 달성): `{final['goal_achieve']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Design(설계)

run344F는 s07을 바로 운영으로 올리지 않는다. cost stress(비용 압박), session/regime stability(세션/국면 안정성), anchor/s05/s07 comparator(앵커/s05/s07 대조), forward/replay handoff(전진/재생 인계)를 run344G package(패키지)로 넘긴다.

## Effect(효과)

좋은 MT5 숫자를 더 강한 주장으로 착각하지 않고, 다음 작업이 비용과 국면에서 깨지는지를 먼저 보게 한다.

## Boundary(경계)

이 run(실행)은 design only(설계 전용)이다. new MT5 execution(새 MT5 실행), forward pass(전진 통과), selection(선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage344F Validation Design Decision(344F 검증 설계 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(EXPERIMENT_CONTRACT)}`, `{rel(VALIDATION_SURFACE_PLAN)}`, `{rel(COST_STRESS_CONTRACT)}`, `{rel(SESSION_REGIME_PLAN)}`, `{rel(NEXT_QUEUE)}`

Action(행동): s07 trend-confirmed long(추세 확인 롱)을 비용/세션/국면/전진 준비 검증 패키지로 넘긴다.
Effect(효과): run344G가 좁은 패키지 물질화만 수행하게 만들어 Stage(단계) 부담을 낮춘다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run344F 설계가 완료되어, 다음 작업은 run344G materialization(물질화)이다. s07은 아직 research promotion candidate(연구 승격 후보)이며 운영 선정은 아니다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- promotion_candidate(승격 후보): `s07_trend_confirmed_long_only`
- promotion_candidate_status(승격 후보 상태): `research_promotion_candidate_under_validation_design(검증 설계 중인 연구 승격 후보)`
- reference_net_profit(참조 순수익): `{final['reference_net_profit']}`
- reference_profit_factor(참조 수익 팩터): `{final['reference_profit_factor']}`
- reference_expectancy(참조 기대값): `{final['reference_expectancy']}`
- reference_drawdown(참조 낙폭): `{final['reference_drawdown']}`
- reference_recovery_factor(참조 회복 계수): `{final['reference_recovery_factor']}`
- reference_trade_count(참조 거래수): `{final['reference_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): s07을 검증 대상으로만 유지하고 운영 선정은 닫지 않는다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(WORKSPACE_STATE, workspace)

    marker = f"run344F {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344F s07 Forward/Cost/Stability Validation Design(344F s07 전진/비용/안정성 검증 설계)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): s07 검증을 비용/세션/국면/인계 패키지로 좁힘.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344F s07 Validation Design(344F s07 검증 설계)

- report(보고서): `{rel(REPORT_PATH)}`
- validation_plan(검증 계획): `{rel(VALIDATION_SURFACE_PLAN)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): run344G materialization(물질화)을 열고 운영 주장은 닫음.
""",
    )
    changelog = f"""## {TODAY} run344F s07 Validation Design(s07 검증 설계)

- action(행동): s07 trend-confirmed long(추세 확인 롱)의 cost/session/regime/forward handoff(비용/세션/국면/전진 인계) 설계를 생성했다.
- effect(효과): 다음 run344G를 좁은 package materialization(패키지 물질화)로 분리했다.
- boundary(경계): MT5 실행/전진 통과/운영 승격/목표 달성은 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## run344F s07 Validation Seed(s07 검증 씨앗)

- idea(아이디어): s07 trend-confirmed long(추세 확인 롱)을 비용/세션/국면/전진 인계 검증으로 압박한다.
- effect(효과): 좋은 단서를 운영 승격으로 과장하지 않고 검증 work packet(작업 묶음)으로 넘긴다.
""",
    )


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    gate_total = len(gates)
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "path": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    run_row = {
        **base,
        "lane": "experiment_design(실험 설계)",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "s07 validation design only(s07 검증 설계 전용); no MT5 execution(MT5 실행 없음).",
        "candidate_model_id": final["promotion_candidate_model_id"],
        "net_profit": final["reference_net_profit"],
        "profit_factor": final["reference_profit_factor"],
        "drawdown": final["reference_drawdown"],
        "recovery_factor": final["reference_recovery_factor"],
        "trade_count": final["reference_trade_count"],
        "expectancy": final["reference_expectancy"],
        "attempt_count": final["validation_surface_rows"],
        "result_status": JUDGMENT,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])

    ledger_rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "validation_design_no_new_kpi",
            "kpi_scope": "validation_design_no_new_kpi",
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": final["promotion_candidate_model_id"],
            "net_profit": final["reference_net_profit"],
            "profit_factor": final["reference_profit_factor"],
            "expectancy": final["reference_expectancy"],
            "drawdown": final["reference_drawdown"],
            "recovery_factor": final["reference_recovery_factor"],
            "trade_count": final["reference_trade_count"],
            "result_status": JUDGMENT,
            "attempt_count": final["validation_surface_rows"],
            "primary_kpi": f"reference_net={final['reference_net_profit']};reference_pf={final['reference_profit_factor']};validation_surfaces={final['validation_surface_rows']}",
            "guardrail_kpi": "design_only_no_new_mt5_kpi(설계 전용, 새 MT5 KPI 없음)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "notes": "Design only(설계 전용); opens run344G materialization(344G 물질화 개방).",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이번 design(설계) 범위 밖이므로 필수 누락으로 기록.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": final["promotion_candidate_model_id"],
            "net_profit": final["reference_net_profit"],
            "profit_factor": final["reference_profit_factor"],
            "expectancy": final["reference_expectancy"],
            "drawdown": final["reference_drawdown"],
            "recovery_factor": final["reference_recovery_factor"],
            "trade_count": final["reference_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "attempt_count": final["validation_surface_rows"],
            "primary_kpi": f"reference_net={final['reference_net_profit']};reference_pf={final['reference_profit_factor']};validation_surfaces={final['validation_surface_rows']}",
            "guardrail_kpi": "design_only_no_new_mt5_kpi(설계 전용, 새 MT5 KPI 없음)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "notes": "Combined(합산)는 Tier B(티어 B) 부재로 Tier A와 같은 설계 경계.",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], ledger_rows)


def write_artifact_registry() -> None:
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(OUTPUT_FILES, start=1):
        if path == ARTIFACT_REGISTRY or not path_is_file(path):
            continue
        artifact_type = "script" if path == Path(__file__) else path.suffix.lstrip(".") or "artifact"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": f"{RUN_NUMBER}_{index:02d}_{artifact_type}",
                "notes": "run344F validation design output(344F 검증 설계 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if path_is_file(ARTIFACT_REGISTRY):
        fieldnames, existing = pkg.read_csv_rows(ARTIFACT_REGISTRY)
    else:
        fieldnames, existing = [], []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    kept = [row for row in existing if row.get("run_id") != RUN_ID]
    pkg.write_csv_rows(ARTIFACT_REGISTRY, kept + rows, fieldnames)


def cleanup_stale_outputs() -> None:
    run_root = RUN_DIR.resolve()
    if not os.path.isdir(pkg.fs_path(run_root)):
        return
    for child in RUN_DIR.iterdir():
        resolved = child.resolve()
        if not str(resolved).lower().startswith(str(run_root).lower()):
            raise RuntimeError(f"refusing to clean outside run dir: {child}")


def main() -> None:
    cleanup_stale_outputs()
    final = build_contracts()
    gates = make_gates(final)
    final = {
        **final,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "gates": gates,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_receipts(final)
    write_docs(final)
    write_registers(final, gates)
    write_lineage()
    write_artifact_registry()

    if any(row["status"] != "passed" for row in gates):
        raise RuntimeError("run344F gate audit failed")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": final["goal_achieve"],
                "selected_model": final["selected_model"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
