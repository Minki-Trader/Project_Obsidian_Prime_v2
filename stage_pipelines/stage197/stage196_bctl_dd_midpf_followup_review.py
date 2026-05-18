from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage196 import bctl_dd_compression_midpf_guard as s196  # noqa: E402

s172 = s196.s172

STAGE_ID = "197_adapter_research__stage196_bctl_dd_midpf_followup_review"
RUN_ID = "run197A_stage197_stage196_bctl_dd_midpf_followup_review_v1"
PACKET_ID = "stage197_stage196_bctl_dd_midpf_followup_review_v1"
PARENT_RUN_ID = "run196A_stage196_bctl_dd_compression_midpf_guard_v1"
SOURCE_STAGE_ID = "196_adapter_research__bctl_dd_compression_midpf_guard"
SOURCE_RUN_ID = "run196A_stage196_bctl_dd_compression_midpf_guard_v1"
SOURCE_STAGE196_EVIDENCE_COMMIT = "24a078cce6907d56c6f8b7fca5d2ca848a68240b"
SOURCE_STAGE196_HASH_RECORD_COMMIT = "018afe6a1cfd4358553e7b4428c1843cefd8639a"
NEXT_STAGE_ID = "198_adapter_research__bctl_adverse_excursion_dd_guard_repair"
NEXT_RUN_ID = "run198A_stage198_bctl_adverse_excursion_dd_guard_repair_v1"
NEXT_PACKET_ID = "stage198_bctl_adverse_excursion_dd_guard_repair_v1"
DECISION = "open_stage198_bctl_adverse_excursion_dd_guard_repair_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage196_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_bctl_adverse_excursion_dd_guard"
BOUNDARY = s196.BOUNDARY
LEGACY_34D = s196.LEGACY_34D

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/196_adapter_research__bctl_dd_compression_midpf_guard/03_reviews/stage196_quality_matrix.csv")
SOURCE_SEGMENT_PATH = Path("stages/196_adapter_research__bctl_dd_compression_midpf_guard/03_reviews/stage196_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/196_adapter_research__bctl_dd_compression_midpf_guard/03_reviews/stage196_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/196_adapter_research__bctl_dd_compression_midpf_guard/03_reviews/stage196_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/196_adapter_research__bctl_dd_compression_midpf_guard/03_reviews/stage196_bctl_dd_midpf_report.md")
SOURCE_DECISION_PATH = Path("stages/196_adapter_research__bctl_dd_compression_midpf_guard/03_reviews/stage196_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage197_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage197_bctl_dd_midpf_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage197_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage197_route_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage197_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage197/stage196_bctl_dd_midpf_followup_review.py")


def rel(path: Path | str) -> str:
    return s172.rel(path)


def fnum(value: Any, default: float = 0.0) -> float:
    return s172.as_float({"value": value}, "value", default)


def read_csv(path: Path) -> list[dict[str, str]]:
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


def by_adapter(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("adapter_id")): row for row in rows}


def segment_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def stage197_read(adapter_id: str, row: Mapping[str, Any]) -> str:
    dd = fnum(row.get("validation_balance_dd_percent"))
    mid = fnum(row.get("validation_mid_pf"))
    late = fnum(row.get("validation_late_net_share"))
    if adapter_id == "s196_bctl_cd8_r0325":
        return "best_tradeoff_but_not_pass(최선 상충안이나 통과 아님)"
    if adapter_id == "s196_bctl_r0320":
        return "dd_improves_but_net_midpf_erode(낙폭은 줄지만 순손익과 중반 수익요인이 약해짐)"
    if adapter_id == "s196_bctl_r0325":
        return "small_dd_gain_midpf_flat(낙폭 소폭 개선, 중반 수익요인 거의 정체)"
    if dd > LEGACY_34D["max_drawdown_percent"] and mid < LEGACY_34D["profit_factor"] and late < 0.50:
        return "source_clue_good_late_oos_but_dd_midpf_short(원천 단서는 후반/표본외가 좋지만 낙폭/중반 부족)"
    return "review_required(검토 필요)"


