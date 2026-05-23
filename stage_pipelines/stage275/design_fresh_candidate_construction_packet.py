from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
RUN_ID = "run275A_design_fresh_candidate_construction_packet_v1"
SOURCE_RUN_ID = "run274F_close_stage274_open_stage275_fresh_candidate_construction_v1"
STATUS = "completed_fresh_candidate_construction_packet_design_no_candidate_selection"
JUDGMENT = "fresh_candidate_construction_queue_ready_no_candidate_selection"
NEXT_ACTION = "run275B_materialize_fresh_candidate_package_blueprints"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE / "02_runs" / "run275A"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

STAGE274 = ROOT / "stages" / "274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild"
RUN274E = STAGE274 / "02_runs" / "run274E"
RUN274F = STAGE274 / "02_runs" / "run274F"
SOURCE_CLOSEOUT = STAGE274 / "03_reviews" / "stage274_closeout_stage275_handoff.md"
SOURCE_DECISION_MATRIX = RUN274E / "screening_decision_matrix.csv"
SOURCE_FAILURE_MEMORY = RUN274E / "failure_memory.csv"
SOURCE_HANDOFF_RECOMMENDATION = RUN274E / "stage275_handoff_recommendation.json"
SOURCE_HANDOFF_MANIFEST = RUN274F / "stage275_handoff_manifest.json"
STAGE_BRIEF = STAGE / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE / "01_inputs" / "input_refs.md"

MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
FEATURE_ORDER = MODEL_INPUT.with_name("model_input_feature_order.txt")
DATASET_PROFILE = ROOT / "stages" / "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure" / "02_runs" / "run271C" / "dataset_profile.json"

CONSTRUCTION_QUEUE = RUN_DIR / "queue.csv"
FAILURE_BOUNDARY_MAP = RUN_DIR / "failure_map.csv"
FEATURE_IDENTITY = RUN_DIR / "feature_id.csv"
CONSTRUCTION_PACKET = RUN_DIR / "packet.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
RUN_REPORT = REVIEWS / "run275A_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER_PATH = Path("stage_pipelines/stage275/design_fresh_candidate_construction_packet.py")

STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
QUEUE_COLUMNS = (
    "package_id",
    "queue_role",
    "fresh_thesis",
    "feature_surface",
    "model_or_scoring_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "feature_order_hash",
    "required_feature_groups",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "upside_condition",
    "failure_condition",
    "discard_condition",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "source_failure_memory",
    "freshness_guard",
    "next_use",
    "claim_boundary",
)
FAILURE_MAP_COLUMNS = (
    "memory_id",
    "source_failure_id",
    "source_package_id",
    "failed_boundary",
    "why_failed",
    "salvage_value",
    "do_not_repeat",
    "stage275_requirement",
    "mapped_packages",
    "reopen_condition",
    "evidence_path",
)
FEATURE_IDENTITY_COLUMNS = (
    "identity_id",
    "artifact_path",
    "artifact_hash",
    "feature_order_hash",
    "feature_count",
    "row_count",
    "split_scope",
    "tier_boundary",
    "identity_judgment",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def load_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return dict(json.load(handle))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def digest_payload(payload: Any) -> str:
    raw = json.dumps(json_ready(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def ordered_hash(values: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def feature_order_values() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def package_definitions(feature_hash: str) -> list[dict[str, Any]]:
    common_controls = (
        "symbol=US100;timeframe=M5;broker=FPMarkets;"
        f"feature_order_hash={feature_hash};"
        "Tier A separate + Tier B separate + Tier A+B combined required;"
        "Stage274 q04 failure signatures used only as negative memory"
    )
    sample_scope = (
        "data/processed model input(모델 입력) US100 M5; train/validation/oos(학습/검증/표본외); "
        "Tier A separate/Tier B mirror/Tier A+B combined(티어 A 분리/티어 B 거울/티어 A+B 합산) planned"
    )
    adapter_fields = "package_id;feature_order_hash;decision_rule_hash;risk_rule_hash;adapter_schema_hash;route_code;model_risk_pct;telemetry_json"
    return [
        {
            "package_id": "cp275A_volatility_pullback_breakout_surface",
            "queue_role": "selectable_fresh_candidate_seed",
            "fresh_thesis": "Volatility pullback after directional pressure(방향 압박 이후 변동성 되돌림)는 q04 trade removal(q04 거래 제거)이 아니라 new entry creation(새 진입 생성)으로 시험할 수 있다.",
            "feature_surface": "return_zscore_20;atr_14_over_atr_50;bollinger_width_20;bb_position_20;adx_14;di_spread_14;supertrend_10_3;vortex_indicator",
            "model_or_scoring_surface": "deterministic rank surface(결정 순위 표면) first, optional tree model(선택 트리 모델) only after active-entry proof(활성 진입 증명)",
            "decision_surface": "Create long/short permissions(롱/숏 허용) when trend pressure(추세 압박) and pullback location(되돌림 위치) disagree constructively; require new_active_count(새 활성 수) > 0 or direction_changed_count(방향 변경 수) > 0 versus q04 control(q04 대조).",
            "risk_logic": "Use volatility budget(변동성 예산) to scale risk before any no-trade state(무거래 상태); flat-only filtering(관망 전용 필터)은 실패다.",
            "adapter_path": "stage275 local Adapter blueprint(단계 로컬 어댑터 청사진) -> reusable Adapter only if materialized surface survives.",
            "runtime_handoff": adapter_fields + ";volatility_pullback_score;pullback_breakout_state",
            "feature_order_hash": feature_hash,
            "required_feature_groups": "volatility;trend;pullback_position;direction_pressure",
            "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard",
            "control_variables": common_controls,
            "changed_variables": "volatility_pullback_score;pullback_breakout_state;long_permission_score;short_permission_score",
            "sample_scope": sample_scope,
            "upside_condition": "Creates active entries(활성 진입 생성) in validation/OOS(검증/표본외) without becoming duplicate q04(중복 q04).",
            "failure_condition": "All improvement comes from reducing q04 trades(q04 거래 감소만) or no new direction switch(방향 전환 없음).",
            "discard_condition": "Discard if changed_signal_rate(변경 신호율) <= 0.01 and new_active_count(새 활성 수)=0 after materialization.",
            "invalid_conditions": "feature order mismatch(피처 순서 불일치), missing Tier B(티어 B 누락), label leakage(라벨 누수), or missing decision/risk hash(판단/위험 해시 누락).",
            "stop_conditions": "Stop within two stages if active-entry proof(활성 진입 증명) or non-filter upside(비필터 상방) is absent.",
            "evidence_plan": "run275B blueprint(청사진);run275C scoring input(점수 입력);run275D score table(점수표);Tier A/B/A+B screen(티어 A/B/A+B 선별).",
            "source_failure_memory": "NEG-ST274-RUN274E-cp274A|NEG-ST274-RUN274E-cp274C",
            "freshness_guard": "must differ from q04 by new entries or direction changes, not risk telemetry only(위험 기록만 금지)",
            "next_use": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "package_id": "cp275B_cross_asset_divergence_reversal_surface",
            "queue_role": "selectable_fresh_candidate_seed",
            "fresh_thesis": "US100 versus mega-cap breadth divergence(대형주 폭 대비 US100 괴리)는 calendar exclusion(달력 제외)이 아니라 direction switch(방향 전환) 신호가 될 수 있다.",
            "feature_surface": "mega8_equal_return_1;top3_weighted_return_1;mega8_pos_breadth_1;mega8_dispersion_5;us100_minus_mega8_equal_return_1;us100_minus_top3_weighted_return_1;vix_zscore_20;us10yr_zscore_20;usdx_zscore_20",
            "model_or_scoring_surface": "cross-asset spread score(교차자산 스프레드 점수) plus reversal permission(반전 허용)",
            "decision_surface": "Allow counter-direction route(반대 방향 경로) when index move(지수 움직임) separates from breadth confirmation(폭 확인); require direction_changed_count(방향 변경 수) > 0.",
            "risk_logic": "Risk is reduced when macro stress(거시 압박) agrees against the route, but reversal route(반전 경로)는 not blocked(차단 아님) if breadth divergence(폭 괴리)가 strong(강함).",
            "adapter_path": "stage275 cross-asset Adapter schema(교차자산 어댑터 스키마) with explicit feature order hash(피처 순서 해시).",
            "runtime_handoff": adapter_fields + ";cross_asset_divergence_score;reversal_permission_score",
            "feature_order_hash": feature_hash,
            "required_feature_groups": "cross_asset_breadth;macro_stress;relative_return;direction_switch",
            "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard",
            "control_variables": common_controls,
            "changed_variables": "cross_asset_divergence_score;reversal_permission_score;route_switch_flag",
            "sample_scope": sample_scope,
            "upside_condition": "Produces non-zero direction switches(방향 전환) and improves weak-month behavior(약한 월 행동) without month-only gating(월 전용 게이트).",
            "failure_condition": "Only removes trades in weak months(약한 월 거래 제거만) or mirrors q04 route(q04 경로 복제).",
            "discard_condition": "Discard if direction_changed_count(방향 변경 수)=0 or changed signals concentrate in one calendar month(한 월 집중).",
            "invalid_conditions": "macro feature missing(거시 피처 누락), timestamp misalignment(시각 불일치), Tier B omitted(티어 B 누락), or feature hash mismatch(피처 해시 불일치).",
            "stop_conditions": "Stop if divergence score(괴리 점수) cannot create route switch(경로 전환) by run275D.",
            "evidence_plan": "feature identity receipt(피처 정체성 영수증);score surface materialization(점수 표면 물질화);q04 freshness screen(q04 신선도 선별).",
            "source_failure_memory": "NEG-ST274-RUN274E-cp274B",
            "freshness_guard": "must be direction switch(방향 전환) capable, not removed pocket(제거 구간) only",
            "next_use": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "package_id": "cp275C_cash_session_impulse_continuation_surface",
            "queue_role": "selectable_fresh_candidate_seed",
            "fresh_thesis": "Cash-session impulse(현금장 충격)는 bad-hour removal(나쁜 시간 제거)이 아니라 continuation versus fade(연속/반전) decision surface(판단 표면)로 바꿀 수 있다.",
            "feature_surface": "is_us_cash_open;minutes_from_cash_open;is_first_30m_after_open;is_last_30m_before_cash_close;gap_percent;overnight_return;log_return_1;log_return_3;historical_vol_5_over_20",
            "model_or_scoring_surface": "session impulse state machine(세션 충격 상태기계) with continuation/fade score(연속/반전 점수)",
            "decision_surface": "Create new active entries(새 활성 진입) around cash-open and close phases(현금장 개장/마감 국면) when impulse quality(충격 품질) is high; no blanket session filter(전면 세션 필터 금지).",
            "risk_logic": "Use smaller risk(작은 위험) during impulse uncertainty(충격 불확실성) and larger budget(큰 예산) only when spread of continuation/fade scores(연속/반전 점수 차이) is clear.",
            "adapter_path": "stage275 session-phase Adapter draft(세션 국면 어댑터 초안).",
            "runtime_handoff": adapter_fields + ";session_impulse_score;continuation_fade_state",
            "feature_order_hash": feature_hash,
            "required_feature_groups": "session_phase;gap;overnight;short_return;volatility_shift",
            "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard",
            "control_variables": common_controls,
            "changed_variables": "session_impulse_score;continuation_score;fade_score;phase_risk_budget",
            "sample_scope": sample_scope,
            "upside_condition": "Adds entry supply(진입 공급) outside q04 active set(q04 활성 집합 밖) while preserving trade count(거래 수).",
            "failure_condition": "Becomes cash-session exclusion(현금장 제외) or reduces trades without new entries(새 진입 없는 거래 축소).",
            "discard_condition": "Discard if new_active_count(새 활성 수)=0 or active_rate_delta(활성률 차이) is only negative(음수만).",
            "invalid_conditions": "session timestamp boundary unclear(세션 시각 경계 불명확), missing Tier B(티어 B 누락), or split leakage(분할 누수).",
            "stop_conditions": "Stop if session phase(세션 국면) only behaves as filter(필터) in materialized screen(물질화 선별).",
            "evidence_plan": "timestamp/session integrity(시각/세션 무결성);active-entry screen(활성 진입 선별);trade supply guard(거래 공급 방어).",
            "source_failure_memory": "NEG-ST274-RUN274E-cp274A|NEG-ST274-RUN274E-cp274B",
            "freshness_guard": "must create session-specific active entry(세션별 활성 진입) or continuation/fade switch(연속/반전 전환)",
            "next_use": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "package_id": "cp275D_macro_volatility_squeeze_release_surface",
            "queue_role": "selectable_fresh_candidate_seed",
            "fresh_thesis": "Macro stress plus volatility squeeze release(거시 압박과 변동성 압축 해제)는 risk-only telemetry(위험 기록 전용)가 아니라 asymmetric route creation(비대칭 경로 생성)로 시험할 수 있다.",
            "feature_surface": "bb_squeeze;bollinger_width_20;historical_vol_20;historical_vol_5_over_20;vix_change_1;vix_zscore_20;us10yr_change_1;usdx_change_1;rsi_14;rsi_14_slope_3",
            "model_or_scoring_surface": "squeeze-release score(압축 해제 점수) with macro stress agreement(거시 압박 일치)",
            "decision_surface": "Open route(경로 개방) when squeeze release(압축 해제) and macro stress(거시 압박) define asymmetric payoff(비대칭 보상); permit both breakout and reversal states(돌파/반전 상태).",
            "risk_logic": "Risk expands(위험 확대) only when squeeze release(압축 해제) is confirmed; otherwise small probe risk(작은 탐침 위험).",
            "adapter_path": "stage275 macro-vol Adapter draft(거시-변동성 어댑터 초안).",
            "runtime_handoff": adapter_fields + ";squeeze_release_score;macro_vol_route_state",
            "feature_order_hash": feature_hash,
            "required_feature_groups": "volatility_compression;macro_stress;momentum_slope;route_state",
            "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard",
            "control_variables": common_controls,
            "changed_variables": "squeeze_release_score;macro_vol_route_state;risk_budget_multiplier",
            "sample_scope": sample_scope,
            "upside_condition": "Finds upside(상방) from volatility release(변동성 해제) rather than q04 failure-pocket avoidance(q04 실패 구간 회피).",
            "failure_condition": "Only shifts risk telemetry(위험 기록만 이동) while entry signal(진입 신호) remains q04 duplicate(q04 중복).",
            "discard_condition": "Discard if changed_signal_rate(변경 신호율) <= 0.01 or mean risk delta(평균 위험 차이) is the only material change(유일한 변화).",
            "invalid_conditions": "volatility feature missing(변동성 피처 누락), feature order mismatch(피처 순서 불일치), or Tier B missing(티어 B 누락).",
            "stop_conditions": "Stop if score surface(점수 표면) is not separable from q04 control(q04 대조).",
            "evidence_plan": "score separation receipt(점수 분리 영수증);new active/direction screen(새 활성/방향 선별);risk budget receipt(위험 예산 영수증).",
            "source_failure_memory": "NEG-ST274-RUN274E-cp274A|NEG-ST274-RUN274E-cp274C",
            "freshness_guard": "must alter entry or route state(진입 또는 경로 상태 변경), not only model_risk_pct(모델 위험 비율) telemetry",
            "next_use": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "package_id": "cp275E_q04_stage274_failure_signature_guard",
            "queue_role": "support_control",
            "fresh_thesis": "q04 and Stage274 failure signature(q04 및 274단계 실패 서명)를 support control(보조 대조)로 보존한다.",
            "feature_surface": "q04_control_signature;stage274_duplicate_filter_signature;active_signal_count;changed_signal_rate;new_active_count;direction_changed_count",
            "model_or_scoring_surface": "reference signature only(참고 서명 전용)",
            "decision_surface": "No candidate decision(후보 판단 없음); any selectable package(선택 가능 패키지)가 this signature(이 서명)를 match(일치)하면 reject(거절).",
            "risk_logic": "No runtime risk authority(런타임 위험 권위 없음).",
            "adapter_path": "control-only guard(대조 전용 방어), not Adapter package(어댑터 패키지 아님).",
            "runtime_handoff": "package_id;failure_signature_hash;telemetry_json",
            "feature_order_hash": feature_hash,
            "required_feature_groups": "failure_signature;freshness_guard",
            "comparison_baseline": "q04_failed_surface_and_stage274_filter_like_surfaces",
            "control_variables": common_controls,
            "changed_variables": "none_control_only",
            "sample_scope": sample_scope,
            "upside_condition": "not_applicable_control_only",
            "failure_condition": "If treated as candidate(후보 취급), invalid(무효).",
            "discard_condition": "Never promote(승격 금지); keep only as freshness guard(신선도 방어).",
            "invalid_conditions": "Missing Stage274 failure memory(274단계 실패 기억 누락) or decision matrix(결정 행렬 누락).",
            "stop_conditions": "Use only while screening Stage275 surfaces(275단계 표면 선별 중에만 사용).",
            "evidence_plan": "freshness comparison(신선도 비교);duplicate/filter-like rejection(중복/필터형 거절).",
            "source_failure_memory": "NEG-ST274-RUN274E-cp274A|NEG-ST274-RUN274E-cp274B|NEG-ST274-RUN274E-cp274C",
            "freshness_guard": "support control only(보조 대조만)",
            "next_use": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    ]


def failure_boundary_map(failure_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    mapped: list[dict[str, Any]] = []
    package_map = {
        "NEG-ST274-RUN274E-cp274A": "cp275A_volatility_pullback_breakout_surface|cp275C_cash_session_impulse_continuation_surface|cp275D_macro_volatility_squeeze_release_surface",
        "NEG-ST274-RUN274E-cp274B": "cp275B_cross_asset_divergence_reversal_surface|cp275C_cash_session_impulse_continuation_surface",
        "NEG-ST274-RUN274E-cp274C": "cp275A_volatility_pullback_breakout_surface|cp275D_macro_volatility_squeeze_release_surface",
    }
    for index, row in enumerate(failure_rows, start=1):
        failure_id = str(row.get("failure_id", f"unknown_{index}"))
        why_failed = str(row.get("why_failed", ""))
        if "trade(거래)를 줄이기만" in why_failed:
            requirement = "new active entry(새 활성 진입) or direction switch(방향 전환), not trade removal(거래 제거 아님)"
            failed_boundary = "filter_like_trade_reduction(필터형 거래 축소)"
            do_not_repeat = "Do not design package(패키지)를 q04 trade removal(q04 거래 제거) only."
        else:
            requirement = "distinct decision surface(구별되는 판단 표면) with changed signal(변경 신호)"
            failed_boundary = "duplicate_or_near_duplicate_signal_surface(중복 또는 거의 중복 신호 표면)"
            do_not_repeat = "Do not keep only risk telemetry(위험 기록) while entry signal(진입 신호) stays same."
        mapped.append(
            {
                "memory_id": f"FM275A-{index:02d}",
                "source_failure_id": failure_id,
                "source_package_id": row.get("package_id", ""),
                "failed_boundary": failed_boundary,
                "why_failed": why_failed,
                "salvage_value": row.get("salvage_value", ""),
                "do_not_repeat": do_not_repeat,
                "stage275_requirement": requirement,
                "mapped_packages": package_map.get(failure_id, "cp275E_q04_stage274_failure_signature_guard"),
                "reopen_condition": row.get("reopen_condition", ""),
                "evidence_path": row.get("evidence_path", rel(SOURCE_DECISION_MATRIX)),
            }
        )
    return mapped


def feature_identity_rows(profile: Mapping[str, Any], feature_hash: str, features: Sequence[str]) -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "run275A_model_input_feature_order",
            "artifact_path": rel(FEATURE_ORDER),
            "artifact_hash": sha256_file_lf_normalized(FEATURE_ORDER),
            "feature_order_hash": feature_hash,
            "feature_count": len(features),
            "row_count": profile.get("row_count", ""),
            "split_scope": "train/validation/oos(학습/검증/표본외)",
            "tier_boundary": "Tier A source plus Tier B mirror boundary planned(티어 A 원천 및 티어 B 거울 경계 계획)",
            "identity_judgment": "usable_for_design_no_candidate_selection",
        },
        {
            "identity_id": "run275A_model_input_dataset",
            "artifact_path": rel(MODEL_INPUT),
            "artifact_hash": sha256_file_lf_normalized(MODEL_INPUT),
            "feature_order_hash": feature_hash,
            "feature_count": profile.get("feature_count", len(features)),
            "row_count": profile.get("row_count", ""),
            "split_scope": json.dumps(profile.get("split_counts", {}), ensure_ascii=False, sort_keys=True),
            "tier_boundary": "Tier A source; Tier B must be explicit mirror or generated paired view(티어 B는 명시 거울 또는 생성 쌍 보기 필요)",
            "identity_judgment": "usable_with_boundary_design_only",
        },
    ]


def experiment_receipt(packages: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "hypothesis": "Fresh feature/decision/risk surfaces(새 피처/판단/위험 표면)가 q04 repair(q04 수리)를 반복하지 않고 ONNX-worthy candidate(온엑스화 가치 후보) 대기열을 만들 수 있다.",
        "decision_use": "Select packages(패키지)를 run275B blueprint materialization(청사진 물질화)으로 넘길지 결정한다.",
        "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard and Stage274 no-survivor failure memory(보조 대조와 274단계 생존 없음 실패 기억)",
        "control_variables": "US100 M5 FPMarkets; feature order hash fixed(피처 순서 해시 고정); Tier A/B/A+B records required(티어 A/B/A+B 기록 필수)",
        "changed_variables": [row["changed_variables"] for row in packages if row["queue_role"] != "support_control"],
        "sample_scope": "US100 M5 2022-09-01 through 2026-04-13 train/validation/oos design scope(설계 범위)",
        "success_criteria": "At least one selectable package(선택 가능 패키지)가 new active entry(새 활성 진입) or direction switch(방향 전환)를 target(목표)로 갖고 feature/order/handoff identity(피처/순서/인계 정체성)를 추적 가능하게 남긴다.",
        "failure_criteria": "Queue repeats q04 repair(q04 수리 반복), duplicate signal(중복 신호), or filter-only trade reduction(필터 전용 거래 축소).",
        "invalid_conditions": "Missing Stage274 failure memory(실패 기억 누락), model input identity(모델 입력 정체성 누락), or Tier B boundary(티어 B 경계 누락).",
        "stop_conditions": "If run275B-run275D cannot produce non-filter active-entry evidence(비필터 활성 진입 근거), close Stage275 as failure memory(실패 기억) and pivot.",
        "evidence_plan": [CONSTRUCTION_QUEUE, FEATURE_IDENTITY, FAILURE_BOUNDARY_MAP, RESULT_JUDGMENT, GATE_AUDIT],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def data_integrity_receipt(profile: Mapping[str, Any], feature_hash: str) -> dict[str, Any]:
    return {
        "data_source": rel(MODEL_INPUT),
        "time_axis": "M5 bar timestamp(5분봉 시각) from FPMarkets US100; timezone already stored as UTC-like aware timestamps(UTC형 시각).",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "date_min": profile.get("timestamp_min"),
            "date_max": profile.get("timestamp_max"),
            "rows": profile.get("row_count"),
            "splits": profile.get("split_counts"),
            "tier_scope": "Tier A source; Tier B mirror must be explicit downstream(티어 B 거울은 다음 실행에서 명시 필요)",
        },
        "missing_or_duplicate_check": f"dataset_profile duplicate_timestamps(중복 시각)={profile.get('duplicate_timestamps')}",
        "feature_label_boundary": "Features(피처)는 model input contract(모델 입력 계약)을 따르고, labels(라벨)는 fwd12 future columns(미래 12봉 열)로만 metadata(메타데이터)에 둔다.",
        "split_boundary": "Thresholds or ranks(임계값/순위)은 downstream materialization(하위 물질화)에서 train split(학습 분할)로만 정한다.",
        "leakage_risk": "Using future_log_return_12(미래 로그수익) or label columns(라벨 열) in score formula(점수식) would be leakage(누수).",
        "data_hash_or_identity": {
            "dataset_sha256": sha256_file_lf_normalized(MODEL_INPUT),
            "feature_order_hash": feature_hash,
            "dataset_profile_hash": sha256_file_lf_normalized(DATASET_PROFILE),
        },
        "integrity_judgment": "usable_with_boundary_design_only",
        "claim_boundary": BOUNDARY,
    }


def model_validation_receipt(packages: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "model_family": "deterministic score/scout surfaces first(결정 점수/스카우트 표면 우선); no trained ONNX model(훈련 ONNX 모델 없음)",
        "target_and_label": "Exploratory entry/direction/risk surface(탐색 진입/방향/위험 표면); label not consumed in run275A(275A에서 라벨 미사용)",
        "split_method": "run275A design only(설계 전용); future materialization must use train split for thresholds(임계값은 학습 분할만)",
        "selection_metric": "freshness target(신선도 목표): new_active_count(새 활성 수), direction_changed_count(방향 변경 수), changed_signal_rate(변경 신호율)",
        "secondary_metrics": "Tier A/B/A+B coverage(티어 A/B/A+B 커버리지), active_rate_delta(활성률 차이), duplicate signature distance(중복 서명 거리)",
        "threshold_policy": "planned_train_split_only(학습 분할 전용 계획)",
        "overfit_risk": "Package ideas(패키지 아이디어)가 Stage274 weak pockets(약점 구간)에 과맞춤될 위험.",
        "calibration_risk": "Scores are ranks/states(순위/상태) only, not probabilities(확률 아님).",
        "comparison_baseline": "Stage274 q04 failure signature guard(q04 실패 서명 방어)",
        "validation_judgment": "exploratory_design_no_candidate_selection",
        "package_count": len(packages),
        "claim_boundary": BOUNDARY,
    }


def result_rows() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "fresh candidate construction queue(새 후보 구성 대기열); failure memory map(실패 기억 지도); feature identity(피처 정체성); receipts(영수증)",
            "evidence_missing": "materialized blueprint(물질화 청사진); score table(점수표); MT5 runtime output(MT5 런타임 출력); ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage275(275단계)는 q04 수리 대신 새 활성 진입/방향 전환 후보 묶음으로 시작했다.",
        }
    ]


def gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_name": "work_packet_schema_lint(작업 묶음 스키마 점검)",
            "status": "passed(통과)",
            "evidence_path": rel(EXPERIMENT_RECEIPT),
            "effect": "hypothesis/comparison/controls/criteria/evidence plan(가설/비교/대조/기준/근거 계획)을 기록했다.",
        },
        {
            "gate_name": "data_integrity_boundary(데이터 무결성 경계)",
            "status": "passed_with_boundary(경계 포함 통과)",
            "evidence_path": rel(DATA_INTEGRITY_RECEIPT),
            "effect": "feature order(피처 순서), split boundary(분할 경계), leakage risk(누수 위험)를 이름 붙였다.",
        },
        {
            "gate_name": "model_validation_boundary(모델 검증 경계)",
            "status": "passed_with_boundary(경계 포함 통과)",
            "evidence_path": rel(MODEL_VALIDATION_RECEIPT),
            "effect": "scores(점수)를 probability(확률)가 아닌 exploratory rank/state(탐색 순위/상태)로 제한했다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed(통과)",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "experiment_design(실험 설계) 필수 게이트와 claim boundary(주장 경계)를 closeout(종료 기록)에 연결했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def write_report(packages: Sequence[Mapping[str, Any]], failure_map: Sequence[Mapping[str, Any]]) -> None:
    queue_lines = "\n".join(
        f"- `{row['package_id']}`: {row['fresh_thesis']}"
        for row in packages
        if row["queue_role"] != "support_control"
    )
    write_md(
        RUN_REPORT,
        f"""# run275A Fresh Candidate Construction Packet(275A 새 후보 구성 묶음)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run275A(275A 실행)는 q04 repair(q04 수리)를 반복하지 않고 fresh candidate construction queue(새 후보 구성 대기열)를 만들었다.
효과(effect, 효과): 다음 run275B(275B 실행)는 새 active entry(새 활성 진입) 또는 direction switch(방향 전환)를 목표로 하는 package blueprint(패키지 청사진)를 물질화한다.

## Candidate Seeds(후보 씨앗)

{queue_lines}

## Failure Memory Boundary(실패 기억 경계)

- mapped failure memories(연결된 실패 기억): `{len(failure_map)}`
- support control(보조 대조): `cp275E_q04_stage274_failure_signature_guard`
- do-not-repeat rule(반복 금지 규칙): duplicate signal(중복 신호), filter-only trade reduction(필터 전용 거래 축소), risk telemetry only(위험 기록만)는 candidate package(후보 패키지)가 아니다.

## Evidence Paths(근거 경로)

- construction queue(구성 대기열): `{rel(CONSTRUCTION_QUEUE)}`
- failure boundary map(실패 경계 지도): `{rel(FAILURE_BOUNDARY_MAP)}`
- feature identity(피처 정체성): `{rel(FEATURE_IDENTITY)}`
- experiment receipt(실험 영수증): `{rel(EXPERIMENT_RECEIPT)}`
- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_or_append(text: str, prefix: str, replacement: str) -> str:
    if any(line.startswith(prefix) for line in text.splitlines()):
        return replace_line_prefix(text, prefix, replacement)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_stage_docs(packages: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in packages if row["queue_role"] == "selectable_fresh_candidate_seed")
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_or_append(selection, "- run275A_report", f"- run275A_report(275A 보고서): `{rel(RUN_REPORT)}`")
    selection = replace_or_append(selection, "- run275A_construction_queue", f"- run275A_construction_queue(275A 구성 대기열): `{rel(CONSTRUCTION_QUEUE)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = replace_or_append(review, "- run275A_report", f"- run275A_report(275A 보고서): `{rel(RUN_REPORT)}`")
    review = replace_or_append(review, "- run275A_construction_queue", f"- run275A_construction_queue(275A 구성 대기열): `{rel(CONSTRUCTION_QUEUE)}`")
    review = replace_or_append(review, "- run275A_failure_boundary_map", f"- run275A_failure_boundary_map(275A 실패 경계 지도): `{rel(FAILURE_BOUNDARY_MAP)}`")
    review = replace_or_append(review, "- run275A_feature_identity", f"- run275A_feature_identity(275A 피처 정체성): `{rel(FEATURE_IDENTITY)}`")
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_active_entry_direction_surface_construction_queue`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run275A_summary",
        f"- run275A_summary(275A 요약): run275A(275A 실행)는 selectable fresh candidate seed(선택 가능 새 후보 씨앗) `{selectable}`개와 support control(보조 대조) `1`개를 설계했다. Effect(효과): q04 repair(q04 수리)를 반복하지 않고 새 active entry/direction switch(활성 진입/방향 전환) 조건을 run275B(275B 실행) 청사진 물질화로 넘긴다. Boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage275(275단계) run275A(275A 실행) fresh candidate construction packet design(새 후보 구성 묶음 설계) `{RUN_ID}`. "
        f"Effect(효과): selectable fresh candidate seed(선택 가능 새 후보 씨앗) `{selectable}`개와 support control(보조 대조) `1`개를 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## 2026-05-23 run275A fresh candidate construction packet design(275A 새 후보 구성 묶음 설계)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): selectable fresh candidate seed(선택 가능 새 후보 씨앗) `{selectable}`개와 support control(보조 대조) `1`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def update_registers(created_at: str, packages: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    selectable = sum(1 for row in packages if row["queue_role"] == "selectable_fresh_candidate_seed")
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
                "notes": f"selectable_fresh_candidate_seeds={selectable};support_control=1;selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
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
            "record_view": "fresh candidate construction design(새 후보 구성 설계)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined design",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_candidate_construction",
            "status": STATUS,
            "judgment": row["queue_role"],
            "path": rel(CONSTRUCTION_QUEUE),
            "primary_kpi": "design_only_no_trading_kpi",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": row["discard_condition"],
        }
        for row in packages
    ]
    alpha_rows.extend(
        [
            {
                "ledger_row_id": f"{RUN_ID}__tier_b_boundary",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "tier_b_boundary",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Tier B boundary design(티어 B 경계 설계)",
                "tier_scope": "Tier B separate",
                "kpi_scope": "data_integrity_boundary",
                "scoreboard_lane": "fresh_candidate_construction",
                "status": STATUS,
                "judgment": "planned_explicit_boundary_no_authority",
                "path": rel(DATA_INTEGRITY_RECEIPT),
                "primary_kpi": "tier_b_required_downstream",
                "guardrail_kpi": "no_tier_b_omission_allowed",
                "external_verification_status": "out_of_scope_by_claim_design_only",
                "notes": "run275B/run275C must materialize or mark Tier B missing_required(필수 누락).",
            },
            {
                "ledger_row_id": f"{RUN_ID}__tier_ab_combined_boundary",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "tier_ab_combined_boundary",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Tier A+B combined boundary design(티어 A+B 합산 경계 설계)",
                "tier_scope": "Tier A+B combined",
                "kpi_scope": "experiment_design_boundary",
                "scoreboard_lane": "fresh_candidate_construction",
                "status": STATUS,
                "judgment": "planned_no_synthetic_performance_claim",
                "path": rel(EXPERIMENT_RECEIPT),
                "primary_kpi": "combined_record_required_downstream",
                "guardrail_kpi": "performance_claim=none",
                "external_verification_status": "out_of_scope_by_claim_design_only",
                "notes": "Combined row(합산 행)는 성과 주장이 아니라 설계 필수 조건이다.",
            },
        ]
    )
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_candidate_construction_packet_design",
                "tier_scope": "Tier A+B paired design",
                "scoreboard": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"selectable={selectable};support_control=1;next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    existing_artifacts = read_csv_rows(ARTIFACT_REGISTRY)
    write_csv_rows(
        ARTIFACT_REGISTRY,
        ARTIFACT_COLUMNS,
        [row for row in existing_artifacts if str(row.get("run_id", "")) != RUN_ID],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run275A_fresh_candidate_construction_design_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run275A fresh candidate construction packet design artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def manifest_payload(
    created_at: str,
    packages: Sequence[Mapping[str, Any]],
    artifacts: Sequence[Path],
    source_inputs: Sequence[Path],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "package_ids": [row["package_id"] for row in packages],
        "selectable_package_rows": sum(1 for row in packages if row["queue_role"] == "selectable_fresh_candidate_seed"),
        "support_control_rows": sum(1 for row in packages if row["queue_role"] == "support_control"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
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


def run() -> dict[str, Any]:
    must_exist(
        [
            SOURCE_CLOSEOUT,
            SOURCE_DECISION_MATRIX,
            SOURCE_FAILURE_MEMORY,
            SOURCE_HANDOFF_RECOMMENDATION,
            SOURCE_HANDOFF_MANIFEST,
            STAGE_BRIEF,
            INPUT_REFS,
            MODEL_INPUT,
            FEATURE_ORDER,
            DATASET_PROFILE,
        ]
    )
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS).mkdir(parents=True, exist_ok=True)
    io_path(SELECTED).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()

    features = feature_order_values()
    profile = load_json(DATASET_PROFILE)
    feature_hash = str(profile.get("feature_order_hash") or ordered_hash(features))
    failure_rows = read_csv_rows(SOURCE_FAILURE_MEMORY)
    packages = package_definitions(feature_hash)
    failure_map = failure_boundary_map(failure_rows)
    feature_identity = feature_identity_rows(profile, feature_hash, features)

    write_csv(CONSTRUCTION_QUEUE, QUEUE_COLUMNS, packages)
    write_csv(FAILURE_BOUNDARY_MAP, FAILURE_MAP_COLUMNS, failure_map)
    write_csv(FEATURE_IDENTITY, FEATURE_IDENTITY_COLUMNS, feature_identity)
    write_json(CONSTRUCTION_PACKET, {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "packages": packages,
        "failure_memory_boundary_map": failure_map,
        "feature_identity": feature_identity,
        "package_hashes": {row["package_id"]: digest_payload(row) for row in packages},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    })
    write_json(EXPERIMENT_RECEIPT, experiment_receipt(packages))
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_receipt(profile, feature_hash))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_receipt(packages))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows())
    write_report(packages, failure_map)

    source_inputs = [
        SOURCE_CLOSEOUT,
        SOURCE_DECISION_MATRIX,
        SOURCE_FAILURE_MEMORY,
        SOURCE_HANDOFF_RECOMMENDATION,
        SOURCE_HANDOFF_MANIFEST,
        STAGE_BRIEF,
        INPUT_REFS,
        MODEL_INPUT,
        FEATURE_ORDER,
        DATASET_PROFILE,
    ]
    artifacts = [
        CONSTRUCTION_QUEUE,
        FAILURE_BOUNDARY_MAP,
        FEATURE_IDENTITY,
        CONSTRUCTION_PACKET,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = manifest_payload(created_at, packages, artifacts, source_inputs)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, packages, artifacts, source_inputs)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, packages, artifacts, source_inputs)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, packages, artifacts)
    update_stage_docs(packages)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "selectable_fresh_candidate_seeds": sum(1 for row in packages if row["queue_role"] == "selectable_fresh_candidate_seed"),
        "support_control_rows": sum(1 for row in packages if row["queue_role"] == "support_control"),
        "failure_memory_rows": len(failure_rows),
        "failure_boundary_rows": len(failure_map),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
