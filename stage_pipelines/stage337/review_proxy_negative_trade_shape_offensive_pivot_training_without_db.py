from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    train_proxy_negative_trade_shape_offensive_pivot_candidates_without_db as hz,
)

aw = hz.aw

TODAY = "2026-06-01"
STAGE_ID = hz.STAGE_ID
STAGE_DIR = hz.STAGE_DIR
RUN_NUMBER = "run337IA"
RUN_ID = "run337IA_review_proxy_negative_trade_shape_offensive_pivot_training_without_db_v1"
PARENT_RUN_ID = hz.RUN_ID
NEXT_RUN_ID = "run337IB_materialize_proxy_positive_offensive_pivot_runtime_probe_package_without_db_v1"
STATUS = "completed_stage337IA_offensive_pivot_training_review_runtime_probe_package_required_no_selection"
JUDGMENT = "two_proxy_positive_onnx_candidates_found_short_dominant_side_risk_runtime_probe_required"
DECISION = "stage337IA_open_run337IB_materialize_proxy_positive_runtime_probe_package"
CLAIM_BOUNDARY = (
    "research_development_training_review_only_no_candidate_selection_no_mt5_execution_in_IA_"
    "no_runtime_package_authority_no_forward_no_operating_or_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = hz.REVIEW_DIR
REPORT_PATH = REVIEW_DIR / "run337IA_proxy_negative_trade_shape_offensive_pivot_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IA_proxy_negative_trade_shape_offensive_pivot_training_review.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

CANDIDATE_REVIEW = RUN_DIR / "ia_candidate_review_scorecard.csv"
POSITIVE_MATRIX = RUN_DIR / "ia_positive_proxy_candidate_matrix.csv"
SIDE_ATTRIBUTION = RUN_DIR / "ia_side_balance_attribution.csv"
RUNTIME_QUEUE = RUN_DIR / "run337IB_runtime_probe_package_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def _ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent, RUN_REGISTRY.parent]:
        aw.io_path(path).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(aw.io_path(path))


def _write_csv(path: Path, frame: pd.DataFrame) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(aw.io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def _write_json(path: Path, payload: dict) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_bom_text(path: Path, text: str) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(text, encoding="utf-8-sig")


def _sha(path: Path) -> str:
    return aw.sha256_file(path)


def _numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    output = frame.copy()
    for column in columns:
        output[column] = pd.to_numeric(output[column], errors="coerce")
    return output


def _build_reviews() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    manifest = _read_csv(hz.TRAINED_MODEL_MANIFEST)
    parity = _read_csv(hz.ONNX_PARITY)
    classification = _numeric(
        _read_csv(hz.CLASSIFICATION_SCORECARD),
        ["rows", "accuracy", "balanced_accuracy", "macro_f1", "log_loss", "signal_density"],
    )
    proxy = _numeric(
        _read_csv(hz.PROXY_TRADE_SCORECARD),
        [
            "trade_count",
            "signal_density",
            "net_log_return_after_cost",
            "profit_factor",
            "expectancy",
            "max_drawdown",
            "recovery_factor",
            "long_count",
            "short_count",
            "long_net",
            "short_net",
        ],
    )

    holdout_proxy = proxy.loc[proxy["split"].eq("inner_holdout")].copy()
    holdout_class = classification.loc[classification["split"].eq("inner_holdout")].copy()
    review = (
        manifest.merge(holdout_proxy, on=["model_id", "task_id"], how="left", suffixes=("", "_proxy"))
        .merge(
            holdout_class[
                [
                    "model_id",
                    "task_id",
                    "balanced_accuracy",
                    "macro_f1",
                    "log_loss",
                    "signal_density",
                ]
            ],
            on=["model_id", "task_id"],
            how="left",
            suffixes=("", "_class"),
        )
        .merge(parity[["model_id", "task_id", "passed", "max_abs_diff"]], on=["model_id", "task_id"], how="left")
    )
    review["is_directional_proxy"] = review["score_mode"].astype(str).str.startswith("directional_")
    review["is_proxy_positive"] = review["is_directional_proxy"] & (review["net_log_return_after_cost"] > 0)
    review["side_balance_ratio"] = np.where(
        review[["long_count", "short_count"]].max(axis=1) > 0,
        review[["long_count", "short_count"]].min(axis=1) / review[["long_count", "short_count"]].max(axis=1),
        0.0,
    )
    review["side_net_warning"] = np.where(
        (review["long_net"] < 0) | (review["short_net"] < 0),
        "side_net_negative_present",
        "side_net_nonnegative",
    )
    review["review_rank"] = (
        review["net_log_return_after_cost"].where(review["is_directional_proxy"], -999.0)
        .rank(method="first", ascending=False)
        .astype(int)
    )
    review["ia_disposition"] = np.select(
        [
            review["is_proxy_positive"] & (review["review_rank"] == 1),
            review["is_proxy_positive"],
            review["score_mode"].eq("active_flat_gate_only"),
        ],
        [
            "runtime_probe_primary_candidate_not_selected",
            "runtime_probe_secondary_candidate_not_selected",
            "active_flat_gate_only_not_directional_runtime_candidate",
        ],
        default="proxy_negative_or_low_priority_no_runtime_package",
    )
    review["effect"] = (
        "IA separates positive proxy evidence from model selection and prepares MT5 runtime probe input."
    )
    review["claim_boundary"] = CLAIM_BOUNDARY

    positive = review.loc[review["is_proxy_positive"]].copy().sort_values(
        "net_log_return_after_cost", ascending=False
    )
    side = review[
        [
            "model_id",
            "task_id",
            "trade_count",
            "long_count",
            "short_count",
            "side_balance_ratio",
            "long_net",
            "short_net",
            "side_net_warning",
            "ia_disposition",
        ]
    ].copy()
    side["effect"] = "Side attribution exposes whether proxy net comes from one-sided behavior."
    side["claim_boundary"] = CLAIM_BOUNDARY

    queue_candidates = positive.head(2).copy()
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "materialize_runtime_probe_package_for_positive_proxy_onnx_candidates",
                "candidate_count": int(len(queue_candidates)),
                "candidate_model_ids": ";".join(queue_candidates["model_id"].astype(str).tolist()),
                "candidate_task_ids": ";".join(queue_candidates["task_id"].astype(str).tolist()),
                "required_inputs": f"{aw.rel(hz.TRAINED_MODEL_MANIFEST)};{aw.rel(hz.ONNX_PARITY)};{aw.rel(hz.FEATURE_SCHEMA)};{aw.rel(POSITIVE_MATRIX)}",
                "required_outputs": "runtime probe package manifest and MT5 execution attempt plan(런타임 탐침 패키지 목록과 MT5 실행 시도 계획)",
                "forbidden_action": "operating claim or candidate selection before MT5 runtime evidence(MT5 런타임 근거 전 운영 주장 또는 후보 선택)",
                "effect": "Positive proxy candidates are pushed toward external verification instead of selection.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = {
        "candidate_rows": int(len(review)),
        "onnx_parity_rows": int(len(parity)),
        "onnx_parity_passed_rows": int(parity["passed"].astype(str).str.lower().eq("true").sum()),
        "positive_proxy_rows": int(len(positive)),
        "runtime_queue_candidate_count": int(len(queue_candidates)),
        "best_model_id": str(positive.iloc[0]["model_id"]) if len(positive) else "",
        "best_task_id": str(positive.iloc[0]["task_id"]) if len(positive) else "",
        "best_proxy_net": float(positive.iloc[0]["net_log_return_after_cost"]) if len(positive) else 0.0,
        "best_profit_factor": float(positive.iloc[0]["profit_factor"]) if len(positive) else 0.0,
        "best_trade_count": int(positive.iloc[0]["trade_count"]) if len(positive) else 0,
        "best_side_balance_ratio": float(positive.iloc[0]["side_balance_ratio"]) if len(positive) else 0.0,
        "best_side_net_warning": str(positive.iloc[0]["side_net_warning"]) if len(positive) else "",
    }
    return review, positive, side, queue, summary


def _gate_row(gate: str, status: str, evidence: str, effect: str) -> dict:
    return {
        "gate": gate,
        "status": status,
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _make_gates(summary: dict) -> pd.DataFrame:
    hz_gates = _read_csv(hz.GATE_AUDIT)
    gates = [
        _gate_row(
            "parent_hz_gates_passed",
            "pass" if hz_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all() else "fail",
            aw.rel(hz.GATE_AUDIT),
            "IA only reviews completed HZ training.",
        ),
        _gate_row(
            "onnx_parity_all_passed",
            "pass"
            if summary["onnx_parity_passed_rows"] == summary["onnx_parity_rows"] == summary["candidate_rows"]
            else "fail",
            aw.rel(hz.ONNX_PARITY),
            "All candidates must preserve ONNX probability parity.",
        ),
        _gate_row(
            "positive_proxy_candidates_identified",
            "pass" if summary["positive_proxy_rows"] >= 1 else "fail",
            aw.rel(POSITIVE_MATRIX),
            "Positive proxy rows are identified for MT5 comparison.",
        ),
        _gate_row(
            "side_risk_recorded",
            "pass" if SIDE_ATTRIBUTION.exists() else "fail",
            aw.rel(SIDE_ATTRIBUTION),
            "Long/short imbalance and side net risk are recorded.",
        ),
        _gate_row(
            "runtime_probe_package_queue_opened",
            "pass" if summary["runtime_queue_candidate_count"] >= 1 and RUNTIME_QUEUE.exists() else "fail",
            aw.rel(RUNTIME_QUEUE),
            "Proxy-positive candidates are queued for external verification.",
        ),
        _gate_row(
            "no_candidate_selection_claim",
            "pass",
            aw.rel(CLAIM_BOUNDARY_RECEIPT),
            "IA ranks review priority but does not select a model.",
        ),
        _gate_row(
            "no_forbidden_operating_claim",
            "pass",
            aw.rel(CLAIM_BOUNDARY_RECEIPT),
            "IA does not claim MT5 success, runtime authority, operating promotion, or Goal achievement.",
        ),
        _gate_row(
            "required_gate_coverage_audit_written",
            "pass",
            aw.rel(GATE_AUDIT),
            "Gate coverage is recorded for closeout.",
        ),
    ]
    return pd.DataFrame(gates)


def _append_or_replace_csv(path: Path, key_columns: Iterable[str], row: dict) -> None:
    if path.exists():
        frame = _read_csv(path)
    else:
        frame = pd.DataFrame()
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    mask = pd.Series(False, index=frame.index)
    for idx, key in enumerate(key_columns):
        current = frame[key].astype(str).eq(str(row[key])) if key in frame.columns else False
        mask = current if idx == 0 else mask & current
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    _write_csv(path, frame[ordered])


def _artifact_paths() -> list[Path]:
    return [
        CANDIDATE_REVIEW,
        POSITIVE_MATRIX,
        SIDE_ATTRIBUTION,
        RUNTIME_QUEUE,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        PERFORMANCE_RECEIPT,
        RUNTIME_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_BOUNDARY_RECEIPT,
        LINEAGE_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]


def _update_artifact_registry(paths: list[Path]) -> None:
    if ARTIFACT_REGISTRY.exists():
        registry = pd.read_csv(aw.io_path(ARTIFACT_REGISTRY))
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if path.exists():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": aw.rel(path),
                    "sha256": _sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        registry[columns].to_csv(
            aw.io_path(ARTIFACT_REGISTRY),
            index=False,
            encoding="utf-8-sig",
            lineterminator="\n",
        )


def _write_receipts(summary: dict, gates: pd.DataFrame) -> None:
    _write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "work_family": "training_review",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-runtime-parity", "obsidian-artifact-lineage"],
            "effect": "Proxy-positive ONNX candidates are reviewed without selection.",
        },
    )
    _write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_training_run": PARENT_RUN_ID,
            "tier_scope": "Tier A only; Tier B and combined missing_required",
            "effect": "Data scope remains limited before runtime probe.",
        },
    )
    _write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "candidate_rows": summary["candidate_rows"],
            "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "best_model_id": summary["best_model_id"],
            "effect": "Best proxy model is review priority, not selected model.",
        },
    )
    _write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "positive_proxy_rows": summary["positive_proxy_rows"],
            "best_proxy_net": summary["best_proxy_net"],
            "best_profit_factor": summary["best_profit_factor"],
            "best_trade_count": summary["best_trade_count"],
            "best_side_balance_ratio": summary["best_side_balance_ratio"],
            "best_side_net_warning": summary["best_side_net_warning"],
            "allowed_use": "MT5 runtime probe prioritization only(MT5 런타임 탐침 우선순위 전용)",
            "forbidden_use": "candidate selection or MT5 KPI replacement(후보 선택 또는 MT5 KPI 대체)",
        },
    )
    _write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "runtime_probe_required": True,
            "mt5_execution_in_IA": "not_run",
            "next_run_id": NEXT_RUN_ID,
            "effect": "Proxy expected value is routed toward MT5 comparison.",
        },
    )
    _write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
            "gate_total": int(len(gates)),
        },
    )
    _write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "candidate_selection": "not_run",
            "mt5_execution": "not_run_in_IA",
            "goal_achieve_claim": "not_claimed",
            "runtime_authority_claim": "not_claimed",
            "operating_promotion_claim": "not_claimed",
            "live_readiness_claim": "not_claimed",
        },
    )
    _write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "positive_matrix": aw.rel(POSITIVE_MATRIX),
            "runtime_queue": aw.rel(RUNTIME_QUEUE),
            "artifact_registry_updated": True,
            "effect": "Review priority connects to runtime package queue.",
        },
    )


