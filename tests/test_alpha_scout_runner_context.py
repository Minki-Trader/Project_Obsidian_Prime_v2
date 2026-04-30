from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "run_stage10_logreg_mt5_scout.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class AlphaScoutRunnerContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module("run_stage10_logreg_mt5_scout_context_test", PIPELINE_MODULE_PATH)

    def test_explicit_context_overrides_configured_global_identity_for_mt5_materialization(self) -> None:
        original = {
            "run_number": self.module.RUN_NUMBER,
            "run_id": self.module.RUN_ID,
            "exploration_label": self.module.EXPLORATION_LABEL,
            "common_run_root": self.module.COMMON_RUN_ROOT,
        }
        try:
            self.module.configure_run_identity(
                run_number="runGlobal",
                run_id="global_run_id",
                exploration_label="global_label",
                common_run_root="Project_Obsidian_Prime_v2/stage10/global_run_id",
            )
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                context = self.module.alpha_scout_runner.build_run_context(
                    stage_id=self.module.STAGE_ID,
                    stage_number=10,
                    run_number="runCtx",
                    run_id="context_run_id",
                    exploration_label="context_label",
                    output_root=root,
                    common_run_root="Project_Obsidian_Prime_v2/stage10/context_run_id",
                    common_files_root=root / "common",
                    terminal_data_root=root / "terminal",
                    tester_profile_root=root / "tester",
                )
                attempt = self.module.materialize_mt5_attempt_files(
                    context=context,
                    run_output_root=root,
                    tier_name=self.module.TIER_A,
                    split_name="validation_is",
                    local_onnx_path=root / "tier_a.onnx",
                    local_feature_matrix_path=root / "tier_a_features.csv",
                    feature_count=58,
                    feature_order_hash="hash_a",
                    rule=self.module.ThresholdRule(
                        threshold_id="unit",
                        short_threshold=0.6,
                        long_threshold=0.45,
                        min_margin=0.0,
                    ),
                    from_date="2025.01.01",
                    to_date="2025.10.01",
                )
                set_text = Path(attempt["set"]["path"]).read_text(encoding="utf-8")

            self.assertIn("InpRunId=context_run_id", set_text)
            self.assertIn("InpExplorationLabel=context_label", set_text)
            self.assertIn("Project_Obsidian_Prime_v2/stage10/context_run_id/models/tier_a.onnx", set_text)
            self.assertIn("Project_Obsidian_Prime_v2_context_run_id_tier_a_validation_is", attempt["ini"]["tester"]["Report"])
            self.assertNotIn("global_run_id", set_text)
        finally:
            self.module.configure_run_identity(**original)


if __name__ == "__main__":
    unittest.main()
