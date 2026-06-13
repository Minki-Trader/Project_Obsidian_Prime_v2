from __future__ import annotations

import json
import math
import pickle
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
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
from stage_pipelines.stage_frontier_03 import frontier03c_regime_asymmetric_label_micro_search as f03c
from stage_pipelines.stage_frontier_03 import frontier03d_regime_asymmetric_label_model_repair as f03d


STAGE_ID = f03b.STAGE_ID
RUN_ID = "frontier03E_bounded_two_teacher_density_repair_v1"
RUN_NUMBER = "frontier03E_repair"
PARENT_RUN_ID = f03d.RUN_ID
SOURCE_LABEL_RUN_ID = f03b.RUN_ID
NEXT_PRECHECK_RUN_ID = "frontier03F_grok_pre_wfo_mt5_or_stress_handoff_v1"
NEXT_CLOSEOUT_REVIEW_RUN_ID = "frontier03F_grok_stage_closeout_review_v1"

RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MODEL_ROOT = RUN_ROOT / "models"
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
PARENT_TOP = Path("stages") / STAGE_ID / "02_runs" / SOURCE_LABEL_RUN_ID / "top_label_proxy_surfaces.csv"

TEACHER_VARIANT_IDS = ("f03b_v11_trend_density_restore", "f03b_v04_trend_easy_chop_strict")
THRESHOLDS = (0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42)
MARGINS = (0.00, 0.02, 0.04, 0.06, 0.08)
COOLDOWNS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
SIDE_MODES = ("both", "long_only", "short_only")
VAL_DD_CEILING = f03d.VAL_DD_CEILING
OOS_DD_CEILING = f03d.OOS_DD_CEILING
FORBIDDEN_CLAIMS = f03b.FORBIDDEN_CLAIMS


