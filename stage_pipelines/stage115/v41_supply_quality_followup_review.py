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


STAGE_ID = "115_adapter_research__v41_supply_quality_followup_review"
RUN_ID = "run115A_stage115_v41_supply_quality_followup_review_v1"
PACKET_ID = "stage115_v41_supply_quality_followup_review_v1"
PARENT_RUN_ID = "run114A_stage114_v41_supply_quality_filter_repair_v1"
SOURCE_STAGE114_ID = "114_adapter_research__v41_supply_quality_filter_repair"
SOURCE_STAGE114_CLOSEOUT_COMMIT = "0d85a7466233f2c6f7f035cc597e191d5820608e"
SOURCE_STAGE114_LATEST_COMMIT = "19778c1e66346dcef4ce8e455c5b5960cfa1e1e7"
SOURCE_STAGE112_LATEST_COMMIT = "defeb9257037327717105cac64b509ccf690e073"
SOURCE_STAGE110_LATEST_COMMIT = "c702502f01e2ef0e9a17d2ac9ec86b6108a82d04"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_density_quality_balance_repair_in_stage116"
NEXT_STAGE_ID = "116_adapter_research__v41_density_quality_balance_repair"
NEXT_RUN_ID = "run116A_stage116_v41_density_quality_balance_repair_v1"
NEXT_PACKET_ID = "stage116_v41_density_quality_balance_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage114_mt5_runtime_evidence_reviewed"
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
    "early_net_profit": 38.84,
    "early_profit_factor": 1.157011764,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE112_REVIEWS = Path("stages/112_adapter_research__v41_route_supply_density_repair/03_reviews")
SOURCE_STAGE112_SUMMARY = SOURCE_STAGE112_REVIEWS / "stage112_route_supply_density_summary.csv"
SOURCE_STAGE112_SEGMENTS = SOURCE_STAGE112_REVIEWS / "stage112_segment_kpi_summary.csv"
SOURCE_STAGE114_REVIEWS = Path("stages") / SOURCE_STAGE114_ID / "03_reviews"
SOURCE_STAGE114_SUMMARY = SOURCE_STAGE114_REVIEWS / "stage114_supply_quality_filter_summary.csv"
SOURCE_STAGE114_SEGMENTS = SOURCE_STAGE114_REVIEWS / "stage114_segment_kpi_summary.csv"
SOURCE_STAGE114_GATE_SUMMARY = SOURCE_STAGE114_REVIEWS / "stage114_gate_feature_summary.csv"
SOURCE_STAGE114_REPORT = SOURCE_STAGE114_REVIEWS / "stage114_supply_quality_filter_report.md"
SOURCE_STAGE114_DECISION = SOURCE_STAGE114_REVIEWS / "stage114_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage115_supply_quality_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage115_stage110_stage112_stage114_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage115_supply_quality_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage115_decision.md"
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


def source_metric(
    source_stage: str,
    source_run_id: str,
    adapter_id: str,
    summary_path: Path,
    segment_path: Path,
) -> dict[str, Any]:
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


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(STAGE110_REFERENCE)]
    rows.append(
        source_metric(
            "stage112_nogate_large_supply_quality_failure",
            "run112A_stage112_v41_route_supply_density_repair_v1",
            "s112_v41_h3_cd9_nogate_lng53",
            SOURCE_STAGE112_SUMMARY,
            SOURCE_STAGE112_SEGMENTS,
        )
    )
    for adapter_id in (
        "s114_v41_h3_cd9_rule_block_lng53",
        "s114_v41_h3_cd9_margin_mid_block_lng53",
        "s114_v41_h3_cd9_rule_margin_block_lng53",
        "s114_v41_h3_cd9_session_margin_block_lng53",
    ):
        rows.append(source_metric("stage114_supply_quality_filter", PARENT_RUN_ID, adapter_id, SOURCE_STAGE114_SUMMARY, SOURCE_STAGE114_SEGMENTS))
    return rows


def row_read(row: Mapping[str, Any]) -> str:
    source = str(row.get("source_stage", ""))
    adapter = str(row.get("adapter_id", ""))
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    trades = num(row, "trade_count")
    if source == "stage110_balanced_reference":
        return "reference_quality_good_but_density_and_34d_gap_remain"
    if "stage112_nogate" in source:
        return "supply_opened_but_pf_and_dd_failed"
    if adapter.endswith("rule_block_lng53"):
        return "density_preserved_net_strong_but_pf_below_34d"
    if adapter.endswith("margin_mid_block_lng53"):
        return "density_mid_net_near_34d_but_pf_and_dd_fail"
    if pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and trades < 180:
        return "quality_recovered_but_density_short"
    if dd > STAGE110_REFERENCE["max_drawdown_percent"]:
        return "dd_still_above_stage110_reference"
    return "requires_next_bounded_repair"


