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

STAGE_ID = "189_adapter_research__stage188_context_feature_followup_review"
RUN_ID = "run189A_stage189_stage188_context_feature_followup_review_v1"
PACKET_ID = "stage189_stage188_context_feature_followup_review_v1"
PARENT_RUN_ID = "run188A_stage188_v2_native_context_feature_branch_after_midwide_tradeoff_v1"
SOURCE_STAGE_ID = "188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff"
SOURCE_RUN_ID = "run188A_stage188_v2_native_context_feature_branch_after_midwide_tradeoff_v1"
SOURCE_STAGE188_CLOSEOUT_COMMIT = "ef973cd401a4dcc02021503a6a77c23b93dda977"
SOURCE_STAGE188_HASH_RECORD_COMMIT = "837e919a8d304367464354156f2ee2fbf6c10c80"
NEXT_STAGE_ID = "190_adapter_research__net_preserving_dd_repair_from_long_strict_clue"
NEXT_RUN_ID = "run190A_stage190_net_preserving_dd_repair_from_long_strict_clue_v1"
NEXT_PACKET_ID = "stage190_net_preserving_dd_repair_from_long_strict_clue_v1"
DECISION = "open_stage190_net_preserving_dd_repair_from_long_strict_clue_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_net_preserving_dd_repair"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage188_mt5_reports_completed"

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

SOURCE_REPORT = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_context_feature_report.md")
SOURCE_QUALITY = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_quality_matrix.csv")
SOURCE_SEGMENT = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_segment_kpi_summary.csv")
SOURCE_SUMMARY = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_context_feature_summary.csv")
SOURCE_BALANCE = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_balance_curve_audit.csv")
SOURCE_GATE = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_gate_feature_summary.csv")
SOURCE_RISK_ATR = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_risk_atr_telemetry.csv")
SOURCE_DECISION = Path("stages/188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff/03_reviews/stage188_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage189_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage189_context_feature_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage189_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage189_route_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage189_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage189/stage188_context_feature_followup_review.py")
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


def by_adapter(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("adapter_id", "")): row for row in rows}


def nested_by_adapter_split(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {(str(row.get("adapter_id", "")), str(row.get("split", ""))): row for row in rows}


def segment_lookup(segment_rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    result: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in segment_rows:
        if row.get("split") != "validation_is":
            continue
        if row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") != "chronological_third":
            continue
        result[(str(row.get("adapter_id", "")), str(row.get("segment", "")))] = row
    return result


def gate_lookup(gate_rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {(str(row.get("adapter_id", "")), str(row.get("split", ""))): row for row in gate_rows}


def summary_lookup(summary_rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {
        (str(row.get("adapter_id", "")), str(row.get("split", ""))): row
        for row in summary_rows
        if row.get("view") == "actual_routed_total"
    }


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, str]],
    segment_rows: Sequence[Mapping[str, str]],
    balance_rows: Sequence[Mapping[str, str]],
    gate_rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    segments = segment_lookup(segment_rows)
    balances = nested_by_adapter_split(balance_rows)
    gates = gate_lookup(gate_rows)
    summaries = summary_lookup(summary_rows)
    control = by_adapter(quality_rows).get("s188_bctl", {})
    control_val_net = as_float(control, "validation_net")
    control_val_dd = as_float(control, "validation_balance_dd_percent")
    control_mid_pf = as_float(control, "validation_mid_pf")
    control_oos_net = as_float(control, "oos_net")
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        val_gate = gates.get((adapter_id, "validation_is"), {})
        oos_gate = gates.get((adapter_id, "oos"), {})
        early = segments.get((adapter_id, "early"), {})
        mid = segments.get((adapter_id, "mid"), {})
        late = segments.get((adapter_id, "late"), {})
        val_balance = balances.get((adapter_id, "validation_is"), {})
        oos_balance = balances.get((adapter_id, "oos"), {})
        val_summary = summaries.get((adapter_id, "validation_is"), {})
        val_net = as_float(row, "validation_net")
        val_dd = as_float(row, "validation_balance_dd_percent")
        mid_pf = as_float(row, "validation_mid_pf")
        oos_net = as_float(row, "oos_net")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "short_block_rule": row.get("short_block_rule", ""),
                "validation_pf": as_float(row, "validation_pf"),
                "validation_net": val_net,
                "validation_net_gap_vs_34d": val_net - LEGACY_34D["net_profit"],
                "validation_net_delta_vs_control": val_net - control_val_net,
                "validation_dd": val_dd,
                "validation_dd_gap_vs_34d": val_dd - LEGACY_34D["max_drawdown_percent"],
                "validation_dd_delta_vs_control": val_dd - control_val_dd,
                "validation_mid_pf": mid_pf,
                "validation_mid_pf_delta_vs_control": mid_pf - control_mid_pf,
                "validation_late_net_share": as_float(row, "validation_late_net_share"),
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": oos_net,
                "oos_net_delta_vs_control": oos_net - control_oos_net,
                "oos_dd": as_float(row, "oos_balance_dd_percent"),
                "validation_trade_count": as_float(val_summary, "trade_count"),
                "validation_same_move_reentry_ratio": as_float(val_summary, "same_move_reentry_ratio"),
                "validation_mfe_capture_ratio": as_float(val_summary, "mfe_capture_ratio"),
                "validation_cost_stressed_expectancy": as_float(val_summary, "cost_stressed_expectancy"),
                "validation_blocked_signal_ratio": as_float(val_gate, "blocked_signal_ratio"),
                "oos_blocked_signal_ratio": as_float(oos_gate, "blocked_signal_ratio"),
                "early_pf": as_float(early, "profit_factor"),
                "mid_net": as_float(mid, "net_profit"),
                "mid_mfe_capture": as_float(mid, "mfe_capture_ratio"),
                "late_pf": as_float(late, "profit_factor"),
                "balance_split_flag": val_balance.get("split_quality_flag", ""),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage189_read": stage189_read(adapter_id),
            }
        )
    return rows


