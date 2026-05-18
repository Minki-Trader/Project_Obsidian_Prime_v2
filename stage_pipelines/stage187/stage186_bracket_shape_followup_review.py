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

STAGE_ID = "187_adapter_research__stage186_bracket_shape_followup_review"
RUN_ID = "run187A_stage187_stage186_bracket_shape_followup_review_v1"
PACKET_ID = "stage187_stage186_bracket_shape_followup_review_v1"
PARENT_RUN_ID = "run186A_stage186_tp45_midwide_bracket_shape_repair_v1"
SOURCE_STAGE_ID = "186_adapter_research__tp45_midwide_bracket_shape_repair"
SOURCE_RUN_ID = "run186A_stage186_tp45_midwide_bracket_shape_repair_v1"
SOURCE_STAGE186_CLOSEOUT_COMMIT = "1f29877f8aa6151ea6f5eef7c74afa8cdfa2211b"
SOURCE_STAGE186_HASH_RECORD_COMMIT = "799809cf2b2bbd21ddc94b97fd883acd0f76f396"
NEXT_STAGE_ID = "188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff"
NEXT_RUN_ID = "run188A_stage188_v2_native_context_feature_branch_after_midwide_tradeoff_v1"
NEXT_PACKET_ID = "stage188_v2_native_context_feature_branch_after_midwide_tradeoff_v1"
DECISION = "open_stage188_v2_native_context_feature_branch_due_to_repeated_midwide_tradeoff_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_repair"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage186_mt5_reports_completed"

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

SOURCE_REPORT = Path("stages/186_adapter_research__tp45_midwide_bracket_shape_repair/03_reviews/stage186_bracket_shape_report.md")
SOURCE_QUALITY = Path("stages/186_adapter_research__tp45_midwide_bracket_shape_repair/03_reviews/stage186_quality_matrix.csv")
SOURCE_SEGMENT = Path("stages/186_adapter_research__tp45_midwide_bracket_shape_repair/03_reviews/stage186_segment_kpi_summary.csv")
SOURCE_BALANCE = Path("stages/186_adapter_research__tp45_midwide_bracket_shape_repair/03_reviews/stage186_balance_curve_audit.csv")
SOURCE_BRACKET = Path("stages/186_adapter_research__tp45_midwide_bracket_shape_repair/03_reviews/stage186_bracket_shape_summary.csv")
SOURCE_RISK_ATR = Path("stages/186_adapter_research__tp45_midwide_bracket_shape_repair/03_reviews/stage186_risk_atr_telemetry.csv")
SOURCE_DECISION = Path("stages/186_adapter_research__tp45_midwide_bracket_shape_repair/03_reviews/stage186_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage187_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage187_bracket_shape_tradeoff_matrix.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage187_route_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage187_failure_attribution.csv"
DECISION_PATH = REVIEWS_ROOT / "stage187_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage187/stage186_bracket_shape_followup_review.py")
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


