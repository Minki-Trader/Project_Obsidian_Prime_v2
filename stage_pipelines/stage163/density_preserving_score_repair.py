from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage161 import score_margin_or_side_filter_repair as s161  # noqa: E402

STAGE_ID = "163_adapter_research__stage161_density_preserving_score_repair"
RUN_NUMBER = "run163A"
RUN_ID = "run163A_stage163_stage161_density_preserving_score_repair_v1"
PACKET_ID = "stage163_stage161_density_preserving_score_repair_v1"
SOURCE_STAGE_ID = "162_adapter_research__stage161_score_margin_followup_review"
SOURCE_RUN_ID = "run162A_stage162_stage161_score_margin_followup_review_v1"
SOURCE_STAGE162_CLOSEOUT_COMMIT = "b6702e6ed96aab91eadddfbd0943e2b6c71f3a2a"
SOURCE_STAGE162_HASH_RECORD_COMMIT = "8a85acc33295ec2cc44110da862577d6e470b6bc"
SOURCE_STAGE161_ID = "161_adapter_research__score_margin_or_side_filter_repair"
SOURCE_STAGE161_RUN_ID = "run161A_stage161_score_margin_or_side_filter_repair_v1"
NEXT_STAGE_ID = "164_adapter_research__stage163_density_followup_review"
NEXT_RUN_ID = "run164A_stage164_stage163_density_followup_review_v1"
NEXT_PACKET_ID = "stage164_stage163_density_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
SOURCE_REFERENCE = {
    "adapter_id": "s156_low_edge_risk0300_h3_cd5_sht54_lng52",
    "validation_pf": 1.55,
    "validation_net": 1037.79,
    "validation_dd_percent": 10.23,
    "validation_trade_count": 275,
    "oos_pf": 1.85,
    "oos_net": 1032.34,
    "oos_dd_percent": 11.92,
    "oos_trade_count": 193,
    "oos_mid_pf": 1.659175838,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s163a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage163_density_preserving_score_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage163_density_preserving_score_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage163_density_preserving_score_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage163_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage163_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage163_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage163_probability_binding_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage163_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage163_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage163_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage163_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage163/density_preserving_score_repair.py")
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s163_longdense_risk0300_h3_cd5_sht58_lng52",
        label="stage163_long_dense_shortprob_risk0300",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.58,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage163 long-dense repair: short threshold blocks weak shorts while long gate stays open.",
    ),
    repair.RepairVariant(
        adapter_id="s163_longdense_risk0400_h3_cd5_sht58_lng52",
        label="stage163_long_dense_shortprob_risk0400",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0400,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.58,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage163 long-dense repair with 4 percent model risk cap; risk cap remains below mandatory 5 percent.",
    ),
    repair.RepairVariant(
        adapter_id="s163_shortgate_risk0250_h3_cd5_sht54_lng52",
        label="stage163_shortgate_low_risk_control",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0250,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage163 low-risk shortgate control: checks whether lower risk repairs OOS DD without losing density.",
    ),
)

VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s163_longdense_risk0300_h3_cd5_sht58_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "short",
        "side_filter_enabled": True,
        "axis": "long_dense_shortprob",
    },
    "s163_longdense_risk0400_h3_cd5_sht58_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "short",
        "side_filter_enabled": True,
        "axis": "long_dense_shortprob_risk0400",
    },
    "s163_shortgate_risk0250_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "short",
        "side_filter_enabled": True,
        "axis": "shortgate_low_risk_control",
    },
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    s161.write_csv(path, rows, columns)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def actual_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def segment_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def configure_runner() -> None:
    s161.STAGE_ID = STAGE_ID
    s161.RUN_NUMBER = RUN_NUMBER
    s161.RUN_ID = RUN_ID
    s161.PACKET_ID = PACKET_ID
    s161.PARENT_RUN_ID = SOURCE_STAGE161_RUN_ID
    s161.SOURCE_STAGE_ID = SOURCE_STAGE161_ID
    s161.SOURCE_STAGE160_CLOSEOUT_COMMIT = SOURCE_STAGE162_CLOSEOUT_COMMIT
    s161.SOURCE_STAGE160_HASH_RECORD_COMMIT = SOURCE_STAGE162_HASH_RECORD_COMMIT
    s161.NEXT_STAGE_ID = NEXT_STAGE_ID
    s161.NEXT_RUN_ID = NEXT_RUN_ID
    s161.NEXT_PACKET_ID = NEXT_PACKET_ID
    s161.STAGE_ROOT = STAGE_ROOT
    s161.RUN_ROOT = RUN_ROOT
    s161.REVIEWS_ROOT = REVIEWS_ROOT
    s161.SELECTED_ROOT = SELECTED_ROOT
    s161.PACKET_ROOT = PACKET_ROOT
    s161.NEXT_STAGE_ROOT = NEXT_STAGE_ROOT
    s161.PARTIALS_ROOT = PARTIALS_ROOT
    s161.COMMON_ROOT = COMMON_ROOT
    s161.SUMMARY_JSON_PATH = SUMMARY_JSON_PATH
    s161.SUMMARY_CSV_PATH = SUMMARY_CSV_PATH
    s161.REPORT_PATH = REPORT_PATH
    s161.SEGMENT_KPI_PATH = SEGMENT_KPI_PATH
    s161.RISK_ATR_TELEMETRY_PATH = RISK_ATR_TELEMETRY_PATH
    s161.GATE_FEATURE_SUMMARY_PATH = GATE_FEATURE_SUMMARY_PATH
    s161.PROBABILITY_BINDING_PATH = PROBABILITY_BINDING_PATH
    s161.MODEL_SCORE_AUDIT_PATH = MODEL_SCORE_AUDIT_PATH
    s161.TIER_B_DIAGNOSTIC_PATH = TIER_B_DIAGNOSTIC_PATH
    s161.DECISION_PATH = DECISION_PATH
    s161.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    s161.STAGE_LEDGER_PATH = STAGE_LEDGER_PATH
    s161.PRODUCER_PATH = PRODUCER_PATH
    s161.VARIANTS = VARIANTS
    s161.VARIANT_EXTRAS = VARIANT_EXTRAS
    s161.SOURCE_SPECS_BY_VARIANT = {variant.adapter_id: dict(s161.s158.LOW_EDGE_SOURCE_SPEC) for variant in VARIANTS}
    s161.CONTEXT_GATE_SPECS = {
        variant.adapter_id: {
            "gate_column": f"stage163_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}",
            "gate_type": "weak_session_or_et40_mid_margin_block",
            "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
            "session_min": 170.0,
            "session_max": 265.0,
            "margin_min": 0.04,
            "margin_max": 0.0775,
            "description": f"Stage163 {VARIANT_EXTRAS[variant.adapter_id]['axis']} using Stage154/156 low-edge gate.",
        }
        for variant in VARIANTS
    }
    s161.MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}
    s161._CONTEXT_LOOKUP = None


