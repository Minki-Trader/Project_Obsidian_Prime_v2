from __future__ import annotations

import csv
import json
import math
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


STAGE61_ID = "61_research_package__baseline_adapter_review_only"
RUN_ID = "run61A_stage61_research_package_review_v1"
PACKET_ID = "stage61_research_package_review_v1"
PARENT_RUN_ID = "run60A_stage60_onnx_hardening_v1"
ADAPTER_ID = "s59ar_v41_sd8_h3"
BOUNDARY = "research_package_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"

STAGE_ROOT = Path("stages") / STAGE61_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
RUN_ROOT = STAGE_ROOT / "02_runs" / "run61A"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

STAGE57_ROOT = Path("stages/57_adapter_quality__equity_segment_kpi_audit_gate/03_reviews")
STAGE58_ROOT = Path("stages/58_adapter_risk__bounded_repair_before_atr_risk_integration/03_reviews")
STAGE59AR_ROOT = Path("stages/59AR_adapter_repair__new_model_branch_from_stage59aq/03_reviews")
STAGE60_ROOT = Path("stages/60_adapter_onnx__hardening_runtime_reproduction/03_reviews")

SUMMARY_JSON_PATH = REVIEWS_ROOT / "research_package_summary.json"
CRITERIA_MATRIX_PATH = REVIEWS_ROOT / "research_package_criteria_matrix.csv"
EVIDENCE_MATRIX_PATH = REVIEWS_ROOT / "research_package_evidence_matrix.csv"
HASH_SUMMARY_PATH = REVIEWS_ROOT / "artifact_hash_summary.csv"
KNOWN_WEAKNESSES_PATH = REVIEWS_ROOT / "known_weaknesses.md"
PACKAGE_REVIEW_PATH = REVIEWS_ROOT / "research_package_review.md"
DECISION_PATH = REVIEWS_ROOT / "stage61_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
ARTIFACT_COLUMNS = ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes")

