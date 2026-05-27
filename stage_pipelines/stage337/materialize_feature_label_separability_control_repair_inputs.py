from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)
from stage_pipelines.stage337.train_guarded_directional_label_action_candidates import (  # noqa: E402
    CANDIDATE_INPUT_MANIFEST,
    SOURCE_MODEL_INPUT,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CV"
RUN_ID = "run337CV_materialize_feature_label_separability_control_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337CU_design_feature_label_separability_control_repair_without_db_v1"
NEXT_RUN_ID = "run337CW_train_feature_label_separability_control_repaired_candidates_without_db_v1"
STATUS = "completed_stage337CV_feature_label_separability_control_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "separability_control_inputs_materialized_ready_for_guarded_training"
DECISION = "stage337CV_open_run337CW_train_feature_label_separability_control_repaired_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CV_feature_label_separability_control_repair_inputs_without_db_"
    "train_only_label_thresholds_validation_oos_readonly_no_model_training_no_threshold_tuning_"
    "no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CV_separability_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CV_feature_label_separability_control_repair_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CU_DIR = STAGE_DIR / "02_runs" / "run337CU"
CU_FINAL = CU_DIR / "final_decision.json"
CU_GATES = CU_DIR / "required_gate_coverage_audit.csv"
CU_SEPARABILITY_DESIGN = CU_DIR / "feature_label_separability_repair_design.csv"
CU_CONTROL_PLAN = CU_DIR / "control_orthogonalization_plan.csv"
CU_MODEL_PLAN = CU_DIR / "model_family_loss_probe_plan.csv"
CU_FIREWALLS = CU_DIR / "density_only_and_oos_selection_firewall.csv"
CU_CV_QUEUE = CU_DIR / "run337CV_materialization_queue.csv"
CN_PURGED_MEMBERSHIP = STAGE_DIR / "02_runs" / "run337CN" / "purged_embargo_split_membership.parquet"
CR_FEATURE_STATE = STAGE_DIR / "02_runs" / "run337CR" / "feature_state_carry_matrix.csv"
CR_DAY_CONCENTRATION = STAGE_DIR / "02_runs" / "run337CR" / "day_block_concentration_matrix.csv"
CS_SCORECARD = STAGE_DIR / "02_runs" / "run337CS" / "repaired_model_scorecard.csv"
CS_CONTROLS = STAGE_DIR / "02_runs" / "run337CS" / "extended_control_scorecard.csv"

LABEL_MARGIN_FRAME = RUN_DIR / "label_margin_candidate_frame.parquet"
LABEL_MARGIN_CONTRACT = RUN_DIR / "label_margin_contract.csv"
TWO_STAGE_LABEL_CONTRACT = RUN_DIR / "two_stage_label_contract.csv"
TWO_STAGE_TRAINING_TASK_MATRIX = RUN_DIR / "two_stage_training_task_matrix.csv"
CONTROL_ORTHOGONAL_FEATURE_SETS = RUN_DIR / "control_orthogonal_feature_sets.csv"
EXTENDED_CONTROL_CONTRACT = RUN_DIR / "extended_control_contract.csv"
TINY_MODEL_PROBE_TASK_MATRIX = RUN_DIR / "tiny_model_probe_task_matrix.csv"
SEPARABILITY_DIAGNOSTIC = RUN_DIR / "feature_label_separability_diagnostic.csv"
CW_QUEUE = RUN_DIR / "run337CW_guarded_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CU_FINAL,
    CU_GATES,
    CU_SEPARABILITY_DESIGN,
    CU_CONTROL_PLAN,
    CU_MODEL_PLAN,
    CU_FIREWALLS,
    CU_CV_QUEUE,
    CN_PURGED_MEMBERSHIP,
    CR_FEATURE_STATE,
    CR_DAY_CONCENTRATION,
    CS_SCORECARD,
    CS_CONTROLS,
    SOURCE_MODEL_INPUT,
    CANDIDATE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    LABEL_MARGIN_FRAME,
    LABEL_MARGIN_CONTRACT,
    TWO_STAGE_LABEL_CONTRACT,
    TWO_STAGE_TRAINING_TASK_MATRIX,
    CONTROL_ORTHOGONAL_FEATURE_SETS,
    EXTENDED_CONTROL_CONTRACT,
    TINY_MODEL_PROBE_TASK_MATRIX,
    SEPARABILITY_DIAGNOSTIC,
    CW_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    EXPERIMENT_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

LABEL_MARGIN_COLUMNS = (
    "source_row_id",
    "timestamp",
    "split",
    "contract_id",
    "margin_policy_id",
    "label_candidate_id",
    "margin_quantile",
    "train_only_margin_threshold",
    "future_log_return_12",
    "volatility_proxy",
    "volnorm_future_return_12",
    "abs_volnorm_future_return_12",
    "label_class",
    "label_name",
    "usable_for_training",
    "usable_for_validation",
    "usable_for_oos",
    "threshold_source",
    "claim_boundary",
)
LABEL_CONTRACT_COLUMNS = (
    "label_candidate_id",
    "contract_id",
    "margin_policy_id",
    "margin_quantile",
    "train_only_margin_threshold",
    "train_rows",
    "validation_rows",
    "oos_rows",
    "train_short",
    "train_flat",
    "train_long",
    "validation_nonflat_rate",
    "oos_nonflat_rate",
    "threshold_source",
    "validation_oos_role",
    "forbidden_action",
    "claim_boundary",
)
TWO_STAGE_CONTRACT_COLUMNS = (
    "two_stage_label_id",
    "contract_id",
    "margin_policy_id",
    "stage1_target",
    "stage2_target",
    "train_only_margin_threshold",
    "train_nonflat_rate",
    "validation_nonflat_rate",
    "oos_nonflat_rate",
    "direction_rows_train",
    "direction_rows_validation",
    "direction_rows_oos",
    "validation_oos_role",
    "forbidden_action",
    "claim_boundary",
)
TWO_STAGE_TASK_COLUMNS = (
    "task_id",
    "contract_id",
    "margin_policy_id",
    "stage",
    "target",
    "required_input",
    "train_rows",
    "validation_rows_readonly",
    "oos_rows_readonly",
    "selection_use",
    "blocked_if",
    "claim_boundary",
)
FEATURE_SET_COLUMNS = (
    "feature_set_id",
    "feature_set_role",
    "source_feature_count",
    "included_feature_count",
    "dropped_feature_count",
    "dropped_feature_rule",
    "included_features_json",
    "dropped_features_json",
    "feature_order_hash",
    "source_artifact",
    "claim_boundary",
)
CONTROL_CONTRACT_COLUMNS = (
    "control_contract_id",
    "control_id",
    "control_family",
    "split",
    "observed_rows",
    "observed_block_rows",
    "worst_control_minus_actual",
    "required_contract",
    "pass_condition",
    "blocks_runtime_probe",
    "forbidden_action",
    "source_artifact",
    "claim_boundary",
)
TINY_TASK_COLUMNS = (
    "task_id",
    "probe_id",
    "model_config_id",
    "contract_id",
    "label_candidate_id",
    "feature_set_id",
    "target_mode",
    "model_family",
    "allowed_size",
    "required_inputs",
    "validation_oos_role",
    "selection_use",
    "forbidden_action",
    "claim_boundary",
)
DIAGNOSTIC_COLUMNS = (
    "label_candidate_id",
    "contract_id",
    "margin_policy_id",
    "split",
    "rows",
    "short_rows",
    "flat_rows",
    "long_rows",
    "nonflat_rate",
    "long_share_of_nonflat",
    "class_entropy",
    "diagnostic_role",
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
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")

LABEL_QUANTILES = (0.60, 0.70)
LABEL_NAMES = {0: "short", 1: "flat", 2: "long"}


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def feature_order_hash(features: Sequence[str]) -> str:
    payload = json.dumps(list(features), ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_parquet(path: Path, frame: pd.DataFrame) -> Path:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return path


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def volatility_proxy(frame: pd.DataFrame) -> pd.Series:
    if "historical_vol_20" in frame.columns:
        proxy = pd.to_numeric(frame["historical_vol_20"], errors="coerce").abs()
    else:
        proxy = pd.to_numeric(frame["log_return_1"], errors="coerce").abs().rolling(20, min_periods=5).std()
    positive = proxy.replace([np.inf, -np.inf], np.nan)
    floor = float(positive[positive > 0].median()) if (positive > 0).any() else 1.0
    return positive.fillna(floor).clip(lower=max(floor * 0.05, 1e-8))


def split_count(rows: pd.DataFrame, mask_column: str) -> int:
    return int(rows[mask_column].fillna(False).astype(bool).sum())


def build_label_margin_inputs(
    frame: pd.DataFrame, membership: pd.DataFrame
) -> tuple[pd.DataFrame, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    base = frame[
        ["source_row_id", "timestamp", "split", "future_log_return_12", "historical_vol_20"]
    ].copy()
    base["volatility_proxy"] = volatility_proxy(frame)
    base["volnorm_future_return_12"] = pd.to_numeric(base["future_log_return_12"], errors="coerce") / base["volatility_proxy"]
    base["abs_volnorm_future_return_12"] = base["volnorm_future_return_12"].abs()

    label_frames: list[pd.DataFrame] = []
    contract_rows: list[dict[str, Any]] = []
    two_stage_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []

    contracts = sorted(str(item) for item in membership["contract_id"].dropna().unique())
    for contract_id in contracts:
        member = membership.loc[membership["contract_id"].astype(str) == contract_id].copy()
        member = member[
            [
                "source_row_id",
                "usable_for_training",
                "usable_for_validation",
                "usable_for_oos",
            ]
        ]
        merged = base.merge(member, on="source_row_id", how="inner")
        train_values = merged.loc[
            merged["usable_for_training"].fillna(False).astype(bool), "abs_volnorm_future_return_12"
        ].dropna()
        for quantile in LABEL_QUANTILES:
            threshold = float(train_values.quantile(quantile))
            suffix = f"q{int(round(quantile * 100))}"
            margin_policy_id = f"volnorm_margin_{suffix}_train_only"
            label_candidate_id = f"label_v4_{margin_policy_id}"
            labeled = merged.copy()
            labeled["contract_id"] = contract_id
            labeled["margin_policy_id"] = margin_policy_id
            labeled["label_candidate_id"] = label_candidate_id
            labeled["margin_quantile"] = quantile
            labeled["train_only_margin_threshold"] = threshold
            labeled["label_class"] = np.where(
                labeled["abs_volnorm_future_return_12"] < threshold,
                1,
                np.where(labeled["future_log_return_12"] < 0, 0, 2),
            ).astype(int)
            labeled["label_name"] = labeled["label_class"].map(LABEL_NAMES)
            labeled["threshold_source"] = "train_split_only_purged_usable(학습 분할 전용 제거 사용 가능 행)"
            labeled["claim_boundary"] = CLAIM_BOUNDARY
            label_frames.append(labeled[list(LABEL_MARGIN_COLUMNS)])

            def usable(mask_column: str) -> pd.DataFrame:
                return labeled.loc[labeled[mask_column].fillna(False).astype(bool)]

            train = usable("usable_for_training")
            validation = usable("usable_for_validation")
            oos = usable("usable_for_oos")
            train_counts = train["label_class"].value_counts().to_dict()
            contract_rows.append(
                {
                    "label_candidate_id": label_candidate_id,
                    "contract_id": contract_id,
                    "margin_policy_id": margin_policy_id,
                    "margin_quantile": quantile,
                    "train_only_margin_threshold": threshold,
                    "train_rows": len(train),
                    "validation_rows": len(validation),
                    "oos_rows": len(oos),
                    "train_short": int(train_counts.get(0, 0)),
                    "train_flat": int(train_counts.get(1, 0)),
                    "train_long": int(train_counts.get(2, 0)),
                    "validation_nonflat_rate": float((validation["label_class"] != 1).mean()) if len(validation) else 0.0,
                    "oos_nonflat_rate": float((oos["label_class"] != 1).mean()) if len(oos) else 0.0,
                    "threshold_source": "train_only(학습 전용)",
                    "validation_oos_role": "read_only_diagnostic(읽기 전용 진단)",
                    "forbidden_action": "no_validation_oos_threshold_tuning(검증/OOS 임계값 조정 금지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            two_stage_label_id = f"two_stage_nonflat_direction_{margin_policy_id}__{contract_id}"
            two_stage_rows.append(
                {
                    "two_stage_label_id": two_stage_label_id,
                    "contract_id": contract_id,
                    "margin_policy_id": margin_policy_id,
                    "stage1_target": "is_nonflat(abs_volnorm_future_return_12 >= train_threshold)(비횡보 여부)",
                    "stage2_target": "direction_when_nonflat(short_vs_long)(비횡보일 때 방향)",
                    "train_only_margin_threshold": threshold,
                    "train_nonflat_rate": float((train["label_class"] != 1).mean()) if len(train) else 0.0,
                    "validation_nonflat_rate": float((validation["label_class"] != 1).mean()) if len(validation) else 0.0,
                    "oos_nonflat_rate": float((oos["label_class"] != 1).mean()) if len(oos) else 0.0,
                    "direction_rows_train": int((train["label_class"] != 1).sum()),
                    "direction_rows_validation": int((validation["label_class"] != 1).sum()),
                    "direction_rows_oos": int((oos["label_class"] != 1).sum()),
                    "validation_oos_role": "read_only_joint_gate(읽기 전용 결합 게이트)",
                    "forbidden_action": "no_oos_stage_choice(OOS 단계 선택 금지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            for split, split_rows in (("train", train), ("validation", validation), ("oos", oos)):
                counts = split_rows["label_class"].value_counts().to_dict()
                total = int(len(split_rows))
                probs = np.array([counts.get(0, 0), counts.get(1, 0), counts.get(2, 0)], dtype=float)
                probs = probs / probs.sum() if probs.sum() else probs
                entropy = float(-np.sum([p * math.log(p, 2) for p in probs if p > 0])) if probs.sum() else 0.0
                nonflat = int(counts.get(0, 0) + counts.get(2, 0))
                diagnostic_rows.append(
                    {
                        "label_candidate_id": label_candidate_id,
                        "contract_id": contract_id,
                        "margin_policy_id": margin_policy_id,
                        "split": split,
                        "rows": total,
                        "short_rows": int(counts.get(0, 0)),
                        "flat_rows": int(counts.get(1, 0)),
                        "long_rows": int(counts.get(2, 0)),
                        "nonflat_rate": float(nonflat / total) if total else 0.0,
                        "long_share_of_nonflat": float(counts.get(2, 0) / nonflat) if nonflat else 0.0,
                        "class_entropy": entropy,
                        "diagnostic_role": "train_sets_threshold;validation_oos_readonly(학습은 임계값 고정, 검증/OOS는 읽기 전용)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )

    label_frame = pd.concat(label_frames, ignore_index=True)
    return label_frame, contract_rows, two_stage_rows, diagnostic_rows


def build_two_stage_tasks(two_stage_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in two_stage_rows:
        for stage, target, row_key in (
            ("stage1_nonflat_gate", "binary_is_nonflat(비횡보 이진)", "train_nonflat_rate"),
            ("stage2_direction_rank", "short_vs_long_rank_when_nonflat(비횡보 방향 순위)", "direction_rows_train"),
        ):
            rows.append(
                {
                    "task_id": f"{stage}__{item['margin_policy_id']}__{item['contract_id']}",
                    "contract_id": item["contract_id"],
                    "margin_policy_id": item["margin_policy_id"],
                    "stage": stage,
                    "target": target,
                    "required_input": rel(LABEL_MARGIN_FRAME),
                    "train_rows": item[row_key] if row_key == "direction_rows_train" else "all_train_rows",
                    "validation_rows_readonly": item["direction_rows_validation"] if row_key == "direction_rows_train" else "all_validation_rows",
                    "oos_rows_readonly": item["direction_rows_oos"] if row_key == "direction_rows_train" else "all_oos_rows",
                    "selection_use": "not_allowed(허용 안 됨)",
                    "blocked_if": "missing_train_only_threshold_or_missing_label_frame(학습 전용 임계값 또는 라벨 프레임 누락)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_feature_sets(feature_columns: Sequence[str], state_carry: pd.DataFrame) -> list[dict[str, Any]]:
    max_carry = state_carry.groupby("feature_name")["abs_autocorrelation"].max().to_dict()
    feature_list = list(feature_columns)
    macro_prefixes = (
        "vix_",
        "us10yr_",
        "usdx_",
        "nvda_",
        "aapl_",
        "msft_",
        "amzn_",
        "mega8_",
        "top3_",
        "us100_minus_",
    )

    def row(feature_set_id: str, role: str, dropped: Sequence[str], rule: str) -> dict[str, Any]:
        dropped_set = set(dropped)
        included = [name for name in feature_list if name not in dropped_set]
        return {
            "feature_set_id": feature_set_id,
            "feature_set_role": role,
            "source_feature_count": len(feature_list),
            "included_feature_count": len(included),
            "dropped_feature_count": len(dropped_set),
            "dropped_feature_rule": rule,
            "included_features_json": list(included),
            "dropped_features_json": sorted(dropped_set),
            "feature_order_hash": feature_order_hash(included),
            "source_artifact": rel(CR_FEATURE_STATE),
            "claim_boundary": CLAIM_BOUNDARY,
        }

    drop_ge80 = [name for name in feature_list if float(max_carry.get(name, 0.0)) >= 0.80]
    drop_ge70 = [name for name in feature_list if float(max_carry.get(name, 0.0)) >= 0.70]
    drop_macro = [name for name in feature_list if name.startswith(macro_prefixes)]
    return [
        row("all_features_control_reference", "control_reference_not_release(대조 기준, 해제 아님)", [], "none(없음)"),
        row("drop_state_carry_ge80", "control_orthogonal_probe(대조 직교 탐침)", drop_ge80, "drop max abs autocorrelation >= 0.80(최대 자기상관 0.80 이상 제거)"),
        row("drop_state_carry_ge70", "control_orthogonal_probe(대조 직교 탐침)", drop_ge70, "drop max abs autocorrelation >= 0.70(최대 자기상관 0.70 이상 제거)"),
        row("drop_macro_equity_stale_sources", "stale_source_probe(낡은 원천 탐침)", drop_macro, "drop macro/equity stale source columns(거시/주식 낡은 원천 열 제거)"),
    ]


def build_control_contract(control_rows: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped = control_rows.groupby(["control_id", "control_family", "split"], dropna=False)
    for (control_id, control_family, split), group in grouped:
        block_rows = int(group["blocks_runtime_probe"].astype(str).str.lower().isin(["true", "1"]).sum())
        worst = pd.to_numeric(group["control_minus_actual"], errors="coerce").max()
        rows.append(
            {
                "control_contract_id": f"{control_id}__{split}",
                "control_id": control_id,
                "control_family": control_family,
                "split": split,
                "observed_rows": int(len(group)),
                "observed_block_rows": block_rows,
                "worst_control_minus_actual": float(worst) if pd.notna(worst) else "",
                "required_contract": "must_degrade_vs_actual_before_runtime_queue(런타임 대기 전 실제보다 약화되어야 함)",
                "pass_condition": "control_trade_balanced_accuracy < actual_trade_balanced_accuracy and < 0.45(대조 거래 균형 정확도가 실제보다 낮고 0.45 미만)",
                "blocks_runtime_probe": "true" if block_rows else "pending",
                "forbidden_action": "do_not_drop_control_after_failure(실패 후 대조 제거 금지)",
                "source_artifact": rel(CS_CONTROLS),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "control_contract_id": "density_quality_joint_gate__validation_oos",
            "control_id": "density_quality_joint_gate",
            "control_family": "signal_density_plus_balanced_accuracy(신호 밀도 + 균형 정확도)",
            "split": "validation_oos",
            "observed_rows": len(control_rows),
            "observed_block_rows": int((control_rows["blocks_runtime_probe"].astype(str).str.lower() == "true").sum()),
            "worst_control_minus_actual": "",
            "required_contract": "density_only_pass_is_not_enough(밀도 단독 통과 불충분)",
            "pass_condition": "validation balanced > 0.40 and density floor met before OOS read(검증 균형 정확도 0.40 초과와 밀도 하한 동시 충족)",
            "blocks_runtime_probe": "true",
            "forbidden_action": "no_density_only_repair(밀도 단독 수리 금지)",
            "source_artifact": f"{rel(CS_SCORECARD)};{rel(CS_CONTROLS)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_tiny_probe_tasks(
    contracts: Sequence[Mapping[str, Any]], feature_sets: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    train_feature_sets = [row for row in feature_sets if row["feature_set_id"] != "all_features_control_reference"]
    model_configs = [
        ("balanced_extratrees_leaf_grid_tiny", "extratrees_depth6_leaf80_balanced", "extra_trees(엑스트라트리)", "leaf=80 depth=6"),
        ("balanced_extratrees_leaf_grid_tiny", "extratrees_depth6_leaf160_balanced", "extra_trees(엑스트라트리)", "leaf=160 depth=6"),
        ("balanced_extratrees_leaf_grid_tiny", "extratrees_depth6_leaf320_balanced", "extra_trees(엑스트라트리)", "leaf=320 depth=6"),
        ("cost_sensitive_direction_loss_scout", "extratrees_leaf160_direction_weight_2x", "extra_trees_weighted(가중 엑스트라트리)", "short/long weight 2x from train only"),
        ("cost_sensitive_direction_loss_scout", "extratrees_leaf160_inverse_train_weight", "extra_trees_weighted(가중 엑스트라트리)", "inverse class frequency from train only"),
        ("two_stage_calibrated_rank_only", "two_stage_rank_leaf160", "two_stage_rank(2단계 순위)", "stage1 nonflat + stage2 direction, rank only"),
    ]
    rows: list[dict[str, Any]] = []
    for contract in contracts:
        for feature_set in train_feature_sets:
            for probe_id, model_config_id, model_family, allowed_size in model_configs:
                task_id = "__".join(
                    [
                        model_config_id,
                        str(contract["label_candidate_id"]),
                        str(contract["contract_id"]),
                        str(feature_set["feature_set_id"]),
                    ]
                )
                rows.append(
                    {
                        "task_id": task_id,
                        "probe_id": probe_id,
                        "model_config_id": model_config_id,
                        "contract_id": contract["contract_id"],
                        "label_candidate_id": contract["label_candidate_id"],
                        "feature_set_id": feature_set["feature_set_id"],
                        "target_mode": "multiclass_or_two_stage_rank(다중분류 또는 2단계 순위)",
                        "model_family": model_family,
                        "allowed_size": allowed_size,
                        "required_inputs": f"{rel(LABEL_MARGIN_FRAME)};{rel(CONTROL_ORTHOGONAL_FEATURE_SETS)};{rel(EXTENDED_CONTROL_CONTRACT)}",
                        "validation_oos_role": "read_only_gates_no_ranking(읽기 전용 게이트, 순위 선택 금지)",
                        "selection_use": "not_allowed(허용 안 됨)",
                        "forbidden_action": "no_broad_search_no_oos_rank_selection(광범위 탐색 및 OOS 순위 선택 금지)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def build_cw_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CW_train_tiny_probe_matrix",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train predeclared tiny probe matrix(사전 선언 소형 탐침 행렬 학습)",
            "required_inputs": rel(TINY_MODEL_PROBE_TASK_MATRIX),
            "required_outputs": "trained_model_manifest.csv;onnx_parity_matrix.csv;scorecard.csv",
            "blocked_if_missing": "tiny probe matrix missing(소형 탐침 행렬 누락)",
            "forbidden_action": "no extra model search(추가 모델 탐색 금지)",
            "effect": "모델 용량 문제와 라벨 분리 문제를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CW_score_extended_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "score every model against extended controls(모든 모델을 확장 대조로 채점)",
            "required_inputs": rel(EXTENDED_CONTROL_CONTRACT),
            "required_outputs": "extended_control_scorecard.csv;runtime_probe_release_disposition.csv",
            "blocked_if_missing": "control contract missing(대조 계약 누락)",
            "forbidden_action": "no MT5 queue when any hard control blocks(강한 대조 차단 시 MT5 대기 금지)",
            "effect": "대조 실패를 런타임으로 우회하지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CW_score_label_separability",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "compare q60/q70 and two-stage separability(큐60/큐70과 2단계 분리력 비교)",
            "required_inputs": f"{rel(LABEL_MARGIN_CONTRACT)};{rel(TWO_STAGE_LABEL_CONTRACT)}",
            "required_outputs": "label_separability_scorecard.csv",
            "blocked_if_missing": "label contracts missing(라벨 계약 누락)",
            "forbidden_action": "no validation/OOS threshold tuning(검증/OOS 임계값 조정 금지)",
            "effect": "라벨 여백 수리가 실제 분리력을 높였는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CW_proxy_expected_only_if_controls_clear",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize proxy expected only for control-cleared rows(대조 통과 행만 프록시 예상값 생성)",
            "required_inputs": "runtime_probe_release_disposition.csv",
            "required_outputs": "proxy_expected_by_policy.csv",
            "blocked_if_missing": "no released rows(해제 행 없음)",
            "forbidden_action": "no MT5 package before control clearance(대조 통과 전 MT5 패키지 금지)",
            "effect": "프록시와 MT5 비교가 가능한 경우만 다음 외부 검증으로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("cv_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CU 설계와 기존 수리 산출물에 연결한다."),
        row("cv_gate_parent_points_to_cv", final["cu_next_action"] == RUN_ID, final["cu_next_action"], RUN_ID, "CU next_action(다음 행동)과 CV 실행을 맞춘다."),
        row("cv_gate_source_rows", final["source_rows"] == 46650, final["source_rows"], "46650", "같은 연구 표본 범위를 유지한다."),
        row("cv_gate_no_duplicate_timestamps", final["duplicate_timestamp_rows"] == 0, final["duplicate_timestamp_rows"], "0", "시간축 중복을 막는다."),
        row("cv_gate_label_contract_rows", final["label_contract_rows"] == final["contract_rows"] * len(LABEL_QUANTILES), final["label_contract_rows"], "contract_rows*2", "q60/q70 학습 전용 라벨 계약을 모두 만든다."),
        row("cv_gate_label_frame_rows", final["label_margin_frame_rows"] == final["source_rows"] * final["label_contract_rows"], final["label_margin_frame_rows"], "source_rows*label_contract_rows", "모든 행과 라벨 계약을 빠짐없이 매핑한다."),
        row("cv_gate_two_stage_rows", final["two_stage_contract_rows"] == final["label_contract_rows"], final["two_stage_contract_rows"], "label_contract_rows", "2단계 라벨 계약을 라벨 계약마다 만든다."),
        row("cv_gate_feature_sets", final["feature_set_rows"] >= 4, final["feature_set_rows"], ">=4", "대조 직교 피처 묶음을 만든다."),
        row("cv_gate_control_contract", final["control_contract_rows"] > 0, final["control_contract_rows"], ">0", "확장 대조 계약을 만든다."),
        row("cv_gate_tiny_probe_matrix", 0 < final["tiny_probe_task_rows"] <= 200, final["tiny_probe_task_rows"], "1..200", "소형 탐침 행렬을 제한된 크기로 묶는다."),
        row("cv_gate_cw_queue", final["queue_rows"] >= 4, final["queue_rows"], ">=4", "다음 CW 실행 조건을 명시한다."),
        row("cv_gate_no_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "CV는 입력 물질화로만 닫는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "timestamp(시각)은 UTC 정렬이고 source_row_id(원천 행 ID)는 정렬 후 부여했다.",
        "sample_scope": "US100 M5 shared research window(공유 연구 구간) 2022-09-01 to 2026-04-13, rows=46650",
        "missing_or_duplicate_check": {
            "duplicate_timestamp_rows": final["duplicate_timestamp_rows"],
            "missing_input_count": final["missing_input_count"],
        },
        "feature_label_boundary": "features(피처)는 현재/과거 열만 쓰고, future_log_return_12(미래 12봉 수익률)는 label(라벨)에만 쓴다. q60/q70 threshold(임계값)는 purged train rows(제거 학습 행)에서만 계산했다.",
        "split_boundary": "purged_embargo_split_membership(제거/격리 분할 소속)의 usable_for_training/validation/oos(학습/검증/OOS 사용 가능)를 따른다.",
        "leakage_risk": "validation/OOS diagnostic(검증/OOS 진단)을 threshold tuning(임계값 조정)이나 model ranking(모델 순위 선택)에 쓰는 경로",
        "data_hash_or_identity": {"source_sha256": final["source_sha256"], "source_rows": final["source_rows"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no_model_training_cv_materialization_only(모델 학습 없음, CV 입력 물질화 전용)",
        "target_and_label": "q60/q70 vol-normalized margin labels(변동성 정규화 여백 라벨) and two-stage nonflat-direction labels(2단계 비횡보-방향 라벨)",
        "split_method": "purged/embargo split(제거/격리 분할)",
        "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
        "secondary_metrics": "class entropy(클래스 엔트로피), nonflat rate(비횡보 비율), extended control clearance(확장 대조 통과)",
        "threshold_policy": "train_only_margin_quantile(학습 전용 여백 분위수)",
        "overfit_risk": "next run could over-read OOS ranks(다음 실행이 OOS 순위를 과해석할 위험)",
        "calibration_risk": "next scores are ranks unless calibrated(다음 점수는 보정 전 순위로만 해석)",
        "comparison_baseline": "run337CS weak density/control repaired candidates(약한 밀도/대조 수리 후보)",
        "validation_judgment": "materialized_inputs_ready_for_guarded_training",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    experiment_receipt = {
        "hypothesis": "Weak discrimination may come from noisy q50 label boundary and state-carry/control alignment(약한 분리력은 q50 라벨 경계 소음과 상태 이월/대조 정렬에서 올 수 있다).",
        "comparison": "q60/q70 labels, two-stage targets, control-orthogonal feature sets(큐60/큐70 라벨, 2단계 타깃, 대조 직교 피처 묶음)",
        "controls": "label_shift_gap72/gap96 and horizon_modulo controls(라벨 이동 72/96 및 기간 모듈로 대조)",
        "stop_conditions": "any extended control block prevents MT5 probe(확장 대조 차단은 MT5 탐침을 막는다).",
        "forbidden_actions": "no OOS threshold tuning, no density-only repair, no MT5 before control clearance(OOS 임계값 조정/밀도 단독 수리/대조 통과 전 MT5 금지)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "label contracts(라벨 계약), feature sets(피처 묶음), control contract(대조 계약), tiny task matrix(소형 작업 행렬), gate audit(게이트 감사)",
        "evidence_missing": "model training(모델 학습), ONNX parity(ONNX 동등성), proxy expected(프록시 예상), MT5 runtime probe(MT5 런타임 탐침)",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "입력은 만들어졌지만 아직 좋은 ONNX(온엑스)나 전진 통과를 뜻하지 않는다.",
    }
    receipt_paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 추적)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CV Separability Inputs(분리력 입력)

## Conclusion(결론)

run337CV(337CV 실행)는 CU 설계(design, 설계)를 실제 입력 산출물(input artifacts, 입력 산출물)로 물질화했다. q60/q70 label margin(라벨 여백), two-stage label(2단계 라벨), control-orthogonal feature sets(대조 직교 피처 묶음), extended control contract(확장 대조 계약), tiny probe task matrix(소형 탐침 작업 행렬)를 만들었다.

Effect(효과): 다음 run337CW(337CW 실행)는 validation/OOS(검증/OOS)로 threshold(임계값)를 고르거나, control failure(대조 실패)를 무시하고 MT5(MetaTrader 5, 메타트레이더5)로 넘어갈 수 없다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- source_rows(원천 행): `{final["source_rows"]}`
- duplicate_timestamp_rows(중복 시각 행): `{final["duplicate_timestamp_rows"]}`
- label_contract_rows(라벨 계약 행): `{final["label_contract_rows"]}`
- label_margin_frame_rows(라벨 여백 프레임 행): `{final["label_margin_frame_rows"]}`
- two_stage_contract_rows(2단계 계약 행): `{final["two_stage_contract_rows"]}`
- feature_set_rows(피처 묶음 행): `{final["feature_set_rows"]}`
- control_contract_rows(대조 계약 행): `{final["control_contract_rows"]}`
- tiny_probe_task_rows(소형 탐침 작업 행): `{final["tiny_probe_task_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CV

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): train-only label thresholds(학습 전용 라벨 임계값)와 extended control contract(확장 대조 계약)을 만들고 CW guarded training(CW 방어 학습)을 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(RUN_MANIFEST)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    workspace_text = re.sub(
        r"current_focus:\n- >-\n  Stage337 run337CV focus complete:.*?(?=\n- >-\n  Stage337 run337CU|\n[A-Za-z0-9_]+:)",
        "current_focus:\n",
        workspace_text,
        count=1,
        flags=re.DOTALL,
    )
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CV focus complete: feature/label separability control repair inputs(피처/라벨 분리력 대조 수리 입력)을 "
        f"`{STATUS}`로 물질화했다. Effect(효과): run337CW(337CW 실행)에서 train-only threshold(학습 전용 임계값)와 extended controls(확장 대조)를 지키는 소형 방어 학습을 실행한다."
    )
    workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337CV(337CV 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): q60/q70 label margin(라벨 여백), two-stage label(2단계 라벨), control-orthogonal feature sets(대조 직교 피처 묶음), tiny probe task matrix(소형 탐침 작업 행렬)를 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CV\(337CV 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CU|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CU(337CU"
    current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_cv_input_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 feature/label separability control repaired guarded training(피처/라벨 분리력 대조 수리 방어 학습)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CV(337CV 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CV(337CV 실행) materialized feature/label separability control repair inputs(피처/라벨 분리력 대조 수리 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(
        line for line in changelog_text.splitlines() if "Stage337 run337CV materialized feature/label separability control repair inputs" not in line
    )
    changelog_entry = (
        f"- {TODAY}: Stage337 run337CV materialized feature/label separability control repair inputs(피처/라벨 분리력 대조 수리 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "feature_label_separability_control_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": (
            f"label_contract_rows={final['label_contract_rows']};"
            f"feature_set_rows={final['feature_set_rows']};"
            f"tiny_probe_task_rows={final['tiny_probe_task_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed."
        ),
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__separability_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "separability_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_input_materialization",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "input_materialization_no_training",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"label_contract_rows={final['label_contract_rows']};tiny_probe_task_rows={final['tiny_probe_task_rows']}",
        "guardrail_kpi": "train_only_thresholds;validation_oos_readonly;extended_controls;no_training;no_selection",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__separability_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "CU repair design materialized into feature label control inputs",
        "kpi_scope": "input_materialization_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__separability_inputs",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "can separability repair inputs be materialized without leakage or OOS selection",
        "metric_scope": "label_margin_feature_sets_control_contract_probe_matrix",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]

    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]

    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    frame = read_source_frame()
    membership = pd.read_parquet(io_path(CN_PURGED_MEMBERSHIP))
    state_carry = pd.read_csv(io_path(CR_FEATURE_STATE))
    control_scorecard = pd.read_csv(io_path(CS_CONTROLS))
    cu_final = read_json(CU_FINAL)
    source_manifest = read_json(CANDIDATE_INPUT_MANIFEST)
    feature_columns = list(source_manifest.get("feature_columns", []))

    label_frame, label_contracts, two_stage_contracts, diagnostic_rows = build_label_margin_inputs(frame, membership)
    two_stage_tasks = build_two_stage_tasks(two_stage_contracts)
    feature_sets = build_feature_sets(feature_columns, state_carry)
    control_contracts = build_control_contract(control_scorecard)
    tiny_tasks = build_tiny_probe_tasks(label_contracts, feature_sets)
    queue_rows = build_cw_queue()

    artifacts: list[Path] = [
        write_parquet(LABEL_MARGIN_FRAME, label_frame),
        write_csv(LABEL_MARGIN_CONTRACT, LABEL_CONTRACT_COLUMNS, label_contracts),
        write_csv(TWO_STAGE_LABEL_CONTRACT, TWO_STAGE_CONTRACT_COLUMNS, two_stage_contracts),
        write_csv(TWO_STAGE_TRAINING_TASK_MATRIX, TWO_STAGE_TASK_COLUMNS, two_stage_tasks),
        write_csv(CONTROL_ORTHOGONAL_FEATURE_SETS, FEATURE_SET_COLUMNS, feature_sets),
        write_csv(EXTENDED_CONTROL_CONTRACT, CONTROL_CONTRACT_COLUMNS, control_contracts),
        write_csv(TINY_MODEL_PROBE_TASK_MATRIX, TINY_TASK_COLUMNS, tiny_tasks),
        write_csv(SEPARABILITY_DIAGNOSTIC, DIAGNOSTIC_COLUMNS, diagnostic_rows),
        write_csv(CW_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cu_next_action": cu_final.get("next_action", ""),
        "source_rows": int(len(frame)),
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "duplicate_timestamp_rows": int(frame["timestamp"].duplicated().sum()),
        "missing_input_count": sum(1 for path in INPUT_FILES if not path_exists(path)),
        "contract_rows": int(membership["contract_id"].nunique()),
        "label_contract_rows": len(label_contracts),
        "label_margin_frame_rows": int(len(label_frame)),
        "two_stage_contract_rows": len(two_stage_contracts),
        "two_stage_task_rows": len(two_stage_tasks),
        "feature_set_rows": len(feature_sets),
        "control_contract_rows": len(control_contracts),
        "tiny_probe_task_rows": len(tiny_tasks),
        "diagnostic_rows": len(diagnostic_rows),
        "queue_rows": len(queue_rows),
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
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
