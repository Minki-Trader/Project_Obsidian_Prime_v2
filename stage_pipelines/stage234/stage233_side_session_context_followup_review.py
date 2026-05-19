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


STAGE_ID = "234_adapter_research__stage233_side_session_context_followup_review"
RUN_ID = "run234A_stage234_stage233_side_session_context_followup_review_v1"
PACKET_ID = "stage234_stage233_side_session_context_followup_review_v1"
SOURCE_STAGE_ID = "233_adapter_research__side_session_context_repair_after_lifecycle_failure"
SOURCE_RUN_ID = "run233A_stage233_side_session_context_repair_after_lifecycle_failure_v1"
SOURCE_STAGE233_EVIDENCE_COMMIT = "971fdb5f65a8c0d8fcf5580b31cea61e4ee71e72"
SOURCE_STAGE233_HASH_RECORD_COMMIT = "2e8b2ca078326880f02501803f5f5b81583e3c94"
NEXT_STAGE_ID = "235_adapter_research__side_specific_validation_net_recovery_after_session_context_tradeoff"
NEXT_RUN_ID = "run235A_stage235_side_specific_validation_net_recovery_after_session_context_tradeoff_v1"
NEXT_PACKET_ID = "stage235_side_specific_validation_net_recovery_after_session_context_tradeoff_v1"
DECISION = "open_stage235_bounded_side_specific_validation_net_recovery_after_session_context_tradeoff_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage233_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_side_specific_validation_net_recovery_after_session_context_tradeoff"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}