def comparison_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in source_rows():
        pf = num(source, "profit_factor")
        net = num(source, "net_profit")
        dd = num(source, "max_drawdown_percent")
        trades = num(source, "trade_count")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_stage": source.get("source_stage", ""),
                "source_run_id": source.get("source_run_id", ""),
                "adapter_id": source.get("adapter_id", ""),
                "split": "oos",
                "profit_factor": fmt(pf),
                "net_profit": fmt(net, 2),
                "max_drawdown_percent": fmt(dd),
                "trade_count": fmt(trades, 0),
                "expectancy": fmt(num(source, "expectancy")),
                "cost_stressed_expectancy": fmt(num(source, "cost_stressed_expectancy")),
                "same_move_reentry_ratio": fmt(num(source, "same_move_reentry_ratio")),
                "mfe_capture_ratio": fmt(num(source, "mfe_capture_ratio")),
                "early_net_profit": fmt(num(source, "early_net_profit"), 2),
                "early_profit_factor": fmt(num(source, "early_profit_factor")),
                "mid_net_profit": fmt(num(source, "mid_net_profit"), 2),
                "mid_profit_factor": fmt(num(source, "mid_profit_factor")),
                "late_net_profit": fmt(num(source, "late_net_profit"), 2),
                "late_profit_factor": fmt(num(source, "late_profit_factor")),
                "pf_gap_to_34d": fmt(pf - LEGACY_34D["profit_factor"]),
                "net_gap_to_34d": fmt(net - LEGACY_34D["net_profit"], 2),
                "dd_gap_to_34d": fmt(dd - LEGACY_34D["max_drawdown_percent"]),
                "trade_count_gap_to_34d": fmt(trades - LEGACY_34D["trade_count"], 0),
                "density_delta_vs_stage110": fmt(trades - STAGE110_REFERENCE["trade_count"], 0),
                "stage115_read": row_read(source),
            }
        )
    return rows


def tradeoff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for row in rows:
        adapter = str(row.get("adapter_id", ""))
        if not adapter.startswith("s114_"):
            continue
        trades = float(row["trade_count"])
        pf = float(row["profit_factor"])
        net = float(row["net_profit"])
        dd = float(row["max_drawdown_percent"])
        if adapter.endswith("rule_block_lng53"):
            route = "stage116_relax_rule_block_with_dd_guard_or_add_second_quality_axis"
        elif adapter.endswith("margin_mid_block_lng53"):
            route = "do_not_use_as_anchor_until_dd_repaired"
        elif adapter.endswith("rule_margin_block_lng53"):
            route = "stage116_try_density_recovery_from_quality_anchor"
        else:
            route = "stage116_try_session_margin_quality_anchor_density_recovery"
        result.append(
            {
                "run_id": RUN_ID,
                "adapter_id": adapter,
                "trade_count": fmt(trades, 0),
                "net_profit": fmt(net, 2),
                "profit_factor": fmt(pf),
                "max_drawdown_percent": fmt(dd),
                "density_delta_vs_stage110": row.get("density_delta_vs_stage110", ""),
                "pf_gap_to_34d": row.get("pf_gap_to_34d", ""),
                "net_gap_to_34d": row.get("net_gap_to_34d", ""),
                "dd_gap_to_34d": row.get("dd_gap_to_34d", ""),
                "trade_count_gap_to_34d": row.get("trade_count_gap_to_34d", ""),
                "read": row.get("stage115_read", ""),
                "next_route": route,
            }
        )
    return result


