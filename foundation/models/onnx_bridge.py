from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from foundation.control_plane.ledger import io_path
from foundation.models.baseline_training import LABEL_ORDER


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(names: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()


def classifier_classes(model: Any) -> list[int]:
    if hasattr(model, "named_steps"):
        for step in reversed(list(model.named_steps.values())):
            if hasattr(step, "classes_"):
                return [int(value) for value in step.classes_]
    if hasattr(model, "classes_"):
        return [int(value) for value in model.classes_]
    raise ValueError("Model does not expose classes_.")


def ordered_sklearn_probabilities(
    model: Any,
    values: np.ndarray,
    class_order: Sequence[int] = LABEL_ORDER,
) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = classifier_classes(model)
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    ordered = np.zeros((raw.shape[0], len(class_order)), dtype="float64")
    for output_index, label in enumerate(class_order):
        if int(label) not in class_to_index:
            raise ValueError(f"Model is missing class {label}; cannot build fixed probability order.")
        ordered[:, output_index] = raw[:, class_to_index[int(label)]]
    return ordered


def _onnx_options_for_model(model: Any) -> dict[int, dict[str, Any]]:
    options = {id(model): {"zipmap": False}}
    if hasattr(model, "named_steps"):
        for step in model.named_steps.values():
            if hasattr(step, "predict_proba"):
                options[id(step)] = {"zipmap": False}
    return options


def _onnx_output_shape(output: Any) -> list[Any]:
    tensor_type = output.type.tensor_type
    dims: list[Any] = []
    for dim in tensor_type.shape.dim:
        if dim.dim_value:
            dims.append(int(dim.dim_value))
        elif dim.dim_param:
            dims.append(str(dim.dim_param))
        else:
            dims.append(None)
    return dims


def _patch_onnxmltools_xgboost_dart_config() -> None:
    """Teach the local onnxmltools converter to read DART's nested gbtree config."""

    import onnxmltools.convert.xgboost.common as xgb_common
    import onnxmltools.convert.xgboost.operator_converters.XGBoost as xgb_converter
    import onnxmltools.convert.xgboost.shape_calculators.Classifier as xgb_classifier_shape

    def get_xgb_params(xgb_node: Any) -> dict[str, Any]:
        if hasattr(xgb_node, "get_xgb_params"):
            params = xgb_node.get_xgb_params()
        else:
            params = dict(getattr(xgb_node, "__dict__", {}))

        if hasattr(xgb_node, "get_booster"):
            config = json.loads(xgb_node.get_booster().save_config())
        else:
            config = json.loads(xgb_node.save_config())

        params = {key: value for key, value in params.items() if value is not None}
        learner = config["learner"]
        model_params = learner["learner_model_param"]
        num_class = int(model_params["num_class"])
        if num_class > 0:
            params["num_class"] = num_class
        if "n_estimators" not in params and getattr(xgb_node, "n_estimators", None) is not None:
            params["n_estimators"] = xgb_node.n_estimators

        base_score_raw = model_params.get("base_score")
        if base_score_raw:
            if base_score_raw.startswith("[") and base_score_raw.endswith("]"):
                params["base_score"] = [float(value) for value in json.loads(base_score_raw)]
            else:
                params["base_score"] = [float(base_score_raw)]

        params["n_targets"] = int(model_params.get("num_target", 1))
        booster_params = learner.get("gradient_booster", {})
        gbtree_params = booster_params.get("gbtree_model_param") or booster_params.get("gbtree", {}).get("gbtree_model_param")
        if gbtree_params and "num_trees" in gbtree_params:
            params["best_ntree_limit"] = int(gbtree_params["num_trees"])
        return params

    def scale_leaf_values(node: dict[str, Any], scale: float) -> None:
        if "leaf" in node:
            node["leaf"] = float(node["leaf"]) * float(scale)
        for child in node.get("children", []) or []:
            scale_leaf_values(child, scale)

    xgb_common.get_xgb_params = get_xgb_params
    xgb_converter.get_xgb_params = get_xgb_params
    xgb_classifier_shape.get_xgb_params = get_xgb_params
    if not getattr(xgb_converter.XGBConverter, "_obsidian_dart_weight_patch", False):
        original_common_members = xgb_converter.XGBConverter.common_members

        def common_members(xgb_node: Any, inputs: Any) -> tuple[Any, Any, Any, Any]:
            objective, base_score, js_trees, best_ntree_limit = original_common_members(xgb_node, inputs)
            if not hasattr(xgb_node, "get_booster"):
                return objective, base_score, js_trees, best_ntree_limit
            try:
                raw = xgb_node.get_booster().save_raw(raw_format="json")
                model_json = json.loads(raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw)
            except Exception:
                return objective, base_score, js_trees, best_ntree_limit
            weights = model_json.get("learner", {}).get("gradient_booster", {}).get("weight_drop") or []
            if weights and len(weights) == len(js_trees):
                for tree, weight in zip(js_trees, weights):
                    scale_leaf_values(tree, float(weight))
            return objective, base_score, js_trees, best_ntree_limit

        xgb_converter.XGBConverter.common_members = staticmethod(common_members)
        xgb_converter.XGBConverter._obsidian_dart_weight_patch = True


def export_sklearn_to_onnx_zipmap_disabled(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
    input_name: str = "float_input",
    target_opset: int = 12,
    drop_label_output: bool = False,
) -> dict[str, Any]:
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType

    onnx_model = convert_sklearn(
        model,
        initial_types=[(input_name, FloatTensorType([None, int(feature_count)]))],
        options=_onnx_options_for_model(model),
        target_opset=target_opset,
    )
    non_tensor_outputs = [
        output.name for output in onnx_model.graph.output if output.type.WhichOneof("value") != "tensor_type"
    ]
    if non_tensor_outputs:
        raise RuntimeError(f"ONNX export produced non-tensor outputs, zipmap may be enabled: {non_tensor_outputs}")
    outputs_before = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
            "shape": _onnx_output_shape(output),
        }
        for output in onnx_model.graph.output
    ]
    probability_outputs = [
        item["name"]
        for item in outputs_before
        if len(item["shape"]) == 2 and item["shape"][-1] in {len(LABEL_ORDER), "N"}
    ]
    if drop_label_output and probability_outputs:
        keep_name = probability_outputs[0]
        keep_outputs = [output for output in onnx_model.graph.output if output.name == keep_name]
        del onnx_model.graph.output[:]
        onnx_model.graph.output.extend(keep_outputs)

    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(output_path).write_bytes(onnx_model.SerializeToString())
    outputs = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
            "shape": _onnx_output_shape(output),
        }
        for output in onnx_model.graph.output
    ]
    final_probability_outputs = [
        item["name"]
        for item in outputs
        if len(item["shape"]) == 2 and item["shape"][-1] in {len(LABEL_ORDER), "N"}
    ]
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "input_name": input_name,
        "target_opset": target_opset,
        "zipmap_disabled": True,
        "label_output_dropped": bool(drop_label_output and probability_outputs),
        "outputs_before_drop": outputs_before,
        "outputs": outputs,
        "probability_output_name": final_probability_outputs[0] if final_probability_outputs else outputs[-1]["name"],
    }


