from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import review_bounded_repair_scaffold_inputs_without_db as bh


aw = bh.aw

TODAY = "2026-05-27"
STAGE_ID = bh.STAGE_ID
RUN_NUMBER = "run337BI"
RUN_ID = "run337BI_materialize_bounded_measurement_harness_without_db_v1"
PARENT_RUN_ID = bh.RUN_ID
NEXT_RUN_ID = "run337BJ_review_bounded_measurement_harness_without_db_v1"
STATUS = "completed_stage337BI_bounded_measurement_harness_inputs_materialized_no_training_no_selection"
JUDGMENT = "measurement_harness_inputs_materialized_for_profit_curve_proxy_mt5_and_gap_repair"
DECISION = "stage337BI_open_run337BJ_review_bounded_measurement_harness_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BI_measurement_harness_inputs_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bh.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BI_measurement_harness.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BI_measurement_harness.md"
SELECTED_STATUS = bh.SELECTED_STATUS
STAGE_BRIEF = bh.STAGE_BRIEF
WORKSPACE_STATE = bh.WORKSPACE_STATE
CURRENT_STATE = bh.CURRENT_STATE
CHANGELOG = bh.CHANGELOG
RUN_REGISTRY = bh.RUN_REGISTRY
ALPHA_LEDGER = bh.ALPHA_LEDGER
ARTIFACT_REGISTRY = bh.ARTIFACT_REGISTRY
STAGE_LEDGER = bh.STAGE_LEDGER

RUN337BH_DIR = STAGE_DIR / "02_runs" / "run337BH"
BH_FINAL = RUN337BH_DIR / "final_decision.json"
BH_MANIFEST = RUN337BH_DIR / "run_manifest.json"
BH_SCAFFOLD_REVIEW = RUN337BH_DIR / "scaffold_input_review_matrix.csv"
BH_PROFIT_REVIEW = RUN337BH_DIR / "profit_curve_contract_review.csv"
BH_PROXY_REVIEW = RUN337BH_DIR / "proxy_mt5_contract_review.csv"
BH_MT5_GAP_REVIEW = RUN337BH_DIR / "mt5_gap_repair_contract_review.csv"
BH_FIREWALL_REVIEW = RUN337BH_DIR / "no_lookahead_firewall_review.csv"
BH_LANE_REVIEW = RUN337BH_DIR / "balanced_lane_review.csv"
BH_HANDOFF = RUN337BH_DIR / "measurement_harness_handoff_boundary.csv"
BH_QUEUE = RUN337BH_DIR / "run337BI_measurement_harness_queue.csv"
BH_GATE_AUDIT = RUN337BH_DIR / "required_gate_coverage_audit.csv"
BH_EXPERIMENT_RECEIPT = RUN337BH_DIR / "experiment_design_receipt.json"
BH_DATA_RECEIPT = RUN337BH_DIR / "data_integrity_receipt.json"
BH_MODEL_RECEIPT = RUN337BH_DIR / "model_validation_receipt.json"
BH_RUNTIME_RECEIPT = RUN337BH_DIR / "runtime_parity_receipt.json"
BH_PERFORMANCE_RECEIPT = RUN337BH_DIR / "performance_attribution_receipt.json"
BH_ARTIFACT_RECEIPT = RUN337BH_DIR / "artifact_lineage_receipt.json"
BH_JUDGMENT_RECEIPT = RUN337BH_DIR / "result_judgment_receipt.json"