def stage189_read(adapter_id: str) -> str:
    if adapter_id == "s188_bctl":
        return "control_keeps_net_pf_but_fails_dd_and_mid_pf"
    if adapter_id == "s188_long_strict":
        return "dd_clue_salvage_net_midpf_damage"
    if adapter_id == "s188_short_relief":
        return "short_relief_overexpands_trade_supply_and_damages_pf"
    if adapter_id == "s188_gate_off":
        return "gate_off_confirms_context_gate_is_required"
    return "unknown"


def best_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            as_float(row, "validation_net") >= LEGACY_34D["net_profit"],
            as_float(row, "validation_pf") >= LEGACY_34D["profit_factor"],
            -max(0.0, as_float(row, "validation_dd_gap_vs_34d")),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_pf"),
        ),
    )


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = {str(row.get("adapter_id", "")): row for row in tradeoff_rows}
    control = rows.get("s188_bctl", {})
    long_strict = rows.get("s188_long_strict", {})
    short_relief = rows.get("s188_short_relief", {})
    gate_off = rows.get("s188_gate_off", {})
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "long_strict(롱 강화)는 validation DD(검증 낙폭)를 34D(34D) 아래로 낮췄다.",
            "comparison_baseline": "s188_bctl control(대조군)",
            "likely_drivers": "blocked signal ratio(차단 신호 비율)가 0.4915에서 0.5385로 올라가며 위험 구간 일부를 줄였다.",
            "segment_checks": "early/mid/late(초반/중반/후반), validation/OOS(검증/표본외), gate ratio(게이트 비율), balance DD(잔고 낙폭)를 확인했다.",
            "trade_shape": (
                f"control trades={as_float(control, 'validation_trade_count'):.0f}, "
                f"long_strict trades={as_float(long_strict, 'validation_trade_count'):.0f}, "
                f"dd_delta={as_float(long_strict, 'validation_dd_delta_vs_control'):.4f}, "
                f"net_delta={as_float(long_strict, 'validation_net_delta_vs_control'):.2f}"
            ),
            "alternative_explanations": "DD(낙폭) 개선이 신호 품질 개선이 아니라 trade count(거래 수) 축소 효과일 수 있다.",
            "attribution_confidence": "medium",
            "next_probe": "Stage190(190단계)에서 control(대조군) net/PF(순손익/수익요인)를 보존하면서 long_strict(롱 강화)의 DD(낙폭) 단서만 제한적으로 적용한다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "long_strict(롱 강화)는 validation net(검증 순손익)과 mid PF(중반 수익요인)를 훼손했다.",
            "comparison_baseline": "s188_bctl control(대조군)",
            "likely_drivers": "차단이 늘면서 중반 구간의 유효 수익 공급도 같이 잘렸다.",
            "segment_checks": "mid segment(중반 구간) net/PF(순손익/수익요인), MFE capture(최대유리이동 포착), late concentration(후반 집중)을 확인했다.",
            "trade_shape": (
                f"mid_pf_delta={as_float(long_strict, 'validation_mid_pf_delta_vs_control'):.6f}; "
                f"late_share={as_float(long_strict, 'validation_late_net_share'):.4f}"
            ),
            "alternative_explanations": "중반 약점은 gate(게이트) 자체보다 model score surface(모델 점수 표면) 포화 또는 exit timing(청산 타이밍) 문제일 수 있다.",
            "attribution_confidence": "medium",
            "next_probe": "DD(낙폭) 감소 단서는 살리되 long filter(롱 필터)는 조건부/부분 적용으로 제한한다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "short_relief(숏 완화)와 gate_off(게이트 해제)는 trade supply(거래 공급)를 늘렸지만 PF(수익요인)와 OOS DD(표본외 낙폭)를 망가뜨렸다.",
            "comparison_baseline": "s188_bctl control(대조군)",
            "likely_drivers": "context gate(문맥 게이트)가 제거되거나 약해지면서 낮은 품질의 신호가 대량 복귀했다.",
            "segment_checks": "trade count(거래 수), OOS DD(표본외 낙폭), early/mid/late PF(초반/중반/후반 수익요인), MFE capture(최대유리이동 포착)을 확인했다.",
            "trade_shape": (
                f"short_relief_net_delta={as_float(short_relief, 'validation_net_delta_vs_control'):.2f}; "
                f"gate_off_net_delta={as_float(gate_off, 'validation_net_delta_vs_control'):.2f}"
            ),
            "alternative_explanations": "완화 자체가 나쁘다기보다 완화된 신호를 별도 score/risk bucket(점수/위험 버킷) 없이 같은 lot/risk(수량/위험)로 다룬 것이 문제일 수 있다.",
            "attribution_confidence": "high",
            "next_probe": "short_relief(숏 완화)와 gate_off(게이트 해제)는 failure memory(실패 기억)로 보존하고 반복하지 않는다.",
        },
    ]