def build_tradeoff_rows(quality_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = by_adapter(quality_rows).get("s196_bctl_ref_r0330", {})
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        mid = segment_lookup(segment_rows, adapter_id, "validation_is", "mid")
        late = segment_lookup(segment_rows, adapter_id, "validation_is", "late")
        val_net = fnum(row.get("validation_net"))
        val_dd = fnum(row.get("validation_balance_dd_percent"))
        val_mid = fnum(row.get("validation_mid_pf"))
        late_share = fnum(row.get("validation_late_net_share"))
        ref_dd = fnum(ref.get("validation_balance_dd_percent"))
        ref_mid = fnum(ref.get("validation_mid_pf"))
        ref_net = fnum(ref.get("validation_net"))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": round(val_net - LEGACY_34D["net_profit"], 6),
                "validation_net_delta_vs_ref": round(val_net - ref_net, 6),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_gap_above_34d": round(val_dd - LEGACY_34D["max_drawdown_percent"], 6),
                "validation_dd_delta_vs_ref": round(val_dd - ref_dd, 6),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d_pf": round(val_mid - LEGACY_34D["profit_factor"], 6),
                "validation_mid_pf_delta_vs_ref": round(val_mid - ref_mid, 6),
                "validation_mid_net": mid.get("net_profit", ""),
                "validation_mid_mfe_capture": mid.get("mfe_capture_ratio", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_late_share_margin_to_50pct": round(0.50 - late_share, 6),
                "validation_late_pf": late.get("profit_factor", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage197_read": stage197_read(adapter_id, row),
            }
        )
    return rows


def best_tradeoff(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            fnum(row.get("validation_dd_delta_vs_ref")) < 0,
            fnum(row.get("validation_mid_pf_delta_vs_ref")),
            fnum(row.get("validation_net_gap_vs_34d")),
            fnum(row.get("oos_pf")),
            -fnum(row.get("validation_late_net_share")),
        ),
    )


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = by_adapter(tradeoff_rows)
    ref = rows["s196_bctl_ref_r0330"]
    r0325 = rows["s196_bctl_r0325"]
    r0320 = rows["s196_bctl_r0320"]
    cd8 = rows["s196_bctl_cd8_r0325"]
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "risk compression(위험 압축)은 DD(낙폭)를 조금 낮췄지만 mid PF(중반 수익요인)와 net(순손익)을 같이 깎았다.",
            "comparison_baseline": "s196_bctl_ref_r0330 reference(참조)",
            "trade_shape": f"ref dd={ref['validation_dd_percent']}, mid_pf={ref['validation_mid_pf']}; r0325 dd={r0325['validation_dd_percent']}, mid_pf={r0325['validation_mid_pf']}; r0320 dd={r0320['validation_dd_percent']}, mid_pf={r0320['validation_mid_pf']}",
            "likely_drivers": "risk cap(위험 상한)만 낮추면 손실 크기는 줄지만 진입 품질 자체는 고치지 못한다.",
            "next_probe": "Stage198(198단계)은 DD(낙폭)를 만든 adverse excursion(불리한 움직임) 구간을 직접 겨냥한다.",
            "attribution_confidence": "medium(중간)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "cooldown 8 + r0325(대기 8 + 위험 0.0325)가 가장 좋은 균형을 만들었다.",
            "comparison_baseline": "s196_bctl_ref_r0330 reference(참조)",
            "trade_shape": f"cd8 net={cd8['validation_net']}, dd={cd8['validation_dd_percent']}, mid_pf={cd8['validation_mid_pf']}, late={cd8['validation_late_net_share']}, oos_pf={cd8['oos_pf']}",
            "likely_drivers": "same-direction re-entry cooldown(동방향 재진입 대기)이 반복 진입 손실 일부를 줄였지만 DD(낙폭) 기준까지는 부족했다.",
            "next_probe": "Stage198(198단계)은 cd8 clue(대기 8 단서)를 보조로 두고 MAE/MFE(최대불리/최대유리)와 drawdown phase(낙폭 국면)를 본다.",
            "attribution_confidence": "medium_high(중상)",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage198_primary(198단계 주 경로)",
            "decision": DECISION,
            "source_clue": "s196_bctl_cd8_r0325_best_tradeoff_not_pass(최선 상충안이지만 통과 아님)",
            "bounded_question": "Can Stage198(198단계) shave the remaining DD(낙폭) gap by guarding adverse excursion(불리한 움직임) without erasing cd8/r0325 net/PF/OOS(대기8/위험0.0325 순손익/수익요인/표본외)?",
            "why": "Stage196 best still has DD above 34D and mid PF below 34D, so risk-only compression is insufficient.",
            "guardrail": "no_risk_increase; preserve_late_share_below_50; preserve_oos_pf_near_1_9(위험 상향 금지; 후반 비중 50% 아래 유지; 표본외 수익요인 1.9 근처 유지)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "s196_bctl_r0320_net_midpf_erosion(위험0.0320 순손익/중반 약화)",
            "bounded_question": "Do not solve DD(낙폭) by simply shrinking risk until edge(우위) collapses.",
            "why": "r0320 improves DD more than r0325, but mid PF and net weaken and DD still does not pass.",
            "guardrail": "do_not_accept_risk_only_cosmetic_dd(위험만 줄인 겉보기 낙폭 개선 수용 금지)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    rows = by_adapter(tradeoff_rows)
    best = best_tradeoff(tradeoff_rows)
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in tradeoff_rows:
        lines.append(
            "| {adapter} | {pf} | {net} | {dd} | {mid} | {late} | {oos} | {read} |".format(
                adapter=item["adapter_id"],
                pf=item["validation_pf"],
                net=item["validation_net"],
                dd=item["validation_dd_percent"],
                mid=item["validation_mid_pf"],
                late=item["validation_late_net_share"],
                oos=item["oos_pf"],
                read=item["stage197_read"],
            )
        )
    cd8 = rows["s196_bctl_cd8_r0325"]
    r0320 = rows["s196_bctl_r0320"]
    return f"""# Stage197 Follow-up Review(197단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage196_evidence_commit(원천 196단계 근거 커밋): `{SOURCE_STAGE196_EVIDENCE_COMMIT}`
- source_stage196_hash_record_commit(원천 196단계 해시 기록 커밋): `{SOURCE_STAGE196_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

{chr(10).join(lines)}

## Easy Read(쉬운 판독)

Stage196(196단계)은 hard pass(강한 통과)를 만들지 못했다. Best tradeoff(최선 상충안)는 `{best['adapter_id']}`이고, validation net(검증 순손익) `{best['validation_net']}`, validation PF(검증 수익요인) `{best['validation_pf']}`, validation DD(검증 낙폭) `{best['validation_dd_percent']}`, mid PF(중반 수익요인) `{best['validation_mid_pf']}`, OOS PF(표본외 수익요인) `{best['oos_pf']}`다.

이 값은 net/PF/OOS(순손익/수익요인/표본외)는 강하지만, DD(낙폭)는 34D(34D) 기준 `{LEGACY_34D['max_drawdown_percent']}`보다 아직 높고 mid PF(중반 수익요인)는 34D PF(34D 수익요인) `{LEGACY_34D['profit_factor']}`보다 낮다. Effect(효과): Stage196(196단계)은 후보를 보존하되 최종으로 보지 않는다.

`s196_bctl_r0320`은 DD(낙폭)를 `{r0320['validation_dd_percent']}`까지 낮췄지만 net(순손익) `{r0320['validation_net']}`와 mid PF(중반 수익요인) `{r0320['validation_mid_pf']}`가 약해졌다. `s196_bctl_cd8_r0325`는 `{cd8['validation_dd_percent']}` DD(낙폭), `{cd8['validation_mid_pf']}` mid PF(중반 수익요인)로 더 균형이 좋지만 여전히 pass(통과)는 아니다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage196(196단계) bctl DD compression/mid PF guard(bctl 낙폭 압축/중반 수익요인 방어).
- evidence_available(사용 가능 근거): Stage196 MT5 Strategy Tester(메타트레이더5 전략 테스터), quality matrix(품질 행렬), segment KPI(구간 핵심 성과 지표), balance curve audit(잔고 곡선 감사), risk/ATR telemetry(위험/ATR 기록).
- judgment_label(판정 라벨): `candidate_not_final_due_to_dd_midpf_gap(낙폭/중반 수익요인 격차로 최종 아님)`.
- next_condition(다음 조건): Stage198(198단계)은 adverse excursion(불리한 움직임)과 drawdown phase(낙폭 국면)를 겨냥해 DD(낙폭)를 더 줄이되, cd8/r0325(대기8/위험0.0325)의 net/PF/OOS(순손익/수익요인/표본외)를 보존해야 한다.

Stage197(197단계)는 research/development only(연구개발 전용)다. Effect(효과): 다음 연구 단계의 질문만 열며 overall goal complete(전체 목표 완료), deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)를 만들지 않는다.
"""


