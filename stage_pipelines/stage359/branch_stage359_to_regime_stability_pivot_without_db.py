from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

SOURCE_STAGE_ID = "359_runtime_probe_execution__high_density_label_pivot_mt5_check"
NEW_STAGE_ID = "360_regime_stability_pivot__oos_long_cash_edge_validation_loss"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run359D"
RUN_ID = "run359D_branch_to_stage360_regime_stability_pivot_v1"
PARENT_RUN_ID = "run359C_review_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run360A_design_regime_stability_pivot_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run358B_package_high_density_label_pivot_mt5_probe_without_db_v1"

STATUS = "completed_stage359D_branch_stage360_regime_stability_pivot_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage359_positive_oos_validation_instability_to_stage360_no_operating_claim"
DECISION = "stage359D_open_run360A_design_regime_stability_pivot_without_db_v1"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_stage359_to_stage360_regime_stability_pivot_handoff_only_"
    "no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run359C"
SOURCE_MT5_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run359B"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_REVIEW_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run359C_high_density_label_pivot_mt5_probe_review.md"
SOURCE_SEGMENT_ATTRIBUTION = SOURCE_RUN_DIR / "trade_level_segment_attribution.csv"
SOURCE_COST_SENSITIVITY = SOURCE_RUN_DIR / "cost_drag_sensitivity.csv"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REVIEW_SUMMARY = SOURCE_RUN_DIR / "review_summary.json"
SOURCE_RUNTIME_DIFF = SOURCE_MT5_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_MT5_SUMMARY = SOURCE_MT5_RUN_DIR / "high_density_label_pivot_mt5_probe_summary.csv"
SOURCE_STRATEGY_REPORTS = SOURCE_MT5_RUN_DIR / "strategy_tester_report_records.json"
SOURCE_SCRIPT = ROOT / "stage_pipelines" / "stage359" / "review_high_density_label_pivot_mt5_probe_without_db.py"

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
SPEC_DIR = NEW_STAGE_DIR / "00_spec"
INPUT_DIR = NEW_STAGE_DIR / "01_inputs"
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
SELECTED_DIR = NEW_STAGE_DIR / "04_selected"

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
INPUT_MANIFEST = INPUT_DIR / "stage360_input_manifest.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
REPORT_PATH = REVIEW_DIR / "run359D_stage_branch.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
README = NEW_STAGE_DIR / "README.md"

SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_README = SOURCE_STAGE_DIR / "README.md"
SOURCE_STAGE_LEDGER = SOURCE_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage359D_branch_to_stage360_regime_stability_pivot.md"

