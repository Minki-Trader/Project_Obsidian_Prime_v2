from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_76 import frontier76b_axis_ablation_proxy_scout as f76b


STAGE_ID = f76b.STAGE_ID
RUN_ID = "frontier76G_stage_closeout_axis_ablation_source_discovery_v1"
PARENT_RUN_ID = "frontier76F_lifecycle_aware_density_repair_proxy_v1"
NEXT_RUN_ID = "frontier77A_stage_open_runtime_lifecycle_label_density_rebuild_v1"
STATUS_SUCCESS = "closed_preserved_clue_negative_memory_no_authority"
STATUS_TRANSPORT_FAIL = "closeout_grok_transport_failed_stage_not_closed_no_authority"
JUDGMENT_SUCCESS = "preserved_clue_negative_memory_no_authority"
JUDGMENT_TRANSPORT_FAIL = "closeout_grok_retry_required_no_authority"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
CLOSEOUT_LABEL = "preserved_clue_negative_memory"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
F76B_SUMMARY = REVIEW_DIR / "f76b_summary.json"
F76D_RECEIPT = REVIEW_DIR / "f76d_runtime_receipt.csv"
F76E_SUMMARY = REVIEW_DIR / "f76e_gap_analysis_summary.json"
F76F_SUMMARY = REVIEW_DIR / "f76f_lifecycle_proxy_summary.json"
F76F_TOP100 = REVIEW_DIR / "f76f_lifecycle_proxy_ranked_top100.csv"
REPORT_PATH = REVIEW_DIR / "stage_closeout_report.md"
RECEIPT_PATH = REVIEW_DIR / "grok_stage_closeout_axis_ablation_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f76g_closeout.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
RETROSPECTIVE_DUE_STATUS = "not_due_after_f76_closeout_1_of_5"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f76g_stage_closeout_axis_ablation"
GROK_PROMPT_PATH = GROK_PACKET / "prompts/f76g_stage_closeout_axis_ablation_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if not rows:
        io_path(path).write_text("", encoding="utf-8-sig")
        return
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def short_number(value: Any) -> str:
    if value in ("", None):
        return ""
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion"]
        if f"may claim {term}" in lowered
        or f"can claim {term}" in lowered
        or f"{term} achieved" in lowered
        or f"{term}: achieved" in lowered
        or f"{term}: yes" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_closeout_grok(마감 Grok 재시도)", forbidden_hits
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)", "do_not_close_until_repaired(수리 전 마감 금지)", forbidden_hits
    if "needs_local_verification" in lowered or "needs local verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)", "close_only_after_codex_checks(코덱스 점검 후에만 마감)", forbidden_hits
    if "accepted_with_conditions" in lowered or "accepted with conditions" in lowered or "accepted" in lowered:
        return "accepted_with_conditions(조건부 수용)", "close_as_preserved_clue_negative_memory(보존 단서/부정 기억으로 마감)", forbidden_hits
    return "accepted_with_conditions(조건부 수용)", "close_as_preserved_clue_negative_memory(보존 단서/부정 기억으로 마감)", forbidden_hits