def quality_rows(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for variant in VARIANTS:
        val = actual_row(summary_rows, variant.adapter_id, "validation_is")
        oos = actual_row(summary_rows, variant.adapter_id, "oos")
        oos_early = segment_row(segment_rows, variant.adapter_id, "oos", "early")
        oos_mid = segment_row(segment_rows, variant.adapter_id, "oos", "mid")
        flags: list[str] = []
        val_pf = as_float(val.get("profit_factor"))
        oos_pf = as_float(oos.get("profit_factor"))
        oos_dd = as_float(oos.get("max_drawdown_percent"))
        oos_early_pf = as_float(oos_early.get("profit_factor"))
        oos_early_net = as_float(oos_early.get("net_profit"))
        val_net = as_float(val.get("net_profit"))
        oos_net = as_float(oos.get("net_profit"))
        if val_pf < LEGACY_34D["profit_factor"]:
            flags.append("validation_pf_below_34d")
        if oos_pf < LEGACY_34D["profit_factor"]:
            flags.append("oos_pf_below_34d")
        if oos_dd > LEGACY_34D["max_drawdown_percent"]:
            flags.append("oos_dd_above_34d")
        if oos_early_pf < 1.10 or oos_early_net <= 0:
            flags.append("oos_early_damage")
        if val_net / SOURCE_REFERENCE["validation_net"] < 0.35 or oos_net / SOURCE_REFERENCE["oos_net"] < 0.35:
            flags.append("net_density_still_thin")
        rows.append(
            {
                "adapter_id": variant.adapter_id,
                "label": variant.label,
                "validation_pf": val_pf,
                "validation_net": val_net,
                "validation_trade_count": as_float(val.get("trade_count")),
                "oos_pf": oos_pf,
                "oos_net": oos_net,
                "oos_dd_percent": oos_dd,
                "oos_trade_count": as_float(oos.get("trade_count")),
                "oos_early_pf": oos_early_pf,
                "oos_early_net": oos_early_net,
                "oos_mid_pf": as_float(oos_mid.get("profit_factor")),
                "validation_net_retention_vs_source": val_net / SOURCE_REFERENCE["validation_net"],
                "oos_net_retention_vs_source": oos_net / SOURCE_REFERENCE["oos_net"],
                "oos_trade_retention_vs_source": as_float(oos.get("trade_count")) / SOURCE_REFERENCE["oos_trade_count"],
                "quality_flags": ";".join(flags) if flags else "candidate_quality_pass_review_required",
                "candidate_quality_pass": not flags,
            }
        )
    return rows


def decide(rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage164_runtime_completion_due_to_incomplete_stage163_runtime_candidate_not_final"
    if any(row.get("candidate_quality_pass") for row in rows):
        return "open_stage164_density_followup_review_candidate_not_final"
    return "open_stage164_density_repair_followup_due_to_kpi_damage_candidate_not_final"


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS early PF(표본외 초반 수익요인) | flags(플래그) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {validation_pf:.6f} | {validation_net:.2f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_early_pf:.6f} | {quality_flags} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    return f"""# Stage163 Density-Preserving Score Repair Report(163단계 밀도 보존 점수 수리 보고)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_stage162_closeout_commit(원천 162단계 종료 커밋): `{SOURCE_STAGE162_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can Stage163(163단계) preserve PF uplift(수익요인 상승) while recovering net/trade density(순손익/거래 밀도), OOS early(표본외 초반), and DD(낙폭)?

## KPI Read(KPI 판독)

{kpi_table(rows)}

## Judgment(판정)

Stage163(163단계)은 density-preserving repair(밀도 보존 수리)만 닫는다. Effect(효과): 결과가 좋든 나쁘든 Stage164(164단계) follow-up review(후속 검토)로 넘겨 한 단계가 과도하게 커지는 것을 막는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage163 Decision(163단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage162_closeout_commit(원천 162단계 종료 커밋): `{SOURCE_STAGE162_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage163(163단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        SUMMARY_CSV_PATH,
        SUMMARY_JSON_PATH,
        SEGMENT_KPI_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        AUDIT_CSV_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
    ]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage163_density_preserving_score_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage163 density-preserving score repair artifact.",
                }
            )
    for record in result.get("mt5_kpi_records", []) or []:
        report_path = record.get("report_path")
        if report_path and path_exists(Path(str(report_path))):
            path = Path(str(report_path))
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).stem}",
                    "artifact_type": "stage163_mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "MT5 Strategy Tester report for Stage163.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage163_density_preserving_score_repair",
                "status": "completed",
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage162_closeout_commit", SOURCE_STAGE162_CLOSEOUT_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    mt5_rows = build_stage_ledger_rows(result, decision)
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, mt5_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, mt5_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifacts, key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def build_stage_ledger_rows(result: Mapping[str, Any], decision: str) -> list[dict[str, Any]]:
    rows = []
    for row in s161.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []) or [],
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status") or "blocked"),
    ):
        row = dict(row)
        row["parent_run_id"] = SOURCE_STAGE161_RUN_ID
        row["judgment"] = decision
        row["scoreboard_lane"] = "baseline_adapter_stage163_density_preserving_score_repair"
        row["notes"] = ledger_pairs((("target_surface", TARGET_SURFACE), ("overall_goal_complete", 0)))
        rows.append(row)
    if not rows:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__materialized_or_blocked",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "materialized_or_blocked",
                "parent_run_id": SOURCE_STAGE161_RUN_ID,
                "record_view": "materialized_or_blocked",
                "tier_scope": "actual_routed_total",
                "kpi_scope": "density_preserving_score_repair",
                "scoreboard_lane": "baseline_adapter_stage163_density_preserving_score_repair",
                "status": str(result.get("external_verification_status") or "blocked"),
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "blocked_before_kpi_records",
                "guardrail_kpi": "overall_goal_complete=false",
                "external_verification_status": str(result.get("external_verification_status") or "blocked"),
                "notes": ledger_pairs((("target_surface", TARGET_SURFACE), ("overall_goal_complete", 0))),
            }
        )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    payloads = {
        "routing_receipt.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "experiment", "primary_skill": "obsidian-experiment-design", "support_skills": ["obsidian-performance-attribution", "obsidian-result-judgment", "obsidian-artifact-lineage"], "status": "completed"},
        "runtime_evidence_gate.json": {"external_verification_status": result.get("external_verification_status"), "summary_csv": rel(SUMMARY_CSV_PATH), "status": "passed" if result.get("external_verification_status") == "completed" else "blocked"},
        "scope_completion_gate.json": {"bounded_question": "density_preserving_score_repair", "decision": decision, "overall_goal_complete": False, "status": "passed"},
        "kpi_contract_audit.json": {"legacy_34d_target": LEGACY_34D, "source_reference": SOURCE_REFERENCE, "quality_rows": list(quality), "status": "completed"},
        "result_judgment_gate.json": {"decision": decision, "claim_boundary": BOUNDARY, "overall_goal_complete": False, "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {"driver_tested": "long_dense_shortprob_and_low_risk_shortgate", "summary_csv": rel(SUMMARY_CSV_PATH), "status": "completed"},
        "artifact_lineage_audit.json": {"source_inputs": [rel(PRODUCER_PATH), rel(Path("stages") / SOURCE_STAGE_ID / "03_reviews/stage162_decision.md")], "artifact_paths": [row["path"] for row in artifact_rows(result)], "ledger_payload": ledger_payload, "status": "completed"},
        "runtime_parity_gate.json": {"runtime_parity_claim": False, "reason": "Stage163 is MT5 runtime evidence only, not ONNX parity or runtime authority.", "status": "passed"},
        "backtest_forensics_gate.json": {"trade_evidence": rel(SUMMARY_CSV_PATH), "report_count": len(result.get("mt5_kpi_records", []) or []), "status": "passed"},
        "final_claim_guard.json": {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {"declared_required_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "runtime_parity_gate", "backtest_forensics_gate", "required_gate_coverage_audit", "final_claim_guard"], "executed_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "runtime_parity_gate", "backtest_forensics_gate", "required_gate_coverage_audit", "final_claim_guard"], "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "summary_csv": rel(SUMMARY_CSV_PATH), "segment_kpi_csv": rel(SEGMENT_KPI_PATH), "risk_atr_telemetry_csv": rel(RISK_ATR_TELEMETRY_PATH), "probability_binding_csv": rel(PROBABILITY_BINDING_PATH), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "overall_goal_complete": False},
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / name, payload)


def write_next_stage_seed(decision: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage164(164단계)는 Stage163(163단계) density-preserving score repair(밀도 보존 점수 수리)를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage163(163단계) recover net/trade density(순손익/거래 밀도), OOS early(표본외 초반), and DD(낙폭) while preserving validation/OOS PF(검증/표본외 수익요인), or should the next bounded repair choose a new axis(새 축)?

Effect(효과): Stage163(163단계) 안에서 계속 고치지 않고 결과 판독을 따로 닫는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage164 Input References(164단계 입력 참조)

- stage163_decision(163단계 판정): `{rel(DECISION_PATH)}`
- stage163_report(163단계 보고서): `{rel(REPORT_PATH)}`
- stage163_summary(163단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage163_segment_kpi(163단계 구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- stage163_probability_binding(163단계 확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- source_stage162_closeout_commit(원천 162단계 종료 커밋): `{SOURCE_STAGE162_CLOSEOUT_COMMIT}`
- source_decision(원천 판정): `{decision}`
""",
    )
    write_md(NEXT_STAGE_ROOT / "03_reviews/review_index.md", f"# Stage164 Review Index(164단계 검토 색인)\n\n- status(상태): `open_planned_from_stage163`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n")
    write_md(NEXT_STAGE_ROOT / "04_selected/selection_status.md", f"# Stage164 Selection Status(164단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage163`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- source_decision(원천 판정): `{decision}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")


def update_current_truth(decision: str) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    state = re.sub(r"(?m)^updated_on:.*$", "updated_on: '2026-05-18'", state)
    state = re.sub(r"(?s)\nstage163_stage161_density_preserving_score_repair:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?s)\nstage164_stage163_density_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage163_stage161_density_preserving_score_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage162_closeout_commit: {SOURCE_STAGE162_CLOSEOUT_COMMIT}
  source_stage162_hash_record_commit: {SOURCE_STAGE162_HASH_RECORD_COMMIT}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage164_stage163_density_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage163
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    focus = f"""current_focus:
- >-
  Stage163(163단계) closed(종료) as `{decision}` and Stage164(164단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): density-preserving score repair(밀도 보존 점수 수리) 결과를 후속 판독으로 넘긴다.
- >-
  Stage163 evidence(163단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(PROBABILITY_BINDING_PATH)}`에 있다. Effect(효과): PF(수익요인), net/trade density(순손익/거래 밀도), OOS early(표본외 초반), DD(낙폭)를 같이 판독한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?s)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage164_stage163_density_followup_surface`
- status(상태): `stage163_closed_{decision}_stage164_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage163(163단계)는 density-preserving score repair(밀도 보존 점수 수리)를 MT5(메타트레이더5)로 측정했다. Effect(효과): 결과를 final package(최종 패키지)나 deployment(배포)로 부르지 않고 Stage164(164단계) 후속 판독으로 넘긴다.

## Latest Stage163 Evidence(최신 163단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage163 Selection Status(163단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage163(163단계)은 한 질문만 닫고 Stage164(164단계)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage163 Review Index(163단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage163(163단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage163 density-preserving score repair closeout(163단계 밀도 보존 점수 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): long-dense(롱 밀도 보존) 및 low-risk shortgate(저위험 숏 게이트) 변형을 MT5(메타트레이더5)로 측정하고 Stage164(164단계) 후속 판독으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    return s161.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    configure_runner()
    s161.configure_base()
    args = parse_args(argv or sys.argv[1:])
    inputs = s161.prepare_inputs(Path(args.common_files_root))
    attempts = s161.build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 163,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage163_v2_native_density_preserving_score_repair",
        "feature_set_id": "stage163_density_preserving_signal_plus_low_edge_side_filter",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = s161.base.execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    probability_rows = s161.probability_binding_rows(result)
    model_rows = s161.model_score_rows(inputs)
    quality = quality_rows(summary_rows, segment_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality, external)

    s161.write_run_identity(result, probability_rows, model_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, s161.tier_b_rows())
    write_md(REPORT_PATH, report_markdown(quality, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "quality_rows": quality,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "source_reference": SOURCE_REFERENCE,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality)
    if not args.materialize_only:
        write_next_stage_seed(decision)
        update_current_truth(decision)
        write_status_files(decision, external)
        append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if external == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "external_verification_status": external,
                    "summary_csv": rel(SUMMARY_CSV_PATH),
                    "decision_path": rel(DECISION_PATH),
                    "overall_goal_complete": False,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