HANDOFF_MANIFEST = RUN_DIR / "stage359C_to_stage360_handoff_manifest.csv"
STAGE_TRANSITION_RECEIPT = RUN_DIR / "stage_transition_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
STATE_SYNC_AUDIT = RUN_DIR / "state_sync_audit.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def ensure_dirs() -> None:
    for directory in [SPEC_DIR, INPUT_DIR, RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames and (extend_header or not fieldnames):
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def source_summary(source_final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "best_attempt_name": source_final.get("best_attempt_name"),
        "best_model_id": source_final.get("best_model_id"),
        "best_probe_split": source_final.get("best_probe_split"),
        "best_net_profit": source_final.get("best_net_profit"),
        "best_profit_factor": source_final.get("best_profit_factor"),
        "best_expectancy": source_final.get("best_expectancy"),
        "best_recovery_factor": source_final.get("best_recovery_factor"),
        "best_max_drawdown_amount": source_final.get("best_max_drawdown_amount"),
        "best_trade_count": source_final.get("best_trade_count"),
        "best_long_trade_count": source_final.get("best_long_trade_count"),
        "best_short_trade_count": source_final.get("best_short_trade_count"),
        "best_trade_density_per_feature_day": source_final.get("best_trade_density_per_feature_day"),
        "proxy_mt5_mismatch_rows": source_final.get("proxy_mt5_mismatch_rows"),
        "proxy_mt5_max_abs_probability_diff": source_final.get("proxy_mt5_max_abs_probability_diff"),
        "oos_positive_rows": source_final.get("oos_positive_rows"),
        "validation_positive_rows": source_final.get("validation_positive_rows"),
        "q05_validation_net_profit": source_final.get("q05_validation_net_profit"),
        "q05_validation_max_drawdown_percent": source_final.get("q05_validation_max_drawdown_percent"),
        "q05_oos_month_positive_count": source_final.get("q05_oos_month_positive_count"),
        "q05_oos_month_total_count": source_final.get("q05_oos_month_total_count"),
        "cost_drag_0_2_survivors": source_final.get("cost_drag_0_2_survivors"),
        "cost_drag_0_3_survivors": source_final.get("cost_drag_0_3_survivors"),
    }


def source_inputs() -> list[tuple[Path, str, str]]:
    return [
        (SOURCE_FINAL_DECISION, "Stage359C final decision(359C 최종 결정)", "tracked_or_ignored_with_manifest"),
        (SOURCE_REVIEW_REPORT, "Stage359C review report(359C 검토 보고서)", "tracked"),
        (SOURCE_SEGMENT_ATTRIBUTION, "Stage359C segment attribution(359C 구간 귀속)", "tracked_or_ignored_with_manifest"),
        (SOURCE_COST_SENSITIVITY, "Stage359C cost sensitivity(359C 비용 민감도)", "tracked_or_ignored_with_manifest"),
        (SOURCE_GATE_AUDIT, "Stage359C gate audit(359C 게이트 감사)", "tracked_or_ignored_with_manifest"),
        (SOURCE_REVIEW_SUMMARY, "Stage359C review summary(359C 검토 요약)", "tracked_or_ignored_with_manifest"),
        (SOURCE_RUNTIME_DIFF, "Stage359B proxy-MT5 diff(359B 프록시-MT5 차이)", "tracked_or_ignored_with_manifest"),
        (SOURCE_MT5_SUMMARY, "Stage359B MT5 summary(359B MT5 요약)", "tracked_or_ignored_with_manifest"),
        (SOURCE_STRATEGY_REPORTS, "Stage359B Strategy Tester reports(359B 전략 테스터 보고서)", "tracked_or_ignored_with_manifest"),
        (SOURCE_SCRIPT, "Stage359C review producer script(359C 검토 생산 스크립트)", "tracked"),
    ]


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, role, storage_boundary in source_inputs():
        rows.append(
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "source_role": role,
                "path": rel(path),
                "available": str(exists(path)).lower(),
                "sha256": sha256_file(path) if exists(path) else "",
                "storage_boundary": storage_boundary,
                "effect": "Stage360 design(360단계 설계)이 OOS clue(표본외 단서)와 validation failure(검증 실패)를 동시에 소비하게 한다.",
            }
        )
    return rows


