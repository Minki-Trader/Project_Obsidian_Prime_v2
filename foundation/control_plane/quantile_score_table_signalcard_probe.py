from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable, Sequence, TypeVar

from foundation.control_plane.ledger import json_ready
from foundation.control_plane.score_table_signalcard_probe import (
    build_score_table_signalcard_probe,
    configure_score_table_signalcard_probe,
    current_score_table_signalcard_probe_config,
    write_score_table_signalcard_probe_packet,
)


RUN_ID = "run27L_quantile_tail_score_table_signalcard_adapter_probe_v1"
PACKET_ID = "stage33_run27L_quantile_tail_score_table_signalcard_adapter_probe_v1"
BOUNDARY = "quantile_tail_score_table_signalcard_adapter_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SELECTED_CANDIDATE_ID = "stage27_run21B_quantile_boosting_tail_risk_runtime_probe_v1"
SELECTED_SOURCE_STAGE_ID = "27_tail_model__quantile_boosting_risk_surface"
SELECTED_SOURCE_RUN_ID = "run21B_quantile_boosting_tail_risk_runtime_probe_v1"
PARITY_TOLERANCE = 3.0e-3

T = TypeVar("T")


def build_quantile_score_table_signalcard_probe(root: Path | str = Path(".")) -> Any:
    return _with_config(lambda: build_score_table_signalcard_probe(root))


def write_quantile_score_table_signalcard_probe_packet(
    root: Path | str = Path("."),
    *,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    return _with_config(lambda: write_score_table_signalcard_probe_packet(root, generated_at_utc=generated_at_utc))


def _with_config(callback: Callable[[], T]) -> T:
    previous = current_score_table_signalcard_probe_config()
    _apply_config()
    try:
        return callback()
    finally:
        configure_score_table_signalcard_probe(
            run_id=str(previous["run_id"]),
            packet_id=str(previous["packet_id"]),
            boundary=str(previous["boundary"]),
            selected_candidate_id=str(previous["selected_candidate_id"]),
            selected_source_stage_id=str(previous["selected_source_stage_id"]),
            selected_source_run_id=str(previous["selected_source_run_id"]),
            parity_tolerance=float(previous["parity_tolerance"]),
        )


def _apply_config() -> None:
    configure_score_table_signalcard_probe(
        run_id=RUN_ID,
        packet_id=PACKET_ID,
        boundary=BOUNDARY,
        selected_candidate_id=SELECTED_CANDIDATE_ID,
        selected_source_stage_id=SELECTED_SOURCE_STAGE_ID,
        selected_source_run_id=SELECTED_SOURCE_RUN_ID,
        parity_tolerance=PARITY_TOLERANCE,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage33 quantile score-table SignalCard adapter probe.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_quantile_score_table_signalcard_probe(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_quantile_score_table_signalcard_probe_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
