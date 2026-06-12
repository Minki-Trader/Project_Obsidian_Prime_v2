from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from foundation.control_plane.grok_review_wrapper import run_grok_review, strip_known_noise


class GrokReviewWrapperTests(unittest.TestCase):
    def test_runs_prompt_without_shell_splitting_and_strips_known_noise(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fake = Path(temp_dir) / "fake_grok.py"
            fake.write_text(
                textwrap.dedent(
                    """
                    import sys

                    prompt = sys.argv[sys.argv.index("-p") + 1]
                    print("MCP server warning should be stripped")
                    print("ANSWER:" + prompt)
                    print("plugin warning on stderr", file=sys.stderr)
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            result = run_grok_review(
                "line one with spaces\nline two",
                executable=sys.executable,
                extra_args=(str(fake),),
                timeout_seconds=5,
            )

        self.assertTrue(result.success, result.to_dict())
        self.assertIn("ANSWER:line one with spaces\nline two", result.clean_stdout)
        self.assertNotIn("MCP server warning", result.clean_stdout)
        self.assertTrue(result.stripped_noise_lines)
        self.assertIn("plugin warning on stderr", result.raw_stderr)

    def test_timeout_returns_diagnostics_without_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fake = Path(temp_dir) / "fake_hang.py"
            fake.write_text(
                "import time\nprint('started')\ntime.sleep(5)\n",
                encoding="utf-8",
            )

            result = run_grok_review(
                "prompt",
                executable=sys.executable,
                extra_args=(str(fake),),
                timeout_seconds=0.1,
            )

        self.assertTrue(result.timed_out)
        self.assertFalse(result.success)
        self.assertIsNone(result.returncode)

    def test_packet_record_writes_clean_and_raw_channels(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fake = Path(temp_dir) / "fake_grok.py"
            output_dir = Path(temp_dir) / "packet"
            fake.write_text("import sys\nprint('ok')\nprint('diag', file=sys.stderr)\n", encoding="utf-8")

            result = run_grok_review(
                "prompt",
                executable=sys.executable,
                extra_args=(str(fake),),
                output_dir=output_dir,
            )

            self.assertTrue((output_dir / "prompt.md").exists())
            self.assertTrue((output_dir / "clean_output.md").exists())
            self.assertTrue((output_dir / "raw_diagnostics.json").exists())
            self.assertTrue((output_dir / "metadata.json").exists())
            self.assertIn("clean_output", result.packet_paths)

    def test_top_level_artifact_detection_flags_mcps(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fake = root / "fake_grok.py"
            fake.write_text(
                "from pathlib import Path\nPath('mcps').mkdir(exist_ok=True)\nprint('ok')\n",
                encoding="utf-8",
            )

            result = run_grok_review(
                "prompt",
                executable=sys.executable,
                extra_args=(str(fake),),
                cwd=root,
                repo_root=root,
            )

        self.assertIn("mcps", result.unexpected_top_level_artifacts)

    def test_strip_known_noise_keeps_normal_content(self) -> None:
        clean, stripped = strip_known_noise("first\nGIT REPO DISCOVERY FAILED\nsecond")

        self.assertEqual(clean, "first\nsecond")
        self.assertEqual(stripped, ["GIT REPO DISCOVERY FAILED"])


if __name__ == "__main__":
    unittest.main()