def balance_lookup(balance_rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {
        (str(row.get("adapter_id", "")), str(row.get("split", ""))): row
        for row in balance_rows
    }


def route_read(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    if adapter_id == "s186_bctl":
        return "control_remains_near_miss_but_dd_and_mid_pf_fail"
    if adapter_id == "s186_tp425":
        return "take_profit_tightening_small_dd_help_net_below_34d"
    if adapter_id == "s186_sl195":
        return "stop_tightening_harms_net_and_mid_pf"
    if adapter_id == "s186_tp425_sl195":
        return "combined_tightening_over_compresses_edge"
    return "bracket_shape_unknown"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, str]],
    segment_rows: Sequence[Mapping[str, str]],
    balance_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    segments = segment_lookup(segment_rows)
    balances = balance_lookup(balance_rows)
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        early = segments.get((adapter_id, "early"), {})
        mid = segments.get((adapter_id, "mid"), {})
        late = segments.get((adapter_id, "late"), {})
        validation_balance = balances.get((adapter_id, "validation_is"), {})
        oos_balance = balances.get((adapter_id, "oos"), {})
        val_dd = as_float(row, "validation_balance_dd_percent")
        val_net = as_float(row, "validation_net")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "atr_stop_multiplier": row.get("atr_stop_multiplier", ""),
                "atr_take_profit_multiplier": row.get("atr_take_profit_multiplier", ""),
                "model_risk_max_pct": row.get("model_risk_max_pct", ""),
                "validation_pf": as_float(row, "validation_pf"),
                "validation_net": val_net,
                "validation_net_gap_vs_34d": val_net - LEGACY_34D["net_profit"],
                "validation_dd": val_dd,
                "validation_dd_gap_vs_34d": val_dd - LEGACY_34D["max_drawdown_percent"],
                "validation_early_pf": as_float(row, "validation_early_pf"),
                "validation_mid_pf": as_float(row, "validation_mid_pf"),
                "validation_late_pf": as_float(row, "validation_late_pf"),
                "validation_late_net_share": as_float(row, "validation_late_net_share"),
                "validation_mid_net": as_float(mid, "net_profit"),
                "validation_mid_mfe_capture": as_float(mid, "mfe_capture_ratio"),
                "validation_early_mfe_capture": as_float(early, "mfe_capture_ratio"),
                "validation_late_mfe_capture": as_float(late, "mfe_capture_ratio"),
                "validation_dd_amount": as_float(validation_balance, "max_drawdown_amount"),
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": as_float(row, "oos_net"),
                "oos_dd": as_float(row, "oos_balance_dd_percent"),
                "oos_dd_amount": as_float(oos_balance, "max_drawdown_amount"),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "route_read": route_read(row),
            }
        )
    return rows


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            as_float(row, "validation_pf") >= LEGACY_34D["profit_factor"],
            as_float(row, "validation_net") >= LEGACY_34D["net_profit"],
            as_float(row, "oos_pf"),
            -max(0.0, as_float(row, "validation_dd_gap_vs_34d")),
            as_float(row, "validation_mid_pf"),
        ),
    )


