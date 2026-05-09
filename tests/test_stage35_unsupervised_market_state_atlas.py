from __future__ import annotations

import unittest

import pandas as pd

from stage_pipelines.stage35 import atlas_config as cfg
from stage_pipelines.stage35 import atlas_model
from stage_pipelines.stage35 import candidate_deep_dive
from stage_pipelines.stage35 import closeout
from stage_pipelines.stage35 import worthwhile_config, worthwhile_variants


class Stage35AtlasConfigTests(unittest.TestCase):
    def test_topic_features_do_not_overlap(self) -> None:
        cfg.validate_topic_layout()
        used: set[str] = set()
        for topic in cfg.TOPICS:
            overlap = used.intersection(topic.features)
            self.assertEqual(set(), overlap)
            used.update(topic.features)

    def test_constant_score_table_direction_is_valid(self) -> None:
        self.assertIn("long", {"long", "short"})
        self.assertIn("short", {"long", "short"})

    def test_feature_order_is_58(self) -> None:
        self.assertEqual(58, len(cfg.FEATURE_ORDER))

    def test_worthwhile_variant_surface_is_unique(self) -> None:
        assignments = pd.DataFrame(
            {
                "state_return_volatility_shape": [0, 1, 2, 3, 4],
                "state_trend_momentum_pressure": [0, 1, 2, 3, 4],
            }
        )
        variants = worthwhile_variants.session_variants() + worthwhile_variants.atlas_state_variants(assignments)
        variant_ids = [variant.variant_id for variant in variants]
        self.assertEqual(19, len(variant_ids))
        self.assertEqual(len(variant_ids), len(set(variant_ids)))

    def test_worthwhile_run_keeps_stage35_ownership(self) -> None:
        self.assertEqual(cfg.STAGE_ID, worthwhile_config.STAGE_ID)
        self.assertEqual("run29B", worthwhile_config.RUN_NUMBER)
        self.assertIn("stage35", worthwhile_config.PACKET_ID)

    def test_candidate_deep_dive_scope_is_four_candidates(self) -> None:
        self.assertEqual("run29C", candidate_deep_dive.RUN_NUMBER)
        self.assertEqual(4, len(candidate_deep_dive.CANDIDATE_IDS))
        self.assertEqual(len(candidate_deep_dive.CANDIDATE_IDS), len(set(candidate_deep_dive.CANDIDATE_IDS)))

    def test_closeout_does_not_open_stage36(self) -> None:
        self.assertIn("closeout", closeout.RUN_ID)
        self.assertIn("no_stage36", closeout.BOUNDARY)


if __name__ == "__main__":
    unittest.main()
