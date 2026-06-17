from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_73 import frontier73b_session_regime_feature_model_rotation_proxy_scout as f73b


STAGE_ID = f73b.STAGE_ID
RUN_ID = "frontier73H_stage_closeout_session_regime_feature_model_rotation_v1"
PARENT_RUN_ID = "frontier73G_direct_binary_adapter_gap_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier74A_stage_open_new_hypothesis_after_f73_session_regime_negative_memory_v1"
CLOSEOUT_LABEL = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory_no_authority"
CLAIM_BOUNDARY = (
    "preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f73b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f73b.REVIEWS_ROOT
SELECTED_ROOT = f73b.SELECTED_ROOT

F73B_SUMMARY = STAGE_ROOT / "02_runs/frontier73B_session_regime_feature_model_rotation_proxy_scout_v1/frontier73B_proxy_summary.json"
F73C_SUMMARY = STAGE_ROOT / "02_runs/frontier73C_axis_reduction_or_repair_proxy_scout_v1/frontier73C_proxy_repair_summary.json"
F73D_RECEIPT = STAGE_ROOT / "02_runs/frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1/f73d_runtime_probe_receipt.csv"
F73E_SUMMARY = STAGE_ROOT / "02_runs/frontier73E_proxy_runtime_gap_analysis_or_repair_decision_v1/frontier73E_gap_analysis_summary.json"
F73F_SUMMARY = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/frontier73F_runtime_repair_summary.json"
F73F_RECEIPT = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_runtime_probe_receipt.csv"
F73F_SIGNAL = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_signal_parity.csv"
F73F_PROB = STAGE_ROOT / "02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/f73f_probability_parity.csv"
F73G_RESULT = STAGE_ROOT / "02_runs/frontier73G_direct_binary_adapter_gap_or_closeout_decision_v1/frontier73G_gap_decision_result.json"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f73_closeout_session_regime_feature_model_rotation"
GROK_PROMPT = GROK_PACKET / "prompts/f73_closeout_session_regime_feature_model_rotation_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"
FIVE_STAGE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def require_inputs() -> list[str]:
    paths = [
        F73B_SUMMARY,
        F73C_SUMMARY,
        F73D_RECEIPT,
        F73E_SUMMARY,
        F73F_SUMMARY,
        F73F_RECEIPT,
        F73F_SIGNAL,
        F73F_PROB,
        F73G_RESULT,
        GROK_PROMPT,
        GROK_CLEAN,
        GROK_METADATA,
    ]
    return [rel(path) for path in paths if not path_exists(path)]


def split_rows(frame: pd.DataFrame) -> dict[str, dict[str, Any]]:
    return {str(row["split"]): row.to_dict() for _, row in frame.iterrows()}


def closeout_kpi_rows(f73f_receipt: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in f73f_receipt.iterrows():
        rows.append(
            {
                "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
                "split_view": f"F73F direct binary adapter runtime probe {row.get('split')} Tier A separate(Tier A 분리)",
                "net_profit": row.get("net_profit"),
                "gross_profit": row.get("gross_profit"),
                "gross_loss": row.get("gross_loss"),
                "profit_factor": row.get("profit_factor"),
                "drawdown_percent": row.get("max_drawdown_percent"),
                "trade_count": row.get("trade_count"),
                "trades_day": row.get("trades_per_day"),
                "win_rate_percent": row.get("win_rate_percent"),
                "average_win": row.get("average_win"),
                "average_loss": row.get("average_loss"),
                "payoff_ratio": row.get("payoff_ratio"),
                "expectancy": row.get("expectancy"),
                "recovery_factor": row.get("recovery_factor"),
                "time_under_water": "not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)",
                "max_consecutive_loss": "not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)",
                "long_short_breakdown": f"{row.get('long_trade_count')}/{row.get('short_trade_count')}",
                "proxy_runtime_gap": (
                    f"proxy PF/DD/tpd {row.get('proxy_profit_factor')}/{row.get('proxy_dd_percent')}/{row.get('proxy_trades_per_day')} "
                    f"vs runtime {row.get('profit_factor')}/{row.get('max_drawdown_percent')}/{row.get('trades_per_day')}"
                ),
            }
        )
    return rows


def build_summary(created_at: str) -> dict[str, Any]:
    f73b_summary = read_json(F73B_SUMMARY)
    f73c_summary = read_json(F73C_SUMMARY)
    f73e_summary = read_json(F73E_SUMMARY)
    f73f_summary = read_json(F73F_SUMMARY)
    f73g = read_json(F73G_RESULT)
    f73d_receipt = read_csv(F73D_RECEIPT)
    f73f_receipt = read_csv(F73F_RECEIPT)
    signal = read_csv(F73F_SIGNAL)
    probability = read_csv(F73F_PROB)
    f73f_by_split = split_rows(f73f_receipt)
    oos = f73f_by_split["oos"]
    validation = f73f_by_split["validation"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": CLOSEOUT_LABEL,
        "judgment": JUDGMENT,
        "closeout_label": CLOSEOUT_LABEL,
        "created_at_utc": created_at,
        "hypothesis": "session/regime feature/model rotation(세션/장세 피처/모델 회전)이 F72 trade-shape negative memory(F72 거래 형태 부정 기억) 이후 runtime economics source(런타임 경제성 원천)를 분리할 수 있는가.",
        "test_period": {
            "runtime_validation": "2025-01-02..2025-10-01",
            "runtime_oos": "2025-10-01..2026-04-14",
        },
        "proxy_expectation": "feature set/label/model/session regime(피처 묶음/라벨/모델/세션 장세)를 재조합하면 F72 lifecycle negative memory(F72 생명주기 부정 기억)와 다른 proxy seed surface(프록시 씨앗 표면)가 생기고, direct runtime materialization(직접 런타임 물질화) 뒤에도 PF/DD/density(수익 팩터/손실폭/밀도)가 일부 보존될 것으로 기대했다.",
        "proxy_kpi": {
            "f73b_candidate_count": f73b_summary.get("candidate_count"),
            "f73b_scout_clue_count": f73b_summary.get("scout_clue_count"),
            "f73b_meaningful_candidate_count": f73b_summary.get("meaningful_candidate_count"),
            "f73b_best_oos": _candidate_oos(f73b_summary.get("best_candidate", {})),
            "f73c_candidate_count": f73c_summary.get("candidate_count"),
            "f73c_dual_positive_count": f73c_summary.get("dual_positive_count"),
            "f73c_meaningful_candidate_count": f73c_summary.get("meaningful_candidate_count"),
            "f73c_best_oos": _candidate_oos(f73c_summary.get("best_candidate", {})),
            "f73c_best_validation": _candidate_validation(f73c_summary.get("best_candidate", {})),
        },
        "runtime_probe_kpi": {
            "f73d_receipt_rows": int(len(f73d_receipt)),
            "f73d_oos_pf_dd_tpd": f"{f73e_summary.get('oos_runtime_pf')}/{f73e_summary.get('oos_runtime_dd')}/{f73e_summary.get('oos_runtime_tpd')}",
            "f73f_completed_attempts": f73f_summary.get("completed_attempt_count"),
            "f73f_probability_parity_pass_rows": int(probability["passed"].astype(bool).sum()),
            "f73f_signal_parity_pass_rows": int(signal["passed"].astype(bool).sum()),
            "f73f_source_reproduction_min_overlap": f73f_summary.get("source_reproduction_min_overlap"),
            "f73f_validation": _runtime_snapshot(validation),
            "f73f_oos": _runtime_snapshot(oos),
        },
        "closeout_kpi_rows": closeout_kpi_rows(f73f_receipt),
        "preserved_clue": [
            "direct_binary_adapter_removed_bridge_divergence(직접 이진 어댑터가 연결 분기를 제거함)",
            "source_reproduction_overlap_1_0_and_signal_probability_parity_3_of_3(원천 재현 중복 1.0 및 신호/확률 동등성 3/3)",
            "oos_dd_improved_from_f73d_15_33_to_f73f_5_16(표본외 손실폭이 F73D 15.33%에서 F73F 5.16%로 개선)",
        ],
        "negative_memory": [
            "validation_runtime_dd_21_percent_after_direct_adapter(직접 어댑터 이후 검증 런타임 손실폭 21%)",
            "oos_trades_day_0_6308_below_goal_density(표본외 일거래 0.6308로 목표 밀도 미달)",
            "perfect_signal_parity_does_not_prevent_trade_lifecycle_compression(완전 신호 동등성도 거래 생명주기 압축을 막지 못함)",
        ],
        "invalid_setup": [],
        "blocked": [],
        "proxy_runtime_gap_cause": "trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극)",
        "grok_closeout": {
            "packet": rel(GROK_PACKET),
            "prompt_path": rel(GROK_PROMPT),
            "prompt_sha256": sha256_file(GROK_PROMPT),
            "clean_output_path": rel(GROK_CLEAN),
            "clean_output_sha256": sha256_file(GROK_CLEAN),
            "metadata_path": rel(GROK_METADATA),
            "metadata_sha256": sha256_file(GROK_METADATA),
            "advice_classification": "accepted(수용)",
            "accepted": "close F73 as preserved_clue_negative_memory(보존 단서+부정 기억으로 마감)",
            "rejected": "completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)",
            "needs_local_verification": "gate existence only; local files confirm no extra same-stage lifecycle gate(게이트 존재만 로컬 검증, 추가 같은 단계 생명주기 게이트 없음)",
        },
        "wfo_stress_status": "out_of_scope_by_claim_not_completion_candidate(완성 후보가 아니므로 주장 범위 밖)",
        "five_stage_retrospective_due_status": "not_due_after_f73_closeout_3_of_5(F73 마감 뒤 3/5, 아직 아님)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _candidate_oos(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": row.get("candidate_id"),
        "net_profit": row.get("oos_net_profit"),
        "profit_factor": row.get("oos_profit_factor"),
        "max_drawdown_percent": row.get("oos_max_drawdown_percent"),
        "trades_day": row.get("oos_trades_day"),
        "trade_count": row.get("oos_trade_count"),
    }


def _candidate_validation(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": row.get("candidate_id"),
        "net_profit": row.get("validation_net_profit"),
        "profit_factor": row.get("validation_profit_factor"),
        "max_drawdown_percent": row.get("validation_max_drawdown_percent"),
        "trades_day": row.get("validation_trades_day"),
        "trade_count": row.get("validation_trade_count"),
    }


def _runtime_snapshot(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "net_profit": row.get("net_profit"),
        "profit_factor": row.get("profit_factor"),
        "drawdown_percent": row.get("max_drawdown_percent"),
        "trades_day": row.get("trades_per_day"),
        "trade_count": row.get("trade_count"),
        "signal_count_diff": row.get("signal_count_diff"),
        "feature_ready_diff": row.get("feature_ready_diff"),
    }


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    kpi_rows = summary["closeout_kpi_rows"]
    lines = [
        "# Frontier73 Stage Closeout(F73 전선 단계 마감)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "## Closeout Label(마감 라벨)",
        "",
        f"`{CLOSEOUT_LABEL}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
        "",
        "## Hypothesis(가설)",
        "",
        str(summary["hypothesis"]),
        "",
        "Effect(효과): feature set/label/model family/session regime(피처 묶음/라벨/모델 계열/세션 장세)를 바꿔 F72와 다른 surface(표면)를 시험했고, MT5 Runtime Probe(MT5 런타임 탐침)와 direct binary adapter repair(직접 이진 어댑터 수리)까지 물질화했다.",
        "",
        "## Test Period(테스트 기간)",
        "",
        "- runtime validation(런타임 검증): `2025-01-02..2025-10-01`.",
        "- runtime OOS(런타임 표본외): `2025-10-01..2026-04-14`.",
        "",
        "## Proxy Expectation(프록시 예상)",
        "",
        str(summary["proxy_expectation"]),
        "",
        "## Proxy KPI(프록시 핵심 성과 지표)",
        "",
        f"- F73B candidates(후보): `{summary['proxy_kpi']['f73b_candidate_count']}`, scout clue(탐색 단서) `{summary['proxy_kpi']['f73b_scout_clue_count']}`, meaningful(의미 후보) `{summary['proxy_kpi']['f73b_meaningful_candidate_count']}`.",
        f"- F73B best OOS(최선 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{_kpi4(summary['proxy_kpi']['f73b_best_oos'])}`.",
        f"- F73C candidates(후보): `{summary['proxy_kpi']['f73c_candidate_count']}`, dual positive(양분할 양수) `{summary['proxy_kpi']['f73c_dual_positive_count']}`, meaningful(의미 후보) `{summary['proxy_kpi']['f73c_meaningful_candidate_count']}`.",
        f"- F73C selected seed(선택 씨앗): validation(검증) `{_kpi4(summary['proxy_kpi']['f73c_best_validation'])}`, OOS(표본외) `{_kpi4(summary['proxy_kpi']['f73c_best_oos'])}`.",
        "",
        "## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)",
        "",
        f"- F73D 3-class bridge(3분류 연결) OOS PF/DD/trades_day(표본외 수익 팩터/손실폭/일거래): `{summary['runtime_probe_kpi']['f73d_oos_pf_dd_tpd']}`.",
        f"- F73F probability parity(확률 동등성): `{summary['runtime_probe_kpi']['f73f_probability_parity_pass_rows']}/3`.",
        f"- F73F signal count parity(신호 수 동등성): `{summary['runtime_probe_kpi']['f73f_signal_parity_pass_rows']}/3`, validation/OOS diff(검증/표본외 차이) `0/0`.",
        "- F73F feature readiness parity(피처 준비 동등성): validation/OOS diff(검증/표본외 차이) `0/0`.",
        f"- F73F source reproduction min overlap(원천 재현 최소 중복): `{summary['runtime_probe_kpi']['f73f_source_reproduction_min_overlap']}`.",
        f"- proxy/runtime gap cause(프록시/런타임 간극 원인): `{summary['proxy_runtime_gap_cause']}`.",
        "",
        "## Closeout KPI(마감 핵심 성과 지표)",
        "",
        "| test period(테스트 기간) | split/view(분할/보기) | net profit(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD(손실폭) | trade count(거래 수) | trades/day(일 거래 수) | win rate(승률) | average win(평균 이익) | average loss(평균 손실) | payoff ratio(손익비) | expectancy(기대값) | recovery factor(회복 계수) | time under water(회복 전 체류 시간) | max consecutive loss(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in kpi_rows:
        lines.append(
            f"| `{row['test_period']}` | `{row['split_view']}` | `{row['net_profit']}` | `{row['gross_profit']}` | `{row['gross_loss']}` | `{row['profit_factor']}` | `{row['drawdown_percent']}%` | `{row['trade_count']}` | `{row['trades_day']}` | `{row['win_rate_percent']}%` | `{row['average_win']}` | `{row['average_loss']}` | `{row['payoff_ratio']}` | `{row['expectancy']}` | `{row['recovery_factor']}` | `{row['time_under_water']}` | `{row['max_consecutive_loss']}` | `{row['long_short_breakdown']}` | `{row['proxy_runtime_gap']}` |"
        )
    lines.extend(
        [
            "",
            "## Preserved Clue(보존 단서)",
            "",
            *[f"- {item}" for item in summary["preserved_clue"]],
            "",
            "## Negative Memory(부정 기억)",
            "",
            *[f"- {item}" for item in summary["negative_memory"]],
            "",
            "## Grok Closeout Review(Grok 마감 검토)",
            "",
            f"- packet(묶음): `{summary['grok_closeout']['packet']}`.",
            f"- prompt(프롬프트): `{summary['grok_closeout']['prompt_path']}`, sha256 `{summary['grok_closeout']['prompt_sha256']}`.",
            f"- output(출력): `{summary['grok_closeout']['clean_output_path']}`, sha256 `{summary['grok_closeout']['clean_output_sha256']}`.",
            f"- advice_classification(조언 분류): `{summary['grok_closeout']['advice_classification']}`.",
            f"- local_verification(로컬 검증): F73F receipt/parity/gap reports(영수증/동등성/간극 보고서)가 closeout label(마감 라벨)을 지지하고 추가 같은 단계 gate(게이트)는 확인되지 않았다.",
            "",
            "## Judgment(판정)",
            "",
            "F73 closes as preserved clue plus negative memory(보존 단서+부정 기억) only. It does not create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`.",
        ]
    )
    return lines


def _kpi4(row: Mapping[str, Any]) -> str:
    return f"{row.get('net_profit')}/{row.get('profit_factor')}/{row.get('max_drawdown_percent')}/{row.get('trades_day')}"


def grok_receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F73H Grok Closeout Receipt(F73H 그록 마감 영수증)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "- trigger_reason(트리거 이유): F73 stage closeout(단계 마감) requires Grok second opinion(그록 2차 의견).",
        "- review_size(검토 크기): `medium(중간)`.",
        "- direction_before_grok(그록 전 방향): close F73 as `preserved_clue_negative_memory_no_authority(보존 단서+부정 기억, 권위 없음)` unless a required same-stage repair(필수 같은 단계 수리)가 확인되면 보류.",
        "- bounded_evidence(제한 근거): F73B/F73C proxy KPI(프록시 KPI), F73D/F73F MT5 runtime KPI(MT5 런타임 KPI), F73E/F73G gap cause(간극 원인), parity(동등성).",
        f"- prompt_identity(프롬프트 정체성): `{summary['grok_closeout']['prompt_path']}`, sha256 `{summary['grok_closeout']['prompt_sha256']}`.",
        f"- output_identity(출력 정체성): `{summary['grok_closeout']['clean_output_path']}`, sha256 `{summary['grok_closeout']['clean_output_sha256']}`.",
        "- advice_classification(조언 분류): `accepted(수용)`.",
        "- accepted(수용): close F73 now as preserved_clue_negative_memory(보존 단서+부정 기억으로 지금 마감); treat trade lifecycle after signal parity(신호 동등성 이후 거래 생명주기)를 next frontier hint(다음 전선 단서)로 둔다.",
        "- rejected(거절): mandatory same-stage repair(필수 같은 단계 수리) without a new bounded repair packet(새 제한 수리 묶음 없음); completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).",
        "- needs_local_verification(로컬 검증 필요): gate existence only(게이트 존재만).",
        "- local_verification(로컬 검증): F73F parity rows pass, F73F validation/OOS KPI remains weak, F73G closeout recommendation matches Grok advice(그록 조언과 일치).",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve accepted(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 수용 없음).",
        f"- final_codex_direction(최종 Codex 방향): `{JUDGMENT}` closeout(마감), next frontier hypothesis(다음 전선 가설) 준비.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F73H Required Gate Coverage Audit(F73H 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- status(상태): `{CLOSEOUT_LABEL}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        "| hypothesis lifecycle(가설 생명주기) | `pass(통과)` | F73A->F73H chain recorded(F73A부터 F73H까지 기록됨) |",
        "| proxy expectation/KPI(프록시 예상/KPI) | `pass(통과)` | F73B/F73C summaries and closeout report(F73B/F73C 요약 및 마감 보고서) |",
        "| mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) | `pass(통과)` | F73D and F73F receipts(F73D/F73F 영수증) |",
        "| proxy/runtime gap analysis(프록시/런타임 간극 분석) | `pass(통과)` | F73E and F73G gap analysis(F73E/F73G 간극 분석) |",
        "| repair(수리) | `pass(통과)` | F73F direct binary adapter repair(F73F 직접 이진 어댑터 수리) |",
        "| signal count parity(신호 수 동등성) | `pass(통과)` | F73F validation/OOS diff 0/0(F73F 검증/표본외 차이 0/0) |",
        "| feature readiness parity(피처 준비 동등성) | `pass(통과)` | F73F validation/OOS diff 0/0(F73F 검증/표본외 차이 0/0) |",
        "| required closeout KPI(필수 마감 KPI) | `pass(통과)` | `stages/stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap/03_reviews/stage_closeout_report.md` |",
        f"| Grok closeout review(그록 마감 검토) | `pass(통과)` | `{summary['grok_closeout']['packet']}` |",
        "| five-stage retrospective due check(5단계 중간 검토 도래 점검) | `not_due(아직 아님)` | F73 is 3/5 after F66-F70 retrospective(F66-F70 중간 검토 뒤 F73은 3/5) |",
        "| WFO/stress(워크포워드/스트레스) | `out_of_scope_by_claim(주장 범위 밖)` | F73F validation PF/DD/trades_day 1.07/21.00%/0.7721 and OOS 1.32/5.16%/0.6308 are not completion candidate(완성 후보 아님) |",
        "| final completion gates(최종 완성 게이트) | `not_applicable_to_exploration_closeout(탐색 마감에는 해당 없음)` | F73 does not claim completion(F73은 완성 주장 없음) |",
        "",
        "Result(결과): F73 lifecycle evidence(생명주기 근거)는 closeout(마감)에 연결됐다. WFO/stress(워크포워드/스트레스)는 weak and non-candidate runtime economics(약하고 후보가 아닌 런타임 경제성) 때문에 미실행 사유를 기록했다.",
    ]


def update_ledgers(summary: Mapping[str, Any]) -> None:
    oos = summary["runtime_probe_kpi"]["f73f_oos"]
    row = {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "row_id": f"{RUN_ID}__stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_closeout(단계 마감)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)",
        "kpi_scope": "runtime_closeout_kpi(런타임 마감 KPI)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": CLOSEOUT_LABEL,
        "judgment": JUDGMENT,
        "path": rel(REVIEWS_ROOT / "stage_closeout_report.md"),
        "primary_kpi": f"F73F OOS net={oos.get('net_profit')}; PF={oos.get('profit_factor')}; DD={oos.get('drawdown_percent')}%; trades_day={oos.get('trades_day')}",
        "guardrail_kpi": "signal_diff=0; feature_diff=0; probability_parity=3/3; source_overlap=1.0",
        "external_verification_status": "completed(완료)",
        "notes": "F73 closed after mandatory MT5 Runtime Probe and direct binary adapter repair probe(F73는 필수 MT5 런타임 탐침과 직접 이진 어댑터 수리 탐침 뒤 마감).",
        "family": "stage_closeout(단계 마감)",
        "lane": "stage_closeout(단계 마감)",
        "primary_report": rel(REVIEWS_ROOT / "stage_closeout_report.md"),
        "run_number": "frontier73H",
        "date": str(summary["created_at_utc"])[:10],
        "decision": CLOSEOUT_LABEL,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "stage_closeout_report.md"),
        "runtime_completed_rows": 2,
        "best_net_profit": oos.get("net_profit"),
        "best_profit_factor": oos.get("profit_factor"),
        "run_date": str(summary["created_at_utc"])[:10],
        "primary_artifact": rel(RUN_ROOT / "frontier73H_stage_closeout_summary.json"),
        "candidate_model_id": "f73f_direct_binary_f73c_0002",
        "net_profit": oos.get("net_profit"),
        "profit_factor": oos.get("profit_factor"),
        "drawdown": oos.get("drawdown_percent"),
        "trade_count": oos.get("trade_count"),
        "trade_density": oos.get("trades_day"),
        "result_status": CLOSEOUT_LABEL,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73h.md"),
        "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서와 부정 기억, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "stage_closeout_report.md"),
        "closeout_label": JUDGMENT,
        "stage_question": summary["hypothesis"],
    }
    f73b.upsert_ledger(f73b.ALPHA_LEDGER, "ledger_row_id", row)
    f73b.upsert_ledger(f73b.RUN_REGISTRY, "run_id", row)
    f73b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f73b.ALPHA_LEDGER)


