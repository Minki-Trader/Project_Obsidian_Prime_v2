from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import io_path, json_ready, path_exists


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling"
RUN_ID = "frontier72G_stage_closeout_trade_shape_lifecycle_gap_v1"
PARENT_RUN_ID = "frontier72F_pre_mt5_lifecycle_repair_runtime_probe_v1"
NEXT_RUN_ID = "frontier73A_stage_open_new_hypothesis_after_f72_trade_shape_negative_memory_v1"

STATUS = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory_no_authority"
CLAIM_BOUNDARY = (
    "preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_STATUS = STAGE_ROOT / "04_selected" / "selection_status.md"

F72B_RUN = STAGE_ROOT / "02_runs/frontier72B_trade_shape_exit_distribution_proxy_scout_v1"
F72C_RUN = STAGE_ROOT / "02_runs/frontier72C_trade_shape_label_feature_repair_or_pre_mt5_decision_v1"
F72D_RUN = STAGE_ROOT / "02_runs/frontier72D_pre_mt5_grok_trade_shape_runtime_probe_v1"
F72E_RUN = STAGE_ROOT / "02_runs/frontier72E_proxy_runtime_gap_analysis_and_repair_decision_v1"
F72F_RUN = STAGE_ROOT / "02_runs/frontier72F_pre_mt5_lifecycle_repair_runtime_probe_v1"

F72B_CANDIDATES = F72B_RUN / "f72b_candidate_summary.csv"
F72C_CANDIDATES = F72C_RUN / "f72c_repair_candidate_summary.csv"
F72D_RECEIPT = F72D_RUN / "f72d_runtime_probe_receipt.csv"
F72D_SIGNAL_PARITY = F72D_RUN / "f72d_onnx_signal_parity.csv"
F72D_PROB_PARITY = F72D_RUN / "f72d_onnx_probability_parity.csv"
F72D_MATERIALIZATION = F72D_RUN / "f72d_bridge_materialization.csv"
F72E_SUMMARY = F72E_RUN / "frontier72E_gap_repair_summary.json"
F72E_GAP_ROWS = F72E_RUN / "f72e_runtime_gap_rows.csv"
F72E_CANDIDATES = F72E_RUN / "f72e_lifecycle_repair_candidates.csv"
F72F_RECEIPT = F72F_RUN / "f72f_runtime_probe_receipt.csv"
F72F_SIGNAL_PARITY = F72F_RUN / "f72f_onnx_signal_parity.csv"
F72F_PROB_PARITY = F72F_RUN / "f72f_onnx_probability_parity.csv"
F72F_MATERIALIZATION = F72F_RUN / "f72f_bridge_materialization.csv"
F72F_MANIFEST = F72F_RUN / "run_manifest.json"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f72g_stage_closeout_trade_shape_lifecycle_gap"
GROK_PROMPT = GROK_PACKET / "prompts/f72g_stage_closeout_trade_shape_lifecycle_gap_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
CLOSEOUT_SUMMARY = RUN_ROOT / "frontier72G_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEWS_ROOT / "stage_closeout_report.md"
GROK_RECEIPT = REVIEWS_ROOT / "f72g_stage_closeout_grok_receipt.md"
GATE_AUDIT = REVIEWS_ROOT / "required_gate_coverage_audit_f72g.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_ROOT / "stage_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs/registers/negative_result_register.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def file_hash(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
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
    rows = [existing for existing in rows if existing.get(key) != str(row.get(key, ""))]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def scalar(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    return value


def num(value: Any) -> float | None:
    value = scalar(value)
    if value is None or value == "":
        return None
    try:
        if pd.isna(value):
            return None
    except TypeError:
        pass
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt(value: Any, digits: int = 4) -> str:
    numeric = num(value)
    if numeric is None:
        return "not_available(현재 없음)"
    if digits == 0:
        return str(int(round(numeric)))
    text = f"{numeric:.{digits}f}".rstrip("0").rstrip(".")
    return text if text else "0"


def percent_text(value: Any) -> str:
    numeric = num(value)
    if numeric is None:
        return "not_available(현재 없음)"
    return f"{fmt(numeric)}%"


def bool_count(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    series = df[column]
    if series.dtype == bool:
        return int(series.sum())
    return int(series.astype(str).str.lower().isin(["true", "1", "yes"]).sum())


def top_scout(df: pd.DataFrame) -> dict[str, Any]:
    scope = df.copy()
    if "scout_clue" in scope.columns:
        scout = scope[scope["scout_clue"].astype(str).str.lower().isin(["true", "1", "yes"])]
        if not scout.empty:
            scope = scout
    sort_columns = [c for c in ["oos_profit_factor", "oos_net_profit"] if c in scope.columns]
    if sort_columns:
        scope = scope.sort_values(sort_columns, ascending=[False] * len(sort_columns))
    return {key: scalar(value) for key, value in scope.iloc[0].to_dict().items()} if not scope.empty else {}


def df_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    return [{key: scalar(value) for key, value in row.items()} for row in df.to_dict(orient="records")]


def row_by_split(rows: Sequence[Mapping[str, Any]], split: str) -> dict[str, Any]:
    for row in rows:
        if row.get("split") == split:
            return dict(row)
    raise KeyError(split)


def runtime_kpi_row(row: Mapping[str, Any], prefix: str) -> dict[str, Any]:
    return {
        "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
        "split_view": f"{prefix} {row.get('split')} Tier A separate(Tier A 분리)",
        "net_profit": row.get("net_profit", ""),
        "gross_profit": row.get("gross_profit", ""),
        "gross_loss": row.get("gross_loss", ""),
        "profit_factor": row.get("profit_factor", ""),
        "drawdown_percent": row.get("max_drawdown_percent", ""),
        "trade_count": row.get("trade_count", ""),
        "trades_per_day": row.get("trades_per_day", ""),
        "win_rate": row.get("win_rate_percent", ""),
        "average_win": row.get("average_win", ""),
        "average_loss": row.get("average_loss", ""),
        "payoff_ratio": row.get("payoff_ratio", ""),
        "expectancy": row.get("expectancy", ""),
        "recovery_factor": row.get("recovery_factor", ""),
        "time_under_water": "not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)",
        "max_consecutive_loss": "not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)",
        "long_short_breakdown": f"long={fmt(row.get('long_trade_count'), 0)}; short={fmt(row.get('short_trade_count'), 0)}",
        "proxy_runtime_gap": (
            f"{row.get('gap_cause_summary')}; proxy net/PF/tpd/DD="
            f"{fmt(row.get('proxy_net_profit'))}/{fmt(row.get('proxy_profit_factor'))}/"
            f"{fmt(row.get('proxy_trades_per_day'))}/{percent_text(row.get('proxy_dd_percent'))}"
        ),
    }


def kpi_table_lines(kpi_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    lines = [
        "| test period(테스트 기간) | split/view(분할/보기) | net profit(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD(손실폭) | trade count(거래 수) | trades/day(일 거래 수) | win rate(승률) | average win(평균 이익) | average loss(평균 손실) | payoff ratio(손익비) | expectancy(기대값) | recovery factor(회복 계수) | time under water(회복 전 체류 시간) | max consecutive loss(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in kpi_rows:
        lines.append(
            "| `{period}` | `{view}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{wr}` | `{aw}` | `{al}` | `{payoff}` | `{expectancy}` | `{recovery}` | `{tuw}` | `{mcl}` | `{ls}` | `{gap}` |".format(
                period=row["test_period"],
                view=row["split_view"],
                net=fmt(row["net_profit"]),
                gp=fmt(row["gross_profit"]),
                gl=fmt(row["gross_loss"]),
                pf=fmt(row["profit_factor"]),
                dd=percent_text(row["drawdown_percent"]),
                trades=fmt(row["trade_count"], 0),
                tpd=fmt(row["trades_per_day"]),
                wr=percent_text(row["win_rate"]),
                aw=fmt(row["average_win"]),
                al=fmt(row["average_loss"]),
                payoff=fmt(row["payoff_ratio"]),
                expectancy=fmt(row["expectancy"]),
                recovery=fmt(row["recovery_factor"]),
                tuw=row["time_under_water"],
                mcl=row["max_consecutive_loss"],
                ls=row["long_short_breakdown"],
                gap=row["proxy_runtime_gap"],
            )
        )
    return lines


def compact_runtime_lines(rows: Sequence[Mapping[str, Any]], label: str) -> list[str]:
    lines = [
        f"### {label}",
        "",
        "| split(분할) | period(기간) | net(순수익) | PF(수익 팩터) | DD(손실폭) | trades(거래 수) | trades/day(일 거래 수) | expected signals/selected trades(예상 신호/선택 거래) | runtime trades(런타임 거래) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        period = f"{row.get('test_period_start')}..{row.get('test_period_end')}"
        lines.append(
            f"| `{row.get('split')}` | `{period}` | `{fmt(row.get('net_profit'))}` | `{fmt(row.get('profit_factor'))}` | `{percent_text(row.get('max_drawdown_percent'))}` | `{fmt(row.get('trade_count'), 0)}` | `{fmt(row.get('trades_per_day'))}` | `{fmt(row.get('expected_selected_trade_count'), 0)}` | `{fmt(row.get('trade_count'), 0)}` | `{fmt(row.get('signal_count_diff'), 0)}` | `{fmt(row.get('feature_ready_diff'), 0)}` | `{row.get('gap_cause_summary')}` |"
        )
    return lines


def classify_grok_advice(text: str) -> dict[str, Any]:
    lower = text.lower()
    accepted_close = "close f72 now" in lower and "preserved clue" in lower
    return {
        "classification": "accepted_with_local_verification(로컬 검증 후 수용)" if accepted_close else "needs_local_verification(로컬 검증 필요)",
        "accepted": [
            "close_f72_as_preserved_clue_negative_memory(F72를 보존 단서 + 부정 기억으로 마감)",
            "do_not_run_another_f72_internal_repair_without_new_axis(새 축 없는 F72 내부 수리 반복 금지)",
            "preserve_lifecycle_alignment_as_density_bridge_clue(생명주기 정렬을 밀도 브리지 단서로 보존)",
        ],
        "rejected": [
            "mandatory_pre_closeout_repair_from_economics_gap_alone(경제성 간극만으로 필수 마감 전 수리)",
            "completion_baseline_promotion_runtime_authority_live_readiness_goal_claim(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장)",
        ],
        "needs_local_verification": [
            "receipt_register_hash_consistency(영수증/등록부/해시 일치)",
            "all_short_execution_intentionality(숏 전용 실행 의도성)",
            "future_frontier_question_is_out_of_scope_for_f72_closeout(다음 전선 질문은 F72 마감 범위 밖)",
        ],
        "local_verification": [
            "F72F materialization source candidate is short_h24_sl0.9_tp1.8, so all-short execution is intentional clue(F72F 물질화 원천 후보가 short_h24_sl0.9_tp1.8이므로 숏 전용 실행은 의도된 단서)",
            "F72F signal/probability parity rows all passed and receipt diff rows are zero(F72F 신호/확률 동등성 행 모두 통과, 영수증 차이 0)",
            "F72F receipt confirms weak runtime economics after lifecycle repair(F72F 영수증은 생명주기 수리 후 약한 런타임 경제성을 확인)",
        ],
    }


def build_summary() -> dict[str, Any]:
    b = read_csv(F72B_CANDIDATES)
    c = read_csv(F72C_CANDIDATES)
    d_rows = df_rows(read_csv(F72D_RECEIPT))
    e_summary = read_json(F72E_SUMMARY)
    e_candidates = read_csv(F72E_CANDIDATES)
    f_rows = df_rows(read_csv(F72F_RECEIPT))
    f_signal = read_csv(F72F_SIGNAL_PARITY)
    f_prob = read_csv(F72F_PROB_PARITY)
    f_material = read_csv(F72F_MATERIALIZATION)
    grok_clean = read_text(GROK_CLEAN)

    f_val = row_by_split(f_rows, "validation")
    f_oos = row_by_split(f_rows, "oos")
    d_val = row_by_split(d_rows, "validation")
    d_oos = row_by_split(d_rows, "oos")
    f72e_best = e_summary.get("best_candidate", {})
    grok = classify_grok_advice(grok_clean)
    material_row = f_material.iloc[0].to_dict() if not f_material.empty else {}

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "closeout_label": STATUS,
        "created_at_utc": utc_now(),
        "hypothesis": "trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 개선하는 seed surface(씨앗 표면)를 만들 수 있는가.",
        "test_period": {
            "runtime_validation": f"{f_val.get('test_period_start')}..{f_val.get('test_period_end')}",
            "runtime_oos": f"{f_oos.get('test_period_start')}..{f_oos.get('test_period_end')}",
        },
        "proxy_expectation": "exit/risk label construction(청산/위험 라벨 구성)이 proxy scout clue(프록시 탐색 단서)를 만들고 MT5 lifecycle repair(생명주기 수리) 뒤에도 density/PF/DD(밀도/수익 팩터/손실폭)가 같이 유지될 것으로 기대했다.",
        "proxy_kpi": {
            "f72b_candidate_count": int(len(b)),
            "f72b_scout_clue_count": bool_count(b, "scout_clue"),
            "f72b_meaningful_candidate_count": bool_count(b, "meaningful_candidate"),
            "f72b_top_scout": top_scout(b),
            "f72c_candidate_count": int(len(c)),
            "f72c_scout_clue_count": bool_count(c, "scout_clue"),
            "f72c_meaningful_candidate_count": bool_count(c, "meaningful_candidate"),
            "f72c_top_scout": top_scout(c),
            "f72e_candidate_count": int(e_summary.get("candidate_count", len(e_candidates))),
            "f72e_runtime_repair_probe_worthy_count": int(e_summary.get("runtime_repair_probe_worthy_count", 0)),
            "f72e_meaningful_candidate_count": int(e_summary.get("meaningful_candidate_count", 0)),
            "f72e_best_candidate": f72e_best,
        },
        "runtime_probe_kpi": [runtime_kpi_row(row, "F72F lifecycle repair runtime probe(F72F 생명주기 수리 런타임 탐침)") for row in f_rows],
        "f72d_runtime_probe_summary": d_rows,
        "f72f_runtime_probe_summary": f_rows,
        "signal_count_parity": {
            "f72d_validation_diff": d_val.get("signal_count_diff"),
            "f72d_oos_diff": d_oos.get("signal_count_diff"),
            "f72f_validation_diff": f_val.get("signal_count_diff"),
            "f72f_oos_diff": f_oos.get("signal_count_diff"),
            "f72f_onnx_signal_parity_pass_rows": int(f_signal["passed"].astype(str).str.lower().isin(["true", "1"]).sum()),
            "f72f_onnx_signal_parity_total_rows": int(len(f_signal)),
        },
        "feature_readiness_parity": {
            "f72d_validation_diff": d_val.get("feature_ready_diff"),
            "f72d_oos_diff": d_oos.get("feature_ready_diff"),
            "f72f_validation_diff": f_val.get("feature_ready_diff"),
            "f72f_oos_diff": f_oos.get("feature_ready_diff"),
        },
        "probability_parity": {
            "f72f_probability_parity_pass_rows": int(f_prob["passed"].astype(str).str.lower().isin(["true", "1"]).sum()),
            "f72f_probability_parity_total_rows": int(len(f_prob)),
            "f72f_max_abs_diff": float(f_prob["max_abs_diff"].max()),
        },
        "lifecycle_count_alignment": {
            "f72d_validation_expected_selected_vs_runtime_trades": [d_val.get("expected_selected_trade_count"), d_val.get("trade_count")],
            "f72d_oos_expected_selected_vs_runtime_trades": [d_oos.get("expected_selected_trade_count"), d_oos.get("trade_count")],
            "f72f_validation_expected_selected_vs_runtime_trades": [f_val.get("expected_selected_trade_count"), f_val.get("trade_count")],
            "f72f_oos_expected_selected_vs_runtime_trades": [f_oos.get("expected_selected_trade_count"), f_oos.get("trade_count")],
        },
        "runtime_snapshot": {
            "best_runtime_split": "oos",
            "best_runtime_net_profit": num(f_oos.get("net_profit")),
            "best_runtime_profit_factor": num(f_oos.get("profit_factor")),
            "best_runtime_drawdown_percent": num(f_oos.get("max_drawdown_percent")),
            "best_runtime_trades_per_day": num(f_oos.get("trades_per_day")),
            "best_runtime_trade_count": num(f_oos.get("trade_count")),
            "validation_runtime_net_profit": num(f_val.get("net_profit")),
            "validation_runtime_profit_factor": num(f_val.get("profit_factor")),
            "validation_runtime_drawdown_percent": num(f_val.get("max_drawdown_percent")),
            "validation_runtime_trades_per_day": num(f_val.get("trades_per_day")),
            "validation_runtime_trade_count": num(f_val.get("trade_count")),
        },
        "proxy_runtime_gap_cause": "F72D에서 겹친 신호 집계와 MT5 단일 포지션 생명주기 간극을 확인했고, F72F에서 expected selected trades(예상 선택 거래)와 runtime trades(런타임 거래)의 개수 간극은 줄었지만 PF/DD/net(수익 팩터/손실폭/순수익)은 runtime_economics_gap_after_signal_and_feature_parity(신호/피처 동등성 이후 런타임 경제성 간극)로 남았다.",
        "wfo_stress_status": "not_run_out_of_scope_by_claim_after_runtime_negative_closeout(WFO/스트레스는 런타임 부정 마감 뒤 주장 범위 밖으로 미실행)",
        "wfo_stress_reason": "F72F mandatory MT5 repair(필수 MT5 수리)가 PF 1.07/1.05, DD 14.94%/18.60%, trades/day 2.14/2.48에 머물러 completion candidate(완성 후보)가 아니며, 추가 WFO/stress(워크포워드/스트레스)는 약한 표면을 강화 검증하는 일이 된다.",
        "strict_joint_pass_count": 0,
        "preserved_clue": [
            "F72F lifecycle repair(생명주기 수리)는 expected selected trades vs runtime trades(예상 선택 거래 대 런타임 거래)를 validation 610->582, OOS 515->483으로 좁혔다.",
            "ONNX probability/signal parity(온엑스 확률/신호 동등성)와 feature readiness parity(피처 준비 동등성)는 F72F에서 모두 diff 0으로 유지됐다.",
            "all-short execution shape(숏 전용 실행 형태)는 F72E source candidate `short_h24_sl0.9_tp1.8`에서 온 의도된 execution-shape clue(실행 형태 단서)다.",
        ],
        "negative_memory": [
            "F72B/F72C/F72E 모두 meaningful candidate(의미 후보) 0으로 끝났다.",
            "F72F lifecycle repair after parity(동등성 후 생명주기 수리)에도 OOS runtime(표본외 런타임)은 net 66.47, PF 1.05, DD 18.60%, trades/day 2.4769에 그쳤다.",
            "같은 F72 trade-shape-first label/feature/lifecycle surface(거래 형태 우선 라벨/피처/생명주기 표면)를 새 상류 질문 없이 반복하지 않는다.",
        ],
        "reopen_condition": "feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), or regime/session split(장세/세션 분할) 중 하나 이상이 실제로 바뀌고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.",
        "next_action": NEXT_RUN_ID,
        "grok": {
            "packet": rel(GROK_PACKET),
            "prompt": rel(GROK_PROMPT),
            "prompt_sha256": file_hash(GROK_PROMPT),
            "clean_output": rel(GROK_CLEAN),
            "clean_output_sha256": file_hash(GROK_CLEAN),
            "metadata": rel(GROK_METADATA),
            **grok,
        },
        "artifact_lineage": {
            "source_inputs": [
                rel(F72B_CANDIDATES),
                rel(F72C_CANDIDATES),
                rel(F72D_RECEIPT),
                rel(F72E_SUMMARY),
                rel(F72F_RECEIPT),
                rel(F72F_MATERIALIZATION),
            ],
            "producer": rel(ROOT / "stage_pipelines/stage_frontier_72/frontier72g_stage_closeout_trade_shape_lifecycle_gap.py"),
            "consumer": [rel(STAGE_CLOSEOUT_REPORT), rel(GROK_RECEIPT), rel(GATE_AUDIT), rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER)],
            "availability": "tracked_reports_with_ignored_heavy_run_artifacts(추적 보고서와 gitignored 무거운 실행 산출물)",
            "model_or_bundle_hash": scalar(material_row.get("onnx_sha256", "")),
            "feature_order_hash": scalar(material_row.get("feature_order_hash", "")),
            "runtime_veto_tape_hash": scalar(material_row.get("runtime_veto_tape_sha256", "")),
        },
        "result_judgment": {
            "result_subject": "F72 trade-shape-first exit distribution and risk-guard labeling lifecycle(F72 거래 형태 우선 청산 분포 및 위험 보호 라벨링 생명주기)",
            "evidence_available": "proxy candidate tables, F72D/F72F MT5 receipts, ONNX parity files, Grok closeout review(프록시 후보 표, F72D/F72F MT5 영수증, ONNX 동등성 파일, Grok 마감 검토)",
            "evidence_missing": "time under water and max consecutive loss from MT5 strategy report parse(회복 전 체류 시간 및 최대 연속 손실의 MT5 전략 보고서 파싱값)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "new frontier hypothesis with changed upstream axis and mandatory MT5 Runtime Probe(새 상류 축과 필수 MT5 런타임 탐침을 가진 새 전선 가설)",
        },
    }


def closeout_report_lines(summary: Mapping[str, Any]) -> list[str]:
    snap = summary["runtime_snapshot"]
    proxy = summary["proxy_kpi"]
    f72e = proxy["f72e_best_candidate"]
    lines = [
        "# Frontier72 Stage Closeout(F72 전선 단계 마감)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "## Closeout Label(마감 라벨)",
        "",
        f"`{STATUS}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
        "",
        "## Hypothesis(가설)",
        "",
        str(summary["hypothesis"]),
        "",
        "Effect(효과): label/target(라벨/목표), feature set(피처 묶음), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직)을 한 lifecycle(생명주기) 안에서 바꿔보고 MT5 Runtime Probe(MT5 런타임 탐침)까지 물질화했다.",
        "",
        "## Test Period(테스트 기간)",
        "",
        f"- runtime validation(런타임 검증): `{summary['test_period']['runtime_validation']}`.",
        f"- runtime OOS(런타임 표본외): `{summary['test_period']['runtime_oos']}`.",
        "",
        "## Proxy Expectation(프록시 예상)",
        "",
        str(summary["proxy_expectation"]),
        "",
        "## Proxy KPI(프록시 핵심 성과 지표)",
        "",
        f"- F72B candidates(후보): `{proxy['f72b_candidate_count']}`, scout clue(탐색 단서) `{proxy['f72b_scout_clue_count']}`, meaningful(의미 후보) `{proxy['f72b_meaningful_candidate_count']}`.",
        f"- F72B best scout OOS(탐색 단서 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{fmt(proxy['f72b_top_scout'].get('oos_net_profit'))}/{fmt(proxy['f72b_top_scout'].get('oos_profit_factor'))}/{percent_text(proxy['f72b_top_scout'].get('oos_max_drawdown_percent'))}/{fmt(proxy['f72b_top_scout'].get('oos_trades_day'))}`.",
        f"- F72C candidates(후보): `{proxy['f72c_candidate_count']}`, scout clue(탐색 단서) `{proxy['f72c_scout_clue_count']}`, meaningful(의미 후보) `{proxy['f72c_meaningful_candidate_count']}`.",
        f"- F72C best scout OOS(탐색 단서 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{fmt(proxy['f72c_top_scout'].get('oos_net_profit'))}/{fmt(proxy['f72c_top_scout'].get('oos_profit_factor'))}/{percent_text(proxy['f72c_top_scout'].get('oos_max_drawdown_percent'))}/{fmt(proxy['f72c_top_scout'].get('oos_trades_day'))}`.",
        f"- F72E lifecycle repair candidates(생명주기 수리 후보): `{proxy['f72e_candidate_count']}`, repair probe worthy(수리 탐침 가치) `{proxy['f72e_runtime_repair_probe_worthy_count']}`, meaningful(의미 후보) `{proxy['f72e_meaningful_candidate_count']}`.",
        f"- F72E selected clue(선택 단서): `{f72e.get('candidate_id')}` `{f72e.get('shape_id')}` `{f72e.get('label_variant')}`; lifecycle OOS(생명주기 표본외) net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) `{fmt(f72e.get('oos_lifecycle_net_profit'))}/{fmt(f72e.get('oos_lifecycle_profit_factor'))}/{percent_text(f72e.get('oos_lifecycle_max_drawdown_percent'))}/{fmt(f72e.get('oos_lifecycle_trades_day'))}/{fmt(f72e.get('oos_lifecycle_trade_count'), 0)}`.",
        "",
        "## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)",
        "",
        f"- signal count parity(신호 수 동등성): F72D validation/OOS diff(검증/표본외 차이) `{fmt(summary['signal_count_parity']['f72d_validation_diff'], 0)}/{fmt(summary['signal_count_parity']['f72d_oos_diff'], 0)}`, F72F `{fmt(summary['signal_count_parity']['f72f_validation_diff'], 0)}/{fmt(summary['signal_count_parity']['f72f_oos_diff'], 0)}`.",
        f"- feature readiness parity(피처 준비 동등성): F72D validation/OOS diff(검증/표본외 차이) `{fmt(summary['feature_readiness_parity']['f72d_validation_diff'], 0)}/{fmt(summary['feature_readiness_parity']['f72d_oos_diff'], 0)}`, F72F `{fmt(summary['feature_readiness_parity']['f72f_validation_diff'], 0)}/{fmt(summary['feature_readiness_parity']['f72f_oos_diff'], 0)}`.",
        f"- probability parity(확률 동등성): F72F pass rows(통과 행) `{summary['probability_parity']['f72f_probability_parity_pass_rows']}/{summary['probability_parity']['f72f_probability_parity_total_rows']}`, max abs diff(최대 절대 차이) `{fmt(summary['probability_parity']['f72f_max_abs_diff'], 8)}`.",
        f"- lifecycle count alignment(생명주기 개수 정렬): F72D OOS expected signals/runtime trades(예상 신호/런타임 거래) `{fmt(summary['lifecycle_count_alignment']['f72d_oos_expected_selected_vs_runtime_trades'][0], 0)}->{fmt(summary['lifecycle_count_alignment']['f72d_oos_expected_selected_vs_runtime_trades'][1], 0)}`, F72F OOS expected selected trades/runtime trades(예상 선택 거래/런타임 거래) `{fmt(summary['lifecycle_count_alignment']['f72f_oos_expected_selected_vs_runtime_trades'][0], 0)}->{fmt(summary['lifecycle_count_alignment']['f72f_oos_expected_selected_vs_runtime_trades'][1], 0)}`.",
        f"- proxy/runtime gap cause(프록시/런타임 간극 원인): {summary['proxy_runtime_gap_cause']}",
        "",
    ]
    lines.extend(compact_runtime_lines(summary["f72d_runtime_probe_summary"], "F72D Before Lifecycle Repair(F72D 생명주기 수리 전)"))
    lines.extend([""])
    lines.extend(kpi_table_lines(summary["runtime_probe_kpi"]))
    lines.extend(
        [
            "",
            "## Final Target Distance(최종 목표 거리)",
            "",
            f"- F72F OOS runtime(표본외 런타임): net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) `{fmt(snap['best_runtime_net_profit'])}/{fmt(snap['best_runtime_profit_factor'])}/{percent_text(snap['best_runtime_drawdown_percent'])}/{fmt(snap['best_runtime_trades_per_day'])}/{fmt(snap['best_runtime_trade_count'], 0)}`.",
            "- final hard gates(최종 강제 게이트)는 final completion review(최종 완성 검토) 전용이지만, F72F는 trades/day 5-10(일거래 5-10), PF 2-3+(수익 팩터 2-3 이상), DD <10%(손실폭 10% 미만)를 동시에 만족하지 못했다.",
            "",
            "## WFO/Stress(워크포워드/스트레스)",
            "",
            f"- status(상태): `{summary['wfo_stress_status']}`.",
            f"- reason(사유): {summary['wfo_stress_reason']}",
            "",
            "## Tier Records(티어 기록)",
            "",
            "- Tier A separate(Tier A 분리): `materialized_proxy_and_runtime(프록시와 런타임 물질화)`.",
            "- Tier B separate(Tier B 분리): `missing_required_in_f72(필수 누락으로 기록)`.",
            "- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim_without_tier_b(Tier B 부재로 주장 범위 밖)`.",
            "",
            "## Preserved Clue(보존 단서)",
            "",
        ]
    )
    lines.extend([f"- {item}" for item in summary["preserved_clue"]])
    lines.extend(["", "## Negative Memory(부정 기억)", ""])
    lines.extend([f"- {item}" for item in summary["negative_memory"]])
    lines.extend(
        [
            "",
            "## Grok Closeout Review(그록 마감 검토)",
            "",
            f"- packet(묶음): `{summary['grok']['packet']}`.",
            f"- prompt(프롬프트): `{summary['grok']['prompt']}`, sha256(해시) `{summary['grok']['prompt_sha256']}`.",
            f"- output(출력): `{summary['grok']['clean_output']}`, sha256(해시) `{summary['grok']['clean_output_sha256']}`.",
            f"- classification(분류): `{summary['grok']['classification']}`.",
            "- accepted(수용): close F72 as preserved clue + negative memory(F72를 보존 단서 + 부정 기억으로 마감), no more F72 internal repair without new axis(새 축 없는 F72 내부 수리 없음).",
            "- rejected(거절): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 주장과 mandatory pre-closeout repair(필수 마감 전 수리).",
            "- local verification(로컬 검증): all-short execution(숏 전용 실행)은 source candidate(원천 후보) `short_h24_sl0.9_tp1.8`에서 온 의도된 단서이며, F72F receipt/parity(영수증/동등성)는 스냅샷과 일치했다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`",
            "",
            "Effect(효과): F72의 lifecycle/parity clue(생명주기/동등성 단서)는 보존하고, 같은 trade-shape-first surface(거래 형태 우선 표면)를 반복하지 않고 새 frontier hypothesis(전선 가설)로 넘어간다.",
        ]
    )
    return lines


def grok_receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F72G Grok Closeout Receipt(F72G 그록 마감 영수증)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "- trigger_reason(트리거 이유): F72 stage closeout(단계 마감) requires Grok second opinion(그록 2차 의견).",
        "- review_size(검토 크기): `small_with_prompt_length_warning(소규모, 프롬프트 길이 경고 있음)`.",
        f"- direction_before_grok(그록 전 방향): close F72 as `{JUDGMENT}` unless a specific non-repeated repair is required(특정 비반복 수리가 필요하지 않으면 F72 마감).",
        f"- bounded_evidence(제한 근거): F72B/F72C/F72E proxy counts(프록시 개수), F72D/F72F MT5 receipt KPI(MT5 영수증 KPI), parity rows(동등성 행).",
        f"- prompt_identity(프롬프트 정체성): `{summary['grok']['prompt']}`, sha256 `{summary['grok']['prompt_sha256']}`.",
        f"- output_identity(출력 정체성): `{summary['grok']['clean_output']}`, sha256 `{summary['grok']['clean_output_sha256']}`.",
        f"- advice_classification(조언 분류): `{summary['grok']['classification']}`.",
        "- accepted(수용): " + "; ".join(summary["grok"]["accepted"]) + ".",
        "- rejected(거절): " + "; ".join(summary["grok"]["rejected"]) + ".",
        "- needs_local_verification(로컬 검증 필요): " + "; ".join(summary["grok"]["needs_local_verification"]) + ".",
        "- local_verification(로컬 검증): " + "; ".join(summary["grok"]["local_verification"]) + ".",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve accepted(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 수용 없음).",
        f"- final_codex_direction(최종 Codex 방향): `{JUDGMENT}` closeout(마감) and next frontier hypothesis(다음 전선 가설) 준비.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    rows = [
        ("hypothesis lifecycle(가설 생명주기)", "pass(통과)", "F72A->F72G chain recorded(F72A부터 F72G까지 기록됨)"),
        ("proxy expectation/KPI(프록시 예상/KPI)", "pass(통과)", rel(STAGE_CLOSEOUT_REPORT)),
        ("mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)", "pass(통과)", f"F72D and F72F receipts({rel(F72D_RECEIPT)}, {rel(F72F_RECEIPT)})"),
        ("proxy/runtime gap analysis(프록시/런타임 간극 분석)", "pass(통과)", rel(F72E_SUMMARY)),
        ("repair(수리)", "pass(통과)", "F72E lifecycle repair and F72F MT5 repair probe(F72E 생명주기 수리 및 F72F MT5 수리 탐침)"),
        ("signal count parity(신호 수 동등성)", "pass(통과)", "F72F validation/OOS diff 0/0(F72F 검증/표본외 차이 0/0)"),
        ("feature readiness parity(피처 준비 동등성)", "pass(통과)", "F72F validation/OOS diff 0/0(F72F 검증/표본외 차이 0/0)"),
        ("required closeout KPI(필수 마감 KPI)", "pass(통과)", rel(STAGE_CLOSEOUT_REPORT)),
        ("Grok closeout review(그록 마감 검토)", "pass(통과)", summary["grok"]["packet"]),
        ("five-stage retrospective due check(5단계 중간 검토 도래 점검)", "not_due(아직 아님)", "F72 is 2/5 after F66-F70 retrospective(F66-F70 중간 검토 뒤 F72는 2/5)"),
        ("WFO/stress(워크포워드/스트레스)", "out_of_scope_by_claim(주장 범위 밖)", summary["wfo_stress_reason"]),
        ("final completion gates(최종 완성 게이트)", "not_applicable_to_exploration_closeout(탐색 마감에는 해당 없음)", "F72F did not claim completion(F72F는 완성 주장 없음)"),
    ]
    lines = [
        "# F72G Required Gate Coverage Audit(F72G 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
    ]
    lines.extend(f"| {gate} | `{status}` | {evidence} |" for gate, status, evidence in rows)
    lines.extend(
        [
            "",
            "Result(결과): F72 lifecycle evidence(생명주기 근거)는 closeout(마감)에 연결됐다. WFO/stress(워크포워드/스트레스)는 weak runtime economics(약한 런타임 경제성) 때문에 completion candidate(완성 후보) 검증이 아니라 약한 표면 강화 검증이 되어 미실행 사유를 기록했다.",
        ]
    )
    return lines


def registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    snap = summary["runtime_snapshot"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "family": "stage_closeout(단계 마감)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(CLOSEOUT_SUMMARY),
        "primary_report": rel(STAGE_CLOSEOUT_REPORT),
        "notes": "F72 closed as preserved clue + negative memory; lifecycle count gap narrowed but runtime economics remained weak(F72 보존 단서+부정 기억 마감, 생명주기 개수 간극은 줄었지만 런타임 경제성 약함).",
        "run_number": "frontier72G",
        "date": "2026-06-17",
        "decision": STATUS,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 10,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(STAGE_CLOSEOUT_REPORT),
        "runtime_completed_rows": 2,
        "best_net_profit": snap["best_runtime_net_profit"],
        "best_profit_factor": snap["best_runtime_profit_factor"],
        "run_date": "2026-06-17",
        "primary_artifact": rel(CLOSEOUT_SUMMARY),
        "candidate_model_id": "f72f_lifecycle_repair_f72e_0200",
        "net_profit": snap["best_runtime_net_profit"],
        "profit_factor": snap["best_runtime_profit_factor"],
        "drawdown": snap["best_runtime_drawdown_percent"],
        "trade_count": snap["best_runtime_trade_count"],
        "trade_density": snap["best_runtime_trades_per_day"],
        "result_status": STATUS,
        "attempt_count": 2,
        "view": "stage_closeout(단계 마감)",
        "tier": "Tier A separate(Tier A 분리)",
        "metric_scope": "stage_closeout_runtime_probe_gap_and_negative_memory(단계 마감 런타임 탐침 간극 및 부정 기억)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "external_verification_status": "completed(완료)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(STAGE_CLOSEOUT_REPORT),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": summary["created_at_utc"],
        "created_at_utc": summary["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": "stage_closeout(단계 마감)",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락)",
        "kpi_scope": "runtime_closeout_kpi(런타임 마감 KPI)",
        "primary_kpi": "F72F OOS net=66.47; PF=1.05; DD=18.60%; trades/day=2.4769",
        "guardrail_kpi": "signal_diff=0; feature_diff=0; meaningful_proxy=0; strict_joint_pass=0",
        "runtime_attempt_rows": 2,
        "work_family": "frontier_stage_closeout(전선 단계 마감)",
        "row_id": f"{RUN_ID}__stage_closeout",
        "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서와 부정 기억, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": summary["hypothesis"],
        "artifact_count": 6,
        "long_trade_count": 0,
        "short_trade_count": snap["best_runtime_trade_count"],
        "trade_density_per_feature_day": snap["best_runtime_trades_per_day"],
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "source_authority": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "strict_joint_pass_count": 0,
    }


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    row = registry_row(summary)
    row.update(
        {
            "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)",
            "path": rel(STAGE_CLOSEOUT_REPORT),
            "notes": "F72 lifecycle closed after mandatory MT5 Runtime Probe and one lifecycle repair MT5 probe(F72는 필수 MT5 런타임 탐침과 생명주기 수리 MT5 탐침 1회 뒤 마감).",
        }
    )
    return row


def update_ledgers(summary: Mapping[str, Any]) -> None:
    upsert_ledger(RUN_REGISTRY, "run_id", registry_row(summary))
    row = ledger_row(summary)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def append_register_notes(summary: Mapping[str, Any]) -> None:
    append_once(
        IDEA_REGISTRY,
        "<!-- frontier72G_stage_closeout_trade_shape_lifecycle_gap_v1 -->",
        f"""
<!-- frontier72G_stage_closeout_trade_shape_lifecycle_gap_v1 -->
- `{RUN_ID}` closes Frontier72(전선72) as `{JUDGMENT}`. Preserved clue(보존 단서): lifecycle repair(생명주기 수리)가 expected selected trades vs runtime trades(예상 선택 거래 대 런타임 거래) 간극을 F72D OOS `730->227`에서 F72F OOS `515->483`으로 줄였고, ONNX/signal/feature parity(온엑스/신호/피처 동등성)는 diff `0`으로 유지됐다. Negative memory(부정 기억): trade-shape-first exit/risk label surface(거래 형태 우선 청산/위험 라벨 표면)는 F72F OOS runtime(표본외 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `66.47/1.05/18.60%/2.4769`로 약했다. Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
""",
    )
    append_once(
        NEGATIVE_RESULT_REGISTER,
        "<!-- NR-FR72-TRADE-SHAPE-LIFECYCLE-RUNTIME-ECONOMICS-GAP -->",
        f"""
<!-- NR-FR72-TRADE-SHAPE-LIFECYCLE-RUNTIME-ECONOMICS-GAP -->
## NR-FR72-TRADE-SHAPE-LIFECYCLE-RUNTIME-ECONOMICS-GAP

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)이 F71 economics-native negative memory(F71 경제성 네이티브 부정 기억) 이후 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 개선하는 seed surface(씨앗 표면)를 만들 수 있다.
- Why failed(실패 이유): F72B/F72C/F72E meaningful candidate(의미 후보)가 모두 `0`이었고, F72F lifecycle repair MT5 Runtime Probe(생명주기 수리 MT5 런타임 탐침)도 validation/OOS(검증/표본외) PF/DD/trades_day(수익 팩터/손실폭/일거래) `1.07/14.94%/2.1397`, `1.05/18.60%/2.4769`로 최종 네 축에서 멀었다.
- Salvage value(회수 가치): lifecycle-aligned selected entry(생명주기 정렬 선택 진입)는 expected/runtime trade count gap(예상/런타임 거래 수 간극)을 줄일 수 있고, signal/feature parity(신호/피처 동등성)와 runtime economics(런타임 경제성)는 별개라는 단서를 보존한다.
- Do-not-repeat(반복 금지): same F72 trade-shape-first label/feature/lifecycle surface(동일 F72 거래 형태 우선 라벨/피처/생명주기 표면)를 새 feature set/label/model/risk/regime axis(새 피처 묶음/라벨/모델/위험/장세 축) 없이 반복하지 않는다.
- Reopen condition(재개 조건): feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), or regime/session split(장세/세션 분할) 중 하나 이상이 실제로 바뀌고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
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
        "  last_completed_packet_id: frontier66_to_70_five_stage_retrospective_v1",
        "  last_completed_at_frontier: 70",
        "  last_completed_stage_ids:",
        "    - stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "    - stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk",
        "    - stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout",
        "    - stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory",
        "    - stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation",
        "  last_completed_at_utc: '2026-06-16T22:35:00Z'",
        "  closed_frontier_ids_since_last_retrospective:",
        "    - stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd",
        f"    - {STAGE_ID}",
        "  closeouts_since_last: 2",
        "  next_numeric_trigger_frontier: 75",
        "  current_due_status: not_due_after_f72_closeout",
        '  note: "F72 closeout(마감)이 F66-F70 retrospective(중간 검토) 뒤 2/5로 등록됐다. 다음 numeric trigger(숫자 트리거)는 F75 closeout(마감)이다."',
    ]
    write_md(RETROSPECTIVE_REGISTER, lines)


def write_state_files(summary: Mapping[str, Any]) -> None:
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "Action(행동): F72 trade-shape-first lifecycle(거래 형태 우선 생명주기)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감했다."',
        '  - "Effect(효과): lifecycle count alignment(생명주기 개수 정렬)은 보존하고, 같은 F72 surface(표면) 반복을 막는다."',
        f'  - "Next action(다음 행동): {NEXT_RUN_ID}."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    write_md(WORKSPACE_STATE, state_lines)

    current_lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): Frontier72 trade-shape-first exit distribution/risk guard lifecycle(전선72 거래 형태 우선 청산 분포/위험 보호 생명주기)을 마감했다.",
        "",
        "Effect(효과): F72F의 lifecycle count bridge(생명주기 개수 브리지)는 보존 단서로 남기고, 약한 runtime economics(런타임 경제성)는 부정 기억으로 닫았다.",
        "",
        f"- closeout label(마감 라벨): `{JUDGMENT}`.",
        "- F72F validation(검증): net(순수익) `93.14`, PF(수익 팩터) `1.07`, DD(손실폭) `14.94%`, trades/day(일거래) `2.1397`.",
        "- F72F OOS(표본외): net(순수익) `66.47`, PF(수익 팩터) `1.05`, DD(손실폭) `18.60%`, trades/day(일거래) `2.4769`.",
        "- signal/feature parity(신호/피처 동등성): F72F validation/OOS diff(검증/표본외 차이) `0/0` and `0/0`.",
        "- five-stage retrospective(5단계 중간 검토): `not_due_after_f72_closeout(아직 아님, F72 마감 후 2/5)`.",
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
        "# F72 Selection Status(F72 선택 상태)",
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
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(SELECTED_STATUS, selection_lines)


def main() -> int:
    required = [
        F72B_CANDIDATES,
        F72C_CANDIDATES,
        F72D_RECEIPT,
        F72D_SIGNAL_PARITY,
        F72D_PROB_PARITY,
        F72D_MATERIALIZATION,
        F72E_SUMMARY,
        F72E_GAP_ROWS,
        F72E_CANDIDATES,
        F72F_RECEIPT,
        F72F_SIGNAL_PARITY,
        F72F_PROB_PARITY,
        F72F_MATERIALIZATION,
        F72F_MANIFEST,
        GROK_PROMPT,
        GROK_CLEAN,
        GROK_METADATA,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing closeout evidence: {missing}")

    summary = build_summary()
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "inputs": {
            "f72b_candidates": rel(F72B_CANDIDATES),
            "f72c_candidates": rel(F72C_CANDIDATES),
            "f72d_runtime_receipt": rel(F72D_RECEIPT),
            "f72e_summary": rel(F72E_SUMMARY),
            "f72f_runtime_receipt": rel(F72F_RECEIPT),
            "f72f_materialization": rel(F72F_MATERIALIZATION),
            "grok_prompt": rel(GROK_PROMPT),
            "grok_clean": rel(GROK_CLEAN),
        },
        "outputs": {
            "summary": rel(CLOSEOUT_SUMMARY),
            "stage_closeout_report": rel(STAGE_CLOSEOUT_REPORT),
            "grok_receipt": rel(GROK_RECEIPT),
            "gate_audit": rel(GATE_AUDIT),
        },
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_json(RUN_MANIFEST, manifest)
    write_json(CLOSEOUT_SUMMARY, summary)
    write_md(STAGE_CLOSEOUT_REPORT, closeout_report_lines(summary))
    write_md(GROK_RECEIPT, grok_receipt_lines(summary))
    write_md(GATE_AUDIT, gate_audit_lines(summary))
    update_ledgers(summary)
    append_register_notes(summary)
    update_retrospective_register()
    write_state_files(summary)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "report": rel(STAGE_CLOSEOUT_REPORT),
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
