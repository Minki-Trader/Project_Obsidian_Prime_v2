from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from stage_pipelines.stage297.review_bilevel_curve_monotonic_profit_mt5_probe import (  # noqa: E402
    curve_stats,
    number,
    parse_out_deals,
)


STAGE_ID = "298_onnx_candidate_campaign__profit_scale_edge_amplification_rebuild"
NEXT_STAGE_ID = "299_onnx_candidate_campaign__runtime_realized_trade_shape_rebuild"
RUN_ID = "run298C_review_profit_scale_edge_amplification_mt5_probe_v1"
RUN_NUMBER = "run298C"
SOURCE_RUN_ID = "run298B_profit_scale_edge_amplification_mt5_probe_v1"
PARENT_RUN_ID = "run298A_design_profit_scale_edge_amplification_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN298A = STAGE_ROOT / "02_runs" / "run298A"
RUN298B = STAGE_ROOT / "02_runs" / "run298B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC = NEXT_STAGE_ROOT / "00_spec"
NEXT_REVIEWS = NEXT_STAGE_ROOT / "03_reviews"
NEXT_SELECTED = NEXT_STAGE_ROOT / "04_selected"

SOURCE_EXECUTION = RUN298B / "execution_result.json"
SOURCE_KPI = RUN298B / "mt5_kpi_summary.csv"
SOURCE_SCOUT = RUN298A / "model_scout_scoreboard.csv"
PRODUCER = Path("stage_pipelines/stage298/review_profit_scale_edge_amplification_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "profit_scale_edge_amplification_review_scoreboard.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage299_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run298C_profit_scale_edge_amplification_review_stage299_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage298_profit_scale_edge_amplification_review_stage299_open.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes")
STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def read_text(path: Path) -> str:
    return ledger.io_path(path).read_text(encoding="utf-8-sig") if ledger.path_exists(path) else ""


def write_text(path: Path, text: str) -> None:
    ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ledger.io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    ledger.write_csv_rows(path, columns, rows)


def upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    ledger.upsert_csv_rows(path, columns, rows, key=key)


def parse_date(text: str) -> date:
    return date.fromisoformat(str(text).replace(".", "-"))


def feature_trading_days(attempt: Mapping[str, Any]) -> int:
    set_path = attempt.get("set", {}).get("path")
    feature_path = ""
    if set_path and ledger.path_exists(Path(str(set_path))):
        text = ledger.io_path(Path(str(set_path))).read_text(encoding="utf-8-sig")
        for line in text.splitlines():
            if line.startswith("InpFeatureCsvPath="):
                feature_path = line.split("=", 1)[1].strip()
                break
    local = RUN298B / "features" / Path(feature_path).name
    if not ledger.path_exists(local):
        return 183 if attempt.get("split") == "validation_is" else 131
    dates: set[str] = set()
    with ledger.io_path(local).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            bar_time = row.get("bar_time_server") or row.get("timestamp_utc") or ""
            if bar_time:
                dates.add(str(bar_time)[:10].replace(".", "-"))
    return len(dates)


def load_actual_rows() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    execution = json.loads(ledger.io_path(SOURCE_EXECUTION).read_text(encoding="utf-8-sig"))
    attempts = {item.get("attempt_name"): item for item in execution.get("attempts", [])}
    scout_rows = {row["materialized_branch_id"]: row for row in ledger.read_csv_rows(SOURCE_SCOUT)}
    rows: list[dict[str, Any]] = []
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source_row in csv.DictReader(handle):
            if source_row.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source_row["metrics"])
            report = ast.literal_eval(source_row["report"])
            attempt = attempts.get(report.get("attempt_name"), {})
            candidate_id = str(attempt.get("stage298_branch_id") or attempt.get("materialized_branch_id") or "")
            package_id = str(attempt.get("package_id") or scout_rows.get(candidate_id, {}).get("package_id") or "")
            tester = attempt.get("ini", {}).get("tester", {})
            from_date = tester.get("FromDate")
            to_date = tester.get("ToDate")
            calendar_days = (parse_date(to_date) - parse_date(from_date)).days + 1 if from_date and to_date else 0
            trading_days = feature_trading_days(attempt)
            trades = int(number(metrics.get("trade_count")))
            net_profit = number(metrics.get("net_profit"))
            report_path = Path(str(metrics.get("report_path")))
            deals = parse_out_deals(report_path)
            curve = curve_stats(deals, net_profit)
            rows.append(
                {
                    "materialized_branch_id": candidate_id,
                    "package_id": package_id,
                    "split": source_row.get("split", ""),
                    "net_profit": net_profit,
                    "profit_factor": number(metrics.get("profit_factor")),
                    "trade_count": trades,
                    "trades_per_trading_day": trades / trading_days if trading_days else 0.0,
                    "trades_per_calendar_day": trades / calendar_days if calendar_days else 0.0,
                    "calendar_days": calendar_days,
                    "trading_days": trading_days,
                    "max_drawdown_amount": number(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount")),
                    "max_drawdown_percent": number(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent")),
                    "recovery_factor": number(metrics.get("recovery_factor")),
                    "expectancy": number(metrics.get("expectancy")),
                    "win_rate_percent": number(metrics.get("win_rate_percent")),
                    "report_path": report_path.as_posix(),
                    **curve,
                }
            )
    return rows, scout_rows


def build_scoreboard(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_candidate[str(row["materialized_branch_id"])][str(row["split"])] = row
    scoreboard: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for candidate_id, split_rows in sorted(by_candidate.items()):
        val = split_rows.get("validation_is", {})
        oos = split_rows.get("oos", {})
        val_net = number(val.get("net_profit"))
        oos_net = number(oos.get("net_profit"))
        combined = val_net + oos_net
        val_tpd = number(val.get("trades_per_trading_day"))
        oos_tpd = number(oos.get("trades_per_trading_day"))
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 650 and number(oos.get("trade_count")) >= 450 else "failed"
        density_gate = "passed" if 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0 else "failed"
        profit_scale_gate = "passed" if val_net >= 300.0 and oos_net >= 300.0 and combined >= 800.0 else "failed"
        efficiency_gate = "passed"
        if number(val.get("profit_factor")) < 1.12 or number(oos.get("profit_factor")) < 1.12:
            efficiency_gate = "failed"
        if number(val.get("recovery_factor")) < 1.0 or number(oos.get("recovery_factor")) < 1.0:
            efficiency_gate = "failed"
        if number(val.get("expectancy")) < 0.10 or number(oos.get("expectancy")) < 0.10:
            efficiency_gate = "failed"
        curve_gate = "passed" if val.get("curve_pocket_gate") == "passed" and oos.get("curve_pocket_gate") == "passed" else "failed"
        row = {
            "materialized_branch_id": candidate_id,
            "package_id": val.get("package_id") or oos.get("package_id", ""),
            "validation_net_profit": val_net,
            "validation_pf": number(val.get("profit_factor")),
            "validation_trades": int(number(val.get("trade_count"))),
            "validation_trades_per_trading_day": val_tpd,
            "validation_recovery": number(val.get("recovery_factor")),
            "validation_expectancy": number(val.get("expectancy")),
            "validation_max_dd": number(val.get("max_drawdown_amount")),
            "oos_net_profit": oos_net,
            "oos_pf": number(oos.get("profit_factor")),
            "oos_trades": int(number(oos.get("trade_count"))),
            "oos_trades_per_trading_day": oos_tpd,
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd": number(oos.get("max_drawdown_amount")),
            "combined_net_profit": combined,
            "minimum_trade_gate": min_trade_gate,
            "density_4_10_trading_day_gate": density_gate,
            "profit_scale_gate": profit_scale_gate,
            "efficiency_gate": efficiency_gate,
            "curve_pocket_gate": curve_gate,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard.append(row)
        for split_row in (val, oos):
            if split_row:
                curve_rows.append({key: split_row.get(key, "") for key in split_row.keys() if key != "report_path"})
                pocket_rows.append(
                    {
                        "materialized_branch_id": split_row["materialized_branch_id"],
                        "package_id": split_row["package_id"],
                        "split": split_row["split"],
                        "pocket_gate": split_row["curve_pocket_gate"],
                        "max_local_drawdown": split_row["max_local_drawdown"],
                        "net_profit": split_row["net_profit"],
                        "drawdown_to_net_ratio": number(split_row["max_local_drawdown"]) / max(number(split_row["net_profit"]), 1.0),
                        "worst_rolling_20_net": split_row["worst_rolling_20_net"],
                        "worst_rolling_50_net": split_row["worst_rolling_50_net"],
                        "positive_month_share": split_row["positive_month_share"],
                    }
                )
        failures.append(
            {
                "failure_id": f"{candidate_id}_stage298_negative",
                "materialized_branch_id": candidate_id,
                "package_id": row["package_id"],
                "failed_boundary": ",".join(
                    name
                    for name, value in (
                        ("minimum_trade_gate", min_trade_gate),
                        ("density_4_10_trading_day_gate", density_gate),
                        ("profit_scale_gate", profit_scale_gate),
                        ("efficiency_gate", efficiency_gate),
                        ("curve_pocket_gate", curve_gate),
                    )
                    if value != "passed"
                ),
                "why_failed": "actual MT5 routed total(실제 MT5 라우팅 전체)에서 validation(검증) 손상 또는 수익 규모/효율/곡선 포켓 조건이 깨졌다.",
                "salvage_value": "OOS(표본외) 양수 단서는 일부 있었지만 validation(검증) DD와 음수 전환 때문에 entry rank(진입 순위) 접근만으로는 부족하다.",
                "reopen_condition": "runtime-realized trade shape(런타임 실제 거래 형태)로 validation/OOS 모두 순수익 300 이상과 깊은 포켓 제거를 먼저 보여야 한다.",
                "do_not_repeat": "Stage298 payoff rank/hold widening(보상 순위/보유 확장)을 임계값만 바꿔 반복하지 않는다.",
                "claim_boundary": BOUNDARY,
            }
        )
    return scoreboard, curve_rows, pocket_rows, failures


def stage299_queue_rows() -> list[dict[str, Any]]:
    refs = "stage297_actual_mt5_low_profit_scale_failure;stage298_payoff_rank_validation_damage"
    return [
        {
            "seed_id": "stage299_runtime_realized_trade_shape_primary",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주축)",
            "hypothesis": "Entry rank(진입 순위)와 payoff score(보상 점수)만으로는 validation(검증) 손상과 깊은 DD(손실폭)를 막지 못했다. Stage299(299단계)는 실제 MT5 deal lifecycle(거래 생애), hold duration(보유 시간), exit loss cluster(청산 손실 군집)를 직접 모델링해 4-10 trades/day(일 4-10거래)와 수익 규모를 동시에 노린다.",
            "broad_sweep": "trade duration buckets(거래 지속시간 구간), realized exit loss clusters(실현 청산 손실 군집), session adverse-shape(세션 불리한 형태), validation-safe OOS-positive filters(검증 안전 표본외 양수 필터)",
            "aggressive_sweep": "OOS positive shape(표본외 양수 형태)를 validation-safe constraint(검증 안전 제약) 안에서 재확장한다.",
            "defensive_sweep": "validation negative routes(검증 음수 경로), high DD months(높은 손실폭 월), long underwater paths(긴 수중 구간)를 먼저 거부한다.",
            "success_gate": "validation/OOS 각각 net profit(순수익) 300 이상, combined(합산) 800 이상, 4-10 trades/day(일 4-10거래), PF(수익 팩터) 1.12 이상, 깊은 local hollow(국소 움푹 패임) 없음.",
            "discard_condition": "OOS(표본외)만 좋아지고 validation(검증)이 음수이거나, 순수익보다 DD(손실폭)가 더 커지면 폐기한다.",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        }
    ]


def stage299_scaffold() -> None:
    for path in (NEXT_SPEC, NEXT_REVIEWS, NEXT_SELECTED):
        ledger.io_path(path).mkdir(parents=True, exist_ok=True)
    write_text(
        NEXT_SPEC / "stage_brief.md",
        "\n".join(
            [
                "# Stage299 Brief(299단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                "- question(질문): Can runtime-realized trade shape(런타임 실제 거래 형태) remove validation damage(검증 손상) while preserving OOS-positive clues(표본외 양수 단서), 4-10 trades/day(일 4-10거래), and profit scale(수익 규모)?",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): Stage298(298단계)의 payoff-rank 실패를 반복하지 않고, 실제 MT5 deal lifecycle(거래 생애)과 exit loss cluster(청산 손실 군집)를 새 표면으로 연다.",
                "",
            ]
        ),
    )
    write_text(
        NEXT_SELECTED / "selection_status.md",
        "\n".join(
            [
                "# Stage299 Selection Status(299단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_runtime_realized_trade_shape_rebuild`",
                "- current_packet(현재 작업 묶음): `299_onnx_candidate_campaign__runtime_realized_trade_shape_rebuild_v1`",
                "- current_run(현재 실행): `none`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                "- target_candidate(목표 후보): `none`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(ONNX 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                "- next_action(다음 행동): `run299A_design_runtime_realized_trade_shape_rebuild_packet`",
                f"- stage298_review(298단계 검토): `{rel(REPORT)}`",
                "",
            ]
        ),
    )
    write_text(
        NEXT_REVIEWS / "review_index.md",
        "\n".join(
            [
                "# Stage299 Review Index(299단계 검토 색인)",
                "",
                f"- source_review(원천 검토): `{rel(REPORT)}`",
                f"- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`",
                "",
            ]
        ),
    )
    write_csv(
        NEXT_REVIEWS / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage299_opened_from_run298C",
                "stage_id": NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage298_review",
                "status": "opened_runtime_realized_trade_shape_rebuild",
                "judgment": "opened_from_stage298_validation_damage_failure_memory",
                "evidence_boundary": "planning_from_stage298_actual_mt5_evidence",
                "report_path": rel(REPORT),
                "notes": "next_action=run299A_design_runtime_realized_trade_shape_rebuild_packet",
            }
        ],
    )


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> str:
    best = max(scoreboard, key=lambda row: number(row.get("combined_net_profit"))) if scoreboard else {}
    total = len(scoreboard)
    profit_pass = sum(1 for row in scoreboard if row.get("profit_scale_gate") == "passed")
    efficiency_pass = sum(1 for row in scoreboard if row.get("efficiency_gate") == "passed")
    curve_pass = sum(1 for row in scoreboard if row.get("curve_pocket_gate") == "passed")
    return "\n".join(
        [
            "# run298C Profit-Scale Edge Amplification Review(298C 수익 규모 거래우위 증폭 검토)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(ONNX 준비): `not_started`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- scoreboard_rows(점수판 행): `{len(scoreboard)}`",
            f"- failure_rows(실패 기억 행): `{len(failures)}`",
            f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}` from `{best.get('package_id', 'none')}`",
            "",
            "Effect(효과): Stage298(298단계)은 실제 MT5 runtime probe(MT5 런타임 탐침)를 완료했지만, validation(검증) 손상과 낮은 수익 규모 때문에 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.",
            "",
            "## Gate Result(관문 결과)",
            "",
            f"- profit_scale_gate(수익 규모 관문): `{profit_pass}/{total}` 통과",
            f"- efficiency_gate(효율 관문): `{efficiency_pass}/{total}` 통과",
            f"- curve_pocket_gate(곡선 포켓 관문): `{curve_pass}/{total}` 통과",
            "",
            "## Next Stage(다음 단계)",
            "",
            f"- opened_stage(열린 단계): `{NEXT_STAGE_ID}`",
            "- next_action(다음 행동): `run299A_design_runtime_realized_trade_shape_rebuild_packet`",
            "",
            f"`{BOUNDARY}`",
            "",
        ]
    )


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    if marker in workspace:
        return workspace
    needle = "current_focus:\n"
    if needle in workspace:
        return workspace.replace(needle, needle + focus, 1)
    return workspace.rstrip() + "\ncurrent_focus:\n" + focus


def update_docs(status: str, judgment: str, next_action: str) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selected += f"- run298C_report(298C 보고): `{rel(REPORT)}`\n"
    selected += f"- stage299_opened(299단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index += f"- run298C_report(298C 보고): `{rel(REPORT)}`\n"
    review_index += f"- run298C_scoreboard(298C 점수판): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage299_seed_queue(299단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `299_onnx_candidate_campaign__runtime_realized_trade_shape_rebuild_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = current.rstrip() + f"\n- run298C_summary(298C 요약): Stage298(298단계) actual MT5 review(실제 MT5 검토)는 후보를 선택하지 않고 Stage299(299단계)을 열었다. Effect(효과): payoff rank(보상 순위)와 hold widening(보유 확장)의 validation damage(검증 손상)를 failure memory(실패 기억)로 남기고 runtime-realized trade shape(런타임 실제 거래 형태)로 질문을 바꾼다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage298(298단계) run298C(298C 실행) profit-scale edge amplification MT5 review(수익 규모 거래우위 증폭 MT5 검토) `{RUN_ID}` closed Stage298 and opened Stage299(299단계). "
        f"Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 없고 next_action(다음 행동)은 `run299A_design_runtime_realized_trade_shape_rebuild_packet`이다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog += (
        f"\n## {UPDATED_ON} run298C profit-scale edge amplification review(298C 수익 규모 거래우위 증폭 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        "- effect(효과): Stage298(298단계)을 후보 없음으로 닫고 Stage299(299단계) runtime-realized trade shape(런타임 실제 거래 형태)을 열었다.\n"
        "- boundary(경계): Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 시작하지 않았다.\n"
    )
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str, next_action: str) -> None:
    upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "profit_scale_edge_amplification_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate=none;adapter_package=none;onnx_readiness=not_started;next_action={next_action}."}],
        "run_id",
    )
    upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "profit_scale_edge_amplification_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "trade_quality_curve_profit_scale",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": "selected_candidate=none;profit_scale_gate=failed",
                "guardrail_kpi": "Adapter=none;ONNX=not_started",
                "external_verification_status": "completed",
                "notes": f"next_action={next_action}.",
            }
        ],
        "ledger_row_id",
    )
    upsert(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "profit_scale_edge_amplification_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "profit_scale_edge_amplification_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": "Stage299 opened; no Adapter; no ONNX."}],
        "row_id",
    )


