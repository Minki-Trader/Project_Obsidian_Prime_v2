from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import route_signal_forward_handoff_feasibility_without_db as bm


aw = bm.aw
bg = bm.bg

TODAY = "2026-05-27"
STAGE_ID = bm.STAGE_ID
RUN_NUMBER = "run337BN"
RUN_ID = "run337BN_design_forward_safe_route_signal_rebuild_packet_without_db_v1"
PARENT_RUN_ID = bm.RUN_ID
NEXT_RUN_ID = "run337BO_materialize_forward_safe_route_signal_rebuild_inputs_without_db_v1"
STATUS = "completed_stage337BN_forward_safe_route_signal_rebuild_design_no_training_no_selection"
JUDGMENT = "forward_safe_rebuild_design_ready_for_input_materialization"
DECISION = "stage337BN_open_run337BO_materialize_live_computable_route_signal_rebuild_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BN_forward_safe_route_signal_rebuild_design_without_db_"
    "no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bm.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bm.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BN_forward_safe_route_signal_rebuild_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BN_forward_safe_route_signal_rebuild_design.md"
SELECTED_STATUS = bm.SELECTED_STATUS
STAGE_BRIEF = bm.STAGE_BRIEF
WORKSPACE_STATE = bm.WORKSPACE_STATE
CURRENT_STATE = bm.CURRENT_STATE
CHANGELOG = bm.CHANGELOG
RUN_REGISTRY = bm.RUN_REGISTRY
ALPHA_LEDGER = bm.ALPHA_LEDGER
ARTIFACT_REGISTRY = bm.ARTIFACT_REGISTRY
STAGE_LEDGER = bm.STAGE_LEDGER

BM_DIR = STAGE_DIR / "02_runs" / "run337BM"
BM_FINAL = BM_DIR / "final_decision.json"
BM_FEASIBILITY = BM_DIR / "route_signal_feasibility_matrix.csv"
BM_FORBIDDEN = BM_DIR / "forbidden_repair_review.csv"
BM_FAILURE_MEMORY = BM_DIR / "failure_memory.csv"
BM_QUEUE = BM_DIR / "run337BN_forward_safe_rebuild_queue.csv"
BM_GATE_AUDIT = BM_DIR / "required_gate_coverage_audit.csv"
STAGE328B_REPORT = bm.STAGE328B_REPORT
STAGE328_CONTRACT = bm.STAGE328_CONTRACT

