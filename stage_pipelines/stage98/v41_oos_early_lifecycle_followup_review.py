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


STAGE_ID = "98_adapter_research__v41_oos_early_lifecycle_followup_review"
RUN_ID = "run98A_stage98_v41_oos_early_lifecycle_followup_review_v1"
PACKET_ID = "stage98_v41_oos_early_lifecycle_followup_review_v1"
PARENT_RUN_ID = "run97A_stage97_v41_oos_early_lifecycle_repair_v1"
SOURCE_STAGE97_ID = "97_adapter_research__v41_oos_early_lifecycle_repair"
SOURCE_STAGE97_CLOSEOUT_COMMIT = "beeb81ebc58ea4492a0fbe015dab3b1ba9f5cbd6"
SOURCE_STAGE97_LATEST_COMMIT = "5154e76f306a4621b7bb11ee0cd1bfc4014d170a"
SOURCE_STAGE93_CLOSEOUT_COMMIT = "a3c2a42e378ffce41e07e947f0e68ed9e76606a6"
SOURCE_STAGE93_LATEST_COMMIT = "e1b59cbbd7e75ddee05bdcb075fd983e1effc8bf"
SOURCE_ADAPTER_ID = "s93_v41_h3_risk475_gate08_sl2075_tp40_cd10"
NEXT_STAGE_ID = "99_adapter_research__v41_oos_early_side_session_context_repair"
NEXT_RUN_ID = "run99A_stage99_v41_oos_early_side_session_context_repair_v1"
NEXT_PACKET_ID = "stage99_v41_oos_early_side_session_context_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_oos_early_side_session_context_repair_in_stage99"
EXTERNAL_STATUS = "completed_existing_stage97_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
LEGACY_34D_LATEST = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
    "expectancy": 2.444554,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE97_REVIEWS = Path("stages") / SOURCE_STAGE97_ID / "03_reviews"
SOURCE_LIFECYCLE_PATH = SOURCE_STAGE97_REVIEWS / "stage97_lifecycle_impact_summary.csv"
SOURCE_SUMMARY_PATH = SOURCE_STAGE97_REVIEWS / "stage97_v41_oos_early_lifecycle_repair_summary.csv"
SOURCE_SEGMENT_PATH = SOURCE_STAGE97_REVIEWS / "stage97_segment_kpi_summary.csv"
SOURCE_RISK_ATR_PATH = SOURCE_STAGE97_REVIEWS / "stage97_risk_atr_telemetry.csv"
SOURCE_GATE_PATH = SOURCE_STAGE97_REVIEWS / "stage97_gate_feature_summary.csv"
SOURCE_TIER_B_PATH = SOURCE_STAGE97_REVIEWS / "stage97_tier_b_diagnostic_summary.csv"
SOURCE_DECISION_PATH = SOURCE_STAGE97_REVIEWS / "stage97_decision.md"
SOURCE_REPORT_PATH = SOURCE_STAGE97_REVIEWS / "stage97_v41_oos_early_lifecycle_repair_report.md"

REPORT_PATH = REVIEWS_ROOT / "stage98_oos_early_lifecycle_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage98_stage93_stage97_comparison.csv"
SEGMENT_FLAGS_PATH = REVIEWS_ROOT / "stage98_stage97_segment_flags.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage98_lifecycle_attribution_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage98_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def rel(path: Path) -> str:
    return path.as_posix()


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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def number(row: Mapping[str, Any], key: str) -> float | None:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value))
    except ValueError:
        return None


