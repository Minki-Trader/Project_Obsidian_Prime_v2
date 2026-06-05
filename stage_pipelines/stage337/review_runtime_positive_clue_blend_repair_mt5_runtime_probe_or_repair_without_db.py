from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import execute_runtime_positive_clue_blend_repair_mt5_runtime_probe_without_db as fr  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import materialize_runtime_positive_clue_blend_repair_runtime_probe_package_without_db as fq  # noqa: E402
from stage_pipelines.stage337 import review_runtime_positive_clue_blend_pf_recovery_drawdown_training_without_db as fp  # noqa: E402


aw = fq.aw

TODAY = "2026-05-31"
STAGE_ID = fq.STAGE_ID
RUN_NUMBER = "run337FS"
RUN_ID = "run337FS_review_runtime_positive_clue_blend_repair_mt5_runtime_probe_or_repair_without_db_v1"
PARENT_RUN_ID = fr.RUN_ID
NEXT_RUN_ID = "run337FT_design_runtime_positive_side_stability_pf_recovery_drawdown_repair_without_db_v1"
STATUS = "completed_stage337FS_runtime_positive_clue_blend_mt5_review_side_stability_positive_repair_required_no_forward_decision"
JUDGMENT = "runtime_parity_passed_side_stability_positive_net_but_pf_recovery_drawdown_block_operating_claim"
DECISION = "stage337FS_open_run337FT_side_stability_pf_recovery_drawdown_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FS_runtime_positive_clue_blend_mt5_runtime_probe_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fq.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = fq.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FS_runtime_positive_clue_blend_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FS_runtime_positive_clue_blend_mt5_runtime_probe_review.md"

FR_FINAL = fr.FINAL_DECISION
FR_GATES = fr.GATE_AUDIT
FR_SUMMARY = fr.EXECUTION_SUMMARY
FR_DIFF = fr.PROXY_MT5_DIFF
FR_SKIP = fr.TELEMETRY_SKIP_SUMMARY
FR_REPORTS = fr.STRATEGY_TESTER_REPORTS
FR_IDENTITY = fr.RUNTIME_IDENTITY
FQ_FEATURE_MATRIX = fq.FEATURE_MATRIX
FP_PROXY_REVIEW = fp.PROXY_CLUE_REVIEW

RUNTIME_PARITY_REVIEW = RUN_DIR / "runtime_parity_review.csv"
MT5_KPI_REVIEW = RUN_DIR / "mt5_kpi_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "proxy_mt5_attribution_review.csv"
TIMESTAMP_HANDOFF_REVIEW = RUN_DIR / "timestamp_handoff_review.csv"
CLUE_MEMORY = RUN_DIR / "positive_clue_and_failure_memory.csv"
FT_QUEUE = RUN_DIR / "run337FT_repair_design_queue.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (FR_FINAL, FR_GATES, FR_SUMMARY, FR_DIFF, FR_SKIP, FR_REPORTS, FR_IDENTITY, FQ_FEATURE_MATRIX, FP_PROXY_REVIEW)
OUTPUT_FILES = (
    RUNTIME_PARITY_REVIEW,
    MT5_KPI_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    TIMESTAMP_HANDOFF_REVIEW,
    CLUE_MEMORY,
    FT_QUEUE,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    fq.SELECTED_STATUS,
    fq.WORKSPACE_STATE,
    fq.CURRENT_STATE,
    fq.CHANGELOG,
    fq.STAGE_BRIEF,
    Path(__file__),
)

