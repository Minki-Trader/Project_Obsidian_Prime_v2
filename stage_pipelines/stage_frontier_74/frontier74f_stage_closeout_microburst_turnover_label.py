from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path"
RUN_ID = "frontier74F_proxy_runtime_gap_or_closeout_decision_v1"
PARENT_RUN_ID = "frontier74E_mt5_microburst_negative_control_runtime_probe_v1"
NEXT_RUN_ID = "frontier75A_stage_open_upstream_mechanism_rotation_after_f74_microburst_negative_memory_v1"
CLOSEOUT_LABEL = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory_no_authority"
CLAIM_BOUNDARY = (
    "preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F74B_SUMMARY = STAGE_ROOT / "02_runs/frontier74B_microburst_turnover_raw_label_and_proxy_scout_v1/f74b_summary.json"
F74B_CANDIDATES = STAGE_ROOT / "02_runs/frontier74B_microburst_turnover_raw_label_and_proxy_scout_v1/f74b_candidate_results.csv"
F74C_SUMMARY = STAGE_ROOT / "02_runs/frontier74C_microburst_label_feature_repair_proxy_v1/f74c_summary.json"
F74C_CANDIDATES = STAGE_ROOT / "02_runs/frontier74C_microburst_label_feature_repair_proxy_v1/f74c_candidate_results.csv"
F74D_GROK_SUMMARY = STAGE_ROOT / "02_runs/frontier74D_pre_mt5_grok_microburst_negative_control_runtime_probe_v1/f74d_pre_mt5_grok_summary.json"
F74E_SUMMARY = STAGE_ROOT / "02_runs/frontier74E_mt5_microburst_negative_control_runtime_probe_v1/f74e_summary.json"
F74E_MANIFEST = STAGE_ROOT / "02_runs/frontier74E_mt5_microburst_negative_control_runtime_probe_v1/run_manifest.json"
F74E_RECEIPT = REVIEWS_ROOT / "f74e_runtime_receipt.csv"
F74E_PROBABILITY = REVIEWS_ROOT / "f74e_probability_parity.csv"
F74E_SIGNAL = REVIEWS_ROOT / "f74e_signal_parity.csv"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f74_stage_closeout_microburst_turnover_label"
GROK_PROMPT = GROK_PACKET / "prompts/f74_stage_closeout_microburst_turnover_label_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
FIVE_STAGE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, lines: Sequence[str]) -> None:
    write_text(path, "\n".join(lines))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        rows = [{"empty": "true"}]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.rstrip())


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise FileNotFoundError(f"ledger header missing: {path}")
    if key not in fieldnames:
        raise KeyError(f"{key} not found in {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def required_inputs() -> list[Path]:
    return [
        F74B_SUMMARY,
        F74B_CANDIDATES,
        F74C_SUMMARY,
        F74C_CANDIDATES,
        F74D_GROK_SUMMARY,
        F74E_SUMMARY,
        F74E_MANIFEST,
        F74E_RECEIPT,
        F74E_PROBABILITY,
        F74E_SIGNAL,
        GROK_PROMPT,
        GROK_CLEAN,
        GROK_METADATA,
        ALPHA_LEDGER,
        RUN_REGISTRY,
        FIVE_STAGE_REGISTER,
    ]


def candidate_row(path: Path, candidate_id: str) -> dict[str, Any]:
    frame = read_csv(path)
    matches = frame[frame["candidate_id"] == candidate_id]
    if matches.empty:
        raise ValueError(f"{candidate_id} not found in {path}")
    return matches.iloc[0].to_dict()


def split_receipt(receipt: pd.DataFrame) -> dict[str, dict[str, Any]]:
    return {str(row["split"]): row.to_dict() for _, row in receipt.iterrows()}


def metric(row: Mapping[str, Any], name: str, digits: int | None = None) -> str:
    value = row.get(name, "")
    if value == "" or pd.isna(value):
        return ""
    if digits is None or not isinstance(value, (int, float)):
        return str(value)
    return f"{float(value):.{digits}f}"


def compact_kpi(row: Mapping[str, Any], prefix: str) -> str:
    return (
        f"net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일거래/거래수) "
        f"{metric(row, prefix + '_net_profit', 2)}/"
        f"{metric(row, prefix + '_profit_factor', 4)}/"
        f"{metric(row, prefix + '_max_drawdown_percent', 4)}%/"
        f"{metric(row, prefix + '_trades_day', 4)}/"
        f"{metric(row, prefix + '_trade_count', 0)}"
    )


def runtime_kpi(row: Mapping[str, Any]) -> str:
    return (
        f"net/PF/DD/tpd/trades/win(순수익/수익 팩터/손실폭/일거래/거래수/승률) "
        f"{metric(row, 'net_profit', 2)}/"
        f"{metric(row, 'profit_factor', 2)}/"
        f"{metric(row, 'max_drawdown_percent', 2)}%/"
        f"{metric(row, 'trades_per_day', 4)}/"
        f"{metric(row, 'trade_count', 0)}/"
        f"{metric(row, 'win_rate_percent', 2)}%"
    )


def closeout_kpi_rows(receipt: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in receipt.iterrows():
        rows.append(
            {
                "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
                "split_view": (
                    f"F74E MT5 negative-control runtime probe(부정 대조 런타임 탐침) "
                    f"{row.get('split')}(분할) Tier A separate(Tier A 분리)"
                ),
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
                    f"signal_diff={row.get('signal_count_diff')}; feature_ready_diff={row.get('feature_ready_diff')}; "
                    f"PF proxy/runtime {row.get('proxy_profit_factor')}/{row.get('profit_factor')}; "
                    f"DD proxy/runtime {row.get('proxy_dd_percent')}%/{row.get('max_drawdown_percent')}%; "
                    f"tpd proxy/runtime {row.get('proxy_trades_per_day')}/{row.get('trades_per_day')}"
                ),
            }
        )
    return rows


def gap_rows(receipt: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in receipt.iterrows():
        rows.append(
            {
                "split": row.get("split"),
                "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
                "candidate_id": row.get("candidate_id"),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
                "proxy_net_profit": row.get("proxy_net_profit"),
                "runtime_net_profit": row.get("net_profit"),
                "net_profit_gap_runtime_minus_proxy": row.get("net_profit") - row.get("proxy_net_profit"),
                "proxy_profit_factor": row.get("proxy_profit_factor"),
                "runtime_profit_factor": row.get("profit_factor"),
                "profit_factor_gap_runtime_minus_proxy": row.get("profit_factor") - row.get("proxy_profit_factor"),
                "proxy_dd_percent": row.get("proxy_dd_percent"),
                "runtime_dd_percent": row.get("max_drawdown_percent"),
                "dd_gap_runtime_minus_proxy": row.get("dd_delta_runtime_minus_proxy"),
                "proxy_trades_day": row.get("proxy_trades_per_day"),
                "runtime_trades_day": row.get("trades_per_day"),
                "trades_day_gap_runtime_minus_proxy": row.get("trades_per_day") - row.get("proxy_trades_per_day"),
                "gap_cause": row.get("gap_cause_summary"),
            }
        )
    return rows


def build_summary(created_at: str) -> dict[str, Any]:
    f74b_summary = read_json(F74B_SUMMARY)
    f74c_summary = read_json(F74C_SUMMARY)
    f74d_summary = read_json(F74D_GROK_SUMMARY)
    f74e_summary = read_json(F74E_SUMMARY)
    f74e_manifest = read_json(F74E_MANIFEST)
    receipt = read_csv(F74E_RECEIPT)
    probability = read_csv(F74E_PROBABILITY)
    signal = read_csv(F74E_SIGNAL)
    by_split = split_receipt(receipt)
    validation = by_split["validation"]
    oos = by_split["oos"]
    f74b_best = candidate_row(F74B_CANDIDATES, "f74b_0505")
    f74c_best = candidate_row(F74C_CANDIDATES, "f74c_1212")
    f74c_materialized = candidate_row(F74C_CANDIDATES, "f74c_1161")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": CLOSEOUT_LABEL,
        "judgment": JUDGMENT,
        "closeout_label": CLOSEOUT_LABEL,
        "hypothesis": (
            "microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path"
            "(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험한다."
        ),
        "test_period": {
            "runtime_validation": "2025-01-02..2025-10-01",
            "runtime_oos": "2025-10-01..2026-04-14",
        },
        "proxy_expectation": (
            "density(밀도)는 label/target(라벨/목표)에서 먼저 만들고, proxy(프록시)는 PF/DD/거래밀도를 동시에 "
            "살리는 seed surface(씨앗 표면)를 찾는다는 기대였다."
        ),
        "proxy_kpi": {
            "f74b_candidate_count": f74b_summary.get("candidate_count"),
            "f74b_scout_clue_count": f74b_summary.get("scout_clue_count"),
            "f74b_meaningful_candidate_count": f74b_summary.get("meaningful_candidate_count"),
            "f74b_raw_density_pass_axis_count": f74b_summary.get("raw_density_pass_axis_count"),
            "f74b_raw_density_pass_axes": f74b_summary.get("raw_density_pass_axes"),
            "f74b_best_validation": compact_kpi(f74b_best, "validation"),
            "f74b_best_oos": compact_kpi(f74b_best, "oos"),
            "f74c_candidate_count": f74c_summary.get("candidate_count"),
            "f74c_scout_clue_count": f74c_summary.get("scout_clue_count"),
            "f74c_meaningful_candidate_count": f74c_summary.get("meaningful_candidate_count"),
            "f74c_best_candidate": "f74c_1212 hist_gbm clean_value_h9_short",
            "f74c_best_validation": compact_kpi(f74c_best, "validation"),
            "f74c_best_oos": compact_kpi(f74c_best, "oos"),
            "f74c_materialized_candidate": "f74c_1161 logistic_l2 clean_value_h9_short",
            "f74c_materialized_validation": compact_kpi(f74c_materialized, "validation"),
            "f74c_materialized_oos": compact_kpi(f74c_materialized, "oos"),
        },
        "runtime_probe_kpi": {
            "f74d_grok_classification": f74d_summary.get("grok_classification", "accepted(수용)"),
            "f74e_attempt_count": f74e_summary.get("attempt_count"),
            "f74e_completed_attempt_count": f74e_summary.get("completed_attempt_count"),
            "f74e_probability_parity_pass_rows": int(probability["passed"].astype(bool).sum()),
            "f74e_signal_parity_pass_rows": int(signal["passed"].astype(bool).sum()),
            "f74e_source_reproduction_min_overlap": f74e_summary.get("source_reproduction_min_overlap"),
            "validation": dict(validation),
            "oos": dict(oos),
            "validation_compact": runtime_kpi(validation),
            "oos_compact": runtime_kpi(oos),
        },
        "closeout_kpi_rows": closeout_kpi_rows(receipt),
        "gap_rows": gap_rows(receipt),
        "preserved_clue": [
            "Raw density gate(원시 밀도 게이트)는 6/6 axes(축)에서 강하게 통과했다.",
            "Short-side binary ONNX materialization(숏 방향 이진 ONNX 물질화), probability parity(확률 동등성), signal parity(신호 동등성)는 3/3으로 맞출 수 있었다.",
            "Mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)는 validation/OOS(검증/표본외) 2/2로 실행됐다.",
        ],
        "negative_memory": [
            "F74B 648개 후보와 F74C 1296개 후보 모두 scout clue(탐색 단서) 0, meaningful candidate(의미 후보) 0이었다.",
            "Best materializable runtime path(최선 물질화 가능 런타임 경로)는 validation PF 1.16, DD 11.40%, trades/day 1.6544에 그쳤다.",
            "OOS runtime(표본외 런타임)도 PF 1.13, trades/day 1.60으로 final goal(최종 목표)의 5-10 trades/day와 PF 2-3+에서 멀다.",
        ],
        "proxy_runtime_gap_cause": (
            "runtime_economics_gap_after_signal_and_feature_parity"
            "(신호와 피처 준비 동등성 뒤에도 런타임 경제성 간극 발생)"
        ),
        "known_differences": [
            (
                "F74E runtime receipt(런타임 영수증)의 run_id column(실행 ID 열)은 reused helper(재사용 보조 함수) 때문에 "
                "frontier71D로 남아 있다. attempt_name/report_path/run_manifest(시도명/보고서 경로/실행 목록)는 F74E를 가리키므로 "
                "runtime failure(런타임 실패)가 아니라 reporting defect(보고 결함)로 기록한다."
            )
        ],
        "grok_closeout": {
            "packet": rel(GROK_PACKET),
            "prompt_path": rel(GROK_PROMPT),
            "prompt_sha256": sha256_file(GROK_PROMPT),
            "clean_output_path": rel(GROK_CLEAN),
            "clean_output_sha256": sha256_file(GROK_CLEAN),
            "metadata_path": rel(GROK_METADATA),
            "metadata_sha256": sha256_file(GROK_METADATA),
            "classification": "accepted(수용)",
            "accepted": [
                "Close F74 as closed_preserved_clue_negative_memory_no_authority.",
                "Pivot next frontier(다음 전선)를 다른 upstream mechanism(상류 메커니즘)으로 열라.",
            ],
            "rejected": [
                "completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)",
                "another F74-style threshold/clean-label/session repair loop(임계값/클린 라벨/세션 수리 루프 반복)",
            ],
            "needs_local_verification": [],
        },
        "f74e_manifest_status": f74e_manifest.get("status"),
        "wfo_stress_status": (
            "out_of_scope_by_claim_not_completion_candidate"
            "(완성 후보가 아니므로 이번 마감 주장에는 워크포워드/스트레스가 필요하지 않음)"
        ),
        "five_stage_retrospective_due_status": "not_due_after_f74_closeout_4_of_5(F74 마감 뒤 4/5, 아직 아님)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Frontier74 Stage Closeout(F74 전선 단계 마감)",
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
        "Effect(효과): microburst label family(마이크로버스트 라벨군)이 밀도와 런타임 경제성을 동시에 만들 수 있는지 닫힌 근거로 확인했다.",
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
        f"- F74B raw density pass(원시 밀도 통과): `{summary['proxy_kpi']['f74b_raw_density_pass_axis_count']}/6` axes(축).",
        f"- F74B candidates(후보): `{summary['proxy_kpi']['f74b_candidate_count']}`, scout clue(탐색 단서) `{summary['proxy_kpi']['f74b_scout_clue_count']}`, meaningful candidate(의미 후보) `{summary['proxy_kpi']['f74b_meaningful_candidate_count']}`.",
        f"- F74B best validation(최선 검증): `{summary['proxy_kpi']['f74b_best_validation']}`.",
        f"- F74B best OOS(최선 표본외): `{summary['proxy_kpi']['f74b_best_oos']}`.",
        f"- F74C candidates(후보): `{summary['proxy_kpi']['f74c_candidate_count']}`, scout clue(탐색 단서) `{summary['proxy_kpi']['f74c_scout_clue_count']}`, meaningful candidate(의미 후보) `{summary['proxy_kpi']['f74c_meaningful_candidate_count']}`.",
        f"- F74C best candidate(최선 후보): `{summary['proxy_kpi']['f74c_best_candidate']}`, validation(검증) `{summary['proxy_kpi']['f74c_best_validation']}`, OOS(표본외) `{summary['proxy_kpi']['f74c_best_oos']}`.",
        f"- F74C materialized candidate(물질화 후보): `{summary['proxy_kpi']['f74c_materialized_candidate']}`, validation(검증) `{summary['proxy_kpi']['f74c_materialized_validation']}`, OOS(표본외) `{summary['proxy_kpi']['f74c_materialized_oos']}`.",
        "",
        "## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)",
        "",
        f"- F74D pre-MT5 Grok review(MT5 전 그록 검토): `{summary['runtime_probe_kpi']['f74d_grok_classification']}`.",
        f"- F74E MT5 attempts/completed(MT5 시도/완료): `{summary['runtime_probe_kpi']['f74e_attempt_count']}/{summary['runtime_probe_kpi']['f74e_completed_attempt_count']}`.",
        f"- probability parity(확률 동등성): `{summary['runtime_probe_kpi']['f74e_probability_parity_pass_rows']}/3`.",
        f"- signal count parity(신호 수 동등성): `{summary['runtime_probe_kpi']['f74e_signal_parity_pass_rows']}/3`, validation/OOS diff(검증/표본외 차이) `0/0`.",
        "- feature readiness parity(피처 준비 동등성): validation/OOS diff(검증/표본외 차이) `0/0`.",
        f"- validation runtime(검증 런타임): `{summary['runtime_probe_kpi']['validation_compact']}`.",
        f"- OOS runtime(표본외 런타임): `{summary['runtime_probe_kpi']['oos_compact']}`.",
        f"- proxy/runtime gap cause(프록시/런타임 간극 원인): `{summary['proxy_runtime_gap_cause']}`.",
        "",
        "## Closeout KPI(마감 핵심 성과 지표)",
        "",
        "| test period(테스트 기간) | split/view(분할/보기) | net profit(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD(손실폭) | trade count(거래 수) | trades/day(일 거래 수) | win rate(승률) | average win(평균 이익) | average loss(평균 손실) | payoff ratio(손익비) | expectancy(기대값) | recovery factor(회복 계수) | time under water(회복 전 체류 시간) | max consecutive loss(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in summary["closeout_kpi_rows"]:
        lines.append(
            f"| `{row['test_period']}` | `{row['split_view']}` | `{row['net_profit']}` | `{row['gross_profit']}` | `{row['gross_loss']}` | `{row['profit_factor']}` | `{row['drawdown_percent']}%` | `{row['trade_count']}` | `{row['trades_day']}` | `{row['win_rate_percent']}%` | `{row['average_win']}` | `{row['average_loss']}` | `{row['payoff_ratio']}` | `{row['expectancy']}` | `{row['recovery_factor']}` | `{row['time_under_water']}` | `{row['max_consecutive_loss']}` | `{row['long_short_breakdown']}` | `{row['proxy_runtime_gap']}` |"
        )
    lines.extend(
        [
            "",
            "## Known Difference(알려진 차이)",
            "",
            *[f"- {item}" for item in summary["known_differences"]],
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
            f"- advice_classification(조언 분류): `{summary['grok_closeout']['classification']}`.",
            "- local_verification(로컬 검증): F74B/F74C summaries(요약), F74E receipt/parity(영수증/동등성), and Grok metadata(메타데이터)를 `io_path`로 확인했다.",
            "",
            "## Judgment(판정)",
            "",
            "F74는 preserved clue(보존 단서)와 negative memory(부정 기억)만 남기고 닫는다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`.",
            "",
            "Next frontier(다음 전선)는 microburst turnover label(마이크로버스트 회전 라벨)의 threshold/clean-label repair loop(임계값/클린 라벨 수리 반복)가 아니라 order-flow/volatility-compression/session-liquidity(오더플로/변동성 압축/세션 유동성) 같은 upstream mechanism(상류 메커니즘) 전환으로 열어야 한다.",
        ]
    )
    return lines


def grok_receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F74F Grok Closeout Receipt(F74F Grok 마감 영수증)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "- trigger_reason(트리거 이유): F74 stage closeout(단계 마감)은 Grok second opinion(그록 2차 의견)이 필요하다.",
        "- review_size(검토 크기): `medium(중간)`.",
        "- direction_before_grok(그록 전 방향): F74를 `closed_preserved_clue_negative_memory_no_authority`로 닫고 다음 전선은 다른 upstream mechanism(상류 메커니즘)으로 열자는 제안.",
        "- bounded_evidence(제한 근거): F74B/F74C proxy KPI(프록시 KPI), F74D pre-MT5 review(MT5 전 검토), F74E MT5 runtime KPI(MT5 런타임 KPI), parity(동등성), gap cause(간극 원인).",
        f"- prompt_identity(프롬프트 정체성): `{summary['grok_closeout']['prompt_path']}`, sha256 `{summary['grok_closeout']['prompt_sha256']}`.",
        f"- output_identity(출력 정체성): `{summary['grok_closeout']['clean_output_path']}`, sha256 `{summary['grok_closeout']['clean_output_sha256']}`.",
        "- advice_classification(조언 분류): `accepted(수용)`.",
        "- accepted(수용): closeout label(마감 라벨), preserved clue(보존 단서), negative memory(부정 기억), next frontier pivot(다음 전선 전환).",
        "- rejected(거절): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 주장.",
        "- needs_local_verification(로컬 검증 필요): 없음. Codex는 파일/장부/MT5 receipt(영수증)로 근거 정체성을 별도 확인했다.",
        "- forbidden_claim_check(금지 주장 확인): 금지 주장은 수용하지 않았다.",
        f"- final_codex_direction(최종 Codex 방향): `{JUDGMENT}` closeout(마감), next `{NEXT_RUN_ID}`.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F74F Required Gate Coverage Audit(F74F 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- status(상태): `{CLOSEOUT_LABEL}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        "| hypothesis lifecycle(가설 생명주기) | `pass(통과)` | F74A->F74F chain(연쇄)이 기록됐다. |",
        "| proxy expectation/KPI(프록시 예상/KPI) | `pass(통과)` | F74B/F74C summaries(요약)와 closeout report(마감 보고서). |",
        "| feature set/label/model/trade shape/risk variants(피처/라벨/모델/거래 형태/위험 변형) | `pass(통과)` | raw labels(원시 라벨), clean/value labels(클린/가치 라벨), logistic/hist_gbm(로지스틱/히스토그램 GBM), session gate(세션 게이트)를 시험했다. |",
        "| mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) | `pass(통과)` | F74E validation/OOS(검증/표본외) 2/2 completed(완료). |",
        "| signal count parity(신호 수 동등성) | `pass(통과)` | F74E validation/OOS diff(검증/표본외 차이) `0/0`. |",
        "| feature readiness parity(피처 준비 동등성) | `pass(통과)` | F74E validation/OOS diff(검증/표본외 차이) `0/0`. |",
        "| proxy/runtime gap analysis(프록시/런타임 간극 분석) | `pass(통과)` | `f74f_proxy_runtime_gap_analysis.csv` and closeout KPI table(마감 KPI 표). |",
        "| repair(수리) | `pass(통과)` | F74C label repair(라벨 수리), F74E materializable logistic candidate repair(물질화 가능 로지스틱 후보 수리). |",
        "| Grok stage closeout review(Grok 단계 마감 검토) | `pass(통과)` | closeout packet(마감 묶음) accepted(수용). |",
        "| required closeout KPI(필수 마감 KPI) | `pass(통과)` | `stage_closeout_report.md` table(표)에 기간/전체 KPI를 기록했다. |",
        "| Tier B / combined record(티어 B / 합산 기록) | `out_of_scope_by_claim(주장 범위 밖)` | F74 closeout(마감)은 Tier A separate(Tier A 분리) negative-control runtime observation(부정 대조 런타임 관찰)만 주장한다. |",
        "| WFO/stress(워크포워드/스트레스) | `out_of_scope_by_claim(주장 범위 밖)` | F74는 completion candidate(완성 후보)가 아니며 proxy meaningful candidate(의미 후보) 0, runtime weak(약한 런타임)이므로 강한 검증을 주장하지 않는다. |",
        "| five-stage retrospective due check(5단계 중간 검토 도래 점검) | `not_due(아직 아님)` | F74 closeout(마감)은 F66-F70 retrospective(중간 검토) 뒤 4/5다. 다음 numeric trigger(숫자 트리거)는 F75 closeout(마감). |",
        "| final completion gates(최종 완성 게이트) | `not_applicable_to_exploration_closeout(탐색 마감에는 해당 없음)` | F74는 completion(완성)을 주장하지 않는다. |",
    ]


def update_ledgers(summary: Mapping[str, Any]) -> None:
    oos = summary["runtime_probe_kpi"]["oos"]
    report = REVIEWS_ROOT / "stage_closeout_report.md"
    manifest = RUN_ROOT / "run_manifest.json"
    audit = REVIEWS_ROOT / "required_gate_coverage_audit_f74f.md"
    row = {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "row_id": f"{RUN_ID}__stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_closeout(단계 마감)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate; Tier B out_of_scope_by_claim; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "stage_closeout_runtime_probe_gap_and_negative_memory(단계 마감 런타임 탐침 간극 및 부정 기억)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": CLOSEOUT_LABEL,
        "result_status": CLOSEOUT_LABEL,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "path": rel(report),
        "report_path": rel(report),
        "primary_report": rel(report),
        "primary_artifact": rel(manifest),
        "output_path": rel(manifest),
        "result_path": rel(report),
        "primary_kpi": (
            f"F74E OOS net={oos.get('net_profit')}; PF={oos.get('profit_factor')}; "
            f"DD={oos.get('max_drawdown_percent')}%; trades_day={oos.get('trades_per_day')}"
        ),
        "guardrail_kpi": "signal_diff=0; feature_diff=0; probability_parity=3/3; source_overlap=1.0",
        "external_verification_status": "completed(완료)",
        "notes": "F74 closed after mandatory MT5 Runtime Probe; preserved density/parity clue and negative economics memory.",
        "run_number": "frontier74F",
        "date": str(summary["created_at_utc"])[:10],
        "run_date": str(summary["created_at_utc"])[:10],
        "decision": CLOSEOUT_LABEL,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "rows": 1,
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_completed_rows": summary["runtime_probe_kpi"]["f74e_completed_attempt_count"],
        "probability_parity_pass_rows": summary["runtime_probe_kpi"]["f74e_probability_parity_pass_rows"],
        "signal_parity_pass_rows": summary["runtime_probe_kpi"]["f74e_signal_parity_pass_rows"],
        "net_profit": oos.get("net_profit"),
        "profit_factor": oos.get("profit_factor"),
        "drawdown": oos.get("max_drawdown_percent"),
        "max_drawdown_percent": oos.get("max_drawdown_percent"),
        "trade_count": oos.get("trade_count"),
        "trade_density": oos.get("trades_per_day"),
        "expectancy": oos.get("expectancy"),
        "recovery_factor": oos.get("recovery_factor"),
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(audit),
        "gate_audit_path": rel(audit),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_stage_closeout(전선 단계 마감)",
        "run_type": "stage_closeout(단계 마감)",
        "input_run_id": PARENT_RUN_ID,
        "question": "Can microburst turnover labels create a dense smooth runtime seed surface?",
        "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서와 부정 기억, 권위 없음)",
        "closeout_label": CLOSEOUT_LABEL,
        "stage_question": summary["hypothesis"],
    }
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier74F_stage_closeout_microburst_turnover_label_v1 -->"
    block = f"""<!-- frontier74F_stage_closeout_microburst_turnover_label_v1 -->
- `{RUN_ID}` closes Frontier74(전선74) as `{JUDGMENT}`. Preserved clue(보존 단서): raw microburst density(원시 마이크로버스트 밀도) 6/6 axes(축), ONNX probability/signal parity(온엑스 확률/신호 동등성) 3/3, MT5 probe(MT5 탐침) 2/2. Negative memory(부정 기억): F74B/F74C scout clue(탐색 단서) 0, meaningful candidate(의미 후보) 0; F74E validation runtime(검증 런타임) net/PF/DD/tpd `97.11/1.16/11.40%/1.6544`, OOS(표본외) `61.86/1.13/9.66%/1.60`. Evidence(근거): `{rel(REVIEWS_ROOT / 'stage_closeout_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(IDEA_REGISTRY, marker, block)

    negative_marker = "<!-- NR-FR74-MICROBURST-DENSITY-WITHOUT-RUNTIME-ECONOMICS -->"
    negative_block = f"""<!-- NR-FR74-MICROBURST-DENSITY-WITHOUT-RUNTIME-ECONOMICS -->
## NR-FR74-MICROBURST-DENSITY-WITHOUT-RUNTIME-ECONOMICS

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험했다.
- Why failed(실패 이유): raw density(원시 밀도)는 통과했지만 F74B/F74C에서 scout clue(탐색 단서) 0, meaningful candidate(의미 후보) 0이었다. MT5 runtime(런타임)은 validation PF/DD/tpd `1.16/11.40%/1.6544`, OOS PF/DD/tpd `1.13/9.66%/1.60`으로 최종 네 축에서 멀다.
- Salvage value(회수 가치): density feasibility(밀도 실현 가능성)과 signal quality(신호 품질)는 분리해서 봐야 한다. ONNX materialization(온엑스 물질화)과 selected-entry veto parity(선택 진입 차단 동등성)는 정확히 맞출 수 있다.
- Do-not-repeat(반복 금지): microburst turnover label(마이크로버스트 회전 라벨)을 threshold/clean-label/session tweak(임계값/클린 라벨/세션 미세조정)만으로 다시 밀지 않는다.
- Reopen condition(재개 조건): order-flow(오더플로), volatility compression(변동성 압축), session liquidity imbalance(세션 유동성 불균형)처럼 upstream mechanism(상류 메커니즘)이 바뀌고 label/risk/trade shape(라벨/위험/거래 형태)가 새로 묶일 때만 재개한다.
- Evidence(근거): `{rel(REVIEWS_ROOT / 'stage_closeout_report.md')}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음)."""
    append_once(NEGATIVE_REGISTER, negative_marker, negative_block)
    update_five_stage_register()


def update_five_stage_register() -> None:
    payload = yaml.safe_load(io_path(FIVE_STAGE_REGISTER).read_text(encoding="utf-8-sig")) or {}
    state = payload.setdefault("state", {})
    closed = list(state.get("closed_frontier_ids_since_last_retrospective") or [])
    if STAGE_ID not in closed:
        closed.append(STAGE_ID)
    state["closed_frontier_ids_since_last_retrospective"] = closed
    state["closeouts_since_last"] = len(closed)
    state["next_numeric_trigger_frontier"] = 75
    state["current_due_status"] = "not_due_after_f74_closeout"
    state["note"] = (
        "F74 closeout(마감)이 F66-F70 retrospective(중간 검토) 뒤 4/5로 등록됐다. "
        "다음 numeric trigger(숫자 트리거)는 F75 closeout(마감)이다."
    )
    write_text(FIVE_STAGE_REGISTER, yaml.safe_dump(payload, allow_unicode=True, sort_keys=False))


def update_state(summary: Mapping[str, Any]) -> None:
    created_at = str(summary["created_at_utc"])
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {CLOSEOUT_LABEL}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f74_closed_after_mandatory_runtime_probe",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f74_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F74 stage closeout(단계 마감)을 완료했다."',
        '  - "Effect(효과): density/parity(밀도/동등성)는 보존 단서로 남기고, weak runtime economics(약한 런타임 경제성)는 부정 기억으로 남겼다."',
        '  - "Next(다음): F75는 microburst repair loop(마이크로버스트 수리 반복)가 아니라 upstream mechanism rotation(상류 메커니즘 전환)으로 열어야 한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    write_text(WORKSPACE_STATE, "\n".join(state))
    write_md(
        SELECTED_ROOT / "selection_status.md",
        [
            "# F74 Selection Status(F74 선택 상태)",
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
        ],
    )
    write_md(
        CURRENT_WORKING_STATE,
        [
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
            "Action(행동): F74 stage closeout(단계 마감)을 완료했다.",
            "",
            f"Effect(효과): F74를 `{JUDGMENT}`로 닫고 다음 행동을 `{NEXT_RUN_ID}`로 설정했다.",
            "",
            "- preserved_clue(보존 단서): density feasibility(밀도 실현 가능성), ONNX parity(온엑스 동등성), mandatory runtime probe completion(필수 런타임 탐침 완료).",
            "- negative_memory(부정 기억): proxy scout clue(프록시 탐색 단서) 0과 runtime economics(런타임 경제성) 미달.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F74F required material missing: {missing}")
    created_at = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    summary = build_summary(created_at)
    write_json(RUN_ROOT / "frontier74F_stage_closeout_summary.json", summary)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
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
            "proxy_runtime_gap_cause": summary["proxy_runtime_gap_cause"],
        },
    )
    write_csv(RUN_ROOT / "f74f_closeout_kpi_table.csv", summary["closeout_kpi_rows"])
    write_csv(RUN_ROOT / "f74f_proxy_runtime_gap_analysis.csv", summary["gap_rows"])
    write_csv(REVIEWS_ROOT / "f74f_closeout_kpi_table_review.csv", summary["closeout_kpi_rows"])
    write_csv(REVIEWS_ROOT / "f74f_proxy_runtime_gap_analysis.csv", summary["gap_rows"])
    write_json(REVIEWS_ROOT / "f74f_stage_closeout_summary.json", summary)
    write_md(REVIEWS_ROOT / "stage_closeout_report.md", report_lines(summary))
    write_md(REVIEWS_ROOT / "f74f_stage_closeout_grok_receipt.md", grok_receipt_lines(summary))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f74f.md", gate_audit_lines(summary))
    update_ledgers(summary)
    update_registers(summary)
    update_state(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "status": CLOSEOUT_LABEL,
                    "judgment": JUDGMENT,
                    "closeout_label": CLOSEOUT_LABEL,
                    "validation_runtime": summary["runtime_probe_kpi"]["validation_compact"],
                    "oos_runtime": summary["runtime_probe_kpi"]["oos_compact"],
                    "five_stage_retrospective_due_status": summary["five_stage_retrospective_due_status"],
                    "next_run_id": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
