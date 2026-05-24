from __future__ import annotations

import ast
import csv
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
    sha256_file_lf_normalized,
    write_csv_rows,
)
from stage_pipelines.stage280.validate_directional_mapping_stability import safe_float, trade_frame  # noqa: E402


STAGE288_ID = "288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild"
STAGE289_ID = "289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild"
RUN_ID = "run288C_review_risk_reward_exit_asymmetry_mt5_probe_v1"
SOURCE_RUN_ID = "run288B_risk_reward_exit_asymmetry_mt5_probe_v1"
STATUS = "completed_risk_reward_exit_review_no_candidate_stage289_opened"
JUDGMENT = "risk_reward_exit_did_not_solve_edge_quality_no_adapter_no_onnx"
NEXT_ACTION = "run289A_design_regime_conditioned_edge_surface_rebuild_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE288 = ROOT / "stages" / STAGE288_ID
RUN288A = STAGE288 / "02_runs" / "run288A"
RUN288B = STAGE288 / "02_runs" / "run288B"
RUN_DIR = STAGE288 / "02_runs" / "run288C"
REVIEWS288 = STAGE288 / "03_reviews"
SELECTED288 = STAGE288 / "04_selected" / "selection_status.md"
REVIEW_INDEX288 = REVIEWS288 / "review_index.md"
STAGE_LEDGER288 = REVIEWS288 / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN288A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN288B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN288B / "execution_result.json"
SOURCE_RUN_MANIFEST = RUN288B / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage288/review_risk_reward_exit_asymmetry_mt5_probe.py")

SCOREBOARD = RUN_DIR / "risk_reward_exit_scoreboard.csv"
LOCAL_POCKETS = RUN_DIR / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
STAGE289_QUEUE = RUN_DIR / "stage289_regime_conditioned_edge_seed_queue.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS288 / "run288C_risk_reward_exit_review_stage289_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage288_risk_reward_exit_review_stage289_open.md"

STAGE289 = ROOT / "stages" / STAGE289_ID
SPEC289 = STAGE289 / "00_spec" / "stage_brief.md"
INPUTS289 = STAGE289 / "01_inputs"
REVIEWS289 = STAGE289 / "03_reviews"
SELECTED289 = STAGE289 / "04_selected" / "selection_status.md"
STAGE_LEDGER289 = REVIEWS289 / "stage_run_ledger.csv"
REVIEW_INDEX289 = REVIEWS289 / "review_index.md"
INPUT_REFS289 = INPUTS289 / "input_refs.md"
QUEUE289 = INPUTS289 / "stage289_regime_conditioned_edge_seed_queue.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_trades_per_day",
    "validation_dd",
    "validation_recovery",
    "validation_expectancy",
    "validation_worst_rolling_20_net",
    "validation_worst_rolling_50_net",
    "validation_underwater_ratio",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_trades_per_day",
    "oos_dd",
    "oos_recovery",
    "oos_expectancy",
    "oos_worst_rolling_20_net",
    "oos_worst_rolling_50_net",
    "oos_underwater_ratio",
    "density_gate",
    "profit_scale_gate",
    "efficiency_gate",
    "curve_quality_gate",
    "review_label",
    "failure_reasons",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
POCKET_COLUMNS = (
    "materialized_branch_id",
    "split",
    "rolling_window",
    "worst_rolling_net",
    "pocket_threshold",
    "pocket_label",
    "source_report_path",
)
FAILURE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "failure_type",
    "failure_reasons",
    "salvage_value",
    "reopen_condition",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "seed_id",
    "source_materialized_branch_id",
    "source_package_id",
    "seed_role",
    "fresh_stage289_question",
    "required_change",
    "forbidden_repair_loop",
    "prior_stage_refs",
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing = read_csv_dicts(path)
    new_keys = {str(row.get(key, "")).strip() for row in rows}
    merged = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, columns, merged)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def parse_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = str(value or "").strip()
    if not text:
        return {}
    return dict(ast.literal_eval(text))


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def parse_records() -> dict[tuple[str, str], dict[str, Any]]:
    records: dict[tuple[str, str], dict[str, Any]] = {}
    known_ids = sorted(manifest_by_id(), key=len, reverse=True)
    for row in read_csv_dicts(SOURCE_KPI):
        if "actual_routed" not in row.get("record_view", ""):
            continue
        metrics = parse_obj(row.get("metrics"))
        report = parse_obj(row.get("report"))
        attempt_name = str(report.get("attempt_name") or row.get("record_view") or "")
        materialized_id = next((item for item in known_ids if item in attempt_name), "")
        if materialized_id:
            records[(materialized_id, str(row.get("split", "")))] = {
                "metrics": metrics,
                "report_path": Path(str(metrics.get("report_path", ""))),
            }
    return records


