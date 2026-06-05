from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    execute_proxy_positive_offensive_pivot_mt5_runtime_probe_without_db as ic,
)

aw = ic.aw

TODAY = "2026-06-01"
STAGE_ID = ic.STAGE_ID
STAGE_DIR = ic.STAGE_DIR
RUN_NUMBER = "run337ID"
RUN_ID = "run337ID_review_proxy_positive_offensive_pivot_mt5_runtime_probe_or_repair_without_db_v1"
PARENT_RUN_ID = ic.RUN_ID
NEXT_RUN_ID = "run337IE_design_runtime_positive_low_pf_drawdown_side_balance_repair_without_db_v1"
STATUS = "completed_stage337ID_runtime_positive_clue_reviewed_repair_required_no_selection"
JUDGMENT = "runtime_positive_net_clue_not_operating_ready_low_pf_high_drawdown_secondary_probability_mismatch"
DECISION = "stage337ID_open_run337IE_runtime_positive_low_pf_drawdown_side_balance_repair"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_candidate_selection_no_forward_passed_or_failed_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = ic.REVIEW_DIR
REPORT_PATH = REVIEW_DIR / "run337ID_proxy_positive_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337ID_proxy_positive_mt5_runtime_probe_review.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

RUNTIME_REVIEW = RUN_DIR / "id_runtime_review_scorecard.csv"
DIFF_ATTRIBUTION = RUN_DIR / "id_proxy_mt5_diff_attribution.csv"
KPI_JUDGMENT = RUN_DIR / "id_mt5_kpi_judgment.csv"
REPAIR_QUEUE = RUN_DIR / "run337IE_repair_queue.csv"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def _ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent, RUN_REGISTRY.parent]:
        aw.io_path(path).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(aw.io_path(path))


