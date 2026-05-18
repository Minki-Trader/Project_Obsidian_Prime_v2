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


STAGE_ID = "125_adapter_research__v41_route_supply_followup_review_after_stage124"
RUN_ID = "run125A_stage125_v41_route_supply_followup_review_after_stage124_v1"
PACKET_ID = "stage125_v41_route_supply_followup_review_after_stage124_v1"
PARENT_RUN_ID = "run124A_stage124_v41_route_supply_density_repair_after_small_gain_v1"
SOURCE_STAGE124_ID = "124_adapter_research__v41_route_supply_density_repair_after_small_gain"
SOURCE_STAGE124_CLOSEOUT_COMMIT = "8a8a3c1d8b4355c116d1602ee6f444e65333fd91"
SOURCE_STAGE124_LATEST_COMMIT = "0e79bb6129abcd37032a925cded784cf775cc609"
SOURCE_STAGE123_LATEST_COMMIT = "410d29cb988af0d3a522201f5491fc8168405f7a"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_shortgate_quality_repair_in_stage126_after_route_supply_damage"
NEXT_STAGE_ID = "126_adapter_research__v41_shortgate_quality_repair_after_route_supply_damage"
NEXT_RUN_ID = "run126A_stage126_v41_shortgate_quality_repair_after_route_supply_damage_v1"
NEXT_PACKET_ID = "stage126_v41_shortgate_quality_repair_after_route_supply_damage_v1"
EXTERNAL_STATUS = "completed_existing_stage124_mt5_runtime_evidence_reviewed"
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
STAGE122_SOURCE = {
    "adapter_id": "s122_v41_h3_cd5_session_margin_risk035_sht54_lng52",
    "profit_factor": 1.75,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE124_ID / "03_reviews"
SOURCE_REPORT = SOURCE_REVIEWS / "stage124_route_supply_density_repair_report.md"
SOURCE_DECISION = SOURCE_REVIEWS / "stage124_decision.md"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage124_route_supply_density_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage124_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage124_risk_atr_telemetry.csv"
SOURCE_GATES = SOURCE_REVIEWS / "stage124_gate_feature_summary.csv"

REPORT_PATH = REVIEWS_ROOT / "stage125_route_supply_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage125_stage122_stage124_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage125_route_supply_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage125_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


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


def source_rows(split: str) -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SOURCE_SUMMARY)
        if row.get("split") == split
        and row.get("view") == "actual_routed_total"
        and row.get("status") == "completed"
    ]


def segment_row(adapter_id: str, split: str, segment: str) -> dict[str, str]:
    for row in read_csv(SOURCE_SEGMENTS):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") == split and row.get("view") == "actual_routed_total" and row.get("segment") == segment:
            return row
    return {}


def risk_row(adapter_id: str, split: str) -> dict[str, str]:
    for row in read_csv(SOURCE_RISK_ATR):
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def gate_row(adapter_id: str, split: str) -> dict[str, str]:
    for row in read_csv(SOURCE_GATES):
        if row.get("variant_id") == adapter_id and row.get("split") == split:
            return row
    return {}