def build_route_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    control = next((row for row in tradeoff_rows if row.get("adapter_id") == "s188_bctl"), {})
    long_strict = next((row for row in tradeoff_rows if row.get("adapter_id") == "s188_long_strict"), {})
    return [
        {
            "run_id": RUN_ID,
            "route": "stage190_primary",
            "decision": DECISION,
            "source_clue": "s188_long_strict_dd_below_34d_plus_s188_bctl_net_pf_reference",
            "bounded_question": "Can Stage190(190단계) preserve control(대조군) validation net/PF(검증 순손익/수익요인) while importing only the useful DD(낙폭) part of long_strict(롱 강화)?",
            "why": (
                f"control net={as_float(control, 'validation_net'):.2f}, PF={as_float(control, 'validation_pf'):.2f}; "
                f"long_strict DD={as_float(long_strict, 'validation_dd'):.4f}, but net={as_float(long_strict, 'validation_net'):.2f}."
            ),
            "guardrail": "do_not_repeat_short_relief_or_gate_off_as_primary",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory",
            "decision": DECISION,
            "source_clue": "s188_short_relief_and_s188_gate_off",
            "bounded_question": "Preserve short_relief(숏 완화) and gate_off(게이트 해제) as failure memory(실패 기억).",
            "why": "Both expanded trades(거래)를 많이 늘렸지만 PF(수익요인), OOS DD(표본외 낙폭), MFE capture(최대유리이동 포착)을 훼손했다.",
            "guardrail": "do_not_hide_failed_branch",
        },
        {
            "run_id": RUN_ID,
            "route": "reference_only",
            "decision": DECISION,
            "source_clue": "s188_bctl",
            "bounded_question": "Keep control(대조군) as development reference(개발 참조).",
            "why": "It still best preserves validation net/PF(검증 순손익/수익요인), but DD/mid PF(낙폭/중반 수익요인) fail.",
            "guardrail": "not_final_not_baseline_not_runtime_authority",
        },
    ]


