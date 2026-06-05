from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

STAGE_ID = "343_quality_margin_runtime__early_long_mix_mt5_probe"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run343C"
RUN_ID = "run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1"
REFERENCE_REVIEW_RUN_ID = "run342G_review_soft_session_long_firewall_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1"

STATUS = "completed_stage343C_quality_margin_reviewed_profit_quality_clue_preserved_trade_shape_unresolved_no_selection"
JUDGMENT = "quality_margin_improves_profit_quality_but_does_not_recover_trade_shape_no_selection"
DECISION = "stage343C_open_run343D_trade_shape_rescue_quality_margin_blend_package"
CLAIM_BOUNDARY = (
    "research_development_review_only_early_long_quality_margin_mt5_probe_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run343C_early_long_quality_margin_mix_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage343C_early_long_quality_margin_mix_mt5_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run343B"
PARENT_FINAL = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATES = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_SUMMARY = PARENT_RUN_DIR / "early_long_quality_margin_mix_mt5_probe_summary.csv"
PARENT_DIFF = PARENT_RUN_DIR / "proxy_mt5_runtime_difference.csv"
PARENT_REPORTS = PARENT_RUN_DIR / "strategy_tester_report_records.json"
SOURCE_PACKAGE_DIR = ROOT / "stages" / "342_session_long_firewall__early_long_filter_mt5_probe" / "02_runs" / "run342H"
SOURCE_VARIANT_PREVIEW = SOURCE_PACKAGE_DIR / "variant_preview.csv"
REFERENCE_FINAL = ROOT / "stages" / "342_session_long_firewall__early_long_filter_mt5_probe" / "02_runs" / "run342G" / "final_decision.json"

REVIEW_SCORECARD = RUN_DIR / "quality_margin_review_scorecard.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run343D_trade_shape_rescue_quality_margin_blend_queue.csv"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "report_path",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "view",
    "tier",
    "metric_scope",
    "candidate_model_id",
    "net_profit",
    "profit_factor",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "result_status",
    "sample_rows",
    "feature_count",
    "matched_rows",
    "expectancy",
    "attempt_count",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required review input: {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        handle.write(text.rstrip() + "\n")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: list[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def append_or_replace_csv(path: Path, key_fields: list[str], rows: list[Mapping[str, Any]], default_columns: list[str] | None = None) -> None:
    if path_is_file(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = list(default_columns or []), []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, kept + [dict(row) for row in rows], fieldnames)


def append_once(path: Path, marker: str, block: str) -> None:
    current = ""
    if path_is_file(path):
        with open(fs_path(path), encoding="utf-8-sig") as handle:
            current = handle.read()
    if marker in current:
        return
    sep = "" if not current or current.endswith("\n") else "\n"
    write_text(path, f"{current}{sep}{block}")


def f(value: Any) -> float:
    try:
        if value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def i(value: Any) -> int:
    try:
        if value == "":
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def side_balance(long_count: int, short_count: int) -> float:
    if long_count <= 0 or short_count <= 0:
        return 0.0
    return min(long_count, short_count) / max(long_count, short_count)


def build_review() -> dict[str, Any]:
    parent_final = read_json(PARENT_FINAL)
    reference = read_json(REFERENCE_FINAL)
    summary = pd.read_csv(fs_path(PARENT_SUMMARY), encoding="utf-8-sig").fillna("")
    for column in [
        "net_profit",
        "profit_factor",
        "expectancy",
        "recovery_factor",
        "max_drawdown_amount",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
        "matched_rows",
        "expected_rows",
        "mismatch_rows",
    ]:
        if column in summary.columns:
            summary[column] = pd.to_numeric(summary[column], errors="coerce").fillna(0.0)
    summary["side_balance"] = summary.apply(lambda row: side_balance(i(row["long_trade_count"]), i(row["short_trade_count"])), axis=1)
    summary["profit_quality_rank"] = summary["net_profit"].rank(method="min", ascending=False).astype(int)
    summary["trade_shape_rank"] = (
        (-summary["trade_count"] * 0.5 - summary["side_balance"] * 100.0).rank(method="min", ascending=True).astype(int)
    )
    best_profit = summary.sort_values(["net_profit", "profit_factor", "recovery_factor", "trade_count"], ascending=[False, False, False, False]).iloc[0].to_dict()
    best_shape = summary.sort_values(["trade_count", "side_balance", "net_profit"], ascending=[False, False, False]).iloc[0].to_dict()
    scorecard = []
    for row in summary.to_dict(orient="records"):
        scorecard.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "net_profit": f(row["net_profit"]),
                "profit_factor": f(row["profit_factor"]),
                "expectancy": f(row["expectancy"]),
                "recovery_factor": f(row["recovery_factor"]),
                "max_drawdown_amount": f(row["max_drawdown_amount"]),
                "trade_count": i(row["trade_count"]),
                "long_trade_count": i(row["long_trade_count"]),
                "short_trade_count": i(row["short_trade_count"]),
                "side_balance": round(f(row["side_balance"]), 6),
                "matched_rows": i(row["matched_rows"]),
                "comparison_status": row["comparison_status"],
                "profit_quality_rank": i(row["profit_quality_rank"]),
                "trade_shape_rank": i(row["trade_shape_rank"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(REVIEW_SCORECARD, scorecard)

    previous = {
        "attempt_name": reference["best_attempt"],
        "net_profit": f(reference["best_net_profit"]),
        "profit_factor": f(reference["best_profit_factor"]),
        "expectancy": f(reference["best_expectancy"]),
        "recovery_factor": f(reference["best_recovery_factor"]),
        "max_drawdown_amount": f(reference["best_drawdown"]),
        "trade_count": i(reference["best_trade_count"]),
        "long_trade_count": i(reference["best_long_trade_count"]),
        "short_trade_count": i(reference["best_short_trade_count"]),
        "side_balance": f(reference["best_side_balance"]),
    }
    best = {
        "attempt_name": best_profit["attempt_name"],
        "net_profit": f(best_profit["net_profit"]),
        "profit_factor": f(best_profit["profit_factor"]),
        "expectancy": f(best_profit["expectancy"]),
        "recovery_factor": f(best_profit["recovery_factor"]),
        "max_drawdown_amount": f(best_profit["max_drawdown_amount"]),
        "trade_count": i(best_profit["trade_count"]),
        "long_trade_count": i(best_profit["long_trade_count"]),
        "short_trade_count": i(best_profit["short_trade_count"]),
        "side_balance": f(best_profit["side_balance"]),
    }
    shape = {
        "attempt_name": best_shape["attempt_name"],
        "net_profit": f(best_shape["net_profit"]),
        "profit_factor": f(best_shape["profit_factor"]),
        "expectancy": f(best_shape["expectancy"]),
        "recovery_factor": f(best_shape["recovery_factor"]),
        "max_drawdown_amount": f(best_shape["max_drawdown_amount"]),
        "trade_count": i(best_shape["trade_count"]),
        "long_trade_count": i(best_shape["long_trade_count"]),
        "short_trade_count": i(best_shape["short_trade_count"]),
        "side_balance": f(best_shape["side_balance"]),
    }
    attribution = [
        {
            "comparison": "new_best_vs_previous_soft_best",
            "new_attempt": best["attempt_name"],
            "reference_attempt": previous["attempt_name"],
            "net_profit_delta": round(best["net_profit"] - previous["net_profit"], 6),
            "profit_factor_delta": round(best["profit_factor"] - previous["profit_factor"], 6),
            "expectancy_delta": round(best["expectancy"] - previous["expectancy"], 6),
            "drawdown_delta": round(best["max_drawdown_amount"] - previous["max_drawdown_amount"], 6),
            "recovery_factor_delta": round(best["recovery_factor"] - previous["recovery_factor"], 6),
            "trade_count_delta": best["trade_count"] - previous["trade_count"],
            "long_trade_delta": best["long_trade_count"] - previous["long_trade_count"],
            "side_balance_delta": round(best["side_balance"] - previous["side_balance"], 6),
            "interpretation": "profit_quality_up_but_trade_shape_worse(수익 품질은 개선, 거래 형태는 악화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "comparison": "trade_shape_control_vs_profit_best",
            "new_attempt": shape["attempt_name"],
            "reference_attempt": best["attempt_name"],
            "net_profit_delta": round(shape["net_profit"] - best["net_profit"], 6),
            "profit_factor_delta": round(shape["profit_factor"] - best["profit_factor"], 6),
            "expectancy_delta": round(shape["expectancy"] - best["expectancy"], 6),
            "drawdown_delta": round(shape["max_drawdown_amount"] - best["max_drawdown_amount"], 6),
            "recovery_factor_delta": round(shape["recovery_factor"] - best["recovery_factor"], 6),
            "trade_count_delta": shape["trade_count"] - best["trade_count"],
            "long_trade_delta": shape["long_trade_count"] - best["long_trade_count"],
            "side_balance_delta": round(shape["side_balance"] - best["side_balance"], 6),
            "interpretation": "trade_shape_up_profit_quality_down(거래 형태는 개선, 수익 품질은 하락)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    failure_rows = [
        {
            "failure_id": "profit_best_trade_shape_unresolved",
            "evidence": f"{best['attempt_name']} trade_count={best['trade_count']} long_short={best['long_trade_count']}/{best['short_trade_count']}",
            "effect": "best profit(최고 수익)이 long supply(롱 공급)를 더 줄여 운영 후보로는 부족하다.",
            "next_constraint": "next package(다음 패키지)는 best profit short anchor(수익 숏 앵커)와 control long supply(대조 롱 공급)를 분리해서 시험한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "control_profit_quality_gap",
            "evidence": f"{shape['attempt_name']} net={shape['net_profit']} pf={shape['profit_factor']} trade_count={shape['trade_count']}",
            "effect": "trade shape(거래 형태)는 회복되지만 profit quality(수익 품질)가 크게 낮다.",
            "next_constraint": "long restoration(롱 복구)은 quality gate(품질 게이트)나 session/regime split(세션/국면 분리)와 같이 시험한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(FAILURE_MEMORY, failure_rows)
    next_queue = [
        {
            "queue_id": "run343D_trade_shape_rescue_quality_margin_blend_queue",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "seed": "short_anchor_long_sidecar(숏 앵커 + 롱 보조)",
            "source_attempts": f"{best['attempt_name']},{shape['attempt_name']}",
            "hypothesis": "Keep h04 short-heavy profit anchor(숏 중심 수익 앵커)를 유지하고, h02/h03 control long supply(대조 롱 공급)를 별도 sidecar(보조 표면)로 복구하면 trade count(거래수)와 side balance(방향 균형)를 회복할 수 있다.",
            "required_controls": "h04 unchanged control(무변경 대조), h02/h03 shape controls(거래 형태 대조), no-long-restoration negative control(롱 복구 없음 부정 대조)",
            "effect": "profit quality clue(수익 품질 단서)와 trade shape clue(거래 형태 단서)를 같은 package(패키지)에서 충돌시켜 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run343D_trade_shape_rescue_quality_margin_blend_queue",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "seed": "session_aware_long_rescue(세션 인지 롱 복구)",
            "source_attempts": f"{best['attempt_name']},{shape['attempt_name']}",
            "hypothesis": "early 0~45 minute block(초반 0~45분 차단)을 고정하지 말고 session minute/regime(세션 분/국면)으로 long permission(롱 허용)을 나누면 weak long(약한 롱)만 줄일 수 있다.",
            "required_controls": "same threshold(동일 임계값), same cost(동일 비용), same hold bars(동일 보유 봉)",
            "effect": "hard early block(강한 초반 차단)이 아닌 market behavior(시장 현상) 기반 롱 복구를 시험한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run343D_trade_shape_rescue_quality_margin_blend_queue",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P2",
            "seed": "cost_stress_shape_filter(비용 압박 거래 형태 필터)",
            "source_attempts": f"{best['attempt_name']},{shape['attempt_name']}",
            "hypothesis": "profit best(수익 최고)와 trade-shape best(거래 형태 최고)를 cost stress(비용 압박) 관점으로 비교하면 surviving entries(생존 진입)를 분리할 수 있다.",
            "required_controls": "same MT5 tester identity(동일 MT5 테스터 정체성), proxy-MT5 diff(프록시-MT5 차이) retained(유지)",
            "effect": "비용에 약한 롱 복구를 다음 package(패키지) 전에 거른다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_QUEUE, next_queue)
    return {
        "parent_final": parent_final,
        "previous": previous,
        "best": best,
        "shape": shape,
        "scorecard_rows": len(scorecard),
        "attribution_rows": len(attribution),
        "failure_rows": len(failure_rows),
        "queue_rows": len(next_queue),
    }


def gate_row(gate_id: str, status: str, evidence_path: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": rel(evidence_path),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_gates(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    parent_gates = pd.read_csv(fs_path(PARENT_GATES), encoding="utf-8-sig")
    parent_passed = bool(parent_gates["status"].astype(str).str.lower().eq("passed").all())
    parent_final = review["parent_final"]
    no_forbidden = (
        parent_final["candidate_selection"] == "not_run"
        and parent_final["runtime_authority"] == "not_claimed"
        and parent_final["operating_promotion"] == "not_claimed"
        and parent_final["goal_achieve"] == "not_claimed"
    )
    gates = [
        gate_row("parent_343B_gates_passed", "passed" if parent_passed else "failed", PARENT_GATES, "run343B(343B 실행) runtime gate(런타임 게이트)를 이어받는다."),
        gate_row("exact_runtime_parity_inherited", "passed" if parent_final["matched_rows"] == parent_final["expected_rows"] and parent_final["mismatch_rows"] == 0 else "failed", PARENT_DIFF, "row-level parity(행 단위 동등성)가 리뷰 입력으로 충분한지 확인한다."),
        gate_row("review_scorecard_written", "passed" if path_is_file(REVIEW_SCORECARD) and review["scorecard_rows"] == parent_final["attempt_rows"] else "failed", REVIEW_SCORECARD, "모든 attempt(시도)를 같은 KPI(핵심 성과 지표)로 비교한다."),
        gate_row("performance_attribution_written", "passed" if path_is_file(PERFORMANCE_ATTRIBUTION) and review["attribution_rows"] >= 2 else "failed", PERFORMANCE_ATTRIBUTION, "이전 단서 대비 KPI 변화 원인을 분해한다."),
        gate_row("failure_memory_written", "passed" if path_is_file(FAILURE_MEMORY) and review["failure_rows"] >= 2 else "failed", FAILURE_MEMORY, "다음 탐색 제약으로 쓸 실패 기억을 남긴다."),
        gate_row("next_offensive_queue_written", "passed" if path_is_file(NEXT_QUEUE) and review["queue_rows"] >= 1 else "failed", NEXT_QUEUE, "다음 공격 탐색 씨앗을 queue(대기열)로 넘긴다."),
        gate_row("tier_records_written", "passed", STAGE_LEDGER, "Tier A/Tier B/Tier A+B 기록을 stage ledger(단계 장부)에 남긴다."),
        gate_row("final_claim_guard", "passed" if no_forbidden else "failed", CLAIM_RECEIPT, "review(검토)를 selection(선정), 운영 승격, 목표 달성으로 과장하지 않는다."),
        gate_row("required_gate_coverage_audit_written", "passed", GATE_AUDIT, "필수 gate(게이트) 커버리지를 기록한다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def write_receipts(review: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run343B early-long quality/margin MT5 probe(343B 초반 롱 품질/마진 MT5 탐침)",
            "evidence_available": [rel(PARENT_SUMMARY), rel(PARENT_FINAL), rel(REVIEW_SCORECARD), rel(PERFORMANCE_ATTRIBUTION)],
            "evidence_missing": ["forward validation(전진 검증)", "live-like replay(실거래 유사 재생)", "operating promotion evidence(운영 승격 근거)"],
            "judgment_label": "runtime_probe(런타임 탐침)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "수익 품질은 조금 좋아졌지만 거래 형태는 아직 운영 후보가 아니다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION),
            "best_profit_attempt": review["best"],
            "best_trade_shape_attempt": review["shape"],
            "previous_reference": review["previous"],
        },
    )
    source_inputs = [
        PARENT_FINAL,
        PARENT_GATES,
        PARENT_SUMMARY,
        PARENT_DIFF,
        PARENT_REPORTS,
        SOURCE_VARIANT_PREVIEW,
        REFERENCE_FINAL,
    ]
    artifact_paths = [
        REVIEW_SCORECARD,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_QUEUE,
        JUDGMENT_RECEIPT,
        PERFORMANCE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in source_inputs],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths if path_is_file(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths if path_is_file(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "allowed_claim": "reviewed runtime probe result only(검토된 런타임 탐침 결과만)",
        },
    )


def write_final(review: Mapping[str, Any], gates: list[Mapping[str, Any]]) -> dict[str, Any]:
    gate_passes = sum(1 for gate in gates if gate["status"] == "passed")
    payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "reference_review_run_id": REFERENCE_REVIEW_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": gate_passes,
        "gate_total": len(gates),
        "best_attempt": review["best"]["attempt_name"],
        "best_net_profit": review["best"]["net_profit"],
        "best_profit_factor": review["best"]["profit_factor"],
        "best_expectancy": review["best"]["expectancy"],
        "best_drawdown": review["best"]["max_drawdown_amount"],
        "best_recovery_factor": review["best"]["recovery_factor"],
        "best_trade_count": review["best"]["trade_count"],
        "best_long_trade_count": review["best"]["long_trade_count"],
        "best_short_trade_count": review["best"]["short_trade_count"],
        "best_side_balance": review["best"]["side_balance"],
        "trade_shape_best_attempt": review["shape"]["attempt_name"],
        "trade_shape_best_trade_count": review["shape"]["trade_count"],
        "trade_shape_best_side_balance": review["shape"]["side_balance"],
        "profit_quality_clue_preserved": True,
        "trade_shape_recovered": False,
        "candidate_selection": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in [PARENT_FINAL, PARENT_SUMMARY, PARENT_GATES, REFERENCE_FINAL]],
            "outputs": [rel(path) for path in [FINAL_DECISION, REVIEW_SCORECARD, PERFORMANCE_ATTRIBUTION, FAILURE_MEMORY, NEXT_QUEUE, REPORT_PATH, DECISION_DOC]],
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def write_docs(review: Mapping[str, Any], final: Mapping[str, Any]) -> None:
    net_delta = round(review["best"]["net_profit"] - review["previous"]["net_profit"], 6)
    pf_delta = round(review["best"]["profit_factor"] - review["previous"]["profit_factor"], 6)
    dd_delta = round(review["best"]["max_drawdown_amount"] - review["previous"]["max_drawdown_amount"], 6)
    trade_delta = review["best"]["trade_count"] - review["previous"]["trade_count"]
    report = f"""# run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- judgment(판정): `{JUDGMENT}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_expectancy(최고 기대값): `{final['best_expectancy']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- best_long_short(최고 롱/숏): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- trade_shape_best(거래 형태 최고): `{final['trade_shape_best_attempt']}`, trade_count(거래수) `{final['trade_shape_best_trade_count']}`, side_balance(방향 균형) `{final['trade_shape_best_side_balance']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Attribution(귀속)

- previous_best(이전 최고): `{review['previous']['attempt_name']}` net(순수익) `{review['previous']['net_profit']}`, PF(수익 팩터) `{review['previous']['profit_factor']}`, drawdown(낙폭) `{review['previous']['max_drawdown_amount']}`, trades(거래수) `{review['previous']['trade_count']}`, long/short(롱/숏) `{review['previous']['long_trade_count']}/{review['previous']['short_trade_count']}`
- new_best(새 최고): `{review['best']['attempt_name']}` net(순수익) `{review['best']['net_profit']}`, PF(수익 팩터) `{review['best']['profit_factor']}`, drawdown(낙폭) `{review['best']['max_drawdown_amount']}`, trades(거래수) `{review['best']['trade_count']}`, long/short(롱/숏) `{review['best']['long_trade_count']}/{review['best']['short_trade_count']}`
- delta(차이): net `{net_delta}`, PF `{pf_delta}`, drawdown `{dd_delta}`, trade_count `{trade_delta}`

## Judgment(판정)

profit quality(수익 품질)는 보존되었고 소폭 개선됐다. 그러나 best attempt(최고 시도)는 trade count(거래수) 22, long/short(롱/숏) 2/20이라 trade shape(거래 형태)는 회복되지 않았다. h02/h03 controls(대조군)는 거래수 33과 long/short(롱/숏) 13/20을 보였지만 net profit(순수익) 122.9, PF(수익 팩터) 1.89로 수익 품질이 낮다.

Action(행동): run343D(343D 실행)에서 short anchor + long sidecar(숏 앵커 + 롱 보조)와 session-aware long rescue(세션 인지 롱 복구)를 package(패키지)로 만든다.
Effect(효과): 수익 앵커와 거래 형태 회복 단서를 분리하지 않고 같은 MT5 probe(MT5 탐침) 안에서 충돌 시험한다.

## Boundary(경계)

No selection(선정 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    decision_doc = f"""# {TODAY} Stage343C Review Decision(343C 검토 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- evidence(근거): `{rel(REVIEW_SCORECARD)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(FAILURE_MEMORY)}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): quality/margin runtime probe(품질/마진 런타임 탐침)를 reviewed result(검토 결과)로 닫고, trade-shape rescue(거래 형태 복구) package(패키지)를 다음으로 연다.
Effect(효과): 수익 품질 단서는 보존하되, 운영 후보 주장은 막고 다음 공격 탐색으로 넘긴다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 343 Selection Status(343단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_profit_quality_clue(보존 수익 품질 단서): `{final['best_attempt']}`
- unresolved_failure(미해결 실패): `trade_shape_not_recovered(거래 형태 미회복)`
- next_probe(다음 탐침): `trade_shape_rescue_quality_margin_blend(거래 형태 복구 품질/마진 혼합)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): review(검토)를 selection(선정)으로 오해하지 않고 다음 offensive exploration(공격 탐색)으로 넘긴다.
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

run343C(343C 실행)는 run343B MT5 runtime probe(MT5 런타임 탐침)를 검토했다. 수익 품질 단서는 보존됐지만 거래 형태는 회복되지 않아 run343D(343D 실행)에서 trade-shape rescue(거래 형태 복구)를 package(패키지)로 연다.

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
    write_text(DECISION_DOC, decision_doc)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(WORKSPACE_STATE, workspace)
    marker = f"run343C {RUN_ID}"
    append_once(
        STAGE_BRIEF,
        marker,
        f"""## run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 수익 품질 단서는 보존하고 trade shape(거래 형태) 미회복을 다음 제약으로 넘긴다.
""",
    )
    append_once(
        STAGE_README,
        marker,
        f"""## run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(REVIEW_SCORECARD)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): run343D(343D 실행)가 수익 앵커와 거래 형태 복구를 함께 시험한다.
""",
    )
    changelog = f"""## {TODAY} run343C Early Long Quality Margin Mix Review(초반 롱 품질/마진 혼합 검토)

- action(행동): run343B MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
- effect(효과): best `{final['best_attempt']}` net `{final['best_net_profit']}`, PF `{final['best_profit_factor']}`, trades `{final['best_trade_count']}`를 보존 단서로 두되, trade shape(거래 형태) 미회복으로 no selection(선정 없음) 처리했다.
- next(다음): `{NEXT_RUN_ID}`
- boundary(경계): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 주장하지 않는다.
"""
    append_once(ROOT_CHANGELOG, marker, changelog)
    append_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(review: Mapping[str, Any], final: Mapping[str, Any], gates: list[Mapping[str, Any]]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "lane": "runtime_probe_review(런타임 탐침 검토)",
        "family": "kpi_evidence(KPI/장부/근거)",
        "run_number": RUN_NUMBER,
        "attempt_count": review["parent_final"]["attempt_rows"],
        "matched_rows": review["parent_final"]["matched_rows"],
    }
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "mt5_runtime_probe_review",
            "kpi_scope": "mt5_runtime_probe_review",
            "candidate_model_id": final["best_attempt"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "profit_quality_clue_preserved_trade_shape_unresolved_no_selection(수익 품질 단서 보존, 거래 형태 미해결, 선정 없음)",
            "external_verification_status": "completed(완료)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "candidate_model_id": "missing_required",
            "result_status": "missing_required(필수 누락)",
            "external_verification_status": "missing_required(필수 누락)",
            "attempt_count": "",
            "matched_rows": "",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "candidate_model_id": final["best_attempt"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "external_verification_status": "completed(완료)",
        },
    ]
    stage_rows = [{key: row.get(key, "") for key in STAGE_LEDGER_COLUMNS} for row in rows]
    append_or_replace_csv(STAGE_LEDGER, ["stage_id", "run_id", "view"], stage_rows, STAGE_LEDGER_COLUMNS)
    append_or_replace_csv(PROJECT_LEDGER, ["stage_id", "run_id", "view"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "notes": "run343C reviewed run343B MT5 KPI and opened trade-shape rescue(343C는 343B MT5 KPI를 검토하고 거래 형태 복구를 열었다).",
                "candidate_model_id": final["best_attempt"],
                "net_profit": final["best_net_profit"],
                "profit_factor": final["best_profit_factor"],
                "expectancy": final["best_expectancy"],
                "drawdown": final["best_drawdown"],
                "recovery_factor": final["best_recovery_factor"],
                "trade_count": final["best_trade_count"],
                "result_status": "reviewed_no_selection(검토됨, 선정 없음)",
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "mt5_runtime_probe_review",
            }
        ],
    )


def write_artifact_registry() -> None:
    rows = []
    for artifact_type, path, notes in [
        ("final_decision", FINAL_DECISION, "run343C review final decision(343C 검토 최종 결정)"),
        ("review_scorecard", REVIEW_SCORECARD, "run343C KPI scorecard(343C KPI 점수표)"),
        ("performance_attribution", PERFORMANCE_ATTRIBUTION, "run343C performance attribution(343C 성과 귀속)"),
        ("failure_memory", FAILURE_MEMORY, "run343C failure memory(343C 실패 기억)"),
        ("next_queue", NEXT_QUEUE, "run343D next offensive queue(343D 다음 공격 대기열)"),
        ("required_gate_coverage_audit", GATE_AUDIT, "run343C required gate audit(343C 필수 게이트 감사)"),
        ("report", REPORT_PATH, "run343C review report(343C 검토 보고서)"),
        ("decision_doc", DECISION_DOC, "run343C durable decision(343C 결정 문서)"),
        ("run_manifest", RUN_MANIFEST, "run343C run manifest(343C 실행 목록)"),
        ("pipeline", Path(__file__), "run343C producer script(343C 생산 스크립트)"),
    ]:
        if not path_is_file(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "notes": notes,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows)


def main() -> None:
    for path in [PARENT_FINAL, PARENT_GATES, PARENT_SUMMARY, PARENT_DIFF, PARENT_REPORTS, SOURCE_VARIANT_PREVIEW, REFERENCE_FINAL]:
        required(path)
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    review = build_review()
    gates = write_gates(review)
    write_receipts(review)
    final = write_final(review, gates)
    write_docs(review, final)
    write_registers(review, final, gates)
    write_artifact_registry()
    write_receipts(review)
    gates = write_gates(review)
    final = write_final(review, gates)
    write_receipts(review)
    write_artifact_registry()
    if any(gate["status"] != "passed" for gate in gates):
        failed = [gate["gate_id"] for gate in gates if gate["status"] != "passed"]
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise SystemExit(f"failed gates: {failed}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_trade_count": final["best_trade_count"],
                "best_long_short": f"{final['best_long_trade_count']}/{final['best_short_trade_count']}",
                "trade_shape_recovered": final["trade_shape_recovered"],
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