def tier_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "stage_branch_handoff_no_new_mt5_execution(단계 분기 인계, 새 MT5 실행 없음)",
        "notes": (
            "Stage359C reviewed MT5 runtime probe(359C 검토된 MT5 런타임 탐침)를 Stage360 regime stability pivot"
            "(360단계 국면 안정성 전환)으로 넘김; selection(선택) 없음."
        ),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": "4",
        "gate_passes": "9",
        "gate_total": "9",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "trained_models": "0",
        "onnx_parity": "",
        "best_proxy": "",
        "candidate_rows": "0",
        "positive_proxy_rows": "",
        "best_model_id": str(summary.get("best_model_id") or ""),
        "best_proxy_net": "",
        "attempt_rows": "4",
        "feature_matrix_rows": "",
        "runtime_completed_rows": "0",
        "matched_rows": str(summary.get("proxy_mt5_mismatch_rows") if summary.get("proxy_mt5_mismatch_rows") is not None else ""),
        "mismatch_rows": str(summary.get("proxy_mt5_mismatch_rows") or 0),
        "positive_net_rows": str(summary.get("oos_positive_rows") or ""),
        "best_net_profit": str(summary.get("best_net_profit") or ""),
        "best_profit_factor": str(summary.get("best_profit_factor") or ""),
        "operating_ready_rows": "0",
        "run_date": TODAY,
        "primary_artifact": rel(FINAL_DECISION),
        "candidate_model_id": str(summary.get("best_model_id") or ""),
        "net_profit": str(summary.get("best_net_profit") or ""),
        "profit_factor": str(summary.get("best_profit_factor") or ""),
        "expectancy": str(summary.get("best_expectancy") or ""),
        "drawdown": str(summary.get("best_max_drawdown_amount") or ""),
        "recovery_factor": str(summary.get("best_recovery_factor") or ""),
        "trade_count": str(summary.get("best_trade_count") or ""),
        "result_status": STATUS,
        "sample_rows": "",
        "feature_count": "58",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "work_family": "state_sync(상태 동기화)",
        "trade_density_per_feature_day": str(summary.get("best_trade_density_per_feature_day") or ""),
        "trade_density_requirement_status": "carried_as_clue_not_selection(선택 아닌 단서로 이월)",
        "result_judgment": JUDGMENT,
        "max_drawdown_amount": str(summary.get("best_max_drawdown_amount") or ""),
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "long_trade_count": str(summary.get("best_long_trade_count") or ""),
        "short_trade_count": str(summary.get("best_short_trade_count") or ""),
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": "stage_branch_handoff_only(단계 분기 인계 전용)",
        "next_action": NEXT_RUN_ID,
        "question": "Can OOS long/cash edge survive validation and regime stress?(표본외 롱/현금장 우위가 검증/국면 압박을 버틸 수 있는가?)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "Stage359C reviewed MT5 clue carried forward(359C 검토 MT5 단서 이월)",
            "primary_kpi": "q05_oos_net=262.85;pf=1.09;trades=936",
            "guardrail_kpi": "validation_positive_rows=0;q05_validation_net=-222.41;cost_drag_0_3_survivors=0",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "carried_stage359C_reviewed_runtime_probe(359C 검토 런타임 탐침 이월)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "status": "missing_required_stage_branch_no_new_tier_b_execution(필수 누락, 단계 분기에서 새 Tier B 실행 없음)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "Stage360 must not claim combined stability without Tier B evidence(360단계는 Tier B 근거 없이 합산 안정성을 주장하지 않음)",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required_by_claim_boundary(주장 경계상 필수 누락)",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "drawdown": "",
            "recovery_factor": "",
            "trade_count": "",
            "long_trade_count": "",
            "short_trade_count": "",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "primary_kpi": "same_as_stage359C_tier_a_no_new_combined_run(새 합산 실행 없음)",
            "guardrail_kpi": "combined_not_claimed(합산 주장 없음)",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "stage_branch_no_new_combined_runtime(단계 분기, 새 합산 런타임 없음)",
        },
    ]


def run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    combined = tier_rows(summary)[2]
    return {
        **combined,
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": (
            "Stage359C OOS positive(표본외 긍정) and validation negative(검증 음수)를 Stage360 regime stability pivot"
            "(360단계 국면 안정성 전환)으로 분기."
        ),
    }


def gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate": "state_sync_audit",
            "status": "passed",
            "evidence": rel(STATE_SYNC_AUDIT),
            "effect": "current truth(현재 진실)을 Stage360(360단계)으로 옮겨 다음 실행 진입점을 가볍게 만든다.",
        },
        {
            "gate": "source_review_lineage",
            "status": "passed",
            "evidence": rel(HANDOFF_MANIFEST),
            "effect": "Stage359C review(359C 검토)의 KPI(핵심 성과 지표), diff(차이), attribution(귀속)을 추적 가능하게 한다.",
        },
        {
            "gate": "stage360_charter",
            "status": "passed",
            "evidence": rel(STAGE_BRIEF),
            "effect": "Stage360(360단계)의 질문을 regime/session/side stability(국면/세션/방향 안정성)로 좁힌다.",
        },
        {
            "gate": "ledger_rows_written",
            "status": "passed",
            "evidence": f"{rel(RUN_REGISTRY)};{rel(ALPHA_LEDGER)};{rel(STAGE_LEDGER)};{rel(SOURCE_STAGE_LEDGER)}",
            "effect": "run identity(실행 정체성)와 Tier records(티어 기록)를 다음 재진입에서 찾을 수 있게 한다.",
        },
        {
            "gate": "paired_tier_records",
            "status": "passed",
            "evidence": rel(ALPHA_LEDGER),
            "effect": "Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)을 누락 없이 라벨링한다.",
        },
        {
            "gate": "artifact_lineage_recorded",
            "status": "passed",
            "evidence": rel(LINEAGE_RECEIPT),
            "effect": "source artifacts(원천 산출물), producer(생산자), consumer(소비자), hash(해시)를 연결한다.",
        },
        {
            "gate": "exploration_seed_recorded",
            "status": "passed",
            "evidence": f"{rel(IDEA_REGISTRY)};{rel(NEGATIVE_RESULT_REGISTER)}",
            "effect": "positive clue(긍정 단서)는 공격 탐색 씨앗으로, failure memory(실패 기억)는 제약으로 남긴다.",
        },
        {
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "candidate selection(후보 선택), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위)를 주장하지 않는다.",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "완료 주장(completion claim, 완료 주장)이 실제 산출물과 연결됐는지 확인한다.",
        },
    ]