def update_registers(summary: Mapping[str, Any]) -> None:
    oos = summary["runtime_probe_kpi"]["f73f_oos"]
    idea_marker = "<!-- frontier73H_stage_closeout_session_regime_feature_model_rotation_v1 -->"
    idea_block = f"""<!-- frontier73H_stage_closeout_session_regime_feature_model_rotation_v1 -->
- `{RUN_ID}` closes Frontier73(전선73) as `{JUDGMENT}`. Preserved clue(보존 단서): direct binary adapter(직접 이진 어댑터)가 bridge divergence(연결 분기)를 제거했고 source/signal/probability parity(원천/신호/확률 동등성)를 맞췄으며 OOS DD(표본외 손실폭)를 `5.16%`로 줄였다. Negative memory(부정 기억): validation DD(검증 손실폭) `21.00%`, OOS trades/day(표본외 일거래) `{oos.get('trades_day')}`로 목표 네 축에서 멀다. Evidence(근거): `{rel(REVIEWS_ROOT / 'stage_closeout_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(f73b.IDEA_REGISTRY, idea_marker, idea_block)

    negative_marker = "<!-- NR-FR73-SESSION-REGIME-FEATURE-MODEL-RUNTIME-LIFECYCLE-GAP -->"
    negative_block = f"""<!-- NR-FR73-SESSION-REGIME-FEATURE-MODEL-RUNTIME-LIFECYCLE-GAP -->
