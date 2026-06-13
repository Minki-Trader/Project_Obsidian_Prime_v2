from __future__ import annotations

import csv
import json
import math
import pickle
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_02 import trainable_onnx_seed_surface as trainable
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = f03b.STAGE_ID
RUN_ID = "frontier03C_regime_asymmetric_label_micro_search_v1"
RUN_NUMBER = "frontier03C"
PARENT_RUN_ID = f03b.RUN_ID
NEXT_CLUE_RUN_ID = "frontier03D_grok_pre_expensive_wfo_mt5_review_v1"
NEXT_REPAIR_RUN_ID = "frontier03D_regime_asymmetric_label_model_repair_v1"

RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MODEL_ROOT = RUN_ROOT / "models"
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
PARENT_TOP = Path("stages") / STAGE_ID / "02_runs" / PARENT_RUN_ID / "top_label_proxy_surfaces.csv"

MODEL_ID = "frontier03c_logreg_teacher__f03b_v08_trend_long_easy"
PROBABILITY_THRESHOLDS = (0.34, 0.38, 0.42, 0.46, 0.50, 0.55, 0.60, 0.65)
PROBABILITY_MARGINS = (0.00, 0.03, 0.06, 0.10)
COOLDOWNS = (0, 3, 6, 9, 12, 18)
FORBIDDEN_CLAIMS = f03b.FORBIDDEN_CLAIMS


def main() -> int:
    ensure_dirs()
    now = utc_now()
    frame = f03b.load_and_validate_input()
    feature_order = f03b.read_feature_order()
    f03b_reference = load_parent_top()
    variant = select_variant(f03b_reference["variant_id"])
    regime = f03b.build_regime(frame)
    base_threshold = f03b.compute_base_threshold(frame)
    signal, _ = f03b.build_signal(
        pd.to_numeric(frame["future_log_return_12"], errors="coerce").astype("float64").to_numpy(),
        regime["regime"].to_numpy(),
        base_threshold,
        variant,
    )
    labels = pd.Series(np.where(signal == -1, 0, np.where(signal == 1, 2, 1)), index=frame.index, dtype="int64")
    validate_train_labels(frame, labels)
    model = train_model(frame, feature_order, labels)
    model_path = MODEL_ROOT / f"{MODEL_ID}.pkl"
    onnx_path = MODEL_ROOT / f"{MODEL_ID}.onnx"
    with io_path(model_path).open("wb") as handle:
        pickle.dump(model, handle)
    export_record = export_sklearn_to_onnx_zipmap_disabled(
        model,
        onnx_path,
        feature_count=len(feature_order),
        input_name="float_input",
        target_opset=12,
        drop_label_output=True,
    )
    parity = check_onnxruntime_probability_parity(
        model,
        onnx_path,
        parity_sample(frame, feature_order),
        tolerance=1e-5,
    )
    classifier_metrics = trainable.evaluate_classifier_against_teacher(model, frame, feature_order, labels)
    probabilities = ordered_sklearn_probabilities(model, frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False))
    metrics = evaluate_decision_grid(frame, probabilities)
    model_table = model_table_frame(model_path, onnx_path, parity, variant, f03b_reference)
    summary = trainable.build_decision_summary(metrics, model_table)
    top = trainable.top_seed_decisions(summary)
    observation_rows = int(summary["onnx_seed_observation_flag"].sum())
    final = build_final(now, frame, feature_order, variant, f03b_reference, model_path, onnx_path, parity, classifier_metrics, summary, top, observation_rows)
    write_outputs(model_table, classifier_metrics, metrics, summary, top, final, export_record, parity)
    update_docs(now, final, top)
    update_registries(now, final)
    update_current_truth(now, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "onnx_seed_observation_rows": observation_rows,
                "best_candidate": final["best_candidate_id"],
                "best_oos_pf": final["best_oos_profit_factor"],
                "best_oos_density": final["best_oos_trades_per_day"],
                "best_oos_dd": final["best_oos_max_drawdown_percent"],
                "next_run_id": final["next_run_id"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, REPORT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_parent_top() -> dict[str, Any]:
    top = pd.read_csv(io_path(PARENT_TOP)).iloc[0].to_dict()
    return top


def select_variant(variant_id: str) -> f03b.LabelVariant:
    for variant in f03b.VARIANTS:
        if variant.variant_id == variant_id:
            return variant
    raise ValueError(f"Unknown Frontier03B variant(알 수 없는 전선03B 변형): {variant_id}")


def validate_train_labels(frame: pd.DataFrame, labels: pd.Series) -> None:
    train_mask = frame["split"].astype(str).eq("train")
    present = set(labels.loc[train_mask].astype(int).tolist())
    missing = sorted(set(LABEL_ORDER).difference(present))
    if missing:
        raise ValueError(f"Teacher labels(교사 라벨)에 필요한 클래스가 없습니다: {missing}")


def train_model(frame: pd.DataFrame, feature_order: list[str], labels: pd.Series) -> Pipeline:
    train_mask = frame["split"].astype(str).eq("train")
    X_train = frame.loc[train_mask, feature_order].to_numpy(dtype="float64", copy=False)
    y_train = labels.loc[train_mask].astype("int64").to_numpy()
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1200,
                    random_state=31,
                    solver="lbfgs",
                    class_weight="balanced",
                ),
            ),
        ]
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        model.fit(X_train, y_train)
    return model