def export_xgboost_classifier_to_onnx(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
    input_name: str = "float_input",
    target_opset: int = 13,
    drop_label_output: bool = True,
) -> dict[str, Any]:
    _patch_onnxmltools_xgboost_dart_config()
    from onnxmltools.convert import convert_xgboost
    from onnxmltools.convert.common.data_types import FloatTensorType

    onnx_model = convert_xgboost(
        model,
        initial_types=[(input_name, FloatTensorType([None, int(feature_count)]))],
        target_opset=target_opset,
    )
    outputs_before = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
            "shape": _onnx_output_shape(output),
        }
        for output in onnx_model.graph.output
    ]
    probability_outputs = [
        item["name"]
        for item in outputs_before
        if len(item["shape"]) == 2 and item["shape"][-1] in {len(LABEL_ORDER), "N"}
    ]
    if drop_label_output and probability_outputs:
        keep_name = probability_outputs[0]
        keep_outputs = [output for output in onnx_model.graph.output if output.name == keep_name]
        del onnx_model.graph.output[:]
        onnx_model.graph.output.extend(keep_outputs)

    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(output_path).write_bytes(onnx_model.SerializeToString())
    outputs = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
            "shape": _onnx_output_shape(output),
        }
        for output in onnx_model.graph.output
    ]
    final_probability_outputs = [
        item["name"]
        for item in outputs
        if len(item["shape"]) == 2 and item["shape"][-1] in {len(LABEL_ORDER), "N"}
    ]
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "input_name": input_name,
        "target_opset": target_opset,
        "zipmap_disabled": True,
        "label_output_dropped": bool(drop_label_output and probability_outputs),
        "outputs_before_drop": outputs_before,
        "outputs": outputs,
        "probability_output_name": final_probability_outputs[0] if final_probability_outputs else outputs[-1]["name"],
    }


