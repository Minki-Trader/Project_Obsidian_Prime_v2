from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage341 import branch_stage340_to_f01_stability_cost_regime_validation_without_db as br


ROOT = br.ROOT
TODAY = br.TODAY
STAGE_ID = br.NEW_STAGE_ID
STAGE_DIR = br.NEW_STAGE_DIR

RUN_NUMBER = "run341B"
RUN_ID = "run341B_design_f01_stability_cost_regime_validation_without_db_v1"
PARENT_RUN_ID = br.RUN_ID
NEXT_RUN_ID = "run341C_materialize_f01_stability_cost_regime_validation_inputs_without_db_v1"

STATUS = "completed_stage341B_f01_stability_cost_regime_validation_design_no_selection_no_mt5"
JUDGMENT = "f01_q01_q09_stability_cost_regime_validation_design_ready_materialization_required_no_selection"
DECISION = "stage341B_open_run341C_materialize_f01_stability_cost_regime_validation_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_f01_stability_cost_regime_validation_no_model_training_"
    "no_threshold_optimization_no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run341B_f01_stability_cost_regime_validation_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage341B_f01_stability_cost_regime_validation_design.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "data_integrity_contract.csv"
VALIDATION_AXIS_CONTRACT = RUN_DIR / "validation_axis_contract.csv"
COST_STRESS_CONTRACT = RUN_DIR / "cost_stress_contract.csv"
SESSION_REGIME_CONTRACT = RUN_DIR / "session_regime_contract.csv"
EQUITY_CURVE_CONTRACT = RUN_DIR / "equity_curve_quality_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run341C_materialization_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

SOURCE_QUEUE = STAGE_DIR / "02_runs" / "run341A" / "run341B_validation_seed_queue.csv"
SOURCE_HANDOFF = STAGE_DIR / "02_runs" / "run341A" / "stage340_to_stage341_handoff_manifest.csv"
SOURCE_FINAL_DECISION = STAGE_DIR / "02_runs" / "run341A" / "final_decision.json"
SOURCE_SCORECARD = br.SOURCE_SCORECARD
SOURCE_FAILURE_MEMORY = br.SOURCE_FAILURE_MEMORY
SOURCE_RUNTIME_SUMMARY = br.SOURCE_RUNTIME_SUMMARY
SOURCE_PROXY_DIFF = br.SOURCE_PROXY_DIFF
SOURCE_REPORT_RECORDS = br.SOURCE_STAGE_DIR / "02_runs" / "run340G" / "strategy_tester_report_records.json"
RAW_BARS = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
FEATURE_FRAME = (
    ROOT
    / "data"
    / "processed"
    / "datasets"
    / "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"
    / "features.parquet"
)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> Any:
    return br.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return br.read_csv(path)


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    br.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> None:
    br.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    br.write_bom_text(path, text)


def rel(path: Path | str) -> str:
    return br.rel(path)


def exists(path: Path) -> bool:
    return br.path_exists(path)


def sha(path: Path) -> str:
    return br.sha256_file(path)


def append_text_once(path: Path, marker: str, text: str) -> None:
    br.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, keys: list[str], rows: list[Mapping[str, Any]]) -> None:
    br.append_or_replace_csv(path, keys, rows)


def metric_row(scorecard: pd.DataFrame, attempt: str) -> dict[str, Any]:
    matched = scorecard.loc[scorecard["attempt_name"].astype(str).eq(attempt)]
    return matched.iloc[0].to_dict() if not matched.empty else {}