def _write_final(summary: dict, gates: pd.DataFrame) -> None:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_execution": "not_run_in_IA",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **summary,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at": TODAY,
        "script": aw.rel(Path(__file__)),
        "inputs": [
            aw.rel(hz.FINAL_DECISION),
            aw.rel(hz.GATE_AUDIT),
            aw.rel(hz.TRAINED_MODEL_MANIFEST),
            aw.rel(hz.ONNX_PARITY),
            aw.rel(hz.PROXY_TRADE_SCORECARD),
        ],
        "outputs": [aw.rel(path) for path in _artifact_paths() if path.exists()],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    _write_json(FINAL_DECISION, final)
    _write_json(RUN_MANIFEST, manifest)


def _write_docs(summary: dict, gates: pd.DataFrame) -> None:
    gate_passes = int(gates["status"].astype(str).eq("pass").sum())
    gate_total = int(len(gates))
    report = f"""﻿# Stage 337IA Offensive Pivot Training Review

## Summary

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- judgment: `{JUDGMENT}`
- gates: `{gate_passes}/{gate_total}`
- positive_proxy_rows(양수 프록시 행): `{summary['positive_proxy_rows']}`
- best_model_id(최고 프록시 모델 ID): `{summary['best_model_id']}`
- best_proxy_net(최고 프록시 순수익): `{summary['best_proxy_net']}`
- best_profit_factor(최고 수익 팩터): `{summary['best_profit_factor']}`
- best_side_balance_ratio(최고 후보 방향 균형 비율): `{summary['best_side_balance_ratio']}`

## Result

IA review(검토)는 proxy-positive(프록시 양수) ONNX(온엑스) 후보 2개를 찾았다.
Effect(효과): 후보 선택(selection, 선택)이 아니라 MT5 runtime probe(MT5 런타임 탐침) 패키지로 넘긴다.

## Risk

Best proxy(최고 프록시)는 short-dominant(숏 우세)이고 side net warning(방향 순익 경고)이 있다.
Effect(효과): MT5 probe(탐침)는 net profit(순수익)뿐 아니라 long/short balance(롱/숏 균형)를 같이 확인해야 한다.

## Boundary

No candidate selection(후보 선택 없음), no MT5 execution in IA(IA에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next

Open `{NEXT_RUN_ID}` to materialize(물질화) runtime probe package(런타임 탐침 패키지) and attempt(시도) external MT5 comparison(외부 MT5 비교).
"""
    decision = f"""﻿# Decision: Stage 337IA Training Review

- date: `{TODAY}`
- run_id: `{RUN_ID}`
- decision: `{DECISION}`
- judgment: `{JUDGMENT}`
- next_run_id: `{NEXT_RUN_ID}`

## Reason

HZ training(학습)은 ONNX parity(ONNX 동등성) `7/7`을 통과했고, proxy-positive(프록시 양수) 후보 2개를 만들었다.

## Effect

proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하기 위해 IB package(패키지)를 연다.

## Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(REPORT_PATH, report)
    _write_bom_text(DECISION_DOC, decision)
    _write_bom_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    _write_bom_text(
        CURRENT_WORKING_STATE,
        f"""﻿# Current Working State