def rolling_min(values: Sequence[float], window: int) -> float:
    if len(values) < window:
        return 0.0
    return float(pd.Series([float(value) for value in values]).rolling(window).sum().min())


def split_days(split: str) -> int:
    return 183 if split == "validation_is" else 131


def curve_stats(report_path: Path, materialized_id: str, split: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    frame = trade_frame(report_path)
    profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
    balance = 0.0
    peak = 0.0
    underwater = 0
    for profit in profits:
        balance += profit
        peak = max(peak, balance)
        if balance < peak:
            underwater += 1
    pockets = []
    for window, threshold in ((20, -120.0), (50, -150.0)):
        worst = rolling_min(profits, window)
        pockets.append(
            {
                "materialized_branch_id": materialized_id,
                "split": split,
                "rolling_window": window,
                "worst_rolling_net": worst,
                "pocket_threshold": threshold,
                "pocket_label": "deep_local_pocket" if worst < threshold else "tolerable",
                "source_report_path": report_path.as_posix(),
            }
        )
    return {"underwater_ratio": underwater / len(profits) if profits else 0.0}, pockets


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = manifest_by_id()
    records = parse_records()
    scoreboard_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for materialized_id, manifest_row in manifest.items():
        data: dict[str, dict[str, Any]] = {}
        for split in ("validation_is", "oos"):
            entry = records.get((materialized_id, split), {})
            metrics = entry.get("metrics", {})
            curve, pockets = curve_stats(Path(str(entry.get("report_path", ""))), materialized_id, split)
            pocket_rows.extend(pockets)
            data[split] = {
                "net": safe_float(metrics.get("net_profit")),
                "pf": safe_float(metrics.get("profit_factor")),
                "trades": safe_float(metrics.get("trade_count")),
                "tpd": safe_float(metrics.get("trade_count")) / split_days(split),
                "dd": safe_float(metrics.get("max_drawdown_amount")),
                "recovery": safe_float(metrics.get("recovery_factor")),
                "expectancy": safe_float(metrics.get("expectancy")),
                "r20": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 20),
                "r50": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 50),
                "underwater_ratio": curve["underwater_ratio"],
            }
        density_ok = 4.0 <= data["validation_is"]["tpd"] <= 10.0 and 4.0 <= data["oos"]["tpd"] <= 10.0
        profit_ok = data["validation_is"]["net"] > 150.0 and data["oos"]["net"] > 250.0
        efficiency_ok = data["validation_is"]["pf"] >= 1.10 and data["oos"]["pf"] >= 1.10 and data["validation_is"]["recovery"] >= 1.0 and data["oos"]["recovery"] >= 1.0
        curve_ok = (
            data["validation_is"]["r20"] >= -120.0
            and data["oos"]["r20"] >= -120.0
            and data["validation_is"]["r50"] >= -150.0
            and data["oos"]["r50"] >= -150.0
            and data["validation_is"]["underwater_ratio"] <= 0.90
            and data["oos"]["underwater_ratio"] <= 0.90
        )
        reasons: list[str] = []
        if not density_ok:
            reasons.append("trade_density_outside_4_10")
        if not profit_ok:
            reasons.append("profit_scale_not_both_splits")
        if not efficiency_ok:
            reasons.append("efficiency_pf_recovery_not_jointly_credible")
        if not curve_ok:
            reasons.append("curve_quality_local_pockets_or_underwater_ratio_fail")
        label = "adapter_candidate_ready" if not reasons else "risk_reward_exit_negative"
        scoreboard = {
            "materialized_branch_id": materialized_id,
            "package_id": manifest_row["package_id"],
            "validation_net_profit": data["validation_is"]["net"],
            "validation_pf": data["validation_is"]["pf"],
            "validation_trade_count": data["validation_is"]["trades"],
            "validation_trades_per_day": data["validation_is"]["tpd"],
            "validation_dd": data["validation_is"]["dd"],
            "validation_recovery": data["validation_is"]["recovery"],
            "validation_expectancy": data["validation_is"]["expectancy"],
            "validation_worst_rolling_20_net": data["validation_is"]["r20"],
            "validation_worst_rolling_50_net": data["validation_is"]["r50"],
            "validation_underwater_ratio": data["validation_is"]["underwater_ratio"],
            "oos_net_profit": data["oos"]["net"],
            "oos_pf": data["oos"]["pf"],
            "oos_trade_count": data["oos"]["trades"],
            "oos_trades_per_day": data["oos"]["tpd"],
            "oos_dd": data["oos"]["dd"],
            "oos_recovery": data["oos"]["recovery"],
            "oos_expectancy": data["oos"]["expectancy"],
            "oos_worst_rolling_20_net": data["oos"]["r20"],
            "oos_worst_rolling_50_net": data["oos"]["r50"],
            "oos_underwater_ratio": data["oos"]["underwater_ratio"],
            "density_gate": "passed" if density_ok else "failed",
            "profit_scale_gate": "passed" if profit_ok else "failed",
            "efficiency_gate": "passed" if efficiency_ok else "failed",
            "curve_quality_gate": "passed" if curve_ok else "failed",
            "review_label": label,
            "failure_reasons": "|".join(reasons) if reasons else "none",
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard_rows.append(scoreboard)
        if reasons:
            failure_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": manifest_row["package_id"],
                    "failure_type": label,
                    "failure_reasons": "|".join(reasons),
                    "salvage_value": "validation_efficiency_clue" if materialized_id.endswith("cp288D_smooth_control_rr24") else "failure_memory",
                    "reopen_condition": "Only reopen through regime-conditioned edge surface, not exit-only repair.",
                    "claim_boundary": BOUNDARY,
                }
            )
    prior_refs = "|".join([rel(SCOREBOARD), rel(LOCAL_POCKETS), rel(FAILURE_MEMORY), rel(ROOT / "stages/287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild/02_runs/run287C/density_scale_curve_pocket_scoreboard.csv")])
    queue_rows = [
        {
            "seed_id": "stage289_validation_efficiency_oos_failure_cp288D",
            "source_materialized_branch_id": "run288A_cp288D_smooth_control_rr24",
            "source_package_id": "cp288D_smooth_control_rr24_surface",
            "seed_role": "validation_efficiency_clue_oos_failure_not_candidate",
            "fresh_stage289_question": "Can regime-conditioned entry-quality surface keep cp288D validation efficiency while avoiding OOS failure?",
            "required_change": "new regime-conditioned edge surface using session/volatility/macro/trend features",
            "forbidden_repair_loop": "Do not only retune ATR SL/TP or max_hold.",
            "prior_stage_refs": prior_refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage289_scale_seed_cp287E_failure_memory",
            "source_materialized_branch_id": "run287A_cp287E_consensus_pullback_mix",
            "source_package_id": "cp287E_consensus_pullback_mix_surface",
            "seed_role": "scale_density_seed_needs_edge_surface_not_candidate",
            "fresh_stage289_question": "Can a regime-conditioned score surface keep cp287E trade density while lifting expectancy?",
            "required_change": "new scoring surface from feature interactions, not exit-only overlay",
            "forbidden_repair_loop": "Do not only repeat Stage287/288 thresholds.",
            "prior_stage_refs": prior_refs,
            "claim_boundary": BOUNDARY,
        },
    ]
    return scoreboard_rows, pocket_rows, failure_rows, queue_rows


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        f"- `{row['package_id']}`: validation(검증) net `{float(row['validation_net_profit']):.2f}`, OOS(표본외) net `{float(row['oos_net_profit']):.2f}`, gates(게이트) `{row['density_gate']}/{row['profit_scale_gate']}/{row['efficiency_gate']}/{row['curve_quality_gate']}`."
        for row in scoreboard_rows
    ]
    return f"""# run288C Risk Reward Exit Review(288C 위험/보상/청산 검토)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage289_seed_count(289단계 씨앗 수): `{len(queue_rows)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Scoreboard(점수판)

{chr(10).join(lines)}

## Decision(결정)

exit/risk reward(청산/위험보상)만으로는 목표 조건을 만들지 못했다. Effect(효과): Stage288(288단계)는 후보 없이 닫고, Stage289(289단계)는 regime-conditioned edge surface(국면 조건부 엣지 표면)를 새 질문으로 연다.
"""