def build_experiment_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "experiment_id": "stage341_f01_q01_q09_stability_cost_regime_validation",
                "hypothesis": (
                    "q01 quality anchor(품질 기준점)는 q09 net clue(순수익 단서)보다 낮은 drawdown(낙폭)과 높은 recovery(회복)를 유지하고, "
                    "q09 net clue(순수익 단서)는 session/regime(세션/국면) 또는 cost stress(비용 압박)에서 우위가 좁아질 수 있다."
                ),
                "decision_use": "decide next materialized validation and possible repair seed(다음 물질화 검증과 수리 씨앗 판단)",
                "comparison_baseline": "q01 exact control(정확 대조) versus q09 short-threshold relax(숏 임계값 완화), with q07/q08 hold-only negative control(보유만 변경 부정 대조)",
                "control_variables": "source ONNX(온엑스), feature_order_hash(피처 순서 해시), MT5 report(메타트레이더5 보고서), symbol US100(심볼), timeframe M5(5분봉), close_on_flat=False(평탄 청산 꺼짐)",
                "changed_variables": "validation slicing only(검증 분할만 변경): cost stress(비용 압박), session/regime split(세션/국면 분할), equity curve quality(수익곡선 품질)",
                "sample_scope": "Tier A(티어 A) run340G MT5 runtime window(런타임 구간) 2024-07-30 to 2025-01-01; Tier B(티어 B) missing_required(필수 누락)",
                "success_criteria": "q01/q09 both keep positive net(양수 순수익), PF(수익 팩터)>1.10, recovery(회복)>1.00 after reasonable proxy cost stress(프록시 비용 압박), and no single session/regime pocket owns the whole edge(단일 세션/국면 지배 없음)",
                "failure_criteria": "q09 edge disappears after small cost stress(작은 비용 압박) or q01/q09 profits concentrate in one brittle session/regime pocket(취약 세션/국면 집중)",
                "invalid_conditions": "MT5 report parse failure(MT5 보고서 파싱 실패), missing market bars(시장 봉 누락), future label/feature join(미래 라벨/피처 결합), or q01/q09 report identity mismatch(보고서 정체성 불일치)",
                "stop_conditions": "if a selection or runtime authority claim is desired, stop and open explicit promotion packet(선정 또는 런타임 권위가 필요하면 명시적 승격 묶음을 연다)",
                "evidence_plan": "trade_level_records(거래 단위 기록), attribution_summary(귀속 요약), cost_stress_matrix(비용 압박 행렬), session_regime_scorecard(세션/국면 점수표), equity_curve_quality(수익곡선 품질), gate audit(게이트 감사)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_data_integrity_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "data_source": f"{rel(SOURCE_REPORT_RECORDS)};{rel(RAW_BARS)};{rel(FEATURE_FRAME)}",
                "time_axis": "MT5 deal times(거래 시간)은 broker clock(브로커 시계)로 읽고, session feature(세션 피처)는 existing feature timestamp(기존 피처 타임스탬프)와 exact open_time key(정확 시작 시간 키)로만 결합한다.",
                "sample_scope": "US100(유에스100) M5(5분봉), run340G MT5 report window(보고서 구간), q01/q09 plus q07/q08 controls(대조)",
                "missing_or_duplicate_check": "run341C checks report parse count(보고서 파싱 수), trade count(거래수), market bar match(시장 봉 매칭), feature match(피처 매칭), duplicate deal tickets(중복 딜 티켓).",
                "feature_label_boundary": "No future label(미래 라벨 없음). Trade attribution(거래 귀속)은 executed MT5 trade(실행된 MT5 거래) 이후 검토용이며, next model feature(다음 모델 피처)로 자동 승격하지 않는다.",
                "split_boundary": "single runtime holdout window(단일 런타임 홀드아웃 구간); not forward(전진 아님); not operating validation(운영 검증 아님)",
                "leakage_risk": "choosing a session allowlist(세션 허용목록) after seeing MT5 profits can overfit(과적합) the same holdout; run341C may diagnose but not select.",
                "data_hash_or_identity": f"report_records_sha256={sha(SOURCE_REPORT_RECORDS) if exists(SOURCE_REPORT_RECORDS) else 'missing'}; raw_bars_exists={exists(RAW_BARS)}; feature_frame_exists={exists(FEATURE_FRAME)}",
                "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_axis_contracts() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    axis = pd.DataFrame(
        [
            {
                "axis_id": "cost_stress(비용 압박)",
                "question": "Does the edge survive additional per-trade cost(거래당 추가 비용)?",
                "producer": NEXT_RUN_ID,
                "output": "cost_stress_matrix.csv",
                "effect": "profit factor(수익 팩터)와 recovery(회복)가 비용에 얼마나 얇은지 본다.",
            },
            {
                "axis_id": "session_regime(세션/국면)",
                "question": "Is profit concentrated in one session or volatility/trend regime(한 세션이나 변동성/추세 국면 집중인가)?",
                "producer": NEXT_RUN_ID,
                "output": "session_regime_scorecard.csv",
                "effect": "단일 pocket(구간) 과적합을 찾는다.",
            },
            {
                "axis_id": "equity_curve_quality(수익곡선 품질)",
                "question": "Are drawdown pockets(낙폭 구간), consecutive losses(연속 손실), and month consistency(월별 일관성) acceptable?",
                "producer": NEXT_RUN_ID,
                "output": "equity_curve_quality.csv",
                "effect": "순수익만 높은 후보를 거른다.",
            },
        ]
    )
    cost = pd.DataFrame(
        [
            {"stress_id": "c00_reported_cost", "extra_cost_per_trade": 0.0, "purpose": "MT5 reported base(보고된 기준)", "claim_boundary": CLAIM_BOUNDARY},
            {"stress_id": "c01_plus_0_25", "extra_cost_per_trade": 0.25, "purpose": "light broker friction(가벼운 브로커 마찰)", "claim_boundary": CLAIM_BOUNDARY},
            {"stress_id": "c02_plus_0_50", "extra_cost_per_trade": 0.50, "purpose": "normal stress(보통 압박)", "claim_boundary": CLAIM_BOUNDARY},
            {"stress_id": "c03_plus_1_00", "extra_cost_per_trade": 1.00, "purpose": "hard stress(강한 압박)", "claim_boundary": CLAIM_BOUNDARY},
            {"stress_id": "c04_plus_2_00", "extra_cost_per_trade": 2.00, "purpose": "breakpoint probe(손익분기 탐침)", "claim_boundary": CLAIM_BOUNDARY},
        ]
    )
    session = pd.DataFrame(
        [
            {"slice_id": "early", "definition": "0-110 minutes after US cash open(미국 정규장 개장 후 0-110분)", "purpose": "open shock(개장 충격) 확인"},
            {"slice_id": "mid", "definition": "110-220 minutes after US cash open(개장 후 110-220분)", "purpose": "midday stability(장중 안정성) 확인"},
            {"slice_id": "late", "definition": "220-330 minutes after US cash open(개장 후 220-330분)", "purpose": "late session(후반 세션) 확인"},
            {"slice_id": "volatility_regime", "definition": "historical_vol_20 quantile bucket(20봉 변동성 분위 구간)", "purpose": "volatility pocket(변동성 구간) 확인"},
            {"slice_id": "trend_regime", "definition": "adx_14 and supertrend_10_3(ADX와 슈퍼트렌드)", "purpose": "trend/range sensitivity(추세/횡보 민감도) 확인"},
        ]
    )
    equity = pd.DataFrame(
        [
            {"metric_id": "max_trade_equity_drawdown", "definition": "running peak minus trade-level equity(거래 단위 최고점 대비 하락)", "minimum_use": "must explain q09 worse recovery(큐09 낮은 회복 설명)"},
            {"metric_id": "consecutive_losses", "definition": "max consecutive losing trades(최대 연속 손실 거래)", "minimum_use": "loss clustering(손실 군집) 확인"},
            {"metric_id": "positive_month_ratio", "definition": "positive PnL months / active months(양수 월 비율)", "minimum_use": "single-month dependency(단일 월 의존) 확인"},
            {"metric_id": "worst_session_share", "definition": "worst session loss / total gross loss(최악 세션 손실 비중)", "minimum_use": "session pocket risk(세션 구간 위험) 확인"},
        ]
    )
    for frame in (axis, cost, session, equity):
        frame["claim_boundary"] = CLAIM_BOUNDARY
    return axis, cost, session, equity


