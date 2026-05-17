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


STAGE_ID = "117_adapter_research__v41_density_quality_followup_review"
RUN_ID = "run117A_stage117_v41_density_quality_followup_review_v1"
PACKET_ID = "stage117_v41_density_quality_followup_review_v1"
PARENT_RUN_ID = "run116A_stage116_v41_density_quality_balance_repair_v1"
SOURCE_STAGE116_ID = "116_adapter_research__v41_density_quality_balance_repair"
SOURCE_STAGE116_CLOSEOUT_COMMIT = "e2ef0707cdaaefc77df92e5dac641db4199c3cb7"
SOURCE_STAGE116_LATEST_COMMIT = "c115268a398da4c8334b2c21530016f110b8e927"
SOURCE_STAGE114_LATEST_COMMIT = "19778c1e66346dcef4ce8e455c5b5960cfa1e1e7"
SOURCE_STAGE110_LATEST_COMMIT = "c702502f01e2ef0e9a17d2ac9ec86b6108a82d04"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_dd_compression_density_repair_in_stage118"
NEXT_STAGE_ID = "118_adapter_research__v41_dd_compression_density_repair"
NEXT_RUN_ID = "run118A_stage118_v41_dd_compression_density_repair_v1"
NEXT_PACKET_ID = "stage118_v41_dd_compression_density_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage116_mt5_runtime_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE110_REFERENCE = {
    "source_stage": "stage110_balanced_reference",
    "source_run_id": "run110A_stage110_v41_trade_density_net_scale_after_dd_tradeoff_repair_v1",
    "adapter_id": "s110_v41_h3_cd9_lng53_early_adx19",
    "profit_factor": 1.637076853,
    "net_profit": 644.76,
    "max_drawdown_percent": 18.69,
    "trade_count": 147,
    "expectancy": 4.386122449,
    "cost_stressed_expectancy": 4.086122449,
    "same_move_reentry_ratio": 0.05442176871,
    "mfe_capture_ratio": 0.2346426109,
    "early_net_profit": 38.84,
    "early_profit_factor": 1.157011764,
    "mid_net_profit": 179.59,
    "mid_profit_factor": 1.726265864,
    "late_net_profit": 426.33,
    "late_profit_factor": 1.988133554,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

STAGE114_REVIEWS = Path("stages/114_adapter_research__v41_supply_quality_filter_repair/03_reviews")
STAGE114_SUMMARY = STAGE114_REVIEWS / "stage114_supply_quality_filter_summary.csv"
STAGE114_SEGMENTS = STAGE114_REVIEWS / "stage114_segment_kpi_summary.csv"
STAGE114_REPORT = STAGE114_REVIEWS / "stage114_supply_quality_filter_report.md"
STAGE116_REVIEWS = Path("stages") / SOURCE_STAGE116_ID / "03_reviews"
STAGE116_SUMMARY = STAGE116_REVIEWS / "stage116_density_quality_balance_summary.csv"
STAGE116_SEGMENTS = STAGE116_REVIEWS / "stage116_segment_kpi_summary.csv"
STAGE116_RISK_ATR = STAGE116_REVIEWS / "stage116_risk_atr_telemetry.csv"
STAGE116_REPORT = STAGE116_REVIEWS / "stage116_density_quality_balance_report.md"
STAGE116_DECISION = STAGE116_REVIEWS / "stage116_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage117_density_quality_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage117_stage110_stage114_stage116_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage117_density_quality_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage117_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

STAGE114_ADAPTERS = (
    "s114_v41_h3_cd9_rule_block_lng53",
    "s114_v41_h3_cd9_margin_mid_block_lng53",
    "s114_v41_h3_cd9_rule_margin_block_lng53",
    "s114_v41_h3_cd9_session_margin_block_lng53",
)

STAGE116_ADAPTERS = (
    "s116_v41_h3_cd9_rule_margin_lng52",
    "s116_v41_h3_cd8_rule_margin_lng53",
    "s116_v41_h3_cd9_session_margin_lng52",
    "s116_v41_h3_cd8_session_margin_lng53",
)

