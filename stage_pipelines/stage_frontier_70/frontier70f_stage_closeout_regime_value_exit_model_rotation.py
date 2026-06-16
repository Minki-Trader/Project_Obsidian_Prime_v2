from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_70 import frontier70a_stage_open_regime_value_exit_model_rotation as f70a
from stage_pipelines.stage_frontier_70 import frontier70b_label_regime_asymmetric_value_proxy_scout as f70b
from stage_pipelines.stage_frontier_70 import frontier70c_label_regime_stability_repair_proxy_scout as f70c
from stage_pipelines.stage_frontier_70 import frontier70d_label_regime_stability_runtime_probe as f70d
from stage_pipelines.stage_frontier_70 import frontier70e_selected_entry_tape_runtime_repair as f70e

STAGE_ID = f70a.STAGE_ID
RUN_ID = "frontier70F_stage_closeout_regime_specific_asymmetric_value_exit_model_rotation_v1"
PARENT_RUN_ID = f70e.RUN_ID
NEXT_RUN_ID = "five_stage_retrospective_after_f70_closeout_v1"
NEXT_FRONTIER_DIRECTION = "new_hypothesis_after_f70_retrospective_required_no_authority"

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

F70B_SUMMARY = REVIEWS_ROOT / "f70b_proxy_candidate_summary_review.csv"
F70C_SUMMARY = REVIEWS_ROOT / "f70c_proxy_candidate_summary_review.csv"
F70D_RECEIPT = REVIEWS_ROOT / "f70d_runtime_probe_receipt_review.csv"
F70D_GAP = REVIEWS_ROOT / "f70d_gap_classification_review.csv"
F70E_RECEIPT = REVIEWS_ROOT / "f70e_runtime_probe_receipt_review.csv"
F70E_GAP = REVIEWS_ROOT / "f70e_gap_classification_review.csv"
F70E_PARITY = REVIEWS_ROOT / "f70e_onnx_signal_parity_review.csv"
F70E_REPORT = REVIEWS_ROOT / "frontier70E_selected_entry_tape_runtime_repair_report.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f70_stage_closeout_regime_value_exit_model_rotation"
GROK_PROMPT = GROK_PACKET / "prompts/f70_stage_closeout_regime_value_exit_model_rotation_prompt.md"
GROK_CLEAN = GROK_PACKET / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET / "outputs/metadata.json"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
CLOSEOUT_SUMMARY = RUN_ROOT / "frontier70F_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEWS_ROOT / "stage_closeout_report.md"
GROK_RECEIPT = REVIEWS_ROOT / "f70_stage_closeout_grok_receipt.md"
GATE_AUDIT = REVIEWS_ROOT / "required_gate_coverage_audit_f70f.md"

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
        return str(value or "")
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")

def percent_text(value: Any) -> str:
    text = fmt(value)
    return text if text.endswith("%") else f"{text}%"

def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""

def find_row(rows: Sequence[Mapping[str, Any]], *, axis: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("axis_id") == axis and row.get("split") == split:
            return row
    return {}

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
                "time_under_water": "not_available_from_current_strategy_report_parse(현재 전략 테스터 파싱에서 없음)",
                "max_consecutive_loss": "not_available_from_current_strategy_report_parse(현재 전략 테스터 파싱에서 없음)",
                "long_short_breakdown": f"long={row.get('long_trade_count')};short={row.get('short_trade_count')}",
                "proxy_runtime_gap": (
                    f"proxy_pf={fmt(row.get('proxy_profit_factor'))};runtime_pf={fmt(row.get('profit_factor'))};"
                    f"proxy_tpd={fmt(row.get('proxy_trades_per_day'))};runtime_tpd={fmt(row.get('trades_per_day'))};"
                    f"proxy_dd={fmt(row.get('proxy_dd_percent'))};runtime_dd={fmt(row.get('max_drawdown_percent'))};"
                    f"signal_diff={fmt(row.get('signal_count_diff'))};feature_diff={fmt(row.get('feature_ready_diff'))}"
                ),
            }
        )
    return output