def build_route_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_row(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "route": "stage188_primary",
            "decision": DECISION,
            "source_clue": best.get("adapter_id", ""),
            "bounded_question": (
                "Can a v2-native context/feature branch(v2 고유 문맥/피처 분기) improve "
                "mid PF(중반 수익요인) and validation DD(검증 낙폭) without more same-surface "
                "bracket micro-tuning(같은 표면 브래킷 미세조정)?"
            ),
            "why": (
                "Stage184(184단계) entry gate(진입 게이트) and Stage186(186단계) bracket shape"
                "(브래킷 모양) both left the same mid PF/DD(중반 수익요인/낙폭) failure cluster."
            ),
            "guardrail": "do_not_keep_tuning_the_same_midwide_surface",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory",
            "decision": DECISION,
            "source_clue": "s186_tp425_sl195",
            "bounded_question": (
                "Preserve tighter TP/SL(더 좁은 익절/손절) as failure memory(실패 기억)."
            ),
            "why": (
                "It reduced some DD amount(낙폭 금액) but damaged validation net(검증 순손익), "
                "mid PF(중반 수익요인), and MFE capture(최대유리이동 포착)."
            ),
            "guardrail": "do_not_hide_failed_branch",
        },
        {
            "run_id": RUN_ID,
            "route": "reference_only",
            "decision": DECISION,
            "source_clue": "s186_bctl",
            "bounded_question": (
                "Keep the control(대조군) as a development reference(개발 참조) only."
            ),
            "why": (
                "It still has validation net/PF(검증 순손익/수익요인) and OOS(표본외) strength, "
                "but DD(낙폭) and mid PF(중반 수익요인) fail the 34D(34D) target."
            ),
            "guardrail": "not_final_not_baseline_not_runtime_authority",
        },
    ]


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows_by_id = {str(row.get("adapter_id", "")): row for row in tradeoff_rows}
    control = rows_by_id.get("s186_bctl", {})
    tp425 = rows_by_id.get("s186_tp425", {})
    sl195 = rows_by_id.get("s186_sl195", {})
    combo = rows_by_id.get("s186_tp425_sl195", {})
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "control(대조군)은 34D(34D) 순손익과 PF(수익요인)를 넘지만 DD(낙폭)와 mid PF(중반 수익요인)가 실패했다.",
            "likely_driver": "entry edge(진입 우위)는 남아 있으나 중반 구간의 trade shape(거래 모양)과 drawdown path(낙폭 경로)가 약하다.",
            "effect": "control(대조군)은 reference(참조)로 남기되 final(최종)로 보지 않는다.",
            "evidence": (
                f"adapter=s186_bctl; val_net={as_float(control, 'validation_net'):.2f}; "
                f"val_pf={as_float(control, 'validation_pf'):.4f}; "
                f"val_dd={as_float(control, 'validation_dd'):.4f}; "
                f"mid_pf={as_float(control, 'validation_mid_pf'):.6f}"
            ),
        },
        {
            "run_id": RUN_ID,
            "observed_change": "TP4.25(익절 4.25)는 DD(낙폭)를 조금 낮췄지만 net(순손익)을 34D(34D) 아래로 밀었다.",
            "likely_driver": "take-profit tightening(익절 축소)이 late winners(후반 수익 거래)를 자르면서 concentration(집중)과 mid weakness(중반 약점)를 해결하지 못했다.",
            "effect": "TP-only repair(익절 단독 수정)는 다음 주축이 아니다.",
            "evidence": (
                f"adapter=s186_tp425; val_net={as_float(tp425, 'validation_net'):.2f}; "
                f"val_dd={as_float(tp425, 'validation_dd'):.4f}; "
                f"mid_pf={as_float(tp425, 'validation_mid_pf'):.6f}; "
                f"late_share={as_float(tp425, 'validation_late_net_share'):.4f}"
            ),
        },
        {
            "run_id": RUN_ID,
            "observed_change": "SL1.95(손절 1.95)는 DD amount(낙폭 금액)을 줄였지만 PF(수익요인), net(순손익), MFE capture(최대유리이동 포착)를 훼손했다.",
            "likely_driver": "stop tightening(손절 축소)이 adverse move(불리한 이동)를 줄이기보다 valid recovery(유효 회복)를 잘랐다.",
            "effect": "SL compression(손절 압축)은 단독 해법으로 보지 않는다.",
            "evidence": (
                f"adapter=s186_sl195; val_net={as_float(sl195, 'validation_net'):.2f}; "
                f"val_dd={as_float(sl195, 'validation_dd'):.4f}; "
                f"mid_pf={as_float(sl195, 'validation_mid_pf'):.6f}; "
                f"mid_mfe_capture={as_float(sl195, 'validation_mid_mfe_capture'):.6f}"
            ),
        },
        {
            "run_id": RUN_ID,
            "observed_change": "TP4.25+SL1.95(익절 4.25+손절 1.95)는 가장 압축됐지만 KPI(핵심 성과 지표)가 가장 약해졌다.",
            "likely_driver": "bracket compression(브래킷 압축)이 edge capture(우위 포착)를 더 많이 깎았다.",
            "effect": "같은 midwide surface(중간넓은 표면)의 bracket micro-tuning(브래킷 미세조정)을 멈추고 Stage188(188단계)로 넘긴다.",
            "evidence": (
                f"adapter=s186_tp425_sl195; val_net={as_float(combo, 'validation_net'):.2f}; "
                f"val_pf={as_float(combo, 'validation_pf'):.4f}; "
                f"val_dd={as_float(combo, 'validation_dd'):.4f}; "
                f"mid_pf={as_float(combo, 'validation_mid_pf'):.6f}"
            ),
        },
    ]