def main() -> int:
    ensure_dirs()
    now = utc_now()
    frame = f03b.load_and_validate_input()
    feature_order = f03b.read_feature_order()
    parent_top = load_parent_top()
    regime = f03b.build_regime(frame)
    base_threshold = f03b.compute_base_threshold(frame)
    model_rows: list[dict[str, Any]] = []
    classifier_rows: list[dict[str, Any]] = []
    export_records: list[dict[str, Any]] = []
    parity_records: list[dict[str, Any]] = []
    metric_frames: list[pd.DataFrame] = []
    teacher_records: list[dict[str, Any]] = []

    for variant_id in TEACHER_VARIANT_IDS:
        variant = select_variant(variant_id)
        parent_row = parent_row_for_variant(parent_top, variant_id)
        labels = build_teacher_labels(frame, regime, base_threshold, variant)
        f03c.validate_train_labels(frame, labels)
        model = f03c.train_model(frame, feature_order, labels)
        model_id = f"frontier03e_logreg_teacher__{variant_id}"
        model_path = MODEL_ROOT / f"{model_id}.pkl"
        onnx_path = MODEL_ROOT / f"{model_id}.onnx"
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
            f03c.parity_sample(frame, feature_order),
            tolerance=1e-5,
        )
        classifier_metrics = trainable.evaluate_classifier_against_teacher(model, frame, feature_order, labels)
        probabilities = ordered_sklearn_probabilities(model, frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False))
        metric_frames.append(evaluate_decision_grid(frame, probabilities, model_id, variant_id))
        model_rows.append(model_table_row(model_id, model_path, onnx_path, parity, variant, parent_row))
        classifier_rows.append({"model_id": model_id, "teacher_variant_id": variant_id, "metrics": json_ready(classifier_metrics)})
        export_records.append(export_record)
        parity_records.append(parity)
        teacher_records.append(teacher_record(variant, labels, frame, parent_row))

    metrics = pd.concat(metric_frames, ignore_index=True)
    model_table = pd.DataFrame(model_rows)
    summary = trainable.build_decision_summary(metrics, model_table)
    summary["teacher_repair_success_flag"] = teacher_repair_success_mask(summary)
    summary["teacher_repair_stop_candidate_flag"] = teacher_repair_stop_candidate_mask(summary)
    summary["teacher_repair_distance_score"] = teacher_repair_distance(summary)
    ranked = rank_summary(summary)
    success_rows = ranked.loc[ranked["teacher_repair_success_flag"].astype(bool)].copy()
    stop_rows = ranked.loc[ranked["teacher_repair_stop_candidate_flag"].astype(bool)].copy()
    final = build_final(now, frame, feature_order, ranked, success_rows, stop_rows, model_table, teacher_records)
    write_outputs(
        model_table=model_table,
        classifier_rows=classifier_rows,
        metrics=metrics,
        summary=summary,
        top=ranked.head(30),
        success_rows=success_rows,
        stop_rows=stop_rows,
        final=final,
        export_records=export_records,
        parity_records=parity_records,
        teacher_records=teacher_records,
    )
    update_docs_and_state(now, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "teacher_repair_success_rows": final["teacher_repair_success_rows"],
                "teacher_repair_stop_candidate_rows": final["teacher_repair_stop_candidate_rows"],
                "best_candidate": final["best_candidate_id"],
                "best_teacher_variant": final["best_teacher_variant_id"],
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


def load_parent_top() -> pd.DataFrame:
    return pd.read_csv(io_path(PARENT_TOP))


def select_variant(variant_id: str) -> f03b.LabelVariant:
    for variant in f03b.VARIANTS:
        if variant.variant_id == variant_id:
            return variant
    raise ValueError(f"Unknown Frontier03B variant(알 수 없는 전선03B 변형): {variant_id}")


def parent_row_for_variant(parent_top: pd.DataFrame, variant_id: str) -> dict[str, Any]:
    rows = parent_top.loc[parent_top["variant_id"].astype(str).eq(variant_id)]
    if rows.empty:
        return {"variant_id": variant_id, "source": "not_found_in_parent_top(부모 상위 표에 없음)"}
    return rows.iloc[0].to_dict()


def build_teacher_labels(
    frame: pd.DataFrame,
    regime: pd.DataFrame,
    base_threshold: float,
    variant: f03b.LabelVariant,
) -> pd.Series:
    signal, _ = f03b.build_signal(
        pd.to_numeric(frame["future_log_return_12"], errors="coerce").astype("float64").to_numpy(),
        regime["regime"].to_numpy(),
        base_threshold,
        variant,
    )
    return pd.Series(np.where(signal == -1, 0, np.where(signal == 1, 2, 1)), index=frame.index, dtype="int64")


def evaluate_decision_grid(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    model_id: str,
    teacher_variant_id: str,
) -> pd.DataFrame:
    cash = pd.to_numeric(frame["is_us_cash_open"], errors="coerce").fillna(0).eq(1).to_numpy(dtype=bool)
    rows: list[dict[str, Any]] = []
    for side_mode in SIDE_MODES:
        for threshold in THRESHOLDS:
            for margin in MARGINS:
                raw_signal = trainable.signal_from_probabilities(
                    probabilities,
                    threshold=float(threshold),
                    margin=float(margin),
                    filter_mask=cash,
                    side_mode=side_mode,
                )
                for cooldown in COOLDOWNS:
                    signal = scout.apply_cooldown(raw_signal, int(cooldown))
                    candidate_id = (
                        f"f03e_repair__{teacher_variant_id}__{side_mode}"
                        f"__p{int(threshold * 100)}__m{int(margin * 100)}__cd{cooldown}"
                    )
                    for split in ("train", "validation", "oos"):
                        rows.append(
                            trainable.evaluate_model_split(
                                frame=frame,
                                signal=signal,
                                split=split,
                                candidate_id=candidate_id,
                                model_id=model_id,
                                teacher_candidate_id=teacher_variant_id,
                                surface="frontier03e_bounded_two_teacher_repair",
                                filter_name="all_cash",
                                side_mode=side_mode,
                                probability_threshold=float(threshold),
                                probability_margin=float(margin),
                                cooldown=int(cooldown),
                            )
                        )
    return pd.DataFrame(rows)


def model_table_row(
    model_id: str,
    model_path: Path,
    onnx_path: Path,
    parity: dict[str, Any],
    variant: f03b.LabelVariant,
    parent_row: dict[str, Any],
) -> dict[str, Any]:
    return {
        "candidate_model_id": model_id,
        "teacher_candidate_id": variant.variant_id,
        "surface": "frontier03e_bounded_two_teacher_repair",
        "filter_name": "all_cash",
        "teacher_description": variant.description,
        "teacher_validation_profit_factor": num(parent_row.get("validation_profit_factor")),
        "teacher_validation_trades_per_day": num(parent_row.get("validation_trades_per_day")),
        "teacher_validation_max_drawdown_percent": num(parent_row.get("validation_max_drawdown_percent")),
        "teacher_oos_profit_factor": num(parent_row.get("oos_profit_factor")),
        "teacher_oos_trades_per_day": num(parent_row.get("oos_trades_per_day")),
        "teacher_oos_max_drawdown_percent": num(parent_row.get("oos_max_drawdown_percent")),
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": sha256_file(onnx_path),
        "onnx_parity_passed": bool(parity["passed"]),
    }


def teacher_record(
    variant: f03b.LabelVariant,
    labels: pd.Series,
    frame: pd.DataFrame,
    parent_row: dict[str, Any],
) -> dict[str, Any]:
    train_mask = frame["split"].astype(str).eq("train")
    counts = labels.loc[train_mask].value_counts().sort_index().to_dict()
    return {
        "teacher_variant_id": variant.variant_id,
        "description": variant.description,
        "train_label_counts": {str(key): int(value) for key, value in counts.items()},
        "parent_proxy_row": json_ready(parent_row),
    }


def teacher_repair_success_mask(summary: pd.DataFrame) -> pd.Series:
    return (
        summary["onnx_parity_passed"].astype(bool)
        & summary["validation_net_profit"].gt(0)
        & summary["oos_net_profit"].gt(0)
        & summary["validation_profit_factor"].ge(1.20)
        & summary["oos_profit_factor"].ge(1.20)
        & summary["oos_trades_per_day"].ge(4.5)
        & summary["validation_max_drawdown_percent"].le(VAL_DD_CEILING)
        & summary["oos_max_drawdown_percent"].le(OOS_DD_CEILING)
    )


def teacher_repair_stop_candidate_mask(summary: pd.DataFrame) -> pd.Series:
    return summary["oos_trades_per_day"].ge(4.0) & summary["oos_profit_factor"].ge(1.15)


def teacher_repair_distance(summary: pd.DataFrame) -> pd.Series:
    validation_pf_gap = np.maximum(0.0, 1.20 - summary["validation_profit_factor"].astype(float)) / 1.20
    oos_pf_gap = np.maximum(0.0, 1.20 - summary["oos_profit_factor"].astype(float)) / 1.20
    density_gap = np.maximum(0.0, 4.5 - summary["oos_trades_per_day"].astype(float)) / 4.5
    validation_dd_gap = np.maximum(0.0, summary["validation_max_drawdown_percent"].astype(float) - VAL_DD_CEILING) / VAL_DD_CEILING
    oos_dd_gap = np.maximum(0.0, summary["oos_max_drawdown_percent"].astype(float) - OOS_DD_CEILING) / OOS_DD_CEILING
    validation_net_gap = np.where(summary["validation_net_profit"].astype(float) > 0, 0.0, 1.0)
    oos_net_gap = np.where(summary["oos_net_profit"].astype(float) > 0, 0.0, 1.0)
    return pd.Series(
        validation_pf_gap + oos_pf_gap + density_gap + validation_dd_gap + oos_dd_gap + validation_net_gap + oos_net_gap,
        index=summary.index,
    )


def rank_summary(summary: pd.DataFrame) -> pd.DataFrame:
    return summary.sort_values(
        [
            "teacher_repair_success_flag",
            "teacher_repair_stop_candidate_flag",
            "teacher_repair_distance_score",
            "oos_profit_factor",
            "oos_trades_per_day",
            "oos_max_drawdown_percent",
        ],
        ascending=[False, False, True, False, False, True],
    ).reset_index(drop=True)


def build_final(
    now: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    ranked: pd.DataFrame,
    success_rows: pd.DataFrame,
    stop_rows: pd.DataFrame,
    model_table: pd.DataFrame,
    teacher_records: list[dict[str, Any]],
) -> dict[str, Any]:
    best = ranked.iloc[0].to_dict()
    success = len(success_rows) > 0
    has_stop_clue = len(stop_rows) > 0
    if success:
        status = "completed_two_teacher_repair_precheck_eligible_no_authority"
        judgment = "precheck_eligible_after_teacher_repair_no_authority"
        next_run_id = NEXT_PRECHECK_RUN_ID
    elif has_stop_clue:
        status = "completed_two_teacher_repair_preserved_clue_needs_closeout_no_authority"
        judgment = "bounded_repair_preserved_clue_no_precheck_no_authority"
        next_run_id = NEXT_CLOSEOUT_REVIEW_RUN_ID
    else:
        status = "completed_two_teacher_repair_negative_memory_needs_closeout_no_authority"
        judgment = "bounded_repair_negative_memory_no_authority"
        next_run_id = NEXT_CLOSEOUT_REVIEW_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_label_run_id": SOURCE_LABEL_RUN_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": now,
        "next_run_id": next_run_id,
        "trained_models": int(len(model_table)),
        "teacher_variant_ids": list(TEACHER_VARIANT_IDS),
        "teacher_records": teacher_records,
        "decision_rows": int(len(ranked)),
        "teacher_repair_success_rows": int(len(success_rows)),
        "teacher_repair_stop_candidate_rows": int(len(stop_rows)),
        "best_candidate_id": str(best["candidate_id"]),
        "best_model_id": str(best["candidate_model_id"]),
        "best_teacher_variant_id": str(best["teacher_candidate_id"]),
        "best_side_mode": str(best["side_mode"]),
        "best_probability_threshold": num(best["probability_threshold"]),
        "best_probability_margin": num(best["probability_margin"]),
        "best_cooldown_bars": int(best["cooldown_bars"]),
        "best_distance_score": num(best["teacher_repair_distance_score"]),
        "best_validation_net_profit": num(best["validation_net_profit"]),
        "best_validation_profit_factor": num(best["validation_profit_factor"]),
        "best_validation_trades_per_day": num(best["validation_trades_per_day"]),
        "best_validation_max_drawdown_percent": num(best["validation_max_drawdown_percent"]),
        "best_oos_net_profit": num(best["oos_net_profit"]),
        "best_oos_profit_factor": num(best["oos_profit_factor"]),
        "best_oos_trades_per_day": num(best["oos_trades_per_day"]),
        "best_oos_max_drawdown_percent": num(best["oos_max_drawdown_percent"]),
        "model_table": json_ready(model_table.to_dict("records")),
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
    *,
    model_table: pd.DataFrame,
    classifier_rows: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    top: pd.DataFrame,
    success_rows: pd.DataFrame,
    stop_rows: pd.DataFrame,
    final: dict[str, Any],
    export_records: list[dict[str, Any]],
    parity_records: list[dict[str, Any]],
    teacher_records: list[dict[str, Any]],
) -> None:
    paths = {
        "model_training_summary": RUN_ROOT / "model_training_summary.csv",
        "classifier_metrics": RUN_ROOT / "classifier_metrics.json",
        "decision_surface_metrics": RUN_ROOT / "decision_surface_metrics.csv",
        "decision_surface_summary": RUN_ROOT / "decision_surface_summary.csv",
        "top_teacher_repair_surfaces": RUN_ROOT / "top_teacher_repair_surfaces.csv",
        "teacher_repair_success_rows": RUN_ROOT / "teacher_repair_success_rows.csv",
        "teacher_repair_stop_candidate_rows": RUN_ROOT / "teacher_repair_stop_candidate_rows.csv",
        "teacher_records": RUN_ROOT / "teacher_records.json",
        "model_export_records": RUN_ROOT / "model_export_records.json",
        "onnx_parity_audit": RUN_ROOT / "onnx_parity_audit.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    model_table.to_csv(io_path(paths["model_training_summary"]), index=False, lineterminator="\n")
    metrics.to_csv(io_path(paths["decision_surface_metrics"]), index=False, lineterminator="\n")
    summary.to_csv(io_path(paths["decision_surface_summary"]), index=False, lineterminator="\n")
    top.to_csv(io_path(paths["top_teacher_repair_surfaces"]), index=False, lineterminator="\n")
    success_rows.to_csv(io_path(paths["teacher_repair_success_rows"]), index=False, lineterminator="\n")
    stop_rows.to_csv(io_path(paths["teacher_repair_stop_candidate_rows"]), index=False, lineterminator="\n")
    f03b.write_json(paths["classifier_metrics"], {"records": classifier_rows})
    f03b.write_json(paths["teacher_records"], {"records": teacher_records})
    f03b.write_json(paths["model_export_records"], {"exports": export_records, "skipped": []})
    f03b.write_json(paths["onnx_parity_audit"], {"records": parity_records})
    f03b.write_text_sig(REPORT_PATH, report_text(final, top))
    outputs = {
        name: {"path": path.as_posix(), "sha256": sha256_file(path)}
        for name, path in paths.items()
        if name != "run_manifest"
    }
    outputs["report"] = {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)}
    outputs["onnx_models"] = [
        {"path": row["onnx_path"], "sha256": row["onnx_sha256"]} for row in model_table.to_dict("records")
    ]
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_03/frontier03e_bounded_two_teacher_density_repair.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_03/frontier03e_bounded_two_teacher_density_repair.py")),
        "inputs": {
            "parent_run_id": PARENT_RUN_ID,
            "source_label_run_id": SOURCE_LABEL_RUN_ID,
            "parent_top": PARENT_TOP.as_posix(),
            "parent_top_sha256": sha256_file(PARENT_TOP),
            "dataset_path": f03b.DATASET_PATH.as_posix(),
            "dataset_sha256": sha256_file(f03b.DATASET_PATH),
            "feature_order_path": f03b.FEATURE_ORDER_PATH.as_posix(),
            "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
        },
        "outputs": outputs,
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    f03b.write_json(paths["run_manifest"], manifest)