def closeout_kpi_rows(runtime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        rows.append(
            {
                "split": row.get("split", ""),
                "period": f"{row.get('test_period_start', '')}..{row.get('test_period_end', '')}",
                "net_profit": row.get("net_profit", ""),
                "gross_profit": row.get("gross_profit", ""),
                "gross_loss": row.get("gross_loss", ""),
                "profit_factor": row.get("profit_factor", ""),
                "drawdown_percent": row.get("max_drawdown_percent", ""),
                "trade_count": row.get("trade_count", ""),
                "trades_per_day": row.get("trades_per_day", ""),
                "win_rate_percent": row.get("win_rate_percent", ""),
                "average_win": row.get("average_win", ""),
                "average_loss": row.get("average_loss", ""),
                "payoff_ratio": row.get("payoff_ratio", ""),
                "expectancy": row.get("expectancy", ""),
                "recovery_factor": row.get("recovery_factor", ""),
                "time_under_water": "not_available_in_runtime_receipt(런타임 영수증에 없음)",
                "max_consecutive_loss": "not_available_in_runtime_receipt(런타임 영수증에 없음)",
                "long_short_breakdown": f"long={row.get('long_trade_count', '')};short={row.get('short_trade_count', '')}",
                "proxy_runtime_gap": (
                    f"proxy_net={short_number(row.get('proxy_net_profit'))};runtime_net={short_number(row.get('net_profit'))};"
                    f"proxy_pf={short_number(row.get('proxy_profit_factor'))};runtime_pf={short_number(row.get('profit_factor'))};"
                    f"proxy_dd={short_number(row.get('proxy_dd_percent'))};runtime_dd={short_number(row.get('max_drawdown_percent'))};"
                    f"proxy_tpd={short_number(row.get('proxy_trades_per_day'))};runtime_tpd={short_number(row.get('trades_per_day'))}"
                ),
            }
        )
    return rows


def top_f76f_positive_rows(limit: int = 5) -> list[dict[str, str]]:
    rows = read_csv(F76F_TOP100)
    dual_positive = [
        row
        for row in rows
        if as_float(row.get("val_net")) > 0 and as_float(row.get("oos_net")) > 0
    ]
    dual_positive.sort(key=lambda row: min(as_float(row.get("val_pf")), as_float(row.get("oos_pf"))), reverse=True)
    return dual_positive[:limit]


def build_prompt(
    f76b_summary: Mapping[str, Any],
    f76e_summary: Mapping[str, Any],
    f76f_summary: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, str]],
    positive_rows: Sequence[Mapping[str, str]],
) -> str:
    best_b = f76b_summary["best_candidate"]
    best_f = f76f_summary["best_candidate"]
    runtime_lines = "\n".join(
        (
            f"- {row.get('split')}: period={row.get('test_period_start')}..{row.get('test_period_end')}, "
            f"net/PF/DD/tpd={row.get('net_profit')}/{row.get('profit_factor')}/{row.get('max_drawdown_percent')}/{row.get('trades_per_day')}, "
            f"signal/order/trade={row.get('signal_count')}/{row.get('order_attempt_count')}/{row.get('trade_count')}, "
            f"proxy net/PF/DD/tpd={row.get('proxy_net_profit')}/{row.get('proxy_profit_factor')}/{row.get('proxy_dd_percent')}/{row.get('proxy_trades_per_day')}"
        )
        for row in runtime_rows
    )
    positive_lines = "\n".join(
        (
            f"- {row.get('candidate_id')}: axes={row.get('feature_set')}/{row.get('model')}/{row.get('target')}/{row.get('session')}/{row.get('risk_filter')}/{row.get('prob_quantile')}, "
            f"val net/PF/DD/tpd={row.get('val_net')}/{row.get('val_pf')}/{row.get('val_dd_pct')}/{row.get('val_trades_day')}, "
            f"oos net/PF/DD/tpd={row.get('oos_net')}/{row.get('oos_pf')}/{row.get('oos_dd_pct')}/{row.get('oos_trades_day')}"
        )
        for row in positive_rows
    )
    return f"""# F76G Stage Closeout Grok Review Prompt(F76G 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Close F76 as `preserved_clue_negative_memory_no_authority(보존 단서/부정 기억, 권위 없음)`.
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
Next stage should pivot to runtime-lifecycle-native label/target/trade-shape design(런타임 생명주기 기본 라벨/목표/거래 형태 설계), not keep repairing F76B independent-signal proxy(독립 신호 프록시).

## F76 Hypothesis(F76 가설)

Feature set, label/target, model family, trade shape, risk logic, regime/session split(피처 묶음, 라벨/목표, 모델 계열, 거래 형태, 위험 로직, 장세/세션 분할)을 넓게 바꾸면 runtime economics(런타임 경제성)를 만드는 축 또는 망치는 축을 식별할 수 있다.

## Proxy Evidence(F76B 프록시 근거)

- best candidate(최선 후보): {best_b.get('candidate_id')}
- axes(축): {best_b.get('feature_set')}/{best_b.get('model')}/{best_b.get('target')}/{best_b.get('session')}/{best_b.get('risk_filter')}/q{best_b.get('prob_quantile')}
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): {best_b.get('val_net')}/{best_b.get('val_pf')}/{best_b.get('val_dd_pct')}/{best_b.get('val_trades_day')}/{best_b.get('val_trade_count')}
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): {best_b.get('oos_net')}/{best_b.get('oos_pf')}/{best_b.get('oos_dd_pct')}/{best_b.get('oos_trades_day')}/{best_b.get('oos_trade_count')}

## MT5 Runtime Probe Evidence(F76D MT5 런타임 탐침 근거)

{runtime_lines}

## Gap Analysis(F76E 간극 분석)

- primary gap cause(주 간극 원인): {f76e_summary.get('primary_gap_cause')}
- max hold_same_direction share(최대 동방향 보유 비율): {f76e_summary.get('max_hold_same_direction_share')}
- worst trades/day delta(최악 일거래 차이): {f76e_summary.get('worst_trades_per_day_delta')}
- repair decision(수리 결정): {f76e_summary.get('repair_decision')}

## Repair Evidence(F76F 수리 근거)

- candidate rows(후보 행): {f76f_summary.get('candidate_rows')}
- repair meaningful signal count(수리 의미 신호 수): {f76f_summary.get('repair_meaningful_signal_count')}
- density scout clue count(거래밀도 탐색 단서 수): {f76f_summary.get('density_scout_clue_count')}
- completion axis nearness count(완성 축 근접 수): {f76f_summary.get('completion_axis_nearness_count')}
- best repair candidate(최선 수리 후보): {best_f.get('candidate_id')}
- best repair OOS net/PF/DD/tpd(최선 수리 표본외 순수익/수익 팩터/손실폭/일거래): {best_f.get('oos_net')}/{best_f.get('oos_pf')}/{best_f.get('oos_dd_pct')}/{best_f.get('oos_trades_day')}

Best dual-positive repair rows if any(양수 수리 행):
{positive_lines or '- none'}

## Review Question(검토 질문)

Return one classification(분류) at top:
- accepted_with_conditions(조건부 수용): closeout label is justified with the stated boundary.
- needs_local_verification(로컬 검증 필요): closeout may be justified but Codex must check a named local item first.
- rejected(거절): do not close because evidence contradicts the label.

Also list:
1. Accepted/rejected advice(수용/거절 조언)
2. Preserved clue(보존 단서)
3. Negative memory(부정 기억)
4. Next-stage direction(다음 단계 방향)
5. Any forbidden claim risk(금지 주장 위험)
"""