def stage289_brief(queue_rows: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage289 Regime Conditioned Edge Surface Rebuild(289단계 국면 조건부 엣지 표면 재구성)

- canonical_stage_id(정식 단계 ID): `{STAGE289_ID}`
- big_question(큰 질문): session/volatility/macro/trend regime(세션/변동성/매크로/추세 국면)을 이용해 4-10 trades/day(일 거래)와 수익 규모를 지키면서 expectancy/PF/recovery/curve pocket(기대값/수익 팩터/회복/곡선 포켓)을 동시에 개선할 수 있는가?
- source_stage(원천 단계): `{STAGE288_ID}`
- seed_count(씨앗 수): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): risk/reward-only(위험보상 단독) 수리를 끝내고 edge quality(엣지 품질)와 decision surface(판단 표면)를 새로 만든다.
"""


def write_outputs(scoreboard_rows: Sequence[Mapping[str, Any]], pocket_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], created_at: str) -> list[Path]:
    for path in (RUN_DIR, REVIEWS288, INPUTS289, REVIEWS289, SELECTED289.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(LOCAL_POCKETS, POCKET_COLUMNS, pocket_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(STAGE289_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(QUEUE289, QUEUE_COLUMNS, queue_rows)
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, [{"result_subject": RUN_ID, "evidence_available": f"{rel(SCOREBOARD)};{rel(LOCAL_POCKETS)};{rel(FAILURE_MEMORY)}", "evidence_missing": "Adapter package;ONNX export;ONNX parity;MT5 runtime reproduction for selected package", "judgment_label": JUDGMENT, "judgment_class": "negative_for_candidate_selection_but_seeded_next_stage(후보 선택은 부정, 다음 단계 씨앗 있음)", "claim_boundary": BOUNDARY, "next_condition": NEXT_ACTION, "user_explanation_hook": "청산/위험보상만으로는 엣지 품질을 못 살렸다."}])
    write_csv(GATE_AUDIT, GATE_COLUMNS, [{"gate_name": "risk_reward_exit_review(위험보상청산 검토)", "status": "passed", "evidence_path": rel(SCOREBOARD), "effect": "Stage288(288단계) 후보를 선택하지 않는 근거를 남겼다."}, {"gate_name": "fresh_stage_transition(새 단계 전환)", "status": "passed", "evidence_path": rel(STAGE289_QUEUE), "effect": "exit-only repair(청산 단독 수리)를 끊고 edge surface(엣지 표면)로 넘긴다."}])
    write_md(REPORT, report_markdown(scoreboard_rows, queue_rows))
    write_md(SPEC289, stage289_brief(queue_rows))
    write_md(INPUT_REFS289, f"# Stage289 Input Refs(289단계 입력 참조)\n\n- `{rel(SCOREBOARD)}`\n- `{rel(LOCAL_POCKETS)}`\n- `{rel(FAILURE_MEMORY)}`\n- `{rel(STAGE289_QUEUE)}`\n- `stages/287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild/02_runs/run287C/density_scale_curve_pocket_scoreboard.csv`\n\nEffect(효과): Stage289(289단계)은 risk/reward-only(위험보상 단독) 실패를 참고해 regime-conditioned edge surface(국면 조건부 엣지 표면)를 만든다.\n")
    write_csv(STAGE_LEDGER289, STAGE_LEDGER_COLUMNS, [{"row_id": "stage289_opened_from_run288C", "stage_id": STAGE289_ID, "run_id": RUN_ID, "view": "stage_open", "tier_scope": "not_applicable", "scoreboard": "stage289_seed_queue", "status": "opened_regime_conditioned_edge_surface_rebuild", "judgment": "stage_opened_no_candidate", "evidence_boundary": "planning_from_stage288_failure_memory", "report_path": rel(REPORT), "notes": f"seed_count={len(queue_rows)};next_action={NEXT_ACTION}"}])
    write_md(REVIEW_INDEX289, f"# Stage289 Review Index(289단계 검토 색인)\n\n- input_refs(입력 참조): `{rel(INPUT_REFS289)}`\n- seed_queue(씨앗 대기열): `{rel(QUEUE289)}`\n")
    write_md(SELECTED289, f"""# Stage289 Selection Status(289단계 선택 상태)

