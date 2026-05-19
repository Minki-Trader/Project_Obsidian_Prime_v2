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


STAGE_ID = "241_adapter_research__stage240_highbonus_repair_followup_review"
RUN_ID = "run241A_stage241_stage240_highbonus_repair_followup_review_v1"
PACKET_ID = "stage241_stage240_highbonus_repair_followup_review_v1"

SOURCE_STAGE_ID = "240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff"
SOURCE_RUN_ID = "run240A_stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff_v1"
SOURCE_STAGE240_EVIDENCE_COMMIT = "fa3b78d9e3f3836e67850d0543bb1b9399cd5345"
SOURCE_STAGE240_HASH_RECORD_COMMIT = "ef22ab10ee95be23ac0c250508234a19f5c78f71"

NEXT_STAGE_ID = "242_adapter_research__selective_midsegment_quality_repair_after_highbonus_tradeoff"
NEXT_RUN_ID = "run242A_stage242_selective_midsegment_quality_repair_after_highbonus_tradeoff_v1"
NEXT_PACKET_ID = "stage242_selective_midsegment_quality_repair_after_highbonus_tradeoff_v1"

DECISION = "open_stage242_bounded_selective_midsegment_quality_repair_after_highbonus_tradeoff_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage240_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_selective_midsegment_quality_repair_after_highbonus_tradeoff"
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
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage240_highbonus_repair_report.md"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage240_quality_matrix.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage240_segment_kpi_summary.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage240_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage240_concentration_risk_summary.csv"
SOURCE_RISK_ATR_PATH = SOURCE_ROOT / "stage240_risk_atr_telemetry.csv"
SOURCE_TRADE_PATH = SOURCE_ROOT / "stage240_trade_audit.csv"
SOURCE_BALANCE_PATH = SOURCE_ROOT / "stage240_balance_curve_audit.csv"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage240_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage241_highbonus_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage241_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage241_performance_attribution.csv"
ROUTE_PATH = REVIEWS_ROOT / "stage241_route_matrix.csv"
FAILURE_PATH = REVIEWS_ROOT / "stage241_failure_memory.csv"
SUMMARY_PATH = REVIEWS_ROOT / "stage241_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage241_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage241/stage240_highbonus_repair_followup_review.py")

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


def classify(row: Mapping[str, Any]) -> tuple[str, str]:
    adapter_id = str(row.get("adapter_id", ""))
    if adapter_id == "s240_highbonus010_samecap":
        return (
            "best_net_oos_but_dd_and_midpf_fail",
            "순손익과 OOS(표본외)는 가장 좋지만 DD(낙폭)와 중간 PF(수익요인)가 실패했다.",
        )
    if adapter_id == "s240_highbonus010_cap0275":
        return (
            "dd_repaired_but_net_oos_damaged_midpf_fail",
            "DD(낙폭)는 34D 기준 안으로 들어왔지만 순손익과 OOS(표본외)가 크게 깎이고 중간 PF(수익요인)는 그대로 약하다.",
        )
    if adapter_id == "s240_highbonus010_cap0251":
        return (
            "best_dd_shape_but_net_oos_collapse",
            "DD(낙폭)는 가장 좋아졌지만 순손익과 OOS(표본외)가 무너져 후보가 아니다.",
        )
    if adapter_id == "s240_highbonus0075_cap0290":
        return (
            "balanced_tradeoff_but_still_below_34d",
            "균형은 가장 낫지만 순손익, 초반 PF(수익요인), 중간 PF(수익요인)가 아직 34D에 못 닿는다.",
        )
    return ("mixed_tradeoff_not_final", "상충이 남아 최종 후보가 아니다.")


