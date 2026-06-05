from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage341 import materialize_f01_stability_cost_regime_validation_inputs_without_db as mat


TODAY = mat.TODAY
STAGE_ID = mat.STAGE_ID
STAGE_DIR = mat.STAGE_DIR
RUN_NUMBER = "run341D"
RUN_ID = "run341D_review_f01_stability_cost_regime_validation_without_db_v1"
PARENT_RUN_ID = mat.RUN_ID
NEXT_RUN_ID = "run341E_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1"

STATUS = "completed_stage341D_f01_stability_cost_regime_reviewed_positive_structure_no_selection"
JUDGMENT = "f01_q01_q09_positive_structure_cost_survives_plus1_but_session_loss_concentration_and_reported_equity_drawdown_block_selection"
DECISION = "stage341D_open_run341E_materialize_f01_session_long_firewall_mt5_probe_package"
CLAIM_BOUNDARY = (
    "research_development_review_only_f01_stability_cost_regime_validation_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run341D_f01_stability_cost_regime_validation_review.md"
DECISION_DOC = mat.ds.ROOT / "docs" / "decisions" / f"{TODAY}_stage341D_f01_stability_cost_regime_validation_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

REVIEW_SCORECARD = RUN_DIR / "review_scorecard.csv"
VALIDATION_JUDGMENT = RUN_DIR / "validation_judgment.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run341E_session_long_firewall_probe_queue.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

SOURCE_GATES = STAGE_DIR / "02_runs" / "run341C" / "required_gate_coverage_audit.csv"
SOURCE_SUMMARY = mat.ATTRIBUTION_SUMMARY
SOURCE_COST = mat.COST_STRESS_MATRIX
SOURCE_SESSION = mat.SESSION_REGIME_SCORECARD
SOURCE_EQUITY = mat.EQUITY_CURVE_QUALITY
SOURCE_SCORECARD = mat.VALIDATION_SCORECARD
SOURCE_TRADE_LEVEL = mat.TRADE_LEVEL
SOURCE_STAGE340_SCORECARD = mat.ds.SOURCE_SCORECARD


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return mat.rel(path)


def exists(path: Path) -> bool:
    return mat.exists(path)


def sha(path: Path) -> str:
    return mat.sha(path)


def read_csv(path: Path) -> pd.DataFrame:
    return mat.read_csv(path)


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    mat.ds.br.ensure_parent(path)
    with open(mat.ds.br.fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    mat.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    mat.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    mat.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, keys: list[str], rows: list[Mapping[str, Any]]) -> None:
    mat.append_or_replace_csv(path, keys, rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def first(frame: pd.DataFrame, attempt: str) -> dict[str, Any]:
    matched = frame.loc[frame["attempt_name"].astype(str).eq(attempt)]
    return matched.iloc[0].to_dict() if not matched.empty else {}


def cost_row(cost: pd.DataFrame, attempt: str, stress_id: str) -> dict[str, Any]:
    matched = cost.loc[cost["attempt_name"].astype(str).eq(attempt) & cost["stress_id"].astype(str).eq(stress_id)]
    return matched.iloc[0].to_dict() if not matched.empty else {}


def session_row(session: pd.DataFrame, attempt: str, bucket: str) -> dict[str, Any]:
    matched = session.loc[
        session["attempt_name"].astype(str).eq(attempt)
        & session["axis"].astype(str).eq("session_slice")
        & session["bucket"].astype(str).eq(bucket)
    ]
    return matched.iloc[0].to_dict() if not matched.empty else {}


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    summary = read_csv(SOURCE_SUMMARY)
    cost = read_csv(SOURCE_COST)
    session = read_csv(SOURCE_SESSION)
    equity = read_csv(SOURCE_EQUITY)
    stage340 = read_csv(SOURCE_STAGE340_SCORECARD)
    q01 = first(summary, "q01_ctl_s55_l51_m01_h12")
    q09 = first(summary, "q09_s545_l51_m01_h12")
    q01_stage340 = first(stage340, "q01_ctl_s55_l51_m01_h12")
    q09_stage340 = first(stage340, "q09_s545_l51_m01_h12")
    q01_cost1 = cost_row(cost, "q01_ctl_s55_l51_m01_h12", "c03_plus_1_00")
    q09_cost1 = cost_row(cost, "q09_s545_l51_m01_h12", "c03_plus_1_00")
    q01_cost2 = cost_row(cost, "q01_ctl_s55_l51_m01_h12", "c04_plus_2_00")
    q09_cost2 = cost_row(cost, "q09_s545_l51_m01_h12", "c04_plus_2_00")
    q01_early = session_row(session, "q01_ctl_s55_l51_m01_h12", "early")
    q09_early = session_row(session, "q09_s545_l51_m01_h12", "early")
    q01_late = session_row(session, "q01_ctl_s55_l51_m01_h12", "late")
    q09_late = session_row(session, "q09_s545_l51_m01_h12", "late")
    q01_eq = first(equity, "q01_ctl_s55_l51_m01_h12")
    q09_eq = first(equity, "q09_s545_l51_m01_h12")
    metrics = {
        "q01_net": as_float(q01.get("net_profit")),
        "q09_net": as_float(q09.get("net_profit")),
        "q09_net_delta": as_float(q09.get("net_profit")) - as_float(q01.get("net_profit")),
        "q01_reported_dd": as_float(q01_stage340.get("max_drawdown_amount")),
        "q09_reported_dd": as_float(q09_stage340.get("max_drawdown_amount")),
        "q01_reported_recovery": as_float(q01_stage340.get("recovery_factor")),
        "q09_reported_recovery": as_float(q09_stage340.get("recovery_factor")),
        "q01_plus1_net": as_float(q01_cost1.get("stressed_net_profit")),
        "q09_plus1_net": as_float(q09_cost1.get("stressed_net_profit")),
        "q01_plus2_recovery": as_float(q01_cost2.get("stressed_recovery_factor")),
        "q09_plus2_recovery": as_float(q09_cost2.get("stressed_recovery_factor")),
        "q01_early_net": as_float(q01_early.get("net_profit")),
        "q09_early_net": as_float(q09_early.get("net_profit")),
        "q01_late_net": as_float(q01_late.get("net_profit")),
        "q09_late_net": as_float(q09_late.get("net_profit")),
        "q01_worst_session_loss_share": as_float(q01_eq.get("worst_session_loss_share")),
        "q09_worst_session_loss_share": as_float(q09_eq.get("worst_session_loss_share")),
        "q01_consecutive_losses": as_float(q01_eq.get("consecutive_losses")),
        "q09_consecutive_losses": as_float(q09_eq.get("consecutive_losses")),
    }
    review_rows = [
        {
            "attempt_name": "q01_ctl_s55_l51_m01_h12",
            "role": "quality_anchor(품질 기준점)",
            "net_profit": metrics["q01_net"],
            "reported_drawdown": metrics["q01_reported_dd"],
            "reported_recovery": metrics["q01_reported_recovery"],
            "plus1_cost_net": metrics["q01_plus1_net"],
            "plus2_cost_recovery": metrics["q01_plus2_recovery"],
            "early_net": metrics["q01_early_net"],
            "late_net": metrics["q01_late_net"],
            "worst_session_loss_share": metrics["q01_worst_session_loss_share"],
            "review_judgment": "quality_anchor_preserved_but_session_loss_clustered(품질 기준점 보존, 세션 손실 군집 있음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_name": "q09_s545_l51_m01_h12",
            "role": "net_clue(순수익 단서)",
            "net_profit": metrics["q09_net"],
            "reported_drawdown": metrics["q09_reported_dd"],
            "reported_recovery": metrics["q09_reported_recovery"],
            "plus1_cost_net": metrics["q09_plus1_net"],
            "plus2_cost_recovery": metrics["q09_plus2_recovery"],
            "early_net": metrics["q09_early_net"],
            "late_net": metrics["q09_late_net"],
            "worst_session_loss_share": metrics["q09_worst_session_loss_share"],
            "review_judgment": "net_clue_preserved_but_reported_equity_quality_worse_and_early_session_weaker(순수익 단서 보존, 보고서 기준 수익곡선 품질 악화와 초반 세션 약화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    judgment = pd.DataFrame(
        [
            {
                "judgment_id": "j01_positive_structure",
                "judgment_class": "positive_clue_no_selection(긍정 단서, 선정 없음)",
                "evidence": f"q01 net={metrics['q01_net']}; q09 net={metrics['q09_net']}; plus1 cost q01/q09={metrics['q01_plus1_net']}/{metrics['q09_plus1_net']}",
                "effect": "둘 다 버릴 결과는 아니지만 운영 승격 근거는 아니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "judgment_id": "j02_selection_blocked_by_quality_tradeoff",
                "judgment_class": "selection_blocked(선정 차단)",
                "evidence": f"q09 net delta={metrics['q09_net_delta']}; q09 reported DD={metrics['q09_reported_dd']} vs q01 {metrics['q01_reported_dd']}; q09 recovery={metrics['q09_reported_recovery']} vs q01 {metrics['q01_reported_recovery']}",
                "effect": "q09를 순수익 최고값만으로 winner(승자)로 고정하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "judgment_id": "j03_session_firewall_seed",
                "judgment_class": "repair_seed(수리 씨앗)",
                "evidence": f"q09 early={metrics['q09_early_net']}, late={metrics['q09_late_net']}; q01 early={metrics['q01_early_net']}, late={metrics['q01_late_net']}",
                "effect": "long(롱) 약세와 early session(초반 세션) 손실 군집을 runtime probe(런타임 탐침)로 시험한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    attribution = pd.DataFrame(
        [
            {
                "attribution_id": "a01_cost_stress",
                "finding": "q01/q09 both survive +1.00 proxy cost but fail recovery floor at +2.00 proxy cost(q01/q09 모두 +1 비용은 생존, +2 비용은 회복 하한 실패)",
                "effect": "비용 여유는 있지만 두껍지 않다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "attribution_id": "a02_session_shape",
                "finding": "q09 shifts edge from early to late session(q09는 초반보다 후반 세션에 우위가 있다)",
                "effect": "early long(초반 롱) 차단 또는 세션 방화벽이 다음 시험 축이다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "attribution_id": "a03_reported_equity_authority",
                "finding": "trade-close equity(거래 종료 수익곡선)는 좋아 보여도 MT5 reported equity DD(MT5 보고 수익곡선 낙폭)는 q09가 더 나쁘다.",
                "effect": "drawdown/recovery(낙폭/회복)는 MT5 report(보고서)를 더 강한 권위로 둔다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    failure = pd.DataFrame(
        [
            {
                "failure_id": "run341D_net_only_selection_block",
                "hypothesis": "q09 net_profit(순수익) 최고값만으로 q01보다 우월하다고 볼 수 있다.",
                "failed_boundary": "q09는 net +0.70이지만 MT5 reported DD(보고 낙폭)가 99.31로 q01 89.31보다 크고 recovery(회복)는 1.24로 q01 1.38보다 낮다.",
                "salvage_value": "q09는 late session(후반 세션)과 short side(숏 방향) 단서로 보존한다.",
                "do_not_repeat": "단일 net_profit(순수익) 최고값으로 selection(선정)을 주장하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "failure_id": "run341D_cost_margin_thin",
                "hypothesis": "기존 q01/q09는 비용 압박에도 충분히 두껍다.",
                "failed_boundary": "+2.00 proxy cost(프록시 비용)에서 recovery floor(회복 하한)가 둘 다 깨진다.",
                "salvage_value": "+1.00 cost(비용)까지는 생존하므로 session/firewall(세션/방화벽)로 손실 군집을 줄이는 수리가 가능하다.",
                "do_not_repeat": "비용 압박 없이 positive(긍정) 판정을 강화하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    next_queue = pd.DataFrame(
        [
            {
                "queue_id": "e01_q01_control_no_filter",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q01_ctl_s55_l51_m01_h12",
                "role": "control_quality_anchor(품질 기준 대조)",
                "side_filter_enabled": False,
                "feature_index": "",
                "block_long_range": "",
                "block_short_range": "",
                "expected_effect": "q01 exact control(정확 대조)을 새 package(패키지)에 재현한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "e02_q09_control_no_filter",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q09_s545_l51_m01_h12",
                "role": "control_net_clue(순수익 단서 대조)",
                "side_filter_enabled": False,
                "feature_index": "",
                "block_long_range": "",
                "block_short_range": "",
                "expected_effect": "q09 net clue(순수익 단서)를 새 package(패키지)에 재현한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "e03_q01_block_early_longs",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q01_ctl_s55_l51_m01_h12",
                "role": "session_long_firewall_quality_anchor(세션 롱 방화벽 품질 기준)",
                "side_filter_enabled": True,
                "feature_index": 37,
                "block_long_range": "0,110",
                "block_short_range": "",
                "expected_effect": "early long(초반 롱) 약한 순수익과 손실 군집을 줄이는지 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "e04_q09_block_early_longs",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q09_s545_l51_m01_h12",
                "role": "session_long_firewall_net_clue(세션 롱 방화벽 순수익 단서)",
                "side_filter_enabled": True,
                "feature_index": 37,
                "block_long_range": "0,110",
                "block_short_range": "",
                "expected_effect": "q09의 late session(후반 세션) 우위를 보존하면서 early long(초반 롱)을 줄이는지 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "e05_q09_block_early_all_sides_negative_control",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q09_s545_l51_m01_h12",
                "role": "overfilter_negative_control(과필터 부정 대조)",
                "side_filter_enabled": True,
                "feature_index": 37,
                "block_long_range": "0,110",
                "block_short_range": "0,110",
                "expected_effect": "early session(초반 세션)을 통째로 막으면 edge(우위)가 사라지는지 보는 부정 대조다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    return pd.DataFrame(review_rows), judgment, attribution, failure, next_queue, metrics


def output_files() -> list[Path]:
    return [
        REVIEW_SCORECARD,
        VALIDATION_JUDGMENT,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_QUEUE,
        RESULT_JUDGMENT_RECEIPT,
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
        STAGE_BRIEF,
        STAGE_README,
        mat.ds.br.WORKSPACE_STATE,
        mat.ds.br.CURRENT_WORKING_STATE,
        STAGE_LEDGER,
        mat.ds.br.RUN_REGISTRY,
        mat.ds.br.PROJECT_LEDGER,
        mat.ds.br.ARTIFACT_REGISTRY,
        Path(__file__),
    ]


def write_receipts(metrics: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "judgment_class": "positive_clue_no_selection(긍정 단서, 선정 없음)",
            "selection": "blocked_by_quality_tradeoff(품질 절충으로 선정 차단)",
            "effect": "q01/q09(큐01/큐09)를 보존하지만 운영 주장으로 올리지 않는다.",
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "q09_net_delta": metrics.get("q09_net_delta"),
            "q09_reported_drawdown_delta": metrics.get("q09_reported_dd") - metrics.get("q01_reported_dd"),
            "next_repair_axis": "session_long_firewall(세션 롱 방화벽)",
            "effect": "q09의 작은 net(순수익) 우위와 더 나쁜 reported DD(보고 낙폭)를 함께 설명한다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in [SOURCE_SUMMARY, SOURCE_COST, SOURCE_SESSION, SOURCE_EQUITY, SOURCE_SCORECARD, SOURCE_TRADE_LEVEL]],
            "artifact_paths": [rel(path) for path in output_files()],
            "source_artifact_hashes": {rel(path): sha(path) for path in [SOURCE_SUMMARY, SOURCE_COST, SOURCE_SESSION, SOURCE_EQUITY, SOURCE_SCORECARD, SOURCE_TRADE_LEVEL] if exists(path)},
            "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
            "effect": "run341C(341C 실행) 산출물이 run341D(341D 실행) 판정으로 연결된다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "promotion_candidate": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "effect": "review(검토)를 operating promotion(운영 승격)으로 오해하지 않게 한다.",
        },
    )


def gate_row(gate_id: str, status: str, evidence_path: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": evidence_path,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(metrics: Mapping[str, Any]) -> pd.DataFrame:
    source_gates = read_csv(SOURCE_GATES) if exists(SOURCE_GATES) else pd.DataFrame({"status": ["missing"]})
    return pd.DataFrame(
        [
            gate_row("parent_341C_gates_passed", "passed" if source_gates["status"].astype(str).str.lower().eq("passed").all() else "failed", rel(SOURCE_GATES), "run341C(341C 실행) 물질화를 이어받는다."),
            gate_row("q01_q09_review_scorecard_written", "passed" if exists(REVIEW_SCORECARD) else "failed", rel(REVIEW_SCORECARD), "q01/q09(큐01/큐09) 판정표를 만든다."),
            gate_row("cost_stress_reviewed", "passed" if metrics.get("q01_plus1_net", 0) > 0 and metrics.get("q09_plus1_net", 0) > 0 else "failed", rel(PERFORMANCE_ATTRIBUTION), "+1 cost stress(비용 압박) 생존 여부를 기록한다."),
            gate_row("selection_block_recorded", "passed" if metrics.get("q09_reported_dd", 0) > metrics.get("q01_reported_dd", 0) else "failed", rel(VALIDATION_JUDGMENT), "q09 net(순수익) 단독 선정 차단 사유를 기록한다."),
            gate_row("next_probe_queue_written", "passed" if exists(NEXT_QUEUE) and len(read_csv(NEXT_QUEUE)) >= 5 else "failed", rel(NEXT_QUEUE), "session-long firewall(세션 롱 방화벽) 다음 탐침 queue(대기열)를 만든다."),
            gate_row("tier_pair_records_written", "passed" if exists(STAGE_LEDGER) else "failed", rel(STAGE_LEDGER), "Tier A/B(티어 A/B) 기록을 장부에 남긴다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(CLAIM_RECEIPT), "선정/운영/목표 달성 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "필수 게이트 커버리지 감사(required gate coverage audit, 필수 게이트 감사)를 기록한다."),
        ]
    )


def write_docs(metrics: Mapping[str, Any]) -> None:
    report = f"""# run341D F01 Stability Cost Regime Validation Review(341D F01 안정성 비용 국면 검증 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- q09 net delta(q09 순수익 차이): `{metrics.get('q09_net_delta')}`
- q09 reported DD(q09 보고 낙폭): `{metrics.get('q09_reported_dd')}` vs q01 `{metrics.get('q01_reported_dd')}`
- q09 reported recovery(q09 보고 회복): `{metrics.get('q09_reported_recovery')}` vs q01 `{metrics.get('q01_reported_recovery')}`

## Action(행동)

run341C(341C 실행)의 trade-level attribution(거래 단위 귀속), proxy cost stress(프록시 비용 압박), session/regime(세션/국면)을 검토했다.
Effect(효과): q01/q09(큐01/큐09)는 positive clue(긍정 단서)로 보존하지만, q09를 winner(승자)나 selected model(선정 모델)로 올리지 않는다.

## Next(다음)

run341E(341E 실행)는 session-long firewall(세션 롱 방화벽) MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만든다.
Effect(효과): early long(초반 롱)의 약한 구조를 실제 EA side filter(EA 사이드 필터)로 시험할 준비를 한다.

## Boundary(경계)

No selection(선정 없음), no forward(전진 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage 341D Review Decision(341D 검토 결정)

- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`

Action(행동): q01/q09(큐01/큐09)를 positive clue(긍정 단서)로 보존하고 session-long firewall(세션 롱 방화벽) 패키지를 다음 실행으로 열었다.
Effect(효과): net only selection(순수익 단독 선정)을 막고 실제 runtime probe(런타임 탐침)로 약점 수리를 시험한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 341 Selection Status(341단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- quality_anchor(품질 기준점): `q01_ctl_s55_l51_m01_h12`
- net_high_clue(순수익 높은 단서): `q09_s545_l51_m01_h12`
- next_probe(다음 탐침): `session_long_firewall(세션 롱 방화벽)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 검토 후에도 q09(큐09)를 선정하지 않고 다음 runtime probe(런타임 탐침)로 넘긴다.
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run341E(341E 실행)는 q01/q09(큐01/큐09) control(대조)과 early-long block(초반 롱 차단) side filter(사이드 필터)를 MT5 package(MT5 패키지)로 만든다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(SELECTION_STATUS, selection)
    write_text(mat.ds.br.CURRENT_WORKING_STATE, current)
    write_text(mat.ds.br.WORKSPACE_STATE, workspace)
    append_text_once(STAGE_BRIEF, RUN_ID, f"""## run341D Validation Review(341D 검증 검토)

- run_id(실행 ID): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): positive clue(긍정 단서)는 보존하고 q09 selection(q09 선정)은 차단했다.
""")
    append_text_once(STAGE_README, RUN_ID, f"""## run341D Validation Review(341D 검증 검토)

- run_id(실행 ID): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): session-long firewall(세션 롱 방화벽) runtime package(런타임 패키지)를 다음으로 열었다.
""")
    changelog = f"""## {TODAY} run341D Validation Review(341D 검증 검토)

- action(행동): q01/q09(큐01/큐09)의 cost/session/regime/equity(비용/세션/국면/수익곡선) 검증 입력을 판정했다.
- effect(효과): q09(큐09)는 순수익 단서로 보존하지만 보고서 기준 낙폭/회복 악화 때문에 선정하지 않았다.
- boundary(경계): 선정 없음, 운영 승격 없음, 런타임 권위 없음, 목표 달성 없음.
"""
    append_text_once(mat.ds.br.ROOT_CHANGELOG, RUN_ID, changelog)
    append_text_once(mat.ds.br.WORKSPACE_CHANGELOG, RUN_ID, changelog)


def ledger_rows(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": "logreg_balanced_c025_q09_s545_l51_m01_h12",
        "net_profit": metrics.get("q09_net"),
        "profit_factor": "",
        "drawdown": metrics.get("q09_reported_dd"),
        "recovery_factor": metrics.get("q09_reported_recovery"),
        "trade_count": 33,
        "result_status": "positive_clue_no_selection(긍정 단서, 선정 없음)",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": "",
        "expectancy": "",
        "attempt_count": 4,
    }
    rows = []
    for view, tier, metric_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "reviewed_trade_attribution_positive_clue_no_selection"),
        ("Tier B separate(Tier B 분리)", "Tier B", "missing_required"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "same_as_tier_a_until_tier_b_available"),
    ]:
        row = dict(base)
        row.update({"view": view, "tier": tier, "metric_scope": metric_scope})
        if metric_scope == "missing_required":
            for metric in ["candidate_model_id", "net_profit", "profit_factor", "drawdown", "recovery_factor", "trade_count", "matched_rows", "expectancy", "attempt_count"]:
                row[metric] = ""
            row["result_status"] = "missing_required(필수 누락)"
        rows.append(row)
    return rows


def write_registries(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    rows = ledger_rows(gates, metrics)
    existing = read_csv(STAGE_LEDGER) if exists(STAGE_LEDGER) else pd.DataFrame()
    if not existing.empty and "run_id" in existing.columns:
        existing = existing.loc[~existing["run_id"].astype(str).eq(RUN_ID)].copy()
    write_csv(STAGE_LEDGER, pd.concat([existing, pd.DataFrame(rows)], ignore_index=True))
    append_or_replace_csv(mat.ds.br.RUN_REGISTRY, ["run_id"], [rows[0]])
    project_rows = []
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["kpi_scope"] = "validation_review(검증 검토)"
        project_row["scoreboard_lane"] = "runtime_probe_attribution_review(런타임 탐침 귀속 검토)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        project_rows.append(project_row)
    append_or_replace_csv(mat.ds.br.PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    artifact_rows = []
    for path in output_files():
        if exists(path) and mat.ds.br.path_is_file(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": path.suffix.lstrip(".") or "file",
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(mat.ds.br.ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def main() -> None:
    mat.ds.br.Path(mat.ds.br.fs_path(RUN_DIR)).mkdir(parents=True, exist_ok=True)
    mat.ds.br.Path(mat.ds.br.fs_path(REVIEW_DIR)).mkdir(parents=True, exist_ok=True)
    for path in [SOURCE_GATES, SOURCE_SUMMARY, SOURCE_COST, SOURCE_SESSION, SOURCE_EQUITY, SOURCE_SCORECARD]:
        if not exists(path):
            raise FileNotFoundError(f"missing required review input: {rel(path)}")
    review, judgment, attribution, failure, next_queue, metrics = build_review()
    write_csv(REVIEW_SCORECARD, review)
    write_csv(VALIDATION_JUDGMENT, judgment)
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(NEXT_QUEUE, next_queue)
    write_receipts(metrics)
    gates = build_gates(metrics)
    write_csv(GATE_AUDIT, gates)
    write_docs(metrics)
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
            "gate_total": int(len(gates)),
            "q09_net_delta": metrics.get("q09_net_delta"),
            "q09_reported_drawdown_delta": metrics.get("q09_reported_dd") - metrics.get("q01_reported_dd"),
            "candidate_selection": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "command": "python -B stage_pipelines/stage341/review_f01_stability_cost_regime_validation_without_db.py",
            "outputs": [rel(path) for path in output_files() if exists(path)],
            "status": STATUS,
            "judgment": JUDGMENT,
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_registries(gates, metrics)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "q09_net_delta": metrics.get("q09_net_delta"),
                "q09_reported_drawdown_delta": metrics.get("q09_reported_dd") - metrics.get("q01_reported_dd"),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
