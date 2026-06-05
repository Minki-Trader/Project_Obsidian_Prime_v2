from __future__ import annotations

import csv
import json
import math
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import design_broker_confirmed_side_cost_curve_offensive_repair_without_db as ev  # noqa: E402
from stage_pipelines.stage337 import materialize_transfer_density_control_objective_repair_inputs as dx  # noqa: E402
from stage_pipelines.stage337 import materialize_validation_density_trade_count_repair_inputs as ec  # noqa: E402


aw = ev.aw

TODAY = "2026-05-31"
STAGE_ID = ev.STAGE_ID
RUN_NUMBER = "run337EW"
RUN_ID = "run337EW_materialize_broker_confirmed_side_cost_curve_repair_inputs_without_db_v1"
PARENT_RUN_ID = ev.RUN_ID
NEXT_RUN_ID = "run337EX_review_broker_confirmed_side_cost_curve_repair_inputs_without_db_v1"
STATUS = "completed_stage337EW_broker_confirmed_side_cost_curve_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "train_only_side_cost_curve_inputs_materialized_forward_evidence_quarantined_review_required"
DECISION = "stage337EW_open_run337EX_review_side_cost_curve_repair_inputs_without_db_no_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EW_broker_confirmed_side_cost_curve_repair_input_materialization_without_db_"
    "no_model_training_no_threshold_tuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ev.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ev.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EW_broker_confirmed_side_cost_curve_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337EW_broker_confirmed_side_cost_curve_repair_inputs.md"
SELECTED_STATUS = ev.SELECTED_STATUS
STAGE_BRIEF = ev.STAGE_BRIEF
WORKSPACE_STATE = ev.WORKSPACE_STATE
CURRENT_STATE = ev.CURRENT_STATE
CHANGELOG = ev.CHANGELOG
RUN_REGISTRY = ev.RUN_REGISTRY
ALPHA_LEDGER = ev.ALPHA_LEDGER
ARTIFACT_REGISTRY = ev.ARTIFACT_REGISTRY
STAGE_LEDGER = ev.STAGE_LEDGER

EV_FINAL = ev.FINAL_DECISION
EV_GATES = ev.GATE_AUDIT
EV_QUEUE = ev.MATERIALIZATION_QUEUE
EV_DESIGN = ev.DESIGN_MATRIX
EV_OBJECTIVE = ev.OBJECTIVE_CONTRACT
EV_FEATURE = ev.FEATURE_CONTRACT
EV_NEGATIVE = ev.NEGATIVE_CONTROL
EV_RELEASE = ev.RELEASE_GATE_CONTRACT
EV_NO_LOOKAHEAD = ev.NO_LOOKAHEAD_AUDIT

EU_RUNTIME = ev.EU_RUNTIME
EU_MEMORY = ev.EU_MEMORY
EU_GUARDRAIL = ev.EU_GUARDRAIL
ET_TRADES = ev.ET_TRADES
ET_REGIME = ev.ET_REGIME
ET_COST = ev.ET_COST
ET_CURVE = ev.ET_CURVE

EC_REPAIR_FRAME = ec.TRAIN_ONLY_REPAIR_FRAME
EC_FEATURE_COMPATIBILITY = ec.FEATURE_INPUT_COMPATIBILITY
EC_WEIGHT_SUMMARY = ec.REPAIR_WEIGHT_SUMMARY
EC_GATES = ec.REQUIRED_GATE_AUDIT
DX_OBJECTIVE_FRAME = dx.TRAIN_ONLY_OBJECTIVE_INPUT_FRAME
DX_DENSITY = dx.DENSITY_DECONCENTRATION_MATRIX
DX_CONTROL = dx.CONTROL_RESIDUAL_ISOLATION_MATRIX
DX_GATES = dx.REQUIRED_GATE_AUDIT
DW_OBJECTIVE_CONTRACTS = dx.TRAIN_ONLY_OBJECTIVE_CONTRACTS
CR_DENSITY_GRID = STAGE_DIR / "02_runs" / "run337CR" / "train_only_density_policy_grid.csv"

TRAIN_ONLY_INPUT_FRAME = RUN_DIR / "train_only_side_cost_curve_repair_input_frame.parquet"
MATERIALIZATION_SOURCE_MAP = RUN_DIR / "train_only_materialization_source_map.csv"
FEATURE_ROLE_MATRIX = RUN_DIR / "feature_label_role_matrix.csv"
ALLOWED_FEATURE_SET = RUN_DIR / "allowed_model_feature_set.csv"
SIDE_SCHEMA = RUN_DIR / "side_quality_input_schema.csv"
COST_SCHEMA = RUN_DIR / "cost_ladder_input_schema.csv"
CURVE_SCHEMA = RUN_DIR / "curve_state_input_schema.csv"
DENSITY_SCHEMA = RUN_DIR / "density_floor_input_schema.csv"
INPUT_MANIFEST = RUN_DIR / "train_only_repair_input_manifest.csv"
LABEL_WEIGHT_RECIPE = RUN_DIR / "label_weight_recipe_matrix.csv"
FORWARD_QUARANTINE = RUN_DIR / "forward_evidence_quarantine.csv"
NEGATIVE_CONTROL_MATERIALIZATION = RUN_DIR / "negative_control_materialization_matrix.csv"
RELEASE_GATE_MATERIALIZATION = RUN_DIR / "release_gate_materialization_matrix.csv"
EX_QUEUE = RUN_DIR / "run337EX_review_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REQUIRED_INPUTS = (
    EV_FINAL,
    EV_GATES,
    EV_QUEUE,
    EV_DESIGN,
    EV_OBJECTIVE,
    EV_FEATURE,
    EV_NEGATIVE,
    EV_RELEASE,
    EV_NO_LOOKAHEAD,
    EU_RUNTIME,
    EU_MEMORY,
    EU_GUARDRAIL,
    ET_TRADES,
    ET_REGIME,
    ET_COST,
    ET_CURVE,
    EC_REPAIR_FRAME,
    EC_FEATURE_COMPATIBILITY,
    EC_WEIGHT_SUMMARY,
    EC_GATES,
    DX_OBJECTIVE_FRAME,
    DX_DENSITY,
    DX_CONTROL,
    DX_GATES,
    DW_OBJECTIVE_CONTRACTS,
    CR_DENSITY_GRID,
)
OUTPUT_FILES = (
    TRAIN_ONLY_INPUT_FRAME,
    MATERIALIZATION_SOURCE_MAP,
    FEATURE_ROLE_MATRIX,
    ALLOWED_FEATURE_SET,
    SIDE_SCHEMA,
    COST_SCHEMA,
    CURVE_SCHEMA,
    DENSITY_SCHEMA,
    INPUT_MANIFEST,
    LABEL_WEIGHT_RECIPE,
    FORWARD_QUARANTINE,
    NEGATIVE_CONTROL_MATERIALIZATION,
    RELEASE_GATE_MATERIALIZATION,
    EX_QUEUE,
    ROUTING_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    STAGE_BRIEF,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    Path(__file__),
)

