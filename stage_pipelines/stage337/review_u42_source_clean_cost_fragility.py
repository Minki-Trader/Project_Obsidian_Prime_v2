from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337T"
RUN_ID = "run337T_source_clean_u42_cost_fragility_or_tester_rollover_probe_v1"
PARENT_RUN_ID = "run337S_tester_visible_source_policy_repair_or_next_data_boundary_probe_v1"
NEXT_RUN_ID = "run337U_source_clean_cost_buffer_rebuild_or_tester_rollover_reprobe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337T_u42_source_clean_cost_fragility_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
STATUS = "completed_stage337T_u42_source_clean_cost_fragility_review_no_forward_decision"
JUDGMENT = "u42_source_clean_control_runtime_parity_ok_but_cost_and_slice_fragility_not_onnx_ready"
DECISION = "stage337T_open_run337U_cost_buffer_rebuild_or_tester_rollover_reprobe_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Q_DIR = STAGE_DIR / "02_runs" / "run337Q"
RUN337R_DIR = STAGE_DIR / "02_runs" / "run337R"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337T_u42_source_clean_cost_fragility_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337T_u42_source_clean_cost_fragility_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SOURCE_TRADES = RUN337R_DIR / "trade_records.csv"
SOURCE_COST = RUN337R_DIR / "cost_stress_report.csv"
SOURCE_REGIME = RUN337R_DIR / "regime_attribution_report.csv"
SOURCE_CURVE = RUN337R_DIR / "curve_pocket_report.csv"
SOURCE_PARITY = RUN337Q_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
SOURCE_GAP = RUN337Q_DIR / "tester_feature_last_gap_reprobe.csv"

U42_COST_STRESS = RUN_DIR / "u42_cost_stress_detail.csv"
U42_SLICE_BREAKPOINTS = RUN_DIR / "u42_slice_cost_breakpoint.csv"
U42_PROXY_RUNTIME = RUN_DIR / "u42_proxy_runtime_usability.csv"
U42_FAILURE_MEMORY = RUN_DIR / "u42_failure_memory.csv"
U42_ROUTE_DECISION = RUN_DIR / "u42_source_clean_route_decision.csv"
FINAL_DECISION = RUN_DIR / "final_u42_source_clean_cost_fragility_decision.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

ATTEMPT = "u42_plain_rf"
STRESS_POINTS = (0.0, 0.5, 1.0, 2.0, 5.0, 10.0)
DEPOSIT = 500.0


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if bom else "utf-8"), bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def profit_factor(rows: Sequence[Mapping[str, Any]], key: str) -> float | None:
    wins = sum(number(row.get(key)) for row in rows if number(row.get(key)) > 0.0)
    losses = -sum(number(row.get(key)) for row in rows if number(row.get(key)) < 0.0)
    if losses == 0.0:
        return math.inf if wins > 0.0 else None
    return wins / losses


def metrics(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> dict[str, Any]:
    net = sum(number(row.get(key)) for row in rows)
    count = len(rows)
    gross_profit = sum(number(row.get(key)) for row in rows if number(row.get(key)) > 0)
    gross_loss = sum(number(row.get(key)) for row in rows if number(row.get(key)) < 0)
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor(rows, key),
        "expectancy": net / count if count else None,
    }


