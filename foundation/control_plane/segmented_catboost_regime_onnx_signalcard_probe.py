from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable, TypeVar

from foundation.control_plane import segmented_catboost_onnx_signalcard_probe as base
from foundation.control_plane.ledger import json_ready


RUN_ID = "run27J_segmented_catboost_regime_onnx_signalcard_probe_v1"
PACKET_ID = "stage33_run27J_segmented_catboost_regime_onnx_signalcard_probe_v1"
BOUNDARY = "segmented_catboost_regime_onnx_signalcard_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SELECTED_CANDIDATE_ID = "stage18_run12D_catboost_regime_split_probe_v1"
SELECTED_SOURCE_RUN_ID = "run12D_catboost_regime_split_probe_v1"

T = TypeVar("T")


def _with_config(fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    previous = base.current_segmented_catboost_onnx_probe_config()
    base.configure_segmented_catboost_onnx_probe(
        run_id=RUN_ID,
        packet_id=PACKET_ID,
        boundary=BOUNDARY,
        selected_candidate_id=SELECTED_CANDIDATE_ID,
        selected_source_run_id=SELECTED_SOURCE_RUN_ID,
    )
    try:
        return fn(*args, **kwargs)
    finally:
        base.configure_segmented_catboost_onnx_probe(**previous)


def build_segmented_catboost_regime_onnx_signalcard_probe(root: Path | str = Path(".")) -> base.SegmentedCatBoostOnnxProbeResult:
    return _with_config(base.build_segmented_catboost_onnx_signalcard_probe, root)


def write_segmented_catboost_regime_onnx_signalcard_probe_packet(
    root: Path | str = Path("."),
    *,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    return _with_config(base.write_segmented_catboost_onnx_signalcard_probe_packet, root, generated_at_utc=generated_at_utc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage33 segmented CatBoost regime ONNX SignalCard adapter probe.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_segmented_catboost_regime_onnx_signalcard_probe(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_segmented_catboost_regime_onnx_signalcard_probe_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
