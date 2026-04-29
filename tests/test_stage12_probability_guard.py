from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from foundation.pipelines import run_stage12_extratrees_standalone_batch20 as batch20
from foundation.pipelines import run_stage12_extratrees_standalone_scout as scout
from foundation.pipelines import run_stage12_batch20_top_mt5_probe as top_probe


class _FakeModel:
    classes_ = np.array([0, 1])

    def predict_proba(self, values):
        return np.full((len(values), 2), 0.5)


class _ShuffledClassModel:
    classes_ = np.array([2, 0, 1])

    def predict_proba(self, values):
        rows = len(values)
        return np.tile(np.array([[0.2, 0.7, 0.1]]), (rows, 1))


class Stage12ProbabilityGuardTests(unittest.TestCase):
    def test_run03b_probability_ordering_rejects_missing_class(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "missing required labels"):
            scout.ordered_predict_proba(_FakeModel(), np.zeros((2, 3)))

    def test_run03d_probability_ordering_rejects_missing_class(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "missing required labels"):
            batch20._ensure_probs(_FakeModel(), pd.DataFrame({"x": [1.0, 2.0]}))

    def test_run03e_probability_ordering_rejects_missing_class(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "Model probability classes missing required labels: \\[2\\]"):
            top_probe.probability_matrix(_FakeModel(), np.zeros((2, 3)))

    def test_run03e_probability_ordering_reorders_shuffled_classes(self) -> None:
        matrix = top_probe.probability_matrix(_ShuffledClassModel(), np.zeros((2, 3)))
        np.testing.assert_allclose(matrix, np.array([[0.7, 0.1, 0.2], [0.7, 0.1, 0.2]]))


if __name__ == "__main__":
    unittest.main()
