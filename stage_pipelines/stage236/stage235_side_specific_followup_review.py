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


STAGE_ID = "236_adapter_research__stage235_side_specific_followup_review"
RUN_ID = "run236A_stage236_stage235_side_specific_followup_review_v1"
PACKET_ID = "stage236_stage235_side_specific_followup_review_v1"
SOURCE_STAGE_ID = "235_adapter_research__side_specific_validation_net_recovery_after_session_context_tradeoff"
SOURCE_RUN_ID = "run235A_stage235_side_specific_validation_net_recovery_after_session_context_tradeoff_v1"
SOURCE_STAGE235_EVIDENCE_COMMIT = "2402dd0bb96c946c485253ae241f71eac61709be"
SOURCE_STAGE235_HASH_RECORD_COMMIT = "deec8b78c2adb1baf0f239a82e750359be22de93"
NEXT_STAGE_ID = "237_adapter_research__reference_micro_threshold_recovery_after_context_side_failure"
NEXT_RUN_ID = "run237A_stage237_reference_micro_threshold_recovery_after_context_side_failure_v1"
NEXT_PACKET_ID = "stage237_reference_micro_threshold_recovery_after_context_side_failure_v1"
DECISION = "open_stage237_bounded_reference_micro_threshold_recovery_after_context_side_failure_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage235_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_reference_micro_threshold_recovery_after_context_side_failure"
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
    "adapter_id": "s235_session_ref_h3_cd8",
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
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage235_side_specific_recovery_report.md"
SOURCE_KPI_PATH = SOURCE_ROOT / "stage235_side_specific_kpi_summary.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage235_segment_kpi_summary.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage235_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage235_concentration_risk_summary.csv"
SOURCE_DRAWDOWN_PATH = SOURCE_ROOT / "stage235_drawdown_recovery_summary.csv"
SOURCE_RISK_ATR_PATH = SOURCE_ROOT / "stage235_risk_atr_telemetry.csv"
SOURCE_GATE_PATH = SOURCE_ROOT / "stage235_gate_feature_summary.csv"
SOURCE_TRADE_AUDIT_PATH = SOURCE_ROOT / "stage235_trade_audit.csv"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage235_quality_matrix.csv"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage235_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage236_side_specific_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage236_side_specific_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage236_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage236_route_matrix.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage236_failure_memory.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage236_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage236_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage236/stage235_side_specific_followup_review.py")

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


def risk_present(risk_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> bool:
    validation = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
    oos = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
    return (
        as_bool(validation.get("atr_enabled"))
        and as_bool(validation.get("model_risk_enabled"))
        and as_bool(oos.get("atr_enabled"))
        and as_bool(oos.get("model_risk_enabled"))
    )


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
    if adapter_id == "s235_session_ref_h3_cd8" and oos_ref_ok:
        return "oos_preserved_small_validation_gap_reference"
    if adapter_id == "s235_cashopen45_h3_cd8":
        return "cashopen45_earlypf_clue_but_midpf_net_oos_damage"
    if adapter_id == "s235_session_ref_short_open_h3_cd8":
        return "short_block_off_severe_damage"
    if adapter_id == "s235_cashopen45_short_open_h3_cd8":
        return "cashopen45_short_open_severe_damage"
    return "mixed_tradeoff_no_full_repair"


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
                "short_block_rule": row.get("short_block_rule", ""),
                "validation_net": val_net,
                "validation_net_gap_vs_34d": round(val_net - LEGACY_34D["net_profit"], 6),
                "validation_pf": as_float(row.get("validation_pf")),
                "validation_early_pf": early_pf,
                "validation_early_pf_gap_vs_34d": round(early_pf - LEGACY_34D["profit_factor"], 9),
                "validation_mid_pf": mid_pf,
                "validation_mid_pf_gap_vs_34d": round(mid_pf - LEGACY_34D["profit_factor"], 9),
                "validation_balance_dd_percent": as_float(row.get("validation_balance_dd_percent")),
                "validation_dd_margin_vs_34d": as_float(row.get("validation_dd_margin_vs_34d")),
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
                "validation_same_move_reentry_ratio": as_float(validation_trade.get("same_move_reentry_ratio")),
                "oos_same_move_reentry_ratio": as_float(oos_trade.get("same_move_reentry_ratio")),
                "atr_model_risk_present": risk_present(risk_rows, adapter_id),
                "quality_flags": row.get("quality_flags", ""),
                "review_class": classify_adapter(row),
                "hard_quality_pass": as_bool(row.get("hard_quality_pass")),
            }
        )
    return rows


