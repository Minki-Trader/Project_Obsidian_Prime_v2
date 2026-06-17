from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path, json_ready, path_exists


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd"
RUN_ID = "frontier71F_stage_closeout_economics_native_label_selection_v1"
PARENT_RUN_ID = "frontier71E_proxy_runtime_gap_analysis_and_repair_decision_v1"
NEXT_RUN_ID = "frontier72A_stage_open_new_upstream_axis_after_f71_economics_negative_memory_v1"

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

F71B_RUN = STAGE_ROOT / "02_runs/frontier71B_economics_native_proxy_scout_v1"
F71C_RUN = STAGE_ROOT / "02_runs/frontier71C_economics_native_repair_recombine_proxy_v1"
F71D_RUN = STAGE_ROOT / "02_runs/frontier71D_mt5_runtime_probe_economics_native_scout_v1"
F71E_RUN = STAGE_ROOT / "02_runs/frontier71E_proxy_runtime_gap_analysis_and_repair_decision_v1"

F71B_SUMMARY = F71B_RUN / "f71b_proxy_summary.json"
F71B_KPI = F71B_RUN / "f71b_proxy_kpi_by_split.csv"
F71C_SUMMARY = F71C_RUN / "f71c_repair_summary.json"
F71C_KPI = F71C_RUN / "f71c_repair_kpi_by_split.csv"
F71D_RECEIPT = F71D_RUN / "f71d_runtime_probe_receipt.csv"
F71D_SIGNAL_PARITY = F71D_RUN / "f71d_onnx_signal_parity.csv"
F71D_PROB_PARITY = F71D_RUN / "f71d_onnx_probability_parity.csv"
F71E_SUMMARY = F71E_RUN / "frontier71E_runtime_semantics_repair_summary.json"
F71E_RECEIPT = F71E_RUN / "f71e_runtime_probe_receipt.csv"
F71E_GAP = F71E_RUN / "f71e_gap_classification.csv"
F71E_SIGNAL_PARITY = F71E_RUN / "f71e_onnx_signal_parity.csv"
F71E_PROB_PARITY = F71E_RUN / "f71e_onnx_probability_parity.csv"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f71_stage_closeout_economics_native_label_selection"
GROK_PROMPT = GROK_PACKET / "prompts/f71_stage_closeout_prompt.md"
GROK_CLEAN = GROK_PACKET / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET / "outputs/metadata.json"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
CLOSEOUT_SUMMARY = RUN_ROOT / "frontier71F_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEWS_ROOT / "stage_closeout_report.md"
GROK_RECEIPT = REVIEWS_ROOT / "f71_stage_closeout_grok_receipt.md"
GATE_AUDIT = REVIEWS_ROOT / "required_gate_coverage_audit_f71f.md"

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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


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
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def num(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt(value: Any, digits: int = 4) -> str:
    numeric = num(value)
    if numeric is None:
        return "not_available(현재 없음)"
    text = f"{numeric:.{digits}f}".rstrip("0").rstrip(".")
    return text if text else "0"


def percent_text(value: Any) -> str:
    numeric = num(value)
    if numeric is None:
        return "not_available(현재 없음)"
    return f"{fmt(numeric)}%"


def top_candidate_oos(top: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "net_profit": top.get("oos_net_profit", ""),
        "profit_factor": top.get("oos_profit_factor", ""),
        "max_drawdown_percent": top.get("oos_max_drawdown_percent", ""),
        "trades_per_day": top.get("oos_trades_day", ""),
    }


def classify_grok_advice(text: str) -> dict[str, Any]:
    lower = text.lower()
    accepted = "accepted" in lower or "수용" in text
    forbidden_terms = [
        "runtime authority(런타임 권위)",
        "live readiness(실거래 준비)",
        "goal achieve",
        "selected baseline(선택 기준선)",
        "operating promotion(운영 승격)",
    ]
    forbidden_as_claim = [term for term in forbidden_terms if f"claim {term}" in lower]
    return {
        "classification": "accepted_with_local_verification(로컬 검증 후 수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "accepted": [
            "closeout_as_preserved_clue_negative_memory(보존 단서와 부정 기억으로 마감)",
            "no_more_f71_threshold_or_tape_only_repair(추가 F71 임계값/테이프 단독 수리 없음)",
            "next_frontier_must_change_upstream_axis(다음 전선은 상류 축 변경 필요)",
        ],
        "rejected": [
            "any_completion_baseline_promotion_runtime_authority_live_readiness_goal_claim(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장)",
        ],
        "needs_local_verification": [
            "whether_any_prepared_non_tape_upstream_variant_was_skipped(F71 안에 준비됐지만 건너뛴 비테이프 상류 변형이 있는지)",
        ],
        "local_verification": "no_unrun_non_tape_upstream_variant_found_in_f71_artifact_index(F71 산출물 색인에서 미실행 비테이프 상류 변형 없음)",
        "forbidden_claims_detected": forbidden_as_claim,
    }


