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
from stage_pipelines.stage194 import tp475_late_concentration_midpf_repair as s194  # noqa: E402

s172 = s194.s172

STAGE_ID = "195_adapter_research__stage194_late_midpf_followup_review"
RUN_ID = "run195A_stage195_stage194_late_midpf_followup_review_v1"
PACKET_ID = "stage195_stage194_late_midpf_followup_review_v1"
PARENT_RUN_ID = "run194A_stage194_tp475_late_concentration_midpf_repair_v1"
SOURCE_STAGE_ID = "194_adapter_research__tp475_late_concentration_midpf_repair"
SOURCE_RUN_ID = "run194A_stage194_tp475_late_concentration_midpf_repair_v1"
SOURCE_STAGE194_EVIDENCE_COMMIT = "213694f828f8326fea63f2d7b478ee07ea5c1edb"
SOURCE_STAGE194_HASH_RECORD_COMMIT = "705c68300d5e82217414ba4bee4e5f97fd9477aa"
NEXT_STAGE_ID = "196_adapter_research__bctl_dd_compression_midpf_guard"
NEXT_RUN_ID = "run196A_stage196_bctl_dd_compression_midpf_guard_v1"
NEXT_PACKET_ID = "stage196_bctl_dd_compression_midpf_guard_v1"
DECISION = "open_stage196_bctl_dd_compression_midpf_guard_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage194_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_bctl_dd_midpf_guard"
BOUNDARY = s194.BOUNDARY
LEGACY_34D = s194.LEGACY_34D

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/194_adapter_research__tp475_late_concentration_midpf_repair/03_reviews/stage194_quality_matrix.csv")
SOURCE_SEGMENT_PATH = Path("stages/194_adapter_research__tp475_late_concentration_midpf_repair/03_reviews/stage194_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/194_adapter_research__tp475_late_concentration_midpf_repair/03_reviews/stage194_balance_curve_audit.csv")
SOURCE_CONCENTRATION_PATH = Path("stages/194_adapter_research__tp475_late_concentration_midpf_repair/03_reviews/stage194_concentration_risk_summary.csv")
SOURCE_RISK_ATR_PATH = Path("stages/194_adapter_research__tp475_late_concentration_midpf_repair/03_reviews/stage194_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/194_adapter_research__tp475_late_concentration_midpf_repair/03_reviews/stage194_tp475_late_midpf_report.md")
SOURCE_DECISION_PATH = Path("stages/194_adapter_research__tp475_late_concentration_midpf_repair/03_reviews/stage194_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage195_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage195_late_midpf_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage195_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage195_route_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage195_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage195/stage194_late_midpf_followup_review.py")


def rel(path: Path | str) -> str:
    return s172.rel(path)


def fnum(value: Any, default: float = 0.0) -> float:
    return s172.as_float({"value": value}, "value", default)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    inferred_columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in inferred_columns:
                inferred_columns.append(key)
    fieldnames = list(columns or inferred_columns)
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


def stage195_read(adapter_id: str, row: Mapping[str, Any]) -> str:
    flags = str(row.get("quality_flags", ""))
    if adapter_id == "s194_bctl_tp475_r0330":
        return "best_tradeoff_net_oos_late_pass_but_dd_regression_midpf_short(최선 상충 순손익/표본외/후반 통과 낙폭 회귀 중반 부족)"
    if adapter_id == "s194_cd8_r0330":
        return "dd_preserved_small_midpf_gain_late_still_above_50(낙폭 보존 중반 소폭 개선 후반 50퍼센트 초과)"
    if adapter_id == "s194_hold2_r0330":
        return "hold_compression_failure_net_midpf_destroyed_late_worse(보유 압축 실패 순손익/중반 훼손 후반 악화)"
    if "validation_late_concentration_above_50pct" in flags:
        return "reference_net_dd_pass_midpf_late_fail(참조 순손익/낙폭 통과 중반/후반 실패)"
    return "measurement_review_required(측정 검토 필요)"