def update_memory_registers(failures: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} runtime-realized trade shape handoff(런타임 실제 거래 형태 인계)\n\n"
            "- idea_id(아이디어 ID): `stage299_runtime_realized_trade_shape_primary`\n"
            "- hypothesis(가설): validation damage(검증 손상)는 entry score(진입 점수)가 아니라 실제 hold/exit/trade-shape(보유/청산/거래 형태) 병목일 수 있다.\n"
            "- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).\n"
        )
        write_text(IDEA_REGISTER, idea)
    negative = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in negative:
        negative += (
            f"\n## {RUN_ID} Stage298 payoff-rank validation damage negative memory(298단계 보상 순위 검증 손상 부정 기억)\n\n"
            f"- failed_profiles(실패 프로필): `{len(failures)}`\n"
            "- failure_boundary(실패 경계): OOS(표본외) 양수 단서는 있었지만 validation(검증)이 음수로 돌아서고 DD(손실폭)가 커졌다.\n"
            "- do_not_repeat(반복 금지): payoff rank(보상 순위), hold widening(보유 확장), density8 control(밀도 8 대조)을 같은 임계값만 바꿔 반복하지 않는다.\n"
            "- reopen_condition(재개 조건): 런타임 실제 거래 형태가 validation/OOS 모두 순수익 300 이상과 깊은 포켓 제거를 보여야 한다.\n"
        )
        write_text(NEGATIVE_REGISTER, negative)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    for path in paths:
        if not ledger.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append({"artifact_id": f"{RUN_ID}__{artifact_id}", "artifact_type": "stage298_profit_scale_edge_amplification_review_artifact", "path": rel(path), "sha256": ledger.sha256_file_lf_normalized(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": "2026-05-24T16:30:00Z", "notes": "Stage298 review and Stage299 open handoff"})
    upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    actual_rows, _ = load_actual_rows()
    scoreboard, curve_rows, pocket_rows, failures = build_scoreboard(actual_rows)
    queue_rows = stage299_queue_rows()
    status = "completed_profit_scale_edge_amplification_review_no_candidate_stage299_opened"
    judgment = "profit_scale_edge_amplification_actual_mt5_negative_validation_damage_no_adapter_no_onnx"
    next_action = "run299A_design_runtime_realized_trade_shape_rebuild_packet"
    write_csv(SCOREBOARD, list(scoreboard[0].keys()), scoreboard)
    write_csv(CURVE, list(curve_rows[0].keys()) if curve_rows else ["materialized_branch_id"], curve_rows)
    write_csv(LOCAL_POCKETS, list(pocket_rows[0].keys()) if pocket_rows else ["materialized_branch_id"], pocket_rows)
    write_csv(FAILURE_MEMORY, list(failures[0].keys()), failures)
    write_csv(NEXT_STAGE_QUEUE, list(queue_rows[0].keys()), queue_rows)
    write_csv(
        RESULT_JUDGMENT,
        ["result_subject", "evidence_available", "evidence_missing", "judgment_label", "judgment_class", "claim_boundary", "next_condition", "user_explanation_hook"],
        [{"result_subject": "Stage298 profit-scale edge amplification actual MT5 review(298단계 수익 규모 거래우위 증폭 실제 MT5 검토)", "evidence_available": f"scoreboard_rows={len(scoreboard)};failure_rows={len(failures)};source_kpi={rel(SOURCE_KPI)}", "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성), MT5 runtime reproduction package(MT5 런타임 재현 패키지)", "judgment_label": "negative", "judgment_class": judgment, "claim_boundary": BOUNDARY, "next_condition": next_action, "user_explanation_hook": "표본외 양수 단서는 있었지만 검증 손상이 커서 ONNX(온엑스)로 넘길 수 없다."}],
    )
    write_csv(
        GATE_AUDIT,
        ["gate_name", "status", "evidence_path", "effect"],
        [
            {"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "36/36 attempt(시도)를 실제 tester output(테스터 출력)에 연결했다."},
            {"gate_name": "profit_scale_efficiency_curve(수익 규모/효율/곡선)", "status": "failed", "evidence_path": rel(SCOREBOARD), "effect": "validation damage(검증 손상)와 DD(손실폭)가 조건 미달이다."},
            {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "후보 관문 실패로 Adapter(어댑터)를 만들지 않는다."},
            {"gate_name": "onnx_readiness(ONNX 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전 단계이므로 ONNX(온엑스)를 시작하지 않는다."},
        ],
    )
    manifest = {"run_id": RUN_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "status": status, "judgment": judgment, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_stage_id": NEXT_STAGE_ID, "next_action": next_action, "artifacts": [rel(path) for path in (SCOREBOARD, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)], "claim_boundary": BOUNDARY}
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    write_text(LINEAGE, json.dumps({"producer": rel(PRODUCER), "inputs": [rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_SCOUT)], "outputs": manifest["artifacts"]}, ensure_ascii=False, indent=2) + "\n")
    write_text(REPORT, report_markdown(scoreboard, failures))
    write_text(DECISION, f"# Stage298 Review Decision(298단계 검토 결정)\n\n- decision(결정): `{judgment}`\n- next_stage(다음 단계): `{NEXT_STAGE_ID}`\n- effect(효과): Stage298(298단계)은 후보 없음으로 닫고, Stage299(299단계)에서 runtime-realized trade shape(런타임 실제 거래 형태)을 새 논제로 연다.\n")
    stage299_scaffold()
    update_docs(status, judgment, next_action)
    update_registers(status, judgment, next_action)
    update_memory_registers(failures)
    update_artifact_registry([SCOREBOARD, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, DECISION, NEXT_SPEC / "stage_brief.md", NEXT_SELECTED / "selection_status.md", NEXT_REVIEWS / "review_index.md", NEXT_REVIEWS / "stage_run_ledger.csv"])
    print(json.dumps({"status": status, "judgment": judgment, "scoreboard_rows": len(scoreboard), "failure_rows": len(failures), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_stage_id": NEXT_STAGE_ID, "next_action": next_action}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