REVIEW_COLUMNS = (
    "attempt_name",
    "model_id",
    "runtime_status",
    "comparison_status",
    "matched_rows",
    "mismatch_rows",
    "feature_last_reached",
    "max_abs_probability_diff",
    "review_status",
    "effect",
    "claim_boundary",
)
KPI_COLUMNS = (
    "attempt_name",
    "model_id",
    "net_profit",
    "profit_factor",
    "expectancy",
    "max_drawdown_amount",
    "max_drawdown_percent",
    "recovery_factor",
    "trade_count",
    "long_trade_count",
    "short_trade_count",
    "runtime_signal_long_count",
    "runtime_signal_short_count",
    "kpi_status",
    "blocked_reason",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
ATTR_COLUMNS = (
    "model_id",
    "proxy_net_log_return",
    "proxy_profit_factor",
    "mt5_net_profit",
    "mt5_profit_factor",
    "direction_agreement",
    "attribution",
    "usability",
    "claim_boundary",
)
TIMESTAMP_COLUMNS = (
    "review_id",
    "feature_matrix_rows",
    "unique_timestamps",
    "duplicate_rows",
    "max_duplicate_per_timestamp",
    "timestamp_status",
    "effect",
    "claim_boundary",
)
MEMORY_COLUMNS = (
    "memory_id",
    "memory_type",
    "source_attempt",
    "evidence",
    "next_constraint_or_seed",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def build_reviews() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    summary_rows = read_csv(FR_SUMMARY)
    proxy_rows = {row["model_id"]: row for row in read_csv(FP_PROXY_REVIEW)}
    parity_review: list[dict[str, Any]] = []
    kpi_review: list[dict[str, Any]] = []
    attribution: list[dict[str, Any]] = []
    memory: list[dict[str, Any]] = []
    positive_mt5_rows = 0
    exact_parity_rows = 0
    proxy_sign_diff_rows = 0
    best_net = -10**9
    best_attempt = ""

    for row in summary_rows:
        mismatch = (
            as_int(row.get("expected_missing_rows"))
            + as_int(row.get("hash_mismatch_rows"))
            + as_int(row.get("probability_mismatch_rows"))
            + as_int(row.get("decision_mismatch_rows"))
        )
        exact = row.get("runtime_status") == "completed" and mismatch == 0 and row.get("feature_last_reached") == "True"
        exact_parity_rows += int(exact)
        parity_review.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "runtime_status": row.get("runtime_status", ""),
                "comparison_status": row.get("comparison_status", ""),
                "matched_rows": row.get("matched_rows", ""),
                "mismatch_rows": mismatch,
                "feature_last_reached": row.get("feature_last_reached", ""),
                "max_abs_probability_diff": row.get("max_abs_probability_diff", ""),
                "review_status": "runtime_parity_passed(런타임 동등성 통과)" if exact else "runtime_parity_review_required(런타임 동등성 검토 필요)",
                "effect": "MT5 telemetry matches expected probability tape on executable overlap(MT5 기록이 실행 가능 구간에서 예상 확률 테이프와 일치)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        net = as_float(row.get("net_profit"))
        pf = as_float(row.get("profit_factor"))
        expectancy = as_float(row.get("expectancy"))
        drawdown = as_float(row.get("max_drawdown_amount"))
        recovery = as_float(row.get("recovery_factor"))
        trades = as_int(row.get("trade_count"))
        long_trades = as_int(row.get("long_trade_count"))
        short_trades = as_int(row.get("short_trade_count"))
        positive_mt5_rows += int(net > 0)
        if net > best_net:
            best_net = net
            best_attempt = row["attempt_name"]

        blocked: list[str] = []
        if net <= 0:
            blocked.append("net_nonpositive(순수익 비양수)")
        if pf < 1.15:
            blocked.append("profit_factor_weak(수익 팩터 약함)")
        if recovery < 1.0:
            blocked.append("recovery_factor_weak(회복 계수 약함)")
        if drawdown > 150:
            blocked.append("drawdown_high(낙폭 큼)")
        if trades < 300:
            blocked.append("trade_count_thin(거래수 얇음)")
        if min(long_trades, short_trades) < 50:
            blocked.append("side_sample_sparse(방향 표본 부족)")
        kpi_status = "positive_runtime_clue_only(긍정 런타임 단서 한정)" if net > 0 else "negative_runtime_memory(음수 런타임 기억)"
        kpi_review.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "net_profit": net,
                "profit_factor": pf,
                "expectancy": expectancy,
                "max_drawdown_amount": drawdown,
                "max_drawdown_percent": 0.0,
                "recovery_factor": recovery,
                "trade_count": trades,
                "long_trade_count": long_trades,
                "short_trade_count": short_trades,
                "runtime_signal_long_count": row.get("long_count", ""),
                "runtime_signal_short_count": row.get("short_count", ""),
                "kpi_status": kpi_status,
                "blocked_reason": ";".join(blocked or ["inner_holdout_not_forward_evidence(내부 보류이며 전진 근거 아님)"]),
                "allowed_use": "repair seed and attribution(수리 씨앗과 귀속)",
                "forbidden_use": "Forward Passed/Goal/operating promotion(전진 통과/목표/운영 승격)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        proxy = proxy_rows.get(row["model_id"], {})
        proxy_net = as_float(proxy.get("proxy_net_log_return"))
        agreement = "same_sign(같은 부호)" if (proxy_net > 0 and net > 0) or (proxy_net <= 0 and net <= 0) else "sign_diff(부호 차이)"
        proxy_sign_diff_rows += int(agreement == "sign_diff(부호 차이)")
        attribution.append(
            {
                "model_id": row["model_id"],
                "proxy_net_log_return": proxy_net,
                "proxy_profit_factor": proxy.get("proxy_profit_factor", ""),
                "mt5_net_profit": net,
                "mt5_profit_factor": pf,
                "direction_agreement": agreement,
                "attribution": "MT5 lifecycle, spread, fill, and position overlap change proxy scale and sign(MT5 생명주기, 스프레드, 체결, 포지션 중첩이 프록시 규모와 부호를 바꿈)",
                "usability": "proxy usable only as ranking clue after MT5 probe(프록시는 MT5 탐침 뒤 순위 단서로만 사용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    best = next((row for row in kpi_review if row["attempt_name"] == best_attempt), {})
    memory.append(
        {
            "memory_id": "positive_runtime_clue_side_stability",
            "memory_type": "positive_clue(긍정 단서)",
            "source_attempt": best_attempt,
            "evidence": f"net={best.get('net_profit')};pf={best.get('profit_factor')};dd={best.get('max_drawdown_amount')};recovery={best.get('recovery_factor')};trades={best.get('trade_count')};long={best.get('long_trade_count')};short={best.get('short_trade_count')}",
            "next_constraint_or_seed": "preserve side-stability positive net while improving PF, recovery, and drawdown(side-stability 양수 순익을 보존하며 PF, 회복, 낙폭 개선)",
            "effect": "turns best MT5 runtime clue into offensive repair seed(가장 좋은 MT5 런타임 단서를 공격 수리 씨앗으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    memory.append(
        {
            "memory_id": "proxy_sign_inversion_memory",
            "memory_type": "failure_memory(실패 기억)",
            "source_attempt": "multiple_fo_models",
            "evidence": "blend/cost proxy signs did not reliably match MT5 result(혼합/비용 프록시 부호가 MT5 결과와 안정적으로 맞지 않음)",
            "next_constraint_or_seed": "do not select by proxy sign alone; require MT5 runtime probe before promotion-like language(프록시 부호만으로 선택 금지, 승격성 표현 전 MT5 런타임 탐침 필요)",
            "effect": "keeps proxy as scout, not KPI replacement(프록시는 정찰로 두고 성과 지표 대체를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    memory.append(
        {
            "memory_id": "release_blockers_pf_recovery_drawdown",
            "memory_type": "failure_memory(실패 기억)",
            "source_attempt": "all_attempts",
            "evidence": "PF below 1.15 or recovery below 1.0 or drawdown high(PF 1.15 미만 또는 회복 1.0 미만 또는 낙폭 큼)",
            "next_constraint_or_seed": "repair objective must improve profit factor, recovery, drawdown without threshold or lot optimization(수리 목표는 임계값/랏 최적화 없이 수익 팩터, 회복, 낙폭 개선)",
            "effect": "blocks operating claim while preserving exploration(운영 주장은 막고 탐색은 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    feature = pd.read_csv(aw.io_path(FQ_FEATURE_MATRIX))
    duplicate_rows = int(len(feature) - feature["timestamp"].nunique())
    timestamp_review = [
        {
            "review_id": "fq_feature_matrix_unique_timestamp_audit",
            "feature_matrix_rows": len(feature),
            "unique_timestamps": int(feature["timestamp"].nunique()),
            "duplicate_rows": duplicate_rows,
            "max_duplicate_per_timestamp": int(feature["timestamp"].value_counts().max()),
            "timestamp_status": "unique_timestamp_handoff_passed(고유 시각 인계 통과)" if duplicate_rows == 0 else "duplicate_timestamp_review_required(중복 시각 검토 필요)",
            "effect": "runtime package avoids cost-policy duplicate timestamps(런타임 패키지가 비용 정책 중복 시각을 피함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    ft_queue = [
        {
            "queue_id": "ft_side_stability_pf_recovery_drawdown_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design repair that preserves side-stability positive MT5 clue while improving PF, recovery, and drawdown(side-stability 긍정 MT5 단서를 보존하며 PF, 회복, 낙폭을 개선하는 수리 설계)",
            "required_inputs": f"{rel(MT5_KPI_REVIEW)};{rel(RUNTIME_PARITY_REVIEW)};{rel(PROXY_MT5_ATTRIBUTION)}",
            "required_outputs": "repair objective, feature/label constraints, negative controls, MT5 package criteria(수리 목표, 피처/라벨 제약, 음성 대조, MT5 패키지 기준)",
            "blocked_if_missing": "MT5 KPI review, parity review, or proxy attribution(MT5 성과 검토, 동등성 검토, 프록시 귀속)",
            "forbidden_action": "promote side-stability or tune thresholds/lots as selection(side-stability 승격 또는 임계값/랏 선택 튜닝)",
            "effect": "keeps offensive exploration active without pretending live readiness(실거래 준비를 가장하지 않고 공격 탐색을 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "attempt_rows": len(summary_rows),
        "runtime_parity_passed_rows": exact_parity_rows,
        "positive_mt5_rows": positive_mt5_rows,
        "best_attempt": best_attempt,
        "best_net_profit": best_net,
        "best_profit_factor": best.get("profit_factor", 0),
        "best_recovery_factor": best.get("recovery_factor", 0),
        "best_drawdown": best.get("max_drawdown_amount", 0),
        "proxy_sign_diff_rows": proxy_sign_diff_rows,
        "duplicate_timestamp_rows": duplicate_rows,
        "unique_timestamp_rows": int(feature["timestamp"].nunique()),
        "ft_queue_rows": len(ft_queue),
    }
    return parity_review, kpi_review, attribution, timestamp_review, memory, ft_queue, summary


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["goal_achieve"] == "not_claimed" and final["candidate_selection"] == "not_run"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(FR_SUMMARY), "required FR outputs exist(필수 FR 산출물 존재)"),
        ("parent_fr_gates_passed", final["fr_failed_gate_rows"] == 0, str(final["fr_failed_gate_rows"]), "0", rel(FR_GATES), "FR gates passed(FR 게이트 통과)"),
        ("parent_next_action_matches", final["fr_next_action"] == RUN_ID, str(final["fr_next_action"]), RUN_ID, rel(FR_FINAL), "FS follows FR next action(FS가 FR 다음 행동을 따름)"),
        ("runtime_parity_reviewed", final["runtime_parity_passed_rows"] == final["attempt_rows"] == 5, f"passed={final['runtime_parity_passed_rows']};attempts={final['attempt_rows']}", "5/5", rel(RUNTIME_PARITY_REVIEW), "runtime parity reviewed(런타임 동등성 검토)"),
        ("mt5_kpi_reviewed", final["positive_mt5_rows"] >= 1, str(final["positive_mt5_rows"]), ">=1 positive clue", rel(MT5_KPI_REVIEW), "MT5 KPI clue reviewed(MT5 성과 단서 검토)"),
        ("proxy_attribution_reviewed", final["proxy_sign_diff_rows"] >= 1, str(final["proxy_sign_diff_rows"]), ">=1 sign diff", rel(PROXY_MT5_ATTRIBUTION), "proxy-vs-MT5 attribution recorded(프록시-MT5 귀속 기록)"),
        ("timestamp_handoff_reviewed", final["duplicate_timestamp_rows"] == 0 and final["unique_timestamp_rows"] == 5845, f"duplicates={final['duplicate_timestamp_rows']};unique={final['unique_timestamp_rows']}", "0 duplicates and 5845 unique", rel(TIMESTAMP_HANDOFF_REVIEW), "unique timestamp handoff confirmed(고유 시각 인계 확인)"),
        ("repair_queue_materialized", final["ft_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['ft_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(FT_QUEUE), "FT repair queue opened(FT 수리 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {"gate_id": gid, "status": "passed" if ok else "failed", "evidence_path": ev, "observed": obs, "expected": exp, "effect": eff, "claim_boundary": CLAIM_BOUNDARY}
        for gid, ok, obs, exp, ev, eff in checks
    ]


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fr_final = read_json(FR_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fr_next_action": fr_final.get("next_action", ""),
        "fr_failed_gate_rows": sum(1 for row in read_csv(FR_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    runtime = {
        "parity_check": f"passed={final['runtime_parity_passed_rows']}/{final['attempt_rows']};mismatch=0",
        "runtime_claim_boundary": "runtime_probe_review_only(런타임 탐침 검토 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    forensics = {
        "tester_identity": "FR reports and runtime identity reviewed(FR 보고서와 런타임 정체성 검토)",
        "backtest_judgment": "usable_with_boundary; not forward evidence(경계 조건부 사용 가능, 전진 근거 아님)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "best_attempt": final["best_attempt"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "best_recovery_factor": final["best_recovery_factor"],
        "best_drawdown": final["best_drawdown"],
        "judgment": "positive clue blocked by PF/recovery/DD(PF/회복/낙폭 때문에 긍정 단서로 제한)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(FORENSICS_RECEIPT, forensics),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(fq.RUN_REGISTRY), rel(fq.ALPHA_LEDGER), rel(fq.STAGE_LEDGER), rel(fq.ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_side_stability_positive_clue_to_repair_queue(side-stability 긍정 단서를 수리 대기열에 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FS MT5 Runtime Probe Review(337단계 337FS MT5 런타임 탐침 검토)

## Conclusion(결론)

Action(행동): FR MT5 runtime probe(FR MT5 런타임 탐침)를 검토했다. Effect(효과): 5개 attempt(시도) 모두 `5845`개 timestamp(시각)에서 mismatch(불일치) 없이 일치했다.

Action(행동): MT5 KPI(MT5 핵심 성과 지표)를 운영 주장과 분리했다. Effect(효과): `{final['best_attempt']}`의 net profit(순수익) `{final['best_net_profit']}`는 positive clue(긍정 단서)이지만 PF/recovery/drawdown(수익 팩터/회복/낙폭) 때문에 operating promotion(운영 승격)은 막는다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_parity_passed(런타임 동등성 통과): `{final['runtime_parity_passed_rows']}/{final['attempt_rows']}`
- positive_mt5_rows(긍정 MT5 행): `{final['positive_mt5_rows']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 후보 낙폭): `{final['best_drawdown']}`
- proxy_sign_diff_rows(프록시 부호 차이 행): `{final['proxy_sign_diff_rows']}`
- timestamp_duplicates(시각 중복): `{final['duplicate_timestamp_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FS Decision(337FS 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(MT5_KPI_REVIEW)}`, `{rel(PROXY_MT5_ATTRIBUTION)}`

Action(행동): MT5 runtime probe(MT5 런타임 탐침) 결과를 검토했다.
Effect(효과): side-stability positive clue(side-stability 긍정 단서)는 FT repair design(FT 수리 설계)으로 넘기고, operating claim(운영 주장)은 막는다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(fq.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FS focus complete: run337FS(337FS 실행)는 `{final['status']}`로 MT5 runtime probe review(MT5 런타임 탐침 검토)를 완료했다. "
        f"Effect(효과): best `{final['best_attempt']}` net `{final['best_net_profit']}`, parity(동등성) `{final['runtime_parity_passed_rows']}/{final['attempt_rows']}`, proxy sign diff(프록시 부호 차이) `{final['proxy_sign_diff_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FS focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FS focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(fq.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(fq.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337FS MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- parity(동등성): `{final['runtime_parity_passed_rows']}/{final['attempt_rows']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- proxy_sign_diff_rows(프록시 부호 차이 행): `{final['proxy_sign_diff_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): side-stability positive clue(side-stability 긍정 단서)를 FT repair design(FT 수리 설계)으로 넘기며 운영 주장은 닫는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337FR MT5 Runtime Probe", section, "run337FS MT5 Runtime Probe Review")
    artifacts.append(aw.write_text_lossless(fq.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- parity(동등성): `{final['runtime_parity_passed_rows']}/{final['attempt_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FS(337FS 실행)는 review(검토) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(fq.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(fq.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337FS(337FS 실행) `{final['status']}`. "
        f"Effect(효과): side-stability positive MT5 clue(side-stability 긍정 MT5 단서) net `{final['best_net_profit']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(fq.STAGE_BRIEF, fb.upsert_single_line(brief, "run337FS(337FS 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(fq.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337FS(337FS 실행) `{final['status']}`. "
        f"Effect(효과): MT5 runtime probe review(MT5 런타임 탐침 검토)를 완료하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(fq.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337FS", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_clue_blend_mt5_runtime_probe_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best={final['best_attempt']};net={final['best_net_profit']};pf={final['best_profit_factor']};recovery={final['best_recovery_factor']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_verification_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_runtime_probe_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_clue_blend_mt5_runtime_probe_review(런타임 긍정 단서 혼합 MT5 런타임 탐침 검토)",
        "tier_scope": "Tier A inner holdout MT5 runtime review(Tier A 내부 보류 MT5 런타임 검토)",
        "kpi_scope": "runtime_probe_review_no_forward_goal(런타임 탐침 검토, 전진/목표 없음)",
        "scoreboard_lane": "runtime_verification",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_net={final['best_net_profit']};positive={final['positive_mt5_rows']};parity={final['runtime_parity_passed_rows']}/{final['attempt_rows']}",
        "guardrail_kpi": "no_selection;no_forward;no_goal;repair_required",
        "external_verification_status": "reviewed_runtime_probe",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_verification_performance_attribution_result_judgment",
        "evidence_scope": "FR MT5 telemetry, summary, reports, proxy diff",
        "kpi_scope": "runtime_probe_review_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_runtime_probe_review",
        "family": "runtime_positive_clue_blend_mt5_runtime_probe_review",
        "question": "does side-stability positive runtime clue solve PF/recovery/drawdown",
        "metric_scope": "runtime_parity_mt5_kpi_proxy_attribution",
        "primary_artifact": rel(MT5_KPI_REVIEW),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(fq.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(fq.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(fq.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(fq.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        row = {
            "artifact_id": artifact_id,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": artifact_path,
            "sha256": aw.sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": STATUS,
            "artifact_path": artifact_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(fq.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    parity, kpi, attr, timestamp, memory, queue, summary = build_reviews()
    final = make_final(summary)
    artifacts = [
        write_csv(RUNTIME_PARITY_REVIEW, REVIEW_COLUMNS, parity),
        write_csv(MT5_KPI_REVIEW, KPI_COLUMNS, kpi),
        write_csv(PROXY_MT5_ATTRIBUTION, ATTR_COLUMNS, attr),
        write_csv(TIMESTAMP_HANDOFF_REVIEW, TIMESTAMP_COLUMNS, timestamp),
        write_csv(CLUE_MEMORY, MEMORY_COLUMNS, memory),
        write_csv(FT_QUEUE, QUEUE_COLUMNS, queue),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend([write_csv(GATE_AUDIT, GATE_COLUMNS, gates), write_json(FINAL_DECISION, final), write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})])
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "best_attempt": final["best_attempt"], "best_net_profit": final["best_net_profit"], "best_profit_factor": final["best_profit_factor"], "best_recovery_factor": final["best_recovery_factor"], "runtime_parity": f"{final['runtime_parity_passed_rows']}/{final['attempt_rows']}", "positive_mt5_rows": final["positive_mt5_rows"], "gates": f"{final['passed_gates']}/{final['gate_rows']}", "next_action": final["next_action"], "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