def fmt(value: float | None, digits: int = 2) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def early_segment_lookup(segment_rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    lookup: dict[str, Mapping[str, str]] = {}
    for row in segment_rows:
        if row.get("split") == "oos" and row.get("segment_type") == "chronological_third" and row.get("segment") == "early":
            lookup[str(row.get("adapter_id"))] = row
    return lookup


def comparison_rows() -> list[dict[str, Any]]:
    lifecycle_rows = read_csv(SOURCE_LIFECYCLE_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    early_lookup = early_segment_lookup(segment_rows)
    rows: list[dict[str, Any]] = []
    for row in lifecycle_rows:
        adapter_id = str(row["variant_id"])
        source_stage = "stage93" if adapter_id.startswith("s93_") else "stage97"
        early = early_lookup.get(adapter_id, {})
        validation_pf = number(row, "validation_pf")
        validation_net = number(row, "validation_net")
        validation_dd = number(row, "validation_dd_pct")
        oos_pf = number(row, "oos_pf")
        oos_net = number(row, "oos_net")
        oos_dd = number(row, "oos_dd_pct")
        rows.append(
            {
                "source_stage": source_stage,
                "adapter_id": adapter_id,
                "changed_axis": row.get("changed_axis", ""),
                "validation_pf": fmt(validation_pf, 9),
                "validation_net": fmt(validation_net, 2),
                "validation_dd_pct": fmt(validation_dd, 2),
                "oos_pf": fmt(oos_pf, 9),
                "oos_net": fmt(oos_net, 2),
                "oos_dd_pct": fmt(oos_dd, 2),
                "oos_early_net": row.get("oos_early_net", ""),
                "oos_early_profit_factor": row.get("oos_early_pf", ""),
                "oos_early_mfe_capture_ratio": early.get("mfe_capture_ratio", ""),
                "validation_pf_gap_to_34d_latest": fmt(None if validation_pf is None else validation_pf - LEGACY_34D_LATEST["profit_factor"], 6),
                "validation_net_gap_to_34d_latest": fmt(None if validation_net is None else validation_net - LEGACY_34D_LATEST["net_profit"], 2),
                "validation_dd_gap_to_34d_latest": fmt(None if validation_dd is None else validation_dd - LEGACY_34D_LATEST["max_drawdown_percent"], 6),
                "oos_pf_gap_to_34d_latest": fmt(None if oos_pf is None else oos_pf - LEGACY_34D_LATEST["profit_factor"], 6),
                "oos_net_gap_to_34d_latest": fmt(None if oos_net is None else oos_net - LEGACY_34D_LATEST["net_profit"], 2),
                "oos_dd_gap_to_34d_latest": fmt(None if oos_dd is None else oos_dd - LEGACY_34D_LATEST["max_drawdown_percent"], 6),
                "stage98_read": row.get("stage97_read", ""),
            }
        )
    return rows


def segment_flag_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_SEGMENT_PATH):
        flag = str(row.get("quality_flag", ""))
        if flag and flag != "acceptable_measurement_only":
            rows.append(
                {
                    "adapter_id": row.get("adapter_id", ""),
                    "split": row.get("split", ""),
                    "segment_type": row.get("segment_type", ""),
                    "segment": row.get("segment", ""),
                    "trade_count": row.get("trade_count", ""),
                    "net_profit": row.get("net_profit", ""),
                    "profit_factor": row.get("profit_factor", ""),
                    "expectancy": row.get("expectancy", ""),
                    "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                    "quality_flag": flag,
                    "stage98_read": segment_flag_read(row),
                }
            )
    return rows


def segment_flag_read(row: Mapping[str, str]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    split = str(row.get("split", ""))
    segment = str(row.get("segment", ""))
    if adapter_id.endswith("_h2_risk475_gate08_sl2075_tp40_cd10") and split == "validation_is":
        return "h2_loses_validation_early_quality"
    if split == "oos" and segment == "early":
        return "oos_early_still_weak_or_negative"
    return "weak_segment_requires_followup"


def attribution_rows(comparison: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = next(row for row in comparison if row["adapter_id"].startswith("s93_"))
    rows: list[dict[str, Any]] = []
    for row in comparison:
        if row is ref:
            continue
        validation_net_delta = float(str(row["validation_net"])) - float(str(ref["validation_net"]))
        validation_pf_delta = float(str(row["validation_pf"])) - float(str(ref["validation_pf"]))
        oos_net_delta = float(str(row["oos_net"])) - float(str(ref["oos_net"]))
        oos_pf_delta = float(str(row["oos_pf"])) - float(str(ref["oos_pf"]))
        oos_early_delta = float(str(row["oos_early_net"])) - float(str(ref["oos_early_net"]))
        if row["adapter_id"].startswith("s97_v41_h2"):
            read = "oos_early_small_clue_but_validation_broken"
        elif row["adapter_id"].startswith("s97_v41_h4"):
            read = "validation_near_preserved_but_oos_early_dd_damaged"
        else:
            read = "validation_density_clue_but_oos_early_not_repaired"
        rows.append(
            {
                "adapter_id": row["adapter_id"],
                "changed_axis": row["changed_axis"],
                "validation_net_delta_vs_stage93": fmt(validation_net_delta, 2),
                "validation_pf_delta_vs_stage93": fmt(validation_pf_delta, 6),
                "oos_net_delta_vs_stage93": fmt(oos_net_delta, 2),
                "oos_pf_delta_vs_stage93": fmt(oos_pf_delta, 6),
                "oos_early_net_delta_vs_stage93": fmt(oos_early_delta, 2),
                "stage98_attribution_read": read,
            }
        )
    return rows


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| variant(변형) | changed axis(변경 축) | validation PF/net/DD(검증 수익팩터/순손익/손실률) | OOS PF/net/DD(표본외 수익팩터/순손익/손실률) | OOS early(표본외 초반) | read(판독) |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| `{}` | {} | {} / {} / {} | {} / {} / {} | {} / PF {} | {} |".format(
                row["adapter_id"],
                row["changed_axis"],
                row["validation_pf"],
                row["validation_net"],
                row["validation_dd_pct"],
                row["oos_pf"],
                row["oos_net"],
                row["oos_dd_pct"],
                row["oos_early_net"],
                row["oos_early_profit_factor"],
                row["stage98_read"],
            )
        )
    return "\n".join(lines)


def report_markdown(comparison: Sequence[Mapping[str, Any]], flags: Sequence[Mapping[str, Any]], attribution: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage98 OOS Early Lifecycle Follow-up Review(98단계 표본외 초반 생명주기 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE97_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- review_type(검토 유형): `bounded_review_gate_no_new_runtime`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage97(97단계)의 lifecycle/hold/re-entry(생명주기/보유/재진입) 조합이 OOS early flatline risk(표본외 초반 평탄화 위험)를 고치면서 Stage93 full split KPI(93단계 전체 분할 핵심성과지표)를 보존했는가?

Answer(답): 아니다. H2(2봉 보유)는 OOS early(표본외 초반)를 `18.35 / PF 1.080`까지 조금 끌어올렸지만 validation(검증)이 `213.26 / PF 1.22`로 크게 무너졌다. H4/CD8(4봉 보유/8봉 쿨다운)은 validation(검증) 단서는 남겼지만 OOS early(표본외 초반)가 음수 또는 거의 평탄으로 돌아갔다.

Effect(효과): lifecycle-only repair(생명주기 단독 수리)는 닫고, Stage99(99단계)에서는 side/session/market context(방향/세션/시장 문맥) 축으로 OOS early(표본외 초반) 원인을 분리한다.

## KPI Read(KPI 판독)

{markdown_table(comparison)}

Legacy 34D latest target(레거시 34D 최신 목표)는 PF(수익 팩터) `{LEGACY_34D_LATEST["profit_factor"]}`, net(순손익) `{LEGACY_34D_LATEST["net_profit"]}`, max DD(최대 손실률) `{LEGACY_34D_LATEST["max_drawdown_percent"]}%`, trades(거래 수) `{LEGACY_34D_LATEST["trade_count"]}`다. Stage97(97단계) 어떤 변형도 이 표면을 안정적으로 넘지 못했다.

## Segment Flags(구간 경고)

- flagged_segment_count(경고 구간 수): `{len(flags)}`
- main_issue(주요 문제): OOS early(표본외 초반)가 여전히 약하거나, H2(2봉 보유)처럼 validation early(검증 초반)가 무너진다.
- evidence(근거): `{rel(SEGMENT_FLAGS_PATH)}`

## Attribution(성과 원인 분해)

- observed_change(관찰 변화): hold/re-entry(보유/재진입) 변경은 full split(전체 분할)과 OOS early(표본외 초반)를 동시에 개선하지 못했다.
- comparison_baseline(비교 기준): `{SOURCE_ADAPTER_ID}` from Stage93(93단계).
- likely_drivers(가능 원인): 필요한 OOS early(표본외 초반) 거래와 validation(검증) 우수 거래가 같은 단순 hold/cooldown(보유/쿨다운) 축으로 분리되지 않는다.
- segment_checks(구간 점검): full split(전체 분할), chronological third(시간순 3분할), OOS early/mid/late(표본외 초반/중반/후반), MFE capture(MFE 포착률), risk/ATR telemetry(위험/ATR 텔레메트리)를 확인했다.
- trade_shape(거래 형태): H2(2봉 보유)는 validation trades(검증 거래) `207`, OOS trades(표본외 거래) `161`; H4(4봉 보유)는 `197/157`; CD8(8봉 쿨다운)은 `209/166`이다.
- alternative_explanations(대체 설명): 단순 생명주기 축이 아니라 side/session/regime(방향/세션/국면) 혼합 또는 early-window market context(초반 구간 시장 문맥)가 원인일 수 있다.
- attribution_confidence(귀속 신뢰도): `medium`. Stage97 trade audit(97단계 거래 감사)은 있으나 Stage98(98단계)는 review gate(검토 게이트)라 새 side/session split(방향/세션 분할)을 만들지 않았다.
- next_probe(다음 탐침): Stage99(99단계)에서 side/session/context(방향/세션/문맥) 기반 OOS early repair(표본외 초반 수리)를 좁게 실행한다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage97 lifecycle/hold/re-entry repair(97단계 생명주기/보유/재진입 수리).
- evidence_available(사용 근거): Stage97 summary(97단계 요약), segment KPI(구간 핵심성과지표), risk/ATR telemetry(위험/ATR 텔레메트리), MT5 Strategy Tester reports(MT5 전략 테스터 보고서), Stage98 comparison(98단계 비교).
- evidence_missing(부족 근거): side/session/regime attribution(방향/세션/국면 귀속), deeper equity path by early-window context(초반 구간 문맥별 자산곡선).
- judgment_label(판정 라벨): `negative_bounded_lifecycle_repair_result_with_salvage_clues`.
- claim_boundary(주장 경계): research/development only(연구개발 한정). 운영, 배포, 기준선 주장은 없다.
- next_condition(다음 조건): Stage99(99단계)가 OOS early(표본외 초반)를 validation/OOS(검증/표본외) 훼손 없이 side/session/context(방향/세션/문맥)으로 분리하는지 확인한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage98 Decision(98단계 판정)

decision(판정): `{DECISION}`

Stage98(98단계)는 Stage97(97단계)의 OOS early lifecycle repair(표본외 초반 생명주기 수리)를 review gate(검토 게이트)로만 판독했다.

Effect(효과): lifecycle/hold/re-entry(생명주기/보유/재진입) 단독 수리는 닫고, 다음 bounded repair(경계 수리)를 side/session/context(방향/세션/문맥) 축으로 넘긴다.

## Evidence(근거)

- source_report(원천 보고서): `{rel(SOURCE_REPORT_PATH)}`
- source_decision(원천 판정): `{rel(SOURCE_DECISION_PATH)}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY_PATH)}`
- source_segment_kpi(원천 구간 KPI): `{rel(SOURCE_SEGMENT_PATH)}`
- source_risk_atr_telemetry(원천 위험/ATR 텔레메트리): `{rel(SOURCE_RISK_ATR_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- segment_flags(구간 경고): `{rel(SEGMENT_FLAGS_PATH)}`
- attribution_summary(귀속 요약): `{rel(ATTRIBUTION_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## KPI Read(KPI 판독)

- H2(2봉 보유): OOS early(표본외 초반)는 조금 좋아졌지만 validation(검증)이 크게 훼손됐다.
- H4(4봉 보유): validation DD(검증 손실률)는 약간 나아졌지만 OOS early(표본외 초반)와 OOS DD(표본외 손실률)가 나빠졌다.
- CD8(8봉 쿨다운): validation(검증) PF/net(수익 팩터/순손익)은 좋아졌지만 OOS(표본외) 전체와 OOS early(표본외 초반)가 약해졌다.
- verdict(결론): Stage97(97단계)은 34D KPI(34D 핵심성과지표) 목표에 아직 부족하다.

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage99(99단계) bounded question(경계 질문): OOS early(표본외 초반) 약점이 side/session/market context(방향/세션/시장 문맥)로 분리되어 validation/OOS full split(검증/표본외 전체 분할)을 훼손하지 않고 수리될 수 있는가?

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def write_stage_files(comparison: Sequence[Mapping[str, Any]], flags: Sequence[Mapping[str, Any]], attribution: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        COMPARISON_PATH,
        comparison,
        (
            "source_stage",
            "adapter_id",
            "changed_axis",
            "validation_pf",
            "validation_net",
            "validation_dd_pct",
            "oos_pf",
            "oos_net",
            "oos_dd_pct",
            "oos_early_net",
            "oos_early_profit_factor",
            "oos_early_mfe_capture_ratio",
            "validation_pf_gap_to_34d_latest",
            "validation_net_gap_to_34d_latest",
            "validation_dd_gap_to_34d_latest",
            "oos_pf_gap_to_34d_latest",
            "oos_net_gap_to_34d_latest",
            "oos_dd_gap_to_34d_latest",
            "stage98_read",
        ),
    )
    write_csv(
        SEGMENT_FLAGS_PATH,
        flags,
        (
            "adapter_id",
            "split",
            "segment_type",
            "segment",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "mfe_capture_ratio",
            "quality_flag",
            "stage98_read",
        ),
    )
    write_csv(
        ATTRIBUTION_PATH,
        attribution,
        (
            "adapter_id",
            "changed_axis",
            "validation_net_delta_vs_stage93",
            "validation_pf_delta_vs_stage93",
            "oos_net_delta_vs_stage93",
            "oos_pf_delta_vs_stage93",
            "oos_early_net_delta_vs_stage93",
            "stage98_attribution_read",
        ),
    )
    write_md(REPORT_PATH, report_markdown(comparison, flags, attribution))
    write_md(DECISION_PATH, decision_markdown())
    write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage98 Review Index(98단계 검토 색인)

- status(상태): `reviewed_closed`
- source_decision(원천 판정): `continue_oos_early_lifecycle_followup_review_in_stage98`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`

Effect(효과): Stage98(98단계)는 Stage97(97단계) closeout(종료 기록)을 review gate(검토 게이트)로 판독하고 Stage99(99단계)로 넘긴다.
""")


def ledger_rows() -> tuple[dict[str, Any], dict[str, Any]]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_v2_native_v41_oos_early_lifecycle_followup_review",
        "status": "reviewed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": (
            f"source_run={PARENT_RUN_ID};source_stage97_closeout_commit={SOURCE_STAGE97_CLOSEOUT_COMMIT};"
            f"source_stage97_latest_commit={SOURCE_STAGE97_LATEST_COMMIT};target_surface={TARGET_SURFACE};"
            "legacy_relation=lesson_only;new_runtime=no_review_gate_only"
        ),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_gate",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "review_gate",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage97_review_gate",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage98_v41_oos_early_lifecycle_followup_review",
        "scoreboard_lane": "regular_risk_execution_review",
        "status": "reviewed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": ledger_pairs(
            (
                ("h2_oos_early", "18.35_pf_1.080"),
                ("h2_validation", "213.26_pf_1.22"),
                ("cd8_validation", "1000.47_pf_1.53"),
                ("cd8_oos_early", "-1.95_pf_0.994"),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("target_surface", TARGET_SURFACE),
                ("new_runtime", "no"),
                ("stage99_next_axis", "side_session_context"),
            )
        ),
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Review-only gate using Stage97 MT5 evidence; no new runtime claim.",
    }
    return run_row, alpha_row


def write_ledgers() -> Mapping[str, Any]:
    run_row, alpha_row = ledger_rows()
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload}


def write_packet_files(ledger_payload: Mapping[str, Any]) -> None:
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-experiment-design", "obsidian-exploration-mandate"],
            "required_gates": ["kpi_contract_audit", "performance_attribution_review", "result_judgment_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "review_type": "bounded_review_gate_no_new_runtime",
            "source_stage97_evidence": [
                rel(SOURCE_SUMMARY_PATH),
                rel(SOURCE_SEGMENT_PATH),
                rel(SOURCE_RISK_ATR_PATH),
                rel(SOURCE_GATE_PATH),
                rel(SOURCE_TIER_B_PATH),
            ],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "result_subject": "stage97_lifecycle_hold_reentry_repair",
            "evidence_available": [
                rel(SOURCE_SUMMARY_PATH),
                rel(SOURCE_SEGMENT_PATH),
                rel(SOURCE_RISK_ATR_PATH),
                rel(COMPARISON_PATH),
                rel(SEGMENT_FLAGS_PATH),
                rel(ATTRIBUTION_PATH),
            ],
            "evidence_missing": ["side_session_regime_attribution", "deeper_equity_path_by_early_window_context"],
            "judgment_label": "negative_bounded_lifecycle_repair_result_with_salvage_clues",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "stage99_side_session_context_repair_must_improve_oos_early_without_damaging_validation_oos_full_split",
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
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
            "source_stage97_closeout_commit": SOURCE_STAGE97_CLOSEOUT_COMMIT,
            "source_stage97_latest_commit": SOURCE_STAGE97_LATEST_COMMIT,
            "source_stage93_closeout_commit": SOURCE_STAGE93_CLOSEOUT_COMMIT,
            "source_stage93_latest_commit": SOURCE_STAGE93_LATEST_COMMIT,
            "comparison_path": rel(COMPARISON_PATH),
            "segment_flags_path": rel(SEGMENT_FLAGS_PATH),
            "attribution_path": rel(ATTRIBUTION_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        (REPORT_PATH, "stage98_v41_oos_early_lifecycle_followup_review_evidence", "Stage98 bounded review report."),
        (COMPARISON_PATH, "stage98_v41_oos_early_lifecycle_followup_review_evidence", "Stage98 Stage93/Stage97 comparison."),
        (SEGMENT_FLAGS_PATH, "stage98_v41_oos_early_lifecycle_followup_review_evidence", "Stage98 Stage97 segment flags."),
        (ATTRIBUTION_PATH, "stage98_v41_oos_early_lifecycle_followup_review_evidence", "Stage98 lifecycle attribution summary."),
        (DECISION_PATH, "stage98_v41_oos_early_lifecycle_followup_review_evidence", "Stage98 decision."),
        (STAGE_LEDGER_PATH, "stage98_v41_oos_early_lifecycle_followup_review_evidence", "Stage98 local ledger."),
        (PACKET_ROOT / "aggregate_summary.json", "packet_summary", "Stage98 packet aggregate summary."),
        (PACKET_ROOT / "routing_receipt.json", "packet_control", "Stage98 routing receipt."),
        (PACKET_ROOT / "runtime_evidence_gate.json", "packet_control", "Stage98 runtime evidence gate."),
        (PACKET_ROOT / "result_judgment_gate.json", "packet_control", "Stage98 result judgment gate."),
    ]
    rows = []
    for path, artifact_type, notes in paths:
        rows.append(
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
        )
    return rows


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

Stage99(99단계)는 Stage98(98단계)의 판정에 따라 OOS early weakness(표본외 초반 약점)를 side/session/market context(방향/세션/시장 문맥) 축으로 좁게 수리하는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

OOS early(표본외 초반) 약점이 side/session/market context(방향/세션/시장 문맥)로 분리되어 validation/OOS full split KPI(검증/표본외 전체 분할 핵심성과지표)를 훼손하지 않고 수리될 수 있는가?

Effect(효과): Stage99(99단계)는 lifecycle-only repair(생명주기 단독 수리)를 반복하지 않고, 다음 원인 후보를 하나로 좁힌다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage99 Input References(99단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage98_report(98단계 보고서): `{rel(REPORT_PATH)}`
- stage98_decision(98단계 판정): `{rel(DECISION_PATH)}`
- source_stage97_summary(원천 97단계 요약): `{rel(SOURCE_SUMMARY_PATH)}`
- source_stage97_trade_audit(원천 97단계 거래 감사): `stages/97_adapter_research__v41_oos_early_lifecycle_repair/03_reviews/stage97_trade_audit.csv`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage99(99단계)는 v2 고유 근거만 이어받아 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage99 Review Index(99단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage99(99단계)는 Stage98(98단계) closeout(종료 기록)을 이어받아 bounded repair(경계 수리)만 수행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage99 Selection Status(99단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage99(99단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage98(98단계) closed(종료) as `{DECISION}` and Stage99(99단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): lifecycle-only repair(생명주기 단독 수리) 실패와 단서를 보존하고 side/session/context(방향/세션/문맥) 경계 수리로 넘긴다.
- >-
  Stage98 result(98단계 결과): Stage97(97단계) H2(2봉 보유)는 OOS early(표본외 초반)를 조금 개선했지만 validation(검증)을 훼손했고, H4/CD8(4봉 보유/8봉 쿨다운)은 OOS early(표본외 초반)를 고치지 못했다. Effect(효과): 34D target surface(34D 목표 표면) 대비 KPI(핵심 성과 지표) 차이를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage98_v41_oos_early_lifecycle_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage97_closeout_commit: {SOURCE_STAGE97_CLOSEOUT_COMMIT}
  source_stage97_latest_commit: {SOURCE_STAGE97_LATEST_COMMIT}
  source_stage93_closeout_commit: {SOURCE_STAGE93_CLOSEOUT_COMMIT}
  source_stage93_latest_commit: {SOURCE_STAGE93_LATEST_COMMIT}
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
    marker = "stage98_v41_oos_early_lifecycle_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage98_v41_oos_early_lifecycle_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- status(상태): `stage98_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage98(98단계) closed(종료) as v2-native v41 OOS early lifecycle follow-up review(브이투 고유 브이41 표본외 초반 생명주기 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage99(99단계)로 이어진다.

## Latest Stage98 Evidence(최신 98단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage98_decision(98단계 판정): `{rel(DECISION_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- segment_flags(구간 경고): `{rel(SEGMENT_FLAGS_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage98 Selection Status(98단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE97_ID}`
- source_decision(원천 판정): `continue_oos_early_lifecycle_followup_review_in_stage98`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage98_decision(98단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage98(98단계)는 Stage97(97단계) lifecycle repair(생명주기 수리)를 판독하고, 운영 의미 없이 Stage99(99단계)로 넘긴다.
""",
    )


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage98 v41 OOS early lifecycle follow-up review closeout(98단계 v41 표본외 초반 생명주기 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage97(97단계)의 lifecycle/hold/re-entry(생명주기/보유/재진입) 수리가 34D KPI(34D 핵심 성과 지표) 목표에 아직 부족하다고 판정하고 Stage99(99단계) side/session/context repair(방향/세션/문맥 수리)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    comparison = comparison_rows()
    flags = segment_flag_rows()
    attribution = attribution_rows(comparison)
    write_stage_files(comparison, flags, attribution)
    ledger_payload = write_ledgers()
    write_packet_files(ledger_payload)
    update_artifact_registry()
    create_next_stage()
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