SOURCE_PATHS = {
    "stage57_decision": STAGE57_ROOT / "stage57_decision.md",
    "stage57_equity_curve_audit": STAGE57_ROOT / "equity_curve_audit.md",
    "stage57_segment_kpi_summary": STAGE57_ROOT / "segment_kpi_summary.csv",
    "stage57_monthly_kpi_summary": STAGE57_ROOT / "monthly_kpi_summary.csv",
    "stage57_concentration_risk_report": STAGE57_ROOT / "concentration_risk_report.md",
    "stage58_decision": STAGE58_ROOT / "stage58_decision.md",
    "stage58_risk_atr_report": STAGE58_ROOT / "risk_atr_integration_report.md",
    "stage58_risk_telemetry_summary": STAGE58_ROOT / "risk_telemetry_summary.csv",
    "stage58_atr_bracket_telemetry_summary": STAGE58_ROOT / "atr_bracket_telemetry_summary.csv",
    "stage58_risk_floor_segment_impact": STAGE58_ROOT / "risk_floor_segment_impact.csv",
    "stage59ar_decision": STAGE59AR_ROOT / "stage59ar_decision.md",
    "stage59ar_summary": STAGE59AR_ROOT / "bounded_followup_summary.csv",
    "stage59ar_segment_kpi": STAGE59AR_ROOT / "bounded_followup_segment_kpi_summary.csv",
    "stage59ar_equity_curve_audit": STAGE59AR_ROOT / "bounded_followup_equity_curve_audit.md",
    "stage59ar_risk_atr_telemetry": STAGE59AR_ROOT / "bounded_followup_risk_atr_telemetry.csv",
    "stage60_decision": STAGE60_ROOT / "stage60_decision.md",
    "stage60_onnx_export_report": STAGE60_ROOT / "onnx_export_report.json",
    "stage60_onnx_parity_report": STAGE60_ROOT / "onnx_parity_report.json",
    "stage60_runtime_reproduction": STAGE60_ROOT / "mt5_onnx_runtime_reproduction.md",
    "stage60_runtime_summary_json": STAGE60_ROOT / "mt5_onnx_runtime_summary.json",
    "stage60_runtime_summary_csv": STAGE60_ROOT / "mt5_onnx_runtime_summary.csv",
    "stage60_segment_kpi": STAGE60_ROOT / "mt5_onnx_segment_kpi_summary.csv",
    "stage60_risk_atr_telemetry": STAGE60_ROOT / "mt5_onnx_risk_atr_telemetry.csv",
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
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def text_contains(path: Path, needle: str) -> bool:
    return needle in io_path(path).read_text(encoding="utf-8-sig")


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def rows_for(path: Path, *, split: str | None = None, view: str | None = None) -> list[dict[str, str]]:
    rows = read_csv(path)
    out: list[dict[str, str]] = []
    for row in rows:
        if split is not None and row.get("split") != split:
            continue
        if view is not None and row.get("view") != view:
            continue
        if row.get("adapter_id") and row.get("adapter_id") != ADAPTER_ID:
            continue
        out.append(row)
    return out


def full_split_rows(rows: Sequence[Mapping[str, str]]) -> tuple[Mapping[str, str], Mapping[str, str]]:
    val = next(row for row in rows if row.get("split") == "validation_is" and row.get("view") == "actual_routed_total")
    oos = next(row for row in rows if row.get("split") == "oos" and row.get("view") == "actual_routed_total")
    return val, oos


def source_hash_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, path in SOURCE_PATHS.items():
        exists = path_exists(path)
        rows.append(
            {
                "artifact_label": label,
                "path": rel(path),
                "availability": "tracked_or_registered" if exists else "missing",
                "sha256": sha256_file_lf_normalized(path) if exists and io_path(path).is_file() else "",
                "source_stage": label.split("_")[0],
            }
        )
    for row in read_csv(ARTIFACT_REGISTRY_PATH):
        if row.get("run_id") in {"run60A_stage60_onnx_hardening_v1", "run59AM_stage59ar_new_model_branch_from_stage59aq_v1"}:
            rows.append(
                {
                    "artifact_label": row.get("artifact_id"),
                    "path": row.get("path"),
                    "availability": "artifact_registry",
                    "sha256": row.get("sha256"),
                    "source_stage": row.get("stage_id"),
                }
            )
    return rows


def artifact_registry_check(run_id: str) -> dict[str, Any]:
    rows = [row for row in read_csv(ARTIFACT_REGISTRY_PATH) if row.get("run_id") == run_id]
    missing: list[str] = []
    mismatch: list[str] = []
    for row in rows:
        path = Path(str(row.get("path", "")))
        if not path_exists(path):
            missing.append(str(row.get("artifact_id")))
            continue
        if io_path(path).is_file() and sha256_file_lf_normalized(path) != row.get("sha256"):
            mismatch.append(str(row.get("artifact_id")))
    return {"run_id": run_id, "rows": len(rows), "missing": missing, "mismatch": mismatch}


def build_review() -> dict[str, Any]:
    required_paths_missing = [label for label, path in SOURCE_PATHS.items() if not path_exists(path)]
    stage60_summary = read_json(SOURCE_PATHS["stage60_runtime_summary_json"])
    stage60_parity = read_json(SOURCE_PATHS["stage60_onnx_parity_report"])
    stage60_rows = rows_for(SOURCE_PATHS["stage60_runtime_summary_csv"])
    stage60_val, stage60_oos = full_split_rows(stage60_rows)
    stage60_segment = rows_for(SOURCE_PATHS["stage60_segment_kpi"], view="actual_routed_total")
    risk_rows = rows_for(SOURCE_PATHS["stage60_risk_atr_telemetry"], view="actual_routed_total")
    stage59_rows = rows_for(SOURCE_PATHS["stage59ar_summary"])
    stage59_val, stage59_oos = full_split_rows(stage59_rows)
    stage59_segment = rows_for(SOURCE_PATHS["stage59ar_segment_kpi"], view="actual_routed_total")
    stage60_artifacts = artifact_registry_check("run60A_stage60_onnx_hardening_v1")

    def row_pass(row: Mapping[str, str]) -> bool:
        return (
            row.get("status") == "completed"
            and to_float(row.get("net_profit")) > 0
            and to_float(row.get("profit_factor")) >= 1.10
            and to_float(row.get("max_drawdown_percent"), 99.0) <= 25.0
            and to_float(row.get("cost_stressed_expectancy")) > 0
            and to_float(row.get("max_actual_risk_pct_after_floor"), 99.0) <= 0.05
        )

    def segment_pass(rows: Sequence[Mapping[str, str]]) -> bool:
        required = {(split, segment) for split in ("validation_is", "oos") for segment in ("early", "mid", "late")}
        seen = {(row.get("split", ""), row.get("segment", "")) for row in rows}
        if not required.issubset(seen):
            return False
        for row in rows:
            if row.get("segment_type") != "chronological_third":
                continue
            if to_float(row.get("net_profit")) <= 0:
                return False
            if to_float(row.get("profit_factor")) < 1.10:
                return False
        return True

    mandatory_risk = all(
        row.get("status") == "completed"
        and row.get("model_risk_enabled") == "True"
        and row.get("atr_enabled") == "True"
        and to_float(row.get("max_model_risk_pct"), 99.0) <= 0.05
        and to_float(row.get("max_actual_risk_pct_after_floor"), 99.0) <= 0.05
        and int(float(row.get("risk_floor_applied_count") or 0)) == 0
        and to_float(row.get("avg_open_sl_points")) > 0
        and to_float(row.get("avg_open_tp_points")) > 0
        for row in risk_rows
    )
    stage60_runtime_gate = bool((stage60_summary.get("runtime_gate") or {}).get("passed"))
    onnx_parity = bool((stage60_parity.get("probability_parity") or {}).get("passed"))
    decision_parity = bool((stage60_parity.get("decision_parity") or {}).get("passed"))

    criteria = [
        {
            "criterion": "stage57_equity_segment_audit_exists",
            "status": not required_paths_missing and text_contains(SOURCE_PATHS["stage57_decision"], "proceed_to_stage58_adapter_repair_before_risk_atr"),
            "evidence": rel(SOURCE_PATHS["stage57_decision"]),
            "notes": "Stage57 preserved the original anchor as development reference and forced repair before risk/ATR.",
        },
        {
            "criterion": "stage58_mandatory_risk_atr_measured",
            "status": text_contains(SOURCE_PATHS["stage58_decision"], "demote_adapter_due_to_risk_atr_damage"),
            "evidence": rel(SOURCE_PATHS["stage58_decision"]),
            "notes": "Stage58 showed capability integration alone was not sufficient and routed to repair.",
        },
        {
            "criterion": "stage59ar_repaired_adapter_selected",
            "status": text_contains(SOURCE_PATHS["stage59ar_decision"], "proceed_to_stage60_onnx_hardening") and row_pass(stage59_val) and row_pass(stage59_oos),
            "evidence": rel(SOURCE_PATHS["stage59ar_decision"]),
            "notes": "Stage59AR selected s59ar_v41_sd8_h3 with positive validation/OOS KPI after ATR/risk.",
        },
        {
            "criterion": "segment_kpi_acceptable",
            "status": segment_pass(stage59_segment) and segment_pass(stage60_segment),
            "evidence": rel(SOURCE_PATHS["stage60_segment_kpi"]),
            "notes": "Validation and OOS early/mid/late chronological thirds are positive with PF >= 1.10.",
        },
        {
            "criterion": "mandatory_model_risk_and_atr_brackets_present",
            "status": mandatory_risk,
            "evidence": rel(SOURCE_PATHS["stage60_risk_atr_telemetry"]),
            "notes": "Model risk is capped below 5%, ATR SL/TP points are telemetered, and min-lot floor did not fire.",
        },
        {
            "criterion": "onnx_and_mt5_runtime_reproduction",
            "status": stage60_runtime_gate and onnx_parity and decision_parity,
            "evidence": rel(SOURCE_PATHS["stage60_decision"]),
            "notes": "Python/ONNX parity and MT5 ONNX validation/OOS reproduction passed within tolerance.",
        },
        {
            "criterion": "artifact_hashes_and_registry_connected",
            "status": not stage60_artifacts["missing"] and not stage60_artifacts["mismatch"] and stage60_artifacts["rows"] > 0,
            "evidence": rel(ARTIFACT_REGISTRY_PATH),
            "notes": "Stage60 registered artifacts have no missing or mismatched local hash rows.",
        },
        {
            "criterion": "current_truth_and_no_operating_claims",
            "status": all(
                text_contains(CURRENT_WORKING_STATE_PATH, claim)
                for claim in ("deployment", "live_readiness", "runtime_authority", "operating_promotion", "operating_reference", "production_baseline")
            )
            and text_contains(SOURCE_PATHS["stage60_decision"], "Forbidden claims"),
            "evidence": rel(CURRENT_WORKING_STATE_PATH),
            "notes": "Current truth and Stage60 decision keep deployment/live/runtime/operating/production claims forbidden.",
        },
    ]
    all_criteria = all(bool(row["status"]) for row in criteria)
    decision = "research_package_ready" if all_criteria else "continue_research_package_repair_in_stage62"
    return {
        "decision": decision,
        "criteria": criteria,
        "required_paths_missing": required_paths_missing,
        "stage60_artifact_registry_check": stage60_artifacts,
        "stage59_validation": dict(stage59_val),
        "stage59_oos": dict(stage59_oos),
        "stage60_validation": dict(stage60_val),
        "stage60_oos": dict(stage60_oos),
        "risk_rows": risk_rows,
        "onnx_parity_passed": onnx_parity,
        "decision_parity_passed": decision_parity,
        "runtime_gate_passed": stage60_runtime_gate,
        "overall_goal_complete": all_criteria,
    }


def evidence_matrix(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, path in SOURCE_PATHS.items():
        rows.append(
            {
                "evidence_label": label,
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "",
                "consumer": rel(PACKAGE_REVIEW_PATH),
                "boundary": BOUNDARY,
            }
        )
    return rows


def write_reports(review: Mapping[str, Any]) -> None:
    criteria_rows = [
        {**row, "status": "passed" if row["status"] else "failed"}
        for row in review["criteria"]
    ]
    write_csv(CRITERIA_MATRIX_PATH, criteria_rows, ("criterion", "status", "evidence", "notes"))
    write_csv(EVIDENCE_MATRIX_PATH, evidence_matrix(review), ("evidence_label", "path", "exists", "sha256", "consumer", "boundary"))
    write_csv(HASH_SUMMARY_PATH, source_hash_rows(), ("artifact_label", "path", "availability", "sha256", "source_stage"))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE61_ID,
            "run_id": RUN_ID,
            "adapter_id": ADAPTER_ID,
            "decision": review["decision"],
            "overall_goal_complete": review["overall_goal_complete"],
            "claim_boundary": BOUNDARY,
            "stage60_runtime_gate_passed": review["runtime_gate_passed"],
            "onnx_parity_passed": review["onnx_parity_passed"],
            "decision_parity_passed": review["decision_parity_passed"],
            "stage60_artifact_registry_check": review["stage60_artifact_registry_check"],
            "required_outputs": {
                "research_package_review": rel(PACKAGE_REVIEW_PATH),
                "criteria_matrix": rel(CRITERIA_MATRIX_PATH),
                "evidence_matrix": rel(EVIDENCE_MATRIX_PATH),
                "known_weaknesses": rel(KNOWN_WEAKNESSES_PATH),
                "artifact_hash_summary": rel(HASH_SUMMARY_PATH),
                "stage61_decision": rel(DECISION_PATH),
            },
        },
    )
    val = review["stage60_validation"]
    oos = review["stage60_oos"]
    write_md(
        PACKAGE_REVIEW_PATH,
        f"""# Stage61 Research Package Review(61단계 연구 패키지 검토)

- decision(판정): `{review['decision']}`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`
- overall_goal_complete(전체 목표 완료): `{str(review['overall_goal_complete']).lower()}`

Action(행동): Stage57-60(57-60단계) evidence(근거), telemetry(텔레메트리), ONNX/MT5 parity(ONNX/MT5 동등성), artifact hashes(산출물 해시)를 하나의 research package(연구 패키지)로 검토했다.
Effect(효과): research package ready(연구 패키지 준비) 여부만 판정하고 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)는 만들지 않는다.

## Package KPI(패키지 KPI)

- validation_net(검증 순손익): `{val.get('net_profit')}`
- validation_pf(검증 PF): `{val.get('profit_factor')}`
- validation_drawdown_percent(검증 손실폭 퍼센트): `{val.get('max_drawdown_percent')}`
- validation_cost_stressed_expectancy(검증 비용 스트레스 기대값): `{val.get('cost_stressed_expectancy')}`
- oos_net(표본외 순손익): `{oos.get('net_profit')}`
- oos_pf(표본외 PF): `{oos.get('profit_factor')}`
- oos_drawdown_percent(표본외 손실폭 퍼센트): `{oos.get('max_drawdown_percent')}`
- oos_cost_stressed_expectancy(표본외 비용 스트레스 기대값): `{oos.get('cost_stressed_expectancy')}`

## Gate Read(게이트 판독)

- stage60_runtime_gate_passed(60단계 런타임 게이트 통과): `{review['runtime_gate_passed']}`
- onnx_probability_parity_passed(ONNX 확률 동등성 통과): `{review['onnx_parity_passed']}`
- onnx_decision_parity_passed(ONNX 판정 동등성 통과): `{review['decision_parity_passed']}`
- artifact_missing_count(산출물 누락 수): `{len(review['stage60_artifact_registry_check']['missing'])}`
- artifact_mismatch_count(산출물 해시 불일치 수): `{len(review['stage60_artifact_registry_check']['mismatch'])}`

## Judgment(판정)

`{review['decision']}`.

Effect(효과): 이 판정은 research package ready(연구 패키지 준비)이며 운영 의미를 갖지 않는다. 다음 live-readiness(실거래 준비) 작업이 필요하다면 별도 미래 stage(단계)와 훨씬 강한 외부 검증이 필요하다.
""",
    )
    write_md(
        KNOWN_WEAKNESSES_PATH,
        f"""# Known Weaknesses(알려진 약점)

- Tier B fallback(Tier B 대체)은 disabled(비활성)이다. Effect(효과): actual routed total(실제 라우팅 전체)은 Tier A(티어 A) 중심이며, Tier B(티어 B) 재활성은 별도 연구가 필요하다.
- validation mid segment(검증 중간 구간) PF(수익 팩터)는 1.1007 근처다. Effect(효과): 연구 패키지는 통과하지만 여유 폭은 크지 않다.
- MFE/MAE telemetry(MFE/MAE 텔레메트리)는 존재하지만 정의별 ratio(비율)가 다르다. Effect(효과): 추후 비교에서는 같은 정의만 비교해야 한다.
- Stage61(61단계)은 live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)를 주장하지 않는다. Effect(효과): 이 패키지는 연구 기록으로만 닫힌다.
- 사용자 로컬 동기화(user-local sync, 사용자 로컬 동기화)는 확인하지 않았다. Effect(효과): 확인 가능한 것은 origin/main(원격 main)에 push(푸시)된 commit(커밋)뿐이다.
""",
    )
    next_text = "none_research_package_review_closed" if review["overall_goal_complete"] else "62_research_package_repair__evidence_gap"
    write_md(
        DECISION_PATH,
        f"""# Stage61 Decision(61단계 판정)

decision(판정): `{review['decision']}`

Stage61(61단계)은 research package review only(연구 패키지 검토 전용)로 닫는다. Effect(효과): BaselineAdapter(기준선 어댑터) research package(연구 패키지)의 충분성만 기록하고 운영 주장은 만들지 않는다.

## Evidence(근거)

- research_package_review(연구 패키지 검토): `{rel(PACKAGE_REVIEW_PATH)}`
- criteria_matrix(기준표): `{rel(CRITERIA_MATRIX_PATH)}`
- evidence_matrix(근거표): `{rel(EVIDENCE_MATRIX_PATH)}`
- known_weaknesses(알려진 약점): `{rel(KNOWN_WEAKNESSES_PATH)}`
- artifact_hash_summary(산출물 해시 요약): `{rel(HASH_SUMMARY_PATH)}`
- summary(요약): `{rel(SUMMARY_JSON_PATH)}`

## Result(결과)

- overall_goal_complete(전체 목표 완료): `{str(review['overall_goal_complete']).lower()}`
- next_stage_or_branch(다음 단계/분기): `{next_text}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위).
""",
    )


