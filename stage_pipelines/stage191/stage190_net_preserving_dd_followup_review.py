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

STAGE_ID = "191_adapter_research__stage190_net_preserving_dd_followup_review"
RUN_ID = "run191A_stage191_stage190_net_preserving_dd_followup_review_v1"
PACKET_ID = "stage191_stage190_net_preserving_dd_followup_review_v1"
PARENT_RUN_ID = "run190A_stage190_net_preserving_dd_repair_from_long_strict_clue_v1"
SOURCE_STAGE_ID = "190_adapter_research__net_preserving_dd_repair_from_long_strict_clue"
SOURCE_RUN_ID = "run190A_stage190_net_preserving_dd_repair_from_long_strict_clue_v1"
SOURCE_STAGE190_CLOSEOUT_COMMIT = "772d6605c69c7fd6ecd717a8b0043207dfc85f9e"
SOURCE_STAGE190_HASH_RECORD_COMMIT = "de91ea6a94c162eb5f0553deb567cb9702e37a5b"

NEXT_STAGE_ID = "192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression"
NEXT_RUN_ID = "run192A_stage192_tp475_midsegment_net_recovery_without_dd_regression_v1"
NEXT_PACKET_ID = "stage192_tp475_midsegment_net_recovery_without_dd_regression_v1"
DECISION = "open_stage192_tp475_midsegment_net_recovery_without_dd_regression_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_tp475_midsegment_net_recovery"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage190_mt5_reports_completed"

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

SOURCE_REPORT = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/"
    "stage190_net_preserving_dd_report.md"
)
SOURCE_QUALITY = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/"
    "stage190_quality_matrix.csv"
)
SOURCE_SEGMENT = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/"
    "stage190_segment_kpi_summary.csv"
)
SOURCE_SUMMARY = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/"
    "stage190_net_preserving_dd_summary.csv"
)
SOURCE_BALANCE = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/"
    "stage190_balance_curve_audit.csv"
)
SOURCE_CONCENTRATION = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/"
    "stage190_concentration_risk_summary.csv"
)
SOURCE_RISK_ATR = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/"
    "stage190_risk_atr_telemetry.csv"
)
SOURCE_DECISION = Path(
    "stages/190_adapter_research__net_preserving_dd_repair_from_long_strict_clue/03_reviews/stage190_decision.md"
)

REPORT_PATH = REVIEWS_ROOT / "stage191_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage191_net_dd_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage191_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage191_route_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage191_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage191/stage190_net_preserving_dd_followup_review.py")
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
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def pass_bool(value: float, target: float, direction: str = "above") -> bool:
    return value >= target if direction == "above" else value <= target


def lookup_by_adapter(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("adapter_id", "")): row for row in rows}


