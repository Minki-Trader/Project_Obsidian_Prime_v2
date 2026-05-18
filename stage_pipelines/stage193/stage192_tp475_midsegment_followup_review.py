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

STAGE_ID = "193_adapter_research__stage192_tp475_midsegment_followup_review"
RUN_ID = "run193A_stage193_stage192_tp475_midsegment_followup_review_v1"
PACKET_ID = "stage193_stage192_tp475_midsegment_followup_review_v1"
PARENT_RUN_ID = "run192A_stage192_tp475_midsegment_net_recovery_without_dd_regression_v1"
SOURCE_STAGE_ID = "192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression"
SOURCE_RUN_ID = "run192A_stage192_tp475_midsegment_net_recovery_without_dd_regression_v1"
SOURCE_STAGE192_CLOSEOUT_COMMIT = "7d02adb83a1ebc3fd9e1977b22dad75a39be16ff"
SOURCE_STAGE192_HASH_RECORD_COMMIT = "724af6a5e5c5ec0b46c3f14b0415dbdc63d4df9e"
NEXT_STAGE_ID = "194_adapter_research__tp475_late_concentration_midpf_repair"
NEXT_RUN_ID = "run194A_stage194_tp475_late_concentration_midpf_repair_v1"
NEXT_PACKET_ID = "stage194_tp475_late_concentration_midpf_repair_v1"
DECISION = "open_stage194_tp475_late_concentration_midpf_repair_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_tp475_late_midpf_repair"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage192_mt5_reports_completed"

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
    "stages/192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression/03_reviews/"
    "stage192_tp475_midsegment_report.md"
)
SOURCE_QUALITY = Path(
    "stages/192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression/03_reviews/"
    "stage192_quality_matrix.csv"
)
SOURCE_SEGMENT = Path(
    "stages/192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression/03_reviews/"
    "stage192_segment_kpi_summary.csv"
)
SOURCE_SUMMARY = Path(
    "stages/192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression/03_reviews/"
    "stage192_tp475_midsegment_summary.csv"
)
SOURCE_PROBABILITY = Path(
    "stages/192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression/03_reviews/"
    "stage192_probability_binding_summary.csv"
)
SOURCE_RISK_ATR = Path(
    "stages/192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression/03_reviews/"
    "stage192_risk_atr_telemetry.csv"
)
SOURCE_DECISION = Path(
    "stages/192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression/03_reviews/stage192_decision.md"
)

REPORT_PATH = REVIEWS_ROOT / "stage193_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage193_tp475_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage193_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage193_route_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage193_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage193/stage192_tp475_midsegment_followup_review.py")
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


