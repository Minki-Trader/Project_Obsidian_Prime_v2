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

STAGE_ID = "170_adapter_research__stage169_net_density_followup_review"
RUN_NUMBER = "run170A"
RUN_ID = "run170A_stage170_stage169_net_density_followup_review_v1"
PACKET_ID = "stage170_stage169_net_density_followup_review_v1"
SOURCE_STAGE_ID = "169_adapter_research__net_density_lift_pf_preservation"
SOURCE_RUN_ID = "run169A_stage169_net_density_lift_pf_preservation_v1"
SOURCE_STAGE169_CLOSEOUT_COMMIT = "9717fa54fd32bda22acd0845b80c1dc922e0fc17"
SOURCE_STAGE169_HASH_RECORD_COMMIT = "5a27b8537dfff9fedb4c8961cfe64b7ab9d25b1a"
NEXT_STAGE_ID = "171_adapter_research__segment_stability_equity_curve_audit"
NEXT_RUN_ID = "run171A_stage171_segment_stability_equity_curve_audit_v1"
NEXT_PACKET_ID = "stage171_segment_stability_equity_curve_audit_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "open_stage171_segment_stability_equity_curve_audit_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage169_completed"
LOCAL_UPDATED_ON = "2026-05-19"

PRIMARY_ADAPTER = "s169_short_pre_risk0350_h3_cd5_sht54_lng52"
BACKUP_ADAPTER = "s169_short_pre_risk0300_h3_cd5_sht54_lng52"
FAILURE_MEMORY_ADAPTER = "s169_short_pre_restore_long_risk0300_h3_cd5_sht54_lng52"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_SUMMARY_JSON = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/03_reviews/"
    "stage169_net_density_lift_pf_preservation_summary.json"
)
SOURCE_SUMMARY_CSV = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/03_reviews/"
    "stage169_net_density_lift_pf_preservation_summary.csv"
)
SOURCE_SEGMENT_CSV = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/03_reviews/"
    "stage169_segment_kpi_summary.csv"
)
SOURCE_REPORT = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/03_reviews/"
    "stage169_net_density_lift_pf_preservation_report.md"
)
SOURCE_DECISION = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/03_reviews/stage169_decision.md"
)

REPORT_PATH = REVIEWS_ROOT / "stage170_stage169_net_density_followup_review.md"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage170_stage169_quality_matrix.csv"
SEGMENT_REVIEW_PATH = REVIEWS_ROOT / "stage170_stage169_segment_review.csv"
ROUTE_CSV_PATH = REVIEWS_ROOT / "stage170_repair_route_summary.csv"
ROUTE_JSON_PATH = REVIEWS_ROOT / "stage170_repair_route_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage170_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage170/stage169_net_density_followup_review.py")

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


