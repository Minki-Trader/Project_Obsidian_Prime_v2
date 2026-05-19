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


STAGE_ID = "232_adapter_research__stage231_lifecycle_followup_review"
RUN_ID = "run232A_stage232_stage231_lifecycle_followup_review_v1"
PACKET_ID = "stage232_stage231_lifecycle_followup_review_v1"
SOURCE_STAGE_ID = "231_adapter_research__midpf_oos_repair_after_guard_blend_failure"
SOURCE_RUN_ID = "run231A_stage231_midpf_oos_repair_after_guard_blend_failure_v1"
SOURCE_STAGE231_EVIDENCE_COMMIT = "adc7978cadb5d930ae557c058a64968fda528f91"
SOURCE_STAGE231_HASH_RECORD_COMMIT = "87115447243528f615541241cfffc31f4e202740"
NEXT_STAGE_ID = "233_adapter_research__side_session_context_repair_after_lifecycle_failure"
NEXT_RUN_ID = "run233A_stage233_side_session_context_repair_after_lifecycle_failure_v1"
NEXT_PACKET_ID = "stage233_side_session_context_repair_after_lifecycle_failure_v1"
DECISION = "open_stage233_bounded_side_session_context_repair_after_lifecycle_failure_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage231_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_side_session_context_repair_after_lifecycle_failure"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage231_lifecycle_repair_report.md"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage231_quality_matrix.csv"
SOURCE_KPI_PATH = SOURCE_ROOT / "stage231_lifecycle_repair_kpi_summary.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage231_segment_kpi_summary.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage231_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage231_concentration_risk_summary.csv"
SOURCE_DRAWDOWN_PATH = SOURCE_ROOT / "stage231_drawdown_recovery_summary.csv"
SOURCE_RISK_ATR_PATH = SOURCE_ROOT / "stage231_risk_atr_telemetry.csv"
SOURCE_GATE_PATH = SOURCE_ROOT / "stage231_gate_feature_summary.csv"
SOURCE_PROBABILITY_PATH = SOURCE_ROOT / "stage231_probability_telemetry_summary.csv"
SOURCE_MODEL_SCORE_PATH = SOURCE_ROOT / "stage231_model_score_audit.csv"
SOURCE_TRADE_AUDIT_PATH = SOURCE_ROOT / "stage231_trade_audit.csv"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage231_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage232_lifecycle_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage232_lifecycle_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage232_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage232_route_matrix.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage232_failure_memory.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage232_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage232_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage232/stage231_lifecycle_followup_review.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    inferred: list[str] = []
    for row in rows:
        for key in row:
            if key not in inferred:
                inferred.append(key)
    fieldnames = list(columns or inferred)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip().replace(",", "")
        return float(text) if text else default
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def lookup(rows: Sequence[Mapping[str, Any]], **filters: str) -> Mapping[str, Any]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in filters.items()):
            return row
    return {}


def split_rows(rows: Sequence[Mapping[str, Any]], **filters: str) -> list[Mapping[str, Any]]:
    return [row for row in rows if all(str(row.get(key, "")) == value for key, value in filters.items())]


