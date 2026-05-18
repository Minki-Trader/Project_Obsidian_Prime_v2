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

STAGE_ID = "185_adapter_research__stage184_midsegment_quality_followup_review"
RUN_ID = "run185A_stage185_stage184_midsegment_quality_followup_review_v1"
PACKET_ID = "stage185_stage184_midsegment_quality_followup_review_v1"
PARENT_RUN_ID = "run184A_stage184_tp45_midwide_midsegment_quality_repair_v1"
SOURCE_STAGE_ID = "184_adapter_research__tp45_midwide_midsegment_quality_repair"
SOURCE_RUN_ID = "run184A_stage184_tp45_midwide_midsegment_quality_repair_v1"
SOURCE_STAGE184_CLOSEOUT_COMMIT = "4d7febab4cc8f55b23a65f6f33f2615bf973301d"
SOURCE_STAGE184_HASH_RECORD_COMMIT = "c8ce36c773ea50caf51a84f758ec3987795154d7"
NEXT_STAGE_ID = "186_adapter_research__tp45_midwide_bracket_shape_repair"
NEXT_RUN_ID = "run186A_stage186_tp45_midwide_bracket_shape_repair_v1"
NEXT_PACKET_ID = "stage186_tp45_midwide_bracket_shape_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage184_mt5_reports_completed"
DECISION = "open_stage186_tp45_midwide_bracket_shape_repair_candidate_not_final"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REPORT = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_midsegment_quality_report.md")
SOURCE_QUALITY = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_quality_matrix.csv")
SOURCE_SEGMENT = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_segment_kpi_summary.csv")
SOURCE_BALANCE = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_balance_curve_audit.csv")
SOURCE_MONTHLY = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_monthly_kpi_summary.csv")
SOURCE_RISK_ATR = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_risk_atr_telemetry.csv")
SOURCE_TRADE_AUDIT = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_trade_audit.csv")
SOURCE_DECISION = Path("stages/184_adapter_research__tp45_midwide_midsegment_quality_repair/03_reviews/stage184_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage185_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage185_quality_tradeoff_matrix.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage185_route_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage185_failure_attribution.csv"
DECISION_PATH = REVIEWS_ROOT / "stage185_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage185/stage184_midsegment_quality_followup_review.py")
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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def load_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        value = row.get(key, default)
        if value in (None, ""):
            return default
        return float(str(value).replace(",", "").replace("%", ""))
    except (TypeError, ValueError):
        return default


def segment_lookup(segment_rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    result: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in segment_rows:
        if row.get("split") != "validation_is" or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == "chronological_third":
            result[(str(row.get("adapter_id", "")), str(row.get("segment", "")))] = row
    return result


def build_tradeoff_rows(quality_rows: Sequence[Mapping[str, str]], segment_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    segments = segment_lookup(segment_rows)
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        mid = segments.get((adapter_id, "mid"), {})
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_pf": as_float(row, "validation_pf"),
                "validation_net": as_float(row, "validation_net"),
                "validation_dd": as_float(row, "validation_balance_dd_percent"),
                "validation_mid_pf": as_float(row, "validation_mid_pf"),
                "validation_mid_net": as_float(mid, "net_profit"),
                "validation_mid_mfe_capture": as_float(mid, "mfe_capture_ratio"),
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": as_float(row, "oos_net"),
                "oos_dd": as_float(row, "oos_balance_dd_percent"),
                "quality_flags": row.get("quality_flags", ""),
                "route_read": route_read(row),
            }
        )
    return rows


def route_read(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    if "qwide" in adapter_id:
        return "wide_quality_gate_damaged_net_oos_and_mid_pf"
    if "thr" in adapter_id:
        return "threshold_lift_no_trade_effect"
    return "control_near_miss_still_dd_and_mid_pf_failed"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            as_float(row, "validation_net") >= LEGACY_34D["net_profit"],
            as_float(row, "validation_pf") >= LEGACY_34D["profit_factor"],
            -max(0.0, as_float(row, "validation_dd") - LEGACY_34D["max_drawdown_percent"]),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_pf"),
        ),
    )