def validation_segments(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    result: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in rows:
        if row.get("split") == "validation_is" and row.get("view") == "actual_routed_total":
            if row.get("segment_type") == "chronological_third":
                result[(str(row.get("adapter_id", "")), str(row.get("segment", "")))] = row
    return result


def validation_summary(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {
        str(row.get("adapter_id", "")): row
        for row in rows
        if row.get("split") == "validation_is" and row.get("view") == "actual_routed_total"
    }


def probability_binding(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, Any]]:
    bucket: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("split") != "validation_is" or row.get("view") != "actual_routed_total":
            continue
        adapter_id = str(row.get("adapter_id", ""))
        target = bucket.setdefault(
            adapter_id,
            {"adapter_id": adapter_id, "near_threshold_rows": 0.0, "band_rows": 0.0, "threshold_or_margin_not_met_rows": 0.0},
        )
        target["near_threshold_rows"] += as_float(row, "directional_near_threshold_001_rows")
        target["band_rows"] += as_float(row, "directional_050_060_band_rows")
        target["threshold_or_margin_not_met_rows"] += as_float(row, "threshold_or_margin_not_met_rows")
    return bucket


def stage193_read(adapter_id: str) -> str:
    if adapter_id == "s192_tp475_r0330":
        return "net_dd_pass_midpf_late_fail(순손익/낙폭 통과 중반 수익요인/후반 집중 실패)"
    if adapter_id == "s192_tp475_r0330_thr0553":
        return "same_as_r0330_threshold_nonbinding(위험 0.0330과 같음 문턱값 비구속)"
    if adapter_id == "s192_tp475_thr0553":
        return "same_as_reference_threshold_nonbinding(참조와 같음 문턱값 비구속)"
    return "reference_dd_pass_net_near_miss_midpf_late_fail(참조 낙폭 통과 순손익 근접 실패 중반/후반 실패)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, str]],
    segment_rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, str]],
    probability_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    segments = validation_segments(segment_rows)
    summaries = validation_summary(summary_rows)
    prob = probability_binding(probability_rows)
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        mid = segments.get((adapter_id, "mid"), {})
        late = segments.get((adapter_id, "late"), {})
        summary = summaries.get(adapter_id, {})
        pbind = prob.get(adapter_id, {})
        validation_net = as_float(row, "validation_net")
        validation_dd = as_float(row, "validation_balance_dd_percent")
        validation_mid_pf = as_float(row, "validation_mid_pf")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "label": row.get("label", ""),
                "axis": row.get("axis", ""),
                "risk_pct_cap": as_float(row, "model_risk_max_pct"),
                "atr_take_profit_multiplier": as_float(row, "atr_take_profit_multiplier"),
                "validation_pf": as_float(row, "validation_pf"),
                "validation_net": validation_net,
                "validation_net_gap_vs_34d": validation_net - LEGACY_34D["net_profit"],
                "validation_net_pass_34d": validation_net >= LEGACY_34D["net_profit"],
                "validation_dd_percent": validation_dd,
                "validation_dd_gap_above_34d": validation_dd - LEGACY_34D["max_drawdown_percent"],
                "validation_dd_pass_34d": validation_dd <= LEGACY_34D["max_drawdown_percent"],
                "validation_mid_pf": validation_mid_pf,
                "validation_mid_pf_gap_vs_34d_pf": validation_mid_pf - LEGACY_34D["profit_factor"],
                "validation_late_net_share": as_float(row, "validation_late_net_share"),
                "validation_mid_net": as_float(mid, "net_profit"),
                "validation_mid_mfe_capture": as_float(mid, "mfe_capture_ratio"),
                "validation_late_pf": as_float(late, "profit_factor"),
                "validation_trade_count": as_float(summary, "trade_count"),
                "validation_mfe_capture_ratio": as_float(summary, "mfe_capture_ratio"),
                "near_threshold_rows": as_float(pbind, "near_threshold_rows"),
                "band_rows": as_float(pbind, "band_rows"),
                "threshold_or_margin_not_met_rows": as_float(pbind, "threshold_or_margin_not_met_rows"),
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": as_float(row, "oos_net"),
                "oos_dd_percent": as_float(row, "oos_balance_dd_percent"),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage193_read": stage193_read(adapter_id),
            }
        )
    return rows