def pick_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    ref = lookup(rows, adapter_id=OOS_REFERENCE["adapter_id"])
    return ref or (rows[0] if rows else {})


def pick_clue(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    clue = lookup(rows, adapter_id="s235_cashopen45_h3_cd8")
    return clue or (rows[0] if rows else {})


def build_attribution_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = lookup(rows, adapter_id="s235_session_ref_h3_cd8")
    cashopen = lookup(rows, adapter_id="s235_cashopen45_h3_cd8")
    short_open = lookup(rows, adapter_id="s235_session_ref_short_open_h3_cd8")
    cash_short = lookup(rows, adapter_id="s235_cashopen45_short_open_h3_cd8")
    return [
        {
            "finding": "reference_preserves_oos_but_misses_small_validation_gaps",
            "evidence": ledger_pairs(
                [
                    ("validation_net_gap", ref.get("validation_net_gap_vs_34d", "")),
                    ("early_pf_gap", ref.get("validation_early_pf_gap_vs_34d", "")),
                    ("mid_pf_gap", ref.get("validation_mid_pf_gap_vs_34d", "")),
                    ("oos_net", ref.get("oos_net", "")),
                    ("oos_pf", ref.get("oos_pf", "")),
                    ("oos_dd", ref.get("oos_balance_dd_percent", "")),
                ]
            ),
            "interpretation": "기준형은 OOS(표본외)를 보존하지만 34D(34D 기준) 대비 검증 순손익, 초반 PF(수익요인), 중반 PF(수익요인)가 조금 모자란다.",
            "next_use": "Stage237(237단계)은 기준형 주변의 작은 threshold(문턱값) 또는 rank-confidence(순위 신뢰도)만 시험한다.",
            "confidence": "high",
        },
        {
            "finding": "cashopen45_is_earlypf_clue_not_package",
            "evidence": ledger_pairs(
                [
                    ("early_pf_gap", cashopen.get("validation_early_pf_gap_vs_34d", "")),
                    ("mid_pf_gap", cashopen.get("validation_mid_pf_gap_vs_34d", "")),
                    ("validation_net_gap", cashopen.get("validation_net_gap_vs_34d", "")),
                    ("oos_net_gap_vs_ref", cashopen.get("oos_net_gap_vs_reference", "")),
                    ("oos_dd_margin_vs_ref", cashopen.get("oos_dd_margin_vs_reference", "")),
                ]
            ),
            "interpretation": "cashopen45(현금장 초반 45분)는 초반 PF(수익요인)만 좋아졌고 검증 순손익, 중반 PF(수익요인), OOS(표본외)를 훼손했다.",
            "next_use": "cashopen45(현금장 초반 45분)를 전체 package(묶음)로 반복하지 않는다.",
            "confidence": "high",
        },
        {
            "finding": "short_block_off_is_hard_failure",
            "evidence": ledger_pairs(
                [
                    ("short_open_validation_net", short_open.get("validation_net", "")),
                    ("short_open_pf", short_open.get("validation_pf", "")),
                    ("cash_short_validation_net", cash_short.get("validation_net", "")),
                    ("cash_short_oos_net", cash_short.get("oos_net", "")),
                ]
            ),
            "interpretation": "short block off(숏 차단 해제)는 거래 수를 늘렸지만 PF(수익요인), 순손익, DD(낙폭)를 크게 망가뜨렸다.",
            "next_use": "short block off(숏 차단 해제)는 Stage237(237단계)에서 재사용하지 않는다.",
            "confidence": "high",
        },
        {
            "finding": "mandatory_atr_and_model_risk_present_but_not_sufficient",
            "evidence": "Stage235(235단계) 후보들은 ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)를 유지했다.",
            "interpretation": "필수 기능은 살아 있지만 KPI(핵심 성과 지표) 통과 조건은 아니다.",
            "next_use": "Stage237(237단계)에서도 ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)는 고정 필수 조건으로 둔다.",
            "confidence": "high",
        },
    ]


def build_route_rows(reference: Mapping[str, Any], clue: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "route": DECISION,
            "action": "Stage237(237단계)을 열어 기준형 주변의 micro threshold(미세 문턱값)와 rank-confidence(순위 신뢰도)를 좁게 시험한다.",
            "effect": "검증 순손익과 초반/중반 PF(수익요인)의 작은 부족분을 회복하되 OOS(표본외) 기준 경계는 보존하는지 확인한다.",
            "reference_adapter": reference.get("adapter_id", ""),
            "clue_adapter": clue.get("adapter_id", ""),
            "risk": "작은 조정도 OOS(표본외) 거래 밀도나 DD(낙폭)를 망가뜨릴 수 있다.",
        },
        {
            "route": "do_not_repeat_failed_context_or_side_axes",
            "action": "cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 축을 반복하지 않는다.",
            "effect": "Stage237(237단계)이 Stage235(235단계) 실패 축을 다시 흡수하지 않고 한 질문만 답하게 한다.",
            "reference_adapter": reference.get("adapter_id", ""),
            "clue_adapter": "",
            "risk": "실패 기억을 무시하면 단계(stage, 단계)가 다시 비대해진다.",
        },
    ]


