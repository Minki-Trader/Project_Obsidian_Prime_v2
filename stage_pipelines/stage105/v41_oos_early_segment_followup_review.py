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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "105_adapter_research__v41_oos_early_segment_followup_review"
RUN_ID = "run105A_stage105_v41_oos_early_segment_followup_review_v1"
PACKET_ID = "stage105_v41_oos_early_segment_followup_review_v1"
PARENT_RUN_ID = "run104A_stage104_v41_oos_early_segment_repair_v1"
SOURCE_STAGE104_ID = "104_adapter_research__v41_oos_early_segment_repair"
SOURCE_STAGE104_CLOSEOUT_COMMIT = "45400b9be01e87d5497aa3a96d1e229494e32444"
SOURCE_STAGE104_LATEST_COMMIT = "61778183dc73e327b612f58b70491a2f14408de2"
SOURCE_STAGE103_LATEST_COMMIT = "1f456de5dddadea119c5cb78c2b5d020f403c78d"
SOURCE_STAGE102_LATEST_COMMIT = "5ca329c468db459a8f68b9c28dd0897dfbf79623"
SOURCE_STAGE100_LATEST_COMMIT = "ef4b4ab1fbcb63a985512af5a6c49d199533e1fd"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_oos_net_density_dd_after_early_recovery_repair_in_stage106"
NEXT_STAGE_ID = "106_adapter_research__v41_oos_net_density_dd_after_early_recovery_repair"
NEXT_RUN_ID = "run106A_stage106_v41_oos_net_density_dd_after_early_recovery_repair_v1"
NEXT_PACKET_ID = "stage106_v41_oos_net_density_dd_after_early_recovery_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage104_mt5_runtime_evidence_reviewed"
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

STAGE100_BEST = {
    "source_stage": "stage100_best",
    "source_run_id": "run100A_stage100_v41_oos_early_context_gate_runtime_repair_v1",
    "adapter_id": "s100_v41_h3_cd8_lng_early_adx20",
    "profit_factor": 1.584029112,
    "net_profit": 605.06,
    "max_drawdown_percent": 18.69,
    "trade_count": 149,
    "expectancy": 4.060805369,
    "early_net_profit": 32.51,
    "early_profit_factor": 1.128143477,
    "early_mfe_capture_ratio": 0.06074909558,
}

STAGE102_BEST = {
    "source_stage": "stage102_best",
    "source_run_id": "run102A_stage102_v41_oos_net_density_dd_repair_v1",
    "adapter_id": "s102_v41_h3_cd8_lng_early_adx18",
    "profit_factor": 1.612695342,
    "net_profit": 639.85,
    "max_drawdown_percent": 18.56,
    "trade_count": 152,
    "expectancy": 4.209539474,
    "early_net_profit": 8.11,
    "early_profit_factor": 1.029162172,
    "early_mfe_capture_ratio": 0.01501486212,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE100_REVIEWS = Path("stages") / "100_adapter_research__v41_oos_early_context_gate_runtime_repair" / "03_reviews"
SOURCE_STAGE102_REVIEWS = Path("stages") / "102_adapter_research__v41_oos_net_density_dd_repair" / "03_reviews"
SOURCE_STAGE104_REVIEWS = Path("stages") / SOURCE_STAGE104_ID / "03_reviews"

SOURCE_STAGE100_SEGMENTS = SOURCE_STAGE100_REVIEWS / "stage100_segment_kpi_summary.csv"
SOURCE_STAGE102_SEGMENTS = SOURCE_STAGE102_REVIEWS / "stage102_segment_kpi_summary.csv"
SOURCE_STAGE104_SUMMARY = SOURCE_STAGE104_REVIEWS / "stage104_oos_early_segment_repair_summary.csv"
SOURCE_STAGE104_SEGMENTS = SOURCE_STAGE104_REVIEWS / "stage104_segment_kpi_summary.csv"
SOURCE_STAGE104_REPORT = SOURCE_STAGE104_REVIEWS / "stage104_oos_early_segment_repair_report.md"
SOURCE_STAGE104_DECISION = SOURCE_STAGE104_REVIEWS / "stage104_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage105_oos_early_segment_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage105_stage100_stage102_stage104_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage105_segment_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage105_decision.md"
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


def num(row: Mapping[str, Any], key: str) -> float | None:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value))
    except ValueError:
        return None


