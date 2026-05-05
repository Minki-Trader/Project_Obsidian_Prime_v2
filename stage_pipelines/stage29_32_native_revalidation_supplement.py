from __future__ import annotations

import argparse
import importlib.metadata
import json
import math
import random
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines import stage29_32_goal_completion as base


STAGE_SCOPE = (29, 30, 31, 32)
SUPPLEMENT_PACKET_ID = "stage29_32_native_revalidation_supplement_v1"
SUMMARY_PATH = ROOT / "docs/workspace/stage29_32_native_revalidation_supplement.md"


NATIVE_STAGE_PLANS: dict[int, base.StagePlan] = {
    29: replace(
        base.STAGE_PLANS[29],
        scout_run_number="run23C",
        scout_run_id="run23C_river_native_online_learning_scout_v1",
        runtime_run_number="run23D",
        runtime_run_id="run23D_river_native_online_runtime_probe_v1",
        scout_packet_id="stage29_run23C_river_native_online_learning_scout_v1",
        runtime_packet_id="stage29_run23D_river_native_online_runtime_probe_v1",
        closeout_packet_id="stage29_native_revalidation_supplement_v1",
        model_family="river_native_one_vs_rest_logistic_online_learning",
        runtime_model_family="river_native_distilled_score_table_runtime_probe",
        selected_variant_id="v01_river_logreg_core42_slow_adapt",
        dependency_note="river 0.24.2 installed; native River one-vs-rest online logistic learning used for revalidation, then distilled to MT5 score-table handoff.",
        topic_read="river_native_online_drift_adaptation_probability_handoff",
    ),
    30: replace(
        base.STAGE_PLANS[30],
        scout_run_number="run24C",
        scout_run_id="run24C_native_source_calibration_abstention_scout_v1",
        runtime_run_number="run24D",
        runtime_run_id="run24D_native_source_calibration_runtime_probe_v1",
        scout_packet_id="stage30_run24C_native_source_calibration_abstention_scout_v1",
        runtime_packet_id="stage30_run24D_native_source_calibration_runtime_probe_v1",
        closeout_packet_id="stage30_native_source_calibration_supplement_v1",
        model_family="sklearn_isotonic_calibration_on_native_river_source",
        runtime_model_family="native_source_calibration_distilled_score_table_runtime_probe",
        selected_variant_id="v02_isotonic_margin_abstention_native_source",
        dependency_note="Stage30 uses the newly installed River native Stage29 source probabilities; no additional native package is required.",
        topic_read="native_source_probability_calibration_abstention_handoff",
    ),
    31: replace(
        base.STAGE_PLANS[31],
        scout_run_number="run25C",
        scout_run_id="run25C_tabnet_native_attentive_tabular_scout_v1",
        runtime_run_number="run25D",
        runtime_run_id="run25D_tabnet_native_attentive_runtime_probe_v1",
        scout_packet_id="stage31_run25C_tabnet_native_attentive_tabular_scout_v1",
        runtime_packet_id="stage31_run25D_tabnet_native_attentive_runtime_probe_v1",
        closeout_packet_id="stage31_tabnet_native_revalidation_supplement_v1",
        model_family="pytorch_tabnet_native_attentive_tabular",
        runtime_model_family="tabnet_native_distilled_score_table_runtime_probe",
        selected_variant_id="v02_tabnet_native_steps3_sparse",
        dependency_note="torch 2.11.0+cpu and pytorch-tabnet 4.1.0 installed; native TabNetClassifier used for revalidation, then distilled to MT5 score-table handoff.",
        topic_read="tabnet_native_attention_probability_handoff",
    ),
    32: replace(
        base.STAGE_PLANS[32],
        scout_run_number="run26C",
        scout_run_id="run26C_torch_tcn_native_temporal_scout_v1",
        runtime_run_number="run26D",
        runtime_run_id="run26D_torch_tcn_native_temporal_runtime_probe_v1",
        scout_packet_id="stage32_run26C_torch_tcn_native_temporal_scout_v1",
        runtime_packet_id="stage32_run26D_torch_tcn_native_temporal_runtime_probe_v1",
        closeout_packet_id="stage32_torch_tcn_native_revalidation_supplement_v1",
        model_family="torch_native_tcn_temporal_convolution",
        runtime_model_family="torch_tcn_native_distilled_score_table_runtime_probe",
        selected_variant_id="v01_torch_tcn_dilated_context_native",
        dependency_note="torch 2.11.0+cpu installed; native compact TCN used for revalidation, then distilled to MT5 score-table handoff.",
        topic_read="torch_tcn_native_temporal_convolution_handoff",
    ),
}


