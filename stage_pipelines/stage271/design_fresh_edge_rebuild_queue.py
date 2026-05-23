from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
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


STAGE270_ID = "270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe"
STAGE271_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
RUN_ID = "run271A_design_fresh_edge_rebuild_queue_v1"
NEXT_ACTION = "run271B_materialize_fresh_edge_rebuild_blueprints"
STATUS = "completed_fresh_edge_rebuild_queue_design_no_candidate_selection"
JUDGMENT = "exploratory_design_queue_ready_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE270_ROOT = ROOT / "stages" / STAGE270_ID
STAGE271_ROOT = ROOT / "stages" / STAGE271_ID
RUN_DIR = STAGE271_ROOT / "02_runs" / "run271A"
REVIEWS = STAGE271_ROOT / "03_reviews"
SELECTED = STAGE271_ROOT / "04_selected"

RUN270D_ROOT = STAGE270_ROOT / "02_runs" / "run270D"
RUN270D_VARIANT_SUMMARY = RUN270D_ROOT / "variant_summary.csv"
RUN270D_NEGATIVE_SLICES = RUN270D_ROOT / "negative_slice_summary.csv"
RUN270D_TIER_DUPLICATE = RUN270D_ROOT / "tier_duplicate_review.csv"
RUN270D_REVIEW_RESULT = RUN270D_ROOT / "review_result.json"
RUN270D_REPORT = STAGE270_ROOT / "03_reviews" / "run270D_report.md"
STAGE270_CLOSEOUT = STAGE270_ROOT / "03_reviews" / "stage270_closeout_stage271_fresh_thesis_handoff.md"
STAGE271_BRIEF = STAGE271_ROOT / "00_spec" / "stage_brief.md"

PACKAGE_QUEUE = RUN_DIR / "fresh_edge_rebuild_package_queue.csv"
FAILURE_MEMORY_MAP = RUN_DIR / "failure_memory_map.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RUN_REPORT = REVIEWS / "run271A_report.md"
SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = Path("stage_pipelines/stage271/design_fresh_edge_rebuild_queue.py")

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
PACKAGE_COLUMNS = (
    "package_id",
    "queue_role",
    "fresh_thesis",
    "feature_surface",
    "scoring_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "upside_condition",
    "failure_condition",
    "discard_condition",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "source_failure_memory",
    "next_use",
)
FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "axis",
    "bucket",
    "split_set",
    "tier_scope_set",
    "variant_count",
    "source_variants",
    "slice_count",
    "total_negative_net",
    "min_slice_net",
    "max_drawdown_percent_max",
    "primary_interpretation",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_stage_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def load_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return dict(json.load(handle))


def fnum(value: str) -> float:
    text = str(value or "").strip()
    return float(text) if text else 0.0


def aggregate_failure_memory(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "splits": set(),
            "tiers": set(),
            "variants": set(),
            "slice_count": 0,
            "total_negative_net": 0.0,
            "min_slice_net": 0.0,
            "max_drawdown_percent_max": 0.0,
        }
    )
    for row in rows:
        net = fnum(row.get("net_profit", "0"))
        if net >= 0:
            continue
        key = (str(row.get("axis", "")).strip(), str(row.get("bucket", "")).strip())
        item = grouped[key]
        item["splits"].add(str(row.get("split", "")).strip())
        item["tiers"].add(str(row.get("tier_scope", "")).strip())
        item["variants"].add(str(row.get("variant_id", "")).strip())
        item["slice_count"] += 1
        item["total_negative_net"] += net
        item["min_slice_net"] = min(float(item["min_slice_net"]), net)
        item["max_drawdown_percent_max"] = max(
            float(item["max_drawdown_percent_max"]),
            fnum(row.get("closed_balance_max_drawdown_percent", "0")),
        )

    ranked = sorted(grouped.items(), key=lambda item: (item[1]["total_negative_net"], item[1]["min_slice_net"]))
    output: list[dict[str, Any]] = []
    for index, ((axis, bucket), item) in enumerate(ranked[:14], start=1):
        variants = sorted(v for v in item["variants"] if v)
        if axis == "weekday" and bucket == "Thursday":
            interpretation = "time_risk_weekday_damage"
        elif axis == "month" and bucket == "2025-11":
            interpretation = "calendar_regime_damage"
        elif axis == "chron_segment" and bucket == "chron_early":
            interpretation = "early_sequence_loss_concentration"
        elif axis == "direction" and bucket == "buy":
            interpretation = "side_specific_loss_pressure"
        elif axis == "session_report":
            interpretation = "session_time_risk_pressure"
        else:
            interpretation = "general_negative_slice_memory"
        output.append(
            {
                "memory_id": f"FM271A-{index:02d}",
                "axis": axis,
                "bucket": bucket,
                "split_set": "|".join(sorted(s for s in item["splits"] if s)),
                "tier_scope_set": "|".join(sorted(s for s in item["tiers"] if s)),
                "variant_count": len(variants),
                "source_variants": "|".join(variants),
                "slice_count": item["slice_count"],
                "total_negative_net": round(float(item["total_negative_net"]), 2),
                "min_slice_net": round(float(item["min_slice_net"]), 2),
                "max_drawdown_percent_max": round(float(item["max_drawdown_percent_max"]), 6),
                "primary_interpretation": interpretation,
            }
        )
    return output