def report_text(final: dict[str, Any], top: pd.DataFrame) -> str:
    rows = top.head(5).to_dict("records")
    return f"""# Frontier03E Bounded Two-Teacher Repair Report(전선03E 상한 있는 두 교사 수리 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Boundary(경계)

This run(이번 실행)은 Grok(그록)의 repair_first(수리 우선) 조언 뒤에 허용된 bounded repair(상한 있는 수리)입니다. Two teacher variants(두 교사 변형) `{', '.join(TEACHER_VARIANT_IDS)}`만 새로 학습했고, WFO(워크포워드), MT5(메타트레이더5), runtime authority(런타임 권위)는 없습니다.

## Best Repair Read(최상위 수리 판독)

- candidate_id(후보 ID): `{final['best_candidate_id']}`
- teacher variant(교사 변형): `{final['best_teacher_variant_id']}`
- threshold/margin/cooldown(임계값/마진/쿨다운): `{fmt(final['best_probability_threshold'])}` / `{fmt(final['best_probability_margin'])}` / `{final['best_cooldown_bars']}`
- side mode(방향 모드): `{final['best_side_mode']}`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{fmt(final['best_validation_net_profit'])}` / `{fmt(final['best_validation_profit_factor'])}` / `{fmt(final['best_validation_trades_per_day'])}/day` / `{fmt(final['best_validation_max_drawdown_percent'])}%`
- OOS net/PF/density/DD(표본밖 순수익/수익 팩터/밀도/손실폭): `{fmt(final['best_oos_net_profit'])}` / `{fmt(final['best_oos_profit_factor'])}` / `{fmt(final['best_oos_trades_per_day'])}/day` / `{fmt(final['best_oos_max_drawdown_percent'])}%`
- success rows(성공 행): `{final['teacher_repair_success_rows']}`
- stop candidate rows(중지 후보 행): `{final['teacher_repair_stop_candidate_rows']}`

## Top Rows(상위 행)

```json
{json.dumps(json_ready(rows), ensure_ascii=False, indent=2)}
```

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 성공이면 Grok precheck review(그록 사전 점검 검토), 실패면 Grok stage closeout review(그록 단계 마감 검토)입니다. Effect(효과)는 WFO/MT5(워크포워드/메타트레이더5) 비용을 쓰기 전에 density/PF/DD(밀도/수익 팩터/손실폭) 동시 개선 여부를 닫는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def update_docs_and_state(now: str, final: dict[str, Any]) -> None:
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

Best repair surface(최상위 수리 표면): `{final['best_candidate_id']}`

Teacher repair success rows(교사 수리 성공 행): `{final['teacher_repair_success_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )
    import yaml

    state = {
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
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    f03b.write_text_sig(
        f03b.CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier03E(전선03E)는 bounded two-teacher repair(상한 있는 두 교사 수리)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{final['best_candidate_id']}` OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `{fmt(final['best_oos_profit_factor'])}` / `{fmt(final['best_oos_trades_per_day'])}/day` / `{fmt(final['best_oos_max_drawdown_percent'])}%`.

Next action(다음 행동): `{final['next_run_id']}`.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, final))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(final))
    f03b.upsert_csv(Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(final))
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: bounded two-teacher repair(상한 있는 두 교사 수리) completed(완료). Effect(효과): Grok(그록)이 허용한 repair cap(수리 상한) 안에서 ONNX density/PF/DD(온엑스 밀도/수익 팩터/손실폭)를 다시 확인했습니다.\n",
    )


def run_registry_row(now: str, final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_two_teacher_repair(상한 있는 두 교사 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"success_rows={final['teacher_repair_success_rows']};stop_rows={final['teacher_repair_stop_candidate_rows']};no_authority",
        "work_family": "model_validation(모델 검증)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["decision_rows"]),
        "claim_boundary": "bounded_teacher_repair_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__teacher_repair",
        "subrun_id": f"{RUN_ID}__teacher_repair",
        "record_view": "teacher_repair(교사 수리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_proxy_no_mt5(파이썬 프록시, MT5 없음)",
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "two_teachers_only_no_wfo_no_mt5_no_authority(두 교사만, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": SOURCE_LABEL_RUN_ID,
        "artifact_path": (RUN_ROOT / "decision_surface_summary.csv").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "bounded_python_teacher_repair_only(상한 있는 파이썬 교사 수리 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can two additional Frontier03B teachers repair ONNX density/PF/DD jointly?(두 추가 전선03B 교사가 온엑스 밀도/수익 팩터/손실폭을 함께 수리할 수 있는가?)",
        "skill_family": "model_validation(모델 검증)",
        "lineage_summary": "frontier03b_label_proxy_to_frontier03e_two_teacher_onnx_repair(전선03B 라벨 프록시에서 전선03E 두 교사 온엑스 수리)",
    }


def ledger_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__teacher_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__teacher_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "teacher_repair(교사 수리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_proxy_no_mt5(파이썬 프록시, MT5 없음)",
        "scoreboard_lane": "bounded_two_teacher_repair(상한 있는 두 교사 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "two_teachers_only_no_wfo_no_mt5_no_authority(두 교사만, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "notes": f"success_rows={final['teacher_repair_success_rows']};stop_rows={final['teacher_repair_stop_candidate_rows']};next={final['next_run_id']};no_authority",
    }


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