def best_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            bool(row.get("validation_dd_pass_34d")),
            bool(row.get("validation_net_pass_34d")),
            as_float(row, "validation_mid_pf"),
            -as_float(row, "validation_late_net_share"),
            as_float(row, "oos_pf"),
        ),
    )


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = {str(row.get("adapter_id", "")): row for row in tradeoff_rows}
    ref = rows.get("s192_tp475_ref", {})
    r0330 = rows.get("s192_tp475_r0330", {})
    thr = rows.get("s192_tp475_thr0553", {})
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "tiny risk nudge(작은 위험 상향)가 validation net/DD(검증 순손익/낙폭)를 동시에 34D(34D) 안으로 넣었다.",
            "comparison_baseline": "s192_tp475_ref reference(참조)",
            "likely_drivers": "risk cap(위험 상한) 0.0325에서 0.0330으로 아주 작게 오른 효과이며, entry signal(진입 신호) 자체 개선은 아니다.",
            "segment_checks": "validation/OOS(검증/표본외), mid PF(중반 수익요인), late share(후반 비중), segment net(구간 순손익)을 확인했다.",
            "trade_shape": (
                f"ref net={as_float(ref, 'validation_net'):.2f}, dd={as_float(ref, 'validation_dd_percent'):.4f}; "
                f"r0330 net={as_float(r0330, 'validation_net'):.2f}, dd={as_float(r0330, 'validation_dd_percent'):.4f}"
            ),
            "alternative_explanations": "net(순손익) 개선은 alpha(알파) 개선이 아니라 position sizing(포지션 크기 조정) 효과일 수 있다.",
            "attribution_confidence": "high(높음)",
            "next_probe": "Stage194(194단계)는 risk cap(위험 상한)을 더 올리지 않고 late/mid quality(후반/중반 품질)를 고친다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "threshold lift(문턱값 상향)는 결과를 바꾸지 않았다.",
            "comparison_baseline": "s192_tp475_ref and s192_tp475_thr0553(참조와 문턱값 변형)",
            "likely_drivers": "directional_near_threshold rows(방향 문턱값 근접 행)가 0이라 0.55/0.53 문턱값이 실제 주문 집합을 바꾸지 못했다.",
            "segment_checks": "probability binding(확률 구속), trade count(거래 수), segment KPI(구간 핵심 성과 지표)를 확인했다.",
            "trade_shape": (
                f"threshold near rows={as_float(thr, 'near_threshold_rows'):.0f}; "
                f"thr net={as_float(thr, 'validation_net'):.2f}; ref net={as_float(ref, 'validation_net'):.2f}"
            ),
            "alternative_explanations": "문턱값보다 context gate(문맥 게이트), lifecycle(보유 생명주기), time/regime exposure(시간/국면 노출)가 더 직접적인 조정축일 수 있다.",
            "attribution_confidence": "high(높음)",
            "next_probe": "Stage194(194단계)는 문턱값 반복 대신 late concentration(후반 집중)과 mid PF(중반 수익요인)를 직접 겨냥한다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "mid PF(중반 수익요인)와 late concentration(후반 집중)은 여전히 실패다.",
            "comparison_baseline": "legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 핵심 성과 지표 목표)",
            "likely_drivers": "TP/risk(익절/위험) 조정은 손익 규모를 바꾸지만 중반 구간의 진입 품질과 후반 집중을 직접 줄이지 못한다.",
            "segment_checks": "chronological third(시간 3분할), late share(후반 비중), MFE capture(최대 유리 이동 포착), OOS PF(표본외 수익요인)를 확인했다.",
            "trade_shape": (
                f"r0330 mid_pf={as_float(r0330, 'validation_mid_pf'):.6f}; "
                f"r0330 late_share={as_float(r0330, 'validation_late_net_share'):.4f}"
            ),
            "alternative_explanations": "후반 집중은 시장 구간 의존성일 수 있어, 다음 단계는 시간/문맥/생명주기 축의 작은 필터를 봐야 한다.",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Stage194(194단계)에서 s192_tp475_r0330을 reference(참조)로 두고 late concentration(후반 집중)을 줄이는 bounded repair(경계 수정)를 실행한다.",
        },
    ]


def build_route_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_reference(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "route": "stage194_primary(194단계 주 경로)",
            "decision": DECISION,
            "source_clue": "s192_tp475_r0330_net_dd_pass_midpf_late_fail(순손익/낙폭 통과 중반/후반 실패)",
            "bounded_question": "Can Stage194(194단계) keep s192_tp475_r0330 net/DD(순손익/낙폭) pass while reducing late concentration(후반 집중) and improving mid PF(중반 수익요인)?",
            "why": (
                f"best={best.get('adapter_id')}; net={as_float(best, 'validation_net'):.2f}; "
                f"dd={as_float(best, 'validation_dd_percent'):.4f}; mid_pf={as_float(best, 'validation_mid_pf'):.6f}; "
                f"late_share={as_float(best, 'validation_late_net_share'):.4f}"
            ),
            "guardrail": "no_more_risk_only_increase(위험만 추가 상향하지 않기)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "threshold_lift_nonbinding(문턱값 상향 비구속)",
            "bounded_question": "Do not repeat 0.55/0.53 threshold lift(문턱값 상향) without a new score surface(점수 표면).",
            "why": "threshold variants(문턱값 변형)는 reference(참조)와 KPI(핵심 성과 지표)가 같았다.",
            "guardrail": "do_not_hide_failed_branch(실패 분기 숨기지 않기)",
        },
    ]