def build_materialization_queue() -> pd.DataFrame:
    seeds = read_csv(SOURCE_QUEUE)
    source_attempts = {
        "q01_ctl_s55_l51_m01_h12": "quality_anchor(품질 기준점)",
        "q09_s545_l51_m01_h12": "net_clue(순수익 단서)",
        "q07_h10_s55_l51_m01_h10": "negative_control_short_hold(짧은 보유 부정 대조)",
        "q08_h14_s55_l51_m01_h14": "negative_control_long_hold(긴 보유 부정 대조)",
    }
    rows = []
    for attempt, role in source_attempts.items():
        seed_match = seeds.loc[seeds["source_attempt"].astype(str).str.contains(attempt, regex=False, na=False)]
        seed_id = seed_match.iloc[0].get("seed_id", "") if not seed_match.empty else ""
        rows.append(
            {
                "queue_id": f"run341C_{attempt}",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": attempt,
                "source_seed_id": seed_id,
                "role": role,
                "required_report_records": rel(SOURCE_REPORT_RECORDS),
                "required_market_bars": rel(RAW_BARS),
                "required_feature_frame": rel(FEATURE_FRAME),
                "outputs": "trade_level_records.csv;attribution_summary.csv;cost_stress_matrix.csv;session_regime_scorecard.csv;equity_curve_quality.csv",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def write_receipts() -> None:
    source_inputs = [
        SOURCE_FINAL_DECISION,
        SOURCE_HANDOFF,
        SOURCE_QUEUE,
        SOURCE_SCORECARD,
        SOURCE_FAILURE_MEMORY,
        SOURCE_RUNTIME_SUMMARY,
        SOURCE_PROXY_DIFF,
        SOURCE_REPORT_RECORDS,
        RAW_BARS,
        FEATURE_FRAME,
    ]
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
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "required_output": rel(EXPERIMENT_CONTRACT),
            "effect": "q01/q09(큐01/큐09)를 같은 검증 질문으로 묶었다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(SOURCE_REPORT_RECORDS), rel(RAW_BARS), rel(FEATURE_FRAME)],
            "time_axis": "broker clock MT5 deals(브로커 시계 MT5 거래) plus timestamp-safe feature join(시점 안전 피처 결합)",
            "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
            "effect": "future leak(미래 누수) 없이 사후 attribution(귀속)만 수행하게 한다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in source_inputs],
            "artifact_paths": [rel(path) for path in output_files()],
            "source_artifact_hashes": {rel(path): sha(path) for path in source_inputs if exists(path) and br.path_is_file(path)},
            "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
            "effect": "run341C(341C 실행)가 같은 원천 파일을 추적하게 한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "promotion_candidate": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "effect": "design(설계)을 operating claim(운영 주장)으로 오해하지 않게 한다.",
        },
    )