def lookup_by_adapter_split(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {(str(row.get("adapter_id", "")), str(row.get("split", ""))): row for row in rows}


def validation_segments(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    result: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in rows:
        if row.get("split") == "validation_is" and row.get("view") == "actual_routed_total":
            if row.get("segment_type") == "chronological_third":
                result[(str(row.get("adapter_id", "")), str(row.get("segment", "")))] = row
    return result


def validation_summary(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    result: dict[str, Mapping[str, str]] = {}
    for row in rows:
        if row.get("split") == "validation_is" and row.get("view") == "actual_routed_total":
            result[str(row.get("adapter_id", ""))] = row
    return result


def validation_risk(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    result: dict[str, Mapping[str, str]] = {}
    for row in rows:
        if row.get("split") == "validation_is" and row.get("view") == "actual_routed_total":
            result[str(row.get("adapter_id", ""))] = row
    return result


def stage191_read(adapter_id: str) -> str:
    if adapter_id == "s190_bctl":
        return "reference_net_pf_ok_but_dd_and_mid_pf_fail(참조 순손익/수익요인은 통과지만 낙폭/중반 수익요인 실패)"
    if adapter_id == "s190_ls_tp475":
        return "primary_tp475_dd_pass_near_net_miss_mid_pf_fail(주 단서 익절 4.75 낙폭 통과 순손익 근접 실패 중반 수익요인 실패)"
    if adapter_id == "s190_ls_r0365":
        return "risk_lift_net_help_but_dd_late_concentration_damage(위험 상향 순손익 도움 낙폭/후반 집중 손상)"
    if adapter_id == "s190_ls_r0365_tp475":
        return "risk_plus_tp_net_best_but_dd_and_late_concentration_fail(위험+익절 순손익 최선이나 낙폭/후반 집중 실패)"
    return "unknown(알 수 없음)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, str]],
    segment_rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, str]],
    balance_rows: Sequence[Mapping[str, str]],
    concentration_rows: Sequence[Mapping[str, str]],
    risk_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    segments = validation_segments(segment_rows)
    summaries = validation_summary(summary_rows)
    balances = lookup_by_adapter_split(balance_rows)
    concentration = lookup_by_adapter_split(concentration_rows)
    risks = validation_risk(risk_rows)
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        early = segments.get((adapter_id, "early"), {})
        mid = segments.get((adapter_id, "mid"), {})
        late = segments.get((adapter_id, "late"), {})
        summary = summaries.get(adapter_id, {})
        balance = balances.get((adapter_id, "validation_is"), {})
        conc = concentration.get((adapter_id, "validation_is"), {})
        risk = risks.get(adapter_id, {})
        validation_pf = as_float(row, "validation_pf")
        validation_net = as_float(row, "validation_net")
        validation_dd = as_float(row, "validation_balance_dd_percent")
        validation_mid_pf = as_float(row, "validation_mid_pf")
        late_share = as_float(row, "validation_late_net_share")
        net_gap = validation_net - LEGACY_34D["net_profit"]
        dd_gap = validation_dd - LEGACY_34D["max_drawdown_percent"]
        mid_pf_gap = validation_mid_pf - LEGACY_34D["profit_factor"]
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "label": row.get("label", ""),
                "axis": row.get("axis", ""),
                "risk_pct_cap": as_float(row, "model_risk_max_pct"),
                "atr_stop_multiplier": as_float(row, "atr_stop_multiplier"),
                "atr_take_profit_multiplier": as_float(row, "atr_take_profit_multiplier"),
                "validation_pf": validation_pf,
                "validation_pf_pass_34d": pass_bool(validation_pf, LEGACY_34D["profit_factor"]),
                "validation_net": validation_net,
                "validation_net_gap_vs_34d": net_gap,
                "validation_net_pass_34d": pass_bool(validation_net, LEGACY_34D["net_profit"]),
                "validation_dd_percent": validation_dd,
                "validation_dd_gap_above_34d": dd_gap,
                "validation_dd_pass_34d": pass_bool(validation_dd, LEGACY_34D["max_drawdown_percent"], "below"),
                "validation_mid_pf": validation_mid_pf,
                "validation_mid_pf_gap_vs_34d_pf": mid_pf_gap,
                "validation_mid_pf_pass_34d_pf": pass_bool(validation_mid_pf, LEGACY_34D["profit_factor"]),
                "validation_late_net_share": late_share,
                "validation_late_share_ok_le_50pct": late_share <= 0.5,
                "validation_early_pf": as_float(early, "profit_factor"),
                "validation_mid_net": as_float(mid, "net_profit"),
                "validation_mid_mfe_capture": as_float(mid, "mfe_capture_ratio"),
                "validation_late_pf": as_float(late, "profit_factor"),
                "validation_trade_count": as_float(summary, "trade_count"),
                "validation_mfe_capture_ratio": as_float(summary, "mfe_capture_ratio"),
                "validation_cost_stressed_expectancy": as_float(summary, "cost_stressed_expectancy"),
                "validation_report_dd_percent": as_float(balance, "max_drawdown_percent"),
                "validation_split_quality_flag": balance.get("split_quality_flag", ""),
                "validation_top1_net_share": as_float(conc, "top1_winner_share_of_net"),
                "validation_top5_net_share": as_float(conc, "top5_winner_share_of_net"),
                "validation_last_quarter_net_share": as_float(conc, "last_quarter_net_share"),
                "risk_floor_applied_count": as_float(risk, "risk_floor_applied_count"),
                "avg_model_risk_pct": as_float(risk, "avg_model_risk_pct"),
                "max_model_risk_pct": as_float(risk, "max_model_risk_pct"),
                "avg_executed_lot": as_float(risk, "avg_executed_lot"),
                "max_executed_lot": as_float(risk, "max_executed_lot"),
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": as_float(row, "oos_net"),
                "oos_dd_percent": as_float(row, "oos_balance_dd_percent"),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage191_read": stage191_read(adapter_id),
            }
        )
    return rows