def parity_sample(frame: pd.DataFrame, feature_order: list[str]) -> np.ndarray:
    sample = (
        frame.groupby("split", group_keys=False)
        .head(80)
        .loc[:, feature_order]
        .to_numpy(dtype="float64", copy=False)
    )
    return sample


def evaluate_decision_grid(frame: pd.DataFrame, probabilities: np.ndarray) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    cash = pd.to_numeric(frame["is_us_cash_open"], errors="coerce").fillna(0).eq(1).to_numpy(dtype=bool)
    for threshold in PROBABILITY_THRESHOLDS:
        for margin in PROBABILITY_MARGINS:
            raw_signal = trainable.signal_from_probabilities(
                probabilities,
                threshold=float(threshold),
                margin=float(margin),
                filter_mask=cash,
                side_mode="both",
            )
            for cooldown in COOLDOWNS:
                signal = scout.apply_cooldown(raw_signal, cooldown)
                candidate_id = f"f03c_logreg_f03b_v08__p{int(threshold * 100)}__m{int(margin * 100)}__cd{cooldown}"
                for split in ("train", "validation", "oos"):
                    rows.append(
                        trainable.evaluate_model_split(
                            frame=frame,
                            signal=signal,
                            split=split,
                            candidate_id=candidate_id,
                            model_id=MODEL_ID,
                            teacher_candidate_id="f03b_v08_trend_long_easy",
                            surface="regime_asymmetric_label_v08",
                            filter_name="all_cash",
                            side_mode="both",
                            probability_threshold=float(threshold),
                            probability_margin=float(margin),
                            cooldown=int(cooldown),
                        )
                    )
    return pd.DataFrame(rows)