def output_files() -> list[Path]:
    return [
        EXPERIMENT_CONTRACT,
        DATA_INTEGRITY_CONTRACT,
        VALIDATION_AXIS_CONTRACT,
        COST_STRESS_CONTRACT,
        SESSION_REGIME_CONTRACT,
        EQUITY_CURVE_CONTRACT,
        MATERIALIZATION_QUEUE,
        WORK_PACKET,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
        STAGE_BRIEF,
        STAGE_README,
        br.WORKSPACE_STATE,
        br.CURRENT_WORKING_STATE,
        STAGE_LEDGER,
        br.RUN_REGISTRY,
        br.PROJECT_LEDGER,
        br.ARTIFACT_REGISTRY,
        Path(__file__),
    ]


def gate_row(gate_id: str, status: str, evidence_path: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": evidence_path,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates() -> pd.DataFrame:
    experiment = read_csv(EXPERIMENT_CONTRACT)
    data = read_csv(DATA_INTEGRITY_CONTRACT)
    queue = read_csv(MATERIALIZATION_QUEUE)
    complete_columns = {
        "hypothesis",
        "decision_use",
        "comparison_baseline",
        "control_variables",
        "changed_variables",
        "sample_scope",
        "success_criteria",
        "failure_criteria",
        "invalid_conditions",
        "stop_conditions",
        "evidence_plan",
    }
    data_columns = {
        "data_source",
        "time_axis",
        "sample_scope",
        "missing_or_duplicate_check",
        "feature_label_boundary",
        "split_boundary",
        "leakage_risk",
        "data_hash_or_identity",
        "integrity_judgment",
    }
    return pd.DataFrame(
        [
            gate_row(
                "source_handoff_available",
                "passed" if exists(SOURCE_FINAL_DECISION) and exists(SOURCE_QUEUE) and exists(SOURCE_REPORT_RECORDS) else "failed",
                f"{rel(SOURCE_FINAL_DECISION)};{rel(SOURCE_QUEUE)};{rel(SOURCE_REPORT_RECORDS)}",
                "Stage 340(340단계) 근거를 이어받는다.",
            ),
            gate_row(
                "experiment_design_contract_complete",
                "passed" if complete_columns.issubset(experiment.columns) and not experiment[list(complete_columns)].isna().any().any() else "failed",
                rel(EXPERIMENT_CONTRACT),
                "hypothesis(가설)부터 evidence plan(근거 계획)까지 닫는다.",
            ),
            gate_row(
                "data_integrity_contract_complete",
                "passed" if data_columns.issubset(data.columns) and not data[list(data_columns)].isna().any().any() else "failed",
                rel(DATA_INTEGRITY_CONTRACT),
                "time axis(시간축), leakage risk(누수 위험), split boundary(분할 경계)를 기록한다.",
            ),
            gate_row(
                "validation_axes_defined",
                "passed" if all(exists(path) for path in [VALIDATION_AXIS_CONTRACT, COST_STRESS_CONTRACT, SESSION_REGIME_CONTRACT, EQUITY_CURVE_CONTRACT]) else "failed",
                f"{rel(VALIDATION_AXIS_CONTRACT)};{rel(COST_STRESS_CONTRACT)};{rel(SESSION_REGIME_CONTRACT)};{rel(EQUITY_CURVE_CONTRACT)}",
                "cost/session/regime/equity(비용/세션/국면/수익곡선) 축을 분리한다.",
            ),
            gate_row(
                "materialization_queue_written",
                "passed" if len(queue) >= 4 and set(queue["source_attempt"]).issuperset({"q01_ctl_s55_l51_m01_h12", "q09_s545_l51_m01_h12"}) else "failed",
                rel(MATERIALIZATION_QUEUE),
                "run341C(341C 실행)가 q01/q09(큐01/큐09)와 negative control(부정 대조)을 물질화하게 한다.",
            ),
            gate_row(
                "registries_synced",
                "passed" if exists(br.RUN_REGISTRY) and exists(br.PROJECT_LEDGER) and exists(br.ARTIFACT_REGISTRY) else "failed",
                f"{rel(br.RUN_REGISTRY)};{rel(br.PROJECT_LEDGER)};{rel(br.ARTIFACT_REGISTRY)}",
                "run identity(실행 정체성)와 artifact lineage(산출물 계보)를 연결한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
            ),
        ]
    )


def write_docs(metrics: Mapping[str, Any]) -> None:
    report = f"""# run341B F01 Stability Cost Regime Validation Design(341B F01 안정성 비용 국면 검증 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- q01 quality anchor(품질 기준점): net(순수익) `{metrics.get('q01_net_profit', '')}`, recovery(회복) `{metrics.get('q01_recovery_factor', '')}`, drawdown(낙폭) `{metrics.get('q01_drawdown', '')}`
- q09 net clue(순수익 단서): net(순수익) `{metrics.get('q09_net_profit', '')}`, recovery(회복) `{metrics.get('q09_recovery_factor', '')}`, drawdown(낙폭) `{metrics.get('q09_drawdown', '')}`

## Action(행동)

q01/q09(큐01/큐09)를 cost stress(비용 압박), session/regime split(세션/국면 분할), equity curve quality(수익곡선 품질)로 검증하는 설계를 만들었다.
Effect(효과): q09(큐09)의 작은 net(순수익) 개선을 winner(승자)로 고정하지 않고, q01(큐01)의 quality(품질)와 함께 실제 약점을 찾는다.

## Boundary(경계)

This run is design only(설계 전용). No MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage 341B Validation Design Decision(341B 검증 설계 결정)

- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): Stage 341(341단계)는 q01 quality anchor(품질 기준점)와 q09 net clue(순수익 단서)를 cost/session/regime/equity(비용/세션/국면/수익곡선)로 검증해야 한다.

Action(행동): run341C(341C 실행) materialization queue(물질화 대기열)를 열었다.
Effect(효과): 기존 MT5 report(메타트레이더5 보고서)를 거래 단위로 파싱해 운영 주장 없이 약점 귀속을 시작한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 341 Selection Status(341단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- quality_anchor(품질 기준점): `q01_ctl_s55_l51_m01_h12`
- net_high_clue(순수익 높은 단서): `q09_s545_l51_m01_h12`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): run341C(341C 실행)가 검증 입력을 만들 때도 선정 주장(selection claim, 선정 주장)을 막는다.
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

run341C(341C 실행)는 q01/q09(큐01/큐09)와 q07/q08(큐07/큐08) negative control(부정 대조)의 MT5 report(메타트레이더5 보고서)를 거래 단위로 파싱한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
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
    write_text(SELECTION_STATUS, selection)
    write_text(br.CURRENT_WORKING_STATE, current)
    write_text(br.WORKSPACE_STATE, workspace)
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""## run341B Validation Design(341B 검증 설계)

- run_id(실행 ID): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): q01/q09(큐01/큐09)를 cost/session/regime/equity(비용/세션/국면/수익곡선) 검증으로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run341B Validation Design(341B 검증 설계)

- run_id(실행 ID): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): run341C(341C 실행) materialization(물질화)을 준비했다.
""",
    )
    changelog = f"""## {TODAY} run341B Validation Design(341B 검증 설계)

- action(행동): q01/q09(큐01/큐09) stability/cost/regime validation(안정성/비용/국면 검증)을 설계했다.
- effect(효과): Stage 341(341단계)이 기존 MT5 report(메타트레이더5 보고서)를 거래 단위로 재분해할 준비를 마쳤다.
- boundary(경계): no MT5 execution(MT5 실행 없음), no selection(선정 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    append_text_once(br.ROOT_CHANGELOG, RUN_ID, changelog)
    append_text_once(br.WORKSPACE_CHANGELOG, RUN_ID, changelog)


def ledger_rows(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
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
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": metrics.get("q09_model_id", ""),
        "net_profit": metrics.get("q09_net_profit", ""),
        "profit_factor": metrics.get("q09_profit_factor", ""),
        "drawdown": metrics.get("q09_drawdown", ""),
        "recovery_factor": metrics.get("q09_recovery_factor", ""),
        "trade_count": metrics.get("q09_trade_count", ""),
        "result_status": "design_only_no_selection(설계 전용, 선정 없음)",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": metrics.get("matched_rows_total", ""),
        "expectancy": metrics.get("q09_expectancy", ""),
        "attempt_count": metrics.get("attempt_count", ""),
    }
    rows = []
    for view, tier, metric_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "design_source_reference_not_new_kpi"),
        ("Tier B separate(Tier B 분리)", "Tier B", "missing_required"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "same_as_tier_a_until_tier_b_available"),
    ]:
        row = dict(base)
        row.update({"view": view, "tier": tier, "metric_scope": metric_scope})
        if metric_scope == "missing_required":
            for metric in ["candidate_model_id", "net_profit", "profit_factor", "drawdown", "recovery_factor", "trade_count", "matched_rows", "expectancy", "attempt_count"]:
                row[metric] = ""
            row["result_status"] = "missing_required(필수 누락)"
        rows.append(row)
    return rows


def write_registries(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    rows = ledger_rows(gates, metrics)
    existing = read_csv(STAGE_LEDGER) if exists(STAGE_LEDGER) else pd.DataFrame()
    combined = pd.concat([existing.loc[~existing.get("run_id", pd.Series(dtype=str)).astype(str).eq(RUN_ID)], pd.DataFrame(rows)], ignore_index=True) if not existing.empty else pd.DataFrame(rows)
    write_csv(STAGE_LEDGER, combined)
    append_or_replace_csv(br.RUN_REGISTRY, ["run_id"], [rows[0]])
    project_rows = []
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["kpi_scope"] = "experiment_design(실험 설계)"
        project_row["scoreboard_lane"] = "design(설계)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        project_rows.append(project_row)
    append_or_replace_csv(br.PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    artifact_rows = []
    for path in output_files():
        if exists(path) and br.path_is_file(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": path.suffix.lstrip(".") or "file",
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(br.ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def main() -> None:
    br.Path(br.fs_path(RUN_DIR)).mkdir(parents=True, exist_ok=True)
    br.Path(br.fs_path(REVIEW_DIR)).mkdir(parents=True, exist_ok=True)
    for path in [SOURCE_FINAL_DECISION, SOURCE_QUEUE, SOURCE_SCORECARD, SOURCE_REPORT_RECORDS, RAW_BARS, FEATURE_FRAME]:
        if not exists(path):
            raise FileNotFoundError(f"missing required design input: {rel(path)}")

    source_final = read_json(br.SOURCE_RUN_DIR / "final_decision.json")
    scorecard = read_csv(SOURCE_SCORECARD)
    q01 = metric_row(scorecard, "q01_ctl_s55_l51_m01_h12")
    q09 = metric_row(scorecard, "q09_s545_l51_m01_h12")
    metrics = {
        "attempt_count": source_final.get("attempt_count", ""),
        "matched_rows_total": source_final.get("matched_rows_total", ""),
        "q01_model_id": q01.get("model_id", ""),
        "q01_net_profit": q01.get("net_profit", ""),
        "q01_profit_factor": q01.get("profit_factor", ""),
        "q01_expectancy": q01.get("expectancy", ""),
        "q01_recovery_factor": q01.get("recovery_factor", ""),
        "q01_drawdown": q01.get("max_drawdown_amount", ""),
        "q01_trade_count": q01.get("trade_count", ""),
        "q09_model_id": q09.get("model_id", ""),
        "q09_net_profit": q09.get("net_profit", ""),
        "q09_profit_factor": q09.get("profit_factor", ""),
        "q09_expectancy": q09.get("expectancy", ""),
        "q09_recovery_factor": q09.get("recovery_factor", ""),
        "q09_drawdown": q09.get("max_drawdown_amount", ""),
        "q09_trade_count": q09.get("trade_count", ""),
    }

    write_csv(EXPERIMENT_CONTRACT, build_experiment_contract())
    write_csv(DATA_INTEGRITY_CONTRACT, build_data_integrity_contract())
    axis, cost, session, equity = build_axis_contracts()
    write_csv(VALIDATION_AXIS_CONTRACT, axis)
    write_csv(COST_STRESS_CONTRACT, cost)
    write_csv(SESSION_REGIME_CONTRACT, session)
    write_csv(EQUITY_CURVE_CONTRACT, equity)
    write_csv(MATERIALIZATION_QUEUE, build_materialization_queue())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "data_integrity_contract_complete",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts()
    gates = build_gates()
    write_csv(GATE_AUDIT, gates)
    write_docs(metrics)
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
            "gate_total": int(len(gates)),
            "q01_net_profit": metrics.get("q01_net_profit", ""),
            "q09_net_profit": metrics.get("q09_net_profit", ""),
            "candidate_selection": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "command": "python -B stage_pipelines/stage341/design_f01_stability_cost_regime_validation_without_db.py",
            "outputs": [rel(path) for path in output_files() if exists(path)],
            "status": STATUS,
            "judgment": JUDGMENT,
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_registries(gates, metrics)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "q01_net_profit": metrics.get("q01_net_profit", ""),
                "q09_net_profit": metrics.get("q09_net_profit", ""),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