def tradeoff_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | axis(축) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | blocked signal(차단 신호) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {axis} | {validation_pf:.6f} | {validation_net:.2f} | {validation_dd:.4f} | {validation_mid_pf:.6f} | {oos_pf:.6f} | {validation_blocked_signal_ratio:.4f} | {stage189_read} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    best = best_reference(tradeoff_rows)
    long_strict = next((row for row in tradeoff_rows if row.get("adapter_id") == "s188_long_strict"), {})
    return f"""# Stage189 Stage188 Context Feature Follow-up Review(189단계 188단계 문맥 피처 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage188_closeout_commit(원천 188단계 종료 커밋): `{SOURCE_STAGE188_CLOSEOUT_COMMIT}`
- source_stage188_hash_record_commit(원천 188단계 해시 기록 커밋): `{SOURCE_STAGE188_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

{tradeoff_table(tradeoff_rows)}

## Easy Read(쉬운 판독)

Stage188(188단계)는 final adapter(최종 어댑터)가 아닙니다. `s188_bctl` control(대조군)은 validation net(검증 순손익) `1012.75`와 PF(수익요인) `1.69`로 가장 낫지만 DD(낙폭) `13.3347%`와 mid PF(중반 수익요인) `1.485500`이 실패입니다.

`s188_long_strict`는 DD(낙폭)를 `12.7583%`로 34D(34D) 기준 `12.909136%` 아래로 낮춘 단서입니다. 하지만 validation net(검증 순손익) `889.64`, mid PF(중반 수익요인) `1.362042`, late share(후반 비중) `0.5305`라서 그대로 채택할 수 없습니다.

`s188_short_relief`와 `s188_gate_off`는 context gate(문맥 게이트)가 필요하다는 failure memory(실패 기억)입니다. Effect(효과): Stage190(190단계)는 gate(게이트)를 풀지 않고, long_strict(롱 강화)의 DD(낙폭) 단서만 net-preserving(순손익 보존) 방식으로 제한 적용한다.

## Best Remaining Reference(남은 최선 참조)

- reference_adapter(참조 어댑터): `{best.get("adapter_id", "none")}`
- validation_net(검증 순손익): `{as_float(best, "validation_net"):.2f}`
- validation_pf(검증 수익요인): `{as_float(best, "validation_pf"):.6f}`
- validation_dd(검증 낙폭): `{as_float(best, "validation_dd"):.4f}`
- validation_mid_pf(검증 중반 수익요인): `{as_float(best, "validation_mid_pf"):.6f}`
- long_strict_dd_clue(롱 강화 낙폭 단서): `{as_float(long_strict, "validation_dd"):.4f}`

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): DD(낙폭) 개선 단서는 생겼지만 net/mid PF(순손익/중반 수익요인) 손상이 커서 Stage190(190단계)에서 net-preserving DD repair(순손익 보존 낙폭 수정)를 좁게 측정한다.
- effect(효과): 34D(34D)는 KPI target(핵심 성과 지표 목표)로만 쓰고, v2-native(브이투 고유) 수리 경로를 계속한다.

Stage189(189단계)는 research/development only(연구개발 전용)입니다. Effect(효과): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않습니다.
"""


def decision_markdown() -> str:
    return f"""# Stage189 Decision(189단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage188_closeout_commit(원천 188단계 종료 커밋): `{SOURCE_STAGE188_CLOSEOUT_COMMIT}`
- source_stage188_hash_record_commit(원천 188단계 해시 기록 커밋): `{SOURCE_STAGE188_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage189(189단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage190(190단계)에서 s188_long_strict(롱 강화)의 DD(낙폭) 단서를 control(대조군) net/PF(순손익/수익요인) 보존 조건으로 재측정한다.
"""


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage190(190단계)는 Stage189(189단계)가 보존한 long_strict(롱 강화) DD clue(낙폭 단서)를 net-preserving(순손익 보존) 방식으로 좁게 수리한다.

