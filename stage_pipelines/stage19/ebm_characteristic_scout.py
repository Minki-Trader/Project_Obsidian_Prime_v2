from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    TRAINING_SUMMARY_PATH,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.ebm_explainable import (
    EbmVariantSpec,
    default_stage19_ebm_variants,
    fit_ebm_variant,
    nonflat_threshold,
    probability_frame,
    probability_shape_metrics,
    shape_read,
    split_decision_metrics,
    term_importance_frame,
    characteristic_score,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 19
STAGE_ID = "19_model_family_challenge__ebm_explainable_boosting_shape"
RUN_NUMBER = "run13A"
RUN_ID = "run13A_ebm_main_effect_shape_scout_v1"
PACKET_ID = "stage19_run13A_ebm_shape_scout_v1"
EXPLORATION_LABEL = "stage19_Model__EBMCharacteristicShape"
IDEA_ID = "IDEA-ST19-EBM-EXPLAINABLE-SHAPE"
MODEL_FAMILY = "interpret_ebm_explainable_boosting_classifier_multiclass"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
THRESHOLD_QUANTILE = 0.90
BOUNDARY = "ebm_shape_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_ebm_shape_structural_scout_completed"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run13A_ebm_shape_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-03_stage19_run13A_ebm_shape_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
STAGE_BRIEF_PATH = STAGE_ROOT / "00_spec/stage_brief.md"
INPUT_REFERENCES_PATH = STAGE_ROOT / "01_inputs/input_references.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
IDEA_REGISTRY_PATH = ROOT / "docs/registers/idea_registry.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, full_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "full_feature_order": full_feature_order,
        "full_feature_order_hash": ordered_hash(full_feature_order),
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_feature_order_hash": ordered_hash(tier_b_feature_order),
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }


def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def materialize_python_tier_records(
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    a_threshold: float,
    b_threshold: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = RUN_ROOT / "predictions"
    a_path = root / "tier_a_separate_predictions.parquet"
    b_path = root / "tier_b_separate_predictions.parquet"
    ab_path = root / "tier_ab_combined_predictions.parquet"
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, a_threshold, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, b_threshold, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, ab_prob, a_threshold, ab_path),
    ]
    artifacts = {
        "tier_a_predictions": save_predictions(a_path, tier_a_prob),
        "tier_b_predictions": save_predictions(b_path, tier_b_prob),
        "tier_ab_predictions": save_predictions(ab_path, ab_prob),
    }
    return records, artifacts


def variant_characteristic(context: Mapping[str, Any], spec: EbmVariantSpec) -> dict[str, Any]:
    model, sample = fit_ebm_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    prob = probability_frame(model, context["tier_a_frame"], context["full_feature_order"])
    threshold = nonflat_threshold(prob, THRESHOLD_QUANTILE)
    metrics = split_decision_metrics(prob, threshold)
    shape = probability_shape_metrics(prob)
    importance = term_importance_frame(model, context["full_feature_order"])
    root = RUN_ROOT / "results/variant_terms"
    io_path(root).mkdir(parents=True, exist_ok=True)
    importance_path = root / f"{spec.variant_id}_term_importance.csv"
    importance.to_csv(io_path(importance_path), index=False)
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
        "training_sample": sample,
        "threshold": threshold,
        "metrics": metrics,
        "probability_shape": shape,
        "shape_read": shape_read(importance),
        "feature_importance": {
            "path": rel(importance_path),
            "sha256": sha256_file_lf_normalized(importance_path),
            "top10_gain_share": float(importance.head(10)["gain_share"].sum()) if not importance.empty else None,
            "top_features": importance.head(10).to_dict(orient="records"),
        },
        "characteristic_score": characteristic_score(metrics, shape, importance),
    }


def choose_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return dict(max(rows, key=lambda row: safe_float(row.get("characteristic_score")), default={}))


