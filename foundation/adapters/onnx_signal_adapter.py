from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from foundation.adapters.contracts import AdapterCandidateContract, AdapterInputContract, AdapterOutputContract, SignalCard
from foundation.control_plane.ledger import io_path
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    ordered_sklearn_probabilities,
    sha256_file,
)


@dataclass(frozen=True)
class OnnxSignalAdapter:
    adapter_id: str
    source_stage_id: str
    source_run_id: str
    mechanism_class: str
    roles: tuple[str, ...]
    feature_names: tuple[str, ...]
    source_model_path: Path
    onnx_model_path: Path
    nonflat_threshold: float
    tier_scope: str
    claim_boundary: str = "signalcard_adapter_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

    def input_contract(self) -> AdapterInputContract:
        return AdapterInputContract(feature_names=self.feature_names, state_names=(self.tier_scope,))

    def output_contract(self) -> AdapterOutputContract:
        return AdapterOutputContract()

    def candidate_contract(self) -> AdapterCandidateContract:
        return AdapterCandidateContract(
            candidate_id=self.adapter_id,
            source_stage_id=self.source_stage_id,
            source_run_id=self.source_run_id,
            mechanism_class=self.mechanism_class,
            roles=self.roles,
            input_contract=self.input_contract(),
            output_contract=self.output_contract(),
            claim_boundary=self.claim_boundary,
        )

    def source_probabilities(self, values: np.ndarray) -> np.ndarray:
        import joblib

        model = joblib.load(io_path(self.source_model_path))
        return ordered_sklearn_probabilities(model, np.asarray(values, dtype="float64"), class_order=LABEL_ORDER)

    def onnx_probabilities(self, values: np.ndarray) -> np.ndarray:
        import onnxruntime as ort

        matrix = np.asarray(values, dtype="float32")
        session = ort.InferenceSession(str(io_path(self.onnx_model_path)), providers=["CPUExecutionProvider"])
        outputs = session.run(None, {session.get_inputs()[0].name: matrix})
        return _find_probability_output(outputs, len(LABEL_ORDER))

    def parity_report(self, values: np.ndarray, *, tolerance: float = 1e-5) -> dict[str, Any]:
        import joblib

        model = joblib.load(io_path(self.source_model_path))
        report = check_onnxruntime_probability_parity(model, self.onnx_model_path, values, tolerance=tolerance)
        report["source_model_path"] = self.source_model_path.as_posix()
        report["source_model_sha256"] = sha256_file(self.source_model_path)
        report["onnx_model_path"] = self.onnx_model_path.as_posix()
        report["onnx_model_sha256"] = sha256_file(self.onnx_model_path)
        report["feature_count"] = len(self.feature_names)
        report["tier_scope"] = self.tier_scope
        return report

    def signal_cards(self, probabilities: np.ndarray, *, row_ids: Sequence[Any] | None = None) -> list[SignalCard]:
        prob = np.asarray(probabilities, dtype="float64")
        if prob.ndim != 2 or prob.shape[1] != len(LABEL_ORDER):
            raise ValueError(f"Expected probability matrix with {len(LABEL_ORDER)} columns.")
        row_values = list(row_ids or range(prob.shape[0]))
        if len(row_values) != prob.shape[0]:
            raise ValueError("row_ids length must match probability rows.")
        cards: list[SignalCard] = []
        for index, row in enumerate(prob):
            cards.append(
                SignalCard(
                    adapter_id=self.adapter_id,
                    roles=self.roles,
                    direction=_direction(row, self.nonflat_threshold),
                    score=float(np.max(row)),
                    confidence=_confidence(row),
                    reason_codes=_reason_codes(row, self.nonflat_threshold),
                    metadata={
                        "tier_scope": self.tier_scope,
                        "row_id": row_values[index],
                        "p_short": float(row[0]),
                        "p_flat": float(row[1]),
                        "p_long": float(row[2]),
                    },
                )
            )
        return cards


def summarize_signal_cards(cards: Sequence[SignalCard]) -> dict[str, Any]:
    direction_counts: dict[str, int] = {}
    scores: list[float] = []
    confidences: list[float] = []
    for card in cards:
        direction_counts[card.direction] = direction_counts.get(card.direction, 0) + 1
        scores.append(float(card.score))
        confidences.append(float(card.confidence))
    return {
        "rows": len(cards),
        "direction_counts": dict(sorted(direction_counts.items())),
        "score_mean": float(np.mean(scores)) if scores else None,
        "confidence_mean": float(np.mean(confidences)) if confidences else None,
        "confidence_p95": float(np.quantile(confidences, 0.95)) if confidences else None,
    }


def _find_probability_output(outputs: Sequence[Any], class_count: int) -> np.ndarray:
    candidates = [
        output
        for output in outputs
        if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == class_count
    ]
    if len(candidates) != 1:
        shapes = [getattr(output, "shape", None) for output in outputs]
        raise RuntimeError(f"Expected one probability output with {class_count} columns; got shapes {shapes}.")
    return np.asarray(candidates[0], dtype="float64")


def _direction(probability_row: np.ndarray, nonflat_threshold: float) -> str:
    best_index = int(np.argmax(probability_row))
    label = int(LABEL_ORDER[best_index])
    direction = str(LABEL_NAMES[label])
    if direction in {"short", "long"} and float(probability_row[best_index]) < float(nonflat_threshold):
        return "no_trade"
    return direction


def _confidence(probability_row: np.ndarray) -> float:
    sorted_prob = np.sort(np.asarray(probability_row, dtype="float64"))
    return float(max(sorted_prob[-1] - sorted_prob[-2], 0.0))


def _reason_codes(probability_row: np.ndarray, nonflat_threshold: float) -> tuple[str, ...]:
    direction = _direction(probability_row, nonflat_threshold)
    if direction == "no_trade":
        return ("below_nonflat_threshold",)
    if direction == "flat":
        return ("flat_class_top_probability",)
    return ("nonflat_threshold_passed",)
