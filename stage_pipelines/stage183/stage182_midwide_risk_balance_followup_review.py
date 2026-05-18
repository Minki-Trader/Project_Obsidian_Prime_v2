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

STAGE_ID = "183_adapter_research__stage182_midwide_risk_balance_followup_review"
RUN_ID = "run183A_stage183_stage182_midwide_risk_balance_followup_review_v1"
PACKET_ID = "stage183_stage182_midwide_risk_balance_followup_review_v1"
PARENT_RUN_ID = "run182A_stage182_tp45_midwide_risk_balance_repair_v1"
SOURCE_STAGE_ID = "182_adapter_research__tp45_midwide_risk_balance_repair"
SOURCE_RUN_ID = "run182A_stage182_tp45_midwide_risk_balance_repair_v1"
SOURCE_STAGE182_CLOSEOUT_COMMIT = "3a916347df9690287249d9573a434e80702ce08b"
SOURCE_STAGE182_HASH_RECORD_COMMIT = "5582720b0413547be769b56e0ef007830056d6df"
NEXT_STAGE_ID = "184_adapter_research__tp45_midwide_midsegment_quality_repair"
NEXT_RUN_ID = "run184A_stage184_tp45_midwide_midsegment_quality_repair_v1"
NEXT_PACKET_ID = "stage184_tp45_midwide_midsegment_quality_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage182_mt5_reports_completed"
DECISION = "open_stage184_tp45_midwide_midsegment_quality_repair_candidate_not_final"

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

SOURCE_REPORT = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_tp45_midwide_risk_balance_report.md")
SOURCE_QUALITY = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_quality_matrix.csv")
SOURCE_SEGMENT = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_segment_kpi_summary.csv")
SOURCE_BALANCE = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_balance_curve_audit.csv")
SOURCE_MONTHLY = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_monthly_kpi_summary.csv")
SOURCE_CONCENTRATION = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_concentration_risk_summary.csv")
SOURCE_RISK_ATR = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_risk_atr_telemetry.csv")
SOURCE_TRADE_AUDIT = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_trade_audit.csv")
SOURCE_DECISION = Path("stages/182_adapter_research__tp45_midwide_risk_balance_repair/03_reviews/stage182_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage183_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage183_risk_balance_tradeoff_matrix.csv"
WEAKNESS_MATRIX_PATH = REVIEWS_ROOT / "stage183_midsegment_weakness_matrix.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage183_repair_route_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage183_performance_attribution.csv"
DECISION_PATH = REVIEWS_ROOT / "stage183_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage183/stage182_midwide_risk_balance_followup_review.py")
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


def as_int(row: Mapping[str, Any], key: str, default: int = 0) -> int:
    try:
        value = row.get(key, default)
        if value in (None, ""):
            return default
        return int(float(str(value).replace(",", "")))
    except (TypeError, ValueError):
        return default


def risk_label(adapter_id: str) -> str:
    if "risk0365" in adapter_id:
        return "0.0365"
    if "risk0340" in adapter_id:
        return "0.0340"
    if "risk0325" in adapter_id:
        return "0.0325"
    if "risk0315" in adapter_id:
        return "0.0315"
    return "unknown"


def segment_lookup(segment_rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str, str], Mapping[str, str]]:
    lookup: dict[tuple[str, str, str], Mapping[str, str]] = {}
    for row in segment_rows:
        if row.get("split") != "validation_is" or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") not in {"full_split", "chronological_third"}:
            continue
        lookup[(str(row.get("adapter_id", "")), str(row.get("segment_type", "")), str(row.get("segment", "")))] = row
    return lookup