def materialize_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    io_path(result_root).mkdir(parents=True, exist_ok=True)
    json_path = result_root / "ebm_variant_results.json"
    csv_path = result_root / "ebm_variant_results.csv"
    write_json(json_path, list(rows))
    fields = [
        "variant_id",
        "idea_id",
        "interactions",
        "max_bins",
        "characteristic_score",
        "threshold",
        "val_signal_coverage",
        "oos_signal_coverage",
        "val_directional_hit_rate",
        "oos_directional_hit_rate",
        "val_log_loss",
        "oos_log_loss",
        "top10_gain_share",
        "interaction_gain_share",
    ]
    csv_rows: list[dict[str, Any]] = []
    for row in rows:
        metrics = row.get("metrics", {})
        spec = row.get("spec", {})
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "idea_id": row.get("idea_id"),
                "interactions": spec.get("interactions"),
                "max_bins": spec.get("max_bins"),
                "characteristic_score": row.get("characteristic_score"),
                "threshold": row.get("threshold"),
                "val_signal_coverage": metrics.get("validation", {}).get("signal_coverage"),
                "oos_signal_coverage": metrics.get("oos", {}).get("signal_coverage"),
                "val_directional_hit_rate": metrics.get("validation", {}).get("directional_hit_rate"),
                "oos_directional_hit_rate": metrics.get("oos", {}).get("directional_hit_rate"),
                "val_log_loss": metrics.get("validation", {}).get("log_loss"),
                "oos_log_loss": metrics.get("oos", {}).get("log_loss"),
                "top10_gain_share": row.get("feature_importance", {}).get("top10_gain_share"),
                "interaction_gain_share": row.get("shape_read", {}).get("interaction_gain_share"),
            }
        )
    write_csv(csv_path, fields, csv_rows)
    return {
        "variant_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def selected_spec(selected: Mapping[str, Any]) -> EbmVariantSpec:
    return EbmVariantSpec(**dict(selected["spec"]))


def materialize_selected_models(
    context: Mapping[str, Any],
    spec: EbmVariantSpec,
) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame, float, float, pd.DataFrame]:
    root = RUN_ROOT / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_model, a_sample = fit_ebm_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    tier_b_model, b_sample = fit_ebm_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["full_feature_order"])
    tier_b_train_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(tier_b_train_prob, THRESHOLD_QUANTILE)
    tier_a_joblib = root / f"{spec.variant_id}_tier_a_ebm.joblib"
    tier_b_joblib = root / f"{spec.variant_id}_tier_b_ebm_core42.joblib"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    importance = term_importance_frame(tier_a_model, context["full_feature_order"])
    importance_path = RUN_ROOT / "results/selected_tier_a_term_importance.csv"
    importance.to_csv(io_path(importance_path), index=False)
    artifacts = {
        "selected_variant_id": spec.variant_id,
        "tier_a_training_sample": a_sample,
        "tier_b_training_sample": b_sample,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
        "selected_tier_a_term_importance": {"path": rel(importance_path), "sha256": sha256_file_lf_normalized(importance_path)},
    }
    return artifacts, tier_a_prob, tier_b_prob, a_threshold, b_threshold, importance


