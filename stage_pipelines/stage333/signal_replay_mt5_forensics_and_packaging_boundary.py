from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage330 import raw_forward_mt5_kpi_regime_cost_curve_review as review  # noqa: E402
STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN_ID = "run333F_signal_replay_mt5_forensics_and_packaging_boundary_v1"
RUN_NUMBER = "run333F"
PARENT_RUN_ID = "run333E_runtime_probe_queue_or_failure_memory_from_screen_v1"
EXPLORATION_LABEL = "stage333_Review__SignalReplayMt5ForensicsPackagingBoundary"
CLAIM_BOUNDARY = (
    "research_development_only_signal_payload_mt5_forensics_no_threshold_retuning_no_lot_optimization_"
    "identity_bridge_not_candidate_onnx_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
STATUS = "completed_signal_replay_mt5_forensics_packaging_boundary_no_forward_decision"
JUDGMENT = "signal_payload_mt5_positive_but_packaging_boundary_research_only_no_goal_achieve"
DECISION = "stage333F_signal_replay_positive_mt5_not_cp322a_forward_authority_packaging_boundary_required"
NEXT_ACTION = "run333G_materialize_exact_candidate_runtime_handoff_or_preserve_boundary_v1"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN333E_DIR = STAGE_DIR / "02_runs" / "run333E"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage333F_signal_replay_mt5_forensics_packaging_boundary.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def configure_imported_review_helpers() -> None:
    review.RUN_ID = RUN_ID
    review.PARENT_RUN_ID = PARENT_RUN_ID
    review.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    review.RUN330E_DIR = RUN333E_DIR


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(review.io_path(path).read_text(encoding="utf-8"))


def load_attempts() -> list[dict[str, Any]]:
    return read_json(RUN333E_DIR / "mt5_probe_attempts.json")


def build_db_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "attempt_name": attempt["attempt_name"],
            "artifact_slug": attempt["artifact_slug"],
            "candidate_id": attempt["candidate_id"],
            "db_source": "not_available",
            "status": "out_of_scope_by_claim",
            "reason": (
                "run333E replays a guarded signal payload through an identity probability bridge. "
                "No original cp322A D/B source tag is present in the runtime telemetry."
            ),
            "effect": (
                "D/B attribution is not invented. An exact candidate handoff must carry source tags "
                "before D/B source authority can be claimed."
            ),
        }
        for attempt in attempts
    ]


def build_packaging_boundary_rows(attempts: Sequence[Mapping[str, Any]], kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    kpi_by_attempt = {str(row["attempt_name"]): row for row in kpi_rows}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        preflight = dict(attempt.get("preflight", {}))
        onnx_check = dict(attempt.get("onnxruntime_check", {}))
        kpi = kpi_by_attempt.get(str(attempt["attempt_name"]), {})
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "source_artifact": attempt["source_artifact"],
                "candidate_id": attempt["candidate_id"],
                "runtime_bridge": "identity_probability_bridge_not_candidate_onnx",
                "threshold": preflight.get("threshold"),
                "signal_payload_parity_matched": preflight.get("signal_payload_parity_matched"),
                "source_signal_rows": preflight.get("source_signal_rows"),
                "guarded_signal_rows": preflight.get("guarded_signal_rows"),
                "replay_nonflat_rows": preflight.get("replay_nonflat_rows"),
                "forced_flat_rows": preflight.get("forced_flat_rows"),
                "onnxruntime_max_abs_diff": onnx_check.get("max_abs_diff"),
                "mt5_net_profit": kpi.get("net_profit"),
                "mt5_profit_factor": kpi.get("profit_factor"),
                "mt5_trade_count": kpi.get("trade_count"),
                "packaging_boundary": (
                    "positive MT5 result belongs to the guarded signal replay package, not to a proven "
                    "exact cp322A ONNX runtime handoff."
                ),
                "forward_decision": "not_available_from_signal_replay_bridge",
                "effect": (
                    "This keeps the research useful while preventing operating promotion, runtime authority, "
                    "or Goal Achieve from being claimed."
                ),
            }
        )
    return rows