def best_density(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    stage114 = [row for row in rows if str(row.get("adapter_id", "")).startswith("s114_")]
    return max(stage114, key=lambda row: (float(row["trade_count"]), float(row["net_profit"]), float(row["profit_factor"])))


def best_quality(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    stage114 = [row for row in rows if str(row.get("adapter_id", "")).startswith("s114_")]
    return max(stage114, key=lambda row: (float(row["profit_factor"]), float(row["net_profit"]), -float(row["max_drawdown_percent"])))


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('source_stage','')} | {row.get('adapter_id','')} | {row.get('profit_factor','')} | {row.get('net_profit','')} | {row.get('max_drawdown_percent','')} | {row.get('trade_count','')} | {row.get('stage115_read','')} |"
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]]) -> str:
    density = best_density(rows)
    quality = best_quality(rows)
    return f"""# Stage115 Supply Quality Follow-up Review(115단계 공급 품질 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE114_ID}`
- source_stage114_closeout_commit(원천 114단계 종료 커밋): `{SOURCE_STAGE114_CLOSEOUT_COMMIT}`
- source_stage114_latest_commit(원천 114단계 최신 커밋): `{SOURCE_STAGE114_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage114(114단계)의 quality filter(품질 필터)가 Stage112 no-gate supply(무제한 공급) 대비 PF/DD(수익 팩터/손실률), 거래 수, 순손익, 초반 구간 품질을 실제로 개선했는가?

Effect(효과): Stage115(115단계)는 새 실행이 아니라 Stage114 실제 MT5 evidence(실제 MT5 근거)를 판독해 다음 bounded repair(경계 수리)를 고른다.

## Comparison(비교)

{markdown_table(rows)}

## Best Reads(최선 판독)

- density_preserver(밀도 보존): `{density.get('adapter_id')}` with trades(거래 수) `{density.get('trade_count')}`, net(순손익) `{density.get('net_profit')}`, PF(수익 팩터) `{density.get('profit_factor')}`, DD%(손실률) `{density.get('max_drawdown_percent')}`.
- quality_recovery(품질 회복): `{quality.get('adapter_id')}` with trades(거래 수) `{quality.get('trade_count')}`, net(순손익) `{quality.get('net_profit')}`, PF(수익 팩터) `{quality.get('profit_factor')}`, DD%(손실률) `{quality.get('max_drawdown_percent')}`.

## Read(판독)

- Stage114(114단계)는 Stage112 no-gate(무제한) 대비 PF(수익 팩터), net(순손익), DD(손실률)를 크게 개선했다.
- 그러나 34D(34D 목표 표면)의 trade count(거래 수) `404`와 DD%(손실률) `12.909136`에는 아직 멀다.
- `s114_v41_h3_cd9_session_margin_block_lng53`는 PF `1.810756`, net `2041.72`로 강하지만 trades(거래 수) `174`라 density(밀도)가 부족하다.
- `s114_v41_h3_cd9_rule_block_lng53`는 trades(거래 수) `253`과 net `1668.39`가 강하지만 PF `1.370076`이라 34D PF(수익 팩터)에는 못 미친다.

## Decision(판정)

decision(판정): `{DECISION}`

Effect(효과): Stage116(116단계)은 high-quality anchor(고품질 앵커)의 밀도를 회복하거나 density preserver(밀도 보존형)의 PF/DD(수익 팩터/손실률)를 보강하는 좁은 수리로 간다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage115 Decision(115단계 판정)

decision(판정): `{DECISION}`

Stage115(115단계)는 Stage114(114단계)의 actual MT5 runtime result(실제 MT5 실행환경 결과)를 후속 검토했다.

Effect(효과): Stage114는 품질 회복 단서를 만들었지만 34D trade density/DD(거래 밀도/손실률)에는 아직 부족하므로, Stage116(116단계)에서 density-quality balance repair(밀도-품질 균형 수리)를 좁게 수행한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- source_stage114_report(원천 114단계 보고서): `{rel(SOURCE_STAGE114_REPORT)}`
- source_stage114_decision(원천 114단계 판정): `{rel(SOURCE_STAGE114_DECISION)}`
- source_stage114_closeout_commit(원천 114단계 종료 커밋): `{SOURCE_STAGE114_CLOSEOUT_COMMIT}`
- source_stage114_latest_commit(원천 114단계 최신 커밋): `{SOURCE_STAGE114_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage115(115단계)는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 향한 v2-native research(브이투 고유 연구)는 Stage116(116단계)로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def write_ledgers(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    density = best_density(rows)
    quality = best_quality(rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_supply_quality_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage114_closeout_commit", SOURCE_STAGE114_CLOSEOUT_COMMIT),
                        ("source_stage114_latest_commit", SOURCE_STAGE114_LATEST_COMMIT),
                        ("density_preserver", density.get("adapter_id")),
                        ("quality_recovery", quality.get("adapter_id")),
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
            "ledger_row_id": f"{RUN_ID}__stage115_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage115_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage114_mt5_runtime_evidence_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage115_supply_quality_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("density_preserver", density.get("adapter_id")),
                    ("density_trades", density.get("trade_count")),
                    ("density_pf", density.get("profit_factor")),
                    ("quality_recovery", quality.get("adapter_id")),
                    ("quality_trades", quality.get("trade_count")),
                    ("quality_pf", quality.get("profit_factor")),
                )
            ),
            "guardrail_kpi": f"target_surface={TARGET_SURFACE};decision={DECISION}",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage115 review only; no new MT5 execution; no operational claim.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_rows = artifact_registry_rows()
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def artifact_registry_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows: list[dict[str, Any]] = []
    for path in (REPORT_PATH, COMPARISON_PATH, TRADEOFF_PATH, DECISION_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage115_supply_quality_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage115 supply quality follow-up review artifact; research only.",
                }
            )
    return rows


def write_packet_files(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    density = best_density(rows)
    quality = best_quality(rows)
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "performance_attribution", "primary_skill": "obsidian-performance-attribution", "support_skills": ["obsidian-result-judgment", "obsidian-experiment-design"], "required_gates": ["kpi_contract_audit", "result_judgment_gate"], "status": "completed"})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "decision": DECISION, "judgment_label": "quality_recovered_but_density_dd_gap_remains", "overall_goal_complete": False, "forbidden_claims": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "operating_reference", "runtime_authority", "legacy_inheritance"]})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "source_stage114_closeout_commit": SOURCE_STAGE114_CLOSEOUT_COMMIT, "source_stage114_latest_commit": SOURCE_STAGE114_LATEST_COMMIT, "density_preserver": density, "quality_recovery": quality, "tradeoff_rows": list(tradeoffs), "ledger_payload": ledger_payload, "overall_goal_complete": False, "pushed_commit_hash": "pending_until_push"})


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage116(116단계)는 Stage115(115단계)의 판정대로 density-quality balance repair(밀도-품질 균형 수리)를 좁게 수행한다.

## Bounded Question(경계 질문)

Stage114(114단계)의 high-quality filters(고품질 필터)에서 거래 수를 회복하거나, density-preserving filter(밀도 보존 필터)의 PF/DD(수익 팩터/손실률)를 보강해서 34D KPI(34D 핵심 성과 지표) 격차를 더 줄일 수 있는가?

Effect(효과): Stage116(116단계)은 새 모델 사냥(model hunting, 모델 탐색)이 아니라 Stage114의 두 좋은 단서 사이 균형을 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage116 Input References(116단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage115_report(115단계 보고서): `{rel(REPORT_PATH)}`
- stage115_comparison(115단계 비교): `{rel(COMPARISON_PATH)}`
- stage114_summary(114단계 요약): `{rel(SOURCE_STAGE114_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage116(116단계)는 Stage114/115 근거를 받아 거래 수와 품질 균형을 계속 밀어붙인다.
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage116 Review Index(116단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage116(116단계)는 Stage115(115단계) closeout(종료 기록)을 이어받아 bounded repair(경계 수리)를 수행한다.
""")
    write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage116 Selection Status(116단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage116(116단계)는 34D KPI(34D 핵심 성과 지표) 이상을 계속 노리지만 운영 의미 없이 연구개발로만 이어진다.
""")


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage115(115단계) closed(종료) as `{DECISION}` and Stage116(116단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): Stage114 품질 회복 단서를 density-quality balance repair(밀도-품질 균형 수리)로 넘긴다.
- >-
  Stage115 result(115단계 결과)는 `{rel(COMPARISON_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록했다. Effect(효과): 공급 보존형과 품질 회복형의 상충을 다음 단계 입력으로 고정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage115_v41_supply_quality_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage114_closeout_commit: {SOURCE_STAGE114_CLOSEOUT_COMMIT}
  source_stage114_latest_commit: {SOURCE_STAGE114_LATEST_COMMIT}
  source_stage112_latest_commit: {SOURCE_STAGE112_LATEST_COMMIT}
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
    marker = "stage115_v41_supply_quality_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage115_v41_supply_quality_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage115 Selection Status(115단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE114_ID}`
- source_decision(원천 판정): `continue_supply_quality_filter_repair_review_in_stage115`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage115_decision(115단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage115(115단계)는 실제 실행 결과를 판독하고, 운영 의미 없이 Stage116(116단계)로 넘긴다.
""")
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage116_density_quality_balance_repair_surface`
- status(상태): `stage115_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage115(115단계) closed(종료) as v2-native v41 supply quality follow-up review(브이투 고유 브이41 공급 품질 후속 검토). Effect(효과): Stage114 품질 회복 단서를 다음 연구인 Stage116(116단계) density-quality balance repair(밀도-품질 균형 수리)로 넘긴다.

## Latest Stage115 Evidence(최신 115단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage115 v41 supply quality follow-up review closeout(115단계 v41 공급 품질 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage114(114단계)의 공급 품질 필터 결과를 34D KPI(핵심 성과 지표) 대비 판독하고, 밀도-품질 균형 수리를 Stage116(116단계)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = comparison_rows()
    tradeoffs = tradeoff_rows(rows)
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
        "density_delta_vs_stage110",
        "stage115_read",
    )
    tradeoff_columns = (
        "run_id",
        "adapter_id",
        "trade_count",
        "net_profit",
        "profit_factor",
        "max_drawdown_percent",
        "density_delta_vs_stage110",
        "pf_gap_to_34d",
        "net_gap_to_34d",
        "dd_gap_to_34d",
        "trade_count_gap_to_34d",
        "read",
        "next_route",
    )
    write_csv(COMPARISON_PATH, rows, comparison_columns)
    write_csv(TRADEOFF_PATH, tradeoffs, tradeoff_columns)
    write_md(REPORT_PATH, report_markdown(rows, tradeoffs))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers(rows, tradeoffs)
    write_packet_files(rows, tradeoffs, ledger_payload)
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
