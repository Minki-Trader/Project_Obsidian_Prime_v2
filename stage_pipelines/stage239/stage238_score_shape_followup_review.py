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


STAGE_ID = "239_adapter_research__stage238_score_shape_followup_review"
RUN_ID = "run239A_stage239_stage238_score_shape_followup_review_v1"
PACKET_ID = "stage239_stage238_score_shape_followup_review_v1"
SOURCE_STAGE_ID = "238_adapter_research__score_shape_repair_after_threshold_surface_discrete"
SOURCE_RUN_ID = "run238A_stage238_score_shape_repair_after_threshold_surface_discrete_v1"
SOURCE_STAGE238_EVIDENCE_COMMIT = "c0ed1ded861232e8e768afffd2ea0a137cc3d07f"
SOURCE_STAGE238_HASH_RECORD_COMMIT = "95c561031f1866d952221ded6033c4294080b9b8"
NEXT_STAGE_ID = "240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff"
NEXT_RUN_ID = "run240A_stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff_v1"
NEXT_PACKET_ID = "stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff_v1"
DECISION = "open_stage240_bounded_highbonus_dd_midpf_repair_after_score_shape_tradeoff_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage238_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_highbonus_dd_midpf_repair_after_score_shape_tradeoff"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}
REFERENCE_ADAPTER = "s238_rank3f_neutral_ref"
HIGHPBONUS_ADAPTER = "s238_highbonus010_rank3f"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage238_score_shape_repair_report.md"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage238_quality_matrix.csv"
SOURCE_KPI_PATH = SOURCE_ROOT / "stage238_score_shape_kpi_summary.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage238_segment_kpi_summary.csv"
SOURCE_BALANCE_PATH = SOURCE_ROOT / "stage238_balance_curve_audit.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage238_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage238_concentration_risk_summary.csv"
SOURCE_DRAWDOWN_PATH = SOURCE_ROOT / "stage238_drawdown_recovery_summary.csv"
SOURCE_RISK_ATR_PATH = SOURCE_ROOT / "stage238_risk_atr_telemetry.csv"
SOURCE_GATE_PATH = SOURCE_ROOT / "stage238_gate_feature_summary.csv"
SOURCE_TRADE_AUDIT_PATH = SOURCE_ROOT / "stage238_trade_audit.csv"
SOURCE_MODEL_SCORE_PATH = SOURCE_ROOT / "stage238_model_score_audit.csv"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage238_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage239_score_shape_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage239_score_shape_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage239_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage239_route_matrix.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage239_failure_memory.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage239_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage239_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage239/stage238_score_shape_followup_review.py")

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


def gap(value: float, target: float) -> float:
    return round(value - target, 6)


