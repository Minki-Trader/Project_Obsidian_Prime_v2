"""Stage 12 standalone ExtraTrees batch-20 structural scout.

This script intentionally uses Stage 12 inputs only. It does not import
Stage 10/11 models, thresholds, promoted criteria, or runtime baselines.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    ledger_pairs,
    upsert_csv_rows,
)

STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
STAGE_DIR = PROJECT_ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run03D"
RUN_ID = "run03D_et_standalone_batch20_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesStandaloneBatch20"
DATASET_ID = "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "model_inputs" / DATASET_ID / "model_input_dataset.parquet"
FEATURE_ORDER_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / DATASET_ID
    / "model_input_feature_order.txt"
)
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
SPEC_PATH = STAGE_DIR / "00_spec" / f"{RUN_NUMBER}_standalone_batch20_plan.md"
REPORT_PATH = RUN_DIR / "reports" / "result_summary.md"
REVIEW_PATH = STAGE_DIR / "03_reviews" / f"{RUN_NUMBER}_standalone_batch20_packet.md"
STAGE_LEDGER_PATH = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = PROJECT_ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY_PATH = PROJECT_ROOT / "docs" / "registers" / "run_registry.csv"
IDEA_REGISTRY_PATH = PROJECT_ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_STATE_PATH = PROJECT_ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE_PATH = PROJECT_ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = PROJECT_ROOT / "docs" / "workspace" / "changelog.md"
SELECTION_STATUS_PATH = STAGE_DIR / "04_selected" / "selection_status.md"


LABEL_TO_CLASS = {-1: 0, 0: 1, 1: 2}
CLASS_TO_LABEL = {0: -1, 1: 0, 2: 1}
CLASS_TO_NAME = {0: "short", 1: "flat", 2: "long"}
ALL_CLASSES = [0, 1, 2]


@dataclass(frozen=True)
class VariantSpec:
    variant_id: str
    idea_id: str
    hypothesis_ko: str
    model_key: str
    feature_selector: str
    threshold_quantile: float = 0.90
    min_margin: float = 0.0
    direction_mode: str = "both"
    model_params: dict[str, Any] = field(default_factory=dict)


BASE_MODEL_PARAMS: dict[str, Any] = {
    "n_estimators": 360,
    "criterion": "gini",
    "max_depth": None,
    "min_samples_split": 2,
    "min_samples_leaf": 20,
    "max_features": "sqrt",
    "bootstrap": False,
    "class_weight": "balanced",
    "random_state": 12031,
    "n_jobs": -1,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding=encoding, newline="\n")


def _read_text(path: Path, encoding: str = "utf-8-sig") -> str:
    return io_path(path).read_text(encoding=encoding)


def _exists(path: Path) -> bool:
    return io_path(path).exists()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _json_default(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        if math.isnan(float(value)):
            return None
        return float(value)
    if isinstance(value, (np.ndarray,)):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    return value


def _write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8",
    )


def _variant_specs() -> list[VariantSpec]:
    specs: list[VariantSpec] = []

    def add(
        suffix: str,
        hypothesis_ko: str,
        model_key: str,
        params: dict[str, Any] | None = None,
        feature_selector: str = "all58",
        q: float = 0.90,
        margin: float = 0.0,
        direction: str = "both",
    ) -> None:
        idx = len(specs) + 1
        specs.append(
            VariantSpec(
                variant_id=f"v{idx:02d}_{suffix}",
                idea_id=f"IDEA-ST12-ET-BATCH20-V{idx:02d}",
                hypothesis_ko=hypothesis_ko,
                model_key=model_key,
                feature_selector=feature_selector,
                threshold_quantile=q,
                min_margin=margin,
                direction_mode=direction,
                model_params=params or {},
            )
        )

    add("base_leaf20_q90", "기본 잎 20 구조가 단독 Stage12 신호를 만든다.", "base_leaf20")
    add("dense_leaf10_q90", "잎 10의 촘촘한 구조가 약한 방향 신호를 더 잘 잡는다.", "dense_leaf10", {"min_samples_leaf": 10})
    add("smooth_leaf40_q90", "잎 40의 부드러운 구조가 잡음을 줄인다.", "smooth_leaf40", {"min_samples_leaf": 40})
    add("log2_features_leaf20_q90", "분기마다 더 적은 피처를 보면 과적합이 줄어든다.", "log2_leaf20", {"max_features": "log2"})
    add("half_features_leaf20_q90", "절반 피처 샘플링이 방향 신호 다양성을 만든다.", "half_features_leaf20", {"max_features": 0.5})
    add("entropy_leaf20_q90", "엔트로피 분할 기준이 비대칭 라벨 구조를 더 잘 본다.", "entropy_leaf20", {"criterion": "entropy"})
    add(
        "balanced_subsample_leaf20_q90",
        "부트스트랩 균형 가중치가 클래스 불균형을 완화한다.",
        "balanced_subsample_leaf20",
        {"bootstrap": True, "class_weight": "balanced_subsample"},
    )
    add("depth12_leaf20_q90", "깊이 12 제한이 표본외 흔들림을 줄인다.", "depth12_leaf20", {"max_depth": 12})
    add("depth8_leaf10_q90", "얕은 깊이와 촘촘한 잎 조합이 안정 신호를 만든다.", "depth8_leaf10", {"max_depth": 8, "min_samples_leaf": 10})
    add(
        "bootstrap70_leaf20_q90",
        "70% 부트스트랩 표본이 모델 분산을 낮춘다.",
        "bootstrap70_leaf20",
        {"bootstrap": True, "max_samples": 0.70},
    )
    add("base_leaf20_q85", "더 낮은 임계값이 신호 밀도를 회복한다.", "base_leaf20", q=0.85)
    add("base_leaf20_q95", "더 높은 임계값이 신호 품질을 선별한다.", "base_leaf20", q=0.95)
    add("base_margin002_q90", "0.02 마진 요구가 애매한 예측을 걸러낸다.", "base_leaf20", margin=0.02)
    add("base_margin005_q90", "0.05 마진 요구가 강한 예측만 남긴다.", "base_leaf20", margin=0.05)
    add("base_short_only_q90", "숏 방향만 남기면 비대칭 수익 신호가 보인다.", "base_leaf20", direction="short_only")
    add("base_long_only_q90", "롱 방향만 남기면 비대칭 수익 신호가 보인다.", "base_leaf20", direction="long_only")
    add(
        "top30_features_q90",
        "훈련 중요도 상위 30개 피처가 약한 피처 잡음을 줄인다.",
        "top30_features",
        feature_selector="top30_from_train_importance",
    )
    add(
        "core42_features_q90",
        "핵심 42개 피처만으로도 단독 Stage12 신호가 유지된다.",
        "core42_features",
        feature_selector="core42",
    )
    add(
        "context16_features_q90",
        "보조 문맥 16개 피처만으로 독립 신호가 있는지 본다.",
        "context16_features",
        feature_selector="context16",
    )
    add("base_inverse_q90", "확률 방향을 반대로 쓰면 구조적 역방향성이 드러난다.", "base_leaf20", direction="inverse")
    return specs


def _model_params(spec: VariantSpec) -> dict[str, Any]:
    params = dict(BASE_MODEL_PARAMS)
    params.update(spec.model_params)
    seed_hash = hashlib.sha256(spec.model_key.encode("utf-8")).hexdigest()
    params["random_state"] = BASE_MODEL_PARAMS["random_state"] + (int(seed_hash[:8], 16) % 10000)
    return params


def _resolve_feature_sets(feature_order: list[str], train_frame: pd.DataFrame) -> dict[str, list[str]]:
    all58 = list(feature_order)
    core42 = list(feature_order[:42])
    context16 = list(feature_order[42:])
    pilot = ExtraTreesClassifier(**BASE_MODEL_PARAMS)
    y_train = train_frame["label_class"].astype(int)
    pilot.fit(train_frame[all58], y_train)
    fi = pd.DataFrame({"feature": all58, "importance": pilot.feature_importances_}).sort_values(
        ["importance", "feature"], ascending=[False, True]
    )
    top30 = fi.head(30)["feature"].tolist()
    fi_path = RUN_DIR / "feature_importance" / "pilot_top30_from_train.csv"
    io_path(fi_path.parent).mkdir(parents=True, exist_ok=True)
    fi.to_csv(io_path(fi_path), index=False, encoding="utf-8")
    return {
        "all58": all58,
        "core42": core42,
        "context16": context16,
        "top30_from_train_importance": top30,
    }


def _ensure_probs(model: ExtraTreesClassifier, x_frame: pd.DataFrame) -> np.ndarray:
    raw = model.predict_proba(x_frame)
    probs = np.zeros((len(x_frame), len(ALL_CLASSES)), dtype=float)
    for col_idx, cls in enumerate(model.classes_):
        probs[:, ALL_CLASSES.index(int(cls))] = raw[:, col_idx]
    return probs


def _split_model_metrics(y_true: pd.Series, probs: np.ndarray) -> dict[str, float]:
    pred = probs.argmax(axis=1)
    return {
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred)),
        "macro_f1": float(f1_score(y_true, pred, average="macro")),
        "log_loss": float(log_loss(y_true, probs, labels=ALL_CLASSES)),
    }


def _decision_frame(
    source: pd.DataFrame,
    probs: np.ndarray,
    threshold: float,
    spec: VariantSpec,
) -> pd.DataFrame:
    p_short = probs[:, 0]
    p_flat = probs[:, 1]
    p_long = probs[:, 2]
    nonflat_conf = np.maximum(p_short, p_long)
    predicted_direction = np.where(p_short >= p_long, 0, 2)
    competing = np.maximum(p_flat, np.where(predicted_direction == 0, p_long, p_short))
    margin = nonflat_conf - competing
    pass_gate = (nonflat_conf >= threshold) & (margin >= spec.min_margin)

    decision = np.full(len(source), 1, dtype=int)
    if spec.direction_mode == "both":
        decision[pass_gate] = predicted_direction[pass_gate]
    elif spec.direction_mode == "short_only":
        decision[pass_gate & (predicted_direction == 0)] = 0
    elif spec.direction_mode == "long_only":
        decision[pass_gate & (predicted_direction == 2)] = 2
    elif spec.direction_mode == "inverse":
        decision[pass_gate & (predicted_direction == 0)] = 2
        decision[pass_gate & (predicted_direction == 2)] = 0
    else:
        raise ValueError(f"unknown direction_mode: {spec.direction_mode}")

    is_signal = decision != 1
    correct = (decision == source["label_class"].to_numpy()) & is_signal
    out = pd.DataFrame(
        {
            "variant_id": spec.variant_id,
            "split": source["split"].to_numpy(),
            "timestamp": source["timestamp"].astype(str).to_numpy(),
            "label_class": source["label_class"].astype(int).to_numpy(),
            "label_direction": source["label_direction"].astype(int).to_numpy(),
            "p_short": p_short,
            "p_flat": p_flat,
            "p_long": p_long,
            "nonflat_conf": nonflat_conf,
            "margin": margin,
            "threshold": threshold,
            "decision_class": decision,
            "decision_direction": [CLASS_TO_LABEL[int(v)] for v in decision],
            "is_signal": is_signal,
            "directional_correct": correct,
        }
    )
    return out


def _signal_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    signals = frame[frame["is_signal"]]
    total = len(frame)
    signal_count = int(len(signals))
    hit_rate = None if signal_count == 0 else float(signals["directional_correct"].mean())
    short_count = int((signals["decision_class"] == 0).sum())
    long_count = int((signals["decision_class"] == 2).sum())
    return {
        "rows": int(total),
        "signal_count": signal_count,
        "coverage": 0.0 if total == 0 else float(signal_count / total),
        "hit_rate": hit_rate,
        "short_count": short_count,
        "long_count": long_count,
    }


def _score(val_metrics: dict[str, Any], oos_metrics: dict[str, Any]) -> float:
    val_hit = val_metrics["hit_rate"] or 0.0
    oos_hit = oos_metrics["hit_rate"] or 0.0
    min_hit = min(val_hit, oos_hit)
    min_signals = min(val_metrics["signal_count"], oos_metrics["signal_count"])
    consistency = max(0.0, 1.0 - abs(val_hit - oos_hit))
    return float(min_hit * math.log1p(min_signals) * consistency)


def _judge_variant(row: dict[str, Any]) -> str:
    val_hit = row["validation_hit_rate"] or 0.0
    oos_hit = row["oos_hit_rate"] or 0.0
    val_n = row["validation_signal_count"]
    oos_n = row["oos_signal_count"]
    if val_n < 50 or oos_n < 30:
        return "inconclusive_sparse_standalone_structural_scout"
    if val_hit >= 0.48 and oos_hit >= 0.48:
        return "candidate_standalone_structural_scout_not_runtime"
    if val_hit <= 0.40 and oos_hit <= 0.40:
        return "negative_standalone_signal_quality"
    if abs(val_hit - oos_hit) >= 0.12:
        return "mixed_unstable_standalone_structural_scout"
    return "inconclusive_standalone_structural_scout"


def _top_rows_table(results: pd.DataFrame, limit: int = 8) -> str:
    cols = [
        "rank",
        "variant_id",
        "validation_signal_count",
        "validation_hit_rate",
        "oos_signal_count",
        "oos_hit_rate",
        "package_score",
        "judgment",
    ]
    rows = results.sort_values(["package_score", "variant_id"], ascending=[False, True]).head(limit).copy()
    rows.insert(0, "rank", range(1, len(rows) + 1))
    lines = ["| rank(순위) | variant(변형) | val signals(검증 신호) | val hit(검증 적중) | oos signals(표본외 신호) | oos hit(표본외 적중) | score(점수) | judgment(판정) |"]
    lines.append("|---:|---|---:|---:|---:|---:|---:|---|")
    for row in rows[cols].to_dict(orient="records"):
        lines.append(
            "| {rank} | {variant_id} | {validation_signal_count} | {validation_hit_rate:.6f} | {oos_signal_count} | {oos_hit_rate:.6f} | {package_score:.6f} | {judgment} |".format(
                rank=row["rank"],
                variant_id=row["variant_id"],
                validation_signal_count=row["validation_signal_count"],
                validation_hit_rate=row["validation_hit_rate"] or 0.0,
                oos_signal_count=row["oos_signal_count"],
                oos_hit_rate=row["oos_hit_rate"] or 0.0,
                package_score=row["package_score"],
                judgment=row["judgment"],
            )
        )
    return "\n".join(lines)


def _write_plan(specs: list[VariantSpec], dataset_hash: str, feature_hash: str) -> None:
    lines = [
        f"# {RUN_NUMBER} Stage 12 standalone batch-20 plan(단독 20개 묶음 계획)",
        "",
        "## Scope(범위)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- exploration label(탐색 라벨): `{EXPLORATION_LABEL}`",
        "- intent(의도): Stage12 단독 ExtraTrees(엑스트라 트리) 계열 안에서 20개 가설을 한 번에 선점하고 Python structural scout(파이썬 구조 탐색)로 돌린다.",
        "- exclusion(제외): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력, 런타임 권위는 사용하지 않는다.",
        "- effect(효과): 단독 실험 경계를 고정하면서 모델 구조, 피처 묶음, 임계값, 방향 규칙의 약점과 가능성을 같이 본다.",
        "",
        "## Inputs(입력)",
        "",
        f"- dataset(데이터셋): `{DATASET_PATH}`",
        f"- dataset sha256(데이터셋 해시): `{dataset_hash}`",
        f"- feature order(피처 순서): `{FEATURE_ORDER_PATH}`",
        f"- feature order sha256(피처 순서 해시): `{feature_hash}`",
        "",
        "## Hypotheses(가설)",
        "",
        "| # | variant(변형) | idea(아이디어) | hypothesis(가설) |",
        "|---:|---|---|---|",
    ]
    for idx, spec in enumerate(specs, 1):
        lines.append(f"| {idx} | `{spec.variant_id}` | `{spec.idea_id}` | {spec.hypothesis_ko} |")
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- 이 패키지는 Python structural scout(파이썬 구조 탐색)다.",
            "- MT5(`MetaTrader 5`, 메타트레이더5) external verification(외부 검증)은 이번 주장 범위 밖(out_of_scope_by_claim, 주장 범위 밖)이다.",
            "- effect(효과): 결과가 좋아 보여도 runtime authority(런타임 권위)나 operating promotion(운영 승격)으로 말하지 않는다.",
        ]
    )
    _write_text(SPEC_PATH, "\n".join(lines) + "\n")


def _write_reports(summary: dict[str, Any], results: pd.DataFrame, specs: list[VariantSpec]) -> None:
    candidate_count = int((results["judgment"] == "candidate_standalone_structural_scout_not_runtime").sum())
    top_table = _top_rows_table(results)
    best = summary["best_variant"]
    report = f"""# {RUN_NUMBER} result summary(결과 요약)