def build_failure_memory(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cashopen = lookup(rows, adapter_id="s235_cashopen45_h3_cd8")
    short_open = lookup(rows, adapter_id="s235_session_ref_short_open_h3_cd8")
    cash_short = lookup(rows, adapter_id="s235_cashopen45_short_open_h3_cd8")
    return [
        {
            "failure_id": f"{RUN_ID}__cashopen45_package_damage",
            "hypothesis": "cashopen45(현금장 초반 45분)가 validation(검증) 초반 PF(수익요인)를 올리면 전체 KPI(핵심 성과 지표)도 회복될 수 있다.",
            "why_failed": ledger_pairs(
                [
                    ("validation_net_gap", cashopen.get("validation_net_gap_vs_34d", "")),
                    ("mid_pf_gap", cashopen.get("validation_mid_pf_gap_vs_34d", "")),
                    ("oos_net_gap_vs_ref", cashopen.get("oos_net_gap_vs_reference", "")),
                    ("oos_dd_margin_vs_ref", cashopen.get("oos_dd_margin_vs_reference", "")),
                ]
            ),
            "salvage_value": "초반 PF(수익요인) 단서만 보존한다.",
            "reopen_condition": "별도 모델 축이 바뀌기 전에는 package(묶음)로 재개하지 않는다.",
            "do_not_repeat": "cashopen45(현금장 초반 45분) 단독 package(묶음)를 반복하지 않는다.",
        },
        {
            "failure_id": f"{RUN_ID}__short_block_off_damage",
            "hypothesis": "short block off(숏 차단 해제)가 검증 순손익 부족을 거래 공급으로 회복할 수 있다.",
            "why_failed": ledger_pairs(
                [
                    ("short_open_validation_net", short_open.get("validation_net", "")),
                    ("short_open_oos_dd", short_open.get("oos_balance_dd_percent", "")),
                    ("cash_short_validation_net", cash_short.get("validation_net", "")),
                    ("cash_short_oos_dd", cash_short.get("oos_balance_dd_percent", "")),
                ]
            ),
            "salvage_value": "숏 차단은 보호 역할을 한다는 실패 기억을 남긴다.",
            "reopen_condition": "side-specific model(방향별 모델)을 새로 만들 때만 별도 Stage(단계)에서 재검토한다.",
            "do_not_repeat": "Stage237(237단계)에서 short block off(숏 차단 해제)를 반복하지 않는다.",
        },
        {
            "failure_id": f"{RUN_ID}__context_side_axes_exhausted_for_now",
            "hypothesis": "세션/현금장/방향 차단 축 조합으로 34D(34D 기준) 이상 KPI(핵심 성과 지표)를 바로 회복할 수 있다.",
            "why_failed": "기준형만 OOS(표본외)를 보존했고 다른 축은 validation/OOS(검증/표본외) 한쪽 또는 양쪽을 훼손했다.",
            "salvage_value": "기준형 주변의 작은 threshold(문턱값) 조정으로 다음 범위를 좁힌다.",
            "reopen_condition": "Stage237(237단계) 이후에도 작은 조정이 실패하면 새 bounded repair(경계 수리)에서 별도 판정한다.",
            "do_not_repeat": "넓은 세션/현금장/숏 차단 실험을 Stage237(237단계)에 섞지 않는다.",
        },
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
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
    return "\n".join(lines)


def report_markdown(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
) -> str:
    attribution = "\n".join(
        f"- {row['finding']}: {row['interpretation']} Effect(효과): {row['next_use']}"
        for row in attribution_rows
    )
    routes = "\n".join(
        f"- {row['route']}: {row['action']} Effect(효과): {row['effect']}"
        for row in route_rows
    )
    return f"""# Stage236 Side-Specific Follow-up Review(236단계 방향별 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage235_evidence_commit(원천 235단계 근거 커밋): `{SOURCE_STAGE235_EVIDENCE_COMMIT}`
- source_stage235_hash_record_commit(원천 235단계 해시 기록 커밋): `{SOURCE_STAGE235_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 설명)

Stage235(235단계)는 기준형 `s235_session_ref_h3_cd8`가 OOS(표본외)를 가장 잘 보존한다는 점을 확인했다. 하지만 34D(34D 기준) 대비 validation net(검증 순손익) `-35.44`, early PF(초반 수익요인) `-0.019452852`, mid PF(중반 수익요인) `-0.041963145`가 남았다.

cashopen45(현금장 초반 45분)는 early PF(초반 수익요인)만 좋아졌고, short block off(숏 차단 해제)는 크게 망가졌다.

Effect(효과): Stage237(237단계)은 새 큰 사냥이 아니라 기준형 주변의 작은 threshold(문턱값)/rank-confidence(순위 신뢰도) 조정만 본다.

## KPI Read(KPI 핵심 성과 지표 판독)

{markdown_table(tradeoff_rows)}

## Attribution(성과 원인 분해)

{attribution}

## Route(다음 경로)

{routes}

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
"""


def decision_markdown(reference: Mapping[str, Any], clue: Mapping[str, Any]) -> str:
    return f"""# Stage236 Decision(236단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage235_evidence_commit(원천 235단계 근거 커밋): `{SOURCE_STAGE235_EVIDENCE_COMMIT}`
- source_stage235_hash_record_commit(원천 235단계 해시 기록 커밋): `{SOURCE_STAGE235_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- reference_adapter(기준 어댑터): `{reference.get('adapter_id', '')}`
- clue_adapter(단서 어댑터): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage236(236단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage237(237단계)이 `s235_session_ref_h3_cd8` 기준형의 작은 validation(검증) 부족분을 micro threshold(미세 문턱값)/rank-confidence(순위 신뢰도)로만 시험하고, cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제)는 반복하지 않게 한다.
"""


def write_stage237_seed(reference: Mapping[str, Any], clue: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage237(237단계)은 Stage236(236단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a very small threshold/rank-confidence adjustment(미세 문턱값/순위 신뢰도 조정) around `{reference.get('adapter_id', '')}` recover validation net/early PF/mid PF(검증 순손익/초반 수익요인/중반 수익요인) to 34D(34D 기준) without damaging OOS net/PF/DD(표본외 순손익/수익요인/낙폭), ATR SL/TP(ATR 손절/익절), and model-controlled risk%(모델 제어 위험 비율)?

Effect(효과): Stage235(235단계)의 cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 실패 축을 반복하지 않고 작은 부족분만 겨냥한다.

## Fixed Requirements(고정 요구)

- reference_adapter(기준 어댑터): `{reference.get('adapter_id', '')}`.
- clue_adapter(단서 어댑터): `{clue.get('adapter_id', '')}` is clue-only(단서 전용), not package(묶음 아님).
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
        f"""# Stage237 Inputs(237단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- reference_adapter(기준 어댑터): `{reference.get('adapter_id', '')}`
- clue_adapter(단서 어댑터): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage237 Review Index(237단계 검토 색인)

- status(상태): `open_planned_from_stage236`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage237 Selection Status(237단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage236`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(reference: Mapping[str, Any], clue: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^\ufeff?current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage236(236단계) closed(종료) as `{DECISION}` and Stage237(237단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): 기준형 주변의 micro threshold(미세 문턱값)/rank-confidence(순위 신뢰도)만 시험한다.
- >-
  Stage236 evidence(236단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 실패 축을 반복하지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage236_stage235_side_specific_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage237_reference_micro_threshold_recovery_after_context_side_failure:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage236_stage235_side_specific_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  reference_adapter: {reference.get('adapter_id', '')}
  clue_adapter: {clue.get('adapter_id', '')}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  failure_memory_path: {rel(FAILURE_MEMORY_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage237_reference_micro_threshold_recovery_after_context_side_failure:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage236
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  reference_adapter: {reference.get('adapter_id', '')}
  clue_adapter: {clue.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `stage236_reference_micro_threshold_recovery_after_context_side_failure`
- status(상태): `stage236_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage236(236단계)는 Stage235(235단계) side-specific validation net recovery(방향별 검증 순손익 회복)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage237(237단계)이 기준형 주변의 작은 threshold/rank-confidence(문턱값/순위 신뢰도)만 시험한다.

## Latest Stage236 Evidence(최신 236단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- reference_adapter(기준 어댑터): `{reference.get('adapter_id', '')}`
- clue_adapter(단서 어댑터): `{clue.get('adapter_id', '')}`
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
        f"""# Stage236 Selection Status(236단계 선택 상태)

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
        f"""# Stage236 Review Index(236단계 검토 색인)

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
        f"\n## {utc_now()} Stage236 side-specific follow-up review closeout(236단계 방향별 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage235(235단계)의 cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 실패 축을 분리하고 Stage237(237단계) micro threshold(미세 문턱값) 수리로 넘겼다.\n"
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
                    "artifact_type": "stage236_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage236 Stage235 side-specific follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(reference: Mapping[str, Any], clue: Mapping[str, Any]) -> dict[str, Any]:
    primary = ledger_pairs(
        [
            ("reference_adapter", reference.get("adapter_id", "")),
            ("validation_net_gap_vs_34d", reference.get("validation_net_gap_vs_34d", "")),
            ("early_pf_gap_vs_34d", reference.get("validation_early_pf_gap_vs_34d", "")),
            ("mid_pf_gap_vs_34d", reference.get("validation_mid_pf_gap_vs_34d", "")),
            ("clue_adapter", clue.get("adapter_id", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage236_role", "review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage236_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage236_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage235_side_specific_followup_review(235단계 방향별 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage236 review-only closeout; not final and not deployment.",
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
                    ("reference_adapter", reference.get("adapter_id", "")),
                    ("clue_adapter", clue.get("adapter_id", "")),
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
    reference: Mapping[str, Any],
    clue: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "reference_adapter": reference.get("adapter_id", ""),
        "clue_adapter": clue.get("adapter_id", ""),
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
            "judgment_label": "negative_side_specific_context_axis_candidate_not_final",
            "next_condition": "Stage237 must attempt only micro threshold or rank-confidence recovery around the reference.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Reference preserves OOS but remains slightly below 34D validation net and segment PF; cashopen and short-open damage the package.",
            "comparison_baseline": "Stage235 session reference versus cashopen45 and short-block-off variants",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [
                rel(SOURCE_QUALITY_PATH),
                rel(SOURCE_KPI_PATH),
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
        f"""# Stage236 Closeout Packet(236단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- reference_adapter(기준 어댑터): `{reference.get('adapter_id', '')}`
- clue_adapter(단서 어댑터): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def run() -> Mapping[str, Any]:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    trade_rows = read_csv(SOURCE_TRADE_AUDIT_PATH)
    if not quality_rows:
        raise FileNotFoundError(f"Missing or empty source quality matrix: {SOURCE_QUALITY_PATH}")

    tradeoff_rows = build_tradeoff_rows(quality_rows, risk_rows, trade_rows)
    reference = pick_reference(tradeoff_rows)
    clue = pick_clue(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows(reference, clue)
    failure_rows = build_failure_memory(tradeoff_rows)

    write_md(REPORT_PATH, report_markdown(tradeoff_rows, attribution_rows, route_rows))
    write_csv(TRADEOFF_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(DECISION_PATH, decision_markdown(reference, clue))
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
            "reference_adapter": reference,
            "clue_adapter": clue,
            "legacy_34d": LEGACY_34D,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_stage237_seed(reference, clue)
    update_current_truth(reference, clue)
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(reference, clue)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(
        tradeoff_rows,
        attribution_rows,
        route_rows,
        failure_rows,
        reference,
        clue,
        {**ledger_payload, "artifact_registry": artifact_payload},
    )
    return {
        "status": "reviewed_closed",
        "run_id": RUN_ID,
        "decision": DECISION,
        "reference_adapter": reference.get("adapter_id", ""),
        "clue_adapter": clue.get("adapter_id", ""),
        "report": rel(REPORT_PATH),
        "next_stage": NEXT_STAGE_ID,
        "overall_goal_complete": False,
    }


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