def build_route_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_row(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "route": "stage186_primary",
            "decision": DECISION,
            "source_clue": best.get("adapter_id", ""),
            "bounded_question": "Can bracket/exit shape(브래킷/청산 모양) improve MFE capture(최대유리이동 포착) and mid PF(중반 수익요인) without broad entry filtering(넓은 진입 필터링)?",
            "why": "threshold(문턱값) did not change trades, and qwide gate(넓은 품질 제한문)는 net/OOS/mid PF(순손익/표본외/중반 수익요인)를 망가뜨렸다.",
            "guardrail": "do_not_continue_wide_entry_gate_as_primary_repair",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory",
            "decision": DECISION,
            "source_clue": "stage184_qwide",
            "bounded_question": "Preserve qwide gate(넓은 품질 제한문) as failure memory(실패 기억).",
            "why": "It lowered trade count(거래 수) but worsened validation net(검증 순손익), mid PF(중반 수익요인), and OOS DD(표본외 낙폭).",
            "guardrail": "do_not_hide_failed_branch",
        },
    ]


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_row(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "threshold lift(문턱값 상향)은 control(대조군)과 같은 KPI(핵심 성과 지표)를 냈다.",
            "likely_driver": "model score(모델 점수)가 이 구간에서 충분히 이산적이라 threshold(문턱값) 변화가 실제 진입을 바꾸지 못했다.",
            "effect": "threshold-only repair(문턱값만 수정)는 다음 주축으로 쓰지 않는다.",
            "evidence": f"best={best.get('adapter_id', '')}; val_net={as_float(best, 'validation_net'):.2f}; val_dd={as_float(best, 'validation_dd'):.4f}; mid_pf={as_float(best, 'validation_mid_pf'):.6f}",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "qwide gate(넓은 품질 제한문)는 거래를 줄였지만 edge(우위)를 같이 잘랐다.",
            "likely_driver": "entry context(진입 문맥) 필터가 중반 손실만이 아니라 late/early winner(후반/초반 승자)도 제거했다.",
            "effect": "다음 stage(단계)는 entry gate(진입 제한문)보다 bracket/exit shape(브래킷/청산 모양)으로 간다.",
            "evidence": "qwide_val_net=553.78;qwide_mid_pf=1.318767;qwide_oos_dd=16.4543",
        },
    ]


def table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | axis(축) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS DD%(표본외 낙폭) | route read(경로 판독) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {axis} | {validation_pf:.6f} | {validation_net:.2f} | {validation_dd:.4f} | {validation_mid_pf:.6f} | {oos_dd:.4f} | {route_read} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]]) -> str:
    best = best_row(tradeoff_rows)
    return f"""# Stage185 Stage184 Midsegment Quality Follow-up Review(185단계 184단계 중반 구간 품질 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage184_closeout_commit(원천 184단계 종료 커밋): `{SOURCE_STAGE184_CLOSEOUT_COMMIT}`
- source_stage184_hash_record_commit(원천 184단계 해시 기록 커밋): `{SOURCE_STAGE184_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

{table(tradeoff_rows)}

## Simple Read(쉬운 판독)

Stage184(184단계)는 실패 경로다. Effect(효과): threshold(문턱값)는 거래를 바꾸지 못했고, qwide quality gate(넓은 품질 제한문)는 net(순손익), mid PF(중반 수익요인), OOS DD(표본외 낙폭)를 악화했다.

## Best Remaining Clue(남은 최선 단서)

- adapter(어댑터): `{best.get("adapter_id", "none")}`
- validation_net(검증 순손익): `{as_float(best, "validation_net"):.2f}`
- validation_dd(검증 낙폭): `{as_float(best, "validation_dd"):.4f}`
- validation_mid_pf(검증 중반 수익요인): `{as_float(best, "validation_mid_pf"):.6f}`

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): entry-gate repair(진입 제한문 수정)는 실패했으므로 bracket/exit shape(브래킷/청산 모양)으로 좁힌다.

Stage185(185단계)는 research/development only(연구개발 전용)이다. Effect(효과): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
"""