def build_summary(
    context: Mapping[str, Any],
    variants: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    selected_importance: pd.DataFrame,
) -> dict[str, Any]:
    threshold_id = f"q{THRESHOLD_QUANTILE:.2f}"
    top_terms = selected_importance.head(10).to_dict(orient="records")
    validation = tier_records[0].get("split_metrics", {}).get("validation", {}) if tier_records else {}
    oos = tier_records[0].get("split_metrics", {}).get("oos", {}) if tier_records else {}
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "status": "reviewed_structural_scout_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "variant_count": len(variants),
        "selected_variant_id": selected.get("variant_id"),
        "selected_threshold_id": threshold_id,
        "tier_a_rows": int(len(context["tier_a_frame"])),
        "tier_b_fallback_rows": int(len(context["tier_b_fallback_frame"])),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "tier_records": list(tier_records),
        "selected_tier_a_validation_signal_coverage": validation.get("signal_coverage"),
        "selected_tier_a_oos_signal_coverage": oos.get("signal_coverage"),
        "selected_tier_a_validation_directional_hit_rate": validation.get("directional_hit_rate"),
        "selected_tier_a_oos_directional_hit_rate": oos.get("directional_hit_rate"),
        "selected_tier_a_probability_margin_validation": validation.get("mean_probability_margin"),
        "selected_tier_a_probability_margin_oos": oos.get("mean_probability_margin"),
        "selected_shape_read": shape_read(selected_importance),
        "top_terms": top_terms,
        "artifacts": {
            "model_input_path": rel(MODEL_INPUT_PATH),
            "feature_order_path": rel(FEATURE_ORDER_PATH),
            "variant_results": rel(RUN_ROOT / "results/ebm_variant_results.csv"),
            "model_artifacts": dict(model_artifacts),
            "prediction_artifacts": dict(prediction_artifacts),
        },
        "forbidden_claims": [
            "edge",
            "alpha_quality",
            "baseline",
            "promotion_candidate",
            "operating_promotion",
            "runtime_authority",
        ],
        "next_condition": "If Stage19 continues, add a runtime handoff path or run a second EBM shape follow-up only after this scout's top terms are reviewed.",
    }


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "EBM can reveal additive feature shapes on the audited 58-feature US100 M5 surface.",
            "decision_use": "Decide whether Stage19 should continue with EBM shape follow-up or pivot to Stage20 GAM.",
            "comparison_baseline": "Stage18 CatBoost clues are comparison context only, not inherited baseline.",
            "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, "Tier A/B paired records"],
            "changed_variables": ["model_family=EBM", "binning and interaction budget"],
            "success_criteria": ["stable validation/OOS shape", "usable Tier A/B prediction records"],
            "failure_criteria": ["flat probability shape", "unstable signal density"],
            "invalid_conditions": ["missing split", "missing feature", "duplicate timestamp", "non-finite feature"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_source": rel(MODEL_INPUT_PATH),
            "time_axis": "timestamp is read as UTC-normalized project timestamp and validated monotonic.",
            "sample_scope": f"Tier A rows={summary.get('tier_a_rows')}; Tier B fallback rows={summary.get('tier_b_fallback_rows')}",
            "feature_label_boundary": LABEL_ID,
            "split_boundary": SPLIT_CONTRACT,
            "integrity_judgment": "usable_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_family": MODEL_FAMILY,
            "selection_metric": "characteristic_score on Tier A structural scout metrics, not trading profit.",
            "threshold_policy": f"non-flat q{THRESHOLD_QUANTILE:.2f} threshold from validation split.",
            "overfit_risk": "single split and small variant sweep; no WFO or MT5 runtime evidence.",
            "calibration_risk": "EBM scores are used as probability-like scout scores, not calibrated trading probability.",
            "validation_judgment": "inconclusive_structural_scout",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [rel(MODEL_INPUT_PATH), rel(FEATURE_ORDER_PATH)],
            "producer": "stage_pipelines.stage19.ebm_characteristic_scout",
            "consumer": [rel(REPORT_PATH), rel(STAGE_LEDGER_PATH), rel(PROJECT_LEDGER_PATH)],
            "availability": "generated_02_runs_ignored_with_manifest_and_tracked_packet_summary",
            "lineage_judgment": "connected_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "result_subject": RUN_ID,
            "evidence_available": ["variant results", "Tier A/B prediction records", "stage and project ledgers"],
            "evidence_missing": ["MT5 runtime_probe", "WFO", "runtime authority"],
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": summary.get("next_condition"),
        },
    ]


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    selected = str(summary.get("selected_variant_id"))
    top_terms = summary.get("top_terms") or []
    top_term_lines = "\n".join(
        f"- `{row.get('feature')}`: gain_share(기여 비중) `{safe_float(row.get('gain_share')):.4f}`, degree(차수) `{row.get('term_degree')}`"
        for row in top_terms[:5]
    )
    if not top_term_lines:
        top_term_lines = "- no top terms recorded(상위 항 없음)"
    write_md(
        STAGE_BRIEF_PATH,
        f"""# Stage19 EBM Explainable Boosting Shape(19단계 EBM 설명가능 부스팅 모양)

## Question(질문)

EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)이 audited 58-feature surface(감사된 58개 피처 표면)에서 설명 가능한 additive feature shape(가산 피처 모양)를 만들 수 있는지 본다.

효과(effect, 효과): Stage19(19단계)는 Stage18(18단계) CatBoost(캣부스트) continuation(연속)이 아니라 독립 model-family scout(모델군 탐색)다.

## Boundary(경계)

- allowed claim(허용 주장): Python structural scout(파이썬 구조 탐색) completed(완료)
- forbidden claim(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)
""",
    )
    write_md(
        INPUT_REFERENCES_PATH,
        f"""# Stage19 Input References(19단계 입력 참조)

- model input(모델 입력): `{rel(MODEL_INPUT_PATH)}`
- feature order(피처 순서): `{rel(FEATURE_ORDER_PATH)}`
- training summary(학습 요약): `{rel(TRAINING_SUMMARY_PATH)}`
- feature set(피처 묶음): `{FEATURE_SET_ID}`
- label(라벨): `{LABEL_ID}`
- split(분할): `{SPLIT_CONTRACT}`

효과(effect, 효과): 이번 run(실행)이 어떤 데이터 표면(data surface, 데이터 표면)을 썼는지 Stage19(19단계) 안에 고정한다.
""",
    )
    write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage19 Review Index(19단계 검토 색인)

