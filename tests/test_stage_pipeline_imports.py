from __future__ import annotations

import importlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPTIONAL_IMPORTS = {"lightgbm", "skl2onnx", "onnxruntime"}


def _module_name(path: Path) -> str:
    return ".".join(path.relative_to(ROOT).with_suffix("").parts)


def _pipeline_modules() -> list[str]:
    return sorted(_module_name(path) for path in (ROOT / "foundation/pipelines").glob("run_stage*.py"))


def _stage_pipeline_modules() -> list[str]:
    return sorted(
        _module_name(path)
        for path in (ROOT / "stage_pipelines").rglob("*.py")
        if path.name != "__init__.py"
    )


class StagePipelineImportSmokeTests(unittest.TestCase):
    def test_wrappers_and_stage_modules_import(self) -> None:
        modules = _pipeline_modules() + _stage_pipeline_modules()
        self.assertGreater(len(modules), 0)

        optional_skips: list[tuple[str, str]] = []
        for module_name in modules:
            with self.subTest(module=module_name):
                try:
                    module = importlib.import_module(module_name)
                except ModuleNotFoundError as exc:
                    if exc.name in OPTIONAL_IMPORTS:
                        optional_skips.append((module_name, str(exc.name)))
                        continue
                    raise

                if module_name.startswith("foundation.pipelines.run_stage"):
                    has_entrypoint = callable(getattr(module, "main", None)) or callable(getattr(module, "run", None))
                    self.assertTrue(has_entrypoint, f"{module_name} does not expose main() or run().")

        self.assertLess(len(optional_skips), len(modules), optional_skips)


if __name__ == "__main__":
    unittest.main()