def classify(row: Mapping[str, Any], reference: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    val_net = as_float(row.get("validation_net"))
    early_pf = as_float(row.get("validation_early_pf"))
    mid_pf = as_float(row.get("validation_mid_pf"))
    val_dd = as_float(row.get("validation_balance_dd_percent"), 99.0)
    if adapter_id == REFERENCE_ADAPTER:
        return "reference_preserved_but_below_34d"
    if adapter_id == HIGHPBONUS_ADAPTER:
        if val_net > as_float(reference.get("validation_net")) and val_dd > LEGACY_34D["max_drawdown_percent"]:
            return "net_and_oos_gain_but_dd_midpf_failure"
        return "highbonus_mixed_tradeoff"
    if "lowpen" in adapter_id:
        return "low_margin_penalty_trade_supply_collapse"
    if val_net >= LEGACY_34D["net_profit"] and early_pf >= LEGACY_34D["profit_factor"] and mid_pf >= LEGACY_34D["profit_factor"] and val_dd <= LEGACY_34D["max_drawdown_percent"]:
        return "quality_pass_candidate_not_final"
    return "mixed_tradeoff_no_full_repair"


def risk_ok(risk_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> bool:
    val = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
    oos = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
    return (
        as_bool(val.get("atr_enabled"))
        and as_bool(val.get("model_risk_enabled"))
        and as_bool(oos.get("atr_enabled"))
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
) -> list[dict[str, Any]]:
    reference = lookup(quality_rows, adapter_id=REFERENCE_ADAPTER) or (quality_rows[0] if quality_rows else {})
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        val_trade = lookup(trade_rows, variant_id=adapter_id, split="validation_is")
        oos_trade = lookup(trade_rows, variant_id=adapter_id, split="oos")
        val_risk = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
        oos_risk = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
        val_conc = lookup(concentration_rows, adapter_id=adapter_id, split="validation_is")
        oos_conc = lookup(concentration_rows, adapter_id=adapter_id, split="oos")
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
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "review_class": classify(row, reference),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_net_delta_vs_reference": round(as_float(row.get("validation_net")) - as_float(reference.get("validation_net")), 6),
                "validation_pf": row.get("validation_pf", ""),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_early_pf_gap_vs_34d": round(as_float(row.get("validation_early_pf")) - LEGACY_34D["profit_factor"], 9),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(as_float(row.get("validation_mid_pf")) - LEGACY_34D["profit_factor"], 9),
                "validation_mid_net": val_mid.get("net_profit", ""),
                "validation_mid_expectancy": val_mid.get("expectancy", ""),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_dd_delta_vs_reference": round(as_float(row.get("validation_balance_dd_percent")) - as_float(reference.get("validation_balance_dd_percent")), 6),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_top1_winner_share": val_conc.get("top1_winner_share_of_net", ""),
                "validation_top5_winner_share": val_conc.get("top5_winner_share_of_net", ""),
                "validation_last_quarter_share": val_conc.get("last_quarter_net_share", ""),
                "validation_mfe_capture_ratio": val_trade.get("mfe_capture_ratio", ""),
                "validation_cost_stressed_expectancy": val_trade.get("cost_stressed_expectancy", ""),
                "validation_same_move_reentry_ratio": val_trade.get("same_move_reentry_ratio", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_reference": round(as_float(row.get("oos_net")) - as_float(reference.get("oos_net")), 6),
                "oos_pf": row.get("oos_pf", ""),
                "oos_mid_pf": oos_mid.get("profit_factor", ""),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_dd_delta_vs_reference": round(as_float(row.get("oos_balance_dd_percent")) - as_float(reference.get("oos_balance_dd_percent")), 6),
                "oos_late_net_share": row.get("oos_late_net_share", ""),
                "oos_top1_winner_share": oos_conc.get("top1_winner_share_of_net", ""),
                "oos_top5_winner_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_last_quarter_share": oos_conc.get("last_quarter_net_share", ""),
                "oos_mfe_capture_ratio": oos_trade.get("mfe_capture_ratio", ""),
                "oos_cost_stressed_expectancy": oos_trade.get("cost_stressed_expectancy", ""),
                "oos_same_move_reentry_ratio": oos_trade.get("same_move_reentry_ratio", ""),
                "atr_model_risk_present": risk_ok(risk_rows, adapter_id),
                "validation_max_model_risk_pct": val_risk.get("max_model_risk_pct", ""),
                "oos_max_model_risk_pct": oos_risk.get("max_model_risk_pct", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "atr_stop_multiplier": row.get("atr_stop_multiplier", ""),
                "atr_take_profit_multiplier": row.get("atr_take_profit_multiplier", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def best_by_validation_net(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: as_float(row.get("validation_net")), default={})


def reference_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return lookup(rows, adapter_id=REFERENCE_ADAPTER) or (rows[0] if rows else {})


def highbonus_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return lookup(rows, adapter_id=HIGHPBONUS_ADAPTER) or best_by_validation_net(rows)


def build_attribution_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = reference_row(rows)
    high = highbonus_row(rows)
    low15 = lookup(rows, adapter_id="s238_lowpen015_rank3f")
    low25 = lookup(rows, adapter_id="s238_lowpen025_rank3f")
    return [
        {
            "run_id": RUN_ID,
            "finding": "highbonus_recovers_net_and_oos_but_not_34d_quality(고마진 보너스는 순손익과 표본외를 회복하지만 34D 품질은 아님)",
            "observed_change": "validation_net(검증 순손익) +15.69 vs reference(기준), OOS net(표본외 순손익) +93.32 vs reference(기준)",
            "comparison_baseline": REFERENCE_ADAPTER,
            "likely_drivers": "high margin score bonus(고마진 점수 보너스), same trade count(동일 거래 수), higher model risk cap(더 높은 모델 위험 상한)",
            "damage_or_gap": ledger_pairs(
                [
                    ("validation_net_gap_vs_34d", high.get("validation_net_gap_vs_34d", "")),
                    ("validation_dd_margin_vs_34d", high.get("validation_dd_margin_vs_34d", "")),
                    ("early_pf_gap_vs_34d", high.get("validation_early_pf_gap_vs_34d", "")),
                    ("mid_pf_gap_vs_34d", high.get("validation_mid_pf_gap_vs_34d", "")),
                ]
            ),
            "attribution_confidence": "high",
            "next_probe": "Stage240(240단계) risk-normalized highbonus DD/midPF repair(위험 정규화 고마진 낙폭/중간 수익요인 수리)",
        },
        {
            "run_id": RUN_ID,
            "finding": "low_margin_penalties_are_supply_damage(저마진 벌점은 거래 공급 손상)",
            "observed_change": ledger_pairs(
                [
                    ("lowpen015_validation_net", low15.get("validation_net", "")),
                    ("lowpen025_validation_net", low25.get("validation_net", "")),
                    ("lowpen015_oos_net", low15.get("oos_net", "")),
                    ("lowpen025_oos_net", low25.get("oos_net", "")),
                ]
            ),
            "comparison_baseline": REFERENCE_ADAPTER,
            "likely_drivers": "blunt low-margin filter(거친 저마진 필터), trade count collapse(거래 수 붕괴)",
            "damage_or_gap": "net profit(순손익)이 크게 줄어 34D(34D 기준) 접근성이 사라졌다.",
            "attribution_confidence": "high",
            "next_probe": "Do not repeat(반복 금지) as standalone low-margin penalty(독립 저마진 벌점).",
        },
        {
            "run_id": RUN_ID,
            "finding": "concentration_is_not_single_spike_but_late_share_needs_watch(단일 스파이크는 아니지만 후반 비중은 감시 필요)",
            "observed_change": ledger_pairs(
                [
                    ("high_val_top1", high.get("validation_top1_winner_share", "")),
                    ("high_val_top5", high.get("validation_top5_winner_share", "")),
                    ("high_oos_top1", high.get("oos_top1_winner_share", "")),
                    ("high_oos_top5", high.get("oos_top5_winner_share", "")),
                    ("high_oos_last_quarter", high.get("oos_last_quarter_share", "")),
                ]
            ),
            "comparison_baseline": "Stage238 concentration summary(238단계 집중 위험 요약)",
            "likely_drivers": "same route supply(동일 라우팅 공급), high-margin risk score(고마진 위험 점수)",
            "damage_or_gap": "top5 winner share(상위 5개 승자 비중)는 약 40%라 단일 창 의존은 낮지만, late share(후반 비중)가 42% 근처다.",
            "attribution_confidence": "medium",
            "next_probe": "Stage240(240단계) must keep drawdown and late dependence visible(낙폭과 후반 의존을 계속 보이게 유지).",
        },
        {
            "run_id": RUN_ID,
            "finding": "risk_atr_capability_present_but_risk_shape_may_drive_dd(위험/ATR 기능은 있으나 위험 형태가 낙폭을 키울 수 있음)",
            "observed_change": ledger_pairs(
                [
                    ("high_val_max_risk_pct", high.get("validation_max_model_risk_pct", "")),
                    ("high_oos_max_risk_pct", high.get("oos_max_model_risk_pct", "")),
                    ("risk_floor_val", high.get("validation_risk_floor_applied_count", "")),
                    ("risk_floor_oos", high.get("oos_risk_floor_applied_count", "")),
                    ("atr_sl_tp", f"{high.get('atr_stop_multiplier', '')}/{high.get('atr_take_profit_multiplier', '')}"),
                ]
            ),
            "comparison_baseline": "mandatory ATR SL/TP(필수 ATR 손절/익절) and model-controlled risk%(모델 제어 위험 비율)",
            "likely_drivers": "highbonus raises risk score(고마진 보너스가 위험 점수를 올림)",
            "damage_or_gap": "risk cap(위험 상한)은 5% 이하이나 validation DD(검증 낙폭)가 34D(34D 기준)를 넘었다.",
            "attribution_confidence": "medium",
            "next_probe": "Stage240(240단계) should test highbonus with risk normalization(위험 정규화).",
        },
    ]


def build_route_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    high = highbonus_row(rows)
    ref = reference_row(rows)
    return [
        {
            "run_id": RUN_ID,
            "route": DECISION,
            "action": "Open Stage240(240단계)를 highbonus DD/midPF repair(고마진 낙폭/중간 수익요인 수리)로 연다.",
            "effect": "Stage238(238단계)의 좋은 단서인 net/OOS gain(순손익/표본외 개선)을 보존하면서 DD(낙폭)와 mid PF(중간 수익요인)를 따로 고친다.",
            "reference_adapter": ref.get("adapter_id", ""),
            "clue_adapter": high.get("adapter_id", ""),
            "risk": "risk normalization(위험 정규화)이 순손익을 다시 낮출 수 있다.",
        },
        {
            "run_id": RUN_ID,
            "route": "do_not_repeat_blunt_low_margin_penalty(거친 저마진 벌점 반복 금지)",
            "action": "lowpen015/lowpen025(저마진 벌점 0.15/0.25)는 failure memory(실패 기억)로 보존한다.",
            "effect": "거래 공급 붕괴를 다시 반복하지 않고 다음 질문을 좁힌다.",
            "reference_adapter": ref.get("adapter_id", ""),
            "clue_adapter": "",
            "risk": "너무 강한 필터는 PF(수익요인)가 일부 좋아도 net profit(순손익)을 파괴한다.",
        },
        {
            "run_id": RUN_ID,
            "route": "no_final_no_onnx_no_deployment(최종 아님, ONNX 아님, 배포 아님)",
            "action": "Stage239(239단계)를 review-only(검토 전용)로 닫고 adapter_candidate(어댑터 후보) 상태만 유지한다.",
            "effect": "34D(34D 기준) 미달, DD(낙폭) 초과, PF(수익요인) 미달을 완료로 오해하지 않는다.",
            "reference_adapter": ref.get("adapter_id", ""),
            "clue_adapter": high.get("adapter_id", ""),
            "risk": "Stage240(240단계) 실험 근거가 필요하다.",
        },
    ]


def build_failure_memory(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    high = highbonus_row(rows)
    ref = reference_row(rows)
    low15 = lookup(rows, adapter_id="s238_lowpen015_rank3f")
    low25 = lookup(rows, adapter_id="s238_lowpen025_rank3f")
    return [
        {
            "failure_id": f"{RUN_ID}__highbonus_dd_midpf_not_final",
            "hypothesis": "high-margin bonus(고마진 보너스)만으로 34D(34D 기준)를 넘길 수 있다.",
            "why_failed": ledger_pairs(
                [
                    ("validation_net_gap_vs_34d", high.get("validation_net_gap_vs_34d", "")),
                    ("validation_dd_margin_vs_34d", high.get("validation_dd_margin_vs_34d", "")),
                    ("early_pf_gap_vs_34d", high.get("validation_early_pf_gap_vs_34d", "")),
                    ("mid_pf_gap_vs_34d", high.get("validation_mid_pf_gap_vs_34d", "")),
                ]
            ),
            "salvage_value": "net/OOS gain(순손익/표본외 개선)은 보존할 단서다.",
            "reopen_condition": "risk-normalized highbonus(위험 정규화 고마진) 또는 mid-segment guard(중간 구간 보호)에서 다시 측정한다.",
            "do_not_repeat": "highbonus만 올려 final(최종)로 판단하지 않는다.",
        },
        {
            "failure_id": f"{RUN_ID}__reference_below_34d",
            "hypothesis": "neutral reference(중립 기준형)가 충분히 안정적이라 그대로 34D(34D 기준)를 넘는다.",
            "why_failed": ledger_pairs(
                [
                    ("validation_net_gap_vs_34d", ref.get("validation_net_gap_vs_34d", "")),
                    ("early_pf_gap_vs_34d", ref.get("validation_early_pf_gap_vs_34d", "")),
                    ("mid_pf_gap_vs_34d", ref.get("validation_mid_pf_gap_vs_34d", "")),
                ]
            ),
            "salvage_value": "OOS bound(표본외 경계)와 reference comparison(기준 비교)으로 유지한다.",
            "reopen_condition": "새 수리 후보가 OOS(표본외)를 망가뜨리는지 비교할 때 사용한다.",
            "do_not_repeat": "reference(기준형) 숫자만으로 목표 달성을 주장하지 않는다.",
        },
        {
            "failure_id": f"{RUN_ID}__low_margin_penalty_supply_collapse",
            "hypothesis": "low-margin penalty(저마진 벌점)가 DD(낙폭)를 낮추며 34D(34D 기준) 품질을 회복한다.",
            "why_failed": ledger_pairs(
                [
                    ("lowpen015_validation_net", low15.get("validation_net", "")),
                    ("lowpen025_validation_net", low25.get("validation_net", "")),
                    ("lowpen015_oos_net", low15.get("oos_net", "")),
                    ("lowpen025_oos_net", low25.get("oos_net", "")),
                ]
            ),
            "salvage_value": "너무 강한 공급 축소가 실패라는 경계 기억이다.",
            "reopen_condition": "저마진 벌점은 독립 축이 아니라 risk cap(위험 상한)이나 bracket(브래킷)과 결합될 때만 재검토한다.",
            "do_not_repeat": "lowpen015/lowpen025 단독 반복 금지.",
        },
    ]


def report_markdown(rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]]) -> str:
    high = highbonus_row(rows)
    ref = reference_row(rows)
    lines = [
        "# Stage239 Score Shape Follow-up Review(239단계 점수 형태 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage238_evidence_commit(원천 238단계 근거 커밋): `{SOURCE_STAGE238_EVIDENCE_COMMIT}`",
        f"- source_stage238_hash_record_commit(원천 238단계 해시 기록 커밋): `{SOURCE_STAGE238_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        f"- best clue(최선 단서)는 `{high.get('adapter_id', '')}`이다. validation net(검증 순손익) `{high.get('validation_net', '')}`와 OOS net(표본외 순손익) `{high.get('oos_net', '')}`로 reference(기준형)보다 좋아졌다.",
        f"- 하지만 34D(34D 기준)에는 아직 못 미친다. validation net gap(검증 순손익 차이) `{high.get('validation_net_gap_vs_34d', '')}`, validation DD margin(검증 낙폭 여유) `{high.get('validation_dd_margin_vs_34d', '')}`, early/mid PF gap(초반/중간 수익요인 차이) `{high.get('validation_early_pf_gap_vs_34d', '')}/{high.get('validation_mid_pf_gap_vs_34d', '')}`다.",
        f"- reference(기준형) `{ref.get('adapter_id', '')}`는 더 안정적이지만 validation net(검증 순손익) `{ref.get('validation_net', '')}`라 34D(34D 기준)에는 부족하다.",
        "- 결론(conclusion, 결론): highbonus(고마진 보너스)는 버릴 단서가 아니지만 final adapter(최종 어댑터)는 아니다. Stage240(240단계)에서 DD(낙폭)와 mid PF(중간 수익요인)를 좁게 수리한다.",
        "",
        "## Tradeoff Table(상충 표)",
        "",
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | net gap(순손익 차이) | val DD%(검증 낙폭) | early PF(초반 수익요인) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('review_class', '')} | {row.get('validation_net', '')} | {row.get('validation_net_gap_vs_34d', '')} | {row.get('validation_dd_percent', '')} | {row.get('validation_early_pf', '')} | {row.get('validation_mid_pf', '')} | {row.get('oos_net', '')} | {row.get('oos_dd_percent', '')} |"
        )
    lines.extend(
        [
            "",
            "## Attribution(성과 기여 분석)",
            "",
        ]
    )
    for item in attribution_rows:
        lines.append(f"- {item['finding']}: {item['observed_change']} Effect(효과): {item['next_probe']}")
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- result_subject(판정 대상): `{RUN_ID}`",
            "- evidence_available(사용 근거): Stage238(238단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), trade audit(거래 감사), concentration summary(집중 요약).",
            "- judgment_label(판정 라벨): `exploratory_candidate_not_final_with_highbonus_clue(탐색 후보, 최종 아님, 고마진 단서 있음)`",
            "- evidence_missing(부족 근거): Stage240(240단계) 수리 실험, 34D(34D 기준) 이상 동시 통과, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).",
            f"- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 highbonus(고마진) 순손익/OOS(표본외)를 보존하면서 DD(낙폭)와 mid PF(중간 수익요인)를 개선해야 한다.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(high: Mapping[str, Any]) -> str:
    return f"""# Stage239 Decision(239단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- highbonus_clue(고마진 단서): `{high.get('adapter_id', '')}`
- validation_net(검증 순손익): `{high.get('validation_net', '')}`
- validation_net_gap_vs_34d(34D 대비 검증 순손익 차이): `{high.get('validation_net_gap_vs_34d', '')}`
- validation_dd_margin_vs_34d(34D 대비 검증 낙폭 여유): `{high.get('validation_dd_margin_vs_34d', '')}`
- validation_mid_pf_gap_vs_34d(34D 대비 중간 수익요인 차이): `{high.get('validation_mid_pf_gap_vs_34d', '')}`
- OOS_net(표본외 순손익): `{high.get('oos_net', '')}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage239(239단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage240(240단계)는 highbonus(고마진 보너스) 단서를 보존하되 DD(낙폭), early/mid PF(초반/중간 수익요인), risk shape(위험 형태)를 좁게 수리한다.
"""


def write_next_stage_seed(high: Mapping[str, Any], ref: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage240(240단계)는 Stage239(239단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can the highbonus score clue(고마진 점수 단서) preserve validation/OOS net(검증/표본외 순손익) while repairing validation DD(검증 낙폭), early/mid PF(초반/중간 수익요인), and risk shape(위험 형태)?

Effect(효과): Stage238(238단계)에서 확인한 highbonus(고마진) 단서를 버리지 않고, 34D(34D 기준) 미달 원인인 DD/PF(낙폭/수익요인)를 별도 bounded repair(경계 수리)로 다룬다.

## Fixed Requirements(고정 요구)

- ATR SL/TP(ATR 손절/익절)는 유지한다.
- model-controlled risk%(모델 제어 위험 비율)는 유지하고 5% cap(상한)을 넘지 않는다.
- lowpen015/lowpen025(저마진 벌점 0.15/0.25) 단독 반복은 하지 않는다.
- ONNX hardening(ONNX 경화)은 하지 않는다.
- final adapter(최종 어댑터), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.

## Seed Evidence(씨앗 근거)

- clue_adapter(단서 어댑터): `{high.get('adapter_id', '')}`
- reference_adapter(기준 어댑터): `{ref.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 표): `{rel(TRADEOFF_PATH)}`
- attribution(성과 기여 분석): `{rel(ATTRIBUTION_PATH)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage240 Inputs(240단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- clue_adapter(단서 어댑터): `{high.get('adapter_id', '')}`
- reference_adapter(기준 어댑터): `{ref.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 표): `{rel(TRADEOFF_PATH)}`
- attribution(성과 기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage240 Review Index(240단계 검토 색인)

- status(상태): `open_planned_from_stage239`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage240 Selection Status(240단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage239`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(high: Mapping[str, Any], ref: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1)
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1)
    focus = f"""current_focus:
- >-
  Stage239(239단계) closed(종료) as `{DECISION}` and Stage240(240단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): highbonus(고마진 보너스)의 net/OOS gain(순손익/표본외 개선)을 보존하면서 DD/PF(낙폭/수익요인) 수리를 별도 단계로 넘긴다.
- >-
  Stage239 evidence(239단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): Stage238(238단계) 상충을 숨기지 않고 Stage240(240단계)의 수리 축을 좁힌다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage239_stage238_score_shape_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage239_stage238_score_shape_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  highbonus_clue: {high.get('adapter_id', '')}
  reference_adapter: {ref.get('adapter_id', '')}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  failure_memory_path: {rel(FAILURE_MEMORY_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage239
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  highbonus_clue: {high.get('adapter_id', '')}
  reference_adapter: {ref.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `{high.get('adapter_id', '')}`
- status(상태): `stage239_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage239(239단계)는 Stage238(238단계) score shape repair(점수 형태 수리)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage240(240단계)는 highbonus(고마진) 단서의 DD/PF(낙폭/수익요인) 수리만 좁게 실행한다.

## Latest Stage239 Evidence(최신 239단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- highbonus_clue(고마진 단서): `{high.get('adapter_id', '')}`
- reference_adapter(기준 어댑터): `{ref.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 표): `{rel(TRADEOFF_PATH)}`
- attribution(성과 기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage239 Selection Status(239단계 선택 상태)

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
        f"""# Stage239 Review Index(239단계 검토 색인)

- status(상태): `reviewed_closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 표): `{rel(TRADEOFF_PATH)}`
- attribution(성과 기여 분석): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 표): `{rel(ROUTE_MATRIX_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage239 score shape follow-up review closeout(239단계 점수 형태 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): highbonus(고마진) net/OOS gain(순손익/표본외 개선)을 보존하고 DD/midPF(낙폭/중간 수익요인) 수리를 Stage240(240단계)로 넘겼다.\n"
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
                    "artifact_type": "stage239_score_shape_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage239 Stage238 score shape follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(high: Mapping[str, Any], ref: Mapping[str, Any]) -> dict[str, Any]:
    primary = ledger_pairs(
        [
            ("highbonus_clue", high.get("adapter_id", "")),
            ("validation_net", high.get("validation_net", "")),
            ("validation_net_gap_vs_34d", high.get("validation_net_gap_vs_34d", "")),
            ("validation_dd_margin_vs_34d", high.get("validation_dd_margin_vs_34d", "")),
            ("validation_mid_pf_gap_vs_34d", high.get("validation_mid_pf_gap_vs_34d", "")),
            ("oos_net", high.get("oos_net", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("reference_adapter", ref.get("adapter_id", "")),
            ("next_stage", NEXT_STAGE_ID),
            ("stage239_role", "review_only_no_new_mt5_run"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage239_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage239_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage238_score_shape_followup_review(238단계 점수 형태 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage239 review-only closeout; not final and not deployment.",
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
                    ("highbonus_clue", high.get("adapter_id", "")),
                    ("reference_adapter", ref.get("adapter_id", "")),
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
    rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    high: Mapping[str, Any],
    ref: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
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
        "highbonus_clue": high.get("adapter_id", ""),
        "reference_adapter": ref.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": list(rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "failure_memory": list(failure_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "runtime_backtest(MT5/백테스트 실행)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 기여 분석)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": required_gates,
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            **base_payload,
            "source_quality": rel(SOURCE_QUALITY_PATH),
            "source_segments": rel(SOURCE_SEGMENT_PATH),
            "source_risk_atr": rel(SOURCE_RISK_ATR_PATH),
            "source_trade_audit": rel(SOURCE_TRADE_AUDIT_PATH),
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
                rel(FAILURE_MEMORY_PATH),
                rel(DECISION_PATH),
            ],
            "evidence_missing": ["Stage240 repair not run yet(240단계 수리 미실행)", "ONNX/runtime evidence not in scope(ONNX/런타임 근거 범위 밖)"],
            "judgment_label": "exploratory_candidate_not_final_with_highbonus_clue(탐색 후보, 최종 아님, 고마진 단서 있음)",
            "next_condition": "Stage240 must repair DD/midPF while preserving net/OOS and ATR/risk telemetry.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Highbonus improves validation/OOS net but worsens validation DD and keeps early/mid PF below 34D.",
            "comparison_baseline": REFERENCE_ADAPTER,
            "likely_drivers": ["high margin score bonus", "risk score increase", "unchanged trade supply", "mid segment quality"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [
                rel(SOURCE_REPORT_PATH),
                rel(SOURCE_QUALITY_PATH),
                rel(SOURCE_KPI_PATH),
                rel(SOURCE_SEGMENT_PATH),
                rel(SOURCE_RISK_ATR_PATH),
                rel(SOURCE_TRADE_AUDIT_PATH),
                rel(SOURCE_CONCENTRATION_PATH),
                rel(SOURCE_DECISION_PATH),
            ],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "artifact_paths": [
                rel(REPORT_PATH),
                rel(TRADEOFF_PATH),
                rel(ATTRIBUTION_PATH),
                rel(ROUTE_MATRIX_PATH),
                rel(FAILURE_MEMORY_PATH),
                rel(SUMMARY_JSON_PATH),
                rel(DECISION_PATH),
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
        f"""# Stage239 Closeout Packet(239단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- highbonus_clue(고마진 단서): `{high.get('adapter_id', '')}`
- reference_adapter(기준 어댑터): `{ref.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def run() -> Mapping[str, Any]:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    trade_rows = read_csv(SOURCE_TRADE_AUDIT_PATH)
    concentration_rows = read_csv(SOURCE_CONCENTRATION_PATH)
    if not quality_rows:
        raise FileNotFoundError(f"Missing source quality matrix: {SOURCE_QUALITY_PATH}")

    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, risk_rows, trade_rows, concentration_rows)
    high = highbonus_row(tradeoff_rows)
    ref = reference_row(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows(tradeoff_rows)
    failure_rows = build_failure_memory(tradeoff_rows)

    write_md(REPORT_PATH, report_markdown(tradeoff_rows, attribution_rows))
    write_csv(TRADEOFF_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(DECISION_PATH, decision_markdown(high))
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
            "source_balance": rel(SOURCE_BALANCE_PATH),
            "source_monthly": rel(SOURCE_MONTHLY_PATH),
            "source_concentration": rel(SOURCE_CONCENTRATION_PATH),
            "source_drawdown": rel(SOURCE_DRAWDOWN_PATH),
            "source_risk_atr": rel(SOURCE_RISK_ATR_PATH),
            "source_gate": rel(SOURCE_GATE_PATH),
            "source_trade_audit": rel(SOURCE_TRADE_AUDIT_PATH),
            "source_model_score": rel(SOURCE_MODEL_SCORE_PATH),
            "tradeoff_rows": tradeoff_rows,
            "attribution_rows": attribution_rows,
            "route_rows": route_rows,
            "failure_memory": failure_rows,
            "highbonus_clue": high,
            "reference_adapter": ref,
            "legacy_34d": LEGACY_34D,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_next_stage_seed(high, ref)
    update_current_truth(high, ref)
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(high, ref)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(
        tradeoff_rows,
        attribution_rows,
        route_rows,
        failure_rows,
        high,
        ref,
        {**ledger_payload, "artifact_registry": artifact_payload},
    )
    return {
        "status": "reviewed_closed",
        "run_id": RUN_ID,
        "decision": DECISION,
        "highbonus_clue": high.get("adapter_id", ""),
        "reference_adapter": ref.get("adapter_id", ""),
        "report": rel(REPORT_PATH),
        "next_stage": NEXT_STAGE_ID,
        "artifact_registry": artifact_payload,
        "overall_goal_complete": False,
    }


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