def decision_markdown() -> str:
    return f"""# Stage185 Decision(185단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage184_closeout_commit(원천 184단계 종료 커밋): `{SOURCE_STAGE184_CLOSEOUT_COMMIT}`
- source_stage184_hash_record_commit(원천 184단계 해시 기록 커밋): `{SOURCE_STAGE184_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage185(185단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage186(186단계)에서 TP45(익절 4.5) midwide bracket/exit shape(중간넓은 문맥 브래킷/청산 모양)를 좁게 측정한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    for path in (PRODUCER_PATH, REPORT_PATH, DECISION_PATH, TRADEOFF_MATRIX_PATH, ROUTE_MATRIX_PATH, ATTRIBUTION_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage185_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage185 Stage184 midsegment quality follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = best_row(tradeoff_rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage185_stage184_midsegment_quality_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage184_closeout_commit", SOURCE_STAGE184_CLOSEOUT_COMMIT),
                        ("source_stage184_hash_record_commit", SOURCE_STAGE184_HASH_RECORD_COMMIT),
                        ("primary_clue", best.get("adapter_id", "none")),
                        ("target_surface", TARGET_SURFACE),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage184_midsegment_quality_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage184_midsegment_quality_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage184_midsegment_quality_followup_review",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best", best.get("adapter_id", "none")),
                    ("validation_net", f"{as_float(best, 'validation_net'):.2f}"),
                    ("validation_dd", f"{as_float(best, 'validation_dd'):.4f}"),
                    ("validation_mid_pf", f"{as_float(best, 'validation_mid_pf'):.6f}"),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("claim_boundary", BOUNDARY),
                    ("route_count", len(route_rows)),
                    ("overall_goal_complete", 0),
                )
            ),
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage185 reviewed Stage184 failure and opened Stage186 bracket shape repair.",
        }
    ]
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
    }


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "attribution": rel(ATTRIBUTION_PATH),
        "tradeoff_rows": list(tradeoff_rows),
        "route_rows": list(route_rows),
        "attribution_rows": list(attribution_rows),
        "ledger_payload": ledger_payload,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage185 Closeout Packet(185단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `completed`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage186(186단계)는 TP45(익절 4.5) midwide context(중간넓은 문맥) 표면에서 bracket/exit shape(브래킷/청산 모양)를 좁게 고친다.

## Bounded Question(경계 질문)

Can a bounded ATR bracket/exit shape repair(ATR 브래킷/청산 모양 수정) improve validation mid PF(검증 중반 수익요인), MFE capture(최대유리이동 포착), and validation DD(검증 낙폭) while preserving validation net/PF(검증 순손익/수익요인), OOS DD(표본외 낙폭), model-controlled risk(모델 제어 위험), and telemetry(기록)?

Effect(효과): Stage184(184단계)의 failed entry gate(실패한 진입 제한문)를 반복하지 않고, 같은 TP45(익절 4.5) midwide surface(중간넓은 표면)의 청산/브래킷 축만 좁게 본다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage186 Inputs(186단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- source_stage184_quality(원천 184단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage184_segment(원천 184단계 구간): `{rel(SOURCE_SEGMENT)}`
- source_stage184_risk_atr(원천 184단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- source_stage184_trade_audit(원천 184단계 거래 감사): `{rel(SOURCE_TRADE_AUDIT)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage186 Review Index(186단계 검토 색인)

- status(상태): `open_planned_from_stage185`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage186 Selection Status(186단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage185`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage185(185단계) closed(종료) as `{DECISION}` and Stage186(186단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): failed entry gate repair(실패한 진입 제한문 수정)를 멈추고 bracket/exit shape repair(브래킷/청산 모양 수정)로 좁힌다.
- >-
  Stage185 evidence(185단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`에 있다. Effect(효과): Stage184(184단계)의 실패를 장부화하고 다음 축을 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage185_stage184_midsegment_quality_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage185_stage184_midsegment_quality_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_MATRIX_PATH)}
  route_matrix_path: {rel(ROUTE_MATRIX_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage186_tp45_midwide_bracket_shape_surface`
- status(상태): `stage185_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage185(185단계)는 Stage184(184단계)의 midsegment quality repair(중반 구간 품질 수정)를 follow-up review(후속 검토)로 판독했다. Effect(효과): entry gate(진입 제한문) 축은 failure memory(실패 기억)로 보존하고 Stage186(186단계) bracket/exit shape(브래킷/청산 모양)로 좁힌다.

## Latest Stage185 Evidence(최신 185단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage185 Selection Status(185단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage185 Review Index(185단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage185 Stage184 midsegment quality follow-up review closeout(185단계 184단계 중반 구간 품질 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage184(184단계) entry gate repair(진입 제한문 수정) 실패를 기록하고 Stage186(186단계) bracket/exit shape repair(브래킷/청산 모양 수정)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = load_csv(SOURCE_QUALITY)
    segment_rows = load_csv(SOURCE_SEGMENT)
    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows)
    route_rows = build_route_rows(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_md(REPORT_PATH, report_markdown(tradeoff_rows, route_rows, attribution_rows))
    write_md(DECISION_PATH, decision_markdown())
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(tradeoff_rows, route_rows, artifacts)
    write_packet_files(tradeoff_rows, route_rows, attribution_rows, ledger_payload)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "external_verification_status": EXTERNAL_STATUS,
                    "report": rel(REPORT_PATH),
                    "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
                    "route_matrix": rel(ROUTE_MATRIX_PATH),
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
    raise SystemExit(main())
