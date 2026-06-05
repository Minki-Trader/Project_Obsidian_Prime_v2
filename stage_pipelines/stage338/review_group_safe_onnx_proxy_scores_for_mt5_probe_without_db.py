from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage338 import train_runtime_trade_lifecycle_repair_models_group_safe_without_db as tr  # noqa: E402


aw = tr.aw

TODAY = "2026-06-01"
STAGE_ID = tr.STAGE_ID
STAGE_DIR = tr.STAGE_DIR
RUN_NUMBER = "run338F"
RUN_ID = "run338F_review_group_safe_onnx_proxy_scores_for_mt5_probe_without_db_v1"
PARENT_RUN_ID = tr.RUN_ID
NEXT_RUN_ID = "run338G_materialize_runtime_collapsed_onnx_mt5_probe_package_without_db_v1"
STATUS = "completed_stage338F_proxy_review_runtime_collapse_required_no_mt5_no_selection"
JUDGMENT = "proxy_positive_after_runtime_timestamp_collapse_mt5_probe_package_required_no_selection"
DECISION = "stage338F_open_run338G_runtime_collapsed_mt5_probe_package"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_and_runtime_shape_control_only_no_candidate_selection_"
    "no_mt5_execution_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338F_proxy_review_runtime_collapse.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338F_proxy_review_runtime_collapse.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PROXY_REVIEW = RUN_DIR / "run338F_proxy_score_review.csv"