- stage_status(단계 상태): `opened_regime_conditioned_edge_surface_rebuild`
- current_packet(현재 작업 묶음): `stage289_regime_conditioned_edge_surface_rebuild_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE288_ID}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUT_REFS289)}`
""")
    write_md(DECISION, f"# Stage288 Closeout and Stage289 Open(288단계 종료와 289단계 개방)\n\n- decision_date(결정일): `{UPDATED_ON}`\n- source_run(원천 실행): `{RUN_ID}`\n- selected_candidate(선택 후보): `none`\n- reason(이유): risk/reward/exit(위험/보상/청산)만으로는 OOS(표본외)와 곡선 포켓을 해결하지 못했다.\n- next_stage(다음 단계): `{STAGE289_ID}`\n- next_action(다음 행동): `{NEXT_ACTION}`\n\nEffect(효과): Adapter/ONNX(어댑터/온엑스)로 넘어가지 않고 regime-conditioned edge surface(국면 조건부 엣지 표면) 연구로 이동한다.\n")
    final = [SCOREBOARD, LOCAL_POCKETS, FAILURE_MEMORY, STAGE289_QUEUE, QUEUE289, RESULT_JUDGMENT, GATE_AUDIT, REPORT, SPEC289, INPUT_REFS289, STAGE_LEDGER289, REVIEW_INDEX289, SELECTED289, DECISION]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE288_ID, "source_run_id": SOURCE_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "created_at_utc": created_at, "scoreboard_rows": len(scoreboard_rows), "failure_rows": len(failure_rows), "stage289_seed_count": len(queue_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final if path_exists(path)}, "claim_boundary": BOUNDARY})
    final.append(RUN_MANIFEST)
    write_json(LINEAGE, {"run_id": RUN_ID, "producer": PRODUCER.as_posix(), "source_artifacts": [rel(SOURCE_MANIFEST), rel(SOURCE_KPI), rel(SOURCE_EXECUTION), rel(SOURCE_RUN_MANIFEST)], "produced_artifacts": [rel(path) for path in final if path_exists(path)], "claim_boundary": BOUNDARY})
    final.append(LINEAGE)
    return [path for path in final if path_exists(path)]


def update_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE288_ID, "lane": "risk_reward_exit_review", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"scoreboard_rows={len(scoreboard_rows)};stage289_seed_count={len(queue_rows)};selected_candidate=none;next_action={NEXT_ACTION}"}], key="run_id")
    upsert_csv(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__review", "stage_id": STAGE288_ID, "run_id": RUN_ID, "subrun_id": "run288C", "parent_run_id": SOURCE_RUN_ID, "record_view": "risk_reward_exit_review(위험/보상/청산 검토)", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "kpi_scope": "candidate_selection_review", "scoreboard_lane": "risk_reward_exit_asymmetry", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};stage289_seed_count={len(queue_rows)}", "guardrail_kpi": "selected_candidate=none;adapter=none;onnx=not_claimed", "external_verification_status": "completed_run288B_mt5_probe", "notes": "Stage288 closed with no candidate; Stage289 opened."}], key="ledger_row_id")
    upsert_csv(STAGE_LEDGER288, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE288_ID, "run_id": RUN_ID, "view": "risk_reward_exit_review", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "scoreboard": rel(SCOREBOARD), "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "no_candidate_no_adapter_no_onnx", "report_path": rel(REPORT), "notes": f"failure_rows={len(failure_rows)};stage289_seed_count={len(queue_rows)}."}], key="row_id")
    artifact_rows = [{"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage288_risk_reward_exit_review_artifact", "path": rel(path), "sha256": sha256_file_lf_normalized(path), "stage_id": STAGE288_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "run288C risk reward exit review(288C 위험/보상/청산 검토)"} for path in artifacts if path_exists(path)]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = io_path(SELECTED288).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- selected_candidate(선택 후보):", "- selected_candidate(선택 후보): `none`")
    selected = replace_line_prefix(selected, "- Adapter package(어댑터 패키지):", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run288C_report", f"- run288C_report(288C 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage289_open", f"- stage289_open(289단계 개방): `{STAGE289_ID}`")
    write_md(SELECTED288, selected)
    review_index = io_path(REVIEW_INDEX288).read_text(encoding="utf-8-sig")
    review_index = append_once(review_index, "run288C_report", f"- run288C_report(288C 보고서): `{rel(REPORT)}`\n- run288C_scoreboard(288C 점수판): `{rel(SCOREBOARD)}`\n- run288C_failure_memory(288C 실패 기억): `{rel(FAILURE_MEMORY)}`")
    write_md(REVIEW_INDEX288, review_index)
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage289_regime_conditioned_edge_surface_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE289_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run288C_summary", f"- run288C_summary(288C 요약): Stage288(288단계)은 risk/reward/exit(위험/보상/청산)만으로 후보를 만들지 못해 후보 없이 닫고 Stage289(289단계)을 열었다. Effect(효과): Adapter/ONNX(어댑터/온엑스)는 진행하지 않고 regime-conditioned edge surface(국면 조건부 엣지 표면)를 새 질문으로 넘긴다.")
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE289_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage288(288단계) run288C(288C 실행) risk reward exit review(위험/보상/청산 검토) `{RUN_ID}` closed Stage288 and opened Stage289(289단계). Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 없고 next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(changelog, RUN_ID, f"## {UPDATED_ON} run288C Risk reward exit review(288C 위험/보상/청산 검토)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Stage288(288단계)을 selected candidate(선택 후보) 없이 닫고 Stage289(289단계)을 열었다.\n- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `not_claimed`다.\n")
    write_md(CHANGELOG, changelog)
    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(idea, "IDEA-ST289-REGIME-CONDITIONED-EDGE-SURFACE", f"| `IDEA-ST289-REGIME-CONDITIONED-EDGE-SURFACE` | `{STAGE289_ID}` | regime-conditioned edge surface(국면 조건부 엣지 표면) | `Tier A used + Tier B fallback stress + actual routed total` | `opened` | Stage288(288단계) exit/risk-only(청산/위험 단독) 실패 후 session/volatility/macro/trend(세션/변동성/매크로/추세) 결합 표면을 만든다. |")
    write_md(IDEA_REGISTER, idea)
    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(negative, "NEG-ST288-RISK-REWARD-EXIT", f"| `NEG-ST288-RISK-REWARD-EXIT` | `{STAGE288_ID}` | `{RUN_ID}` | risk/reward/exit-only failed(위험/보상/청산 단독 실패) | OOS and curve did not survive(표본외와 곡선 생존 실패) | reopen only with regime-conditioned edge surface(국면 조건부 엣지 표면으로만 재개) |")
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    created_at = utc_now()
    scoreboard_rows, pocket_rows, failure_rows, queue_rows = build_outputs()
    artifacts = write_outputs(scoreboard_rows, pocket_rows, failure_rows, queue_rows, created_at)
    update_docs(created_at, artifacts, scoreboard_rows, failure_rows, queue_rows)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "scoreboard_rows": len(scoreboard_rows), "failure_rows": len(failure_rows), "stage289_seed_count": len(queue_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