def weak_months_by_adapter(monthly_rows: Sequence[Mapping[str, str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for row in monthly_rows:
        if row.get("split") != "validation_is":
            continue
        if "pf_below_34d" not in str(row.get("quality_flag", "")):
            continue
        result.setdefault(str(row.get("adapter_id", "")), []).append(str(row.get("month", "")))
    return result


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, str]],
    segment_rows: Sequence[Mapping[str, str]],
    balance_rows: Sequence[Mapping[str, str]],
    monthly_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    segments = segment_lookup(segment_rows)
    weak_months = weak_months_by_adapter(monthly_rows)
    balance_by_adapter = {
        str(row.get("adapter_id", "")): row
        for row in balance_rows
        if row.get("split") == "validation_is"
    }
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        mid = segments.get((adapter_id, "chronological_third", "mid"), {})
        early = segments.get((adapter_id, "chronological_third", "early"), {})
        late = segments.get((adapter_id, "chronological_third", "late"), {})
        balance = balance_by_adapter.get(adapter_id, {})
        val_net = as_float(row, "validation_net")
        val_dd = as_float(row, "validation_balance_dd_percent")
        mid_pf = as_float(row, "validation_mid_pf")
        conclusion = "risk_only_incomplete"
        if val_dd <= LEGACY_34D["max_drawdown_percent"] and val_net < LEGACY_34D["net_profit"]:
            conclusion = "dd_fixed_but_net_below_34d"
        elif val_dd > LEGACY_34D["max_drawdown_percent"] and val_net >= LEGACY_34D["net_profit"]:
            conclusion = "net_preserved_but_dd_failed"
        if mid_pf < LEGACY_34D["profit_factor"]:
            conclusion += "_and_mid_pf_failed"
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "risk_cap": risk_label(adapter_id),
                "validation_pf": as_float(row, "validation_pf"),
                "validation_net": val_net,
                "validation_net_gap_vs_34d": val_net - LEGACY_34D["net_profit"],
                "validation_balance_dd_percent": val_dd,
                "validation_dd_margin_vs_34d": LEGACY_34D["max_drawdown_percent"] - val_dd,
                "validation_mid_pf": mid_pf,
                "validation_mid_pf_gap_vs_34d": mid_pf - LEGACY_34D["profit_factor"],
                "validation_mid_net": as_float(mid, "net_profit"),
                "validation_mid_trade_count": as_int(mid, "trade_count"),
                "validation_mid_drawdown": as_float(mid, "max_closed_trade_drawdown"),
                "validation_mid_mfe_capture": as_float(mid, "mfe_capture_ratio"),
                "validation_early_pf": as_float(early, "profit_factor"),
                "validation_late_pf": as_float(late, "profit_factor"),
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": as_float(row, "oos_net"),
                "oos_balance_dd_percent": as_float(row, "oos_balance_dd_percent"),
                "late_net_share": as_float(balance, "late_net_share"),
                "weak_validation_months": ";".join(weak_months.get(adapter_id, [])),
                "quality_flags": str(row.get("quality_flags", "")),
                "conclusion": conclusion,
            }
        )
    return rows


def best_near_miss(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            as_float(row, "validation_net") >= LEGACY_34D["net_profit"],
            -abs(as_float(row, "validation_balance_dd_percent") - LEGACY_34D["max_drawdown_percent"]),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_pf"),
        ),
    )


def build_weakness_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in tradeoff_rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "risk_cap": row.get("risk_cap", ""),
                "primary_weakness": "validation_mid_pf_below_34d",
                "evidence": (
                    f"mid_pf={as_float(row, 'validation_mid_pf'):.6f}; "
                    f"mid_drawdown={as_float(row, 'validation_mid_drawdown'):.2f}; "
                    f"mid_mfe_capture={as_float(row, 'validation_mid_mfe_capture'):.6f}; "
                    f"weak_months={row.get('weak_validation_months', '')}"
                ),
                "effect": "risk_cap_change_lowered_dd_but_did_not_repair_mid_window_quality",
                "next_repair_need": "target_midwindow_trade_quality_not_calendar_copy",
            }
        )
    return rows