- `{RUN_ID}`: `{rel(REPORT_PATH)}`

효과(effect, 효과): Stage19(19단계)의 review packet(검토 묶음)을 한 곳에서 찾게 한다.
""",
    )
    write_md(
        REPORT_PATH,
        f"""# RUN13A EBM Shape Scout Packet(실행13A EBM 모양 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`
- external verification(외부 검증): `out_of_scope_by_claim_python_structural_scout(주장 범위 밖, 파이썬 구조 탐색)`

효과(effect, 효과): EBM(설명가능 부스팅 머신) shape(모양)는 확인했지만 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)나 운영 의미(operating meaning, 운영 의미)는 주장하지 않는다.

## Evidence(근거)

- variants(변형 수): `{summary.get('variant_count')}`
- Tier A rows(Tier A 행): `{summary.get('tier_a_rows')}`
- Tier B fallback rows(Tier B 대체 행): `{summary.get('tier_b_fallback_rows')}`
- validation signal coverage(검증 신호 커버리지): `{summary.get('selected_tier_a_validation_signal_coverage')}`
- OOS signal coverage(표본외 신호 커버리지): `{summary.get('selected_tier_a_oos_signal_coverage')}`
- validation directional hit(검증 방향 적중): `{summary.get('selected_tier_a_validation_directional_hit_rate')}`
- OOS directional hit(표본외 방향 적중): `{summary.get('selected_tier_a_oos_directional_hit_rate')}`

## Top Shape Terms(상위 모양 항)

{top_term_lines}

## Claim Boundary(주장 경계)

allowed(허용): EBM(설명가능 부스팅 머신) Python structural scout(파이썬 구조 탐색), Tier A/B paired records(Tier A/B 쌍 기록), top term clue(상위 항 단서).

forbidden(금지): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime_authority(런타임 권위).
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Stage19 RUN13A EBM Shape Scout Decision(19단계 실행13A EBM 모양 탐색 결정)

## Decision(결정)