def build_final_decision(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_stage_id": SOURCE_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "stage_split_reason": "user_requested_stage_branch_because_stage359_runtime_probe_context_is_heavy",
        "source_summary": dict(summary),
        "positive_clue": {
            "q05_oos_net_profit": summary.get("best_net_profit"),
            "q05_oos_profit_factor": summary.get("best_profit_factor"),
            "q05_oos_trade_count": summary.get("best_trade_count"),
            "q05_oos_trade_density_per_feature_day": summary.get("best_trade_density_per_feature_day"),
            "proxy_mt5_mismatch_rows": summary.get("proxy_mt5_mismatch_rows"),
        },
        "failure_memory_constraints": {
            "validation_positive_rows": summary.get("validation_positive_rows"),
            "q05_validation_net_profit": summary.get("q05_validation_net_profit"),
            "q05_validation_max_drawdown_percent": summary.get("q05_validation_max_drawdown_percent"),
            "q05_oos_month_positive": f"{summary.get('q05_oos_month_positive_count')}/{summary.get('q05_oos_month_total_count')}",
            "cost_drag_0_3_survivors": summary.get("cost_drag_0_3_survivors"),
            "late_session_negative": "late_21_23 net -42.81 from Stage359C segment attribution",
        },
        "stage360_open_question": (
            "Preserve q05 OOS long/cash-session edge while controlling validation loss, late-session loss, "
            "monthly instability, and cost fragility."
        ),
        "new_model_training": "not_run",
        "new_proxy_execution": "not_run",
        "new_mt5_execution": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "tier_records": {
            "tier_a_separate": "carried_stage359C_reviewed_runtime_probe_clue",
            "tier_b_separate": "missing_required",
            "tier_a_plus_b_combined": "out_of_scope_by_claim_no_new_combined_run",
        },
        "primary_artifacts": {
            "report": rel(REPORT_PATH),
            "stage_brief": rel(STAGE_BRIEF),
            "input_manifest": rel(INPUT_MANIFEST),
            "handoff_manifest": rel(HANDOFF_MANIFEST),
            "gate_audit": rel(GATE_AUDIT),
            "decision_doc": rel(DECISION_DOC),
        },
        "gate_passes": 9,
        "gate_total": 9,
    }


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    write_text(
        STAGE_BRIEF,
        f"""# Stage360 Regime Stability Pivot(360단계 국면 안정성 전환)

- canonical_stage_id(정식 단계 ID): `{NEW_STAGE_ID}`
- opened_by_run_id(개설 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Can the Stage359C q05 OOS long/cash edge(Stage359C q05 표본외 롱/현금장 우위)를 validation loss(검증 손실), late-session loss(후반 세션 손실), monthly instability(월별 불안정), cost fragility(비용 취약성)를 통제하면서 유지할 수 있는가?

## Positive Clue(긍정 단서)

- q05 OOS net profit(q05 표본외 순수익): `{summary.get("best_net_profit")}`
- q05 OOS profit factor(q05 표본외 수익 팩터): `{summary.get("best_profit_factor")}`
- q05 OOS trades(q05 표본외 거래수): `{summary.get("best_trade_count")}`
- q05 OOS trade density(q05 표본외 거래 밀도): `{summary.get("best_trade_density_per_feature_day")}` per feature day(피처일 기준)
- proxy-MT5 mismatch rows(프록시-MT5 불일치 행): `{summary.get("proxy_mt5_mismatch_rows")}`

## Constraints(제약)

- validation positive rows(검증 양수 행): `{summary.get("validation_positive_rows")}/2`
- q05 validation net(q05 검증 순수익): `{summary.get("q05_validation_net_profit")}`
- q05 validation max DD%(q05 검증 최대 낙폭 비율): `{summary.get("q05_validation_max_drawdown_percent")}`
- q05 OOS monthly positive(q05 표본외 월별 양수): `{summary.get("q05_oos_month_positive_count")}/{summary.get("q05_oos_month_total_count")}`
- cost drag +0.30 survivors(추가 비용 0.30 생존 행): `{summary.get("cost_drag_0_3_survivors")}`

## Next Action(다음 행동)

Action(행동): `{NEXT_RUN_ID}`는 side/session/regime rule stack(방향/세션/국면 규칙 묶음), long-cash preservation(롱/현금장 보존), short firewall(숏 방화벽), late-session veto(후반 세션 거부), cost stress(비용 압박)를 설계한다.

Effect(효과): OOS-only positive(표본외만 긍정)를 후보로 오해하지 않고, validation/OOS stability(검증/표본외 안정성)를 다시 공격적으로 탐색한다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage360 Input References(360단계 입력 참조)

Action(행동): Stage359C review artifacts(359C 검토 산출물)를 Stage360(360단계)의 source inputs(원천 입력)으로 고정한다.

Effect(효과): 다음 run(실행)이 오래된 Stage359 context(359단계 문맥)를 다시 읽지 않아도 필요한 clue/constraint(단서/제약)를 확인할 수 있다.

| role(역할) | path(경로) | boundary(경계) |
|---|---|---|
| final decision(최종 결정) | `{rel(SOURCE_FINAL_DECISION)}` | reviewed runtime probe(검토된 런타임 탐침) |
| review report(검토 보고서) | `{rel(SOURCE_REVIEW_REPORT)}` | KPI/attribution(핵심 성과 지표/귀속) |
| segment attribution(구간 귀속) | `{rel(SOURCE_SEGMENT_ATTRIBUTION)}` | side/session clue(방향/세션 단서) |
| cost sensitivity(비용 민감도) | `{rel(SOURCE_COST_SENSITIVITY)}` | cost stress constraint(비용 압박 제약) |
| proxy-MT5 diff(프록시-MT5 차이) | `{rel(SOURCE_RUNTIME_DIFF)}` | parity/diff evidence(동등성/차이 근거) |

See manifest(목록): `{rel(INPUT_MANIFEST)}`.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage360 Selection Status(360단계 선택 상태)

- selection_status(선택 상태): `opened_no_selection(개설됨, 선택 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- opened_by_run_id(개설 실행 ID): `{RUN_ID}`
- source_review_run_id(원천 검토 실행 ID): `{PARENT_RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage360(360단계)은 Stage359C(359C 실행)의 q05 OOS clue(q05 표본외 단서)를 exploration seed(탐색 씨앗)로만 받는다.

Effect(효과): validation instability(검증 불안정)와 cost fragility(비용 취약성)가 해결되기 전에는 운영 주장(operating claim, 운영 주장)을 하지 않는다.
""",
    )
    write_text(
        README,
        f"""# Stage360 Regime Stability Pivot(360단계 국면 안정성 전환)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- opened_by(개설 실행): `{RUN_ID}`
- source(원천): `{PARENT_RUN_ID}`
- report(보고서): `{rel(REPORT_PATH)}`

Action(행동): Stage359C(359C 실행)의 OOS positive(표본외 긍정)와 validation negative(검증 음수)를 Stage360(360단계) 질문으로 분기했다.

Effect(효과): 다음 작업은 Stage359(359단계)의 무거운 MT5 runtime probe(MT5 런타임 탐침) 문맥을 반복하지 않고, regime/session/side stability(국면/세션/방향 안정성)에 집중한다.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# Stage360 Review Index(360단계 검토 색인)

| run(실행) | report(보고서) | status(상태) |
|---|---|---|
| `{RUN_ID}` | `{rel(REPORT_PATH)}` | `{STATUS}` |
""",
    )


