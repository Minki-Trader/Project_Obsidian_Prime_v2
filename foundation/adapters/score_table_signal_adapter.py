from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from foundation.adapters.contracts import AdapterCandidateContract, AdapterInputContract, AdapterOutputContract, SignalCard
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import sha256_file


@dataclass(frozen=True)
class ScoreTableSignalAdapter:
    adapter_id: str
    source_stage_id: str
    source_run_id: str
    mechanism_class: str
    roles: tuple[str, ...]
    feature_names: tuple[str, ...]
    score_table_path: Path
    nonflat_threshold: float
    tier_scope: str
    claim_boundary: str = "score_table_signalcard_adapter_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

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

    def table_probabilities(self, values: np.ndarray) -> np.ndarray:
        table = load_ebm_score_table(self.score_table_path, feature_count=len(self.feature_names))
        return score_ebm_table_probabilities(table, np.asarray(values, dtype="float64"))

    def parity_report_against_probabilities(
        self,
        values: np.ndarray,
        expected_probabilities: np.ndarray,
        *,
        tolerance: float = 2.0e-3,
    ) -> dict[str, Any]:
        actual = self.table_probabilities(values)
        expected = np.asarray(expected_probabilities, dtype="float64")
        if actual.shape != expected.shape:
            raise ValueError(f"Probability shape mismatch: {actual.shape} != {expected.shape}")
        diffs = np.abs(actual - expected)
        max_abs_diff = float(np.max(diffs)) if len(actual) else 0.0
        return {
            "passed": bool(max_abs_diff <= float(tolerance)),
            "max_abs_diff": max_abs_diff,
            "mean_abs_diff": float(np.mean(diffs)) if len(actual) else 0.0,
            "p95_abs_diff": float(np.quantile(diffs, 0.95)) if len(actual) else 0.0,
            "tolerance": float(tolerance),
            "rows": int(actual.shape[0]),
            "score_table_path": self.score_table_path.as_posix(),
            "score_table_sha256": sha256_file(self.score_table_path),
            "feature_count": len(self.feature_names),
            "tier_scope": self.tier_scope,
        }

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
