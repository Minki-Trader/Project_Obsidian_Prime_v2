from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render an MT5 .set helper for the Stage 03 feature snapshot audit."
    )
    parser.add_argument(
        "--mt5-request",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path to the MT5 request pack JSON.",
    )
    parser.add_argument(
        "--output-set",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_audit_inputs.set",
        help="Repo-relative path to the rendered MT5 .set file.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_set(mt5_request: dict[str, Any]) -> str:
    lines = [
        "; Stage 03 runtime parity MT5 feature snapshot audit inputs",
        "InpEnableFeatureSnapshotAudit=true",
        "InpFeatureSnapshotAuditUseCommonFiles=true",
        f"InpFeatureSnapshotAuditPath={mt5_request['common_files_output_path']}",
        f"InpFeatureSnapshotAuditTargetWindowsUtc={mt5_request['target_windows_utc']}",
        "InpFeatureSnapshotAuditIncludeSkipRows=true",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    request_path = Path(args.mt5_request)
    output_path = Path(args.output_set)
    mt5_request = load_json(request_path)
    rendered = render_set(mt5_request)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output_set": str(output_path.resolve()),
                "common_files_output_path": mt5_request["common_files_output_path"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
