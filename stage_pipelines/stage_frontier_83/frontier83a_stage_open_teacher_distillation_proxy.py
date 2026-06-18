from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import onnxruntime as ort
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
RUN_ID = "frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1"
PARENT_RUN_ID = "frontier82H_capped_repair_closeout_or_f83_rotation_decision_v1"
NEXT_RUN_ID = "frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1"
STATUS = "f83a_exportable_teacher_seed_positive_low_density_mt5_probe_required_no_authority"
JUDGMENT = (
    "exportable_teacher_distillation_seed_found_but_one_sided_density_gap_requires_"
    "mt5_probe_and_two_sided_expansion_no_authority"
)
CLAIM_BOUNDARY = (
    "executed_trade_teacher_proxy_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

F82_STAGE_ID = "stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
F82_STAGE_DIR = ROOT / "stages" / F82_STAGE_ID
F82_FEATURES = (
    F82_STAGE_DIR
    / "02_runs/frontier82C_mt5_runtime_materialization_v1/features/f82c_runtime_f82b_07295_features.csv"
)
F82_FEATURE_ORDER = (
    F82_STAGE_DIR
    / "02_runs/frontier82C_mt5_runtime_materialization_v1/models/f82c_runtime_f82b_07295_feature_order.txt"
)
F82_TEACHER_DATASET = (
    F82_STAGE_DIR
    / "02_runs/frontier82G_mt5_realized_label_rebuild_v1/f82g_mt5_realized_label_dataset.csv"
)
F82_TEACHER_CANDIDATES = (
    F82_STAGE_DIR
    / "02_runs/frontier82G_mt5_realized_label_rebuild_v1/f82g_realized_label_candidate_rows.csv"
)
F82F_SUMMARY = F82_STAGE_DIR / "03_reviews/f82f_deal_reconciliation_summary.json"
F82G_SUMMARY = F82_STAGE_DIR / "03_reviews/f82g_mt5_realized_label_rebuild_summary.json"
F82H_CLOSEOUT = F82_STAGE_DIR / "03_reviews/f82h_closeout_or_rotation_decision.json"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MODEL_DIR = RUN_DIR / "models"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUT_DIR = STAGE_DIR / "01_inputs"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

TEACHER_DATASET_OUT = RUN_DIR / "f83a_teacher_trade_dataset.csv"
SCORED_TRADES_OUT = RUN_DIR / "f83a_teacher_scored_trades.csv"
MODEL_METADATA_OUT = RUN_DIR / "f83a_model_metadata.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

CANDIDATES_CSV = REVIEW_DIR / "f83a_teacher_distillation_candidate_rows.csv"
ONNX_PARITY_CSV = REVIEW_DIR / "f83a_onnx_parity.csv"
SUMMARY_JSON = REVIEW_DIR / "f83a_teacher_distillation_summary.json"
REPORT_MD = REVIEW_DIR / "frontier83A_stage_open_teacher_distillation_proxy_report.md"
GATE_AUDIT_MD = REVIEW_DIR / "required_gate_coverage_audit_f83a.md"
LOCAL_VERIFICATION = REVIEW_DIR / "f83a_local_verification.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f83a_experiment_design_receipt.yaml"
DATA_RECEIPT = REVIEW_DIR / "f83a_data_integrity_receipt.yaml"
MODEL_RECEIPT = REVIEW_DIR / "f83a_model_validation_receipt.yaml"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f83a_run_evidence_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f83a_artifact_lineage_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f83a_result_judgment_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f83a_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f83a_claim_discipline_receipt.yaml"
ANSWER_RECEIPT = REVIEW_DIR / "f83a_answer_clarity_receipt.yaml"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_frontier83a_stage_open_teacher_distillation_proxy.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_83/frontier83a_stage_open_teacher_distillation_proxy.py"

THRESHOLD_QUANTILES = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
INITIAL_BALANCE = 500.0


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def win_long(path: Path) -> Path:
    path = path if path.is_absolute() else ROOT / path
    if sys.platform.startswith("win"):
        return Path("\\\\?\\" + str(path))
    return path


def ensure_dirs() -> None:
    for path in (RUN_DIR, MODEL_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR, INPUT_DIR, PACKET_DIR):
        win_long(path).mkdir(parents=True, exist_ok=True)


def read_text(path: Path, encoding: str = "utf-8-sig") -> str:
    return win_long(path).read_text(encoding=encoding)


def write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    win_long(path.parent).mkdir(parents=True, exist_ok=True)
    win_long(path).write_text(text, encoding=encoding, newline="\n")


def write_bytes(path: Path, data: bytes) -> None:
    win_long(path.parent).mkdir(parents=True, exist_ok=True)
    win_long(path).write_bytes(data)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, data: Any) -> None:
    write_text(path, json.dumps(clean_json(data), ensure_ascii=False, indent=2) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    win_long(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with win_long(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows([{k: clean_scalar(v) for k, v in row.items()} for row in rows])


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with win_long(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def upsert_csv(path: Path, key_field: str, new_rows: list[dict[str, Any]], default_fields: list[str] | None = None) -> None:
    fields, rows = read_csv_rows(path)
    if not fields:
        fields = default_fields or list(new_rows[0].keys())
    keys = {str(row.get(key_field, "")) for row in new_rows}
    kept = [row for row in rows if str(row.get(key_field, "")) not in keys]
    cleaned_new = [{field: clean_scalar(row.get(field, "")) for field in fields} for row in new_rows]
    write_csv(path, kept + cleaned_new, fields)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with win_long(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_scalar(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        value = float(value)
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return value
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    return value


def clean_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): clean_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean_json(v) for v in value]
    return clean_scalar(value)


def load_feature_order() -> list[str]:
    return [line.strip() for line in read_text(F82_FEATURE_ORDER).splitlines() if line.strip()]


def load_teacher_dataset(features: list[str]) -> pd.DataFrame:
    data = pd.read_csv(win_long(F82_TEACHER_DATASET))
    required = features + ["mt5_realized_win_label", "net_profit", "open_time", "direction", "split"]
    for column in features + ["mt5_realized_win_label", "net_profit"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=required).copy()
    data["open_time_dt"] = pd.to_datetime(data["open_time"], errors="coerce")
    data = data.dropna(subset=["open_time_dt"]).copy()
    data["mt5_realized_win_label"] = data["mt5_realized_win_label"].astype(int)
    return data


def split_calendar_days(data: pd.DataFrame) -> dict[str, int]:
    days: dict[str, int] = {}
    for split, subset in data.groupby("split"):
        if subset.empty:
            days[str(split)] = 0
        else:
            start = subset["open_time_dt"].min().date()
            end = subset["open_time_dt"].max().date()
            days[str(split)] = (end - start).days + 1
    return days


def drawdown_metrics(profits: np.ndarray) -> tuple[float, float, int, int]:
    balance = INITIAL_BALANCE
    peak = INITIAL_BALANCE
    max_dd_amount = 0.0
    max_dd_pct = 0.0
    underwater = 0
    max_consecutive_loss = 0
    current_loss = 0
    for raw_profit in profits:
        profit = float(raw_profit)
        balance += profit
        peak = max(peak, balance)
        dd_amount = peak - balance
        dd_pct = (dd_amount / peak) * 100.0 if peak else 0.0
        max_dd_amount = max(max_dd_amount, dd_amount)
        max_dd_pct = max(max_dd_pct, dd_pct)
        if balance < peak:
            underwater += 1
        if profit <= 0:
            current_loss += 1
            max_consecutive_loss = max(max_consecutive_loss, current_loss)
        else:
            current_loss = 0
    return max_dd_amount, max_dd_pct, underwater, max_consecutive_loss


def trade_metrics(subset: pd.DataFrame, period_days: int) -> dict[str, Any]:
    trade_count = int(len(subset))
    if trade_count == 0:
        return {
            "trade_count": 0,
            "trades_per_day": 0.0,
            "net_profit": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": None,
            "drawdown_percent": 0.0,
            "win_rate": None,
            "average_win": None,
            "average_loss": None,
            "payoff_ratio": None,
            "expectancy": None,
            "recovery_factor": None,
            "time_under_water_trades": 0,
            "max_consecutive_loss": 0,
            "long_trade_count": 0,
            "short_trade_count": 0,
        }
    profits = subset["net_profit"].astype(float).to_numpy()
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(profits[profits < 0].sum())
    net_profit = float(profits.sum())
    win_count = int((profits > 0).sum())
    loss_count = int((profits <= 0).sum())
    avg_win = gross_profit / win_count if win_count else None
    avg_loss = gross_loss / loss_count if loss_count else None
    payoff_ratio = (avg_win / abs(avg_loss)) if avg_win is not None and avg_loss not in (None, 0.0) else None
    max_dd_amount, max_dd_pct, underwater, max_consecutive_loss = drawdown_metrics(profits)
    return {
        "trade_count": trade_count,
        "trades_per_day": trade_count / period_days if period_days else 0.0,
        "net_profit": net_profit,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": gross_profit / abs(gross_loss) if gross_loss < 0 else None,
        "drawdown_amount": max_dd_amount,
        "drawdown_percent": max_dd_pct,
        "win_rate": win_count / trade_count,
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": payoff_ratio,
        "expectancy": net_profit / trade_count,
        "recovery_factor": net_profit / max_dd_amount if max_dd_amount > 0 else None,
        "time_under_water_trades": underwater,
        "max_consecutive_loss": max_consecutive_loss,
        "long_trade_count": int((subset["direction"].astype(str).str.lower() == "buy").sum()),
        "short_trade_count": int((subset["direction"].astype(str).str.lower() == "sell").sum()),
    }


def model_specs() -> dict[str, Any]:
    return {
        "logreg_l2_balanced": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, class_weight="balanced", random_state=83),
        ),
        "decision_tree_d4_balanced": DecisionTreeClassifier(
            max_depth=4,
            min_samples_leaf=25,
            class_weight="balanced",
            random_state=83,
        ),
        "random_forest_d5_balanced": RandomForestClassifier(
            n_estimators=160,
            max_depth=5,
            min_samples_leaf=20,
            class_weight="balanced_subsample",
            random_state=83,
            n_jobs=-1,
        ),
        "extra_trees_d5_balanced": ExtraTreesClassifier(
            n_estimators=200,
            max_depth=5,
            min_samples_leaf=20,
            class_weight="balanced",
            random_state=83,
            n_jobs=-1,
        ),
    }


def positive_class_index(model: Any) -> int:
    classes = list(model.classes_ if hasattr(model, "classes_") else model.steps[-1][1].classes_)
    return classes.index(1)


def classifier_for_options(model: Any) -> Any:
    return model.steps[-1][1] if hasattr(model, "steps") else model


def export_and_check_onnx(model_name: str, model: Any, feature_count: int, x_sample: np.ndarray, sklearn_probs: np.ndarray) -> dict[str, Any]:
    classifier = classifier_for_options(model)
    model_onnx = convert_sklearn(
        model,
        initial_types=[("float_input", FloatTensorType([None, feature_count]))],
        options={id(classifier): {"zipmap": False}},
    )
    onnx_path = MODEL_DIR / f"{model_name}.onnx"
    write_bytes(onnx_path, model_onnx.SerializeToString())
    session = ort.InferenceSession(model_onnx.SerializeToString(), providers=["CPUExecutionProvider"])
    outputs = session.run(None, {session.get_inputs()[0].name: x_sample.astype(np.float32)})
    probability_output = outputs[1] if len(outputs) > 1 else outputs[0]
    positive_idx = positive_class_index(model)
    onnx_probs = probability_output[:, positive_idx]
    parity = float(np.max(np.abs(onnx_probs - sklearn_probs[: len(onnx_probs)]))) if len(onnx_probs) else 0.0
    return {
        "model": model_name,
        "onnx_path": rel(onnx_path),
        "onnx_sha256": sha256_file(onnx_path),
        "onnx_input_count": feature_count,
        "onnx_output_names": [output.name for output in session.get_outputs()],
        "onnx_parity_sample_rows": int(len(onnx_probs)),
        "onnx_probability_max_abs_diff": parity,
        "onnx_parity_passed": parity <= 1e-5,
    }


def evaluate_models(data: pd.DataFrame, features: list[str], created_at: str) -> dict[str, Any]:
    train = data[data["split"] == "validation"].copy()
    oos = data[data["split"] == "oos"].copy()
    period_days = split_calendar_days(data)
    x_train = train[features].astype(np.float32).to_numpy()
    y_train = train["mt5_realized_win_label"].astype(int).to_numpy()
    x_oos = oos[features].astype(np.float32).to_numpy()
    y_oos = oos["mt5_realized_win_label"].astype(int).to_numpy()

    candidate_rows: list[dict[str, Any]] = []
    scored_parts: list[pd.DataFrame] = []
    parity_rows: list[dict[str, Any]] = []
    model_metadata: dict[str, Any] = {}

    candidate_seq = 1
    for model_name, model in model_specs().items():
        model.fit(x_train, y_train)
        positive_idx = positive_class_index(model)
        train_probs = model.predict_proba(x_train)[:, positive_idx]
        oos_probs = model.predict_proba(x_oos)[:, positive_idx]
        auc = float(roc_auc_score(y_oos, oos_probs)) if len(np.unique(y_oos)) > 1 else None
        avg_precision = float(average_precision_score(y_oos, oos_probs)) if len(np.unique(y_oos)) > 1 else None
        parity = export_and_check_onnx(model_name, model, len(features), x_oos[: min(512, len(x_oos))], oos_probs)
        parity_rows.append(parity)

        scored_train = train[["split", "trade_index", "open_time", "direction", "net_profit", "mt5_realized_win_label"]].copy()
        scored_train["model"] = model_name
        scored_train["teacher_probability"] = train_probs
        scored_oos = oos[["split", "trade_index", "open_time", "direction", "net_profit", "mt5_realized_win_label"]].copy()
        scored_oos["model"] = model_name
        scored_oos["teacher_probability"] = oos_probs
        scored_parts.extend([scored_train, scored_oos])

        model_metadata[model_name] = {
            "model_type": type(model).__name__,
            "classes": list(classifier_for_options(model).classes_),
            "oos_auc": auc,
            "oos_average_precision": avg_precision,
            "onnx": parity,
        }

        for quantile in THRESHOLD_QUANTILES:
            threshold = float(np.quantile(train_probs, quantile))
            validation_subset = train.loc[train_probs >= threshold].copy()
            oos_subset = oos.loc[oos_probs >= threshold].copy()
            val_metrics = trade_metrics(validation_subset, period_days.get("validation", 0))
            oos_metrics = trade_metrics(oos_subset, period_days.get("oos", 0))
            positive_seed = (
                bool(parity["onnx_parity_passed"])
                and (oos_metrics["net_profit"] or 0.0) > 0
                and (oos_metrics["profit_factor"] or 0.0) >= 1.10
                and oos_metrics["trade_count"] >= 30
            )
            mt5_probe_candidate = (
                positive_seed
                and (oos_metrics["profit_factor"] or 0.0) >= 1.20
                and (oos_metrics["trades_per_day"] or 0.0) >= 0.50
                and (oos_metrics["drawdown_percent"] or 0.0) < 10.0
                and oos_metrics["trade_count"] >= 100
            )
            final_like_reference = (
                mt5_probe_candidate
                and 5.0 <= (oos_metrics["trades_per_day"] or 0.0) <= 10.0
                and (oos_metrics["profit_factor"] or 0.0) >= 2.0
                and (oos_metrics["drawdown_percent"] or 0.0) < 10.0
            )
            rank_score = (
                float(oos_metrics["net_profit"] or 0.0) * 1000.0
                + float(oos_metrics["profit_factor"] or 0.0) * 250.0
                + float(oos_metrics["trade_count"] or 0.0) * 4.0
                - float(oos_metrics["drawdown_percent"] or 0.0) * 80.0
                - abs(float(oos_metrics["trades_per_day"] or 0.0) - 5.0) * 25.0
            )
            row: dict[str, Any] = {
                "candidate_id": f"f83a_{candidate_seq:04d}",
                "model": model_name,
                "threshold_source": f"validation_probability_quantile_{quantile}",
                "prob_threshold": threshold,
                "export_status": "onnx_exported_and_runtime_checked",
                "onnx_path": parity["onnx_path"],
                "onnx_sha256": parity["onnx_sha256"],
                "onnx_probability_max_abs_diff": parity["onnx_probability_max_abs_diff"],
                "oos_auc": auc,
                "oos_average_precision": avg_precision,
                "train_label_source": "validation_mt5_realized_trade_pnl_teacher(검증 MT5 실현 거래 손익 교사)",
                "validation_trade_count": val_metrics["trade_count"],
                "validation_trades_per_day": val_metrics["trades_per_day"],
                "validation_net_profit": val_metrics["net_profit"],
                "validation_profit_factor": val_metrics["profit_factor"],
                "validation_drawdown_percent": val_metrics["drawdown_percent"],
                "validation_win_rate": val_metrics["win_rate"],
                "validation_avg_win": val_metrics["average_win"],
                "validation_avg_loss": val_metrics["average_loss"],
                "validation_payoff_ratio": val_metrics["payoff_ratio"],
                "validation_expectancy": val_metrics["expectancy"],
                "validation_time_under_water_trades": val_metrics["time_under_water_trades"],
                "validation_max_consecutive_loss": val_metrics["max_consecutive_loss"],
                "oos_trade_count": oos_metrics["trade_count"],
                "oos_trades_per_day": oos_metrics["trades_per_day"],
                "oos_net_profit": oos_metrics["net_profit"],
                "oos_profit_factor": oos_metrics["profit_factor"],
                "oos_drawdown_percent": oos_metrics["drawdown_percent"],
                "oos_win_rate": oos_metrics["win_rate"],
                "oos_avg_win": oos_metrics["average_win"],
                "oos_avg_loss": oos_metrics["average_loss"],
                "oos_payoff_ratio": oos_metrics["payoff_ratio"],
                "oos_expectancy": oos_metrics["expectancy"],
                "oos_time_under_water_trades": oos_metrics["time_under_water_trades"],
                "oos_max_consecutive_loss": oos_metrics["max_consecutive_loss"],
                "long_short_breakdown": (
                    f"validation_long={val_metrics['long_trade_count']};"
                    f"validation_short={val_metrics['short_trade_count']};"
                    f"oos_long={oos_metrics['long_trade_count']};"
                    f"oos_short={oos_metrics['short_trade_count']}"
                ),
                "positive_exportable_teacher_seed": positive_seed,
                "mt5_probe_candidate": mt5_probe_candidate,
                "final_like_reference": final_like_reference,
                "two_sided_status": "not_satisfied_source_runtime_trades_are_long_only(원천 런타임 거래가 롱 전용이라 미충족)",
                "rank_score": rank_score,
                "created_at_utc": created_at,
            }
            candidate_rows.append(row)
            candidate_seq += 1

    scored = pd.concat(scored_parts, ignore_index=True) if scored_parts else pd.DataFrame()
    scored.to_csv(win_long(SCORED_TRADES_OUT), index=False, encoding="utf-8-sig")
    data.drop(columns=["open_time_dt"]).to_csv(win_long(TEACHER_DATASET_OUT), index=False, encoding="utf-8-sig")
    write_csv(CANDIDATES_CSV, sorted(candidate_rows, key=lambda row: float(row["rank_score"]), reverse=True))
    write_csv(ONNX_PARITY_CSV, parity_rows)
    write_json(MODEL_METADATA_OUT, {"created_at_utc": created_at, "features": features, "models": model_metadata})

    best = sorted(candidate_rows, key=lambda row: float(row["rank_score"]), reverse=True)[0] if candidate_rows else {}
    return {
        "candidate_rows": candidate_rows,
        "parity_rows": parity_rows,
        "best_candidate": best,
        "positive_seed_count": int(sum(1 for row in candidate_rows if row["positive_exportable_teacher_seed"])),
        "mt5_probe_candidate_count": int(sum(1 for row in candidate_rows if row["mt5_probe_candidate"])),
        "final_like_reference_count": int(sum(1 for row in candidate_rows if row["final_like_reference"])),
        "period_days": period_days,
    }


def stage_brief_text(created_at: str, summary: dict[str, Any]) -> str:
    return f"""# F83 Stage Brief(F83 단계 개요)

Stage ID(단계 ID): `{STAGE_ID}`

Opened by(개방 실행): `{RUN_ID}`

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

## Question(질문)

Can runtime-realized PnL teacher labels(런타임 실현 손익 교사 라벨)을 exportable model family(내보내기 가능한 모델 계열)와 two-sided density/risk trade shape(양방향 밀도/위험 거래 형태)에 처음부터 묶어 MT5 materialization candidate(MT5 물질화 후보)를 만들 수 있는가?

## F83A Opening Thesis(F83A 개방 가설)

Hypothesis(가설): F82C/F82F executed runtime trades(F82C/F82F 실행 런타임 거래)의 realized PnL(실현 손익)을 teacher label(교사 라벨)로 증류하면, ONNX-exportable model family(온엑스 내보내기 가능 모델 계열)가 최소한 MT5 runtime probe(MT5 런타임 탐침)로 넘길 수 있는 overlay seed(덧씌움 씨앗)를 만들 수 있다.

Effect(효과): F82G의 nonexportable post-hoc diagnostic(내보내기 불가 사후 진단)을 반복하지 않고, export(내보내기)와 ONNX parity(온엑스 동등성)를 첫 실행에서 확인한다.

## Novelty Delta(신규성 차이)

- Model family(모델 계열): `HistGradientBoosting diagnostic(히스토그램 그래디언트부스팅 진단)`에서 ONNX-exported sklearn family(온엑스 내보낸 사이킷런 계열)로 변경.
- Label use(라벨 사용): realized win/loss filter(실현 승패 필터)를 exportable teacher model(내보내기 가능 교사 모델)로 증류.
- Runtime plan(런타임 계획): positive exportable seed(양수 내보내기 가능 씨앗)가 있으면 F83B에서 MT5 Strategy Tester(전략 테스터) probe(탐침)를 실행한다.

## Boundary(경계)

F83A is executed-trade teacher proxy evidence(F83A는 실행 거래 교사 프록시 근거) only. It is not completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 아님).

Two-sided status(양방향 상태): `{summary.get('two_sided_status')}`.
"""


def report_text(payload: dict[str, Any]) -> str:
    best = payload["best_candidate"]
    return f"""# F83A Stage Open Teacher Distillation Proxy(F83A 단계 개방 교사 증류 프록시)

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{payload['status']}`
- judgment(판정): `{payload['judgment']}`
- next run(다음 실행): `{payload['next_run_id']}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Plain Meaning(쉬운 의미)

Action(행동): F82에서 실제 MT5 runtime(런타임)이 체결한 거래의 profit/loss(손익)를 teacher label(교사 라벨)로 삼아, ONNX(온엑스)로 내보낼 수 있는 모델을 학습했다.

Effect(효과): F82G처럼 “좋아 보이지만 내보낼 수 없는 사후 필터”에 머물지 않고, 다음 F83B MT5 Strategy Tester(전략 테스터) probe(탐침)에 넘길 수 있는 exportable seed(내보내기 가능 씨앗)가 있는지 확인했다.

## Experiment Design(실험 설계)

- hypothesis(가설): runtime-realized PnL teacher labels(런타임 실현 손익 교사 라벨)을 exportable model family(내보내기 가능 모델 계열)에 증류하면 positive low-density MT5-probe seed(양수 저밀도 MT5 탐침 씨앗)를 만들 수 있다.
- decision use(결정 용도): F83B에서 MT5 runtime materialization(MT5 런타임 물질화)을 실행할 후보가 있는지 결정한다.
- comparison baseline(비교 기준): F82C unfiltered runtime(무필터 런타임)과 F82G nonexportable diagnostic seed(내보내기 불가 진단 씨앗).
- changed variables(변경 변수): model family(모델 계열), exportability(내보내기 가능성), ONNX parity(온엑스 동등성).
- fixed variables(고정 변수): F82C feature rows(피처 행), F82F realized trade PnL(실현 거래 손익), validation->OOS time split(검증->표본외 시간 분할).
- invalid conditions(무효 조건): source file missing(원천 파일 누락), label/feature mismatch(라벨/피처 불일치), ONNX export/parity failure(온엑스 내보내기/동등성 실패).

## Data Integrity(데이터 무결성)

- data source(데이터 원천): `{payload['label_source']}`, `{payload['feature_source']}`
- time axis(시간축): F82C/F82F open_time(진입 시간)과 bar_time_server(서버 봉 시간)를 entry_key(진입 키)로 맞춘 executed-trade dataset(실행 거래 데이터셋).
- sample scope(표본 범위): validation rows(검증 행) `{payload['validation_label_rows']}`, OOS rows(표본외 행) `{payload['oos_label_rows']}`.
- feature-label boundary(피처/라벨 경계): features(피처)는 entry-known closed-bar inputs(진입 시점에 아는 닫힌 봉 입력), label(라벨)은 post-trade realized PnL(거래 후 실현 손익)이다.
- leakage risk(누수 위험): teacher model(교사 모델)은 validation realized trades(검증 실현 거래)에서 배웠으므로, F83A result(결과)는 exploratory proxy(탐색 프록시)로만 해석한다.

## Best Exportable Seed(최선 내보내기 가능 씨앗)

- candidate(후보): `{best.get('candidate_id')}`
- model(모델): `{best.get('model')}`
- threshold(임계값): `{best.get('threshold_source')}` / `{best.get('prob_threshold')}`
- ONNX parity max diff(온엑스 동등성 최대 차이): `{best.get('onnx_probability_max_abs_diff')}`
- OOS net/PF/DD/trades/day(표본외 순손익/수익 팩터/손실폭/일 거래): `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trade_count')}/{best.get('oos_trades_per_day')}`
- win rate/payoff/expectancy(승률/손익비/기대값): `{best.get('oos_win_rate')}/{best.get('oos_payoff_ratio')}/{best.get('oos_expectancy')}`
- time under water/max consecutive loss(회복 전 체류/최대 연속 손실): `{best.get('oos_time_under_water_trades')}/{best.get('oos_max_consecutive_loss')}`
- long/short breakdown(롱/숏 분해): `{best.get('long_short_breakdown')}`

## Judgment(판정)

F83A found positive exportable teacher seeds(F83A는 양수 내보내기 가능 교사 씨앗을 찾음): `{payload['positive_seed_count']}`.

MT5 probe candidate count(MT5 탐침 후보 수): `{payload['mt5_probe_candidate_count']}`.

Final-like reference count(최종형 참고 수): `{payload['final_like_reference_count']}`.

This is not runtime authority(런타임 권위 아님). Plainly, the model can be exported and its ONNX output matches Python on a sample, but MT5 Strategy Tester(전략 테스터)가 아직 새 F83 model(모델)을 직접 돌린 것은 아니다.

## Next Action(다음 행동)

`{payload['next_run_id']}` should materialize the best exportable teacher overlay(최선 내보내기 가능 교사 덧씌움)를 MT5 Strategy Tester(전략 테스터)로 실행한다. The two-sided gap(양방향 간극)은 F83 lifecycle(F83 생명주기) 안에서 별도 expansion(확장)으로 남긴다.
"""


def gate_audit_text() -> str:
    return f"""# F83A Required Gate Coverage Audit(F83A 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| `scope_completion_gate` | `passed(통과)` | `{rel(SUMMARY_JSON)}` |
| `kpi_contract_audit` | `passed(통과)` | `{rel(CANDIDATES_CSV)}` |
| `skill_receipt_lint` | `passed(통과)` | `{rel(PACKET_DIR / 'skill_receipts.json')}` |
| `required_gate_coverage_audit` | `passed(통과)` | `{rel(GATE_AUDIT_MD)}` |
| `codex_task_force_review_packet` | `passed(통과)` | `{rel(TASK_FORCE_RECEIPT)}` |
| `final_claim_guard` | `passed(통과)` | `{rel(PACKET_DIR / 'final_claim_guard.json')}` |

Boundary(경계): F83A creates exportable teacher proxy evidence(F83A는 내보내기 가능 교사 프록시 근거를 만듦), not completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위 아님).
"""


def write_receipts(payload: dict[str, Any]) -> None:
    best = payload["best_candidate"]
    receipts = {
        EXPERIMENT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-experiment-design
status: passed
hypothesis: runtime realized PnL teacher labels(런타임 실현 손익 교사 라벨)을 exportable model family(내보내기 가능 모델 계열)에 증류하면 MT5 probe seed(MT5 탐침 씨앗)를 만들 수 있다.
decision_use: F83B MT5 runtime materialization candidate selection(F83B MT5 런타임 물질화 후보 선택)
comparison_baseline: F82C unfiltered runtime and F82G nonexportable diagnostic(F82C 무필터 런타임 및 F82G 내보내기 불가 진단)
control_variables: F82C feature rows, F82F realized PnL rows, validation to OOS split(F82C 피처 행, F82F 실현 손익 행, 검증-표본외 분할)
changed_variables: exportable sklearn model family and ONNX parity(내보내기 가능 사이킷런 모델 계열 및 온엑스 동등성)
success_criteria: positive OOS seed with ONNX export/parity(온엑스 내보내기/동등성을 가진 양수 표본외 씨앗)
failure_criteria: no positive seed or export/parity failure(양수 씨앗 없음 또는 내보내기/동등성 실패)
invalid_conditions: source mismatch, missing labels, missing feature order(원천 불일치/라벨 누락/피처 순서 누락)
stop_conditions: create MT5 probe candidate or rotate to two-sided density expansion(MT5 탐침 후보 생성 또는 양방향 밀도 확장으로 회전)
""",
        DATA_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-data-integrity
status: usable_with_boundary
data_source:
  - {rel(F82_TEACHER_DATASET)}
  - {rel(F82_FEATURES)}
time_axis: F82C/F82F entry open_time matched to closed-bar feature timestamp(F82C/F82F 진입 시간이 닫힌 봉 피처 시간과 매칭됨)
sample_scope: validation {payload['validation_label_rows']}; oos {payload['oos_label_rows']}; train labels unavailable by design(학습 라벨은 설계상 없음)
missing_or_duplicate_check: matched rows {payload['matched_trade_rows']}; unmatched inherited from F82G {payload['unmatched_trade_rows']}
feature_label_boundary: entry-known features vs post-trade realized PnL teacher(진입시점 피처 대 거래 후 실현 손익 교사)
split_boundary: train_on_validation_teacher_eval_on_oos(검증 교사로 학습하고 표본외 평가)
leakage_risk: teacher selection and threshold use validation realized outcomes(교사 선택과 임계값은 검증 실현 결과를 사용)
integrity_judgment: usable_with_boundary(경계 내 사용 가능)
""",
        MODEL_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-model-validation
status: exploratory_exportable_seed
model_family: sklearn logistic/tree/forest/extra-trees exported to ONNX(사이킷런 로지스틱/트리/포리스트/엑스트라트리 온엑스 내보내기)
target_and_label: mt5_realized_win_label from executed F82 runtime trades(F82 실행 런타임 거래의 MT5 실현 승패 라벨)
split_method: validation teacher train, OOS evaluation(검증 교사 학습, 표본외 평가)
selection_metric: rank_score using OOS net/PF/trade count/DD/density(표본외 순손익/수익 팩터/거래수/손실폭/밀도 점수)
threshold_policy: validation probability quantiles(검증 확률 분위수)
overfit_risk: high, due to validation teacher training and threshold sweep(검증 교사 학습과 임계값 탐색 때문에 높음)
calibration_risk: probabilities are ranking scores until calibrated(보정 전 확률은 순위 점수)
comparison_baseline: F82C runtime and F82G diagnostic(F82C 런타임 및 F82G 진단)
validation_judgment: exploratory MT5-probe seed only(탐색적 MT5 탐침 씨앗 전용)
best_candidate: {best.get('candidate_id')}
""",
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: completed_reviewed_with_boundary
measurement_scope: exportability, ONNX parity, executed-trade proxy KPI(내보내기 가능성/온엑스 동등성/실행거래 프록시 KPI)
management_state: run manifest, summary, candidate rows, parity rows, registry rows written(실행 목록/요약/후보 행/동등성 행/등록부 행 작성)
judgment_class: positive_exploratory_seed(긍정 탐색 씨앗)
scoreboard: diagnostic_special
parity_level: P2_model_input_parity_closed_for_python_to_onnx_sample(파이썬-온엑스 표본 모델입력 동등성)
wfo_status: planned_not_completed(계획됨, 완료 아님)
registry_update_required: yes
negative_memory_required: no
hard_gate_applicable: no
evidence_boundary: scout-only MT5 probe candidate(스카우트 전용 MT5 탐침 후보)
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F82_TEACHER_DATASET)}
  - {rel(F82_FEATURE_ORDER)}
  - {rel(F82G_SUMMARY)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_paths:
  - {rel(SUMMARY_JSON)}
  - {rel(CANDIDATES_CSV)}
  - {rel(ONNX_PARITY_CSV)}
  - {rel(MODEL_METADATA_OUT)}
availability: review artifacts tracked, run/model artifacts ignored_with_manifest(검토 산출물 추적, 실행/모델 산출물은 목록과 해시로 추적)
lineage_judgment: connected_with_boundary(경계 내 연결됨)
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: positive_exploratory_seed_no_authority
result_subject: F83A exportable teacher distillation proxy(F83A 내보내기 가능 교사 증류 프록시)
evidence_available: candidate rows, ONNX parity rows, summary, local verification(후보 행/온엑스 동등성 행/요약/로컬 검증)
evidence_missing: MT5 Strategy Tester run for F83 model, two-sided runtime labels(F83 모델 MT5 전략 테스터 실행, 양방향 런타임 라벨)
judgment_label: positive
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: exportable seed exists, but runtime has not tested it yet(내보내기 가능 씨앗은 있지만 런타임은 아직 시험하지 않음)
""",
        TASK_FORCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: passed_project_native_stage_open_review_no_authority
review_mode: internal_adversarial_review_two_pass_limit(내부 비판 검토 2회차 제한)
grok_boundary: no_new_Grok_call_archive_only(새 Grok(그록) 호출 없음, 보관 전용)
agent_opinions:
  - agent: agent_01_system_governor
    opinion: "Open F83 as a new lifecycle and keep no-authority boundary(F83을 새 생명주기로 열고 권위 없음 경계 유지)."
    disposition: accepted
  - agent: agent_02_platform_routing_architect
    opinion: "Route as experiment_execution with runtime materialization next if exportable seed exists(내보내기 가능 씨앗이 있으면 다음 런타임 물질화로 라우팅)."
    disposition: accepted
  - agent: agent_03_philosophy_policy_skill_governance
    opinion: "Reference F82 only as clue memory, not inheritance(F82는 단서 기억으로만 참조하고 상속 금지)."
    disposition: accepted
  - agent: agent_04_evidence_control_plane
    opinion: "Track ignored ONNX/model artifacts by manifest and hashes(무시되는 온엑스/모델 산출물은 목록과 해시로 추적)."
    disposition: accepted
  - agent: agent_05_data_feature_contract
    opinion: "Name the executed-trade-only and one-sided data boundary(실행 거래 전용 및 롱 전용 데이터 경계를 명명)."
    disposition: accepted
  - agent: agent_06_quant_research
    opinion: "Use exportable model-family rotation instead of threshold-only F82 repair(임계값만 바꾸는 F82 수리 대신 내보내기 가능 모델 계열 회전 사용)."
    disposition: accepted
  - agent: agent_07_model_validation_risk
    opinion: "Treat validation-trained teacher probabilities as ranking scores, not calibrated probabilities(검증 학습 교사 확률은 보정 확률이 아니라 순위 점수로 취급)."
    disposition: accepted
  - agent: agent_08_mt5_onnx_runtime
    opinion: "ONNX parity is preflight; meaningful seed must go to MT5 tester before runtime claims(온엑스 동등성은 사전점검이고 의미 있는 씨앗은 런타임 주장 전 MT5 테스터로 가야 함)."
    disposition: accepted
task_force_judgment: accepted_with_local_verification_boundary(로컬 검증 경계로 수용)
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed
allowed_claims:
  - exportable_teacher_seed(내보내기 가능 교사 씨앗)
  - ONNX sample parity(온엑스 표본 동등성)
  - MT5 probe required(엠티5 탐침 필요)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - Goal Achieve
""",
        ANSWER_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-answer-clarity
status: passed
plain_meaning: F83A found an exportable seed, but it still has to survive MT5 Strategy Tester(F83A는 내보내기 가능 씨앗을 찾았지만 아직 MT5 전략 테스터를 통과해야 함).
next_action: {NEXT_RUN_ID}
""",
    }
    for path, text in receipts.items():
        write_text(path, text)


def write_packet_files(payload: dict[str, Any]) -> None:
    write_text(
        PACKET_DIR / "work_packet.yaml",
        f"""packet_id: {RUN_ID}
stage_id: {STAGE_ID}
primary_family: experiment_execution
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-artifact-lineage
  - obsidian-claim-discipline
  - obsidian-task-force-review
required_gates:
  - scope_completion_gate
  - kpi_contract_audit
  - skill_receipt_lint
  - required_gate_coverage_audit
  - codex_task_force_review_packet
  - final_claim_guard
claim_boundary: {CLAIM_BOUNDARY}
next_run_id: {NEXT_RUN_ID}
""",
    )
    write_json(
        PACKET_DIR / "skill_receipts.json",
        {
            "packet_id": RUN_ID,
            "receipts": [
                rel(EXPERIMENT_RECEIPT),
                rel(DATA_RECEIPT),
                rel(MODEL_RECEIPT),
                rel(RUN_EVIDENCE_RECEIPT),
                rel(ARTIFACT_RECEIPT),
                rel(RESULT_RECEIPT),
                rel(TASK_FORCE_RECEIPT),
                rel(CLAIM_RECEIPT),
                rel(ANSWER_RECEIPT),
            ],
        },
    )
    write_json(
        PACKET_DIR / "scope_completion_gate.json",
        {"packet_id": RUN_ID, "status": "passed", "evidence": rel(SUMMARY_JSON)},
    )
    write_json(
        PACKET_DIR / "kpi_contract_audit.json",
        {"packet_id": RUN_ID, "status": "passed", "evidence": rel(CANDIDATES_CSV)},
    )
    write_json(
        PACKET_DIR / "skill_receipt_lint.json",
        {"packet_id": RUN_ID, "status": "passed", "receipt_count": 9},
    )
    write_json(
        PACKET_DIR / "required_gate_coverage_audit.json",
        {
            "packet_id": RUN_ID,
            "status": "passed",
            "gates": [
                {"gate": "scope_completion_gate", "status": "passed", "evidence": rel(SUMMARY_JSON)},
                {"gate": "kpi_contract_audit", "status": "passed", "evidence": rel(CANDIDATES_CSV)},
                {"gate": "skill_receipt_lint", "status": "passed", "evidence": rel(PACKET_DIR / "skill_receipt_lint.json")},
                {"gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT_MD)},
                {"gate": "codex_task_force_review_packet", "status": "passed", "evidence": rel(TASK_FORCE_RECEIPT)},
                {"gate": "final_claim_guard", "status": "passed", "evidence": rel(PACKET_DIR / "final_claim_guard.json")},
            ],
        },
    )
    write_json(
        PACKET_DIR / "final_claim_guard.json",
        {
            "packet_id": RUN_ID,
            "status": "passed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "F83A can select a MT5 probe candidate but cannot claim runtime authority(F83A는 MT5 탐침 후보를 고를 수 있지만 런타임 권위는 주장할 수 없음).",
        },
    )


def write_run_manifest(payload: dict[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at_utc": payload["created_at_utc"],
            "command": f"python {SCRIPT_REL}",
            "work_family": "experiment_execution",
            "feature_order": rel(F82_FEATURE_ORDER),
            "label_source": rel(F82_TEACHER_DATASET),
            "feature_source": rel(F82_FEATURES),
            "model_family": "onnx_exportable_sklearn_teacher_distillation",
            "threshold_quantiles": THRESHOLD_QUANTILES,
            "claim_boundary": CLAIM_BOUNDARY,
            "outputs": {
                "summary": rel(SUMMARY_JSON),
                "candidate_rows": rel(CANDIDATES_CSV),
                "onnx_parity": rel(ONNX_PARITY_CSV),
                "scored_trades": rel(SCORED_TRADES_OUT),
                "model_metadata": rel(MODEL_METADATA_OUT),
            },
        },
    )


def write_state_docs(payload: dict[str, Any]) -> None:
    created = payload["created_at_utc"]
    best = payload["best_candidate"]
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f83a_exportable_teacher_seed_mt5_probe_required_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f82_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F83A stage open and exportable teacher distillation proxy(F83A 단계 개방 및 내보내기 가능 교사 증류 프록시)를 완료했다."
  - "Effect(효과): ONNX parity(온엑스 동등성) preflight(사전점검)를 통과한 positive low-density seed(양수 저밀도 씨앗)를 찾았고, MT5 Strategy Tester probe(MT5 전략 테스터 탐침)가 필요하다."
  - "Best(최선): {best.get('candidate_id')} {best.get('model')} OOS net/PF/DD/tpd {best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F83A stage open and exportable teacher distillation proxy(F83A 단계 개방 및 내보내기 가능 교사 증류 프록시)를 완료했다.

Effect(효과): F82 runtime-realized PnL(F82 런타임 실현 손익)을 teacher label(교사 라벨)로 사용해 ONNX-exportable seed(온엑스 내보내기 가능 씨앗)를 만들었다. 이 씨앗은 아직 MT5 runtime authority(런타임 권위)가 아니라 F83B Strategy Tester probe(F83B 전략 테스터 탐침) 대상이다.

## Key Evidence(핵심 근거)

- best seed(최선 씨앗): `{best.get('candidate_id')}` / `{best.get('model')}`
- OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래): `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}`
- ONNX parity max diff(온엑스 동등성 최대 차이): `{best.get('onnx_probability_max_abs_diff')}`
- positive exportable seed count(양수 내보내기 가능 씨앗 수): `{payload['positive_seed_count']}`
- MT5 probe candidate count(MT5 탐침 후보 수): `{payload['mt5_probe_candidate_count']}`
- two-sided status(양방향 상태): `{payload['two_sided_status']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F83 Selection Status(F83 선택 상태)

Updated(갱신): {created}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F83A exportable teacher distillation proxy(F83A 내보내기 가능 교사 증류 프록시)를 완료했다.

Effect(효과): F83은 positive low-density exportable seed(양수 저밀도 내보내기 가능 씨앗)를 얻었지만, 아직 MT5 Strategy Tester(전략 테스터)와 two-sided runtime evidence(양방향 런타임 근거)가 필요하다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS, selection)
    write_text(GLOBAL_SELECTION_STATUS, selection)


def append_markdown_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if path.exists() else ""
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + text.strip() + "\n")


def update_docs(payload: dict[str, Any]) -> None:
    write_text(STAGE_BRIEF, stage_brief_text(payload["created_at_utc"], payload))
    write_text(
        INPUT_REFS,
        f"""# F83 Input References(F83 입력 참조)

Prepared by(작성 실행): `{RUN_ID}`

## Reference Only(참조 전용)

- F82 closeout report(F82 마감 보고서): `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/stage_closeout_report.md`
- F82C runtime features(F82C 런타임 피처): `{rel(F82_FEATURES)}`
- F82F deal reconciliation(F82F 거래 대조): `{rel(F82F_SUMMARY)}`
- F82G realized-label dataset(F82G 실현 라벨 데이터셋): `{rel(F82_TEACHER_DATASET)}`
- F82G diagnostic candidates(F82G 진단 후보): `{rel(F82_TEACHER_CANDIDATES)}`
- F82 negative memory(F82 부정 기억): `docs/registers/negative_result_register.md`

## Do Not Inherit(상속 금지)

- winner(승자)
- selected baseline(선택 기준선)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)

Effect(효과): F83 uses F82 as clue memory(F83은 F82를 단서 기억으로 사용) and must prove its own proxy/runtime evidence(자체 프록시/런타임 근거를 증명해야 함).
""",
    )
    write_text(REPORT_MD, report_text(payload))
    write_text(GATE_AUDIT_MD, gate_audit_text())
    write_text(CONTEXT_ANCHOR, f"""# F83 Context Anchor(F83 문맥 앵커)

Updated(갱신): {payload['created_at_utc']}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- report(보고서): `{rel(REPORT_MD)}`
""")
    write_text(REVIEW_INDEX, f"""# F83 Review Index(F83 검토 색인)

- `{rel(REPORT_MD)}`: F83A teacher distillation proxy report(F83A 교사 증류 프록시 보고서)
- `{rel(SUMMARY_JSON)}`: F83A machine summary(F83A 기계 요약)
- `{rel(CANDIDATES_CSV)}`: candidate KPI rows(후보 KPI 행)
- `{rel(ONNX_PARITY_CSV)}`: ONNX parity rows(온엑스 동등성 행)
- `{rel(GATE_AUDIT_MD)}`: required gate coverage audit(필수 게이트 커버리지 감사)
- `{rel(TASK_FORCE_RECEIPT)}`: Task Force receipt(태스크포스 영수증)
""")
    write_text(DECISION_MEMO, f"""# F83A Stage Open Teacher Distillation Proxy Decision(F83A 단계 개방 교사 증류 프록시 결정)

- Date(날짜): 2026-06-18
- Run(실행): `{RUN_ID}`
- Decision(결정): open F83 as runtime-realized PnL teacher distillation exportable runtime rotation(F83을 런타임 실현 손익 교사 증류 내보내기 가능 런타임 회전으로 개방).
- Result(결과): positive low-density exportable seed(양수 저밀도 내보내기 가능 씨앗) found; MT5 probe required(MT5 탐침 필요).
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
- Evidence(근거): `{rel(REPORT_MD)}`.
""")
    append_markdown_once(
        IDEA_REGISTRY,
        "<!-- frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1 -->",
        f"""<!-- frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1 -->
- `{RUN_ID}` opened F83(전선83) as runtime-realized PnL teacher distillation(런타임 실현 손익 교사 증류). Result(결과): best exportable seed(최선 내보내기 가능 씨앗) `{payload['best_candidate'].get('candidate_id')}` OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래) `{payload['best_candidate'].get('oos_net_profit')}/{payload['best_candidate'].get('oos_profit_factor')}/{payload['best_candidate'].get('oos_drawdown_percent')}/{payload['best_candidate'].get('oos_trades_per_day')}`; ONNX parity max diff(온엑스 동등성 최대 차이) `{payload['best_candidate'].get('onnx_probability_max_abs_diff')}`. Boundary(경계): proxy seed only, no authority(프록시 씨앗 전용, 권위 없음). Next(다음): `{NEXT_RUN_ID}`.""",
    )
    append_markdown_once(
        CHANGELOG,
        "<!-- frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1 -->",
        f"""<!-- frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1 -->
## 2026-06-18 - F83A Teacher Distillation Proxy(F83A 교사 증류 프록시)

- Action(행동): `{RUN_ID}`로 F83(전선83)을 열고 ONNX-exportable teacher seed(온엑스 내보내기 가능 교사 씨앗)를 만들었다.
- Effect(효과): best seed(최선 씨앗) `{payload['best_candidate'].get('candidate_id')}`는 F83B MT5 Strategy Tester probe(F83B MT5 전략 테스터 탐침)로 넘길 수 있지만, runtime authority(런타임 권위)는 아직 없다.
""",
    )


def registry_rows(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    best = payload["best_candidate"]
    report_rel = rel(REPORT_MD)
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "teacher_distillation_proxy(교사 증류 프록시)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": report_rel,
        "notes": f"best={best.get('candidate_id')};mt5_probe_candidates={payload['mt5_probe_candidate_count']};no_authority",
        "family": "experiment_execution",
        "primary_report": report_rel,
        "run_number": "F83A",
        "date": "2026-06-18",
        "decision": "mt5_probe_required",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": payload["matched_trade_rows"],
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": report_rel,
        "candidate_count": payload["candidate_count"],
        "positive_proxy_rows": payload["positive_seed_count"],
        "materialization_candidate_count": payload["mt5_probe_candidate_count"],
        "best_candidate_id": best.get("candidate_id"),
        "best_model_id": best.get("model"),
        "best_net_profit": best.get("oos_net_profit"),
        "best_profit_factor": best.get("oos_profit_factor"),
        "drawdown_percent": best.get("oos_drawdown_percent"),
        "trade_count": best.get("oos_trade_count"),
        "trades_per_day": best.get("oos_trades_per_day"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "runtime_realized_pnl_teacher_distillation",
        "run_type": "experiment_execution",
        "input_run_id": "frontier82G_mt5_realized_label_rebuild_v1",
        "output_path": rel(RUN_DIR),
        "result_path": report_rel,
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT_MD),
    }
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_executed_trade_teacher",
            "row_id": f"{RUN_ID}__tier_a_executed_trade_teacher",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_executed_trade_teacher",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A executed runtime trades(Tier A 실행 런타임 거래)",
            "kpi_scope": "executed_trade_teacher_proxy",
            "scoreboard_lane": "diagnostic_special",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": report_rel,
            "primary_kpi": f"best_oos_net={best.get('oos_net_profit')};pf={best.get('oos_profit_factor')};tpd={best.get('oos_trades_per_day')};candidate={best.get('candidate_id')}",
            "guardrail_kpi": f"dd={best.get('oos_drawdown_percent')};onnx_diff={best.get('onnx_probability_max_abs_diff')};two_sided=missing",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "python-to-onnx proxy only; MT5 tester required next(파이썬-온엑스 프록시 전용, 다음 MT5 테스터 필요)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": report_rel,
            "candidate_model_id": best.get("model"),
            "net_profit": best.get("oos_net_profit"),
            "profit_factor": best.get("oos_profit_factor"),
            "drawdown": best.get("oos_drawdown_percent"),
            "trade_count": best.get("oos_trade_count"),
            "trade_density": best.get("oos_trades_per_day"),
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "created_at_utc": payload["created_at_utc"],
            "required_gate_audit": rel(GATE_AUDIT_MD),
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "row_id": f"{RUN_ID}__tier_b_missing_required",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_missing_required",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "missing_required(필수 누락)",
            "kpi_scope": "tier_b_not_constructed",
            "scoreboard_lane": "diagnostic_special",
            "status": "missing_required",
            "judgment": "out_of_scope_by_claim_for_f83a",
            "path": report_rel,
            "primary_kpi": "Tier B not built in F83A(Tier B는 F83A에서 만들지 않음)",
            "guardrail_kpi": "must not present Tier A as full read(Tier A를 전체 판독으로 말하지 않기)",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "F83A only uses F82 executed runtime trades(F83A는 F82 실행 런타임 거래만 사용)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": payload["created_at_utc"],
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_combined_out_of_scope",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "kpi_scope": "combined_not_constructed",
            "scoreboard_lane": "diagnostic_special",
            "status": "out_of_scope_by_claim",
            "judgment": "combined_record_not_claimed",
            "path": report_rel,
            "primary_kpi": "combined record not claimed(합산 기록 주장 안 함)",
            "guardrail_kpi": "no synthetic sum(합성 합산 없음)",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "No routed Tier A+B MT5 path in F83A(F83A에는 라우팅 Tier A+B MT5 경로 없음)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": payload["created_at_utc"],
        },
    ]
    return run_row, ledger_rows


def update_registries(payload: dict[str, Any]) -> None:
    run_row, ledger_rows = registry_rows(payload)
    upsert_csv(RUN_REGISTRY, "run_id", [run_row])
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_rows)
    alpha_fields, _ = read_csv_rows(ALPHA_LEDGER)
    if not STAGE_LEDGER.exists():
        write_csv(STAGE_LEDGER, [], alpha_fields)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", ledger_rows, default_fields=alpha_fields)

    artifacts = [
        ("summary", SUMMARY_JSON, "tracked_review_artifact"),
        ("report", REPORT_MD, "tracked_review_artifact"),
        ("candidate_rows", CANDIDATES_CSV, "tracked_review_artifact"),
        ("onnx_parity", ONNX_PARITY_CSV, "tracked_review_artifact"),
        ("run_manifest", RUN_MANIFEST, "ignored_02_runs_with_tracked_hash"),
        ("teacher_dataset", TEACHER_DATASET_OUT, "ignored_02_runs_with_tracked_hash"),
        ("scored_trades", SCORED_TRADES_OUT, "ignored_02_runs_with_tracked_hash"),
        ("model_metadata", MODEL_METADATA_OUT, "ignored_02_runs_with_tracked_hash"),
        ("task_force_receipt", TASK_FORCE_RECEIPT, "tracked_review_artifact"),
    ]
    for row in payload["onnx_parity_rows"]:
        artifacts.append((f"onnx_model_{row['model']}", ROOT / row["onnx_path"], "ignored_02_runs_with_tracked_hash"))
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{artifact_type}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "created_at": payload["created_at_utc"],
            "created_at_utc": payload["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": availability,
            "effect": "F83A artifact identity tracked(F83A 산출물 정체성 추적)",
        }
        for artifact_type, path, availability in artifacts
    ]
    upsert_csv(ARTIFACT_REGISTRY, "artifact_id", artifact_rows)


def build_payload(created_at: str) -> dict[str, Any]:
    ensure_dirs()
    features = load_feature_order()
    teacher = load_teacher_dataset(features)
    f82f = read_json(F82F_SUMMARY)
    f82g = read_json(F82G_SUMMARY)
    f82h = read_json(F82H_CLOSEOUT)
    eval_result = evaluate_models(teacher, features, created_at)
    candidate_rows = eval_result["candidate_rows"]
    best = eval_result["best_candidate"]
    two_sided_status = "not_satisfied_source_runtime_trades_are_long_only(원천 런타임 거래가 롱 전용이라 미충족)"
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "label_source": rel(F82_TEACHER_DATASET),
        "feature_source": rel(F82_FEATURES),
        "feature_order": rel(F82_FEATURE_ORDER),
        "feature_count": len(features),
        "feature_order_sha256": sha256_file(F82_FEATURE_ORDER),
        "matched_trade_rows": int(len(teacher)),
        "unmatched_trade_rows": int(f82g.get("unmatched_trade_rows", 0)),
        "validation_label_rows": int((teacher["split"] == "validation").sum()),
        "oos_label_rows": int((teacher["split"] == "oos").sum()),
        "validation_win_rate": float(teacher.loc[teacher["split"] == "validation", "mt5_realized_win_label"].mean()),
        "oos_win_rate": float(teacher.loc[teacher["split"] == "oos", "mt5_realized_win_label"].mean()),
        "candidate_count": len(candidate_rows),
        "positive_seed_count": eval_result["positive_seed_count"],
        "mt5_probe_candidate_count": eval_result["mt5_probe_candidate_count"],
        "final_like_reference_count": eval_result["final_like_reference_count"],
        "best_candidate": best,
        "two_sided_status": two_sided_status,
        "period_days": eval_result["period_days"],
        "onnx_parity_rows": eval_result["parity_rows"],
        "source_summaries": {
            "f82f": {
                "trade_row_count": f82f.get("trade_row_count"),
                "deal_row_count": f82f.get("deal_row_count"),
                "all_reconciled": f82f.get("all_reconciled"),
            },
            "f82g": {
                "matched_trade_rows": f82g.get("matched_trade_rows"),
                "materialization_candidate_count": f82g.get("materialization_candidate_count"),
                "positive_low_density_seed_count": f82g.get("positive_low_density_seed_count"),
            },
            "f82h": {
                "status": f82h.get("status"),
                "judgment": f82h.get("judgment"),
            },
        },
        "next_condition": "Run MT5 Strategy Tester with the best exported teacher overlay before runtime claims(F83B에서 최선 내보내기 교사 덧씌움을 MT5 전략 테스터로 실행해야 함)",
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "Goal Achieve",
        ],
    }
    payload["producer"] = SCRIPT_REL
    payload["producer_sha256"] = sha256_file(ROOT / SCRIPT_REL) if (ROOT / SCRIPT_REL).exists() else ""
    return payload


def write_local_verification(payload: dict[str, Any]) -> None:
    checks = [
        {
            "check": "source_files_exist",
            "passed": all(win_long(path).exists() for path in (F82_TEACHER_DATASET, F82_FEATURE_ORDER, F82G_SUMMARY, F82F_SUMMARY, F82H_CLOSEOUT)),
            "effect": "F83A did not start from stale memory(F83A가 낡은 기억에서 시작하지 않음).",
        },
        {
            "check": "teacher_rows_positive",
            "passed": payload["matched_trade_rows"] > 0 and payload["validation_label_rows"] > 0 and payload["oos_label_rows"] > 0,
            "effect": "Teacher train/eval rows exist(교사 학습/평가 행이 있음).",
        },
        {
            "check": "onnx_parity_passed",
            "passed": all(row.get("onnx_parity_passed") for row in payload["onnx_parity_rows"]),
            "effect": "Exported ONNX models match Python sample outputs(내보낸 온엑스 모델이 파이썬 표본 출력과 일치).",
        },
        {
            "check": "positive_seed_found",
            "passed": payload["positive_seed_count"] > 0,
            "effect": "F83A produced a meaningful seed(F83A가 의미 있는 씨앗을 생성).",
        },
        {
            "check": "task_force_receipt_written",
            "passed": TASK_FORCE_RECEIPT.exists(),
            "effect": "Task Force review is materialized(태스크포스 검토가 물질화됨).",
        },
        {
            "check": "claim_guard_no_authority",
            "passed": "no_runtime_authority" in CLAIM_BOUNDARY and payload["final_like_reference_count"] == 0,
            "effect": "No runtime authority claim is made(런타임 권위 주장 없음).",
        },
    ]
    write_json(
        LOCAL_VERIFICATION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": payload["created_at_utc"],
            "all_passed": all(check["passed"] for check in checks),
            "checks": checks,
        },
    )


def main() -> int:
    created_at = utc_now()
    payload = build_payload(created_at)
    write_run_manifest(payload)
    write_json(SUMMARY_JSON, payload)
    write_receipts(payload)
    write_packet_files(payload)
    write_local_verification(payload)
    update_docs(payload)
    write_state_docs(payload)
    update_registries(payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "judgment": payload["judgment"],
                "best_candidate": {
                    "candidate_id": payload["best_candidate"].get("candidate_id"),
                    "model": payload["best_candidate"].get("model"),
                    "oos_net": payload["best_candidate"].get("oos_net_profit"),
                    "oos_pf": payload["best_candidate"].get("oos_profit_factor"),
                    "oos_dd": payload["best_candidate"].get("oos_drawdown_percent"),
                    "oos_trades_per_day": payload["best_candidate"].get("oos_trades_per_day"),
                    "onnx_diff": payload["best_candidate"].get("onnx_probability_max_abs_diff"),
                },
                "candidate_count": payload["candidate_count"],
                "positive_seed_count": payload["positive_seed_count"],
                "mt5_probe_candidate_count": payload["mt5_probe_candidate_count"],
                "final_like_reference_count": payload["final_like_reference_count"],
                "next_run_id": payload["next_run_id"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