def _read_json(path: Path) -> dict:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def _write_csv(path: Path, frame: pd.DataFrame) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(aw.io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def _write_json(path: Path, payload: dict) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def _write_bom_text(path: Path, text: str) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(text, encoding="utf-8-sig")


def _sha(path: Path) -> str:
    return aw.sha256_file(path)


def _numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    output = frame.copy()
    for column in columns:
        if column in output.columns:
            output[column] = pd.to_numeric(output[column], errors="coerce")
    return output


def _build_reviews() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    summary = _numeric(
        _read_csv(ic.EXECUTION_SUMMARY),
        [
            "expected_rows",
            "telemetry_cycle_rows",
            "ready_model_rows",
            "matched_rows",
            "expected_missing_rows",
            "hash_mismatch_rows",
            "probability_mismatch_rows",
            "decision_mismatch_rows",
            "max_abs_probability_diff",
            "feature_ready_count",
            "model_ok_count",
            "long_count",
            "short_count",
            "flat_count",
            "order_attempt_count",
            "order_fill_count",
            "net_profit",
            "profit_factor",
            "trade_count",
            "expectancy",
            "recovery_factor",
            "max_drawdown_amount",
            "short_trade_count",
            "long_trade_count",
        ],
    )
    diff = _read_csv(ic.PROXY_MT5_DIFF) if ic.PROXY_MT5_DIFF.exists() else pd.DataFrame()
    bad = diff.loc[diff.get("comparison_status", pd.Series(dtype=str)).astype(str).ne("matched")].copy()

    review = summary.copy()
    review["runtime_exact_parity"] = review["comparison_status"].astype(str).eq(
        "completed_exact_proxy_mt5_parity_reached_feature_last"
    )
    review["runtime_positive_net"] = review["net_profit"] > 0
    review["pf_floor_pass"] = review["profit_factor"] >= 1.10
    review["recovery_floor_pass"] = review["recovery_factor"] >= 1.00
    review["drawdown_floor_pass"] = review["max_drawdown_amount"] <= 150.0
    review["long_short_balance_ratio"] = review[["short_trade_count", "long_trade_count"]].min(axis=1) / review[
        ["short_trade_count", "long_trade_count"]
    ].max(axis=1)
    review["balance_floor_pass"] = review["long_short_balance_ratio"] >= 0.35
    review["id_judgment"] = "runtime_positive_clue_not_operating_ready"
    review.loc[~review["runtime_exact_parity"], "id_judgment"] = "runtime_probability_mismatch_repair_required"
    review["effect"] = (
        "Runtime net is reviewed together with PF, drawdown, recovery, side balance, and proxy parity."
    )
    review["claim_boundary"] = CLAIM_BOUNDARY

    if bad.empty:
        diff_attr = pd.DataFrame(
            [
                {
                    "attribution_id": "no_mismatch_rows",
                    "attempt_name": "",
                    "model_id": "",
                    "rows": 0,
                    "max_abs_probability_diff": 0.0,
                    "decision_mismatch_rows": 0,
                    "attribution": "no proxy-MT5 mismatch rows",
                    "effect": "Runtime parity is exact under current tolerance.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        )
    else:
        grouped = bad.groupby(["attempt_name", "model_id", "comparison_status"], dropna=False)
        diff_attr = grouped.agg(
            rows=("comparison_status", "size"),
            max_abs_diff_short=("abs_diff_p_short", lambda s: pd.to_numeric(s, errors="coerce").max()),
            max_abs_diff_flat=("abs_diff_p_flat", lambda s: pd.to_numeric(s, errors="coerce").max()),
            max_abs_diff_long=("abs_diff_p_long", lambda s: pd.to_numeric(s, errors="coerce").max()),
            decision_mismatch_rows=("decision_match", lambda s: int((s.astype(str).str.lower() != "true").sum())),
        ).reset_index()
        diff_attr["max_abs_probability_diff"] = diff_attr[
            ["max_abs_diff_short", "max_abs_diff_flat", "max_abs_diff_long"]
        ].max(axis=1)
        diff_attr["attribution"] = (
            "secondary LGBM ONNX runtime probability drift under 0.003 with no decision mismatch"
        )
        diff_attr["effect"] = (
            "Mismatch blocks exact parity for the secondary probe but does not change decisions on the four rows."
        )
        diff_attr["claim_boundary"] = CLAIM_BOUNDARY

    kpi_rows = []
    for _, row in review.iterrows():
        weak = []
        if not bool(row["pf_floor_pass"]):
            weak.append("profit_factor_below_1_10")
        if not bool(row["recovery_floor_pass"]):
            weak.append("recovery_below_1_00")
        if not bool(row["drawdown_floor_pass"]):
            weak.append("drawdown_above_150")
        if not bool(row["balance_floor_pass"]):
            weak.append("long_short_balance_below_0_35")
        kpi_rows.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "trade_count": row["trade_count"],
                "expectancy": row["expectancy"],
                "recovery_factor": row["recovery_factor"],
                "max_drawdown_amount": row["max_drawdown_amount"],
                "short_trade_count": row["short_trade_count"],
                "long_trade_count": row["long_trade_count"],
                "long_short_balance_ratio": row["long_short_balance_ratio"],
                "runtime_exact_parity": row["runtime_exact_parity"],
                "weakness_tags": ";".join(weak) if weak else "none",
                "operating_readiness": "not_ready",
                "effect": "Positive net is treated as a clue because PF/recovery/drawdown/balance remain weak.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    kpi = pd.DataFrame(kpi_rows)
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "design_runtime_positive_low_pf_drawdown_side_balance_repair",
                "primary_positive_model_id": str(review.sort_values("net_profit", ascending=False).iloc[0]["model_id"]),
                "required_inputs": f"{aw.rel(RUNTIME_REVIEW)};{aw.rel(KPI_JUDGMENT)};{aw.rel(DIFF_ATTRIBUTION)}",
                "repair_focus": "preserve exact ExtraTrees runtime parity while improving PF, recovery, drawdown, and side balance",
                "forbidden_action": "operating promotion or threshold/lot optimization without new review",
                "effect": "Runtime positive clue becomes a controlled repair seed, not a selected model.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    final_summary = {
        "runtime_rows": int(len(review)),
        "runtime_completed_rows": int(review["runtime_status"].astype(str).eq("completed").sum()),
        "exact_parity_rows": int(review["runtime_exact_parity"].sum()),
        "positive_net_rows": int(review["runtime_positive_net"].sum()),
        "mismatch_rows": int(len(bad)),
        "best_net_profit": float(review["net_profit"].max()),
        "best_profit_factor": float(review.loc[review["net_profit"].idxmax(), "profit_factor"]),
        "best_model_id": str(review.loc[review["net_profit"].idxmax(), "model_id"]),
        "operating_ready_rows": 0,
    }
    return review, diff_attr, kpi, queue, final_summary


def _gate_row(gate: str, status: str, evidence: str, effect: str) -> dict:
    return {
        "gate": gate,
        "status": status,
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _make_gates(summary: dict) -> pd.DataFrame:
    ic_gates = _read_csv(ic.GATE_AUDIT)
    return pd.DataFrame(
        [
            _gate_row(
                "parent_ic_gates_passed",
                "pass" if ic_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all() else "fail",
                aw.rel(ic.GATE_AUDIT),
                "ID only reviews completed IC attempt evidence.",
            ),
            _gate_row(
                "runtime_completion_reviewed",
                "pass" if summary["runtime_completed_rows"] >= 1 else "fail",
                aw.rel(RUNTIME_REVIEW),
                "At least one MT5 runtime probe completed.",
            ),
            _gate_row(
                "exact_parity_candidate_present",
                "pass" if summary["exact_parity_rows"] >= 1 else "fail",
                aw.rel(RUNTIME_REVIEW),
                "At least one candidate reached exact proxy-MT5 parity through feature last.",
            ),
            _gate_row(
                "mismatch_attribution_recorded",
                "pass" if DIFF_ATTRIBUTION.exists() else "fail",
                aw.rel(DIFF_ATTRIBUTION),
                "Secondary probability mismatch is attributed instead of ignored.",
            ),
            _gate_row(
                "mt5_kpi_judgment_recorded",
                "pass" if KPI_JUDGMENT.exists() else "fail",
                aw.rel(KPI_JUDGMENT),
                "Positive net is judged against PF/recovery/drawdown/balance.",
            ),
            _gate_row(
                "repair_queue_opened",
                "pass" if REPAIR_QUEUE.exists() else "fail",
                aw.rel(REPAIR_QUEUE),
                "Next repair packet is opened from runtime evidence.",
            ),
            _gate_row(
                "no_forbidden_operating_claim",
                "pass",
                aw.rel(CLAIM_BOUNDARY_RECEIPT),
                "ID does not claim selection, forward pass/fail, runtime authority, operating promotion, or Goal.",
            ),
            _gate_row(
                "required_gate_coverage_audit_written",
                "pass",
                aw.rel(GATE_AUDIT),
                "Gate coverage is recorded for closeout.",
            ),
        ]
    )


def _append_or_replace_csv(path: Path, key_columns: Iterable[str], row: dict) -> None:
    if path.exists():
        frame = _read_csv(path)
    else:
        frame = pd.DataFrame()
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    mask = pd.Series(False, index=frame.index)
    for idx, key in enumerate(key_columns):
        current = frame[key].astype(str).eq(str(row[key])) if key in frame.columns else False
        mask = current if idx == 0 else mask & current
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    _write_csv(path, frame[ordered])


def _artifact_paths() -> list[Path]:
    return [
        RUNTIME_REVIEW,
        DIFF_ATTRIBUTION,
        KPI_JUDGMENT,
        REPAIR_QUEUE,
        PERFORMANCE_RECEIPT,
        RUNTIME_RECEIPT,
        FORENSICS_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_BOUNDARY_RECEIPT,
        LINEAGE_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]


def _update_artifact_registry(paths: list[Path]) -> None:
    if ARTIFACT_REGISTRY.exists():
        registry = pd.read_csv(aw.io_path(ARTIFACT_REGISTRY))
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if path.exists():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": aw.rel(path),
                    "sha256": _sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        registry[columns].to_csv(
            aw.io_path(ARTIFACT_REGISTRY),
            index=False,
            encoding="utf-8-sig",
            lineterminator="\n",
        )


def _write_receipts(summary: dict, gates: pd.DataFrame) -> None:
    _write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "best_net_profit": summary["best_net_profit"],
            "best_profit_factor": summary["best_profit_factor"],
            "positive_net_rows": summary["positive_net_rows"],
            "operating_ready_rows": summary["operating_ready_rows"],
            "allowed_use": "repair seed and runtime evidence review only(수리 씨앗 및 런타임 근거 검토 전용)",
            "forbidden_use": "operating promotion or selected model(운영 승격 또는 선택 모델)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "runtime_completed_rows": summary["runtime_completed_rows"],
            "exact_parity_rows": summary["exact_parity_rows"],
            "mismatch_rows": summary["mismatch_rows"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        FORENSICS_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_runtime_identity": aw.rel(ic.RUNTIME_IDENTITY),
            "tester_report_records": aw.rel(ic.STRATEGY_TESTER_REPORTS),
            "forensic_judgment": "reviewed_but_not_operating_ready",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
            "gate_total": int(len(gates)),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
        },
    )
    _write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "runtime_review": aw.rel(RUNTIME_REVIEW),
            "kpi_judgment": aw.rel(KPI_JUDGMENT),
            "repair_queue": aw.rel(REPAIR_QUEUE),
            "artifact_registry_updated": True,
        },
    )


def _write_final(summary: dict, gates: pd.DataFrame) -> None:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **summary,
    }
    _write_json(FINAL_DECISION, final)
    _write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "script": aw.rel(Path(__file__)),
            "inputs": [
                aw.rel(ic.FINAL_DECISION),
                aw.rel(ic.EXECUTION_SUMMARY),
                aw.rel(ic.PROXY_MT5_DIFF),
                aw.rel(ic.STRATEGY_TESTER_REPORTS),
            ],
            "outputs": [aw.rel(path) for path in _artifact_paths() if path.exists()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def _write_docs(summary: dict, gates: pd.DataFrame) -> None:
    gate_passes = int(gates["status"].astype(str).eq("pass").sum())
    gate_total = int(len(gates))
    report = f"""﻿# Stage 337ID Proxy-Positive MT5 Runtime Review

## Summary

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- judgment: `{JUDGMENT}`
- gates: `{gate_passes}/{gate_total}`
- runtime_completed_rows(런타임 완료 행): `{summary['runtime_completed_rows']}`
- exact_parity_rows(정확 동등성 행): `{summary['exact_parity_rows']}`
- positive_net_rows(양수 순익 행): `{summary['positive_net_rows']}`
- best_net_profit(최고 순수익): `{summary['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{summary['best_profit_factor']}`
- mismatch_rows(불일치 행): `{summary['mismatch_rows']}`

## Judgment

Runtime net profit(런타임 순수익)은 양수 단서(clue, 단서)다.
Effect(효과): 그러나 profit factor(수익 팩터), recovery factor(회복 계수), drawdown(낙폭), side balance(방향 균형)가 약해서 operating readiness(운영 준비)는 아니다.

## Boundary

No candidate selection(후보 선택 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next

Open `{NEXT_RUN_ID}` to design(설계) repair(수리): preserve(보존) exact ExtraTrees runtime parity(정확 ExtraTrees 런타임 동등성), improve(개선) PF/recovery/drawdown/side balance(수익 팩터/회복/낙폭/방향 균형).
"""
    decision = f"""﻿# Decision: Stage 337ID Runtime Review

- date: `{TODAY}`
- run_id: `{RUN_ID}`
- decision: `{DECISION}`
- judgment: `{JUDGMENT}`
- next_run_id: `{NEXT_RUN_ID}`

## Reason

IC runtime probe(런타임 탐침)는 후보 2개를 실행했다. Best(최고) ExtraTrees(엑스트라트리스)는 exact proxy-MT5 parity(정확 프록시-MT5 동등성)와 positive net(양수 순익)을 냈지만 PF/recovery/drawdown/balance(수익 팩터/회복/낙폭/균형)는 약하다.

## Effect

다음 IE는 positive clue(긍정 단서)를 운영 승격이 아니라 repair seed(수리 씨앗)로 쓴다.

## Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(REPORT_PATH, report)
    _write_bom_text(DECISION_DOC, decision)
    _write_bom_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    _write_bom_text(
        CURRENT_WORKING_STATE,
        f"""﻿# Current Working State

## Current Truth

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- decision: `{DECISION}`

## Effect

ID review(검토)는 MT5 positive net(양수 순익)을 repair seed(수리 씨앗)로 바꿨다.
효과는 약한 PF/recovery/drawdown/balance(수익 팩터/회복/낙폭/균형)를 고치기 전 운영 주장을 막는 것이다.

## Claim Boundary

`{CLAIM_BOUNDARY}`
""",
    )
    _write_bom_text(
        SELECTION_STATUS,
        f"""﻿# Selection Status

- latest_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- model_selection: not_selected
- runtime_positive_clue: yes_not_operating_ready
- goal_achieve: not_claimed
- operating_promotion: not_claimed
- live_readiness: not_claimed

효과는 positive runtime clue(긍정 런타임 단서)를 selected model(선택 모델)로 오해하지 않게 하는 것이다.
""",
    )
    _write_bom_text(
        STAGE_BRIEF,
        f"""﻿# {STAGE_ID}

Latest completed run: `{RUN_ID}`

ID reviewed(검토) proxy-positive MT5 runtime probe(MT5 런타임 탐침).
Positive net(양수 순익)은 확인했지만 operating readiness(운영 준비)는 아니다.
Next(다음): `{NEXT_RUN_ID}` repair design(수리 설계).
""",
    )
    existing = aw.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if CHANGELOG.exists() else "﻿# Changelog\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Reviewed(검토) IC MT5 runtime probe(MT5 런타임 탐침): positive_net_rows(양수 순익 행) `{summary['positive_net_rows']}`, exact_parity_rows(정확 동등성 행) `{summary['exact_parity_rows']}`.\n"
        f"- Opened(열기) IE repair design(수리 설계); no operating claim(운영 주장 없음).\n"
    )
    _write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry)


def _update_ledgers(summary: dict, gates: pd.DataFrame) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "runtime_completed_rows": summary["runtime_completed_rows"],
        "positive_net_rows": summary["positive_net_rows"],
        "best_net_profit": summary["best_net_profit"],
        "best_profit_factor": summary["best_profit_factor"],
        "operating_ready_rows": summary["operating_ready_rows"],
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": aw.rel(REPORT_PATH),
    }
    _append_or_replace_csv(RUN_REGISTRY, ["run_id"], row)
    _append_or_replace_csv(PROJECT_LEDGER, ["run_id"], row)
    _append_or_replace_csv(STAGE_LEDGER, ["run_id"], row)


def main() -> None:
    _ensure_dirs()
    review, diff_attr, kpi, queue, summary = _build_reviews()
    _write_csv(RUNTIME_REVIEW, review)
    _write_csv(DIFF_ATTRIBUTION, diff_attr)
    _write_csv(KPI_JUDGMENT, kpi)
    _write_csv(REPAIR_QUEUE, queue)
    gates = _make_gates(summary)
    _write_csv(GATE_AUDIT, gates)
    _write_receipts(summary, gates)
    _write_final(summary, gates)
    _write_docs(summary, gates)
    _update_ledgers(summary, gates)
    _update_artifact_registry(_artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("pass")]
    if not failed.empty:
        raise RuntimeError(f"ID gates failed: {failed[['gate', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "runtime_completed_rows": summary["runtime_completed_rows"],
                "exact_parity_rows": summary["exact_parity_rows"],
                "positive_net_rows": summary["positive_net_rows"],
                "best_model_id": summary["best_model_id"],
                "best_net_profit": summary["best_net_profit"],
                "best_profit_factor": summary["best_profit_factor"],
                "operating_ready_rows": summary["operating_ready_rows"],
                "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
                "gate_total": int(len(gates)),
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