def tradeoff_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | risk(위험) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {risk:.4f} | {net:.2f} | {dd:.4f} | {mid:.6f} | {late:.4f} | {oos_pf:.6f} | {read} |".format(
                adapter=row.get("adapter_id", ""),
                risk=as_float(row, "risk_pct_cap"),
                net=as_float(row, "validation_net"),
                dd=as_float(row, "validation_dd_percent"),
                mid=as_float(row, "validation_mid_pf"),
                late=as_float(row, "validation_late_net_share"),
                oos_pf=as_float(row, "oos_pf"),
                read=row.get("stage193_read", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    best = best_reference(tradeoff_rows)
    return f"""# Stage193 Follow-up Review(193단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage192_closeout_commit(원천 192단계 종료 커밋): `{SOURCE_STAGE192_CLOSEOUT_COMMIT}`
- source_stage192_hash_record_commit(원천 192단계 해시 기록 커밋): `{SOURCE_STAGE192_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

{tradeoff_table(tradeoff_rows)}

## Easy Read(쉬운 판독)

Stage192(192단계)는 중요한 단서를 만들었다. `s192_tp475_r0330`은 validation net(검증 순손익) `1021.45`, validation PF(검증 수익요인) `1.70`, validation DD(검증 낙폭) `12.7865%`로 34D(34D)의 큰 KPI(핵심 성과 지표) 세 축을 넘었다.

하지만 mid PF(중반 수익요인) `1.398279`와 late share(후반 비중) `0.5278`은 실패다. Effect(효과): 이 결과는 final adapter(최종 어댑터)가 아니라, net/DD(순손익/낙폭)를 살린 상태에서 mid/late(중반/후반)를 고칠 수 있다는 repair clue(수정 단서)다.

Threshold lift(문턱값 상향)는 결과를 바꾸지 않았다. Effect(효과): Stage194(194단계)는 같은 문턱값을 반복하지 않고 context/lifecycle/session(문맥/보유 생명주기/세션) 쪽으로 좁게 가야 한다.

## Best Remaining Reference(남은 최선 참조)

- reference_adapter(참조 어댑터): `{best.get("adapter_id", "none")}`
- validation_net(검증 순손익): `{as_float(best, "validation_net"):.2f}`
- validation_dd(검증 낙폭): `{as_float(best, "validation_dd_percent"):.4f}`
- validation_mid_pf(검증 중반 수익요인): `{as_float(best, "validation_mid_pf"):.6f}`
- validation_late_share(검증 후반 비중): `{as_float(best, "validation_late_net_share"):.4f}`

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): risk cap(위험 상한) 0.0330은 net/DD(순손익/낙폭)를 통과시켰지만, mid PF/late concentration(중반 수익요인/후반 집중)을 직접 고치지 못했다.
- effect(효과): Stage194(194단계)는 위험 상향을 반복하지 않고 late concentration/mid PF(후반 집중/중반 수익요인)만 좁게 수리한다.

Stage193(193단계)는 research/development only(연구개발 전용)입니다. Effect(효과): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않습니다.
"""


def decision_markdown() -> str:
    return f"""# Stage193 Decision(193단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage192_closeout_commit(원천 192단계 종료 커밋): `{SOURCE_STAGE192_CLOSEOUT_COMMIT}`
- source_stage192_hash_record_commit(원천 192단계 해시 기록 커밋): `{SOURCE_STAGE192_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage193(193단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage194(194단계)에서 `s192_tp475_r0330`의 net/DD(순손익/낙폭) 통과를 보존하면서 late concentration/mid PF(후반 집중/중반 수익요인)를 수리한다.
"""


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage194(194단계)는 `s192_tp475_r0330`을 reference(참조)로 두고 late concentration/mid PF(후반 집중/중반 수익요인)를 좁게 수리한다.

## Bounded Question(경계 질문)

Can Stage194(194단계) preserve validation net/PF/DD(검증 순손익/수익요인/낙폭) pass from `s192_tp475_r0330` while reducing late concentration(후반 집중) below 50% and improving mid PF(중반 수익요인), without another risk-only increase(위험만 추가 상향)?

Effect(효과): Stage192(192단계)의 좋은 net/DD(순손익/낙폭)를 잃지 않으면서 남은 품질 실패만 겨냥한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage194 Inputs(194단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage192_quality(원천 192단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage192_segment(원천 192단계 구간): `{rel(SOURCE_SEGMENT)}`
- source_stage192_probability(원천 192단계 확률 구속): `{rel(SOURCE_PROBABILITY)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage194 Review Index(194단계 검토 색인)

- status(상태): `open_planned_from_stage193`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage194 Selection Status(194단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage193`
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
        f"""# Stage193 Selection Status(193단계 선택 상태)

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
        f"""# Stage193 Review Index(193단계 검토 색인)

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
  Stage193(193단계) closed(종료) as `{DECISION}` and Stage194(194단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): `s192_tp475_r0330`의 net/DD(순손익/낙폭) 통과를 보존하면서 late concentration/mid PF(후반 집중/중반 수익요인)만 좁게 고친다.
- >-
  Stage193 evidence(193단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): Stage192(192단계)의 부분 성공과 남은 실패를 분리해 기록한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage193_stage192_tp475_midsegment_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage193_stage192_tp475_midsegment_followup_review:
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
- adapter_under_review(검토 중 어댑터): `stage194_tp475_late_concentration_midpf_repair`
- status(상태): `stage193_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage193(193단계)는 Stage192(192단계) TP4.75(익절 4.75) 수리 결과를 follow-up review(후속 검토)했다. Effect(효과): `s192_tp475_r0330`은 net/DD(순손익/낙폭) 통과 단서로 남기고, threshold lift(문턱값 상향)는 non-binding failure memory(비구속 실패 기억)로 남긴다.

## Latest Stage193 Evidence(최신 193단계 근거)

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
        f"\n## {utc_now()} Stage193 Stage192 TP4.75 follow-up review closeout(193단계 192단계 익절 4.75 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): `s192_tp475_r0330`을 net/DD(순손익/낙폭) 통과 단서로 보존하고 Stage194(194단계) late/mid repair(후반/중반 수정)로 넘겼다.\n"
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
                "lane": "baseline_adapter_stage193_stage192_tp475_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage192_closeout_commit", SOURCE_STAGE192_CLOSEOUT_COMMIT),
                        ("source_stage192_hash_record_commit", SOURCE_STAGE192_HASH_RECORD_COMMIT),
                        ("best_reference", best.get("adapter_id", "none")),
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
            "ledger_row_id": f"{RUN_ID}__stage192_tp475_midsegment_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage192_tp475_midsegment_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage192_tp475_net_dd_mid_late_tradeoff",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_reference", best.get("adapter_id", "none")),
                    ("validation_net", f"{as_float(best, 'validation_net'):.2f}"),
                    ("validation_dd", f"{as_float(best, 'validation_dd_percent'):.4f}"),
                    ("validation_mid_pf", f"{as_float(best, 'validation_mid_pf'):.6f}"),
                    ("validation_late_share", f"{as_float(best, 'validation_late_net_share'):.4f}"),
                )
            ),
            "guardrail_kpi": ledger_pairs((("claim_boundary", BOUNDARY), ("route_count", len(route_rows)), ("overall_goal_complete", 0))),
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage193 reviewed Stage192 TP4.75 midsegment recovery and opened Stage194 late/mid repair.",
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
                    "artifact_type": "stage193_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage193 Stage192 TP4.75 follow-up review evidence.",
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
        f"""# Stage193 Closeout Packet(193단계 종료 작업 묶음)

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
    probability_rows = load_csv(SOURCE_PROBABILITY)

    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, summary_rows, probability_rows)
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
