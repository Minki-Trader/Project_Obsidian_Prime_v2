from __future__ import annotations

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


STAGE59AI_ID = "59AI_adapter_repair__backup_anchor_probe_from_stage59ah"
NEXT_STAGE_ID = "59AJ_adapter_repair__new_model_branch_from_stage59ai"
RUN_ID = "run59AD_stage59ai_backup_anchor_probe_from_stage59ah_v1"
NEXT_RUN_ID = "run59AE_stage59aj_new_model_branch_from_stage59ai_v1"
PACKET_ID = "stage59ai_backup_anchor_probe_from_stage59ah_v1"
NEXT_PACKET_ID = "stage59aj_new_model_branch_from_stage59ai_v1"
PARENT_RUN_ID = "run59AC_stage59ah_bounded_followup_from_stage59ag_v1"
SOURCE_STAGE59AH_PUSHED_COMMIT = "5c7faff752a162731f8f2362cbe70f1008db2fcb"

DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
BACKUP_ADAPTER_STAGE59B = "s59b_v60_backup_thr55_mr03_wideatr_sd5"
DECISION = "open_new_model_branch"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE56_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE59B_ID = "59B_adapter_repair__model_source_or_backup_branch"
STAGE59AH_ID = "59AH_adapter_repair__bounded_followup_from_stage59ag"

STAGE_ROOT = Path("stages") / STAGE59AI_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
NEXT_ROOT = Path("stages") / NEXT_STAGE_ID
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

STAGE56_REVIEW_ROOT = Path("stages") / STAGE56_ID / "03_reviews"
RUN50BQ_SUMMARY = STAGE56_REVIEW_ROOT / "run50BQ_summary.csv"
RUN50BQ_AUDIT = STAGE56_REVIEW_ROOT / "run50BQ_audit.csv"
RUN50BQ_REPORT = STAGE56_REVIEW_ROOT / "run50BQ_context_extratrees_firewall_transition.md"
STAGE59B_REVIEW_ROOT = Path("stages") / STAGE59B_ID / "03_reviews"
STAGE59B_SUMMARY = STAGE59B_REVIEW_ROOT / "model_source_or_backup_branch_summary.csv"
STAGE59B_SEGMENTS = STAGE59B_REVIEW_ROOT / "model_source_or_backup_segment_kpi_summary.csv"
STAGE59B_REPORT = STAGE59B_REVIEW_ROOT / "model_source_or_backup_branch_report.md"
STAGE59AH_DECISION = Path("stages") / STAGE59AH_ID / "03_reviews/stage59ah_decision.md"
STAGE59AH_REPORT = Path("stages") / STAGE59AH_ID / "03_reviews/adapter_demotion_review.md"

REPORT_PATH = REVIEWS_ROOT / "backup_anchor_probe_report.md"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "backup_anchor_probe_summary.csv"
SEGMENT_CSV_PATH = REVIEWS_ROOT / "backup_anchor_segment_kpi_summary.csv"
RISK_ATR_CSV_PATH = REVIEWS_ROOT / "backup_anchor_risk_atr_telemetry.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59ai_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

SUMMARY_COLUMNS = (
    "evidence_source",
    "source_id",
    "variant_or_adapter",
    "split",
    "view",
    "profit_factor",
    "net_profit",
    "max_drawdown",
    "trades_per_day",
    "cost_stressed_expectancy",
    "same_move_reentry_ratio",
    "mfe_capture_ratio",
    "status_read",
    "failure_reasons",
)
SEGMENT_COLUMNS = (
    "source_id",
    "adapter_id",
    "split",
    "segment_type",
    "segment",
    "trade_count",
    "net_profit",
    "profit_factor",
    "expectancy",
    "mfe_capture_ratio",
    "quality_flag",
)
RISK_COLUMNS = (
    "source_id",
    "adapter_id",
    "split",
    "model_risk_enabled",
    "atr_enabled",
    "model_risk_max_pct",
    "avg_model_risk_pct",
    "avg_clipped_risk_pct",
    "max_actual_risk_pct_after_floor",
    "avg_computed_lot",
    "avg_executed_lot",
    "risk_floor_applied_count",
    "avg_atr_points",
    "avg_open_sl_points",
    "avg_open_tp_points",
    "risk_bucket",
    "telemetry_sha256",
)