def metric(row: Mapping[str, str], val_by_adapter: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    adapter_id = str(row.get("adapter_id", ""))
    val = val_by_adapter.get(adapter_id, {})
    early = segment_row(adapter_id, "oos", "early")
    mid = segment_row(adapter_id, "oos", "mid")
    late = segment_row(adapter_id, "oos", "late")
    risk = risk_row(adapter_id, "oos")
    gate = gate_row(adapter_id, "oos")
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    trades = num(row, "trade_count")
    return {
        "run_id": RUN_ID,
        "adapter_id": adapter_id,
        "repair_label": row.get("repair_label", ""),
        "gate_block_mode": gate.get("block_mode", ""),
        "gate_blocked_rows": num(gate, "blocked_rows"),
        "gate_blocked_ratio": num(gate, "blocked_ratio"),
        "stage122_source_adapter_id": STAGE122_SOURCE["adapter_id"],
        "stage122_source_profit_factor": STAGE122_SOURCE["profit_factor"],
        "stage122_source_net_profit": STAGE122_SOURCE["net_profit"],
        "stage122_source_max_drawdown_percent": STAGE122_SOURCE["max_drawdown_percent"],
        "stage122_source_trade_count": STAGE122_SOURCE["trade_count"],
        "validation_profit_factor": num(val, "profit_factor"),
        "validation_net_profit": num(val, "net_profit"),
        "validation_max_drawdown_percent": num(val, "max_drawdown_percent"),
        "validation_trade_count": num(val, "trade_count"),
        "oos_profit_factor": pf,
        "oos_net_profit": net,
        "oos_max_drawdown_percent": dd,
        "oos_trade_count": trades,
        "oos_cost_stressed_expectancy": num(row, "cost_stressed_expectancy"),
        "same_move_reentry_ratio": num(row, "same_move_reentry_ratio"),
        "mfe_capture_ratio": num(row, "mfe_capture_ratio"),
        "early_profit_factor": num(early, "profit_factor"),
        "early_net_profit": num(early, "net_profit"),
        "early_trade_count": num(early, "trade_count"),
        "mid_profit_factor": num(mid, "profit_factor"),
        "mid_net_profit": num(mid, "net_profit"),
        "mid_trade_count": num(mid, "trade_count"),
        "late_profit_factor": num(late, "profit_factor"),
        "late_net_profit": num(late, "net_profit"),
        "late_trade_count": num(late, "trade_count"),
        "trade_gain_vs_stage122_source": trades - STAGE122_SOURCE["trade_count"],
        "pf_delta_vs_stage122_source": pf - STAGE122_SOURCE["profit_factor"],
        "net_delta_vs_stage122_source": net - STAGE122_SOURCE["net_profit"],
        "dd_delta_vs_stage122_source": dd - STAGE122_SOURCE["max_drawdown_percent"],
        "pf_gap_to_34d": pf - LEGACY_34D["profit_factor"],
        "net_gap_to_34d": net - LEGACY_34D["net_profit"],
        "dd_gap_to_34d": dd - LEGACY_34D["max_drawdown_percent"],
        "trade_count_gap_to_34d": trades - LEGACY_34D["trade_count"],
        "risk_floor_applied_count": num(risk, "risk_floor_applied_count"),
        "max_model_risk_pct": num(risk, "max_model_risk_pct"),
        "max_actual_risk_pct_after_floor": num(risk, "max_actual_risk_pct_after_floor"),
        "risk_bucket": risk.get("risk_bucket", ""),
    }


def read_metric(row: Mapping[str, Any]) -> str:
    pf = num(row, "oos_profit_factor")
    net = num(row, "oos_net_profit")
    dd = num(row, "oos_max_drawdown_percent")
    gain = num(row, "trade_gain_vs_stage122_source")
    if gain >= 20 and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= 16.0:
        return "material_density_gain_quality_preserved"
    if gain > 0 and pf >= 1.45 and dd <= 22.0:
        return "salvageable_density_gain_quality_damaged"
    if gain > 0:
        return "density_gain_with_large_quality_damage"
    return "no_density_gain"


def build_rows() -> list[dict[str, Any]]:
    val_by_adapter = {row.get("adapter_id", ""): row for row in source_rows("validation_is")}
    rows = [metric(row, val_by_adapter) for row in source_rows("oos")]
    for row in rows:
        row["stage125_read"] = read_metric(row)
    return rows


def best_density(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: num(row, "oos_trade_count"), default={})


def best_salvage(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            str(row.get("stage125_read")) == "salvageable_density_gain_quality_damaged",
            num(row, "oos_profit_factor"),
            -num(row, "oos_max_drawdown_percent"),
            num(row, "oos_trade_count"),
        ),
        default={},
    )


def comparison_columns() -> list[str]:
    return [
        "run_id",
        "adapter_id",
        "repair_label",
        "gate_block_mode",
        "gate_blocked_rows",
        "gate_blocked_ratio",
        "stage122_source_adapter_id",
        "stage122_source_profit_factor",
        "stage122_source_net_profit",
        "stage122_source_max_drawdown_percent",
        "stage122_source_trade_count",
        "validation_profit_factor",
        "validation_net_profit",
        "validation_max_drawdown_percent",
        "validation_trade_count",
        "oos_profit_factor",
        "oos_net_profit",
        "oos_max_drawdown_percent",
        "oos_trade_count",
        "oos_cost_stressed_expectancy",
        "same_move_reentry_ratio",
        "mfe_capture_ratio",
        "early_profit_factor",
        "early_net_profit",
        "early_trade_count",
        "mid_profit_factor",
        "mid_net_profit",
        "mid_trade_count",
        "late_profit_factor",
        "late_net_profit",
        "late_trade_count",
        "trade_gain_vs_stage122_source",
        "pf_delta_vs_stage122_source",
        "net_delta_vs_stage122_source",
        "dd_delta_vs_stage122_source",
        "pf_gap_to_34d",
        "net_gap_to_34d",
        "dd_gap_to_34d",
        "trade_count_gap_to_34d",
        "risk_floor_applied_count",
        "max_model_risk_pct",
        "max_actual_risk_pct_after_floor",
        "risk_bucket",
        "stage125_read",
    ]


