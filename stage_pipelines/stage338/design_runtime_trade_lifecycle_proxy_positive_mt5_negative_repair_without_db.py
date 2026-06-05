from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage338 import branch_stage337_to_runtime_trade_lifecycle_repair_without_db as br  # noqa: E402


aw = br.aw

TODAY = "2026-06-01"
STAGE_ID = br.NEW_STAGE_ID
STAGE_DIR = br.NEW_STAGE_DIR
RUN_NUMBER = "run338B"
RUN_ID = "run338B_design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_without_db_v1"
PARENT_RUN_ID = br.RUN_ID
NEXT_RUN_ID = "run338C_materialize_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_inputs_without_db_v1"
STATUS = "completed_stage338B_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_design_no_training_no_selection"
JUDGMENT = "trade_lifecycle_repair_design_opened_from_valid_negative_runtime_probe_no_selection"
DECISION = "stage338B_open_run338C_materialize_runtime_trade_lifecycle_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338B_runtime_trade_lifecycle_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338B_runtime_trade_lifecycle_repair_design.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SOURCE_INPUT_FRAME = (
    ROOT
    / "stages"
    / "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
    / "02_runs"
    / "run337JL"
    / "jl_runtime_positive_low_pf_recovery_drawdown_repair_input_frame.parquet"
)

DESIGN_MATRIX = RUN_DIR / "run338B_trade_lifecycle_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "run338B_experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "run338B_data_integrity_contract.csv"
LABEL_BLUEPRINT = RUN_DIR / "run338B_trade_lifecycle_label_blueprint.csv"
FEATURE_BLUEPRINT = RUN_DIR / "run338B_pretrade_feature_blueprint.csv"
RULE_STACK_CONTRACT = RUN_DIR / "run338B_rule_stack_contract.csv"
MODEL_VALIDATION_CONTRACT = RUN_DIR / "run338B_model_validation_contract.csv"
KPI_CONTRACT = RUN_DIR / "run338B_kpi_acceptance_contract.csv"
TIER_PAIR_CONTRACT = RUN_DIR / "run338B_tier_pair_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run338C_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    br.FINAL_DECISION,
    br.SEED_SURFACE,
    br.NEGATIVE_MEMORY,
    br.DESIGN_QUEUE,
    br.INPUT_MANIFEST,
    br.jr.SCORECARD,
    br.jr.ATTRIBUTION,
    SOURCE_INPUT_FRAME,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    EXPERIMENT_CONTRACT,
    DATA_INTEGRITY_CONTRACT,
    LABEL_BLUEPRINT,
    FEATURE_BLUEPRINT,
    RULE_STACK_CONTRACT,
    MODEL_VALIDATION_CONTRACT,
    KPI_CONTRACT,
    TIER_PAIR_CONTRACT,
    MATERIALIZATION_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def parquet_identity(path: Path) -> dict[str, Any]:
    parquet_file = pq.ParquetFile(str(io(path)))
    columns = parquet_file.schema_arrow.names
    return {
        "path": rel(path),
        "exists": exists(path),
        "sha256": sha(path),
        "row_count": parquet_file.metadata.num_rows,
        "column_count": len(columns),
        "columns": columns,
        "first_columns": columns[:20],
    }


