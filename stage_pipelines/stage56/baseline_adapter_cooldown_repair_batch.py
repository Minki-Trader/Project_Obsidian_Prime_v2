from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair


def configure_run50bv() -> None:
    repair.RUN_NUMBER = "run50BV"
    repair.RUN_ID = "run50BV_stage56_baseline_adapter_cooldown_repair_v1"
    repair.PACKET_ID = "stage56_baseline_adapter_cooldown_repair_v1"
    repair.BLOCKED_LABEL = "blocked_adapter_cooldown_repair_mt5_execution_missing_evidence"
    repair.RUN_ROOT = repair.STAGE_ROOT / "02_runs" / repair.RUN_NUMBER
    repair.PACKET_ROOT = Path("docs/agent_control/packets") / repair.PACKET_ID
    repair.COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{repair.RUN_NUMBER}_baseline_adapter_cooldown_repair"
    repair.REPORT_PATH = repair.REVIEWS_ROOT / "run50BV_baseline_adapter_cooldown_repair_report.md"
    repair.SUMMARY_JSON_PATH = repair.REVIEWS_ROOT / "run50BV_baseline_adapter_cooldown_repair_summary.json"
    repair.SUMMARY_CSV_PATH = repair.REVIEWS_ROOT / "run50BV_baseline_adapter_cooldown_repair_summary.csv"
    repair.AUDIT_CSV_PATH = repair.REVIEWS_ROOT / "run50BV_baseline_adapter_cooldown_repair_audit.csv"
    repair.RISK_CSV_PATH = repair.REVIEWS_ROOT / "run50BV_baseline_adapter_cooldown_repair_risk_telemetry.csv"
    repair.REPAIR_VARIANTS = (
        repair.RepairVariant(
            adapter_id="ba05_no_atr_reentry_cooldown3",
            label="no_atr_reentry_cooldown3",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.1,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            reentry_cooldown_bars=3,
            notes="No ATR and fixed lot; add 3-bar general re-entry cooldown to reduce cost-heavy churn while preserving density.",
        ),
        repair.RepairVariant(
            adapter_id="ba06_no_atr_reentry_cooldown6",
            label="no_atr_reentry_cooldown6",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.1,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            reentry_cooldown_bars=6,
            notes="No ATR and fixed lot; add 6-bar general re-entry cooldown to test a stronger cost/same-move repair.",
        ),
        repair.RepairVariant(
            adapter_id="ba07_no_atr_same_direction_cooldown6",
            label="no_atr_same_direction_cooldown6",
            atr_enabled=False,
            model_risk_enabled=False,
            fixed_lot=0.1,
            atr_stop_multiplier=0.0,
            atr_take_profit_multiplier=0.0,
            model_risk_max_pct=0.0,
            same_direction_reentry_cooldown_bars=6,
            notes="No ATR and fixed lot; block same-direction re-entry for 6 bars while allowing opposite transitions.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    configure_run50bv()
    return repair.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