STAGE116_TO_STAGE114 = {
    "s116_v41_h3_cd9_rule_margin_lng52": "s114_v41_h3_cd9_rule_margin_block_lng53",
    "s116_v41_h3_cd8_rule_margin_lng53": "s114_v41_h3_cd9_rule_margin_block_lng53",
    "s116_v41_h3_cd9_session_margin_lng52": "s114_v41_h3_cd9_session_margin_block_lng53",
    "s116_v41_h3_cd8_session_margin_lng53": "s114_v41_h3_cd9_session_margin_block_lng53",
}


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def num(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        return default
    try:
        return float(str(value))
    except ValueError:
        return default


def fmt(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def summary_row(path: Path, adapter_id: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") == "oos" and row.get("view") == "actual_routed_total" and row.get("status") == "completed":
            return row
    return {}


def segment_row(path: Path, adapter_id: str, segment_type: str, segment: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") != "oos" or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == segment_type and row.get("segment") == segment:
            return row
    return {}


def metric_row(source_stage: str, source_run_id: str, adapter_id: str, summary_path: Path, segment_path: Path) -> dict[str, Any]:
    summary = summary_row(summary_path, adapter_id)
    full = segment_row(segment_path, adapter_id, "full_split", "actual_routed_total")
    early = segment_row(segment_path, adapter_id, "chronological_third", "early")
    mid = segment_row(segment_path, adapter_id, "chronological_third", "mid")
    late = segment_row(segment_path, adapter_id, "chronological_third", "late")
    return {
        "source_stage": source_stage,
        "source_run_id": source_run_id,
        "adapter_id": adapter_id,
        "profit_factor": num(full, "profit_factor", num(summary, "profit_factor")),
        "net_profit": num(full, "net_profit", num(summary, "net_profit")),
        "max_drawdown_percent": num(summary, "max_drawdown_percent"),
        "trade_count": num(full, "trade_count", num(summary, "trade_count")),
        "expectancy": num(full, "expectancy", num(summary, "expectancy")),
        "cost_stressed_expectancy": num(summary, "cost_stressed_expectancy"),
        "same_move_reentry_ratio": num(summary, "same_move_reentry_ratio"),
        "mfe_capture_ratio": num(full, "mfe_capture_ratio", num(summary, "mfe_capture_ratio")),
        "early_net_profit": num(early, "net_profit"),
        "early_profit_factor": num(early, "profit_factor"),
        "mid_net_profit": num(mid, "net_profit"),
        "mid_profit_factor": num(mid, "profit_factor"),
        "late_net_profit": num(late, "net_profit"),
        "late_profit_factor": num(late, "profit_factor"),
    }


def risk_atr_summary() -> dict[str, Any]:
    rows = [row for row in read_csv(STAGE116_RISK_ATR) if row.get("split") == "oos" and row.get("view") == "actual_routed_total"]
    if not rows:
        return {
            "atr_enabled": "missing",
            "model_risk_enabled": "missing",
            "risk_floor_applied_count": "missing",
            "max_model_risk_pct": "missing",
            "max_actual_risk_pct_after_floor": "missing",
        }
    return {
        "atr_enabled": all(row.get("atr_enabled") == "True" for row in rows),
        "model_risk_enabled": all(row.get("model_risk_enabled") == "True" for row in rows),
        "risk_floor_applied_count": int(sum(num(row, "risk_floor_applied_count") for row in rows)),
        "max_model_risk_pct": max(num(row, "max_model_risk_pct") for row in rows),
        "max_actual_risk_pct_after_floor": max(num(row, "max_actual_risk_pct_after_floor") for row in rows),
        "risk_bucket": ",".join(sorted({row.get("risk_bucket", "") for row in rows if row.get("risk_bucket")})),
    }


def base_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_stage": "legacy_34d_lesson_target",
            "source_run_id": "legacy_34d_lesson_only",
            "adapter_id": "legacy_34d_kpi_target_not_v2_result",
            "profit_factor": LEGACY_34D["profit_factor"],
            "net_profit": LEGACY_34D["net_profit"],
            "max_drawdown_percent": LEGACY_34D["max_drawdown_percent"],
            "trade_count": LEGACY_34D["trade_count"],
        },
        dict(STAGE110_REFERENCE),
    ]
    for adapter_id in STAGE114_ADAPTERS:
        rows.append(metric_row("stage114_supply_quality_filter", "run114A_stage114_v41_supply_quality_filter_repair_v1", adapter_id, STAGE114_SUMMARY, STAGE114_SEGMENTS))
    for adapter_id in STAGE116_ADAPTERS:
        rows.append(metric_row("stage116_density_quality_balance_repair", PARENT_RUN_ID, adapter_id, STAGE116_SUMMARY, STAGE116_SEGMENTS))
    return rows


def row_read(row: Mapping[str, Any], by_adapter: Mapping[str, Mapping[str, Any]]) -> str:
    source = str(row.get("source_stage", ""))
    adapter = str(row.get("adapter_id", ""))
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    trades = num(row, "trade_count")
    if source == "legacy_34d_lesson_target":
        return "lesson_only_target_not_v2_result"
    if source == "stage110_balanced_reference":
        return "prior_reference_has_lower_net_and_density_but_lower_dd_than_stage116"
    if adapter.endswith("rule_block_lng53"):
        return "density_preserved_but_pf_below_34d_and_dd_high"
    if adapter.endswith("margin_mid_block_lng53"):
        return "moderate_density_but_net_pf_and_dd_not_enough"
    if source == "stage114_supply_quality_filter":
        if pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and trades < 180:
            return "quality_anchor_strong_but_density_and_dd_gap_remain"
        return "stage114_reference_surface_for_stage116"
    if source == "stage116_density_quality_balance_repair":
        anchor = by_adapter.get(STAGE116_TO_STAGE114.get(adapter, ""), {})
        trade_delta = trades - num(anchor, "trade_count")
        pf_delta = pf - num(anchor, "profit_factor")
        dd_delta = dd - num(anchor, "max_drawdown_percent")
        if abs(trade_delta) < 0.5 and abs(pf_delta) < 0.000001 and abs(dd_delta) < 0.000001:
            return "unchanged_from_stage114_quality_anchor"
        if trade_delta > 0 and (pf_delta < 0 or dd_delta > 0):
            return "tiny_density_gain_with_quality_or_dd_damage"
        return "stage116_variant_requires_followup_review"
    return "requires_review"


def comparison_rows() -> list[dict[str, Any]]:
    raw_rows = base_rows()
    by_adapter = {str(row.get("adapter_id", "")): row for row in raw_rows}
    output: list[dict[str, Any]] = []
    for row in raw_rows:
        pf = num(row, "profit_factor")
        net = num(row, "net_profit")
        dd = num(row, "max_drawdown_percent")
        trades = num(row, "trade_count")
        anchor = by_adapter.get(STAGE116_TO_STAGE114.get(str(row.get("adapter_id", "")), ""), {})
        output.append(
            {
                "run_id": RUN_ID,
                "source_stage": row.get("source_stage", ""),
                "source_run_id": row.get("source_run_id", ""),
                "adapter_id": row.get("adapter_id", ""),
                "split": "oos",
                "profit_factor": fmt(pf),
                "net_profit": fmt(net, 2),
                "max_drawdown_percent": fmt(dd),
                "trade_count": fmt(trades, 0),
                "expectancy": fmt(num(row, "expectancy")),
                "cost_stressed_expectancy": fmt(num(row, "cost_stressed_expectancy")),
                "same_move_reentry_ratio": fmt(num(row, "same_move_reentry_ratio")),
                "mfe_capture_ratio": fmt(num(row, "mfe_capture_ratio")),
                "early_net_profit": fmt(num(row, "early_net_profit"), 2),
                "early_profit_factor": fmt(num(row, "early_profit_factor")),
                "mid_net_profit": fmt(num(row, "mid_net_profit"), 2),
                "mid_profit_factor": fmt(num(row, "mid_profit_factor")),
                "late_net_profit": fmt(num(row, "late_net_profit"), 2),
                "late_profit_factor": fmt(num(row, "late_profit_factor")),
                "pf_gap_to_34d": fmt(pf - LEGACY_34D["profit_factor"]),
                "net_gap_to_34d": fmt(net - LEGACY_34D["net_profit"], 2),
                "dd_gap_to_34d": fmt(dd - LEGACY_34D["max_drawdown_percent"]),
                "trade_count_gap_to_34d": fmt(trades - LEGACY_34D["trade_count"], 0),
                "dd_gap_to_stage110": fmt(dd - STAGE110_REFERENCE["max_drawdown_percent"]),
                "stage116_anchor_adapter": anchor.get("adapter_id", ""),
                "trade_count_delta_vs_stage114_anchor": fmt(trades - num(anchor, "trade_count"), 0) if anchor else "",
                "pf_delta_vs_stage114_anchor": fmt(pf - num(anchor, "profit_factor")) if anchor else "",
                "net_delta_vs_stage114_anchor": fmt(net - num(anchor, "net_profit"), 2) if anchor else "",
                "dd_delta_vs_stage114_anchor": fmt(dd - num(anchor, "max_drawdown_percent")) if anchor else "",
                "stage117_read": row_read(row, by_adapter),
            }
        )
    return output


def stage116_rows(rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [row for row in rows if row.get("source_stage") == "stage116_density_quality_balance_repair"]


def stage114_rows(rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [row for row in rows if row.get("source_stage") == "stage114_supply_quality_filter"]


def best_stage116_quality(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(stage116_rows(rows), key=lambda row: (num(row, "profit_factor"), num(row, "net_profit"), -num(row, "max_drawdown_percent")), default={})


def best_stage116_density(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(stage116_rows(rows), key=lambda row: (num(row, "trade_count"), num(row, "net_profit"), num(row, "profit_factor")), default={})


def best_stage114_density(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(stage114_rows(rows), key=lambda row: (num(row, "trade_count"), num(row, "net_profit"), num(row, "profit_factor")), default={})


def tradeoff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in stage116_rows(rows):
        read = str(row.get("stage117_read", ""))
        if read == "unchanged_from_stage114_quality_anchor":
            next_probe = "do_not_repeat_threshold_only_density_recovery"
        elif "tiny_density_gain" in read:
            next_probe = "compress_dd_before_more_density_relaxation"
        else:
            next_probe = "review_before_next_repair"
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "stage116_anchor_adapter": row.get("stage116_anchor_adapter", ""),
                "trade_count": row.get("trade_count", ""),
                "profit_factor": row.get("profit_factor", ""),
                "net_profit": row.get("net_profit", ""),
                "max_drawdown_percent": row.get("max_drawdown_percent", ""),
                "trade_count_delta_vs_stage114_anchor": row.get("trade_count_delta_vs_stage114_anchor", ""),
                "pf_delta_vs_stage114_anchor": row.get("pf_delta_vs_stage114_anchor", ""),
                "net_delta_vs_stage114_anchor": row.get("net_delta_vs_stage114_anchor", ""),
                "dd_delta_vs_stage114_anchor": row.get("dd_delta_vs_stage114_anchor", ""),
                "trade_count_gap_to_34d": row.get("trade_count_gap_to_34d", ""),
                "dd_gap_to_34d": row.get("dd_gap_to_34d", ""),
                "dd_gap_to_stage110": row.get("dd_gap_to_stage110", ""),
                "read": read,
                "next_probe": next_probe,
            }
        )
    return output


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        if row.get("source_stage") not in {"legacy_34d_lesson_target", "stage110_balanced_reference", "stage114_supply_quality_filter", "stage116_density_quality_balance_repair"}:
            continue
        lines.append(
            f"| {row.get('source_stage', '')} | {row.get('adapter_id', '')} | {row.get('profit_factor', '')} | {row.get('net_profit', '')} | {row.get('max_drawdown_percent', '')} | {row.get('trade_count', '')} | {row.get('stage117_read', '')} |"
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]], risk: Mapping[str, Any]) -> str:
    best_quality = best_stage116_quality(rows)
    best_density = best_stage116_density(rows)
    stage114_density = best_stage114_density(rows)
    tradeoff_text = "\n".join(
        f"- `{row.get('adapter_id')}`: {row.get('read')} -> {row.get('next_probe')}"
        for row in tradeoffs
    )
    return f"""# Stage117 Density Quality Follow-up Review(117단계 밀도-품질 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE116_ID}`
- source_stage116_closeout_commit(원천 116단계 종료 커밋): `{SOURCE_STAGE116_CLOSEOUT_COMMIT}`
- source_stage116_latest_commit(원천 116단계 최신 커밋): `{SOURCE_STAGE116_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage116(116단계)이 Stage114/115(114/115단계)의 quality anchor(품질 기준점)에서 density(밀도)를 되살렸는가, 아니면 DD compression(손실률 압축)을 먼저 해야 하는가?

Effect(효과): Stage117(117단계)는 새 MT5 실행(run, 실행)을 하지 않고, 기존 Stage116 runtime evidence(실행환경 근거)를 판독해서 다음 bounded repair(경계 수리)를 하나로 좁힌다.

## Comparison(비교)

{markdown_table(rows)}

## Best Reads(최선 판독)

- best_stage116_quality(116단계 품질 최선): `{best_quality.get('adapter_id')}` with PF(수익 팩터) `{best_quality.get('profit_factor')}`, net(순손익) `{best_quality.get('net_profit')}`, DD%(손실률) `{best_quality.get('max_drawdown_percent')}`, trades(거래 수) `{best_quality.get('trade_count')}`.
- best_stage116_density(116단계 밀도 최선): `{best_density.get('adapter_id')}` with PF(수익 팩터) `{best_density.get('profit_factor')}`, net(순손익) `{best_density.get('net_profit')}`, DD%(손실률) `{best_density.get('max_drawdown_percent')}`, trades(거래 수) `{best_density.get('trade_count')}`.
- retained_stage114_density(유지된 114단계 밀도): `{stage114_density.get('adapter_id')}` with trades(거래 수) `{stage114_density.get('trade_count')}`, PF(수익 팩터) `{stage114_density.get('profit_factor')}`.

## Risk/ATR Telemetry(위험/ATR 텔레메트리)

- atr_enabled(ATR 켜짐): `{risk.get('atr_enabled')}`
- model_risk_enabled(모델 위험 켜짐): `{risk.get('model_risk_enabled')}`
- risk_floor_applied_count(최소 lot 바닥 적용 수): `{risk.get('risk_floor_applied_count')}`
- max_model_risk_pct(최대 모델 위험 퍼센트): `{risk.get('max_model_risk_pct')}`
- max_actual_risk_pct_after_floor(바닥 적용 뒤 최대 실제 위험 퍼센트): `{risk.get('max_actual_risk_pct_after_floor')}`

## Tradeoff(상충)

{tradeoff_text}

## Judgment(판정)

- result_subject(판정 대상): Stage116 density-quality balance repair(116단계 밀도-품질 균형 수리).
- evidence_available(있는 근거): Stage116 MT5 runtime summary(실행환경 요약), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), Stage114/110/34D comparison(비교).
- evidence_missing(부족 근거): DD%(손실률)를 34D target(목표) 근처로 낮추면서 trades(거래 수)를 크게 회복한 v2-native evidence(브이투 고유 근거).
- judgment_label(판정 라벨): `quality_strong_density_and_dd_gap_remain`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

## Decision(판정)

decision(판정): `{DECISION}`

Effect(효과): Stage118(118단계)은 threshold-only density recovery(임계값만 낮추는 밀도 회복)를 반복하지 않고, DD compression(손실률 압축)을 먼저 보되 PF/net(수익 팩터/순손익)과 density(밀도)를 지키는 좁은 수리로 간다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage117 Decision(117단계 판정)

decision(판정): `{DECISION}`

Stage117(117단계)는 Stage116(116단계)의 actual MT5 runtime evidence(실제 MT5 실행환경 근거)를 검토했다.

Effect(효과): Stage116은 PF/net(수익 팩터/순손익)은 강하지만, 거래 수와 DD%(손실률)가 34D 목표와 Stage110 reference(참조점)에 아직 부족하므로 Stage118(118단계)로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- source_stage116_report(원천 116단계 보고서): `{rel(STAGE116_REPORT)}`
- source_stage116_decision(원천 116단계 판정): `{rel(STAGE116_DECISION)}`
- source_stage116_closeout_commit(원천 116단계 종료 커밋): `{SOURCE_STAGE116_CLOSEOUT_COMMIT}`
- source_stage116_latest_commit(원천 116단계 최신 커밋): `{SOURCE_STAGE116_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage117(117단계)는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 향한 v2-native research(브이투 고유 연구)는 Stage118(118단계)로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def write_ledgers(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best_quality = best_stage116_quality(rows)
    best_density = best_stage116_density(rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_density_quality_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage116_closeout_commit", SOURCE_STAGE116_CLOSEOUT_COMMIT),
                        ("source_stage116_latest_commit", SOURCE_STAGE116_LATEST_COMMIT),
                        ("best_quality", best_quality.get("adapter_id")),
                        ("best_density", best_density.get("adapter_id")),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage117_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage117_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage116_mt5_runtime_evidence_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage117_density_quality_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_quality", best_quality.get("adapter_id")),
                    ("best_quality_trades", best_quality.get("trade_count")),
                    ("best_quality_pf", best_quality.get("profit_factor")),
                    ("best_quality_dd", best_quality.get("max_drawdown_percent")),
                    ("best_density", best_density.get("adapter_id")),
                    ("best_density_trades", best_density.get("trade_count")),
                )
            ),
            "guardrail_kpi": f"target_surface={TARGET_SURFACE};decision={DECISION}",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage117 review only; no new MT5 execution; no operational claim.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows(),
        key="artifact_id",
    )
    return {
        "run_registry": run_payload,
        "alpha_ledger": alpha_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows: list[dict[str, Any]] = []
    for path in (REPORT_PATH, COMPARISON_PATH, TRADEOFF_PATH, DECISION_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage117_density_quality_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage117 density quality follow-up review artifact; research only.",
                }
            )
    return rows


def write_packet_files(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]], risk: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    best_quality = best_stage116_quality(rows)
    best_density = best_stage116_density(rows)
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "performance_attribution",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-result-judgment", "obsidian-artifact-lineage"],
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "artifact_lineage_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "source_stage116_summary": rel(STAGE116_SUMMARY),
            "source_stage116_segments": rel(STAGE116_SEGMENTS),
            "source_stage116_risk_atr": rel(STAGE116_RISK_ATR),
            "external_verification_status": EXTERNAL_STATUS,
            "status": "passed_for_followup_review",
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "decision": DECISION,
            "judgment_label": "quality_strong_density_and_dd_gap_remain",
            "overall_goal_complete": False,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
                "legacy_inheritance",
            ],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage116_closeout_commit": SOURCE_STAGE116_CLOSEOUT_COMMIT,
            "source_stage116_latest_commit": SOURCE_STAGE116_LATEST_COMMIT,
            "best_stage116_quality": best_quality,
            "best_stage116_density": best_density,
            "risk_atr_summary": risk,
            "tradeoff_rows": list(tradeoffs),
            "ledger_payload": ledger_payload,
            "overall_goal_complete": False,
            "pushed_commit_hash": "pending_until_push",
        },
    )


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage118(118단계)은 Stage117(117단계)의 판정대로 DD compression(손실률 압축)과 density preservation(밀도 보존)을 좁게 수리한다.

## Bounded Question(경계 질문)

Stage116(116단계)의 strong PF/net(강한 수익 팩터/순손익)을 크게 훼손하지 않으면서 DD%(손실률)를 Stage110 reference(110단계 참조점) 이하 또는 34D target(34D 목표)에 더 가깝게 압축할 수 있는가?

Effect(효과): Stage118(118단계)은 새 모델 hunting(모델 탐색)이 아니라 DD guard(손실률 방어), entry context(진입 문맥), hold/exit shape(보유/청산 형태) 중 하나의 좁은 축으로 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage118 Input References(118단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage117_report(117단계 보고서): `{rel(REPORT_PATH)}`
- stage117_comparison(117단계 비교): `{rel(COMPARISON_PATH)}`
- stage116_summary(116단계 요약): `{rel(STAGE116_SUMMARY)}`
- stage116_segments(116단계 구간): `{rel(STAGE116_SEGMENTS)}`
- stage116_risk_atr(116단계 위험/ATR): `{rel(STAGE116_RISK_ATR)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage118(118단계)은 Stage116/117 근거에서 출발하고 legacy inheritance(레거시 상속)는 하지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage118 Review Index(118단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage118(118단계)은 Stage117 closeout(종료 기록)을 이어받아 bounded repair(경계 수리)를 수행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage118 Selection Status(118단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage118(118단계)은 34D KPI(34D 핵심 성과 지표) 격차를 계속 줄이지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage117(117단계) closed(종료) as `{DECISION}` and Stage118(118단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): Stage116의 PF/net(수익 팩터/순손익)은 강하지만 DD%(손실률)와 density(밀도) 격차가 남아 DD compression(손실률 압축) 수리로 넘긴다.
- >-
  Stage117 result(117단계 결과)는 `{rel(COMPARISON_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록했다. Effect(효과): Stage114/116/34D KPI(핵심 성과 지표) 차이를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage117_v41_density_quality_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage116_closeout_commit: {SOURCE_STAGE116_CLOSEOUT_COMMIT}
  source_stage116_latest_commit: {SOURCE_STAGE116_LATEST_COMMIT}
  source_stage114_latest_commit: {SOURCE_STAGE114_LATEST_COMMIT}
  source_stage110_latest_commit: {SOURCE_STAGE110_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage117_v41_density_quality_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage117_v41_density_quality_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage117 Selection Status(117단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE116_ID}`
- source_decision(원천 판정): `continue_density_quality_followup_review_in_stage117`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage117_decision(117단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage117(117단계)는 기존 실행 결과를 판독하고, 운영 의미 없이 Stage118(118단계)로 넘긴다.
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage118_dd_compression_density_repair_surface`
- status(상태): `stage117_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage117(117단계) closed(종료) as v2-native v41 density quality follow-up review(브이투 고유 브이41 밀도 품질 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage118(118단계) DD compression density repair(손실률 압축 밀도 수리)로 이어진다.

## Latest Stage117 Evidence(최신 117단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage117 v41 density-quality follow-up review closeout(117단계 v41 밀도-품질 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage116(116단계) 결과를 34D KPI(핵심 성과 지표)와 Stage114/110 참조점에 대고 판정하고, DD compression density repair(손실률 압축 밀도 수리)를 Stage118(118단계)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = comparison_rows()
    tradeoffs = tradeoff_rows(rows)
    risk = risk_atr_summary()
    comparison_columns = (
        "run_id",
        "source_stage",
        "source_run_id",
        "adapter_id",
        "split",
        "profit_factor",
        "net_profit",
        "max_drawdown_percent",
        "trade_count",
        "expectancy",
        "cost_stressed_expectancy",
        "same_move_reentry_ratio",
        "mfe_capture_ratio",
        "early_net_profit",
        "early_profit_factor",
        "mid_net_profit",
        "mid_profit_factor",
        "late_net_profit",
        "late_profit_factor",
        "pf_gap_to_34d",
        "net_gap_to_34d",
        "dd_gap_to_34d",
        "trade_count_gap_to_34d",
        "dd_gap_to_stage110",
        "stage116_anchor_adapter",
        "trade_count_delta_vs_stage114_anchor",
        "pf_delta_vs_stage114_anchor",
        "net_delta_vs_stage114_anchor",
        "dd_delta_vs_stage114_anchor",
        "stage117_read",
    )
    tradeoff_columns = (
        "run_id",
        "adapter_id",
        "stage116_anchor_adapter",
        "trade_count",
        "profit_factor",
        "net_profit",
        "max_drawdown_percent",
        "trade_count_delta_vs_stage114_anchor",
        "pf_delta_vs_stage114_anchor",
        "net_delta_vs_stage114_anchor",
        "dd_delta_vs_stage114_anchor",
        "trade_count_gap_to_34d",
        "dd_gap_to_34d",
        "dd_gap_to_stage110",
        "read",
        "next_probe",
    )
    write_csv(COMPARISON_PATH, rows, comparison_columns)
    write_csv(TRADEOFF_PATH, tradeoffs, tradeoff_columns)
    write_md(REPORT_PATH, report_markdown(rows, tradeoffs, risk))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers(rows)
    write_packet_files(rows, tradeoffs, risk, ledger_payload)
    update_current_truth()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "external_verification_status": EXTERNAL_STATUS,
                    "report_path": rel(REPORT_PATH),
                    "decision_path": rel(DECISION_PATH),
                    "next_stage": NEXT_STAGE_ID,
                    "best_stage116_quality": best_stage116_quality(rows).get("adapter_id"),
                    "best_stage116_density": best_stage116_density(rows).get("adapter_id"),
                    "risk_atr_summary": risk,
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
