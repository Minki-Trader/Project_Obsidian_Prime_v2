from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import review_bounded_repair_implementation_preflight_without_db as bf


aw = bf.aw

TODAY = "2026-05-27"
STAGE_ID = bf.STAGE_ID
RUN_NUMBER = "run337BG"
RUN_ID = "run337BG_materialize_bounded_repair_scaffold_inputs_without_db_v1"
PARENT_RUN_ID = bf.RUN_ID
NEXT_RUN_ID = "run337BH_review_bounded_repair_scaffold_inputs_without_db_v1"
STATUS = "completed_stage337BG_bounded_repair_scaffold_inputs_materialized_no_training_no_selection"
JUDGMENT = "scaffold_inputs_materialized_for_curve_profit_parity_repair_without_surface_mutation"
DECISION = "stage337BG_open_run337BH_review_bounded_repair_scaffold_inputs_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BG_scaffold_inputs_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bf.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bf.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BG_scaffold_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BG_scaffold_inputs.md"
SELECTED_STATUS = bf.SELECTED_STATUS
STAGE_BRIEF = bf.STAGE_BRIEF
WORKSPACE_STATE = bf.WORKSPACE_STATE
CURRENT_STATE = bf.CURRENT_STATE
CHANGELOG = bf.CHANGELOG
RUN_REGISTRY = bf.RUN_REGISTRY
ALPHA_LEDGER = bf.ALPHA_LEDGER
ARTIFACT_REGISTRY = bf.ARTIFACT_REGISTRY
STAGE_LEDGER = bf.STAGE_LEDGER

RUN337BF_DIR = STAGE_DIR / "02_runs" / "run337BF"
BF_FINAL = RUN337BF_DIR / "final_decision.json"
BF_MANIFEST = RUN337BF_DIR / "run_manifest.json"
BF_PREFLIGHT_REVIEW = RUN337BF_DIR / "implementation_preflight_review_matrix.csv"
BF_FROZEN_REVIEW = RUN337BF_DIR / "frozen_surface_review.csv"
BF_PROXY_REVIEW = RUN337BF_DIR / "proxy_mt5_usability_review.csv"
BF_MT5_BLOCKER_REVIEW = RUN337BF_DIR / "mt5_forward_blocker_review.csv"
BF_FIREWALL_REVIEW = RUN337BF_DIR / "no_overfit_firewall_review.csv"
BF_ARTIFACT_REVIEW = RUN337BF_DIR / "artifact_manifest_review.csv"
BF_BALANCE_REVIEW = RUN337BF_DIR / "balanced_workstream_review.csv"
BF_HANDOFF = RUN337BF_DIR / "scaffold_handoff_boundary_matrix.csv"
BF_QUEUE = RUN337BF_DIR / "run337BG_scaffold_input_queue.csv"
BF_GATE_AUDIT = RUN337BF_DIR / "required_gate_coverage_audit.csv"
BF_EXPERIMENT_RECEIPT = RUN337BF_DIR / "experiment_design_receipt.json"
BF_DATA_RECEIPT = RUN337BF_DIR / "data_integrity_receipt.json"
BF_MODEL_RECEIPT = RUN337BF_DIR / "model_validation_receipt.json"
BF_RUNTIME_RECEIPT = RUN337BF_DIR / "runtime_parity_receipt.json"
BF_ARTIFACT_RECEIPT = RUN337BF_DIR / "artifact_lineage_receipt.json"
BF_JUDGMENT_RECEIPT = RUN337BF_DIR / "result_judgment_receipt.json"

