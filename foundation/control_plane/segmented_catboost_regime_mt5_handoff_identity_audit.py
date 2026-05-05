from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable, TypeVar

from foundation.control_plane import segmented_catboost_mt5_handoff_identity_audit as base
from foundation.control_plane.ledger import json_ready


RUN_ID = "run27K_segmented_catboost_regime_mt5_handoff_identity_audit_v1"
PACKET_ID = "stage33_run27K_segmented_catboost_regime_mt5_handoff_identity_audit_v1"
BOUNDARY = "segmented_catboost_regime_mt5_handoff_identity_audit_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SOURCE_RUN_ID = "run27J_segmented_catboost_regime_onnx_signalcard_probe_v1"
SELECTED_SOURCE_RUN_ID = "run12D_catboost_regime_split_probe_v1"

T = TypeVar("T")


def _with_config(fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    previous = base.current_segmented_catboost_mt5_handoff_identity_config()
    base.configure_segmented_catboost_mt5_handoff_identity_audit(
        run_id=RUN_ID,
        packet_id=PACKET_ID,
        boundary=BOUNDARY,
        source_run_id=SOURCE_RUN_ID,
        selected_source_run_id=SELECTED_SOURCE_RUN_ID,
    )
    try:
        return fn(*args, **kwargs)
    finally:
        base.configure_segmented_catboost_mt5_handoff_identity_audit(**previous)


def build_segmented_catboost_regime_mt5_handoff_identity_audit(
    root: Path | str = Path("."),
) -> base.SegmentedCatBoostMt5HandoffIdentityAuditResult:
    return _with_config(base.build_segmented_catboost_mt5_handoff_identity_audit, root)


def write_segmented_catboost_regime_mt5_handoff_identity_audit_packet(
    root: Path | str = Path("."),
    *,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    return _with_config(base.write_segmented_catboost_mt5_handoff_identity_audit_packet, root, generated_at_utc=generated_at_utc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage33 segmented CatBoost regime MT5 handoff identity audit.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_segmented_catboost_regime_mt5_handoff_identity_audit(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_segmented_catboost_regime_mt5_handoff_identity_audit_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