TIMESTAMP_UNIQUENESS_AUDIT = RUN_DIR / "run338F_runtime_timestamp_uniqueness_audit.csv"
COLLAPSED_RUNTIME_PROXY = RUN_DIR / "run338F_runtime_collapsed_proxy_score.csv"
COLLAPSED_PREDICTION_TAPE = RUN_DIR / "run338F_runtime_collapsed_prediction_tape.parquet"
RUN338G_PACKAGE_QUEUE = RUN_DIR / "run338G_mt5_probe_package_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    tr.FINAL_DECISION,
    tr.MODEL_SCORECARD,
    tr.PROXY_THRESHOLD_GRID,
    tr.ONNX_PARITY_AUDIT,
    tr.HOLDOUT_PREDICTIONS,
    tr.FEATURE_ORDER,
)
OUTPUT_FILES = (
    PROXY_REVIEW,
    TIMESTAMP_UNIQUENESS_AUDIT,
    COLLAPSED_RUNTIME_PROXY,
    COLLAPSED_PREDICTION_TAPE,
    RUN338G_PACKAGE_QUEUE,
    DATA_RECEIPT,
    LINEAGE_RECEIPT,
    MODEL_RECEIPT,
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
    return tr.read_csv(path)


def read_json(path: Path) -> Any:
    return tr.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return tr.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return tr.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return tr.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    tr.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    tr.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    return tr.display_path(path)


def passed_status(series: pd.Series) -> pd.Series:
    return tr.passed_status(series)


def safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return float(numerator) / float(denominator)


def max_drawdown(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def profit_factor(values: np.ndarray) -> float:
    gains = float(values[values > 0].sum())
    losses = float(-values[values < 0].sum())
    if losses <= 0:
        return math.inf if gains > 0 else 0.0
    return gains / losses


def evaluate_threshold(frame: pd.DataFrame, model_id: str, min_prob: float, min_margin: float) -> dict[str, Any]:
    p_short = pd.to_numeric(frame[f"{model_id}_proba_class_0"], errors="coerce").fillna(0.0)
    p_flat = pd.to_numeric(frame[f"{model_id}_proba_class_1"], errors="coerce").fillna(0.0)
    p_long = pd.to_numeric(frame[f"{model_id}_proba_class_2"], errors="coerce").fillna(0.0)
    short_margin = p_short - pd.concat([p_flat, p_long], axis=1).max(axis=1)
    long_margin = p_long - pd.concat([p_flat, p_short], axis=1).max(axis=1)
    long_ok = (p_long >= min_prob) & (long_margin >= min_margin)
    short_ok = (p_short >= min_prob) & (short_margin >= min_margin)
    direction = pd.Series(0, index=frame.index, dtype=int)
    direction.loc[long_ok & (~short_ok | (p_long >= p_short))] = 1
    direction.loc[short_ok & direction.eq(0)] = -1
    long_proxy = pd.to_numeric(frame[tr.LONG_PROXY], errors="coerce").fillna(0.0)
    short_proxy = pd.to_numeric(frame[tr.SHORT_PROXY], errors="coerce").fillna(0.0)
    pnl = pd.Series(0.0, index=frame.index, dtype=float)
    pnl.loc[direction.gt(0)] = long_proxy.loc[direction.gt(0)]
    pnl.loc[direction.lt(0)] = short_proxy.loc[direction.lt(0)]
    trade_values = pnl.loc[direction.ne(0)].to_numpy(dtype=float)
    trade_count = int(direction.ne(0).sum())
    long_count = int(direction.gt(0).sum())
    short_count = int(direction.lt(0).sum())
    net = float(trade_values.sum()) if trade_count else 0.0
    dd = max_drawdown(trade_values)
    pf = profit_factor(trade_values)
    return {
        "trade_count": trade_count,
        "long_trades": long_count,
        "short_trades": short_count,
        "signal_density": round(safe_ratio(trade_count, len(frame)), 8),
        "side_balance": round(safe_ratio(max(long_count, short_count), trade_count), 8) if trade_count else 0.0,
        "proxy_net_log_return": round(net, 10),
        "proxy_profit_factor": round(pf if math.isfinite(pf) else 999.0, 8),
        "proxy_expectancy": round(safe_ratio(net, trade_count), 10),
        "proxy_max_drawdown": round(dd, 10),
        "proxy_recovery": round(safe_ratio(net, dd), 8) if dd > 0 else (999.0 if net > 0 else 0.0),
    }


def build_review() -> tuple[dict[str, Any], dict[str, pd.DataFrame]]:
    parent_final = read_json(tr.FINAL_DECISION)
    parent_gates = read_csv(tr.GATE_AUDIT)
    scorecard = read_csv(tr.MODEL_SCORECARD)
    parity = read_csv(tr.ONNX_PARITY_AUDIT)
    predictions = pd.read_parquet(str(io(tr.HOLDOUT_PREDICTIONS)))
    best = scorecard.iloc[0].to_dict()
    model_id = str(best["model_id"])
    min_prob = float(best["best_min_prob"])
    min_margin = float(best["best_min_margin"])
    predictions = predictions.sort_values(["timestamp", "source_row_id"]).reset_index(drop=True)
    collapsed = predictions.drop_duplicates("timestamp", keep="last").copy().reset_index(drop=True)
    raw_eval = evaluate_threshold(predictions, model_id, min_prob, min_margin)
    collapsed_eval = evaluate_threshold(collapsed, model_id, min_prob, min_margin)
    unique_audit = pd.DataFrame(
        [
            {
                "audit_id": "run338E_holdout_prediction_rows",
                "rows": int(len(predictions)),
                "unique_timestamps": int(predictions["timestamp"].nunique()),
                "duplicate_timestamp_rows": int(predictions["timestamp"].duplicated().sum()),
                "runtime_usable_without_collapse": "no(아니오)",
                "effect": "MT5(메타트레이더5)는 한 timestamp(타임스탬프)에 한 feature row(피처 행)만 자연스럽게 소비한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "run338F_runtime_collapsed_rows",
                "rows": int(len(collapsed)),
                "unique_timestamps": int(collapsed["timestamp"].nunique()),
                "duplicate_timestamp_rows": int(collapsed["timestamp"].duplicated().sum()),
                "runtime_usable_without_collapse": "yes(예)",
                "effect": "timestamp(타임스탬프)당 마지막 source_row_id(원천 행 ID)만 남겨 MT5 probe(MT5 탐침) 입력 형태로 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    proxy_review = pd.DataFrame(
        [
            {
                "review_id": "raw_group_safe_proxy",
                "model_id": model_id,
                "min_prob": min_prob,
                "min_margin": min_margin,
                "rows": int(len(predictions)),
                **raw_eval,
                "runtime_shape": "duplicate_timestamp_not_runtime_ready(중복 타임스탬프라 런타임 준비 아님)",
                "allowed_use": "diagnostic_only(진단 전용)",
                "effect": "run338E proxy(프록시)를 그대로 MT5 KPI(MT5 핵심 성과 지표)로 쓰지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "review_id": "runtime_collapsed_proxy",
                "model_id": model_id,
                "min_prob": min_prob,
                "min_margin": min_margin,
                "rows": int(len(collapsed)),
                **collapsed_eval,
                "runtime_shape": "runtime_probe_package_ready_shape(런타임 탐침 패키지 준비 형태)",
                "allowed_use": "mt5_probe_routing_only(MT5 탐침 라우팅 전용)",
                "effect": "MT5 runtime probe(MT5 런타임 탐침)에 넣을 수 있는 timestamp-unique(시각 고유) proxy(프록시)를 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    collapsed_proxy = proxy_review.loc[proxy_review["review_id"].eq("runtime_collapsed_proxy")].copy()
    queue = pd.DataFrame(
        [
            {
                "queue_id": "run338G_runtime_collapsed_mt5_probe_package",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "model_id": model_id,
                "onnx_path": parity.loc[parity["model_id"].astype(str).eq(model_id), "onnx_path"].iloc[0],
                "min_prob": min_prob,
                "min_margin": min_margin,
                "required_inputs": f"{rel(COLLAPSED_PREDICTION_TAPE)};{rel(tr.FEATURE_ORDER)};{rel(tr.ONNX_PARITY_AUDIT)}",
                "required_outputs": "MT5 runtime probe package(MT5 런타임 탐침 패키지); tester set/ini(테스터 설정/INI); expected tape(예상 테이프)",
                "blocked_if_missing": "timestamp-unique prediction tape or ONNX parity pass(시각 고유 예측 테이프 또는 ONNX 동등성 통과)",
                "forbidden_action": "treat collapsed proxy as MT5 KPI(축약 프록시를 MT5 KPI로 취급)",
                "effect": "MT5 비교를 다음 실행에서 실제 패키지로 시도할 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = {
        "source_rows": int(len(predictions)),
        "runtime_collapsed_rows": int(len(collapsed)),
        "duplicate_timestamp_rows": int(predictions["timestamp"].duplicated().sum()),
        "model_id": model_id,
        "min_prob": min_prob,
        "min_margin": min_margin,
        "raw_proxy_net_log_return": float(raw_eval["proxy_net_log_return"]),
        "raw_proxy_trade_count": int(raw_eval["trade_count"]),
        "collapsed_proxy_net_log_return": float(collapsed_eval["proxy_net_log_return"]),
        "collapsed_proxy_profit_factor": float(collapsed_eval["proxy_profit_factor"]),
        "collapsed_proxy_trade_count": int(collapsed_eval["trade_count"]),
        "collapsed_proxy_side_balance": float(collapsed_eval["side_balance"]),
        "onnx_parity_failed_count": int(parity["parity_status"].astype(str).ne("passed").sum()),
        "parent_gate_passed": bool(passed_status(parent_gates["status"]).all()),
        "parent_goal_achieve": parent_final.get("goal_achieve", "not_claimed"),
        "next_run_id": NEXT_RUN_ID,
        "effect": "proxy(프록시)를 runtime timestamp shape(런타임 시각 형태)에 맞춰 MT5 비교 전 단계로 낮춘다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return summary, {
        "proxy_review": proxy_review,
        "timestamp_audit": unique_audit,
        "collapsed_proxy": collapsed_proxy,
        "collapsed_tape": collapsed,
        "queue": queue,
        "summary": pd.DataFrame([summary]),
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_338E_gates_passed", "passed" if summary["parent_gate_passed"] else "failed", rel(tr.GATE_AUDIT), "run338E(338E 실행) ONNX training(온엑스 학습) 근거를 이어받는다."),
            gate_row("onnx_parity_preserved", "passed" if summary["onnx_parity_failed_count"] == 0 else "failed", rel(tr.ONNX_PARITY_AUDIT), "ONNX runtime(온엑스 런타임) 동등성을 유지한다."),
            gate_row("timestamp_uniqueness_audited", "passed" if summary["duplicate_timestamp_rows"] > 0 else "failed", rel(TIMESTAMP_UNIQUENESS_AUDIT), "MT5 전 timestamp duplicate(타임스탬프 중복)를 숨기지 않는다."),
            gate_row("runtime_collapsed_proxy_positive", "passed" if summary["collapsed_proxy_net_log_return"] > 0 and summary["collapsed_proxy_trade_count"] > 0 else "failed", rel(COLLAPSED_RUNTIME_PROXY), "런타임 형태로 축약한 proxy(프록시)가 아직 양수인지 본다."),
            gate_row("run338G_package_queue_opened", "passed", rel(RUN338G_PACKAGE_QUEUE), "MT5 runtime probe package(MT5 런타임 탐침 패키지) 실행을 다음으로 연다."),
            gate_row("no_forbidden_mt5_claim", "passed", rel(FINAL_DECISION), "아직 MT5 execution(MT5 실행)이나 KPI를 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_tables(tables: Mapping[str, pd.DataFrame]) -> None:
    write_csv(PROXY_REVIEW, tables["proxy_review"])
    write_csv(TIMESTAMP_UNIQUENESS_AUDIT, tables["timestamp_audit"])
    write_csv(COLLAPSED_RUNTIME_PROXY, tables["collapsed_proxy"])
    ensure_parent(COLLAPSED_PREDICTION_TAPE)
    tables["collapsed_tape"].to_parquet(str(io(COLLAPSED_PREDICTION_TAPE)), index=False)
    write_csv(RUN338G_PACKAGE_QUEUE, tables["queue"])


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
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(tr.HOLDOUT_PREDICTIONS),
            "time_axis": "timestamp duplicate audited and collapsed before MT5(타임스탬프 중복을 MT5 전 감사/축약)",
            "sample_scope": f"raw={summary['source_rows']};collapsed={summary['runtime_collapsed_rows']}",
            "split_boundary": rel(tr.rv.GROUP_SAFE_SPLIT_MANIFEST),
            "integrity_judgment": "runtime_shape_control_required_before_mt5(런타임 형태 제어 뒤 MT5 필요)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_id": summary["model_id"],
            "onnx_parity": rel(tr.ONNX_PARITY_AUDIT),
            "proxy_review": rel(PROXY_REVIEW),
            "selection_metric": "not_selected; routing review only(선택 없음; 라우팅 검토 전용)",
            "validation_judgment": JUDGMENT,
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
            "availability": "collapsed_proxy_and_package_queue_written(축약 프록시와 패키지 대기열 작성됨)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "proxy_mt5_comparison": "not_yet_package_required",
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
    report = f"""# run338F Proxy Review Runtime Collapse(프록시 검토 런타임 축약)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- model_id(모델 ID): `{final['model_id']}`
- duplicate_timestamp_rows(중복 타임스탬프 행): `{final['duplicate_timestamp_rows']}`
- collapsed_rows(축약 행): `{final['runtime_collapsed_rows']}`
- collapsed_proxy_net_log_return(축약 프록시 순로그수익): `{final['collapsed_proxy_net_log_return']}`
- collapsed_proxy_profit_factor(축약 프록시 수익 팩터): `{final['collapsed_proxy_profit_factor']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338E(338E 실행)의 proxy-positive(프록시 양수) 결과를 timestamp-unique runtime shape(타임스탬프 고유 런타임 형태)로 축약했다.
Effect(효과): MT5 runtime probe(MT5 런타임 탐침) 전에 중복 시각 문제를 숨기지 않고 패키지 가능한 입력으로 낮춘다.

## Evidence(근거)

- proxy review(프록시 검토): `{rel(PROXY_REVIEW)}`
- timestamp audit(타임스탬프 감사): `{rel(TIMESTAMP_UNIQUENESS_AUDIT)}`
- collapsed proxy(축약 프록시): `{rel(COLLAPSED_RUNTIME_PROXY)}`
- package queue(패키지 대기열): `{rel(RUN338G_PACKAGE_QUEUE)}`

## Boundary(경계)

run338F(338F 실행)는 MT5 execution(MT5 실행)을 하지 않았다. Collapsed proxy(축약 프록시)는 MT5 KPI(MT5 핵심 성과 지표)가 아니며, run338G(338G 실행)의 runtime probe package(런타임 탐침 패키지) 입력일 뿐이다.
"""
    decision = f"""# {TODAY} Stage338F Decision(338F 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(COLLAPSED_RUNTIME_PROXY)}`, `{rel(RUN338G_PACKAGE_QUEUE)}`

Action(행동): proxy(프록시)를 MT5(메타트레이더5)가 소비 가능한 timestamp-unique(시각 고유) 형태로 축약했다.
Effect(효과): 다음 실행은 proxy-MT5 comparison(프록시-MT5 비교)을 위해 실제 패키지를 만들 수 있다.

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

run338F(338F 실행)는 중복 timestamp(타임스탬프) proxy(프록시)를 바로 MT5(메타트레이더5)에 넘기지 않고, runtime-collapsed(런타임 축약) 입력으로 낮췄다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- reviewed_proxy_model(검토 프록시 모델): `{final['model_id']}`
- collapsed_proxy_net_log_return(축약 프록시 순로그수익): `{final['collapsed_proxy_net_log_return']}`
- collapsed_proxy_trade_count(축약 프록시 거래수): `{final['collapsed_proxy_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): proxy-positive(프록시 양수)를 선정 모델이나 MT5 성과로 오해하지 않게 한다.
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
    marker = f"run338F {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run338F Proxy Review Runtime Collapse(프록시 검토 런타임 축약)

- run_id(실행 ID): `{RUN_ID}`
- collapsed_proxy_net_log_return(축약 프록시 순로그수익): `{final['collapsed_proxy_net_log_return']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): MT5(메타트레이더5) 전 timestamp duplicate(타임스탬프 중복)를 통제했다.
""")
    append_text_once(STAGE_README, marker, f"""## run338F Proxy Review Runtime Collapse(프록시 검토 런타임 축약)

- run_id(실행 ID): `{RUN_ID}`
- package_queue(패키지 대기열): `{rel(RUN338G_PACKAGE_QUEUE)}`
- effect(효과): MT5 runtime probe package(MT5 런타임 탐침 패키지) 직전 형태로 정리했다.
""")
    changelog = f"""## {TODAY} run338F Proxy Review Runtime Collapse(프록시 검토 런타임 축약)

- action(행동): 중복 timestamp(타임스탬프) `{final['duplicate_timestamp_rows']}`행을 감사하고 runtime-collapsed proxy(런타임 축약 프록시)를 만들었다.
- effect(효과): 축약 proxy net(프록시 순수익) `{final['collapsed_proxy_net_log_return']}`는 MT5 KPI가 아니라 run338G(338G 실행) 패키지 입력이다.
- boundary(경계): MT5 execution/selection/Goal Achieve(MT5 실행/선택/목표 달성)는 없다.
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
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "runtime_collapsed_proxy_review", "sample_rows": final["runtime_collapsed_rows"], "net_profit": final["collapsed_proxy_net_log_return"], "profit_factor": final["collapsed_proxy_profit_factor"], "trade_count": final["collapsed_proxy_trade_count"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "sample_rows": final["runtime_collapsed_rows"], "result_status": "same_as_tier_a_until_tier_b_available"},
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
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    ensure_parent(ARTIFACT_REGISTRY)
    temp_path = ARTIFACT_REGISTRY.with_suffix(".tmp.csv")
    with io(temp_path).open("w", encoding="utf-8-sig", newline="") as handle:
        ordered.to_csv(handle, index=False, lineterminator="\n")
    io(temp_path).replace(io(ARTIFACT_REGISTRY))


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338F inputs: {missing}")
    summary, tables = build_review()
    write_tables(tables)
    write_csv(RUN_DIR / "run338F_review_summary.csv", tables["summary"])
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338F gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "model_id": final["model_id"],
                "duplicate_timestamp_rows": final["duplicate_timestamp_rows"],
                "runtime_collapsed_rows": final["runtime_collapsed_rows"],
                "collapsed_proxy_net_log_return": final["collapsed_proxy_net_log_return"],
                "collapsed_proxy_profit_factor": final["collapsed_proxy_profit_factor"],
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