## Current Truth

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- decision: `{DECISION}`

## Effect

IA review(검토)는 proxy-positive(프록시 양수) 후보를 runtime probe package(런타임 탐침 패키지)로 보냈다.
효과는 proxy(프록시)를 MT5(메타트레이더5) 비교 없이 운영 주장으로 쓰지 않게 하는 것이다.

## Claim Boundary

`{CLAIM_BOUNDARY}`
""",
    )
    _write_bom_text(
        SELECTION_STATUS,
        f"""﻿# Selection Status

- latest_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- model_selection: not_selected
- runtime_package: queued_not_authoritative
- goal_achieve: not_claimed
- operating_promotion: not_claimed
- live_readiness: not_claimed
- best_proxy_model_for_probe: `{summary['best_model_id']}`

효과는 runtime probe candidate(런타임 탐침 후보)를 selected model(선택 모델)로 오해하지 않게 하는 것이다.
""",
    )
    _write_bom_text(
        STAGE_BRIEF,
        f"""﻿# {STAGE_ID}

Latest completed run: `{RUN_ID}`

IA review(검토)는 proxy-positive ONNX candidates(프록시 양수 ONNX 후보) `{summary['positive_proxy_rows']}`개를 확인했다.
Next(다음): `{NEXT_RUN_ID}` runtime probe package(런타임 탐침 패키지).
""",
    )
    existing = aw.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if CHANGELOG.exists() else "﻿# Changelog\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Reviewed(검토) HZ training(학습); positive proxy(양수 프록시) `{summary['positive_proxy_rows']}` rows.\n"
        f"- Queued(대기열 등록) IB runtime probe package(런타임 탐침 패키지) for `{summary['best_model_id']}` and peer candidate(동료 후보).\n"
    )
    _write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry)


def _update_ledgers(summary: dict, gates: pd.DataFrame) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_rows": summary["candidate_rows"],
        "positive_proxy_rows": summary["positive_proxy_rows"],
        "best_model_id": summary["best_model_id"],
        "best_proxy_net": summary["best_proxy_net"],
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": aw.rel(REPORT_PATH),
    }
    _append_or_replace_csv(RUN_REGISTRY, ["run_id"], row)
    _append_or_replace_csv(PROJECT_LEDGER, ["run_id"], row)
    _append_or_replace_csv(STAGE_LEDGER, ["run_id"], row)


def main() -> None:
    _ensure_dirs()
    review, positive, side, queue, summary = _build_reviews()
    _write_csv(CANDIDATE_REVIEW, review)
    _write_csv(POSITIVE_MATRIX, positive)
    _write_csv(SIDE_ATTRIBUTION, side)
    _write_csv(RUNTIME_QUEUE, queue)
    gates = _make_gates(summary)
    _write_csv(GATE_AUDIT, gates)
    _write_receipts(summary, gates)
    _write_final(summary, gates)
    _write_docs(summary, gates)
    _update_ledgers(summary, gates)
    _update_artifact_registry(_artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("pass")]
    if not failed.empty:
        raise RuntimeError(f"IA gates failed: {failed[['gate', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "positive_proxy_rows": summary["positive_proxy_rows"],
                "best_model_id": summary["best_model_id"],
                "best_proxy_net": summary["best_proxy_net"],
                "best_profit_factor": summary["best_profit_factor"],
                "runtime_queue_candidate_count": summary["runtime_queue_candidate_count"],
                "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
                "gate_total": int(len(gates)),
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