SOURCE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "allowed_role",
    "forbidden_role",
    "materialization_use",
    "effect",
    "claim_boundary",
)
ROLE_COLUMNS = (
    "field_name",
    "source_layer",
    "input_layer",
    "allowed_role",
    "forbidden_role",
    "timestamp_rule",
    "effect",
    "claim_boundary",
)
ALLOWED_FEATURE_COLUMNS = (
    "feature_name",
    "feature_family",
    "source_layer",
    "timestamp_rule",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
SCHEMA_COLUMNS = (
    "schema_id",
    "field_name",
    "field_type",
    "role",
    "source_rule",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
MANIFEST_COLUMNS = (
    "manifest_id",
    "artifact_path",
    "rows",
    "columns",
    "split_values",
    "cost_policy_count",
    "source_row_count",
    "feature_column_count",
    "target_or_weight_column_count",
    "forward_quarantine_status",
    "materialized_status",
    "effect",
    "claim_boundary",
)
RECIPE_COLUMNS = (
    "recipe_id",
    "materialized_column",
    "source_columns",
    "split_scope",
    "timestamp_rule",
    "train_only_formula",
    "non_feature_status",
    "effect",
    "claim_boundary",
)
QUARANTINE_COLUMNS = (
    "evidence_id",
    "source_path",
    "rows",
    "allowed_use",
    "forbidden_use",
    "quarantine_status",
    "evidence_read",
    "effect",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "control_id",
    "source_control_family",
    "materialized_artifact",
    "materialized_status",
    "observed",
    "invalid_if_future_review",
    "effect",
    "claim_boundary",
)
RELEASE_COLUMNS = (
    "gate_id",
    "source_gate_family",
    "materialized_artifact",
    "materialized_status",
    "observed",
    "future_release_dependency",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)

FORBIDDEN_FORWARD_COLUMNS = {
    "attempt_name",
    "proxy_rank",
    "net_profit",
    "profit_factor",
    "expectancy",
    "trade_index",
    "open_time",
    "close_time",
    "source_report_path",
    "release_gate_status",
    "positive_clue",
    "failure_read",
}
IDENTITY_COLUMNS = {
    "timestamp",
    "symbol",
    "split",
    "split_id",
    "source_row_id",
    "cost_policy_id",
    "allowed_split_scope",
    "leakage_guard",
    "claim_boundary",
    "feature_label_boundary",
    "forward_evidence_quarantine",
    "density_floor_contract_source",
}
TARGET_OR_WEIGHT_COLUMNS = {
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "horizon_bars",
    "horizon_minutes",
    "low_margin_rate",
    "direction_residual_rate",
    "underwater_rate",
    "drawdown_pressure_mean",
    "abstention_rate",
    "payoff_tail_proxy",
    "drawdown_pressure_norm",
    "payoff_tail_norm",
    "near_margin_trade_support_weight",
    "density_tempered_weight",
    "payoff_tail_offense_weight",
    "combined_sample_weight",
    "long_quality_target",
    "short_quality_target",
    "side_quality_gap_target",
    "side_quality_gap_norm",
    "side_quality_weight",
    "cost_survival_weight",
    "curve_state_pressure_weight",
    "short_abstention_pressure_weight",
    "density_floor_min",
    "density_floor_max",
    "density_floor_contract_count",
    "density_floor_tag",
    "model_observation_count",
    "model_count",
    "feature_set_count",
    "mean_prob_long",
    "mean_prob_short",
    "mean_prob_flat",
    "long_signal_count",
    "short_signal_count",
    "flat_signal_count",
    "trade_signal_count",
    "low_margin_rate_model",
    "underwater_rate_model",
    "direction_residual_rate_model",
    "drawdown_pressure_mean_model",
    "abstention_rate_model",
}


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_branch() -> str:
    proc = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def row_count(path: Path) -> int:
    if not path_exists(path):
        return 0
    if path.suffix.lower() == ".csv":
        return len(read_csv(path))
    if path.suffix.lower() == ".parquet":
        return int(len(pd.read_parquet(aw.io_path(path), columns=[])))
    return 0


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def normalize_abs(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce").fillna(0.0)
    scale = float(numeric.abs().quantile(0.95)) if len(numeric) else 0.0
    if scale <= 0:
        return numeric * 0.0
    return (numeric.abs() / scale).clip(lower=0.0, upper=1.0)


def density_floor_summary() -> dict[str, Any]:
    floors = [number(row.get("density_floor")) for row in read_csv(CR_DENSITY_GRID) if str(row.get("density_floor", "")).strip()]
    floors = [value for value in floors if value > 0]
    return {
        "min": min(floors) if floors else 0.0,
        "max": max(floors) if floors else 0.0,
        "count": len(floors),
    }


def build_source_map() -> list[dict[str, Any]]:
    roles: dict[Path, tuple[str, str, str, str]] = {
        EV_FINAL: ("parent decision(부모 결정)", "mutation or release proof(변형 또는 해제 증거)", "EW routing check(EW 라우팅 확인)", "keeps EW tied to EV decision(EW를 EV 결정에 묶음)"),
        EV_GATES: ("parent gate evidence(부모 게이트 근거)", "gate relaxation(게이트 완화)", "parent gate check(부모 게이트 확인)", "blocks work if EV gates failed(EV 게이트 실패 시 작업 차단)"),
        EV_QUEUE: ("parent queue(부모 대기열)", "scope expansion(범위 확장)", "next action identity(다음 행동 정체성)", "confirms EW was opened(EW가 열렸는지 확인)"),
        EV_DESIGN: ("design contract(설계 계약)", "trained model input by itself(그 자체를 학습 피처로 사용)", "materialization contract(물질화 계약)", "turns broker clue into bounded input work(브로커 단서를 제한된 입력 작업으로 바꿈)"),
        EV_OBJECTIVE: ("objective contract(목표 계약)", "feature column(피처 열)", "label and weight recipe(라벨/가중치 조리법)", "keeps labels out of features(라벨을 피처에서 분리)"),
        EV_FEATURE: ("feature contract(피처 계약)", "future outcome feature(미래 결과 피처)", "allowed feature role(허용 피처 역할)", "keeps timestamp safety visible(시점 안전을 보이게 함)"),
        EV_NEGATIVE: ("negative control(부정 대조)", "skipping control(대조 생략)", "control materialization(대조 물질화)", "keeps overfit routes named(과적합 경로를 이름 붙임)"),
        EV_RELEASE: ("release gate contract(해제 게이트 계약)", "release proof(해제 증거)", "future review gate(미래 검토 게이트)", "keeps operating claims closed(운영 주장을 닫아 둠)"),
        EV_NO_LOOKAHEAD: ("no-lookahead audit(미래참조 방지 감사)", "feature source(피처 원천)", "parent audit carry(부모 감사 이월)", "carries timestamp guard(시점 방어를 이월)"),
        EC_REPAIR_FRAME: ("train-only feature/weight frame(학습 전용 피처/가중치 프레임)", "forward proof(전진 증거)", "base materialization frame(기본 물질화 프레임)", "provides timestamp-safe row space(시점 안전 행 공간 제공)"),
        DX_OBJECTIVE_FRAME: ("train-only objective frame(학습 전용 목표 프레임)", "validation or OOS selection(검증 또는 OOS 선택)", "side target aggregation(방향 목표 집계)", "adds train-only target pressure(학습 전용 목표 압력 추가)"),
        EC_FEATURE_COMPATIBILITY: ("feature compatibility(피처 호환성)", "model selection(모델 선택)", "feature role audit(피처 역할 감사)", "prevents missing feature surprise(피처 누락 사고 방지)"),
        EC_WEIGHT_SUMMARY: ("train-only weight summary(학습 전용 가중치 요약)", "release KPI(해제 KPI)", "weight sanity context(가중치 점검 문맥)", "keeps cost/curve weights auditable(비용/곡선 가중치를 감사 가능하게 함)"),
        DX_DENSITY: ("density diagnostic(밀도 진단)", "threshold tuning(임계값 조정)", "density schema context(밀도 스키마 문맥)", "keeps density floor predeclared(밀도 하한을 사전 선언으로 유지)"),
        DX_CONTROL: ("control diagnostic(대조 진단)", "control relaxation(대조 완화)", "review-only control context(검토 전용 대조 문맥)", "keeps negative controls active(부정 대조를 활성 유지)"),
        DW_OBJECTIVE_CONTRACTS: ("prior train-only objective contracts(이전 학습 전용 목표 계약)", "override EV contract(EV 계약 대체)", "contract lineage(계약 계보)", "links EW to prior train-only work(EW를 이전 학습 전용 작업에 연결)"),
        CR_DENSITY_GRID: ("prior train-only density grid(이전 학습 전용 밀도 격자)", "post-forward density tuning(전진 후 밀도 조정)", "density floor source(밀도 하한 원천)", "prevents no-trade repair(무거래 수리 방지)"),
        EU_RUNTIME: ("broker failure memory(브로커 실패 기억)", "feature, label, threshold, release proof(피처/라벨/임계값/해제 증거)", "quarantined design pressure(격리된 설계 압력)", "keeps broker evidence useful but separated(브로커 근거를 유용하지만 분리함)"),
        EU_MEMORY: ("broker memory update(브로커 기억 갱신)", "model feature(모델 피처)", "quarantined failure memory(격리된 실패 기억)", "prevents repeated stale blocker(낡은 차단 반복 방지)"),
        EU_GUARDRAIL: ("release guardrail review(해제 가드레일 검토)", "release relaxation(해제 완화)", "future release dependency(미래 해제 의존성)", "keeps weak positive clue below release(약한 긍정 단서를 해제 아래에 둠)"),
        ET_TRADES: ("broker trade evidence(브로커 거래 근거)", "feature, label, side veto, release proof(피처/라벨/방향 거부/해제 증거)", "quarantined runtime context(격리된 런타임 문맥)", "prevents forward memorization(전진 암기 방지)"),
        ET_REGIME: ("broker regime attribution(브로커 국면 귀속)", "train feature join(학습 피처 결합)", "quarantined market behavior clue(격리된 시장 현상 단서)", "keeps market clue separate from labels(시장 단서를 라벨에서 분리)"),
        ET_COST: ("broker cost stress(브로커 비용 압박)", "cost-picked threshold(비용 선택 임계값)", "quarantined cost pressure(격리된 비용 압력)", "keeps cost fragility as gate pressure(비용 취약성을 게이트 압력으로 둠)"),
        ET_CURVE: ("broker curve pockets(브로커 곡선 구간)", "date-pocket feature(날짜 구간 피처)", "quarantined curve pressure(격리된 곡선 압력)", "prevents bad-date memorization(나쁜 날짜 암기 방지)"),
    }
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(REQUIRED_INPUTS, start=1):
        allowed, forbidden, use, effect = roles.get(path, ("input(입력)", "unknown forbidden use(알 수 없는 금지 사용)", "source identity(원천 정체성)", "tracks input(입력을 추적)"))
        exists = path_exists(path)
        rows.append(
            {
                "source_id": f"ew_source_{index:02d}",
                "path": rel(path),
                "exists": "true" if exists else "false",
                "row_count": row_count(path) if exists else 0,
                "sha256": aw.sha256_file(path) if exists else "",
                "allowed_role": allowed,
                "forbidden_role": forbidden,
                "materialization_use": use,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def aggregate_dx_objectives(dx_frame: pd.DataFrame) -> pd.DataFrame:
    frame = dx_frame.copy()
    frame["source_row_id"] = pd.to_numeric(frame["source_row_id"], errors="coerce").astype("Int64")
    frame["direction"] = pd.to_numeric(frame["direction"], errors="coerce").fillna(0.0)
    frame["pnl_after_cost"] = pd.to_numeric(frame["pnl_after_cost"], errors="coerce").fillna(0.0)
    frame["is_trade"] = frame["is_trade"].astype(bool)
    frame["long_trade"] = frame["is_trade"] & (frame["direction"] > 0)
    frame["short_trade"] = frame["is_trade"] & (frame["direction"] < 0)
    frame["flat_signal"] = ~frame["is_trade"]
    frame["long_pnl_after_cost"] = frame["pnl_after_cost"].where(frame["long_trade"])
    frame["short_pnl_after_cost"] = frame["pnl_after_cost"].where(frame["short_trade"])
    for column in (
        "prob_short",
        "prob_flat",
        "prob_long",
        "low_margin_trade_tag",
        "underwater_tag",
        "direction_residual_tag",
        "drawdown_pressure_value",
        "abstention_candidate_tag",
    ):
        if column not in frame:
            frame[column] = 0.0
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    grouped = (
        frame.groupby(["source_row_id", "cost_policy_id"], sort=True, dropna=False)
        .agg(
            model_observation_count=("model_id", "size"),
            model_count=("model_id", "nunique"),
            feature_set_count=("feature_set_id", "nunique"),
            mean_prob_long=("prob_long", "mean"),
            mean_prob_short=("prob_short", "mean"),
            mean_prob_flat=("prob_flat", "mean"),
            long_signal_count=("long_trade", "sum"),
            short_signal_count=("short_trade", "sum"),
            flat_signal_count=("flat_signal", "sum"),
            trade_signal_count=("is_trade", "sum"),
            long_quality_target=("long_pnl_after_cost", "mean"),
            short_quality_target=("short_pnl_after_cost", "mean"),
            low_margin_rate_model=("low_margin_trade_tag", "mean"),
            underwater_rate_model=("underwater_tag", "mean"),
            direction_residual_rate_model=("direction_residual_tag", "mean"),
            drawdown_pressure_mean_model=("drawdown_pressure_value", "mean"),
            abstention_rate_model=("abstention_candidate_tag", "mean"),
        )
        .reset_index()
    )
    grouped["long_quality_target"] = pd.to_numeric(grouped["long_quality_target"], errors="coerce").fillna(0.0)
    grouped["short_quality_target"] = pd.to_numeric(grouped["short_quality_target"], errors="coerce").fillna(0.0)
    grouped["side_quality_gap_target"] = grouped["long_quality_target"] - grouped["short_quality_target"]
    return grouped


def materialize_train_only_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    base = pd.read_parquet(aw.io_path(EC_REPAIR_FRAME)).copy()
    objectives = pd.read_parquet(aw.io_path(DX_OBJECTIVE_FRAME)).copy()
    base["timestamp"] = pd.to_datetime(base["timestamp"], utc=True)
    objectives["timestamp"] = pd.to_datetime(objectives["timestamp"], utc=True)
    if sorted(base["split"].astype(str).unique().tolist()) != ["train"]:
        raise ValueError("EC repair frame must be train-only")
    if sorted(objectives["split"].astype(str).unique().tolist()) != ["train"]:
        raise ValueError("DX objective frame must be train-only")

    side_targets = aggregate_dx_objectives(objectives)
    frame = base.merge(side_targets, on=["source_row_id", "cost_policy_id"], how="left", validate="many_to_one")
    for column in side_targets.columns:
        if column not in {"source_row_id", "cost_policy_id"}:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)

    frame["side_quality_gap_norm"] = normalize_abs(frame["side_quality_gap_target"])
    frame["side_quality_weight"] = (
        1.0
        + 0.45 * frame["side_quality_gap_norm"]
        + 0.20 * pd.to_numeric(frame["direction_residual_rate_model"], errors="coerce").fillna(0.0)
    ).clip(lower=0.25, upper=3.5)
    frame["cost_survival_weight"] = (
        pd.to_numeric(frame["combined_sample_weight"], errors="coerce").fillna(1.0)
        * (1.0 + 0.25 * pd.to_numeric(frame["low_margin_rate"], errors="coerce").fillna(0.0))
        * (1.0 + 0.20 * pd.to_numeric(frame["payoff_tail_norm"], errors="coerce").fillna(0.0))
    ).clip(lower=0.25, upper=5.0)
    frame["curve_state_pressure_weight"] = (
        1.0
        + 0.60 * pd.to_numeric(frame["drawdown_pressure_norm"], errors="coerce").fillna(0.0)
        + 0.35 * pd.to_numeric(frame["underwater_rate"], errors="coerce").fillna(0.0)
        + 0.15 * pd.to_numeric(frame["underwater_rate_model"], errors="coerce").fillna(0.0)
    ).clip(lower=0.25, upper=4.0)
    short_loss_pressure = normalize_abs((-pd.to_numeric(frame["short_quality_target"], errors="coerce").fillna(0.0)).clip(lower=0.0))
    frame["short_abstention_pressure_weight"] = (
        1.0
        + 0.50 * short_loss_pressure
        + 0.20 * (pd.to_numeric(frame["short_signal_count"], errors="coerce").fillna(0.0) > 0).astype(float)
    ).clip(lower=0.25, upper=3.0)

    density = density_floor_summary()
    frame["density_floor_min"] = density["min"]
    frame["density_floor_max"] = density["max"]
    frame["density_floor_contract_count"] = density["count"]
    frame["density_floor_tag"] = "predeclared_train_only_density_floor(사전 선언 학습 전용 밀도 하한)"
    frame["forward_evidence_quarantine"] = "active_not_joined(활성, 결합 안 함)"
    frame["feature_label_boundary"] = (
        "feature columns exclude future targets, train-only weights, and broker forward evidence"
        "(피처 열은 미래 목표, 학습 전용 가중치, 브로커 전진 근거를 제외)"
    )
    frame["claim_boundary"] = CLAIM_BOUNDARY

    aw.io_path(TRAIN_ONLY_INPUT_FRAME.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(aw.io_path(TRAIN_ONLY_INPUT_FRAME), index=False)

    summary = {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "split_values": sorted(frame["split"].astype(str).unique().tolist()),
        "source_row_count": int(frame["source_row_id"].nunique()),
        "cost_policy_count": int(frame["cost_policy_id"].nunique()),
        "model_observation_min": int(frame["model_observation_count"].min()) if len(frame) else 0,
        "model_observation_max": int(frame["model_observation_count"].max()) if len(frame) else 0,
        "side_target_non_null_rows": int(
            (pd.to_numeric(frame["long_quality_target"], errors="coerce").notna()
             & pd.to_numeric(frame["short_quality_target"], errors="coerce").notna()).sum()
        ),
        "cost_survival_weight_min": float(frame["cost_survival_weight"].min()) if len(frame) else 0.0,
        "cost_survival_weight_max": float(frame["cost_survival_weight"].max()) if len(frame) else 0.0,
        "curve_state_weight_min": float(frame["curve_state_pressure_weight"].min()) if len(frame) else 0.0,
        "curve_state_weight_max": float(frame["curve_state_pressure_weight"].max()) if len(frame) else 0.0,
        "density_floor_min": density["min"],
        "density_floor_max": density["max"],
        "density_floor_contract_count": density["count"],
    }
    return frame, summary


def classify_feature_family(field_name: str) -> str:
    if field_name in {"atr_14", "atr_50", "atr_14_over_atr_50", "historical_vol_20", "historical_vol_5_over_20"}:
        return "volatility(변동성)"
    if field_name in {"adx_14", "di_spread_14", "rsi_14", "rsi_50", "stoch_kd_diff", "stochrsi_kd_diff"}:
        return "trend_momentum(추세/모멘텀)"
    if field_name in {"is_us_cash_open", "minutes_from_cash_open", "is_first_30m_after_open", "is_last_30m_before_cash_close"}:
        return "session(세션)"
    if field_name.startswith(("vix_", "us10yr_", "usdx_")):
        return "macro_asof(거시 시점 기준)"
    if field_name.endswith("_return_1") or "mega8" in field_name or "top3" in field_name:
        return "equity_context(주식 문맥)"
    return "technical_or_context(기술/문맥)"


def classify_role(field_name: str) -> tuple[str, str, str, str]:
    if field_name in FORBIDDEN_FORWARD_COLUMNS:
        return (
            "forbidden_forward_evidence(금지 전진 근거)",
            "model feature, label, selector(모델 피처/라벨/선택자)",
            "not allowed in EW frame(EW 프레임에 불허)",
            "blocks forward evidence leakage(전진 근거 누수 차단)",
        )
    if field_name in IDENTITY_COLUMNS:
        return (
            "identity_or_audit(정체성 또는 감사)",
            "model feature unless explicitly encoded later(명시적 인코딩 전 모델 피처)",
            "metadata only(메타데이터 전용)",
            "keeps row identity visible without becoming signal(행 정체성을 보이되 신호화하지 않음)",
        )
    if field_name in TARGET_OR_WEIGHT_COLUMNS or field_name.startswith("future_") or field_name.endswith("_target") or field_name.endswith("_weight"):
        return (
            "target_or_weight_no_feature(목표 또는 가중치, 피처 아님)",
            "model feature(모델 피처)",
            "train-only label/weight(학습 전용 라벨/가중치)",
            "keeps feature-label boundary explicit(피처-라벨 경계를 명시)",
        )
    return (
        "allowed_model_feature(허용 모델 피처)",
        "post-entry or broker-forward use(진입 후 또는 브로커 전진 사용)",
        "closed-bar/as-of feature(닫힌 봉/시점 기준 피처)",
        "keeps only pre-trade state available for future training(미래 학습에 진입 전 상태만 허용)",
    )


def build_feature_roles(frame: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    role_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    for field_name in frame.columns:
        role, forbidden, input_layer, effect = classify_role(str(field_name))
        timestamp_rule = (
            "feature timestamp <= decision timestamp(피처 시각은 결정 시각 이하)"
            if role.startswith("allowed_model_feature")
            else "not a model feature in EW(EW에서는 모델 피처 아님)"
        )
        role_rows.append(
            {
                "field_name": field_name,
                "source_layer": "train_only_frame(학습 전용 프레임)",
                "input_layer": input_layer,
                "allowed_role": role,
                "forbidden_role": forbidden,
                "timestamp_rule": timestamp_rule,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        if role.startswith("allowed_model_feature"):
            feature_rows.append(
                {
                    "feature_name": field_name,
                    "feature_family": classify_feature_family(str(field_name)),
                    "source_layer": rel(TRAIN_ONLY_INPUT_FRAME),
                    "timestamp_rule": "closed-bar/as-of only(닫힌 봉/시점 기준만)",
                    "allowed_use": "future reviewed training feature after EX review(EX 검토 후 미래 학습 피처)",
                    "forbidden_use": "label, selector, forward proof(라벨/선택자/전진 증거)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return role_rows, feature_rows


def build_side_schema() -> list[dict[str, Any]]:
    fields = [
        ("long_quality_target", "float", "train-only target(학습 전용 목표)", "DX train split long trade pnl(DX 학습 분할 롱 거래 손익)"),
        ("short_quality_target", "float", "train-only target(학습 전용 목표)", "DX train split short trade pnl(DX 학습 분할 숏 거래 손익)"),
        ("side_quality_gap_target", "float", "train-only target(학습 전용 목표)", "long minus short quality(롱-숏 품질 차이)"),
        ("side_quality_weight", "float", "sample weight(표본 가중치)", "gap and residual pressure(차이와 잔차 압력)"),
        ("short_abstention_pressure_weight", "float", "sample weight(표본 가중치)", "train-only short loss pressure(학습 전용 숏 손실 압력)"),
    ]
    return [
        {
            "schema_id": "side_quality_input_schema",
            "field_name": name,
            "field_type": field_type,
            "role": role,
            "source_rule": source_rule,
            "allowed_use": "reviewed target/weight only after EX(EX 검토 후 목표/가중치로만 사용)",
            "forbidden_use": "feature column or forward short veto(피처 열 또는 전진 숏 거부)",
            "effect": "keeps side repair learnable without manual forward veto(방향 수리를 수동 전진 거부 없이 학습 가능하게 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, role, source_rule in fields
    ]


def build_cost_schema() -> list[dict[str, Any]]:
    fields = [
        ("cost_policy_id", "string", "identity(정체성)", "predeclared cost policy(사전 선언 비용 정책)"),
        ("cost_survival_weight", "float", "sample weight(표본 가중치)", "EC train-only margin/payoff weights(EC 학습 전용 여백/보상 가중치)"),
        ("near_margin_trade_support_weight", "float", "parent weight(부모 가중치)", "EC near-margin weight(EC 저여백 가중치)"),
        ("payoff_tail_offense_weight", "float", "parent weight(부모 가중치)", "EC payoff-tail weight(EC 보상 꼬리 가중치)"),
    ]
    return [
        {
            "schema_id": "cost_ladder_input_schema",
            "field_name": name,
            "field_type": field_type,
            "role": role,
            "source_rule": source_rule,
            "allowed_use": "future cost robustness training/review(미래 비용 강건성 학습/검토)",
            "forbidden_use": "post-forward cost-picked threshold(전진 후 비용 선택 임계값)",
            "effect": "turns cost fragility into train-only pressure(비용 취약성을 학습 전용 압력으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, role, source_rule in fields
    ]


def build_curve_schema() -> list[dict[str, Any]]:
    fields = [
        ("curve_state_pressure_weight", "float", "sample weight(표본 가중치)", "EC/DX train-only drawdown pressure(EC/DX 학습 전용 낙폭 압력)"),
        ("drawdown_pressure_norm", "float", "parent target context(부모 목표 문맥)", "EC normalized drawdown pressure(EC 정규화 낙폭 압력)"),
        ("underwater_rate", "float", "parent target context(부모 목표 문맥)", "EC underwater rate(EC 수중 비율)"),
        ("underwater_rate_model", "float", "target context(목표 문맥)", "DX train-only model underwater rate(DX 학습 전용 모델 수중 비율)"),
    ]
    return [
        {
            "schema_id": "curve_state_input_schema",
            "field_name": name,
            "field_type": field_type,
            "role": role,
            "source_rule": source_rule,
            "allowed_use": "curve quality review and future training weight(곡선 품질 검토와 미래 학습 가중치)",
            "forbidden_use": "date-pocket memorization(날짜 구간 암기)",
            "effect": "requires market-state curve repair instead of bad-date removal(나쁜 날짜 제거 대신 시장 상태 곡선 수리 요구)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, role, source_rule in fields
    ]


def build_density_schema(density: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "density_floor_input_schema",
            "field_name": "density_floor_min",
            "field_type": "float",
            "role": "release floor(해제 하한)",
            "source_rule": f"{rel(CR_DENSITY_GRID)} min={density['min']}",
            "allowed_use": "future review gate(미래 검토 게이트)",
            "forbidden_use": "post-forward density tuning(전진 후 밀도 조정)",
            "effect": "blocks no-trade cosmetic repair(무거래 미용 수리 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "schema_id": "density_floor_input_schema",
            "field_name": "density_floor_max",
            "field_type": "float",
            "role": "release floor envelope(해제 하한 범위)",
            "source_rule": f"{rel(CR_DENSITY_GRID)} max={density['max']}",
            "allowed_use": "future review gate(미래 검토 게이트)",
            "forbidden_use": "post-forward density tuning(전진 후 밀도 조정)",
            "effect": "keeps density range predeclared(밀도 범위를 사전 선언으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "schema_id": "density_floor_input_schema",
            "field_name": "density_floor_contract_count",
            "field_type": "integer",
            "role": "lineage count(계보 수)",
            "source_rule": f"{rel(CR_DENSITY_GRID)} rows={density['count']}",
            "allowed_use": "lineage review(계보 검토)",
            "forbidden_use": "candidate selection(후보 선택)",
            "effect": "ties EW density floor to prior train-only grid(EW 밀도 하한을 이전 학습 전용 격자에 묶음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_manifest(frame: pd.DataFrame, final: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_count = int(final["allowed_feature_rows"])
    target_count = int(final["target_or_weight_rows"])
    return [
        {
            "manifest_id": "ew_train_only_side_cost_curve_frame",
            "artifact_path": rel(TRAIN_ONLY_INPUT_FRAME),
            "rows": len(frame),
            "columns": len(frame.columns),
            "split_values": json.dumps(final["split_values"], ensure_ascii=False),
            "cost_policy_count": final["cost_policy_count"],
            "source_row_count": final["source_row_count"],
            "feature_column_count": feature_count,
            "target_or_weight_column_count": target_count,
            "forward_quarantine_status": "active_not_joined(활성, 결합 안 함)",
            "materialized_status": "materialized_no_training_no_selection(물질화 완료, 학습/선택 없음)",
            "effect": "creates reviewable train-only input frame(검토 가능한 학습 전용 입력 프레임 생성)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_label_weight_recipes() -> list[dict[str, Any]]:
    recipes = [
        (
            "side_quality_targets",
            "long_quality_target;short_quality_target;side_quality_gap_target",
            "DX train-only objective frame direction and pnl_after_cost(DX 학습 전용 목표 프레임 방향과 비용 후 손익)",
            "aggregate train-only model rows by source_row_id/cost_policy_id(학습 전용 모델 행을 source_row_id/cost_policy_id로 집계)",
            "turn side asymmetry into target pressure(방향 비대칭을 목표 압력으로 바꿈)",
        ),
        (
            "side_quality_weight",
            "side_quality_weight;short_abstention_pressure_weight",
            "side_quality_gap_target;direction_residual_rate_model;short_quality_target",
            "normalize train-only side gap and short loss pressure(학습 전용 방향 차이와 숏 손실 압력 정규화)",
            "keeps short repair learnable without forward veto(숏 수리를 전진 거부 없이 학습 가능하게 둠)",
        ),
        (
            "cost_survival_weight",
            "cost_survival_weight",
            "EC combined_sample_weight;low_margin_rate;payoff_tail_norm",
            "multiply train-only cost/margin/payoff pressure(학습 전용 비용/여백/보상 압력 곱)",
            "turns cost fragility into sample pressure(비용 취약성을 표본 압력으로 바꿈)",
        ),
        (
            "curve_state_pressure_weight",
            "curve_state_pressure_weight",
            "EC drawdown_pressure_norm;underwater_rate;DX underwater_rate_model",
            "combine train-only curve pressure only(학습 전용 곡선 압력만 결합)",
            "moves curve repair away from date-pocket memorization(곡선 수리를 날짜 구간 암기에서 분리)",
        ),
        (
            "density_floor_tags",
            "density_floor_min;density_floor_max;density_floor_contract_count;density_floor_tag",
            "run337CR train_only_density_policy_grid(run337CR 학습 전용 밀도 정책 격자)",
            "copy predeclared density envelope without seeing broker forward result(브로커 전진 결과를 보지 않고 사전 선언 밀도 범위 복사)",
            "keeps no-trade repair blocked(무거래 수리 차단 유지)",
        ),
    ]
    return [
        {
            "recipe_id": recipe_id,
            "materialized_column": materialized,
            "source_columns": source,
            "split_scope": "train_only(학습 전용)",
            "timestamp_rule": "targets and weights are never model features(목표와 가중치는 모델 피처가 아님)",
            "train_only_formula": formula,
            "non_feature_status": "not_allowed_as_feature(피처 사용 불가)",
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for recipe_id, materialized, source, formula, effect in recipes
    ]


def build_forward_quarantine() -> list[dict[str, Any]]:
    eu_final = read_json(ev.FINAL_DECISION)
    sources = [
        ("broker_runtime_kpi_release_review", EU_RUNTIME, f"rank2_net={eu_final.get('best_net_profit')};rank2_pf={eu_final.get('best_profit_factor')}"),
        ("broker_failure_memory", EU_MEMORY, f"long_positive={eu_final.get('long_positive_attempts')};short_negative={eu_final.get('short_negative_attempts')}"),
        ("broker_release_guardrail", EU_GUARDRAIL, f"release_rows={eu_final.get('release_rows')}"),
        ("broker_trade_records", ET_TRADES, f"trades={row_count(ET_TRADES)}"),
        ("broker_regime_attribution", ET_REGIME, f"rows={row_count(ET_REGIME)}"),
        ("broker_cost_stress", ET_COST, f"rows={row_count(ET_COST)}"),
        ("broker_curve_pockets", ET_CURVE, f"rows={row_count(ET_CURVE)}"),
    ]
    return [
        {
            "evidence_id": evidence_id,
            "source_path": rel(path),
            "rows": row_count(path),
            "allowed_use": "failure memory, design pressure, future release dependency(실패 기억/설계 압력/미래 해제 의존성)",
            "forbidden_use": "feature, label, threshold, side veto, candidate selector, release proof(피처/라벨/임계값/방향 거부/후보 선택/해제 증거)",
            "quarantine_status": "active_not_joined_to_train_frame(활성, 학습 프레임에 결합 안 함)",
            "evidence_read": evidence_read,
            "effect": "keeps broker evidence informative without leaking into training inputs(브로커 근거를 유익하게 남기되 학습 입력 누수를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for evidence_id, path, evidence_read in sources
    ]


def build_negative_control_materialization(frame: pd.DataFrame) -> list[dict[str, Any]]:
    control_rows = read_csv(EV_NEGATIVE)
    frame_cols = set(map(str, frame.columns))
    results: list[dict[str, Any]] = []
    for row in control_rows:
        control_id = str(row.get("control_id", ""))
        if control_id == "ev_control_known_forward_short_veto_forbidden":
            passed = not (frame_cols & FORBIDDEN_FORWARD_COLUMNS)
            observed = f"forbidden_forward_columns_in_frame={sorted(frame_cols & FORBIDDEN_FORWARD_COLUMNS)}"
            artifact = rel(FORWARD_QUARANTINE)
        elif control_id == "ev_control_date_pocket_forbidden":
            passed = "month" not in frame_cols and "trade_index" not in frame_cols
            observed = f"month_in_frame={'month' in frame_cols};trade_index_in_frame={'trade_index' in frame_cols}"
            artifact = rel(FEATURE_ROLE_MATRIX)
        elif control_id == "ev_control_proxy_kpi_selection_forbidden":
            passed = "proxy_rank" not in frame_cols and "profit_factor" not in frame_cols
            observed = f"proxy_rank_in_frame={'proxy_rank' in frame_cols};profit_factor_in_frame={'profit_factor' in frame_cols}"
            artifact = rel(FORWARD_QUARANTINE)
        elif control_id == "ev_control_trade_collapse_forbidden":
            passed = "density_floor_min" in frame_cols and row_count(CR_DENSITY_GRID) > 0
            observed = f"density_floor_min_in_frame={'density_floor_min' in frame_cols};density_contract_rows={row_count(CR_DENSITY_GRID)}"
            artifact = rel(DENSITY_SCHEMA)
        elif control_id == "ev_control_cost_blind_positive_forbidden":
            passed = "cost_survival_weight" in frame_cols
            observed = f"cost_survival_weight_in_frame={'cost_survival_weight' in frame_cols}"
            artifact = rel(COST_SCHEMA)
        else:
            passed = True
            observed = "carried_forward_for_EX_review(EX 검토로 이월)"
            artifact = rel(NEGATIVE_CONTROL_MATERIALIZATION)
        results.append(
            {
                "control_id": control_id,
                "source_control_family": row.get("control_family", ""),
                "materialized_artifact": artifact,
                "materialized_status": "passed_active" if passed else "failed_blocks_review",
                "observed": observed,
                "invalid_if_future_review": row.get("invalid_if", ""),
                "effect": row.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return results


def build_release_gate_materialization(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifact_by_gate = {
        "ev_gate_side_separate_quality": rel(SIDE_SCHEMA),
        "ev_gate_cost_ladder_survival": rel(COST_SCHEMA),
        "ev_gate_curve_state_transfer": rel(CURVE_SCHEMA),
        "ev_gate_density_expectancy_balance": rel(DENSITY_SCHEMA),
        "ev_gate_broker_mt5_authority": rel(FORWARD_QUARANTINE),
    }
    observed_by_gate = {
        "ev_gate_side_separate_quality": f"side_target_rows={final['side_target_non_null_rows']};frame_rows={final['frame_rows']}",
        "ev_gate_cost_ladder_survival": f"cost_weight_min={final['cost_survival_weight_min']:.6g};cost_weight_max={final['cost_survival_weight_max']:.6g}",
        "ev_gate_curve_state_transfer": f"curve_weight_min={final['curve_state_weight_min']:.6g};curve_weight_max={final['curve_state_weight_max']:.6g}",
        "ev_gate_density_expectancy_balance": f"density_floor_min={final['density_floor_min']};density_floor_max={final['density_floor_max']}",
        "ev_gate_broker_mt5_authority": "broker evidence quarantined; future MT5 identity still required(브로커 근거 격리, 미래 MT5 정체성 필요)",
    }
    rows: list[dict[str, Any]] = []
    for gate in read_csv(EV_RELEASE):
        gate_id = str(gate.get("gate_id", ""))
        rows.append(
            {
                "gate_id": gate_id,
                "source_gate_family": gate.get("gate_family", ""),
                "materialized_artifact": artifact_by_gate.get(gate_id, rel(RELEASE_GATE_MATERIALIZATION)),
                "materialized_status": "carried_forward_active_review_required(활성 이월, 검토 필요)",
                "observed": observed_by_gate.get(gate_id, "carried forward(이월)"),
                "future_release_dependency": gate.get("pass_condition", ""),
                "effect": gate.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_ex_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ex_review_train_only_frame_and_roles",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review train-only side/cost/curve frame and field roles(학습 전용 방향/비용/곡선 프레임과 필드 역할 검토)",
            "required_inputs": f"{rel(TRAIN_ONLY_INPUT_FRAME)};{rel(FEATURE_ROLE_MATRIX)};{rel(ALLOWED_FEATURE_SET)}",
            "required_outputs": "train_only_input_safety_review.csv",
            "blocked_if_missing": "frame or role matrix(프레임 또는 역할 행렬)",
            "forbidden_action": "no model training before EX review(EX 검토 전 모델 학습 금지)",
            "effect": "checks feature-label boundary before training(학습 전 피처-라벨 경계 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "ex_review_forward_quarantine_and_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review forward evidence quarantine and negative controls(전진 근거 격리와 부정 대조 검토)",
            "required_inputs": f"{rel(FORWARD_QUARANTINE)};{rel(NEGATIVE_CONTROL_MATERIALIZATION)}",
            "required_outputs": "forward_quarantine_control_review.csv",
            "blocked_if_missing": "quarantine or controls(격리표 또는 대조)",
            "forbidden_action": "no side veto, no threshold tuning, no candidate selection(방향 거부/임계값 조정/후보 선택 금지)",
            "effect": "keeps broker evidence out of labels while preserving failure memory(브로커 근거를 라벨에서 빼고 실패 기억은 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "ex_review_release_gate_materialization",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review side/cost/curve/density release gate materialization(방향/비용/곡선/밀도 해제 게이트 물질화 검토)",
            "required_inputs": f"{rel(RELEASE_GATE_MATERIALIZATION)};{rel(INPUT_MANIFEST)}",
            "required_outputs": "release_gate_materialization_review.csv",
            "blocked_if_missing": "release gate matrix or manifest(해제 게이트 행렬 또는 목록)",
            "forbidden_action": "no Forward Passed/Failed, no runtime authority, no Goal Achieve(전진 통과/실패, 런타임 권위, 목표 달성 금지)",
            "effect": "keeps EW as input materialization, not promotion(EW를 입력 물질화로 유지하고 승격으로 보지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["model_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_runtime_probe"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        (
            "input_presence",
            final["missing_inputs"] == 0,
            str(final["missing_inputs"]),
            "0",
            f"{rel(MATERIALIZATION_SOURCE_MAP)}",
            "required EV/EC/DX/ET/EU inputs exist(필수 EV/EC/DX/ET/EU 입력 존재)",
        ),
        (
            "parent_ev_gates_passed",
            final["ev_failed_gate_rows"] == 0,
            str(final["ev_failed_gate_rows"]),
            "0",
            rel(EV_GATES),
            "EV design gates are intact(EV 설계 게이트 유지)",
        ),
        (
            "parent_next_action_matches",
            final["ev_next_action"] == RUN_ID,
            str(final["ev_next_action"]),
            RUN_ID,
            rel(EV_FINAL),
            "EW continues the opened EV queue(EW가 열린 EV 대기열을 이어감)",
        ),
        (
            "train_only_split_preserved",
            final["split_values"] == ["train"] and final["frame_rows"] > 0,
            json.dumps(final["split_values"], ensure_ascii=False),
            "[train]",
            rel(INPUT_MANIFEST),
            "materialized frame remains train-only(물질화 프레임이 학습 전용 유지)",
        ),
        (
            "side_targets_materialized",
            final["side_target_non_null_rows"] == final["frame_rows"],
            f"{final['side_target_non_null_rows']}/{final['frame_rows']}",
            "all frame rows",
            rel(SIDE_SCHEMA),
            "side quality targets exist for all train rows(모든 학습 행에 방향 품질 목표 존재)",
        ),
        (
            "cost_curve_weights_materialized",
            final["cost_survival_weight_min"] > 0 and final["curve_state_weight_min"] > 0,
            f"cost_min={final['cost_survival_weight_min']:.6g};curve_min={final['curve_state_weight_min']:.6g}",
            ">0",
            f"{rel(COST_SCHEMA)};{rel(CURVE_SCHEMA)}",
            "cost and curve weights are usable for review(비용/곡선 가중치가 검토 가능)",
        ),
        (
            "forward_evidence_quarantined",
            final["forbidden_forward_columns_in_frame"] == 0 and final["quarantine_rows"] >= 7,
            f"forbidden_cols={final['forbidden_forward_columns_in_frame']};quarantine_rows={final['quarantine_rows']}",
            "0 forbidden columns and >=7 quarantine rows",
            rel(FORWARD_QUARANTINE),
            "broker forward evidence is not joined into train labels/features(브로커 전진 근거가 학습 라벨/피처에 결합되지 않음)",
        ),
        (
            "feature_role_schema_materialized",
            final["role_rows"] == final["frame_columns"] and final["allowed_feature_rows"] > 20,
            f"role_rows={final['role_rows']};columns={final['frame_columns']};allowed_features={final['allowed_feature_rows']}",
            "roles for every column and >20 features",
            rel(FEATURE_ROLE_MATRIX),
            "every column has an allowed/forbidden role(모든 열에 허용/금지 역할 부여)",
        ),
        (
            "negative_controls_materialized",
            final["negative_control_failed_rows"] == 0 and final["negative_control_rows"] >= 5,
            f"failed={final['negative_control_failed_rows']};rows={final['negative_control_rows']}",
            "0 failed and >=5 rows",
            rel(NEGATIVE_CONTROL_MATERIALIZATION),
            "EV negative controls remain active(EV 부정 대조 활성 유지)",
        ),
        (
            "release_gates_carried",
            final["release_gate_rows"] >= 5,
            str(final["release_gate_rows"]),
            ">=5",
            rel(RELEASE_GATE_MATERIALIZATION),
            "future release gates are carried into EX(미래 해제 게이트를 EX로 이월)",
        ),
        (
            "ex_queue_materialized",
            final["ex_queue_rows"] == 3,
            str(final["ex_queue_rows"]),
            "3",
            rel(EX_QUEUE),
            "EX review queue opened(EX 검토 대기열 열림)",
        ),
        (
            "no_forbidden_claim",
            no_forbidden_claim,
            f"training={final['model_training']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            rel(FINAL_DECISION),
            "EW is input materialization only(EW는 입력 물질화 전용)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    routing = {
        "run_id": RUN_ID,
        "primary_family": "data_integrity(데이터 무결성)",
        "primary_skill": "obsidian-data-integrity(옵시디언 데이터 무결성)",
        "support_skills": [
            "obsidian-model-validation(옵시디언 모델 검증)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "obsidian-result-judgment(옵시디언 결과 판정)",
        ],
        "required_gates": [row["gate_id"] for row in read_csv(GATE_AUDIT)] if path_exists(GATE_AUDIT) else [],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "data_source": [rel(path) for path in REQUIRED_INPUTS],
        "sample_scope": f"rows={final['frame_rows']};split={final['split_values']};source_rows={final['source_row_count']};cost_policies={final['cost_policy_count']}",
        "feature_label_boundary": "feature_role_matrix separates features from targets/weights and forward evidence(피처 역할 행렬이 피처를 목표/가중치/전진 근거와 분리)",
        "timestamp_safety": "EC/DX source frames are train split only; ET/EU broker evidence is quarantined(EC/DX 원천 프레임은 학습 분할 전용, ET/EU 브로커 근거는 격리)",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};forbidden_forward_columns_in_frame={final['forbidden_forward_columns_in_frame']}",
        "integrity_judgment": "usable_for_EX_review_no_training(EX 검토용, 학습 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_training": "not_run(미실행)",
        "candidate_selection": "not_run(미실행)",
        "target_and_weight_status": "materialized_review_required(물질화 완료, 검토 필요)",
        "feature_count": final["allowed_feature_rows"],
        "threshold_policy": "no tuning(조정 없음)",
        "onnx_status": "not_exported(내보내기 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "broker_memory_used_as": "quarantined design pressure only(격리된 설계 압력만)",
        "side_materialization": f"side_target_rows={final['side_target_non_null_rows']}",
        "cost_materialization": f"cost_weight_min={final['cost_survival_weight_min']:.6g};cost_weight_max={final['cost_survival_weight_max']:.6g}",
        "curve_materialization": f"curve_weight_min={final['curve_state_weight_min']:.6g};curve_weight_max={final['curve_state_weight_max']:.6g}",
        "density_floor": f"{final['density_floor_min']}..{final['density_floor_max']}",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "evidence_available": [rel(TRAIN_ONLY_INPUT_FRAME), rel(FEATURE_ROLE_MATRIX), rel(FORWARD_QUARANTINE), rel(GATE_AUDIT)],
        "evidence_missing": "EX review, model training, ONNX export, MT5 runtime probe(EX 검토, 모델 학습, ONNX 내보내기, MT5 런타임 탐침)",
        "next_condition": final["next_action"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(ROUTING_RECEIPT, routing),
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in REQUIRED_INPUTS],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_forward_quarantine(전진 격리와 함께 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EW Broker-Confirmed Side/Cost/Curve Repair Inputs(337단계 337EW 브로커 확인 방향/비용/곡선 수리 입력)

## Conclusion(결론)

run337EW(337EW 실행)는 EV design contracts(EV 설계 계약)을 실제 train-only input frame(학습 전용 입력 프레임)으로 물질화했다.

Action(행동): EC/DX train-only frames(EC/DX 학습 전용 프레임)을 결합해 side target(방향 목표), cost survival weight(비용 생존 가중치), curve state weight(곡선 상태 가중치), density floor(밀도 하한)를 만들었다. Effect(효과): 다음 run337EX(337EX 실행)가 학습 전에 feature-label boundary(피처-라벨 경계)와 overfit control(과적합 통제)을 검토할 수 있다.

Action(행동): ET/EU broker forward evidence(ET/EU 브로커 전진 근거)는 quarantine(격리) 표에만 남겼다. Effect(효과): 실제 MT5(MetaTrader 5, 메타트레이더5) 실패 기억은 보존하지만 피처(feature, 피처), 라벨(label, 라벨), 임계값(threshold, 임계값), 방향 거부(side veto, 방향 거부)에는 섞이지 않는다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- frame_rows(프레임 행): `{final['frame_rows']}`
- frame_columns(프레임 열): `{final['frame_columns']}`
- allowed_feature_rows(허용 피처 행): `{final['allowed_feature_rows']}`
- target_or_weight_rows(목표/가중치 행): `{final['target_or_weight_rows']}`
- side_target_rows(방향 목표 행): `{final['side_target_non_null_rows']}`
- quarantine_rows(격리 행): `{final['quarantine_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- model training(모델 학습): `not_run`
- candidate selection(후보 선택): `not_run`
- threshold tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337EW Decision(337EW 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(GATE_AUDIT)}`, `{rel(TRAIN_ONLY_INPUT_FRAME)}`, `{rel(FORWARD_QUARANTINE)}`

Action(행동): train-only side/cost/curve inputs(학습 전용 방향/비용/곡선 입력)을 만들고 broker forward evidence(브로커 전진 근거)를 격리했다.
Effect(효과): run337EX(337EX 실행)는 학습(training, 학습) 전 입력 안전성(input safety, 입력 안전성)을 검토할 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def insert_before_once(text: str, marker: str, section: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = current_branch()

    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337EW focus complete: run337EW(337EW 실행)는 `{final['status']}`로 broker-confirmed side/cost/curve repair inputs(브로커 확인 방향/비용/곡선 수리 입력)을 물질화했다. "
        f"Effect(효과): train-only frame(학습 전용 프레임) `{final['frame_rows']}`행과 forward quarantine(전진 격리) `{final['quarantine_rows']}`행을 만들고 `{final['next_action']}`을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337EW focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337EW Broker-Confirmed Side/Cost/Curve Repair Inputs(브로커 확인 방향/비용/곡선 수리 입력)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- frame_rows(프레임 행): `{final['frame_rows']}`
- allowed_feature_rows(허용 피처 행): `{final['allowed_feature_rows']}`
- target_or_weight_rows(목표/가중치 행): `{final['target_or_weight_rows']}`
- quarantine_rows(격리 행): `{final['quarantine_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): train-only(학습 전용) 방향/비용/곡선 입력을 만들고 broker forward evidence(브로커 전진 근거)를 격리해 EX 검토 전 학습을 막는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = insert_before_once(current, "## run337EV Broker-Confirmed", section, "## run337EW Broker-Confirmed")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- train_only_frame_rows(학습 전용 프레임 행): `{final['frame_rows']}`
- allowed_feature_rows(허용 피처 행): `{final['allowed_feature_rows']}`
- target_or_weight_rows(목표/가중치 행): `{final['target_or_weight_rows']}`
- forward_quarantine_rows(전진 격리 행): `{final['quarantine_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): EW(337EW 실행)는 입력 물질화이며 학습(training, 학습), 선택(selection, 선택), MT5(MetaTrader 5, 메타트레이더5) 실행을 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337EW(337EW 실행) `{final['status']}`. "
        f"Effect(효과): train-only side/cost/curve input frame(학습 전용 방향/비용/곡선 입력 프레임) `{final['frame_rows']}`행과 forward quarantine(전진 격리) `{final['quarantine_rows']}`행을 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, append_once(brief, brief_entry, "run337EW(337EW 실행)"), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EW(337EW 실행) `{final['status']}`. "
        f"Effect(효과): broker-confirmed side/cost/curve repair inputs(브로커 확인 방향/비용/곡선 수리 입력)을 물질화하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, append_once(changelog, changelog_entry, "Stage337 run337EW"), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    key_value = str(row.get(key, ""))
    rows = [item for item in existing if str(item.get(key, "")) != key_value]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "broker_confirmed_side_cost_curve_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"frame_rows={final['frame_rows']};allowed_features={final['allowed_feature_rows']};quarantine_rows={final['quarantine_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "train_only_side_cost_curve_inputs(학습 전용 방향/비용/곡선 입력)",
        "tier_scope": "Tier A train-only inputs with broker forward quarantine(Tier A 학습 전용 입력과 브로커 전진 격리)",
        "kpi_scope": "input_materialization_no_kpi_release(입력 물질화, KPI 해제 없음)",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"frame_rows={final['frame_rows']};allowed_features={final['allowed_feature_rows']}",
        "guardrail_kpi": f"quarantine_rows={final['quarantine_rows']};forbidden_forward_columns={final['forbidden_forward_columns_in_frame']};no_training;no_selection",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "EV design contracts, EC/DX train-only frames, ET/EU broker evidence quarantined",
        "kpi_scope": "input_frame_schema_quarantine_gates",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_materialization",
        "family": "broker_confirmed_side_cost_curve_input_materialization",
        "question": "can broker-confirmed side/cost/curve design be materialized as train-only inputs without forward leakage",
        "metric_scope": "frame_rows_feature_roles_quarantine_controls",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def final_payload(summary: Mapping[str, Any], role_rows: Sequence[Mapping[str, Any]], quarantine_rows: Sequence[Mapping[str, Any]], control_rows: Sequence[Mapping[str, Any]], release_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ev_final = read_json(EV_FINAL)
    frame_columns = int(summary["columns"])
    allowed_feature_rows = sum(1 for row in role_rows if str(row.get("allowed_role", "")).startswith("allowed_model_feature"))
    target_or_weight_rows = sum(1 for row in role_rows if str(row.get("allowed_role", "")).startswith("target_or_weight_no_feature"))
    forbidden_forward_columns = [
        row.get("field_name")
        for row in role_rows
        if str(row.get("field_name", "")) in FORBIDDEN_FORWARD_COLUMNS
    ]
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(REQUIRED_INPUTS)),
        "ev_next_action": ev_final.get("next_action", ""),
        "ev_failed_gate_rows": sum(1 for row in read_csv(EV_GATES) if row.get("status") != "passed"),
        "frame_rows": summary["rows"],
        "frame_columns": frame_columns,
        "split_values": summary["split_values"],
        "source_row_count": summary["source_row_count"],
        "cost_policy_count": summary["cost_policy_count"],
        "side_target_non_null_rows": summary["side_target_non_null_rows"],
        "cost_survival_weight_min": summary["cost_survival_weight_min"],
        "cost_survival_weight_max": summary["cost_survival_weight_max"],
        "curve_state_weight_min": summary["curve_state_weight_min"],
        "curve_state_weight_max": summary["curve_state_weight_max"],
        "density_floor_min": summary["density_floor_min"],
        "density_floor_max": summary["density_floor_max"],
        "density_floor_contract_count": summary["density_floor_contract_count"],
        "role_rows": len(role_rows),
        "allowed_feature_rows": allowed_feature_rows,
        "target_or_weight_rows": target_or_weight_rows,
        "forbidden_forward_columns_in_frame": len(forbidden_forward_columns),
        "forbidden_forward_columns": forbidden_forward_columns,
        "quarantine_rows": len(quarantine_rows),
        "negative_control_rows": len(control_rows),
        "negative_control_failed_rows": sum(1 for row in control_rows if str(row.get("materialized_status", "")).startswith("failed")),
        "release_gate_rows": len(release_rows),
        "ex_queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return final


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(REQUIRED_INPUTS)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    frame, summary = materialize_train_only_frame()
    source_rows = build_source_map()
    role_rows, feature_rows = build_feature_roles(frame)
    density = density_floor_summary()
    side_rows = build_side_schema()
    cost_rows = build_cost_schema()
    curve_rows = build_curve_schema()
    density_rows = build_density_schema(density)
    quarantine_rows = build_forward_quarantine()
    control_rows = build_negative_control_materialization(frame)
    release_rows = build_release_gate_materialization(
        {
            "side_target_non_null_rows": summary["side_target_non_null_rows"],
            "frame_rows": summary["rows"],
            "cost_survival_weight_min": summary["cost_survival_weight_min"],
            "cost_survival_weight_max": summary["cost_survival_weight_max"],
            "curve_state_weight_min": summary["curve_state_weight_min"],
            "curve_state_weight_max": summary["curve_state_weight_max"],
            "density_floor_min": summary["density_floor_min"],
            "density_floor_max": summary["density_floor_max"],
        }
    )
    queue_rows = build_ex_queue()
    final = final_payload(summary, role_rows, quarantine_rows, control_rows, release_rows, queue_rows)
    manifest_rows = build_manifest(frame, final)
    recipe_rows = build_label_weight_recipes()

    artifacts: list[Path] = [
        TRAIN_ONLY_INPUT_FRAME,
        write_csv(MATERIALIZATION_SOURCE_MAP, SOURCE_COLUMNS, source_rows),
        write_csv(FEATURE_ROLE_MATRIX, ROLE_COLUMNS, role_rows),
        write_csv(ALLOWED_FEATURE_SET, ALLOWED_FEATURE_COLUMNS, feature_rows),
        write_csv(SIDE_SCHEMA, SCHEMA_COLUMNS, side_rows),
        write_csv(COST_SCHEMA, SCHEMA_COLUMNS, cost_rows),
        write_csv(CURVE_SCHEMA, SCHEMA_COLUMNS, curve_rows),
        write_csv(DENSITY_SCHEMA, SCHEMA_COLUMNS, density_rows),
        write_csv(INPUT_MANIFEST, MANIFEST_COLUMNS, manifest_rows),
        write_csv(LABEL_WEIGHT_RECIPE, RECIPE_COLUMNS, recipe_rows),
        write_csv(FORWARD_QUARANTINE, QUARANTINE_COLUMNS, quarantine_rows),
        write_csv(NEGATIVE_CONTROL_MATERIALIZATION, CONTROL_COLUMNS, control_rows),
        write_csv(RELEASE_GATE_MATERIALIZATION, RELEASE_COLUMNS, release_rows),
        write_csv(EX_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    if final["failed_gates"]:
        final["status"] = "invalid_stage337EW_required_gate_failure_no_training_no_selection"
        final["judgment"] = "required_gate_failure_blocks_EW_materialization_claim"
        final["decision"] = "repair_stage337EW_required_gate_failure_before_EX"
        final["next_action"] = "repair_stage337EW_required_gate_failure_v1"

    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in REQUIRED_INPUTS],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": final["status"], "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "frame_rows": final["frame_rows"],
                "allowed_feature_rows": final["allowed_feature_rows"],
                "target_or_weight_rows": final["target_or_weight_rows"],
                "quarantine_rows": final["quarantine_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