def fmt(value: float | None, digits: int = 6) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def stage104_full_rows() -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in read_csv(SOURCE_STAGE104_SEGMENTS):
        if row.get("split") != "oos":
            continue
        if row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == "full_split":
            output[row.get("adapter_id", "")] = row
    return output


def stage104_summary_rows() -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in read_csv(SOURCE_STAGE104_SUMMARY):
        if row.get("split") == "oos" and row.get("view") == "actual_routed_total":
            output[row.get("adapter_id", "")] = row
    return output


def early_lookup(path: Path, adapter_id: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") != "oos":
            continue
        if row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == "chronological_third" and row.get("segment") == "early":
            return row
    return {}


def source_metric_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [dict(STAGE100_BEST), dict(STAGE102_BEST)]
    full = stage104_full_rows()
    summary = stage104_summary_rows()
    for adapter_id in sorted(full):
        full_row = full[adapter_id]
        summary_row = summary.get(adapter_id, {})
        early = early_lookup(SOURCE_STAGE104_SEGMENTS, adapter_id)
        source_stage = "stage104_candidate"
        if adapter_id == "s104_v41_h3_cd8_lng_early_adx19":
            source_stage = "stage104_balanced_candidate"
        rows.append(
            {
                "source_stage": source_stage,
                "source_run_id": PARENT_RUN_ID,
                "adapter_id": adapter_id,
                "profit_factor": num(full_row, "profit_factor"),
                "net_profit": num(full_row, "net_profit"),
                "max_drawdown_percent": num(summary_row, "max_drawdown_percent"),
                "trade_count": num(full_row, "trade_count"),
                "expectancy": num(full_row, "expectancy"),
                "early_net_profit": num(early, "net_profit"),
                "early_profit_factor": num(early, "profit_factor"),
                "early_mfe_capture_ratio": num(early, "mfe_capture_ratio"),
            }
        )
    return rows


def row_read(row: Mapping[str, Any]) -> str:
    source = str(row.get("source_stage", ""))
    net = float(row.get("net_profit") or 0.0)
    pf = float(row.get("profit_factor") or 0.0)
    dd = float(row.get("max_drawdown_percent") or 0.0)
    early_net = float(row.get("early_net_profit") or 0.0)
    early_pf = float(row.get("early_profit_factor") or 0.0)
    if source == "stage100_best":
        return "reference_pf_meets_34d_but_net_dd_trade_density_gap_remains"
    if source == "stage102_best":
        return "full_oos_best_so_far_but_oos_early_degraded"
    early_recovered = early_net >= STAGE100_BEST["early_net_profit"] and early_pf >= STAGE100_BEST["early_profit_factor"]
    if early_recovered and net > STAGE100_BEST["net_profit"] and pf >= LEGACY_34D["profit_factor"] and dd > LEGACY_34D["max_drawdown_percent"]:
        return "early_recovered_full_oos_preserved_partly_but_34d_net_dd_gap_remains"
    if not early_recovered and net > STAGE100_BEST["net_profit"]:
        return "net_improves_but_early_repair_not_preserved"
    return "not_preferred_tradeoff"


def comparison_rows() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in source_metric_rows():
        pf = float(row.get("profit_factor") or 0.0)
        net = float(row.get("net_profit") or 0.0)
        dd = float(row.get("max_drawdown_percent") or 0.0)
        trades = float(row.get("trade_count") or 0.0)
        early_net = float(row.get("early_net_profit") or 0.0)
        early_pf = float(row.get("early_profit_factor") or 0.0)
        early_mfe = float(row.get("early_mfe_capture_ratio") or 0.0)
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
                "expectancy": fmt(float(row.get("expectancy") or 0.0), 6),
                "early_net_profit": fmt(early_net, 2),
                "early_profit_factor": fmt(early_pf),
                "early_mfe_capture_ratio": fmt(early_mfe),
                "pf_gap_to_34d_latest": fmt(pf - LEGACY_34D["profit_factor"]),
                "net_gap_to_34d_latest": fmt(net - LEGACY_34D["net_profit"], 2),
                "dd_gap_to_34d_latest": fmt(dd - LEGACY_34D["max_drawdown_percent"]),
                "trade_count_gap_to_34d_latest": fmt(trades - LEGACY_34D["trade_count"], 0),
                "net_delta_vs_stage100_best": fmt(net - STAGE100_BEST["net_profit"], 2),
                "net_delta_vs_stage102_best": fmt(net - STAGE102_BEST["net_profit"], 2),
                "early_net_delta_vs_stage102_best": fmt(early_net - STAGE102_BEST["early_net_profit"], 2),
                "stage105_read": row_read(row),
            }
        )
    return output