def build_route_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_near_miss(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "route": "stage184_primary",
            "decision": DECISION,
            "source_clue": best.get("adapter_id", ""),
            "bounded_question": (
                "Can TP45 midwide context(익절 4.5 중간넓은 문맥) repair the validation mid-window "
                "PF(검증 중반 수익요인) and DD(낙폭) with a targeted quality gate(품질 제한문), "
                "while preserving net(순손익), OOS(표본외), ATR bracket(ATR 브래킷), and model risk(모델 위험)?"
            ),
            "why": (
                "risk cap(위험 상한) alone almost reaches DD(낙폭), but mid PF(중반 수익요인) "
                "stays below 34D(레거시 34D) and the lowest cap(최저 상한) drops net(순손익)."
            ),
            "guardrail": "do_not_calendar_hardcode_weak_months_use_diagnostics_only",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory",
            "decision": DECISION,
            "source_clue": "risk_only_axis",
            "bounded_question": "Do not continue pure risk cap(위험 상한) lowering as the only repair.",
            "why": "It trades net(순손익) for DD(낙폭) and leaves mid PF(중반 수익요인) weak.",
            "guardrail": "preserve_as_failure_memory_not_invalid_strategy_death",
        },
    ]


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    near = best_near_miss(tradeoff_rows)
    dd_fixed = next((row for row in tradeoff_rows if as_float(row, "validation_balance_dd_percent") <= LEGACY_34D["max_drawdown_percent"]), {})
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "risk_cap_downshift(위험 상한 하향)은 DD(낙폭)를 거의 선형으로 낮췄다.",
            "comparison_baseline": "stage182_midwide_risk0365_control",
            "likely_drivers": "same_trade_set_scaled_by_model_risk(같은 거래 집합의 모델 위험 축소)",
            "segment_checks": (
                f"near_miss={near.get('adapter_id', '')}; "
                f"near_miss_val_net={as_float(near, 'validation_net'):.2f}; "
                f"near_miss_val_dd={as_float(near, 'validation_balance_dd_percent'):.4f}; "
                f"near_miss_mid_pf={as_float(near, 'validation_mid_pf'):.6f}"
            ),
            "trade_shape": "mid_window(중반 구간)의 PF(수익요인)와 MFE capture(최대유리이동 포착률)가 핵심 약점이다.",
            "alternative_explanations": "calendar weak months(달력 약한 달)는 진단 단서일 뿐이며 hardcode(고정 규칙)로 쓰면 과적합 위험이 있다.",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Stage184(184단계) midwindow quality gate(중반 품질 제한문)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "risk0315(위험 0.0315)는 DD(낙폭)를 12.8880까지 낮췄지만 net(순손익)이 968.71로 34D(레거시 34D) 아래였다.",
            "comparison_baseline": "legacy_34d_kpi_target_lesson_only",
            "likely_drivers": "risk_budget_too_low_for_existing_trade_quality(현재 거래 품질 대비 위험 예산 부족)",
            "segment_checks": f"dd_fixed_candidate={dd_fixed.get('adapter_id', 'none')}",
            "trade_shape": "risk-only(위험만 조정)로는 34D 이상 KPI(핵심 성과 지표)를 동시에 만족하지 못한다.",
            "alternative_explanations": "one narrow cap(하나의 좁은 상한)만 문제가 아니라 mid PF(중반 수익요인)가 모든 cap(상한)에서 약하다.",
            "attribution_confidence": "high(높음)",
            "next_probe": "quality_first_then_risk_balance(품질 우선 후 위험 균형)",
        },
    ]