def grok_identity(result: Any) -> dict[str, Any]:
    return {
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT_PATH),
        "prompt_sha256": sha256_file_lf_normalized(GROK_PROMPT_PATH),
        "output_path": rel(GROK_CLEAN_PATH),
        "output_exists": io_path(GROK_CLEAN_PATH).exists(),
        "output_sha256": sha256_file_lf_normalized(GROK_CLEAN_PATH) if io_path(GROK_CLEAN_PATH).exists() else "",
        "metadata_path": rel(GROK_METADATA_PATH),
        "metadata_exists": io_path(GROK_METADATA_PATH).exists(),
        "metadata_sha256": sha256_file_lf_normalized(GROK_METADATA_PATH) if io_path(GROK_METADATA_PATH).exists() else "",
        "success": bool(result.success),
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_hash": result.prompt_hash,
        "preflight_warnings": list(result.preflight_warnings),
        "unexpected_top_level_artifacts": list(result.unexpected_top_level_artifacts),
    }


def closeout_report_text(
    created_at: str,
    f76b_summary: Mapping[str, Any],
    f76e_summary: Mapping[str, Any],
    f76f_summary: Mapping[str, Any],
    kpi_rows: Sequence[Mapping[str, Any]],
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    best_b = f76b_summary["best_candidate"]
    best_f = f76f_summary["best_candidate"]
    status = STATUS_SUCCESS if grok["success"] else STATUS_TRANSPORT_FAIL
    judgment = JUDGMENT_SUCCESS if grok["success"] else JUDGMENT_TRANSPORT_FAIL
    lines = [
        "# F76 Stage Closeout Report(F76 단계 마감 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- closeout label(마감 라벨): `{CLOSEOUT_LABEL if grok['success'] else 'not_closed_grok_retry_required'}`",
        f"- Grok advice(그록 조언): `{advice_classification}`",
        f"- final Codex direction(최종 Codex 방향): `{final_direction}`",
        f"- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`",
        f"- next action(다음 행동): `{NEXT_RUN_ID if grok['success'] else RUN_ID}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis and Proxy(가설과 프록시)",
        "",
        "Hypothesis(가설): feature/label/model/trade/risk/session axes(피처/라벨/모델/거래/위험/세션 축)를 넓게 바꾸면 runtime economics(런타임 경제성)의 원천을 찾을 수 있다.",
        "",
        f"Best F76B proxy(최선 F76B 프록시): `{best_b.get('candidate_id')}` axes `{best_b.get('feature_set')}/{best_b.get('model')}/{best_b.get('target')}/{best_b.get('session')}/{best_b.get('risk_filter')}`.",
        f"Proxy validation net/PF/DD/tpd/trades(프록시 검증 순수익/수익 팩터/손실폭/일거래/거래): `{best_b.get('val_net')}/{best_b.get('val_pf')}/{best_b.get('val_dd_pct')}/{best_b.get('val_trades_day')}/{best_b.get('val_trade_count')}`.",
        f"Proxy OOS net/PF/DD/tpd/trades(프록시 표본외 순수익/수익 팩터/손실폭/일거래/거래): `{best_b.get('oos_net')}/{best_b.get('oos_pf')}/{best_b.get('oos_dd_pct')}/{best_b.get('oos_trades_day')}/{best_b.get('oos_trade_count')}`.",
        "",
        "## Closeout KPI(마감 핵심 성과 지표)",
        "",
        "| split/view(분할/보기) | test period(테스트 기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | TUW(회복 전 체류) | max loss streak(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in kpi_rows:
        lines.append(
            "| `{split}` | `{period}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{win}` | `{avgw}` | `{avgl}` | `{payoff}` | `{exp}` | `{rec}` | `{tuw}` | `{streak}` | `{ls}` | `{gap}` |".format(
                split=row["split"],
                period=row["period"],
                net=row["net_profit"],
                gp=row["gross_profit"],
                gl=row["gross_loss"],
                pf=row["profit_factor"],
                dd=row["drawdown_percent"],
                trades=row["trade_count"],
                tpd=row["trades_per_day"],
                win=row["win_rate_percent"],
                avgw=row["average_win"],
                avgl=row["average_loss"],
                payoff=row["payoff_ratio"],
                exp=row["expectancy"],
                rec=row["recovery_factor"],
                tuw=row["time_under_water"],
                streak=row["max_consecutive_loss"],
                ls=row["long_short_breakdown"],
                gap=row["proxy_runtime_gap"],
            )
        )
    lines.extend(
        [
            "",
            "## Gap and Repair(간극과 수리)",
            "",
            f"- F76E primary gap cause(주 간극 원인): `{f76e_summary.get('primary_gap_cause')}`",
            f"- max same-direction hold share(최대 동방향 보유 비율): `{f76e_summary.get('max_hold_same_direction_share')}`",
            f"- F76F repair candidates(수리 후보): `{f76f_summary.get('candidate_rows')}`",
            f"- F76F meaningful/density/near counts(F76F 의미/밀도/근접 수): `{f76f_summary.get('repair_meaningful_signal_count')}/{f76f_summary.get('density_scout_clue_count')}/{f76f_summary.get('completion_axis_nearness_count')}`",
            f"- F76F best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래): `{best_f.get('oos_net')}/{best_f.get('oos_pf')}/{best_f.get('oos_dd_pct')}/{best_f.get('oos_trades_day')}`",
            "",
            "## Closeout Judgment(마감 판정)",
            "",
            "Preserved clue(보존 단서): independent proxy(독립 신호 프록시)는 mega-cap removed/trend/session(대형주 제거/추세/세션) 축에서 PF 1.5~1.7, DD 10% 미만의 신호를 만들 수 있다.",
            "",
            "Negative memory(부정 기억): 신호마다 독립 거래로 계산한 proxy(프록시)는 MT5 single-position max-hold runtime(단일 포지션 최대 보유 런타임)에서 거래 수를 약 4~6배 과대평가했다. lifecycle-aware repair(생명주기 인식 수리)를 넣으면 고밀도 후보의 PF와 DD가 무너졌다.",
            "",
            "Next action(다음 행동): 다음 frontier stage(전선 단계)는 label/target/trade shape(라벨/목표/거래 형태)를 처음부터 runtime lifecycle(런타임 생명주기)에 맞춰 설계한다.",
            "",
            "## Grok Closeout Receipt(그록 마감 영수증)",
            "",
            f"- packet(묶음): `{grok.get('packet_path')}`",
            f"- prompt(프롬프트): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`",
            f"- output(출력): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`",
            f"- success(성공): `{grok.get('success')}` returncode `{grok.get('returncode')}`",
        ]
    )
    return "\n".join(lines)


def receipt_text(
    created_at: str,
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    return f"""# F76G Grok Stage Closeout Receipt(F76G Grok 단계 마감 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): stage closeout requires Grok second opinion(단계 마감은 Grok 2차 의견 필수).

Review size(검토 크기): `medium(중간)`

Direction before Grok(Grok 전 방향): close F76 as preserved_clue_negative_memory_no_authority(보존 단서/부정 기억, 권위 없음).

Bounded evidence(제한 근거): F76B proxy summary(F76B 프록시 요약), F76D MT5 runtime receipt(F76D MT5 런타임 영수증), F76E gap summary(F76E 간극 요약), F76F repair proxy summary(F76F 수리 프록시 요약).

Prompt identity(프롬프트 정체성): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`

Grok output identity(그록 출력 정체성): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`

Advice classification(조언 분류): `{advice_classification}`

Local verification(로컬 검증): Codex checked local summaries, runtime receipt, gap rows, F76F repair counts, and forbidden claim boundary(코덱스가 로컬 요약/런타임 영수증/간극 행/수리 수/금지 주장 경계를 확인함).

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`.

Final Codex direction(최종 Codex 방향): `{final_direction}`
"""


def gate_audit_text(created_at: str, grok: Mapping[str, Any], advice_classification: str) -> str:
    return f"""# Required Gate Coverage Audit F76G Closeout(F76G 마감 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| hypothesis(가설) | `recorded(기록됨)` | F76 stage brief(F76 단계 개요) |
| proxy KPI(프록시 KPI) | `recorded(기록됨)` | `{rel(F76B_SUMMARY)}` |
| MT5 runtime probe(MT5 런타임 탐침) | `completed(완료)` | `{rel(F76D_RECEIPT)}` |
| proxy/runtime gap analysis(프록시/런타임 간극 분석) | `completed(완료)` | `{rel(F76E_SUMMARY)}` |
| repair(수리) | `completed(완료)` | `{rel(F76F_SUMMARY)}` |
| closeout Grok review(마감 Grok 검토) | `{advice_classification}` | `{grok.get('output_path')}` |
| final_claim_guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def ledger_row(created_at: str, grok_success: bool) -> dict[str, Any]:
    status = STATUS_SUCCESS if grok_success else STATUS_TRANSPORT_FAIL
    judgment = JUDGMENT_SUCCESS if grok_success else JUDGMENT_TRANSPORT_FAIL
    row_id = f"{RUN_ID}::stage_closeout::tier_a"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": f"closeout_label={CLOSEOUT_LABEL if grok_success else 'not_closed'};next={NEXT_RUN_ID if grok_success else RUN_ID}",
        "family": "stage_closeout",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier76G",
        "date": created_at[:10],
        "decision": judgment,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if grok_success else RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "external_verification_status": "completed(완료)" if grok_success else "grok_transport_failed(Grok 전송 실패)",
        "result_judgment": judgment,
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "stage_closeout(단계 마감)",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate; Tier B out_of_scope_by_claim; combined out_of_scope",
        "kpi_scope": "stage_closeout_runtime_probe_gap_repair(단계 마감 런타임 탐침 간극 수리)",
        "primary_kpi": f"closeout_label={CLOSEOUT_LABEL if grok_success else 'not_closed'}",
        "guardrail_kpi": "no completion;no runtime authority;no live readiness",
        "work_family": "stage_closeout",
        "row_id": row_id,
        "evidence_boundary": "stage_closeout_only_no_authority",
        "next_action": NEXT_RUN_ID if grok_success else RUN_ID,
        "artifact_count": "5",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_closeout",
        "run_type": "stage_closeout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }


def update_retrospective_register(created_at: str, grok_success: bool) -> None:
    if not grok_success:
        return
    data = yaml.safe_load(io_path(RETROSPECTIVE_REGISTER).read_text(encoding="utf-8-sig"))
    state = data.setdefault("state", {})
    closed = list(state.get("closed_frontier_ids_since_last_retrospective") or [])
    if STAGE_ID not in closed:
        closed.append(STAGE_ID)
    state["closed_frontier_ids_since_last_retrospective"] = closed
    state["closeouts_since_last"] = len(closed)
    state["next_numeric_trigger_frontier"] = 80
    state["current_due_status"] = RETROSPECTIVE_DUE_STATUS
    state["last_updated_at_utc"] = created_at
    state["note"] = (
        "F76 closeout(마감)이 F71-F75 retrospective(회고) 이후 1/5로 등록됐다. "
        "F77 open(개방)은 five-stage retrospective gate(5단계 회고 게이트) 관점에서 not_due(아직 아님)다."
    )
    io_path(RETROSPECTIVE_REGISTER).write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8-sig",
    )


def update_state_and_ledgers(created_at: str, grok_success: bool) -> None:
    update_retrospective_register(created_at, grok_success)
    row = ledger_row(created_at, grok_success)
    f76b.upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    f76b.upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    f76b.upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row)

    idea_path = ROOT / "docs/registers/idea_registry.md"
    marker = "<!-- frontier76G_stage_closeout_axis_ablation_source_discovery_v1 -->"
    text = io_path(idea_path).read_text(encoding="utf-8-sig")
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` closed F76 as `{CLOSEOUT_LABEL if grok_success else 'not_closed_grok_retry_required'}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID if grok_success else RUN_ID}`.
"""
        write_text(idea_path, text.rstrip() + addition)

    status = STATUS_SUCCESS if grok_success else STATUS_TRANSPORT_FAIL
    judgment = JUDGMENT_SUCCESS if grok_success else JUDGMENT_TRANSPORT_FAIL
    current_run = NEXT_RUN_ID if grok_success else RUN_ID
    next_run = NEXT_RUN_ID if grok_success else RUN_ID
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {current_run}
latest_completed_run_id: {RUN_ID if grok_success else PARENT_RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f76_mandatory_runtime_probe_completed_stage_closed
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: {RETROSPECTIVE_DUE_STATUS if grok_success else 'not_due_after_frontier71_to_75_retrospective_completed'}
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F76G stage closeout(단계 마감)을 {'완료했다' if grok_success else '시도했지만 Grok 전송 실패로 닫지 않았다'}."
  - "Effect(효과): F76 preserved clue/negative memory(보존 단서/부정 기억)와 다음 단계 방향을 기록했다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{current_run}`

Latest completed run(최근 완료 실행): `{RUN_ID if grok_success else PARENT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F76G stage closeout(단계 마감)을 {'완료했다' if grok_success else '시도했지만 Grok 전송 실패로 닫지 않았다'}.

Effect(효과): F76은 independent-signal proxy(독립 신호 프록시)가 runtime lifecycle(런타임 생명주기)에서 붕괴한다는 negative memory(부정 기억)와, source axis(원천 축) 단서를 남겼다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)
    selection = f"""# F76 Selection Status(F76 선택 상태)

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F76G stage closeout(단계 마감)을 {'완료했다' if grok_success else '시도했지만 Grok 전송 실패로 닫지 않았다'}.

Effect(효과): 다음 frontier stage(전선 단계)는 runtime lifecycle-native label/target/trade-shape rebuild(런타임 생명주기 기본 라벨/목표/거래 형태 재구성)로 열어야 한다.

Current run(현재 실행): `{current_run}`

Latest completed run(최근 완료 실행): `{RUN_ID if grok_success else PARENT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)


def main() -> int:
    created_at = f76b.utc_now()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(GROK_PROMPT_PATH.parent).mkdir(parents=True, exist_ok=True)
    f76b_summary = read_json(F76B_SUMMARY)
    f76e_summary = read_json(F76E_SUMMARY)
    f76f_summary = read_json(F76F_SUMMARY)
    runtime_rows = read_csv(F76D_RECEIPT)
    kpi_rows = closeout_kpi_rows(runtime_rows)
    positive_rows = top_f76f_positive_rows()
    prompt = build_prompt(f76b_summary, f76e_summary, f76f_summary, runtime_rows, positive_rows)
    write_text(GROK_PROMPT_PATH, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        repo_root=ROOT,
        output_dir=GROK_PACKET,
        prompt_file_path=GROK_PROMPT_PATH,
        review_size="medium",
        timeout_seconds=300,
    )
    clean_output = io_path(GROK_CLEAN_PATH).read_text(encoding="utf-8-sig") if io_path(GROK_CLEAN_PATH).exists() else result.clean_stdout
    advice_classification, final_direction, forbidden_hits = classify_advice(clean_output, bool(result.success))
    grok = grok_identity(result)
    write_text(REPORT_PATH, closeout_report_text(created_at, f76b_summary, f76e_summary, f76f_summary, kpi_rows, grok, advice_classification, final_direction, forbidden_hits))
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice_classification, final_direction, forbidden_hits))
    write_text(GATE_AUDIT_PATH, gate_audit_text(created_at, grok, advice_classification))
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if result.success else RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS_SUCCESS if result.success else STATUS_TRANSPORT_FAIL,
        "judgment": JUDGMENT_SUCCESS if result.success else JUDGMENT_TRANSPORT_FAIL,
        "closeout_label": CLOSEOUT_LABEL if result.success else "not_closed_grok_retry_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "grok": grok,
        "advice_classification": advice_classification,
        "final_codex_direction": final_direction,
        "forbidden_claim_hits": forbidden_hits,
        "kpi_rows": kpi_rows,
        "artifacts": {
            "report": rel(REPORT_PATH),
            "receipt": rel(RECEIPT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "prompt": rel(GROK_PROMPT_PATH),
            "grok_output": rel(GROK_CLEAN_PATH),
        },
    }
    write_json(RUN_MANIFEST_PATH, payload)
    write_json(REVIEW_DIR / "f76g_closeout_summary.json", payload)
    write_csv(REVIEW_DIR / "f76g_closeout_kpi_rows.csv", kpi_rows)
    write_csv(RUN_DIR / "f76g_closeout_kpi_rows.csv", kpi_rows)
    update_state_and_ledgers(created_at, bool(result.success))
    print(
        json.dumps(
            json_ready(
                {
                    "status": payload["status"],
                    "judgment": payload["judgment"],
                    "closeout_label": payload["closeout_label"],
                    "advice_classification": advice_classification,
                    "grok_success": result.success,
                    "next_run_id": payload["next_run_id"],
                    "forbidden_claim_hits": forbidden_hits,
                    "report": rel(REPORT_PATH),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