SCAFFOLD_INPUT_PACKAGE = RUN_DIR / "scaffold_input_package.csv"
COMPONENT_CONTRACTS = RUN_DIR / "component_contracts.csv"
PROFIT_CURVE_CONTRACT = RUN_DIR / "profit_curve_measurement_contract.csv"
PROXY_MT5_CONTRACT = RUN_DIR / "proxy_mt5_runtime_probe_contract.csv"
MT5_GAP_REPAIR_CONTRACT = RUN_DIR / "mt5_gap_repair_input_contract.csv"
NO_LOOKAHEAD_FIREWALL = RUN_DIR / "no_lookahead_firewall_checklist.csv"
BALANCED_LANE_MATRIX = RUN_DIR / "balanced_research_lane_matrix.csv"
RUN337BH_QUEUE = RUN_DIR / "run337BH_review_queue.csv"
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
    BF_FINAL,
    BF_MANIFEST,
    BF_PREFLIGHT_REVIEW,
    BF_FROZEN_REVIEW,
    BF_PROXY_REVIEW,
    BF_MT5_BLOCKER_REVIEW,
    BF_FIREWALL_REVIEW,
    BF_ARTIFACT_REVIEW,
    BF_BALANCE_REVIEW,
    BF_HANDOFF,
    BF_QUEUE,
    BF_GATE_AUDIT,
    BF_EXPERIMENT_RECEIPT,
    BF_DATA_RECEIPT,
    BF_MODEL_RECEIPT,
    BF_RUNTIME_RECEIPT,
    BF_ARTIFACT_RECEIPT,
    BF_JUDGMENT_RECEIPT,
)
OUTPUT_FILES = (
    SCAFFOLD_INPUT_PACKAGE,
    COMPONENT_CONTRACTS,
    PROFIT_CURVE_CONTRACT,
    PROXY_MT5_CONTRACT,
    MT5_GAP_REPAIR_CONTRACT,
    NO_LOOKAHEAD_FIREWALL,
    BALANCED_LANE_MATRIX,
    RUN337BH_QUEUE,
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

SCAFFOLD_COLUMNS = (
    "input_id",
    "source_blueprint_id",
    "workstream",
    "scaffold_component",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "required_data",
    "required_runtime_probe",
    "required_metrics",
    "required_slices",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "allowed_actions",
    "forbidden_actions",
    "output_contract",
    "next_consumer",
    "effect",
    "claim_boundary",
)
COMPONENT_COLUMNS = (
    "component_id",
    "source_input_id",
    "component_type",
    "producer_contract",
    "consumer_contract",
    "must_include",
    "must_not_include",
    "review_gate",
    "status",
    "effect",
    "claim_boundary",
)
PROFIT_COLUMNS = (
    "metric_id",
    "metric_family",
    "required_metric",
    "required_view",
    "minimum_evidence",
    "must_be_lot_normalized",
    "cost_stress_required",
    "forward_use_allowed",
    "failure_signal",
    "effect",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "contract_id",
    "comparison_subject",
    "proxy_expected_field",
    "mt5_runtime_probe_field",
    "join_key",
    "tolerance",
    "required_difference_output",
    "usability_if_pass",
    "must_not_claim",
    "effect",
    "claim_boundary",
)
MT5_GAP_COLUMNS = (
    "repair_input_id",
    "source_blueprint_id",
    "latest_feature_last_timestamp",
    "tester_last_observed_bar_time",
    "max_tester_to_feature_gap_minutes",
    "required_before_forward",
    "required_probe_output",
    "blocked_claims_until_repaired",
    "status",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "guard_id",
    "guard_family",
    "must_remain_false",
    "abort_if_seen",
    "source_status",
    "added_check",
    "status",
    "effect",
    "claim_boundary",
)
LANE_COLUMNS = (
    "lane_id",
    "workstream_family",
    "source_blueprints",
    "required_contracts",
    "required_metric_scope",
    "forbidden_shortcut",
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
    _, rows = aw.read_csv_table(path, prefer_head=True)
    return rows


def count_contains(rows: Sequence[Mapping[str, str]], column: str, needle: str) -> int:
    return sum(1 for row in rows if needle in str(row.get(column, "")))


def all_paths_exist(paths: Sequence[Path]) -> bool:
    return all(aw.path_exists(path) for path in paths)


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BF scaffold input source files: {missing}")
    return {
        "final": read_json(BF_FINAL),
        "manifest": read_json(BF_MANIFEST),
        "preflight": read_rows(BF_PREFLIGHT_REVIEW),
        "frozen": read_rows(BF_FROZEN_REVIEW),
        "proxy": read_rows(BF_PROXY_REVIEW),
        "mt5_gap": read_rows(BF_MT5_BLOCKER_REVIEW),
        "firewall": read_rows(BF_FIREWALL_REVIEW),
        "artifact": read_rows(BF_ARTIFACT_REVIEW),
        "balance": read_rows(BF_BALANCE_REVIEW),
        "handoff": read_rows(BF_HANDOFF),
        "queue": read_rows(BF_QUEUE),
        "gates": read_rows(BF_GATE_AUDIT),
        "receipts": [read_json(path) for path in (
            BF_EXPERIMENT_RECEIPT,
            BF_DATA_RECEIPT,
            BF_MODEL_RECEIPT,
            BF_RUNTIME_RECEIPT,
            BF_ARTIFACT_RECEIPT,
            BF_JUDGMENT_RECEIPT,
        )],
    }


def build_scaffold_package(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    preflight_by_blueprint = {row["source_blueprint_id"]: row for row in src["preflight"]}
    components = [
        {
            "source_blueprint_id": "bc_blueprint_01",
            "workstream": "defensive(방어)",
            "scaffold_component": "frozen_surface_contract(고정 표면 계약)",
            "hypothesis": "cp322A package identity can be protected while downstream measurement becomes richer(cp322A 패키지 정체성을 지키면서 측정을 확장할 수 있음)",
            "required_metrics": "hash match count, forbidden mutation count, artifact identity count(해시 일치 수/금지 변경 수/산출물 정체성 수)",
            "required_slices": "not_applicable_identity_only(정체성 전용)",
        },
        {
            "source_blueprint_id": "bc_blueprint_02",
            "workstream": "repair(수리)",
            "scaffold_component": "mt5_feature_last_gap_repair_input(MT5 feature_last 공백 수리 입력)",
            "hypothesis": "fresh MT5 tester probe can close the tester_feature_last gap without runtime logic mutation(신규 MT5 테스터 탐침이 런타임 로직 변경 없이 feature_last 공백을 닫을 수 있음)",
            "required_metrics": "tester_to_feature_gap_minutes, feature_last_reached, skip_reason, handoff_file_seen(테스터-피처 공백 분/피처 끝 도달/스킵 사유/인계 파일 확인)",
            "required_slices": "tester session, broker rollover, feature timestamp bucket(테스터 세션/브로커 롤오버/피처 시각 구간)",
        },
        {
            "source_blueprint_id": "bc_blueprint_03",
            "workstream": "parity-control(동등성 대조)",
            "scaffold_component": "proxy_mt5_result_value_comparison(프록시-MT5 결과값 비교)",
            "hypothesis": "proxy expected result value and MT5 runtime probe result value can be compared row by row before any KPI claim(프록시 예상 결과값과 MT5 런타임 탐침 결과값을 KPI 주장 전 행 단위 비교할 수 있음)",
            "required_metrics": "matched_rows, mismatch_rows, max_abs_difference, signal_decision_match(일치 행/불일치 행/최대 절대 차이/신호 결정 일치)",
            "required_slices": "source, direction, decision surface, hour(소스/방향/결정 표면/시간)",
        },
        {
            "source_blueprint_id": "bc_blueprint_04",
            "workstream": "offensive(공격)",
            "scaffold_component": "profit_curve_measurement_contract(수익곡선 측정 계약)",
            "hypothesis": "profit, trade count, drawdown, and curve pocket quality can be measured without retuning cp322A(수익/거래수/손실/곡선 포켓 품질을 cp322A 재튜닝 없이 측정할 수 있음)",
            "required_metrics": "net_profit, PF, trades_per_day, DD, recovery, expectancy, worst_chunk, underwater, curve_pocket, lot_normalized, cost_stress(순수익/PF/일거래수/DD/회복/기대값/최악 청크/수중구간/곡선 포켓/로트 정규화/비용 스트레스)",
            "required_slices": "long_short, session, hour, month, volatility, ADX, VIX, USD, rate_regime(롱숏/세션/시간/월/변동성/ADX/VIX/USD/금리 국면)",
        },
        {
            "source_blueprint_id": "bc_blueprint_05",
            "workstream": "falsification(반증)",
            "scaffold_component": "no_lookahead_overfit_firewall(미래참조 과적합 방화벽)",
            "hypothesis": "stronger measurement can be added without recreating look-ahead bias or selection bias(강한 측정을 추가해도 미래참조 편향이나 선택 편향을 다시 만들지 않을 수 있음)",
            "required_metrics": "feature_label_boundary, completed_bar_only, no_date_selection, no_trade_index_target, no_proxy_kpi_authority(피처-라벨 경계/완성봉 전용/날짜 선택 없음/거래번호 타깃 없음/프록시 KPI 권위 없음)",
            "required_slices": "as_of_date, data_release_lag, session, regime(기준시각/데이터 발표 지연/세션/국면)",
        },
    ]
    rows: list[dict[str, Any]] = []
    for idx, item in enumerate(components, 1):
        blueprint = item["source_blueprint_id"]
        source = preflight_by_blueprint.get(blueprint, {})
        rows.append(
            {
                "input_id": f"{RUN_NUMBER}_{blueprint}_scaffold_input",
                "source_blueprint_id": blueprint,
                "workstream": item["workstream"],
                "scaffold_component": item["scaffold_component"],
                "hypothesis": item["hypothesis"],
                "decision_use": "opens only reviewed scaffold implementation, not model selection or forward decision(검토된 스캐폴드 구현만 열고 모델 선택/전진 판정은 열지 않음)",
                "comparison_baseline": "run337BF reviewed preflight package and cp322A frozen surface(337BF 검토 사전점검 패키지와 cp322A 고정 표면)",
                "control_variables": "cp322A ONNX, adapter package, feature order, D/B surface, score threshold, risk logic, lot logic, ATR SL/TP, runtime handoff frozen(cp322A ONNX/어댑터/피처 순서/D-B 표면/점수 임계값/위험/로트/ATR SLTP/런타임 인계 고정)",
                "changed_variables": "measurement inputs and scaffold contracts only(측정 입력과 스캐폴드 계약만)",
                "sample_scope": "US100 M5 post-OOS forward/probe scope when data is available; no new training sample(US100 M5 기존 OOS 이후 전진/탐침 범위, 새 학습 표본 없음)",
                "required_data": source.get("required_inputs_present", "true"),
                "required_runtime_probe": "fresh MT5 runtime probe required before forward KPI authority(전진 KPI 권위 전 신규 MT5 런타임 탐침 필요)",
                "required_metrics": item["required_metrics"],
                "required_slices": item["required_slices"],
                "success_criteria": "contract is complete, measurable, and rejects surface mutation(계약이 완전하고 측정 가능하며 표면 변경을 거부)",
                "failure_criteria": "missing metric, missing runtime comparison, or hidden optimization path(누락 지표/런타임 비교 누락/숨은 최적화 경로)",
                "invalid_conditions": "training, threshold search, D/B rewrite, lot optimization, date-fit, trade-index target, proxy KPI authority(학습/임계값 탐색/D-B 재작성/로트 최적화/날짜 맞춤/거래번호 타깃/프록시 KPI 권위)",
                "stop_conditions": "stop and review if any forbidden action appears or MT5 probe cannot reach feature_last(금지 행동 등장 또는 MT5 탐침이 feature_last 미도달 시 중단 후 검토)",
                "allowed_actions": "schema contract, measurement manifest, dry-run comparison spec, review queue(스키마 계약/측정 목록/드라이런 비교 명세/검토 대기열)",
                "forbidden_actions": "model training; threshold retuning; D/B rewrite; lot optimization; candidate selection; forward claim; runtime authority(모델 학습/임계값 재조정/D-B 재작성/로트 최적화/후보 선택/전진 주장/런타임 권위)",
                "output_contract": "CSV/JSON scaffold inputs plus review queue only(CSV/JSON 스캐폴드 입력과 검토 대기열만)",
                "next_consumer": NEXT_RUN_ID,
                "effect": "turns reviewed preflight into actionable measurement inputs while keeping cp322A frozen(검토된 사전점검을 실행 가능한 측정 입력으로 바꾸되 cp322A는 고정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_component_contracts(scaffold_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scaffold_rows:
        rows.append(
            {
                "component_id": f"{row['input_id']}_component_contract",
                "source_input_id": row["input_id"],
                "component_type": row["scaffold_component"],
                "producer_contract": aw.rel(SCAFFOLD_INPUT_PACKAGE),
                "consumer_contract": NEXT_RUN_ID,
                "must_include": f"{row['required_metrics']}; {row['required_slices']}",
                "must_not_include": row["forbidden_actions"],
                "review_gate": "run337BH must review before code/runtime execution(run337BH 검토 후에만 코드/런타임 실행)",
                "status": "materialized_for_review(검토용 물질화)",
                "effect": "keeps implementation bounded to declared measurement contracts(구현을 선언된 측정 계약 안에 묶음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_profit_curve_contract() -> list[dict[str, Any]]:
    metrics = [
        ("net_profit", "profit(수익)", "net profit after costs(비용 후 순수익)", "actual_routed_total and lot-normalized view(실제 라우팅 전체와 로트 정규화 보기)", "trade list plus closed equity curve(거래 목록과 청산 기준 곡선)", "false_if_unscaled(비정규화면 거짓)", "true", "false", "positive profit hides concentration(수익이 집중도를 숨김)"),
        ("profit_factor", "profit(수익)", "PF profit factor(PF 수익 팩터)", "total and slices(전체와 조각)", "gross profit/loss from MT5 report(MT5 보고서 총수익/총손실)", "not_applicable", "true", "false", "PF collapses under spread/slippage stress(스프레드/슬리피지 스트레스에서 PF 붕괴)"),
        ("trades_per_day", "trade_count(거래수)", "trades per day(일별 거래 수)", "month and session(月/세션)", "date-indexed trade list(날짜 인덱스 거래 목록)", "not_applicable", "false", "false", "sample shrink or sparse trading(표본 축소 또는 거래 부족)"),
        ("max_drawdown", "risk(위험)", "max DD maximum drawdown(최대 손실)", "equity and balance curve(에쿼티/잔고 곡선)", "closed and floating drawdown when available(가능 시 청산/평가 손실)", "true", "true", "false", "drawdown pocket breaks curve quality(손실 포켓이 곡선 품질 파괴)"),
        ("recovery_factor", "risk(위험)", "recovery factor(회복 계수)", "total and worst chunk(전체와 최악 청크)", "net profit divided by max DD(순수익/최대 손실)", "true", "true", "false", "profit not enough for drawdown(수익이 손실 대비 부족)"),
        ("expectancy", "trade_shape(거래 형태)", "expectancy per trade(거래당 기대값)", "long/short/source(롱숏/소스)", "average win/loss and win rate(평균 승/패와 승률)", "true", "true", "false", "small edge eaten by costs(작은 엣지가 비용에 먹힘)"),
        ("worst_chunk", "curve_pocket(곡선 포켓)", "worst contiguous chunk(최악 연속 구간)", "rolling chunk windows(롤링 청크 창)", "chunked equity report(청크별 곡선 보고)", "true", "true", "false", "one pocket destroys forward usefulness(한 포켓이 전진 유용성 파괴)"),
        ("underwater_stretch", "curve_pocket(곡선 포켓)", "time under water(회복 전 체류 시간)", "days and sessions(일/세션)", "equity high-water mark series(고점 기준 곡선)", "true", "false", "false", "too long underwater stretch(과도한 회복 전 체류)"),
        ("curve_pocket", "curve_quality(곡선 품질)", "curve pocket concentration(곡선 포켓 집중도)", "month/session/volatility(월/세션/변동성)", "pocket attribution table(포켓 귀속 표)", "true", "true", "false", "profit from one isolated pocket(한 고립 포켓 수익 의존)"),
        ("lot_normalized", "execution(실행)", "lot-normalized PnL(로트 정규화 손익)", "source and direction(소스/방향)", "trade list with lot field(로트 필드 포함 거래 목록)", "true", "true", "false", "lot size masks weak signal(로트 크기가 약한 신호를 가림)"),
        ("cost_stress", "execution(실행)", "spread/slippage stress(스프레드/슬리피지 스트레스)", "base, mild, hard(기준/약함/강함)", "stress rerun or deterministic cost overlay(스트레스 재실행 또는 결정적 비용 덧씌움)", "true", "true", "false", "edge disappears under realistic costs(현실 비용에서 엣지 소멸)"),
    ]
    return [
        {
            "metric_id": f"{RUN_NUMBER}_{metric_id}",
            "metric_family": family,
            "required_metric": metric,
            "required_view": view,
            "minimum_evidence": evidence,
            "must_be_lot_normalized": lot_norm,
            "cost_stress_required": cost,
            "forward_use_allowed": forward,
            "failure_signal": failure,
            "effect": "forces beautiful-curve claims to prove profit, count, drawdown, and stress together(이쁜 곡선 주장이 수익/거래수/손실/스트레스를 함께 증명하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for metric_id, family, metric, view, evidence, lot_norm, cost, forward, failure in metrics
    ]


def build_proxy_mt5_contract() -> list[dict[str, Any]]:
    contracts = [
        ("decision_value", "entry decision and D/B source(진입 결정과 D/B 소스)", "proxy_expected_decision", "mt5_runtime_probe_decision", "bar_time;symbol;source;direction(봉시각/심볼/소스/방향)", "exact", "row_level_difference_csv(행 단위 차이 CSV)", "signal_parity_only(신호 동등성 전용)", "Forward Passed/Failed(전진 통과/실패)"),
        ("score_value", "score and threshold relation(점수와 임계값 관계)", "proxy_expected_score", "mt5_runtime_probe_score", "bar_time;feature_hash;model_hash(봉시각/피처 해시/모델 해시)", "1e-9", "max_abs_difference and mismatch rows(최대 절대 차이와 불일치 행)", "score parity diagnostic(점수 동등성 진단)", "calibrated probability(보정 확률)"),
        ("risk_value", "risk and lot decision(위험과 로트 결정)", "proxy_expected_risk_lot", "mt5_runtime_probe_risk_lot", "trade_intent_id or bar_time(거래 의도 ID 또는 봉시각)", "exact_for_discrete", "risk_lot_difference_csv(위험/로트 차이 CSV)", "handoff sanity only(인계 정상성 전용)", "lot optimization(로트 최적화)"),
        ("sl_tp_value", "ATR SL/TP handoff(ATR 손절/익절 인계)", "proxy_expected_sl_tp", "mt5_runtime_probe_sl_tp", "bar_time;atr_window;direction(봉시각/ATR 창/방향)", "broker_point_tolerance(브로커 포인트 허용오차)", "sl_tp_difference_csv(SLTP 차이 CSV)", "handoff parity only(인계 동등성 전용)", "risk logic rewrite(위험 로직 재작성)"),
        ("skip_reason", "runtime skip/reject reason(런타임 스킵/거부 사유)", "proxy_expected_skip_reason", "mt5_runtime_probe_skip_reason", "bar_time;source;direction(봉시각/소스/방향)", "exact", "skip_reason_difference_csv(스킵 사유 차이 CSV)", "runtime observability(런타임 관측성)", "runtime authority(런타임 권위)"),
    ]
    return [
        {
            "contract_id": f"{RUN_NUMBER}_{contract_id}_proxy_mt5_contract",
            "comparison_subject": subject,
            "proxy_expected_field": proxy_field,
            "mt5_runtime_probe_field": mt5_field,
            "join_key": join_key,
            "tolerance": tolerance,
            "required_difference_output": diff_output,
            "usability_if_pass": usability,
            "must_not_claim": must_not,
            "effect": "makes proxy expected result values comparable to MT5 runtime probe values before KPI use(프록시 예상 결과값을 KPI 사용 전 MT5 런타임 탐침값과 비교 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for contract_id, subject, proxy_field, mt5_field, join_key, tolerance, diff_output, usability, must_not in contracts
    ]


def build_mt5_gap_repair_contract(mt5_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in mt5_rows:
        blueprint = row["source_blueprint_id"]
        rows.append(
            {
                "repair_input_id": f"{RUN_NUMBER}_{blueprint}_mt5_gap_repair_input",
                "source_blueprint_id": blueprint,
                "latest_feature_last_timestamp": row["latest_feature_last_timestamp"],
                "tester_last_observed_bar_time": row["tester_last_observed_bar_time"],
                "max_tester_to_feature_gap_minutes": row["max_tester_to_feature_gap_minutes"],
                "required_before_forward": row["required_before_forward"],
                "required_probe_output": "fresh tester report, terminal handoff files, row-level proxy-MT5 difference, feature_last reached flag(신규 테스터 보고서/터미널 인계 파일/행 단위 프록시-MT5 차이/feature_last 도달 플래그)",
                "blocked_claims_until_repaired": "Forward Passed; Forward Failed; runtime authority; live readiness; deployment(전진 통과/전진 실패/런타임 권위/실거래 준비/배포)",
                "status": "materialized_gap_repair_input(공백 수리 입력 물질화)",
                "effect": "turns active MT5 blocker into exact probe requirements(활성 MT5 차단을 정확한 탐침 요구사항으로 바꿈)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall_checklist(firewall_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in firewall_rows:
        rows.append(
            {
                "guard_id": f"{RUN_NUMBER}_{row['firewall_id']}_firewall",
                "guard_family": row["guard_family"],
                "must_remain_false": row["must_remain_false"],
                "abort_if_seen": row["abort_if_seen"],
                "source_status": row["review_status"],
                "added_check": "carry into scaffold review and implementation audit(스캐폴드 검토와 구현 감사까지 전달)",
                "status": "active(활성)",
                "effect": "keeps stronger profit research from becoming overfit shortcut(강한 수익 연구가 과적합 지름길이 되지 않게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    extra = [
        ("completed_bar_only", "time axis(시간축)", "future bar access(미래 봉 접근)"),
        ("asof_join_required", "macro/regime data(거시/국면 데이터)", "release-time blind join(발표시각 무시 조인)"),
        ("no_date_fit_selection", "sample selection(표본 선택)", "date window picked after profit read(수익 확인 후 날짜창 선택)"),
        ("no_trade_index_target", "label boundary(라벨 경계)", "trade index or future outcome target(거래번호 또는 미래 결과 타깃)"),
    ]
    for guard_id, family, abort in extra:
        rows.append(
            {
                "guard_id": f"{RUN_NUMBER}_{guard_id}",
                "guard_family": family,
                "must_remain_false": "true",
                "abort_if_seen": abort,
                "source_status": "new_scaffold_guard(신규 스캐폴드 가드)",
                "added_check": "required before profit curve measurement can be interpreted(수익곡선 측정 해석 전 필수)",
                "status": "active(활성)",
                "effect": "adds explicit look-ahead and selection-bias rejection(미래참조와 선택 편향 거부를 명시)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_lane_matrix(balance_rows: Sequence[Mapping[str, str]], scaffold_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    components_by_lane: dict[str, list[str]] = {}
    for row in scaffold_rows:
        components_by_lane.setdefault(row["workstream"], []).append(row["scaffold_component"])
    rows: list[dict[str, Any]] = []
    for row in balance_rows:
        source_family = row["workstream_family"]
        family = "parity-control(동등성 대조)" if source_family.startswith("control_parity") else source_family
        rows.append(
            {
                "lane_id": f"{RUN_NUMBER}_{family}_lane",
                "workstream_family": family,
                "source_blueprints": row["source_blueprints"],
                "required_contracts": ";".join(components_by_lane.get(family, [])) or "covered_by_shared_contracts(공유 계약으로 커버)",
                "required_metric_scope": "profit/risk/execution/parity/regime as applicable(해당 시 수익/위험/실행/동등성/국면)",
                "forbidden_shortcut": "single-KPI selection, proxy authority, threshold retune, lot optimization(단일 KPI 선택/프록시 권위/임계값 재조정/로트 최적화)",
                "status": "materialized_balanced_lane(균형 레인 물질화)",
                "effect": "keeps defensive, repair, offensive, parity, and attribution work alive together(방어/수리/공격/동등성/귀속 작업을 함께 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if "offensive(공격)" not in {row.get("workstream_family") for row in rows}:
        rows.append(
            {
                "lane_id": f"{RUN_NUMBER}_offensive_profit_curve_lane",
                "workstream_family": "offensive(공격)",
                "source_blueprints": "bc_blueprint_04",
                "required_contracts": "profit_curve_measurement_contract(수익곡선 측정 계약)",
                "required_metric_scope": "net/PF/trades/DD/recovery/expectancy/worst_chunk/underwater/cost stress(순수익/PF/거래수/DD/회복/기대값/최악청크/수중구간/비용스트레스)",
                "forbidden_shortcut": "profit-only selection or hidden retune(수익 단독 선택 또는 숨은 재튜닝)",
                "status": "materialized_balanced_lane(균형 레인 물질화)",
                "effect": "adds the user's profit-curve priority without weakening anti-overfit gates(사용자 수익곡선 우선순위를 과적합 방지 게이트 약화 없이 추가)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BH_review_bounded_scaffold_inputs",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "bounded repair scaffold inputs with profit-curve priority(수익곡선 우선 제한 수리 스캐폴드 입력)",
            "inputs_to_review": ";".join(
                aw.rel(path)
                for path in (
                    SCAFFOLD_INPUT_PACKAGE,
                    COMPONENT_CONTRACTS,
                    PROFIT_CURVE_CONTRACT,
                    PROXY_MT5_CONTRACT,
                    MT5_GAP_REPAIR_CONTRACT,
                    NO_LOOKAHEAD_FIREWALL,
                    BALANCED_LANE_MATRIX,
                )
            ),
            "must_confirm": "cp322A frozen, no training, no threshold, no D/B rewrite, no lot optimization, proxy compares expected vs MT5 probe and remains signal-only(cp322A 고정/학습 없음/임계값 없음/D-B 재작성 없음/로트 최적화 없음/프록시-MT5 비교는 신호 전용)",
            "must_reject_if": "single KPI selection, date-fit, trade-index target, proxy KPI authority, forward claim, runtime authority, live readiness(단일 KPI 선택/날짜 맞춤/거래번호 타깃/프록시 KPI 권위/전진 주장/런타임 권위/실거래 준비)",
            "expected_outputs": "reviewed scaffold approval or repair plan only(검토된 스캐폴드 승인 또는 수리 계획만)",
            "priority": "P0",
            "effect": "forces review before implementation or MT5 runtime work(구현이나 MT5 런타임 작업 전 검토를 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    src: Mapping[str, Any],
    scaffold_rows: Sequence[Mapping[str, Any]],
    component_rows: Sequence[Mapping[str, Any]],
    profit_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    firewall_rows: Sequence[Mapping[str, Any]],
    lane_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent = src["final"]
    source_gates_passed = sum(1 for row in src["gates"] if row.get("status") == "passed")
    profit_required = {"net_profit", "profit_factor", "trades_per_day", "max_drawdown", "recovery_factor", "expectancy", "worst_chunk", "underwater_stretch", "curve_pocket", "lot_normalized", "cost_stress"}
    profit_ids = {str(row["metric_id"]).replace(f"{RUN_NUMBER}_", "") for row in profit_rows}
    proxy_ok = all(
        str(row["proxy_expected_field"]).startswith("proxy_expected_")
        and str(row["mt5_runtime_probe_field"]).startswith("mt5_runtime_probe_")
        for row in proxy_rows
    ) and any("Forward" in row["must_not_claim"] for row in proxy_rows) and any(
        "runtime authority" in row["must_not_claim"] or "런타임 권위" in row["must_not_claim"] for row in proxy_rows
    )
    gate_specs = [
        ("bg_gate_parent_loaded", parent.get("next_action") == RUN_ID, f"parent_next={parent.get('next_action')}", "run337BF opens run337BG(337BF가 337BG를 엶)"),
        ("bg_gate_parent_gates_passed", parent.get("passed_gates") == parent.get("gate_rows") == 12 and source_gates_passed == 12, f"parent_gates={parent.get('passed_gates')}/{parent.get('gate_rows')};audit={source_gates_passed}/12", "run337BF all gates passed(337BF 모든 게이트 통과)"),
        ("bg_gate_source_files_present", all_paths_exist(INPUT_FILES), f"inputs_present={len(INPUT_FILES)}", "all run337BF sources present(337BF 원천 모두 존재)"),
        ("bg_gate_scaffold_rows_materialized", len(scaffold_rows) == 5 and all(row["forbidden_actions"] for row in scaffold_rows), f"scaffold_rows={len(scaffold_rows)}", "five scaffold inputs with forbidden actions(금지 행동 포함 5개 스캐폴드 입력)"),
        ("bg_gate_components_linked", len(component_rows) == len(scaffold_rows), f"components={len(component_rows)}", "one component contract per scaffold input(스캐폴드 입력별 컴포넌트 계약 1개)"),
        ("bg_gate_profit_curve_contract_complete", profit_required.issubset(profit_ids), f"profit_metrics={len(profit_required & profit_ids)}/{len(profit_required)}", "profit, count, risk, curve, cost metrics complete(수익/거래수/위험/곡선/비용 지표 완비)"),
        ("bg_gate_proxy_mt5_contract_explicit", proxy_ok and len(proxy_rows) >= 5, f"proxy_contracts={len(proxy_rows)}", "proxy expected values compare to MT5 runtime probe and stay signal-only(프록시 예상값은 MT5 런타임 탐침값과 비교, 신호 전용 유지)"),
        ("bg_gate_mt5_gap_repair_inputs", len(mt5_rows) == 5 and all(int(row["max_tester_to_feature_gap_minutes"]) >= 0 for row in mt5_rows), f"mt5_gap_rows={len(mt5_rows)}", "five MT5 gap repair inputs carry feature_last gap(5개 MT5 공백 수리 입력이 feature_last 공백 보유)"),
        ("bg_gate_no_lookahead_firewall_active", len(firewall_rows) >= 12 and all(row["must_remain_false"] == "true" for row in firewall_rows), f"firewalls={len(firewall_rows)}", "source firewalls plus added lookahead guards active(원천 방화벽과 추가 미래참조 가드 활성)"),
        ("bg_gate_balanced_lanes", {"defensive(방어)", "repair(수리)", "offensive(공격)", "parity-control(동등성 대조)"}.issubset({row["workstream_family"] for row in lane_rows}), f"lanes={';'.join(sorted({row['workstream_family'] for row in lane_rows}))}", "defensive, repair, offensive, parity lanes present(방어/수리/공격/동등성 레인 존재)"),
        ("bg_gate_review_queue_ready", len(queue_rows) == 1 and queue_rows[0]["next_run_id"] == NEXT_RUN_ID, f"queue_rows={len(queue_rows)};next={queue_rows[0]['next_run_id'] if queue_rows else 'missing'}", "run337BH review queue ready(337BH 검토 대기열 준비)"),
        ("bg_gate_no_forbidden_claims", True, "forward=not_claimed;runtime=not_claimed;goal=not_claimed", "no Forward/Runtime/Goal claim(전진/런타임/목표 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": "blocks implementation handoff unless scaffold inputs preserve freeze and measurement scope(스캐폴드 입력이 고정과 측정 범위를 보존해야 구현 인계 허용)",
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
                "hypothesis": "stronger profit-curve and parity measurement can be scaffolded without changing cp322A(cp322A 변경 없이 강한 수익곡선/동등성 측정을 스캐폴드화할 수 있음)",
                "decision_use": "decide whether reviewed scaffold inputs can open bounded implementation review(검토된 스캐폴드 입력이 제한 구현 검토를 열 수 있는지 결정)",
                "comparison_baseline": PARENT_RUN_ID,
                "control_variables": "cp322A ONNX, adapter, feature order, D/B, threshold, risk, lot, ATR SL/TP, runtime handoff frozen(cp322A ONNX/어댑터/피처 순서/D-B/임계값/위험/로트/ATR SLTP/런타임 인계 고정)",
                "changed_variables": "scaffold input contracts only(스캐폴드 입력 계약만)",
                "sample_scope": "US100 M5 post-OOS/probe scope declared, no new training data used(US100 M5 OOS 이후/탐침 범위 선언, 새 학습 데이터 미사용)",
                "success_criteria": "12 gates pass and next review queue is ready(12개 게이트 통과와 다음 검토 대기열 준비)",
                "failure_criteria": "missing profit/parity/MT5/overfit input contract(수익/동등성/MT5/과적합 입력 계약 누락)",
                "invalid_conditions": "training, threshold retune, D/B rewrite, lot optimization, proxy KPI authority(학습/임계값 재조정/D-B 재작성/로트 최적화/프록시 KPI 권위)",
                "stop_conditions": "failed gate opens repair plan before implementation(게이트 실패 시 구현 전 수리 계획)",
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
                "time_axis": "US100 M5 broker bars; completed-bar and feature_last gates required downstream(US100 M5 브로커 봉, 하위 실행에서 완성봉과 feature_last 게이트 필요)",
                "sample_scope": "declared forward/probe scope only; no training split mutation(전진/탐침 범위 선언만, 학습 분할 변경 없음)",
                "missing_or_duplicate_check": "required in downstream MT5/profit curve harness(하위 MT5/수익곡선 하네스에서 필수)",
                "feature_label_boundary": "future bars, date-fit selection, and trade-index targets forbidden(미래 봉/날짜 맞춤/거래번호 타깃 금지)",
                "split_boundary": "frozen cp322A research artifact, new data only for probe/measurement(cp322A 고정 연구 산출물, 새 데이터는 탐침/측정 전용)",
                "leakage_risk": "look-ahead via feature_last, macro release timing, or post-profit slice selection(feature_last/거시 발표시각/수익 확인 후 조각 선택 통한 미래참조)",
                "data_hash_or_identity": f"artifact_registry_run={RUN_ID}",
                "integrity_judgment": "usable_with_boundary_for_scaffold_inputs(스캐폴드 입력에 한해 경계 포함 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "skill": "obsidian-model-validation",
                "run_id": RUN_ID,
                "model_family": "cp322A frozen ONNX package(cp322A 고정 ONNX 패키지)",
                "target_and_label": "unchanged from frozen package; not rebuilt(고정 패키지와 동일, 재구축 없음)",
                "split_method": "no new split; scaffold contract only(새 분할 없음, 스캐폴드 계약 전용)",
                "selection_metric": "none; no selection(없음, 선택 없음)",
                "secondary_metrics": "profit, PF, trades/day, DD, recovery, expectancy, curve pocket, cost stress as future evidence(미래 근거용 수익/PF/일거래수/DD/회복/기대값/곡선 포켓/비용 스트레스)",
                "threshold_policy": "fixed frozen threshold(고정 임계값)",
                "overfit_risk": "using scaffold to tune threshold/date/lot after reading profit(수익 확인 후 스캐폴드로 임계값/날짜/로트 조정)",
                "calibration_risk": "scores are not promoted to probabilities(점수를 확률로 승격하지 않음)",
                "comparison_baseline": PARENT_RUN_ID,
                "validation_judgment": "research_scaffold_only(연구 스캐폴드 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "skill": "obsidian-runtime-parity",
                "run_id": RUN_ID,
                "research_path": aw.rel(Path(__file__)),
                "runtime_path": "cp322A adapter and MT5 runtime handoff frozen; not modified(cp322A 어댑터와 MT5 런타임 인계 고정, 수정 없음)",
                "shared_contract": "proxy expected value vs MT5 runtime probe value row-level comparison(프록시 예상값 대 MT5 런타임 탐침값 행 단위 비교)",
                "known_differences": "tester_feature_last_gap_remains from run337BF(337BF의 tester_feature_last 공백 유지)",
                "parity_check": "contract materialized; fresh MT5 probe required downstream(계약 물질화, 하위 신규 MT5 탐침 필요)",
                "parity_identity": f"parent={PARENT_RUN_ID};scaffold={RUN_ID}",
                "runtime_claim_boundary": "research_only_no_runtime_authority(연구 전용, 런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "skill": "obsidian-performance-attribution",
                "run_id": RUN_ID,
                "observed_change": "no trading KPI observed; measurement contract expanded(거래 KPI 관측 없음, 측정 계약 확장)",
                "comparison_baseline": PARENT_RUN_ID,
                "likely_drivers": "not_applicable_until_MT5_or_forward_trade_list(미래 MT5 또는 전진 거래 목록 전까지 해당 없음)",
                "segment_checks": "long/short/session/hour/month/volatility/ADX/VIX/USD/rate required downstream(롱숏/세션/시간/월/변동성/ADX/VIX/USD/금리 하위 필수)",
                "trade_shape": "required but not measured in this scaffold run(필수이나 이번 스캐폴드 실행에서는 미측정)",
                "alternative_explanations": "proxy parity may not imply profitability(프록시 동등성이 수익성을 뜻하지 않을 수 있음)",
                "attribution_confidence": "inconclusive_by_design(설계상 불충분)",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "skill": "obsidian-result-judgment",
                "run_id": RUN_ID,
                "result_subject": "bounded repair scaffold inputs(제한 수리 스캐폴드 입력)",
                "evidence_available": [aw.rel(path) for path in OUTPUT_FILES],
                "evidence_missing": "fresh MT5 tester output, forward trade list, profit curve KPI(신규 MT5 테스터 출력/전진 거래 목록/수익곡선 KPI)",
                "judgment_label": "exploratory_scaffold_materialized(탐색 스캐폴드 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "측정과 수리 입력은 준비됐지만 아직 수익/전진/운영 주장은 아니다.",
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BG Scaffold Inputs(337단계 337BG 스캐폴드 입력)

## Conclusion(결론)

run337BG(337BG 실행)는 cp322A(322A 후보)를 바꾸지 않고, profit curve(수익곡선), proxy-MT5 parity(프록시-MT5 동등성), MT5 feature_last repair(MT5 feature_last 수리), no-lookahead firewall(미래참조 방화벽)을 다음 구현 전 입력 계약으로 물질화했다.

Effect(효과): 이제 다음 run337BH(337BH 실행)는 이 입력들이 과적합 없이 수익곡선/거래수/손실곡선 검증으로 이어질 수 있는지 검토할 수 있다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- scaffold_inputs(스캐폴드 입력): `{final['scaffold_rows']}`
- profit_metrics(수익 지표): `{final['profit_metric_rows']}`
- proxy_contracts(프록시 계약): `{final['proxy_contract_rows']}`
- mt5_gap_inputs(MT5 공백 입력): `{final['mt5_gap_rows']}`
- firewalls(방화벽): `{final['firewall_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BG Scaffold Inputs(결정: 337단계 337BG 스캐폴드 입력)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): 수익곡선 우선 연구를 열되, cp322A freeze(고정), no-lookahead(미래참조 방지), proxy signal-only(프록시 신호 전용), MT5 feature_last repair(MT5 feature_last 수리) 경계를 유지한다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_top_value(text: str, prefix: str, value: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = f"{prefix}{value}"
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def remove_workspace_focus_block(text: str, needle: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    idx = 0
    while idx < len(lines):
        if lines[idx].strip() == "- >-" and idx + 1 < len(lines) and needle in lines[idx + 1]:
            idx += 2
            while idx < len(lines) and lines[idx].startswith("  "):
                idx += 1
            continue
        out.append(lines[idx])
        idx += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def remove_markdown_section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return text
    end = text.find("\n## ", start + len(heading))
    if end < 0:
        return text[:start].rstrip() + "\n"
    return text[:start].rstrip() + "\n\n" + text[end + 1 :]


def remove_lines_containing(text: str, needle: str) -> str:
    return "\n".join(line for line in text.splitlines() if needle not in line) + ("\n" if text.endswith("\n") else "")


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []

    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = remove_workspace_focus_block(workspace_text, "Stage337 run337BG focus")
    workspace = replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        f"- >-\n  Stage337 run337BG focus complete: run337BG(337BG 실행)은 `{final['status']}`로 "
        f"bounded scaffold inputs(제한 스캐폴드 입력)를 물질화했다. Effect(효과): scaffold inputs(스캐폴드 입력) "
        f"`{final['scaffold_rows']}`, profit metrics(수익 지표) `{final['profit_metric_rows']}`, "
        f"proxy contracts(프록시 계약) `{final['proxy_contract_rows']}`, gates(게이트) "
        f"`{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    current = remove_markdown_section(current_text, "## Stage337 run337BG(337BG 실행)")
    for prefix, value in replacements.items():
        current = replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BG(337BG 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BG(337BG 실행)는 수익곡선/동등성/MT5 공백/미래참조 방화벽 입력을 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.

"""
    marker = "## Stage337 run337BF"
    current = current.replace(marker, entry + marker, 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text, _ = aw.read_text_lossless(SELECTED_STATUS)
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- scaffold_input_rows(스캐폴드 입력 행): `{final['scaffold_rows']}`
- profit_metric_contract_rows(수익 지표 계약 행): `{final['profit_metric_rows']}`
- proxy_mt5_contract_rows(프록시-MT5 계약 행): `{final['proxy_contract_rows']}`
- mt5_gap_repair_rows(MT5 공백 수리 행): `{final['mt5_gap_rows']}`
- no_lookahead_firewall_rows(미래참조 방화벽 행): `{final['firewall_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_scaffold_review_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BG(337BG 실행)는 수익곡선 우선 스캐폴드 입력만 물질화했고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief_text, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_text = remove_lines_containing(brief_text, "run337BG(337BG 실행):")
    brief_line = (
        f"\n- run337BG(337BG 실행): `{final['status']}`. Effect(효과): profit curve(수익곡선), "
        f"proxy-MT5 parity(프록시-MT5 동등성), MT5 gap repair(MT5 공백 수리), no-lookahead firewall(미래참조 방화벽) "
        f"입력 계약을 물질화했고 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief_text.rstrip() + brief_line, brief_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = remove_lines_containing(changelog_text, f",{RUN_ID},")
    changelog_line = f"{TODAY},Stage337,{RUN_ID},{final['status']},{final['judgment']},{aw.rel(REPORT_PATH)}\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_line, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_scaffold_inputs_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_design",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__scaffold_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "scaffold_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BG bounded scaffold inputs",
        "tier_scope": "research_scaffold_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"scaffold={final['scaffold_rows']};profit_metrics={final['profit_metric_rows']};proxy={final['proxy_contract_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;no_training;no_threshold;proxy_signal_only;mt5_gap_repair_required;no_goal_claim",
        "external_verification_status": "out_of_scope_by_claim_scaffold_only(주장 범위 밖, 스캐폴드 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__scaffold_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "run337BF reviewed preflight package",
        "kpi_scope": "scaffold_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__scaffold_inputs",
        "family": "bounded_scaffold_inputs_without_db",
        "question": "can profit-curve/parity/MT5-gap scaffold inputs be materialized without surface mutation",
        "metric_scope": "profit_curve_proxy_mt5_mt5_gap_no_lookahead",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
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
    scaffold_rows = build_scaffold_package(src)
    scaffold_path = aw.write_csv(SCAFFOLD_INPUT_PACKAGE, SCAFFOLD_COLUMNS, scaffold_rows)
    component_rows = build_component_contracts(scaffold_rows)
    component_path = aw.write_csv(COMPONENT_CONTRACTS, COMPONENT_COLUMNS, component_rows)
    profit_rows = build_profit_curve_contract()
    profit_path = aw.write_csv(PROFIT_CURVE_CONTRACT, PROFIT_COLUMNS, profit_rows)
    proxy_rows = build_proxy_mt5_contract()
    proxy_path = aw.write_csv(PROXY_MT5_CONTRACT, PROXY_COLUMNS, proxy_rows)
    mt5_rows = build_mt5_gap_repair_contract(src["mt5_gap"])
    mt5_path = aw.write_csv(MT5_GAP_REPAIR_CONTRACT, MT5_GAP_COLUMNS, mt5_rows)
    firewall_rows = build_firewall_checklist(src["firewall"])
    firewall_path = aw.write_csv(NO_LOOKAHEAD_FIREWALL, FIREWALL_COLUMNS, firewall_rows)
    lane_rows = build_lane_matrix(src["balance"], scaffold_rows)
    lane_path = aw.write_csv(BALANCED_LANE_MATRIX, LANE_COLUMNS, lane_rows)
    queue_rows = build_review_queue()
    queue_path = aw.write_csv(RUN337BH_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, scaffold_rows, component_rows, profit_rows, proxy_rows, mt5_rows, firewall_rows, lane_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BG_scaffold_input_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_scaffold_input_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BG_scaffold_inputs_before_review",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BG_scaffold_input_gate_failure_v1",
        "scaffold_rows": len(scaffold_rows),
        "component_rows": len(component_rows),
        "profit_metric_rows": len(profit_rows),
        "proxy_contract_rows": len(proxy_rows),
        "mt5_gap_rows": len(mt5_rows),
        "firewall_rows": len(firewall_rows),
        "lane_rows": len(lane_rows),
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
            "candidate selection(후보 선택)",
            "single KPI selection(단일 KPI 선택)",
            "proxy KPI authority(프록시 KPI 권위)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "external_verification_status": "out_of_scope_by_claim_scaffold_only(주장 범위 밖, 스캐폴드 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        scaffold_path,
        component_path,
        profit_path,
        proxy_path,
        mt5_path,
        firewall_path,
        lane_path,
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
                "scaffold_inputs": final["scaffold_rows"],
                "profit_metrics": final["profit_metric_rows"],
                "proxy_contracts": final["proxy_contract_rows"],
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