def pick_primary_clue(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if bool(row.get("validation_dd_pass_34d"))]
    if candidates:
        return max(
            candidates,
            key=lambda row: (
                as_float(row, "validation_net"),
                as_float(row, "validation_mid_pf"),
                -as_float(row, "validation_late_net_share"),
            ),
        )
    return max(rows, key=lambda row: (-as_float(row, "validation_dd_gap_above_34d"), as_float(row, "validation_net")))


def pick_net_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: (as_float(row, "validation_net"), as_float(row, "validation_pf")))


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = {str(row.get("adapter_id", "")): row for row in tradeoff_rows}
    bctl = rows.get("s190_bctl", {})
    tp475 = rows.get("s190_ls_tp475", {})
    risk_tp = rows.get("s190_ls_r0365_tp475", {})
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "TP 4.75(익절 4.75)는 validation DD(검증 낙폭)를 34D(34D) 아래로 낮췄다.",
            "comparison_baseline": "s190_bctl control(대조군)",
            "likely_drivers": "take profit multiplier(익절 배수) 확장이 손익 분포를 바꾸며 DD(낙폭)를 낮췄지만 net(순손익)을 조금 깎았다.",
            "segment_checks": "early/mid/late(초반/중반/후반), validation/OOS(검증/표본외), late concentration(후반 집중), MFE capture(최대 유리 이동 포착)를 확인했다.",
            "trade_shape": (
                f"tp475 net_gap_vs_34d={as_float(tp475, 'validation_net_gap_vs_34d'):.2f}; "
                f"tp475 dd_gap_above_34d={as_float(tp475, 'validation_dd_gap_above_34d'):.4f}; "
                f"tp475 mid_pf={as_float(tp475, 'validation_mid_pf'):.6f}"
            ),
            "alternative_explanations": "DD(낙폭) 개선은 신호 품질 개선이 아니라 exit geometry(청산 구조) 변화일 수 있다.",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Stage192(192단계)에서 TP 4.75(익절 4.75)의 DD(낙폭) 단서를 유지하며 mid PF(중반 수익요인)와 net(순손익)을 회복한다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "risk lift(위험 상향)는 net(순손익)을 회복했지만 DD(낙폭)와 late concentration(후반 집중)을 악화했다.",
            "comparison_baseline": "s190_ls_tp475 DD-pass clue(낙폭 통과 단서)",
            "likely_drivers": "risk cap(위험 상한) 0.0365가 좋은 구간 수익도 키우지만 손실 클러스터도 함께 키웠다.",
            "segment_checks": "validation DD(검증 낙폭), late share(후반 비중), OOS DD(표본외 낙폭), risk telemetry(위험 기록)를 확인했다.",
            "trade_shape": (
                f"risk_tp net={as_float(risk_tp, 'validation_net'):.2f}; "
                f"risk_tp dd={as_float(risk_tp, 'validation_dd_percent'):.4f}; "
                f"risk_tp late_share={as_float(risk_tp, 'validation_late_net_share'):.4f}"
            ),
            "alternative_explanations": "net(순손익) 개선은 alpha(알파) 개선이 아니라 position size(포지션 크기) 확대 효과일 수 있다.",
            "attribution_confidence": "high(높음)",
            "next_probe": "Stage192(192단계)는 risk lift(위험 상향)를 주축으로 쓰지 않고, DD(낙폭)를 깨지 않는 net recovery(순손익 회복)만 좁게 본다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "모든 Stage190(190단계) 변형에서 validation mid PF(검증 중반 수익요인)가 34D PF(34D 수익요인) 아래에 남았다.",
            "comparison_baseline": "legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 핵심 성과 지표 목표)",
            "likely_drivers": "risk/TP(위험/익절)만 바꾸면 mid segment(중반 구간)의 진입 품질 문제를 직접 고치지 못한다.",
            "segment_checks": "chronological third(시간 3분할) mid segment(중반 구간) PF(수익요인), net(순손익), MFE capture(최대 유리 이동 포착)를 확인했다.",
            "trade_shape": (
                f"bctl mid_pf={as_float(bctl, 'validation_mid_pf'):.6f}; "
                f"tp475 mid_pf={as_float(tp475, 'validation_mid_pf'):.6f}; "
                f"risk_tp mid_pf={as_float(risk_tp, 'validation_mid_pf'):.6f}"
            ),
            "alternative_explanations": "중반 약점은 model score(모델 점수), context gate(문맥 게이트), lifecycle(보유 생명주기) 중 하나일 수 있어 Stage191(191단계)에서 확정하지 않는다.",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Stage192(192단계)는 mid segment(중반 구간)를 직접 겨냥하되 TP 4.75(익절 4.75)의 DD(낙폭) 장점을 잃지 않는 질문으로 제한한다.",
        },
    ]


