from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
RUN_ID = "run272D_review_time_risk_router_mt5_probe_v1"
SOURCE_RUN_ID = "run272C_time_risk_router_mt5_signal_replay_v1"
STATUS = "completed_time_risk_router_mt5_probe_review_no_candidate_selection"
JUDGMENT = "q04_pressure_survivor_for_stability_validation_no_candidate_selection"
NEXT_ACTION = "open_stage273_time_risk_router_stability_validation"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN272C = STAGE / "02_runs" / "run272C"
RUN_DIR = STAGE / "02_runs" / "run272D"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

KPI_SUMMARY = RUN272C / "mt5_kpi_summary.csv"
RUNTIME_SUPPLY = RUN272C / "runtime_supply_matrix.csv"
BACKTEST_FORENSICS = RUN272C / "backtest_forensics.csv"
RUN272C_MANIFEST = RUN272C / "run_manifest.json"
RUN272C_LINEAGE = RUN272C / "artifact_lineage_receipt.json"
RUN272C_REPORT = REVIEWS / "run272C_report.md"

PRESSURE_REVIEW = RUN_DIR / "pressure_survivor_review.csv"
SURVIVOR_QUEUE = RUN_DIR / "stage273_stability_queue.csv"
FAILURE_MEMORY = RUN_DIR / "pressure_failure_memory.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run272D_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
IDEA_REGISTER = ROOT / "docs/registers/idea_registry.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def remove_focus_items(text: str, marker: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("current_focus:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "-")):
            end = index
            break
    focus_lines = lines[start + 1:end]
    kept: list[str] = []
    index = 0
    while index < len(focus_lines):
        line = focus_lines[index]
        if not line.startswith("- >-"):
            kept.append(line)
            index += 1
            continue
        block_end = index + 1
        while block_end < len(focus_lines) and not focus_lines[block_end].startswith("- >-"):
            block_end += 1
        block = focus_lines[index:block_end]
        if not any(marker in block_line for block_line in block):
            kept.extend(block)
        index = block_end
    return "\n".join([*lines[: start + 1], *kept, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def variant_token(record_view: str) -> str:
    match = pd.Series([record_view]).str.extract(r"mt5_(q\d+)").iloc[0, 0]
    return str(match)


def classify_variant(row: Mapping[str, Any]) -> tuple[str, str]:
    token = str(row["variant"])
    val_pf = float(row["validation_profit_factor"])
    oos_pf = float(row["oos_profit_factor"])
    val_net = float(row["validation_net_profit"])
    oos_net = float(row["oos_net_profit"])
    oos_trades = int(row["oos_trade_count"])
    max_dd = float(row["max_drawdown_percent_max"])
    if token == "q01":
        return "reference_control_only", "base router is reference evidence only, not a candidate."
    if val_pf >= 1.10 and oos_pf >= 1.10 and val_net > 0 and oos_net > 0 and oos_trades >= 300:
        if max_dd >= 35.0:
            return "pressure_survivor_with_drawdown_watch", "PF and expectancy survived but drawdown remains a stability gate."
        return "pressure_survivor_for_stability_validation", "PF, net, expectancy, and trade count survived first runtime pressure."
    if val_net > 0 and oos_net > 0:
        return "watch_but_not_survivor_due_to_pf_or_dd", "Net stayed positive but PF/drawdown quality is not strong enough."
    return "failure_memory_runtime_probe", "Runtime KPI did not survive basic positive-net pressure."


def build_review_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    kpi = pd.read_csv(io_path(KPI_SUMMARY))
    supply = pd.read_csv(io_path(RUNTIME_SUPPLY))
    if kpi.empty:
        raise ValueError("run272C KPI summary is empty.")
    kpi["variant"] = kpi["record_view"].map(variant_token)
    grouped_rows: list[dict[str, Any]] = []
    for (variant, tier_scope), group in kpi.groupby(["variant", "tier_scope"], dropna=False):
        val = group[group["split"].eq("validation_is")].iloc[0]
        oos = group[group["split"].eq("oos")].iloc[0]
        row = {
            "variant": variant,
            "tier_scope": tier_scope,
            "validation_net_profit": float(val["net_profit"]),
            "oos_net_profit": float(oos["net_profit"]),
            "net_profit_sum": round(float(val["net_profit"]) + float(oos["net_profit"]), 2),
            "validation_profit_factor": float(val["profit_factor"]),
            "oos_profit_factor": float(oos["profit_factor"]),
            "profit_factor_min": min(float(val["profit_factor"]), float(oos["profit_factor"])),
            "validation_trade_count": int(val["trade_count"]),
            "oos_trade_count": int(oos["trade_count"]),
            "trade_count_sum": int(val["trade_count"]) + int(oos["trade_count"]),
            "validation_expectancy": float(val["expectancy"]),
            "oos_expectancy": float(oos["expectancy"]),
            "expectancy_min": min(float(val["expectancy"]), float(oos["expectancy"])),
            "validation_max_drawdown_percent": float(val["max_drawdown_percent"]),
            "oos_max_drawdown_percent": float(oos["max_drawdown_percent"]),
            "max_drawdown_percent_max": max(float(val["max_drawdown_percent"]), float(oos["max_drawdown_percent"])),
            "validation_win_rate_percent": float(val["win_rate_percent"]),
            "oos_win_rate_percent": float(oos["win_rate_percent"]),
            "report_path_validation": val["report_path"],
            "report_path_oos": oos["report_path"],
            "claim_boundary": BOUNDARY,
        }
        decision, reason = classify_variant(row)
        row["review_decision"] = decision
        row["review_reason"] = reason
        grouped_rows.append(row)

    survivor_rows = []
    failure_rows = []
    supply_index = supply.groupby(["variant_id", "tier_scope"], dropna=False).agg(
        nonflat_signal_count=("nonflat_signal_count", "sum"),
        long_signal_count=("long_signal_count", "sum"),
        short_signal_count=("short_signal_count", "sum"),
        rows=("rows", "sum"),
    ).reset_index()
    for row in grouped_rows:
        token = row["variant"]
        if row["review_decision"].startswith("pressure_survivor"):
            variant_id = {
                "q04": "run272A_q04_weak_clock_throttle_router",
            }.get(str(token), str(token))
            match = supply_index[(supply_index["variant_id"].astype(str).str.contains(str(token))) & (supply_index["tier_scope"].eq(row["tier_scope"]))]
            if not match.empty:
                supply_row = match.iloc[0]
                signal_mix = {
                    "nonflat_signal_count": int(supply_row["nonflat_signal_count"]),
                    "long_signal_count": int(supply_row["long_signal_count"]),
                    "short_signal_count": int(supply_row["short_signal_count"]),
                    "rows": int(supply_row["rows"]),
                }
            else:
                signal_mix = {}
            survivor_rows.append(
                {
                    "survivor_id": f"run272D_{token}_{str(row['tier_scope']).lower().replace(' ', '_')}",
                    "variant": token,
                    "variant_id": variant_id,
                    "tier_scope": row["tier_scope"],
                    "next_stage_role": "stability_validation_seed",
                    "survivor_boundary": "pressure_survivor_not_selected_candidate",
                    "net_profit_sum": row["net_profit_sum"],
                    "profit_factor_min": row["profit_factor_min"],
                    "expectancy_min": row["expectancy_min"],
                    "trade_count_sum": row["trade_count_sum"],
                    "max_drawdown_percent_max": row["max_drawdown_percent_max"],
                    "signal_mix_json": json.dumps(signal_mix, ensure_ascii=False, sort_keys=True),
                    "required_next_evidence": "balance/equity_curve_zoom;month_session_slice;Tier A/B stability;Adapter identity check",
                    "claim_boundary": BOUNDARY,
                }
            )
        else:
            failure_rows.append(
                {
                    "variant": token,
                    "tier_scope": row["tier_scope"],
                    "failure_memory_label": row["review_decision"],
                    "reason": row["review_reason"],
                    "net_profit_sum": row["net_profit_sum"],
                    "profit_factor_min": row["profit_factor_min"],
                    "trade_count_sum": row["trade_count_sum"],
                    "max_drawdown_percent_max": row["max_drawdown_percent_max"],
                    "claim_boundary": BOUNDARY,
                }
            )
    return grouped_rows, survivor_rows, failure_rows


def write_report(review_rows: Sequence[Mapping[str, Any]], survivor_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    lines = "\n".join(
        f"- `{row['variant']}` `{row['tier_scope']}`: net_sum(순수익 합) `{row['net_profit_sum']}`, PF_min(최소 수익 팩터) `{row['profit_factor_min']}`, trades(거래 수) `{row['trade_count_sum']}`, DD_max(최대 손실폭) `{row['max_drawdown_percent_max']}`, decision(결정) `{row['review_decision']}`"
        for row in review_rows
    )
    survivor_lines = "\n".join(
        f"- `{row['variant']}` `{row['tier_scope']}`: `{row['survivor_boundary']}`, next(다음) `{row['next_stage_role']}`"
        for row in survivor_rows
    ) or "- none(없음)"
    failure_lines = "\n".join(
        f"- `{row['variant']}` `{row['tier_scope']}`: `{row['failure_memory_label']}`"
        for row in failure_rows
    ) or "- none(없음)"
    write_md(
        RUN_REPORT,
        f"""# run272D Time-Risk Router MT5 Probe Review(272D 시간 위험 라우터 MT5 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- survivor_rows(생존 행): `{len(survivor_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run272D(272D 실행)는 run272C(272C 실행)의 MT5(`MetaTrader 5`, 메타트레이더5) KPI(핵심 성과 지표)를 Tier A/Tier B(티어 A/티어 B) 쌍으로 다시 읽었다.
효과(effect, 효과): q04(4번 분기)는 stability validation seed(안정성 검증 씨앗)로 남기고, q01~q03(1~3번 분기)은 대조 또는 failure memory(실패 기억)로 둔다.

## Review Table(검토 표)

{lines}

## Survivors(생존 분기)

{survivor_lines}

## Failure Memory(실패 기억)

{failure_lines}

## Boundary(경계)

q04(4번 분기)는 pressure survivor(압박 생존 분기)일 뿐 selected candidate(선택 후보)가 아니다.
효과(effect, 효과): 다음 Stage273(273단계) stability validation(안정성 검증)이 q04(4번 분기)를 더 깨뜨리거나 좁힐 수 있다.

`{BOUNDARY}`
""",
    )


def update_ledgers(review_rows: Sequence[Mapping[str, Any]], survivor_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_probe_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"survivor_rows={len(survivor_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{str(row['variant']).lower()}_{str(row['tier_scope']).lower().replace(' ', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{row['variant']}_{str(row['tier_scope']).lower().replace(' ', '_')}",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": f"MT5 probe review {row['variant']} {row['tier_scope']}",
            "tier_scope": row["tier_scope"],
            "kpi_scope": "mt5_runtime_probe_review",
            "scoreboard_lane": "runtime_probe_review",
            "status": STATUS,
            "judgment": row["review_decision"],
            "path": rel(PRESSURE_REVIEW),
            "primary_kpi": f"net_sum={row['net_profit_sum']};pf_min={row['profit_factor_min']};trades={row['trade_count_sum']}",
            "guardrail_kpi": f"max_dd_pct={row['max_drawdown_percent_max']};selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "completed_from_run272C",
            "notes": row["review_reason"],
        }
        for row in review_rows
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__{str(row['variant']).lower()}_{str(row['tier_scope']).lower().replace(' ', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": f"mt5_probe_review_{row['variant']}_{str(row['tier_scope']).lower().replace(' ', '_')}",
            "tier_scope": row["tier_scope"],
            "scoreboard": "runtime_probe_review",
            "status": STATUS,
            "judgment": row["review_decision"],
            "evidence_boundary": "pressure_survivor_or_failure_memory_no_candidate",
            "report_path": rel(RUN_REPORT),
            "notes": row["review_reason"],
        }
        for row in review_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs(survivor_rows: Sequence[Mapping[str, Any]]) -> None:
    selection = SELECTION_STATUS.read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        f"run272D(272D 실행)는 run272C(272C 실행)의 MT5(`MetaTrader 5`, 메타트레이더5) KPI(핵심 성과 지표)를 검토해 q04(4번 분기)를 pressure survivor(압박 생존 분기)로 분리했다.\n효과(effect, 효과): survivor rows(생존 행) `{len(survivor_rows)}`개를 Stage273(273단계) stability validation(안정성 검증) 씨앗으로 넘기지만, selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 아직 없다.",
    )
    selection = append_once(selection, "run272D_report", f"- run272D_report(272D 보고): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run272D_stage273_stability_queue", f"- run272D_stage273_stability_queue(272D 273단계 안정성 대기열): `{rel(SURVIVOR_QUEUE)}`")
    write_md(SELECTION_STATUS, selection)

    current = CURRENT_STATE.read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run272D_summary",
        f"- run272D_summary(272D 요약): run272D(272D 실행)는 q04(4번 분기)를 pressure survivor(압박 생존 분기)로 남겼다. Effect(효과): Stage273(273단계) stability validation(안정성 검증) 씨앗은 생겼지만, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    review = REVIEW_INDEX.read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run272D_report",
        f"- run272D_report(272D 보고): `{rel(RUN_REPORT)}`\n- run272D_pressure_review(272D 압박 검토): `{rel(PRESSURE_REVIEW)}`\n- run272D_stage273_stability_queue(272D 273단계 안정성 대기열): `{rel(SURVIVOR_QUEUE)}`",
    )
    write_md(REVIEW_INDEX, review)

    workspace = WORKSPACE_STATE.read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage272(272단계) run272D(272D 실행) time-risk router MT5 probe review(시간 위험 라우터 MT5 탐침 검토) `{RUN_ID}`. "
        f"Effect(효과): q04(4번 분기)를 pressure survivor(압박 생존 분기)로 분리했고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_focus_items(workspace, RUN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = CHANGELOG.read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run272D time-risk router MT5 probe review(272D 시간 위험 라우터 MT5 탐침 검토)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): q04(4번 분기)를 Stage273(273단계) stability validation(안정성 검증) seed(씨앗)로 분리했다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)

    if path_exists(IDEA_REGISTER):
        ideas = IDEA_REGISTER.read_text(encoding="utf-8-sig")
        ideas = append_once(
            ideas,
            "IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272D",
            f"| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272D` | `{STAGE_ID}` | q04(4번 분기)를 pressure survivor(압박 생존 분기)로 Stage273(273단계)에 넘긴다 | `Tier A + Tier B paired MT5 runtime probe(Tier A + Tier B 쌍 MT5 런타임 탐침)` | `pressure_survivor_no_candidate` | survivor rows(생존 행) `{len(survivor_rows)}`개, selected candidate(선택 후보) 없음 |",
        )
        write_md(IDEA_REGISTER, ideas)


def write_result_and_lineage(created_at: str, artifacts: Sequence[Path]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": "run272D time-risk router MT5 probe review(272D 시간 위험 라우터 MT5 탐침 검토)",
                "evidence_available": "run272C MT5 KPI summary;backtest forensics;runtime supply matrix;tester reports",
                "evidence_missing": "month/session trade list attribution;Adapter package;ONNX export/parity;full stability validation",
                "judgment_label": JUDGMENT,
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "q04는 좋아 보이는 생존 분기지만 아직 후보가 아니라 다음 안정성 검증 씨앗이다.",
            }
        ],
    )
    source_inputs = [KPI_SUMMARY, RUNTIME_SUPPLY, BACKTEST_FORENSICS, RUN272C_MANIFEST, RUN272C_LINEAGE, RUN272C_REPORT]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage272/review_time_risk_router_mt5_probe.py",
        "entry_command": "python stage_pipelines/stage272/review_time_risk_router_mt5_probe.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)


def update_artifact_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run272D_review_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run272D time-risk router MT5 probe review artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def execute() -> dict[str, Any]:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    review_rows, survivor_rows, failure_rows = build_review_rows()
    write_csv(PRESSURE_REVIEW, review_rows)
    write_csv(SURVIVOR_QUEUE, survivor_rows)
    write_csv(FAILURE_MEMORY, failure_rows)
    write_report(review_rows, survivor_rows, failure_rows)
    artifacts = [PRESSURE_REVIEW, SURVIVOR_QUEUE, FAILURE_MEMORY, RESULT_JUDGMENT, RUN_REPORT, RUN_MANIFEST, LINEAGE_RECEIPT]
    write_result_and_lineage(created_at, artifacts)
    update_ledgers(review_rows, survivor_rows)
    update_state_docs(survivor_rows)
    artifacts = [PRESSURE_REVIEW, SURVIVOR_QUEUE, FAILURE_MEMORY, RESULT_JUDGMENT, RUN_REPORT, RUN_MANIFEST, LINEAGE_RECEIPT]
    write_result_and_lineage(created_at, artifacts)
    update_artifact_registry(created_at, artifacts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "survivor_rows": len(survivor_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