def build_design_tables() -> tuple[dict[str, pd.DataFrame], dict[str, Any]]:
    seed = read_csv(br.SEED_SURFACE).fillna("")
    negative = read_csv(br.NEGATIVE_MEMORY).fillna("")
    branch_final = read_json(br.FINAL_DECISION)
    source_identity = parquet_identity(SOURCE_INPUT_FRAME)
    source_columns = set(source_identity["columns"])

    design_rows = [
        {
            "design_id": "tlr01_density_margin_cost_throttle",
            "hypothesis": "Extreme signal density(극단 신호 밀도)를 margin/cost throttle(마진/비용 제한)로 낮추면 MT5 PF(MT5 수익 팩터)와 drawdown(낙폭)이 개선된다.",
            "changed_variables": "density cap(밀도 상한); probability margin(확률 마진); cost stress buffer(비용 압박 완충); cooldown(쿨다운)",
            "control_variables": "US100 M5, source feature set(원천 피처 세트), timestamp-safe split(시점 안전 분할), fixed lot probe(고정 랏 탐침)",
            "label_family": "trade_lifecycle_net_after_cost_fwd18(18봉 거래 생명주기 비용 후 순손익)",
            "rule_stack": "top-margin entry(상위 마진 진입); min cost buffer(최소 비용 완충); cooldown after loss(손실 뒤 쿨다운)",
            "model_family_plan": "ExtraTrees(엑스트라트리즈);XGBoost(엑스지부스트);HistGradientBoosting(히스토그램 그래디언트 부스팅)",
            "success_criteria": "MT5 runtime probe(MT5 런타임 탐침) net_profit(순수익)>0, PF>1.05, recovery>0.25, drawdown below Stage337 best(337단계 최저 나쁜 후보보다 낮음)",
            "failure_criteria": "parity ok(동등성 정상) but MT5 net<=0 or PF<=1(순수익/수익 팩터 실패)",
            "effect": "과잉 거래를 직접 줄여 proxy-positive MT5-negative(프록시 양수 MT5 음수) 붕괴를 압박한다.",
        },
        {
            "design_id": "tlr02_side_specific_loss_quarantine",
            "hypothesis": "Long/short side loss quarantine(롱/숏 방향별 손실 격리)을 붙이면 balance control(균형 대조)의 음수 손익을 줄인다.",
            "changed_variables": "side-specific label penalty(방향별 라벨 벌점); long loss veto(롱 손실 거부); short preserve guard(숏 보존 가드)",
            "control_variables": "same source rows(동일 원천 행), no future features(미래 피처 없음), no lot optimization(랏 최적화 없음)",
            "label_family": "side_runtime_pnl_fwd18(방향별 런타임 손익 18봉)",
            "rule_stack": "side gate(방향 게이트); asymmetric cooldown(비대칭 쿨다운); side exposure cap(방향 노출 상한)",
            "model_family_plan": "XGBoost(엑스지부스트);ExtraTrees(엑스트라트리즈)",
            "success_criteria": "both long/short net(롱/숏 순손익) not deeply negative and side ratio(방향 비율) above 0.55",
            "failure_criteria": "one side(한 방향)가 전체 PF(수익 팩터)를 계속 무너뜨림",
            "effect": "수량 균형을 수익 균형으로 오해하지 않게 한다.",
        },
        {
            "design_id": "tlr03_drawdown_corridor_exit_pressure",
            "hypothesis": "Drawdown corridor(낙폭 통로)와 adverse excursion(불리 이동) 압박 라벨이 MT5 max drawdown(최대 낙폭)을 줄인다.",
            "changed_variables": "MFE/MAE proxy(유리/불리 이동 프록시); max hold compression(최대 보유 압축); drawdown penalty(낙폭 벌점)",
            "control_variables": "fixed horizon family(고정 horizon 계열), existing pretrade columns only(기존 사전 피처만)",
            "label_family": "survival_drawdown_corridor_fwd18(18봉 생존 낙폭 통로)",
            "rule_stack": "early exit pressure(조기 청산 압박); no reentry during drawdown cluster(낙폭 군집 중 재진입 금지)",
            "model_family_plan": "ExtraTrees(엑스트라트리즈);HistGradientBoosting(히스토그램 그래디언트 부스팅)",
            "success_criteria": "drawdown(낙폭) < 250 and recovery(회복 계수) positive(양수)",
            "failure_criteria": "trade count(거래수) remains high while drawdown(낙폭) stays above 300",
            "effect": "수익보다 먼저 계좌 생존성을 압박한다.",
        },
        {
            "design_id": "tlr04_session_regime_loss_firewall",
            "hypothesis": "Session/regime firewall(세션/국면 방화벽)이 손실 세션을 피하면 expectancy(기대값)가 양수로 이동한다.",
            "changed_variables": "session buckets(세션 구간); volatility regime(변동성 국면); macro proxy stress(거시 프록시 압박)",
            "control_variables": "is_us_cash_open and macro proxy columns(미국 현금장/거시 프록시 열) are pretrade only(사전 피처 전용)",
            "label_family": "session_regime_lifecycle_net_fwd18(세션/국면 생명주기 순손익 18봉)",
            "rule_stack": "session allowlist(세션 허용목록); regime veto(국면 거부); risk-off cooldown(위험회피 쿨다운)",
            "model_family_plan": "XGBoost(엑스지부스트);ExtraTrees(엑스트라트리즈)",
            "success_criteria": "positive expectancy(양수 기대값) with no single session dominance(단일 세션 지배 없음)",
            "failure_criteria": "profit(수익)이 한 세션이나 한 국면에만 몰림",
            "effect": "시장 현상과 거래 실행을 같은 설계 표면에 묶는다.",
        },
        {
            "design_id": "tlr05_sparse_extreme_edge_router",
            "hypothesis": "Sparse extreme edge router(희소 극단 엣지 라우터)가 trade count(거래수)를 줄여 PF(수익 팩터)를 양수권으로 끌어올린다.",
            "changed_variables": "edge percentile(엣지 분위수); abstention class(관망 클래스); min margin(최소 마진)",
            "control_variables": "no threshold selected for operation(운영 임계값 선택 없음), only research sweep(연구 탐색만)",
            "label_family": "active_flat_lifecycle_edge_fwd18(활성 관망 생명주기 엣지 18봉)",
            "rule_stack": "flat rescue(관망 구제); extreme edge only(극단 엣지만); churn penalty(회전율 벌점)",
            "model_family_plan": "ExtraTrees(엑스트라트리즈);Logistic calibration scout(로지스틱 보정 탐색)",
            "success_criteria": "trade count(거래수) materially lower and PF(수익 팩터)>1.05",
            "failure_criteria": "too few trades(거래 부족) or same negative expectancy(동일 음수 기대값)",
            "effect": "많이 맞히는 모델이 아니라 거래할 가치가 있는 순간만 찾는다.",
        },
    ]
    design_matrix = pd.DataFrame(design_rows)
    design_matrix["source_stage"] = br.OLD_STAGE_ID
    design_matrix["source_run_id"] = br.jr.RUN_ID
    design_matrix["claim_boundary"] = CLAIM_BOUNDARY

    label_rows = [
        {
            "label_id": "tl_label_runtime_net_after_cost_fwd18",
            "horizon_bars": 18,
            "class_mapping": "0=short_allowed(숏 허용),1=flat_or_skip(관망/스킵),2=long_allowed(롱 허용)",
            "formula_intent": "future path PnL(미래 경로 손익) minus spread/slippage stress(스프레드/슬리피지 압박)를 label(라벨)에만 사용",
            "feature_label_boundary": "all features at timestamp t or earlier(모든 피처는 t시점 이하), label uses t+1..t+18(라벨은 t+1..t+18)",
            "invalid_if": "future return columns(미래 수익 열)이 feature matrix(피처 행렬)에 포함됨",
        },
        {
            "label_id": "tl_label_side_specific_loss_quarantine_fwd18",
            "horizon_bars": 18,
            "class_mapping": "side-specific class with loss quarantine(방향별 손실 격리 클래스)",
            "formula_intent": "penalize side(방향) if historical lifecycle loss tail(생명주기 손실 꼬리) dominates",
            "feature_label_boundary": "side penalty(방향 벌점)는 label generation(라벨 생성) 안에서만 계산",
            "invalid_if": "side future net(방향 미래 순손익)이 pretrade feature(사전 피처)로 들어감",
        },
        {
            "label_id": "tl_label_drawdown_survival_corridor_fwd18",
            "horizon_bars": 18,
            "class_mapping": "trade allowed only if net positive and adverse excursion controlled(순손익 양수와 불리 이동 통제 시 거래 허용)",
            "formula_intent": "combine endpoint PnL(종가 손익), max adverse excursion(최대 불리 이동), hold compression(보유 압축)",
            "feature_label_boundary": "drawdown outcome(낙폭 결과)은 label-only(라벨 전용)",
            "invalid_if": "future max adverse excursion(미래 최대 불리 이동)을 feature(피처)로 사용",
        },
        {
            "label_id": "tl_label_session_regime_lifecycle_net_fwd18",
            "horizon_bars": 18,
            "class_mapping": "session/regime conditioned trade label(세션/국면 조건부 거래 라벨)",
            "formula_intent": "same lifecycle objective(생명주기 목적)를 session/regime subgroup(세션/국면 하위그룹)별로 안정화",
            "feature_label_boundary": "session/regime features(세션/국면 피처)는 t시점 정보만, future PnL(미래 손익)은 라벨만",
            "invalid_if": "session subgroup selection(세션 하위그룹 선택)이 holdout MT5 result(MT5 홀드아웃 결과)를 보고 정해짐",
        },
    ]
    label_blueprint = pd.DataFrame(label_rows)
    label_blueprint["source_columns_available"] = ";".join(
        [column for column in ["timestamp", "future_timestamp", "hx_future_log_return_18", "jd_label_class_runtime_pnl_fwd18", "jl_label_class_profit_quality_fwd18"] if column in source_columns]
    )
    label_blueprint["claim_boundary"] = CLAIM_BOUNDARY

    feature_groups = [
        ("price_momentum_volatility(가격/모멘텀/변동성)", ["log_return_1", "return_zscore_20", "atr_14", "historical_vol_20", "adx_14"]),
        ("session_context(세션 문맥)", ["is_us_cash_open", "minutes_from_cash_open", "is_first_30m_after_open", "is_last_30m_before_cash_close"]),
        ("macro_proxy(거시 프록시)", ["vix_change_1", "vix_zscore_20", "us10yr_change_1", "usdx_zscore_20"]),
        ("mega_cap_breadth(대형주 폭)", ["mega8_equal_return_1", "top3_weighted_return_1", "mega8_pos_breadth_1", "mega8_dispersion_5"]),
    ]
    feature_blueprint = pd.DataFrame(
        [
            {
                "feature_group": group,
                "planned_columns": ";".join(columns),
                "available_columns": ";".join([column for column in columns if column in source_columns]),
                "missing_columns": ";".join([column for column in columns if column not in source_columns]),
                "timestamp_rule": "feature value must be observable at or before bar timestamp(피처 값은 봉 시각 이하에서 관측 가능해야 함)",
                "effect": "Stage338C(338C) materialization(물질화)이 실제 schema(스키마)에 맞게 feature set(피처 세트)을 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for group, columns in feature_groups
        ]
    )

    rule_stack = pd.DataFrame(
        [
            {
                "rule_id": "rule_density_cap",
                "rule_type": "entry throttle(진입 제한)",
                "parameter_family": "max signal density(최대 신호 밀도) 0.10/0.20/0.35 scout(탐색)",
                "fixed_for_training": "not fixed(고정 아님), design sweep only(설계 탐색 전용)",
                "risk_if_wrong": "too sparse or overfit threshold(너무 희소하거나 임계값 과적합)",
                "effect": "Stage337(337단계)의 0.95+ density(밀도)를 직접 압박한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "rule_id": "rule_side_loss_quarantine",
                "rule_type": "side guard(방향 가드)",
                "parameter_family": "side-specific loss veto(방향별 손실 거부), asymmetric cooldown(비대칭 쿨다운)",
                "fixed_for_training": "candidate rule stack(후보 규칙 묶음)",
                "risk_if_wrong": "removes profitable rebound side(수익 반등 방향 제거)",
                "effect": "롱/숏 균형을 수익 균형으로 검증한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "rule_id": "rule_cost_drawdown_corridor",
                "rule_type": "risk guard(위험 가드)",
                "parameter_family": "extra cost points(추가 비용 포인트), max adverse corridor(최대 불리 이동 통로)",
                "fixed_for_training": "cost stress variants(비용 압박 변형)",
                "risk_if_wrong": "kills all trades(모든 거래 제거)",
                "effect": "순수익보다 먼저 drawdown(낙폭)과 recovery(회복)를 방어한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "rule_id": "rule_session_regime_firewall",
                "rule_type": "context router(문맥 라우터)",
                "parameter_family": "session allowlist(세션 허용목록), volatility regime veto(변동성 국면 거부)",
                "fixed_for_training": "stage-local design(단계 로컬 설계)",
                "risk_if_wrong": "session overfit(세션 과적합)",
                "effect": "시장 현상 분석을 수익 구조에 붙인다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    experiment_contract = pd.DataFrame(
        [
            {
                "hypothesis": "Timestamp-safe trade lifecycle labels/features/rules can convert reproduced proxy signals into positive MT5 KPI(시점 안전 거래 생명주기 라벨/피처/규칙이 재현된 프록시 신호를 양수 MT5 KPI로 바꿀 수 있다).",
                "decision_use": "choose which input materialization and training variants to run next(다음 입력 물질화와 학습 변형 선택)",
                "comparison_baseline": "Stage337 JR valid negative runtime probe(Stage337 JR 유효한 부정 런타임 탐침), not baseline for operation(운영 기준선 아님)",
                "control_variables": "FPMarkets US100 M5, source time axis(원천 시간축), no future features(미래 피처 없음), no lot optimization(랏 최적화 없음)",
                "changed_variables": "label objective(라벨 목적), density throttle(밀도 제한), side quarantine(방향 격리), cost/drawdown rule stack(비용/낙폭 규칙 묶음)",
                "sample_scope": f"source_rows={source_identity['row_count']};source_columns={source_identity['column_count']};Stage338C will create Tier A/B records(338C가 Tier A/B 기록 생성)",
                "success_criteria": "MT5 runtime probe(MT5 런타임 탐침) positive net/PF/recovery with parity(동등성 포함 양수 순수익/PF/회복)",
                "failure_criteria": "parity ok but MT5 net<=0/PF<=1/recovery<=0(동등성 정상이나 MT5 성과 음수)",
                "invalid_conditions": "look-ahead feature(미래참조 피처), split contamination(분할 오염), missing source identity(원천 정체성 누락)",
                "stop_conditions": "stop or pivot when three materially different rule stacks fail MT5 runtime probe(서로 다른 규칙 묶음 3개가 MT5에서 실패하면 중단/전환)",
                "evidence_plan": "design contracts, materialized input frame, training manifest, ONNX parity, MT5 runtime probe, proxy-MT5 diff(설계 계약/입력/학습/ONNX 동등성/MT5 탐침/차이)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    data_integrity = pd.DataFrame(
        [
            {
                "data_source": rel(SOURCE_INPUT_FRAME),
                "time_axis": "FPMarkets US100 M5 bar timestamp(봉 시각), ordered by timestamp/source_row_id(시각/원천 행 순서)",
                "sample_scope": f"rows={source_identity['row_count']};columns={source_identity['column_count']};Stage338 design only(338단계 설계 전용)",
                "missing_or_duplicate_check": "deferred to run338C materialization(338C 입력 생성에서 확인)",
                "feature_label_boundary": "feature columns exclude future_* and label outcome columns(피처 열은 future_* 및 라벨 결과 열 제외)",
                "split_boundary": "Stage338C must preserve chronological split(338C는 시간순 분할 유지)",
                "leakage_risk": "using MT5 negative result to tune threshold directly(MT5 음수 결과로 임계값 직접 조정)",
                "data_hash_or_identity": f"sha256={source_identity['sha256']};rows={source_identity['row_count']};columns={source_identity['column_count']}",
                "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    model_validation = pd.DataFrame(
        [
            {
                "model_family": "tree multiclass models and sparse meta-filter scout(트리 다중분류 모델과 희소 메타 필터 탐색)",
                "target_and_label": "trade lifecycle labels in LABEL_BLUEPRINT(라벨 청사진의 거래 생명주기 라벨)",
                "split_method": "chronological inner train/holdout, later MT5 runtime probe(시간순 내부 학습/홀드아웃 후 MT5 런타임 탐침)",
                "selection_metric": "not selected in run338B(338B에서는 선택 없음); later multi-KPI MT5 score(이후 다중 KPI MT5 점수)",
                "secondary_metrics": "PF, expectancy, drawdown, recovery, trade count, side balance, signal density(PF/기대값/낙폭/회복/거래수/방향 균형/밀도)",
                "threshold_policy": "design-only sweep(설계 전용 탐색), no operating threshold(운영 임계값 없음)",
                "overfit_risk": "multiple rule stacks and thresholds(다중 규칙 묶음과 임계값)",
                "calibration_risk": "probabilities may be ranking only(확률은 순위일 수 있음)",
                "comparison_baseline": "Stage337 negative probe as reference surface only(Stage337 부정 탐침은 참고 표면 전용)",
                "validation_judgment": "exploratory(탐색)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    kpi_contract = pd.DataFrame(
        [
            {
                "kpi_layer": "proxy scout(프록시 탐색)",
                "required_metrics": "proxy net log return, signal density, side balance, drawdown pressure(프록시 순로그수익/신호 밀도/방향 균형/낙폭 압박)",
                "cannot_replace": "MT5 KPI(MT5 핵심 성과 지표)",
                "effect": "빠른 후보 선별만 허용한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "kpi_layer": "MT5 runtime probe(MT5 런타임 탐침)",
                "required_metrics": "net profit, PF, expectancy, drawdown, recovery, trade count, long/short balance(순수익/PF/기대값/낙폭/회복/거래수/롱숏 균형)",
                "cannot_replace": "forward or live readiness(전진 또는 실거래 준비)",
                "effect": "운영 주장 전 런타임 현실성을 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    tier_pair = pd.DataFrame(
        [
            {
                "record_view": "Tier A separate(Tier A 분리)",
                "required": "yes(예)",
                "planned_source": "full-context rows if source tier labels available(티어 라벨 가능 시 전체 문맥 행)",
                "missing_policy": "must record blocked/missing_required if unavailable(없으면 차단/필수 누락 기록)",
                "effect": "전체 문맥 표본을 단독 판독한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "record_view": "Tier B separate(Tier B 분리)",
                "required": "yes(예)",
                "planned_source": "partial-context rows or explicit missing_required(부분 문맥 행 또는 명시적 필수 누락)",
                "missing_policy": "do not omit(생략 금지)",
                "effect": "부분 문맥 표본 영향을 숨기지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "record_view": "Tier A+B combined(Tier A+B 합산)",
                "required": "yes(예)",
                "planned_source": "combined/routed actual records(합산/라우팅 실제 기록)",
                "missing_policy": "mark synthetic vs actual(합성/실제 구분)",
                "effect": "합산 결과를 과장하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    materialization_queue = pd.DataFrame(
        [
            {
                "queue_id": "run338C_materialize_trade_lifecycle_inputs",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "materialize timestamp-safe trade lifecycle repair inputs(시점 안전 거래 생명주기 수리 입력 생성)",
                "required_inputs": f"{rel(SOURCE_INPUT_FRAME)};{rel(DESIGN_MATRIX)};{rel(LABEL_BLUEPRINT)};{rel(FEATURE_BLUEPRINT)};{rel(RULE_STACK_CONTRACT)}",
                "required_outputs": "input frame parquet(입력 프레임 parquet); feature schema(피처 스키마); label audit(라벨 감사); Tier records(티어 기록); run338D review queue(검토 대기열)",
                "blocked_if_missing": "source input frame or timestamp columns(원천 입력 프레임 또는 시각 열)",
                "forbidden_action": "training or model selection during materialization(입력 생성 중 학습 또는 모델 선택)",
                "effect": "설계를 실제 학습 가능한 입력으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    tables = {
        "design_matrix": design_matrix,
        "label_blueprint": label_blueprint,
        "feature_blueprint": feature_blueprint,
        "rule_stack": rule_stack,
        "experiment_contract": experiment_contract,
        "data_integrity": data_integrity,
        "model_validation": model_validation,
        "kpi_contract": kpi_contract,
        "tier_pair": tier_pair,
        "materialization_queue": materialization_queue,
    }
    summary = {
        "source_rows": source_identity["row_count"],
        "source_columns": source_identity["column_count"],
        "source_sha256": source_identity["sha256"],
        "design_variants": len(design_matrix),
        "label_blueprints": len(label_blueprint),
        "feature_groups": len(feature_blueprint),
        "rule_rows": len(rule_stack),
        "source_stage": br.OLD_STAGE_ID,
        "source_run_id": br.jr.RUN_ID,
        "branch_run_id": br.RUN_ID,
        "source_best_model_id": branch_final.get("best_model_id", ""),
        "source_best_mt5_net_profit": branch_final.get("best_mt5_net_profit", ""),
        "source_best_mt5_profit_factor": branch_final.get("best_mt5_profit_factor", ""),
    }
    return tables, summary


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(br.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row("parent_338A_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(br.GATE_AUDIT), "Stage338A(338A) 분기 근거가 통과한 뒤 설계한다."),
            gate_row("source_input_identity_recorded", "passed" if summary["source_rows"] > 0 and summary["source_columns"] > 0 else "failed", rel(DATA_INTEGRITY_CONTRACT), "source input frame(원천 입력 프레임)의 row/column/hash(행/열/해시)를 기록한다."),
            gate_row("experiment_design_contract_written", "passed" if exists(EXPERIMENT_CONTRACT) else "failed", rel(EXPERIMENT_CONTRACT), "hypothesis/comparison/control(가설/비교/대조)을 고정한다."),
            gate_row("feature_label_boundary_written", "passed" if exists(LABEL_BLUEPRINT) and exists(FEATURE_BLUEPRINT) else "failed", f"{rel(LABEL_BLUEPRINT)};{rel(FEATURE_BLUEPRINT)}", "feature-label boundary(피처-라벨 경계)를 명시한다."),
            gate_row("model_validation_contract_written", "passed" if exists(MODEL_VALIDATION_CONTRACT) else "failed", rel(MODEL_VALIDATION_CONTRACT), "selection/threshold/calibration(선택/임계값/보정) 위험을 낮춰 주장한다."),
            gate_row("tier_pair_contract_written", "passed" if exists(TIER_PAIR_CONTRACT) else "failed", rel(TIER_PAIR_CONTRACT), "Tier A/B paired records(Tier A/B 쌍 기록)를 강제한다."),
            gate_row("run338C_materialization_queue_opened", "passed" if exists(MATERIALIZATION_QUEUE) else "failed", rel(MATERIALIZATION_QUEUE), "다음 입력 생성 queue(대기열)를 연다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(FINAL_DECISION), "model selection/training/MT5/Goal(모델 선택/학습/MT5/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "trade lifecycle repair can convert reproduced proxy signal into positive MT5 KPI(거래 생명주기 수리가 재현된 프록시 신호를 양수 MT5 KPI로 바꿀 수 있음)",
            "decision_use": "open run338C input materialization(338C 입력 생성 열기)",
            "comparison_baseline": "Stage337 JR valid negative reference surface(Stage337 JR 유효한 부정 참고 표면)",
            "control_variables": "US100 M5, timestamp-safe source, no training in design(US100 M5/시점 안전 원천/설계 중 학습 없음)",
            "changed_variables": "label objective, rule stack, density/side/cost/drawdown controls(라벨 목적/규칙 묶음/밀도·방향·비용·낙폭 대조)",
            "sample_scope": f"rows={summary['source_rows']};columns={summary['source_columns']}",
            "evidence_plan": rel(MATERIALIZATION_QUEUE),
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(SOURCE_INPUT_FRAME),
            "time_axis": "US100 M5 timestamp(US100 M5 시각), chronological split required(시간순 분할 필요)",
            "sample_scope": f"rows={summary['source_rows']};columns={summary['source_columns']}",
            "feature_label_boundary": rel(LABEL_BLUEPRINT),
            "split_boundary": rel(DATA_INTEGRITY_CONTRACT),
            "data_hash_or_identity": summary["source_sha256"],
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "tree multiclass and sparse meta-filter scout(트리 다중분류 및 희소 메타 필터 탐색)",
            "target_and_label": rel(LABEL_BLUEPRINT),
            "split_method": "chronological inner train/holdout then MT5 probe(시간순 내부 학습/홀드아웃 후 MT5 탐침)",
            "selection_metric": "not selected in run338B(338B에서 선택 없음)",
            "threshold_policy": "design sweep only(설계 탐색 전용)",
            "validation_judgment": "exploratory(탐색)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in OUTPUT_FILES if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "threshold_tuning": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338B Runtime Trade Lifecycle Repair Design(런타임 거래 생명주기 수리 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- design_variants(설계 변형): `{final['design_variants']}`
- source_rows(원천 행): `{final['source_rows']}`
- source_columns(원천 열): `{final['source_columns']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

Stage337(337단계)의 proxy-positive MT5-negative(프록시 양수 MT5 음수) valid negative(유효한 부정)를 Stage338(338단계)의 trade lifecycle repair(거래 생명주기 수리) 설계로 바꿨다.
Effect(효과): 다음 run338C가 timestamp-safe(시점 안전) 입력을 만들고, 이후 학습/ONNX(온엑스)/MT5(메타트레이더5) 검증으로 이어갈 수 있다.

## Design Surface(설계 표면)

- design matrix(설계 행렬): `{rel(DESIGN_MATRIX)}`
- label blueprint(라벨 청사진): `{rel(LABEL_BLUEPRINT)}`
- feature blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT)}`
- rule stack(규칙 묶음): `{rel(RULE_STACK_CONTRACT)}`
- materialization queue(입력 생성 대기열): `{rel(MATERIALIZATION_QUEUE)}`

## Boundary(경계)

run338B는 design only(설계 전용)다. Model training(모델 학습), candidate selection(후보 선택), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338B Decision(338B 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(DESIGN_MATRIX)}`, `{rel(EXPERIMENT_CONTRACT)}`, `{rel(DATA_INTEGRITY_CONTRACT)}`, `{rel(MATERIALIZATION_QUEUE)}`

Action(행동): trade lifecycle repair(거래 생명주기 수리) 설계를 materialization-ready(입력 생성 준비) 상태로 닫았다.
Effect(효과): Stage338(338단계)이 곧바로 data/materialization(데이터/입력 생성)으로 이동한다.

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

run338B는 설계를 닫았고, run338C는 실제 timestamp-safe(시점 안전) input frame(입력 프레임)을 만들어야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- design_variants(설계 변형): `{final['design_variants']}`
- materialization_queue(입력 생성 대기열): `{rel(MATERIALIZATION_QUEUE)}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 설계가 모델 선택처럼 보이지 않게 한다.
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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run338B {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run338B Trade Lifecycle Repair Design(거래 생명주기 수리 설계)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- design_variants(설계 변형): `{final['design_variants']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): valid negative(유효한 부정)를 입력 생성 가능한 실험 설계로 바꿨다.
""",
    )
    append_text_once(STAGE_README, marker, f"""## run338B Design(설계)

- run_id(실행 ID): `{RUN_ID}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): Stage338(338단계)의 첫 실제 설계 표면을 생성했다.
""")
    changelog = f"""## {TODAY} run338B Runtime Trade Lifecycle Repair Design(런타임 거래 생명주기 수리 설계)

- action(행동): `{final['design_variants']}`개 design variant(설계 변형)와 feature/label/rule contracts(피처/라벨/규칙 계약)를 만들었다.
- effect(효과): run338C input materialization(입력 생성)이 바로 실행 가능한 queue(대기열)를 얻었다.
- boundary(경계): training/model selection/MT5 execution(학습/모델 선택/MT5 실행)은 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "experiment_design", "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    write_csv(ARTIFACT_REGISTRY, registry[required + [c for c in registry.columns if c not in required]])


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338B inputs: {missing}")

    tables, summary = build_design_tables()
    write_csv(DESIGN_MATRIX, tables["design_matrix"])
    write_csv(LABEL_BLUEPRINT, tables["label_blueprint"])
    write_csv(FEATURE_BLUEPRINT, tables["feature_blueprint"])
    write_csv(RULE_STACK_CONTRACT, tables["rule_stack"])
    write_csv(EXPERIMENT_CONTRACT, tables["experiment_contract"])
    write_csv(DATA_INTEGRITY_CONTRACT, tables["data_integrity"])
    write_csv(MODEL_VALIDATION_CONTRACT, tables["model_validation"])
    write_csv(KPI_CONTRACT, tables["kpi_contract"])
    write_csv(TIER_PAIR_CONTRACT, tables["tier_pair"])
    write_csv(MATERIALIZATION_QUEUE, tables["materialization_queue"])
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338B gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "design_variants": final["design_variants"],
                "source_rows": final["source_rows"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
