from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import the MT5 snapshot audit, compare it to the Python snapshot, and render the Stage 03 report."
    )
    parser.add_argument(
        "--mt5-request",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path to the MT5 request pack JSON.",
    )
    parser.add_argument(
        "--python-snapshot",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path to the Python snapshot JSON.",
    )
    parser.add_argument(
        "--comparison-json",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path for the comparison summary JSON.",
    )
    parser.add_argument(
        "--mt5-snapshot",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl",
        help="Repo-relative path for the imported MT5 snapshot JSONL.",
    )
    parser.add_argument(
        "--report-path",
        default="stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md",
        help="Repo-relative path for the rendered markdown report.",
    )
    parser.add_argument(
        "--common-root",
        default=None,
        help="Optional override for the MT5 Common Files root.",
    )
    parser.add_argument(
        "--source-path",
        default=None,
        help="Optional explicit source MT5 JSONL path. Overrides the path derived from the MT5 request.",
    )
    parser.add_argument(
        "--skip-import",
        action="store_true",
        help="Skip the Common Files import step and use the repo-local MT5 snapshot path as-is.",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-5,
        help="Absolute tolerance for ready-row feature comparisons.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=None,
        help="Optional explicit review date for the rendered markdown report.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_step(args: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    stdout = result.stdout.strip()
    if not stdout:
        return {}
    return json.loads(stdout)


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()
    mt5_request_path = Path(args.mt5_request)

    import_summary: dict[str, Any] | None = None
    if not args.skip_import:
        import_cmd = [
            sys.executable,
            "foundation/parity/import_fpmarkets_v2_mt5_snapshot_audit.py",
            "--mt5-request",
            args.mt5_request,
            "--destination-path",
            args.mt5_snapshot,
        ]
        if args.common_root:
            import_cmd.extend(["--common-root", args.common_root])
        if args.source_path:
            import_cmd.extend(["--source-path", args.source_path])
        import_summary = run_step(import_cmd, cwd=repo_root)

    compare_cmd = [
        sys.executable,
        "foundation/parity/compare_fpmarkets_v2_runtime_parity.py",
        "--python-snapshot",
        args.python_snapshot,
        "--mt5-request",
        args.mt5_request,
        "--mt5-snapshot",
        args.mt5_snapshot,
        "--output-json",
        args.comparison_json,
        "--tolerance",
        str(args.tolerance),
    ]
    compare_summary = run_step(compare_cmd, cwd=repo_root)

    render_cmd = [
        sys.executable,
        "foundation/parity/render_fpmarkets_v2_runtime_parity_report.py",
        "--comparison-json",
        args.comparison_json,
        "--python-snapshot",
        args.python_snapshot,
        "--mt5-request",
        args.mt5_request,
        "--mt5-snapshot",
        args.mt5_snapshot,
        "--report-path",
        args.report_path,
    ]
    if args.reviewed_on:
        render_cmd.extend(["--reviewed-on", args.reviewed_on])
    render_summary = run_step(render_cmd, cwd=repo_root)

    mt5_request = load_json(mt5_request_path)
    print(
        json.dumps(
            {
                "status": "ok",
                "import_performed": not args.skip_import,
                "import_summary": import_summary,
                "compare_summary": compare_summary,
                "render_summary": render_summary,
                "common_files_output_path": mt5_request.get("common_files_output_path"),
                "repo_import_path": mt5_request.get("repo_import_path"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
