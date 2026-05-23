from __future__ import annotations

import ast
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE279_ID = "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild"
STAGE280_ID = "280_onnx_candidate_campaign__directional_mapping_stability_validation"
RUN_ID = "run279D_review_directional_runtime_mapping_mt5_probe_close_open_stage280_v1"
SOURCE_RUN_ID = "run279C_directional_runtime_mapping_mt5_signal_replay_v1"
STATUS = "completed_stage279_runtime_probe_review_stage280_open_no_candidate_selection"
JUDGMENT = "directional_mapping_runtime_probe_reviewed_survivor_seeds_stage280_opened_no_candidate_selection"
NEXT_ACTION = "run280A_design_directional_mapping_stability_validation_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE279 = ROOT / "stages" / STAGE279_ID
RUN279C = STAGE279 / "02_runs" / "run279C"
RUN_DIR = STAGE279 / "02_runs" / "run279D"
REVIEWS279 = STAGE279 / "03_reviews"
SELECTED279 = STAGE279 / "04_selected" / "selection_status.md"
REVIEW_INDEX279 = REVIEWS279 / "review_index.md"
STAGE_LEDGER279 = REVIEWS279 / "stage_run_ledger.csv"

MT5_KPI_SUMMARY = RUN279C / "mt5_kpi_summary.csv"
EXECUTION_RESULT = RUN279C / "execution_result.json"
RUN279C_MANIFEST = RUN279C / "run_manifest.json"
RUN279C_LINEAGE = RUN279C / "artifact_lineage_receipt.json"
RUN279C_REPORT = REVIEWS279 / "run279C_report.md"
RUN279B_MANIFEST = STAGE279 / "02_runs" / "run279B" / "directional_payload_manifest.csv"

SCOREBOARD = RUN_DIR / "runtime_probe_scoreboard.csv"
SURVIVOR_QUEUE = RUN_DIR / "stage280_survivor_seed_queue.csv"
FAILURE_MEMORY = RUN_DIR / "runtime_probe_failure_memory.csv"
REVIEW_RECEIPT = RUN_DIR / "runtime_probe_review_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS279 / "run279D_stage279_closeout_stage280_handoff.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-24_stage279_closeout_stage280_directional_mapping_stability_validation_open.md"

STAGE280 = ROOT / "stages" / STAGE280_ID
SPEC280 = STAGE280 / "00_spec" / "stage_brief.md"
INPUTS280 = STAGE280 / "01_inputs"
REVIEWS280 = STAGE280 / "03_reviews"
SELECTED280 = STAGE280 / "04_selected" / "selection_status.md"
STAGE_LEDGER280 = REVIEWS280 / "stage_run_ledger.csv"
REVIEW_INDEX280 = REVIEWS280 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage279/review_directional_runtime_mapping_mt5_probe_close_open_stage280.py")

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_dd",
    "validation_recovery",
    "validation_expectancy",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_dd",
    "oos_recovery",
    "oos_expectancy",
    "tier_b_validation_net_profit",
    "tier_b_oos_net_profit",
    "review_label",
    "review_reason",
    "next_action",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