def tradeoff_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | axis(축) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | mid MFE cap(중반 최대유리이동 포착) | OOS PF(표본외 수익요인) | route read(경로 판독) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {axis} | {validation_pf:.6f} | {validation_net:.2f} | {validation_dd:.4f} | {validation_mid_pf:.6f} | {validation_mid_mfe_capture:.6f} | {oos_pf:.6f} | {route_read} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    best = best_row(tradeoff_rows)
    return f"""# Stage187 Stage186 Bracket Shape Follow-up Review(187단계 186단계 브래킷 모양 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage186_closeout_commit(원천 186단계 종료 커밋): `{SOURCE_STAGE186_CLOSEOUT_COMMIT}`
- source_stage186_hash_record_commit(원천 186단계 해시 기록 커밋): `{SOURCE_STAGE186_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

{tradeoff_table(tradeoff_rows)}

## Easy Read(쉬운 판독)

Stage186(186단계)는 positive final-net story(최종 순손익 긍정 이야기)가 아닙니다. Control(대조군) `s186_bctl`만 validation net(검증 순손익)과 PF(수익요인)가 34D(34D)를 넘지만 validation DD(검증 낙폭)가 13.3347%로 34D(34D) 12.909136%보다 높고, validation mid PF(검증 중반 수익요인)는 1.485500으로 약합니다.

TP/SL tightening(익절/손절 축소)은 DD amount(낙폭 금액)을 조금 낮췄지만, net(순손익), mid PF(중반 수익요인), MFE capture(최대유리이동 포착)를 같이 깎았습니다. Effect(효과): 같은 midwide surface(중간넓은 표면)의 bracket micro-tuning(브래킷 미세조정)은 주축 repair(수정)로 계속 밀지 않습니다.

## Best Remaining Clue(남은 최선 단서)

- adapter(어댑터): `{best.get("adapter_id", "none")}`
- validation_net(검증 순손익): `{as_float(best, "validation_net"):.2f}`
- validation_pf(검증 수익요인): `{as_float(best, "validation_pf"):.6f}`
- validation_dd(검증 낙폭): `{as_float(best, "validation_dd"):.4f}`
- validation_mid_pf(검증 중반 수익요인): `{as_float(best, "validation_mid_pf"):.6f}`
- oos_pf(표본외 수익요인): `{as_float(best, "oos_pf"):.6f}`

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): Stage184(184단계) entry gate(진입 게이트)와 Stage186(186단계) bracket shape(브래킷 모양)가 같은 DD/mid PF(낙폭/중반 수익요인) 문제를 해결하지 못했다.
- effect(효과): Stage188(188단계)에서는 v2-native context/feature branch(v2 고유 문맥/피처 분기)로 표면을 바꿔, 같은 수치 미세조정 반복을 끊는다.

Stage187(187단계)는 research/development only(연구개발 전용)입니다. Effect(효과): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않습니다.
"""


def decision_markdown() -> str:
    return f"""# Stage187 Decision(187단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage186_closeout_commit(원천 186단계 종료 커밋): `{SOURCE_STAGE186_CLOSEOUT_COMMIT}`
- source_stage186_hash_record_commit(원천 186단계 해시 기록 커밋): `{SOURCE_STAGE186_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage187(187단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): 반복된 midwide bracket/entry tradeoff(중간넓은 브래킷/진입 상충)를 failure memory(실패 기억)로 보존하고, Stage188(188단계)에서 v2-native context/feature branch(v2 고유 문맥/피처 분기)를 좁게 측정한다.
"""


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage188(188단계)는 Stage184/186(184/186단계)의 repeated midwide tradeoff(반복된 중간넓은 표면 상충) 이후 v2-native context/feature branch(v2 고유 문맥/피처 분기)를 좁게 연다.

## Bounded Question(경계 질문)

Can a v2-native context/feature branch(v2 고유 문맥/피처 분기) improve validation DD(검증 낙폭), validation mid PF(검증 중반 수익요인), MFE capture(최대유리이동 포착), and validation/OOS consistency(검증/표본외 일관성) without copying legacy 34D(레거시 34D) method(방식)?