def float_or_none(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def rounded(value: Any, digits: int = 4) -> float | str:
    number = float_or_none(value)
    if number is None:
        return ""
    return round(number, digits)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def load_stage169() -> Mapping[str, Any]:
    return json.loads(io_path(SOURCE_SUMMARY_JSON).read_text(encoding="utf-8-sig"))


def load_segment_rows() -> list[dict[str, Any]]:
    with io_path(SOURCE_SEGMENT_CSV).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def segment_lookup(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in segment_rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def full_lookup(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in segment_rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "full_split"
        ):
            return row
    return {}


def build_segment_review(segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for adapter_id in (BACKUP_ADAPTER, PRIMARY_ADAPTER, FAILURE_MEMORY_ADAPTER):
        validation_full = full_lookup(segment_rows, adapter_id, "validation_is")
        oos_full = full_lookup(segment_rows, adapter_id, "oos")
        for split in ("validation_is", "oos"):
            full = validation_full if split == "validation_is" else oos_full
            full_net = float_or_none(full.get("net_profit"))
            for segment in ("early", "mid", "late"):
                source = segment_lookup(segment_rows, adapter_id, split, segment)
                net = float_or_none(source.get("net_profit"))
                pf = float_or_none(source.get("profit_factor"))
                contribution = round(net / full_net, 4) if net is not None and full_net not in (None, 0) else ""
                pf_flag = "below_34d_pf" if pf is not None and pf < LEGACY_34D["profit_factor"] else "pf_ok_vs_34d"
                role = "primary_audit_anchor" if adapter_id == PRIMARY_ADAPTER else "comparison_memory"
                if adapter_id == BACKUP_ADAPTER:
                    role = "lower_risk_backup"
                if adapter_id == FAILURE_MEMORY_ADAPTER:
                    role = "long_restore_failure_memory"
                rows.append(
                    {
                        "run_id": RUN_ID,
                        "source_run_id": SOURCE_RUN_ID,
                        "adapter_id": adapter_id,
                        "split": split,
                        "segment": segment,
                        "role": role,
                        "trade_count": rounded(source.get("trade_count"), 2),
                        "net_profit": rounded(source.get("net_profit"), 2),
                        "profit_factor": rounded(source.get("profit_factor"), 6),
                        "expectancy": rounded(source.get("expectancy"), 6),
                        "max_closed_trade_drawdown": rounded(source.get("max_closed_trade_drawdown"), 2),
                        "mfe_capture_ratio": rounded(source.get("mfe_capture_ratio"), 6),
                        "net_contribution_of_split": contribution,
                        "pf_flag": pf_flag,
                        "stage170_note": segment_note(adapter_id, split, segment, pf_flag, contribution),
                    }
                )
    return rows


def segment_note(adapter_id: str, split: str, segment: str, pf_flag: str, contribution: Any) -> str:
    if adapter_id == PRIMARY_ADAPTER and split == "validation_is" and segment in {"early", "mid"}:
        return "primary(주 후보)는 near-34D total net(34D 근접 전체 순손익)이지만 이 validation segment(검증 구간) PF(수익요인)가 34D 아래라서 repair(수리) 전에 audit(감사)가 필요하다."
    if adapter_id == PRIMARY_ADAPTER and split == "validation_is" and segment == "late":
        return f"primary late validation(주 후보 검증 후반)이 validation net(검증 순손익)의 {contribution}를 차지하므로 concentration(집중도)과 equity shape(자산 곡선 모양)을 확인한다."
    if adapter_id == PRIMARY_ADAPTER and split == "oos":
        return "primary OOS segment(주 후보 표본외 구간)는 PF-positive(수익요인 양호)지만 late contribution(후반 기여)이 concentration risk(집중 위험)인지 감사한다."
    if adapter_id == FAILURE_MEMORY_ADAPTER and split == "oos":
        return "long restore(롱 복원)는 density(밀도)를 늘렸지만 OOS PF/DD(표본외 수익요인/낙폭)를 훼손했으므로 failure memory(실패 기억)로 보존한다."
    return f"{pf_flag}; comparison row(비교 행) for Stage171 bounded audit(171단계 경계 감사)."


def quality_rows(stage169: Mapping[str, Any], segment_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    stage167_primary = stage169.get("stage167_primary", {})
    rows: list[dict[str, Any]] = []
    for row in stage169.get("quality_rows", []):
        adapter_id = str(row.get("adapter_id", ""))
        validation_pf = float_or_none(row.get("validation_pf"))
        validation_net = float_or_none(row.get("validation_net"))
        oos_pf = float_or_none(row.get("oos_pf"))
        oos_dd = float_or_none(row.get("oos_dd_percent"))
        oos_early_pf = float_or_none(row.get("oos_early_pf"))
        validation_net_gap = round(validation_net - LEGACY_34D["net_profit"], 2) if validation_net is not None else ""
        validation_pf_margin = (
            round(validation_pf - LEGACY_34D["profit_factor"], 6) if validation_pf is not None else ""
        )
        oos_dd_margin = round(LEGACY_34D["max_drawdown_percent"] - oos_dd, 4) if oos_dd is not None else ""

        if adapter_id == PRIMARY_ADAPTER:
            judgment = "near_34d_net_pf_dd_pass_segment_equity_audit_required"
            route_role = "primary_stage171_segment_equity_audit_anchor"
            route_reason = (
                "validation net(검증 순손익)은 34D보다 3.64 낮을 뿐이고 PF/DD/OOS early(수익요인/낙폭/표본외 초반)는 유지된다. "
                "하지만 validation early/mid PF(검증 초반/중반 수익요인)가 34D 아래이고 late net concentration(후반 순손익 집중)을 audit(감사)해야 한다."
            )
        elif adapter_id == BACKUP_ADAPTER:
            judgment = "lower_risk_backup_pf_dd_pass_net_gap_remaining"
            route_role = "secondary_lower_risk_backup"
            route_reason = (
                "risk 3.0(위험 3.0)은 PF/DD/OOS(수익요인/낙폭/표본외)를 안정적으로 지키지만 validation net(검증 순손익)은 34D보다 많이 낮다. "
                "따라서 risk 3.5(위험 3.5)의 concentration(집중도)이 실패할 때 fallback(대체 후보)으로 쓴다."
            )
        else:
            judgment = "failure_memory_long_restore_oos_pf_dd_damage"
            route_role = "negative_long_restore_failure_memory"
            route_reason = (
                "long density restore(롱 밀도 복원)는 validation net(검증 순손익)을 올렸지만 OOS PF(표본외 수익요인)를 34D 경계로 밀고 "
                "OOS DD(표본외 낙폭)를 34D guardrail(보호 기준) 밖으로 보냈다."
            )

        validation_weak_segments = [
            item["segment"]
            for item in segment_review
            if item.get("adapter_id") == adapter_id
            and item.get("split") == "validation_is"
            and item.get("pf_flag") == "below_34d_pf"
        ]
        oos_weak_segments = [
            item["segment"]
            for item in segment_review
            if item.get("adapter_id") == adapter_id
            and item.get("split") == "oos"
            and item.get("pf_flag") == "below_34d_pf"
        ]

        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "model_risk_max_pct": model_risk_cap(stage169, adapter_id),
                "validation_pf": rounded(validation_pf, 6),
                "validation_pf_margin_vs_34d": validation_pf_margin,
                "validation_net": rounded(validation_net, 2),
                "validation_net_gap_vs_34d": validation_net_gap,
                "validation_trade_count": rounded(row.get("validation_trade_count"), 2),
                "oos_pf": rounded(oos_pf, 6),
                "oos_net": rounded(row.get("oos_net"), 2),
                "oos_dd_percent": rounded(oos_dd, 4),
                "oos_dd_margin_vs_34d": oos_dd_margin,
                "oos_trade_count": rounded(row.get("oos_trade_count"), 2),
                "oos_early_pf": rounded(oos_early_pf, 6),
                "validation_weak_segments": ";".join(validation_weak_segments),
                "oos_weak_segments": ";".join(oos_weak_segments),
                "stage167_primary_validation_net": rounded(stage167_primary.get("validation_net"), 2),
                "validation_net_delta_vs_stage167_primary": rounded(row.get("validation_net_delta_vs_stage167_primary"), 2),
                "quality_flags": row.get("quality_flags", ""),
                "stage170_judgment": judgment,
                "route_role": route_role,
                "route_reason": route_reason,
            }
        )
    return rows


def model_risk_cap(stage169: Mapping[str, Any], adapter_id: str) -> float | str:
    for row in stage169.get("summary_rows", []):
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == "validation_is"
            and row.get("view") == "actual_routed_total"
        ):
            return rounded(row.get("model_risk_max_pct"), 4)
    return ""


def route_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    primary = next(row for row in rows if row["route_role"] == "primary_stage171_segment_equity_audit_anchor")
    backup = next(row for row in rows if row["route_role"] == "secondary_lower_risk_backup")
    failure = next(row for row in rows if row["route_role"] == "negative_long_restore_failure_memory")
    return [
        {
            "run_id": RUN_ID,
            "route_rank": 1,
            "route": "stage171_primary_segment_equity_concentration_audit",
            "adapter_id": primary["adapter_id"],
            "bounded_question": (
                "Does the near-34D risk 3.5 adapter(34D 근접 위험 3.5 어댑터) survive segment/equity/concentration audit(구간/자산 곡선/집중도 감사) "
                "without one late-window spike(후반 단일 급등) carrying the result(결과 지탱)?"
            ),
            "why": primary["route_reason"],
            "do_not_do": "Do not declare final(최종 선언 금지), do not start ONNX hardening(ONNX 경화 시작 금지), and do not tune inside Stage170(170단계 안 튜닝 금지).",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 2,
            "route": "stage171_lower_risk_backup_comparison",
            "adapter_id": backup["adapter_id"],
            "bounded_question": "Can the risk 3.0 backup(위험 3.0 대체 후보) explain whether the risk 3.5 lift(위험 3.5 상승)가 only scaling(단순 스케일링)인지?",
            "why": backup["route_reason"],
            "do_not_do": "Do not prefer lower risk(낮은 위험 선호 금지) if it fails the 34D net target(34D 순손익 목표 실패) and the primary passes stability audit(주 후보 안정성 감사 통과).",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 3,
            "route": "preserve_long_restore_oos_damage_memory",
            "adapter_id": failure["adapter_id"],
            "bounded_question": "Keep long-restore damage(롱 복원 손상)를 visible(가시화) while Stage171 audits concentration(171단계가 집중도를 감사).",
            "why": failure["route_reason"],
            "do_not_do": "Do not cherry-pick validation net(검증 순손익 골라보기 금지) while ignoring OOS PF/DD damage(표본외 수익요인/낙폭 손상 무시 금지).",
        },
    ]


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | role(역할) | val PF(검증 수익요인) | val net(검증 순손익) | gap vs 34D(34D 대비 차이) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | weak segments(약한 구간) | judgment(판정) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        weak = row.get("validation_weak_segments") or row.get("oos_weak_segments") or "none"
        lines.append(
            "| {adapter_id} | {route_role} | {validation_pf} | {validation_net} | {validation_net_gap_vs_34d} | {oos_pf} | {oos_net} | {oos_dd_percent} | {weak} | {stage170_judgment} |".format(
                weak=weak,
                **row,
            )
        )
    return "\n".join(lines)


def segment_table(segment_review: Sequence[Mapping[str, Any]], adapter_id: str) -> str:
    rows = [row for row in segment_review if row.get("adapter_id") == adapter_id]
    lines = [
        "| split(분할) | segment(구간) | trades(거래) | net(순손익) | PF(수익요인) | net share(순손익 비중) | flag(표식) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {split} | {segment} | {trade_count} | {net_profit} | {profit_factor} | {net_contribution_of_split} | {pf_flag} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], segment_review: Sequence[Mapping[str, Any]], routes: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage170 Stage169 Net/Density Follow-up Review(170단계 169단계 순손익/밀도 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE169_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_STAGE169_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage169(169단계) move net/density(순손익/밀도) closer to legacy 34D(레거시 34D) while preserving PF/DD/OOS early(수익요인/낙폭/표본외 초반)?

## Simple KPI Read(쉬운 핵심 성과 지표 판독)

Stage169(169단계)는 34D(34D) 근처까지 왔다. 특히 `{PRIMARY_ADAPTER}`는 validation net(검증 순손익) `983.96`으로 34D `987.60`보다 `3.64` 낮고, validation PF(검증 수익요인) `1.61`은 34D `1.583157`보다 높다. OOS DD(표본외 낙폭) `11.03%`도 34D `12.909136%`보다 낮다.

Effect(효과): KPI(핵심 성과 지표) 큰 줄기는 좋아졌지만, final(최종)이나 operating(운영) 주장은 아직 금지한다.

{kpi_table(rows)}

## Segment Warning(구간 경고)

Primary(주 후보) `{PRIMARY_ADAPTER}`는 total KPI(전체 핵심 성과 지표)가 강하지만 validation early/mid(검증 초반/중반) PF(수익요인)가 34D 아래다. Late validation(검증 후반)이 순손익의 큰 비중을 들고 있어, Stage171(171단계)에서 equity curve(자산 곡선), balance curve(잔고 곡선), concentration(집중도), recovery(회복)를 봐야 한다.

{segment_table(segment_review, PRIMARY_ADAPTER)}

## Attribution(원인 분해)

- action(행동): risk cap(위험 상한)을 `0.025`에서 `0.035`로 올린 변형이 net(순손익)을 크게 올렸다. effect(효과): signal quality(신호 품질) 개선인지 단순 scaling(스케일링)인지 분리 검토가 필요하다.
- action(행동): long restore(롱 복원) 변형을 같이 보존했다. effect(효과): validation net(검증 순손익)은 좋아도 OOS PF/DD(표본외 수익요인/낙폭)가 훼손되면 후보에서 밀어야 한다.
- action(행동): segment KPI(구간 핵심 성과 지표)를 별도 표로 남겼다. effect(효과): 높은 final net(최종 순손익) 하나로 약한 구간을 덮지 않는다.

## Route Decision(경로 판정)

1. primary(주): `{routes[0]["route"]}` from `{routes[0]["adapter_id"]}`.
2. secondary(보조): `{routes[1]["route"]}` from `{routes[1]["adapter_id"]}`.
3. failure_memory(실패 기억): `{routes[2]["route"]}` from `{routes[2]["adapter_id"]}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage170 Decision(170단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage169_closeout_commit(원천 169단계 종료 커밋): `{SOURCE_STAGE169_CLOSEOUT_COMMIT}`
- source_stage169_hash_record_commit(원천 169단계 해시 기록 커밋): `{SOURCE_STAGE169_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_review(구간 검토): `{rel(SEGMENT_REVIEW_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage170(170단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        QUALITY_MATRIX_PATH,
        SEGMENT_REVIEW_PATH,
        ROUTE_CSV_PATH,
        ROUTE_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        SOURCE_REPORT,
        SOURCE_SUMMARY_JSON,
        SOURCE_SUMMARY_CSV,
        SOURCE_SEGMENT_CSV,
        SOURCE_DECISION,
    ]
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage170_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage170 review-only evidence(170단계 검토 전용 근거); no deployment(배포) or live-readiness(실거래 준비) claim(주장).",
                }
            )
    return rows


def write_ledgers() -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage170_stage169_net_density_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage169_closeout_commit", SOURCE_STAGE169_CLOSEOUT_COMMIT),
                        ("source_stage169_hash_record_commit", SOURCE_STAGE169_HASH_RECORD_COMMIT),
                        ("primary_adapter", PRIMARY_ADAPTER),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only_no_inheritance"),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__review_only",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "review_only",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "stage170_review_only",
            "tier_scope": "Stage169 MT5 evidence",
            "kpi_scope": "stage169_net_density_followup_review",
            "scoreboard_lane": "research_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": "near_34d_net_pf_dd_pass_segment_equity_audit_required",
            "guardrail_kpi": "no_final_adapter_no_deployment_no_live_readiness",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage170 reviewed Stage169 MT5 evidence and opened Stage171 bounded segment/equity audit.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifacts = artifact_rows()
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {
        "run_registry": run_payload,
        "alpha_ledger": alpha_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(
    ledger_payload: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    segment_review: Sequence[Mapping[str, Any]],
    routes: Sequence[Mapping[str, Any]],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "report_path": rel(REPORT_PATH),
        "quality_matrix": rel(QUALITY_MATRIX_PATH),
        "segment_review": rel(SEGMENT_REVIEW_PATH),
        "route_summary": rel(ROUTE_CSV_PATH),
        "ledger_payload": ledger_payload,
        "quality_rows": list(rows),
        "segment_review_rows": list(segment_review),
        "route_rows": list(routes),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage170 Closeout Packet(170단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage170(170단계) review-only(검토 전용) 결과를 packet(작업 묶음)에 연결하고 Stage171(171단계)의 segment/equity audit(구간/자산 곡선 감사) 질문을 좁혔다.
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage171(171단계)는 Stage169(169단계) near-34D(34D 근접) 후보를 segment/equity/concentration audit(구간/자산 곡선/집중도 감사)로만 본다.

## Bounded Question(경계 질문)

Does `{PRIMARY_ADAPTER}` survive segment stability(구간 안정성), equity curve(자산 곡선), balance curve(잔고 곡선), concentration(집중도), drawdown recovery(낙폭 회복), and MFE/MAE behavior(MFE/MAE 동작) audit as a research candidate(연구 후보), or must it route to another bounded repair(경계 수리)?

Effect(효과): 34D KPI(34D 핵심 성과 지표)에 가까운 숫자만 보고 final(최종)로 착각하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage171 Inputs(171단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_stage169_closeout_commit(원천 169단계 종료 커밋): `{SOURCE_STAGE169_CLOSEOUT_COMMIT}`
- source_stage169_hash_record_commit(원천 169단계 해시 기록 커밋): `{SOURCE_STAGE169_HASH_RECORD_COMMIT}`
- stage170_report(170단계 보고서): `{rel(REPORT_PATH)}`
- stage170_quality_matrix(170단계 품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- stage170_segment_review(170단계 구간 검토): `{rel(SEGMENT_REVIEW_PATH)}`
- stage170_route_summary(170단계 경로 요약): `{rel(ROUTE_CSV_PATH)}`
- source_stage169_segment_kpi(원천 169단계 구간 핵심 성과 지표): `{rel(SOURCE_SEGMENT_CSV)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage171 Review Index(171단계 검토 색인)

- status(상태): `open_planned_from_stage170`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage171 Selection Status(171단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage170`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on: .*$", f"updated_on: '{LOCAL_UPDATED_ON}'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage170(170단계) closed(종료) as `{DECISION}` and Stage171(171단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage169(169단계)의 near-34D(34D 근접) KPI(핵심 성과 지표)를 segment/equity/concentration audit(구간/자산 곡선/집중도 감사)로 넘긴다.
- >-
  Stage170 evidence(170단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(SEGMENT_REVIEW_PATH)}`, `{rel(ROUTE_CSV_PATH)}`에 있다. Effect(효과): final net(최종 순손익) 하나로 판정하지 않고 early/mid/late(초반/중반/후반) 품질을 같이 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\n\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage170_stage169_net_density_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage170_stage169_net_density_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage169_closeout_commit: {SOURCE_STAGE169_CLOSEOUT_COMMIT}
  source_stage169_hash_record_commit: {SOURCE_STAGE169_HASH_RECORD_COMMIT}
  decision: {DECISION}
  primary_adapter: {PRIMARY_ADAPTER}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  segment_review_path: {rel(SEGMENT_REVIEW_PATH)}
  route_summary_path: {rel(ROUTE_CSV_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
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
- adapter_under_review(검토 중 어댑터): `{PRIMARY_ADAPTER}`
- status(상태): `stage170_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage170(170단계)는 Stage169(169단계) net/density lift(순손익/밀도 상승)를 review-only(검토 전용)로 판독했다. Effect(효과): `{PRIMARY_ADAPTER}`를 Stage171(171단계) segment/equity/concentration audit(구간/자산 곡선/집중도 감사)의 주 후보로 넘긴다.

## Latest Stage170 Evidence(최신 170단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_review(구간 검토): `{rel(SEGMENT_REVIEW_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage170 Selection Status(170단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage170(170단계)은 review-only(검토 전용) 질문만 닫고, 전체 목표 완료를 주장하지 않는다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage170 Review Index(170단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_review(구간 검토): `{rel(SEGMENT_REVIEW_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage170 Stage169 net/density follow-up review closeout(170단계 169단계 순손익/밀도 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage171(171단계)을 segment/equity/concentration audit(구간/자산 곡선/집중도 감사)로 열어 near-34D(34D 근접) 후보를 더 검증한다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    stage169 = load_stage169()
    segment_rows = load_segment_rows()
    segment_review = build_segment_review(segment_rows)
    rows = quality_rows(stage169, segment_review)
    routes = route_rows(rows)
    write_csv(QUALITY_MATRIX_PATH, rows)
    write_csv(SEGMENT_REVIEW_PATH, segment_review)
    write_csv(ROUTE_CSV_PATH, routes)
    write_json(
        ROUTE_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "quality_rows": rows,
            "segment_review_rows": segment_review,
            "route_rows": routes,
            "legacy_34d": LEGACY_34D,
            "primary_adapter": PRIMARY_ADAPTER,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_md(REPORT_PATH, report_markdown(rows, segment_review, routes))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers()
    write_packet_files(ledger_payload, rows, segment_review, routes)
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "report_path": rel(REPORT_PATH),
                    "primary_adapter": PRIMARY_ADAPTER,
                    "next_stage": NEXT_STAGE_ID,
                    "overall_goal_complete": False,
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