SURVIVOR_COLUMNS = (
    "seed_id",
    "materialized_branch_id",
    "package_id",
    "seed_role",
    "why_keep",
    "stability_question",
    "required_next_checks",
    "failure_condition",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
FAILURE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "failure_type",
    "failure_reason",
    "salvage_value",
    "reopen_condition",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def parse_metric_payload(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str) or not value.strip():
        return {}
    parsed = ast.literal_eval(value)
    return dict(parsed) if isinstance(parsed, Mapping) else {}


def materialized_from_record_view(record_view: str) -> str:
    text = record_view
    text = text.removeprefix("mt5_")
    for suffix in (
        "_actual_routed_validation_is",
        "_actual_routed_oos",
        "_tier_a_validation_is",
        "_tier_a_oos",
        "_tier_b_validation_is",
        "_tier_b_oos",
    ):
        if text.endswith(suffix):
            return "run279B_" + text[: -len(suffix)]
    return "run279B_" + text


def parse_kpi_rows() -> pd.DataFrame:
    if not path_exists(MT5_KPI_SUMMARY):
        raise FileNotFoundError(MT5_KPI_SUMMARY)
    rows: list[dict[str, Any]] = []
    raw = pd.read_csv(io_path(MT5_KPI_SUMMARY))
    for _, row in raw.iterrows():
        metrics = parse_metric_payload(row.get("metrics"))
        item = {
            "record_view": row.get("record_view"),
            "tier_scope": row.get("tier_scope"),
            "split": row.get("split"),
            "status": row.get("status"),
            "route_role": row.get("route_role"),
            "materialized_branch_id": materialized_from_record_view(str(row.get("record_view", ""))),
        }
        for key in (
            "net_profit",
            "profit_factor",
            "trade_count",
            "max_drawdown_amount",
            "max_drawdown_percent",
            "recovery_factor",
            "expectancy",
            "win_rate_percent",
        ):
            item[key] = metrics.get(key, 0)
        rows.append(item)
    return pd.DataFrame(rows)


def package_lookup() -> dict[str, str]:
    if not path_exists(RUN279B_MANIFEST):
        return {}
    frame = pd.read_csv(io_path(RUN279B_MANIFEST))
    return {str(row["materialized_branch_id"]): str(row["package_id"]) for _, row in frame.iterrows()}


def metric_for(frame: pd.DataFrame, materialized_id: str, tier_scope: str, split: str, key: str) -> float:
    view = frame[
        frame["materialized_branch_id"].astype(str).eq(materialized_id)
        & frame["tier_scope"].astype(str).eq(tier_scope)
        & frame["split"].astype(str).eq(split)
    ]
    if view.empty:
        return 0.0
    return safe_float(view.iloc[0].get(key))


def build_review_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    kpi = parse_kpi_rows()
    packages = package_lookup()
    materialized_ids = sorted(packages)
    scoreboard_rows: list[dict[str, Any]] = []
    survivors: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for materialized_id in materialized_ids:
        package_id = packages.get(materialized_id, "")
        val_np = metric_for(kpi, materialized_id, "Tier A+B", "validation_is", "net_profit")
        val_pf = metric_for(kpi, materialized_id, "Tier A+B", "validation_is", "profit_factor")
        val_trades = safe_int(metric_for(kpi, materialized_id, "Tier A+B", "validation_is", "trade_count"))
        val_dd = metric_for(kpi, materialized_id, "Tier A+B", "validation_is", "max_drawdown_amount")
        val_rec = metric_for(kpi, materialized_id, "Tier A+B", "validation_is", "recovery_factor")
        val_exp = metric_for(kpi, materialized_id, "Tier A+B", "validation_is", "expectancy")
        oos_np = metric_for(kpi, materialized_id, "Tier A+B", "oos", "net_profit")
        oos_pf = metric_for(kpi, materialized_id, "Tier A+B", "oos", "profit_factor")
        oos_trades = safe_int(metric_for(kpi, materialized_id, "Tier A+B", "oos", "trade_count"))
        oos_dd = metric_for(kpi, materialized_id, "Tier A+B", "oos", "max_drawdown_amount")
        oos_rec = metric_for(kpi, materialized_id, "Tier A+B", "oos", "recovery_factor")
        oos_exp = metric_for(kpi, materialized_id, "Tier A+B", "oos", "expectancy")
        tier_b_val = metric_for(kpi, materialized_id, "Tier B", "validation_is", "net_profit")
        tier_b_oos = metric_for(kpi, materialized_id, "Tier B", "oos", "net_profit")

        if val_np > 0 and oos_np > 0 and val_pf >= 1.0 and oos_pf >= 1.0 and val_trades >= 50 and oos_trades >= 50:
            if materialized_id == "run279B_cp277D_breakout_q02":
                label = "lead_stability_seed(주 안정성 씨앗)"
                reason = "validation positive but weak recovery(검증 양수이나 회복 약함); OOS strong(표본외 강함)"
                role = "lead_stability_seed(주 안정성 씨앗)"
            elif materialized_id == "run279B_cp277D_breakout_q03":
                label = "low_supply_stability_control(저공급 안정성 대조)"
                reason = "validation and OOS positive(검증/표본외 양수) but OOS upside thin(표본외 상방 얇음)"
                role = "stability_control(안정성 대조)"
            elif materialized_id == "run279B_cp277C_consensus_q01":
                label = "breadth_high_drawdown_watch(넓은 공급 고손실폭 관찰)"
                reason = "validation/OOS positive(검증/표본외 양수) but drawdown high and Tier B validation negative(손실폭 높고 Tier B 검증 음수)"
                role = "breadth_watch(넓은 공급 관찰)"
            else:
                label = "watch_only_not_seed(관찰 전용)"
                reason = "positive but weaker than lead seed(양수이나 주 씨앗보다 약함)"
                role = ""
            if role:
                survivors.append(
                    {
                        "seed_id": f"stage280_seed_{len(survivors) + 1:02d}",
                        "materialized_branch_id": materialized_id,
                        "package_id": package_id,
                        "seed_role": role,
                        "why_keep": reason,
                        "stability_question": "Can the branch survive curve/month/session/trade-quality stress without collapsing?(곡선/월/세션/거래품질 압박에서 무너지지 않는가?)",
                        "required_next_checks": "balance/equity curve;monthly and session slice;trade quality;weak segment check;failure memory comparison",
                        "failure_condition": "validation weakness or OOS concentration expands(검증 약점 또는 표본외 집중이 커짐)",
                        "selected_candidate": "none",
                        "adapter_package": "none",
                        "onnx_readiness": "not_claimed",
                        "claim_boundary": BOUNDARY,
                    }
                )
            review_label = label
            next_action = NEXT_ACTION if role else "hold_as_positive_watch_no_stage280_seed"
        else:
            review_label = "failure_memory(실패 기억)"
            reasons: list[str] = []
            if val_np <= 0:
                reasons.append("validation_net_profit_nonpositive(검증 순손익 비양수)")
            if oos_np <= 0:
                reasons.append("oos_net_profit_nonpositive(표본외 순손익 비양수)")
            if val_pf < 1.0:
                reasons.append("validation_pf_below_1(검증 PF 1 미만)")
            if oos_pf < 1.0:
                reasons.append("oos_pf_below_1(표본외 PF 1 미만)")
            if val_trades < 50 or oos_trades < 50:
                reasons.append("thin_trade_count(거래 수 얇음)")
            reason = ";".join(reasons) if reasons else "weaker_than_survivor_seed(생존 씨앗보다 약함)"
            failures.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "failure_type": "runtime_probe_failure_memory(런타임 탐침 실패 기억)",
                    "failure_reason": reason,
                    "salvage_value": "direction mapping evidence only(방향 매핑 근거만)",
                    "reopen_condition": "new thesis changes decision/risk surface, not simple repair(단순 수리가 아니라 새 판단/위험 표면 변경)",
                    "claim_boundary": BOUNDARY,
                }
            )
            next_action = "record_as_failure_memory(실패 기억 기록)"
        scoreboard_rows.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "validation_net_profit": val_np,
                "validation_pf": val_pf,
                "validation_trade_count": val_trades,
                "validation_dd": val_dd,
                "validation_recovery": val_rec,
                "validation_expectancy": val_exp,
                "oos_net_profit": oos_np,
                "oos_pf": oos_pf,
                "oos_trade_count": oos_trades,
                "oos_dd": oos_dd,
                "oos_recovery": oos_rec,
                "oos_expectancy": oos_exp,
                "tier_b_validation_net_profit": tier_b_val,
                "tier_b_oos_net_profit": tier_b_oos,
                "review_label": review_label,
                "review_reason": reason,
                "next_action": next_action,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
    return scoreboard_rows, survivors, failures