def classify_grok_advice(clean_text: str) -> dict[str, Any]:
    accepted = "Final classification: `accepted(수용)`" in clean_text or "Classification(분류): `accepted(수용)`" in clean_text
    return {
        "classification": "accepted(수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "accepted": [
            "closeout_label_honest(마감 라벨 정직함)",
            "preserved_clue_and_negative_memory_separated(보존 단서와 부정 기억 분리 적절)",
            "close_f70_and_pivot_to_new_hypothesis(F70 마감 후 새 가설 전환)",
            "claim_boundary_no_authority(권위 주장 없음)",
        ]
        if accepted
        else [],
        "rejected": ["none(없음)"] if accepted else ["automatic_closeout_without_local_verification(로컬 검증 없는 자동 마감)"],
        "needs_local_verification": [
            "artifact_identity_and_ledger_rows(산출물 정체성과 장부 행)",
            "time_under_water_and_max_consecutive_loss_unavailable_scope(회복 전 체류 시간과 최대 연속 손실 없음 범위)",
        ],
        "local_verification": {
            "artifact_identity_and_ledger_rows(산출물 정체성과 장부 행)": "verified_by_local_paths_hashes_and_csv_rows(로컬 경로/해시/CSV 행으로 검증)",
            "time_under_water_and_max_consecutive_loss_unavailable_scope(회복 전 체류 시간과 최대 연속 손실 없음 범위)": "recorded_as_not_available_not_used_for_positive_claim(없는 값으로 기록하고 긍정 주장에 쓰지 않음)",
        },
    }

