from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair


def configure_run50bx() -> None:
    repair.RUN_NUMBER = "run50BX"
    repair.RUN_ID = "run50BX_stage56_baseline_adapter_lot_scale_repair_v1"
    repair.PACKET_ID = "stage56_baseline_adapter_lot_scale_repair_v1"
    repair.BLOCKED_LABEL = "blocked_adapter_lot_scale_repair_mt5_execution_missing_evidence"
    repair.RUN_ROOT = repair.STAGE_ROOT / "02_runs" / repair.RUN_NUMBER
    repair.PACKET_ROOT = Path("docs/agent_control/packets") / repair.PACKET_ID
    repair.COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{repair.RUN_NUMBER}_baseline_adapter_lot_scale_repair"
    repair.REPORT_PATH = repair.REVIEWS_ROOT / "run50BX_baseline_adapter_lot_scale_repair_report.md"
    repair.SUMMARY_JSON_PATH = repair.REVIEWS_ROOT / "run50BX_baseline_adapter_lot_scale_repair_summary.json"
    repair.SUMMARY_CSV_PATH = repair.REVIEWS_ROOT / "run50BX_baseline_adapter_lot_scale_repair_summary.csv"
    repair.AUDIT_CSV_PATH = repair.REVIEWS_ROOT / "run50BX_baseline_adapter_lot_scale_repair_audit.csv"
    repair.RISK_CSV_PATH = repair.REVIEWS_ROOT / "run50BX_baseline_adapter_lot_scale_repair_risk_telemetry.csv"
    repair.REPAIR_VARIANTS = (
        repair.RepairVariant(
            adapter_id="ba11_no_atr_sd4_lot025",
            label="no_atr_same_direction_cooldown4_lot025",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.25,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            same_direction_reentry_cooldown_bars=4,
            notes="Scale fixed lot from 0.10 to 0.25 on the best density-preserving same-direction cooldown4 lifecycle.",
        ),
        repair.RepairVariant(
            adapter_id="ba12_no_atr_close_only_lot025",
            label="no_atr_close_only_opposite_lot025",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.25,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            reverse_on_opposite_signal=False,
            close_only_on_opposite_signal=True,
            notes="Scale fixed lot from 0.10 to 0.25 on the close-only opposite lifecycle.",
        ),
        repair.RepairVariant(
            adapter_id="ba13_no_atr_control_lot025",
            label="no_atr_control_lot025",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.25,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            notes="Scale the reproduced no-ATR control to 0.25 lot as a pure cost-stress exposure check.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    configure_run50bx()
    return repair.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