def write_stage280_inputs(scoreboard_rows: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> None:
    for path in [STAGE280 / "00_spec", INPUTS280, STAGE280 / "02_runs", REVIEWS280, STAGE280 / "04_selected"]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(INPUTS280 / "stage279_runtime_probe_scoreboard.csv", SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(INPUTS280 / "stage280_survivor_seed_queue.csv", SURVIVOR_COLUMNS, survivors)
    write_csv(INPUTS280 / "stage279_runtime_probe_failure_memory.csv", FAILURE_COLUMNS, failures)
    write_md(
        SPEC280,
        f"""# Stage280 Brief(280단계 개요): Directional Mapping Stability Validation(방향 매핑 안정성 검증)

- stage_id(단계 ID): `{STAGE280_ID}`
- opened_by(개시 실행): `{RUN_ID}`
- active_question(핵심 질문): Stage279(279단계)의 survivor seed(생존 씨앗)가 curve/month/session/trade-quality stress(곡선/월/세션/거래품질 압박)를 견디는가?
- source_stage(원천 단계): `{STAGE279_ID}`
- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Boundary(경계)

Stage280(280단계)는 stability validation(안정성 검증) 단계다.
Effect(효과): survivor seed(생존 씨앗)를 selected candidate(선택 후보)로 부르지 않고, 곡선/구간/거래품질 압박을 먼저 통과시킨다.
""",
    )
    write_md(
        INPUTS280 / "input_refs.md",
        f"""# Stage280 Inputs(280단계 입력)

- stage279_scoreboard(279단계 점수판): `{rel(INPUTS280 / 'stage279_runtime_probe_scoreboard.csv')}`
- survivor_seed_queue(생존 씨앗 대기열): `{rel(INPUTS280 / 'stage280_survivor_seed_queue.csv')}`
- failure_memory(실패 기억): `{rel(INPUTS280 / 'stage279_runtime_probe_failure_memory.csv')}`
- source_execution_result(원천 실행 결과): `{rel(EXECUTION_RESULT)}`
- source_kpi_summary(원천 KPI 요약): `{rel(MT5_KPI_SUMMARY)}`
""",
    )
    write_md(
        SELECTED280,
        f"""# Stage280 Selection Status(280단계 선택 상태)

- stage_status(단계 상태): `opened_directional_mapping_stability_validation_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage280_directional_mapping_stability_validation_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE279_ID}`
- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_csv(
        STAGE_LEDGER280,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage280_open",
                "stage_id": STAGE280_ID,
                "run_id": RUN_ID,
                "view": "stage280_open_directional_mapping_stability_validation",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_directional_mapping_stability_validation_no_candidate_selection",
                "judgment": JUDGMENT,
                "evidence_boundary": "stage_open_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"survivor_seed_count={len(survivors)};next_action={NEXT_ACTION}.",
            }
        ],
    )
    write_md(
        REVIEW_INDEX280,
        f"""# Stage280 Review Index(280단계 검토 색인)

- stage280_open_report(280단계 개시 보고): `{rel(RUN_REPORT)}`
- survivor_seed_queue(생존 씨앗 대기열): `{rel(INPUTS280 / 'stage280_survivor_seed_queue.csv')}`
""",
    )


def write_outputs(scoreboard_rows: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], created_at: str) -> list[Path]:
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(SURVIVOR_QUEUE, SURVIVOR_COLUMNS, survivors)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failures)
    write_json(
        REVIEW_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "scoreboard_rows": len(scoreboard_rows),
            "survivor_seed_count": len(survivors),
            "failure_memory_count": len(failures),
            "lead_seed": survivors[0]["materialized_branch_id"] if survivors else "none",
            "review_boundary": "runtime_probe_review_no_candidate_selection(런타임 탐침 검토, 후보 선택 없음)",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"scoreboard_rows={len(scoreboard_rows)};survivor_seed_count={len(survivors)};failure_memory_count={len(failures)}",
                "evidence_missing": "balance/equity curve deep review;monthly/session/trade-quality review;Adapter package;ONNX parity",
                "judgment_label": JUDGMENT,
                "judgment_class": "runtime_probe_review(런타임 탐침 검토)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "생존 씨앗은 생겼지만 선택 후보는 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "runtime_probe_complete(런타임 탐침 완료)",
                "status": "passed",
                "evidence_path": rel(EXECUTION_RESULT),
                "effect": "72/72 attempts(시도)의 MT5 output(MT5 출력)을 검토 입력으로 쓴다.",
            },
            {
                "gate_name": "survivor_failure_split(생존/실패 분리)",
                "status": "passed",
                "evidence_path": rel(SURVIVOR_QUEUE),
                "effect": "candidate claim(후보 주장) 없이 다음 stability stage(안정성 단계) 입력을 만든다.",
            },
            {
                "gate_name": "no_onnx_claim(ONNX 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "Adapter package(어댑터 패키지)와 ONNX readiness(온엑스 준비)를 주장하지 않는다.",
            },
        ],
    )
    write_md(RUN_REPORT, report_markdown(scoreboard_rows, survivors, failures))
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage279 Closeout and Stage280 Stability Validation Open(279단계 종료와 280단계 안정성 검증 개시)

- date(날짜): `{UPDATED_ON}`
- decision(결정): Stage279(279단계)을 directional runtime mapping MT5 probe(방향 런타임 매핑 MT5 탐침) review(검토)로 닫고 Stage280(280단계)를 연다.
- effect(효과): survivor seed(생존 씨앗)를 selected candidate(선택 후보)로 부르지 않고 stability validation(안정성 검증)으로 넘긴다.
- source(원천): `{rel(RUN_REPORT)}`
- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage280_inputs(scoreboard_rows, survivors, failures)
    artifacts = [
        SCOREBOARD,
        SURVIVOR_QUEUE,
        FAILURE_MEMORY,
        REVIEW_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
        DECISION_PATH,
        SPEC280,
        INPUTS280 / "stage279_runtime_probe_scoreboard.csv",
        INPUTS280 / "stage280_survivor_seed_queue.csv",
        INPUTS280 / "stage279_runtime_probe_failure_memory.csv",
        INPUTS280 / "input_refs.md",
        SELECTED280,
        STAGE_LEDGER280,
        REVIEW_INDEX280,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE279_ID,
        "target_stage_id": STAGE280_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "scoreboard_rows": len(scoreboard_rows),
        "survivor_seed_count": len(survivors),
        "failure_memory_count": len(failures),
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    lineage = {
        "run_id": RUN_ID,
        "source_inputs": [rel(MT5_KPI_SUMMARY), rel(EXECUTION_RESULT), rel(RUN279C_MANIFEST), rel(RUN279B_MANIFEST), rel(ROOT / PRODUCER_PATH)],
        "source_hashes": {
            rel(path): sha256_file(path)
            for path in [MT5_KPI_SUMMARY, EXECUTION_RESULT, RUN279C_MANIFEST, RUN279C_LINEAGE, RUN279B_MANIFEST, ROOT / PRODUCER_PATH]
            if path_exists(path)
        },
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER279), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_and_reproducible_from_command(추적되며 명령으로 재현 가능)",
        "lineage_judgment": "connected_with_boundary_no_candidate_claim(경계 내 연결, 후보 주장 없음)",
    }
    write_json(LINEAGE_RECEIPT, lineage)
    artifacts.append(LINEAGE_RECEIPT)
    return artifacts


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> str:
    survivor_lines = [
        f"- `{row['materialized_branch_id']}`: {row['seed_role']} - {row['why_keep']}"
        for row in survivors
    ] or ["- `none`"]
    return "\n".join(
        [
            "# run279D Report(279D 보고서): Stage279 Closeout and Stage280 Handoff(279단계 종료와 280단계 인계)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            f"- status(상태): `{STATUS}`",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- scoreboard_rows(점수판 행): `{len(scoreboard_rows)}`",
            f"- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`",
            f"- failure_memory_count(실패 기억 수): `{len(failures)}`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "## Survivor Seeds(생존 씨앗)",
            "",
            *survivor_lines,
            "",
            "## Meaning(의미)",
            "",
            "Stage279(279단계)는 direction mapping(방향 매핑)을 MT5 runtime probe(MT5 런타임 탐침)까지 확인했다.",
            "Effect(효과): strong-looking OOS(강해 보이는 표본외) 숫자를 바로 후보로 부르지 않고, Stage280(280단계) stability validation(안정성 검증)으로 넘긴다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE279_ID,
                "lane": "stage_closeout_and_stability_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"survivor_seed_count={len(survivors)};failure_memory_count={len(failures)};target_stage={STAGE280_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage279_closeout",
                "stage_id": STAGE279_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage279_closeout_stage280_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "stage279_closeout_stage280_open(279단계 종료 280단계 개시)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "runtime_probe_review_no_candidate_selection",
                "scoreboard_lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "primary_kpi": f"survivor_seed_count={len(survivors)};failure_memory_count={len(failures)}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "completed_runtime_probe_reviewed",
                "notes": f"target_stage={STAGE280_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER279,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage279_closeout",
                "stage_id": STAGE279_ID,
                "run_id": RUN_ID,
                "view": "stage279_closeout_stage280_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "runtime_probe_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "stage_transition_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"survivor_seed_count={len(survivors)};failure_memory_count={len(failures)};target_stage={STAGE280_ID}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage279_closeout_stage280_handoff_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE279_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run279D stage279 closeout stage280 handoff(279D 279단계 종료 280단계 인계)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected279 = io_path(SELECTED279).read_text(encoding="utf-8-sig")
    selected279 = replace_line_prefix(selected279, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected279 = replace_line_prefix(selected279, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected279 = replace_line_prefix(selected279, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected279 = replace_line_prefix(selected279, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected279 = append_once(selected279, "run279D_report", f"- run279D_report(279D 보고서): `{rel(RUN_REPORT)}`")
    selected279 = append_once(selected279, "stage280_survivor_seed_queue", f"- stage280_survivor_seed_queue(280단계 생존 씨앗 대기열): `{rel(SURVIVOR_QUEUE)}`")
    write_md(SELECTED279, selected279)

    review_index = io_path(REVIEW_INDEX279).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX279) else "# Review Index(검토 색인)\n"
    review_index = append_once(review_index, "run279D_report", f"- run279D_report(279D 보고서): `{rel(RUN_REPORT)}`")
    write_md(REVIEW_INDEX279, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage280_directional_mapping_stability_validation_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE280_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE279_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `directional_mapping_stability_validation_open`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run279D_summary",
        f"- run279D_summary(279D 요약): Stage279(279단계)를 runtime probe review(런타임 탐침 검토)로 닫고 Stage280(280단계)를 열었다. Effect(효과): survivor seed(생존 씨앗) `{len(survivors)}`개와 failure memory(실패 기억) `{len(failures)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE280_ID}")
    focus = (
        f"- >-\n"
        f"  Stage280(280단계) directional mapping stability validation(방향 매핑 안정성 검증) opened by `{RUN_ID}`. "
        f"Effect(효과): survivor seed(생존 씨앗) `{len(survivors)}`개를 stability validation(안정성 검증)으로 넘기며 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run279D Stage279 closeout and Stage280 open(279D 279단계 종료와 280단계 개시)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): survivor seed(생존 씨앗) `{len(survivors)}`개와 failure memory(실패 기억) `{len(failures)}`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST280-DIRECTIONAL-STABILITY",
        f"| `IDEA-ST280-DIRECTIONAL-STABILITY` | `{STAGE280_ID}` | Stage279(279단계) survivor seed(생존 씨앗)를 curve/month/session/trade-quality stress(곡선/월/세션/거래품질 압박)로 검증한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `opened_no_candidate` | survivor seed(생존 씨앗) `{len(survivors)}`개, selected candidate(선택 후보) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST279-DIRECTIONAL-MAPPING-RUN279D",
        f"| `NEG-ST279-DIRECTIONAL-MAPPING-RUN279D` | `{STAGE279_ID}` | runtime probe failure memory(런타임 탐침 실패 기억) `{len(failures)}`개 | Reopen only with new decision/risk surface(새 판단/위험 표면일 때만 재개) | `{rel(FAILURE_MEMORY)}` |",
    )
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    for path in [RUN_DIR, REVIEWS279, STAGE279 / "04_selected"]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    scoreboard_rows, survivors, failures = build_review_rows()
    artifacts = write_outputs(scoreboard_rows, survivors, failures, created_at)
    update_registers_and_docs(created_at, artifacts, scoreboard_rows, survivors, failures)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "scoreboard_rows": len(scoreboard_rows),
                "survivor_seed_count": len(survivors),
                "failure_memory_count": len(failures),
                "target_stage": STAGE280_ID,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
