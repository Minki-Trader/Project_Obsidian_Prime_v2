from __future__ import annotations

import hashlib
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


def export_sklearn_to_onnx_zipmap_disabled(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
    input_name: str = "float_input",
    target_opset: int = 12,
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
    probability_outputs = [
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
        "outputs": outputs,
        "probability_output_name": probability_outputs[0] if probability_outputs else outputs[-1]["name"],
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