def export_catboost_classifier_to_onnx(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
    target_opset: int = 13,
    drop_label_output: bool = True,
) -> dict[str, Any]:
    """Export CatBoost and expose the probability tensor instead of ZipMap."""

    import onnx
    from onnx import TensorProto, helper

    raw_path = output_path.with_suffix(".raw.onnx")
    io_path(raw_path.parent).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_raw_path = Path(tmp_dir) / "catboost.raw.onnx"
        temp_output_path = Path(tmp_dir) / "catboost.tensor.onnx"
        model.save_model(
            str(temp_raw_path),
            format="onnx",
            export_parameters={
                "onnx_domain": "ai.catboost",
                "onnx_model_version": 1,
                "onnx_doc_string": "Project Obsidian Prime v2 CatBoost runtime probe",
                "onnx_graph_name": "CatBoostModel",
            },
        )
        io_path(raw_path).write_bytes(temp_raw_path.read_bytes())
        onnx_model = onnx.load(str(temp_raw_path))
        outputs_before = [
            {
                "name": output.name,
                "value_type": output.type.WhichOneof("value"),
                "shape": _onnx_output_shape(output) if output.type.WhichOneof("value") == "tensor_type" else [],
            }
            for output in onnx_model.graph.output
        ]
        zipmap_nodes = [node for node in onnx_model.graph.node if node.op_type == "ZipMap"]
        if len(zipmap_nodes) != 1:
            raise RuntimeError(f"Expected exactly one CatBoost ZipMap node, found {len(zipmap_nodes)}.")
        probability_name = zipmap_nodes[0].input[0]

        kept_nodes = [node for node in onnx_model.graph.node if node is not zipmap_nodes[0]]
        del onnx_model.graph.node[:]
        onnx_model.graph.node.extend(kept_nodes)

        label_outputs = [output for output in onnx_model.graph.output if output.name == "label"]
        del onnx_model.graph.output[:]
        if not drop_label_output and label_outputs:
            onnx_model.graph.output.extend(label_outputs[:1])
        onnx_model.graph.output.extend(
            [helper.make_tensor_value_info(probability_name, TensorProto.FLOAT, [None, len(LABEL_ORDER)])]
        )
        onnx.checker.check_model(onnx_model)
        onnx.save(onnx_model, str(temp_output_path))
        io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
        io_path(output_path).write_bytes(temp_output_path.read_bytes())
    outputs = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
            "shape": _onnx_output_shape(output),
        }
        for output in onnx_model.graph.output
    ]
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "raw_path": raw_path.as_posix(),
        "raw_sha256": sha256_file(raw_path),
        "input_name": "features",
        "target_opset": target_opset,
        "zipmap_removed": True,
        "label_output_dropped": bool(drop_label_output),
        "outputs_before_drop": outputs_before,
        "outputs": outputs,
        "probability_output_name": probability_name,
    }


def _find_probability_output(outputs: Sequence[np.ndarray], class_count: int) -> np.ndarray:
    candidates = [
        output
        for output in outputs
        if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == class_count
    ]
    if len(candidates) != 1:
        shapes = [getattr(output, "shape", None) for output in outputs]
        raise RuntimeError(f"Expected one probability output with {class_count} columns; got shapes {shapes}.")
    return np.asarray(candidates[0], dtype="float64")


def check_onnxruntime_probability_parity(
    model: Any,
    onnx_path: Path,
    values: np.ndarray,
    *,
    class_order: Sequence[int] = LABEL_ORDER,
    tolerance: float = 1e-5,
) -> dict[str, Any]:
    import onnxruntime as ort

    classes = classifier_classes(model)
    if list(classes) != [int(label) for label in class_order]:
        raise ValueError(f"Model class order {classes} does not match expected class order {list(class_order)}.")
    X = np.asarray(values, dtype="float32")
    expected = ordered_sklearn_probabilities(model, X.astype("float64"), class_order=class_order)
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: X})
    actual = _find_probability_output(outputs, len(class_order))
    diff = np.abs(actual - expected)
    row_sum_error = np.abs(actual.sum(axis=1) - 1.0)
    return {
        "passed": bool(float(diff.max()) <= tolerance),
        "rows": int(X.shape[0]),
        "class_order": [int(label) for label in class_order],
        "tolerance": float(tolerance),
        "max_abs_diff": float(diff.max()),
        "mean_abs_diff": float(diff.mean()),
        "onnx_row_sum_max_abs_error": float(row_sum_error.max()) if len(row_sum_error) else 0.0,
        "input_name": input_name,
        "output_names": [output.name for output in session.get_outputs()],
    }