def build_tradeoff_rows(quality_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = by_adapter(quality_rows).get("s194_ref_r0330", {})
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        mid = segment_lookup(segment_rows, adapter_id, "validation_is", "mid")
        late = segment_lookup(segment_rows, adapter_id, "validation_is", "late")
        val_net = fnum(row.get("validation_net"))
        val_dd = fnum(row.get("validation_balance_dd_percent"))
        val_mid = fnum(row.get("validation_mid_pf"))
        late_share = fnum(row.get("validation_late_net_share"))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": round(val_net - LEGACY_34D["net_profit"], 6),
                "validation_net_delta_vs_ref": round(val_net - fnum(ref.get("validation_net")), 6),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_gap_above_34d": round(val_dd - LEGACY_34D["max_drawdown_percent"], 6),
                "validation_dd_delta_vs_ref": round(val_dd - fnum(ref.get("validation_balance_dd_percent")), 6),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d_pf": round(val_mid - LEGACY_34D["profit_factor"], 6),
                "validation_mid_pf_delta_vs_ref": round(val_mid - fnum(ref.get("validation_mid_pf")), 6),
                "validation_mid_net": mid.get("net_profit", ""),
                "validation_mid_mfe_capture": mid.get("mfe_capture_ratio", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_late_share_margin_to_50pct": round(0.50 - late_share, 6),
                "validation_late_share_delta_vs_ref": round(late_share - fnum(ref.get("validation_late_net_share")), 6),
                "validation_late_pf": late.get("profit_factor", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage195_read": stage195_read(adapter_id, row),
            }
        )
    return rows


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_id = by_adapter(tradeoff_rows)
    ref = by_id["s194_ref_r0330"]
    bctl = by_id["s194_bctl_tp475_r0330"]
    cd8 = by_id["s194_cd8_r0330"]
    hold2 = by_id["s194_hold2_r0330"]
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "bctl context rebalance(문맥 재균형)가 validation net/PF/OOS(검증 순손익/수익요인/표본외)와 late share(후반 비중)를 개선했지만 DD(낙폭)를 34D(34D) 위로 밀었다.",
            "comparison_baseline": "s194_ref_r0330 reference(참조)",
            "likely_drivers": "long gate(롱 게이트)가 wide_lowedge(넓은 저엣지)에서 lowedge_gate(저엣지 게이트)로 바뀌며 trade supply(거래 공급)가 늘었고 수익도 늘었지만 손실 클러스터도 커졌다.",
            "segment_checks": "validation/OOS(검증/표본외), chronological third(시간 3분할), mid PF(중반 수익요인), late share(후반 비중), balance DD(잔고 낙폭)를 확인했다.",
            "trade_shape": f"ref net={ref['validation_net']}, dd={ref['validation_dd_percent']}, mid_pf={ref['validation_mid_pf']}, late={ref['validation_late_net_share']}; bctl net={bctl['validation_net']}, dd={bctl['validation_dd_percent']}, mid_pf={bctl['validation_mid_pf']}, late={bctl['validation_late_net_share']}",
            "alternative_explanations": "수익 개선은 신호 품질 자체보다 문맥 허용 폭과 거래 수 증가의 효과일 수 있다.",
            "attribution_confidence": "medium_high(중상)",
            "next_probe": "Stage196(196단계)은 bctl(문맥 재균형)을 기준으로 DD(낙폭)를 34D(34D) 아래로 압축하고 mid PF(중반 수익요인)를 지키는 변형만 본다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "cd8 cooldown widening(8봉 대기 확대)은 DD(낙폭)를 지키면서 mid PF(중반 수익요인)를 조금 올렸지만 late share(후반 비중)는 50% 위에 남았다.",
            "comparison_baseline": "s194_ref_r0330 reference(참조)",
            "likely_drivers": "same-direction re-entry cooldown(동방향 재진입 대기) 확대가 일부 반복 진입을 줄였지만 profit timing(수익 시간대) 의존성은 충분히 깨지 못했다.",
            "segment_checks": "mid/late segment(중반/후반 구간), OOS PF(표본외 수익요인), DD recovery(낙폭 회복)를 확인했다.",
            "trade_shape": f"cd8 net={cd8['validation_net']}, dd={cd8['validation_dd_percent']}, mid_pf={cd8['validation_mid_pf']}, late={cd8['validation_late_net_share']}",
            "alternative_explanations": "cooldown(대기)의 효과는 작고, late concentration(후반 집중)은 세션/국면 의존성일 수 있다.",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Stage196(196단계)에서 bctl(문맥 재균형)과 DD guard(낙폭 방어)를 조합할 때 cd8(8봉 대기)은 보조 단서로만 둔다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "hold2(2봉 보유)는 DD(낙폭)를 낮췄지만 net/mid PF(순손익/중반 수익요인)를 크게 훼손하고 late concentration(후반 집중)을 악화했다.",
            "comparison_baseline": "s194_ref_r0330 reference(참조)",
            "likely_drivers": "max hold(최대 보유) 2봉은 winning trade(수익 거래)의 MFE capture(최대 유리 이동 포착)를 너무 일찍 끊었다.",
            "segment_checks": "validation early/mid/late(검증 초반/중반/후반), OOS net(표본외 순손익), MFE capture(최대 유리 이동 포착)를 확인했다.",
            "trade_shape": f"hold2 net={hold2['validation_net']}, dd={hold2['validation_dd_percent']}, mid_pf={hold2['validation_mid_pf']}, late={hold2['validation_late_net_share']}",
            "alternative_explanations": "짧은 보유가 손실을 줄이는 대신 수익 실현 구조를 망가뜨린 결과일 수 있다.",
            "attribution_confidence": "high(높음)",
            "next_probe": "Stage196(196단계)에서는 hard hold2(강제 2봉 보유)를 반복하지 않는다.",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage196_primary(196단계 주 경로)",
            "decision": DECISION,
            "source_clue": "s194_bctl_tp475_r0330_net_oos_late_pass_dd_fail(문맥 재균형 순손익/표본외/후반 통과 낙폭 실패)",
            "bounded_question": "Can Stage196(196단계) keep bctl(문맥 재균형) net/PF/OOS/late-share(순손익/수익요인/표본외/후반 비중) gains while compressing validation DD(검증 낙폭) below 34D(34D) and guarding mid PF(중반 수익요인)?",
            "why": "bctl net=1161.27, PF=1.73, late_share=0.4887, OOS PF=1.95 are strongest, but DD=13.4559 exceeds 34D by about 0.5468pp and mid PF=1.5251 is still short.",
            "guardrail": "no_risk_increase; preserve_late_share_below_50; do_not_repeat_hold2_failure(위험 상향 금지; 후반 비중 50퍼센트 아래 보존; 2봉 보유 실패 반복 금지)",
        },
        {
            "run_id": RUN_ID,
            "route": "supporting_clue(보조 단서)",
            "decision": DECISION,
            "source_clue": "s194_cd8_r0330_dd_preserved_late_still_fail(8봉 대기 낙폭 보존 후반 실패)",
            "bounded_question": "Can cooldown(대기) be used only as a DD guard(낙폭 방어) if it does not erase bctl(문맥 재균형) gains?",
            "why": "cd8 DD=12.7954 stayed inside 34D but late_share=0.5132 remained above 50%.",
            "guardrail": "cooldown_is_guard_not_primary_fix(대기는 보조 방어이지 주 수리가 아님)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "s194_hold2_r0330_net_midpf_damage(2봉 보유 순손익/중반 훼손)",
            "bounded_question": "Do not repeat hard hold2(강제 2봉 보유) as the next repair path.",
            "why": "hold2 validation net=380.76 and mid_pf=1.0836 collapsed while late_share=0.763 worsened.",
            "guardrail": "do_not_hide_failed_branch(실패 분기 숨기지 않기)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    def row(adapter_id: str) -> Mapping[str, Any]:
        return by_adapter(tradeoff_rows)[adapter_id]

    bctl = row("s194_bctl_tp475_r0330")
    cd8 = row("s194_cd8_r0330")
    hold2 = row("s194_hold2_r0330")
    ref = row("s194_ref_r0330")
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
                read=item["stage195_read"],
            )
        )
    return f"""# Stage195 Follow-up Review(195단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage194_evidence_commit(원천 194단계 근거 커밋): `{SOURCE_STAGE194_EVIDENCE_COMMIT}`
- source_stage194_hash_record_commit(원천 194단계 해시 기록 커밋): `{SOURCE_STAGE194_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

{chr(10).join(lines)}

## Easy Read(쉬운 판독)

Stage194(194단계)는 one clean winner(깔끔한 승자)를 만들지 못했다. `s194_bctl_tp475_r0330`은 validation net(검증 순손익) `{bctl['validation_net']}`, validation PF(검증 수익요인) `{bctl['validation_pf']}`, late share(후반 비중) `{bctl['validation_late_net_share']}`, OOS PF(표본외 수익요인) `{bctl['oos_pf']}`로 가장 좋은 수리 단서다.

하지만 bctl(문맥 재균형)은 validation DD(검증 낙폭) `{bctl['validation_dd_percent']}`로 34D(34D) 한계 `{LEGACY_34D['max_drawdown_percent']}`를 넘었고, mid PF(중반 수익요인) `{bctl['validation_mid_pf']}`도 34D PF(34D 수익요인) `{LEGACY_34D['profit_factor']}`보다 낮다. Effect(효과): bctl(문맥 재균형)은 final(최종)이 아니라 다음 수리의 anchor clue(기준 단서)다.

`s194_cd8_r0330`은 DD(낙폭)를 `{cd8['validation_dd_percent']}`로 지켰지만 late share(후반 비중)가 `{cd8['validation_late_net_share']}`라 아직 실패다. `s194_hold2_r0330`은 net(순손익) `{hold2['validation_net']}`로 무너져 failure memory(실패 기억)로 남긴다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage194(194단계) TP4.75/r0330(TP4.75/위험 0.0330) late/mid repair(후반/중반 수정).
- evidence_available(사용 가능 근거): Stage194 MT5 Strategy Tester(메타트레이더5 전략 테스터), quality matrix(품질 행렬), segment KPI(구간 핵심 성과 지표), balance curve audit(잔고 곡선 감사), risk/ATR telemetry(위험/ATR 기록).
- evidence_missing(빠진 근거): Stage196(196단계)의 DD-compressed bctl(낙폭 압축 문맥 재균형) 재측정.
- judgment_label(판정 라벨): `exploratory_candidate_not_final(탐색 후보 최종 아님)`.
- claim_boundary(주장 경계): research/development only(연구개발 전용). deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 금지다.
- next_condition(다음 조건): bctl(문맥 재균형)의 net/PF/OOS/late-share(순손익/수익요인/표본외/후반 비중)를 보존하면서 validation DD(검증 낙폭)를 34D(34D) 아래로 압축하고 mid PF(중반 수익요인)를 올리는 Stage196(196단계) 측정.

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): bctl(문맥 재균형)이 가장 좋은 수익/후반 비중 단서지만 DD(낙폭)가 한계를 넘었다.
- effect(효과): Stage196(196단계)은 위험 상향 없이 bctl(문맥 재균형)의 DD/mid PF(낙폭/중반 수익요인) 상충만 좁게 수리한다.

Stage195(195단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과 판독은 다음 연구 단계를 여는 근거이지 전체 목표 완료가 아니다.
"""


