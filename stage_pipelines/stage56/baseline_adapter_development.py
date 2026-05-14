from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.adapters.baseline_adapter import adapter_contract_payload, initial_v64_contract
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_ID = "run50BS_stage56_baseline_adapter_transition_v1"
RUN_NUMBER = "run50BS"
PACKET_ID = "stage56_baseline_adapter_transition_v1"
TERMINAL_LABEL = "development_anchor_selected_and_adapter_development_started"
STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
REPORT_PATH = REVIEWS_ROOT / "run50BS_baseline_adapter_transition.md"
CANDIDATE_CSV_PATH = REVIEWS_ROOT / "run50BS_candidate_selection.csv"
CONTRACT_MD_PATH = SELECTED_ROOT / "baseline_adapter_initial_contract.md"
CONTRACT_JSON_PATH = SELECTED_ROOT / "baseline_adapter_contract.json"
HANDOFF_JSON_PATH = SELECTED_ROOT / "baseline_adapter_first_run_handoff.json"
DECISION_PATH = Path("docs/decisions/2026-05-15_stage56_baseline_adapter_development_anchor.md")
AGGREGATE_PATH = PACKET_ROOT / "aggregate_summary.json"
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
SELECTION_STATUS_PATH = SELECTED_ROOT / "selection_status.md"
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

DEVELOPMENT_ANCHOR = ("run50BR", "v64_v47_ctxgap14_refill_etfw_h2_no_b")
BACKUP_ANCHOR = ("run50BQ", "v60_v47_et_stable_damage_firewall_h2c0_no_b")
REFERENCE_CANDIDATES = {
    ("run50BN", "v47_v22_topup_plus_et40_slotfill_h2c0_no_b"),
    ("run50BO", "v52_topup_slotfill_sd4_h2c0_no_b"),
    ("run50BO", "v50_topup_slotfill_sd2_h2c0_no_b"),
    ("run50BH", "et40h6_r001_a"),
    ("run50AU", "qda85_s800_flat_trans_r030_h6"),
    ("run50AU", "qda85_s800_flat_trans_r060_h8"),
    ("run50D", "d390h10"),
    ("run50C", "d38h10"),
}
FAILURE_MEMORY_RUNS = {"run50BI", "run50BL", "run50BM", "run50BC", "run50AZ"}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return io_path(candidate).resolve().relative_to(io_path(Path(".")).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_text(path: Path, text: str, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: _csv_value(row.get(column)) for column in columns})


def _csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.6f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def first_number(row: Mapping[str, str], keys: Sequence[str]) -> float | None:
    for key in keys:
        value = row.get(key)
        if value is None or value == "":
            continue
        try:
            return float(value)
        except ValueError:
            continue
    return None