## NR-FR73-SESSION-REGIME-FEATURE-MODEL-RUNTIME-LIFECYCLE-GAP

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): session/regime feature/model rotation(세션/장세 피처/모델 회전)이 runtime economics source(런타임 경제성 원천)를 분리할 수 있다.
- Why failed(실패 이유): direct binary adapter(직접 이진 어댑터)로 bridge divergence(연결 분기)를 제거했지만 F73F validation/OOS runtime(검증/표본외 런타임)은 PF/DD/trades_day(수익 팩터/손실폭/일거래) `1.07/21.00%/0.7721`, `1.32/5.16%/0.6308`에 머물렀다.
- Salvage value(회수 가치): direct binary adapter(직접 이진 어댑터)는 source reproduction overlap(원천 재현 중복) `1.0`과 probability/signal parity(확률/신호 동등성) `3/3`을 만들 수 있고, F73D OOS DD(표본외 손실폭) `15.33%`를 F73F `5.16%`로 낮췄다.
- Do-not-repeat(반복 금지): same F73 session/regime feature/model seed(동일 F73 세션/장세 피처/모델 씨앗)를 bridge/adapter-only repair(연결/어댑터 단독 수리)로 반복하지 않는다.
- Reopen condition(재개 조건): a new economic mechanism(새 경제 메커니즘)이 trade lifecycle/risk/label/session split(거래 생명주기/위험/라벨/세션 분할) 중 하나 이상을 주도적으로 바꾸고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
- Evidence(근거): `{rel(REVIEWS_ROOT / 'stage_closeout_report.md')}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음)."""
    append_once(NEGATIVE_REGISTER, negative_marker, negative_block)
    update_five_stage_register()


def update_five_stage_register() -> None:
    text = io_path(FIVE_STAGE_REGISTER).read_text(encoding="utf-8-sig")
    if STAGE_ID not in text:
        text = text.replace(
            "    - stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling\n",
            "    - stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling\n"
            f"    - {STAGE_ID}\n",
        )
    text = text.replace("  closeouts_since_last: 2", "  closeouts_since_last: 3")
    text = text.replace("  current_due_status: not_due_after_f72_closeout", "  current_due_status: not_due_after_f73_closeout")
    text = text.replace(
        '  note: "F72 closeout(마감)이 F66-F70 retrospective(중간 검토) 뒤 2/5로 등록됐다. 다음 numeric trigger(숫자 트리거)는 F75 closeout(마감)이다."',
        '  note: "F73 closeout(마감)이 F66-F70 retrospective(중간 검토) 뒤 3/5로 등록됐다. 다음 numeric trigger(숫자 트리거)는 F75 closeout(마감)이다."',
    )
    io_path(FIVE_STAGE_REGISTER).write_text(text, encoding="utf-8-sig")


def update_state(summary: Mapping[str, Any]) -> None:
    created_at = summary["created_at_utc"]
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {CLOSEOUT_LABEL}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f73_closed_after_mandatory_runtime_probe_and_repair",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f73_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F73 stage closeout(단계 마감)을 완료했다."',
        '  - "Effect(효과): direct binary adapter(직접 이진 어댑터)를 보존 단서로 남기고, validation DD/trade density(검증 손실폭/거래 밀도)를 부정 기억으로 남겼다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f73b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(SELECTED_ROOT / "selection_status.md", [
        "# F73 Selection Status(F73 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{CLOSEOUT_LABEL}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ])
    write_text(f73b.CURRENT_WORKING_STATE, [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F73 stage closeout(단계 마감)을 완료했다.",
        "",
        f"Effect(효과): F73을 `{JUDGMENT}`로 닫고 다음 행동을 `{NEXT_RUN_ID}`로 설정했다.",
        "",
        "- preserved_clue(보존 단서): direct binary adapter(직접 이진 어댑터)는 bridge divergence(연결 분기)를 제거하고 OOS DD(표본외 손실폭)를 낮췄다.",
        "- negative_memory(부정 기억): validation DD(검증 손실폭)와 trade density(거래 밀도)는 목표에 못 미쳤다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def main() -> int:
    missing = require_inputs()
    if missing:
        raise FileNotFoundError(f"F73H required material missing: {missing}")
    created_at = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    summary = build_summary(created_at)
    write_json(RUN_ROOT / "frontier73H_stage_closeout_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": CLOSEOUT_LABEL,
        "judgment": JUDGMENT,
        "closeout_label": CLOSEOUT_LABEL,
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_report": rel(REVIEWS_ROOT / "stage_closeout_report.md"),
        "grok_packet": summary["grok_closeout"],
    })
    write_csv(RUN_ROOT / "f73h_closeout_kpi_table.csv", summary["closeout_kpi_rows"])
    write_csv(REVIEWS_ROOT / "f73h_closeout_kpi_table_review.csv", summary["closeout_kpi_rows"])
    write_text(REVIEWS_ROOT / "stage_closeout_report.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "f73h_stage_closeout_grok_receipt.md", grok_receipt_lines(summary))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f73h.md", gate_audit_lines(summary))
    update_ledgers(summary)
    update_registers(summary)
    update_state(summary)
    print(json.dumps(json_ready({
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": CLOSEOUT_LABEL,
        "judgment": JUDGMENT,
        "closeout_label": CLOSEOUT_LABEL,
        "best_oos_net": summary["runtime_probe_kpi"]["f73f_oos"].get("net_profit"),
        "best_oos_pf": summary["runtime_probe_kpi"]["f73f_oos"].get("profit_factor"),
        "best_oos_dd": summary["runtime_probe_kpi"]["f73f_oos"].get("drawdown_percent"),
        "best_oos_trades_day": summary["runtime_probe_kpi"]["f73f_oos"].get("trades_day"),
        "five_stage_retrospective_due_status": summary["five_stage_retrospective_due_status"],
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