def formatted_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    int_cols = {"gate_blocked_rows", "stage122_source_trade_count", "validation_trade_count", "oos_trade_count", "early_trade_count", "mid_trade_count", "late_trade_count", "trade_gain_vs_stage122_source", "trade_count_gap_to_34d", "risk_floor_applied_count"}
    money_cols = {"stage122_source_net_profit", "validation_net_profit", "oos_net_profit", "early_net_profit", "mid_net_profit", "late_net_profit", "net_delta_vs_stage122_source", "net_gap_to_34d"}
    output = []
    for row in rows:
        out: dict[str, Any] = {}
        for col in comparison_columns():
            value = row.get(col, "")
            if isinstance(value, float):
                out[col] = fmt(value, 0) if col in int_cols else fmt(value, 2) if col in money_cols else fmt(value)
            else:
                out[col] = value
        output.append(out)
    return output


def tradeoff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        read = str(row.get("stage125_read", ""))
        if read == "salvageable_density_gain_quality_damaged":
            next_probe = "repair_shortgate_quality_not_more_nogate_supply"
        elif read == "density_gain_with_large_quality_damage":
            next_probe = "preserve_density_damage_failure_memory"
        elif read == "material_density_gain_quality_preserved":
            next_probe = "open_full_equity_segment_review"
        else:
            next_probe = "no_route_supply_followup"
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "gate_block_mode": row.get("gate_block_mode", ""),
                "oos_profit_factor": fmt(num(row, "oos_profit_factor")),
                "oos_net_profit": fmt(num(row, "oos_net_profit"), 2),
                "oos_max_drawdown_percent": fmt(num(row, "oos_max_drawdown_percent")),
                "oos_trade_count": fmt(num(row, "oos_trade_count"), 0),
                "trade_gain_vs_stage122_source": fmt(num(row, "trade_gain_vs_stage122_source"), 0),
                "pf_delta_vs_stage122_source": fmt(num(row, "pf_delta_vs_stage122_source")),
                "net_delta_vs_stage122_source": fmt(num(row, "net_delta_vs_stage122_source"), 2),
                "dd_delta_vs_stage122_source": fmt(num(row, "dd_delta_vs_stage122_source")),
                "trade_count_gap_to_34d": fmt(num(row, "trade_count_gap_to_34d"), 0),
                "read": read,
                "next_probe": next_probe,
            }
        )
    return output


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | gate(게이트) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | gain(증가) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {gate} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} | {read} |".format(
                adapter=row.get("adapter_id", ""),
                gate=row.get("gate_block_mode", ""),
                pf=num(row, "oos_profit_factor"),
                net=num(row, "oos_net_profit"),
                dd=num(row, "oos_max_drawdown_percent"),
                trades=num(row, "oos_trade_count"),
                gain=num(row, "trade_gain_vs_stage122_source"),
                read=row.get("stage125_read", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]]) -> str:
    density = best_density(rows)
    salvage = best_salvage(rows)
    tradeoff_text = "\n".join(
        f"- `{row.get('adapter_id')}`: {row.get('read')} -> {row.get('next_probe')}" for row in tradeoffs
    )
    return f"""# Stage125 Route Supply Follow-up Review(125단계 경로 공급 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE124_ID}`
- source_stage124_closeout_commit(원천 124단계 종료 커밋): `{SOURCE_STAGE124_CLOSEOUT_COMMIT}`
- source_stage124_latest_commit(원천 124단계 최신 커밋): `{SOURCE_STAGE124_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage124(124단계)의 route supply(경로 공급) 증가는 PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록)를 보존했는가?

Effect(효과): Stage125(125단계)는 새 실험을 하지 않고 Stage124 evidence(근거)만 읽어 다음 bounded repair(경계 수리)를 정한다.

## Result Table(결과표)

{markdown_table(rows)}

## Plain Read(쉬운 판독)

- best_density(최대 밀도): `{density.get('adapter_id', '')}` with trades(거래 수) `{num(density, 'oos_trade_count'):.0f}`, PF `{num(density, 'oos_profit_factor'):.2f}`, DD `{num(density, 'oos_max_drawdown_percent'):.2f}`.
- best_salvage(회수 단서): `{salvage.get('adapter_id', '')}` with trades(거래 수) `{num(salvage, 'oos_trade_count'):.0f}`, PF `{num(salvage, 'oos_profit_factor'):.2f}`, DD `{num(salvage, 'oos_max_drawdown_percent'):.2f}`.
- meaning(의미): no-gate(무게이트)는 거래 수를 343건까지 늘렸지만 PF/net/DD가 크게 망가졌다. shortgate(숏 게이트)는 230건으로 덜 망가졌지만 아직 34D KPI(핵심 성과 지표)에 못 미친다.

## Tradeoff Notes(트레이드오프 메모)

{tradeoff_text}

## Judgment(판정)

- result_subject(판정 대상): Stage124 route supply density repair(124단계 경로 공급 밀도 수리).
- evidence_available(있는 근거): Stage124 MT5 runtime summaries(MT5 실행환경 요약), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): shortgate quality repair(숏 게이트 품질 수리) 후의 검증/표본외 안정성.
- judgment_label(판정 라벨): `route_supply_density_gain_quality_damaged`.
- claim_boundary(주장 경계): `{BOUNDARY}`.
- next_condition(다음 조건): Stage126(126단계)에서 shortgate(숏 게이트) 밀도 증가를 보존하면서 PF/net/DD를 회복할 수 있는지 본다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage125 Decision(125단계 판정)

decision(판정): `{DECISION}`

Stage125(125단계)는 Stage124(124단계)의 route supply(경로 공급) 결과를 검토했다.

Effect(효과): no-gate(무게이트) 확장은 밀도는 늘렸지만 PF/net/DD(수익 팩터/순손익/손실률)를 크게 손상했고, shortgate(숏 게이트)만 회수 단서로 남긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- source_stage124_report(원천 124단계 보고서): `{rel(SOURCE_REPORT)}`
- source_stage124_decision(원천 124단계 판정): `{rel(SOURCE_DECISION)}`
- source_stage124_closeout_commit(원천 124단계 종료 커밋): `{SOURCE_STAGE124_CLOSEOUT_COMMIT}`
- source_stage124_latest_commit(원천 124단계 최신 커밋): `{SOURCE_STAGE124_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage125(125단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research/development(브이투 고유 연구개발)는 Stage126(126단계) shortgate quality repair(숏 게이트 품질 수리)로 이어진다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows = []
    for path in [REPORT_PATH, COMPARISON_PATH, TRADEOFF_PATH, DECISION_PATH, STAGE_LEDGER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage125_route_supply_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage125 v2-native route supply follow-up review artifact.",
                }
            )
    return rows


def write_ledgers(rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    salvage = best_salvage(rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_route_supply_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage124_closeout_commit", SOURCE_STAGE124_CLOSEOUT_COMMIT),
                        ("source_stage124_latest_commit", SOURCE_STAGE124_LATEST_COMMIT),
                        ("salvage_adapter", salvage.get("adapter_id")),
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
            "ledger_row_id": f"{RUN_ID}__stage125_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage125_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage124_mt5_runtime_evidence_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage125_route_supply_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("salvage_adapter", salvage.get("adapter_id")),
                    ("pf", salvage.get("oos_profit_factor")),
                    ("net", salvage.get("oos_net_profit")),
                    ("dd", salvage.get("oos_max_drawdown_percent")),
                    ("trades", salvage.get("oos_trade_count")),
                )
            ),
            "guardrail_kpi": f"target_surface={TARGET_SURFACE};decision={DECISION};overall_goal_complete=false",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage125 review only; no new MT5 execution; no operational claim.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    salvage = best_salvage(rows)
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "result_judgment", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"], "required_gates": ["kpi_contract_audit", "result_judgment_gate", "artifact_lineage_gate"], "status": "completed"})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "source_stage124_summary": rel(SOURCE_SUMMARY), "source_stage124_segments": rel(SOURCE_SEGMENTS), "source_stage124_risk_atr": rel(SOURCE_RISK_ATR), "source_stage124_gates": rel(SOURCE_GATES), "comparison_path": rel(COMPARISON_PATH), "tradeoff_path": rel(TRADEOFF_PATH), "status": "passed_review_only"})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": DECISION, "judgment_label": "route_supply_density_gain_quality_damaged", "salvage_adapter": salvage, "overall_goal_complete": False})
    write_json(PACKET_ROOT / "artifact_lineage_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_GATES)], "producer": rel(Path("stage_pipelines/stage125/v41_route_supply_followup_review_after_stage124.py")), "artifact_paths": [rel(REPORT_PATH), rel(COMPARISON_PATH), rel(TRADEOFF_PATH), rel(DECISION_PATH), rel(STAGE_LEDGER_PATH)], "availability": "tracked_after_stage_boundary_commit", "lineage_judgment": "connected_with_boundary"})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "source_stage124_closeout_commit": SOURCE_STAGE124_CLOSEOUT_COMMIT, "source_stage124_latest_commit": SOURCE_STAGE124_LATEST_COMMIT, "salvage_adapter": salvage.get("adapter_id"), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "overall_goal_complete": False})


def create_next_stage() -> None:
    write_md(NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage126(126단계)는 Stage125(125단계)의 판정대로 shortgate(숏 게이트) 경로 공급 단서를 품질 수리한다.

## Bounded Question(경계 질문)

Stage124 shortgate(124단계 숏 게이트)의 거래 수 증가를 일부 보존하면서 PF/net/DD(수익 팩터/순손익/손실률)를 34D KPI(핵심 성과 지표)에 더 가깝게 회복할 수 있는가?

Effect(효과): Stage126(126단계)는 no-gate(무게이트) 확장을 반복하지 않고, 회수 가능성이 가장 큰 shortgate(숏 게이트) 표면만 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""")
    write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage126 Input References(126단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage125_report(125단계 보고서): `{rel(REPORT_PATH)}`
- stage125_tradeoff(125단계 트레이드오프): `{rel(TRADEOFF_PATH)}`
- stage124_summary(124단계 요약): `{rel(SOURCE_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage126 Review Index(126단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
""")
    write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage126 Selection Status(126단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage125(125단계) closed(종료) as `{DECISION}` and Stage126(126단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): route supply(경로 공급)는 no-gate(무게이트)가 아니라 shortgate(숏 게이트) 품질 수리로 좁힌다.
- >-
  Stage125 result(125단계 결과)는 `{rel(REPORT_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록했다. Effect(효과): Stage124의 거래 수 증가는 품질 손상을 동반했다는 실패 기억을 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage125_v41_route_supply_followup_review_after_stage124:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage124_closeout_commit: {SOURCE_STAGE124_CLOSEOUT_COMMIT}
  source_stage124_latest_commit: {SOURCE_STAGE124_LATEST_COMMIT}
  source_stage123_latest_commit: {SOURCE_STAGE123_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage125_v41_route_supply_followup_review_after_stage124:"
    if marker in text:
        text = re.sub(r"\nstage125_v41_route_supply_followup_review_after_stage124:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage125 Selection Status(125단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE124_ID}`
- source_decision(원천 판정): `continue_route_supply_followup_review_in_stage125_due_to_damage_or_no_gain`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage125_decision(125단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage125 Review Index(125단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
""")
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage126_shortgate_quality_repair_surface`
- status(상태): `stage125_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage125(125단계) closed(종료) as v2-native v41 route supply follow-up review(브이투 고유 브이41 경로 공급 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage126(126단계) shortgate quality repair(숏 게이트 품질 수리)로 이어진다.

## Latest Stage125 Evidence(최신 125단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage125 v41 route supply follow-up review closeout(125단계 v41 경로 공급 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage124 no-gate(무게이트) 밀도 확장의 품질 손상을 기록하고 shortgate(숏 게이트) 품질 수리로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = build_rows()
    tradeoffs = tradeoff_rows(rows)
    write_csv(COMPARISON_PATH, formatted_rows(rows), comparison_columns())
    write_csv(TRADEOFF_PATH, tradeoffs, ["run_id", "adapter_id", "gate_block_mode", "oos_profit_factor", "oos_net_profit", "oos_max_drawdown_percent", "oos_trade_count", "trade_gain_vs_stage122_source", "pf_delta_vs_stage122_source", "net_delta_vs_stage122_source", "dd_delta_vs_stage122_source", "trade_count_gap_to_34d", "read", "next_probe"])
    write_md(REPORT_PATH, report_markdown(rows, tradeoffs))
    write_md(DECISION_PATH, decision_markdown())
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(rows, artifacts)
    write_packet_files(rows, ledger_payload)
    update_current_truth()
    append_changelog()
    print(json.dumps({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "report": rel(REPORT_PATH)}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