def build_decision_payload(
    kpi_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    stress_1 = {
        str(row["attempt_name"]): row
        for row in cost_rows
        if float(row["extra_cost_per_round_trip_account_ccy"]) == 1.0
    }
    supportive_signal_evidence: list[str] = []
    fragility_flags: list[str] = []
    for row in kpi_rows:
        attempt = str(row["attempt_name"])
        pf = review.to_float(row.get("profit_factor")) or 0.0
        net = review.to_float(row.get("net_profit")) or 0.0
        dd_pct = review.to_float(row.get("equity_dd_percent")) or 999.0
        survives_cost = bool(stress_1.get(attempt, {}).get("survives_pf_gt_1"))
        if net > 0 and pf > 1.2 and dd_pct <= 15 and survives_cost:
            supportive_signal_evidence.append(attempt)
        if net <= 0 or pf <= 1.05 or not survives_cost:
            fragility_flags.append(attempt)
    worst_chunks = [
        row
        for row in curve_rows
        if row.get("chunk_type") == "rolling_worst_net"
    ]
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "supportive_signal_evidence_not_selection": supportive_signal_evidence,
        "fragility_flags": fragility_flags,
        "worst_curve_pocket_count": len(worst_chunks),
        "reason": (
            "run333E produced completed MT5 report and telemetry for a guarded signal payload replay. "
            "The positive KPI is useful evidence, but the ONNX is an identity bridge and D/B source tags "
            "are absent, so this cannot become cp322A forward authority."
        ),
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "runtime_parity(런타임 동등성)",
            "status": "completed_with_boundary",
            "evidence_path": review.rel(RUN333E_DIR / "runtime_parity_receipt.json"),
            "effect": "run333E MT5 report/telemetry(보고서/실행기록)를 검토 입력으로 쓰되 runtime authority(런타임 권위)는 주장하지 않는다.",
        },
        {
            "gate_name": "backtest_forensics(백테스트 포렌식)",
            "status": "completed",
            "evidence_path": review.rel(RUN333E_DIR / "backtest_forensics_receipt.json"),
            "effect": "Strategy Tester(전략 테스터) report(보고서), telemetry(실행기록), report hash(보고서 해시)를 연결한다.",
        },
        {
            "gate_name": "performance_attribution(성과 귀속)",
            "status": "completed",
            "evidence_path": review.rel(RUN_DIR / "performance_attribution_receipt.json"),
            "effect": "KPI(핵심 성과 지표)를 direction/session/hour/month/cost/curve pocket(방향/세션/시간/월/비용/곡선 포켓)으로 분해한다.",
        },
        {
            "gate_name": "packaging_boundary(패키징 경계)",
            "status": "completed",
            "evidence_path": review.rel(RUN_DIR / "packaging_boundary_report.csv"),
            "effect": "identity bridge(정체성 연결기) 결과를 exact cp322A ONNX authority(정확 cp322A 온엑스 권위)로 오해하지 않게 막는다.",
        },
        {
            "gate_name": "result_judgment(결과 판정)",
            "status": "passed_no_goal_achieve",
            "evidence_path": review.rel(RUN_DIR / "result_judgment.csv"),
            "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
        {
            "gate_name": "artifact_lineage(산출물 계보)",
            "status": "passed",
            "evidence_path": review.rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "effect": "run333E MT5 evidence(근거)에서 run333F review(검토)까지 입력과 산출물을 연결한다.",
        },
    ]


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        RUN333E_DIR / "execution_result.json",
        RUN333E_DIR / "mt5_runtime_probe_summary.csv",
        RUN333E_DIR / "mt5" / "reports",
        RUN333E_DIR / "runtime_telemetry",
        RUN333E_DIR / "signal_replay_preflight_audit.csv",
    ]
    all_paths = list(dict.fromkeys([*artifacts, Path(__file__)]))
    return {
        "generated_at_utc": generated_at_utc,
        "source_inputs": [review.rel(path) for path in inputs],
        "producer": review.rel(Path(__file__)),
        "consumer": NEXT_ACTION,
        "artifact_paths": [review.rel(path) for path in all_paths if path.exists()],
        "artifact_hashes": {
            review.rel(path): review.sha256_file(path)
            for path in all_paths
            if path.exists() and path.is_file()
        },
        "lineage_judgment": "connected_with_signal_replay_packaging_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_reports(kpi_rows: Sequence[Mapping[str, Any]], decision_payload: Mapping[str, Any]) -> list[Path]:
    rows = sorted(kpi_rows, key=lambda row: float(row.get("net_profit") or 0.0), reverse=True)
    table = "\n".join(
        [
            "| attempt(시도) | net(순손익) | PF(수익 팩터) | trades/day(일 거래) | DD%(드로다운 퍼센트) | recovery(회복 계수) |",
            "|---|---:|---:|---:|---:|---:|",
            *[
                f"| {row['attempt_name']} | {row['net_profit']} | {row['profit_factor']} | {row['trades_per_day']} | {row['equity_dd_percent']} | {row['recovery_factor']} |"
                for row in rows
            ],
        ]
    )
    supportive = ", ".join(str(item) for item in decision_payload["supportive_signal_evidence_not_selection"]) or "none"
    fragile = ", ".join(str(item) for item in decision_payload["fragility_flags"]) or "none"
    report = review.write_md(
        REVIEWS_DIR / "run333F_signal_replay_mt5_forensics_and_packaging_boundary.md",
        f"""
# run333F Signal Replay MT5 Forensics And Packaging Boundary(333F 신호 재생 MT5 포렌식 및 패키징 경계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- decision(결정): `{decision_payload['decision']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## MT5 KPI(MT5 핵심 성과 지표)

{table}

## Read(판독)

- supportive_signal_evidence_not_selection(선택이 아닌 신호 근거): `{supportive}`
- fragility_flags(취약성 표시): `{fragile}`
- D/B attribution(D/B 귀속): `out_of_scope_by_claim`
- packaging_boundary(패키징 경계): `identity bridge(정체성 연결기) 결과는 exact cp322A ONNX(정확 cp322A 온엑스) 권위가 아니다`
- effect(효과): 좋은 MT5(메타트레이더5) 숫자는 연구 근거로 보존하지만, candidate selection(후보 선택), forward pass(전진 통과), runtime authority(런타임 권위)는 막는다.

## Next(다음)

`{NEXT_ACTION}`
""",
    )
    decision_doc = review.write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage333F Signal Replay MT5 Forensics Decision(333F 신호 재생 MT5 포렌식 결정)

- decision(결정): `{decision_payload['decision']}`
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): run333E MT5(메타트레이더5) 양수 결과를 overfit/packaging boundary(과적합/패키징 경계) 안에 가두고, exact handoff(정확 인계) 수리 전에는 운영 의미로 승격하지 않는다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    return [report, decision_doc]