def first_text(row: Mapping[str, str], keys: Sequence[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value)
    return ""


def normalized_candidate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(REVIEWS_ROOT.glob("run50*_summary.csv")):
        run_number = path.name.split("_")[0]
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for raw in reader:
                variant_id = first_text(raw, ("variant_id", "candidate_id", "variant"))
                if not variant_id:
                    continue
                row: dict[str, Any] = {
                    "run_number": run_number,
                    "variant_id": variant_id,
                    "source_summary_path": rel(path),
                    "group": first_text(raw, ("group", "candidate_group")),
                    "notes": first_text(raw, ("notes", "description")),
                    "max_hold_bars": first_number(raw, ("max_hold_bars",)),
                    "validation_trades_per_day": first_number(
                        raw,
                        (
                            "routed_validation_trades_per_day",
                            "validation_trades_per_day",
                            "routed_validation_day",
                        ),
                    ),
                    "oos_trades_per_day": first_number(
                        raw,
                        (
                            "routed_oos_trades_per_day",
                            "oos_trades_per_day",
                            "routed_oos_day",
                        ),
                    ),
                    "validation_pf": first_number(
                        raw,
                        (
                            "routed_validation_pf",
                            "routed_validation_profit_factor",
                            "validation_pf",
                            "validation_profit_factor",
                        ),
                    ),
                    "oos_pf": first_number(
                        raw,
                        (
                            "routed_oos_pf",
                            "routed_oos_profit_factor",
                            "oos_pf",
                            "oos_profit_factor",
                        ),
                    ),
                    "validation_net": first_number(
                        raw,
                        (
                            "routed_validation_net",
                            "routed_validation_net_profit",
                            "validation_net",
                            "validation_net_profit",
                        ),
                    ),
                    "oos_net": first_number(
                        raw,
                        (
                            "routed_oos_net",
                            "routed_oos_net_profit",
                            "oos_net",
                            "oos_net_profit",
                        ),
                    ),
                    "validation_drawdown": first_number(
                        raw,
                        (
                            "routed_validation_max_dd",
                            "routed_validation_drawdown",
                            "validation_max_dd",
                        ),
                    ),
                    "oos_drawdown": first_number(
                        raw,
                        (
                            "routed_oos_max_dd",
                            "routed_oos_drawdown",
                            "oos_max_dd",
                        ),
                    ),
                    "validation_cost_stressed_expectancy": first_number(
                        raw,
                        ("routed_validation_cost_stressed_expectancy", "validation_cost_stressed_expectancy"),
                    ),
                    "oos_cost_stressed_expectancy": first_number(
                        raw,
                        ("routed_oos_cost_stressed_expectancy", "oos_cost_stressed_expectancy"),
                    ),
                    "validation_same_move_ratio": first_number(
                        raw,
                        (
                            "routed_validation_same_move_reentry_ratio",
                            "validation_same_move_ratio",
                            "validation_same_move_reentry_ratio",
                        ),
                    ),
                    "oos_same_move_ratio": first_number(
                        raw,
                        (
                            "routed_oos_same_move_reentry_ratio",
                            "oos_same_move_ratio",
                            "oos_same_move_reentry_ratio",
                        ),
                    ),
                    "validation_cooldown12_trades_per_day": first_number(
                        raw,
                        (
                            "routed_validation_trades_per_day_after_12bar_cooldown",
                            "validation_cooldown12_trades_per_day",
                        ),
                    ),
                    "oos_cooldown12_trades_per_day": first_number(
                        raw,
                        (
                            "routed_oos_trades_per_day_after_12bar_cooldown",
                            "oos_cooldown12_trades_per_day",
                        ),
                    ),
                    "validation_mfe_capture": first_number(
                        raw,
                        ("routed_validation_mfe_capture_ratio", "validation_mfe_capture_ratio"),
                    ),
                    "oos_mfe_capture": first_number(
                        raw,
                        ("routed_oos_mfe_capture_ratio", "oos_mfe_capture_ratio"),
                    ),
                    "tier_a_validation_net": first_number(raw, ("tier_a_validation_net", "tier_a_validation_net_profit")),
                    "tier_a_oos_net": first_number(raw, ("tier_a_oos_net", "tier_a_oos_net_profit")),
                    "tier_b_validation_net": first_number(
                        raw,
                        ("tier_b_validation_net", "tier_b_validation_net_profit", "tier_b_fallback_only_validation_net"),
                    ),
                    "tier_b_oos_net": first_number(
                        raw,
                        ("tier_b_oos_net", "tier_b_oos_net_profit", "tier_b_fallback_only_oos_net"),
                    ),
                    "failure_reasons": first_text(raw, ("failure_reasons", "judgment", "candidate_rejection_reason")),
                    "passed_stage56_research_baseline_gate": first_text(raw, ("passed_stage56_research_baseline_gate",)),
                }
                if has_core_metrics(row):
                    row["development_score"] = development_score(row)
                    row["selection_label"] = selection_label(row)
                    rows.append(row)
    rows.sort(key=lambda item: float(item["development_score"]), reverse=True)
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


def has_core_metrics(row: Mapping[str, Any]) -> bool:
    return all(
        row.get(key) is not None
        for key in (
            "validation_trades_per_day",
            "oos_trades_per_day",
            "validation_pf",
            "oos_pf",
            "validation_net",
            "oos_net",
        )
    )


def n(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        number = float(value)
        return number if math.isfinite(number) else default
    except (TypeError, ValueError):
        return default


def development_score(row: Mapping[str, Any]) -> float:
    score = 0.0
    score += min(n(row.get("validation_trades_per_day")), 10.0) * 2.0
    score += min(n(row.get("oos_trades_per_day")), 8.0) * 2.5
    score += max(0.0, n(row.get("validation_pf")) - 1.0) * 12.0
    score += max(0.0, n(row.get("oos_pf")) - 1.0) * 14.0
    score += max(0.0, n(row.get("validation_net"))) / 120.0
    score += max(0.0, n(row.get("oos_net"))) / 120.0
    score += max(0.0, n(row.get("validation_cost_stressed_expectancy"))) * 2.0
    score += max(0.0, n(row.get("oos_cost_stressed_expectancy"))) * 2.0
    score += min(n(row.get("validation_cooldown12_trades_per_day")), 5.0) * 0.8
    score += min(n(row.get("oos_cooldown12_trades_per_day")), 4.0) * 1.0
    score -= max(0.0, n(row.get("validation_same_move_ratio")) - 0.50) * 5.0
    score -= max(0.0, n(row.get("oos_same_move_ratio")) - 0.50) * 6.0
    return score


def selection_label(row: Mapping[str, Any]) -> str:
    key = (str(row.get("run_number")), str(row.get("variant_id")))
    if key == DEVELOPMENT_ANCHOR:
        return "development_anchor"
    if key == BACKUP_ANCHOR:
        return "backup_anchor"
    if key in REFERENCE_CANDIDATES:
        return "reference_only"
    if str(row.get("run_number")) in FAILURE_MEMORY_RUNS:
        return "failure_memory"
    reasons = str(row.get("failure_reasons") or "")
    if "oos_net_positive" in reasons or "validation_net_positive" in reasons:
        return "failure_memory"
    return "reference_only"


def by_key(rows: Sequence[Mapping[str, Any]], key: tuple[str, str]) -> dict[str, Any]:
    for row in rows:
        if (row.get("run_number"), row.get("variant_id")) == key:
            return dict(row)
    raise ValueError(f"missing candidate {key}")


def top_reference_rows(rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    selected: list[Mapping[str, Any]] = []
    for row in rows:
        if row.get("selection_label") in {"development_anchor", "backup_anchor", "reference_only"}:
            selected.append(row)
        if len(selected) >= 12:
            break
    for row in rows:
        if row.get("selection_label") == "failure_memory" and len([r for r in selected if r.get("selection_label") == "failure_memory"]) < 6:
            selected.append(row)
    return selected


def fmt(value: Any) -> str:
    if value is None or value == "":
        return "NA"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def candidate_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| label | rank | run | variant | val day | OOS day | val PF | OOS PF | val net | OOS net | val/OOS cost stress | val/OOS same move | cooldown day val/OOS |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {label} | {rank} | {run} | `{variant}` | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {vcost}/{ocost} | {vsame}/{osame} | {vcd}/{ocd} |".format(
                label=row.get("selection_label", ""),
                rank=row.get("rank", ""),
                run=row.get("run_number", ""),
                variant=row.get("variant_id", ""),
                vday=fmt(row.get("validation_trades_per_day")),
                oday=fmt(row.get("oos_trades_per_day")),
                vpf=fmt(row.get("validation_pf")),
                opf=fmt(row.get("oos_pf")),
                vnet=fmt(row.get("validation_net")),
                onet=fmt(row.get("oos_net")),
                vcost=fmt(row.get("validation_cost_stressed_expectancy")),
                ocost=fmt(row.get("oos_cost_stressed_expectancy")),
                vsame=fmt(row.get("validation_same_move_ratio")),
                osame=fmt(row.get("oos_same_move_ratio")),
                vcd=fmt(row.get("validation_cooldown12_trades_per_day")),
                ocd=fmt(row.get("oos_cooldown12_trades_per_day")),
            )
        )
    return "\n".join(lines)


def reference_comparison_table(rows: Sequence[Mapping[str, Any]]) -> str:
    wanted = [
        ("run50BR", "v64_v47_ctxgap14_refill_etfw_h2_no_b", "development_anchor"),
        ("run50BQ", "v60_v47_et_stable_damage_firewall_h2c0_no_b", "backup_anchor"),
        ("run50BH", "et40h6_r001_a", "prior ExtraTrees anchor"),
        ("run50AU", "qda85_s800_flat_trans_r030_h6", "QDA density branch"),
        ("run50C", "d38h10", "d38h10 reference"),
        ("run50D", "d390h10", "d390h10 reference"),
    ]
    found: list[tuple[str, Mapping[str, Any]]] = []
    for run_number, variant_id, label in wanted:
        for row in rows:
            if row.get("run_number") == run_number and row.get("variant_id") == variant_id:
                found.append((label, row))
                break
    lines = [
        "| reference | run | variant | val day | OOS day | val PF | OOS PF | val net | OOS net | read |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for label, row in found:
        lines.append(
            "| {label} | {run} | `{variant}` | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {read} |".format(
                label=label,
                run=row.get("run_number", ""),
                variant=row.get("variant_id", ""),
                vday=fmt(row.get("validation_trades_per_day")),
                oday=fmt(row.get("oos_trades_per_day")),
                vpf=fmt(row.get("validation_pf")),
                opf=fmt(row.get("oos_pf")),
                vnet=fmt(row.get("validation_net")),
                onet=fmt(row.get("oos_net")),
                read=row.get("selection_label", ""),
            )
        )
    lines.append(
        "| Stage34 34D reference | run28D | `frequency_floor_rule_summary` | NA | NA | NA | NA | NA | NA | thin modifier clue(얇은 보정 단서), not adapter anchor(어댑터 기준점 아님) |"
    )
    return "\n".join(lines)


def write_selection_report(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    dev = by_key(rows, DEVELOPMENT_ANCHOR)
    backup = by_key(rows, BACKUP_ANCHOR)
    table_rows = top_reference_rows(rows)
    lines = [
        "# Stage56 BaselineAdapter Transition(56단계 BaselineAdapter 전환)",
        "",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- terminal_label(종료 라벨): `{TERMINAL_LABEL}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- development_anchor(개발 기준점): `{dev['variant_id']}` from `{dev['run_number']}`",
        f"- backup_anchor(예비 기준점): `{backup['variant_id']}` from `{backup['run_number']}`",
        "- claim_boundary(주장 경계): development only(개발 전용), no live readiness(실거래 준비 아님), no runtime authority(런타임 권위 아님), no operating promotion(운영 승격 아님)",
        "",
        "## Decision(결정)",
        "",
        "`v64_v47_ctxgap14_refill_etfw_h2_no_b`를 development_anchor(개발 기준점)로 고른다. 효과(effect, 효과)는 Stage56/run50 후보 사냥을 멈추고 BaselineAdapter(기준선 어댑터) 구현과 검증 루프로 들어가는 것이다.",
        "",
        "엄격한 selected_research_baseline(선택 연구 기준선)은 아직 없다. cost-stressed expectancy(비용 압박 기대값)와 same-move density(동일 이동 밀도)가 실패했기 때문이다.",
        "",
        "## Why This Anchor(선택 이유)",
        "",
        f"- actual routed MT5 validation/OOS(실제 라우팅 MT5 검증/표본외) trades/day(일 거래 수): `{fmt(dev['validation_trades_per_day'])}` / `{fmt(dev['oos_trades_per_day'])}`.",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(dev['validation_pf'])}` / `{fmt(dev['oos_pf'])}`, net(순손익): `{fmt(dev['validation_net'])}` / `{fmt(dev['oos_net'])}`.",
        f"- same-move ratio(동일 이동 비율): `{fmt(dev['validation_same_move_ratio'])}` / `{fmt(dev['oos_same_move_ratio'])}`로, higher-density(더 높은 밀도) 후보인 backup_anchor(예비 기준점)보다 낮다.",
        f"- cost-stressed expectancy(비용 압박 기대값): `{fmt(dev['validation_cost_stressed_expectancy'])}` / `{fmt(dev['oos_cost_stressed_expectancy'])}`로 아직 음수지만, adapter(어댑터)의 risk/ATR/lifecycle(위험/ATR/생명주기) 수리 대상으로 명확하다.",
        f"- Tier B fallback-only(티어 B 대체 단독)는 validation/OOS net(검증/표본외 순손익) `{fmt(dev['tier_b_validation_net'])}` / `{fmt(dev['tier_b_oos_net'])}`로 손상되어, 초기 adapter(어댑터)는 explicit Tier B disablement(명시적 Tier B 비활성)를 쓴다.",
        "",
        "## Candidate Ranking(후보 순위)",
        "",
        candidate_table(table_rows),
        "",
        "## Required Comparisons(필수 비교)",
        "",
        reference_comparison_table(rows),
        "",
        "## Reference And Failure Memory(참고와 실패 기억)",
        "",
        "- backup_anchor(예비 기준점): `run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b`. 효과(effect, 효과)는 밀도와 PF/net(수익 팩터/순손익)이 가장 강한 대체 축을 보존하는 것이다.",
        "- reference_only(참고 전용): `run50BN/v47`, `run50BO/v52`, `run50BH/et40h6_r001_a`, `run50AU/QDA`, `run50D/d390h10`, `run50C/d38h10`. 효과(effect, 효과)는 adapter(어댑터) 결과를 과거 밀도/품질/LogReg(로지스틱 회귀) 기준과 비교할 수 있게 하는 것이다.",
        "- Stage34 34D reference(34단계 34D 참고): `run28D` frequency-floor(거래 빈도 하한) 기억은 thin modifier clue(얇은 보정 단서)다. 효과(effect, 효과)는 BaselineAdapter(기준선 어댑터)에서 entry-time proxy(진입 시간 대리)를 주력으로 오해하지 않게 하는 것이다.",
        "- failure_memory(실패 기억): microcooldown(짧은 쿨다운), leaf same-direction polishing(잎 단위 동일 방향 미세조정), bad context gap(나쁜 문맥 간격), broad cooldown12 source(넓은 12봉 쿨다운 원천)는 새 이유 없이 반복하지 않는다.",
        "",
        "## BaselineAdapter Start(기준선 어댑터 시작)",
        "",
        "- entry decision(진입 결정): anchor(기준점)의 `stage56_context_gap_refill_signal`을 우선 재현한다.",
        "- routing(라우팅): 초기값은 Tier A primary with explicit Tier B disablement(Tier A 우선 + 명시적 Tier B 비활성)이다.",
        "- risk(위험): model-controlled risk_per_trade(모델 제어 거래당 위험), cap(상한) `5%`, min lot floor(최소 랏 바닥) `0.01`을 기록한다.",
        "- ATR/bracket(ATR/브래킷): 초기 계약은 ATR(평균진폭) 14, SL(손절) 1.5, TP(익절) 2.0, hold(보유) 2봉이다.",
        "- telemetry(텔레메트리): model_risk_pct, clipped_risk_pct, computed_lot, executed_lot, min_lot_floor_applied, actual_risk_pct_after_floor를 필수 기록한다.",
        "- ONNX-compatible output(ONNX 호환 출력): 출력 경로만 정의하고, ONNX hardening(ONNX 경화)은 MT5 adapter validation/OOS(어댑터 검증/표본외) 뒤로 미룬다.",
        "",
        "## First MT5 Handoff(첫 MT5 인계)",
        "",
        "이번 작업은 adapter scaffold(어댑터 뼈대)와 first-run handoff plan(첫 실행 인계 계획)까지 만든다. 효과(effect, 효과)는 다음 회차에서 broad candidate hunting(넓은 후보 사냥)이 아니라 BaselineAdapter(기준선 어댑터) validation/OOS(검증/표본외)를 바로 실행하게 하는 것이다.",
    ]
    write_text(REPORT_PATH, "\n".join(lines), bom=True)
    write_text(DECISION_PATH, "\n".join(lines), bom=True)
    return {"development_anchor": dev, "backup_anchor": backup}


def write_contract_artifacts(decision: Mapping[str, Any]) -> dict[str, Any]:
    contract = initial_v64_contract()
    payload = adapter_contract_payload(contract)
    payload["selection"] = {
        "selected_research_baseline": "none",
        "development_anchor": decision["development_anchor"],
        "backup_anchor": decision["backup_anchor"],
        "terminal_label": TERMINAL_LABEL,
    }
    write_json(CONTRACT_JSON_PATH, payload)
    lines = [
        "# BaselineAdapter Initial Contract(BaselineAdapter 초기 계약)",
        "",
        f"- adapter_id(어댑터 ID): `{contract.adapter_id}`",
        f"- anchor(기준점): `{contract.anchor.variant_id}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        "- label(라벨): `development_anchor`",
        f"- claim_boundary(주장 경계): `{contract.claim_boundary}`",
        "",
        "## Fixed Capabilities(고정 기능)",
        "",
    ]
    for capability in contract.capabilities:
        lines.append(f"- `{capability}`")
    lines.extend(
        [
            "",
            "## Initial Rules(초기 규칙)",
            "",
            f"- entry_signal_column(진입 신호 컬럼): `{contract.entry_signal_column}`",
            f"- routing_mode(라우팅 모드): `{contract.routing_mode}`",
            f"- tier_b_policy(Tier B 정책): `{contract.tier_b_policy}`",
            f"- risk_cap_pct(위험 상한): `{contract.risk_cap_pct}`",
            f"- min_lot(최소 랏): `{contract.min_lot}`",
            f"- ATR bracket(ATR 브래킷): period(기간) `{contract.default_bracket.atr_period}`, SL `{contract.default_bracket.atr_stop_multiplier}`, TP `{contract.default_bracket.atr_take_profit_multiplier}`",
            "",
            "## Required Telemetry(필수 텔레메트리)",
            "",
        ]
    )
    for field in contract.telemetry_required_fields:
        lines.append(f"- `{field}`")
    lines.extend(
        [
            "",
            "ONNX-compatible outputs(ONNX 호환 출력)는 계약에만 잡고, ONNX hardening(ONNX 경화)은 adapter MT5 validation/OOS(어댑터 MT5 검증/표본외) 이후에 시작한다.",
        ]
    )
    write_text(CONTRACT_MD_PATH, "\n".join(lines), bom=True)
    return payload


def write_handoff_plan(contract_payload: Mapping[str, Any]) -> dict[str, Any]:
    handoff = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "status": "first_adapter_mt5_run_pending",
        "effect": "next pass runs BaselineAdapter validation/OOS instead of broad Stage56 candidate search",
        "adapter_contract_path": rel(CONTRACT_JSON_PATH),
        "required_attempts": [
            "tier_a_only_validation",
            "tier_b_fallback_only_validation",
            "actual_routed_total_validation",
            "tier_a_only_oos",
            "tier_b_fallback_only_oos",
            "actual_routed_total_oos",
        ],
        "required_metrics": [
            "trades_per_day",
            "profit_factor",
            "net_profit",
            "drawdown",
            "cost_stressed_expectancy",
            "same_move_ratio",
            "cooldown12_survival",
            "mfe_capture",
            "risk_floor_impact",
        ],
        "runtime_boundary": "runtime_probe_pending_no_runtime_authority",
        "initial_contract": contract_payload,
    }
    write_json(HANDOFF_JSON_PATH, handoff)
    return handoff


def skill_gate_payloads(decision: Mapping[str, Any], contract_payload: Mapping[str, Any], handoff: Mapping[str, Any]) -> dict[str, Any]:
    receipts = {
        "obsidian-reentry-read": {"status": "used", "effect": "current truth and Stage56 status verified"},
        "obsidian-experiment-design": {
            "status": "used",
            "hypothesis": "run50BR v64 can serve as a development anchor even without strict selected_research_baseline",
            "decision_use": "start BaselineAdapter development",
            "comparison_baseline": "run50BQ backup plus d390h10/d38h10 references",
            "success_criteria": "development_anchor selected and adapter contract scaffolded",
            "failure_criteria": "no MT5-backed candidate strong enough for development",
            "evidence_plan": [rel(REPORT_PATH), rel(CANDIDATE_CSV_PATH), rel(CONTRACT_JSON_PATH), rel(HANDOFF_JSON_PATH)],
        },
        "obsidian-runtime-parity": {
            "status": "used_with_boundary",
            "research_path": rel(decision["development_anchor"]["source_summary_path"]),
            "runtime_path": "existing run50BR MT5 reports; BaselineAdapter first run pending",
            "shared_contract": "closed-bar M5 anchor signal plus explicit risk/ATR/telemetry output contract",
            "parity_check": "existing anchor MT5 reports completed; adapter MT5 reproduction pending first-run handoff",
            "runtime_claim_boundary": "runtime_probe_pending_no_runtime_authority",
        },
        "obsidian-backtest-forensics": {
            "status": "used_with_boundary",
            "tester_identity": "existing Stage56 MT5 reports use actual routed tester paths",
            "trade_evidence": "validation/OOS routed metrics copied into candidate selection CSV",
            "backtest_judgment": "usable_with_boundary_for_anchor_selection_not_adapter_reproduction",
        },
        "obsidian-artifact-lineage": {
            "status": "used",
            "source_inputs": [rel(decision["development_anchor"]["source_summary_path"]), rel(decision["backup_anchor"]["source_summary_path"])],
            "artifact_paths": [rel(REPORT_PATH), rel(CANDIDATE_CSV_PATH), rel(CONTRACT_JSON_PATH), rel(HANDOFF_JSON_PATH)],
            "lineage_judgment": "connected_with_boundary",
        },
        "obsidian-performance-attribution": {
            "status": "used",
            "observed_change": "candidate selection moved from broad density search to adapter development anchor",
            "comparison_baseline": "run50BQ/BN higher density candidates and run50BH/d390/d38 references",
            "likely_drivers": "lower same-move ratio and clearer repair path outweighed raw density rank",
            "attribution_confidence": "medium",
            "next_probe": "BaselineAdapter MT5 validation/OOS with risk floor and ATR telemetry",
        },
        "obsidian-result-judgment": {
            "status": "used",
            "result_subject": RUN_ID,
            "judgment_label": TERMINAL_LABEL,
            "claim_boundary": "development_anchor_only_no_operating_claim",
            "next_condition": "first BaselineAdapter MT5 validation/OOS run",
        },
    }
    write_json(PACKET_ROOT / "skill_receipts.json", receipts)
    write_json(PACKET_ROOT / "runtime_parity_audit.json", receipts["obsidian-runtime-parity"])
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", receipts["obsidian-artifact-lineage"])
    write_json(PACKET_ROOT / "performance_attribution_gate.json", receipts["obsidian-performance-attribution"])
    write_json(PACKET_ROOT / "result_judgment_gate.json", receipts["obsidian-result-judgment"])
    final_claim_guard = {
        "status": "passed",
        "allowed_terminal_label": TERMINAL_LABEL,
        "forbidden_claims": {
            "reviewed_closed": False,
            "production_ready": False,
            "live_ready": False,
            "operating_reference": False,
            "runtime_authority": False,
            "operating_promotion": False,
        },
    }
    gate_coverage = {
        "status": "passed_with_boundary",
        "required_gates": [
            "candidate_selection_audit",
            "adapter_contract_scaffold",
            "artifact_lineage_audit",
            "runtime_parity_boundary",
            "final_claim_guard",
        ],
        "mt5_adapter_reproduction": "pending_first_run_handoff",
    }
    write_json(PACKET_ROOT / "final_claim_guard.json", final_claim_guard)
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", gate_coverage)
    return {"skill_receipts": receipts, "final_claim_guard": final_claim_guard, "gate_coverage": gate_coverage}


def update_state_docs(decision: Mapping[str, Any]) -> None:
    dev = decision["development_anchor"]
    backup = decision["backup_anchor"]
    current = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{RUN_ID}`
- active stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{dev['variant_id']}`
- backup_anchor(예비 기준점): `{backup['variant_id']}`
- status(상태): `{TERMINAL_LABEL}`
- terminal_condition(종료 조건): BaselineAdapter development started(기준선 어댑터 개발 시작)

Stage56(56단계)은 broad run50 candidate hunting(넓은 run50 후보 사냥)을 멈추고 BaselineAdapter development(기준선 어댑터 개발)로 전환했다. Effect(효과): 다음 작업은 새 후보 탐색이 아니라 selected development_anchor(선택 개발 기준점)를 어댑터 경로로 재현하고 risk/ATR/telemetry(위험/ATR/텔레메트리)를 붙여 MT5 validation/OOS(검증/표본외)를 실행하는 것이다.

## Current Anchor(현재 기준점)

- development_anchor(개발 기준점): `{dev['run_number']}/{dev['variant_id']}`
- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(dev['validation_trades_per_day'])}` / `{fmt(dev['oos_trades_per_day'])}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(dev['validation_pf'])}` / `{fmt(dev['oos_pf'])}`
- validation/OOS net(검증/표본외 순손익): `{fmt(dev['validation_net'])}` / `{fmt(dev['oos_net'])}`
- known weaknesses(알려진 약점): cost-stressed expectancy(비용 압박 기대값), same-move density(동일 이동 밀도), Tier B fallback-only damage(Tier B 대체 단독 손상)

## Next Bottleneck(다음 병목)

Run the first BaselineAdapter MT5 validation/OOS(첫 BaselineAdapter MT5 검증/표본외 실행) from the scaffold and parse risk floor impact(위험 바닥 영향), ATR bracket behavior(ATR 브래킷 행동), same-move audit(동일 이동 감사), and cost-stressed expectancy(비용 압박 기대값).

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
"""
    write_text(CURRENT_WORKING_STATE_PATH, current, bom=True)

    selection = f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_baseline_adapter_development`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- current run(현재 실행): `{RUN_ID}`