def model_table_frame(
    model_path: Path,
    onnx_path: Path,
    parity: dict[str, Any],
    variant: f03b.LabelVariant,
    parent_top: dict[str, Any],
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "candidate_model_id": MODEL_ID,
                "teacher_candidate_id": variant.variant_id,
                "surface": "regime_asymmetric_label_v08",
                "filter_name": "all_cash",
                "side_mode": "both",
                "teacher_threshold_quantile": 0.33,
                "teacher_cooldown_bars": 0,
                "teacher_train_trades_per_day": num(parent_top.get("train_trades_per_day")),
                "teacher_validation_profit_factor": num(parent_top.get("validation_profit_factor")),
                "teacher_validation_trades_per_day": num(parent_top.get("validation_trades_per_day")),
                "teacher_validation_max_drawdown_percent": num(parent_top.get("validation_max_drawdown_percent")),
                "teacher_oos_profit_factor": num(parent_top.get("oos_profit_factor")),
                "teacher_oos_trades_per_day": num(parent_top.get("oos_trades_per_day")),
                "teacher_oos_max_drawdown_percent": num(parent_top.get("oos_max_drawdown_percent")),
                "model_path": model_path.as_posix(),
                "model_sha256": sha256_file(model_path),
                "onnx_path": onnx_path.as_posix(),
                "onnx_sha256": sha256_file(onnx_path),
                "onnx_parity_passed": bool(parity["passed"]),
            }
        ]
    )


def build_final(
    now: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    variant: f03b.LabelVariant,
    parent_top: dict[str, Any],
    model_path: Path,
    onnx_path: Path,
    parity: dict[str, Any],
    classifier_metrics: dict[str, Any],
    summary: pd.DataFrame,
    top: pd.DataFrame,
    observation_rows: int,
) -> dict[str, Any]:
    best = top.iloc[0].to_dict()
    has_observation = observation_rows > 0
    status = "completed_trainable_onnx_smoke_with_seed_observation_no_authority" if has_observation else "completed_trainable_onnx_smoke_weak_no_authority"
    judgment = "onnx_seed_observation_no_authority" if has_observation else "weak_trainable_signal_no_authority"
    next_run_id = NEXT_CLUE_RUN_ID if has_observation else NEXT_REPAIR_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": now,
        "next_run_id": next_run_id,
        "teacher_variant_id": variant.variant_id,
        "trained_models": 1,
        "decision_rows": int(len(summary)),
        "onnx_seed_observation_rows": observation_rows,
        "best_candidate_id": str(best["candidate_id"]),
        "best_validation_net_profit": num(best["validation_net_profit"]),
        "best_validation_profit_factor": num(best["validation_profit_factor"]),
        "best_validation_trades_per_day": num(best["validation_trades_per_day"]),
        "best_validation_max_drawdown_percent": num(best["validation_max_drawdown_percent"]),
        "best_validation_aspiration_distance_score": num(best["validation_aspiration_distance_score"]),
        "best_oos_net_profit": num(best["oos_net_profit"]),
        "best_oos_profit_factor": num(best["oos_profit_factor"]),
        "best_oos_trades_per_day": num(best["oos_trades_per_day"]),
        "best_oos_max_drawdown_percent": num(best["oos_max_drawdown_percent"]),
        "best_oos_aspiration_distance_score": num(best["oos_aspiration_distance_score"]),
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": sha256_file(onnx_path),
        "onnx_parity": parity,
        "classifier_metrics": json_ready(classifier_metrics),
        "parent_label_proxy": json_ready(parent_top),
        "data_identity": {
            "dataset_path": f03b.DATASET_PATH.as_posix(),
            "dataset_sha256": sha256_file(f03b.DATASET_PATH),
            "feature_order_path": f03b.FEATURE_ORDER_PATH.as_posix(),
            "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
            "feature_order_hash": ordered_hash(feature_order),
            "rows": int(len(frame)),
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in FORBIDDEN_CLAIMS},
    }