def build_route_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    primary = pick_primary_clue(tradeoff_rows)
    net_ref = pick_net_reference(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "route": "stage192_primary(192단계 주 경로)",
            "decision": DECISION,
            "source_clue": "s190_ls_tp475_dd_pass_near_net_miss(익절 4.75 낙폭 통과 순손익 근접 실패)",
            "bounded_question": "Can Stage192(192단계) keep TP 4.75(익절 4.75) DD(낙폭) benefit while recovering validation net/PF(검증 순손익/수익요인) and mid PF(중반 수익요인)?",
            "why": (
                f"primary={primary.get('adapter_id')}; "
                f"net_gap_vs_34d={as_float(primary, 'validation_net_gap_vs_34d'):.2f}; "
                f"dd_gap_above_34d={as_float(primary, 'validation_dd_gap_above_34d'):.4f}."
            ),
            "guardrail": "do_not_use_risk_lift_as_score_improvement(위험 상향을 점수 개선으로 오해하지 않기)",
        },
        {
            "run_id": RUN_ID,
            "route": "reference_only(참조 전용)",
            "decision": DECISION,
            "source_clue": "s190_bctl_or_best_net_reference(대조군 또는 최고 순손익 참조)",
            "bounded_question": "Keep the best net/PF(순손익/수익요인) surface as comparison only.",
            "why": (
                f"net_reference={net_ref.get('adapter_id')}; "
                f"net={as_float(net_ref, 'validation_net'):.2f}; "
                f"dd={as_float(net_ref, 'validation_dd_percent'):.4f}; "
                f"mid_pf={as_float(net_ref, 'validation_mid_pf'):.6f}."
            ),
            "guardrail": "not_final_not_baseline_not_runtime_authority(최종/기준선/런타임 권위 아님)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "risk_lift_variants(위험 상향 변형)",
            "bounded_question": "Preserve risk lift(위험 상향) as damage memory unless DD(낙폭) guard is solved.",
            "why": "risk lift(위험 상향)는 net(순손익)을 키웠지만 validation DD(검증 낙폭)와 late concentration(후반 집중)을 악화했다.",
            "guardrail": "do_not_cherry_pick_final_net(최종 순손익만 골라보지 않기)",
        },
    ]