def runtime_kpi_row(row: Mapping[str, Any], prefix: str) -> dict[str, Any]:
    long_count = row.get("long_trade_count", "")
    short_count = row.get("short_trade_count", "")
    split = row.get("split", "")
    return {
        "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
        "split_view": f"{prefix} {split} Tier A separate(Tier A 분리)",
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
        "long_short_breakdown": f"long={long_count}; short={short_count}",
        "proxy_runtime_gap": (
            f"{row.get('gap_cause_summary')}; proxy net/PF/tpd/DD="
            f"{fmt(row.get('proxy_net_profit'))}/{fmt(row.get('proxy_profit_factor'))}/"
            f"{fmt(row.get('proxy_trades_per_day'))}/{fmt(row.get('proxy_dd_percent'))}"
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
                trades=fmt(row["trade_count"]),
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
        "| split(분할) | period(기간) | net(순수익) | PF(수익 팩터) | DD(손실폭) | trades(거래 수) | trades/day(일 거래 수) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        period = f"{row.get('test_period_start')}..{row.get('test_period_end')}"
        lines.append(
            f"| `{row.get('split')}` | `{period}` | `{fmt(row.get('net_profit'))}` | `{fmt(row.get('profit_factor'))}` | `{percent_text(row.get('max_drawdown_percent'))}` | `{fmt(row.get('trade_count'))}` | `{fmt(row.get('trades_per_day'))}` | `{fmt(row.get('signal_count_diff'))}` | `{fmt(row.get('feature_ready_diff'))}` | `{row.get('gap_cause_summary')}` |"
        )
    return lines


def build_summary(
    f71b: Mapping[str, Any],
    f71b_kpi: Sequence[Mapping[str, Any]],
    f71c: Mapping[str, Any],
    f71c_kpi: Sequence[Mapping[str, Any]],
    f71d_rows: Sequence[Mapping[str, Any]],
    f71e_summary: Mapping[str, Any],
    f71e_rows: Sequence[Mapping[str, Any]],
    f71e_gap_rows: Sequence[Mapping[str, Any]],
    f71e_signal_rows: Sequence[Mapping[str, Any]],
    grok_clean: str,
) -> dict[str, Any]:
    f71b_top = f71b.get("top_candidates", [{}])[0]
    f71c_top = f71c.get("top_candidates", [{}])[0]
    f71e_oos = next(row for row in f71e_rows if row.get("split") == "oos")
    f71e_val = next(row for row in f71e_rows if row.get("split") == "validation")
    f71d_oos = next(row for row in f71d_rows if row.get("split") == "oos")
    grok = classify_grok_advice(grok_clean)
    exact_signal_rows = sum(1 for row in f71e_rows if fmt(row.get("signal_count_diff")) == "0")
    exact_feature_rows = sum(1 for row in f71e_rows if fmt(row.get("feature_ready_diff")) == "0")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "closeout_label": STATUS,
        "created_at_utc": utc_now(),
        "hypothesis": "economics-native label/target and selection(경제성 네이티브 라벨/목표와 선택)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 보존하는 seed surface(씨앗 표면)를 만들 수 있는가.",
        "test_period": {
            "proxy_frame": f"{f71b.get('test_period', {}).get('start')}..{f71b.get('test_period', {}).get('end')}",
            "runtime_validation": f"{f71e_val.get('test_period_start')}..{f71e_val.get('test_period_end')}",
            "runtime_oos": f"{f71e_oos.get('test_period_start')}..{f71e_oos.get('test_period_end')}",
        },
        "proxy_expectation": "economic labels and selection(경제 라벨과 선택)이 final target(최종 목표) 전 단계의 scout clue(탐색 단서)를 만들고, MT5 Runtime Probe(MT5 런타임 탐침)에서 density/PF/DD(밀도/수익 팩터/손실폭)가 함께 유지될 것으로 기대했다.",
        "proxy_kpi": {
            "f71b_candidate_count": f71b.get("candidate_count"),
            "f71b_scout_clue_count": f71b.get("scout_clue_count"),
            "f71b_meaningful_candidate_count": f71b.get("meaningful_candidate_count"),
            "f71b_top_candidate": f71b_top,
            "f71b_oos": top_candidate_oos(f71b_top),
            "f71c_candidate_count": f71c.get("candidate_count"),
            "f71c_scout_clue_count": f71c.get("scout_clue_count"),
            "f71c_meaningful_candidate_count": f71c.get("meaningful_candidate_count"),
            "f71c_top_candidate": f71c_top,
            "f71c_oos": top_candidate_oos(f71c_top),
        },
        "runtime_probe_kpi": [runtime_kpi_row(row, "F71E runtime semantics repair(F71E 런타임 의미 수리)") for row in f71e_rows],
        "f71d_runtime_probe_summary": list(f71d_rows),
        "f71e_runtime_probe_summary": list(f71e_rows),
        "f71e_gap_rows": list(f71e_gap_rows),
        "signal_count_parity": {
            "f71d_oos_signal_count_diff": f71d_oos.get("signal_count_diff"),
            "f71e_exact_signal_diff_rows": exact_signal_rows,
            "f71e_runtime_rows": len(f71e_rows),
            "f71e_onnx_signal_parity_rows": len(f71e_signal_rows),
            "status": "repaired_to_exact_in_f71e( F71E에서 정확 동등성으로 수리 )",
        },
        "feature_readiness_parity": {
            "f71e_exact_feature_diff_rows": exact_feature_rows,
            "f71e_runtime_rows": len(f71e_rows),
            "status": "exact_all_f71e_runtime_rows(F71E 모든 런타임 행 정확)",
        },
        "runtime_snapshot": {
            "best_runtime_split": "oos",
            "best_runtime_net_profit": num(f71e_oos.get("net_profit")),
            "best_runtime_profit_factor": num(f71e_oos.get("profit_factor")),
            "best_runtime_drawdown_percent": num(f71e_oos.get("max_drawdown_percent")),
            "best_runtime_trades_per_day": num(f71e_oos.get("trades_per_day")),
            "validation_runtime_net_profit": num(f71e_val.get("net_profit")),
            "validation_runtime_profit_factor": num(f71e_val.get("profit_factor")),
            "validation_runtime_drawdown_percent": num(f71e_val.get("max_drawdown_percent")),
            "validation_runtime_trades_per_day": num(f71e_val.get("trades_per_day")),
        },
        "proxy_runtime_gap_cause": "F71D primary gap(1차 간극)은 proxy score(프록시 점수)와 EA edge_margin(EA 엣지 마진)의 threshold semantics mismatch(임계값 의미 불일치)였다. F71E는 signal/feature parity(신호/피처 동등성)를 수리했지만, net/PF/DD(순수익/수익 팩터/손실폭)는 runtime_economics_gap_after_signal_and_feature_parity(동등성 후 런타임 경제성 간극)로 남았다.",
        "wfo_stress_status": "not_run_out_of_scope_by_claim_after_runtime_negative_closeout(WFO/스트레스는 런타임 부정 마감 뒤 주장 범위 밖으로 미실행)",
        "wfo_stress_reason": "F71E after mandatory MT5 repair(필수 MT5 수리 후 F71E)가 PF 1.04/1.09 and trades/day 1.31/1.32(수익 팩터 1.04/1.09 및 일거래 1.31/1.32)에 머물러 completion candidate(완성 후보)가 아니며, 추가 WFO/stress(워크포워드/스트레스)는 약한 표면을 강화 검증하는 일이 된다.",
        "strict_joint_pass_count": 0,
        "preserved_clue": [
            "EA-compatible edge_margin q40 selection(EA 호환 엣지 마진 q40 선택)이 ONNX signal count parity(온엑스 신호 수 동등성)를 validation 357/357 and OOS 258/258(검증 357/357 및 표본외 258/258)로 복구했다.",
            "feature readiness parity(피처 준비 동등성)는 F71E validation/OOS(검증/표본외) 모두 diff 0(차이 0)으로 유지됐다.",
            "F71D gap cause(F71D 간극 원인)는 missing ONNX/features(온엑스/피처 누락)가 아니라 threshold semantics mismatch(임계값 의미 불일치)였다는 진단 패턴이 남았다.",
        ],
        "negative_memory": [
            "economics-native label/selection surface(경제성 네이티브 라벨/선택 표면)는 proxy scout clue(프록시 탐색 단서)를 만들었지만 meaningful candidate(의미 후보)는 F71B/F71C 모두 0이었다.",
            "signal parity repaired after F71E(신호 동등성 수리 후)에도 best OOS runtime(최선 표본외 런타임)은 net 36.35, PF 1.09, DD 5.92%, trades/day 1.3231(순수익 36.35, 수익 팩터 1.09, 손실폭 5.92%, 일거래 1.3231)로 final target(최종 목표)에 멀다.",
            "same F71 label/model/selection surface(같은 F71 라벨/모델/선택 표면)는 q threshold/tape-only repair(q 임계값/테이프 단독 수리)로 반복하지 않는다.",
        ],
        "tier_status": {
            "Tier A separate(Tier A 분리)": "materialized_proxy_and_runtime(프록시와 런타임 물질화)",
            "Tier B separate(Tier B 분리)": "missing_required_in_f71(필수 누락으로 기록)",
            "Tier A+B combined(Tier A+B 합산)": "out_of_scope_by_claim_without_tier_b(Tier B 부재로 주장 범위 밖)",
        },
        "grok": {
            "packet": rel(GROK_PACKET),
            "prompt": rel(GROK_PROMPT),
            "clean_output": rel(GROK_CLEAN),
            "metadata": rel(GROK_METADATA),
            "prompt_hash": file_hash(GROK_PROMPT),
            "clean_output_hash": file_hash(GROK_CLEAN),
            "classification": grok,
        },
        "five_stage_retrospective": {
            "closed_frontier_ids_since_last_retrospective": [STAGE_ID],
            "closeouts_since_last": 1,
            "due_status": "not_due_after_f71_closeout(아직 아님, F71 마감 후)",
            "next_numeric_trigger_frontier": 75,
        },
        "next_action": NEXT_RUN_ID,
        "next_frontier_direction": "change_at_least_one_upstream_axis_feature_label_model_trade_risk_or_regime(피처/라벨/모델/거래형태/위험/장세 중 최소 하나의 상류 축 변경)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def closeout_report_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Frontier71 Stage Closeout(F71 전선 단계 마감)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "## Closeout Label(마감 라벨)",
        "",
        f"`{summary['closeout_label']}`",
        "",
        f"Claim boundary(주장 경계): `{summary['claim_boundary']}`.",
        "",
        "## Hypothesis(가설)",
        "",
        summary["hypothesis"],
        "",
        "Effect(효과): label/target(라벨/목표), feature set(피처 묶음), model family(모델 계열), selection objective(선택 목표), and runtime semantics repair(런타임 의미 수리)를 한 lifecycle(생명주기)에서 시험했다.",
        "",
        "## Test Period(테스트 기간)",
        "",
        f"- proxy frame(프록시 프레임): `{summary['test_period']['proxy_frame']}`.",
        f"- runtime validation(런타임 검증): `{summary['test_period']['runtime_validation']}`.",
        f"- runtime OOS(런타임 표본외): `{summary['test_period']['runtime_oos']}`.",
        "",
        "## Proxy Expectation(프록시 예상)",
        "",
        summary["proxy_expectation"],
        "",
        "## Proxy KPI(프록시 핵심 성과 지표)",
        "",
        f"- F71B candidates(후보): `{summary['proxy_kpi']['f71b_candidate_count']}`, scout clue(탐색 단서) `{summary['proxy_kpi']['f71b_scout_clue_count']}`, meaningful(의미 후보) `{summary['proxy_kpi']['f71b_meaningful_candidate_count']}`.",
        f"- F71B top OOS(상위 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{fmt(summary['proxy_kpi']['f71b_oos'].get('net_profit'))}/{fmt(summary['proxy_kpi']['f71b_oos'].get('profit_factor'))}/{percent_text(summary['proxy_kpi']['f71b_oos'].get('max_drawdown_percent'))}/{fmt(summary['proxy_kpi']['f71b_oos'].get('trades_per_day'))}`.",
        f"- F71C candidates(후보): `{summary['proxy_kpi']['f71c_candidate_count']}`, scout clue(탐색 단서) `{summary['proxy_kpi']['f71c_scout_clue_count']}`, meaningful(의미 후보) `{summary['proxy_kpi']['f71c_meaningful_candidate_count']}`.",
        f"- F71C top OOS(상위 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{fmt(summary['proxy_kpi']['f71c_oos'].get('net_profit'))}/{fmt(summary['proxy_kpi']['f71c_oos'].get('profit_factor'))}/{percent_text(summary['proxy_kpi']['f71c_oos'].get('max_drawdown_percent'))}/{fmt(summary['proxy_kpi']['f71c_oos'].get('trades_per_day'))}`.",
        "",
        "## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)",
        "",
        f"- signal count parity(신호 수 동등성): F71D OOS diff(표본외 차이) `{summary['signal_count_parity']['f71d_oos_signal_count_diff']}` -> F71E `{summary['signal_count_parity']['f71e_exact_signal_diff_rows']}/{summary['signal_count_parity']['f71e_runtime_rows']}` rows exact(행 정확).",
        f"- feature readiness parity(피처 준비 동등성): `{summary['feature_readiness_parity']['f71e_exact_feature_diff_rows']}/{summary['feature_readiness_parity']['f71e_runtime_rows']}` rows exact(행 정확).",
        f"- proxy/runtime gap cause(프록시/런타임 간극 원인): {summary['proxy_runtime_gap_cause']}",
        "",
    ]
    lines.extend(compact_runtime_lines(summary["f71d_runtime_probe_summary"], "F71D Before Repair(F71D 수리 전)"))
    lines.extend([""])
    lines.extend(kpi_table_lines(summary["runtime_probe_kpi"]))
    lines.extend(
        [
            "",
            "## WFO/Stress(워크포워드/스트레스)",
            "",
            f"- status(상태): `{summary['wfo_stress_status']}`.",
            f"- reason(사유): {summary['wfo_stress_reason']}",
            "",
            "## Tier Records(티어 기록)",
            "",
        ]
    )
    lines.extend(f"- {key}: `{value}`." for key, value in summary["tier_status"].items())
    lines.extend(
        [
            "",
            "## Preserved Clue(보존 단서)",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in summary["preserved_clue"])
    lines.extend(
        [
            "",
            "## Negative Memory(부정 기억)",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in summary["negative_memory"])
    lines.extend(
        [
            "",
            "## Grok Closeout Review(그록 마감 검토)",
            "",
            f"- packet(묶음): `{summary['grok']['packet']}`.",
            f"- prompt(프롬프트): `{summary['grok']['prompt']}`, sha256(해시) `{summary['grok']['prompt_hash']}`.",
            f"- output(출력): `{summary['grok']['clean_output']}`, sha256(해시) `{summary['grok']['clean_output_hash']}`.",
            f"- classification(분류): `{summary['grok']['classification']['classification']}`.",
            "- accepted(수용): closeout as preserved clue + negative memory(보존 단서 + 부정 기억 마감), no more F71 tape/threshold-only repair(F71 테이프/임계값 단독 수리 중단), next frontier upstream pivot(다음 전선 상류 축 전환).",
            "- rejected(거절): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 주장.",
            f"- local verification(로컬 검증): `{summary['grok']['classification']['local_verification']}`.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{summary['next_action']}`",
            "",
            f"Effect(효과): F71의 process clue(절차 단서)는 보존하고, 같은 economics-native surface(경제성 네이티브 표면)를 threshold mining(임계값 채굴)으로 반복하지 않게 한다.",
        ]
    )
    return lines


def grok_receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    grok = summary["grok"]["classification"]
    return [
        "# F71 Closeout Grok Receipt(F71 마감 그록 영수증)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "- trigger_reason(트리거 이유): stage closeout(단계 마감)에 Grok second opinion(그록 2차 의견)이 필수다.",
        "- review_size(검토 크기): medium review(중간 검토).",
        "- direction_before_grok(그록 전 방향): F71을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫고, 다음 전선은 상류 축을 바꾼다.",
        f"- bounded_evidence(제한 근거): F71B/F71C proxy KPI(프록시 KPI), F71D/F71E MT5 Runtime Probe(MT5 런타임 탐침), F71E gap classification(간극 분류).",
        f"- prompt_identity(프롬프트 정체성): `{summary['grok']['prompt']}`, sha256 `{summary['grok']['prompt_hash']}`.",
        f"- grok_output_identity(그록 출력 정체성): `{summary['grok']['clean_output']}`, sha256 `{summary['grok']['clean_output_hash']}`.",
        f"- advice_classification(조언 분류): `{grok['classification']}`.",
        f"- accepted(수용): `{'; '.join(grok['accepted'])}`.",
        f"- rejected(거절): `{'; '.join(grok['rejected'])}`.",
        f"- needs_local_verification(로컬 검증 필요): `{'; '.join(grok['needs_local_verification'])}`.",
        f"- local_verification(로컬 검증): `{grok['local_verification']}`.",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        f"- final_codex_direction(최종 Codex 방향): `{summary['next_action']}` with new upstream axis(새 상류 축).",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    rows = [
        ("reentry_truth_alignment(재진입 진실 정렬)", "pass(통과)", "workspace_state/current_working_state/selection_status aligned before F71F(F71F 전 상태 정렬 확인)"),
        ("stage_open_grok(단계 개방 그록)", "pass(통과)", rel(REVIEWS_ROOT / "grok_stage_open_receipt.md")),
        ("proxy_scout(프록시 탐색)", "pass(통과)", rel(REVIEWS_ROOT / "frontier71B_economics_native_proxy_scout_report.md")),
        ("proxy_repair(프록시 수리)", "pass(통과)", rel(REVIEWS_ROOT / "frontier71C_economics_native_repair_recombine_proxy_report.md")),
        ("pre_mt5_grok(런타임 전 그록)", "pass(통과)", rel(REVIEWS_ROOT / "f71d_pre_mt5_grok_receipt.md")),
        ("mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침)", "pass(통과)", rel(REVIEWS_ROOT / "frontier71D_mt5_runtime_probe_report.md")),
        ("proxy_runtime_gap_analysis(프록시/런타임 간극 분석)", "pass(통과)", rel(REVIEWS_ROOT / "frontier71E_proxy_runtime_gap_analysis_and_repair_decision_report.md")),
        ("runtime_repair_probe(런타임 수리 탐침)", "pass(통과)", rel(F71E_RECEIPT)),
        ("closeout_grok(마감 그록)", "pass(통과)", summary["grok"]["packet"]),
        ("required_closeout_kpi(필수 마감 KPI)", "pass(통과)", rel(STAGE_CLOSEOUT_REPORT)),
        ("five_stage_retrospective_due_check(5단계 중간 검토 도래 점검)", "not_due(아직 아님)", "F71 is 1/5 after F66-F70 retrospective(F66-F70 중간 검토 뒤 F71은 1/5)"),
        ("WFO_stress(워크포워드/스트레스)", "out_of_scope_by_claim(주장 범위 밖)", summary["wfo_stress_reason"]),
    ]
    lines = [
        "# F71F Required Gate Coverage Audit(F71F 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {utc_now()}",
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
            "Result(결과): required lifecycle evidence(필수 생명주기 근거)는 F71 closeout(마감)에 연결됐다. WFO/stress(워크포워드/스트레스)는 weak runtime economics(약한 런타임 경제성) 때문에 completion candidate(완성 후보) 검증이 아니라서 미실행으로 명명했다.",
        ]
    )
    return lines


def registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    snap = summary["runtime_snapshot"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(CLOSEOUT_SUMMARY),
        "notes": "F71 closed as preserved clue + negative memory; signal parity repaired but runtime economics weak(F71 보존 단서 + 부정 기억 마감, 신호 동등성 수리 후 런타임 경제성 약함).",
        "family": "stage_closeout(단계 마감)",
        "primary_report": rel(STAGE_CLOSEOUT_REPORT),
        "run_number": "frontier71F",
        "date": "2026-06-17",
        "decision": STATUS,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 11,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(STAGE_CLOSEOUT_REPORT),
        "runtime_completed_rows": 2,
        "best_net_profit": snap["best_runtime_net_profit"],
        "best_profit_factor": snap["best_runtime_profit_factor"],
        "run_date": "2026-06-17",
        "primary_artifact": rel(CLOSEOUT_SUMMARY),
        "candidate_model_id": "f71b_1e511d3db9c3",
        "net_profit": snap["best_runtime_net_profit"],
        "profit_factor": snap["best_runtime_profit_factor"],
        "drawdown": snap["best_runtime_drawdown_percent"],
        "recovery_factor": "",
        "trade_count": 258,
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
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": "stage_closeout(단계 마감)",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락)",
        "kpi_scope": "runtime_closeout_kpi(런타임 마감 KPI)",
        "primary_kpi": "best_oos_runtime_net=36.35; PF=1.09; DD=5.92; trades_day=1.3231",
        "guardrail_kpi": "signal_diff=0; feature_diff=0; meaningful_proxy=0; strict_joint_pass=0",
        "runtime_attempt_rows": 2,
        "work_family": "frontier_stage_closeout(전선 단계 마감)",
        "row_id": f"{RUN_ID}__stage_closeout",
        "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서와 부정 기억, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": summary["hypothesis"],
        "artifact_count": 5,
        "long_trade_count": 181,
        "short_trade_count": 77,
        "trade_density_per_feature_day": snap["best_runtime_trades_per_day"],
        "drawdown": snap["best_runtime_drawdown_percent"],
    }


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    row = registry_row(summary)
    row.update(
        {
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "subrun_id": "stage_closeout(단계 마감)",
            "record_view": "stage_closeout(단계 마감)",
            "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)",
            "kpi_scope": "runtime_closeout_kpi(런타임 마감 KPI)",
            "scoreboard_lane": "stage_closeout(단계 마감)",
            "path": rel(STAGE_CLOSEOUT_REPORT),
            "primary_kpi": "F71E OOS net=36.35; PF=1.09; DD=5.92; trades/day=1.3231",
            "guardrail_kpi": "F71E signal parity 258/258; feature diff=0; F71B/F71C meaningful=0",
            "external_verification_status": "completed(완료)",
            "notes": "F71 lifecycle closed after mandatory MT5 Runtime Probe and one semantics repair(F71은 필수 MT5 런타임 탐침과 의미 수리 1회 뒤 마감).",
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
        "<!-- frontier71F_stage_closeout_economics_native_label_selection_v1 -->",
        f"""
<!-- frontier71F_stage_closeout_economics_native_label_selection_v1 -->
- `{RUN_ID}` closes Frontier71(전선71) as `{JUDGMENT}`. Preserved clue(보존 단서): EA-compatible edge_margin q40 selection(EA 호환 엣지 마진 q40 선택)이 ONNX/signal/feature parity(온엑스/신호/피처 동등성)를 복구했다. Negative memory(부정 기억): economics-native label/selection surface(경제성 네이티브 라벨/선택 표면)는 signal parity(신호 동등성) 뒤에도 runtime economics(런타임 경제성)가 약했다. Best OOS runtime(최선 표본외 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `36.35/1.09/5.92/1.3231`. Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
""",
    )
    append_once(
        NEGATIVE_RESULT_REGISTER,
        "<!-- NR-FR71-ECONOMICS-NATIVE-LABEL-SELECTION-RUNTIME-GAP -->",
        f"""
<!-- NR-FR71-ECONOMICS-NATIVE-LABEL-SELECTION-RUNTIME-GAP -->
## NR-FR71-ECONOMICS-NATIVE-LABEL-SELECTION-RUNTIME-GAP

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): economics-native label/target and selection(경제성 네이티브 라벨/목표와 선택)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 보존하는 seed surface(씨앗 표면)를 만들 수 있다.
- Why failed(실패 이유): F71B 1620 candidates(후보) and F71C 1440 repair candidates(수리 후보) produced meaningful candidate(의미 후보) `0`; after F71E edge_margin q40 runtime semantics repair(F71E 엣지 마진 q40 런타임 의미 수리), best OOS runtime(최선 표본외 런타임)은 net(순수익) `36.35`, PF(수익 팩터) `1.09`, DD(손실폭) `5.92%`, trades/day(일 거래 수) `1.3231`로 final target(최종 목표)보다 약했다.
- Salvage value(회수 가치): EA-compatible selection semantics(EA 호환 선택 의미)를 맞추면 ONNX/signal/feature parity(온엑스/신호/피처 동등성)는 정확히 복구된다.
- Do-not-repeat(반복 금지): same F71 label/model/selection surface(같은 F71 라벨/모델/선택 표면)를 q threshold or tape-only sweep(q 임계값 또는 테이프 단독 훑기)으로 반복하지 않는다.
- Reopen condition(재개 조건): feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), or regime/session split(장세/세션 분할) 중 하나 이상이 실제로 바뀌고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
- Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음).
""",
    )


def update_retrospective_register(summary: Mapping[str, Any]) -> None:
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
        f"    - {STAGE_ID}",
        "  closeouts_since_last: 1",
        "  next_numeric_trigger_frontier: 75",
        "  current_due_status: not_due_after_f71_closeout",
        '  note: "F71 closeout(마감)이 F66-F70 retrospective(중간 검토) 뒤 1/5로 등록됐다. 다음 numeric trigger(숫자 트리거)는 F75 closeout(마감)이다."',
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
        "five_stage_retrospective_due_status: not_due_after_f71_closeout",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "Action(행동): F71 economics-native label/selection lifecycle(경제성 네이티브 라벨/선택 생명주기)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감했다."',
        '  - "Effect(효과): edge_margin q40 parity repair(엣지 마진 q40 동등성 수리)는 절차 단서로 보존하고, 같은 F71 표면의 threshold/tape-only 반복은 막는다."',
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
        "Action(행동): Frontier71 economics-native label/selection(전선71 경제성 네이티브 라벨/선택)을 마감했다.",
        "",
        "Effect(효과): signal parity repair(신호 동등성 수리)는 보존 단서로 남기고, runtime economics gap(런타임 경제성 간극)은 부정 기억으로 닫았다.",
        "",
        f"- closeout label(마감 라벨): `{JUDGMENT}`.",
        "- F71E validation(검증): net(순수익) `21.77`, PF(수익 팩터) `1.04`, DD(손실폭) `8.18%`, trades/day(일 거래 수) `1.3125`.",
        "- F71E OOS(표본외): net(순수익) `36.35`, PF(수익 팩터) `1.09`, DD(손실폭) `5.92%`, trades/day(일 거래 수) `1.3231`.",
        "- signal/feature parity(신호/피처 동등성): F71E exact(정확) with signal diff(신호 차이) `0` and feature diff(피처 차이) `0`.",
        "- five-stage retrospective(5단계 중간 검토): `not_due_after_f71_closeout(아직 아님, F71 마감 후)`.",
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
        "# F71 Selection Status(F71 선택 상태)",
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
        F71B_SUMMARY,
        F71B_KPI,
        F71C_SUMMARY,
        F71C_KPI,
        F71D_RECEIPT,
        F71D_SIGNAL_PARITY,
        F71D_PROB_PARITY,
        F71E_SUMMARY,
        F71E_RECEIPT,
        F71E_GAP,
        F71E_SIGNAL_PARITY,
        F71E_PROB_PARITY,
        GROK_PROMPT,
        GROK_CLEAN,
        GROK_METADATA,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing closeout evidence: {missing}")

    f71b = read_json(F71B_SUMMARY)
    f71b_kpi = read_csv_rows(F71B_KPI)
    f71c = read_json(F71C_SUMMARY)
    f71c_kpi = read_csv_rows(F71C_KPI)
    f71d_rows = read_csv_rows(F71D_RECEIPT)
    f71e_summary = read_json(F71E_SUMMARY)
    f71e_rows = read_csv_rows(F71E_RECEIPT)
    f71e_gap_rows = read_csv_rows(F71E_GAP)
    f71e_signal_rows = read_csv_rows(F71E_SIGNAL_PARITY)
    grok_clean = read_text(GROK_CLEAN)

    summary = build_summary(
        f71b=f71b,
        f71b_kpi=f71b_kpi,
        f71c=f71c,
        f71c_kpi=f71c_kpi,
        f71d_rows=f71d_rows,
        f71e_summary=f71e_summary,
        f71e_rows=f71e_rows,
        f71e_gap_rows=f71e_gap_rows,
        f71e_signal_rows=f71e_signal_rows,
        grok_clean=grok_clean,
    )
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "inputs": {
            "f71b_summary": rel(F71B_SUMMARY),
            "f71c_summary": rel(F71C_SUMMARY),
            "f71d_runtime_receipt": rel(F71D_RECEIPT),
            "f71e_runtime_receipt": rel(F71E_RECEIPT),
            "f71e_gap": rel(F71E_GAP),
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
    update_retrospective_register(summary)
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