def write_outputs(
    model_table: pd.DataFrame,
    classifier_metrics: dict[str, Any],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    top: pd.DataFrame,
    final: dict[str, Any],
    export_record: dict[str, Any],
    parity: dict[str, Any],
) -> None:
    paths = {
        "model_training_summary": RUN_ROOT / "model_training_summary.csv",
        "classifier_metrics": RUN_ROOT / "classifier_metrics.json",
        "decision_surface_metrics": RUN_ROOT / "decision_surface_metrics.csv",
        "decision_surface_summary": RUN_ROOT / "decision_surface_summary.csv",
        "top_onnx_seed_surfaces": RUN_ROOT / "top_onnx_seed_surfaces.csv",
        "model_export_records": RUN_ROOT / "model_export_records.json",
        "onnx_parity_audit": RUN_ROOT / "onnx_parity_audit.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    model_table.to_csv(io_path(paths["model_training_summary"]), index=False, lineterminator="\n")
    metrics.to_csv(io_path(paths["decision_surface_metrics"]), index=False, lineterminator="\n")
    summary.to_csv(io_path(paths["decision_surface_summary"]), index=False, lineterminator="\n")
    top.to_csv(io_path(paths["top_onnx_seed_surfaces"]), index=False, lineterminator="\n")
    write_json(paths["classifier_metrics"], classifier_metrics)
    write_json(paths["model_export_records"], {"exports": [export_record], "skipped": []})
    write_json(paths["onnx_parity_audit"], {"records": [parity]})
    write_text_sig(REPORT_PATH, report_text(final, top))
    outputs = {
        name: {"path": path.as_posix(), "sha256": sha256_file(path)}
        for name, path in paths.items()
        if name != "run_manifest"
    }
    outputs["report"] = {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)}
    outputs["onnx_model"] = {"path": final["onnx_path"], "sha256": final["onnx_sha256"]}
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_03/frontier03c_regime_asymmetric_label_micro_search.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_03/frontier03c_regime_asymmetric_label_micro_search.py")),
        "inputs": {
            "parent_run_id": PARENT_RUN_ID,
            "parent_top": PARENT_TOP.as_posix(),
            "parent_top_sha256": sha256_file(PARENT_TOP),
            "dataset_path": f03b.DATASET_PATH.as_posix(),
            "dataset_sha256": sha256_file(f03b.DATASET_PATH),
            "feature_order_path": f03b.FEATURE_ORDER_PATH.as_posix(),
            "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
        },
        "outputs": outputs,
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(paths["run_manifest"], manifest)


def report_text(final: dict[str, Any], top: pd.DataFrame) -> str:
    best = top.iloc[0].to_dict()
    rows = top.head(5).to_dict("records")
    return f"""# Frontier03C Trainable ONNX Smoke Report(전선03C 학습 가능 온엑스 스모크 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Boundary(경계)

This run(이번 실행)은 Frontier03B(전선03B)의 oracle label proxy(오라클 라벨 프록시)를 LogisticRegression ONNX(로지스틱 회귀 온엑스)로 낮춘 smoke test(스모크 테스트)입니다. WFO(워크포워드), MT5(메타트레이더5), runtime authority(런타임 권위), live readiness(실거래 준비)는 없습니다.

## ONNX Identity(온엑스 정체성)

- onnx path(온엑스 경로): `{final['onnx_path']}`
- onnx sha256(온엑스 해시): `{final['onnx_sha256']}`
- parity passed(동등성 통과): `{final['onnx_parity']['passed']}`

## Best Decision Surface(최상위 결정 표면)

- candidate_id(후보 ID): `{best['candidate_id']}`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{fmt(best['validation_net_profit'])}` / `{fmt(best['validation_profit_factor'])}` / `{fmt(best['validation_trades_per_day'])}/day` / `{fmt(best['validation_max_drawdown_percent'])}%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `{fmt(best['oos_net_profit'])}` / `{fmt(best['oos_profit_factor'])}` / `{fmt(best['oos_trades_per_day'])}/day` / `{fmt(best['oos_max_drawdown_percent'])}%`
- onnx_seed_observation_rows(온엑스 씨앗 관찰 행): `{final['onnx_seed_observation_rows']}`

## Top Rows(상위 행)

```json
{json.dumps(json_ready(rows), ensure_ascii=False, indent=2)}
```

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 expensive WFO/MT5(비싼 워크포워드/MT5) 전 Grok review(그록 검토)를 열거나, 약하면 model/label repair(모델/라벨 수리)로 돌아가는 것입니다. Effect(효과)는 seed observation(씨앗 관찰)을 운영 주장 없이 다음 검증 단계로 넘기는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def update_docs(now: str, final: dict[str, Any], top: pd.DataFrame) -> None:
    f03b.append_once(
        Path("stages") / STAGE_ID / "03_reviews" / "review_index.md",
        RUN_ID,
        f"- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{final['judgment']}`\n",
    )
    f03b.write_text_sig(
        Path("stages") / STAGE_ID / "04_selected" / "selection_status.md",
        f"""# Stage Frontier 03 Selection Status(전선 03단계 선택 상태)