def segment_rows_for(path: Path, source_stage: str, adapter_id: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in read_csv(path):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") != "oos" or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") not in {"full_split", "chronological_third"}:
            continue
        segment = row.get("segment", "")
        if row.get("segment_type") == "full_split":
            read = "full_oos_reference"
        elif segment == "early":
            net = num(row, "net_profit") or 0.0
            pf = num(row, "profit_factor") or 0.0
            if net >= STAGE100_BEST["early_net_profit"] and pf >= STAGE100_BEST["early_profit_factor"]:
                read = "early_floor_preserved"
            else:
                read = "early_floor_weak"
        elif segment == "mid":
            read = "mid_profit_contribution"
        else:
            read = "late_profit_contribution"
        output.append(
            {
                "run_id": RUN_ID,
                "source_stage": source_stage,
                "adapter_id": adapter_id,
                "segment": segment,
                "trade_count": row.get("trade_count", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                "stage105_segment_read": read,
            }
        )
    return output


def tradeoff_rows() -> list[dict[str, Any]]:
    rows = []
    rows.extend(segment_rows_for(SOURCE_STAGE100_SEGMENTS, "stage100_best", STAGE100_BEST["adapter_id"]))
    rows.extend(segment_rows_for(SOURCE_STAGE102_SEGMENTS, "stage102_best", STAGE102_BEST["adapter_id"]))
    for adapter_id in stage104_full_rows():
        source_stage = "stage104_balanced_candidate" if adapter_id == "s104_v41_h3_cd8_lng_early_adx19" else "stage104_candidate"
        rows.extend(segment_rows_for(SOURCE_STAGE104_SEGMENTS, source_stage, adapter_id))
    return rows


def best_balanced(comparison: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in comparison if str(row.get("source_stage", "")).startswith("stage104")]
    return max(
        candidates,
        key=lambda row: (
            float(row.get("early_net_profit") or 0.0) >= STAGE100_BEST["early_net_profit"],
            float(row.get("early_profit_factor") or 0.0) >= STAGE100_BEST["early_profit_factor"],
            float(row.get("net_profit") or 0.0),
            float(row.get("profit_factor") or 0.0),
            -float(row.get("max_drawdown_percent") or 999.0),
        ),
    )


def report_markdown(comparison: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]], best: Mapping[str, Any]) -> str:
    lines = [
        "# Stage105 OOS Early Segment Follow-up Review(105단계 표본외 초반 구간 후속 검토)",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- source_stage104_closeout_commit(원천 104단계 종료 커밋): `{SOURCE_STAGE104_CLOSEOUT_COMMIT}`",
        f"- source_stage104_latest_commit(원천 104단계 최신 커밋): `{SOURCE_STAGE104_LATEST_COMMIT}`",
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Bounded Question(경계 질문)",
        "",
        "Stage104(104단계)의 OOS early segment repair(표본외 초반 구간 수리)가 Stage100 best(100단계 최선), Stage102 best(102단계 최선), 34D target surface(34D 목표 표면) 대비 어느 균형을 만들었는가?",
        "",
        "Effect(효과): Stage105(105단계)는 새 최적화가 아니라 실제 MT5 runtime(실행환경) 근거를 판독하고, 다음 수리 범위를 좁힌다.",
        "",
        "## KPI Comparison(KPI 비교)",
        "",
        "| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | early net(초반 순손익) | early PF(초반 수익 팩터) | net vs 34D(34D 대비 순손익) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in comparison:
        lines.append(
            f"| {row['source_stage']} | {row['adapter_id']} | {row['profit_factor']} | {row['net_profit']} | {row['max_drawdown_percent']} | {row['early_net_profit']} | {row['early_profit_factor']} | {row['net_gap_to_34d_latest']} | {row['stage105_read']} |"
        )
    lines.extend(
        [
            "",
            "## Attribution(성과 귀속)",
            "",
            "- observed_change(관찰 변화): Stage104(104단계)는 Stage102 best(102단계 최선)의 약한 OOS early(표본외 초반)를 `8.11`에서 `32.51`로 회복했지만, full OOS net(전체 표본외 순손익)은 `639.85`에서 `614.67`로 낮아졌다.",
            "- comparison_baseline(비교 기준): Stage100 best(100단계 최선), Stage102 best(102단계 최선), 34D target surface(34D 목표 표면).",
            "- likely_drivers(가능 원인): ADX gate(ADX 제한문)를 18 미만에서 19 미만으로 되돌린 조정이 초반 손실을 줄였지만, Stage102(102단계)의 완화된 거래 밀도와 중후반 수익 일부를 포기했다.",
            "- segment_checks(구간 점검): full split(전체 분할), early/mid/late(초반/중반/후반), Tier A+B routed total(Tier A+B 실제 라우팅 전체), MFE capture(MFE 포착률)를 확인했다.",
            "- trade_shape(거래 형태): Stage104 balanced(104단계 균형 후보)는 OOS trade count(표본외 거래 수) `150`으로 34D target(34D 목표) `404`보다 크게 낮고, net(순손익)도 `614.67`로 목표 `987.60`에 부족하다.",
            "- alternative_explanations(대안 설명): 표본외 중반 profit concentration(수익 집중)과 낮은 거래 밀도 때문에 headline PF(대표 수익 팩터)가 실제 목표 격차를 가릴 수 있다.",
            "- attribution_confidence(귀속 신뢰도): `medium` because(왜냐하면) 같은 MT5 runtime evidence(실행환경 근거) 안에서 구간별 tradeoff(상충)가 반복 확인됐다.",
            "- next_probe(다음 탐침): Stage106(106단계)에서 early floor(초반 바닥)를 보존 조건으로 두고 OOS net density/DD(표본외 순손익 밀도/손실률)를 좁게 수리한다.",
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(판정 대상): Stage104 OOS early segment repair(104단계 표본외 초반 구간 수리).",
            "- evidence_available(있는 근거): Stage104 MT5 runtime reports(실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).",
            "- evidence_missing(빠진 근거): 34D 수준 net/DD/trade density(순손익/손실률/거래 밀도)를 동시에 만족하는 수리 결과.",
            "- judgment_label(판정 라벨): `exploratory_repair_continues`.",
            f"- claim_boundary(주장 경계): `{BOUNDARY}`.",
            f"- next_condition(다음 조건): `{DECISION}`.",
            "- user_explanation_hook(쉬운 설명): 초반은 고쳤지만, 전체 힘은 아직 34D 목표만큼 세지 않다.",
            "",
            "## Segment Tradeoff(구간 상충)",
            "",
            "| source(원천) | adapter(어댑터) | segment(구간) | net(순손익) | PF(수익 팩터) | MFE capture(MFE 포착률) | read(판독) |",
            "|---|---|---|---:|---:|---:|---|",
        ]
    )
    for row in tradeoffs:
        lines.append(
            f"| {row['source_stage']} | {row['adapter_id']} | {row['segment']} | {row['net_profit']} | {row['profit_factor']} | {row['mfe_capture_ratio']} | {row['stage105_segment_read']} |"
        )
    lines.extend(
        [
            "",
            "## Decision(판정)",
            "",
            f"decision(판정): `{DECISION}`",
            "",
            f"best_balanced_candidate(균형 최선 후보): `{best['adapter_id']}`",
            "",
            "Stage104(104단계)는 OOS early(표본외 초반)를 회복했지만, 전체 목표 완료가 아니다. Effect(효과): Stage106(106단계)은 초반 회복을 보존 조건으로 걸고 OOS net density/DD(표본외 순손익 밀도/손실률)를 다시 좁게 수리한다.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).",
        ]
    )
    return "\n".join(lines) + "\n"


def decision_markdown(best: Mapping[str, Any]) -> str:
    return f"""# Stage105 Decision(105단계 판정)

decision(판정): `{DECISION}`

Stage105(105단계)는 Stage104(104단계)의 actual MT5 runtime result(실제 MT5 실행환경 결과)를 후속 검토했다.

Effect(효과): OOS early segment(표본외 초반 구간)은 회복됐지만, 34D KPI(34D 핵심 성과 지표) 수준의 net/DD/trade density(순손익/손실률/거래 밀도)는 아직 부족하다고 기록한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- segment_tradeoff_summary(구간 상충 요약): `{rel(TRADEOFF_PATH)}`
- source_stage104_summary(원천 104단계 요약): `{rel(SOURCE_STAGE104_SUMMARY)}`
- source_stage104_segment_kpi(원천 104단계 구간 KPI): `{rel(SOURCE_STAGE104_SEGMENTS)}`
- best_balanced_candidate(균형 최선 후보): `{best['adapter_id']}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def ledger_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "ledger_row_id": f"{RUN_ID}__review_gate",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "review_gate",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "stage105_review_gate",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage105_v41_oos_early_segment_followup_review",
            "scoreboard_lane": "regular_risk_execution_review",
            "status": "reviewed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                [
                    ("best_balanced_adapter", best.get("adapter_id")),
                    ("oos_pf", best.get("profit_factor")),
                    ("oos_net", best.get("net_profit")),
                    ("oos_dd_pct", best.get("max_drawdown_percent")),
                    ("oos_early_net", best.get("early_net_profit")),
                ]
            ),
            "guardrail_kpi": "34d_net_dd_trade_density_gap_remains_after_early_recovery",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Review-only gate using Stage104 MT5 runtime evidence; no new runtime claim.",
        }
    ]


def write_ledgers(best: Mapping[str, Any]) -> Mapping[str, Any]:
    rows = ledger_rows(best)
    write_csv(STAGE_LEDGER_PATH, rows, ALPHA_LEDGER_COLUMNS)
    project = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_oos_early_segment_followup_review",
                "status": "reviewed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": (
                    f"source_run={PARENT_RUN_ID};source_stage104_latest_commit={SOURCE_STAGE104_LATEST_COMMIT};"
                    f"target_surface={TARGET_SURFACE};legacy_relation=lesson_only;new_runtime=no_review_gate_only"
                ),
            }
        ],
        key="run_id",
    )
    return {"stage_ledger_path": rel(STAGE_LEDGER_PATH), "project_ledger": project, "run_registry": registry}


def packet_files(best: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "source_runtime_summary": rel(SOURCE_STAGE104_SUMMARY),
            "source_segment_summary": rel(SOURCE_STAGE104_SEGMENTS),
            "claim_boundary": BOUNDARY,
            "new_runtime": False,
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "result_subject": "Stage104 OOS early segment repair",
            "evidence_available": [rel(SOURCE_STAGE104_SUMMARY), rel(SOURCE_STAGE104_SEGMENTS), rel(SOURCE_STAGE104_REPORT)],
            "evidence_missing": "34D-level net/DD/trade density while preserving early floor",
            "judgment_label": "exploratory_repair_continues",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
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
            "best_balanced_candidate": best,
            "source_stage104_closeout_commit": SOURCE_STAGE104_CLOSEOUT_COMMIT,
            "source_stage104_latest_commit": SOURCE_STAGE104_LATEST_COMMIT,
            "comparison_path": rel(COMPARISON_PATH),
            "tradeoff_path": rel(TRADEOFF_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        (REPORT_PATH, "stage105_v41_oos_early_segment_followup_review_evidence", "Stage105 bounded review report."),
        (COMPARISON_PATH, "stage105_v41_oos_early_segment_followup_review_evidence", "Stage105 Stage100/102/104/34D comparison."),
        (TRADEOFF_PATH, "stage105_v41_oos_early_segment_followup_review_evidence", "Stage105 segment tradeoff summary."),
        (DECISION_PATH, "stage105_v41_oos_early_segment_followup_review_evidence", "Stage105 decision."),
        (STAGE_LEDGER_PATH, "stage105_v41_oos_early_segment_followup_review_evidence", "Stage105 local ledger."),
        (PACKET_ROOT / "aggregate_summary.json", "packet_summary", "Stage105 packet aggregate summary."),
        (PACKET_ROOT / "routing_receipt.json", "packet_control", "Stage105 routing receipt."),
        (PACKET_ROOT / "runtime_evidence_gate.json", "packet_control", "Stage105 runtime evidence gate."),
        (PACKET_ROOT / "result_judgment_gate.json", "packet_control", "Stage105 result judgment gate."),
    ]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": notes,
        }
        for path, artifact_type, notes in paths
    ]


def update_artifact_registry() -> Mapping[str, Any]:
    return upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows(),
        key="artifact_id",
    )


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage106(106단계)는 Stage105(105단계)의 판정대로 early floor(초반 바닥)를 보존한 채 OOS net density/DD(표본외 순손익 밀도/손실률)를 좁게 수리한다.

## Bounded Question(경계 질문)

Stage104 balanced candidate(104단계 균형 후보)의 OOS early(표본외 초반) 회복을 보존하면서 Stage102 best(102단계 최선)의 full OOS net/PF/DD(전체 표본외 순손익/수익 팩터/손실률) 장점을 되찾을 수 있는가?

Effect(효과): Stage106(106단계)은 새 모델 사냥(model hunting, 모델 탐색)이 아니라, 초반 바닥 보존 조건이 있는 순손익 밀도와 손실률 수리만 맡는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage106 Input References(106단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_comparison(원천 비교): `{rel(COMPARISON_PATH)}`
- source_tradeoff(원천 상충): `{rel(TRADEOFF_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage106(106단계)은 Stage105(105단계)가 확인한 약점, 즉 34D KPI(34D 핵심 성과 지표) 대비 net/DD/trade density(순손익/손실률/거래 밀도) 격차만 좁게 다룬다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage106 Review Index(106단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage106(106단계)은 Stage105(105단계) closeout(종료 기록)을 이어받아 좁은 수리만 수행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage106 Selection Status(106단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage106(106단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage105(105단계) closed(종료) as `{DECISION}` and Stage106(106단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): OOS early(표본외 초반) 회복은 보존 조건으로 남기고 OOS net density/DD(표본외 순손익 밀도/손실률) 수리로 넘긴다.
- >-
  Stage105 result(105단계 결과)는 `{rel(COMPARISON_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록된다. Effect(효과): Stage104(104단계)의 균형 후보가 34D KPI(34D 핵심 성과 지표)에 아직 부족한 이유를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage105_v41_oos_early_segment_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage104_closeout_commit: {SOURCE_STAGE104_CLOSEOUT_COMMIT}
  source_stage104_latest_commit: {SOURCE_STAGE104_LATEST_COMMIT}
  source_stage103_latest_commit: {SOURCE_STAGE103_LATEST_COMMIT}
  source_stage102_latest_commit: {SOURCE_STAGE102_LATEST_COMMIT}
  source_stage100_latest_commit: {SOURCE_STAGE100_LATEST_COMMIT}
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
    marker = "stage105_v41_oos_early_segment_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage105_v41_oos_early_segment_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage105 Selection Status(105단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE104_ID}`
- source_decision(원천 판정): `continue_oos_early_segment_repair_review_in_stage105`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage105_decision(105단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage105(105단계)는 Stage104(104단계) 실제 실행 결과를 판독하고, 운영 의미 없이 Stage106(106단계)로 넘긴다.
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
- adapter_under_review(검토 중 어댑터): `stage104_balanced_candidate_s104_v41_h3_cd8_lng_early_adx19`
- status(상태): `stage105_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage105(105단계) closed(종료) as v2-native v41 OOS early segment follow-up review(브이투 고유 브이41 표본외 초반 구간 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage106(106단계)로 이어진다.

## Latest Stage105 Evidence(최신 105단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- segment_tradeoff_summary(구간 상충 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage105 v41 OOS early segment follow-up review closeout(105단계 v41 표본외 초반 구간 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage104(104단계)는 OOS early(표본외 초반)를 회복했지만 34D KPI(34D 핵심 성과 지표) 대비 net/DD/trade density(순손익/손실률/거래 밀도)가 부족해 Stage106(106단계) 좁은 수리로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    comparison = comparison_rows()
    tradeoffs = tradeoff_rows()
    best = best_balanced(comparison)
    write_csv(
        COMPARISON_PATH,
        comparison,
        (
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
            "early_net_profit",
            "early_profit_factor",
            "early_mfe_capture_ratio",
            "pf_gap_to_34d_latest",
            "net_gap_to_34d_latest",
            "dd_gap_to_34d_latest",
            "trade_count_gap_to_34d_latest",
            "net_delta_vs_stage100_best",
            "net_delta_vs_stage102_best",
            "early_net_delta_vs_stage102_best",
            "stage105_read",
        ),
    )
    write_csv(
        TRADEOFF_PATH,
        tradeoffs,
        (
            "run_id",
            "source_stage",
            "adapter_id",
            "segment",
            "trade_count",
            "net_profit",
            "profit_factor",
            "mfe_capture_ratio",
            "stage105_segment_read",
        ),
    )
    write_md(REPORT_PATH, report_markdown(comparison, tradeoffs, best))
    write_md(DECISION_PATH, decision_markdown(best))
    ledger_payload = write_ledgers(best)
    packet_files(best, ledger_payload)
    update_artifact_registry()
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
                    "report": rel(REPORT_PATH),
                    "decision_path": rel(DECISION_PATH),
                    "next_stage": NEXT_STAGE_ID,
                    "best_balanced_candidate": best.get("adapter_id"),
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