def decision_md() -> str:
    return f"""# Stage197 Decision(197단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage196_evidence_commit(원천 196단계 근거 커밋): `{SOURCE_STAGE196_EVIDENCE_COMMIT}`
- source_stage196_hash_record_commit(원천 196단계 해시 기록 커밋): `{SOURCE_STAGE196_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage197(197단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage198(198단계)에서 adverse excursion DD guard(불리한 움직임 낙폭 방어)를 좁게 시험한다.
"""


def write_next_stage_seed() -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage198(198단계)은 Stage197(197단계) 판독에서 고른 `s196_bctl_cd8_r0325` 단서를 adverse excursion DD guard(불리한 움직임 낙폭 방어)로 좁게 수리한다.

## Bounded Question(경계 질문)

Can Stage198(198단계) reduce the remaining validation DD(검증 낙폭) gap below 34D(34D) by guarding adverse excursion/drawdown phase(불리한 움직임/낙폭 국면) while preserving cd8/r0325 net/PF/OOS/late-share(대기8/위험0.0325 순손익/수익요인/표본외/후반 비중)?

Effect(효과): risk-only compression(위험만 압축)이 부족하다는 Stage196(196단계) 근거를 받아, 진입 품질/손실 국면 자체를 좁게 겨냥한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage198 Inputs(198단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- primary_clue(주 단서): `s196_bctl_cd8_r0325`
- source_quality_matrix(원천 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_segment_kpi(원천 구간 핵심 성과 지표): `{rel(SOURCE_SEGMENT_PATH)}`
- source_balance_audit(원천 잔고 곡선 감사): `{rel(SOURCE_BALANCE_PATH)}`
- source_risk_atr(원천 위험/ATR 기록): `{rel(SOURCE_RISK_ATR_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage198 Review Index(198단계 검토 색인)

- status(상태): `open_planned_from_stage197`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage198 Selection Status(198단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage197`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]]) -> None:
    best = best_tradeoff(tradeoff_rows)
    primary_kpi = (
        f"best={best['adapter_id']};"
        f"validation_net={best['validation_net']};"
        f"validation_pf={best['validation_pf']};"
        f"validation_dd={best['validation_dd_percent']};"
        f"validation_mid_pf={best['validation_mid_pf']};"
        f"oos_pf={best['oos_pf']}"
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage196_bctl_dd_midpf_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage196_bctl_dd_midpf_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage196_bctl_dd_midpf_tradeoff",
        "scoreboard_lane": "regular_risk_execution",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": primary_kpi,
        "guardrail_kpi": f"claim_boundary={BOUNDARY};overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage197 reviewed Stage196 bctl DD/mid PF tradeoff and opened Stage198 adverse excursion DD guard repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage197_stage196_bctl_dd_midpf_followup_review",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            (
                ("source_stage196_evidence_commit", SOURCE_STAGE196_EVIDENCE_COMMIT),
                ("source_stage196_hash_record_commit", SOURCE_STAGE196_HASH_RECORD_COMMIT),
                ("target_surface", TARGET_SURFACE),
                ("overall_goal_complete", 0),
            )
        ),
    }
    write_csv(STAGE_LEDGER_PATH, [ledger_row], columns=s172.ALPHA_LEDGER_COLUMNS)
    upsert_csv_rows(RUN_REGISTRY_PATH, s172.RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, s172.ALPHA_LEDGER_COLUMNS, [ledger_row], key="ledger_row_id")


