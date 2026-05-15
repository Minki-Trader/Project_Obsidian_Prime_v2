from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair


def configure_run50by() -> None:
    repair.RUN_NUMBER = "run50BY"
    repair.RUN_ID = "run50BY_stage56_baseline_adapter_same_move_lot_repair_v1"
    repair.PACKET_ID = "stage56_baseline_adapter_same_move_lot_repair_v1"
    repair.BLOCKED_LABEL = "blocked_adapter_same_move_lot_repair_mt5_execution_missing_evidence"
    repair.RUN_ROOT = repair.STAGE_ROOT / "02_runs" / repair.RUN_NUMBER
    repair.PACKET_ROOT = Path("docs/agent_control/packets") / repair.PACKET_ID
    repair.COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{repair.RUN_NUMBER}_baseline_adapter_same_move_lot_repair"
    repair.REPORT_PATH = repair.REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_report.md"
    repair.SUMMARY_JSON_PATH = repair.REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_summary.json"
    repair.SUMMARY_CSV_PATH = repair.REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_summary.csv"
    repair.AUDIT_CSV_PATH = repair.REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_audit.csv"
    repair.RISK_CSV_PATH = repair.REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_risk_telemetry.csv"
    repair.REPAIR_VARIANTS = (
        repair.RepairVariant(
            adapter_id="ba14_no_atr_sd5_lot025",
            label="no_atr_same_direction_cooldown5_lot025",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.25,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            same_direction_reentry_cooldown_bars=5,
            notes="Interpolate same-direction cooldown5 at 0.25 lot to reduce same-move while trying to keep OOS density above 5.",
        ),
        repair.RepairVariant(
            adapter_id="ba15_no_atr_close_only_sd3_lot025",
            label="no_atr_close_only_same_direction_cooldown3_lot025",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.25,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            same_direction_reentry_cooldown_bars=3,
            reverse_on_opposite_signal=False,
            close_only_on_opposite_signal=True,
            notes="Close-only opposite plus 3-bar same-direction cooldown at 0.25 lot.",
        ),
        repair.RepairVariant(
            adapter_id="ba16_no_atr_close_only_sd2_lot025",
            label="no_atr_close_only_same_direction_cooldown2_lot025",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.25,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            same_direction_reentry_cooldown_bars=2,
            reverse_on_opposite_signal=False,
            close_only_on_opposite_signal=True,
            notes="Close-only opposite plus 2-bar same-direction cooldown at 0.25 lot.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    configure_run50by()
    return repair.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
