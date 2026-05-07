from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from stage_pipelines.stage33.artifacts import RUN_ID, STAGE_ID, materialize
from stage_pipelines.stage33.evidence_sources import collect_evidence_rows
from stage_pipelines.stage33.role_classifier import build_gate_payloads, build_role_map


def run(root: Path, *, write: bool) -> dict[str, Any]:
    evidence_rows, inventory = collect_evidence_rows(root)
    role_map = build_role_map(evidence_rows)
    gates = build_gate_payloads(role_map, inventory)
    payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "inventory": inventory,
        "role_map": role_map,
        "gates": gates,
        "evidence_rows": [row.compact() for row in evidence_rows],
    }
    if write:
        summary = materialize(root, payload)
    else:
        summary = {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "write": False,
            "inventory": inventory,
            "candidate_count": role_map.get("candidate_count"),
            "candidate_ids": [item["candidate_id"] for item in role_map.get("adapter_candidates", [])],
            "gate_status": {name: gate.get("status") for name, gate in gates.items()},
            "onnx_artifacts_generated": False,
            "mt5_probe_executed": False,
            "model_training_executed": False,
        }
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage33 evidence-driven adapter role map.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--no-write", action="store_true", help="Scan and summarize without writing artifacts.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run(Path(args.root), write=not args.no_write)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