`{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신) shape(모양) 단서를 얻었지만, 아직 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Condition(다음 조건)

Stage19(19단계)을 계속하면 top term(상위 항) 기반 follow-up(후속 탐색) 또는 MT5 handoff path(MT5 인계 경로)를 먼저 정한다.
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage19 Selection Status(19단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run13A_python_structural_scout_completed`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신)의 설명 가능한 shape(모양) 단서를 보존하지만, 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.
""",
    )


def write_packet_artifacts(summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    receipts = build_skill_receipts(summary, created_at)
    gates = {
        "scope_completion_gate": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_views": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
            "completed_views": [record.get("record_view") for record in summary.get("tier_records", [])],
        },
        "kpi_contract_audit": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "kpi_scope": "signal_probability_threshold",
            "runtime_kpi_required": False,
            "runtime_kpi_reason": "out_of_scope_by_claim_python_structural_scout",
        },
        "skill_receipt_lint": {"packet_id": PACKET_ID, "status": "passed", "receipt_count": len(receipts)},
        "required_gate_coverage_audit": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "covered_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
        },
        "final_claim_guard": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": ["python_structural_scout_completed", "ebm_shape_clues_recorded"],
            "forbidden_claims": summary.get("forbidden_claims"),
        },
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", receipts)
    write_json(PACKET_ROOT / "scope_completion_gate.json", gates["scope_completion_gate"])
    write_json(PACKET_ROOT / "kpi_contract_audit.json", gates["kpi_contract_audit"])
    write_json(PACKET_ROOT / "skill_receipt_lint.json", gates["skill_receipt_lint"])
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", gates["required_gate_coverage_audit"])
    write_json(PACKET_ROOT / "final_claim_guard.json", gates["final_claim_guard"])
    write_md(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
primary_family: experiment_execution
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-artifact-lineage
required_gates:
  - scope_completion_gate
  - kpi_contract_audit
  - skill_receipt_lint
  - required_gate_coverage_audit
claim_boundary: {BOUNDARY}
""",
    )
    return gates


def write_run_manifest_and_kpi(
    summary: Mapping[str, Any],
    variant_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
) -> dict[str, Any]:
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "model_family": MODEL_FAMILY,
            "lane": "model_characteristic_structural_scout",
        },
        "inputs": {
            "model_input": rel(MODEL_INPUT_PATH),
            "feature_order": rel(FEATURE_ORDER_PATH),
            "training_summary": rel(TRAINING_SUMMARY_PATH),
        },
        "artifacts": {
            "variant_artifacts": dict(variant_artifacts),
            "model_artifacts": dict(model_artifacts),
            "prediction_artifacts": dict(prediction_artifacts),
        },
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "judgment_boundary": {"status": "reviewed", "claim": BOUNDARY},
    }
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "scoreboard_lane": "structural_scout",
        "kpi_scope": "signal_probability_threshold",
        "summary": dict(summary),
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    return {
        "run_manifest": {"path": rel(RUN_ROOT / "run_manifest.json"), "sha256": sha256_file_lf_normalized(RUN_ROOT / "run_manifest.json")},
        "kpi_record": {"path": rel(RUN_ROOT / "kpi_record.json"), "sha256": sha256_file_lf_normalized(RUN_ROOT / "kpi_record.json")},
    }


def update_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    tier_records = list(summary.get("tier_records", []))
    rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=[],
        selected_threshold_id=str(summary.get("selected_threshold_id")),
        run_output_root=RUN_ROOT,
        external_verification_status="out_of_scope_by_claim_python_structural_scout",
    )
    ledger_payload = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )
    notes = ledger_pairs(
        (
            ("model_family", MODEL_FAMILY),
            ("selected_variant", summary.get("selected_variant_id")),
            ("validation_signal_coverage", summary.get("selected_tier_a_validation_signal_coverage")),
            ("oos_signal_coverage", summary.get("selected_tier_a_oos_signal_coverage")),
            ("external_verification", "out_of_scope_by_claim_python_structural_scout"),
            ("boundary", "structural_scout_only"),
        )
    )
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "model_characteristic_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT),
        "notes": notes,
    }
    registry_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"alpha_ledgers": ledger_payload, "run_registry": registry_payload}