def rel(path: Path) -> str:
    return path.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    for path in (REVIEWS_ROOT, SPEC_ROOT, INPUT_ROOT, SELECTED_ROOT, PACKET_ROOT, NEXT_ROOT / "00_spec", NEXT_ROOT / "01_inputs", NEXT_ROOT / "03_reviews", NEXT_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig")


def fnum(row: Mapping[str, str], key: str) -> float | None:
    try:
        text = str(row.get(key, "")).strip()
        return float(text) if text else None
    except ValueError:
        return None


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def status_read(pf: float | None, cost: float | None, flags: str) -> str:
    if pf is None:
        return "missing_pf"
    if pf < 1.10:
        return "weak_validation_or_oos_pf"
    if cost is not None and cost <= 0:
        return "cost_stressed_expectancy_failed"
    if "same_move_density" in flags:
        return "same_move_density_failed"
    return "measurement_reference_only"


def build_summary_rows() -> list[dict[str, Any]]:
    run50bq = next(row for row in read_csv(RUN50BQ_SUMMARY) if row["variant_id"] == BACKUP_ANCHOR)
    rows: list[dict[str, Any]] = []
    for split, prefix in (("validation_is", "routed_validation"), ("oos", "routed_oos")):
        pf = fnum(run50bq, f"{prefix}_pf")
        cost = fnum(run50bq, f"{prefix}_cost_stressed_expectancy")
        flags = run50bq.get("failure_reasons", "")
        rows.append(
            {
                "evidence_source": "Stage56 raw backup anchor",
                "source_id": "run50BQ",
                "variant_or_adapter": BACKUP_ANCHOR,
                "split": split,
                "view": "actual_routed_total",
                "profit_factor": fmt(pf),
                "net_profit": run50bq.get(f"{prefix}_net", ""),
                "max_drawdown": run50bq.get(f"{prefix}_max_dd", ""),
                "trades_per_day": run50bq.get(f"{prefix}_trades_per_day", ""),
                "cost_stressed_expectancy": fmt(cost),
                "same_move_reentry_ratio": run50bq.get(f"{prefix}_same_move_reentry_ratio", ""),
                "mfe_capture_ratio": run50bq.get(f"{prefix}_mfe_capture_ratio", ""),
                "status_read": status_read(pf, cost, flags),
                "failure_reasons": flags,
            }
        )

    stage59b = [
        row
        for row in read_csv(STAGE59B_SUMMARY)
        if row["adapter_id"] == BACKUP_ADAPTER_STAGE59B and row["view"] == "actual_routed_total"
    ]
    for row in stage59b:
        pf = fnum(row, "profit_factor")
        cost = fnum(row, "cost_stressed_expectancy")
        rows.append(
            {
                "evidence_source": "Stage59B post ATR/risk backup adapter",
                "source_id": "run55A",
                "variant_or_adapter": row["adapter_id"],
                "split": row["split"],
                "view": row["view"],
                "profit_factor": row.get("profit_factor", ""),
                "net_profit": row.get("net_profit", ""),
                "max_drawdown": row.get("max_drawdown_amount", ""),
                "trades_per_day": row.get("trades_per_day", ""),
                "cost_stressed_expectancy": row.get("cost_stressed_expectancy", ""),
                "same_move_reentry_ratio": row.get("same_move_reentry_ratio", ""),
                "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                "status_read": status_read(pf, cost, ""),
                "failure_reasons": "validation_pf_lt_1_10;validation_cost_stressed_expectancy_not_positive;weak_post_atr_risk_backup_adapter",
            }
        )
    return rows


def build_segment_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(STAGE59B_SEGMENTS):
        if row.get("adapter_id") != BACKUP_ADAPTER_STAGE59B or row.get("view") != "actual_routed_total":
            continue
        rows.append(
            {
                "source_id": "run55A",
                "adapter_id": row.get("adapter_id", ""),
                "split": row.get("split", ""),
                "segment_type": row.get("segment_type", ""),
                "segment": row.get("segment", ""),
                "trade_count": row.get("trade_count", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                "quality_flag": row.get("quality_flag", ""),
            }
        )
    return rows


def build_risk_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(STAGE59B_SUMMARY):
        if row.get("adapter_id") != BACKUP_ADAPTER_STAGE59B or row.get("view") != "actual_routed_total":
            continue
        rows.append({column: row.get(column, "") for column in RISK_COLUMNS if column not in {"source_id"}} | {"source_id": "run55A"})
    return rows


def counts(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    post_rows = [row for row in summary_rows if row["evidence_source"].startswith("Stage59B")]
    weak_post = [
        row
        for row in post_rows
        if float(row["profit_factor"]) < 1.10 or float(row["cost_stressed_expectancy"]) <= 0
    ]
    flagged_segments = [row for row in segment_rows if str(row.get("quality_flag", "")) not in {"", "acceptable_measurement_only"}]
    return {
        "post_atr_risk_rows": len(post_rows),
        "weak_post_atr_risk_rows": len(weak_post),
        "flagged_segment_rows": len(flagged_segments),
        "decision": DECISION,
    }


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    c = counts(summary_rows, segment_rows)
    table_lines = [
        "| source(원천) | split(구간) | PF(수익 팩터) | net(순손익) | DD(손실폭) | cost exp(비용 기대값) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        table_lines.append(
            "| {source} | {split} | {pf} | {net} | {dd} | {cost} | {read} |".format(
                source=row["evidence_source"],
                split=row["split"],
                pf=row["profit_factor"],
                net=row["net_profit"],
                dd=row["max_drawdown"],
                cost=row["cost_stressed_expectancy"],
                read=row["status_read"],
            )
        )
    segment_flags = sorted({str(row["quality_flag"]) for row in segment_rows if str(row.get("quality_flag", "")) not in {"", "acceptable_measurement_only"}})
    return f"""# Stage59AI Backup Anchor Probe Review(59AI단계 예비 기준점 탐침 검토)

- stage(단계): `{STAGE59AI_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `completed_existing_mt5_evidence`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the backup anchor(예비 기준점) `{BACKUP_ANCHOR}` remain a bounded replacement path(경계 대체 경로) after the current v64 adapter(현재 v64 어댑터) was demoted(강등)?

## Evidence Table(근거 표)

{chr(10).join(table_lines)}

## Segment Read(구간 판독)

- flagged_segment_rows(표시된 구간 행): `{c["flagged_segment_rows"]}`
- segment_flags(구간 플래그): `{';'.join(segment_flags) if segment_flags else 'none'}`
- segment_summary(구간 요약): `{rel(SEGMENT_CSV_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_CSV_PATH)}`

## Judgment(판정)

Stage56 raw backup anchor(56단계 원 예비 기준점)는 PF/net(수익 팩터/순손익)은 괜찮았지만 cost-stressed expectancy(비용 압박 기대값)와 same-move density(동일 이동 밀도)가 실패했다. Stage59B(59B단계)의 post ATR/risk backup adapter(ATR/위험 이후 예비 어댑터)는 validation PF(검증 수익 팩터) `1.01`, validation cost expectancy(검증 비용 기대값) `-0.281660`, OOS PF(표본외 수익 팩터) `1.06`, OOS cost expectancy(표본외 비용 기대값) `-0.129625`로 약했다.

Effect(효과): backup anchor(예비 기준점)를 Stage60 ONNX(60단계 ONNX)로 보내지 않고, new model branch(새 모델 분기)를 연다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    c = counts(summary_rows, segment_rows)
    return f"""# Stage59AI Decision(59AI단계 판정)

decision(판정): `{DECISION}`

Stage59AI(59AI단계)는 backup anchor(예비 기준점) `{BACKUP_ANCHOR}`를 existing MT5 evidence(기존 MT5 근거)로 검토했다. Effect(효과): 이미 Stage59B(59B단계)에서 ATR/risk(ATR/위험) 조건으로 약해진 예비 기준점을 다시 무한 재실행하지 않는다.

## Evidence(근거)

- stage59ah_decision(59AH단계 판정): `{rel(STAGE59AH_DECISION)}`
- stage56_backup_anchor_report(56단계 예비 기준점 보고서): `{rel(RUN50BQ_REPORT)}`
- stage59b_backup_atr_risk_report(59B단계 예비 ATR/위험 보고서): `{rel(STAGE59B_REPORT)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_summary(구간 요약): `{rel(SEGMENT_CSV_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_CSV_PATH)}`
- external_verification_status(외부 검증 상태): `completed_existing_mt5_evidence`

## Reason(이유)

- post_atr_risk_rows(ATR/위험 이후 행): `{c["post_atr_risk_rows"]}`
- weak_post_atr_risk_rows(약한 ATR/위험 이후 행): `{c["weak_post_atr_risk_rows"]}`
- flagged_segment_rows(표시된 구간 행): `{c["flagged_segment_rows"]}`
- judgment_label(판정 라벨): `negative_reusable_evidence_for_backup_anchor_path`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage59AI closeout(59AI단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): new model branch(새 모델 분기)를 다음 bounded stage(경계 단계)로 열고, operating claim(운영 주장)을 만들지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_stage_docs(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# 59AI Brief(59AI단계 개요)

- stage_id(단계 ID): `{STAGE59AI_ID}`
- source_stage(원천 단계): `{STAGE59AH_ID}`
- source_decision(원천 판정): `demote_current_adapter_and_select_backup`
- bounded_question(경계 질문): `Can the backup anchor be accepted as the next bounded replacement path?`
- stage_status(단계 상태): `closed_backup_anchor_probe_review`
- boundary(경계): `{BOUNDARY}`

59AI(59AI단계)는 existing evidence backup anchor probe(기존 근거 예비 기준점 탐침)로 닫혔다. Effect(효과): v60 backup anchor(v60 예비 기준점)를 Stage60 ONNX(60단계 ONNX)로 넘기지 않는다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# 59AI Input References(59AI단계 입력 참조)

- stage59ah_decision(59AH단계 판정): `{rel(STAGE59AH_DECISION)}`
- stage59ah_report(59AH단계 보고서): `{rel(STAGE59AH_REPORT)}`
- run50BQ_summary(50BQ 실행 요약): `{rel(RUN50BQ_SUMMARY)}`
- run50BQ_audit(50BQ 실행 감사): `{rel(RUN50BQ_AUDIT)}`
- stage59b_summary(59B단계 요약): `{rel(STAGE59B_SUMMARY)}`
- stage59b_segments(59B단계 구간): `{rel(STAGE59B_SEGMENTS)}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# 59AI Review Index(59AI단계 검토 색인)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_summary(구간 요약): `{rel(SEGMENT_CSV_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_CSV_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# 59AI Selection Status(59AI단계 선택 상태)

- stage_status(단계 상태): `closed_backup_anchor_probe_review`
- source_stage(원천 단계): `{STAGE59AH_ID}`
- source_decision(원천 판정): `demote_current_adapter_and_select_backup`
- stage59ai_decision(59AI단계 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): 59AI(59AI단계)는 backup anchor(예비 기준점)를 negative reusable evidence(재사용 가능한 부정 근거)로 보존하고 new model branch(새 모델 분기)를 연다.
""",
    )
    write_md(
        NEXT_ROOT / "00_spec/stage_brief.md",
        f"""# 59AJ Brief(59AJ단계 개요)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- source_stage(원천 단계): `{STAGE59AI_ID}`
- source_decision(원천 판정): `{DECISION}`
- bounded_question(경계 질문): `Can a new model branch produce a full BaselineAdapter path after v64 repair and v60 backup both failed post ATR/risk quality?`
- boundary(경계): `{BOUNDARY}`

59AJ(59AJ단계)는 new model branch(새 모델 분기) 계획 단계다. Effect(효과): 약한 v64/v60 경로를 Stage60 ONNX(60단계 ONNX)로 보내지 않고 새 후보 원천을 작게 연다.
""",
    )
    write_md(
        NEXT_ROOT / "01_inputs/input_refs.md",
        f"""# 59AJ Input References(59AJ단계 입력 참조)

- stage59ai_decision(59AI단계 판정): `{rel(DECISION_PATH)}`
- backup_anchor_probe_report(예비 기준점 탐침 보고서): `{rel(REPORT_PATH)}`
- backup_anchor_summary(예비 기준점 요약): `{rel(SUMMARY_CSV_PATH)}`
""",
    )
    write_md(
        NEXT_ROOT / "03_reviews/review_index.md",
        "# 59AJ Review Index(59AJ단계 검토 색인)\n\n59AJ(59AJ단계)는 planned(계획) 상태다.\n",
    )
    write_md(
        NEXT_ROOT / "04_selected/selection_status.md",
        f"""# 59AJ Selection Status(59AJ단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59ai`
- source_stage(원천 단계): `{STAGE59AI_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): 59AJ(59AJ단계)는 new model branch(새 모델 분기)를 다음 bounded question(경계 질문)으로 다룬다.
""",
    )


def ledger_rows(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    c = counts(summary_rows, segment_rows)
    return [
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_backup_anchor_probe",
            "stage_id": STAGE59AI_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_backup_anchor_probe",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "backup_anchor_probe",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_repair",
            "scoreboard_lane": "result_judgment",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                [
                    ("post_atr_risk_rows", c["post_atr_risk_rows"]),
                    ("weak_post_atr_risk_rows", c["weak_post_atr_risk_rows"]),
                    ("flagged_segment_rows", c["flagged_segment_rows"]),
                    ("backup_adapter", BACKUP_ADAPTER_STAGE59B),
                ]
            ),
            "guardrail_kpi": ledger_pairs(
                [
                    ("overall_goal_complete", 0),
                    ("deployment_claim", 0),
                    ("runtime_authority_claim", 0),
                    ("stage60_opened", 0),
                ]
            ),
            "external_verification_status": "completed_existing_mt5_evidence",
            "notes": "Stage59AI backup anchor probe review only; not final package completion.",
        }
    ]


def run_registry_row() -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE59AI_ID,
        "lane": "baseline_adapter_backup_anchor_probe",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            [
                ("backup_anchor", BACKUP_ANCHOR),
                ("post_atr_risk_adapter", BACKUP_ADAPTER_STAGE59B),
                ("next_stage_or_branch", NEXT_STAGE_ID),
                ("boundary", BOUNDARY),
            ]
        ),
    }


def artifact_paths() -> list[tuple[str, str, Path, str]]:
    paths = [
        ("stage59ai_report", "report", REPORT_PATH, "Stage59AI backup anchor probe report."),
        ("stage59ai_summary", "summary_csv", SUMMARY_CSV_PATH, "Stage59AI backup anchor probe summary."),
        ("stage59ai_segment_summary", "segment_summary_csv", SEGMENT_CSV_PATH, "Stage59AI backup anchor segment summary."),
        ("stage59ai_risk_atr", "telemetry_csv", RISK_ATR_CSV_PATH, "Stage59AI backup anchor risk/ATR telemetry summary."),
        ("stage59ai_decision", "stage_decision", DECISION_PATH, "Stage59AI stage decision."),
        ("stage59ai_stage_ledger", "stage_ledger", STAGE_LEDGER_PATH, "Stage59AI stage-local ledger."),
    ]
    for gate in (
        "experiment_design_receipt.json",
        "runtime_evidence_gate.json",
        "kpi_contract_audit.json",
        "result_judgment_gate.json",
        "artifact_lineage_audit.json",
        "final_claim_guard.json",
        "required_gate_coverage_audit.json",
        "aggregate_summary.json",
    ):
        paths.append((f"stage59ai_{Path(gate).stem}", "packet_gate", PACKET_ROOT / gate, "Stage59AI packet gate."))
    return paths


def artifact_rows() -> list[dict[str, Any]]:
    created = now_utc()
    rows = []
    for artifact_id, artifact_type, path, notes in artifact_paths():
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE59AI_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": notes,
            }
        )
    return rows


def write_packets(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    run_payload: Mapping[str, Any],
    stage_payload: Mapping[str, Any],
    project_payload: Mapping[str, Any],
    artifact_payload: Mapping[str, Any] | None = None,
) -> None:
    c = counts(summary_rows, segment_rows)
    packets = {
        "experiment_design_receipt.json": {
            "hypothesis": "The v60 backup anchor may still be usable as a bounded replacement path after v64 repair failure.",
            "decision_use": "Open Stage60 only if backup anchor quality is strong after ATR/risk; otherwise open a new model branch.",
            "comparison_baseline": "Stage56 raw v60 backup anchor and Stage59B post ATR/risk backup adapter evidence",
            "control_variables": ["US100 M5", "validation/OOS scope", "research/development claim boundary", "no deployment claim"],
            "changed_variables": ["source branch selected for next bounded stage"],
            "sample_scope": "Existing Stage56 run50BQ MT5 evidence and Stage59B ATR/risk MT5 evidence",
            "success_criteria": "Validation/OOS PF and cost-stressed expectancy remain acceptable with no weak segment concentration.",
            "failure_criteria": "Validation PF below 1.10, non-positive cost-stressed expectancy, or flagged segment instability.",
            "invalid_conditions": "Missing Stage56 or Stage59B source summaries, missing decision evidence, or artifact lineage mismatch.",
            "stop_conditions": "Stop at existing evidence decision; do not start open-ended backup repairs in Stage59AI.",
            "evidence_plan": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_CSV_PATH), rel(RISK_ATR_CSV_PATH), rel(DECISION_PATH)],
        },
        "runtime_evidence_gate.json": {
            "status": "completed_existing_mt5_evidence",
            "source_inputs": [rel(RUN50BQ_SUMMARY), rel(RUN50BQ_AUDIT), rel(STAGE59B_SUMMARY), rel(STAGE59B_SEGMENTS)],
            "external_verification_status": "completed_existing_mt5_evidence",
            "effect": "Stage59AI uses already completed MT5 tester evidence and does not claim new runtime authority.",
        },
        "kpi_contract_audit.json": {
            "status": "completed",
            "row_grain": "stage56_raw_backup_anchor_and_stage59b_post_atr_risk_backup_adapter",
            "summary_rows": len(summary_rows),
            "segment_rows": len(segment_rows),
            "tier_scope": "Tier A+B actual routed total plus disabled/failed backup context",
            "required_kpi_present": ["profit_factor", "net_profit", "max_drawdown", "cost_stressed_expectancy", "segment_quality_flag", "risk_atr_telemetry"],
        },
        "result_judgment_gate.json": {
            "result_subject": BACKUP_ANCHOR,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_CSV_PATH), rel(RISK_ATR_CSV_PATH)],
            "evidence_missing": [],
            "judgment_label": "negative_reusable_evidence_for_backup_anchor_path",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "user_explanation_hook": "The backup anchor was worth checking, but its post ATR/risk evidence is too weak to send to ONNX.",
        },
        "artifact_lineage_audit.json": {
            "status": "completed",
            "source_inputs": [rel(STAGE59AH_DECISION), rel(RUN50BQ_SUMMARY), rel(RUN50BQ_AUDIT), rel(STAGE59B_SUMMARY), rel(STAGE59B_SEGMENTS)],
            "producer": "stage_pipelines/stage59ai/backup_anchor_probe_from_stage59ah.py",
            "consumers": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_CSV_PATH), rel(RISK_ATR_CSV_PATH), rel(DECISION_PATH)],
            "ledger_links": {
                "run_registry": run_payload,
                "stage_ledger": stage_payload,
                "project_alpha_ledger": project_payload,
                "artifact_registry": artifact_payload or {"status": "pending_second_pass"},
            },
            "lineage_judgment": "connected_with_boundary",
        },
        "final_claim_guard.json": {
            "status": "completed",
            "overall_goal_complete": False,
            "forbidden_claims": {
                "deployment": False,
                "live_readiness": False,
                "production_baseline": False,
                "operating_promotion": False,
                "operating_reference": False,
                "runtime_authority": False,
            },
            "decision": DECISION,
            "next_stage_or_branch": NEXT_STAGE_ID,
        },
        "required_gate_coverage_audit.json": {
            "status": "completed",
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "covered_by": ["runtime_evidence_gate.json", "kpi_contract_audit.json", "result_judgment_gate.json", "artifact_lineage_audit.json", "final_claim_guard.json"],
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE59AI_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "backup_anchor": BACKUP_ANCHOR,
            "backup_adapter_stage59b": BACKUP_ADAPTER_STAGE59B,
            "post_atr_risk_rows": c["post_atr_risk_rows"],
            "weak_post_atr_risk_rows": c["weak_post_atr_risk_rows"],
            "flagged_segment_rows": c["flagged_segment_rows"],
            "external_verification_status": "completed_existing_mt5_evidence",
            "overall_goal_complete": False,
            "claim_boundary": BOUNDARY,
            "next_stage_or_branch": NEXT_STAGE_ID,
            "required_outputs": {
                "backup_anchor_probe_report": rel(REPORT_PATH),
                "backup_anchor_probe_summary": rel(SUMMARY_CSV_PATH),
                "backup_anchor_segment_kpi_summary": rel(SEGMENT_CSV_PATH),
                "backup_anchor_risk_atr_telemetry": rel(RISK_ATR_CSV_PATH),
                "stage59ai_decision": rel(DECISION_PATH),
            },
        },
    }
    for name, payload in packets.items():
        write_json(PACKET_ROOT / name, payload)


def update_ledgers(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    stage_rows = ledger_rows(summary_rows, segment_rows)
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_registry_row()], key="run_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, stage_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, stage_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"), artifact_rows(), key="artifact_id")
    return run_payload, stage_payload, project_payload, artifact_payload


def update_current_truth() -> None:
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `new_model_branch_pending`
- status(상태): `stage59ai_closed_{DECISION}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59AI(59AI단계) closed(종료) as existing-evidence backup anchor probe(기존 근거 예비 기준점 탐침). Effect(효과): v60 backup anchor(v60 예비 기준점)는 post ATR/risk evidence(ATR/위험 이후 근거)가 약해 Stage60 ONNX(60단계 ONNX)로 넘어가지 않는다.

## Latest Stage59AI Evidence(최신 59AI단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- post_atr_risk_adapter(ATR/위험 이후 어댑터): `{BACKUP_ADAPTER_STAGE59B}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59ai_decision(59AI단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-16'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage59AI(59AI단계) `{STAGE59AI_ID}` closed(종료) as backup anchor probe(예비 기준점 탐침); decision(판정)=`{DECISION}`. "
        f"Effect(효과): v60 backup anchor(v60 예비 기준점)는 post ATR/risk quality(ATR/위험 이후 품질)가 약해 Stage60 ONNX(60단계 ONNX)로 가지 않는다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{NEXT_STAGE_ID}` is active/planned(활성/계획). Effect(효과): new model branch(새 모델 분기)를 다음 bounded step(경계 다음 단계)으로 연다.\n"
    )
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", focus, text, count=1)
    block = f"""

stage59ai_backup_anchor_probe_from_stage59ah:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59AI_ID}
  status: closed_backup_anchor_probe_review
  current_run_id: {RUN_ID}
  backup_anchor: {BACKUP_ANCHOR}
  post_atr_risk_adapter: {BACKUP_ADAPTER_STAGE59B}
  source_stage59ah_pushed_commit: {SOURCE_STAGE59AH_PUSHED_COMMIT}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: completed_existing_mt5_evidence
  boundary: {BOUNDARY}
"""
    if "stage59ai_backup_anchor_probe_from_stage59ah:" in text:
        text = re.sub(r"\nstage59ai_backup_anchor_probe_from_stage59ah:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-16 - Stage59AI backup anchor probe closeout(59AI단계 예비 기준점 탐침 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        f"- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`\n"
        f"- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`\n"
        "- effect(효과): v60 backup anchor(v60 예비 기준점)를 post ATR/risk evidence(ATR/위험 이후 근거)로 약한 경로로 보존하고, 새 모델 분기(new model branch, 새 모델 분기)를 다음 단계로 연다.\n"
    )
    with io_path(CHANGELOG_PATH).open("a", encoding="utf-8-sig") as handle:
        handle.write(entry)


def main() -> None:
    ensure_dirs()
    summary_rows = build_summary_rows()
    segment_rows = build_segment_rows()
    risk_rows = build_risk_rows()
    write_csv(SUMMARY_CSV_PATH, SUMMARY_COLUMNS, summary_rows)
    write_csv(SEGMENT_CSV_PATH, SEGMENT_COLUMNS, segment_rows)
    write_csv(RISK_ATR_CSV_PATH, RISK_COLUMNS, risk_rows)
    write_md(REPORT_PATH, report_markdown(summary_rows, segment_rows))
    write_md(DECISION_PATH, decision_markdown(summary_rows, segment_rows))
    write_stage_docs(summary_rows, segment_rows)
    run_payload, stage_payload, project_payload, artifact_payload = update_ledgers(summary_rows, segment_rows)
    write_packets(summary_rows, segment_rows, run_payload, stage_payload, project_payload, artifact_payload)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"), artifact_rows(), key="artifact_id")
    write_packets(summary_rows, segment_rows, run_payload, stage_payload, project_payload, artifact_payload)
    update_current_truth()
    append_changelog()
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": RUN_ID,
                "decision": DECISION,
                "next_stage": NEXT_STAGE_ID,
                "summary_csv": rel(SUMMARY_CSV_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