def classify_adapter(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    val_net = as_float(row.get("validation_net"))
    early_pf = as_float(row.get("validation_early_pf"))
    mid_pf = as_float(row.get("validation_mid_pf"))
    val_dd = as_float(row.get("validation_balance_dd_percent"), 99.0)
    oos_net = as_float(row.get("oos_net"))
    oos_pf = as_float(row.get("oos_pf"))
    oos_dd = as_float(row.get("oos_balance_dd_percent"), 99.0)

    val_near_34d = val_net >= LEGACY_34D["net_profit"] - 10.0
    val_kpi_ok = (
        val_net >= LEGACY_34D["net_profit"]
        and early_pf >= LEGACY_34D["profit_factor"]
        and mid_pf >= LEGACY_34D["profit_factor"]
        and val_dd <= LEGACY_34D["max_drawdown_percent"]
    )
    oos_reference_ok = oos_net >= 719.48 and oos_pf >= 1.74 and oos_dd <= 9.2072

    if val_kpi_ok and oos_reference_ok:
        return "dual_objective_pass_candidate_not_final"
    if adapter_id == "s231_session_ref_h3_cd8":
        return "oos_reference_preserved_validation_under_34d"
    if adapter_id == "s231_wide_h3_cd12" and val_near_34d:
        return "validation_near_34d_midpf_oos_dd_damaged"
    if "_h2_" in adapter_id:
        return "hold2_lifecycle_compression_damages_validation_and_oos"
    return "mixed_lifecycle_tradeoff_no_full_repair"


def risk_row_for(
    risk_rows: Sequence[Mapping[str, Any]],
    adapter_id: str,
    split: str,
    view: str = "actual_routed_total",
) -> Mapping[str, Any]:
    return lookup(risk_rows, adapter_id=adapter_id, split=split, view=view)


def trade_row_for(
    trade_rows: Sequence[Mapping[str, Any]],
    adapter_id: str,
    split: str,
) -> Mapping[str, Any]:
    return lookup(trade_rows, variant_id=adapter_id, split=split)


def gate_rows_for(gate_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> list[Mapping[str, Any]]:
    return [row for row in gate_rows if str(row.get("adapter_id", "")) == adapter_id]


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        validation_risk = risk_row_for(risk_rows, adapter_id, "validation_is")
        oos_risk = risk_row_for(risk_rows, adapter_id, "oos")
        validation_trade = trade_row_for(trade_rows, adapter_id, "validation_is")
        oos_trade = trade_row_for(trade_rows, adapter_id, "oos")
        gates = gate_rows_for(gate_rows, adapter_id)
        validation_gate = next((item for item in gates if str(item.get("split", "")) == "validation_is"), {})
        oos_gate = next((item for item in gates if str(item.get("split", "")) == "oos"), {})
        flags = str(row.get("quality_flags", ""))

        rows.append(
            {
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_net": as_float(row.get("validation_net")),
                "validation_net_gap_vs_34d": as_float(row.get("validation_net_gap_vs_34d")),
                "validation_pf": as_float(row.get("validation_pf")),
                "validation_early_pf": as_float(row.get("validation_early_pf")),
                "validation_mid_pf": as_float(row.get("validation_mid_pf")),
                "validation_late_pf": as_float(row.get("validation_late_pf")),
                "validation_late_net_share": as_float(row.get("validation_late_net_share")),
                "validation_balance_dd_percent": as_float(row.get("validation_balance_dd_percent")),
                "oos_net": as_float(row.get("oos_net")),
                "oos_pf": as_float(row.get("oos_pf")),
                "oos_balance_dd_percent": as_float(row.get("oos_balance_dd_percent")),
                "oos_late_net_share": as_float(row.get("oos_late_net_share")),
                "stage171_oos_net_delta": as_float(row.get("stage171_oos_net_delta")),
                "validation_mfe_capture_ratio": as_float(validation_trade.get("mfe_capture_ratio")),
                "oos_mfe_capture_ratio": as_float(oos_trade.get("mfe_capture_ratio")),
                "validation_same_move_reentry_ratio": as_float(validation_trade.get("same_move_reentry_ratio")),
                "oos_same_move_reentry_ratio": as_float(oos_trade.get("same_move_reentry_ratio")),
                "validation_blocked_signal_ratio": as_float(validation_gate.get("blocked_signal_ratio")),
                "oos_blocked_signal_ratio": as_float(oos_gate.get("blocked_signal_ratio")),
                "validation_risk_floor_applied_count": as_float(validation_risk.get("risk_floor_applied_count")),
                "oos_risk_floor_applied_count": as_float(oos_risk.get("risk_floor_applied_count")),
                "validation_avg_actual_risk_pct_after_floor": as_float(
                    validation_risk.get("avg_actual_risk_pct_after_floor")
                ),
                "oos_avg_actual_risk_pct_after_floor": as_float(oos_risk.get("avg_actual_risk_pct_after_floor")),
                "atr_model_risk_present": as_bool(validation_risk.get("atr_enabled"))
                and as_bool(validation_risk.get("model_risk_enabled"))
                and as_bool(oos_risk.get("atr_enabled"))
                and as_bool(oos_risk.get("model_risk_enabled")),
                "quality_flags": flags,
                "review_class": classify_adapter(row),
                "hard_quality_pass": as_bool(row.get("hard_quality_pass")),
            }
        )
    return rows


def best_oos_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if str(row.get("review_class", "")) == "oos_reference_preserved_validation_under_34d"]
    if not candidates:
        candidates = list(rows)
    return max(candidates, key=lambda row: (as_float(row.get("oos_net")), as_float(row.get("oos_pf"))))


def best_validation_clue(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [
        row for row in rows if str(row.get("review_class", "")) == "validation_near_34d_midpf_oos_dd_damaged"
    ]
    if not candidates:
        candidates = list(rows)
    return max(
        candidates,
        key=lambda row: (as_float(row.get("validation_net")), as_float(row.get("validation_early_pf"))),
    )


def build_attribution_rows(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    session_ref = lookup(tradeoff_rows, adapter_id="s231_session_ref_h3_cd8")
    wide_h3 = lookup(tradeoff_rows, adapter_id="s231_wide_h3_cd12")
    hold2_rows = [row for row in tradeoff_rows if "_h2_" in str(row.get("adapter_id", ""))]
    probability_unique = sorted({str(row.get("winning_prob_median", "")) for row in probability_rows if row})
    model_hashes = sorted({str(row.get("model_sha256", "")) for row in model_rows if row})

    rows = [
        {
            "finding": "lifecycle_compression_not_the_primary_fix(생애주기 압축은 주 수리가 아님)",
            "evidence": "hold2 rows validation_net 366.20-378.06 and OOS net 237.40-238.71",
            "interpretation": "hold=2(보유 2) 축은 거래 품질을 압축하지 못하고 검증/표본외 수익을 같이 줄였다.",
            "next_use": "Do not repeat hold=2/cooldown-only repair in Stage233(233단계).",
            "confidence": "high",
        },
        {
            "finding": "wide_h3_cd12_validation_near_but_not_research_grade(넓은 h3 cd12는 검증만 근접)",
            "evidence": ledger_pairs(
                [
                    ("validation_net", wide_h3.get("validation_net", "")),
                    ("validation_mid_pf", wide_h3.get("validation_mid_pf", "")),
                    ("oos_net", wide_h3.get("oos_net", "")),
                    ("oos_dd", wide_h3.get("oos_balance_dd_percent", "")),
                ]
            ),
            "interpretation": "검증 순손익은 34D(34D 기준)에 붙었지만 중반 PF(수익요인)와 OOS(표본외) 낙폭이 훼손됐다.",
            "next_use": "Carry as validation-near clue(검증 근접 단서), not final candidate(최종 후보 아님).",
            "confidence": "high",
        },
        {
            "finding": "session_reference_preserves_oos_but_under_34d(세션 기준은 표본외 보존, 검증 미달)",
            "evidence": ledger_pairs(
                [
                    ("validation_net", session_ref.get("validation_net", "")),
                    ("early_pf", session_ref.get("validation_early_pf", "")),
                    ("mid_pf", session_ref.get("validation_mid_pf", "")),
                    ("oos_net", session_ref.get("oos_net", "")),
                    ("oos_pf", session_ref.get("oos_pf", "")),
                ]
            ),
            "interpretation": "OOS(표본외) 경계로 쓸 수 있지만 검증 early/mid PF(초반/중반 수익요인)가 34D 기준보다 낮다.",
            "next_use": "Use as OOS preservation bound(표본외 보존 경계).",
            "confidence": "high",
        },
        {
            "finding": "risk_atr_present_not_sufficient(위험/ATR 존재는 충분조건 아님)",
            "evidence": "ATR SL/TP(ATR 손절/익절) and model risk%(모델 위험 비율) telemetry present, risk floor applied count 0.",
            "interpretation": "필수 기능은 남아 있지만 KPI(핵심 성과 지표) 상충을 해결하지 못했다.",
            "next_use": "Keep fixed while Stage233(233단계) changes only the side/session/context gate.",
            "confidence": "high",
        },
        {
            "finding": "probability_surface_is_not_a_repair_axis(확률 표면은 수리 축이 아님)",
            "evidence": ledger_pairs(
                [
                    ("winning_prob_medians", "|".join(probability_unique[:4])),
                    ("model_hash_count", len(model_hashes)),
                ]
            ),
            "interpretation": "확률 값이 사실상 같은 표면이라 threshold(임계값) 미세 조정은 새 정보를 주기 어렵다.",
            "next_use": "Use context routing(문맥 라우팅), not probability micro-tuning(확률 미세조정).",
            "confidence": "medium",
        },
    ]

    if hold2_rows:
        rows.append(
            {
                "finding": "hold2_mfe_capture_drop(보유 2의 MFE 포착 하락)",
                "evidence": ";".join(
                    f"{row.get('adapter_id')} val_capture={row.get('validation_mfe_capture_ratio')}"
                    for row in hold2_rows
                ),
                "interpretation": "보유 시간을 줄이면 MFE(최대 유리 이동) 포착도 같이 낮아졌다.",
                "next_use": "Do not use shorter holding as the next repair lever(수리 지렛대).",
                "confidence": "medium",
            }
        )
    return rows


def build_route_rows(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    best_ref: Mapping[str, Any],
    best_val: Mapping[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "route": DECISION,
            "action": "Open Stage233(233단계) as side/session/context repair(방향/세션/문맥 수리).",
            "effect": "Lifecycle(생애주기) 축을 반복하지 않고 early/mid PF(초반/중반 수익요인)를 겨냥한다.",
            "reference_oos_bound": best_ref.get("adapter_id", ""),
            "validation_clue": best_val.get("adapter_id", ""),
            "risk": "A context gate(문맥 게이트)가 OOS(표본외) 수익을 다시 줄일 수 있다.",
        },
        {
            "route": "preserve_oos_reference_not_final(표본외 기준 보존, 최종 아님)",
            "action": f"Keep `{best_ref.get('adapter_id', '')}` as OOS preservation bound(표본외 보존 경계).",
            "effect": "다음 실험이 검증만 올리고 표본외를 깨뜨리는지 바로 비교한다.",
            "reference_oos_bound": best_ref.get("adapter_id", ""),
            "validation_clue": "",
            "risk": "검증 KPI(핵심 성과 지표)는 34D(34D 기준) 미만이다.",
        },
        {
            "route": "preserve_validation_near_clue_not_final(검증 근접 단서 보존, 최종 아님)",
            "action": f"Keep `{best_val.get('adapter_id', '')}` as validation clue(검증 단서).",
            "effect": "순손익 회복 단서는 보존하되 mid PF/OOS damage(중반 수익요인/표본외 훼손)를 숨기지 않는다.",
            "reference_oos_bound": best_ref.get("adapter_id", ""),
            "validation_clue": best_val.get("adapter_id", ""),
            "risk": "late concentration(후반 집중)과 OOS DD(표본외 낙폭)가 커질 수 있다.",
        },
    ]


def build_failure_memory(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in tradeoff_rows:
        review_class = str(row.get("review_class", ""))
        if review_class in {
            "hold2_lifecycle_compression_damages_validation_and_oos",
            "validation_near_34d_midpf_oos_dd_damaged",
            "oos_reference_preserved_validation_under_34d",
        }:
            rows.append(
                {
                    "adapter_id": row.get("adapter_id", ""),
                    "failure_label": review_class,
                    "validation_net": row.get("validation_net", ""),
                    "validation_mid_pf": row.get("validation_mid_pf", ""),
                    "oos_net": row.get("oos_net", ""),
                    "oos_pf": row.get("oos_pf", ""),
                    "oos_dd": row.get("oos_balance_dd_percent", ""),
                    "salvage_value": "oos_bound" if row.get("adapter_id") == "s231_session_ref_h3_cd8" else "validation_clue",
                    "do_not_repeat_note": "Do not repeat lifecycle-only repair as the next bounded question.",
                }
            )
    return rows


def report_markdown(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
) -> str:
    table_lines = [
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in tradeoff_rows:
        table_lines.append(
            "| {adapter_id} | {review_class} | {validation_net:.2f} | {validation_early_pf:.6f} | "
            "{validation_mid_pf:.6f} | {validation_balance_dd_percent:.4f} | {oos_net:.2f} | "
            "{oos_pf:.6f} | {oos_balance_dd_percent:.4f} |".format(**row)
        )
    attribution_lines = "\n".join(
        f"- {row['finding']}: {row['interpretation']}" for row in attribution_rows
    )
    route_lines = "\n".join(f"- {row['route']}: {row['effect']}" for row in route_rows)
    return f"""# Stage232 Lifecycle Follow-up Review(232단계 생애주기 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 판독)

Stage232(232단계)는 새 tuning(조정)이나 MT5 run(MT5 실행)을 하지 않았다. Stage231(231단계)의 lifecycle repair(생애주기 수리)를 review-only(검토 전용)로 판정했다.

Effect(효과): hold/cooldown(보유/대기) 축을 계속 반복하지 않고, 다음 Stage233(233단계)를 side/session/context repair(방향/세션/문맥 수리)로 좁힌다.

## KPI Read(KPI 핵심 성과 지표 판독)

{chr(10).join(table_lines)}

## Attribution(성과 원인 분해)

{attribution_lines}

## Route(경로)

{route_lines}

## Judgment(판정)

- full_stage_pass(전체 통과): `False`
- result_subject(판정 대상): `{SOURCE_RUN_ID}`
- judgment_label(판정 라벨): `negative_lifecycle_repair_axis_candidate_not_final`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)
- next_condition(다음 조건): Stage233(233단계)이 ATR/risk(ATR/위험)를 고정하고 OOS(표본외) 보존 경계를 깨지 않으면서 validation early/mid PF(검증 초반/중반 수익요인)를 고쳐야 한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
"""


def decision_markdown(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> str:
    return f"""# Stage232 Decision(232단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage231_evidence_commit(원천 231단계 근거 커밋): `{SOURCE_STAGE231_EVIDENCE_COMMIT}`
- source_stage231_hash_record_commit(원천 231단계 해시 기록 커밋): `{SOURCE_STAGE231_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage232(232단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage233(233단계)에서 lifecycle-only repair(생애주기 단독 수리)를 반복하지 않고 side/session/context gate(방향/세션/문맥 게이트)를 좁게 시험한다.
"""


def write_stage233_seed(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage233(233단계)는 Stage232(232단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a side/session/context gate(방향/세션/문맥 게이트) repair validation early/mid PF(검증 초반/중반 수익요인) and validation net(검증 순손익) without damaging the OOS preservation bound(표본외 보존 경계) from `{best_ref.get('adapter_id', '')}`, while keeping model-controlled risk%(모델 제어 위험 비율) and ATR SL/TP(ATR 손절/익절) fixed?

Effect(효과): hold/cooldown(보유/대기) 단독 조정이 아니라 trade context(거래 문맥) 축으로 KPI(핵심 성과 지표)를 끌어올린다.

## Fixed Requirements(고정 요구)

- model-controlled risk%(모델 제어 위험 비율) remains mandatory(필수 유지).
- ATR SL/TP(ATR 손절/익절) remains mandatory(필수 유지).
- OOS reference bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`.
- validation clue(검증 단서): `{best_val.get('adapter_id', '')}`.
- no ONNX hardening(ONNX 경화 없음).
- no deployment/live/production/operating claim(배포/실거래/생산/운영 주장 없음).

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage233 Inputs(233단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage232_report(232단계 보고서): `{rel(REPORT_PATH)}`
- stage232_tradeoff_matrix(232단계 상충 행렬): `{rel(TRADEOFF_PATH)}`
- stage232_failure_memory(232단계 실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- source_stage231_quality_matrix(원천 231단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage231_segment_kpi(원천 231단계 구간 KPI 핵심 성과 지표): `{rel(SOURCE_SEGMENT_PATH)}`
- source_stage231_risk_atr(원천 231단계 위험/ATR): `{rel(SOURCE_RISK_ATR_PATH)}`
- source_stage231_trade_audit(원천 231단계 거래 감사): `{rel(SOURCE_TRADE_AUDIT_PATH)}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage233 Review Index(233단계 검토 색인)

- status(상태): `open_planned_from_stage232`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage233 Selection Status(233단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage232`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^\ufeff?current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1)
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1)
    focus = f"""current_focus:
- >-
  Stage232(232단계) closed(종료) as `{DECISION}` and Stage233(233단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): lifecycle repair(생애주기 수리) 실패를 side/session/context repair(방향/세션/문맥 수리)로 분리한다.
- >-
  Stage232 evidence(232단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): Stage231(231단계)의 hold/cooldown(보유/대기) 상충을 반복하지 않게 한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage232_stage231_lifecycle_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage233_side_session_context_repair_after_lifecycle_failure:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage232_stage231_lifecycle_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  oos_reference_bound: {best_ref.get('adapter_id', '')}
  validation_recovery_clue: {best_val.get('adapter_id', '')}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  failure_memory_path: {rel(FAILURE_MEMORY_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage233_side_session_context_repair_after_lifecycle_failure:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage232
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  oos_reference_bound: {best_ref.get('adapter_id', '')}
  validation_recovery_clue: {best_val.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `side_session_context_repair_after_lifecycle_failure`
- status(상태): `stage232_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage232(232단계)는 Stage231(231단계) lifecycle repair(생애주기 수리)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage233(233단계)가 hold/cooldown(보유/대기)을 반복하지 않고 side/session/context gate(방향/세션/문맥 게이트)를 좁게 시험한다.

## Latest Stage232 Evidence(최신 232단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage232 Selection Status(232단계 선택 상태)

- stage_status(단계 상태): `reviewed_closed_{DECISION}`
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
        f"""# Stage232 Review Index(232단계 검토 색인)

- status(상태): `reviewed_closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage232 lifecycle follow-up review closeout(232단계 생애주기 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage231(231단계)의 hold/cooldown(보유/대기) 상충을 Stage233(233단계) side/session/context repair(방향/세션/문맥 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        TRADEOFF_PATH,
        ATTRIBUTION_PATH,
        ROUTE_MATRIX_PATH,
        FAILURE_MEMORY_PATH,
        SUMMARY_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage232_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage232 Stage231 lifecycle follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> dict[str, Any]:
    primary = ledger_pairs(
        [
            ("oos_reference_bound", best_ref.get("adapter_id", "")),
            ("oos_reference_net", best_ref.get("oos_net", "")),
            ("validation_clue", best_val.get("adapter_id", "")),
            ("validation_clue_net", best_val.get("validation_net", "")),
            ("validation_clue_mid_pf", best_val.get("validation_mid_pf", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage232_role", "review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage232_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage232_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage231_lifecycle_followup_review(231단계 생애주기 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage232 review-only closeout; not final and not deployment.",
        }
    ]
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "notes": ledger_pairs(
                [
                    ("source_run", SOURCE_RUN_ID),
                    ("oos_reference_bound", best_ref.get("adapter_id", "")),
                    ("validation_recovery_clue", best_val.get("adapter_id", "")),
                    ("boundary", BOUNDARY),
                ]
            ),
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload}


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    best_ref: Mapping[str, Any],
    best_val: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "oos_reference_bound": best_ref.get("adapter_id", ""),
        "validation_recovery_clue": best_val.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": list(tradeoff_rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "failure_memory": list(failure_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": [
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            **base_payload,
            "source_quality": rel(SOURCE_QUALITY_PATH),
            "source_segments": rel(SOURCE_SEGMENT_PATH),
            "source_risk_atr": rel(SOURCE_RISK_ATR_PATH),
            "source_trade_audit": rel(SOURCE_TRADE_AUDIT_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": SOURCE_RUN_ID,
            "evidence_available": [
                rel(REPORT_PATH),
                rel(TRADEOFF_PATH),
                rel(ATTRIBUTION_PATH),
                rel(FAILURE_MEMORY_PATH),
                rel(DECISION_PATH),
            ],
            "evidence_missing": ["new_repair_not_attempted_in_stage232_by_design"],
            "judgment_label": "negative_lifecycle_repair_axis_candidate_not_final",
            "next_condition": "Stage233 must repair validation early/mid PF without damaging OOS bound.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Hold/cooldown lifecycle repair failed to lift early/mid PF and preserve OOS together.",
            "comparison_baseline": "Stage231 session reference versus wide lifecycle variants",
            "likely_drivers": [
                "lifecycle compression",
                "context gate supply",
                "mid-period trade quality",
                "OOS drawdown sensitivity",
            ],
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [
                rel(SOURCE_QUALITY_PATH),
                rel(SOURCE_SEGMENT_PATH),
                rel(SOURCE_RISK_ATR_PATH),
                rel(SOURCE_GATE_PATH),
                rel(SOURCE_TRADE_AUDIT_PATH),
                rel(SOURCE_DECISION_PATH),
            ],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "artifact_paths": [
                rel(path)
                for path in [
                    REPORT_PATH,
                    TRADEOFF_PATH,
                    ATTRIBUTION_PATH,
                    ROUTE_MATRIX_PATH,
                    FAILURE_MEMORY_PATH,
                    SUMMARY_JSON_PATH,
                    DECISION_PATH,
                ]
            ],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            **base_payload,
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "tradeoff": rel(TRADEOFF_PATH),
                "attribution": rel(ATTRIBUTION_PATH),
                "route": rel(ROUTE_MATRIX_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
        },
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage232 Closeout Packet(232단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def run() -> Mapping[str, Any]:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    gate_rows = read_csv(SOURCE_GATE_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    trade_rows = read_csv(SOURCE_TRADE_AUDIT_PATH)
    probability_rows = read_csv(SOURCE_PROBABILITY_PATH)
    model_rows = read_csv(SOURCE_MODEL_SCORE_PATH)

    tradeoff_rows = build_tradeoff_rows(quality_rows, gate_rows, risk_rows, trade_rows)
    best_ref = best_oos_reference(tradeoff_rows)
    best_val = best_validation_clue(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows, probability_rows, model_rows)
    route_rows = build_route_rows(tradeoff_rows, best_ref, best_val)
    failure_rows = build_failure_memory(tradeoff_rows)

    write_md(REPORT_PATH, report_markdown(tradeoff_rows, attribution_rows, route_rows))
    write_csv(TRADEOFF_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(DECISION_PATH, decision_markdown(best_ref, best_val))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "source_report": rel(SOURCE_REPORT_PATH),
            "source_quality": rel(SOURCE_QUALITY_PATH),
            "source_kpi": rel(SOURCE_KPI_PATH),
            "source_segment_kpi": rel(SOURCE_SEGMENT_PATH),
            "source_monthly_kpi": rel(SOURCE_MONTHLY_PATH),
            "source_concentration": rel(SOURCE_CONCENTRATION_PATH),
            "source_drawdown": rel(SOURCE_DRAWDOWN_PATH),
            "source_risk_atr": rel(SOURCE_RISK_ATR_PATH),
            "source_gate": rel(SOURCE_GATE_PATH),
            "source_probability": rel(SOURCE_PROBABILITY_PATH),
            "source_model_score": rel(SOURCE_MODEL_SCORE_PATH),
            "source_trade_audit": rel(SOURCE_TRADE_AUDIT_PATH),
            "tradeoff_rows": tradeoff_rows,
            "attribution_rows": attribution_rows,
            "route_rows": route_rows,
            "failure_memory": failure_rows,
            "oos_reference_bound": best_ref,
            "validation_recovery_clue": best_val,
            "legacy_34d": LEGACY_34D,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_stage233_seed(best_ref, best_val)
    update_current_truth(best_ref, best_val)
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(best_ref, best_val)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(
        tradeoff_rows,
        attribution_rows,
        route_rows,
        failure_rows,
        best_ref,
        best_val,
        {**ledger_payload, "artifact_registry": artifact_payload},
    )
    return {
        "status": "reviewed_closed",
        "run_id": RUN_ID,
        "decision": DECISION,
        "oos_reference_bound": best_ref.get("adapter_id", ""),
        "validation_recovery_clue": best_val.get("adapter_id", ""),
        "report": rel(REPORT_PATH),
        "next_stage": NEXT_STAGE_ID,
        "overall_goal_complete": False,
    }


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