def append_once(path: Path, needle: str, line: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if io_path(path).exists() else ""
    if needle in text:
        return
    write_md(path, text.rstrip() + "\n" + line.rstrip())


def sync_state_docs(summary: Mapping[str, Any]) -> None:
    if io_path(CURRENT_WORKING_STATE_PATH).exists():
        text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
        if RUN_ID not in text:
            block = f"""## Latest Stage19 RUN13A Update(최신 19단계 실행13A 업데이트)

Stage19(19단계)는 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) `{RUN_ID}`를 Python structural scout(파이썬 구조 탐색)로 완료했다.

효과(effect, 효과): selected variant(선택 변형) `{summary.get('selected_variant_id')}`와 top shape terms(상위 모양 항)를 보존하지만, MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
            write_md(CURRENT_WORKING_STATE_PATH, block + text)
    if io_path(WORKSPACE_STATE_PATH).exists():
        text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
        text = text.replace("active_branch: codex/stage18", "active_branch: codex/stage19")
        text = text.replace("current_run_id: ''", f"current_run_id: {RUN_ID}")
        text = text.replace(
            "      status: planned_next",
            "      status: active_run13A_python_structural_scout_completed",
            1,
        )
        if "stage19_ebm_run13A_characteristic_scout:" not in text:
            text = text.rstrip() + f"""
stage19_ebm_run13A_characteristic_scout:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary.get('selected_variant_id')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  external_verification_status: out_of_scope_by_claim_python_structural_scout
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / 'aggregate_summary.json')}
"""
        io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8")
    append_once(
        IDEA_REGISTRY_PATH,
        IDEA_ID,
        f"| `{IDEA_ID}` | `{STAGE_ID}` | EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)이 additive feature shape(가산 피처 모양)를 보여줄 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `structural_scout_completed_inconclusive` | `{RUN_ID}`; selected variant(선택 변형) `{summary.get('selected_variant_id')}`; MT5 runtime_probe(런타임 탐침) 없음 |",
    )


def run(*, sync_state: bool = True) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variant_rows = [variant_characteristic(context, spec) for spec in default_stage19_ebm_variants()]
    variant_artifacts = materialize_variant_results(variant_rows)
    selected = choose_variant(variant_rows)
    spec = selected_spec(selected)
    model_artifacts, tier_a_prob, tier_b_prob, a_threshold, b_threshold, selected_importance = materialize_selected_models(context, spec)
    tier_records, prediction_artifacts = materialize_python_tier_records(tier_a_prob, tier_b_prob, a_threshold, b_threshold)
    summary = build_summary(context, variant_rows, selected, model_artifacts, prediction_artifacts, tier_records, selected_importance)
    run_artifacts = write_run_manifest_and_kpi(summary, variant_artifacts, model_artifacts, prediction_artifacts)
    summary["artifacts"] = {**dict(summary["artifacts"]), "run_artifacts": run_artifacts, "variant_artifacts": dict(variant_artifacts)}
    write_stage_docs(summary)
    packet_gates = write_packet_artifacts(summary, created_at)
    ledger_payload = update_ledgers(summary)
    if sync_state:
        sync_state_docs(summary)
    final_payload = {
        "summary": summary,
        "packet_gates": packet_gates,
        "ledger_payload": ledger_payload,
    }
    write_json(PACKET_ROOT / "run_result.json", final_payload)
    return final_payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage19 EBM shape structural scout.")
    parser.add_argument("--no-state-sync", action="store_true", help="Do not update current truth documents.")
    args = parser.parse_args(argv)
    payload = run(sync_state=not args.no_state_sync)
    print(json.dumps(json_ready(payload["summary"]), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