HARNESS_COMPONENTS = RUN_DIR / "measurement_harness_components.csv"
PROFIT_CURVE_SCHEMA = RUN_DIR / "profit_curve_trade_schema.csv"
PROXY_MT5_DIFF_SCHEMA = RUN_DIR / "proxy_mt5_difference_schema.csv"
MT5_PROBE_MANIFEST = RUN_DIR / "mt5_runtime_probe_manifest.csv"
COST_STRESS_MATRIX = RUN_DIR / "cost_stress_matrix.csv"
LOT_NORMALIZATION_SCHEMA = RUN_DIR / "lot_normalization_schema.csv"
REGIME_SLICE_SCHEMA = RUN_DIR / "regime_slice_schema.csv"
NO_LOOKAHEAD_VALIDATION_SCHEMA = RUN_DIR / "no_lookahead_validation_schema.csv"
HARNESS_EXECUTION_PLAN = RUN_DIR / "measurement_harness_execution_plan.csv"
RUN337BJ_QUEUE = RUN_DIR / "run337BJ_review_queue.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BH_FINAL,
    BH_MANIFEST,
    BH_SCAFFOLD_REVIEW,
    BH_PROFIT_REVIEW,
    BH_PROXY_REVIEW,
    BH_MT5_GAP_REVIEW,
    BH_FIREWALL_REVIEW,
    BH_LANE_REVIEW,
    BH_HANDOFF,
    BH_QUEUE,
    BH_GATE_AUDIT,
    BH_EXPERIMENT_RECEIPT,
    BH_DATA_RECEIPT,
    BH_MODEL_RECEIPT,
    BH_RUNTIME_RECEIPT,
    BH_PERFORMANCE_RECEIPT,
    BH_ARTIFACT_RECEIPT,
    BH_JUDGMENT_RECEIPT,
)
OUTPUT_FILES = (
    HARNESS_COMPONENTS,
    PROFIT_CURVE_SCHEMA,
    PROXY_MT5_DIFF_SCHEMA,
    MT5_PROBE_MANIFEST,
    COST_STRESS_MATRIX,
    LOT_NORMALIZATION_SCHEMA,
    REGIME_SLICE_SCHEMA,
    NO_LOOKAHEAD_VALIDATION_SCHEMA,
    HARNESS_EXECUTION_PLAN,
    RUN337BJ_QUEUE,
    REQUIRED_GATE_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

COMPONENT_COLUMNS = (
    "component_id",
    "component_family",
    "source_contract",
    "required_input_artifact",
    "required_output_artifact",
    "required_fields",
    "validation_rule",
    "forbidden_use",
    "consumer",
    "status",
    "effect",
    "claim_boundary",
)
SCHEMA_COLUMNS = (
    "field_id",
    "field_name",
    "field_type",
    "required",
    "source",
    "validation_rule",
    "downstream_metric",
    "forbidden_inference",
    "effect",
    "claim_boundary",
)
STRESS_COLUMNS = (
    "stress_id",
    "stress_family",
    "spread_multiplier",
    "slippage_points",
    "commission_adjustment",
    "applies_to",
    "required_output",
    "failure_signal",
    "effect",
    "claim_boundary",
)
PLAN_COLUMNS = (
    "plan_id",
    "sequence",
    "work_item",
    "required_inputs",
    "required_outputs",
    "must_pass_before_next",
    "blocked_claims",
    "status",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "review_subject",
    "inputs_to_review",
    "must_confirm",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BH measurement harness source files: {missing}")
    return {
        "final": read_json(BH_FINAL),
        "manifest": read_json(BH_MANIFEST),
        "scaffold": read_rows(BH_SCAFFOLD_REVIEW),
        "profit": read_rows(BH_PROFIT_REVIEW),
        "proxy": read_rows(BH_PROXY_REVIEW),
        "mt5_gap": read_rows(BH_MT5_GAP_REVIEW),
        "firewall": read_rows(BH_FIREWALL_REVIEW),
        "lanes": read_rows(BH_LANE_REVIEW),
        "handoff": read_rows(BH_HANDOFF),
        "queue": read_rows(BH_QUEUE),
        "gates": read_rows(BH_GATE_AUDIT),
        "receipts": [read_json(path) for path in (
            BH_EXPERIMENT_RECEIPT,
            BH_DATA_RECEIPT,
            BH_MODEL_RECEIPT,
            BH_RUNTIME_RECEIPT,
            BH_PERFORMANCE_RECEIPT,
            BH_ARTIFACT_RECEIPT,
            BH_JUDGMENT_RECEIPT,
        )],
    }


def build_components() -> list[dict[str, Any]]:
    rows = [
        ("profit_curve_ingest", "profit_curve(수익곡선)", aw.rel(BH_PROFIT_REVIEW), "MT5 report and trade list(MT5 보고서와 거래 목록)", aw.rel(PROFIT_CURVE_SCHEMA), "trade_id;open_time;close_time;direction;lot;net_profit;balance;equity", "all required trade and equity fields present(필수 거래/곡선 필드 존재)", "Forward Passed/Failed without fresh MT5 output(신규 MT5 출력 없는 전진 통과/실패)", NEXT_RUN_ID),
        ("proxy_mt5_diff_builder", "proxy_mt5_parity(프록시-MT5 동등성)", aw.rel(BH_PROXY_REVIEW), "proxy expected rows and MT5 runtime probe rows(프록시 예상 행과 MT5 런타임 탐침 행)", aw.rel(PROXY_MT5_DIFF_SCHEMA), "join_key;proxy_expected_value;mt5_runtime_probe_value;difference;usable_scope", "difference rows must include mismatch and usability judgment(차이 행은 불일치와 사용성 판정 포함)", "proxy KPI authority(프록시 KPI 권위)", NEXT_RUN_ID),
        ("mt5_probe_manifest", "runtime_probe(런타임 탐침)", aw.rel(BH_MT5_GAP_REVIEW), "MT5 tester report, terminal files, feature_last flag(MT5 테스터 보고서/터미널 파일/feature_last 플래그)", aw.rel(MT5_PROBE_MANIFEST), "probe_id;terminal_path;report_path;feature_last_reached;tester_last_bar", "feature_last reached must be explicit(feature_last 도달 여부 명시)", "runtime authority(런타임 권위)", NEXT_RUN_ID),
        ("cost_stress_overlay", "execution_stress(실행 스트레스)", aw.rel(BH_PROFIT_REVIEW), "trade list with spread/slippage fields(스프레드/슬리피지 필드 포함 거래 목록)", aw.rel(COST_STRESS_MATRIX), "stress_id;spread_multiplier;slippage_points;net_after_stress", "base/mild/hard stress required(기준/약함/강함 스트레스 필수)", "profit-only selection(수익 단독 선택)", NEXT_RUN_ID),
        ("lot_normalizer", "execution_normalization(실행 정규화)", aw.rel(BH_PROFIT_REVIEW), "trade list with lot field(로트 필드 포함 거래 목록)", aw.rel(LOT_NORMALIZATION_SCHEMA), "trade_id;lot;point_value;net_per_lot;risk_per_lot", "lot-normalized result must be present(로트 정규화 결과 필수)", "lot optimization(로트 최적화)", NEXT_RUN_ID),
        ("regime_slicer", "regime_attribution(국면 귀속)", aw.rel(BH_PROFIT_REVIEW), "as-of regime sidecars if available(가능 시 기준시각 국면 사이드카)", aw.rel(REGIME_SLICE_SCHEMA), "session;hour;month;volatility;ADX;VIX;USD;rate_regime", "release-time and as-of boundaries required(발표시각과 기준시각 경계 필수)", "look-ahead regime join(미래참조 국면 조인)", NEXT_RUN_ID),
        ("no_lookahead_validator", "falsification(반증)", aw.rel(BH_FIREWALL_REVIEW), "all harness inputs(모든 하네스 입력)", aw.rel(NO_LOOKAHEAD_VALIDATION_SCHEMA), "as_of_time;bar_close_time;feature_time;label_time;release_time", "feature_time <= decision_time and release_time <= as_of_time(피처시각은 결정시각 이하, 발표시각은 기준시각 이하)", "date-fit or trade-index target(날짜 맞춤 또는 거래번호 타깃)", NEXT_RUN_ID),
    ]
    return [
        {
            "component_id": f"{RUN_NUMBER}_{component_id}",
            "component_family": family,
            "source_contract": source_contract,
            "required_input_artifact": input_artifact,
            "required_output_artifact": output_artifact,
            "required_fields": fields,
            "validation_rule": validation,
            "forbidden_use": forbidden,
            "consumer": consumer,
            "status": "materialized_for_review(검토용 물질화)",
            "effect": "turns reviewed contracts into concrete harness inputs without touching cp322A(검토된 계약을 cp322A 변경 없이 구체 하네스 입력으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for component_id, family, source_contract, input_artifact, output_artifact, fields, validation, forbidden, consumer in rows
    ]


def build_profit_schema() -> list[dict[str, Any]]:
    fields = [
        ("trade_id", "string", "MT5 trade/deal list(MT5 거래 목록)", "unique non-empty(고유·비어있지 않음)", "trade_count(거래수)", "none"),
        ("open_time", "datetime_utc", "MT5 trade list(MT5 거래 목록)", "open_time <= close_time(진입시각 <= 청산시각)", "session/hour/month slices(세션/시간/월 조각)", "timezone-free comparison(시간대 없는 비교)"),
        ("close_time", "datetime_utc", "MT5 trade list(MT5 거래 목록)", "close_time completed before KPI read(KPI 판독 전 청산 완료)", "closed equity curve(청산 기준 곡선)", "floating-only profit claim(평가손익만으로 수익 주장)"),
        ("direction", "enum_long_short", "MT5 trade list(MT5 거래 목록)", "long or short only(롱 또는 숏만)", "long_short attribution(롱숏 귀속)", "direction missing attribution(방향 누락 귀속)"),
        ("source", "enum_D_B_DB", "runtime/proxy handoff(런타임/프록시 인계)", "D/B/D+B/none allowed(D/B/D+B/없음 허용)", "D/B attribution(D/B 귀속)", "source-free KPI(소스 없는 KPI)"),
        ("lot", "float", "MT5 trade list(MT5 거래 목록)", "lot > 0(로트 양수)", "lot_normalized result(로트 정규화 결과)", "lot optimization(로트 최적화)"),
        ("net_profit", "float", "MT5 report/trade list(MT5 보고서/거래 목록)", "cost included(비용 포함)", "net_profit/PF/expectancy(순수익/PF/기대값)", "gross-only profit(총수익만 사용)"),
        ("balance_after", "float", "equity curve(곡선)", "monotonic time order(시간 순서)", "drawdown/recovery(손실/회복)", "unordered curve(정렬 안 된 곡선)"),
        ("equity_after", "float", "equity curve(곡선)", "optional but if present ordered(선택, 있으면 정렬)", "underwater stretch(회복 전 체류)", "equity omitted without note(설명 없는 에쿼티 누락)"),
        ("spread_points", "float", "MT5 runtime/probe(MT5 런타임/탐침)", ">= 0", "cost stress(비용 스트레스)", "spread-free stress(스프레드 없는 스트레스)"),
        ("slippage_points", "float", "MT5 runtime/probe(MT5 런타임/탐침)", ">= 0", "cost stress(비용 스트레스)", "slippage-free stress(슬리피지 없는 스트레스)"),
    ]
    return [
        {
            "field_id": f"{RUN_NUMBER}_profit_{name}",
            "field_name": name,
            "field_type": field_type,
            "required": "true",
            "source": source,
            "validation_rule": validation,
            "downstream_metric": metric,
            "forbidden_inference": forbidden,
            "effect": "makes profit curve KPI auditable from raw trades(원거래에서 수익곡선 KPI를 감사 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, source, validation, metric, forbidden in fields
    ]


def build_proxy_schema() -> list[dict[str, Any]]:
    fields = [
        ("bar_time", "datetime_utc", "proxy and MT5 runtime probe(프록시와 MT5 런타임 탐침)", "join key required(조인 키 필수)", "row matching(행 매칭)", "nearest-time join without audit(감사 없는 근접시각 조인)"),
        ("symbol", "string", "proxy and MT5 runtime probe(프록시와 MT5 런타임 탐침)", "must equal US100(US100 일치)", "symbol parity(심볼 동등성)", "cross-symbol comparison(교차 심볼 비교)"),
        ("source", "enum_D_B_DB", "proxy and MT5 runtime probe(프록시와 MT5 런타임 탐침)", "D/B/D+B/none(D/B/D+B/없음)", "D/B attribution(D/B 귀속)", "source ignored(소스 무시)"),
        ("direction", "enum_long_short_none", "proxy and MT5 runtime probe(프록시와 MT5 런타임 탐침)", "long/short/none(롱/숏/없음)", "direction parity(방향 동등성)", "direction-free parity(방향 없는 동등성)"),
        ("proxy_expected_value", "float_or_string", "proxy output(프록시 출력)", "not null(누락 없음)", "expected value(예상값)", "proxy value as KPI(프록시 값을 KPI로 사용)"),
        ("mt5_runtime_probe_value", "float_or_string", "MT5 runtime probe(MT5 런타임 탐침)", "not null after probe(탐침 후 누락 없음)", "runtime probe value(런타임 탐침값)", "runtime authority claim(런타임 권위 주장)"),
        ("difference", "float_or_exact_match", "computed by harness(하네스 계산)", "tolerance applied(허용오차 적용)", "mismatch rows(불일치 행)", "silent mismatch(조용한 불일치)"),
        ("usable_scope", "enum_signal_only_handoff_only_diagnostic", "harness judgment(하네스 판정)", "must not be forward KPI(전진 KPI 불가)", "proxy usability(프록시 사용성)", "Forward Passed/Failed(전진 통과/실패)"),
    ]
    return [
        {
            "field_id": f"{RUN_NUMBER}_proxy_{name}",
            "field_name": name,
            "field_type": field_type,
            "required": "true",
            "source": source,
            "validation_rule": validation,
            "downstream_metric": metric,
            "forbidden_inference": forbidden,
            "effect": "forces proxy expected values and MT5 runtime probe values to be compared before use(사용 전 프록시 예상값과 MT5 런타임 탐침값 비교 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, source, validation, metric, forbidden in fields
    ]


def build_mt5_probe_manifest() -> list[dict[str, Any]]:
    fields = [
        ("probe_id", "string", "harness config(하네스 설정)", "unique non-empty(고유·비어있지 않음)", "probe identity(탐침 정체성)", "anonymous tester output(익명 테스터 출력)"),
        ("terminal_data_path", "path", "MT5 terminal(MT5 터미널)", "path exists before runtime claim(런타임 주장 전 경로 존재)", "terminal files(터미널 파일)", "missing handoff file(누락 인계 파일)"),
        ("tester_report_path", "path", "MT5 strategy tester(MT5 전략 테스터)", "report exists after probe(탐침 후 보고서 존재)", "tester evidence(테스터 근거)", "compile-only evidence(컴파일만 근거)"),
        ("feature_last_timestamp", "datetime_utc", "feature pipeline(피처 파이프라인)", "known before probe(탐침 전 알려짐)", "feature_last gap(feature_last 공백)", "unknown feature boundary(모르는 피처 경계)"),
        ("tester_last_observed_bar_time", "datetime_utc", "tester output(테스터 출력)", ">= feature_last required for forward(전진에는 feature_last 이상 필요)", "tester visibility(테스터 가시성)", "stale tester history(낡은 테스터 기록)"),
        ("feature_last_reached", "bool", "computed by harness(하네스 계산)", "true required before forward claim(전진 주장 전 true 필요)", "forward readiness gate(전진 준비 게이트)", "Forward claim while false(false 상태 전진 주장)"),
        ("proxy_mt5_difference_path", "path", "harness output(하네스 출력)", "required after probe(탐침 후 필수)", "proxy-MT5 difference(프록시-MT5 차이)", "unreviewed proxy use(미검토 프록시 사용)"),
    ]
    return [
        {
            "field_id": f"{RUN_NUMBER}_mt5_{name}",
            "field_name": name,
            "field_type": field_type,
            "required": "true",
            "source": source,
            "validation_rule": validation,
            "downstream_metric": metric,
            "forbidden_inference": forbidden,
            "effect": "makes fresh MT5 probe evidence explicit before any forward read(전진 판독 전 신규 MT5 탐침 근거를 명시)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, source, validation, metric, forbidden in fields
    ]


def build_cost_stress_matrix() -> list[dict[str, Any]]:
    rows = [
        ("base", "baseline(기준)", "1.0", "0", "0", "all trades(전체 거래)", "base_net_profit;base_pf;base_dd", "base already weak(기준도 약함)"),
        ("mild_spread", "spread(스프레드)", "1.25", "0", "0", "all trades(전체 거래)", "mild_spread_net;mild_spread_pf", "PF drops below base tolerance(PF가 기준 허용범위 아래로 하락)"),
        ("hard_spread", "spread(스프레드)", "1.50", "0", "0", "all trades(전체 거래)", "hard_spread_net;hard_spread_pf", "edge disappears under hard spread(강한 스프레드에서 엣지 소멸)"),
        ("mild_slippage", "slippage(슬리피지)", "1.0", "1", "0", "entry and exit(진입과 청산)", "mild_slippage_net;mild_slippage_pf", "expectancy turns weak(기대값 약화)"),
        ("hard_slippage", "slippage(슬리피지)", "1.0", "2", "0", "entry and exit(진입과 청산)", "hard_slippage_net;hard_slippage_pf", "drawdown pocket expands(손실 포켓 확대)"),
        ("combined_hard", "combined(합산)", "1.50", "2", "0", "all trades(전체 거래)", "combined_hard_net;combined_hard_dd", "curve breaks under combined costs(합산 비용에서 곡선 붕괴)"),
    ]
    return [
        {
            "stress_id": f"{RUN_NUMBER}_{stress_id}",
            "stress_family": family,
            "spread_multiplier": spread,
            "slippage_points": slip,
            "commission_adjustment": commission,
            "applies_to": applies_to,
            "required_output": output,
            "failure_signal": failure,
            "effect": "prevents fragile profit from passing without execution stress(취약한 수익이 실행 스트레스 없이 통과하지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for stress_id, family, spread, slip, commission, applies_to, output, failure in rows
    ]


def build_lot_schema() -> list[dict[str, Any]]:
    rows = [
        ("trade_id", "string", "trade list(거래 목록)", "must join profit schema(수익 스키마와 조인)", "lot-normalized result(로트 정규화 결과)", "none"),
        ("lot", "float", "trade list(거래 목록)", "lot > 0(로트 양수)", "net_per_lot(로트당 손익)", "lot optimization(로트 최적화)"),
        ("contract_size", "float", "broker symbol spec(브로커 심볼 명세)", "> 0", "risk normalization(위험 정규화)", "unknown contract spec(모르는 계약 명세)"),
        ("point_value", "float", "broker symbol spec(브로커 심볼 명세)", "> 0", "point-normalized PnL(포인트 정규화 손익)", "instrument mismatch(상품 불일치)"),
        ("net_per_lot", "float", "computed by harness(하네스 계산)", "net_profit / lot(순수익 / 로트)", "expectancy per lot(로트당 기대값)", "raw lot-masked KPI(로트에 가려진 원 KPI)"),
        ("dd_per_lot", "float", "computed by harness(하네스 계산)", "drawdown / lot(손실 / 로트)", "risk per lot(로트당 위험)", "drawdown masked by lot(로트에 가려진 손실)"),
    ]
    return [
        {
            "field_id": f"{RUN_NUMBER}_lot_{name}",
            "field_name": name,
            "field_type": field_type,
            "required": "true",
            "source": source,
            "validation_rule": validation,
            "downstream_metric": metric,
            "forbidden_inference": forbidden,
            "effect": "separates signal quality from lot size effects(신호 품질과 로트 크기 효과를 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, source, validation, metric, forbidden in rows
    ]


def build_regime_schema() -> list[dict[str, Any]]:
    rows = [
        ("session", "enum_asia_europe_us_overlap", "bar time(봉 시각)", "computed from broker/UTC policy(브로커/UTC 정책으로 계산)", "session slice(세션 조각)", "session-free conclusion(세션 없는 결론)"),
        ("hour", "int_0_23", "bar time(봉 시각)", "0 <= hour <= 23", "hour slice(시간 조각)", "hour cherry-pick(시간 체리픽)"),
        ("month", "int_1_12", "bar time(봉 시각)", "1 <= month <= 12", "month slice(월 조각)", "month cherry-pick(월 체리픽)"),
        ("volatility_bucket", "enum_low_mid_high", "as-of features(기준시각 피처)", "computed before decision(결정 전 계산)", "volatility slice(변동성 조각)", "future volatility bucket(미래 변동성 구간)"),
        ("adx_bucket", "enum_low_mid_high", "as-of features(기준시각 피처)", "computed before decision(결정 전 계산)", "ADX slice(ADX 조각)", "future ADX(미래 ADX)"),
        ("vix_bucket", "enum_low_mid_high_missing", "as-of macro sidecar(기준시각 거시 사이드카)", "release_time <= as_of_time(발표시각 <= 기준시각)", "VIX slice(VIX 조각)", "future VIX join(미래 VIX 조인)"),
        ("usd_bucket", "enum_weak_mid_strong_missing", "as-of macro sidecar(기준시각 거시 사이드카)", "release_time <= as_of_time(발표시각 <= 기준시각)", "USD slice(USD 조각)", "future USD join(미래 USD 조인)"),
        ("rate_regime", "enum_cut_hold_hike_uncertain_missing", "as-of rate calendar(기준시각 금리 일정)", "known_at <= as_of_time(인지시각 <= 기준시각)", "rate regime slice(금리 국면 조각)", "future rate outcome(미래 금리 결과)"),
    ]
    return [
        {
            "field_id": f"{RUN_NUMBER}_regime_{name}",
            "field_name": name,
            "field_type": field_type,
            "required": "true",
            "source": source,
            "validation_rule": validation,
            "downstream_metric": metric,
            "forbidden_inference": forbidden,
            "effect": "makes regime attribution useful without look-ahead joins(미래참조 조인 없이 국면 귀속을 쓸 수 있게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, source, validation, metric, forbidden in rows
    ]


def build_no_lookahead_schema() -> list[dict[str, Any]]:
    rows = [
        ("as_of_time", "datetime_utc", "harness clock(하네스 시계)", "required for every row(모든 행 필수)", "all gates(모든 게이트)", "implicit now(암묵적 현재시각)"),
        ("bar_close_time", "datetime_utc", "broker bars(브로커 봉)", "bar_close_time <= as_of_time(봉 마감 <= 기준시각)", "completed bar check(완성봉 확인)", "open bar feature(미완성봉 피처)"),
        ("feature_time", "datetime_utc", "feature pipeline(피처 파이프라인)", "feature_time <= decision_time(피처시각 <= 결정시각)", "feature boundary(피처 경계)", "future feature(미래 피처)"),
        ("label_time", "datetime_utc", "trade outcome(거래 결과)", "label_time > decision_time for labels only(라벨 전용이면 라벨시각 > 결정시각)", "label boundary(라벨 경계)", "label in feature(라벨의 피처 유입)"),
        ("release_time", "datetime_utc_or_null", "macro/regime sidecar(거시/국면 사이드카)", "release_time <= as_of_time or null(발표시각 <= 기준시각 또는 null)", "macro as-of check(거시 기준시각 확인)", "future release join(미래 발표 조인)"),
        ("selection_time", "datetime_utc", "experiment ledger(실험 장부)", "selection_time before KPI read(KPI 판독 전 선택시각)", "selection-bias check(선택 편향 확인)", "post-profit selection(수익 확인 후 선택)"),
        ("trade_index_target_used", "bool", "harness audit(하네스 감사)", "must be false(false 필수)", "trade-index guard(거래번호 가드)", "trade index target(거래번호 타깃)"),
    ]
    return [
        {
            "field_id": f"{RUN_NUMBER}_lookahead_{name}",
            "field_name": name,
            "field_type": field_type,
            "required": "true",
            "source": source,
            "validation_rule": validation,
            "downstream_metric": metric,
            "forbidden_inference": forbidden,
            "effect": "keeps the measurement harness from recreating look-ahead bias(측정 하네스가 미래참조 편향을 재생성하지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, source, validation, metric, forbidden in rows
    ]


def build_execution_plan() -> list[dict[str, Any]]:
    rows = [
        ("ingest_mt5_outputs", "1", "ingest fresh MT5 tester report and terminal handoff(신규 MT5 테스터 보고서와 터미널 인계 수집)", aw.rel(MT5_PROBE_MANIFEST), "raw trade list and probe evidence(원거래 목록과 탐침 근거)", "feature_last_reached true before forward use(feature_last 도달 true 전진 사용 전 필수)", "Forward/Runtime/Goal(전진/런타임/목표)"),
        ("build_proxy_diff", "2", "join proxy expected values to MT5 runtime probe values(프록시 예상값과 MT5 런타임 탐침값 조인)", aw.rel(PROXY_MT5_DIFF_SCHEMA), "proxy-MT5 row-level difference(프록시-MT5 행 단위 차이)", "mismatch and usability reviewed(불일치와 사용성 검토)", "proxy KPI authority(프록시 KPI 권위)"),
        ("build_profit_curve", "3", "compute profit/risk/trade-shape curve metrics(수익/위험/거래형태 곡선 지표 계산)", aw.rel(PROFIT_CURVE_SCHEMA), "profit curve report(수익곡선 보고)", "trade list complete and sorted(거래 목록 완전·정렬)", "single KPI selection(단일 KPI 선택)"),
        ("apply_lot_and_cost", "4", "apply lot normalization and cost stress(로트 정규화와 비용 스트레스 적용)", f"{aw.rel(LOT_NORMALIZATION_SCHEMA)};{aw.rel(COST_STRESS_MATRIX)}", "lot-normalized and stressed metrics(로트 정규화 및 스트레스 지표)", "base/mild/hard stress present(기준/약함/강함 스트레스 존재)", "lot optimization(로트 최적화)"),
        ("slice_regimes", "5", "slice by direction/session/hour/month/volatility/ADX/VIX/USD/rate(방향/세션/시간/월/변동성/ADX/VIX/USD/금리 조각)", aw.rel(REGIME_SLICE_SCHEMA), "regime attribution tables(국면 귀속 표)", "as-of release checks pass(기준시각 발표 확인 통과)", "future regime join(미래 국면 조인)"),
        ("run_firewall", "6", "run no-lookahead validation(미래참조 방지 검증)", aw.rel(NO_LOOKAHEAD_VALIDATION_SCHEMA), "firewall audit(방화벽 감사)", "no guard failure(가드 실패 없음)", "valid result claim if guard fails(가드 실패 시 유효 주장)"),
    ]
    return [
        {
            "plan_id": f"{RUN_NUMBER}_{plan_id}",
            "sequence": sequence,
            "work_item": work,
            "required_inputs": inputs,
            "required_outputs": outputs,
            "must_pass_before_next": must_pass,
            "blocked_claims": blocked,
            "status": "materialized_for_review(검토용 물질화)",
            "effect": "orders harness work so parity and leakage gates precede KPI interpretation(동등성·누수 게이트가 KPI 해석보다 앞서게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for plan_id, sequence, work, inputs, outputs, must_pass, blocked in rows
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BJ_review_bounded_measurement_harness",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "bounded measurement harness package(제한 측정 하네스 패키지)",
            "inputs_to_review": ";".join(
                aw.rel(path)
                for path in (
                    HARNESS_COMPONENTS,
                    PROFIT_CURVE_SCHEMA,
                    PROXY_MT5_DIFF_SCHEMA,
                    MT5_PROBE_MANIFEST,
                    COST_STRESS_MATRIX,
                    LOT_NORMALIZATION_SCHEMA,
                    REGIME_SLICE_SCHEMA,
                    NO_LOOKAHEAD_VALIDATION_SCHEMA,
                    HARNESS_EXECUTION_PLAN,
                )
            ),
            "must_confirm": "profit curve, proxy-MT5 expected-vs-runtime, MT5 feature_last, cost stress, lot normalization, regime as-of, no-lookahead gates(수익곡선/프록시-MT5 예상값 대 런타임값/MT5 feature_last/비용 스트레스/로트 정규화/국면 기준시각/미래참조 게이트)",
            "must_reject_if": "training, threshold retune, D/B rewrite, lot optimization, single KPI selection, proxy KPI authority, Forward/Runtime/Goal claim(학습/임계값 재조정/D-B 재작성/로트 최적화/단일 KPI 선택/프록시 KPI 권위/전진·런타임·목표 주장)",
            "expected_outputs": "reviewed harness approval or repair plan only(검토된 하네스 승인 또는 수리 계획만)",
            "priority": "P0",
            "effect": "forces harness review before actual MT5/profit execution(실제 MT5/수익 실행 전 하네스 검토를 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def count_rows(rows: Sequence[Mapping[str, Any]], column: str, value: str) -> int:
    return sum(1 for row in rows if str(row.get(column, "")) == value)


def build_gates(
    src: Mapping[str, Any],
    components: Sequence[Mapping[str, Any]],
    profit_schema: Sequence[Mapping[str, Any]],
    proxy_schema: Sequence[Mapping[str, Any]],
    mt5_manifest: Sequence[Mapping[str, Any]],
    cost_stress: Sequence[Mapping[str, Any]],
    lot_schema: Sequence[Mapping[str, Any]],
    regime_schema: Sequence[Mapping[str, Any]],
    lookahead_schema: Sequence[Mapping[str, Any]],
    execution_plan: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent = src["final"]
    source_gates_passed = sum(1 for row in src["gates"] if row.get("status") == "passed")
    component_families = {row["component_family"] for row in components}
    profit_fields = {row["field_name"] for row in profit_schema}
    proxy_fields = {row["field_name"] for row in proxy_schema}
    mt5_fields = {row["field_name"] for row in mt5_manifest}
    lookahead_fields = {row["field_name"] for row in lookahead_schema}
    gate_specs = [
        ("bi_gate_parent_loaded", parent.get("next_action") == RUN_ID, f"parent_next={parent.get('next_action')}", "run337BH opens run337BI(337BH가 337BI를 엶)"),
        ("bi_gate_parent_gates_passed", parent.get("passed_gates") == parent.get("gate_rows") == 12 and source_gates_passed == 12, f"parent_gates={parent.get('passed_gates')}/{parent.get('gate_rows')};audit={source_gates_passed}/12", "run337BH all gates passed(337BH 모든 게이트 통과)"),
        ("bi_gate_components_complete", len(components) == 7 and any("profit_curve" in family for family in component_families) and any("proxy_mt5" in family for family in component_families), f"components={len(components)}", "seven harness components including profit and proxy(수익과 프록시 포함 7개 하네스 컴포넌트)"),
        ("bi_gate_profit_schema_complete", {"trade_id", "open_time", "close_time", "direction", "source", "lot", "net_profit", "balance_after", "spread_points", "slippage_points"}.issubset(profit_fields), f"profit_fields={len(profit_fields)}", "profit trade schema has required KPI fields(수익 거래 스키마 필수 KPI 필드 보유)"),
        ("bi_gate_proxy_schema_complete", {"proxy_expected_value", "mt5_runtime_probe_value", "difference", "usable_scope"}.issubset(proxy_fields), f"proxy_fields={len(proxy_fields)}", "proxy expected vs MT5 runtime values and usability fields present(프록시 예상값/MT5 런타임값/사용성 필드 존재)"),
        ("bi_gate_mt5_manifest_complete", {"feature_last_timestamp", "tester_last_observed_bar_time", "feature_last_reached", "proxy_mt5_difference_path"}.issubset(mt5_fields), f"mt5_fields={len(mt5_fields)}", "MT5 feature_last and difference outputs required(MT5 feature_last와 차이 출력 필수)"),
        ("bi_gate_cost_stress_complete", len(cost_stress) >= 6 and any(row["stress_id"].endswith("combined_hard") for row in cost_stress), f"cost_stress={len(cost_stress)}", "base/mild/hard/combined stress present(기준/약함/강함/합산 스트레스 존재)"),
        ("bi_gate_lot_schema_complete", {"lot", "net_per_lot", "dd_per_lot"}.issubset({row["field_name"] for row in lot_schema}), f"lot_fields={len(lot_schema)}", "lot-normalized profit and drawdown fields present(로트 정규화 수익/손실 필드 존재)"),
        ("bi_gate_regime_schema_complete", {"session", "hour", "month", "volatility_bucket", "adx_bucket", "vix_bucket", "usd_bucket", "rate_regime"}.issubset({row["field_name"] for row in regime_schema}), f"regime_fields={len(regime_schema)}", "session/hour/month/volatility/ADX/VIX/USD/rate fields present(세션/시간/월/변동성/ADX/VIX/USD/금리 필드 존재)"),
        ("bi_gate_no_lookahead_schema_complete", {"as_of_time", "bar_close_time", "feature_time", "label_time", "release_time", "selection_time", "trade_index_target_used"}.issubset(lookahead_fields), f"lookahead_fields={len(lookahead_fields)}", "time boundary and trade-index guards present(시간 경계와 거래번호 가드 존재)"),
        ("bi_gate_execution_plan_ordered", [row["sequence"] for row in execution_plan] == ["1", "2", "3", "4", "5", "6"], f"plan_sequence={','.join(row['sequence'] for row in execution_plan)}", "ordered execution plan from MT5 evidence to firewall( MT5 근거부터 방화벽까지 순서 계획)"),
        ("bi_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0]["next_run_id"] == NEXT_RUN_ID, f"queue={len(queue_rows)};next={queue_rows[0]['next_run_id'] if queue_rows else 'missing'}", "run337BJ review queue ready(337BJ 검토 대기열 준비)"),
        ("bi_gate_no_forbidden_claims", True, "forward=not_claimed;runtime=not_claimed;goal=not_claimed", "no Forward/Runtime/Goal claim(전진/런타임/목표 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": "blocks actual execution unless measurement harness covers profit, parity, cost, regime, and no-lookahead gates(측정 하네스가 수익/동등성/비용/국면/미래참조 게이트를 커버해야 실제 실행 허용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in gate_specs
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "skill": "obsidian-experiment-design",
                "run_id": RUN_ID,
                "hypothesis": "measurement harness inputs can convert reviewed contracts into executable evidence requirements(측정 하네스 입력이 검토 계약을 실행 가능한 근거 요구사항으로 바꿀 수 있음)",
                "decision_use": "open run337BJ review only, not execution authority(run337BJ 검토만 열고 실행 권위는 열지 않음)",
                "comparison_baseline": PARENT_RUN_ID,
                "control_variables": "cp322A ONNX, threshold, D/B, risk, lot, ATR SL/TP, runtime handoff frozen(cp322A ONNX/임계값/D-B/위험/로트/ATR SLTP/런타임 인계 고정)",
                "changed_variables": "harness input schemas only(하네스 입력 스키마만)",
                "sample_scope": "no new trading data interpreted(새 거래 데이터 해석 없음)",
                "success_criteria": "all harness gates pass and run337BJ queue ready(모든 하네스 게이트 통과와 run337BJ 대기열 준비)",
                "failure_criteria": "missing profit/proxy/MT5/cost/lot/regime/lookahead schema(수익/프록시/MT5/비용/로트/국면/미래참조 스키마 누락)",
                "invalid_conditions": "model training, threshold retune, proxy KPI authority, Forward claim(모델 학습/임계값 재조정/프록시 KPI 권위/전진 주장)",
                "stop_conditions": "failed gate opens repair before execution(게이트 실패 시 실행 전 수리)",
                "evidence_plan": [aw.rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "skill": "obsidian-data-integrity",
                "run_id": RUN_ID,
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "schema requires UTC times, completed bars, feature_time, label_time, release_time(스키마는 UTC 시각/완성봉/피처시각/라벨시각/발표시각 요구)",
                "sample_scope": "schema-only, no KPI sample(스키마 전용, KPI 표본 없음)",
                "missing_or_duplicate_check": "required downstream in trade/proxy rows(하위 거래/프록시 행에서 필수)",
                "feature_label_boundary": "feature_time <= decision_time; label stays out of features(피처시각 <= 결정시각, 라벨은 피처 밖)",
                "split_boundary": "frozen cp322A measurement-only path(cp322A 고정 측정 전용 경로)",
                "leakage_risk": "future release joins and post-profit selection guarded(미래 발표 조인과 수익 확인 후 선택 가드)",
                "data_hash_or_identity": f"artifact_registry_run={RUN_ID}",
                "integrity_judgment": "usable_with_boundary_for_harness_review(하네스 검토에 한해 경계 포함 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "skill": "obsidian-model-validation",
                "run_id": RUN_ID,
                "model_family": "cp322A frozen ONNX package(cp322A 고정 ONNX 패키지)",
                "target_and_label": "unchanged and not rebuilt(변경 없고 재구축 없음)",
                "split_method": "schema-only, no split mutation(스키마 전용, 분할 변경 없음)",
                "selection_metric": "none; no selection(없음, 선택 없음)",
                "secondary_metrics": "future measurement metrics only(미래 측정 지표 전용)",
                "threshold_policy": "fixed frozen threshold(고정 임계값)",
                "overfit_risk": "single-KPI selection, date-fit, trade-index target blocked(단일 KPI 선택/날짜 맞춤/거래번호 타깃 차단)",
                "calibration_risk": "score fields not probabilities(점수 필드는 확률 아님)",
                "comparison_baseline": PARENT_RUN_ID,
                "validation_judgment": "research_harness_inputs_only(연구 하네스 입력 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "skill": "obsidian-runtime-parity",
                "run_id": RUN_ID,
                "research_path": aw.rel(Path(__file__)),
                "runtime_path": "MT5 runtime not executed; manifest schema only(MT5 런타임 미실행, 목록 스키마 전용)",
                "shared_contract": "proxy expected value and MT5 runtime probe value difference schema(프록시 예상값과 MT5 런타임 탐침값 차이 스키마)",
                "known_differences": "tester_feature_last_gap remains until actual probe(실제 탐침 전까지 tester_feature_last 공백 유지)",
                "parity_check": "schema materialized, no runtime authority(스키마 물질화, 런타임 권위 없음)",
                "parity_identity": f"parent={PARENT_RUN_ID};harness={RUN_ID}",
                "runtime_claim_boundary": "research_only_no_runtime_authority(연구 전용, 런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "skill": "obsidian-performance-attribution",
                "run_id": RUN_ID,
                "observed_change": "measurement schemas materialized; no trading KPI observed(측정 스키마 물질화, 거래 KPI 관측 없음)",
                "comparison_baseline": PARENT_RUN_ID,
                "likely_drivers": "not_applicable_until_trade_list(거래 목록 전까지 해당 없음)",
                "segment_checks": "direction/session/hour/month/volatility/ADX/VIX/USD/rate schema present(방향/세션/시간/월/변동성/ADX/VIX/USD/금리 스키마 존재)",
                "trade_shape": "schema ready, not measured(스키마 준비, 미측정)",
                "alternative_explanations": "harness can still reject actual MT5 data(하네스가 실제 MT5 데이터를 거절할 수 있음)",
                "attribution_confidence": "inconclusive_by_design(설계상 불충분)",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "skill": "obsidian-artifact-lineage",
                "run_id": RUN_ID,
                "source_inputs": [aw.rel(path) for path in INPUT_FILES],
                "producer": aw.rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [aw.rel(path) for path in OUTPUT_FILES],
                "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
                "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
                "availability": "tracked_and_reproducible_from_script(추적됨, 스크립트로 재현 가능)",
                "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "skill": "obsidian-result-judgment",
                "run_id": RUN_ID,
                "result_subject": "bounded measurement harness inputs(제한 측정 하네스 입력)",
                "evidence_available": [aw.rel(path) for path in OUTPUT_FILES],
                "evidence_missing": "actual MT5 runtime probe, forward trade list, computed KPI(실제 MT5 런타임 탐침/전진 거래 목록/계산 KPI)",
                "judgment_label": "exploratory_harness_inputs_materialized(탐색 하네스 입력 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "측정 틀은 더 구체화됐지만 아직 실제 수익 검증은 아니다.",
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BI Measurement Harness Inputs(337단계 337BI 측정 하네스 입력)

## Conclusion(결론)

run337BI(337BI 실행)는 profit curve(수익곡선), proxy-MT5 difference(프록시-MT5 차이), MT5 runtime probe(MT5 런타임 탐침), cost stress(비용 스트레스), lot normalization(로트 정규화), regime slices(국면 조각), no-lookahead validation(미래참조 방지 검증) 스키마를 물질화했다.

Effect(효과): 다음 run337BJ(337BJ 실행)는 실제 MT5/profit execution(MT5/수익 실행) 전에 이 하네스가 충분한지 검토할 수 있다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- components(컴포넌트): `{final['component_rows']}`
- profit_fields(수익 필드): `{final['profit_schema_rows']}`
- proxy_fields(프록시 필드): `{final['proxy_schema_rows']}`
- mt5_manifest_fields(MT5 목록 필드): `{final['mt5_manifest_rows']}`
- cost_stress_rows(비용 스트레스 행): `{final['cost_stress_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

아직 MT5 runtime probe(MT5 런타임 탐침), forward trade list(전진 거래 목록), computed KPI(계산 KPI)는 없다. 따라서 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BI Measurement Harness(결정: 337단계 337BI 측정 하네스)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): 수익곡선 중심 자동매매 검증을 실제 계산 직전까지 끌고 가되, cp322A freeze(고정)와 no-lookahead(미래참조 방지)를 유지한다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bh.bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BI focus")
    workspace = bh.bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        f"- >-\n  Stage337 run337BI focus complete: run337BI(337BI 실행)은 `{final['status']}`로 "
        f"bounded measurement harness inputs(제한 측정 하네스 입력)를 물질화했다. Effect(효과): "
        f"components(컴포넌트) `{final['component_rows']}`, profit fields(수익 필드) `{final['profit_schema_rows']}`, "
        f"proxy fields(프록시 필드) `{final['proxy_schema_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 "
        f"Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bh.bg.remove_markdown_section(current_text, "## Stage337 run337BI(337BI 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bh.bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BI(337BI 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BI(337BI 실행)는 수익곡선/프록시-MT5/MT5 탐침/비용/로트/국면/미래참조 측정 하네스 입력을 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.

"""
    marker = "## Stage337 run337BH"
    current = current.replace(marker, entry + marker, 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- harness_component_rows(하네스 컴포넌트 행): `{final['component_rows']}`
- profit_schema_rows(수익 스키마 행): `{final['profit_schema_rows']}`
- proxy_mt5_schema_rows(프록시-MT5 스키마 행): `{final['proxy_schema_rows']}`
- mt5_probe_manifest_rows(MT5 탐침 목록 행): `{final['mt5_manifest_rows']}`
- cost_stress_rows(비용 스트레스 행): `{final['cost_stress_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_measurement_harness_review_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BI(337BI 실행)는 측정 하네스 입력만 물질화했고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief_text, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_text = bh.bg.remove_lines_containing(brief_text, "run337BI(337BI 실행):")
    brief_line = (
        f"\n- run337BI(337BI 실행): `{final['status']}`. Effect(효과): measurement harness(측정 하네스) 입력을 물질화했고 "
        f"Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief_text.rstrip() + brief_line, brief_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = bh.bg.remove_lines_containing(changelog_text, f",{RUN_ID},")
    changelog_line = f"{TODAY},Stage337,{RUN_ID},{final['status']},{final['judgment']},{aw.rel(REPORT_PATH)}\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_line, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_measurement_harness_inputs_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_execution",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__harness_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "harness_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BI bounded measurement harness inputs",
        "tier_scope": "research_harness_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"components={final['component_rows']};profit_fields={final['profit_schema_rows']};proxy_fields={final['proxy_schema_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;proxy_expected_vs_mt5_runtime_required;feature_last_required;no_lookahead;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_harness_inputs_only(주장 범위 밖, 하네스 입력 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__harness_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337BH reviewed scaffold inputs",
        "kpi_scope": "harness_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__harness_inputs",
        "family": "bounded_measurement_harness_inputs_without_db",
        "question": "can reviewed contracts become executable measurement harness inputs without surface mutation",
        "metric_scope": "profit_curve_proxy_mt5_mt5_gap_cost_lot_regime_no_lookahead",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    components = build_components()
    component_path = aw.write_csv(HARNESS_COMPONENTS, COMPONENT_COLUMNS, components)
    profit_schema = build_profit_schema()
    profit_path = aw.write_csv(PROFIT_CURVE_SCHEMA, SCHEMA_COLUMNS, profit_schema)
    proxy_schema = build_proxy_schema()
    proxy_path = aw.write_csv(PROXY_MT5_DIFF_SCHEMA, SCHEMA_COLUMNS, proxy_schema)
    mt5_manifest = build_mt5_probe_manifest()
    mt5_path = aw.write_csv(MT5_PROBE_MANIFEST, SCHEMA_COLUMNS, mt5_manifest)
    cost_stress = build_cost_stress_matrix()
    stress_path = aw.write_csv(COST_STRESS_MATRIX, STRESS_COLUMNS, cost_stress)
    lot_schema = build_lot_schema()
    lot_path = aw.write_csv(LOT_NORMALIZATION_SCHEMA, SCHEMA_COLUMNS, lot_schema)
    regime_schema = build_regime_schema()
    regime_path = aw.write_csv(REGIME_SLICE_SCHEMA, SCHEMA_COLUMNS, regime_schema)
    lookahead_schema = build_no_lookahead_schema()
    lookahead_path = aw.write_csv(NO_LOOKAHEAD_VALIDATION_SCHEMA, SCHEMA_COLUMNS, lookahead_schema)
    execution_plan = build_execution_plan()
    plan_path = aw.write_csv(HARNESS_EXECUTION_PLAN, PLAN_COLUMNS, execution_plan)
    queue_rows = build_queue()
    queue_path = aw.write_csv(RUN337BJ_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, components, profit_schema, proxy_schema, mt5_manifest, cost_stress, lot_schema, regime_schema, lookahead_schema, execution_plan, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BI_measurement_harness_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_measurement_harness_input_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BI_measurement_harness_before_review",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BI_measurement_harness_gate_failure_v1",
        "component_rows": len(components),
        "profit_schema_rows": len(profit_schema),
        "proxy_schema_rows": len(proxy_schema),
        "mt5_manifest_rows": len(mt5_manifest),
        "cost_stress_rows": len(cost_stress),
        "lot_schema_rows": len(lot_schema),
        "regime_schema_rows": len(regime_schema),
        "lookahead_schema_rows": len(lookahead_schema),
        "execution_plan_rows": len(execution_plan),
        "queue_rows": len(queue_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(__file__),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(로트 최적화)",
            "single KPI selection(단일 KPI 선택)",
            "proxy KPI authority(프록시 KPI 권위)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "runtime authority claim(런타임 권위 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "external_verification_status": "out_of_scope_by_claim_harness_inputs_only(주장 범위 밖, 하네스 입력 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        component_path,
        profit_path,
        proxy_path,
        mt5_path,
        stress_path,
        lot_path,
        regime_path,
        lookahead_path,
        plan_path,
        queue_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "components": final["component_rows"],
                "profit_fields": final["profit_schema_rows"],
                "proxy_fields": final["proxy_schema_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