def table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | risk cap(위험 상한) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | mid MFE cap(중반 최대유리이동 포착) | OOS DD%(표본외 낙폭) | conclusion(결론) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {risk_cap} | {validation_pf:.6f} | {validation_net:.2f} | {validation_balance_dd_percent:.4f} | {validation_mid_pf:.6f} | {validation_mid_mfe_capture:.6f} | {oos_balance_dd_percent:.4f} | {conclusion} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]]) -> str:
    best = best_near_miss(tradeoff_rows)
    return f"""# Stage183 Stage182 Midwide Risk Balance Follow-up Review(183단계 182단계 중간넓은 문맥 위험 균형 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage182_closeout_commit(원천 182단계 종료 커밋): `{SOURCE_STAGE182_CLOSEOUT_COMMIT}`
- source_stage182_hash_record_commit(원천 182단계 해시 기록 커밋): `{SOURCE_STAGE182_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

{table(tradeoff_rows)}

## Simple Read(쉬운 판독)

Stage182(182단계)는 방향은 맞지만 아직 34D(레거시 34D) 이상이 아니다. Effect(효과): risk cap(위험 상한)을 낮추면 validation DD(검증 낙폭)는 줄지만, validation mid PF(검증 중반 수익요인)는 모든 variant(변형)에서 34D(레거시 34D) 아래이고, DD(낙폭)를 통과한 risk0315(위험 0.0315)는 validation net(검증 순손익)이 34D(레거시 34D) 아래로 내려간다.

## Best Near Miss(가장 가까운 미달 후보)

- adapter(어댑터): `{best.get("adapter_id", "none")}`
- validation_net(검증 순손익): `{as_float(best, "validation_net"):.2f}`
- validation_dd(검증 낙폭): `{as_float(best, "validation_balance_dd_percent"):.4f}`
- validation_mid_pf(검증 중반 수익요인): `{as_float(best, "validation_mid_pf"):.6f}`
- weak_months(약한 달): `{best.get("weak_validation_months", "")}`

## Attribution(귀인)

- observed_change(관찰 변화): `{attribution_rows[0].get("observed_change", "")}`
- likely_drivers(가능 원인): `{attribution_rows[0].get("likely_drivers", "")}`
- trade_shape(거래 모양): `{attribution_rows[0].get("trade_shape", "")}`
- effect(효과): Stage184(184단계)는 calendar hardcode(달력 고정 규칙)가 아니라 midwindow quality gate(중반 품질 제한문)와 trade-quality diagnostics(거래 품질 진단)로 좁게 진행한다.

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- decision(판정): `{DECISION}`
- reason(이유): risk-only repair(위험만 조정하는 수정)는 net/DD/PF(순손익/낙폭/수익요인)를 동시에 만족하지 못했다.

Stage183(183단계)는 research/development only(연구개발 전용)이다. Effect(효과): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
"""


def decision_markdown() -> str:
    return f"""# Stage183 Decision(183단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage182_closeout_commit(원천 182단계 종료 커밋): `{SOURCE_STAGE182_CLOSEOUT_COMMIT}`
- source_stage182_hash_record_commit(원천 182단계 해시 기록 커밋): `{SOURCE_STAGE182_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- weakness_matrix(약점 행렬): `{rel(WEAKNESS_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage183(183단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage184(184단계)에서 TP45(익절 4.5) midwide context(중간넓은 문맥)의 midsegment quality repair(중반 구간 품질 수정)를 좁게 측정한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    for path in (PRODUCER_PATH, REPORT_PATH, DECISION_PATH, TRADEOFF_MATRIX_PATH, WEAKNESS_MATRIX_PATH, ROUTE_MATRIX_PATH, ATTRIBUTION_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage183_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage183 Stage182 midwide risk-balance follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = best_near_miss(tradeoff_rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage183_stage182_midwide_risk_balance_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage182_closeout_commit", SOURCE_STAGE182_CLOSEOUT_COMMIT),
                        ("source_stage182_hash_record_commit", SOURCE_STAGE182_HASH_RECORD_COMMIT),
                        ("primary_near_miss", best.get("adapter_id", "none")),
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
            "ledger_row_id": f"{RUN_ID}__stage182_midwide_risk_balance_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage182_midwide_risk_balance_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage182_midwide_risk_balance_followup_review",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("near_miss", best.get("adapter_id", "none")),
                    ("validation_pf", f"{as_float(best, 'validation_pf'):.6f}"),
                    ("validation_net", f"{as_float(best, 'validation_net'):.2f}"),
                    ("validation_dd", f"{as_float(best, 'validation_balance_dd_percent'):.4f}"),
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
            "notes": "Stage183 reviewed Stage182 risk-balance tradeoff and opened Stage184 midsegment quality repair.",
        }
    ]
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
    }


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], weakness_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
        "weakness_matrix": rel(WEAKNESS_MATRIX_PATH),
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "attribution": rel(ATTRIBUTION_PATH),
        "tradeoff_rows": list(tradeoff_rows),
        "weakness_rows": list(weakness_rows),
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
        f"""# Stage183 Closeout Packet(183단계 종료 작업 묶음)

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