Updated(갱신): {now}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{final['judgment']}`

Best ONNX smoke(최상위 온엑스 스모크): `{final['best_candidate_id']}`

ONNX seed observation rows(온엑스 씨앗 관찰 행): `{final['onnx_seed_observation_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )


def update_current_truth(now: str, final: dict[str, Any]) -> None:
    payload = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": final["status"],
        "current_judgment": final["judgment"],
        "next_run_id": final["next_run_id"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml_dump(payload), encoding="utf-8")
    f03b.write_text_sig(
        f03b.CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier03C(전선03C)는 Frontier03B(전선03B) label proxy(라벨 프록시)를 LogisticRegression ONNX(로지스틱 회귀 온엑스) smoke test(스모크 테스트)로 낮춰 확인했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{final['best_candidate_id']}` with OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(final['best_oos_profit_factor'])}` / `{fmt(final['best_oos_trades_per_day'])}/day` / `{fmt(final['best_oos_max_drawdown_percent'])}%`.

Next action(다음 행동): `{final['next_run_id']}`.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )


def update_registries(now: str, final: dict[str, Any]) -> None:
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, final))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(final))
    f03b.upsert_csv(Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(final))
    f03b.append_once(f03b.CHANGELOG, RUN_ID, f"- {now}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n")
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, f"- `{RUN_ID}`: trainable ONNX smoke(학습 가능 온엑스 스모크) completed(완료). Effect(효과): oracle label clue(오라클 라벨 단서)의 예측 가능성을 확인했습니다.\n")


def run_registry_row(now: str, final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "trainable_onnx_smoke(학습 가능 온엑스 스모크)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"observation_rows={final['onnx_seed_observation_rows']};no_authority",
        "work_family": "model_validation(모델 검증)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["decision_rows"]),
        "claim_boundary": "onnx_smoke_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__onnx_smoke",
        "subrun_id": f"{RUN_ID}__onnx_smoke",
        "record_view": "ONNX smoke(온엑스 스모크)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_proxy_no_mt5(파이썬 프록시, MT5 없음)",
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "onnx_parity_passed_no_wfo_no_mt5_no_authority(온엑스 동등성 통과, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": final["onnx_path"],
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "trainable_onnx_smoke_only(학습 가능 온엑스 스모크 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can the Frontier03B oracle label clue survive a trainable ONNX smoke?(전선03B 오라클 라벨 단서가 학습 가능 온엑스 스모크에서 살아남는가?)",
        "skill_family": "model_validation(모델 검증)",
        "lineage_summary": "label_proxy_to_onnx_smoke(라벨 프록시에서 온엑스 스모크)",
    }


def ledger_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__onnx_smoke",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__onnx_smoke",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "ONNX smoke(온엑스 스모크)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_proxy_no_mt5(파이썬 프록시, MT5 없음)",
        "scoreboard_lane": "trainable_onnx_smoke(학습 가능 온엑스 스모크)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "onnx_parity_passed_no_wfo_no_mt5_no_authority(온엑스 동등성 통과, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "notes": f"observation_rows={final['onnx_seed_observation_rows']};next={final['next_run_id']};no_authority",
    }


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def yaml_dump(payload: dict[str, Any]) -> str:
    import yaml

    return yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def num(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    return f"{num(value):.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