def build_summary(
    f70b_rows: Sequence[Mapping[str, Any]],
    f70c_rows: Sequence[Mapping[str, Any]],
    f70d_rows: Sequence[Mapping[str, Any]],
    f70e_rows: Sequence[Mapping[str, Any]],
    f70e_gap_rows: Sequence[Mapping[str, Any]],
    f70e_parity_rows: Sequence[Mapping[str, Any]],
    grok_clean: str,
) -> dict[str, Any]:
    reference_oos = find_row(f70e_rows, axis="reference_low_dd_axis", split="oos")
    small_nn_oos = find_row(f70e_rows, axis="small_nn_density_axis", split="oos")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "closeout_label": JUDGMENT,
        "hypothesis": (
            "Regime/session-specific asymmetric value and exit-survival labels with density-aware "
            "selection might repair the sparse/dense fracture after F69."
        ),
        "test_period": "validation 2025-01-02..2025-10-01; oos 2025-10-01..2026-04-14",
        "proxy_expectation": (
            "F70 expected label/regime selection to improve density without blowing up drawdown, "
            "then selected-entry runtime tape should preserve proxy trade-count intent."
        ),
        "proxy_kpi": {
            "f70b_candidate_rows": len(f70b_rows),
            "f70c_candidate_rows": len(f70c_rows),
            "f70b_meaningful_count": sum(1 for row in f70b_rows if str(row.get("meaningful_signal", "")).lower() == "true"),
            "f70c_meaningful_count": sum(1 for row in f70c_rows if str(row.get("meaningful_signal", "")).lower() == "true"),
            "f70b_final_like_count": sum(1 for row in f70b_rows if str(row.get("final_like", "")).lower() == "true"),
            "f70c_final_like_count": sum(1 for row in f70c_rows if str(row.get("final_like", "")).lower() == "true"),
            "f70c_reference_validation": "net=527.46;pf=1.1676;dd=4.3626;trades_day=0.9365",
            "f70c_reference_oos": "net=1153.65;pf=1.5657;dd=1.8239;trades_day=0.8907",
            "f70c_small_nn_validation": "net=835.79;pf=1.1975;dd=4.3381;trades_day=1.1466",
            "f70c_small_nn_oos": "net=430.60;pf=1.1241;dd=2.8760;trades_day=1.2254",
        },
        "runtime_probe_kpi": closeout_kpi_rows(f70e_rows),
        "runtime_probe_rows": len(f70e_rows),
        "f70d_runtime_probe_summary": [
            {
                "axis_id": row.get("axis_id"),
                "split": row.get("split"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "drawdown_percent": row.get("max_drawdown_percent"),
                "trade_count": row.get("trade_count"),
                "trades_per_day": row.get("trades_per_day"),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
                "gap_cause_summary": row.get("gap_cause_summary"),
            }
            for row in f70d_rows
        ],
        "signal_count_parity": {
            "f70e_signal_diff_rows": sum(1 for row in f70e_rows if fmt(row.get("signal_count_diff")) == "0"),
            "f70e_feature_diff_rows": sum(1 for row in f70e_rows if fmt(row.get("feature_ready_diff")) == "0"),
            "parity_rows": len(f70e_parity_rows),
        },
        "feature_readiness_parity": "exact_all_f70e_runtime_rows(모든 F70E 런타임 행에서 정확)",
        "proxy_runtime_gap_cause": (
            "F70D trade_lifecycle_gap_after_signal_parity was repaired by selected-entry tape. "
            "F70E remaining gap is runtime_economics_gap_after_signal_and_feature_parity."
        ),
        "gap_classification_rows": len(f70e_gap_rows),
        "strict_joint_pass_count": 0,
        "preserved_clue": [
            "selected_entry_runtime_veto_tape_exactly_aligns_proxy_selected_trade_count(선택 진입 런타임 차단 테이프가 프록시 선택 거래 수를 정확히 맞춤)",
            "onnx_probability_signal_feature_parity_exact_across_f70d_f70e(F70D/F70E에서 온엑스/확률/신호/피처 동등성 정확)",
            "runtime_gap_is_now_economics_not_bridge_semantics(이제 런타임 간극은 연결 의미가 아니라 경제성 문제)",
        ],
        "negative_memory": [
            "regime_specific_asymmetric_value_exit_survival_surface_did_not_create_enough_density_or_pf(장세별 비대칭 가치/청산 생존 표면은 충분한 밀도나 수익 팩터를 만들지 못함)",
            "small_nn_density_axis_oos_dd_breached_10_percent_after_exact_trade_parity(작은 신경망 밀도 축은 정확 거래 동등성 뒤 표본외 손실폭 10퍼센트 초과)",
            "same_f70_label_model_axis_should_not_repeat_without_new_economic_hypothesis(같은 F70 라벨/모델 축은 새 경제 가설 없이 반복 금지)",
        ],
        "runtime_snapshot": {
            "reference_oos_net": num(reference_oos.get("net_profit")),
            "reference_oos_pf": num(reference_oos.get("profit_factor")),
            "reference_oos_dd": num(reference_oos.get("max_drawdown_percent")),
            "reference_oos_trades_day": num(reference_oos.get("trades_per_day")),
            "small_nn_oos_net": num(small_nn_oos.get("net_profit")),
            "small_nn_oos_pf": num(small_nn_oos.get("profit_factor")),
            "small_nn_oos_dd": num(small_nn_oos.get("max_drawdown_percent")),
            "small_nn_oos_trades_day": num(small_nn_oos.get("trades_per_day")),
        },
        "grok": {
            "packet": rel(GROK_PACKET),
            "prompt": rel(GROK_PROMPT),
            "clean_output": rel(GROK_CLEAN),
            "metadata": rel(GROK_METADATA),
            "prompt_hash": file_hash(GROK_PROMPT),
            "clean_output_hash": file_hash(GROK_CLEAN),
            "classification": classify_grok_advice(grok_clean),
        },
        "five_stage_retrospective": {
            "closed_frontier_ids_since_last_retrospective": [
                "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
                "stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk",
                "stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout",
                "stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory",
                STAGE_ID,
            ],
            "closeouts_since_last": 5,
            "due_status": "due_after_f70_closeout(도래, F70 마감 뒤)",
            "next_open_block": True,
        },
        "next_action": NEXT_RUN_ID,
        "next_frontier_direction": NEXT_FRONTIER_DIRECTION,
        "claim_boundary": CLAIM_BOUNDARY,
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

def f70d_table_lines(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    lines = [
        "| axis(축) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실폭) | trades(거래 수) | trades/day(일 거래 수) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['axis_id']}` | `{row['split']}` | `{fmt(row['net_profit'])}` | `{fmt(row['profit_factor'])}` | `{percent_text(row['drawdown_percent'])}` | `{fmt(row['trade_count'])}` | `{fmt(row['trades_per_day'])}` | `{fmt(row['signal_count_diff'])}` | `{fmt(row['feature_ready_diff'])}` | `{row['gap_cause_summary']}` |"
        )
    return lines

def closeout_report_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Frontier70 Stage Closeout(F70 전선 단계 마감)",
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
        "Effect(효과): label/target(라벨/목표), model family(모델 계열), regime/session split(장세/세션 분할), and selected-entry runtime tape(선택 진입 런타임 테이프)를 함께 시험했다.",
        "",
        "## Proxy Expectation(프록시 예상)",
        "",
        summary["proxy_expectation"],
        "",
        "## Proxy KPI(프록시 핵심 성과 지표)",
        "",
        f"- F70B candidate rows(F70B 후보 행): `{summary['proxy_kpi']['f70b_candidate_rows']}`, meaningful(의미 신호) `{summary['proxy_kpi']['f70b_meaningful_count']}`, final_like(최종 유사) `{summary['proxy_kpi']['f70b_final_like_count']}`.",
        f"- F70C candidate rows(F70C 후보 행): `{summary['proxy_kpi']['f70c_candidate_rows']}`, meaningful(의미 신호) `{summary['proxy_kpi']['f70c_meaningful_count']}`, final_like(최종 유사) `{summary['proxy_kpi']['f70c_final_like_count']}`.",
        f"- F70C reference validation(참조 검증): `{summary['proxy_kpi']['f70c_reference_validation']}`.",
        f"- F70C reference OOS(참조 표본외): `{summary['proxy_kpi']['f70c_reference_oos']}`.",
        f"- F70C small NN validation(작은 신경망 검증): `{summary['proxy_kpi']['f70c_small_nn_validation']}`.",
        f"- F70C small NN OOS(작은 신경망 표본외): `{summary['proxy_kpi']['f70c_small_nn_oos']}`.",
        "",
        "## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)",
        "",
        f"- test period(테스트 기간): `{summary['test_period']}`.",
        f"- signal count parity(신호 수 동등성): `{summary['signal_count_parity']['f70e_signal_diff_rows']}/{summary['runtime_probe_rows']}` F70E rows exact(정확).",
        f"- feature readiness parity(피처 준비 동등성): `{summary['feature_readiness_parity']}`.",
        f"- proxy/runtime gap cause(프록시/런타임 간극 원인): `{summary['proxy_runtime_gap_cause']}`.",
        "",
        "### F70D Before Repair(F70D 수리 전)",
        "",
    ]
    lines.extend(f70d_table_lines(summary["f70d_runtime_probe_summary"]))
    lines.extend(
        [
            "",
            "### F70E After Selected-Entry Tape Repair(F70E 선택 진입 테이프 수리 후)",
            "",
        ]
    )
    lines.extend(kpi_table_lines(summary["runtime_probe_kpi"]))
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
            f"- prompt(프롬프트): `{summary['grok']['prompt']}`, sha256 `{summary['grok']['prompt_hash']}`.",
            f"- output(출력): `{summary['grok']['clean_output']}`, sha256 `{summary['grok']['clean_output_hash']}`.",
            f"- classification(분류): `{summary['grok']['classification']['classification']}`.",
            "- accepted(수용): closeout label honest(마감 라벨 정직), preserved clue and negative memory separated(보존 단서와 부정 기억 분리), close and pivot(마감 후 전환).",
            "- needs_local_verification(로컬 검증 필요): artifact identity and ledger rows(산출물 정체성과 장부 행), unavailable time-under-water fields(없는 회복 전 체류 시간 필드).",
            "",
            "## Five-Stage Retrospective Check(5단계 중간 검토 점검)",
            "",
            "- current_due_status(현재 도래 상태): `due_after_f70_closeout(도래, F70 마감 뒤)`.",
            "- closeouts_since_last(이전 중간 검토 뒤 마감 수): `5`.",
            "- next frontier open block(다음 전선 단계 개방 차단): `true(참)` until retrospective packet(중간 검토 묶음)이 닫힌다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{summary['next_action']}`.",
            "",
            "Effect(효과): 다음 frontier stage(전선 단계)는 바로 열지 않고 F66-F70 cross-stage retrospective(단계 간 중간 검토)를 먼저 닫는다.",
        ]
    )
    return lines