OOS_REFERENCE = {
    "adapter_id": "s233_session_ref_h3_cd8",
    "oos_net": 719.48,
    "oos_pf": 1.74,
    "oos_dd": 9.2072,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage233_side_session_context_repair_report.md"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage233_quality_matrix.csv"
SOURCE_KPI_PATH = SOURCE_ROOT / "stage233_side_session_context_kpi_summary.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage233_segment_kpi_summary.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage233_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage233_concentration_risk_summary.csv"
SOURCE_DRAWDOWN_PATH = SOURCE_ROOT / "stage233_drawdown_recovery_summary.csv"
SOURCE_RISK_ATR_PATH = SOURCE_ROOT / "stage233_risk_atr_telemetry.csv"
SOURCE_GATE_PATH = SOURCE_ROOT / "stage233_gate_feature_summary.csv"
SOURCE_TRADE_AUDIT_PATH = SOURCE_ROOT / "stage233_trade_audit.csv"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage233_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage234_side_session_context_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage234_side_session_context_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage234_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage234_route_matrix.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage234_failure_memory.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage234_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage234_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage234/stage233_side_session_context_followup_review.py")

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


def classify_adapter(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    val_net = as_float(row.get("validation_net"))
    early_pf = as_float(row.get("validation_early_pf"))
    mid_pf = as_float(row.get("validation_mid_pf"))
    val_dd = as_float(row.get("validation_balance_dd_percent"), 99.0)
    oos_net = as_float(row.get("oos_net"))
    oos_pf = as_float(row.get("oos_pf"))
    oos_dd = as_float(row.get("oos_balance_dd_percent"), 99.0)

    validation_ok = (
        val_net >= LEGACY_34D["net_profit"]
        and early_pf >= LEGACY_34D["profit_factor"]
        and mid_pf >= LEGACY_34D["profit_factor"]
        and val_dd <= LEGACY_34D["max_drawdown_percent"]
    )
    oos_ref_ok = (
        oos_net >= OOS_REFERENCE["oos_net"]
        and oos_pf >= OOS_REFERENCE["oos_pf"]
        and oos_dd <= OOS_REFERENCE["oos_dd"]
    )
    if validation_ok and oos_ref_ok:
        return "dual_objective_pass_candidate_not_final"
    if adapter_id in {"s233_session_ref_h3_cd8", "s233_session_p10_h3_cd8"} and oos_ref_ok:
        return "oos_preserved_validation_under_34d"
    if adapter_id == "s233_session_p5_h3_cd8":
        return "session_p5_damages_midpf_oos_net_and_late_concentration"
    if adapter_id == "s233_cashopen_long_h3_cd8":
        return "cashopen_midpf_dd_clue_but_net_oos_damage"
    return "mixed_tradeoff_no_full_repair"


def risk_present(risk_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> bool:
    validation = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
    oos = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
    return (
        as_bool(validation.get("atr_enabled"))
        and as_bool(validation.get("model_risk_enabled"))
        and as_bool(oos.get("atr_enabled"))
        and as_bool(oos.get("model_risk_enabled"))
    )


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        validation_trade = lookup(trade_rows, variant_id=adapter_id, split="validation_is")
        oos_trade = lookup(trade_rows, variant_id=adapter_id, split="oos")
        review_class = classify_adapter(row)
        val_net = as_float(row.get("validation_net"))
        early_pf = as_float(row.get("validation_early_pf"))
        mid_pf = as_float(row.get("validation_mid_pf"))
        oos_net = as_float(row.get("oos_net"))
        oos_pf = as_float(row.get("oos_pf"))
        oos_dd = as_float(row.get("oos_balance_dd_percent"))
        rows.append(
            {
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_net": val_net,
                "validation_net_gap_vs_34d": round(val_net - LEGACY_34D["net_profit"], 6),
                "validation_pf": as_float(row.get("validation_pf")),
                "validation_early_pf": early_pf,
                "validation_early_pf_gap_vs_34d": round(early_pf - LEGACY_34D["profit_factor"], 9),
                "validation_mid_pf": mid_pf,
                "validation_mid_pf_gap_vs_34d": round(mid_pf - LEGACY_34D["profit_factor"], 9),
                "validation_balance_dd_percent": as_float(row.get("validation_balance_dd_percent")),
                "oos_net": oos_net,
                "oos_net_gap_vs_reference": round(oos_net - OOS_REFERENCE["oos_net"], 6),
                "oos_pf": oos_pf,
                "oos_pf_gap_vs_reference": round(oos_pf - OOS_REFERENCE["oos_pf"], 9),
                "oos_balance_dd_percent": oos_dd,
                "oos_dd_margin_vs_reference": round(OOS_REFERENCE["oos_dd"] - oos_dd, 6),
                "validation_late_net_share": as_float(row.get("validation_late_net_share")),
                "oos_late_net_share": as_float(row.get("oos_late_net_share")),
                "validation_mfe_capture_ratio": as_float(validation_trade.get("mfe_capture_ratio")),
                "oos_mfe_capture_ratio": as_float(oos_trade.get("mfe_capture_ratio")),
                "atr_model_risk_present": risk_present(risk_rows, adapter_id),
                "quality_flags": row.get("quality_flags", ""),
                "review_class": review_class,
                "hard_quality_pass": as_bool(row.get("hard_quality_pass")),
            }
        )
    return rows


def best_oos_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [
        row for row in rows if str(row.get("review_class", "")) == "oos_preserved_validation_under_34d"
    ]
    if not candidates:
        candidates = list(rows)
    return max(candidates, key=lambda row: (as_float(row.get("oos_net")), as_float(row.get("oos_pf"))))


def best_repair_clue(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [
        row for row in rows if str(row.get("review_class", "")) == "cashopen_midpf_dd_clue_but_net_oos_damage"
    ]
    if not candidates:
        candidates = list(rows)
    return max(
        candidates,
        key=lambda row: (
            as_float(row.get("validation_mid_pf")),
            -as_float(row.get("validation_balance_dd_percent")),
            as_float(row.get("oos_pf")),
        ),
    )


def build_attribution_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = lookup(rows, adapter_id="s233_session_ref_h3_cd8")
    p10 = lookup(rows, adapter_id="s233_session_p10_h3_cd8")
    p5 = lookup(rows, adapter_id="s233_session_p5_h3_cd8")
    cashopen = lookup(rows, adapter_id="s233_cashopen_long_h3_cd8")
    return [
        {
            "finding": "session_ref_and_p10_are_effectively_no_gain",
            "evidence": ledger_pairs(
                [
                    ("ref_validation_net", ref.get("validation_net", "")),
                    ("p10_validation_net", p10.get("validation_net", "")),
                    ("ref_oos_net", ref.get("oos_net", "")),
                    ("p10_oos_net", p10.get("oos_net", "")),
                ]
            ),
            "interpretation": "session_p10(세션 10분 변형)은 기준 세션과 같은 KPI(핵심 성과 지표)라 새 수리축으로 보기 어렵다.",
            "next_use": "Do not repeat session_p10 no-op(효과 없는 반복) as Stage235(235단계).",
            "confidence": "high",
        },
        {
            "finding": "session_p5_widens_but_damages_midpf_and_oos",
            "evidence": ledger_pairs(
                [
                    ("validation_net", p5.get("validation_net", "")),
                    ("validation_mid_pf", p5.get("validation_mid_pf", "")),
                    ("oos_net", p5.get("oos_net", "")),
                    ("validation_late_share", p5.get("validation_late_net_share", "")),
                ]
            ),
            "interpretation": "session_p5(세션 5분 변형)은 넓혔지만 validation mid PF(검증 중반 수익요인), OOS net(표본외 순손익), late concentration(후반 집중)을 악화했다.",
            "next_use": "Do not widen the long session gate(롱 세션 게이트) in this form.",
            "confidence": "high",
        },
        {
            "finding": "cashopen_is_a_midpf_clue_not_a_package",
            "evidence": ledger_pairs(
                [
                    ("validation_mid_pf", cashopen.get("validation_mid_pf", "")),
                    ("validation_dd", cashopen.get("validation_balance_dd_percent", "")),
                    ("oos_pf", cashopen.get("oos_pf", "")),
                    ("validation_net", cashopen.get("validation_net", "")),
                    ("oos_net", cashopen.get("oos_net", "")),
                    ("oos_dd", cashopen.get("oos_balance_dd_percent", "")),
                ]
            ),
            "interpretation": "cashopen(현금장 초반)은 mid PF(중반 수익요인)와 DD(낙폭) 단서를 주지만 validation net(검증 순손익), early PF(초반 수익요인), OOS net/DD(표본외 순손익/낙폭)를 훼손했다.",
            "next_use": "Use cashopen as a guarded clue(보호 단서), not as the whole adapter(전체 어댑터).",
            "confidence": "high",
        },
        {
            "finding": "atr_and_model_risk_remain_present_but_not_sufficient",
            "evidence": "All Stage233 variants retained ATR SL/TP(ATR 손절/익절) and model-controlled risk%(모델 제어 위험 비율).",
            "interpretation": "mandatory capability(필수 기능)는 유지됐지만 KPI(핵심 성과 지표) 통과 조건은 아니다.",
            "next_use": "Keep ATR/risk fixed while Stage235(235단계) repairs side-specific validation net(방향별 검증 순손익).",
            "confidence": "high",
        },
    ]


def build_route_rows(best_ref: Mapping[str, Any], best_clue: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "route": DECISION,
            "action": "Open Stage235(235단계) as bounded side-specific validation net recovery(방향별 검증 순손익 회복).",
            "effect": "Stage233(233단계)의 cashopen mid PF clue(현금장 초반 중반 수익요인 단서)를 보존하되 OOS reference bound(표본외 기준 경계)를 깨지 않는지 시험한다.",
            "oos_reference_bound": best_ref.get("adapter_id", ""),
            "repair_clue": best_clue.get("adapter_id", ""),
            "risk": "The clue may reduce trade supply(거래 공급) or raise OOS drawdown(표본외 낙폭).",
        },
        {
            "route": "do_not_repeat_session_p5_or_p10_as_primary_axis",
            "action": "Preserve p5/p10 evidence as failure/no-op memory(실패/무효 반복 기억).",
            "effect": "Stage235(235단계)가 같은 세션 폭 조절을 반복하지 않는다.",
            "oos_reference_bound": best_ref.get("adapter_id", ""),
            "repair_clue": "",
            "risk": "Ignoring the failure memory would create another broad stage(넓어진 단계).",
        },
    ]


def build_failure_memory(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "failure_id": f"{RUN_ID}__session_p5_damage",
            "hypothesis": "Slightly wider long session gate(조금 넓은 롱 세션 게이트) can recover validation net/PF(검증 순손익/수익요인).",
            "why_failed": "It lowered validation net and mid PF, worsened OOS net, and pushed validation late share above 50%.",
            "salvage_value": "It proves simple widening is not the next repair axis.",
            "reopen_condition": "Only reopen if a side-specific model or separate early-window guard changes the trade source.",
            "do_not_repeat": "Do not rerun p5/p10 session-width-only repair.",
        },
        {
            "failure_id": f"{RUN_ID}__cashopen_not_package",
            "hypothesis": "Cash-open long context(현금장 초반 롱 문맥) can solve mid PF(중반 수익요인) and OOS(표본외) together.",
            "why_failed": "It improved mid PF and DD but damaged validation net, early PF, OOS net, and OOS DD.",
            "salvage_value": "Use as a narrow clue for side-specific validation recovery.",
            "reopen_condition": "Reopen only as a guarded subcomponent with OOS reference bound enforced.",
            "do_not_repeat": "Do not use cashopen-only long gate as a full package.",
        },
    ]


def report_markdown(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in tradeoff_rows:
        lines.append(
            "| {adapter} | {klass} | {val:.2f} | {early:.6f} | {mid:.6f} | {oos:.2f} | {oos_pf:.6f} | {oos_dd:.4f} |".format(
                adapter=row.get("adapter_id", ""),
                klass=row.get("review_class", ""),
                val=as_float(row.get("validation_net")),
                early=as_float(row.get("validation_early_pf")),
                mid=as_float(row.get("validation_mid_pf")),
                oos=as_float(row.get("oos_net")),
                oos_pf=as_float(row.get("oos_pf")),
                oos_dd=as_float(row.get("oos_balance_dd_percent")),
            )
        )
    attribution = "\n".join(
        f"- {row['finding']}: {row['interpretation']} Effect(효과): {row['next_use']}"
        for row in attribution_rows
    )
    routes = "\n".join(f"- {row['route']}: {row['action']} Effect(효과): {row['effect']}" for row in route_rows)
    return f"""# Stage234 Side/Session/Context Follow-up Review(234단계 방향/세션/문맥 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage233_evidence_commit(원천 233단계 근거 커밋): `{SOURCE_STAGE233_EVIDENCE_COMMIT}`
- source_stage233_hash_record_commit(원천 233단계 해시 기록 커밋): `{SOURCE_STAGE233_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 설명)

Stage233(233단계)는 34D KPI(핵심 성과 지표)에 못 닿았다. session_ref(세션 기준)는 OOS(표본외)를 지키지만 validation early/mid PF(검증 초반/중반 수익요인)가 낮고, cashopen(현금장 초반)은 mid PF(중반 수익요인) 단서만 주며 net/OOS(순손익/표본외)를 훼손했다.

Effect(효과): Stage235(235단계)는 세션 폭 조절을 반복하지 않고, side-specific validation net recovery(방향별 검증 순손익 회복)를 좁게 시험한다.

## KPI Read(KPI 핵심 성과 지표 판독)

{chr(10).join(lines)}

## Attribution(성과 원인 분해)

{attribution}

## Route(다음 경로)

{routes}

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
"""


def decision_markdown(best_ref: Mapping[str, Any], best_clue: Mapping[str, Any]) -> str:
    return f"""# Stage234 Decision(234단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage233_evidence_commit(원천 233단계 근거 커밋): `{SOURCE_STAGE233_EVIDENCE_COMMIT}`
- source_stage233_hash_record_commit(원천 233단계 해시 기록 커밋): `{SOURCE_STAGE233_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- repair_clue(수리 단서): `{best_clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage234(234단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage235(235단계)가 `s233_session_ref_h3_cd8`의 OOS(표본외) 보존 경계를 지키면서 `s233_cashopen_long_h3_cd8`의 mid PF(중반 수익요인) 단서를 방향별로 좁게 시험한다.
"""


def write_stage235_seed(best_ref: Mapping[str, Any], best_clue: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage235(235단계)는 Stage234(234단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can side-specific validation net recovery(방향별 검증 순손익 회복) use the cashopen mid PF clue(현금장 초반 중반 수익요인 단서) without losing the OOS reference bound(표본외 기준 경계) from `{best_ref.get('adapter_id', '')}`?

Effect(효과): Stage233(233단계)의 session_p5/session_p10(세션 5분/10분) 반복을 피하고, 검증 순손익과 초반 수익요인을 좁게 복구한다.

## Fixed Requirements(고정 요구)

- OOS reference bound(표본외 기준 경계): `{best_ref.get('adapter_id', '')}`.
- cashopen clue(현금장 초반 단서): `{best_clue.get('adapter_id', '')}`.
- model-controlled risk%(모델 제어 위험 비율) remains mandatory(필수 유지).
- ATR SL/TP(ATR 손절/익절) remains mandatory(필수 유지).
- no ONNX hardening(ONNX 경화 없음).
- no deployment/live/production/operating claim(배포/실거래/생산/운영 주장 없음).

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage235 Inputs(235단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- oos_reference_bound(표본외 기준 경계): `{best_ref.get('adapter_id', '')}`
- cashopen_clue(현금장 초반 단서): `{best_clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage235 Review Index(235단계 검토 색인)

- status(상태): `open_planned_from_stage234`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage235 Selection Status(235단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage234`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(best_ref: Mapping[str, Any], best_clue: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^\ufeff?current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage234(234단계) closed(종료) as `{DECISION}` and Stage235(235단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage233(233단계)의 session/context(세션/문맥) 상충을 side-specific validation net recovery(방향별 검증 순손익 회복)로 좁힌다.
- >-
  Stage234 evidence(234단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): 세션 폭 반복과 cashopen-only(현금장 초반 단독) 반복을 막는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage234_stage233_side_session_context_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage235_side_specific_validation_net_recovery_after_session_context_tradeoff:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage234_stage233_side_session_context_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  oos_reference_bound: {best_ref.get('adapter_id', '')}
  repair_clue: {best_clue.get('adapter_id', '')}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  failure_memory_path: {rel(FAILURE_MEMORY_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage235_side_specific_validation_net_recovery_after_session_context_tradeoff:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage234
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  oos_reference_bound: {best_ref.get('adapter_id', '')}
  repair_clue: {best_clue.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `side_specific_validation_net_recovery_after_session_context_tradeoff`
- status(상태): `stage234_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage234(234단계)는 Stage233(233단계) side/session/context repair(방향/세션/문맥 수리)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage235(235단계)가 검증 순손익/초반 수익요인 회복을 방향별로 좁게 시험한다.

## Latest Stage234 Evidence(최신 234단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- repair_clue(수리 단서): `{best_clue.get('adapter_id', '')}`
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
        f"""# Stage234 Selection Status(234단계 선택 상태)

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
        f"""# Stage234 Review Index(234단계 검토 색인)

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
        f"\n## {utc_now()} Stage234 side/session/context follow-up review closeout(234단계 방향/세션/문맥 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage233(233단계)의 세션/현금장 상충을 Stage235(235단계) 방향별 검증 순손익 회복으로 넘겼다.\n"
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
                    "artifact_type": "stage234_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage234 Stage233 side/session/context follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(best_ref: Mapping[str, Any], best_clue: Mapping[str, Any]) -> dict[str, Any]:
    primary = ledger_pairs(
        [
            ("oos_reference_bound", best_ref.get("adapter_id", "")),
            ("oos_reference_net", best_ref.get("oos_net", "")),
            ("repair_clue", best_clue.get("adapter_id", "")),
            ("repair_clue_mid_pf", best_clue.get("validation_mid_pf", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage234_role", "review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage234_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage234_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage233_side_session_context_followup_review(233단계 방향/세션/문맥 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage234 review-only closeout; not final and not deployment.",
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
                    ("repair_clue", best_clue.get("adapter_id", "")),
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
    best_clue: Mapping[str, Any],
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
        "repair_clue": best_clue.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": list(tradeoff_rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "failure_memory": list(failure_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "result_judgment_gate.json": {
            **base_payload,
            "judgment_label": "negative_side_session_context_repair_axis_candidate_not_final",
            "next_condition": "Stage235 must recover validation net and early PF without losing OOS reference bound.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Cashopen improved mid PF but damaged net/OOS; session width changes were no-op or damaging.",
            "comparison_baseline": "Stage233 session reference versus p5, p10, and cashopen long context variants",
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
        f"""# Stage234 Closeout Packet(234단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- repair_clue(수리 단서): `{best_clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def run() -> Mapping[str, Any]:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    trade_rows = read_csv(SOURCE_TRADE_AUDIT_PATH)

    tradeoff_rows = build_tradeoff_rows(quality_rows, risk_rows, trade_rows)
    best_ref = best_oos_reference(tradeoff_rows)
    best_clue = best_repair_clue(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows(best_ref, best_clue)
    failure_rows = build_failure_memory(tradeoff_rows)

    write_md(REPORT_PATH, report_markdown(tradeoff_rows, attribution_rows, route_rows))
    write_csv(TRADEOFF_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(DECISION_PATH, decision_markdown(best_ref, best_clue))
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
            "source_trade_audit": rel(SOURCE_TRADE_AUDIT_PATH),
            "tradeoff_rows": tradeoff_rows,
            "attribution_rows": attribution_rows,
            "route_rows": route_rows,
            "failure_memory": failure_rows,
            "oos_reference_bound": best_ref,
            "repair_clue": best_clue,
            "legacy_34d": LEGACY_34D,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_stage235_seed(best_ref, best_clue)
    update_current_truth(best_ref, best_clue)
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(best_ref, best_clue)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(
        tradeoff_rows,
        attribution_rows,
        route_rows,
        failure_rows,
        best_ref,
        best_clue,
        {**ledger_payload, "artifact_registry": artifact_payload},
    )
    return {
        "status": "reviewed_closed",
        "run_id": RUN_ID,
        "decision": DECISION,
        "oos_reference_bound": best_ref.get("adapter_id", ""),
        "repair_clue": best_clue.get("adapter_id", ""),
        "report": rel(REPORT_PATH),
        "next_stage": NEXT_STAGE_ID,
        "overall_goal_complete": False,
    }


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