def tradeoff_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | TP(익절) | risk(위험) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {tp:.2f} | {risk:.4f} | {pf:.6f} | {net:.2f} | {dd:.4f} | {mid:.6f} | {late:.4f} | {read} |".format(
                adapter_id=row.get("adapter_id", ""),
                tp=as_float(row, "atr_take_profit_multiplier"),
                risk=as_float(row, "risk_pct_cap"),
                pf=as_float(row, "validation_pf"),
                net=as_float(row, "validation_net"),
                dd=as_float(row, "validation_dd_percent"),
                mid=as_float(row, "validation_mid_pf"),
                late=as_float(row, "validation_late_net_share"),
                read=row.get("stage191_read", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    primary = pick_primary_clue(tradeoff_rows)
    net_ref = pick_net_reference(tradeoff_rows)
    return f"""# Stage191 Follow-up Review(191단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage190_closeout_commit(원천 190단계 종료 커밋): `{SOURCE_STAGE190_CLOSEOUT_COMMIT}`
- source_stage190_hash_record_commit(원천 190단계 해시 기록 커밋): `{SOURCE_STAGE190_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage190(190단계)가 validation net/PF(검증 순손익/수익요인)를 보존하고 validation DD(검증 낙폭)를 낮추며 validation mid PF(검증 중반 수익요인)와 OOS(표본외)를 충분히 지켰는지 판독했다.

## KPI Read(KPI 핵심 성과 지표 판독)

{tradeoff_table(tradeoff_rows)}

## Easy Read(쉬운 판독)

Stage190(190단계)는 아직 34D(34D) 이상 KPI(핵심 성과 지표) 후보가 아니다. `s190_ls_tp475`는 validation DD(검증 낙폭) `12.6421%`로 34D(34D) 기준 `12.909136%` 아래에 들어온 단서다. 하지만 validation net(검증 순손익) `978.36`이 34D(34D) 기준 `987.60`보다 낮고, validation mid PF(검증 중반 수익요인)도 `1.386547`로 약하다.

`s190_ls_r0365_tp475`는 validation net(검증 순손익) `1167.26`까지 올라가지만 validation DD(검증 낙폭)가 `14.1540%`로 악화되고 late share(후반 비중)가 `0.5464`로 커진다. Effect(효과): net(순손익) 회복을 risk lift(위험 상향)로만 해결하면 34D(34D) 목표의 DD(낙폭) 품질을 잃는다.

## Best Clue(최선 단서)

- primary_clue(주 단서): `{primary.get("adapter_id", "none")}`
- validation_net_gap_vs_34d(검증 순손익 34D 대비 차이): `{as_float(primary, "validation_net_gap_vs_34d"):.2f}`
- validation_dd_gap_above_34d(검증 낙폭 34D 초과 차이): `{as_float(primary, "validation_dd_gap_above_34d"):.4f}`
- validation_mid_pf(검증 중반 수익요인): `{as_float(primary, "validation_mid_pf"):.6f}`
- net_reference(순손익 참조): `{net_ref.get("adapter_id", "none")}`

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): TP 4.75(익절 4.75)의 DD(낙폭) 장점을 유지하면서 net(순손익) `+9.24` 이상과 mid PF(중반 수익요인)를 회복하는 좁은 수리가 필요하다.
- effect(효과): legacy 34D(레거시 34D)는 KPI target(핵심 성과 지표 목표)로만 쓰고, v2-native(브이투 고유) 수리 경로를 계속한다.

Stage191(191단계)는 research/development only(연구개발 전용)입니다. Effect(효과): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않습니다.
"""


def decision_markdown() -> str:
    return f"""# Stage191 Decision(191단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage190_closeout_commit(원천 190단계 종료 커밋): `{SOURCE_STAGE190_CLOSEOUT_COMMIT}`
- source_stage190_hash_record_commit(원천 190단계 해시 기록 커밋): `{SOURCE_STAGE190_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage191(191단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage192(192단계)에서 TP 4.75(익절 4.75)의 DD(낙폭) 단서를 유지하면서 net/mid PF(순손익/중반 수익요인)를 회복하는 bounded repair(경계 수정)를 실행한다.
"""


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage192(192단계)는 Stage191(191단계)이 보존한 `s190_ls_tp475` 단서를 좁게 수리한다.

## Bounded Question(경계 질문)

Can TP 4.75(익절 4.75)의 validation DD(검증 낙폭) pass(통과)를 보존하면서 validation net(검증 순손익)을 34D(34D) 이상으로 회복하고 validation mid PF(검증 중반 수익요인)와 late concentration(후반 집중)을 악화시키지 않을 수 있는가?

Effect(효과): risk lift(위험 상향)만으로 net(순손익)을 키우는 길을 피하고, v2-native(브이투 고유) midsegment repair(중반 구간 수정) 질문으로 좁힌다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage192 Inputs(192단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage190_quality(원천 190단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage190_summary(원천 190단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage190_segment(원천 190단계 구간): `{rel(SOURCE_SEGMENT)}`
- source_stage190_risk_atr(원천 190단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage192 Review Index(192단계 검토 색인)

- status(상태): `open_planned_from_stage191`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage192 Selection Status(192단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage191`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage191 Selection Status(191단계 선택 상태)

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
        f"""# Stage191 Review Index(191단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage191(191단계) closed(종료) as `{DECISION}` and Stage192(192단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): TP 4.75(익절 4.75)의 DD(낙폭) 단서를 유지하며 net/mid PF(순손익/중반 수익요인) 회복을 좁게 시험한다.
- >-
  Stage191 evidence(191단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): Stage190(190단계)의 net/DD/mid PF(순손익/낙폭/중반 수익요인) 상충을 숨기지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage191_stage190_net_preserving_dd_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage191_stage190_net_preserving_dd_followup_review:
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
  attribution_path: {rel(ATTRIBUTION_PATH)}
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
- adapter_under_review(검토 중 어댑터): `stage192_tp475_midsegment_net_recovery_without_dd_regression`
- status(상태): `stage191_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage191(191단계)는 Stage190(190단계) net-preserving DD repair(순손익 보존 낙폭 수정)를 follow-up review(후속 검토)했다. Effect(효과): `s190_ls_tp475`를 DD-pass near-miss clue(낙폭 통과 근접 실패 단서)로 보존하고, 위험 상향 변형은 DD/late concentration damage memory(낙폭/후반 집중 손상 기억)로 남긴다.

## Latest Stage191 Evidence(최신 191단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage191 Stage190 net-preserving DD follow-up review closeout(191단계 190단계 순손익 보존 낙폭 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): TP 4.75(익절 4.75)의 DD-pass near-miss clue(낙폭 통과 근접 실패 단서)를 Stage192(192단계) 수리 질문으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    primary = pick_primary_clue(tradeoff_rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage191_stage190_net_preserving_dd_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage190_closeout_commit", SOURCE_STAGE190_CLOSEOUT_COMMIT),
                        ("source_stage190_hash_record_commit", SOURCE_STAGE190_HASH_RECORD_COMMIT),
                        ("primary_clue", primary.get("adapter_id", "none")),
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
            "ledger_row_id": f"{RUN_ID}__stage190_net_preserving_dd_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage190_net_preserving_dd_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage190_net_dd_midpf_tradeoff",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("primary_clue", primary.get("adapter_id", "none")),
                    ("validation_net", f"{as_float(primary, 'validation_net'):.2f}"),
                    ("validation_dd", f"{as_float(primary, 'validation_dd_percent'):.4f}"),
                    ("validation_mid_pf", f"{as_float(primary, 'validation_mid_pf'):.6f}"),
                    ("validation_net_gap_vs_34d", f"{as_float(primary, 'validation_net_gap_vs_34d'):.2f}"),
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
            "notes": "Stage191 reviewed Stage190 net/DD tradeoff and opened Stage192 TP475 midsegment net recovery repair.",
        }
    ]
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
    }


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    for path in (
        PRODUCER_PATH,
        REPORT_PATH,
        DECISION_PATH,
        TRADEOFF_MATRIX_PATH,
        ATTRIBUTION_PATH,
        ROUTE_MATRIX_PATH,
        STAGE_LEDGER_PATH,
    ):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage191_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage191 Stage190 net-preserving DD follow-up review evidence.",
                }
            )
    return rows


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
    artifacts_payload: Mapping[str, Any],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
        "attribution": rel(ATTRIBUTION_PATH),
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "tradeoff_rows": list(tradeoff_rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "ledger_payload": ledger_payload,
        "artifacts_payload": artifacts_payload,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage191 Closeout Packet(191단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `completed`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def main() -> int:
    quality_rows = load_csv(SOURCE_QUALITY)
    segment_rows = load_csv(SOURCE_SEGMENT)
    summary_rows = load_csv(SOURCE_SUMMARY)
    balance_rows = load_csv(SOURCE_BALANCE)
    concentration_rows = load_csv(SOURCE_CONCENTRATION)
    risk_rows = load_csv(SOURCE_RISK_ATR)

    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, summary_rows, balance_rows, concentration_rows, risk_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows(tradeoff_rows)

    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_md(REPORT_PATH, report_markdown(tradeoff_rows))
    write_md(DECISION_PATH, decision_markdown())
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(tradeoff_rows, route_rows)
    artifacts_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, ledger_payload, artifacts_payload)

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