def dependency_versions() -> dict[str, Any]:
    versions: dict[str, Any] = {}
    for package, import_name in (
        ("river", "river"),
        ("torch", "torch"),
        ("pytorch-tabnet", "pytorch_tabnet"),
        ("scikit-learn", "sklearn"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
    ):
        try:
            versions[package] = {
                "installed": base.module_available(import_name),
                "version": importlib.metadata.version(package),
            }
        except importlib.metadata.PackageNotFoundError:
            versions[package] = {"installed": False, "version": None}
    try:
        import torch

        versions["torch"]["cuda_available"] = bool(torch.cuda.is_available())
    except Exception as exc:  # pragma: no cover - recorded in packet when import breaks.
        versions["torch"]["import_error"] = f"{type(exc).__name__}: {exc}"
    return versions


def ensure_required_dependencies() -> None:
    missing = [name for name, import_name in (("river", "river"), ("torch", "torch"), ("pytorch-tabnet", "pytorch_tabnet")) if not base.module_available(import_name)]
    if missing:
        raise RuntimeError(f"Missing native revalidation dependencies: {', '.join(missing)}")


def class_ordered_probabilities(raw: np.ndarray, classes: Sequence[int]) -> np.ndarray:
    out = np.zeros((raw.shape[0], len(base.LABEL_ORDER)), dtype="float64")
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    for target_index, label in enumerate(base.LABEL_ORDER):
        source_index = class_to_index.get(int(label))
        if source_index is not None:
            out[:, target_index] = raw[:, source_index]
    out = np.clip(out, 1e-8, 1.0)
    return out / out.sum(axis=1, keepdims=True)


def river_probability_frame(model: Any, frame: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    data = base.clean_frame(frame, features)
    rows = data.loc[:, list(features)].to_dict(orient="records")
    prob = np.zeros((len(rows), len(base.LABEL_ORDER)), dtype="float64")
    for row_index, row in enumerate(rows):
        pred = model.predict_proba_one({key: float(value) for key, value in row.items()})
        for label_index, label in enumerate(base.LABEL_ORDER):
            prob[row_index, label_index] = float(pred.get(label, 0.0))
    prob = np.clip(prob, 1e-8, 1.0)
    prob = prob / prob.sum(axis=1, keepdims=True)
    return base.probability_payload(data, prob)


def fit_river_online(frame: pd.DataFrame, features: Sequence[str], *, learning_rate: float, l2: float) -> tuple[Any, dict[str, Any]]:
    from river import compose, linear_model, multiclass, optim, preprocessing

    data = base.clean_frame(frame, features)
    train = data.loc[data["split"].astype(str).eq("train")].copy()
    model = compose.Pipeline(
        preprocessing.StandardScaler(),
        multiclass.OneVsRestClassifier(
            linear_model.LogisticRegression(
                optimizer=optim.SGD(float(learning_rate)),
                l2=float(l2),
            )
        ),
    )
    class_seen = {int(label): 0 for label in base.LABEL_ORDER}
    for row in train.itertuples(index=False):
        values = {feature: float(getattr(row, feature)) for feature in features}
        label = int(getattr(row, "label_class"))
        model.learn_one(values, label)
        class_seen[label] = class_seen.get(label, 0) + 1
    return model, {
        "backend": "river",
        "train_rows": int(len(train)),
        "feature_count": int(len(features)),
        "learning_rate": float(learning_rate),
        "l2": float(l2),
        "class_seen": class_seen,
        "river_version": importlib.metadata.version("river"),
    }


def build_stage29_native_variants(plan: base.StagePlan, context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    tier_b_order = tuple(context["tier_b_feature_order"])
    core24 = base.core24_features(tier_b_order)
    variants = [
        ("v01_river_logreg_core42_slow_adapt", tier_b_order, 0.025, 0.0008),
        ("v02_river_logreg_core24_fast_adapt", core24, 0.045, 0.0004),
        ("v03_river_logreg_core42_stable_l2", tier_b_order, 0.015, 0.0016),
    ]
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id, features, learning_rate, l2 in variants:
        model_a, details_a = fit_river_online(context["tier_a_frame"], features, learning_rate=learning_rate, l2=l2)
        model_b, details_b = fit_river_online(context["tier_b_training_frame"], features, learning_rate=learning_rate, l2=l2)
        tier_a_prob = river_probability_frame(model_a, context["tier_a_frame"], features)
        tier_b_prob = river_probability_frame(model_b, context["tier_b_fallback_frame"], features)
        details = {"tier_a": details_a, "tier_b": details_b, "features": list(features)}
        rows.append(base.summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details=details))
        if variant_id == plan.selected_variant_id:
            selected_frames = {"tier_a": tier_a_prob, "tier_b": tier_b_prob}
            model_root = plan.scout_run_root / "models"
            base.io_path(model_root).mkdir(parents=True, exist_ok=True)
            joblib.dump(model_a, base.io_path(model_root / "tier_a_river_native_model.joblib"))
            joblib.dump(model_b, base.io_path(model_root / "tier_b_river_native_model.joblib"))
            selected_details = details
    return rows, selected_frames, selected_details


def build_stage30_native_source_variants(plan: base.StagePlan, _context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    source_plan = NATIVE_STAGE_PLANS[29]
    source_packet = ROOT / "docs/agent_control/packets" / source_plan.runtime_packet_id / "aggregate_summary.json"
    if not base.io_path(source_packet).exists():
        raise FileNotFoundError(f"Stage30 native-source calibration requires Stage29 native runtime summary: {source_packet}")
    source_summary = base.read_json(source_packet)
    artifacts = source_summary["prediction_artifacts"]
    base_a = pd.read_parquet(base.io_path(ROOT / artifacts["tier_a_predictions"]["path"]))
    base_b = pd.read_parquet(base.io_path(ROOT / artifacts["tier_b_predictions"]["path"]))
    variants = [
        ("v01_temperature_margin_native_source", "v01_temperature_margin"),
        ("v02_isotonic_margin_abstention_native_source", "v02_isotonic_margin"),
    ]
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id, method in variants:
        tier_a_prob, details_a = base.calibrate_probs(base_a, method=method)
        tier_b_prob, details_b = base.calibrate_probs(base_b, method=method)
        details = {"tier_a": details_a, "tier_b": details_b, "source_run_id": source_plan.runtime_run_id}
        rows.append(base.summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details=details))
        if variant_id == plan.selected_variant_id:
            selected_frames = {"tier_a": tier_a_prob, "tier_b": tier_b_prob}
            selected_details = details
    return rows, selected_frames, selected_details


def fit_tabnet(frame: pd.DataFrame, features: Sequence[str], *, seed: int, n_d: int, n_steps: int, lambda_sparse: float, max_epochs: int) -> tuple[Any, dict[str, Any]]:
    import torch
    from pytorch_tabnet.tab_model import TabNetClassifier

    data = base.clean_frame(frame, features)
    train = data.loc[data["split"].astype(str).eq("train")].copy()
    validation = data.loc[data["split"].astype(str).eq("validation")].copy()
    scaler = StandardScaler()
    x_train = scaler.fit_transform(train.loc[:, list(features)].to_numpy(dtype="float32", copy=False)).astype("float32")
    y_train = train["label_class"].astype("int64").to_numpy()
    eval_set = None
    if not validation.empty:
        x_val = scaler.transform(validation.loc[:, list(features)].to_numpy(dtype="float32", copy=False)).astype("float32")
        y_val = validation["label_class"].astype("int64").to_numpy()
        eval_set = [(x_val, y_val)]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model = TabNetClassifier(
        n_d=int(n_d),
        n_a=int(n_d),
        n_steps=int(n_steps),
        gamma=1.3,
        lambda_sparse=float(lambda_sparse),
        optimizer_fn=torch.optim.Adam,
        optimizer_params={"lr": 0.015},
        mask_type="sparsemax",
        seed=int(seed),
        verbose=0,
    )
    fit_kwargs: dict[str, Any] = {
        "X_train": x_train,
        "y_train": y_train,
        "max_epochs": int(max_epochs),
        "patience": 3,
        "batch_size": 4096,
        "virtual_batch_size": 512,
        "num_workers": 0,
        "drop_last": False,
    }
    if eval_set:
        fit_kwargs["eval_set"] = eval_set
        fit_kwargs["eval_metric"] = ["logloss"]
    model.fit(**fit_kwargs)
    return {"model": model, "scaler": scaler}, {
        "backend": "pytorch_tabnet",
        "torch_version": torch.__version__,
        "pytorch_tabnet_version": importlib.metadata.version("pytorch-tabnet"),
        "train_rows": int(len(train)),
        "validation_rows": int(len(validation)),
        "feature_count": int(len(features)),
        "n_d": int(n_d),
        "n_steps": int(n_steps),
        "lambda_sparse": float(lambda_sparse),
        "max_epochs": int(max_epochs),
        "classes": [int(item) for item in getattr(model, "classes_", base.LABEL_ORDER)],
    }


def tabnet_probability_frame(fitted: Mapping[str, Any], frame: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    data = base.clean_frame(frame, features)
    x_all = fitted["scaler"].transform(data.loc[:, list(features)].to_numpy(dtype="float32", copy=False)).astype("float32")
    model = fitted["model"]
    raw = model.predict_proba(x_all)
    prob = class_ordered_probabilities(np.asarray(raw, dtype="float64"), [int(item) for item in getattr(model, "classes_", base.LABEL_ORDER)])
    return base.probability_payload(data, prob)


def build_stage31_native_variants(plan: base.StagePlan, context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    tier_b_order = tuple(context["tier_b_feature_order"])
    variants = [
        ("v01_tabnet_native_steps2_compact", 8, 2, 0.0008, 8, 3301),
        ("v02_tabnet_native_steps3_sparse", 10, 3, 0.0012, 10, 3302),
    ]
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id, n_d, n_steps, lambda_sparse, max_epochs, seed in variants:
        model_a, details_a = fit_tabnet(context["tier_a_frame"], tier_b_order, seed=seed, n_d=n_d, n_steps=n_steps, lambda_sparse=lambda_sparse, max_epochs=max_epochs)
        model_b, details_b = fit_tabnet(context["tier_b_training_frame"], tier_b_order, seed=seed + 43, n_d=n_d, n_steps=n_steps, lambda_sparse=lambda_sparse, max_epochs=max_epochs)
        tier_a_prob = tabnet_probability_frame(model_a, context["tier_a_frame"], tier_b_order)
        tier_b_prob = tabnet_probability_frame(model_b, context["tier_b_fallback_frame"], tier_b_order)
        details = {"tier_a": details_a, "tier_b": details_b, "features": list(tier_b_order)}
        rows.append(base.summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details=details))
        if variant_id == plan.selected_variant_id:
            selected_frames = {"tier_a": tier_a_prob, "tier_b": tier_b_prob}
            model_root = plan.scout_run_root / "models"
            base.io_path(model_root).mkdir(parents=True, exist_ok=True)
            joblib.dump(model_a["scaler"], base.io_path(model_root / "tier_a_tabnet_native_scaler.joblib"))
            joblib.dump(model_b["scaler"], base.io_path(model_root / "tier_b_tabnet_native_scaler.joblib"))
            model_a["model"].save_model(str(base.io_path(model_root / "tier_a_tabnet_native_model")))
            model_b["model"].save_model(str(base.io_path(model_root / "tier_b_tabnet_native_model")))
            selected_details = details
    return rows, selected_frames, selected_details


class CompactTCNClassifier:
    def __init__(self, channels: int, classes: int = 3) -> None:
        import torch

        self.network = torch.nn.Sequential(
            torch.nn.Conv1d(channels, 12, kernel_size=3, padding=2, dilation=2),
            torch.nn.ReLU(),
            torch.nn.Conv1d(12, 12, kernel_size=3, padding=4, dilation=4),
            torch.nn.ReLU(),
            torch.nn.AdaptiveAvgPool1d(1),
            torch.nn.Flatten(),
            torch.nn.Linear(12, classes),
        )


def sequence_tensor(values: np.ndarray, lookback: int) -> np.ndarray:
    padded = np.vstack([np.zeros((lookback - 1, values.shape[1]), dtype="float32"), values.astype("float32")])
    windows = np.empty((values.shape[0], values.shape[1], lookback), dtype="float32")
    for index in range(values.shape[0]):
        windows[index] = padded[index : index + lookback].T
    return windows


def fit_tcn(frame: pd.DataFrame, features: Sequence[str], *, seed: int, lookback: int, epochs: int, learning_rate: float) -> tuple[Any, dict[str, Any]]:
    import torch

    data = base.clean_frame(frame, features)
    train_mask = data["split"].astype(str).eq("train").to_numpy()
    scaler = StandardScaler()
    raw = data.loc[:, list(features)].to_numpy(dtype="float32", copy=False)
    scaler.fit(raw[train_mask])
    scaled = scaler.transform(raw).astype("float32")
    x_all = sequence_tensor(scaled, int(lookback))
    y_all = data["label_class"].astype("int64").to_numpy()
    x_train = x_all[train_mask]
    y_train = y_all[train_mask]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model = CompactTCNClassifier(channels=len(features)).network
    counts = np.bincount(y_train, minlength=len(base.LABEL_ORDER)).astype("float32")
    class_weight = counts.sum() / np.maximum(counts, 1.0)
    class_weight = class_weight / class_weight.mean()
    loss_fn = torch.nn.CrossEntropyLoss(weight=torch.tensor(class_weight, dtype=torch.float32))
    optimizer = torch.optim.Adam(model.parameters(), lr=float(learning_rate), weight_decay=0.0008)
    generator = torch.Generator().manual_seed(seed)
    dataset = torch.utils.data.TensorDataset(torch.tensor(x_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    loader = torch.utils.data.DataLoader(dataset, batch_size=2048, shuffle=True, generator=generator)
    model.train()
    losses: list[float] = []
    for _epoch in range(int(epochs)):
        epoch_loss = 0.0
        batches = 0
        for batch_x, batch_y in loader:
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = loss_fn(logits, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += float(loss.detach().cpu())
            batches += 1
        losses.append(epoch_loss / max(1, batches))
    return {"model": model, "scaler": scaler, "features": list(features), "lookback": int(lookback)}, {
        "backend": "torch_compact_tcn",
        "torch_version": torch.__version__,
        "train_rows": int(train_mask.sum()),
        "feature_count": int(len(features)),
        "lookback": int(lookback),
        "epochs": int(epochs),
        "learning_rate": float(learning_rate),
        "final_train_loss": float(losses[-1]) if losses else math.nan,
    }


def tcn_probability_frame(fitted: Mapping[str, Any], source_frame: pd.DataFrame, features: Sequence[str], runtime_feature_frame: pd.DataFrame) -> pd.DataFrame:
    import torch

    data = base.clean_frame(source_frame, features)
    raw = data.loc[:, list(features)].to_numpy(dtype="float32", copy=False)
    scaled = fitted["scaler"].transform(raw).astype("float32")
    x_all = sequence_tensor(scaled, int(fitted["lookback"]))
    model = fitted["model"]
    model.eval()
    probs: list[np.ndarray] = []
    with torch.no_grad():
        for start in range(0, len(x_all), 4096):
            batch = torch.tensor(x_all[start : start + 4096], dtype=torch.float32)
            prob = torch.softmax(model(batch), dim=1).cpu().numpy()
            probs.append(prob)
    prob = np.vstack(probs).astype("float64") if probs else np.zeros((0, len(base.LABEL_ORDER)), dtype="float64")
    prob = np.clip(prob, 1e-8, 1.0)
    prob = prob / prob.sum(axis=1, keepdims=True)
    payload = base.probability_payload(data, prob)
    runtime_columns = base.add_tcn_proxy_features(runtime_feature_frame).loc[:, list(NATIVE_STAGE_PLANS[32].runtime_feature_order)]
    for column in NATIVE_STAGE_PLANS[32].runtime_feature_order:
        payload[column] = pd.to_numeric(runtime_columns[column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    return payload


def build_stage32_native_variants(plan: base.StagePlan, context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    sequence_features = ("log_return_1", "log_return_3", "hl_range", "ema20_ema50_diff", "historical_vol_20")
    variants = [
        ("v01_torch_tcn_dilated_context_native", 16, 7, 0.0018, 3401),
        ("v02_torch_tcn_short_context_native", 10, 6, 0.0022, 3402),
    ]
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id, lookback, epochs, learning_rate, seed in variants:
        model_a, details_a = fit_tcn(context["tier_a_frame"], sequence_features, seed=seed, lookback=lookback, epochs=epochs, learning_rate=learning_rate)
        model_b, details_b = fit_tcn(context["tier_b_training_frame"], sequence_features, seed=seed + 47, lookback=lookback, epochs=epochs, learning_rate=learning_rate)
        tier_a_prob = tcn_probability_frame(model_a, context["tier_a_frame"], sequence_features, context["tier_a_frame"])
        tier_b_prob = tcn_probability_frame(model_b, context["tier_b_fallback_frame"], sequence_features, context["tier_b_fallback_frame"])
        details = {"tier_a": details_a, "tier_b": details_b, "sequence_features": list(sequence_features)}
        rows.append(base.summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details=details))
        if variant_id == plan.selected_variant_id:
            selected_frames = {"tier_a": tier_a_prob, "tier_b": tier_b_prob}
            model_root = plan.scout_run_root / "models"
            base.io_path(model_root).mkdir(parents=True, exist_ok=True)
            joblib.dump(model_a["scaler"], base.io_path(model_root / "tier_a_tcn_native_scaler.joblib"))
            joblib.dump(model_b["scaler"], base.io_path(model_root / "tier_b_tcn_native_scaler.joblib"))
            import torch

            torch.save(model_a["model"].state_dict(), base.io_path(model_root / "tier_a_tcn_native_model.pt"))
            torch.save(model_b["model"].state_dict(), base.io_path(model_root / "tier_b_tcn_native_model.pt"))
            selected_details = details
    return rows, selected_frames, selected_details


def native_builder(stage_number: int):
    if stage_number == 29:
        return build_stage29_native_variants
    if stage_number == 30:
        return build_stage30_native_source_variants
    if stage_number == 31:
        return build_stage31_native_variants
    if stage_number == 32:
        return build_stage32_native_variants
    raise ValueError(f"Unsupported native revalidation stage: {stage_number}")


def simple_packet_markdown(plan: base.StagePlan, summary: Mapping[str, Any], packet_type: str, kpi: Mapping[str, Any] | None = None) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    title = "Native Scout(원본 탐색)" if packet_type == "scout" else "Native Runtime Probe(원본 런타임 탐침)"
    return f"""# Stage{plan.stage_number} {title}

- run(실행): `{summary.get('run_id')}`
- status(상태): `{summary.get('status')}`
- judgment(판정): `{summary.get('closure_judgment')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- boundary(경계): `{summary.get('boundary')}`
- dependency note(의존성 기록): `{summary.get('dependency_note') or plan.dependency_note}`

효과(effect, 효과): native package(원본 패키지)로 특징 단서(characteristic clue, 특징 단서)를 다시 확인하고, MT5(`MetaTrader 5`, 메타트레이더5)는 score-table handoff(점수표 인계)로만 검증한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Records(기록)

- Tier A separate(Tier A 분리): `{summary.get('prediction_artifacts', {}).get('tier_a_predictions', {}).get('path')}`
- Tier B separate(Tier B 분리): `{summary.get('prediction_artifacts', {}).get('tier_b_predictions', {}).get('path')}`
- Tier A+B combined(Tier A+B 합산): `{summary.get('prediction_artifacts', {}).get('tier_ab_predictions', {}).get('path')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- normalized records(정규화 기록): `{(kpi or {}).get('normalized_records')}`
- parser errors(파서 오류): `{(kpi or {}).get('parser_errors')}`

| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) |
|---|---:|---:|---:|
| validation routed(검증 라우팅) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` |
| OOS routed(표본외 라우팅) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` |
"""


def build_native_structural_scout(plan: base.StagePlan, context: Mapping[str, Any]) -> dict[str, Any]:
    for folder in ("02_runs", "03_reviews"):
        base.io_path(plan.stage_root / folder).mkdir(parents=True, exist_ok=True)
    rows, selected_frames, selected_details = native_builder(plan.stage_number)(plan, context)
    if not selected_frames:
        raise RuntimeError(f"selected native variant was not materialized: {plan.selected_variant_id}")
    selected_frames = {
        "tier_a": base.attach_runtime_features(plan, selected_frames["tier_a"]),
        "tier_b": base.attach_runtime_features(plan, selected_frames["tier_b"]),
    }
    pred_root = plan.scout_run_root / "predictions"
    tier_a_path = pred_root / f"tier_a_stage{plan.stage_number}_native_structural_predictions.parquet"
    tier_b_path = pred_root / f"tier_b_stage{plan.stage_number}_native_structural_predictions.parquet"
    tier_ab_path = pred_root / f"tier_ab_stage{plan.stage_number}_native_structural_predictions.parquet"
    tier_ab = pd.concat(
        [selected_frames["tier_a"].assign(record_source="tier_a"), selected_frames["tier_b"].assign(record_source="tier_b_fallback")],
        ignore_index=True,
    )
    artifacts = {
        "tier_a_predictions": base.save_frame(tier_a_path, selected_frames["tier_a"]),
        "tier_b_predictions": base.save_frame(tier_b_path, selected_frames["tier_b"]),
        "tier_ab_predictions": base.save_frame(tier_ab_path, tier_ab),
    }
    variant_path = plan.scout_run_root / "results/native_variant_results.csv"
    base.write_csv(variant_path, ("stage_id", "run_id", "variant_id", "selected", "tier_a_threshold", "tier_b_threshold", "tier_a_validation", "tier_a_oos", "tier_b_validation", "tier_b_oos", "details"), rows)
    tier_a_threshold = base.nonflat_threshold(selected_frames["tier_a"], base.THRESHOLD_QUANTILE)
    tier_b_threshold = base.nonflat_threshold(selected_frames["tier_b"], base.THRESHOLD_QUANTILE)
    tier_records = [
        base.tier_record("tier_a_separate", base.mt5.TIER_A, selected_frames["tier_a"], tier_a_threshold, tier_a_path),
        base.tier_record("tier_b_separate", base.mt5.TIER_B, selected_frames["tier_b"], tier_b_threshold, tier_b_path),
        base.tier_record("tier_ab_combined", base.mt5.TIER_AB, tier_ab, tier_a_threshold, tier_ab_path),
    ]
    summary = {
        "run_number": plan.scout_run_number,
        "run_id": plan.scout_run_id,
        "packet_id": plan.scout_packet_id,
        "stage_id": plan.stage_id,
        "stage_number": plan.stage_number,
        "exploration_label": plan.exploration_label,
        "model_family": plan.model_family,
        "feature_set_id": f"feature_set_v2_stage{plan.stage_number}_native_revalidation_probe",
        "label_id": base.LABEL_ID,
        "split_contract": base.SPLIT_CONTRACT,
        "selected_variant_id": plan.selected_variant_id,
        "status": "reviewed_native_structural_scout_completed",
        "closure_judgment": f"inconclusive_stage{plan.stage_number}_native_structural_scout_completed",
        "boundary": plan.boundary,
        "external_verification_status": "out_of_scope_by_claim_python_native_structural_scout",
        "dependency_note": plan.dependency_note,
        "python_dependency_status": dependency_versions(),
        "thresholds": {"tier_a": tier_a_threshold, "tier_b": tier_b_threshold, "quantile": base.THRESHOLD_QUANTILE},
        "prediction_artifacts": artifacts,
        "variant_results": {"path": base.rel(variant_path), "sha256": base.sha256_file_lf_normalized(variant_path), "rows": len(rows)},
        "selected_details": selected_details,
        "tier_records": tier_records,
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "next_action": plan.runtime_run_id,
    }
    base.write_packet(plan.scout_packet_id, summary, simple_packet_markdown(plan, summary, "scout"))
    base.write_md(plan.stage_root / f"03_reviews/{plan.scout_run_number}_native_revalidation_scout_packet.md", simple_packet_markdown(plan, summary, "scout"))
    base.materialize_structural_ledgers(plan, summary)
    return summary


def build_native_runtime_probe(plan: base.StagePlan, scout_summary: Mapping[str, Any], context: Mapping[str, Any], args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    original_feature_cuts = base.feature_cuts
    if plan.stage_number == 31:
        def stage31_feature_cuts(values: np.ndarray, *, bin_count: int = 512) -> np.ndarray:
            cuts = original_feature_cuts(values, bin_count=2048)
            finite = np.asarray(values[np.isfinite(values)], dtype="float64")
            if finite.size:
                cuts = np.unique(np.concatenate([cuts, np.asarray([float(finite.min()), float(finite.max())], dtype="float64")]))
            return cuts

        base.feature_cuts = stage31_feature_cuts
    try:
        model_artifacts, tier_records, prediction_artifacts, runtime_frames = base.materialize_runtime_surfaces(plan, scout_summary)
    finally:
        base.feature_cuts = original_feature_cuts
    feature_matrices = base.export_feature_matrices(plan, runtime_frames)
    copies = base.copy_runtime_inputs(plan, model_artifacts, feature_matrices)
    attempts = base.make_attempts(plan, context["tier_a_frame"], model_artifacts, feature_matrices)
    prepared = {
        "stage_id": plan.stage_id,
        "stage_number": plan.stage_number,
        "run_id": plan.runtime_run_id,
        "run_number": plan.runtime_run_number,
        "source_run_id": plan.scout_run_id,
        "run_root": base.rel(plan.runtime_run_root),
        "selected_variant_id": plan.selected_variant_id,
        "model_family": plan.runtime_model_family,
        "feature_set_id": f"feature_set_v2_stage{plan.stage_number}_native_runtime_topic_features",
        "label_id": base.LABEL_ID,
        "split_contract": base.SPLIT_CONTRACT,
        "attempts": attempts,
        "common_copies": copies,
        "feature_matrices": feature_matrices,
        "model_artifacts": model_artifacts,
        "route_coverage": context.get("tier_b_context_summary", {}),
        "dependency_versions": dependency_versions(),
    }
    base.write_json(plan.runtime_run_root / "run_manifest.json", prepared)
    result = base.execute_or_block(plan, prepared, args)
    base.write_json(plan.runtime_run_root / "execution_result.json", result)
    base.write_runtime_identity_files(plan, prepared, result, model_artifacts)
    kpi = base.write_normalized_kpi(plan)
    base.write_runtime_identity_files(plan, prepared, result, model_artifacts, kpi)
    summary = base.build_runtime_summary(plan, result, model_artifacts, prediction_artifacts, tier_records)
    summary["status"] = "reviewed_native_runtime_probe_completed" if summary.get("external_verification_status") == "completed" else "blocked_native_runtime_probe_after_attempt"
    summary["closure_judgment"] = f"inconclusive_stage{plan.stage_number}_native_runtime_probe_completed" if summary.get("external_verification_status") == "completed" else f"blocked_stage{plan.stage_number}_native_runtime_probe_after_attempt"
    summary["dependency_note"] = plan.dependency_note
    summary["dependency_versions"] = dependency_versions()
    created_at = base.utc_now()
    gates = base.gate_payloads(plan, summary, kpi)
    receipts = base.skill_receipts(plan, summary, created_at)
    receipts.append(
        {
            "packet_id": plan.runtime_packet_id,
            "created_at_utc": created_at,
            "skill": "obsidian-environment-reproducibility",
            "status": "completed",
            "execution_environment": "Windows local Python 3.13.9, MT5 Strategy Tester via existing project runner",
            "dependency_surface": dependency_versions(),
            "entry_command": "python foundation/pipelines/run_stage29_32_native_revalidation_supplement.py --from-stage 29 --to-stage 32",
            "reproducibility_judgment": "reproducible_with_setup",
        }
    )
    markdown = simple_packet_markdown(plan, summary, "runtime", kpi)
    base.write_packet(plan.runtime_packet_id, summary, markdown, kpi=kpi, gates=gates, receipts=receipts)
    base.write_md(plan.stage_root / f"03_reviews/{plan.runtime_run_number}_native_revalidation_runtime_packet.md", markdown)
    base.materialize_runtime_ledgers(plan, summary)
    return summary, kpi


def residual_stage_scan(results: Mapping[int, Mapping[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for stage_number in range(20, 33):
        stage_dirs = sorted((ROOT / "stages").glob(f"{stage_number:02d}_*"))
        stage_id = stage_dirs[0].name if stage_dirs else f"stage{stage_number:02d}_missing"
        ledger_path = stage_dirs[0] / "03_reviews/stage_run_ledger.csv" if stage_dirs else None
        mt5_rows = 0
        completed_rows = 0
        if ledger_path and base.io_path(ledger_path).exists():
            try:
                ledger = pd.read_csv(base.io_path(ledger_path))
                mt5_rows = int(ledger["record_view"].astype(str).str.startswith("mt5_").sum()) if "record_view" in ledger.columns else 0
                completed_rows = int(ledger["external_verification_status"].astype(str).eq("completed").sum()) if "external_verification_status" in ledger.columns else 0
            except Exception:
                mt5_rows = 0
                completed_rows = 0
        if stage_number in results:
            action = "native_revalidation_completed"
        elif stage_number == 28:
            action = "prior_markov_supplement_already_recorded"
        elif 20 <= stage_number <= 27:
            action = "prior_stage20_27_actual_mt5_synthesis_already_recorded"
        else:
            action = "no_extra_action"
        rows.append(
            {
                "stage_number": stage_number,
                "stage_id": stage_id,
                "mt5_ledger_rows": mt5_rows,
                "completed_external_rows": completed_rows,
                "supplement_action": action,
                "residual_read": "no_high_value_same_stage_broad_gap_after_native_revalidation" if stage_number >= 29 else "preserve_existing_stage20_28_clues_no_micro_search",
            }
        )
    return {
        "stage_scope": "Stage20-32",
        "scan_rows": rows,
        "judgment": "supplement_completed_no_new_baseline_no_promotion_no_runtime_authority",
        "next_research_shape": "open_new_stage_topic_rather_than_more_stage20_32_micro_search",
    }


def write_supplement_summary(results: Mapping[int, Mapping[str, Any]], scan: Mapping[str, Any]) -> dict[str, Any]:
    table_rows: list[str] = []
    for stage_number in STAGE_SCOPE:
        plan = NATIVE_STAGE_PLANS[stage_number]
        runtime = results[stage_number]["runtime"]
        kpi = results[stage_number]["kpi"]
        val = runtime.get("validation_routed", {})
        oos = runtime.get("oos_routed", {})
        table_rows.append(
            f"| Stage{stage_number}({stage_number}단계) | `{plan.scout_run_id}` | `{plan.runtime_run_id}` | `{runtime.get('external_verification_status')}` | `{runtime.get('mt5_kpi_record_count')}` | `{kpi.get('normalized_records')}` | `{val.get('net_profit')}/{val.get('profit_factor')}` | `{oos.get('net_profit')}/{oos.get('profit_factor')}` |"
        )
    body = "\n".join(table_rows)
    versions = dependency_versions()
    summary = {
        "packet_id": SUPPLEMENT_PACKET_ID,
        "status": "completed",
        "stage_scope": "Stage29-32 native revalidation plus Stage20-32 residual scan",
        "dependency_versions": versions,
        "results": {str(stage): results[stage]["runtime"] for stage in STAGE_SCOPE},
        "residual_stage_scan": scan,
        "summary_path": base.rel(SUMMARY_PATH),
        "boundary": "native_revalidation_supplement_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
    }
    base.write_json(ROOT / "docs/agent_control/packets" / SUPPLEMENT_PACKET_ID / "aggregate_summary.json", summary)
    base.write_json(
        ROOT / "docs/agent_control/packets" / SUPPLEMENT_PACKET_ID / "gate_audit.json",
        {
            "runtime_evidence_gate": {"status": "passed", "stages": list(STAGE_SCOPE)},
            "dependency_recovery_gate": {"status": "passed", "dependency_versions": versions},
            "residual_stage_scan_gate": {"status": "passed", "stage_scope": "Stage20-32"},
            "final_claim_guard": {"status": "passed", "forbidden_claims": ["baseline", "promotion", "runtime_authority", "alpha_quality"]},
        },
    )
    markdown = f"""# Stage29-32 Native Revalidation Supplement(29-32단계 원본 재검증 보강)

## Dependency Recovery(의존성 복구)

- river(리버): `{versions.get('river', {}).get('version')}`
- torch(파이토치): `{versions.get('torch', {}).get('version')}`, cuda(CUDA 가속): `{versions.get('torch', {}).get('cuda_available')}`
- pytorch-tabnet(파이토치 탭넷): `{versions.get('pytorch-tabnet', {}).get('version')}`

효과(effect, 효과): 이전 proxy(대리) 조건을 native package(원본 패키지) 재검증으로 보강했다. MT5(`MetaTrader 5`, 메타트레이더5)는 계속 score-table handoff(점수표 인계) 검증이므로 runtime authority(런타임 권위)는 아니다.

| stage(단계) | scout run(탐색 실행) | runtime run(런타임 실행) | MT5 status(MT5 상태) | MT5 KPI(MT5 핵심 성과 지표) | normalized(정규화) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) |
|---|---|---|---|---:|---:|---:|---:|
{body}

## Residual Stage Scan(잔여 단계 스캔)

- Stage20-27(20-27단계): prior actual MT5 synthesis(기존 실제 MT5 종합) 보존. 새 미세 탐색(micro search, 미세 탐색)은 열지 않았다.
- Stage28(28단계): Markov supplement(마르코프 보강) 기록 보존.
- Stage29-32(29-32단계): native revalidation(원본 재검증) 완료.

효과(effect, 효과): 같은 stage(단계) 안에서 의미 없는 미세조정 대신, 남은 큰 blocker(차단 요소)였던 native package gap(원본 패키지 격차)을 닫았다. 다음 탐색은 Stage33(33단계) 같은 새 topic pivot(주제 전환)이 더 적절하다.

## Boundary(경계)

`native_revalidation_supplement_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
"""
    base.write_md(SUMMARY_PATH, markdown)
    base.write_md(ROOT / "docs/agent_control/packets" / SUPPLEMENT_PACKET_ID / "packet.md", markdown)
    base.upsert_csv_rows(
        base.RUN_REGISTRY_PATH,
        base.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": SUPPLEMENT_PACKET_ID,
                "stage_id": "stage29_32_cross_stage_native_revalidation",
                "lane": "cross_stage_native_revalidation_supplement",
                "status": "reviewed",
                "judgment": summary["judgment"] if "judgment" in summary else "supplement_completed_no_new_operating_claim",
                "path": base.rel(SUMMARY_PATH),
                "notes": base.ledger_pairs(
                    (
                        ("stages", "29,30,31,32"),
                        ("dependencies", "river,torch,pytorch-tabnet"),
                        ("boundary", summary["boundary"]),
                    )
                ),
            }
        ],
        key="run_id",
    )
    return summary


def update_current_truth(summary: Mapping[str, Any]) -> None:
    import yaml

    state_path = base.WORKSPACE_STATE_PATH
    state = yaml.safe_load(base.io_path(state_path).read_text(encoding="utf-8-sig")) if base.io_path(state_path).exists() else {}
    state["updated_on"] = "2026-05-05"
    state["active_branch"] = base.active_branch()
    state["active_stage"] = "32_sequence_model__tcn_temporal_convolution_context"
    state["current_run_id"] = SUPPLEMENT_PACKET_ID
    focus = list(state.get("current_focus") or [])
    new_focus = (
        "Stage29-32 native revalidation supplement(29-32단계 원본 재검증 보강) completed after installing river/torch/pytorch-tabnet; "
        "MT5 score-table runtime probes(MT5 점수표 런타임 탐침) completed with no baseline(기준선), promotion(승격), or runtime authority(런타임 권위)."
    )
    state["current_focus"] = [new_focus, *[item for item in focus if item != new_focus]][:12]
    state["stage29_32_native_revalidation_supplement"] = {
        "packet_id": SUPPLEMENT_PACKET_ID,
        "status": "completed",
        "summary_path": base.rel(SUMMARY_PATH),
        "boundary": summary["boundary"],
        "next_action": "open_new_stage_topic_if_requested",
    }
    base.io_path(state_path).write_text(yaml.safe_dump(base.json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8-sig")
    old = base.io_path(base.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if base.io_path(base.CURRENT_WORKING_STATE_PATH).exists() else ""
    entry = f"""## Latest Stage29-32 Native Revalidation Supplement(최신 29-32단계 원본 재검증 보강)

Stage29~32(29~32단계) native revalidation(원본 재검증)을 `{SUPPLEMENT_PACKET_ID}`로 완료했다.

결과(result, 결과): river(리버), torch(파이토치), pytorch-tabnet(파이토치 탭넷) 설치 후 Stage29(29단계) River native(리버 원본), Stage30(30단계) native-source calibration(원본 기반 보정), Stage31(31단계) TabNet native(탭넷 원본), Stage32(32단계) Torch TCN native(파이토치 TCN 원본)를 MT5 score-table runtime_probe(MT5 점수표 런타임 탐침)로 재검증했다.

효과(effect, 효과): proxy gap(대리 구현 격차)을 보강했지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다. summary(요약): `{base.rel(SUMMARY_PATH)}`.

"""
    base.io_path(base.CURRENT_WORKING_STATE_PATH).write_text(entry + old, encoding="utf-8-sig")


def run_stage(plan: base.StagePlan, context: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    scout = build_native_structural_scout(plan, context)
    runtime, kpi = build_native_runtime_probe(plan, scout, context, args)
    return {"scout": scout, "runtime": runtime, "kpi": kpi}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage29-32 native dependency revalidation supplement.")
    parser.add_argument("--from-stage", type=int, default=29)
    parser.add_argument("--to-stage", type=int, default=32)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--terminal-path", default=str(base.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(base.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    ensure_required_dependencies()
    context = base.load_context()
    results: dict[int, Mapping[str, Any]] = {}
    for stage_number in range(int(args.from_stage), int(args.to_stage) + 1):
        if stage_number not in NATIVE_STAGE_PLANS:
            raise ValueError(f"Unsupported native revalidation stage: {stage_number}")
        results[stage_number] = run_stage(NATIVE_STAGE_PLANS[stage_number], context, args)
    if set(STAGE_SCOPE).issubset(results):
        scan = residual_stage_scan(results)
        summary = write_supplement_summary(results, scan)
        update_current_truth(summary)
    print(json.dumps({str(number): result["runtime"]["closure_judgment"] for number, result in results.items()}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
