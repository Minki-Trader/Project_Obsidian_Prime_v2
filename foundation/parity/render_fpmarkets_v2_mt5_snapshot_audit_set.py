from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render an MT5 .set helper for the runtime feature snapshot audit."
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


def split_target_windows_spec(target_windows_utc: str, *, max_chunk_length: int = 230) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    current_length = 0

    for raw_window in target_windows_utc.split(";"):
        window = raw_window.strip()
        if not window:
            continue
        candidate_length = len(window) if not current else current_length + 1 + len(window)
        if current and candidate_length > max_chunk_length:
            chunks.append(";".join(current))
            current = [window]
            current_length = len(window)
            continue
        if not current and len(window) > max_chunk_length:
            raise RuntimeError(f"Single MT5 target window exceeds chunk limit: {window}")
        current.append(window)
        current_length = candidate_length

    if current:
        chunks.append(";".join(current))
    return chunks or [""]


def render_set(mt5_request: dict[str, Any]) -> str:
    target_window_chunks = split_target_windows_spec(str(mt5_request["target_windows_utc"]))
    lines = [
        "; Runtime parity MT5 feature snapshot audit inputs",
        f"InpOutputPath={mt5_request['common_files_output_path']}",
        "InpOutputUseCommonFiles=true",
        f"InpTargetWindowsUtc={target_window_chunks[0]}",
        f"InpTargetWindowsUtcPart2={target_window_chunks[1] if len(target_window_chunks) > 1 else ''}",
        f"InpTargetWindowsUtcPart3={target_window_chunks[2] if len(target_window_chunks) > 2 else ''}",
        f"InpTargetWindowsUtcPart4={target_window_chunks[3] if len(target_window_chunks) > 3 else ''}",
        "InpMainSymbol=US100",
        "InpTimeframe=5",
        "InpMainWarmupBars=300",
        "InpExternalWarmupBars=25",
        f"InpWindowStartUtc={mt5_request['window_start_utc'].replace('T', ' ').replace('Z', '')}",
        f"InpDatasetId={mt5_request['dataset_id']}",
        f"InpFixtureSetId={mt5_request['fixture_set_id']}",
        f"InpBundleId={mt5_request['bundle_id']}",
        f"InpRuntimeId={mt5_request['target_runtime_id']}",
        f"InpReportId={mt5_request['report_id']}",
        f"InpParserVersion={mt5_request['parser_version']}",
        f"InpParserContractVersion={mt5_request['parser_contract_version']}",
        f"InpFeatureContractVersion={mt5_request['feature_contract_version']}",
        f"InpRuntimeContractVersion={mt5_request['runtime_contract_version']}",
        f"InpFeatureOrderHash={mt5_request['feature_order_hash']}",
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