WORK_PACKET_SPEC = RUN_DIR / "forward_safe_rebuild_work_packet_spec.csv"
LIVE_COMPUTABLE_INPUT_CONTRACT = RUN_DIR / "live_computable_input_contract.csv"
NO_OVERFIT_GATE_MATRIX = RUN_DIR / "no_overfit_gate_matrix.csv"
NEGATIVE_CONTROL_MATRIX = RUN_DIR / "negative_control_matrix.csv"
REBUILD_LANE_MATRIX = RUN_DIR / "rebuild_lane_matrix.csv"
MT5_EXTERNAL_PROOF_PLAN = RUN_DIR / "mt5_external_proof_plan.csv"
DATASET_MATERIALIZATION_PLAN = RUN_DIR / "dataset_materialization_plan.csv"
RUN337BO_QUEUE = RUN_DIR / "run337BO_input_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BM_FINAL,
    BM_FEASIBILITY,
    BM_FORBIDDEN,
    BM_FAILURE_MEMORY,
    BM_QUEUE,
    BM_GATE_AUDIT,
    STAGE328B_REPORT,
    STAGE328_CONTRACT,
)
OUTPUT_FILES = (
    WORK_PACKET_SPEC,
    LIVE_COMPUTABLE_INPUT_CONTRACT,
    NO_OVERFIT_GATE_MATRIX,
    NEGATIVE_CONTROL_MATRIX,
    REBUILD_LANE_MATRIX,
    MT5_EXTERNAL_PROOF_PLAN,
    DATASET_MATERIALIZATION_PLAN,
    RUN337BO_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

WORK_PACKET_COLUMNS = (
    "packet_id",
    "question",
    "allowed_scope",
    "forbidden_scope",
    "primary_evidence",
    "required_output",
    "effect",
    "claim_boundary",
)
INPUT_COLUMNS = (
    "input_family",
    "allowed_source",
    "asof_rule",
    "forbidden_source",
    "materialization_requirement",
    "parity_requirement",
    "effect",
    "claim_boundary",
)
GATE_MATRIX_COLUMNS = (
    "gate_id",
    "gate_family",
    "must_pass_before",
    "pass_condition",
    "reject_if",
    "effect",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "control_type",
    "test_question",
    "expected_failure_signal",
    "must_not_use_for_selection",
    "effect",
    "claim_boundary",
)
LANE_COLUMNS = (
    "lane_id",
    "lane_name",
    "allowed_model_surface",
    "allowed_threshold_policy",
    "risk_policy",
    "required_falsification",
    "status",
    "effect",
    "claim_boundary",
)
PROOF_COLUMNS = (
    "proof_id",
    "proof_layer",
    "required_external_check",
    "minimum_artifacts",
    "pass_condition",
    "blocked_status_if_missing",
    "effect",
    "claim_boundary",
)
DATASET_COLUMNS = (
    "dataset_id",
    "source_window",
    "split_policy",
    "materialization_action",
    "integrity_checks",
    "blocked_status_if_missing",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = bm.QUEUE_COLUMNS
GATE_COLUMNS = bm.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BN inputs: {missing}")
    return {
        "bm_final": read_json(BM_FINAL),
        "bm_feasibility": read_rows(BM_FEASIBILITY),
        "bm_forbidden": read_rows(BM_FORBIDDEN),
        "bm_failure_memory": read_rows(BM_FAILURE_MEMORY),
        "bm_queue": read_rows(BM_QUEUE),
        "bm_gates": read_rows(BM_GATE_AUDIT),
        "stage328b_text": aw.io_path(STAGE328B_REPORT).read_text(encoding="utf-8-sig"),
        "stage328": read_json(STAGE328_CONTRACT),
    }


def build_work_packet_spec() -> list[dict[str, Any]]:
    return [
        {
            "packet_id": "bn_packet_boundary",
            "question": "Can a new route-signal rebuild be made from live-computable market inputs without reusing cp322A outcome-distilled handoff?(실시간 계산 가능 시장 입력만으로 새 경로 신호 재구축을 만들 수 있는가?)",
            "allowed_scope": "design only; no training; no threshold tuning; no candidate selection(설계만 허용, 학습/임계값 조정/후보 선택 없음)",
            "forbidden_scope": "cp322A exact forward pass claim, outcome source reuse, split-local forward rank fitting(cp322A 정확 전진 통과 주장, 결과 원천 재사용, 전진 구간 분할 순위 맞춤)",
            "primary_evidence": ";".join([aw.rel(BM_FEASIBILITY), aw.rel(BM_FAILURE_MEMORY), aw.rel(STAGE328B_REPORT)]),
            "required_output": "run337BO materialization queue with data, parity, no-overfit, and external MT5 proof gates(run337BO 입력 물질화 대기열)",
            "effect": "turns the cp322A handoff failure into a controlled rebuild path(cp322A 인계 실패를 통제된 재구축 경로로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "packet_id": "bn_profit_goal_boundary",
            "question": "How do we pursue stronger future ONNX without selecting by forward profit?(전진 수익으로 고르지 않고 더 강한 미래 ONNX를 어떻게 찾을 것인가?)",
            "allowed_scope": "predeclare falsification and measurement gates before new model work(새 모델 작업 전 반증/측정 게이트 사전 선언)",
            "forbidden_scope": "repair-by-forward-KPI, lot optimization, score threshold retune(전진 KPI 맞춤 수리, 로트 최적화, 점수 임계값 재조정)",
            "primary_evidence": aw.rel(BM_FORBIDDEN),
            "required_output": "negative controls and out-of-sample protocol must exist before model training(학습 전 부정 대조와 외부표본 프로토콜 필요)",
            "effect": "keeps the search aggressive but prevents another overfit loop(탐색은 공격적으로 유지하되 다른 과적합 순환을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_live_computable_contract() -> list[dict[str, Any]]:
    return [
        {
            "input_family": "target_us100_m5_bars(대상 US100 M5 봉)",
            "allowed_source": "broker M5 OHLCV closed bars only(브로커 M5 종가 확정 봉만)",
            "asof_rule": "features at timestamp T use bars closed at or before T(T 시각 피처는 T 이하 확정 봉만 사용)",
            "forbidden_source": "future bars, tester result, realized trade PnL(미래 봉, 테스터 결과, 실현 거래 손익)",
            "materialization_requirement": "row count, duplicate, gap, timezone, and broker session audit(행 수/중복/공백/시간대/브로커 세션 감사)",
            "parity_requirement": "Python feature row must match MT5 closed-bar feature row(파이썬 피처 행과 MT5 확정봉 피처 행 일치)",
            "effect": "anchors the rebuild on data available at decision time(결정 시점에 존재하는 데이터로 재구축을 고정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "input_family": "external_market_m5_context(외부 시장 M5 문맥)",
            "allowed_source": "as-of joined external closed bars and published macro/rate/VIX values(시점 기준 결합 외부 확정봉 및 공표된 거시/금리/VIX 값)",
            "asof_rule": "external timestamp must be less than or equal to US100 inference timestamp(외부 시각은 US100 추론 시각 이하)",
            "forbidden_source": "same-bar future close from delayed symbols, revised future macro value(지연 심볼의 미래 종가, 미래 수정 거시값)",
            "materialization_requirement": "per-symbol freshness, lag, missingness, and release-time receipt(심볼별 신선도/지연/결측/공표시각 영수증)",
            "parity_requirement": "join replay must be deterministic from raw source files(원천 파일에서 결정적으로 재현 가능)",
            "effect": "keeps regime context useful without letting it leak future information(국면 문맥은 쓰되 미래 정보 누수를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "input_family": "route_signal_score_sources(경로 신호 점수 원천)",
            "allowed_source": "model probabilities, raw-market derived filters, predeclared train-only calibrators(모델 확률, 시장 원천 필터, 사전 선언 train-only 보정기)",
            "asof_rule": "all transforms fit on train or rolling past window only(모든 변환은 학습 또는 과거 rolling 창으로만 맞춤)",
            "forbidden_source": "split-local rank fitted on forward data, outcome-distilled Stage318 source(전진 데이터 분할 순위 맞춤, 결과 증류 Stage318 원천)",
            "materialization_requirement": "fit boundary manifest and hash for every transform(모든 변환의 적합 경계 목록과 해시)",
            "parity_requirement": "signal parity table must compare Python expected signal and MT5 emitted signal(파이썬 예상 신호와 MT5 출력 신호 동등성 표 필요)",
            "effect": "replaces the unsafe cp322A handoff with a reproducible live-computable signal path(위험한 cp322A 인계를 재현 가능한 실시간 계산 경로로 대체)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_no_overfit_gate_matrix() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "bn_gate_no_forward_fit",
            "gate_family": "model_validation(모델 검증)",
            "must_pass_before": "any training or candidate comparison(학습 또는 후보 비교 전)",
            "pass_condition": "forward window is read-only and absent from fit artifacts(전진 구간은 읽기 전용이고 적합 산출물에 없음)",
            "reject_if": "any threshold, rank, scaler, or calibrator is fit on forward rows(임계값/순위/스케일러/보정기가 전진 행에 맞춰짐)",
            "effect": "prevents forward retuning from entering the rebuild(전진 재조정이 재구축에 들어오는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "bn_gate_outcome_source_ban",
            "gate_family": "data_integrity(데이터 무결성)",
            "must_pass_before": "feature materialization(피처 물질화 전)",
            "pass_condition": "no realized MT5 result, PnL, or outcome-distilled label is an input(실현 MT5 결과/손익/결과 증류 라벨이 입력이 아님)",
            "reject_if": "source column is derived from trade result or future label(원천 컬럼이 거래 결과나 미래 라벨에서 파생됨)",
            "effect": "closes the cp322A route-signal failure mode(cp322A 경로 신호 실패 모드를 닫음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "bn_gate_python_mt5_signal_parity",
            "gate_family": "runtime_parity(런타임 동등성)",
            "must_pass_before": "MT5 KPI interpretation(MT5 KPI 해석 전)",
            "pass_condition": "timestamp-aligned Python and MT5 signals match within declared tolerance(시각 맞춤 파이썬/MT5 신호가 허용오차 안에서 일치)",
            "reject_if": "MT5 signal count, side, score, or feature timestamp diverges without explained skip(MT5 신호 수/방향/점수/피처 시각이 설명 없이 어긋남)",
            "effect": "keeps proxy usable only when runtime meaning matches(런타임 의미가 맞을 때만 프록시를 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "bn_gate_cost_curve_stress",
            "gate_family": "performance_attribution(성과 귀속)",
            "must_pass_before": "research handoff(연구 인계 전)",
            "pass_condition": "net, PF, drawdown, recovery, curve pocket, and trade density survive cost stress(순익/PF/DD/회복/곡선 포켓/거래 밀도가 비용 압박을 버팀)",
            "reject_if": "profit exists only in one cost-light pocket or one side/session/month(수익이 비용 낮은 한 구간이나 한 방향/세션/월에만 존재)",
            "effect": "aligns the search with robust auto-trading shape(강건한 자동매매 곡선 모양과 탐색을 맞춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "bn_gate_external_mt5_required",
            "gate_family": "backtest_forensics(백테스트 포렌식)",
            "must_pass_before": "any positive forward judgment(긍정 전진 판정 전)",
            "pass_condition": "real-tick MT5 report, trade list, settings, and runtime logs are present(실제 틱 MT5 보고서/거래 목록/설정/런타임 로그 존재)",
            "reject_if": "only proxy KPI exists or tester setting identity is missing(프록시 KPI만 있거나 테스터 설정 정체성이 없음)",
            "effect": "prevents paper-only success claims(종이 결과만으로 성공 주장하는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_negative_controls() -> list[dict[str, Any]]:
    controls = [
        ("bn_neg_time_shift", "time_shift(시간 이동)", "Does signal disappear when features are shifted away from labels?(피처를 라벨에서 밀면 신호가 사라지는가?)", "PF and expectancy collapse(PF와 기대값 붕괴)"),
        ("bn_neg_side_flip", "side_flip(방향 반전)", "Is edge directional rather than symmetric noise?(엣지가 방향성인가, 잡음인가?)", "flipped side does not preserve edge(반전 방향은 엣지 유지 안 됨)"),
        ("bn_neg_label_shuffle", "label_shuffle(라벨 섞기)", "Does training fail under shuffled outcomes?(섞은 결과에서 학습이 실패하는가?)", "rank and PF degrade to noise(순위와 PF가 잡음 수준으로 약화)"),
        ("bn_neg_session_holdout", "session_holdout(세션 보류)", "Does the curve rely on one session only?(곡선이 한 세션에만 의존하는가?)", "held-out session exposes fragility(보류 세션에서 취약성 노출)"),
        ("bn_neg_month_block", "month_block(월 단위 차단)", "Does one month carry the curve?(한 달이 곡선을 떠받치는가?)", "blocked month changes are bounded(월 차단 변화가 제한적)"),
        ("bn_neg_spread_stress", "spread_stress(스프레드 압박)", "Does the edge survive wider cost?(넓은 비용을 버티는가?)", "thin-cost lanes fail before selection(비용 얇은 경로는 선택 전 실패)"),
        ("bn_neg_volatility_slice", "volatility_slice(변동성 구간)", "Does performance vanish outside one volatility state?(한 변동성 상태 밖에서 성과가 사라지는가?)", "bad slice is visible before handoff(나쁜 구간이 인계 전 보임)"),
        ("bn_neg_adx_vix_macro", "regime_holdout(국면 보류)", "Does ADX/VIX/USD/rate regime explain hidden concentration?(ADX/VIX/USD/금리 국면이 숨은 집중을 설명하는가?)", "regime pocket is labeled, not hidden(국면 포켓이 숨지 않고 라벨링됨)"),
    ]
    return [
        {
            "control_id": control_id,
            "control_type": control_type,
            "test_question": question,
            "expected_failure_signal": expected,
            "must_not_use_for_selection": "true; negative controls diagnose, not tune(참; 부정 대조는 진단용이지 조정용 아님)",
            "effect": "turns fragility into recorded failure memory(취약성을 기록된 실패 기억으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for control_id, control_type, question, expected in controls
    ]


def build_rebuild_lanes() -> list[dict[str, Any]]:
    return [
        {
            "lane_id": "bn_lane_rank_free_absolute_score",
            "lane_name": "rank-free absolute score route(순위 없는 절대 점수 경로)",
            "allowed_model_surface": "new candidate only; cp322A exact status remains research artifact(새 후보 전용, cp322A 정확판은 연구 산출물 유지)",
            "allowed_threshold_policy": "train-only or nested validation predeclared before forward(전진 전 학습 전용 또는 중첩 검증 사전 선언)",
            "risk_policy": "fixed risk and lot-normalized review before any lot change(로트 변경 전 고정 위험 및 로트 정규화 검토)",
            "required_falsification": "time shift, spread stress, side flip, Python-MT5 parity(시간 이동/스프레드 압박/방향 반전/파이썬-MT5 동등성)",
            "status": "allowed_for_run337BO_materialization",
            "effect": "removes split-local forward rank dependence(전진 분할 순위 의존을 제거)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "bn_lane_live_market_regime_gate",
            "lane_name": "live market regime gate route(실시간 시장 국면 게이트 경로)",
            "allowed_model_surface": "raw-market filters plus model probabilities(시장 원천 필터와 모델 확률)",
            "allowed_threshold_policy": "predeclared train/validation only(학습/검증 구간 사전 선언만)",
            "risk_policy": "ATR stop and target must be declared before MT5 proof(ATR 손절/익절은 MT5 검증 전 선언)",
            "required_falsification": "session, hour, month, volatility, ADX, VIX, USD, rate slices(세션/시간/월/변동성/ADX/VIX/USD/금리 구간)",
            "status": "allowed_for_run337BO_materialization",
            "effect": "lets regime context help without outcome leakage(국면 문맥을 쓰되 결과 누수를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "bn_lane_proxy_only_diagnostic",
            "lane_name": "proxy diagnostic route(프록시 진단 경로)",
            "allowed_model_surface": "diagnostic signal only, no KPI authority(진단 신호만, KPI 권위 없음)",
            "allowed_threshold_policy": "none for selection(선택용 없음)",
            "risk_policy": "not used for operating claim(운영 주장에 사용 안 함)",
            "required_falsification": "proxy-MT5 difference report and runtime handoff proof(프록시-MT5 차이 보고와 런타임 인계 증명)",
            "status": "allowed_for_debug_not_selection",
            "effect": "keeps proxy useful while preventing proxy-only promotion(프록시는 유용하게 두되 프록시만으로 승격하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_external_proof_plan() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "bn_proof_data_forward_window",
            "proof_layer": "data_integrity(데이터 무결성)",
            "required_external_check": "2026-04-14 이후 최신 확보 가능 US100 M5 broker data audit(2026-04-14 이후 최신 US100 M5 브로커 데이터 감사)",
            "minimum_artifacts": "raw data path, row count, timestamp min/max, missing/duplicate report(원천 경로/행 수/시각 범위/결측 중복 보고)",
            "pass_condition": "forward rows exist and are complete enough for declared window(전진 행이 존재하고 선언 구간에 충분히 완전)",
            "blocked_status_if_missing": "blocked_forward_data_missing",
            "effect": "prevents success without new forward data(새 전진 데이터 없이 성공 처리하는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "proof_id": "bn_proof_python_mt5_parity",
            "proof_layer": "runtime_parity(런타임 동등성)",
            "required_external_check": "MT5 runtime probe emits feature timestamp, score, side, skip reason(MT5 런타임 탐침이 피처 시각/점수/방향/스킵 이유 출력)",
            "minimum_artifacts": "Python expected CSV, MT5 output CSV, diff CSV(파이썬 예상 CSV, MT5 출력 CSV, 차이 CSV)",
            "pass_condition": "timestamp-aligned signal parity passes before KPI read(시각 맞춤 신호 동등성이 KPI 해석 전 통과)",
            "blocked_status_if_missing": "blocked_runtime_parity_missing",
            "effect": "keeps MT5 and research meaning aligned(MT5와 연구 의미를 맞춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "proof_id": "bn_proof_real_tick_backtest",
            "proof_layer": "backtest_forensics(백테스트 포렌식)",
            "required_external_check": "MT5 Strategy Tester real tick report with settings and trades(MT5 전략 테스터 실제 틱 보고서와 설정/거래)",
            "minimum_artifacts": "HTML/XML report, trade list, set file, ini file, terminal log(HTML/XML 보고서, 거래 목록, set 파일, ini 파일, 터미널 로그)",
            "pass_condition": "report identity matches generated package and no tester gap remains(보고서 정체성이 생성 패키지와 맞고 테스터 공백 없음)",
            "blocked_status_if_missing": "blocked_mt5_report_missing",
            "effect": "prevents runtime authority from being inferred from proxy(프록시에서 런타임 권위를 추론하지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "proof_id": "bn_proof_cost_and_curve",
            "proof_layer": "performance_attribution(성과 귀속)",
            "required_external_check": "cost, slippage, lot-normalized, curve pocket and underwater reports(비용/슬리피지/로트 정규화/곡선 포켓/수중 구간 보고)",
            "minimum_artifacts": "cost stress CSV, lot-normalized CSV, curve pocket report(비용 압박 CSV, 로트 정규화 CSV, 곡선 포켓 보고)",
            "pass_condition": "fragility is either rejected or recorded before handoff(취약성이 거절되거나 인계 전 기록)",
            "blocked_status_if_missing": "blocked_attribution_missing",
            "effect": "aligns with the user's robust auto-trading target(사용자의 강건 자동매매 목표와 맞춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dataset_plan() -> list[dict[str, Any]]:
    return [
        {
            "dataset_id": "bn_dataset_forward_us100_m5",
            "source_window": "after 2026-04-14 through latest available broker data(2026-04-14 이후 최신 확보 가능 브로커 데이터까지)",
            "split_policy": "forward is holdout; no fitting; no threshold choice(전진 구간은 보류, 적합/임계값 선택 없음)",
            "materialization_action": "run337BO audits raw US100 M5 availability and produces canonical forward frame(run337BO가 원천 US100 M5와 표준 전진 프레임 생성)",
            "integrity_checks": "timezone, duplicates, gaps, broker sessions, M5 close alignment(시간대/중복/공백/브로커 세션/M5 종가 정렬)",
            "blocked_status_if_missing": "blocked_forward_data_missing",
            "effect": "makes data availability a hard gate instead of a note(데이터 확보를 메모가 아니라 강한 게이트로 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "dataset_id": "bn_dataset_train_validation_controls",
            "source_window": "historical train/validation only, excluding forward holdout(과거 학습/검증만, 전진 보류 제외)",
            "split_policy": "controls and transforms fit before forward read(대조군과 변환은 전진 읽기 전 적합)",
            "materialization_action": "run337BO inventories existing train/validation artifacts and missing rebuild inputs(run337BO가 기존 산출물과 누락 입력 목록화)",
            "integrity_checks": "fit-boundary manifest, transform hash, source lineage(적합 경계 목록, 변환 해시, 원천 계보)",
            "blocked_status_if_missing": "blocked_fit_boundary_missing",
            "effect": "keeps train controls separate from forward judging(학습 대조와 전진 판정을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BO_materialize_forward_safe_route_signal_rebuild_inputs",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "forward-safe route-signal rebuild input materialization(전진 안전 경로 신호 재구축 입력 물질화)",
            "inputs_to_review": ";".join(
                [
                    aw.rel(WORK_PACKET_SPEC),
                    aw.rel(LIVE_COMPUTABLE_INPUT_CONTRACT),
                    aw.rel(NO_OVERFIT_GATE_MATRIX),
                    aw.rel(NEGATIVE_CONTROL_MATRIX),
                    aw.rel(REBUILD_LANE_MATRIX),
                    aw.rel(MT5_EXTERNAL_PROOF_PLAN),
                    aw.rel(DATASET_MATERIALIZATION_PLAN),
                ]
            ),
            "must_confirm": "live-computable data availability, as-of joins, no outcome source, no forward fit(실시간 계산 가능 데이터, 시점 기준 결합, 결과 원천 없음, 전진 적합 없음)",
            "must_reject_if": "uses cp322A outcome-distilled route source, tunes on forward, skips MT5 parity(cp322A 결과 증류 경로 원천 사용, 전진 조정, MT5 동등성 생략)",
            "expected_outputs": "canonical input inventory, blocked data list, parity preflight, next execution queue(표준 입력 목록, 차단 데이터 목록, 동등성 사전점검, 다음 실행 대기열)",
            "priority": "P0",
            "effect": "moves from design to concrete data/input evidence(설계에서 실제 데이터/입력 근거로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "work_family": "experiment_design",
                "primary_skill": "obsidian-experiment-design",
                "design_boundary": "pre-training rebuild packet only(학습 전 재구축 묶음만)",
                "hypothesis": "live-computable route signal may replace unsafe outcome-distilled cp322A handoff(실시간 계산 가능 경로 신호가 위험한 결과 증류 cp322A 인계를 대체할 수 있음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_boundary": "forward data must be audited in run337BO before any result claim(run337BO에서 전진 데이터 감사 전 결과 주장 금지)",
                "leakage_controls": "as-of joins, no future rank fit, no outcome source(시점 기준 결합, 미래 순위 적합 없음, 결과 원천 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_boundary": "no model training and no candidate selection in run337BN(run337BN에서는 모델 학습과 후보 선택 없음)",
                "allowed_next": "input materialization and predeclared control setup only(입력 물질화와 사전 선언 대조 설정만)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "runtime_boundary": "external MT5 proof requirements declared but not executed(MT5 외부 검증 요구사항 선언, 실행은 아직 아님)",
                "runtime_authority": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "lineage": f"parent={PARENT_RUN_ID};source={aw.rel(BM_FAILURE_MEMORY)}",
                "artifact_boundary": "design artifacts only(설계 산출물만)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "judgment": final["judgment"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in payloads]


def build_gates(
    src: Mapping[str, Any],
    work_rows: Sequence[Mapping[str, Any]],
    input_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    lane_rows: Sequence[Mapping[str, Any]],
    proof_rows: Sequence[Mapping[str, Any]],
    dataset_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    bm_passed = sum(1 for row in src["bm_gates"] if row.get("status") == "passed")
    live_rebuild_allowed = any(
        row.get("option_id") == "live_computable_rebuild" and "allowed" in row.get("decision", "")
        for row in src["bm_feasibility"]
    )
    outcome_ban_named = any(row.get("gate_id") == "bn_gate_outcome_source_ban" for row in gate_rows)
    external_mt5_named = any("MT5" in row.get("required_external_check", "") for row in proof_rows)
    forward_missing_block_named = any(row.get("blocked_status_if_missing") == "blocked_forward_data_missing" for row in dataset_rows)
    specs = [
        ("bn_gate_parent_final_loaded", src["bm_final"].get("next_action") == RUN_ID, f"parent_next={src['bm_final'].get('next_action')}", "run337BM opens run337BN(run337BM이 run337BN을 연다)"),
        ("bn_gate_parent_gates_passed", bm_passed == 10 and src["bm_final"].get("passed_gates") == 10, f"bm_gates={bm_passed}", "run337BM gates passed(run337BM 게이트 통과)"),
        ("bn_gate_live_rebuild_option_present", live_rebuild_allowed, f"live_rebuild_allowed={live_rebuild_allowed}", "live-computable rebuild option allowed(실시간 계산 가능 재구축 선택지 허용)"),
        ("bn_gate_work_packet_spec_ready", len(work_rows) >= 2, f"work_rows={len(work_rows)}", "work packet boundaries recorded(작업 묶음 경계 기록)"),
        ("bn_gate_live_input_contract_ready", len(input_rows) >= 3, f"input_rows={len(input_rows)}", "live-computable input contract recorded(실시간 계산 가능 입력 계약 기록)"),
        ("bn_gate_no_overfit_controls_ready", len(gate_rows) >= 5 and outcome_ban_named, f"gate_rows={len(gate_rows)};outcome_ban={outcome_ban_named}", "no-overfit gates include outcome-source ban(무과적합 게이트가 결과 원천 금지를 포함)"),
        ("bn_gate_negative_controls_ready", len(negative_rows) >= 8, f"negative_rows={len(negative_rows)}", "negative controls predeclared(부정 대조 사전 선언)"),
        ("bn_gate_rebuild_lanes_scoped", all("allowed" in row.get("status", "") for row in lane_rows), f"lane_rows={len(lane_rows)}", "lanes scoped before training(학습 전 경로 범위 지정)"),
        ("bn_gate_external_proof_required", external_mt5_named and len(proof_rows) >= 4, f"proof_rows={len(proof_rows)};mt5={external_mt5_named}", "external MT5 proof required(외부 MT5 검증 필요)"),
        ("bn_gate_forward_data_blocker_named", forward_missing_block_named, f"forward_missing_block={forward_missing_block_named}", "missing forward data has blocked status(전진 데이터 누락 차단 상태 존재)"),
        ("bn_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue_rows={len(queue_rows)}", "run337BO queue ready(run337BO 대기열 준비)"),
        ("bn_gate_no_goal_or_forward_pass_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "keeps rebuild design auditable before execution(재구축 설계를 실행 전에 감사 가능하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BN Forward-Safe Route-Signal Rebuild Design(전진 안전 경로 신호 재구축 설계)

## Conclusion(결론)

run337BN(337BN 실행)은 cp322A exact handoff(정확 cp322A 인계)를 수리하지 않고, 새 forward-safe route-signal rebuild(전진 안전 경로 신호 재구축) 설계를 열었다.

Effect(효과): 다음 실행은 수익을 고르는 일이 아니라 live-computable input(실시간 계산 가능 입력), as-of join(시점 기준 결합), no outcome source(결과 원천 금지), Python-MT5 parity(파이썬-MT5 동등성), external MT5 proof(외부 MT5 검증)를 먼저 물질화한다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- work_packet_rows(작업 묶음 행): `{final['work_packet_rows']}`
- input_contract_rows(입력 계약 행): `{final['input_contract_rows']}`
- negative_controls(부정 대조): `{final['negative_control_rows']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

- training(학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BN Forward-Safe Route-Signal Rebuild Design(결정: 337단계 337BN 전진 안전 경로 신호 재구축 설계)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): cp322A exact(정확 cp322A)는 연구 산출물로 보존하고, 다음은 outcome-free(결과 없는), live-computable(실시간 계산 가능), MT5-verifiable(MT5 검증 가능) 재구축 입력 물질화다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BN focus")
    workspace = bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        "- >-\n"
        "  Stage337 run337BN focus complete: forward-safe route-signal rebuild design"
        "(전진 안전 경로 신호 재구축 설계)를 완료했다. Effect(효과): "
        "학습/선택 없이 live-computable input(실시간 계산 가능 입력), no-overfit gate"
        "(무과적합 게이트), negative control(부정 대조), external MT5 proof"
        "(외부 MT5 검증) 요구사항을 고정하고 run337BO(337BO 실행)를 연다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bg.remove_markdown_section(current_text, "## Stage337 run337BN(337BN 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BN(337BN 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BN(337BN 실행)은 cp322A exact handoff(정확 cp322A 인계)를 고치지 않고 forward-safe route-signal rebuild(전진 안전 경로 신호 재구축) 설계를 만들었다. 학습/선택/전진 통과/목표 달성은 주장하지 않는다.
"""
    current = current.replace("## Stage337 run337BM(337BM 실행)", entry + "\n## Stage337 run337BM(337BM 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `forward_safe_design_ready_for_input_materialization`
- actual_mt5_execution(실제 MT5 실행): `not_run_design_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cp322A exact(정확 cp322A)는 보존하고, 다음은 전진 안전 재구축 입력 물질화다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_text = (
        stage_text.rstrip()
        + f"\n- {TODAY}: run337BN(337BN 실행) designed forward-safe route-signal rebuild(전진 안전 경로 신호 재구축) gates and opened run337BO(337BO 실행). Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = (
        changelog_text.rstrip()
        + f"\n- {TODAY}: Stage337 run337BN created forward-safe route-signal rebuild design(전진 안전 경로 신호 재구축 설계) with no-overfit gates(무과적합 게이트), negative controls(부정 대조), and MT5 proof requirements(MT5 검증 요구사항).\n"
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "forward_safe_route_signal_rebuild_design_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_design",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__forward_safe_rebuild_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "forward_safe_rebuild_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BN forward-safe route-signal rebuild design",
        "tier_scope": "design_only_no_trading_kpi",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"design_gates={final['passed_gates']}/{final['gate_rows']};negative_controls={final['negative_control_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_forward_claim;no_goal_achieve",
        "external_verification_status": "declared_required_not_executed(요구 선언, 미실행)",
        "notes": f"next_action={final['next_action']};cp322a_preserved_research_artifact.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__forward_safe_rebuild_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "run337BM failure memory and Stage328B live-feature rebuild requirement",
        "kpi_scope": "design_no_trading_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": "goal_achieve_not_claimed;forward_passed_not_claimed;training_not_run",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__forward_safe_rebuild_design",
        "family": "forward_safe_route_signal_rebuild_design_without_db",
        "question": "how to rebuild route signal without outcome source or forward rank fit",
        "metric_scope": "design_gates_negative_controls_external_proof_plan",
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
    work_rows = build_work_packet_spec()
    work_path = aw.write_csv(WORK_PACKET_SPEC, WORK_PACKET_COLUMNS, work_rows)
    input_rows = build_live_computable_contract()
    input_path = aw.write_csv(LIVE_COMPUTABLE_INPUT_CONTRACT, INPUT_COLUMNS, input_rows)
    no_overfit_rows = build_no_overfit_gate_matrix()
    no_overfit_path = aw.write_csv(NO_OVERFIT_GATE_MATRIX, GATE_MATRIX_COLUMNS, no_overfit_rows)
    negative_rows = build_negative_controls()
    negative_path = aw.write_csv(NEGATIVE_CONTROL_MATRIX, NEGATIVE_COLUMNS, negative_rows)
    lane_rows = build_rebuild_lanes()
    lane_path = aw.write_csv(REBUILD_LANE_MATRIX, LANE_COLUMNS, lane_rows)
    proof_rows = build_external_proof_plan()
    proof_path = aw.write_csv(MT5_EXTERNAL_PROOF_PLAN, PROOF_COLUMNS, proof_rows)
    dataset_rows = build_dataset_plan()
    dataset_path = aw.write_csv(DATASET_MATERIALIZATION_PLAN, DATASET_COLUMNS, dataset_rows)
    queue_rows = build_queue()
    queue_path = aw.write_csv(RUN337BO_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, work_rows, input_rows, no_overfit_rows, negative_rows, lane_rows, proof_rows, dataset_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BN_rebuild_design_gate_failure",
        "judgment": JUDGMENT if all_gates_pass else "forward_safe_rebuild_design_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BN_design_before_input_materialization",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BN_rebuild_design_gate_failure_v1",
        "work_packet_rows": len(work_rows),
        "input_contract_rows": len(input_rows),
        "no_overfit_gate_rows": len(no_overfit_rows),
        "negative_control_rows": len(negative_rows),
        "rebuild_lane_rows": len(lane_rows),
        "external_proof_rows": len(proof_rows),
        "dataset_plan_rows": len(dataset_rows),
        "queue_rows": len(queue_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": count_passed(gate_rows),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "training": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "no_training": True,
        "no_selection": True,
        "generated_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = build_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final) if all_gates_pass else []
    register_paths = update_registers(final) if all_gates_pass else []
    artifact_inputs = [
        work_path,
        input_path,
        no_overfit_path,
        negative_path,
        lane_path,
        proof_path,
        dataset_path,
        queue_path,
        gate_path,
        final_path,
        manifest_path,
        *receipt_paths,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_inputs, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "passed_gates": final["passed_gates"],
                "gate_rows": final["gate_rows"],
                "negative_controls": final["negative_control_rows"],
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