## Bounded Question(경계 질문)

Can a bounded net-preserving DD repair(경계 순손익 보존 낙폭 수정) keep the control(대조군) validation net/PF(검증 순손익/수익요인) while selectively importing the Stage188(188단계) long_strict(롱 강화) drawdown reduction(낙폭 감소) clue?

Effect(효과): gate_off(게이트 해제)나 short_relief(숏 완화)를 반복하지 않고, DD(낙폭) 단서만 제한적으로 적용해 34D(34D) KPI(핵심 성과 지표)에 가까워지는지 본다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage190 Inputs(190단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage188_quality(원천 188단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage188_summary(원천 188단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage188_segment(원천 188단계 구간): `{rel(SOURCE_SEGMENT)}`
- source_stage188_gate(원천 188단계 게이트): `{rel(SOURCE_GATE)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage190 Review Index(190단계 검토 색인)

- status(상태): `open_planned_from_stage189`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage190 Selection Status(190단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage189`
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
        f"""# Stage189 Selection Status(189단계 선택 상태)

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
        f"""# Stage189 Review Index(189단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
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
  Stage189(189단계) closed(종료) as `{DECISION}` and Stage190(190단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): long_strict(롱 강화)의 DD(낙폭) 단서를 control(대조군) net/PF(순손익/수익요인) 보존 조건으로 다시 측정한다.
- >-
  Stage189 evidence(189단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): Stage188(188단계)의 DD/net/mid PF(낙폭/순손익/중반 수익요인) 상충을 숨기지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 KPI target(핵심 성과 지표 목표)로만 쓴다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage189_stage188_context_feature_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage189_stage188_context_feature_followup_review:
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
- adapter_under_review(검토 중 어댑터): `stage190_net_preserving_dd_repair_from_long_strict_clue`
- status(상태): `stage189_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage189(189단계)는 Stage188(188단계) context/feature branch(문맥/피처 분기)를 follow-up review(후속 검토)했다. Effect(효과): long_strict(롱 강화)는 DD(낙폭) 단서로만 보존하고, short_relief/gate_off(숏 완화/게이트 해제)는 failure memory(실패 기억)로 보존한다.

## Latest Stage189 Evidence(최신 189단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
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
        f"\n## {utc_now()} Stage189 Stage188 context feature follow-up review closeout(189단계 188단계 문맥 피처 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage188(188단계)의 long_strict(롱 강화) DD(낙폭) 단서를 보존하고 Stage190(190단계) net-preserving DD repair(순손익 보존 낙폭 수정)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = best_reference(tradeoff_rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage189_stage188_context_feature_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage188_closeout_commit", SOURCE_STAGE188_CLOSEOUT_COMMIT),
                        ("source_stage188_hash_record_commit", SOURCE_STAGE188_HASH_RECORD_COMMIT),
                        ("reference", best.get("adapter_id", "none")),
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
            "ledger_row_id": f"{RUN_ID}__stage188_context_feature_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage188_context_feature_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage188_context_feature_followup_review",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("reference", best.get("adapter_id", "none")),
                    ("validation_net", f"{as_float(best, 'validation_net'):.2f}"),
                    ("validation_pf", f"{as_float(best, 'validation_pf'):.6f}"),
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
            "notes": "Stage189 reviewed Stage188 context feature tradeoff and opened Stage190 net-preserving DD repair.",
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
    for path in (PRODUCER_PATH, REPORT_PATH, DECISION_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage189_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage189 Stage188 context feature follow-up review evidence.",
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
        f"""# Stage189 Closeout Packet(189단계 종료 작업 묶음)

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
    balance_rows = load_csv(SOURCE_BALANCE)
    gate_rows = load_csv(SOURCE_GATE)
    summary_rows = load_csv(SOURCE_SUMMARY)
    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, balance_rows, gate_rows, summary_rows)
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
