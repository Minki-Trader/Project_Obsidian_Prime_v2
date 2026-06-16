from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_69 import frontier69b_event_first_first_hit_proxy_sweep as f69b
from stage_pipelines.stage_frontier_69 import frontier69d_event_first_onnx_runtime_probe as f69d
from stage_pipelines.stage_frontier_69 import frontier69e_proxy_runtime_gap_analysis_and_repair_decision as f69e


STAGE_ID = f69b.STAGE_ID
RUN_ID = "frontier69F_stage_closeout_event_first_axis_rotation_v1"
PARENT_RUN_ID = f69e.RUN_ID
NEXT_STAGE_ID = "stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation"
NEXT_RUN_ID = "frontier70A_stage_open_regime_specific_asymmetric_value_exit_model_rotation_v1"
IDEA_ID = f69b.IDEA_ID

STATUS = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory_no_authority"
CLAIM_BOUNDARY = (
    "preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F69D_RECEIPT = REVIEWS_ROOT / "f69d_runtime_probe_receipt_review.csv"
F69D_GAP = REVIEWS_ROOT / "f69d_gap_classification_review.csv"
F69E_DECISION = REVIEWS_ROOT / "f69e_proxy_runtime_gap_decision_review.json"
F69E_REPORT = REVIEWS_ROOT / "frontier69E_proxy_runtime_gap_analysis_and_repair_decision_report.md"
F69E_SWEEP = REVIEWS_ROOT / "f69e_trade_shape_repair_sweep_review.csv"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f69_stage_closeout_event_first_axis_rotation"
GROK_PROMPT = GROK_PACKET / "prompts/f69_stage_closeout_event_first_axis_rotation_prompt.md"
GROK_CLEAN = GROK_PACKET / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET / "outputs/metadata.json"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
CLOSEOUT_SUMMARY = RUN_ROOT / "frontier69F_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEWS_ROOT / "stage_closeout_report.md"
GROK_RECEIPT = REVIEWS_ROOT / "f69_stage_closeout_grok_receipt.md"
GATE_AUDIT = REVIEWS_ROOT / "required_gate_coverage_audit_f69f.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_ROOT / "stage_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs/registers/negative_result_register.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS = SELECTED_ROOT / "selection_status.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def num(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: Any, digits: int = 6) -> str:
    number = num(value)
    if number is None:
        text = str(value or "")
        return text
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def percent_text(value: Any) -> str:
    text = fmt(value)
    return text if text.endswith("%") else f"{text}%"


def grok_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def closeout_kpi_rows(runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in runtime_rows:
        output.append(
            {
                "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
                "split_view": f"{row.get('split')} / {row.get('axis_id')}",
                "net_profit": row.get("net_profit"),
                "gross_profit": row.get("gross_profit"),
                "gross_loss": row.get("gross_loss"),
                "profit_factor": row.get("profit_factor"),
                "drawdown_percent": row.get("max_drawdown_percent"),
                "trade_count": row.get("trade_count"),
                "trades_per_day": row.get("trades_per_day"),
                "win_rate": row.get("win_rate_percent"),
                "average_win": row.get("average_win"),
                "average_loss": row.get("average_loss"),
                "payoff_ratio": row.get("payoff_ratio"),
                "expectancy": row.get("expectancy"),
                "recovery_factor": row.get("recovery_factor"),
                "time_under_water": "not_available_from_f69d_strategy_report_parse(전략 테스터 파싱에서 없음)",
                "max_consecutive_loss": "not_available_from_f69d_strategy_report_parse(전략 테스터 파싱에서 없음)",
                "long_short_breakdown": f"long={row.get('long_trade_count')};short={row.get('short_trade_count')}",
                "proxy_runtime_gap": (
                    f"proxy_pf={fmt(row.get('proxy_profit_factor'))};runtime_pf={fmt(row.get('profit_factor'))};"
                    f"proxy_tpd={fmt(row.get('proxy_trades_per_day'))};runtime_tpd={fmt(row.get('trades_per_day'))};"
                    f"proxy_dd={fmt(row.get('proxy_dd_percent'))};runtime_dd={fmt(row.get('max_drawdown_percent'))}"
                ),
            }
        )
    return output


def classify_grok_advice() -> dict[str, Any]:
    return {
        "accepted": [
            "closeout_label_honest(마감 라벨 정직함)",
            "no_mandatory_extra_trade_shape_mt5_repair(추가 거래 형태 MT5 수리 필수 아님)",
            "next_frontier_should_pivot_label_and_model_family(다음 전선은 라벨과 모델 계열을 전환해야 함)",
        ],
        "rejected": [
            "none(없음)",
        ],
        "needs_local_verification": [
            "HGB fallback scope(HGB 대체 범위)",
        ],
        "local_verification": {
            "HGB fallback scope(HGB 대체 범위)": (
                "accepted_as_guardrail_only(보호 장치 전용으로 수용). F69D pre-MT5 receipt records HGB exclusion accepted and HGB fallback temptation guarded; "
                "F69D final direction was fixed two ExtraTrees axes and both exported successfully."
            )
        },
        "forbidden_claim_check": "passed_no_completion_baseline_promotion_runtime_authority_live_readiness_goal_achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)",
    }


def build_summary(runtime_rows: Sequence[Mapping[str, Any]], f69e_decision: Mapping[str, Any]) -> dict[str, Any]:
    kpi = closeout_kpi_rows(runtime_rows)
    f69e_sweep = f69e_decision["repair_sweep"]
    sparse_oos = next((row for row in runtime_rows if row.get("axis_id") == "pf_sparse_export_axis" and row.get("split") == "oos"), {})
    dense_oos = next((row for row in runtime_rows if row.get("axis_id") == "density_weak_export_axis" and row.get("split") == "oos"), {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "closeout_label": JUDGMENT,
        "hypothesis": "Event-first first-hit opportunity modeling can create a new PF source after F68 risk-only negative memory.",
        "test_period": "validation 2025-01-02..2025-10-01; oos 2025-10-01..2026-04-14",
        "runtime_probe_rows": len(runtime_rows),
        "strict_joint_pass_count": 0,
        "preserved_clue": [
            "exact_onnx_probability_signal_feature_parity(정확한 온엑스/확률/신호/피처 동등성)",
            "runtime_veto_tape_observation_tooling(런타임 차단 테이프 관찰 도구화)",
            "sparse_event_first_pf_clue_but_too_thin(희박 이벤트 우선 PF 단서, 너무 얇음)",
        ],
        "negative_memory": [
            "event_first_extratrees_trade_shape_only_repair_failed_joint_axes(이벤트 우선 엑스트라트리스 거래 형태 단독 수리는 네 축 동시 실패)",
            "density_lift_collapses_pf_or_dd(밀도 상승은 PF 또는 DD를 훼손)",
            "same_surface_threshold_cooldown_daily_quota_loop_should_not_repeat(동일 표면 임계값/쿨다운/일별 할당 반복 금지)",
        ],
        "closeout_kpi": kpi,
        "runtime_snapshot": {
            "sparse_oos_net": num(sparse_oos.get("net_profit")),
            "sparse_oos_pf": num(sparse_oos.get("profit_factor")),
            "sparse_oos_dd": num(sparse_oos.get("max_drawdown_percent")),
            "sparse_oos_trades_day": num(sparse_oos.get("trades_per_day")),
            "dense_oos_net": num(dense_oos.get("net_profit")),
            "dense_oos_pf": num(dense_oos.get("profit_factor")),
            "dense_oos_dd": num(dense_oos.get("max_drawdown_percent")),
            "dense_oos_trades_day": num(dense_oos.get("trades_per_day")),
        },
        "f69e_repair_sweep": {
            "sweep_rows": f69e_sweep["sweep_rows"],
            "final_gate_like_count": f69e_sweep["final_gate_like_count"],
            "joint_soft_count": f69e_sweep["joint_soft_count"],
            "density_at_least_3_both_count": f69e_sweep["density_at_least_3_both_count"],
        },
        "grok": {
            "packet": rel(GROK_PACKET),
            "prompt": rel(GROK_PROMPT),
            "clean_output": rel(GROK_CLEAN),
            "metadata": rel(GROK_METADATA),
            "prompt_hash": grok_hash(GROK_PROMPT),
            "clean_output_hash": grok_hash(GROK_CLEAN),
            "classification": classify_grok_advice(),
        },
        "five_stage_retrospective": {
            "after_f69_closeout_count": 4,
            "due_status": "not_due(아직 아님)",
            "next_numeric_trigger_frontier": 70,
        },
        "next_frontier_proposal": {
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "direction": "regime_specific_asymmetric_value_exit_label_and_model_family_rotation(장세별 비대칭 가치/청산 라벨 및 모델 계열 회전)",
            "must_change": ["label_target(라벨/목표)", "model_family(모델 계열)"],
            "do_not_repeat": "F69 event-first ExtraTrees threshold/cooldown/daily quota repair loop(F69 이벤트 우선 엑스트라트리스 임계값/쿨다운/일별 할당 수리 반복)",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_table_lines(kpi_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    lines = [
        "| period(기간) | split/view(분할/보기) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD(손실폭) | trades(거래) | trades/day(일거래) | win rate(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | Tuw(회복 전 체류) | max consec loss(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in kpi_rows:
        lines.append(
            "| `{period}` | `{view}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{wr}` | `{aw}` | `{al}` | `{payoff}` | `{expect}` | `{recovery}` | `{tuw}` | `{mcl}` | `{ls}` | `{gap}` |".format(
                period=row["test_period"],
                view=row["split_view"],
                net=fmt(row["net_profit"]),
                gp=fmt(row["gross_profit"]),
                gl=fmt(row["gross_loss"]),
                pf=fmt(row["profit_factor"]),
                dd=percent_text(row["drawdown_percent"]),
                trades=fmt(row["trade_count"]),
                tpd=fmt(row["trades_per_day"]),
                wr=percent_text(row["win_rate"]),
                aw=fmt(row["average_win"]),
                al=fmt(row["average_loss"]),
                payoff=fmt(row["payoff_ratio"]),
                expect=fmt(row["expectancy"]),
                recovery=fmt(row["recovery_factor"]),
                tuw=row["time_under_water"],
                mcl=row["max_consecutive_loss"],
                ls=row["long_short_breakdown"],
                gap=row["proxy_runtime_gap"],
            )
        )
    return lines


def closeout_report_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Frontier69 Stage Closeout(F69 전선 단계 마감)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "## Closeout Label(마감 라벨)",
        "",
        f"`{summary['closeout_label']}`",
        "",
        "Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        "",
        "## Hypothesis(가설)",
        "",
        "Event-first first-hit opportunity model(이벤트 우선 선도달 기회 모델)이 F68 risk-only negative memory(F68 위험 단독 부정 기억) 뒤 새 PF source(수익 팩터 원천)를 만들 수 있는지 시험했다.",
        "",
        "## Result(결과)",
        "",
        "Action(행동): F69B/F69C proxy(프록시), F69D MT5 Runtime Probe(MT5 런타임 탐침), F69E proxy/runtime gap repair(프록시/런타임 간극 수리)를 마감 근거로 묶었다.",
        "",
        "Effect(효과): ONNX/RuntimeVetoTape/MT5 bridge(온엑스/런타임 차단 테이프/MT5 연결)는 보존 단서로 남기고, F69 event-first ExtraTrees trade-shape-only repair(이벤트 우선 엑스트라트리스 거래 형태 단독 수리)는 반복 금지 부정 기억으로 닫는다.",
        "",
        "## Closeout KPI(마감 핵심 성과 지표)",
        "",
        f"- test period(테스트 기간): `{summary['test_period']}`.",
        f"- strict joint pass count(엄격 공동 통과 수): `{summary['strict_joint_pass_count']}`.",
    ]
    lines.extend(kpi_table_lines(summary["closeout_kpi"]))
    lines.extend(
        [
            "",
            "## Preserved Clue(보존 단서)",
            "",
            "- ONNX/probability/signal/feature parity(온엑스/확률/신호/피처 동등성)는 정확했다.",
            "- RuntimeVetoTape bridge(런타임 차단 테이프 연결)는 event mask(이벤트 마스크) 관찰 도구로 유효했다.",
            "- Sparse event-first first-hit surface(희박 이벤트 우선 선도달 표면)는 PF clue(수익 팩터 단서)를 만들 수 있지만 너무 얇다.",
            "",
            "## Negative Memory(부정 기억)",
            "",
            "- F69 event-first ExtraTrees surface(이벤트 우선 엑스트라트리스 표면)는 threshold/cooldown/daily quota(임계값/쿨다운/일별 할당) 수리만으로 네 축을 동시에 맞추지 못했다.",
            "- Density lift(밀도 상승)는 PF collapse(PF 붕괴) 또는 DD breach(손실폭 훼손)를 만들었다.",
            "- 같은 event-first trade-shape-only loop(이벤트 우선 거래 형태 단독 반복)를 다음 frontier(전선)로 가져가지 않는다.",
            "",
            "## Grok Closeout Review(그록 마감 검토)",
            "",
            f"- packet(패킷): `{summary['grok']['packet']}`.",
            f"- prompt(프롬프트): `{summary['grok']['prompt']}`, sha256 `{summary['grok']['prompt_hash']}`.",
            f"- output(출력): `{summary['grok']['clean_output']}`, sha256 `{summary['grok']['clean_output_hash']}`.",
            "- accepted(수용): closeout label honest(마감 라벨 정직), no extra trade-shape-only MT5 repair mandatory(추가 거래 형태 단독 MT5 수리 필수 아님), next frontier pivot(다음 전선 전환).",
            "- needs_local_verification(로컬 검증 필요): HGB fallback scope(HGB 대체 범위).",
            "- local verification(로컬 검증): HGB는 F69D에서 guardrail-only(보호 장치 전용)였고, fixed ExtraTrees axes(고정 엑스트라트리스 축) 2개가 export/parity/MT5(내보내기/동등성/MT5)를 완료했으므로 closeout blocker(마감 차단)가 아니다.",
            "",
            "## Five-Stage Retrospective Check(5단계 중간 검토 점검)",
            "",
            "- F69 closeout(마감) 후 count(수): `4/5`.",
            "- due status(도래 상태): `not_due(아직 아님)`.",
            "- next numeric trigger(다음 숫자 트리거): F70 closeout(F70 마감).",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{summary['next_frontier_proposal']['run_id']}` under `{summary['next_frontier_proposal']['stage_id']}`.",
            "",
            "Direction(방향): regime-specific asymmetric value/exit label(장세별 비대칭 가치/청산 라벨) plus model family rotation(모델 계열 회전).",
        ]
    )
    return lines


def grok_receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    classification = summary["grok"]["classification"]
    return [
        "# F69 Closeout Grok Receipt(F69 마감 그록 영수증)",
        "",
        f"- created_at_utc(생성): `{utc_now()}`",
        "- trigger_reason(트리거 이유): stage closeout review(단계 마감 검토).",
        "- review_size(검토 크기): `medium(중간)`.",
        "- direction_before_grok(그록 전 방향): close F69 as preserved clue + negative memory no authority(F69를 보존 단서 + 부정 기억 권위 없음으로 마감).",
        f"- bounded_evidence(제한 근거): `{rel(GROK_PROMPT)}`.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{summary['grok']['prompt_hash']}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{summary['grok']['clean_output_hash']}`.",
        f"- accepted(수용): `{'; '.join(classification['accepted'])}`.",
        f"- rejected(거절): `{'; '.join(classification['rejected'])}`.",
        f"- needs_local_verification(로컬 검증 필요): `{'; '.join(classification['needs_local_verification'])}`.",
        f"- local_verification(로컬 검증): `{classification['local_verification']['HGB fallback scope(HGB 대체 범위)']}`.",
        f"- forbidden_claim_check(금지 주장 확인): `{classification['forbidden_claim_check']}`.",
        f"- final_codex_direction(최종 Codex 방향): close F69 and pivot next frontier(전선69 마감 및 다음 전선 전환).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# Required Gate Coverage Audit F69F(필수 게이트 커버리지 감사 F69F)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| hypothesis lifecycle(가설 생명주기) | passed(통과) | F69A..F69F reports(F69A..F69F 보고서) | 가설->프록시->MT5 탐침->간극 분석->수리->마감 연결 |",
        f"| mandatory MT5 runtime probe(필수 MT5 런타임 탐침) | passed(통과) | `{rel(F69D_RECEIPT)}` | F69에서 실제 Strategy Tester(전략 테스터) KPI를 남김 |",
        f"| proxy/runtime gap analysis(프록시/런타임 간극 분석) | passed(통과) | `{rel(F69E_REPORT)}` | bridge vs economics(연결 vs 경제성)를 분리 |",
        f"| repair attempt(수리 시도) | passed(통과) | `{rel(F69E_SWEEP)}` | threshold/cooldown/daily quota(임계값/쿨다운/일별 할당)를 650행 탐색 |",
        f"| Grok closeout review(그록 마감 검토) | passed(통과) | `{rel(GROK_RECEIPT)}` | 외부 2차 의견을 수용/검증/경계 처리 |",
        f"| closeout KPI(마감 KPI) | passed(통과) | `{rel(STAGE_CLOSEOUT_REPORT)}` | 기간, 순수익, PF, DD, 거래수, 기대값, 회복계수, 롱/숏, proxy/runtime gap 기록 |",
        "| five-stage retrospective due check(5단계 중간 검토 도래 점검) | passed_not_due(통과, 아직 아님) | `docs/registers/five_stage_retrospective_register.yaml` | F69 후 4/5, F70 마감 때 도래 |",
        f"| claim boundary(주장 경계) | passed(통과) | `{CLAIM_BOUNDARY}` | 금지 주장 없음 |",
        "",
        f"Summary(요약): closeout label(마감 라벨) `{summary['closeout_label']}`; next(다음) `{NEXT_RUN_ID}`.",
    ]


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    sparse = summary["runtime_snapshot"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(STAGE_CLOSEOUT_REPORT),
        "notes": "F69 closed after proxy, MT5 runtime probe, gap analysis, repair sweep, and Grok closeout review.",
        "family": "kpi_evidence(핵심 성과 지표 근거)",
        "primary_report": rel(STAGE_CLOSEOUT_REPORT),
        "run_number": "frontier69F",
        "date": "2026-06-17",
        "decision": "close_f69_and_prepare_f70_axis_pivot",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(STAGE_CLOSEOUT_REPORT),
        "run_date": "2026-06-17",
        "primary_artifact": rel(CLOSEOUT_SUMMARY),
        "net_profit": sparse.get("sparse_oos_net"),
        "profit_factor": sparse.get("sparse_oos_pf"),
        "drawdown": sparse.get("sparse_oos_dd"),
        "trade_count": 7,
        "result_status": STATUS,
        "attempt_count": 0,
        "view": "stage_closeout(단계 마감)",
        "tier": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope(티어 A 분리; 티어 B 필수 누락; 합산 범위 밖)",
        "metric_scope": "stage_closeout_runtime_probe_and_gap(단계 마감 런타임 탐침 및 간극)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "external_verification_status": "completed_mt5_runtime_probe_and_grok_closeout_review(완료된 MT5 런타임 탐침 및 그록 마감 검토)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(STAGE_CLOSEOUT_REPORT),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": utc_now(),
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": "stage_closeout(단계 마감)",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope",
        "kpi_scope": "runtime_probe_closeout_decision(런타임 탐침 마감 결정)",
        "primary_kpi": "sparse_oos_pf=2.94; sparse_oos_tpd=0.0359; dense_oos_pf=1.19; dense_oos_tpd=1.3385",
        "guardrail_kpi": "f69e_final_gate_like=0; f69e_joint_soft=0; no authority claims",
        "runtime_attempt_rows": 4,
        "work_family": "kpi_evidence(핵심 성과 지표 근거)",
        "row_id": f"{RUN_ID}__stage_closeout",
        "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서/부정 기억, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "What did F69 prove and what should be preserved?(F69가 무엇을 증명했고 무엇을 보존할지)",
        "artifact_count": 7,
        "created_at_utc": utc_now(),
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_stage_closeout(전선 단계 마감)",
        "run_type": "stage_closeout(단계 마감)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(CLOSEOUT_SUMMARY),
        "result_path": rel(STAGE_CLOSEOUT_REPORT),
        "selected_net_profit": "",
        "selected_profit_factor": "",
        "selected_trade_density": "",
        "goal_achieve": "not_claimed",
        "source_authority": "F69D MT5 runtime probe observation and F69E proxy repair sweep(F69D 런타임 탐침 관찰 및 F69E 프록시 수리 탐색)",
        "trade_density": sparse.get("sparse_oos_trades_day"),
        "expected_trade_density": "5-10 trades/day final target not met(최종 목표 일 5-10 미달)",
        "max_drawdown_percent": sparse.get("sparse_oos_dd"),
        "strict_joint_pass_count": 0,
    }


def update_registers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    append_once(
        IDEA_REGISTRY,
        "<!-- frontier69F_stage_closeout_event_first_axis_rotation_v1 -->",
        f"""
<!-- frontier69F_stage_closeout_event_first_axis_rotation_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` closes Frontier69(전선69) as `{JUDGMENT}`. Preserved clue(보존 단서): exact ONNX/signal/feature parity(정확한 온엑스/신호/피처 동등성) and RuntimeVetoTape observation tooling(런타임 차단 테이프 관찰 도구). Negative memory(부정 기억): event-first ExtraTrees trade-shape-only repair(이벤트 우선 엑스트라트리스 거래 형태 단독 수리)는 5-10 trades/day(일 5-10회), PF 2-3+(수익 팩터 2-3 이상), DD <10%(손실폭 10% 미만)를 동시에 만들지 못했다. Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
""",
    )
    append_once(
        NEGATIVE_RESULT_REGISTER,
        "<!-- NR-FR69-EVENT-FIRST-EXTRATREES-TRADE-SHAPE-REPAIR -->",
        f"""
<!-- NR-FR69-EVENT-FIRST-EXTRATREES-TRADE-SHAPE-REPAIR -->
## NR-FR69-EVENT-FIRST-EXTRATREES-TRADE-SHAPE-REPAIR

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): event-first first-hit opportunity model(이벤트 우선 선도달 기회 모델)이 F68 risk-only negative memory(F68 위험 단독 부정 기억) 뒤 새 PF source(수익 팩터 원천)를 만들 수 있다.
- Why failed(실패 이유): sparse PF clue(희박 PF 단서)는 trades/day(일거래)가 `0.0359` OOS 수준으로 너무 얇고, dense repair(밀도 수리)는 PF가 `1.19` OOS 또는 그 이하로 약했다. F69E 650-row repair sweep(F69E 650행 수리 탐색)에서 final_gate_like(최종 조건 유사) `0`, joint_soft(완화 공동 조건) `0`이었다.
- Salvage value(회수 가치): ONNX/probability/signal/feature parity(온엑스/확률/신호/피처 동등성)와 RuntimeVetoTape event mask bridge(런타임 차단 테이프 이벤트 마스크 연결)는 관찰 도구로 보존한다.
- Reopen condition(재개 조건): label/target(라벨/목표) and model family(모델 계열)를 함께 바꾸고, density objective(밀도 목표)를 post-hoc quota(사후 할당)가 아니라 label/selection(라벨/선택)에 내장할 때만 재개한다.
- Do-not-repeat(반복 금지): same F69 event-first ExtraTrees threshold/cooldown/daily quota repair loop(동일 F69 이벤트 우선 엑스트라트리스 임계값/쿨다운/일별 할당 수리 반복)를 반복하지 않는다.
- Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음).
""",
    )


def update_retrospective_register() -> None:
    lines = [
        "version: five_stage_retrospective_register_v1",
        "source_of_truth: docs/registers/five_stage_retrospective_register.yaml",
        'purpose: "Track five-stage Grok retrospective(5단계 Grok 중간 검토) cadence without relying on Codex memory(코덱스 기억)."',
        "adopted_at_utc: '2026-06-16T12:05:00Z'",
        "adopted_during_stage_id: stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "cadence:",
        '  primary_trigger: "closing_frontier_number % 5 == 0"',
        '  fallback_trigger: "len(closed_frontier_ids_since_last_retrospective) >= 5"',
        "  next_open_block: true",
        '  scope_rule: "Use latest five canonical frontier closeout stage ids with closeout receipts, not numeric NN-4..NN alone."',
        "required_outputs:",
        "  - five_stage_retrospective_packet",
        "  - bounded_evidence_table",
        "  - grok_receipt",
        "  - codex_local_verification",
        "  - advice_classification",
        "  - compact_retrospective_report",
        "  - next_stage_open_block_check",
        "required_row_fields:",
        "  - stage_id",
        "  - hypothesis",
        "  - proxy_kpi",
        "  - mt5_runtime_probe_kpi",
        "  - proxy_runtime_gap_cause",
        "  - closeout_label",
        "  - preserved_clue",
        "  - negative_memory",
        "  - systemic_repeat",
        "  - next_action",
        "claim_boundary:",
        "  allowed:",
        "    - direction_delta",
        "    - repair_priority_delta",
        "  forbidden:",
        "    - completion",
        "    - baseline",
        "    - promotion",
        "    - runtime_authority",
        "    - live_readiness",
        "    - goal_achieve",
        "",
        "state:",
        "  last_completed_packet_id: null",
        "  last_completed_at_frontier: null",
        "  last_completed_stage_ids: []",
        "  last_completed_at_utc: null",
        "  closed_frontier_ids_since_last_retrospective:",
        "    - stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "    - stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk",
        "    - stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout",
        f"    - {STAGE_ID}",
        "  closeouts_since_last: 4",
        "  next_numeric_trigger_frontier: 70",
        "  current_due_status: not_due",
        '  note: "F66, F67, F68, and F69 closeouts(마감)은 4/5로 계산했다. Next expected numeric trigger(다음 숫자 트리거)는 F70 closeout(마감)이다."',
    ]
    io_path(RETROSPECTIVE_REGISTER).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def write_state_files(summary: Mapping[str, Any]) -> None:
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_stage_id: {NEXT_STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f69_runtime_probe_completed_observation_recorded_no_authority(F69 런타임 탐침 완료/관찰 기록, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f69_closeout_4_of_5",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "F69F action(행동): F69 event-first axis rotation(이벤트 우선 축 회전)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감했다."',
        '  - "Effect(효과): exact bridge parity(정확한 연결 동등성)는 보존하고, same trade-shape-only repair loop(동일 거래 형태 단독 수리 반복)는 다음 전선으로 가져가지 않는다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}` with label/target and model-family pivot(라벨/목표 및 모델 계열 전환)."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")

    current_lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        f"Next stage(다음 단계): `{NEXT_STAGE_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): Frontier69 event-first axis rotation(전선69 이벤트 우선 축 회전)을 마감했다.",
        "",
        "Effect(효과): RuntimeVetoTape/ONNX bridge(런타임 차단 테이프/온엑스 연결)는 보존 단서로 남겼고, event-first ExtraTrees trade-shape-only repair(이벤트 우선 엑스트라트리스 거래 형태 단독 수리)는 부정 기억으로 닫았다.",
        "",
        f"- closeout label(마감 라벨): `{JUDGMENT}`.",
        f"- strict joint pass count(엄격 공동 통과 수): `{summary['strict_joint_pass_count']}`.",
        f"- F69E final gate-like rows(F69E 최종 조건 유사 행): `{summary['f69e_repair_sweep']['final_gate_like_count']}`.",
        f"- five-stage retrospective(5단계 중간 검토): `not_due(아직 아님)`, 4/5.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- stage closeout(단계 마감): `{rel(STAGE_CLOSEOUT_REPORT)}`",
        f"- Grok receipt(그록 영수증): `{rel(GROK_RECEIPT)}`",
        f"- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(CURRENT_WORKING_STATE, current_lines)

    selection_lines = [
        "# F69 Selection Status(F69 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- closeout_report(마감 보고서): `{rel(STAGE_CLOSEOUT_REPORT)}`",
        f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(SELECTION_STATUS, selection_lines)


def main() -> int:
    required = [F69D_RECEIPT, F69D_GAP, F69E_DECISION, GROK_PROMPT, GROK_CLEAN, GROK_METADATA]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing closeout evidence: {missing}")
    runtime_rows = read_csv_rows(F69D_RECEIPT)
    f69e_decision = read_json(F69E_DECISION)
    summary = build_summary(runtime_rows, f69e_decision)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
        "inputs": {
            "runtime_receipt": rel(F69D_RECEIPT),
            "runtime_gap": rel(F69D_GAP),
            "f69e_decision": rel(F69E_DECISION),
            "grok_prompt": rel(GROK_PROMPT),
            "grok_clean": rel(GROK_CLEAN),
        },
        "outputs": {
            "summary": rel(CLOSEOUT_SUMMARY),
            "stage_closeout_report": rel(STAGE_CLOSEOUT_REPORT),
            "grok_receipt": rel(GROK_RECEIPT),
            "gate_audit": rel(GATE_AUDIT),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(CLOSEOUT_SUMMARY, summary)
    write_md(STAGE_CLOSEOUT_REPORT, closeout_report_lines(summary))
    write_md(GROK_RECEIPT, grok_receipt_lines(summary))
    write_md(GATE_AUDIT, gate_audit_lines(summary))
    update_registers(summary)
    update_retrospective_register()
    write_state_files(summary)
    print(json.dumps(json_ready({"status": STATUS, "judgment": JUDGMENT, "next_run_id": NEXT_RUN_ID, "retrospective_due": "not_due_4_of_5"}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