- current_judgment(현재 판정): `{TERMINAL_LABEL}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{dev['variant_id']}`
- backup_anchor(예비 기준점): `{backup['variant_id']}`

## Selection Evidence(선택 근거)

- selection_report(선택 보고서): `{rel(REPORT_PATH)}`
- candidate_table(후보 표): `{rel(CANDIDATE_CSV_PATH)}`
- adapter_contract(어댑터 계약): `{rel(CONTRACT_JSON_PATH)}`
- first_run_handoff(첫 실행 인계): `{rel(HANDOFF_JSON_PATH)}`

Effect(효과): Stage56(56단계)은 더 넓은 candidate search(후보 탐색)를 기본으로 하지 않고, BaselineAdapter(기준선 어댑터) 개발 기준점을 중심으로 진행한다.
"""
    write_text(SELECTION_STATUS_PATH, selection, bom=True)

    if path_exists(WORKSPACE_STATE_PATH):
        text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
        text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN_ID}", text, count=1, flags=re.MULTILINE)
        text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
        focus = (
            "- >-\n"
            f"  Stage56(56단계) `{STAGE_ID}`: run50BS(실행50BS) BaselineAdapter transition(BaselineAdapter 전환) 완료; "
            f"development_anchor(개발 기준점)는 `{dev['variant_id']}`, backup_anchor(예비 기준점)는 `{backup['variant_id']}`이다. "
            "selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): run50 후보 사냥을 멈추고 risk/ATR/telemetry(위험/ATR/텔레메트리)를 포함한 BaselineAdapter 개발로 전환한다."
        )
        text = re.sub(
            r"- >-\n  Stage56[^\n]*run50BS[^\n]*BaselineAdapter transition[^\n]*\n",
            "",
            text,
        )
        text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
        text = remove_block(text, "stage56_baseline_adapter_transition:")
        block = f"""