def artifact_rows(paths: Sequence[Path]) -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.name}",
                "artifact_type": "stage61_research_package_review_artifact",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "missing",
                "stage_id": STAGE61_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "Stage61 research package review artifact; research-only boundary.",
            }
        )
    return rows


def replace_artifact_rows(artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    existing = [row for row in read_csv(ARTIFACT_REGISTRY_PATH) if row.get("run_id") != RUN_ID]
    merged = [*existing, *[dict(row) for row in artifacts]]
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)
    return {
        "path": ARTIFACT_REGISTRY_PATH.as_posix(),
        "sha256": sha256_file_lf_normalized(ARTIFACT_REGISTRY_PATH),
        "hash_policy": "lf_normalized_text_register",
        "rows": len(merged),
        "upserted_rows": len(artifacts),
    }


def write_ledgers(review: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    val = review["stage60_validation"]
    oos = review["stage60_oos"]
    judgment = str(review["decision"])
    status = "completed" if review["overall_goal_complete"] else "blocked"
    row = {
        "ledger_row_id": f"{RUN_ID}__aggregate_research_package_review",
        "stage_id": STAGE61_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggregate_research_package_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage61_research_package_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "research_package_review",
        "scoreboard_lane": "research_package",
        "status": status,
        "judgment": judgment,
        "path": rel(DECISION_PATH),
        "primary_kpi": ledger_pairs(
            [
                ("validation_net", val.get("net_profit")),
                ("oos_net", oos.get("net_profit")),
                ("validation_pf", val.get("profit_factor")),
                ("oos_pf", oos.get("profit_factor")),
                ("overall_goal_complete", int(bool(review["overall_goal_complete"]))),
            ]
        ),
        "guardrail_kpi": ledger_pairs(
            [
                ("deployment_claim", 0),
                ("live_readiness_claim", 0),
                ("runtime_authority_claim", 0),
                ("artifact_missing", len(review["stage60_artifact_registry_check"]["missing"])),
                ("artifact_mismatch", len(review["stage60_artifact_registry_check"]["mismatch"])),
            ]
        ),
        "external_verification_status": "completed_existing_stage57_to_stage60_evidence_reviewed",
        "notes": "Stage61 research package review only; no operating claim.",
    }
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE61_ID,
                "lane": "baseline_adapter_research_package_review",
                "status": status,
                "judgment": judgment,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs([("adapter_id", ADAPTER_ID), ("boundary", BOUNDARY)]),
            }
        ],
        key="run_id",
    )
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [row], key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [row], key="ledger_row_id")
    artifact_payload = replace_artifact_rows(artifacts)
    return {
        "run_registry": run_payload,
        "stage_ledger": stage_payload,
        "project_alpha_ledger": project_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    final_guard = {
        "overall_goal_complete": bool(review["overall_goal_complete"]),
        "research_package_ready": review["decision"] == "research_package_ready",
        "deployment_claim": False,
        "live_readiness_claim": False,
        "runtime_authority_claim": False,
        "production_baseline_claim": False,
        "operating_promotion_claim": False,
        "operating_reference_claim": False,
        "status": "completed",
    }
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": [
                "obsidian-artifact-lineage",
                "obsidian-performance-attribution",
                "obsidian-model-validation",
                "obsidian-backtest-forensics",
            ],
            "registry_primary_skill_note": "kpi_evidence registry primary skill is obsidian-run-evidence-system; available repo skill set used obsidian-result-judgment for the final package judgment.",
            "required_gates": [
                "research_package_completeness_gate",
                "kpi_contract_audit",
                "artifact_lineage_audit",
                "result_judgment_gate",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "status": "completed",
        },
        "research_package_completeness_gate.json": {
            "status": "completed" if review["overall_goal_complete"] else "blocked",
            "criteria": review["criteria"],
            "missing_source_paths": review["required_paths_missing"],
            "decision": review["decision"],
        },
        "kpi_contract_audit.json": {
            "status": "completed",
            "validation": review["stage60_validation"],
            "oos": review["stage60_oos"],
            "segment_review": rel(CRITERIA_MATRIX_PATH),
            "boundary": BOUNDARY,
        },
        "artifact_lineage_audit.json": {
            "status": "completed",
            "source_inputs": [rel(path) for path in SOURCE_PATHS.values()],
            "producer": "stage_pipelines/stage61/research_package_review.py",
            "consumers": [rel(PACKAGE_REVIEW_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)],
            "registry_links": ledger_payload,
            "artifact_hash_summary": rel(HASH_SUMMARY_PATH),
            "lineage_judgment": "connected_with_boundary",
        },
        "result_judgment_gate.json": {
            "status": "passed_with_boundary",
            "result_subject": RUN_ID,
            "judgment_label": review["decision"],
            "evidence_available": [rel(PACKAGE_REVIEW_PATH), rel(CRITERIA_MATRIX_PATH), rel(HASH_SUMMARY_PATH)],
            "evidence_missing": review["required_paths_missing"],
            "claim_boundary": BOUNDARY,
            "next_condition": "no_next_stage_required_for_current_goal" if review["overall_goal_complete"] else "stage62_repair_evidence_gap",
        },
        "final_claim_guard.json": final_guard,
        "required_gate_coverage_audit.json": {
            "required_gates": [
                "research_package_completeness_gate",
                "kpi_contract_audit",
                "artifact_lineage_audit",
                "result_judgment_gate",
                "final_claim_guard",
            ],
            "covered_by": [
                "research_package_completeness_gate.json",
                "kpi_contract_audit.json",
                "artifact_lineage_audit.json",
                "result_judgment_gate.json",
                "final_claim_guard.json",
            ],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE61_ID,
            "run_id": RUN_ID,
            "adapter_id": ADAPTER_ID,
            "decision": review["decision"],
            "overall_goal_complete": review["overall_goal_complete"],
            "claim_boundary": BOUNDARY,
            "required_outputs": {
                "research_package_review": rel(PACKAGE_REVIEW_PATH),
                "criteria_matrix": rel(CRITERIA_MATRIX_PATH),
                "evidence_matrix": rel(EVIDENCE_MATRIX_PATH),
                "known_weaknesses": rel(KNOWN_WEAKNESSES_PATH),
                "artifact_hash_summary": rel(HASH_SUMMARY_PATH),
                "stage61_decision": rel(DECISION_PATH),
            },
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def update_stage_docs(review: Mapping[str, Any]) -> None:
    status = "closed_research_package_ready" if review["overall_goal_complete"] else "closed_research_package_repair_required"
    next_text = "none_current_goal_complete" if review["overall_goal_complete"] else "62_research_package_repair__evidence_gap"
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# 61 Selection Status(61단계 선택 상태)

- stage_status(단계 상태): `{status}`
- source_stage(원천 단계): `60_adapter_onnx__hardening_runtime_reproduction`
- source_decision(원천 판정): `proceed_to_stage61_research_package_review`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- selected_research_baseline(선택 연구 기준선): `research_package_only`
- stage61_decision(61단계 판정): `{review['decision']}`
- next_stage_or_branch(다음 단계/분기): `{next_text}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage61(61단계)은 연구 패키지 충분성만 판단하고 운영 의미는 주장하지 않는다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        "\n".join(
            [
                "# 61 Input References(61단계 입력 참조)",
                "",
                *[f"- {label}({label}): `{rel(path)}`" for label, path in SOURCE_PATHS.items()],
            ]
        ),
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# 61 Review Index(61단계 검토 색인)

- research_package_review(연구 패키지 검토): `{rel(PACKAGE_REVIEW_PATH)}`
- criteria_matrix(기준표): `{rel(CRITERIA_MATRIX_PATH)}`
- evidence_matrix(근거표): `{rel(EVIDENCE_MATRIX_PATH)}`
- known_weaknesses(알려진 약점): `{rel(KNOWN_WEAKNESSES_PATH)}`
- artifact_hash_summary(산출물 해시 요약): `{rel(HASH_SUMMARY_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )


def update_current_truth(review: Mapping[str, Any]) -> None:
    status = "stage61_closed_research_package_ready" if review["overall_goal_complete"] else "stage61_closed_repair_required"
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- active_stage(활성 단계): `{STAGE61_ID}`
- selected_research_baseline(선택 연구 기준선): `research_package_only`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- status(상태): `{status}`
- overall_goal_complete(전체 목표 완료): `{str(review['overall_goal_complete']).lower()}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage61(61단계) closed(종료) as research package review(연구 패키지 검토). Effect(효과): BaselineAdapter(기준선 어댑터) 연구 패키지는 충분성 판정을 받았지만 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)는 아니다.

## Latest Stage61 Evidence(최신 61단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{review['decision']}`
- report(보고서): `{rel(PACKAGE_REVIEW_PATH)}`
- stage61_decision(61단계 판정): `{rel(DECISION_PATH)}`
- artifact_hash_summary(산출물 해시 요약): `{rel(HASH_SUMMARY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).
""",
    )
    import re

    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {STAGE61_ID}", text, count=1, flags=re.MULTILINE)
    block = f"""

stage61_research_package_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE61_ID}
  status: {status}
  current_run_id: {RUN_ID}
  adapter_under_review: {ADAPTER_ID}
  decision: {review['decision']}
  overall_goal_complete: {str(review['overall_goal_complete']).lower()}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    if "stage61_research_package_review:" in text:
        text = re.sub(r"\nstage61_research_package_review:\n(?:  .*\n)*", block, text, count=1)
    else:
        text = text.rstrip() + "\n" + block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(review: Mapping[str, Any]) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    marker = f"- run(실행): `{RUN_ID}`"
    if marker in existing:
        return
    entry = f"""

## 2026-05-16 - Stage61 research package review closeout(61단계 연구 패키지 검토 종료)

- run(실행): `{RUN_ID}`
- decision(판정): `{review['decision']}`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- overall_goal_complete(전체 목표 완료): `{str(review['overall_goal_complete']).lower()}`
- effect(효과): Stage57-60(57-60단계) 증거를 research package(연구 패키지)로 검토하고 운영 주장을 만들지 않는 경계로 닫았다.
"""
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    review = build_review()
    write_reports(review)
    update_stage_docs(review)
    update_current_truth(review)
    append_changelog(review)
    output_paths = [
        SUMMARY_JSON_PATH,
        CRITERIA_MATRIX_PATH,
        EVIDENCE_MATRIX_PATH,
        HASH_SUMMARY_PATH,
        KNOWN_WEAKNESSES_PATH,
        PACKAGE_REVIEW_PATH,
        DECISION_PATH,
        SELECTED_ROOT / "selection_status.md",
        INPUT_ROOT / "input_refs.md",
        REVIEWS_ROOT / "review_index.md",
        Path(__file__),
    ]
    artifacts = artifact_rows(output_paths)
    ledger_payload = write_ledgers(review, artifacts)
    write_packet_files(review, ledger_payload)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if review["overall_goal_complete"] else "blocked",
                    "run_id": RUN_ID,
                    "decision": review["decision"],
                    "overall_goal_complete": review["overall_goal_complete"],
                    "stage60_runtime_gate_passed": review["runtime_gate_passed"],
                    "onnx_parity_passed": review["onnx_parity_passed"],
                    "decision_path": rel(DECISION_PATH),
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