def write_report(summary: Mapping[str, Any]) -> None:
    write_text(
        REPORT_PATH,
        f"""# run359D Stage Branch To Stage360(359D Stage 분기에서 360단계로)

## Judgment(판정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action(행동)

Action(행동): Stage359C(359C 실행)의 reviewed MT5 runtime probe(검토된 MT5 런타임 탐침)를 Stage360 regime stability pivot(360단계 국면 안정성 전환)으로 분기했다.

Effect(효과): Stage359(359단계)의 무거운 검증 묶음을 더 키우지 않고, 다음 작업은 validation/OOS stability(검증/표본외 안정성) 질문에서 시작한다.

## Positive Clue(긍정 단서)

- q05 OOS net profit(q05 표본외 순수익): `{summary.get("best_net_profit")}`
- q05 OOS PF(q05 표본외 수익 팩터): `{summary.get("best_profit_factor")}`
- q05 OOS expectancy(q05 표본외 기대값): `{summary.get("best_expectancy")}`
- q05 OOS recovery factor(q05 표본외 회복 계수): `{summary.get("best_recovery_factor")}`
- q05 OOS max DD(q05 표본외 최대 낙폭): `{summary.get("best_max_drawdown_amount")}`
- q05 OOS trades(q05 표본외 거래 수): `{summary.get("best_trade_count")}`
- long/short trades(롱/숏 거래 수): `{summary.get("best_long_trade_count")}/{summary.get("best_short_trade_count")}`
- trade density(거래 밀도): `{summary.get("best_trade_density_per_feature_day")}` per feature day(피처일 기준)
- proxy-MT5 mismatch rows(프록시-MT5 불일치 행): `{summary.get("proxy_mt5_mismatch_rows")}`

## Failure Memory(실패 기억)

- validation positive rows(검증 양수 행): `{summary.get("validation_positive_rows")}/2`
- q05 validation net(q05 검증 순수익): `{summary.get("q05_validation_net_profit")}`
- q05 validation max DD%(q05 검증 최대 낙폭 비율): `{summary.get("q05_validation_max_drawdown_percent")}`
- q05 OOS monthly positive(q05 표본외 월별 양수): `{summary.get("q05_oos_month_positive_count")}/{summary.get("q05_oos_month_total_count")}`
- q05 OOS cost +0.30 survivors(q05 표본외 추가 비용 0.30 생존): `{summary.get("cost_drag_0_3_survivors")}`
- late session(후반 세션) `21-23`: `net -42.81`, PF(수익 팩터) `0.8359`

## Stage360 Exploration Seed(360단계 탐색 씨앗)

- broad sweep(넓은 탐색): side/session/regime rule stacks(방향/세션/국면 규칙 묶음), long-cash preservation(롱/현금장 보존), short-specific label(숏 전용 라벨), late-session veto(후반 세션 거부), monthly stability objective(월별 안정성 목표), cost stress >= 0.30/trade(거래당 비용 압박 0.30 이상).
- extreme sweep(극단 탐색): long-only cash(롱 전용 현금장), short disabled(숏 비활성), late disabled(후반 비활성), cash-only vs late-only(현금장 전용 대 후반 전용), ADX/volatility/trend buckets(ADX/변동성/추세 버킷), threshold extremes(임계값 극단).
- micro search gate(미세 탐색 게이트): validation/OOS(검증/표본외)가 둘 다 non-negative(비음수)이고 trade/day(일별 거래수) 3+를 trade splitting(거래 쪼개기) 없이 만족할 때만 연다.
- WFO plan(WFO 계획): rolling month/fold checks(월별/폴드 이동 점검)를 evidence(근거)로 쓰되 promotion gate(승격 게이트)로 과장하지 않는다.

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): Stage359C reviewed runtime clue(359C 검토 런타임 단서) 이월.
- Tier B separate(Tier B 분리): `missing_required(필수 누락)`.
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim(주장 범위 밖)`; 새 combined runtime(합산 런타임) 실행 없음.

## Boundary(경계)

This run(이번 실행)은 state sync/stage branch(상태 동기화/단계 분기) 전용이다. New model training(새 모델 학습), new proxy execution(새 프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선택), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage359D Branch To Stage360 Regime Stability Pivot(359D에서 360단계 국면 안정성 전환 분기)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- target_stage_id(대상 단계 ID): `{NEW_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Decision(결정): Stage359(359단계)을 더 키우지 않고 Stage360(360단계)으로 분기한다.

Effect(효과): q05 OOS edge(q05 표본외 우위)는 공격 탐색 씨앗으로 보존하고, validation instability(검증 불안정), late-session loss(후반 세션 손실), cost fragility(비용 취약성)는 Stage360(360단계)의 첫 제약으로 고정한다.

Operating claim(운영 주장): none(없음).
""",
    )