def risk_present(risk_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> bool:
    val = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
    oos = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
    return (
        as_bool(val.get("atr_enabled"))
        and as_bool(oos.get("atr_enabled"))
        and as_bool(val.get("model_risk_enabled"))
        and as_bool(oos.get("model_risk_enabled"))
        and as_float(val.get("max_model_risk_pct")) <= 0.05
        and as_float(oos.get("max_model_risk_pct")) <= 0.05
    )


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    concentration_rows: Sequence[Mapping[str, Any]],
    balance_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    samecap = lookup(quality_rows, adapter_id="s240_highbonus010_samecap")
    samecap_net = as_float(samecap.get("validation_net"))
    samecap_oos = as_float(samecap.get("oos_net"))
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        review_class, plain_read = classify(row)
        val_mid = lookup(
            segment_rows,
            adapter_id=adapter_id,
            split="validation_is",
            view="actual_routed_total",
            segment_type="chronological_third",
            segment="mid",
        )
        oos_mid = lookup(
            segment_rows,
            adapter_id=adapter_id,
            split="oos",
            view="actual_routed_total",
            segment_type="chronological_third",
            segment="mid",
        )
        val_trade = lookup(trade_rows, adapter_id=adapter_id, split="validation_is")
        oos_trade = lookup(trade_rows, adapter_id=adapter_id, split="oos")
        val_risk = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
        oos_risk = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
        val_conc = lookup(concentration_rows, adapter_id=adapter_id, split="validation_is")
        oos_conc = lookup(concentration_rows, adapter_id=adapter_id, split="oos")
        val_balance = lookup(balance_rows, adapter_id=adapter_id, split="validation_is")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "review_class": review_class,
                "plain_read": plain_read,
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_net_delta_vs_samecap": round(as_float(row.get("validation_net")) - samecap_net, 6),
                "validation_pf": row.get("validation_pf", ""),
                "validation_pf_gap_vs_34d": round(as_float(row.get("validation_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_early_pf_gap_vs_34d": round(as_float(row.get("validation_early_pf")) - LEGACY_34D["profit_factor"], 9),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(as_float(row.get("validation_mid_pf")) - LEGACY_34D["profit_factor"], 9),
                "validation_mid_net": val_mid.get("net_profit", ""),
                "validation_mid_expectancy": val_mid.get("expectancy", ""),
                "validation_balance_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_recovery_factor": val_balance.get("recovery_factor", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_top1_winner_share": val_conc.get("top1_winner_share_of_net", ""),
                "validation_top5_winner_share": val_conc.get("top5_winner_share_of_net", ""),
                "validation_mfe_capture_ratio": val_trade.get("mfe_capture_ratio", ""),
                "validation_cost_stressed_expectancy": val_trade.get("cost_stressed_expectancy", ""),
                "validation_same_move_reentry_ratio": val_trade.get("same_move_reentry_ratio", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_samecap": round(as_float(row.get("oos_net")) - samecap_oos, 6),
                "oos_pf": row.get("oos_pf", ""),
                "oos_mid_pf": oos_mid.get("profit_factor", ""),
                "oos_balance_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_late_net_share": row.get("oos_late_net_share", ""),
                "oos_top1_winner_share": oos_conc.get("top1_winner_share_of_net", ""),
                "oos_top5_winner_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_mfe_capture_ratio": oos_trade.get("mfe_capture_ratio", ""),
                "oos_cost_stressed_expectancy": oos_trade.get("cost_stressed_expectancy", ""),
                "oos_same_move_reentry_ratio": oos_trade.get("same_move_reentry_ratio", ""),
                "atr_model_risk_present": risk_present(risk_rows, adapter_id),
                "validation_max_model_risk_pct": val_risk.get("max_model_risk_pct", ""),
                "oos_max_model_risk_pct": oos_risk.get("max_model_risk_pct", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def best_by(rows: Sequence[Mapping[str, Any]], key: str, reverse: bool = True) -> Mapping[str, Any]:
    if not rows:
        return {}
    return sorted(rows, key=lambda row: as_float(row.get(key)), reverse=reverse)[0]


def build_attribution_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    cap0275 = lookup(rows, adapter_id="s240_highbonus010_cap0275")
    cap0251 = lookup(rows, adapter_id="s240_highbonus010_cap0251")
    cap0290 = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    return [
        {
            "run_id": RUN_ID,
            "finding": "global_risk_cap_compresses_dd_but_damages_net_oos",
            "observed_change": ledger_pairs(
                [
                    ("cap0275_dd_margin_vs_34d", cap0275.get("validation_dd_margin_vs_34d", "")),
                    ("cap0275_validation_net_delta_vs_samecap", cap0275.get("validation_net_delta_vs_samecap", "")),
                    ("cap0275_oos_net_delta_vs_samecap", cap0275.get("oos_net_delta_vs_samecap", "")),
                    ("cap0251_validation_net_delta_vs_samecap", cap0251.get("validation_net_delta_vs_samecap", "")),
                    ("cap0251_oos_net_delta_vs_samecap", cap0251.get("oos_net_delta_vs_samecap", "")),
                ]
            ),
            "comparison_baseline": "s240_highbonus010_samecap",
            "likely_drivers": "전역 risk cap(위험 상한)이 모든 좋은 거래의 크기도 같이 줄였다.",
            "segment_checks": "validation/OOS(검증/표본외), chronological mid(시간 중간 구간), DD(낙폭), cost stress(비용 압박)",
            "attribution_confidence": "high",
            "next_probe": "Stage242(242단계)는 전역 cap(상한) 반복이 아니라 선택적 midsegment(중간 구간) 수리를 시험한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "mid_pf_is_not_repaired_by_global_risk_scaling",
            "observed_change": ledger_pairs(
                [
                    ("samecap_mid_pf_gap_vs_34d", samecap.get("validation_mid_pf_gap_vs_34d", "")),
                    ("cap0275_mid_pf_gap_vs_34d", cap0275.get("validation_mid_pf_gap_vs_34d", "")),
                    ("cap0251_mid_pf_gap_vs_34d", cap0251.get("validation_mid_pf_gap_vs_34d", "")),
                    ("cap0290_mid_pf_gap_vs_34d", cap0290.get("validation_mid_pf_gap_vs_34d", "")),
                ]
            ),
            "comparison_baseline": "legacy 34D KPI(레거시 34D 핵심 성과 지표)",
            "likely_drivers": "중간 구간의 entry quality(진입 품질)나 bracket capture(브래킷 포착) 문제이지 단순 크기 문제만은 아니다.",
            "segment_checks": "early/mid/late PF(초반/중간/후반 수익요인), MFE/MAE proxy(MFE/MAE 대용 기록)",
            "attribution_confidence": "medium",
            "next_probe": "Stage242(242단계)에서 midsegment(중간 구간) 조건부 guard(보호문) 또는 bracket/risk bucket(브래킷/위험 구간)을 좁게 본다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "balanced_variant_is_a_clue_not_a_candidate",
            "observed_change": ledger_pairs(
                [
                    ("cap0290_validation_net", cap0290.get("validation_net", "")),
                    ("cap0290_validation_dd_margin_vs_34d", cap0290.get("validation_dd_margin_vs_34d", "")),
                    ("cap0290_mid_pf_gap_vs_34d", cap0290.get("validation_mid_pf_gap_vs_34d", "")),
                    ("cap0290_oos_net", cap0290.get("oos_net", "")),
                ]
            ),
            "comparison_baseline": "s240_highbonus010_samecap and 34D(34D 기준)",
            "likely_drivers": "highbonus strength(고마진 강도)를 낮추면 DD(낙폭)는 나아지지만 수익 공급이 줄어든다.",
            "segment_checks": "validation net(검증 순손익), OOS net(표본외 순손익), DD margin(낙폭 여유), mid PF(중간 수익요인)",
            "attribution_confidence": "medium",
            "next_probe": "Stage242(242단계)는 cap0290 균형감을 참고하되 순손익/OOS(표본외)를 먼저 보존해야 한다.",
        },
    ]


def build_route_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    cap0290 = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    return [
        {
            "run_id": RUN_ID,
            "route": DECISION,
            "action": "Stage242(242단계)를 선택적 midsegment quality repair(중간 구간 품질 수리)로 연다.",
            "effect": "전역 risk cap(위험 상한) 반복을 피하고, 순손익/OOS(표본외)를 보존하면서 DD/PF(낙폭/수익요인) 원인만 좁게 건드린다.",
            "source_clue": samecap.get("adapter_id", ""),
            "secondary_clue": cap0290.get("adapter_id", ""),
            "not_allowed": "ONNX(온닉스) 작업, final adapter(최종 어댑터) 주장, deployment(배포) 주장",
        },
        {
            "run_id": RUN_ID,
            "route": "preserve_stage240_failure_memory",
            "action": "cap0275/cap0251(위험 상한 0.0275/0.0251)은 실패 기억(failure memory, 실패 기억)으로 남긴다.",
            "effect": "낙폭만 좋아지고 순손익/OOS(표본외)가 무너지는 경로를 반복하지 않는다.",
            "source_clue": "s240_highbonus010_cap0275;s240_highbonus010_cap0251",
            "secondary_clue": "",
            "not_allowed": "전역 cap(상한)만 더 낮추는 단독 캠페인",
        },
    ]


def build_failure_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    cap0275 = lookup(rows, adapter_id="s240_highbonus010_cap0275")
    cap0251 = lookup(rows, adapter_id="s240_highbonus010_cap0251")
    cap0290 = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    return [
        {
            "failure_id": f"{RUN_ID}__samecap_net_oos_not_enough",
            "hypothesis": "Stage238 highbonus(고마진 보너스) 단서를 그대로 유지하면 34D(34D 기준)에 충분히 가까울 수 있다.",
            "why_failed": ledger_pairs(
                [
                    ("validation_net_gap_vs_34d", samecap.get("validation_net_gap_vs_34d", "")),
                    ("validation_dd_margin_vs_34d", samecap.get("validation_dd_margin_vs_34d", "")),
                    ("validation_mid_pf_gap_vs_34d", samecap.get("validation_mid_pf_gap_vs_34d", "")),
                ]
            ),
            "salvage_value": "validation/OOS net(검증/표본외 순손익) 보존 단서",
            "do_not_repeat": "DD/PF(낙폭/수익요인) 실패를 무시하고 최종 후보로 부르지 않는다.",
        },
        {
            "failure_id": f"{RUN_ID}__global_risk_cap_net_oos_damage",
            "hypothesis": "전역 risk cap(위험 상한)을 낮추면 DD(낙폭)와 PF(수익요인)를 동시에 수리할 수 있다.",
            "why_failed": ledger_pairs(
                [
                    ("cap0275_validation_net_delta_vs_samecap", cap0275.get("validation_net_delta_vs_samecap", "")),
                    ("cap0275_oos_net_delta_vs_samecap", cap0275.get("oos_net_delta_vs_samecap", "")),
                    ("cap0251_validation_net_delta_vs_samecap", cap0251.get("validation_net_delta_vs_samecap", "")),
                    ("cap0251_oos_net_delta_vs_samecap", cap0251.get("oos_net_delta_vs_samecap", "")),
                ]
            ),
            "salvage_value": "DD(낙폭) 개선 방향은 확인했지만 전역 적용은 손상",
            "do_not_repeat": "전역 cap(상한)만 낮추는 독립 실험을 반복하지 않는다.",
        },
        {
            "failure_id": f"{RUN_ID}__balanced_cap0290_still_not_34d",
            "hypothesis": "highbonus strength(고마진 강도)를 낮추고 cap(상한)을 중간값으로 두면 34D(34D 기준)에 도달할 수 있다.",
            "why_failed": ledger_pairs(
                [
                    ("validation_net_gap_vs_34d", cap0290.get("validation_net_gap_vs_34d", "")),
                    ("validation_early_pf_gap_vs_34d", cap0290.get("validation_early_pf_gap_vs_34d", "")),
                    ("validation_mid_pf_gap_vs_34d", cap0290.get("validation_mid_pf_gap_vs_34d", "")),
                    ("oos_net_delta_vs_samecap", cap0290.get("oos_net_delta_vs_samecap", "")),
                ]
            ),
            "salvage_value": "균형형 보조 단서",
            "do_not_repeat": "균형이 좋아 보인다는 이유만으로 수익 부족을 덮지 않는다.",
        },
    ]


def report_markdown(
    rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
) -> str:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    best_dd = best_by(rows, "validation_dd_margin_vs_34d", reverse=True)
    balanced = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    lines = [
        "# Stage241 Highbonus Follow-up Review(241단계 고마진 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage240_evidence_commit(원천 240단계 근거 커밋): `{SOURCE_STAGE240_EVIDENCE_COMMIT}`",
        f"- source_stage240_hash_record_commit(원천 240단계 해시 기록 커밋): `{SOURCE_STAGE240_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        f"- `s240_highbonus010_samecap`은 validation net(검증 순손익) `{samecap.get('validation_net', '')}`와 OOS net(표본외 순손익) `{samecap.get('oos_net', '')}`로 가장 강한 단서다. Effect(효과): 순손익 축은 버리면 안 된다.",
        f"- 하지만 같은 변형은 validation DD(검증 낙폭) `{samecap.get('validation_balance_dd_percent', '')}`로 34D(34D 기준)보다 나쁘고, mid PF(중간 수익요인) `{samecap.get('validation_mid_pf', '')}`도 부족하다. Effect(효과): 최종 후보가 아니다.",
        f"- best DD(최선 낙폭) 변형 `{best_dd.get('adapter_id', '')}`은 DD margin(낙폭 여유) `{best_dd.get('validation_dd_margin_vs_34d', '')}`가 좋지만 validation/OOS net(검증/표본외 순손익)이 무너졌다. Effect(효과): 전역 risk cap(위험 상한) 반복은 맞지 않다.",
        f"- balanced clue(균형 단서) `{balanced.get('adapter_id', '')}`은 DD(낙폭)는 기준 안에 들어오지만 net gap(순손익 차이) `{balanced.get('validation_net_gap_vs_34d', '')}`, mid PF gap(중간 수익요인 차이) `{balanced.get('validation_mid_pf_gap_vs_34d', '')}`가 남는다.",
        "- 결론(conclusion, 결론): Stage242(242단계)는 전역 cap(상한)이 아니라 selective midsegment quality repair(선택적 중간 구간 품질 수리)를 해야 한다.",
        "",
        "## Tradeoff Matrix(상충 행렬)",
        "",
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('review_class', '')} | {row.get('validation_net', '')} | {row.get('validation_balance_dd_percent', '')} | {row.get('validation_mid_pf', '')} | {row.get('oos_net', '')} | {row.get('plain_read', '')} |"
        )
    lines.extend(["", "## Attribution(성과 기여 분석)", ""])
    for item in attribution_rows:
        lines.append(f"- {item['finding']}: {item['observed_change']} Effect(효과): {item['next_probe']}")
    lines.extend(["", "## Route(경로)", ""])
    for item in route_rows:
        lines.append(f"- {item['route']}: {item['action']} Effect(효과): {item['effect']}")
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- result_subject(판정 대상): `{RUN_ID}`",
            "- evidence_available(사용 근거): Stage240(240단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), balance/concentration audit(잔고/집중 감사).",
            "- judgment_label(판정 라벨): `stage240_highbonus_tradeoff_reviewed_not_final(240단계 고마진 상충 검토됨, 최종 아님)`",
            "- evidence_missing(부족 근거): 선택적 midsegment repair(중간 구간 수리) 실행, 34D(34D 기준) 이상 동시 통과, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).",
            f"- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 순손익/OOS(표본외)를 보존하면서 DD(낙폭), mid PF(중간 수익요인), cost-stressed expectancy(비용 압박 기대값)를 좁게 수리해야 한다.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    balanced = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    return f"""# Stage241 Decision(241단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- strongest_net_oos_clue(최강 순손익/표본외 단서): `{samecap.get('adapter_id', '')}`
- balanced_secondary_clue(균형 보조 단서): `{balanced.get('adapter_id', '')}`
- samecap_validation_net(동일 상한 검증 순손익): `{samecap.get('validation_net', '')}`
- samecap_validation_dd_margin_vs_34d(동일 상한 34D 대비 낙폭 여유): `{samecap.get('validation_dd_margin_vs_34d', '')}`
- samecap_validation_mid_pf_gap_vs_34d(동일 상한 34D 대비 중간 수익요인 차이): `{samecap.get('validation_mid_pf_gap_vs_34d', '')}`
- balanced_validation_net_gap_vs_34d(균형형 34D 대비 검증 순손익 차이): `{balanced.get('validation_net_gap_vs_34d', '')}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage241(241단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage242(242단계)는 전역 risk cap(위험 상한)을 반복하지 않고, highbonus(고마진) 순손익/OOS(표본외)를 보존하면서 midsegment quality(중간 구간 품질)를 좁게 수리한다.
"""


def write_next_stage_seed(rows: Sequence[Mapping[str, Any]]) -> None:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    balanced = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage242(242단계)는 Stage241(241단계) review(검토)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a selective midsegment quality repair(선택적 중간 구간 품질 수리) preserve highbonus validation/OOS net(고마진 검증/표본외 순손익) while repairing validation DD(검증 낙폭), mid PF(중간 수익요인), cost-stressed expectancy(비용 압박 기대값), and ATR/risk telemetry(ATR/위험 기록)?

Effect(효과): Stage240(240단계)의 전역 risk cap(위험 상한) 손상을 반복하지 않고, 손상 원인으로 보이는 중간 구간 품질만 좁게 건드린다.

## Fixed Requirements(고정 요구)

- Preserve ATR SL/TP(ATR 손절/익절).
- Preserve model-controlled risk%(모델 제어 위험 비율) and 5% cap(5% 상한).
- Do not repeat standalone global risk cap compression(전역 위험 상한 압축 단독 반복 금지).
- Do not run ONNX hardening(ONNX 경화) in this stage.
- Do not claim final adapter(최종 어댑터), deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), or runtime authority(런타임 권위).

## Seed Evidence(씨앗 근거)

- strongest_net_oos_clue(최강 순손익/표본외 단서): `{samecap.get('adapter_id', '')}`
- balanced_secondary_clue(균형 보조 단서): `{balanced.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 기여 분석): `{rel(ATTRIBUTION_PATH)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage242 Inputs(242단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- strongest_net_oos_clue(최강 순손익/표본외 단서): `{samecap.get('adapter_id', '')}`
- balanced_secondary_clue(균형 보조 단서): `{balanced.get('adapter_id', '')}`
- source_stage240_quality(원천 240단계 품질): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage240_segments(원천 240단계 구간): `{rel(SOURCE_SEGMENT_PATH)}`
- source_stage240_risk_atr(원천 240단계 위험/ATR): `{rel(SOURCE_RISK_ATR_PATH)}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage242 Review Index(242단계 검토 색인)

- status(상태): `open_planned_from_stage241`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage242 Selection Status(242단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage241`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def replace_stage_block(text: str, key: str, block: str) -> str:
    pattern = rf"(?ms)^({re.escape(key)}:\r?\n).*?(?=^\S|\Z)"
    if re.search(pattern, text):
        return re.sub(pattern, block.rstrip() + "\n\n", text, count=1)
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_current_truth(rows: Sequence[Mapping[str, Any]]) -> None:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    balanced = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1)
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1)
    focus = f"""current_focus:
- >-
  Stage241(241단계) closed(종료) as `{DECISION}` and Stage242(242단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): highbonus(고마진) 순손익/OOS(표본외)를 보존하면서 중간 구간 품질과 낙폭을 좁게 수리한다.
- >-
  Stage241 evidence(241단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): Stage240(240단계)의 전역 risk cap(위험 상한) 손상을 실패 기억으로 남기고 다음 수리축을 좁힌다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=^\S)", focus, state, count=1)
    stage241_block = f"""stage241_stage240_highbonus_repair_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  strongest_net_oos_clue: {samecap.get('adapter_id', '')}
  balanced_secondary_clue: {balanced.get('adapter_id', '')}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  failure_memory_path: {rel(FAILURE_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    stage242_block = f"""stage242_selective_midsegment_quality_repair_after_highbonus_tradeoff:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage241
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  strongest_net_oos_clue: {samecap.get('adapter_id', '')}
  balanced_secondary_clue: {balanced.get('adapter_id', '')}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage241_stage240_highbonus_repair_followup_review", stage241_block)
    state = replace_stage_block(state, "stage242_selective_midsegment_quality_repair_after_highbonus_tradeoff", stage242_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n", encoding="utf-8-sig")

    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{samecap.get('adapter_id', '')}`
- status(상태): `stage241_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage241(241단계)는 Stage240(240단계) highbonus DD/midPF repair(고마진 낙폭/중간 수익요인 수리)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage242(242단계)가 전역 risk cap(위험 상한)을 반복하지 않고 selective midsegment quality repair(선택적 중간 구간 품질 수리)만 좁게 실행한다.

## Latest Stage241 Evidence(최신 241단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- strongest_net_oos_clue(최강 순손익/표본외 단서): `{samecap.get('adapter_id', '')}`
- balanced_secondary_clue(균형 보조 단서): `{balanced.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage241 Selection Status(241단계 선택 상태)

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
        f"""# Stage241 Review Index(241단계 검토 색인)

- status(상태): `reviewed_closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 기여 분석): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage241 highbonus follow-up review closeout(241단계 고마진 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage240(240단계)의 전역 risk cap(위험 상한) 손상을 실패 기억으로 보존하고 Stage242(242단계)를 선택적 중간 구간 수리로 열었다.\n"
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
        ROUTE_PATH,
        FAILURE_PATH,
        SUMMARY_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage241_highbonus_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage241 Stage240 highbonus follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    balanced = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    primary = ledger_pairs(
        [
            ("strongest_net_oos_clue", samecap.get("adapter_id", "")),
            ("validation_net", samecap.get("validation_net", "")),
            ("validation_net_gap_vs_34d", samecap.get("validation_net_gap_vs_34d", "")),
            ("validation_dd_margin_vs_34d", samecap.get("validation_dd_margin_vs_34d", "")),
            ("validation_mid_pf_gap_vs_34d", samecap.get("validation_mid_pf_gap_vs_34d", "")),
            ("oos_net", samecap.get("oos_net", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("balanced_secondary_clue", balanced.get("adapter_id", "")),
            ("next_stage", NEXT_STAGE_ID),
            ("stage241_role", "review_only_no_new_mt5_run"),
            ("boundary", BOUNDARY),
            ("overall_goal_complete", 0),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage241_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage241_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage240_highbonus_followup_review(240단계 고마진 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage241 review-only closeout; not final and not deployment.",
        }
    ]
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "notes": ledger_pairs(
                [
                    ("source_run", SOURCE_RUN_ID),
                    ("strongest_net_oos_clue", samecap.get("adapter_id", "")),
                    ("balanced_secondary_clue", balanced.get("adapter_id", "")),
                    ("boundary", BOUNDARY),
                ]
            ),
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(
    rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    samecap = lookup(rows, adapter_id="s240_highbonus010_samecap")
    balanced = lookup(rows, adapter_id="s240_highbonus0075_cap0290")
    required_gates = [
        "kpi_contract_audit",
        "result_judgment_gate",
        "performance_attribution_gate",
        "artifact_lineage_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "strongest_net_oos_clue": samecap.get("adapter_id", ""),
        "balanced_secondary_clue": balanced.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "quality_rows": list(rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "failure_memory": list(failure_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "kpi_evidence(KPI/근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 기여 분석)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
            ],
            "required_gates": required_gates,
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            **base_payload,
            "source_quality": rel(SOURCE_QUALITY_PATH),
            "source_segments": rel(SOURCE_SEGMENT_PATH),
            "source_risk_atr": rel(SOURCE_RISK_ATR_PATH),
            "source_trade_audit": rel(SOURCE_TRADE_PATH),
            "summary_rows": len(rows),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(REPORT_PATH),
                rel(TRADEOFF_PATH),
                rel(ATTRIBUTION_PATH),
                rel(FAILURE_PATH),
                rel(DECISION_PATH),
            ],
            "evidence_missing": [
                "Stage242 selective repair not run yet(242단계 선택적 수리 미실행)",
                "ONNX/runtime evidence not in scope(ONNX/런타임 근거 범위 밖)",
            ],
            "judgment_label": "stage240_highbonus_tradeoff_reviewed_not_final(240단계 고마진 상충 검토됨, 최종 아님)",
            "next_condition": "Stage242 must repair midsegment quality while preserving net/OOS and ATR/risk telemetry.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Global risk cap improves DD but damages validation/OOS net and does not repair mid PF.",
            "comparison_baseline": "s240_highbonus010_samecap and legacy 34D KPI(레거시 34D 핵심 성과 지표)",
            "likely_drivers": ["global risk cap compression", "midsegment entry quality", "risk/bracket interaction"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [
                rel(SOURCE_REPORT_PATH),
                rel(SOURCE_QUALITY_PATH),
                rel(SOURCE_SEGMENT_PATH),
                rel(SOURCE_MONTHLY_PATH),
                rel(SOURCE_CONCENTRATION_PATH),
                rel(SOURCE_RISK_ATR_PATH),
                rel(SOURCE_TRADE_PATH),
                rel(SOURCE_BALANCE_PATH),
                rel(SOURCE_DECISION_PATH),
            ],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "artifact_paths": [
                rel(REPORT_PATH),
                rel(TRADEOFF_PATH),
                rel(ATTRIBUTION_PATH),
                rel(ROUTE_PATH),
                rel(FAILURE_PATH),
                rel(SUMMARY_PATH),
                rel(DECISION_PATH),
            ],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
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
            "required_gates": required_gates,
            "covered_by": [
                "kpi_contract_audit.json",
                "result_judgment_gate.json",
                "performance_attribution_gate.json",
                "artifact_lineage_audit.json",
                "final_claim_guard.json",
                "required_gate_coverage_audit.json",
            ],
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "tradeoff": rel(TRADEOFF_PATH),
                "attribution": rel(ATTRIBUTION_PATH),
                "route": rel(ROUTE_PATH),
                "failure_memory": rel(FAILURE_PATH),
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
        f"""# Stage241 Closeout Packet(241단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- strongest_net_oos_clue(최강 순손익/표본외 단서): `{samecap.get('adapter_id', '')}`
- balanced_secondary_clue(균형 보조 단서): `{balanced.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def run() -> Mapping[str, Any]:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    if not quality_rows:
        raise FileNotFoundError(f"Missing source quality matrix: {SOURCE_QUALITY_PATH}")
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    trade_rows = read_csv(SOURCE_TRADE_PATH)
    concentration_rows = read_csv(SOURCE_CONCENTRATION_PATH)
    balance_rows = read_csv(SOURCE_BALANCE_PATH)

    rows = build_tradeoff_rows(quality_rows, segment_rows, risk_rows, trade_rows, concentration_rows, balance_rows)
    attribution_rows = build_attribution_rows(rows)
    route_rows = build_route_rows(rows)
    failure_rows = build_failure_rows(rows)

    write_md(REPORT_PATH, report_markdown(rows, attribution_rows, route_rows))
    write_csv(TRADEOFF_PATH, rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_PATH, route_rows)
    write_csv(FAILURE_PATH, failure_rows)
    write_md(DECISION_PATH, decision_markdown(rows))
    write_status_files()
    write_next_stage_seed(rows)
    update_current_truth(rows)
    append_changelog()

    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "external_verification_status": EXTERNAL_STATUS,
        "quality_rows": rows,
        "attribution_rows": attribution_rows,
        "route_rows": route_rows,
        "failure_memory": failure_rows,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
    }
    write_json(SUMMARY_PATH, summary)

    ledger_payload = write_ledgers(rows)
    summary["ledger_payload"] = ledger_payload
    write_json(SUMMARY_PATH, summary)
    write_packet_files(rows, attribution_rows, route_rows, failure_rows, ledger_payload)
    return summary


if __name__ == "__main__":
    result = run()
    print(
        json.dumps(
            {
                "stage": STAGE_ID,
                "run": RUN_ID,
                "decision": result["decision"],
                "rows": len(result["quality_rows"]),
                "overall_goal_complete": result["overall_goal_complete"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