def decision_md() -> str:
    return f"""# Stage195 Decision(195단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage194_evidence_commit(원천 194단계 근거 커밋): `{SOURCE_STAGE194_EVIDENCE_COMMIT}`
- source_stage194_hash_record_commit(원천 194단계 해시 기록 커밋): `{SOURCE_STAGE194_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage195(195단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage196(196단계)에서 bctl(문맥 재균형)의 DD/mid PF(낙폭/중반 수익요인) 상충을 좁게 수리한다.
"""


def write_next_stage_seed() -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage196(196단계)은 Stage195(195단계)에서 고른 bctl(문맥 재균형) 단서를 DD compression/mid PF guard(낙폭 압축/중반 수익요인 방어)로 좁게 수리한다.

## Bounded Question(경계 질문)

Can Stage196(196단계) preserve `s194_bctl_tp475_r0330` net/PF/OOS/late-share(순손익/수익요인/표본외/후반 비중) gains while compressing validation DD(검증 낙폭) below 34D(34D) and improving or guarding mid PF(중반 수익요인), without risk-only increase(위험만 상향)?

Effect(효과): Stage194(194단계)의 가장 좋은 단서를 버리지 않고, 실패한 DD/mid PF(낙폭/중반 수익요인)만 좁게 고친다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage196 Inputs(196단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- primary_clue(주 단서): `s194_bctl_tp475_r0330`
- source_quality_matrix(원천 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_segment_kpi(원천 구간 핵심 성과 지표): `{rel(SOURCE_SEGMENT_PATH)}`
- source_balance_audit(원천 잔고 곡선 감사): `{rel(SOURCE_BALANCE_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage196 Review Index(196단계 검토 색인)

- status(상태): `open_planned_from_stage195`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage196 Selection Status(196단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage195`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]]) -> None:
    bctl = by_adapter(tradeoff_rows)["s194_bctl_tp475_r0330"]
    primary_kpi = (
        f"best_clue=s194_bctl_tp475_r0330;"
        f"validation_net={bctl['validation_net']};"
        f"validation_dd={bctl['validation_dd_percent']};"
        f"validation_mid_pf={bctl['validation_mid_pf']};"
        f"validation_late_share={bctl['validation_late_net_share']};"
        f"oos_pf={bctl['oos_pf']}"
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage194_late_midpf_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage194_late_midpf_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage194_late_midpf_bctl_dd_tradeoff",
        "scoreboard_lane": "regular_risk_execution",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": primary_kpi,
        "guardrail_kpi": f"claim_boundary={BOUNDARY};overall_goal_complete=0;route_count=3",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage195 reviewed Stage194 late/mid repair and opened Stage196 bctl DD compression guard.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage195_stage194_late_midpf_followup_review",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            (
                ("source_stage194_evidence_commit", SOURCE_STAGE194_EVIDENCE_COMMIT),
                ("source_stage194_hash_record_commit", SOURCE_STAGE194_HASH_RECORD_COMMIT),
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
        (REPORT_PATH, "Stage195 bounded follow-up review report."),
        (TRADEOFF_MATRIX_PATH, "Stage195 late/mid/DD tradeoff matrix."),
        (ATTRIBUTION_PATH, "Stage195 performance attribution."),
        (ROUTE_MATRIX_PATH, "Stage195 route matrix."),
        (DECISION_PATH, "Stage195 decision."),
        (STAGE_LEDGER_PATH, "Stage195 local ledger."),
    ]
    created = s172.utc_now()
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage195_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": note,
        }
        for path, note in paths
    ]


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> None:
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
        f"""# Stage195 Closeout Packet(195단계 종료 작업 묶음)

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
  Stage195(195단계) closed(종료) as `{DECISION}` and Stage196(196단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage194(194단계)의 bctl(문맥 재균형) 단서를 DD/mid PF(낙폭/중반 수익요인) 수리로 넘긴다.
- >-
  Stage195 evidence(195단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): bctl(문맥 재균형)의 순손익/후반 비중 장점과 낙폭 실패를 분리해 기록한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage195_stage194_late_midpf_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage195_stage194_late_midpf_followup_review:
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
  attribution_path: {rel(ATTRIBUTION_PATH)}
  route_matrix_path: {rel(ROUTE_MATRIX_PATH)}
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
- adapter_under_review(검토 중 어댑터): `stage196_bctl_dd_compression_midpf_guard`
- status(상태): `stage195_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage195(195단계)는 Stage194(194단계) 결과를 review(검토)했고 `s194_bctl_tp475_r0330`을 best clue(최선 단서)로 남겼다. Effect(효과): Stage196(196단계)는 bctl(문맥 재균형)의 net/PF/OOS/late-share(순손익/수익요인/표본외/후반 비중) 장점을 보존하면서 DD/mid PF(낙폭/중반 수익요인)를 좁게 수리한다.

## Latest Stage195 Evidence(최신 195단계 근거)

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
        f"""# Stage195 Selection Status(195단계 선택 상태)

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
        f"""# Stage195 Review Index(195단계 검토 색인)

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
        f"\n## {s172.utc_now()} Stage195 Stage194 late/mid follow-up review closeout(195단계 194단계 후반/중반 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): bctl(문맥 재균형)을 다음 DD/mid PF(낙폭/중반 수익요인) 수리 단서로 고정하고, hold2(2봉 보유)는 실패 기억으로 남겼다.\n"
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
    artifacts = artifact_rows()
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, s194.ARTIFACT_COLUMNS, artifacts, key="artifact_id")
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
                    "report": rel(REPORT_PATH),
                    "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
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