def package_queue(memory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    memory_index = {str(row["primary_interpretation"]): str(row["memory_id"]) for row in memory}
    thursday = memory_index.get("time_risk_weekday_damage", "FM271A-01")
    november = memory_index.get("calendar_regime_damage", "FM271A-02")
    early = memory_index.get("early_sequence_loss_concentration", "FM271A-03")
    side = memory_index.get("side_specific_loss_pressure", "FM271A-04")
    session = memory_index.get("session_time_risk_pressure", "FM271A-05")
    paired_scope = "Tier A separate(티어 A 분리), Tier B separate(티어 B 분리), Tier A+B combined(티어 A+B 합산) planned with mirror-boundary receipt(거울 경계 영수증)"
    controls = "symbol=US100;timeframe=M5;broker=FPMarkets;Stage270 MT5 cost/deposit/leverage contract preserved;no Stage270 candidate inheritance"
    evidence = "design receipt;data integrity receipt;model validation receipt;artifact lineage receipt;run271B blueprint materialization;later MT5/ONNX only after package gate"
    return [
        {
            "package_id": "cp271A_damage_first_loss_asymmetry_surface",
            "queue_role": "selectable_fresh_candidate_seed",
            "fresh_thesis": "damage-first loss-asymmetry(손상 우선 손실 비대칭)로 이익 꼬리가 아니라 깨지는 구간을 먼저 분리한다",
            "feature_surface": "loss_pressure_state;recent_negative_expectancy;side_specific_damage;weak_slice_overlap",
            "scoring_surface": "damage_risk_score(손상 위험 점수) plus opportunity_score(기회 점수);rank_only_not_probability(확률 아님)",
            "decision_surface": "opportunity_score high and damage_risk_score low;hard skip when damage state is active",
            "risk_logic": "damage_budget_skip(손상 예산 스킵);loss-streak cooloff(손실 연속 냉각);side-specific exposure cap(방향별 노출 제한)",
            "adapter_path": "stage271 adapter blueprint first; promote reusable feature logic to foundation/features only after repeated use",
            "runtime_handoff": "planned compact handoff with feature_order_hash, decision_rule_hash, risk_rule_hash",
            "comparison_baseline": "q03 preserved clue(보존 단서) and q01 control reference(대조 참고) only",
            "control_variables": controls,
            "changed_variables": "new damage-risk feature surface;new decision rule;new risk skip budget",
            "sample_scope": paired_scope,
            "upside_condition": "validation/OOS both avoid deep negative damage slices while keeping enough trade supply for MT5 probe",
            "failure_condition": "damage skip collapses supply or repeats q03/q01 Thursday/2025-11/chron_early losses",
            "discard_condition": "no separate improvement over q03 clue in weak-slice map or any fatal Tier A/B mismatch",
            "invalid_conditions": "feature_label leakage;timestamp ordering ambiguity;missing Tier A/B boundary;untraceable feature order",
            "stop_conditions": "stop after two materialized branches without weak-slice improvement; open new stage if question changes",
            "evidence_plan": evidence,
            "source_failure_memory": "|".join([thursday, november, early, side]),
            "next_use": "run271B_blueprint_materialization",
        },
        {
            "package_id": "cp271B_time_risk_phase_router_surface",
            "queue_role": "selectable_fresh_candidate_seed",
            "fresh_thesis": "time-risk phase router(시간 위험 국면 라우터)로 요일/월/세션 손상을 동일 필터가 아니라 상태별 의사결정으로 다룬다",
            "feature_surface": "weekday_phase;month_regime_pressure;session_clock_risk;chron_phase_age",
            "scoring_surface": "phase_risk_score(국면 위험 점수) plus phase_opportunity_score(국면 기회 점수);rank_only_not_probability(확률 아님)",
            "decision_surface": "route or abstain by time-risk phase;do not widen supply inside damaged phases",
            "risk_logic": "phase-specific lot cap(국면별 랏 제한);Thursday/2025-11 guardrail(목요일/2025-11 방어선);session risk cooloff(세션 위험 냉각)",
            "adapter_path": "stage271 router blueprint;runtime handoff keeps phase fields explicit",
            "runtime_handoff": "planned phase_id, phase_score, action_code, reject_reason fields",
            "comparison_baseline": "Stage270 q02/q03/q05 active probes as failure memory, not candidate baselines",
            "control_variables": controls,
            "changed_variables": "new time-phase routing surface;new abstention path;new phase risk cap",
            "sample_scope": paired_scope,
            "upside_condition": "same broad sample shows reduced Thursday/month/session damage without all-skip behavior",
            "failure_condition": "router becomes calendar blacklist only or fails outside the known weak buckets",
            "discard_condition": "weak-bucket improvement is offset by worse neutral buckets or trade count collapse",
            "invalid_conditions": "calendar feature uses future month boundary;report-time/session timezone not named;missing route counts",
            "stop_conditions": "stop if route/skip counts cannot be attributed by phase in run271B/run271C",
            "evidence_plan": evidence,
            "source_failure_memory": "|".join([thursday, november, session, early]),
            "next_use": "run271B_blueprint_materialization",
        },
        {
            "package_id": "cp271C_recovery_tail_payoff_rebalance_surface",
            "queue_role": "selectable_fresh_candidate_seed",
            "fresh_thesis": "recovery-tail payoff rebalance(회복-꼬리 보상 재균형)로 tail reward(꼬리 보상) 극단화가 아니라 손실 회복 형태를 재설계한다",
            "feature_surface": "payoff_balance_state;expected_recovery_pressure;drawdown_slope_state;thin_tail_warning",
            "scoring_surface": "recovery_quality_score(회복 품질 점수) plus payoff_fragility_score(보상 취약성 점수);rank_only_not_probability(확률 아님)",
            "decision_surface": "accept only when recovery_quality_score covers payoff fragility;reject extreme thin-tail contexts",
            "risk_logic": "bounded reward target(경계 보상 목표);drawdown-slope abort(손실폭 기울기 중단);expectancy guard(기대값 방어)",
            "adapter_path": "stage271 payoff blueprint;later Adapter package must expose risk_rule_hash",
            "runtime_handoff": "planned target_bucket, recovery_score, payoff_fragility_score, risk_action fields",
            "comparison_baseline": "q04 tail reward extreme(꼬리 보상 극단) failure memory and q03 preserved clue",
            "control_variables": controls,
            "changed_variables": "new recovery/payoff shape surface;new bounded target logic;new drawdown-slope risk action",
            "sample_scope": paired_scope,
            "upside_condition": "OOS net and PF improve without validation DD exploding;weak slices shrink rather than move",
            "failure_condition": "tail payoff remains sparse, DD heavy, or monthly/weekday damage migrates",
            "discard_condition": "risk action removes upside or repeats q04 OOS negative profile",
            "invalid_conditions": "drawdown feature computed from future equity;untracked risk action;missing feature order hash",
            "stop_conditions": "stop if no branch produces materialized score table with traceable risk logic",
            "evidence_plan": evidence,
            "source_failure_memory": "|".join([november, thursday, early]),
            "next_use": "run271B_blueprint_materialization",
        },
        {
            "package_id": "cp271D_stage270_reference_control_boundary",
            "queue_role": "support_control_reference_only",
            "fresh_thesis": "control boundary(대조 경계)는 새 후보가 Stage270(270단계) 비필터 분기를 이름만 바꿔 복사하지 않았는지 확인한다",
            "feature_surface": "Stage270 q01/q03 source fields only as reference, not new candidate feature owner",
            "scoring_surface": "reference-only score comparison(참고 전용 점수 비교);not selectable(선택 불가)",
            "decision_surface": "no candidate decision;used for difference audit(차이 감사)",
            "risk_logic": "no runtime risk logic;reference boundary only",
            "adapter_path": "no Adapter path;control receipt only",
            "runtime_handoff": "out_of_scope_by_claim(주장 범위 밖)",
            "comparison_baseline": "q01 positive control reference and q03 preserved clue",
            "control_variables": controls,
            "changed_variables": "none;reference audit only",
            "sample_scope": paired_scope,
            "upside_condition": "not_applicable_reference_control",
            "failure_condition": "if selectable branches are indistinguishable from q01/q03, mark design invalid",
            "discard_condition": "discard as candidate always; keep as control receipt",
            "invalid_conditions": "control used as selected candidate or ONNX readiness evidence",
            "stop_conditions": "stop control usage after blueprint difference audit is complete",
            "evidence_plan": evidence,
            "source_failure_memory": "q01_control_reference|q03_preserved_clue",
            "next_use": "run271B_difference_audit_control",
        },
    ]


def experiment_receipt(packages: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-model-validation(모델 검증)",
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-result-judgment(결과 판정)",
        ],
        "required_gate_coverage": {
            "work_packet_schema_lint": "covered_by_experiment_design_receipt",
            "final_claim_guard": BOUNDARY,
        },
        "package_designs": [
            {
                "package_id": row["package_id"],
                "hypothesis": row["fresh_thesis"],
                "decision_use": row["next_use"],
                "comparison_baseline": row["comparison_baseline"],
                "control_variables": row["control_variables"],
                "changed_variables": row["changed_variables"],
                "sample_scope": row["sample_scope"],
                "success_criteria": row["upside_condition"],
                "failure_criteria": row["failure_condition"],
                "invalid_conditions": row["invalid_conditions"],
                "stop_conditions": row["stop_conditions"],
                "evidence_plan": row["evidence_plan"],
            }
            for row in packages
        ],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def data_integrity_receipt(source_hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "data_source": {
            "variant_summary": rel(RUN270D_VARIANT_SUMMARY),
            "negative_slice_summary": rel(RUN270D_NEGATIVE_SLICES),
            "tier_duplicate_review": rel(RUN270D_TIER_DUPLICATE),
            "stage270_closeout": rel(STAGE270_CLOSEOUT),
        },
        "time_axis": "MT5 report time(메타트레이더5 보고 시간) from run270C/run270D; Stage271 design creates no new bars",
        "sample_scope": "US100 M5(US100 5분봉), Stage270 validation_is(검증 표본내) and OOS(표본외) failure memory, Tier A plus Tier B mirror-boundary receipt",
        "missing_or_duplicate_check": "run270D parser checks matched all 20 reports; Tier B rows are mirror structural replay, not fallback authority",
        "feature_label_boundary": "no new feature/label table is computed in run271A; future run271B must reject label/future columns before materialization",
        "split_boundary": "run270D validation_is and OOS are kept as source labels; no threshold is selected in run271A",
        "leakage_risk": "selection bias from designing around known weak slices; mitigated by marking this as exploratory design only",
        "data_hash_or_identity": dict(source_hashes),
        "integrity_judgment": "usable_with_boundary",
    }


def model_validation_receipt(packages: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "model_family": "planned scoring/adapter surfaces only; no trained model in run271A",
        "target_and_label": "future target not materialized in run271A; later branch must bind to existing label contracts before scoring",
        "split_method": "design uses Stage270 validation_is/OOS failure memory and plans Tier A/B paired materialization",
        "selection_metric": "none_selected; later screening must use trade supply, net profit, PF, DD, recovery, expectancy, and weak-slice damage together",
        "secondary_metrics": "trade_count, weak_month, weak_weekday, weak_session, chron_segment, drawdown slope, route counts",
        "threshold_policy": "planned thresholds only; no optimized threshold selected",
        "overfit_risk": "high because Stage271 starts from known Stage270 weak slices; must validate outside the named weak buckets",
        "calibration_risk": "scores are rank/surface scores, not calibrated probability",
        "comparison_baseline": [row["comparison_baseline"] for row in packages],
        "validation_judgment": "exploratory_design_only_no_candidate_selection",
    }


def result_rows() -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "package_queue;failure_memory_map;experiment_design_receipt;data_integrity_receipt;model_validation_receipt;artifact_lineage_receipt",
            "evidence_missing": "materialized score tables;MT5 runtime output;Adapter package;ONNX export/parity;MT5 runtime reproduction",
            "judgment_label": "exploratory_design",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "새 후보 패키지 대기열은 생겼지만 선택 후보(selected candidate, 선택 후보)는 아직 없다.",
        }
    ]