Stage184(184단계)는 Stage182(182단계)와 Stage183(183단계)의 결론을 받아 TP45(익절 4.5) midwide context(중간넓은 문맥) 표면의 midsegment quality(중반 구간 품질)를 좁게 고친다.

## Bounded Question(경계 질문)

Can a targeted midwindow quality gate(중반 품질 제한문) or trade-quality repair(거래 품질 수정) improve validation mid PF(검증 중반 수익요인) and validation DD(검증 낙폭) without dropping validation net/PF(검증 순손익/수익요인), OOS DD(표본외 낙폭), ATR bracket(ATR 브래킷), or model-controlled risk(모델 제어 위험)?

Effect(효과): calendar hardcode(달력 고정 규칙)나 legacy copy(레거시 복사)가 아니라, Stage182(182단계)에서 드러난 중반 구간 약점만 v2-native research(v2 고유 연구)로 좁게 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage184 Inputs(184단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- weakness_matrix(약점 행렬): `{rel(WEAKNESS_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- source_stage182_quality(원천 182단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage182_segment(원천 182단계 구간): `{rel(SOURCE_SEGMENT)}`
- source_stage182_risk_atr(원천 182단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- source_stage182_trade_audit(원천 182단계 거래 감사): `{rel(SOURCE_TRADE_AUDIT)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage184 Review Index(184단계 검토 색인)

- status(상태): `open_planned_from_stage183`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage184 Selection Status(184단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage183`
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
  Stage183(183단계) closed(종료) as `{DECISION}` and Stage184(184단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): risk-only repair(위험만 조정하는 수정)를 멈추고 midsegment quality repair(중반 구간 품질 수정)로 좁힌다.
- >-
  Stage183 evidence(183단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(WEAKNESS_MATRIX_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): net(순손익), PF(수익요인), DD(낙폭), mid PF(중반 수익요인)의 상충을 장부화했다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage183_stage182_midwide_risk_balance_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage183_stage182_midwide_risk_balance_followup_review:
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
  weakness_matrix_path: {rel(WEAKNESS_MATRIX_PATH)}
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
- adapter_under_review(검토 중 어댑터): `stage182_tp45_midwide_risk_balance_surface`
- status(상태): `stage183_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage183(183단계)는 Stage182(182단계)의 risk balance(위험 균형) 결과를 follow-up review(후속 검토)로 판독했다. Effect(효과): risk cap(위험 상한)만 낮추는 길은 중단하고, Stage184(184단계)에서 midsegment quality(중반 구간 품질)를 좁게 고친다.

## Latest Stage183 Evidence(최신 183단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- weakness_matrix(약점 행렬): `{rel(WEAKNESS_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage183 Selection Status(183단계 선택 상태)

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
        f"""# Stage183 Review Index(183단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- weakness_matrix(약점 행렬): `{rel(WEAKNESS_MATRIX_PATH)}`
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
        f"\n## {utc_now()} Stage183 Stage182 midwide risk balance follow-up review closeout(183단계 182단계 중간넓은 문맥 위험 균형 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): risk-only repair(위험만 조정하는 수정)는 34D(레거시 34D) 이상을 동시에 만족하지 못해 Stage184(184단계) midsegment quality repair(중반 구간 품질 수정)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = load_csv(SOURCE_QUALITY)
    segment_rows = load_csv(SOURCE_SEGMENT)
    balance_rows = load_csv(SOURCE_BALANCE)
    monthly_rows = load_csv(SOURCE_MONTHLY)
    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, balance_rows, monthly_rows)
    weakness_rows = build_weakness_rows(tradeoff_rows)
    route_rows = build_route_rows(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(WEAKNESS_MATRIX_PATH, weakness_rows)
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
    write_packet_files(tradeoff_rows, weakness_rows, route_rows, attribution_rows, ledger_payload)
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
                    "weakness_matrix": rel(WEAKNESS_MATRIX_PATH),
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