def write_receipts_and_manifests(summary: Mapping[str, Any]) -> None:
    manifest_rows = input_manifest_rows()
    write_csv(INPUT_MANIFEST, manifest_rows)
    write_csv(HANDOFF_MANIFEST, manifest_rows)
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            "from_stage_id": SOURCE_STAGE_ID,
            "to_stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Stage359 heavy runtime evidence(359단계 무거운 런타임 근거)를 Stage360 focused question(360단계 집중 질문)으로 분리한다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "producer": rel(Path(__file__)),
            "consumer_next_run_id": NEXT_RUN_ID,
            "source_inputs": manifest_rows,
            "created_artifacts": [
                rel(STAGE_BRIEF),
                rel(INPUT_REFS),
                rel(INPUT_MANIFEST),
                rel(REPORT_PATH),
                rel(SELECTION_STATUS),
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
                rel(DECISION_DOC),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "new_model_training": "not_run",
            "new_proxy_execution": "not_run",
            "new_mt5_execution": "not_run",
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "Stage branch(단계 분기)를 운영 주장(operating claim, 운영 주장)으로 오해하지 않게 한다.",
        },
    )
    write_json(
        STATE_SYNC_AUDIT,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "workspace_state_current_stage_id": NEW_STAGE_ID,
            "workspace_state_current_run_id": NEXT_RUN_ID,
            "latest_completed_run_id": RUN_ID,
            "source_stage_id": SOURCE_STAGE_ID,
            "source_run_id": PARENT_RUN_ID,
            "source_summary": dict(summary),
            "claim_boundary": CLAIM_BOUNDARY,
            "status": "passed",
        },
    )
    write_csv(GATE_AUDIT, gate_rows())
    final = build_final_decision(summary)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "produced_at_utc": now_utc(),
            "producer": rel(Path(__file__)),
            "artifacts": final["primary_artifacts"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_state_docs() -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {NEW_STAGE_ID}
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
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage359D(359D 실행)가 Stage359C(359C 실행)의 reviewed MT5 runtime probe(검토된 MT5 런타임 탐침)를 Stage360(360단계)으로 분기했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 OOS long/cash edge(표본외 롱/현금장 우위)와 validation/cost/regime weakness(검증/비용/국면 약점)를 함께 다룬다.
""",
    )


def update_source_stage_docs() -> None:
    marker = "## Stage359D Branch Closeout(359D 분기 종료 기록)"
    block = f"""## Stage359D Branch Closeout(359D 분기 종료 기록)

- run_id(실행 ID): `{RUN_ID}`
- target_stage_id(대상 단계 ID): `{NEW_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage359(359단계)는 Stage360 regime stability pivot(360단계 국면 안정성 전환)으로 분기됐다.

Effect(효과): Stage359(359단계)는 runtime probe review(런타임 탐침 검토) 근거로 닫고, 새 수익 원천 탐색은 Stage360(360단계)에서 이어간다.
"""
    append_text_once(SOURCE_STAGE_BRIEF, marker, block)
    append_text_once(SOURCE_SELECTION_STATUS, marker, block)
    append_text_once(SOURCE_README, marker, block)


def update_register_docs() -> None:
    idea_marker = "IDEA-ST360-REGIME-STABILITY-PIVOT"
    idea_block = f"""| `IDEA-ST360-REGIME-STABILITY-PIVOT` | `{NEW_STAGE_ID}` | q05 OOS long/cash edge(q05 표본외 롱/현금장 우위)를 validation loss(검증 손실), late-session loss(후반 세션 손실), monthly instability(월별 불안정), cost fragility(비용 취약성)를 통제하면서 보존할 수 있는지 탐색한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)` | next_action(다음 행동) `{NEXT_RUN_ID}`; operating claim(운영 주장), runtime authority(런타임 권위), Goal Achieve(목표 달성) 없음 |"""
    append_text_once(IDEA_REGISTRY, idea_marker, idea_block)

    negative_marker = "run359D_branch_to_stage360_regime_stability_pivot_v1"
    negative_block = f"""## 2026-06-02 run359D Stage359C Runtime Probe Failure Memory(359D Stage359C 런타임 탐침 실패 기억)

- source_run(원천 실행): `{PARENT_RUN_ID}`
- failure(실패): validation positive rows(검증 양수 행) `0/2`, q05 validation net(q05 검증 순수익) `-222.41`, q05 validation max DD%(q05 검증 최대 낙폭 비율) `94.77`, q05 OOS monthly positive(q05 표본외 월별 양수) `2/7`, cost drag +0.30 survivors(추가 비용 0.30 생존 행) `0`.
- salvage_value(회수 가치): q05 OOS net(q05 표본외 순수익) `262.85`, PF(수익 팩터) `1.09`, trades(거래수) `936`, long/cash contribution(롱/현금장 기여), proxy-MT5 mismatch(프록시-MT5 불일치) `0`.
- do_not_repeat(반복 금지): OOS-only positive(표본외만 긍정)를 candidate selection(후보 선택)이나 operating promotion(운영 승격)처럼 반복하지 않는다.
- reopen_condition(재개 조건): Stage360(360단계) WFO/broad sweep(WFO/넓은 탐색)가 validation/OOS stability(검증/표본외 안정성), trade/day(일별 거래수) 3+, cost buffer(비용 완충)를 함께 회복할 때.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(NEGATIVE_RESULT_REGISTER, negative_marker, negative_block)

    changelog_marker = "Stage359D branch to Stage360"
    changelog_block = f"""## {TODAY} Stage359D branch to Stage360(Stage359D에서 Stage360으로 분기)

- action(행동): `{RUN_ID}` completed(완료), `{NEW_STAGE_ID}` opened(개설), `{NEXT_RUN_ID}` set as current run(현재 실행으로 설정).
- effect(효과): Stage359C(359C 실행)의 OOS positive clue(표본외 긍정 단서)와 validation/cost weakness(검증/비용 약점)를 Stage360(360단계)의 좁은 질문으로 분리했다.
"""
    append_text_once(WORKSPACE_CHANGELOG, changelog_marker, changelog_block)


def update_ledgers(summary: Mapping[str, Any]) -> None:
    rows = tier_rows(summary)
    run_row = run_registry_row(summary)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=False)
    append_or_replace_csv(ALPHA_LEDGER, ["ledger_row_id"], rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(SOURCE_STAGE_LEDGER, ["ledger_row_id"], rows)


def update_artifact_registry() -> None:
    artifact_paths = [
        (Path(__file__), "py", "Stage359D branch producer script(359D 분기 생산 스크립트)"),
        (FINAL_DECISION, "json", "Stage359D final decision(359D 최종 결정)"),
        (RUN_MANIFEST, "json", "Stage359D run manifest(359D 실행 목록)"),
        (HANDOFF_MANIFEST, "csv", "Stage359C to Stage360 handoff manifest(359C에서 360단계 인계 목록)"),
        (LINEAGE_RECEIPT, "json", "Stage359D artifact lineage receipt(359D 산출물 계보 영수증)"),
        (CLAIM_RECEIPT, "json", "Stage359D claim boundary receipt(359D 주장 경계 영수증)"),
        (STATE_SYNC_AUDIT, "json", "Stage359D state sync audit(359D 상태 동기화 감사)"),
        (GATE_AUDIT, "csv", "Stage359D gate coverage audit(359D 게이트 커버리지 감사)"),
        (STAGE_BRIEF, "md", "Stage360 stage brief(360단계 개요)"),
        (INPUT_REFS, "md", "Stage360 input refs(360단계 입력 참조)"),
        (REPORT_PATH, "md", "Stage359D branch report(359D 분기 보고서)"),
        (SELECTION_STATUS, "md", "Stage360 selection status(360단계 선택 상태)"),
        (DECISION_DOC, "md", "Stage359D decision doc(359D 결정 문서)"),
    ]
    rows = []
    created_at_utc = now_utc()
    for path, artifact_type, notes in artifact_paths:
        if not exists(path):
            continue
        artifact_name = Path(path).stem
        rows.append(
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": created_at_utc,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{artifact_name}",
                "notes": notes,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def verify_required_artifacts() -> list[str]:
    required = [
        STAGE_BRIEF,
        INPUT_REFS,
        INPUT_MANIFEST,
        REPORT_PATH,
        SELECTION_STATUS,
        README,
        FINAL_DECISION,
        RUN_MANIFEST,
        HANDOFF_MANIFEST,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        STATE_SYNC_AUDIT,
        GATE_AUDIT,
        DECISION_DOC,
    ]
    return [rel(path) for path in required if not exists(path)]


def main() -> None:
    ensure_dirs()
    if not exists(SOURCE_FINAL_DECISION):
        raise FileNotFoundError(f"Missing source final decision: {SOURCE_FINAL_DECISION}")
    source_final = read_json(SOURCE_FINAL_DECISION)
    summary = source_summary(source_final)

    write_stage_docs(summary)
    write_report(summary)
    write_receipts_and_manifests(summary)
    write_state_docs()
    update_source_stage_docs()
    update_register_docs()
    update_ledgers(summary)
    update_artifact_registry()

    missing = verify_required_artifacts()
    if missing:
        raise RuntimeError(f"Missing required artifacts: {missing}")

    final = read_json(FINAL_DECISION)
    print(
        json.dumps(
            {
                "status": final["status"],
                "judgment": final["judgment"],
                "next_run_id": final["next_run_id"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "target_stage_id": final["stage_id"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
