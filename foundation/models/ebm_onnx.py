from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import numpy as np

from foundation.control_plane.ledger import io_path
from foundation.models.baseline_training import LABEL_ORDER
from foundation.models.onnx_bridge import ordered_sklearn_probabilities, sha256_file


def _validate_main_effects(model: Any, feature_count: int) -> None:
    if str(getattr(model, "link_", "")) != "mlogit":
        raise ValueError("Only multiclass mlogit EBM models are supported.")
    classes = [int(value) for value in getattr(model, "classes_", [])]
    if classes != list(LABEL_ORDER):
        raise ValueError(f"EBM class order mismatch: {classes} != {list(LABEL_ORDER)}")
    if len(getattr(model, "term_features_", [])) != len(getattr(model, "term_scores_", [])):
        raise ValueError("EBM term feature/score length mismatch.")
    for term_features in model.term_features_:
        if len(tuple(term_features)) != 1:
            raise ValueError("Only main-effect EBM terms can be exported to this runtime ONNX graph.")
        feature_index = int(tuple(term_features)[0])
        if feature_index < 0 or feature_index >= int(feature_count):
            raise ValueError(f"EBM feature index is outside input width: {feature_index}")


def export_ebm_main_effects_to_onnx(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
    input_name: str = "float_input",
    target_opset: int = 13,
) -> dict[str, Any]:
    """Export a main-effect multiclass EBM as an ONNX scoring graph.

    The graph mirrors EBM's additive score calculation:
    feature bin lookup -> class score sum -> intercept -> softmax.
    """

    import onnx
    from onnx import TensorProto, helper, numpy_helper

    _validate_main_effects(model, feature_count)

    nodes = []
    initializers = [
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), "axes_unsqueeze_1"),
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), "axes_reduce_1"),
        numpy_helper.from_array(np.asarray(1, dtype=np.int64), "one_i64"),
    ]

    running_score: str | None = None
    for term_index, term_features in enumerate(model.term_features_):
        feature_index = int(tuple(term_features)[0])
        column_index = f"feature_index_{term_index}"
        column = f"feature_column_{term_index}"
        column_2d = f"feature_column_2d_{term_index}"
        cuts_name = f"cuts_{term_index}"
        comparison = f"bin_comparison_{term_index}"
        comparison_i64 = f"bin_comparison_i64_{term_index}"
        bin_count = f"bin_count_{term_index}"
        bin_index = f"bin_index_{term_index}"
        score_table = f"score_table_{term_index}"
        term_score = f"term_score_{term_index}"

        cuts = np.asarray(model.bins_[feature_index][0], dtype=np.float32)
        scores = np.asarray(model.term_scores_[term_index], dtype=np.float32)
        initializers.extend(
            [
                numpy_helper.from_array(np.asarray(feature_index, dtype=np.int64), column_index),
                numpy_helper.from_array(cuts, cuts_name),
                numpy_helper.from_array(scores, score_table),
            ]
        )
        nodes.extend(
            [
                helper.make_node("Gather", [input_name, column_index], [column], axis=1),
                helper.make_node("Unsqueeze", [column, "axes_unsqueeze_1"], [column_2d]),
                helper.make_node("Greater", [column_2d, cuts_name], [comparison]),
                helper.make_node("Cast", [comparison], [comparison_i64], to=TensorProto.INT64),
                helper.make_node("ReduceSum", [comparison_i64, "axes_reduce_1"], [bin_count], keepdims=0),
                helper.make_node("Add", [bin_count, "one_i64"], [bin_index]),
                helper.make_node("Gather", [score_table, bin_index], [term_score], axis=0),
            ]
        )
        if running_score is None:
            initializers.append(numpy_helper.from_array(np.asarray(model.intercept_, dtype=np.float32), "intercept"))
            running_score = f"score_sum_{term_index}"
            nodes.append(helper.make_node("Add", [term_score, "intercept"], [running_score]))
        else:
            next_score = f"score_sum_{term_index}"
            nodes.append(helper.make_node("Add", [running_score, term_score], [next_score]))
            running_score = next_score

    if running_score is None:
        raise ValueError("EBM model has no terms to export.")

    nodes.append(helper.make_node("Softmax", [running_score], ["probabilities"], axis=1))
    graph = helper.make_graph(
        nodes,
        "ObsidianPrimeEbmMainEffects",
        [helper.make_tensor_value_info(input_name, TensorProto.FLOAT, [None, int(feature_count)])],
        [helper.make_tensor_value_info("probabilities", TensorProto.FLOAT, [None, len(LABEL_ORDER)])],
        initializers,
    )
    onnx_model = helper.make_model(
        graph,
        opset_imports=[helper.make_operatorsetid("", int(target_opset))],
        producer_name="Project Obsidian Prime v2 EBM exporter",
    )
    onnx_model.ir_version = 7
    onnx.checker.check_model(onnx_model)
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    onnx.save(onnx_model, str(io_path(output_path)))
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "input_name": input_name,
        "target_opset": int(target_opset),
        "zipmap_disabled": True,
        "export_policy": "main_effect_terms_additive_softmax",
        "probability_output_name": "probabilities",
        "outputs": [{"name": "probabilities", "value_type": "tensor_type", "shape": [None, len(LABEL_ORDER)]}],
    }


def check_ebm_onnx_probability_parity(
    model: Any,
    onnx_path: Path,
    values: np.ndarray,
    *,
    tolerance: float = 5.0e-4,
) -> dict[str, Any]:
    import onnxruntime as ort

    values32 = np.asarray(values, dtype=np.float32)
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    onnx_prob = np.asarray(session.run(None, {input_name: values32})[0], dtype=np.float64)
    sklearn_prob = ordered_sklearn_probabilities(model, values32.astype("float64"))
    max_abs_diff = float(np.max(np.abs(sklearn_prob - onnx_prob))) if len(values32) else 0.0
    return {
        "passed": bool(max_abs_diff <= float(tolerance)),
        "max_abs_diff": max_abs_diff,
        "tolerance": float(tolerance),
        "rows": int(len(values32)),
        "onnx_path": onnx_path.as_posix(),
    }
