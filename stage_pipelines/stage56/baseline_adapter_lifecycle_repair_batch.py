from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair


def configure_run50bw() -> None:
    repair.RUN_NUMBER = "run50BW"
    repair.RUN_ID = "run50BW_stage56_baseline_adapter_lifecycle_repair_v1"
    repair.PACKET_ID = "stage56_baseline_adapter_lifecycle_repair_v1"
    repair.BLOCKED_LABEL = "blocked_adapter_lifecycle_repair_mt5_execution_missing_evidence"
    repair.RUN_ROOT = repair.STAGE_ROOT / "02_runs" / repair.RUN_NUMBER
    repair.PACKET_ROOT = Path("docs/agent_control/packets") / repair.PACKET_ID
    repair.COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{repair.RUN_NUMBER}_baseline_adapter_lifecycle_repair"
    repair.REPORT_PATH = repair.REVIEWS_ROOT / "run50BW_baseline_adapter_lifecycle_repair_report.md"
    repair.SUMMARY_JSON_PATH = repair.REVIEWS_ROOT / "run50BW_baseline_adapter_lifecycle_repair_summary.json"
    repair.SUMMARY_CSV_PATH = repair.REVIEWS_ROOT / "run50BW_baseline_adapter_lifecycle_repair_summary.csv"
    repair.AUDIT_CSV_PATH = repair.REVIEWS_ROOT / "run50BW_baseline_adapter_lifecycle_repair_audit.csv"
    repair.RISK_CSV_PATH = repair.REVIEWS_ROOT / "run50BW_baseline_adapter_lifecycle_repair_risk_telemetry.csv"
    repair.REPAIR_VARIANTS = (
        repair.RepairVariant(
            adapter_id="ba08_no_atr_same_direction_cooldown4",
            label="no_atr_same_direction_cooldown4",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.1,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            same_direction_reentry_cooldown_bars=4,
            notes="Interpolate same-direction cooldown between run50BU control and run50BV cooldown6 to recover OOS density.",
        ),
        repair.RepairVariant(
            adapter_id="ba09_no_atr_close_only_opposite",
            label="no_atr_close_only_opposite",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.1,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            reverse_on_opposite_signal=False,
            close_only_on_opposite_signal=True,
            notes="Close on opposite signal without immediate same-bar reverse open to reduce churn and cost stress.",
        ),
        repair.RepairVariant(
            adapter_id="ba10_no_atr_close_only_same_dir_cd4",
            label="no_atr_close_only_same_dir_cd4",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.1,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            same_direction_reentry_cooldown_bars=4,
            reverse_on_opposite_signal=False,
            close_only_on_opposite_signal=True,
            notes="Combine close-only opposite lifecycle with 4-bar same-direction cooldown.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    configure_run50bw()
    return repair.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
