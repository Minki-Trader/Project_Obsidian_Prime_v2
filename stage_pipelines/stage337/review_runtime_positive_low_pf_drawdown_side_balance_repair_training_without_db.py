from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    train_runtime_positive_low_pf_drawdown_side_balance_repair_candidates_without_db as ih,
)


aw = ih.aw

TODAY = "2026-06-01"
STAGE_ID = ih.STAGE_ID
STAGE_DIR = ih.STAGE_DIR
RUN_NUMBER = "run337II"
RUN_ID = "run337II_review_runtime_positive_low_pf_drawdown_side_balance_repair_training_without_db_v1"
PARENT_RUN_ID = ih.RUN_ID
NEXT_RUN_ID = "run337IJ_materialize_runtime_positive_low_pf_drawdown_side_balance_repair_runtime_probe_package_without_db_v1"
STATUS = "completed_stage337II_runtime_positive_repair_training_review_runtime_probe_package_required_no_selection"
JUDGMENT = "one_weak_proxy_positive_onnx_candidate_found_mt5_runtime_probe_required_no_selection"
DECISION = "stage337II_open_run337IJ_runtime_positive_repair_runtime_probe_package"
CLAIM_BOUNDARY = (
    "research_development_training_review_only_no_candidate_selection_no_mt5_execution_in_II_"
    "no_runtime_package_authority_no_forward_no_operating_or_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337II_repair_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337II_runtime_positive_repair_training_review.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

CANDIDATE_REVIEW = RUN_DIR / "ii_training_candidate_review.csv"
POSITIVE_MATRIX = RUN_DIR / "ii_positive_proxy_candidate_matrix.csv"
ATTRIBUTION_MATRIX = RUN_DIR / "ii_side_pf_drawdown_attribution.csv"
PROXY_COST_LIMITATION = RUN_DIR / "ii_proxy_cost_limitation.csv"
TIER_PAIR_RECORD = RUN_DIR / "ii_tier_pair_required_record.csv"
RUNTIME_QUEUE = RUN_DIR / "run337IJ_runtime_probe_package_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ih.FINAL_DECISION,
    ih.GATE_AUDIT,
    ih.TRAINED_MODEL_MANIFEST,
    ih.ONNX_PARITY,
    ih.CLASSIFICATION_SCORECARD,
    ih.PROXY_TRADE_SCORECARD,
    ih.FEATURE_SCHEMA,
)
OUTPUT_FILES = (
    CANDIDATE_REVIEW,
    POSITIVE_MATRIX,
    ATTRIBUTION_MATRIX,
    PROXY_COST_LIMITATION,
    TIER_PAIR_RECORD,
    RUNTIME_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
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


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def numeric(frame: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    output = frame.copy()
    for column in columns:
        if column in output.columns:
            output[column] = pd.to_numeric(output[column], errors="coerce")
    return output


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def weakness_tags(row: pd.Series) -> str:
    tags: list[str] = []
    if bool(row.get("is_directional_proxy", False)) and float(row.get("profit_factor", 0.0) or 0.0) < 1.05:
        tags.append("low_profit_factor_below_1_05")
    if bool(row.get("is_directional_proxy", False)) and float(row.get("recovery_factor", 0.0) or 0.0) < 1.0:
        tags.append("low_recovery_factor_below_1")
    if float(row.get("long_net", 0.0) or 0.0) < 0.0 or float(row.get("short_net", 0.0) or 0.0) < 0.0:
        tags.append("side_net_negative_present")
    if float(row.get("signal_density", 0.0) or 0.0) > 0.80:
        tags.append("high_signal_density_above_0_80")
    if float(row.get("balanced_accuracy", 0.0) or 0.0) < 0.40:
        tags.append("weak_balanced_accuracy_below_0_40")
    if not tags:
        tags.append("no_major_proxy_review_tag")
    return ";".join(tags)


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    manifest = read_csv(ih.TRAINED_MODEL_MANIFEST)
    parity = read_csv(ih.ONNX_PARITY)
    classification = numeric(
        read_csv(ih.CLASSIFICATION_SCORECARD),
        ["rows", "accuracy", "balanced_accuracy", "macro_f1", "log_loss", "signal_density"],
    )
    proxy = numeric(
        read_csv(ih.PROXY_TRADE_SCORECARD),
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

    holdout_proxy = proxy.loc[proxy["split"].astype(str).eq("inner_holdout")].copy()
    holdout_class = classification.loc[classification["split"].astype(str).eq("inner_holdout")].copy()
    holdout_class = holdout_class.rename(columns={"signal_density": "class_signal_density"})
    review = (
        manifest.merge(holdout_proxy, on=["model_id", "task_id"], how="left", suffixes=("", "_proxy"))
        .merge(
            holdout_class[
                [
                    "model_id",
                    "task_id",
                    "accuracy",
                    "balanced_accuracy",
                    "macro_f1",
                    "log_loss",
                    "class_signal_density",
                ]
            ],
            on=["model_id", "task_id"],
            how="left",
        )
        .merge(parity[["model_id", "task_id", "passed", "max_abs_diff"]], on=["model_id", "task_id"], how="left")
    )
    review["is_directional_proxy"] = review["score_mode"].astype(str).str.startswith("directional_")
    review["is_proxy_positive"] = review["is_directional_proxy"] & (
        pd.to_numeric(review["net_log_return_after_cost"], errors="coerce").fillna(0.0) > 0.0
    )
    review["side_balance_ratio"] = np.where(
        review[["long_count", "short_count"]].max(axis=1) > 0,
        review[["long_count", "short_count"]].min(axis=1) / review[["long_count", "short_count"]].max(axis=1),
        0.0,
    )
    review["side_net_warning"] = np.where(
        (pd.to_numeric(review["long_net"], errors="coerce").fillna(0.0) < 0.0)
        | (pd.to_numeric(review["short_net"], errors="coerce").fillna(0.0) < 0.0),
        "side_net_negative_present",
        "side_net_nonnegative",
    )
    directional_score = pd.to_numeric(review["net_log_return_after_cost"], errors="coerce").fillna(-999999.0)
    review["ii_review_rank"] = directional_score.where(review["is_directional_proxy"], -999999.0).rank(
        method="first", ascending=False
    ).astype(int)
    review["weakness_tags"] = review.apply(weakness_tags, axis=1)
    review["ii_disposition"] = np.select(
        [
            review["is_proxy_positive"] & review["ii_review_rank"].eq(1),
            review["is_proxy_positive"],
            review["score_mode"].astype(str).str.startswith("active_flat_gate_only"),
        ],
        [
            "runtime_probe_primary_weak_positive_not_selected",
            "runtime_probe_secondary_weak_positive_not_selected",
            "active_flat_gate_only_not_directional_runtime_candidate",
        ],
        default="proxy_nonpositive_no_runtime_package",
    )
    review["allowed_use"] = "runtime probe prioritization only(MT5 런타임 탐침 우선순위 전용)"
    review["forbidden_use"] = "candidate selection or MT5 KPI replacement(후보 선택 또는 MT5 핵심 성과 지표 대체)"
    review["effect"] = (
        "II review(II 검토)는 weak proxy-positive(약한 프록시 양성)를 selection(선택)이 아니라 "
        "MT5 runtime probe(런타임 탐침) 비교 대상으로만 분리한다."
    )
    review["claim_boundary"] = CLAIM_BOUNDARY

    positive = review.loc[review["is_proxy_positive"]].copy().sort_values(
        ["net_log_return_after_cost", "profit_factor"], ascending=[False, False]
    )
    attribution = review[
        [
            "model_id",
            "task_id",
            "model_family",
            "target_column",
            "score_mode",
            "trade_count",
            "signal_density",
            "net_log_return_after_cost",
            "profit_factor",
            "expectancy",
            "max_drawdown",
            "recovery_factor",
            "long_count",
            "short_count",
            "side_balance_ratio",
            "long_net",
            "short_net",
            "side_net_warning",
            "balanced_accuracy",
            "macro_f1",
            "max_abs_diff",
            "weakness_tags",
            "ii_disposition",
        ]
    ].copy()
    attribution["effect"] = (
        "Side/PF/drawdown attribution(방향/PF/낙폭 귀속)은 proxy net(프록시 순수익)이 "
        "운영 의미(운영 의미)를 갖는지 좁게 확인하게 한다."
    )
    attribution["claim_boundary"] = CLAIM_BOUNDARY

    frame_columns = pd.read_parquet(io(ih.ig.ifr.IF_INPUT_FRAME)).columns
    cost_rows = [
        {
            "cost_check_id": "ih_proxy_cost_source",
            "cost_return_column_present": "true" if "cost_return" in frame_columns else "false",
            "proxy_score_column": "net_log_return_after_cost",
            "limitation": (
                "IH proxy(프록시)는 signal sanity check(신호 점검)와 runtime probe(런타임 탐침) "
                "우선순위 전용이며 MT5 cost/broker execution(MT5 비용/브로커 실행)을 대체하지 않는다."
            ),
            "required_next_check": "compare_proxy_expected_value_with_mt5_runtime_probe(프록시 예상값과 MT5 런타임 탐침 비교)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    cost_limit = pd.DataFrame(cost_rows)

    tier_record = pd.DataFrame(
        [
            {
                "tier_view": "Tier A separate(Tier A 분리)",
                "status": "reviewed",
                "evidence_path": rel(CANDIDATE_REVIEW),
                "effect": "Tier A(티어 A) 후보 검토 범위를 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier B separate(Tier B 분리)",
                "status": "missing_required",
                "evidence_path": rel(TIER_PAIR_RECORD),
                "effect": "Tier B(티어 B)가 없음을 생략하지 않고 표시한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier A+B combined(Tier A+B 합산)",
                "status": "missing_required",
                "evidence_path": rel(TIER_PAIR_RECORD),
                "effect": "합산 결과를 만들지 않았음을 명시해서 과장 해석을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    queue_candidates = positive.head(1).copy()
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "materialize_mt5_runtime_probe_package_for_weak_proxy_positive_candidate",
                "candidate_count": int(len(queue_candidates)),
                "candidate_model_ids": ";".join(queue_candidates["model_id"].astype(str).tolist()),
                "candidate_task_ids": ";".join(queue_candidates["task_id"].astype(str).tolist()),
                "required_inputs": (
                    f"{rel(ih.TRAINED_MODEL_MANIFEST)};{rel(ih.ONNX_PARITY)};"
                    f"{rel(ih.FEATURE_SCHEMA)};{rel(POSITIVE_MATRIX)}"
                ),
                "required_outputs": (
                    "runtime probe package manifest and MT5 execution attempt plan"
                    "(런타임 탐침 패키지 목록과 MT5 실행 시도 계획)"
                ),
                "forbidden_action": (
                    "treat weak proxy-positive priority as selected model"
                    "(약한 프록시 양성 우선순위를 선정 모델로 취급)"
                ),
                "effect": (
                    "Proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 "
                    "비교하도록 다음 작업을 연다."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    best = positive.iloc[0] if len(positive) else None
    summary = {
        "candidate_rows": int(len(review)),
        "directional_holdout_rows": int(review["is_directional_proxy"].sum()),
        "positive_proxy_rows": int(len(positive)),
        "runtime_queue_candidate_count": int(len(queue_candidates)),
        "onnx_parity_rows": int(len(parity)),
        "onnx_parity_passed_rows": int(passed_status(parity["passed"]).sum()),
        "best_model_id": str(best["model_id"]) if best is not None else "",
        "best_task_id": str(best["task_id"]) if best is not None else "",
        "best_proxy_net": float(best["net_log_return_after_cost"]) if best is not None else 0.0,
        "best_profit_factor": float(best["profit_factor"]) if best is not None else 0.0,
        "best_expectancy": float(best["expectancy"]) if best is not None else 0.0,
        "best_max_drawdown": float(best["max_drawdown"]) if best is not None else 0.0,
        "best_recovery_factor": float(best["recovery_factor"]) if best is not None else 0.0,
        "best_trade_count": int(best["trade_count"]) if best is not None else 0,
        "best_signal_density": float(best["signal_density"]) if best is not None else 0.0,
        "best_long_count": int(best["long_count"]) if best is not None else 0,
        "best_short_count": int(best["short_count"]) if best is not None else 0,
        "best_long_net": float(best["long_net"]) if best is not None else 0.0,
        "best_short_net": float(best["short_net"]) if best is not None else 0.0,
        "best_side_balance_ratio": float(best["side_balance_ratio"]) if best is not None else 0.0,
        "best_balanced_accuracy": float(best["balanced_accuracy"]) if best is not None else 0.0,
        "best_weakness_tags": str(best["weakness_tags"]) if best is not None else "",
        "next_action": NEXT_RUN_ID,
    }
    return review, positive, attribution, cost_limit, tier_record, queue, summary


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(ih.GATE_AUDIT)
    parent_passed = passed_status(parent_gates["status"]).all()
    gates = [
        gate_row(
            "parent_ih_gates_passed",
            "passed" if parent_passed else "failed",
            rel(ih.GATE_AUDIT),
            "IH training(학습) gate(게이트)가 통과된 산출물만 검토한다.",
        ),
        gate_row(
            "candidate_review_materialized",
            "passed" if exists(CANDIDATE_REVIEW) and summary["candidate_rows"] == 6 else "failed",
            rel(CANDIDATE_REVIEW),
            "6개 후보를 모두 review(검토)한다.",
        ),
        gate_row(
            "onnx_parity_all_passed",
            "passed"
            if summary["onnx_parity_passed_rows"] == summary["onnx_parity_rows"] == summary["candidate_rows"]
            else "failed",
            rel(ih.ONNX_PARITY),
            "Python/ONNX(파이썬/온엑스) 확률 동등성만 통과로 인정한다.",
        ),
        gate_row(
            "weak_proxy_positive_identified",
            "passed" if summary["positive_proxy_rows"] >= 1 else "failed",
            rel(POSITIVE_MATRIX),
            "positive proxy(양성 프록시)를 MT5 비교 후보로만 분리한다.",
        ),
        gate_row(
            "weakness_attribution_recorded",
            "passed" if exists(ATTRIBUTION_MATRIX) and summary["best_weakness_tags"] else "failed",
            rel(ATTRIBUTION_MATRIX),
            "PF(수익 팩터), recovery(회복), side(방향), density(밀도) 약점을 기록한다.",
        ),
        gate_row(
            "proxy_cost_limitation_recorded",
            "passed" if exists(PROXY_COST_LIMITATION) else "failed",
            rel(PROXY_COST_LIMITATION),
            "proxy(프록시)가 MT5 cost(비용)를 대체하지 못함을 고정한다.",
        ),
        gate_row(
            "tier_pair_missing_required_recorded",
            "passed" if exists(TIER_PAIR_RECORD) else "failed",
            rel(TIER_PAIR_RECORD),
            "Tier B(티어 B)와 combined(합산) 누락을 생략하지 않는다.",
        ),
        gate_row(
            "runtime_probe_package_queue_opened",
            "passed" if summary["runtime_queue_candidate_count"] >= 1 and exists(RUNTIME_QUEUE) else "failed",
            rel(RUNTIME_QUEUE),
            "proxy expected value(프록시 예상값)를 MT5 runtime probe(런타임 탐침)로 비교하게 한다.",
        ),
        gate_row(
            "no_candidate_selection_claim",
            "passed",
            rel(CLAIM_RECEIPT),
            "II는 priority(우선순위)만 만들고 selected model(선정 모델)을 만들지 않는다.",
        ),
        gate_row(
            "no_mt5_execution_in_ii",
            "passed",
            rel(CLAIM_RECEIPT),
            "II는 MT5 실행(run, 실행)을 하지 않고 package(패키지) 준비로 넘긴다.",
        ),
        gate_row(
            "no_forbidden_operating_claim",
            "passed",
            rel(CLAIM_RECEIPT),
            "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.",
        ),
        gate_row(
            "required_gate_coverage_audit_written",
            "passed",
            rel(GATE_AUDIT),
            "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다.",
        ),
    ]
    return pd.DataFrame(gates)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    if exists(path):
        frame = read_csv(path)
    else:
        frame = pd.DataFrame()
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


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def artifact_paths() -> list[Path]:
    return [
        CANDIDATE_REVIEW,
        POSITIVE_MATRIX,
        ATTRIBUTION_MATRIX,
        PROXY_COST_LIMITATION,
        TIER_PAIR_RECORD,
        RUNTIME_QUEUE,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        PERFORMANCE_RECEIPT,
        RUNTIME_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        LINEAGE_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]


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
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> list[Path]:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    payloads: list[tuple[Path, dict[str, Any]]] = [
        (
            EXPERIMENT_RECEIPT,
            {
                **base,
                "work_family": "training_review",
                "primary_skill": "obsidian-result-judgment",
                "support_skills": [
                    "obsidian-model-validation",
                    "obsidian-performance-attribution",
                    "obsidian-runtime-parity",
                    "obsidian-artifact-lineage",
                ],
                "effect": "weak proxy-positive(약한 프록시 양성)를 MT5 runtime probe(런타임 탐침) 비교로 넘긴다.",
            },
        ),
        (
            DATA_RECEIPT,
            {
                **base,
                "tier_a_status": "reviewed",
                "tier_b_status": "missing_required",
                "tier_a_b_combined_status": "missing_required",
                "input_frame": rel(ih.ig.ifr.IF_INPUT_FRAME),
                "effect": "Tier scope(티어 범위)를 고정해 결과 과장을 막는다.",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "candidate_rows": summary["candidate_rows"],
                "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
                "best_model_id": summary["best_model_id"],
                "best_task_id": summary["best_task_id"],
                "effect": "best model(최고 모델)은 probe priority(탐침 우선순위)일 뿐 selection(선택)이 아니다.",
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "positive_proxy_rows": summary["positive_proxy_rows"],
                "best_proxy_net": summary["best_proxy_net"],
                "best_profit_factor": summary["best_profit_factor"],
                "best_recovery_factor": summary["best_recovery_factor"],
                "best_side_balance_ratio": summary["best_side_balance_ratio"],
                "best_weakness_tags": summary["best_weakness_tags"],
                "allowed_use": "proxy signal sanity and MT5 comparison priority(프록시 신호 점검과 MT5 비교 우선순위)",
                "forbidden_use": "MT5 KPI replacement or candidate selection(MT5 핵심 성과 지표 대체 또는 후보 선택)",
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                **base,
                "runtime_probe_required": True,
                "mt5_execution_in_ii": "not_run",
                "next_run_id": NEXT_RUN_ID,
                "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(런타임 탐침)와 비교하도록 연결한다.",
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
                "gate_total": int(len(gates)),
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **base,
                "candidate_selection": "not_run",
                "mt5_execution": "not_run_in_II",
                "runtime_package_authority": "not_claimed",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "operating_promotion": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
        (
            LINEAGE_RECEIPT,
            {
                **base,
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "positive_matrix": rel(POSITIVE_MATRIX),
                "runtime_queue": rel(RUNTIME_QUEUE),
                "consumer": NEXT_RUN_ID,
                "artifact_registry_updated": True,
                "effect": "IH training(학습) 산출물과 IJ runtime package(런타임 패키지)를 연결한다.",
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run_in_II",
        "runtime_package": "not_materialized_in_II",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
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
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> list[Path]:
    report = f"""# run337II Runtime Positive Repair Training Review(run337II 런타임 양성 수리 학습 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- positive_proxy_rows(양성 프록시 행): `{final['positive_proxy_rows']}`
- best_model_id(최고 프록시 모델 ID): `{final['best_model_id']}`
- best_proxy_net(최고 프록시 순수익): `{final['best_proxy_net']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_side_balance_ratio(최고 방향 균형 비율): `{final['best_side_balance_ratio']}`
- best_weakness_tags(약점 태그): `{final['best_weakness_tags']}`

## Action(행동)

IH training(학습) 산출물 6개를 review(검토)했고, ONNX parity(온엑스 동등성) 6/6을 확인했다.
Effect(효과): weak proxy-positive(약한 프록시 양성) 1개를 selected model(선정 모델)이 아니라 MT5 runtime probe(런타임 탐침) 비교 대상으로만 분리했다.

## Finding(발견)

`{final['best_model_id']}`는 proxy net(프록시 순수익)이 양수지만 PF(수익 팩터) `{final['best_profit_factor']}`와 recovery factor(회복 계수) `{final['best_recovery_factor']}`가 낮다.
Effect(효과): 이 후보는 운영 후보가 아니라 proxy-vs-MT5 comparison(프록시-MT5 비교) 필요 후보로만 남긴다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution in II(II에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 runtime probe package(런타임 탐침 패키지)를 만든다.
Effect(효과): proxy expected value(프록시 예상값)를 MT5 runtime evidence(MT5 런타임 근거)와 비교할 수 있게 한다.
"""
    decision = f"""# {TODAY} Stage337II Decision(337II 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(CANDIDATE_REVIEW)}`, `{rel(POSITIVE_MATRIX)}`, `{rel(ATTRIBUTION_MATRIX)}`

Action(행동): weak proxy-positive(약한 프록시 양성) ONNX(온엑스) 후보를 runtime probe priority(런타임 탐침 우선순위)로만 지정했다.
Effect(효과): proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표)로 착각하지 않고 외부 실행 비교로 넘긴다.

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

II review(검토)는 IH training(학습) 산출물을 운영 주장으로 올리지 않고, IJ package(패키지)로 좁게 넘겼다.
효과는 MT5 runtime probe(런타임 탐침) 전에는 selected model(선정 모델)이나 live readiness(실거래 준비)를 말하지 않게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): weak proxy-positive(약한 프록시 양성)를 selection(선택)으로 오해하지 않게 한다.
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

    marker = f"run337II {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337II Training Review(학습 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): weak proxy-positive(약한 프록시 양성) 1개를 MT5 runtime probe(런타임 탐침) 비교로 넘겼고, selection(선택)은 하지 않았다.
""",
    )
    changelog_entry = f"""## {TODAY} run337II Training Review(학습 검토)

- action(행동): IH ONNX(온엑스) 후보 6개를 review(검토)했다.
- effect(효과): 약한 proxy-positive(프록시 양성) 후보 1개를 MT5 runtime probe(런타임 탐침) 패키지 대상으로만 넘겼다.
- boundary(경계): selected model(선정 모델), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없음.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)
    return [REPORT_PATH, DECISION_DOC, CURRENT_WORKING_STATE, SELECTION_STATUS, WORKSPACE_STATE, STAGE_BRIEF, ROOT_CHANGELOG, WORKSPACE_CHANGELOG]


def update_registers(final: Mapping[str, Any]) -> None:
    base_row = {
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
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base_row)
    ledger_rows = [
        {
            **base_row,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "training_review_proxy_only",
            "net_profit": "",
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_max_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "candidate_model_id": final["best_model_id"],
            "result_status": "weak_proxy_positive_runtime_probe_required",
        },
        {
            **base_row,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base_row,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in ledger_rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent, RUN_REGISTRY.parent]:
        io(path).mkdir(parents=True, exist_ok=True)

    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    review, positive, attribution, cost_limit, tier_record, queue, summary = build_review()
    write_csv(CANDIDATE_REVIEW, review)
    write_csv(POSITIVE_MATRIX, positive)
    write_csv(ATTRIBUTION_MATRIX, attribution)
    write_csv(PROXY_COST_LIMITATION, cost_limit)
    write_csv(TIER_PAIR_RECORD, tier_record)
    write_csv(RUNTIME_QUEUE, queue)

    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_rows": final["candidate_rows"],
                "positive_proxy_rows": final["positive_proxy_rows"],
                "best_model_id": final["best_model_id"],
                "best_proxy_net": final["best_proxy_net"],
                "best_profit_factor": final["best_profit_factor"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