Effect(효과): 34D(34D)는 KPI target(핵심 성과 지표 목표)로만 쓰고, 개발 방식은 v2-native(브이투 고유)로 유지한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage188 Inputs(188단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- source_stage186_quality(원천 186단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage186_segment(원천 186단계 구간): `{rel(SOURCE_SEGMENT)}`
- source_stage186_balance(원천 186단계 잔고): `{rel(SOURCE_BALANCE)}`
- source_stage186_risk_atr(원천 186단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage188 Review Index(188단계 검토 색인)

- status(상태): `open_planned_from_stage187`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage188 Selection Status(188단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage187`
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
        f"""# Stage187 Selection Status(187단계 선택 상태)

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
        f"""# Stage187 Review Index(187단계 검토 색인)

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


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage187(187단계) closed(종료) as `{DECISION}` and Stage188(188단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage184/186(184/186단계)의 repeated midwide tradeoff(반복된 중간넓은 상충)를 멈추고 v2-native context/feature branch(v2 고유 문맥/피처 분기)로 이동한다.
- >-
  Stage187 evidence(187단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`에 있다. Effect(효과): bracket micro-tuning(브래킷 미세조정) 실패를 숨기지 않고 다음 stage(단계)의 질문을 좁힌다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 KPI target(핵심 성과 지표 목표)로만 쓴다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage187_stage186_bracket_shape_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage187_stage186_bracket_shape_followup_review:
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
  attribution_path: {rel(ATTRIBUTION_PATH)}
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
- adapter_under_review(검토 중 어댑터): `post_stage186_midwide_tradeoff_surface`
- status(상태): `stage187_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage187(187단계)는 Stage186(186단계) bracket/exit shape repair(브래킷/청산 모양 수정)를 follow-up review(후속 검토)했다. Effect(효과): tighter bracket(더 좁은 브래킷)이 34D(34D) KPI(핵심 성과 지표)를 넘기지 못한다는 failure memory(실패 기억)를 남기고, Stage188(188단계) v2-native context/feature branch(v2 고유 문맥/피처 분기)로 넘긴다.

## Latest Stage187 Evidence(최신 187단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- attribution(귀인): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage187 Stage186 bracket shape follow-up review closeout(187단계 186단계 브래킷 모양 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): bracket/exit shape repair(브래킷/청산 모양 수정)의 tradeoff(상충)를 기록하고 Stage188(188단계) v2-native context/feature branch(v2 고유 문맥/피처 분기)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = best_row(tradeoff_rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage187_stage186_bracket_shape_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage186_closeout_commit", SOURCE_STAGE186_CLOSEOUT_COMMIT),
                        ("source_stage186_hash_record_commit", SOURCE_STAGE186_HASH_RECORD_COMMIT),
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
            "ledger_row_id": f"{RUN_ID}__stage186_bracket_shape_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage186_bracket_shape_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage186_bracket_shape_followup_review",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best", best.get("adapter_id", "none")),
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
            "notes": "Stage187 reviewed Stage186 bracket shape tradeoff and opened Stage188 v2-native branch.",
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
    for path in (PRODUCER_PATH, REPORT_PATH, DECISION_PATH, TRADEOFF_MATRIX_PATH, ROUTE_MATRIX_PATH, ATTRIBUTION_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage187_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage187 Stage186 bracket shape follow-up review evidence.",
                }
            )
    return rows


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
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
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "attribution": rel(ATTRIBUTION_PATH),
        "tradeoff_rows": list(tradeoff_rows),
        "route_rows": list(route_rows),
        "attribution_rows": list(attribution_rows),
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
        f"""# Stage187 Closeout Packet(187단계 종료 작업 묶음)

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
    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, balance_rows)
    route_rows = build_route_rows(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)

    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_md(REPORT_PATH, report_markdown(tradeoff_rows))
    write_md(DECISION_PATH, decision_markdown())
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(tradeoff_rows, route_rows)
    artifacts_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, route_rows, attribution_rows, ledger_payload, artifacts_payload)

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