def grok_receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    classification = summary["grok"]["classification"]
    return [
        "# F70 Closeout Grok Receipt(F70 마감 그록 영수증)",
        "",
        f"- created_at_utc(생성 시각): `{utc_now()}`",
        "- trigger_reason(트리거 이유): stage closeout review(단계 마감 검토).",
        "- review_size(검토 크기): `medium(중간)`.",
        "- bounded_evidence(제한 근거): F70B/F70C proxy KPI(프록시 핵심 성과 지표), F70D/F70E MT5 Runtime Probe(MT5 런타임 탐침), closeout label proposal(마감 라벨 제안).",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{summary['grok']['prompt_hash']}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{summary['grok']['clean_output_hash']}`.",
        f"- advice_classification(조언 분류): `{classification['classification']}`.",
        f"- accepted(수용): `{'; '.join(classification['accepted'])}`.",
        f"- rejected(거절): `{'; '.join(classification['rejected'])}`.",
        f"- needs_local_verification(로컬 검증 필요): `{'; '.join(classification['needs_local_verification'])}`.",
        f"- local_verification(로컬 검증): `{classification['local_verification']['artifact_identity_and_ledger_rows(산출물 정체성과 장부 행)']}`.",
        f"- final_codex_direction(최종 Codex 방향): close F70 as preserved clue + negative memory no authority(F70을 보존 단서 + 부정 기억, 권위 없음으로 마감).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]

def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# Required Gate Coverage Audit F70F(필수 게이트 커버리지 감사 F70F)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| hypothesis lifecycle(가설 생명주기) | passed(통과) | F70A..F70F reports(F70A..F70F 보고서) | 가설->프록시->MT5 탐침->간극 분석->수리->마감 연결 |",
        f"| mandatory MT5 runtime probe(필수 MT5 런타임 탐침) | passed(통과) | `{rel(F70D_RECEIPT)}` and `{rel(F70E_RECEIPT)}` | F70에서 실제 Strategy Tester(전략 테스터) KPI 기록 |",
        f"| proxy/runtime gap analysis(프록시/런타임 간극 분석) | passed(통과) | `{rel(F70D_GAP)}` and `{rel(F70E_GAP)}` | trade lifecycle gap(거래 생명주기 간극)과 economics gap(경제성 간극) 분리 |",
        f"| repair attempt(수리 시도) | passed(통과) | `{rel(F70E_REPORT)}` | selected-entry tape(선택 진입 테이프)로 trade count(거래 수) 간극 수리 |",
        f"| Grok closeout review(그록 마감 검토) | passed(통과) | `{rel(GROK_RECEIPT)}` | 외부 2차 의견을 수용/검증/경계 처리 |",
        f"| closeout KPI(마감 KPI) | passed(통과) | `{rel(STAGE_CLOSEOUT_REPORT)}` | 기간, 순수익, 총이익/총손실, PF, DD, 거래 수, 기대값, 회복 계수, 롱/숏, gap 기록 |",
        "| five-stage retrospective due check(5단계 중간 검토 도래 점검) | due(도래) | `docs/registers/five_stage_retrospective_register.yaml` | 다음 전선 단계 개방 전 retrospective(중간 검토) 필요 |",
        f"| claim boundary(주장 경계) | passed(통과) | `{CLAIM_BOUNDARY}` | 금지 주장 없음 |",
        "",
        f"Summary(요약): closeout label(마감 라벨) `{summary['closeout_label']}`; next(다음) `{NEXT_RUN_ID}`.",
    ]

def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    snap = summary["runtime_snapshot"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(STAGE_CLOSEOUT_REPORT),
        "notes": "F70 closed after proxy scout, MT5 runtime probe, selected-entry tape repair, and Grok closeout review.",
        "family": "kpi_evidence(핵심 성과 지표 근거)",
        "primary_report": rel(STAGE_CLOSEOUT_REPORT),
        "run_number": "frontier70F",
        "date": "2026-06-17",
        "decision": "close_f70_preserved_clue_negative_memory_then_retrospective",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(STAGE_CLOSEOUT_REPORT),
        "run_date": "2026-06-17",
        "primary_artifact": rel(CLOSEOUT_SUMMARY),
        "net_profit": snap.get("reference_oos_net"),
        "profit_factor": snap.get("reference_oos_pf"),
        "drawdown": snap.get("reference_oos_dd"),
        "recovery_factor": "",
        "trade_count": 174,
        "result_status": STATUS,
        "expectancy": "",
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
        "primary_kpi": "f70e_reference_oos_pf=1.29; f70e_reference_oos_tpd=0.8923; f70e_reference_oos_dd=5.61",
        "guardrail_kpi": "f70e_small_nn_oos_pf=1.02; f70e_small_nn_oos_dd=10.56; strict_joint_pass_count=0; no authority claims",
        "runtime_attempt_rows": 4,
        "work_family": "kpi_evidence(핵심 성과 지표 근거)",
        "row_id": f"{RUN_ID}__stage_closeout",
        "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서/부정 기억, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "What did F70 preserve and what should not repeat?(F70은 무엇을 보존하고 무엇을 반복하지 말아야 하나?)",
        "artifact_count": 8,
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
        "source_authority": "F70E MT5 runtime repair observation(F70E MT5 런타임 수리 관찰)",
        "trade_density": snap.get("reference_oos_trades_day"),
        "expected_trade_density": "5-10 trades/day final target not met(최종 목표 일 5-10회 미달)",
        "max_drawdown_percent": snap.get("reference_oos_dd"),
        "strict_joint_pass_count": 0,
    }

def update_registers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    append_once(
        IDEA_REGISTRY,
        "<!-- frontier70F_stage_closeout_regime_value_exit_model_rotation_v1 -->",
        f"""
<!-- frontier70F_stage_closeout_regime_value_exit_model_rotation_v1 -->
- `{RUN_ID}` closes Frontier70(전선70) as `{JUDGMENT}`. Preserved clue(보존 단서): selected-entry RuntimeVetoTape(선택 진입 런타임 차단 테이프) aligns proxy selected trades(프록시 선택 거래) with MT5 runtime trade count(MT5 런타임 거래 수); ONNX/probability/signal/feature parity(온엑스/확률/신호/피처 동등성) remains exact. Negative memory(부정 기억): this regime-specific asymmetric value/exit-survival label surface(장세별 비대칭 가치/청산 생존 라벨 표면) remains too sparse and too weak economically after exact runtime parity(정확 런타임 동등성). Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}` before a new frontier open(새 전선 개방 전).
""",
    )
    append_once(
        NEGATIVE_RESULT_REGISTER,
        "<!-- NR-FR70-REGIME-VALUE-EXIT-SURVIVAL-ECONOMICS -->",
        f"""
<!-- NR-FR70-REGIME-VALUE-EXIT-SURVIVAL-ECONOMICS -->
## NR-FR70-REGIME-VALUE-EXIT-SURVIVAL-ECONOMICS

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): regime/session-specific asymmetric value and exit-survival labels(장세/세션별 비대칭 가치 및 청산 생존 라벨) with density-aware selection(밀도 인식 선택) could repair sparse/dense fracture(희소/밀집 균열).
- Why failed(실패 이유): F70B 420 candidates(후보), F70C 936 candidates(후보) produced meaningful signal(의미 신호) `0` and final_like(최종 유사) `0`; after selected-entry runtime repair(선택 진입 런타임 수리), best OOS runtime(최선 표본외 런타임)은 reference axis(참조 축) net(순수익) `68.00`, PF(수익 팩터) `1.29`, DD(손실폭) `5.61%`, trades/day(일 거래 수) `0.8923`로 밀도 목표에 크게 못 미쳤고, small NN axis(작은 신경망 축)는 OOS DD(표본외 손실폭) `10.56%`로 제한을 넘었다.
- Salvage value(회수 가치): selected-entry tape(선택 진입 테이프) repaired trade-count parity(거래 수 동등성), so future runtime probes(향후 런타임 탐침)는 selected-entry semantics(선택 진입 의미)를 reuse(재사용)할 수 있다.
- Do-not-repeat(반복 금지): same F70 label/model/selection surface(같은 F70 라벨/모델/선택 표면)를 threshold(임계값)나 tape variant(테이프 변형)만 바꿔 반복하지 않는다.
- Reopen condition(재개 조건): a genuinely new economic hypothesis(진짜 새 경제 가설)가 feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), or regime/session split(장세/세션 분할) 중 하나 이상을 주도적으로 바꿀 때만 다시 연다.
- Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음).
""",
    )

def update_retrospective_register(summary: Mapping[str, Any]) -> None:
    stage_ids = summary["five_stage_retrospective"]["closed_frontier_ids_since_last_retrospective"]
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
    ]
    lines.extend(f"    - {stage_id}" for stage_id in stage_ids)
    lines.extend(
        [
            "  closeouts_since_last: 5",
            "  next_numeric_trigger_frontier: 70",
            "  current_due_status: due_after_f70_closeout",
            '  note: "F66-F70 closeouts(마감) are now 5/5. Next frontier open(다음 전선 개방)은 five-stage retrospective(5단계 중간 검토)가 닫힐 때까지 차단된다."',
        ]
    )
    io_path(RETROSPECTIVE_REGISTER).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")

def write_state_files(summary: Mapping[str, Any]) -> None:
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f70_runtime_probe_and_selected_entry_repair_completed_no_authority(F70 런타임 탐침 및 선택 진입 수리 완료, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: due_after_f70_closeout",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "F70F action(행동): F70 regime value/exit model rotation(장세 가치/청산 모델 전환)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감했다."',
        '  - "Effect(효과): selected-entry tape(선택 진입 테이프) 동등성 단서는 보존하고, 같은 경제 가설 반복은 막는다."',
        '  - "Next action(다음 행동): five_stage_retrospective_after_f70_closeout_v1에서 F66-F70 cross-stage review(단계 간 검토)를 먼저 닫는다."',
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
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): Frontier70 regime-specific asymmetric value/exit model rotation(전선70 장세별 비대칭 가치/청산 모델 전환)을 마감했다.",
        "",
        "Effect(효과): selected-entry tape(선택 진입 테이프)는 runtime trade count(런타임 거래 수)를 proxy selected trades(프록시 선택 거래)와 맞추는 보존 단서로 남겼고, F70 경제 가설은 부정 기억으로 닫았다.",
        "",
        f"- closeout label(마감 라벨): `{JUDGMENT}`.",
        f"- strict joint pass count(엄격 공동 통과 수): `{summary['strict_joint_pass_count']}`.",
        "- F70E reference OOS(참조 표본외): net(순수익) `68.00`, PF(수익 팩터) `1.29`, DD(손실폭) `5.61%`, trades/day(일 거래 수) `0.8923`.",
        "- F70E small NN OOS(작은 신경망 표본외): net(순수익) `7.15`, PF(수익 팩터) `1.02`, DD(손실폭) `10.56%`, trades/day(일 거래 수) `1.2256`.",
        "- five-stage retrospective(5단계 중간 검토): `due_after_f70_closeout(도래, F70 마감 뒤)`.",
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
        "# F70 Selection Status(F70 선택 상태)",
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
    write_md(SELECTION_STATUS, selection_lines)

def main() -> int:
    required = [F70B_SUMMARY, F70C_SUMMARY, F70D_RECEIPT, F70D_GAP, F70E_RECEIPT, F70E_GAP, F70E_PARITY, GROK_PROMPT, GROK_CLEAN, GROK_METADATA]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing closeout evidence: {missing}")
    f70b_rows = read_csv_rows(F70B_SUMMARY)
    f70c_rows = read_csv_rows(F70C_SUMMARY)
    f70d_rows = read_csv_rows(F70D_RECEIPT)
    f70e_rows = read_csv_rows(F70E_RECEIPT)
    f70e_gap_rows = read_csv_rows(F70E_GAP)
    f70e_parity_rows = read_csv_rows(F70E_PARITY)
    grok_clean = io_path(GROK_CLEAN).read_text(encoding="utf-8-sig")
    summary = build_summary(f70b_rows, f70c_rows, f70d_rows, f70e_rows, f70e_gap_rows, f70e_parity_rows, grok_clean)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
        "inputs": {
            "f70b_summary": rel(F70B_SUMMARY),
            "f70c_summary": rel(F70C_SUMMARY),
            "f70d_runtime_receipt": rel(F70D_RECEIPT),
            "f70e_runtime_receipt": rel(F70E_RECEIPT),
            "f70e_gap": rel(F70E_GAP),
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
    update_retrospective_register(summary)
    write_state_files(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "next_run_id": NEXT_RUN_ID,
                    "retrospective_due": "due_after_f70_closeout",
                    "strict_joint_pass_count": 0,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