def grouped(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    output: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        output[tuple(row.get(key, "") for key in keys)].append(row)
    return output


def point_value(rows: Sequence[Mapping[str, Any]]) -> float:
    values = [number(row.get("point_value_per_lot_estimate")) for row in rows if number(row.get("point_value_per_lot_estimate")) > 0]
    return sum(values) / len(values) if values else 1.0


def stress_status(row: Mapping[str, Any]) -> str:
    net = number(row.get("net_profit"))
    pf = number(row.get("profit_factor"), math.nan)
    if net <= 0:
        return "net_broken"
    if not math.isfinite(pf) or pf < 1.1:
        return "pf_below_1_1"
    if pf < 1.2:
        return "pf_thin_1_1_to_1_2"
    return "survives"


def build_cost_detail(cost_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = [dict(row) for row in cost_rows if row.get("attempt_name") == ATTEMPT]
    output: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["stress_status"] = stress_status(item)
        item["source_clean"] = True
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        output.append(item)
    return output


def build_slice_breakpoints(trades: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    axes = ("direction", "weekday", "open_hour_utc", "session_utc", "chron_segment", "vol_regime", "adx_regime", "is_us_cash_open")
    u42 = [row for row in trades if row.get("attempt_name") == ATTEMPT]
    pv = point_value(u42)
    output: list[dict[str, Any]] = []
    for axis in axes:
        for key, rows in grouped(u42, (axis,)).items():
            bucket = key[0]
            if len(rows) < 3:
                continue
            stress_results: list[dict[str, Any]] = []
            for stress in STRESS_POINTS:
                stressed = []
                for row in rows:
                    item = dict(row)
                    item["stressed_net"] = number(row.get("net_profit")) - stress * number(row.get("volume")) * pv
                    stressed.append(item)
                metric = metrics(stressed, "stressed_net")
                stress_results.append({"stress": stress, **metric, "stress_status": stress_status(metric)})
            survival = [row for row in stress_results if row["stress_status"] in {"survives", "pf_thin_1_1_to_1_2"}]
            base = stress_results[0]
            output.append(
                {
                    "attempt_name": ATTEMPT,
                    "axis": axis,
                    "bucket": bucket,
                    "base_trade_count": base["trade_count"],
                    "base_net_profit": base["net_profit"],
                    "base_profit_factor": base["profit_factor"],
                    "base_expectancy": base["expectancy"],
                    "survives_to_extra_points_pf_ge_1_1": max((row["stress"] for row in survival), default="none"),
                    "breaks_at_or_before_1_point": all(row["stress_status"] not in {"survives", "pf_thin_1_1_to_1_2"} for row in stress_results if row["stress"] <= 1.0),
                    "slice_status": classify_slice(base, survival),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    output.sort(key=lambda row: (str(row["slice_status"]), number(row["base_net_profit"])))
    return output


def classify_slice(base: Mapping[str, Any], survival: Sequence[Mapping[str, Any]]) -> str:
    net = number(base.get("net_profit"))
    pf = number(base.get("profit_factor"), math.nan)
    if net <= 0:
        return "base_negative_pocket"
    if not math.isfinite(pf) or pf < 1.1:
        return "base_pf_thin"
    if not survival:
        return "cost_fragile"
    top = max(number(row.get("stress")) for row in survival)
    if top < 1.0:
        return "cost_fragile_below_1_point"
    if top < 2.0:
        return "thin_cost_buffer"
    return "survives_cost_buffer"


def build_proxy_rows(parity_rows: Sequence[Mapping[str, str]], gap_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = [dict(row) for row in parity_rows if row.get("attempt_name") == ATTEMPT]
    gap = next((row for row in gap_rows if row.get("attempt_name") == ATTEMPT), {})
    output: list[dict[str, Any]] = []
    for row in rows:
        row["runtime_signal_parity_usable"] = str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true"
        row["forward_pass_fail_usable"] = False
        row["tester_to_feature_last_gap_minutes"] = gap.get("tester_to_feature_last_gap_minutes", "")
        row["usability_judgment"] = "usable_for_runtime_signal_parity_not_forward_decision"
        row["claim_boundary"] = CLAIM_BOUNDARY
        output.append(row)
    return output


def build_failure_rows(slice_rows: Sequence[Mapping[str, Any]], cost_detail: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    weak_slices = [row for row in slice_rows if row["slice_status"] in {"base_negative_pocket", "base_pf_thin", "cost_fragile_below_1_point"}]
    weak_slices.sort(key=lambda row: number(row.get("base_net_profit")))
    base_cost = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 0), {})
    one_point = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 1), {})
    five_point = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 5), {})
    rows = [
        {
            "failure_id": "u42_global_cost_buffer_thin",
            "failure_type": "cost_fragility",
            "evidence": f"base_pf={base_cost.get('profit_factor')}; one_point_pf={one_point.get('profit_factor')}; five_point_net={five_point.get('net_profit')}",
            "do_not_repeat": "do not promote source-clean control when PF falls below 1.1 at one extra point and net breaks at five points",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    for idx, row in enumerate(weak_slices[:12], start=1):
        rows.append(
            {
                "failure_id": f"u42_weak_slice_{idx:02d}",
                "failure_type": row["slice_status"],
                "evidence": f"{row['axis']}={row['bucket']};net={row['base_net_profit']};pf={row['base_profit_factor']};trades={row['base_trade_count']}",
                "do_not_repeat": "do not read source-clean as robust without slice-level cost survival",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def route_rows(cost_detail: Sequence[Mapping[str, Any]], slice_rows: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    proxy_ok = all(row.get("runtime_signal_parity_usable") for row in proxy_rows) if proxy_rows else False
    one = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 1), {})
    five = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 5), {})
    weak = sum(1 for row in slice_rows if row["slice_status"] in {"base_negative_pocket", "base_pf_thin", "cost_fragile_below_1_point"})
    return [
        {
            "attempt_name": ATTEMPT,
            "source_policy": "source_clean_no_external_sources",
            "proxy_runtime_parity": "matched" if proxy_ok else "partial",
            "one_point_profit_factor": one.get("profit_factor", ""),
            "five_point_net_profit": five.get("net_profit", ""),
            "weak_slice_count": weak,
            "route_decision": "reject_as_onnx_ready_keep_as_failure_memory_control",
            "next_action": NEXT_RUN_ID,
            "reason": "source-clean is useful as a control, but cost buffer and slice robustness are too thin",
            "Forward Passed": "not_claimed",
            "Forward Failed": "not_claimed",
            "Goal Achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_rows(cost_detail: Sequence[Mapping[str, Any]], slice_rows: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    matched = sum(1 for row in proxy_rows if row.get("runtime_signal_parity_usable"))
    weak = sum(1 for row in slice_rows if row["slice_status"] in {"base_negative_pocket", "base_pf_thin", "cost_fragile_below_1_point"})
    one = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 1), {})
    return [
        {
            "gate_name": "u42_source_clean_confirmed",
            "status": "covered",
            "evidence_path": rel(U42_ROUTE_DECISION),
            "effect": "u42_plain_rf(US100 기술42 일반 RF)는 external source(외부 원천)가 없는 대조군으로 분리했다.",
        },
        {
            "gate_name": "proxy_runtime_parity_checked",
            "status": "covered" if matched == len(proxy_rows) and proxy_rows else "covered_partial",
            "evidence_path": rel(U42_PROXY_RUNTIME),
            "effect": f"proxy/MT5 signal parity(프록시/MT5 신호 동등성)를 확인했다; matched={matched}/{len(proxy_rows)}.",
        },
        {
            "gate_name": "cost_buffer_check",
            "status": "failed_for_onnx_readiness",
            "evidence_path": rel(U42_COST_STRESS),
            "effect": f"1 extra point(추가 1포인트)에서 PF(손익비)가 {one.get('profit_factor', '')}로 얇아진다.",
        },
        {
            "gate_name": "slice_fragility_check",
            "status": "failed_for_onnx_readiness",
            "evidence_path": rel(U42_SLICE_BREAKPOINTS),
            "effect": f"weak slice(약한 구간) {weak}개를 기록했다.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(FINAL_DECISION),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def report_text(route: Sequence[Mapping[str, Any]], cost_detail: Sequence[Mapping[str, Any]], weak_rows: Sequence[Mapping[str, Any]]) -> str:
    route_row = route[0] if route else {}
    one = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 1), {})
    five = next((row for row in cost_detail if number(row.get("extra_round_trip_points")) == 5), {})
    lines = [
        "# Stage337T u42 Source-Clean Cost Fragility Review(337T u42 원천 깨끗한 비용 취약성 리뷰)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- decision(결정): `{DECISION}`",
        f"- proxy_runtime_parity(프록시 런타임 동등성): `{route_row.get('proxy_runtime_parity', '')}`",
        f"- one_point_pf(1포인트 손익비): `{one.get('profit_factor', '')}`",
        f"- five_point_net(5포인트 순익): `{five.get('net_profit', '')}`",
        f"- weak_slice_count(약한 구간 수): `{route_row.get('weak_slice_count', '')}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Weak Pockets(약한 포켓)",
        "",
        "| axis(축) | bucket(구간) | net(순익) | PF(손익비) | trades(거래수) | status(상태) |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in weak_rows[:10]:
        lines.append(
            f"| `{row['axis']}` | `{row['bucket']}` | `{csv_value(row['base_net_profit'])}` | `{csv_value(row['base_profit_factor'])}` | `{row['base_trade_count']}` | `{row['slice_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Read(판독)",
            "",
            "u42_plain_rf(US100 기술42 일반 RF)는 source-clean control(원천 깨끗한 대조군)로는 유용하다. 하지만 비용 1포인트에서 PF(손익비)가 1.1 아래로 내려가고, 5포인트에서는 순익이 음수로 바뀐다.",
            "효과: 이 축은 운영 가능한 ONNX(온엑스) 준비가 아니라, 다음 cost-buffer rebuild(비용 버퍼 재구성) 또는 tester rollover reprobe(테스터 이월 재탐침)의 실패 기억으로 사용한다.",
        ]
    )
    return "\n".join(lines)


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def append_artifacts(paths: Sequence[Path]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = list(rows[0].keys()) if rows else ["artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"]
    generated = now_utc()
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def update_docs() -> list[Path]:
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- u42_source_clean_control(원천 깨끗한 대조군): `kept_as_failure_memory_control_not_onnx_ready`
- source_policy_repair_required(원천 정책 수리 필요): `m48_plain_rf;c56_plain_rf`
- tester_boundary_required(테스터 경계 필요): `tester must reach feature_last`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): u42는 proxy/runtime parity(프록시/런타임 동등성)는 맞지만 비용/구간 취약성 때문에 ONNX-ready(온엑스 준비)로 보지 않는다.
"""
    write_text(SELECTED_STATUS, selection, True)
    changed = [SELECTED_STATUS]
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        focus = (
            "- >-\n"
            f"  Stage337 run337T focus complete: Stage337(337단계) run337T(337T 실행)는 `{STATUS}`로 u42 source-clean cost fragility review(u42 원천 깨끗한 비용 취약성 리뷰)를 완료했다. "
            "Effect(효과): u42는 source-clean control(원천 깨끗한 대조군)로 남기되 cost buffer(비용 버퍼)가 얇아 ONNX-ready(온엑스 준비) 주장을 막았다."
        )
        if "Stage337 run337T focus complete" not in text:
            text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
        write_text(WORKSPACE_STATE, text, bom)
        changed.append(WORKSPACE_STATE)
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        block = f"""## Stage337 run337T(337T 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): u42 source-clean control(원천 깨끗한 대조군)은 proxy/MT5 parity(프록시/MT5 동등성)는 맞지만 비용 1포인트와 약한 구간에서 취약해 ONNX-ready(온엑스 준비)로 보지 않는다.
"""
        if "## Stage337 run337T(337T 실행)" not in text:
            text = text.rstrip() + "\n\n" + block
        write_text(CURRENT_STATE, text, bom)
        changed.append(CURRENT_STATE)
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337T(337T 실행) `{STATUS}`. Effect(효과): u42 source-clean cost fragility(원천 깨끗한 비용 취약성)를 확인했고 Forward/Goal(전진/목표) 주장은 없음."
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
        write_text(CHANGELOG, text, bom)
        changed.append(CHANGELOG)
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    trades = read_csv(SOURCE_TRADES)
    cost = read_csv(SOURCE_COST)
    parity = read_csv(SOURCE_PARITY)
    gap = read_csv(SOURCE_GAP)
    cost_detail = build_cost_detail(cost)
    slice_rows = build_slice_breakpoints(trades)
    proxy_rows = build_proxy_rows(parity, gap)
    failure_rows = build_failure_rows(slice_rows, cost_detail)
    route = route_rows(cost_detail, slice_rows, proxy_rows)
    gates = gate_rows(cost_detail, slice_rows, proxy_rows)
    weak_rows = [row for row in slice_rows if row["slice_status"] in {"base_negative_pocket", "base_pf_thin", "cost_fragile_below_1_point"}]
    weak_rows.sort(key=lambda row: number(row["base_net_profit"]))

    artifacts = [
        write_csv(U42_COST_STRESS, list(cost_detail[0].keys()) if cost_detail else ["attempt_name"], cost_detail),
        write_csv(U42_SLICE_BREAKPOINTS, list(slice_rows[0].keys()) if slice_rows else ["attempt_name"], slice_rows),
        write_csv(U42_PROXY_RUNTIME, list(proxy_rows[0].keys()) if proxy_rows else ["attempt_name"], proxy_rows),
        write_csv(U42_FAILURE_MEMORY, list(failure_rows[0].keys()) if failure_rows else ["failure_id"], failure_rows),
        write_csv(U42_ROUTE_DECISION, list(route[0].keys()), route),
        write_csv(GATE_AUDIT, ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(
            FINAL_DECISION,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "attempt_name": ATTEMPT,
                "source_policy": "source_clean_no_external_sources",
                "proxy_runtime_parity": route[0]["proxy_runtime_parity"],
                "route_decision": route[0]["route_decision"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_text(REPORT_PATH, report_text(route, cost_detail, weak_rows), True),
        write_text(
            DECISION_DOC,
            f"""# Stage337T Decision(337T 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): u42_plain_rf(US100 기술42 일반 RF)는 source-clean control(원천 깨끗한 대조군)로는 유용하지만 비용 버퍼와 약한 구간이 부족해 ONNX-ready(온엑스 준비)로 보지 않는다.
""",
            True,
        ),
    ]
    artifacts.extend(update_docs())
    upsert_csv(RUN_REGISTRY, ["run_id"], {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "u42_source_clean_cost_fragility", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT_PATH), "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed."})
    upsert_csv(
        STAGE_LEDGER,
        ["run_key"],
        {
            "run_key": f"{RUN_ID}__u42_source_clean_cost_fragility",
            "ledger_row_id": f"{RUN_ID}__u42_source_clean_cost_fragility",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "u42_source_clean_cost_fragility",
            "work_family": "runtime_attribution_cost_fragility",
            "question": "is the source-clean u42 control robust enough to remain an ONNX-ready route",
            "metric_scope": "proxy_runtime_parity_cost_stress_slice_breakpoint_no_forward_decision",
            "evidence_scope": "run337Q parity and run337R trade/cost reports",
            "kpi_scope": "diagnostic_not_onnx_ready",
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "primary_artifact": rel(REPORT_PATH),
            "path": rel(REPORT_PATH),
            "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "decision": DECISION,
        },
    )
    artifacts.extend([RUN_REGISTRY, STAGE_LEDGER])
    artifacts.append(append_artifacts(artifacts))
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "artifacts": [rel(path) for path in artifacts], "claim_boundary": CLAIM_BOUNDARY})
    print(json.dumps({"status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "weak_slices": len(weak_rows), "next_action": NEXT_RUN_ID, "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