## Boundary(경계)

- run(실행): `{RUN_ID}`
- scope(범위): Stage12 단독 ExtraTrees(엑스트라 트리) batch-20 structural scout(구조 탐색)
- no inheritance(비계승): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력은 사용하지 않았다.
- external verification(외부 검증): `out_of_scope_by_claim_standalone_python_structural_scout`
- effect(효과): 이번 결과는 후보를 좁히는 데만 쓰고, MT5(`MetaTrader 5`, 메타트레이더5) 런타임 성능 주장으로 올리지 않는다.

## Package Read(패키지 판독)

- variants tested(시험 변형): `{len(specs)}`
- candidate count(후보 수): `{candidate_count}`
- best variant by package score(패키지 점수 기준 최상위): `{best['variant_id']}`
- best validation hit(최상위 검증 적중): `{best['validation_hit_rate']:.6f}` with `{best['validation_signal_count']}` signals(신호)
- best OOS hit(최상위 표본외 적중): `{best['oos_hit_rate']:.6f}` with `{best['oos_signal_count']}` signals(신호)
- package judgment(패키지 판정): `{summary['package_judgment']}`

## Top Variants(상위 변형)

{top_table}

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): completed(완료), 20 variants(변형), Python structural scout(파이썬 구조 탐색).
- Tier B separate(Tier B 분리): `out_of_scope_by_claim_standalone_tier_a_only`.
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim_standalone_tier_a_only`.

## Failure Memory(실패 기억)

- validation/OOS(검증/표본외) 한쪽만 좋은 변형은 `mixed_unstable`로 낮춰 적었다.
- signal count(신호 수)가 너무 적은 변형은 `inconclusive_sparse`로 낮춰 적었다.
- effect(효과): 다음 MT5 probe(메타트레이더5 탐침) 후보를 고를 때 표본외 착시와 희소 신호 착시를 분리한다.
"""
    _write_text(REPORT_PATH, report)

    review = f"""# {RUN_NUMBER} review packet(검토 묶음)

## Result(결과)

`{RUN_ID}`는 Stage12 단독 20개 가설 패키지다. Python structural scout(파이썬 구조 탐색)는 완료됐다.

{top_table}

## Evidence(근거)

- manifest(실행 목록): `{RUN_DIR / 'run_manifest.json'}`
- KPI record(KPI 기록): `{RUN_DIR / 'kpi_record.json'}`
- variant results(변형 결과): `{RUN_DIR / 'results' / 'variant_results.csv'}`
- scored predictions(점수 예측): `{RUN_DIR / 'predictions' / 'scored_validation_oos.parquet'}`
- summary(요약): `{RUN_DIR / 'summary.json'}`

## Judgment(판정)

- package judgment(패키지 판정): `{summary['package_judgment']}`
- MT5 external verification(메타트레이더5 외부 검증): `out_of_scope_by_claim`.
- effect(효과): 좋은 변형이 있어도 운영 의미로 승격하지 않고, 다음 좁은 MT5 runtime probe(런타임 탐침) 후보만 만든다.
"""
    _write_text(REVIEW_PATH, review)


def _ledger_row(
    run_id: str,
    subrun_id: str,
    view_id: str,
    tier_scope: str,
    kpi_scope: str,
    status: str,
    judgment: str,
    primary_kpi_name: str,
    primary_kpi_value: Any,
    notes: str,
) -> dict[str, Any]:
    external_status = (
        "out_of_scope_by_claim"
        if status == "out_of_scope_by_claim"
        else "out_of_scope_by_claim_standalone_python_structural_scout"
    )
    return {
        "ledger_row_id": f"{run_id}__{subrun_id}__{view_id}",
        "stage_id": STAGE_ID,
        "run_id": run_id,
        "subrun_id": subrun_id,
        "parent_run_id": run_id,
        "record_view": view_id,
        "tier_scope": tier_scope,
        "kpi_scope": kpi_scope,
        "scoreboard_lane": "standalone_python_batch20_structural_scout",
        "status": status,
        "judgment": judgment,
        "path": str(RUN_DIR.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "primary_kpi": ledger_pairs(((primary_kpi_name, primary_kpi_value),)),
        "guardrail_kpi": ledger_pairs(
            (
                ("standalone_stage12", True),
                ("stage10_11_inheritance", False),
                ("stage10_11_baseline", False),
                ("review_path", str(REVIEW_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/")),
            )
        ),
        "external_verification_status": external_status,
        "notes": notes,
    }


def _update_ledgers(summary: dict[str, Any], results: pd.DataFrame) -> None:
    best = summary["best_variant"]
    package_notes = (
        f"Stage12 standalone batch20; no Stage10/11 inheritance; "
        f"best={best['variant_id']} val_hit={best['validation_hit_rate']:.6f} "
        f"oos_hit={best['oos_hit_rate']:.6f}; external_verification=out_of_scope_by_claim"
    )
    rows = [
        _ledger_row(
            RUN_ID,
            "package",
            "tier_a_batch20",
            "Tier A",
            "standalone_python_batch20_structural_scout",
            "completed",
            summary["package_judgment"],
            "variant_count",
            summary["variant_count"],
            package_notes,
        )
    ]
    for _, row in results.sort_values("variant_id").iterrows():
        rows.append(
            _ledger_row(
                RUN_ID,
                row["variant_id"],
                "tier_a_variant",
                "Tier A",
                "standalone_variant_signal_quality",
                "completed",
                row["judgment"],
                "oos_hit_rate",
                row["oos_hit_rate"],
                (
                    f"{row['idea_id']}; val_signals={row['validation_signal_count']} "
                    f"val_hit={row['validation_hit_rate']:.6f}; "
                    f"oos_signals={row['oos_signal_count']} oos_hit={row['oos_hit_rate']:.6f}"
                ),
            )
        )
    rows.extend(
        [
            _ledger_row(
                RUN_ID,
                "boundary",
                "tier_b_separate",
                "Tier B",
                "standalone_scope_boundary",
                "out_of_scope_by_claim",
                "out_of_scope_by_claim_standalone_tier_a_only",
                "status",
                "out_of_scope_by_claim",
                "Standalone Stage12 batch20 is Tier A only; Tier B not claimed.",
            ),
            _ledger_row(
                RUN_ID,
                "boundary",
                "tier_ab_combined",
                "Tier A+B",
                "standalone_scope_boundary",
                "out_of_scope_by_claim",
                "out_of_scope_by_claim_standalone_tier_a_only",
                "status",
                "out_of_scope_by_claim",
                "Standalone Stage12 batch20 is Tier A only; combined view not claimed.",
            ),
        ]
    )
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")

    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "standalone_python_batch20_structural_scout",
        "status": "completed",
        "judgment": summary["package_judgment"],
        "path": str(RUN_DIR.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "notes": ledger_pairs(
            (
                ("run_number", RUN_NUMBER),
                ("run_label", EXPLORATION_LABEL),
                ("variant_count", summary["variant_count"]),
                ("best_variant", best["variant_id"]),
                ("best_validation_hit_rate", best["validation_hit_rate"]),
                ("best_oos_hit_rate", best["oos_hit_rate"]),
                ("external_verification", summary["external_verification_status"]),
                ("notes", package_notes),
            )
        ),
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")


def _update_idea_registry(results: pd.DataFrame) -> None:
    if not _exists(IDEA_REGISTRY_PATH):
        return
    text = _read_text(IDEA_REGISTRY_PATH, encoding="utf-8-sig")
    lines = [
        "",
        f"### Stage 12(12단계) {RUN_NUMBER} standalone(단독) batch-20(20개 묶음)",
        "",
        "| idea_id(아이디어 ID) | status(상태) | hypothesis(가설) | evidence(근거) |",
        "|---|---|---|---|",
    ]
    for _, row in results.sort_values("variant_id").iterrows():
        lines.append(
            f"| `{row['idea_id']}` | `{row['judgment']}` | {row['hypothesis_ko']} | `{RUN_ID}` `{row['variant_id']}` val_hit(검증 적중)={row['validation_hit_rate']:.6f}, oos_hit(표본외 적중)={row['oos_hit_rate']:.6f} |"
        )
    block = "\n".join(lines) + "\n"
    pattern = re.compile(
        rf"\n### Stage 12(?:\(12단계\))? {RUN_NUMBER} standalone(?:\(단독\))? batch-20(?:\(20개 묶음\))?.*?(?=\n### |\n## Rule|\Z)",
        flags=re.DOTALL,
    )
    if pattern.search(text):
        text = pattern.sub(block.rstrip(), text)
    elif "\n## Rule" in text:
        text = text.replace("\n## Rule", block + "\n## Rule", 1)
    else:
        text = text.rstrip() + "\n" + block
    _write_text(IDEA_REGISTRY_PATH, text)


def _update_selection_status(summary: dict[str, Any], results: pd.DataFrame) -> None:
    if _exists(SELECTION_STATUS_PATH):
        text = _read_text(SELECTION_STATUS_PATH, encoding="utf-8-sig")
    else:
        text = f"# {STAGE_ID} selection status(선택 상태)\n"
    best = summary["best_variant"]
    block = f"""

## {RUN_NUMBER} standalone batch20 read(단독 20개 묶음 판독)

- run(실행): `{RUN_ID}`
- best structural variant(최상위 구조 변형): `{best['variant_id']}`
- validation/OOS(검증/표본외): `{best['validation_hit_rate']:.6f}` / `{best['oos_hit_rate']:.6f}`
- judgment(판정): `{summary['package_judgment']}`
- MT5(`MetaTrader 5`, 메타트레이더5): `out_of_scope_by_claim`
- effect(효과): Stage12 단독 후보 압축은 가능하지만 운영 승격이나 런타임 권위는 주장하지 않는다.
"""
    pattern = re.compile(
        rf"\n## {RUN_NUMBER} standalone batch20 read\(단독 20개 묶음 판독\).*?(?=\n## |\Z)",
        flags=re.DOTALL,
    )
    if pattern.search(text):
        text = pattern.sub(block.rstrip(), text)
    else:
        text = text.rstrip() + block
    _write_text(SELECTION_STATUS_PATH, text.rstrip() + "\n")


def _update_workspace_state(summary: dict[str, Any]) -> None:
    if not _exists(WORKSPACE_STATE_PATH):
        return
    text = _read_text(WORKSPACE_STATE_PATH, encoding="utf-8-sig")
    best = summary["best_variant"]
    replacement = f"""stage12_model_family_challenge:
  stage_id: "{STAGE_ID}"
  status: "active_standalone_batch20_python_structural_scout_completed"
  lane: "standalone_python_batch20_structural_scout"
  current_run_id: "{RUN_ID}"
  current_run_label: "{EXPLORATION_LABEL}"
  current_status: "stage12_standalone_batch20_python_structural_scout_completed"
  current_summary:
    boundary: "Stage12 standalone(단독); no Stage10/11 inheritance(10/11단계 비계승) or baseline(기준선)"
    latest_mt5_runtime_probe: "run03C_et_standalone_mt5_runtime_probe_v1"
    latest_python_package: "{RUN_ID}"
    variant_count: {summary['variant_count']}
    best_variant: "{best['variant_id']}"
    best_validation_hit_rate: {best['validation_hit_rate']:.12f}
    best_oos_hit_rate: {best['oos_hit_rate']:.12f}
    package_judgment: "{summary['package_judgment']}"
    external_verification: "out_of_scope_by_claim_standalone_python_structural_scout"
    next_action: "Choose narrow MT5 runtime probe(좁은 메타트레이더5 런타임 탐침) candidate(후보) only after standalone package review(단독 패키지 검토)"
"""
    pattern = re.compile(r"stage12_model_family_challenge:\n.*?(?=\nopen_items:)", flags=re.DOTALL)
    if pattern.search(text):
        text = pattern.sub(replacement, text)
    else:
        text = text.rstrip() + "\n" + replacement + "\n"
    _write_text(WORKSPACE_STATE_PATH, text)


def _update_current_working_state(summary: dict[str, Any]) -> None:
    if not _exists(CURRENT_STATE_PATH):
        return
    text = _read_text(CURRENT_STATE_PATH, encoding="utf-8-sig")
    best = summary["best_variant"]
    block = f"""## 현재 Stage 12 상태(Current Stage 12 State, 현재 Stage 12 상태)

- 활성 단계(active stage, 활성 단계): `12_model_family_challenge__extratrees_training_effect`.
- 현재 실행(current run, 현재 실행): `{RUN_ID}`.
- 독립 경계(standalone boundary, 독립 경계): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력은 사용하지 않는다.
- 최신 MT5 런타임 탐침(latest MT5 runtime probe, 최신 MT5 런타임 탐침): `run03C_et_standalone_mt5_runtime_probe_v1`.
- 최신 Python 패키지(latest Python package, 최신 파이썬 패키지): `{RUN_ID}`.
- 패키지 결과(package result, 패키지 결과): 20개 변형(variant, 변형) 완료, 최상위 `{best['variant_id']}`.
- 최상위 검증/표본외 적중(best validation/OOS hit, 최상위 검증/표본외 적중): `{best['validation_hit_rate']:.6f}` / `{best['oos_hit_rate']:.6f}`.
- 판정(judgment, 판정): `{summary['package_judgment']}`.
- 효과(effect, 효과): 후보 압축은 가능하지만 MT5(`MetaTrader 5`, 메타트레이더5) 외부 검증 없이 runtime authority(런타임 권위)나 operating promotion(운영 승격)을 주장하지 않는다.
"""
    pattern = re.compile(
        r"## 현재 Stage 12 상태\(Current Stage 12 State, 현재 Stage 12 상태\).*?(?=\n## 현재 경계)",
        flags=re.DOTALL,
    )
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        text = text.rstrip() + "\n\n" + block
    _write_text(CURRENT_STATE_PATH, text)


def _update_changelog(summary: dict[str, Any]) -> None:
    if not _exists(CHANGELOG_PATH):
        return
    text = _read_text(CHANGELOG_PATH, encoding="utf-8-sig")
    best = summary["best_variant"]
    entry = (
        f"\n- 2026-04-28: `{RUN_ID}` completed(완료). Stage12 standalone batch20(단독 20개 묶음) "
        f"Python structural scout(파이썬 구조 탐색), best(최상위) `{best['variant_id']}` "
        f"validation/OOS hit(검증/표본외 적중) `{best['validation_hit_rate']:.6f}` / "
        f"`{best['oos_hit_rate']:.6f}`, MT5 external verification(메타트레이더5 외부 검증) "
        f"`out_of_scope_by_claim`.\n"
    )
    pattern = re.compile(rf"\n- 2026-04-28: `{RUN_ID}` completed\(완료\).*?(?=\n- |\Z)", flags=re.DOTALL)
    if pattern.search(text):
        text = pattern.sub(entry.rstrip(), text)
    else:
        text = text.rstrip() + entry
    _write_text(CHANGELOG_PATH, text.rstrip() + "\n")


def _prepare_dataset() -> tuple[pd.DataFrame, list[str], str, str]:
    if not _exists(DATASET_PATH):
        raise FileNotFoundError(DATASET_PATH)
    if not _exists(FEATURE_ORDER_PATH):
        raise FileNotFoundError(FEATURE_ORDER_PATH)
    dataset_hash = _sha256(DATASET_PATH)
    feature_hash = _sha256(FEATURE_ORDER_PATH)
    frame = pd.read_parquet(io_path(DATASET_PATH))
    feature_order = [
        line.strip()
        for line in _read_text(FEATURE_ORDER_PATH, encoding="utf-8").splitlines()
        if line.strip()
    ]
    missing = [feature for feature in feature_order if feature not in frame.columns]
    if missing:
        raise ValueError(f"missing feature columns: {missing[:5]}")
    required = ["timestamp", "split"]
    missing_required = [col for col in required if col not in frame.columns]
    if missing_required:
        raise ValueError(f"missing required columns: {missing_required}")
    frame = frame.copy()
    if "label_class" in frame.columns:
        frame["label_class"] = frame["label_class"].astype(int)
    elif "label_direction" in frame.columns:
        frame["label_class"] = frame["label_direction"].map(LABEL_TO_CLASS).astype(int)
    else:
        raise ValueError("missing label_class or label_direction")
    if "label_direction" not in frame.columns:
        frame["label_direction"] = frame["label_class"].map(CLASS_TO_LABEL).astype(int)
    return frame, feature_order, dataset_hash, feature_hash


def run() -> dict[str, Any]:
    started_at = _utc_now()
    specs = _variant_specs()
    frame, feature_order, dataset_hash, feature_hash = _prepare_dataset()
    _write_plan(specs, dataset_hash, feature_hash)

    train = frame[frame["split"] == "train"].reset_index(drop=True)
    validation = frame[frame["split"] == "validation"].reset_index(drop=True)
    oos = frame[frame["split"] == "oos"].reset_index(drop=True)
    split_frames = {"train": train, "validation": validation, "oos": oos}
    feature_sets = _resolve_feature_sets(feature_order, train)

    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(RUN_DIR / "results").mkdir(parents=True, exist_ok=True)
    io_path(RUN_DIR / "predictions").mkdir(parents=True, exist_ok=True)
    io_path(RUN_DIR / "reports").mkdir(parents=True, exist_ok=True)

    model_cache: dict[tuple[str, tuple[str, ...]], ExtraTreesClassifier] = {}
    prob_cache: dict[tuple[str, tuple[str, ...]], dict[str, np.ndarray]] = {}
    result_rows: list[dict[str, Any]] = []
    scored_frames: list[pd.DataFrame] = []

    for spec in specs:
        features = feature_sets[spec.feature_selector]
        feature_key = tuple(features)
        cache_key = (spec.model_key, feature_key)
        if cache_key not in model_cache:
            params = _model_params(spec)
            model = ExtraTreesClassifier(**params)
            model.fit(train[features], train["label_class"].astype(int))
            model_cache[cache_key] = model
            prob_cache[cache_key] = {
                split_name: _ensure_probs(model, split_frame[features])
                for split_name, split_frame in split_frames.items()
            }
        model = model_cache[cache_key]
        probs_by_split = prob_cache[cache_key]
        val_probs = probs_by_split["validation"]
        val_conf = np.maximum(val_probs[:, 0], val_probs[:, 2])
        threshold = float(np.quantile(val_conf, spec.threshold_quantile))

        split_model_metrics = {
            split_name: _split_model_metrics(split_frame["label_class"].astype(int), probs)
            for split_name, split_frame, probs in [
                ("train", train, probs_by_split["train"]),
                ("validation", validation, probs_by_split["validation"]),
                ("oos", oos, probs_by_split["oos"]),
            ]
        }
        split_signal_metrics: dict[str, dict[str, Any]] = {}
        for split_name in ["train", "validation", "oos"]:
            decision = _decision_frame(split_frames[split_name], probs_by_split[split_name], threshold, spec)
            split_signal_metrics[split_name] = _signal_metrics(decision)
            if split_name in {"validation", "oos"}:
                scored_frames.append(decision)

        row: dict[str, Any] = {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "variant_id": spec.variant_id,
            "idea_id": spec.idea_id,
            "hypothesis_ko": spec.hypothesis_ko,
            "model_key": spec.model_key,
            "feature_selector": spec.feature_selector,
            "feature_count": len(features),
            "threshold_quantile": spec.threshold_quantile,
            "threshold": threshold,
            "min_margin": spec.min_margin,
            "direction_mode": spec.direction_mode,
            "model_params_json": json.dumps(_model_params(spec), ensure_ascii=False, sort_keys=True),
            "model_classes": ",".join(CLASS_TO_NAME[int(c)] for c in model.classes_),
        }
        for split_name in ["train", "validation", "oos"]:
            for key, value in split_model_metrics[split_name].items():
                row[f"{split_name}_{key}"] = value
            for key, value in split_signal_metrics[split_name].items():
                row[f"{split_name}_{key}"] = value
        row["package_score"] = _score(split_signal_metrics["validation"], split_signal_metrics["oos"])
        row["candidate_for_mt5_probe"] = bool(
            (row["validation_signal_count"] >= 100)
            and (row["oos_signal_count"] >= 50)
            and ((row["validation_hit_rate"] or 0.0) >= 0.48)
            and ((row["oos_hit_rate"] or 0.0) >= 0.48)
        )
        row["judgment"] = _judge_variant(row)
        result_rows.append(row)

    results = pd.DataFrame(result_rows).sort_values(["package_score", "variant_id"], ascending=[False, True])
    results.to_csv(io_path(RUN_DIR / "results" / "variant_results.csv"), index=False, encoding="utf-8")
    pd.concat(scored_frames, ignore_index=True).to_parquet(
        io_path(RUN_DIR / "predictions" / "scored_validation_oos.parquet"),
        index=False,
    )

    variant_plan = pd.DataFrame(
        [
            {
                "variant_id": spec.variant_id,
                "idea_id": spec.idea_id,
                "hypothesis_ko": spec.hypothesis_ko,
                "model_key": spec.model_key,
                "feature_selector": spec.feature_selector,
                "threshold_quantile": spec.threshold_quantile,
                "min_margin": spec.min_margin,
                "direction_mode": spec.direction_mode,
                "model_params_json": json.dumps(_model_params(spec), ensure_ascii=False, sort_keys=True),
            }
            for spec in specs
        ]
    )
    variant_plan.to_csv(io_path(RUN_DIR / "variant_plan.csv"), index=False, encoding="utf-8")

    candidate_count = int(results["candidate_for_mt5_probe"].sum())
    package_judgment = (
        "candidate_compression_possible_not_runtime"
        if candidate_count > 0
        else "inconclusive_standalone_batch20_structural_scout"
    )
    best = results.iloc[0].to_dict()
    summary = {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "exploration_label": EXPLORATION_LABEL,
        "started_at_utc": started_at,
        "completed_at_utc": _utc_now(),
        "dataset_path": str(DATASET_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "dataset_sha256": dataset_hash,
        "feature_order_path": str(FEATURE_ORDER_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "feature_order_sha256": feature_hash,
        "variant_count": len(specs),
        "candidate_count": candidate_count,
        "package_judgment": package_judgment,
        "external_verification_status": "out_of_scope_by_claim_standalone_python_structural_scout",
        "standalone_boundary": {
            "stage10_11_inheritance": False,
            "stage10_11_baseline": False,
            "tier_scope": "Tier A only",
            "tier_b_status": "out_of_scope_by_claim_standalone_tier_a_only",
            "tier_ab_status": "out_of_scope_by_claim_standalone_tier_a_only",
        },
        "model_persistence": "not_persisted_batch_scout_reproducible_from_manifest",
        "best_variant": best,
        "artifacts": {
            "plan": str(SPEC_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "variant_plan": str((RUN_DIR / "variant_plan.csv").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "variant_results": str((RUN_DIR / "results" / "variant_results.csv").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "scored_predictions": str((RUN_DIR / "predictions" / "scored_validation_oos.parquet").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "summary": str((RUN_DIR / "summary.json").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "kpi_record": str((RUN_DIR / "kpi_record.json").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "report": str(REPORT_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "review": str(REVIEW_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        },
    }
    _write_json(RUN_DIR / "summary.json", summary)
    _write_json(
        RUN_DIR / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "kpi_scope": "standalone_python_batch20_structural_scout",
            "variant_count": len(specs),
            "candidate_count": candidate_count,
            "package_judgment": package_judgment,
            "best_variant": {
                "variant_id": best["variant_id"],
                "validation_signal_count": best["validation_signal_count"],
                "validation_hit_rate": best["validation_hit_rate"],
                "oos_signal_count": best["oos_signal_count"],
                "oos_hit_rate": best["oos_hit_rate"],
                "package_score": best["package_score"],
            },
            "tier_records": {
                "tier_a_separate": "completed",
                "tier_b_separate": "out_of_scope_by_claim_standalone_tier_a_only",
                "tier_ab_combined": "out_of_scope_by_claim_standalone_tier_a_only",
            },
            "external_verification_status": "out_of_scope_by_claim_standalone_python_structural_scout",
        },
    )
    _write_json(
        RUN_DIR / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "command": "python foundation/pipelines/run_stage12_extratrees_standalone_batch20.py",
            "dataset_path": str(DATASET_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "dataset_sha256": dataset_hash,
            "feature_order_path": str(FEATURE_ORDER_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "feature_order_sha256": feature_hash,
            "variant_count": len(specs),
            "variant_ids": [spec.variant_id for spec in specs],
            "standalone_boundary": summary["standalone_boundary"],
            "external_verification_status": summary["external_verification_status"],
            "created_at_utc": summary["completed_at_utc"],
        },
    )
    _write_reports(summary, results, specs)
    _update_ledgers(summary, results)
    _update_idea_registry(results)
    _update_selection_status(summary, results)
    _update_workspace_state(summary)
    _update_current_working_state(summary)
    _update_changelog(summary)
    return summary


if __name__ == "__main__":
    payload = run()
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default))