def artifact_rows() -> list[dict[str, Any]]:
    paths = [
        (REPORT_PATH, "Stage197 bounded follow-up review report."),
        (TRADEOFF_MATRIX_PATH, "Stage197 bctl DD/mid PF tradeoff matrix."),
        (ATTRIBUTION_PATH, "Stage197 performance attribution."),
        (ROUTE_MATRIX_PATH, "Stage197 route matrix."),
        (DECISION_PATH, "Stage197 decision."),
        (STAGE_LEDGER_PATH, "Stage197 local ledger."),
    ]
    created = s172.utc_now()
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage197_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": note,
        }
        for path, note in paths
    ]


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "external_verification_status": EXTERNAL_STATUS,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
        "attribution": rel(ATTRIBUTION_PATH),
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "tradeoff_rows": list(tradeoff_rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    s172.write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    s172.write_json(PACKET_ROOT / "packet_receipt.json", payload)
    s172.write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage197 Closeout Packet(197단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `completed`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage197(197단계) closed(종료) as `{DECISION}` and Stage198(198단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage196(196단계)의 risk-only compression(위험만 압축) 한계를 adverse excursion DD guard(불리한 움직임 낙폭 방어) 수리로 넘긴다.
- >-
  Stage197 evidence(197단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): `s196_bctl_cd8_r0325`를 최선 단서로 남기되 DD/mid PF(낙폭/중반 수익요인) 실패를 최종 완료로 오해하지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage197_stage196_bctl_dd_midpf_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage197_stage196_bctl_dd_midpf_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_MATRIX_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    s172.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage197_stage196_bctl_dd_midpf_followup_review`
- status(상태): `stage197_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage197(197단계)는 Stage196(196단계) bctl DD/mid PF(bctl 낙폭/중반 수익요인) 결과를 follow-up review(후속 검토)했다. Effect(효과): Stage198(198단계)은 adverse excursion DD guard(불리한 움직임 낙폭 방어)를 좁게 시험한다.

## Latest Stage197 Evidence(최신 197단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    s172.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage197 Selection Status(197단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
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
    s172.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage197 Review Index(197단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage197 Stage196 bctl DD mid PF follow-up review closeout(197단계 196단계 bctl 낙폭 중반 수익요인 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage196(196단계)의 최선 상충안과 실패 원인을 분리해 Stage198(198단계) adverse excursion DD guard(불리한 움직임 낙폭 방어)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows()
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows))
    s172.write_md(DECISION_PATH, decision_md())
    write_ledgers(tradeoff_rows)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, s172.ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows)
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
                    "external_verification_status": EXTERNAL_STATUS,
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                    "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