def update_selection_status(decision_payload: Mapping[str, Any]) -> Path:
    supportive = ", ".join(str(item) for item in decision_payload["supportive_signal_evidence_not_selection"]) or "none"
    return review.write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage333 Selection Status(333단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- latest_runtime_probe(최신 런타임 탐침): `{PARENT_RUN_ID}`
- latest_forensics_review(최신 포렌식 검토): `{RUN_ID}`
- supportive_signal_evidence_not_selection(선택이 아닌 신호 근거): `{supportive}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): MT5(메타트레이더5) signal replay(신호 재생) 결과를 연구 근거로 보존하되 cp322A exact ONNX handoff(정확 온엑스 인계) 판정은 열어둔다.
""",
    )


def update_current_truth(decision_payload: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = review.read_text_lossless(WORKSPACE_STATE)
    workspace_text = review.replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage333(333단계) run333F(333F 실행) signal replay MT5 forensics(신호 재생 MT5 포렌식)를 `{decision_payload['status']}`로 닫았다. "
        "Effect(효과): run333E MT5 양수 결과를 KPI/regime/cost/curve/package boundary(핵심지표/국면/비용/곡선/패키징 경계)로 분해했지만 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage333(333단계) run333F(333F 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    review.write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = review.read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v6`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준): `none`",
        "- target_surface(": "- target_surface(목표 표면): `signal_replay_mt5_forensics_packaging_boundary`",
        "- status(": f"- status(상태): `{decision_payload['status']}`",
        "- decision(": f"- decision(판정): `{decision_payload['judgment']}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = review.replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run333F_summary(333F 요약): signal replay MT5 forensics(신호 재생 MT5 포렌식)를 `{decision_payload['status']}`로 닫았다. "
        "Effect(효과): positive MT5 evidence(양수 MT5 근거)를 보존했지만 identity bridge/package boundary(정체성 연결기/패키징 경계) 때문에 Forward Passed(전진 통과)와 Goal Achieve(목표 달성)는 없다."
    )
    if "run333F_summary(333F 요약)" not in current_text:
        current_text = current_text.replace(f"- decision(판정): `{decision_payload['judgment']}`\n", f"- decision(판정): `{decision_payload['judgment']}`\n{summary}\n", 1)
    review.write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    review.append_if_missing(
        CHANGELOG,
        "Stage333F Signal Replay MT5 Forensics And Packaging Boundary",
        f"""
## 2026-05-26 - Stage333F Signal Replay MT5 Forensics And Packaging Boundary(333F 신호 재생 MT5 포렌식 및 패키징 경계)

- run333F(333F 실행): run333E(333E 실행)의 completed MT5 report/telemetry(완료 MT5 보고서/실행기록)를 KPI(핵심 성과 지표), regime(국면), cost stress(비용 압박), curve pocket(곡선 포켓), packaging boundary(패키징 경계)로 분해했다.
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- effect(효과): 양수 신호 재생 근거는 보존하지만 selected candidate(선택 후보), Forward Passed(전진 통과), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, decision_payload: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run333F_signal_replay_mt5_forensics_and_packaging_boundary.md"
    review.upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "performance_attribution",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "path": review.rel(report_path),
                "notes": "signal_replay_mt5_forensics_packaging_boundary;no_selection;goal_achieve_not_claimed.",
            }
        ],
    )
    review.upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__signal_replay_mt5_forensics",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "signal_replay_mt5_forensics_packaging_boundary",
                "tier_scope": "raw_forward_signal_payload_replay",
                "kpi_scope": "kpi_regime_cost_curve_packaging_boundary",
                "scoreboard_lane": "performance_attribution",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "path": review.rel(report_path),
                "primary_kpi": "signal_replay_mt5_kpi_report",
                "guardrail_kpi": "identity_bridge_not_candidate_onnx;db_attribution_out_of_scope;goal_achieve_not_claimed",
                "external_verification_status": "uses_completed_run333E_mt5_report_and_runtime_telemetry",
                "notes": f"decision={decision_payload['decision']};next_action={NEXT_ACTION}.",
            }
        ],
    )
    review.upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__signal_replay_mt5_forensics",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "signal_replay_mt5_forensics(신호 재생 MT5 포렌식)",
                "tier_scope": "raw_forward_signal_payload_replay(원본 전진 신호 재생)",
                "scoreboard": "kpi_regime_cost_curve_packaging_boundary(KPI/국면/비용/곡선/패키징 경계)",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": review.rel(report_path),
                "notes": "no_candidate_selected;forward_passed_not_claimed;goal_achieve_not_claimed.",
                "decision": decision_payload["decision"],
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact_path in artifacts:
        if artifact_path.exists() and artifact_path.is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{review.rel(artifact_path)}",
                    "artifact_type": "stage333F_signal_replay_forensics_artifact",
                    "path": review.rel(artifact_path),
                    "sha256": review.sha256_file(artifact_path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "signal replay MT5 forensics and packaging-boundary artifact; no operating claim.",
                }
            )
    review.upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_outputs(generated_at_utc: str) -> list[Path]:
    configure_imported_review_helpers()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    SELECTED_DIR.mkdir(parents=True, exist_ok=True)
    attempts = load_attempts()
    execution_result = read_json(RUN333E_DIR / "execution_result.json")
    bars = review.load_bars()
    trade_rows, long_short_rows, kpi_rows = review.build_trade_rows(attempts, execution_result, bars)
    regime_rows = review.build_regime_rows(trade_rows)
    db_rows = build_db_rows(attempts)
    lot_rows = review.build_lot_rows(kpi_rows)
    cost_rows = review.build_cost_rows(trade_rows)
    curve_rows, underwater_rows = review.build_curve_rows(trade_rows)
    packaging_rows = build_packaging_boundary_rows(attempts, kpi_rows)
    decision_payload = build_decision_payload(kpi_rows, cost_rows, curve_rows)

    artifacts: list[Path] = []
    artifacts.append(
        review.write_csv(
            RUN_DIR / "signal_replay_mt5_kpi_report.csv",
            [
                "attempt_name",
                "candidate_id",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "session_days",
                "rows_evaluated",
                "signal_count",
                "order_attempt_count",
                "order_fill_count",
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "recovery_factor",
                "equity_dd_amount",
                "equity_dd_percent",
                "long_trade_count",
                "short_trade_count",
                "long_win_rate_percent",
                "short_win_rate_percent",
                "recomputed_net_profit",
                "recomputed_profit_factor",
                "recomputed_max_drawdown",
                "net_recompute_delta",
                "max_underwater_trade_count",
                "max_underwater_start",
                "max_underwater_end",
                "claim_boundary",
            ],
            kpi_rows,
        )
    )
    artifacts.append(review.write_csv(RUN_DIR / "trade_level_records.csv", list(trade_rows[0].keys()) if trade_rows else [], trade_rows))
    artifacts.append(review.write_csv(RUN_DIR / "long_short_attribution_report.csv", ["attempt_name", "artifact_slug", "direction", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], long_short_rows))
    artifacts.append(review.write_csv(RUN_DIR / "regime_attribution_report.csv", ["attempt_name", "artifact_slug", "axis", "bucket", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], regime_rows))
    artifacts.append(review.write_csv(RUN_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv", ["attempt_name", "artifact_slug", "axis", "bucket", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], regime_rows))
    artifacts.append(review.write_csv(RUN_DIR / "db_attribution_report.csv", ["attempt_name", "artifact_slug", "candidate_id", "db_source", "status", "reason", "effect"], db_rows))
    artifacts.append(review.write_csv(RUN_DIR / "lot_normalized_report.csv", ["attempt_name", "artifact_slug", "fixed_lot", "net_profit_at_fixed_lot", "equity_dd_amount_at_fixed_lot", "net_profit_per_1lot_linear", "equity_dd_amount_per_1lot_linear", "expectancy_per_1lot_linear", "normalization_boundary"], lot_rows))
    artifacts.append(review.write_csv(RUN_DIR / "cost_stress_report.csv", ["attempt_name", "artifact_slug", "extra_cost_per_round_trip_account_ccy", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "max_drawdown_after_cost", "survives_pf_gt_1", "stress_boundary"], cost_rows))
    artifacts.append(review.write_csv(RUN_DIR / "curve_pocket_report.csv", ["attempt_name", "artifact_slug", "chunk_type", "chunk_id", "start_time", "end_time", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], curve_rows))
    artifacts.append(review.write_csv(RUN_DIR / "underwater_stretch_report.csv", ["attempt_name", "artifact_slug", "total_trade_count", "max_underwater_trade_count", "max_underwater_start", "max_underwater_end", "max_drawdown"], underwater_rows))
    artifacts.append(review.write_csv(RUN_DIR / "packaging_boundary_report.csv", list(packaging_rows[0].keys()) if packaging_rows else [], packaging_rows))
    artifacts.append(review.write_json(RUN_DIR / "final_forward_decision.json", decision_payload))
    artifacts.append(review.write_json(RUN_DIR / "performance_attribution_receipt.json", {"status": "completed", "kpi_report": review.rel(artifacts[0]), "regime_report": review.rel(artifacts[3]), "cost_stress_report": review.rel(artifacts[7]), "curve_pocket_report": review.rel(artifacts[8]), "packaging_boundary_report": review.rel(artifacts[10]), "claim_boundary": CLAIM_BOUNDARY}))
    artifacts.append(review.write_csv(RUN_DIR / "result_judgment.csv", ["run_id", "status", "judgment", "decision", "forward_passed", "forward_failed", "goal_achieve", "next_action", "claim_boundary"], [{**decision_payload, "run_id": RUN_ID}]))
    artifacts.append(review.write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gate_rows()))
    artifacts.append(review.write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    artifacts.append(review.write_json(RUN_DIR / "run_manifest.json", {"stage_id": STAGE_ID, "run_id": RUN_ID, "run_number": RUN_NUMBER, "parent_run_id": PARENT_RUN_ID, "exploration_label": EXPLORATION_LABEL, "generated_at_utc": generated_at_utc, **decision_payload}))

    artifacts.extend(write_reports(kpi_rows, decision_payload))
    artifacts.append(update_selection_status(decision_payload))
    artifacts.extend(update_current_truth(decision_payload))
    update_registers(generated_at_utc, decision_payload, artifacts)
    return artifacts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage333F signal replay MT5 forensics and packaging boundary review.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "artifact_count": len(artifacts),
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