def next_use_label(value: Any) -> str:
    text = str(value)
    labels = {
        "run271B_blueprint_materialization": "`run271B_blueprint_materialization`(271B 청사진 물질화)",
        "run271B_difference_audit_control": "`run271B_difference_audit_control`(271B 차이 감사 대조)",
    }
    return labels.get(text, f"`{text}`(다음 사용)")


def manifest_payload(packages: Sequence[Mapping[str, Any]], memory_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE271_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": utc_now(),
        "source_inputs": {
            "stage270_closeout": rel(STAGE270_CLOSEOUT),
            "run270D_report": rel(RUN270D_REPORT),
            "run270D_variant_summary": rel(RUN270D_VARIANT_SUMMARY),
            "run270D_negative_slice_summary": rel(RUN270D_NEGATIVE_SLICES),
            "run270D_review_result": rel(RUN270D_REVIEW_RESULT),
            "stage271_brief": rel(STAGE271_BRIEF),
        },
        "outputs": {
            "package_queue": rel(PACKAGE_QUEUE),
            "failure_memory_map": rel(FAILURE_MEMORY_MAP),
            "experiment_design_receipt": rel(EXPERIMENT_RECEIPT),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT),
            "model_validation_receipt": rel(MODEL_VALIDATION_RECEIPT),
            "artifact_lineage_receipt": rel(ARTIFACT_LINEAGE_RECEIPT),
            "result_judgment": rel(RESULT_JUDGMENT),
            "report": rel(RUN_REPORT),
        },
        "counts": {
            "package_rows": len(packages),
            "selectable_package_rows": sum(1 for row in packages if row["queue_role"] == "selectable_fresh_candidate_seed"),
            "support_control_rows": sum(1 for row in packages if row["queue_role"] != "selectable_fresh_candidate_seed"),
            "failure_memory_rows": len(memory_rows),
        },
        "boundary": BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }


def artifact_lineage_payload(paths: Sequence[Path], source_hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "source_inputs": {
            "source_hashes": dict(source_hashes),
            "source_paths": [rel(path) for path in (STAGE270_CLOSEOUT, RUN270D_VARIANT_SUMMARY, RUN270D_NEGATIVE_SLICES, RUN270D_TIER_DUPLICATE, RUN270D_REVIEW_RESULT)],
        },
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_or_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def report_markdown(packages: Sequence[Mapping[str, Any]], memory_rows: Sequence[Mapping[str, Any]]) -> str:
    selectable = [row for row in packages if row["queue_role"] == "selectable_fresh_candidate_seed"]
    top_memory = "\n".join(
        f"- `{row['memory_id']}` {row['axis']}={row['bucket']}: net `{row['total_negative_net']}`, variants `{row['variant_count']}`, read `{row['primary_interpretation']}`"
        for row in memory_rows[:6]
    )
    package_lines = "\n".join(
        f"- `{row['package_id']}`: {row['fresh_thesis']}. 효과(effect, 효과): {next_use_label(row['next_use'])}로 넘긴다."
        for row in packages
    )
    return f"""# run271A Fresh Edge Rebuild Queue Design(271A 새 거래 우위 재구성 대기열 설계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selectable_package_rows(선택 가능 패키지 행): `{len(selectable)}`
- support_control_rows(보조 대조 행): `{len(packages) - len(selectable)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Design Meaning(설계 의미)

Stage271(271단계)는 Stage270(270단계)의 non-filter reward-skew repair(비필터 보상 기울기 수리)를 반복하지 않는다.
효과(effect, 효과): damaging slice(손상 구간), time-risk state(시간 위험 상태), recovery/payoff shape(회복/보상 형태)를 새 candidate package(후보 패키지) 질문으로 바꾼다.

## Package Queue(패키지 대기열)

{package_lines}

## Failure Memory Used(사용한 실패 기억)

{top_memory}

## Gate Coverage(게이트 커버리지)

- work_packet_schema_lint(작업 묶음 스키마 점검): `{rel(EXPERIMENT_RECEIPT)}`
- data_integrity_boundary(데이터 무결성 경계): `{rel(DATA_INTEGRITY_RECEIPT)}`
- model_validation_boundary(모델 검증 경계): `{rel(MODEL_VALIDATION_RECEIPT)}`
- artifact_lineage_audit(산출물 계보 감사): `{rel(ARTIFACT_LINEAGE_RECEIPT)}`
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def update_selection_status() -> None:
    text = f"""# Stage271 Selection Status(271단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `stage271_fresh_edge_rebuild_after_nonfilter_failure_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE270_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- package_queue(패키지 대기열): `{rel(PACKAGE_QUEUE)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

run271A(271A 실행)는 selectable fresh candidate seed(선택 가능 새 후보 씨앗) `3`개와 support control(보조 대조) `1`개를 만들었다.
효과(effect, 효과): 아직 candidate package(후보 패키지)가 선택된 것이 아니라, run271B(271B 실행)에서 물질화할 설계 대기열이 생긴 것이다.

## Boundary(경계)

`{BOUNDARY}`
"""
    write_md(SELECTION_STATUS, text)


def update_review_index() -> None:
    text = f"""# Stage271 Review Index(271단계 검토 색인)

## Current State(현재 상태)

Stage271(271단계)는 run271A(271A 실행) fresh edge rebuild queue design(새 거래 우위 재구성 대기열 설계)을 완료했다.
효과(effect, 효과): selected candidate(선택 후보) 없이 run271B(271B 실행) blueprint materialization(청사진 물질화)로 넘어간다.

## Reports(보고)

- stage brief(단계 개요): `{rel(STAGE271_BRIEF)}`
- run271A report(271A 보고): `{rel(RUN_REPORT)}`
- run271A package queue(271A 패키지 대기열): `{rel(PACKAGE_QUEUE)}`
"""
    write_md(REVIEW_INDEX, text)


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


def update_state_docs() -> None:
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE271_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `fresh_edge_rebuild_after_nonfilter_failure_package_queue`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run271A_summary(271A 요약)",
        f"- run271A_summary(271A 요약): run271A(271A 실행)는 selectable fresh candidate seed(선택 가능 새 후보 씨앗) `3`개와 support control(보조 대조) `1`개를 설계했다. Effect(효과): Stage270(270단계)의 failure memory(실패 기억)를 후보 보존이 아니라 새 candidate package queue(후보 패키지 대기열)로 바꿨고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE271_ID}")
    focus = (
        "- >-\n"
        f"  Stage271(271단계) run271A(271A 실행) fresh edge rebuild queue design(새 거래 우위 재구성 대기열 설계) `{RUN_ID}`. "
        "Effect(효과): selectable fresh candidate seed(선택 가능 새 후보 씨앗) `3`개와 support control(보조 대조) `1`개를 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run271A fresh edge rebuild queue design(271A 새 거래 우위 재구성 대기열 설계)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): selectable fresh candidate seed(선택 가능 새 후보 씨앗) `3`개와 support control(보조 대조) `1`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_registers(created_at: str, artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE271_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": "package_rows=4;selectable=3;support_control=1;selected_candidate=none;onnx_readiness=not_claimed.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_separate_design",
            "stage_id": STAGE271_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_separate_design",
            "parent_run_id": "",
            "record_view": "Tier A separate design(티어 A 분리 설계)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_edge_rebuild_queue",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(PACKAGE_QUEUE),
            "primary_kpi": "selectable_package_rows=3;support_control_rows=1",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Tier A materialization planned in run271B.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_separate_design",
            "stage_id": STAGE271_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_separate_design",
            "parent_run_id": "",
            "record_view": "Tier B separate design(티어 B 분리 설계)",
            "tier_scope": "Tier B separate",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_edge_rebuild_queue",
            "status": STATUS,
            "judgment": "planned_with_mirror_boundary_receipt",
            "path": rel(DATA_INTEGRITY_RECEIPT),
            "primary_kpi": "tier_b_status=planned_boundary_not_authority",
            "guardrail_kpi": "no_fallback_authority_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Tier B from Stage270 was mirror structural replay; run271B must preserve boundary.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_design",
            "stage_id": STAGE271_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_combined_design",
            "parent_run_id": "",
            "record_view": "Tier A+B combined design(티어 A+B 합산 설계)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_edge_rebuild_queue",
            "status": STATUS,
            "judgment": "planned_combined_record_no_performance_claim",
            "path": rel(EXPERIMENT_RECEIPT),
            "primary_kpi": "combined_record=planned",
            "guardrail_kpi": "performance_claim=none",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Combined record is a design requirement, not a synthetic performance claim.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__design",
                "stage_id": STAGE271_ID,
                "run_id": RUN_ID,
                "view": "fresh_edge_rebuild_queue_design",
                "tier_scope": "Tier A+B paired design",
                "scoreboard": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"selectable=3;support_control=1;next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "run271A_design_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE271_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run271A fresh edge rebuild design artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def run() -> dict[str, Any]:
    must_exist(
        [
            RUN270D_VARIANT_SUMMARY,
            RUN270D_NEGATIVE_SLICES,
            RUN270D_TIER_DUPLICATE,
            RUN270D_REVIEW_RESULT,
            RUN270D_REPORT,
            STAGE270_CLOSEOUT,
            STAGE271_BRIEF,
        ]
    )
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS).mkdir(parents=True, exist_ok=True)
    io_path(SELECTED).mkdir(parents=True, exist_ok=True)

    negative_rows = read_csv_rows(RUN270D_NEGATIVE_SLICES)
    memory_rows = aggregate_failure_memory(negative_rows)
    packages = package_queue(memory_rows)
    source_paths = [RUN270D_VARIANT_SUMMARY, RUN270D_NEGATIVE_SLICES, RUN270D_TIER_DUPLICATE, RUN270D_REVIEW_RESULT, RUN270D_REPORT, STAGE270_CLOSEOUT, STAGE271_BRIEF]
    source_hashes = {rel(path): sha256_file_lf_normalized(path) for path in source_paths}

    write_stage_csv(FAILURE_MEMORY_MAP, FAILURE_MEMORY_COLUMNS, memory_rows)
    write_stage_csv(PACKAGE_QUEUE, PACKAGE_COLUMNS, packages)
    write_json(EXPERIMENT_RECEIPT, experiment_receipt(packages))
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_receipt(source_hashes))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_receipt(packages))
    write_stage_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())
    write_json(RUN_MANIFEST, manifest_payload(packages, memory_rows))
    write_md(RUN_REPORT, report_markdown(packages, memory_rows))
    update_selection_status()
    update_review_index()

    artifacts = [
        RUN_MANIFEST,
        PACKAGE_QUEUE,
        FAILURE_MEMORY_MAP,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        RUN_REPORT,
        SELECTION_STATUS,
        REVIEW_INDEX,
    ]
    write_json(ARTIFACT_LINEAGE_RECEIPT, artifact_lineage_payload([*artifacts, ARTIFACT_LINEAGE_RECEIPT], source_hashes))
    artifacts.append(ARTIFACT_LINEAGE_RECEIPT)

    created_at = utc_now()
    update_registers(created_at, artifacts)
    update_state_docs()

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE271_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "package_rows": len(packages),
        "selectable_package_rows": sum(1 for row in packages if row["queue_role"] == "selectable_fresh_candidate_seed"),
        "support_control_rows": sum(1 for row in packages if row["queue_role"] != "selectable_fresh_candidate_seed"),
        "failure_memory_rows": len(memory_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