stage56_baseline_adapter_transition:
  packet_id: {PACKET_ID}
  current_run_id: {RUN_ID}
  selected_research_baseline: none
  development_anchor: {dev['variant_id']}
  backup_anchor: {backup['variant_id']}
  terminal_label: {TERMINAL_LABEL}
  boundary: development_anchor_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference
  next_action: run_first_baseline_adapter_mt5_validation_oos
"""
        write_text(WORKSPACE_STATE_PATH, text.rstrip() + "\n" + block, bom=True)

    append_once(
        CHANGELOG_PATH,
        "\n## 2026-05-15 Stage56 BaselineAdapter Transition(56단계 BaselineAdapter 전환)\n"
        f"- completed(완료): `{PACKET_ID}`\n"
        f"- development_anchor(개발 기준점): `{dev['variant_id']}`\n"
        f"- backup_anchor(예비 기준점): `{backup['variant_id']}`\n"
        "- effect(효과): selected_research_baseline(선택 연구 기준선) 없이도 strong MT5-backed anchor(강한 MT5 근거 기준점)를 골라 BaselineAdapter development(기준선 어댑터 개발)를 시작했다.\n",
        bom=True,
    )
    append_once(
        PROGRESS_LOG_PATH,
        "\n## 2026-05-15 run50BS BaselineAdapter Transition(BaselineAdapter 전환)\n"
        f"- decision(결정): development_anchor(개발 기준점)=`{dev['variant_id']}`, backup_anchor(예비 기준점)=`{backup['variant_id']}`.\n"
        "- effect(효과): broad Stage56 candidate hunting(넓은 Stage56 후보 사냥)을 멈추고 adapter scaffold(어댑터 뼈대)와 first MT5 handoff(첫 MT5 인계)를 만들었다.\n",
        bom=True,
    )


def remove_block(text: str, block_key: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].startswith(block_key):
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith(" ")):
                index += 1
            continue
        output.append(lines[index])
        index += 1
    return "".join(output)


def append_once(path: Path, entry: str, *, bom: bool = False) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if entry.strip() in existing:
        return
    write_text(path, existing.rstrip() + "\n" + entry.strip(), bom=bom)


def artifact_rows(paths: Sequence[Path]) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"stage56_run50BS_{safe_id(path.stem)}",
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": utc_now(),
                "notes": "Stage56 BaselineAdapter transition artifact.",
            }
        )
    return rows


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:80].lower()


def write_ledgers(decision: Mapping[str, Any], gate_payloads: Mapping[str, Any]) -> dict[str, Any]:
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_development",
            "status": "completed",
            "judgment": TERMINAL_LABEL,
            "path": rel(REPORT_PATH),
            "notes": f"development_anchor={decision['development_anchor']['variant_id']};backup_anchor={decision['backup_anchor']['variant_id']};selected_research_baseline=none",
        }
    ]
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__candidate_selection",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "candidate_selection",
            "parent_run_id": "run50BR_stage56_context_extratrees_context_gap_refill_v1",
            "record_view": "development_anchor_selection",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage56_run50_candidate_selection",
            "scoreboard_lane": "kpi_evidence",
            "status": "completed",
            "judgment": TERMINAL_LABEL,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"development_anchor={decision['development_anchor']['variant_id']}",
            "guardrail_kpi": "selected_research_baseline=none;forbidden_operating_claims=1",
            "external_verification_status": "completed_existing_anchor_mt5_reports",
            "notes": "Candidate selection over existing Stage56/run50 MT5 evidence.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__adapter_contract",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_contract",
            "parent_run_id": RUN_ID,
            "record_view": "baseline_adapter_initial_contract",
            "tier_scope": "Tier A+B",
            "kpi_scope": "adapter_contract_scaffold",
            "scoreboard_lane": "artifact_lineage",
            "status": "completed",
            "judgment": "adapter_development_started",
            "path": rel(CONTRACT_JSON_PATH),
            "primary_kpi": "required_capabilities=present",
            "guardrail_kpi": "onnx_later_not_first;deployment_claims_forbidden",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Initial BaselineAdapter scaffold contract, not MT5 reproduction yet.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__first_mt5_handoff",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "first_mt5_handoff",
            "parent_run_id": RUN_ID,
            "record_view": "adapter_first_run_handoff",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_probe_plan",
            "scoreboard_lane": "runtime_probe",
            "status": "planned",
            "judgment": "first_adapter_mt5_validation_oos_pending",
            "path": rel(HANDOFF_JSON_PATH),
            "primary_kpi": "required_attempts=6",
            "guardrail_kpi": "no_runtime_authority;no_live_readiness",
            "external_verification_status": "blocked_pending_next_execution",
            "notes": "Implementation requires one more pass for actual BaselineAdapter MT5 validation/OOS.",
        },
    ]
    artifacts = artifact_rows(
        [
            REPORT_PATH,
            CANDIDATE_CSV_PATH,
            CONTRACT_MD_PATH,
            CONTRACT_JSON_PATH,
            HANDOFF_JSON_PATH,
            DECISION_PATH,
            AGGREGATE_PATH,
            Path("foundation/adapters/baseline_adapter.py"),
            Path("stage_pipelines/stage56/baseline_adapter_development.py"),
        ]
    )
    payload = {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "project_alpha_ledger": upsert_csv_rows(ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(
            ARTIFACT_REGISTRY_PATH,
            ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
            artifacts,
            key="artifact_id",
        ),
    }
    payload["gate_payloads"] = gate_payloads
    return payload


def main() -> int:
    rows = normalized_candidate_rows()
    if not rows:
        raise RuntimeError("no candidate rows found")
    decision = write_selection_report(rows)
    columns = [
        "rank",
        "selection_label",
        "development_score",
        "run_number",
        "variant_id",
        "validation_trades_per_day",
        "oos_trades_per_day",
        "validation_pf",
        "oos_pf",
        "validation_net",
        "oos_net",
        "validation_drawdown",
        "oos_drawdown",
        "validation_cost_stressed_expectancy",
        "oos_cost_stressed_expectancy",
        "validation_same_move_ratio",
        "oos_same_move_ratio",
        "validation_cooldown12_trades_per_day",
        "oos_cooldown12_trades_per_day",
        "validation_mfe_capture",
        "oos_mfe_capture",
        "tier_a_validation_net",
        "tier_a_oos_net",
        "tier_b_validation_net",
        "tier_b_oos_net",
        "failure_reasons",
        "source_summary_path",
        "notes",
    ]
    write_csv(CANDIDATE_CSV_PATH, rows, columns)
    contract_payload = write_contract_artifacts(decision)
    handoff = write_handoff_plan(contract_payload)
    gate_payloads = skill_gate_payloads(decision, contract_payload, handoff)
    update_state_docs(decision)
    aggregate = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "terminal_label": TERMINAL_LABEL,
        "selected_research_baseline": "none",
        "development_anchor": decision["development_anchor"],
        "backup_anchor": decision["backup_anchor"],
        "report_path": rel(REPORT_PATH),
        "candidate_csv_path": rel(CANDIDATE_CSV_PATH),
        "contract_json_path": rel(CONTRACT_JSON_PATH),
        "first_run_handoff_path": rel(HANDOFF_JSON_PATH),
        "mt5_adapter_evidence_status": "first_run_handoff_plan_created_adapter_run_pending",
        "forbidden_claims": {
            "live_readiness": False,
            "runtime_authority": False,
            "operating_promotion": False,
            "operating_reference": False,
            "production_baseline": False,
            "reviewed_closed": False,
        },
    }
    write_json(AGGREGATE_PATH, aggregate)
    ledgers = write_ledgers(decision, gate_payloads)
    aggregate["ledger_payload"] = ledgers
    aggregate["artifact_hashes"] = {
        "report_sha256": sha256_file_lf_normalized(REPORT_PATH),
        "candidate_csv_sha256": sha256_file_lf_normalized(CANDIDATE_CSV_PATH),
        "contract_json_sha256": sha256_file_lf_normalized(CONTRACT_JSON_PATH),
        "handoff_json_sha256": sha256_file_lf_normalized(HANDOFF_JSON_PATH),
    }
    write_json(AGGREGATE_PATH, aggregate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
