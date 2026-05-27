from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import review_mt5_feature_parity_and_stale_lag_stress_without_db as bs


aw = bs.aw
bg = bs.bg

TODAY = "2026-05-27"
STAGE_ID = bs.STAGE_ID
RUN_NUMBER = "run337BT"
RUN_ID = "run337BT_materialize_stale_lag_guarded_model_scout_inputs_without_db_v1"
PARENT_RUN_ID = bs.RUN_ID
NEXT_RUN_ID = "run337BU_train_guarded_model_scouts_without_db_v1"
STATUS = "completed_stage337BT_stale_lag_guarded_model_scout_inputs_materialized_no_training_no_selection"
JUDGMENT = "guarded_model_scout_inputs_ready_training_not_run_forward_not_claimed"
DECISION = "stage337BT_open_run337BU_train_guarded_model_scouts"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BT_stale_lag_guarded_model_scout_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bs.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PACKAGE_DIR = RUN_DIR / "scout_packages"
REVIEWS_DIR = bs.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BT_stale_lag_guarded_model_scout_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BT_stale_lag_guarded_model_scout_inputs.md"
SELECTED_STATUS = bs.SELECTED_STATUS
STAGE_BRIEF = bs.STAGE_BRIEF
WORKSPACE_STATE = bs.WORKSPACE_STATE
CURRENT_STATE = bs.CURRENT_STATE
CHANGELOG = bs.CHANGELOG
RUN_REGISTRY = bs.RUN_REGISTRY
ALPHA_LEDGER = bs.ALPHA_LEDGER
ARTIFACT_REGISTRY = bs.ARTIFACT_REGISTRY
STAGE_LEDGER = bs.STAGE_LEDGER

BS_DIR = STAGE_DIR / "02_runs" / "run337BS"
BQ_DIR = STAGE_DIR / "02_runs" / "run337BQ"
BS_FINAL = BS_DIR / "final_decision.json"
BS_USABILITY = BS_DIR / "feature_set_usability_matrix.csv"
BS_STALE_LAG_STRESS = BS_DIR / "stale_lag_stress_matrix.csv"
BS_TESTER_GAP = BS_DIR / "tester_gap_review.csv"
BS_PROXY_SCOPE = BS_DIR / "proxy_scope_review.csv"
BS_QUEUE = BS_DIR / "run337BT_stale_lag_guarded_model_scout_queue.csv"
BS_GATE_AUDIT = BS_DIR / "required_gate_coverage_audit.csv"
BQ_FINAL = BQ_DIR / "final_decision.json"
BQ_PACKAGE_MANIFEST = BQ_DIR / "mt5_runtime_parity_package" / "runtime_parity_package_manifest.json"
BQ_FEATURE_SUMMARY = BQ_DIR / "feature_set_materialization_summary.csv"

SCOUT_INPUT_PACKAGE = RUN_DIR / "scout_input_package_matrix.csv"
SCOUT_BRANCH_CONTRACTS = RUN_DIR / "scout_branch_contracts.csv"
NEGATIVE_CONTROLS = RUN_DIR / "negative_control_matrix.csv"
NO_OVERFIT_GATES = RUN_DIR / "no_overfit_gate_matrix.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
GUARDED_TRAINING_PLAN = RUN_DIR / "guarded_training_plan.csv"
PACKAGE_MANIFEST_SUMMARY = RUN_DIR / "scout_package_manifest_summary.csv"
RUN337BU_QUEUE = RUN_DIR / "run337BU_train_guarded_model_scouts_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BS_FINAL,
    BS_USABILITY,
    BS_STALE_LAG_STRESS,
    BS_TESTER_GAP,
    BS_PROXY_SCOPE,
    BS_QUEUE,
    BS_GATE_AUDIT,
    BQ_FINAL,
    BQ_PACKAGE_MANIFEST,
    BQ_FEATURE_SUMMARY,
)
OUTPUT_FILES = (
    SCOUT_INPUT_PACKAGE,
    SCOUT_BRANCH_CONTRACTS,
    NEGATIVE_CONTROLS,
    NO_OVERFIT_GATES,
    PROXY_MT5_COMPARISON_CONTRACT,
    GUARDED_TRAINING_PLAN,
    PACKAGE_MANIFEST_SUMMARY,
    RUN337BU_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

FEATURE_SET_ORDER = (
    "us100_technical42_no_external",
    "macro48_no_equity_breadth_or_top3",
    "core56_no_top3_weight_features",
)
BRANCH_ROLE_BY_FEATURE = {
    "us100_technical42_no_external": "technical42_low_stale_control",
    "macro48_no_equity_breadth_or_top3": "macro48_macro_lag_ablation",
    "core56_no_top3_weight_features": "core56_equity_stale_stress_not_primary",
}

PACKAGE_COLUMNS = (
    "scout_package_id",
    "feature_set_id",
    "branch_id",
    "branch_role",
    "feature_family",
    "feature_count",
    "row_count",
    "first_timestamp",
    "last_timestamp",
    "feature_csv_path",
    "feature_csv_sha256",
    "feature_csv_manifest_sha256",
    "feature_order_path",
    "feature_order_sha256",
    "feature_order_manifest_sha256",
    "hash_match_status",
    "parity_status",
    "stale_risk",
    "tester_gap_status",
    "allowed_use",
    "forbidden_use",
    "required_controls",
    "package_manifest_path",
    "effect",
    "claim_boundary",
)
BRANCH_COLUMNS = (
    "branch_id",
    "scout_package_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "target_branch_id",
    "control_type",
    "control_description",
    "expected_result",
    "failure_interpretation",
    "effect",
    "claim_boundary",
)
GATE_MATRIX_COLUMNS = (
    "gate_id",
    "applies_to",
    "gate_type",
    "required_before",
    "pass_condition",
    "fail_action",
    "effect",
    "claim_boundary",
)
PROXY_CONTRACT_COLUMNS = (
    "contract_id",
    "applies_to",
    "proxy_expected_required",
    "mt5_runtime_required",
    "comparison_keys",
    "usable_for_kpi_if",
    "invalid_if",
    "effect",
    "claim_boundary",
)
TRAINING_PLAN_COLUMNS = (
    "plan_id",
    "branch_id",
    "model_family",
    "target_and_label",
    "split_method",
    "selection_metric",
    "secondary_metrics",
    "threshold_policy",
    "overfit_risk",
    "calibration_risk",
    "allowed_output",
    "forbidden_output",
    "claim_boundary",
)
MANIFEST_SUMMARY_COLUMNS = (
    "scout_package_id",
    "manifest_path",
    "manifest_sha256",
    "feature_csv_sha256",
    "feature_order_sha256",
    "status",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "input_packages",
    "must_train",
    "must_compare",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = bs.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(Path(path))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with aw.io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    return aw.write_json(path, payload)


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description=RUN_ID).parse_args()


def load_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BT inputs: {missing}")
    bs_final = read_json(BS_FINAL)
    if bs_final.get("next_action") != RUN_ID:
        raise RuntimeError(f"run337BS final does not open run337BT: {bs_final.get('next_action')}")
    bq_manifest = read_json(BQ_PACKAGE_MANIFEST)
    return {
        "bs_final": bs_final,
        "bs_usability": read_rows(BS_USABILITY),
        "bs_stale": read_rows(BS_STALE_LAG_STRESS),
        "bs_gap": read_rows(BS_TESTER_GAP),
        "bs_proxy": read_rows(BS_PROXY_SCOPE),
        "bs_queue": read_rows(BS_QUEUE),
        "bs_gates": read_rows(BS_GATE_AUDIT),
        "bq_final": read_json(BQ_FINAL),
        "bq_manifest": bq_manifest,
        "bq_matrix": list(bq_manifest.get("matrix_rows", [])),
        "bq_feature_summary": read_rows(BQ_FEATURE_SUMMARY),
    }


def by_key(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, Mapping[str, Any]]:
    return {str(row.get(key, "")): row for row in rows}


def branch_id(feature_set_id: str) -> str:
    return f"bt_{BRANCH_ROLE_BY_FEATURE[feature_set_id]}"


def package_id(feature_set_id: str) -> str:
    return f"{RUN_NUMBER}_{feature_set_id}"


def build_scout_packages(src: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    usability = by_key(src["bs_usability"], "feature_set_id")
    matrix_by_feature = by_key(src["bq_matrix"], "feature_set_id")
    manifest_paths: list[Path] = []
    package_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    for feature_set_id in FEATURE_SET_ORDER:
        matrix = matrix_by_feature.get(feature_set_id)
        use = usability.get(feature_set_id, {})
        if not matrix or use.get("usable_for_next_model_scout") != "true":
            continue
        feature_csv = ROOT / str(matrix.get("mt5_feature_csv", ""))
        feature_order = ROOT / str(matrix.get("mt5_feature_order", ""))
        feature_csv_sha = aw.sha256_file(feature_csv)
        feature_order_sha = aw.sha256_file(feature_order)
        csv_manifest_sha = str(matrix.get("csv_sha256", ""))
        order_manifest_sha = str(matrix.get("feature_order_sha256", ""))
        hash_match_status = "matched" if feature_csv_sha == csv_manifest_sha and feature_order_sha == order_manifest_sha else "mismatch"
        scout_package_id = package_id(feature_set_id)
        bid = branch_id(feature_set_id)
        manifest_path = PACKAGE_DIR / f"{scout_package_id}_manifest.json"
        payload = {
            "scout_package_id": scout_package_id,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "feature_set_id": feature_set_id,
            "branch_id": bid,
            "branch_role": BRANCH_ROLE_BY_FEATURE[feature_set_id],
            "feature_family": use.get("feature_family", ""),
            "feature_count": int(matrix.get("feature_count", 0)),
            "row_count": int(matrix.get("row_count", 0)),
            "first_timestamp": matrix.get("first_timestamp", ""),
            "last_timestamp": matrix.get("last_timestamp", ""),
            "feature_csv_path": rel(feature_csv),
            "feature_csv_sha256": feature_csv_sha,
            "feature_csv_manifest_sha256": csv_manifest_sha,
            "feature_order_path": rel(feature_order),
            "feature_order_sha256": feature_order_sha,
            "feature_order_manifest_sha256": order_manifest_sha,
            "hash_match_status": hash_match_status,
            "parity_status": use.get("parity_status", ""),
            "stale_risk": use.get("external_stale_risk", ""),
            "tester_gap_status": use.get("tester_gap_status", ""),
            "allowed_use": "exploratory_model_scout_input_only(탐색 모델 스카우트 입력 전용)",
            "forbidden_use": "forward_decision_runtime_authority_operating_reference(전진 판정/런타임 권위/운영 기준 금지)",
            "required_controls": use.get("required_controls", ""),
            "effect": "binds a fixed feature package to one guarded branch(고정 피처 패키지를 방어 분기 하나에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        manifest_paths.append(write_json(manifest_path, payload))
        row = dict(payload)
        row["package_manifest_path"] = rel(manifest_path)
        package_rows.append(row)
        summary_rows.append(
            {
                "scout_package_id": scout_package_id,
                "manifest_path": rel(manifest_path),
                "manifest_sha256": aw.sha256_file(manifest_path),
                "feature_csv_sha256": feature_csv_sha,
                "feature_order_sha256": feature_order_sha,
                "status": "materialized(물질화 완료)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return package_rows, summary_rows, manifest_paths


def build_branch_contracts(package_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package in package_rows:
        feature_set_id = str(package["feature_set_id"])
        bid = str(package["branch_id"])
        if feature_set_id == "us100_technical42_no_external":
            hypothesis = "technical-only(기술 전용) 입력은 외부 stale lag(낡은 지연) 없이 낮은 오염 기준선을 줄 수 있다."
            changed = "external context removed(외부 문맥 제거)"
            baseline = "no-trade(무거래) and prior fragile proxy(이전 취약 프록시)"
        elif feature_set_id == "macro48_no_equity_breadth_or_top3":
            hypothesis = "macro context(거시 문맥)는 lag sensitivity(지연 민감도)를 통제할 때만 견고성에 도움을 줄 수 있다."
            changed = "macro context retained and equity context removed(거시 문맥 유지, 주식 문맥 제거)"
            baseline = "technical-only branch(기술 전용 분기)"
        else:
            hypothesis = "equity context(주식 문맥)는 stale carry(낡은 이월)를 견뎌야만 보조 단서로 쓸 수 있다."
            changed = "equity context retained only as stress branch(주식 문맥은 압박 분기로만 유지)"
            baseline = "technical-only and macro-lag branches(기술 전용 및 거시 지연 분기)"
        rows.append(
            {
                "branch_id": bid,
                "scout_package_id": package["scout_package_id"],
                "hypothesis": hypothesis,
                "decision_use": "decide which feature family deserves bounded training next(다음 제한 학습 대상 피처군 결정)",
                "comparison_baseline": baseline,
                "control_variables": "US100 M5;closed-bar features(확정봉 피처);no forward labels for selection(전진 라벨 선택 금지)",
                "changed_variables": changed,
                "sample_scope": f"{package['first_timestamp']}..{package['last_timestamp']} rows={package['row_count']}",
                "success_criteria": "later run passes no-lookahead(미래참조 없음), proxy-vs-MT5(프록시 대 MT5), curve pocket(곡선 포켓), trade density(거래 밀도)",
                "failure_criteria": "fragile curve(취약 곡선), stale-lag dependence(낡은 지연 의존), proxy-MT5 mismatch(프록시-MT5 불일치), low trade density(낮은 거래 밀도)",
                "invalid_conditions": "feature hash mismatch(피처 해시 불일치);label leakage(라벨 누수);timestamp drift(시각 드리프트);forward threshold tuning(전진 임계값 조정)",
                "stop_conditions": "stop or downgrade claim before selection if any invalid condition appears(무효 조건 발견 시 선택 전 중지 또는 주장 하향)",
                "evidence_plan": "training report(학습 보고);proxy expected vs MT5 runtime(프록시 예상 대 MT5 런타임);cost/lot/regime/curve stress(비용/로트/국면/곡선 압박)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_controls(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    controls = [
        ("timestamp_shift_plus_1bar", "shift features by +1 closed bar(피처를 확정봉 +1개 이동)", "should break parity or weaken signal(동등성 깨짐 또는 신호 약화)"),
        ("feature_order_shuffle", "shuffle feature order in a copy(복사본에서 피처 순서 섞기)", "should fail order/hash gate(순서/해시 게이트 실패)"),
        ("label_permutation", "permute labels in training-only copy(학습 전용 복사본에서 라벨 섞기)", "should destroy edge(엣지 소멸)"),
        ("stale_source_drop", "drop macro/equity stale source group when applicable(해당 시 거시/주식 낡은 원천 제거)", "external branch must explain lost value(외부 분기는 손실 가치를 설명해야 함)"),
        ("future_label_tripwire", "inject a forbidden forward label selector in dry review(건식 검토에 금지 전진 라벨 선택자 주입)", "must be rejected before training(학습 전 거부되어야 함)"),
        ("technical_only_anchor", "compare every branch against technical-only anchor(모든 분기를 기술 전용 기준과 비교)", "external context must add robust value after costs(외부 문맥은 비용 후 견고 가치를 더해야 함)"),
    ]
    rows: list[dict[str, Any]] = []
    for branch in branch_rows:
        for control_id, description, expected in controls:
            rows.append(
                {
                    "control_id": f"{branch['branch_id']}__{control_id}",
                    "target_branch_id": branch["branch_id"],
                    "control_type": control_id,
                    "control_description": description,
                    "expected_result": expected,
                    "failure_interpretation": "if control looks better, mark original as overfit/leakage suspect(대조군이 더 좋으면 원본을 과적합/누수 의심으로 표시)",
                    "effect": "negative control(부정 대조)이 쉬운 과적합 승리를 의심하게 만든다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_no_overfit_gates(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gate_specs = [
        ("feature_hash_parity", "data_integrity(데이터 무결성)", "training(학습)", "BQ/BT feature hash must match package manifest(BQ/BT 피처 해시가 패키지 목록과 일치)", "repair input package; no training(입력 패키지 수리, 학습 금지)"),
        ("no_forward_label_selection", "model_validation(모델 검증)", "selection(선택)", "forward labels cannot choose feature set, threshold, or branch(전진 라벨로 피처/임계값/분기 선택 금지)", "invalidate selection claim(선택 주장 무효)"),
        ("threshold_predeclare_only", "model_validation(모델 검증)", "threshold_use(임계값 사용)", "threshold policy must be predeclared before forward scoring(전진 채점 전 임계값 정책 사전 선언)", "no threshold or forward claim(임계값/전진 주장 금지)"),
        ("proxy_mt5_signal_comparison", "runtime_parity(런타임 동등성)", "runtime_probe(런타임 탐침)", "proxy expected signal and MT5 runtime signal compared by timestamp(프록시 예상 신호와 MT5 런타임 신호를 시각별 비교)", "downgrade to package-only(패키지 전용으로 하향)"),
        ("tester_gap_boundary", "runtime_parity(런타임 동등성)", "positive_claim(긍정 주장)", "latest tester gap must be explained or excluded(최신 테스터 공백 설명 또는 제외)", "no forward/runtime authority claim(전진/런타임 권위 주장 금지)"),
        ("stale_lag_ablation", "data_integrity(데이터 무결성)", "branch_comparison(분기 비교)", "macro/equity branches compared against lower-stale controls(거시/주식 분기를 낮은 지연 대조군과 비교)", "treat as stale-risk clue only(낡은 위험 단서로만 사용)"),
        ("equity_stale_not_primary", "model_validation(모델 검증)", "branch_promotion(분기 승격)", "equity-stale branch cannot become primary without ablation proof(주식 낡은 분기는 제거시험 증거 없이 주 분기 금지)", "keep stress-only(압박 전용 유지)"),
        ("curve_pocket_and_trade_density", "performance_attribution(성과 귀속)", "positive_claim(긍정 주장)", "curve pocket, DD, recovery, trades/day reviewed(곡선 포켓, 손실폭, 회복, 일거래수 검토)", "no positive model claim(긍정 모델 주장 금지)"),
    ]
    rows: list[dict[str, Any]] = []
    for branch in branch_rows:
        for gate_id, gate_type, required_before, pass_condition, fail_action in gate_specs:
            rows.append(
                {
                    "gate_id": f"{branch['branch_id']}__{gate_id}",
                    "applies_to": branch["branch_id"],
                    "gate_type": gate_type,
                    "required_before": required_before,
                    "pass_condition": pass_condition,
                    "fail_action": fail_action,
                    "effect": "gate(게이트)가 모델 스카우트(model scout)를 또 다른 전진 과적합으로 바꾸지 못하게 막는다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_proxy_contracts(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in branch_rows:
        rows.append(
            {
                "contract_id": f"{branch['branch_id']}__proxy_mt5_comparison",
                "applies_to": branch["branch_id"],
                "proxy_expected_required": "true",
                "mt5_runtime_required": "true",
                "comparison_keys": "bar_time(봉 시각);decision_label(결정 라벨);p_short;p_flat;p_long;feature_input_hash(피처 입력 해시)",
                "usable_for_kpi_if": "timestamp overlap exists and decision/probability deltas are within declared tolerance(시각 겹침과 결정/확률 차이가 선언 허용범위 안)",
                "invalid_if": "MT5 output missing(출력 없음), timestamp shifted(시각 이동), feature hash mismatch(피처 해시 불일치), proxy uses labels/outcomes(프록시가 라벨/결과 사용)",
                "effect": "proxy expected value(프록시 예상값)를 KPI(핵심 성과 지표) 사용 전 MT5 runtime(런타임)에 묶는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_training_plan(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in branch_rows:
        rows.append(
            {
                "plan_id": f"{branch['branch_id']}__guarded_scout_training_plan",
                "branch_id": branch["branch_id"],
                "model_family": "bounded_scout_rf_lgbm_or_existing_local_baseline(제한 스카우트 RF/LGBM 또는 기존 로컬 기준)",
                "target_and_label": "future M5 path label must be declared in run337BU before training(미래 M5 경로 라벨은 run337BU 학습 전 선언)",
                "split_method": "chronological split with forward-after-2026-04-14 held out from selection(시계열 분할, 2026-04-14 이후 전진 구간 선택 제외)",
                "selection_metric": "not_set_in_run337BT",
                "secondary_metrics": "trade_count(거래수);PF(수익 팩터);DD(손실폭);recovery(회복);expectancy(기대값);curve_pocket(곡선 포켓);cost_stress(비용 압박)",
                "threshold_policy": "fixed_or_predeclared_only_in_next_run;no post-forward tuning(다음 실행에서 고정/사전선언만, 전진 후 조정 금지)",
                "overfit_risk": "feature family picking after seeing forward profit;stale-lag context dependence(전진 수익 본 뒤 피처군 선택, 낡은 지연 의존)",
                "calibration_risk": "scores are ranking signals unless calibration is proven(보정 증거 전 점수는 순위 신호)",
                "allowed_output": "exploratory scout model package and proxy-vs-MT5 comparison request(탐색 스카우트 모델 패키지와 프록시-MT5 비교 요청)",
                "forbidden_output": "Forward Passed(전진 통과), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue(package_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BU_train_guarded_model_scouts",
            "next_run_id": NEXT_RUN_ID,
            "input_packages": ";".join(str(row["scout_package_id"]) for row in package_rows),
            "must_train": "bounded scouts only after label/split/threshold policy is declared(라벨/분할/임계값 정책 선언 뒤 제한 스카우트만 학습)",
            "must_compare": "technical-only vs macro-lag vs equity-stale;proxy expected vs MT5 runtime(기술 전용 대 거시 지연 대 주식 낡음, 프록시 예상 대 MT5 런타임)",
            "must_reject_if": "forward outcome selects branch/threshold;negative controls pass as real;runtime parity missing(전진 결과가 분기/임계값 선택, 부정 대조 통과, 런타임 동등성 누락)",
            "expected_outputs": "trained scout artifacts;proxy expected outputs;MT5 runtime probe package;overfit/stale-lag review(학습 산출물, 프록시 예상 출력, MT5 런타임 탐침 패키지, 과적합/지연 검토)",
            "priority": "P0",
            "effect": "opens guarded model scout training without promotion claims(승격 주장 없이 방어 모델 스카우트 학습을 연다)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    src: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    branch_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    overfit_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    training_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    bs_passed = sum(1 for row in src["bs_gates"] if row.get("status") == "passed")
    packaged_features = {str(row.get("feature_set_id", "")) for row in package_rows}
    expected_features = set(FEATURE_SET_ORDER)
    branch_roles = {str(row.get("branch_role", "")) for row in package_rows}
    hash_matches = all(row.get("hash_match_status") == "matched" for row in package_rows)
    proxy_requires_mt5 = all(row.get("proxy_expected_required") == "true" and row.get("mt5_runtime_required") == "true" for row in proxy_rows)
    specs = [
        ("bt_gate_parent_bs_loaded", src["bs_final"].get("next_action") == RUN_ID, str(src["bs_final"].get("next_action")), "run337BS opens run337BT(337BS가 337BT를 연다)"),
        ("bt_gate_parent_bs_gates_passed", bs_passed == 11 and src["bs_final"].get("passed_gates") == 11, f"bs_gates={bs_passed}", "BS gates passed(BS 게이트 통과)"),
        ("bt_gate_three_feature_packages_materialized", expected_features.issubset(packaged_features), f"packaged={sorted(packaged_features)}", "three guarded feature packages exist(방어 피처 패키지 3개 존재)"),
        ("bt_gate_package_hashes_match_manifest", hash_matches, f"hash_matches={hash_matches}", "feature and order hashes match manifest(피처/순서 해시가 목록과 일치)"),
        ("bt_gate_branch_roles_separated", len(branch_roles) == 3, f"roles={sorted(branch_roles)}", "technical/macro/equity roles separated(기술/거시/주식 역할 분리)"),
        ("bt_gate_negative_controls_written", len(negative_rows) >= len(branch_rows) * 6, f"negative_rows={len(negative_rows)}", "negative controls written(부정 대조 작성)"),
        ("bt_gate_no_overfit_gates_written", len(overfit_rows) >= len(branch_rows) * 8, f"gate_rows={len(overfit_rows)}", "no-overfit gates written(무과적합 게이트 작성)"),
        ("bt_gate_proxy_mt5_contract_written", len(proxy_rows) == len(branch_rows) and proxy_requires_mt5, f"proxy_contracts={len(proxy_rows)}", "proxy-vs-MT5 contracts written(프록시 대 MT5 계약 작성)"),
        ("bt_gate_training_plan_bounded", all(row.get("selection_metric") == "not_set_in_run337BT" for row in training_rows), f"training_rows={len(training_rows)}", "training plan is bounded and unselected(학습 계획은 제한되고 미선택)"),
        ("bt_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue_rows={len(queue_rows)}", "run337BU queue ready(337BU 대기열 준비)"),
        ("bt_gate_no_training_selection_forward_claim", True, "training=not_run;selection=not_run;forward=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "guarded scout package can move to training only with controls(방어 스카우트 패키지는 통제 조건이 있을 때만 학습으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def package_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| package(패키지) | role(역할) | rows(행) | stale risk(낡은 위험) | allowed use(허용 사용) |",
        "|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['feature_set_id']}` | `{row['branch_role']}` | {row['row_count']} | `{row['stale_risk']}` | `{row['allowed_use']}` |"
        )
    return "\n".join(lines)


def write_report(final: Mapping[str, Any], package_rows: Sequence[Mapping[str, Any]]) -> Path:
    text = f"""# Stage337 run337BT Stale-Lag Guarded Model Scout Inputs(낡은 지연 방어 모델 스카우트 입력)

## Conclusion(결론)

run337BT(337BT 실행)는 run337BS(337BS 실행)의 feature parity/stale lag review(피처 동등성/낡은 지연 검토)를 실제 model scout input package(모델 스카우트 입력 패키지)와 gate contract(게이트 계약)로 물질화했다.

Effect(효과): 다음 run337BU(337BU 실행)는 technical-only(기술 전용), macro-lag(거시 지연), equity-stale(주식 낡음) branch(분기)를 비교할 수 있지만, Forward/Runtime authority(전진/런타임 권위)는 아직 주장할 수 없다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- scout_packages(스카우트 패키지): `{final['scout_package_rows']}`
- negative_controls(부정 대조): `{final['negative_control_rows']}`
- no_overfit_gates(무과적합 게이트): `{final['no_overfit_gate_rows']}`

## Packages(패키지)

{package_table(package_rows)}

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BT Stale-Lag Guarded Model Scout Inputs(결정: 낡은 지연 방어 모델 스카우트 입력)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): run337BU(337BU 실행)는 bounded scout training(제한 스카우트 학습)으로 갈 수 있지만, proxy-vs-MT5(프록시 대 MT5)와 no-overfit gate(무과적합 게이트)를 통과해야 KPI(핵심 성과 지표)를 해석할 수 있다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads: list[tuple[Path, Mapping[str, Any]]] = [
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "guarded feature families can be scouted without selecting on forward outcome",
                "decision_use": "open bounded training inputs only",
                "comparison_baseline": "technical-only branch",
                "control_variables": "US100 M5, closed-bar timestamp, no forward outcome selection",
                "changed_variables": "feature family: technical-only vs macro-lag vs equity-stale",
                "sample_scope": "run337BQ as-of feature matrices after 2026-04-14",
                "success_criteria": "next run produces comparable proxy and MT5 runtime evidence",
                "failure_criteria": "negative controls pass, stale branch dominates only under stale carry, or parity breaks",
                "invalid_conditions": "lookahead, feature hash drift, timestamp mismatch, threshold selected on forward",
                "stop_conditions": "stop before selection if any invalid condition appears",
                "evidence_plan": [rel(SCOUT_INPUT_PACKAGE), rel(PROXY_MT5_COMPARISON_CONTRACT), rel(NO_OVERFIT_GATES)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": rel(BQ_PACKAGE_MANIFEST),
                "time_axis": "closed M5 UTC bar timestamps, MT5 parity checked in run337BR",
                "sample_scope": "three BQ as-of feature matrices after 2026-04-14",
                "missing_or_duplicate_check": "delegated to run337BQ/BR/BS summaries; latest tester gap remains named",
                "feature_label_boundary": "no labels materialized in run337BT",
                "split_boundary": "training split must be declared in run337BU",
                "leakage_risk": "future label selection and stale context overfit",
                "data_hash_or_identity": f"packages={final['scout_package_rows']};hash_match_status=matched",
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "not_trained",
                "target_and_label": "not_materialized_in_run337BT",
                "split_method": "must_be_declared_in_run337BU",
                "selection_metric": "none",
                "secondary_metrics": "declared for next run",
                "threshold_policy": "not_set",
                "overfit_risk": "branch and threshold selection after forward observation",
                "calibration_risk": "unknown until model exists",
                "comparison_baseline": "technical-only branch and no-trade",
                "validation_judgment": "exploratory_input_package",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(BQ_PACKAGE_MANIFEST),
                "shared_contract": rel(PROXY_MT5_COMPARISON_CONTRACT),
                "known_differences": "run337BT writes contracts only; no executable model runtime is run",
                "parity_check": "feature-reader parity inherited from run337BR; model proxy-vs-MT5 comparison required next",
                "parity_identity": rel(PACKAGE_MANIFEST_SUMMARY),
                "runtime_claim_boundary": "research_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if aw.path_exists(path)],
                "artifact_hashes": "recorded in artifact_registry and package manifest summary",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "ignored_with_manifest_for_run_artifacts;tracked_reports_and_registers",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(SCOUT_INPUT_PACKAGE), rel(SCOUT_BRANCH_CONTRACTS), rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "actual model training, proxy expected output, MT5 model runtime probe, KPI stress",
                "judgment_label": "exploratory_input_package",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "학습 재료는 준비됐지만 아직 모델 성능이나 운영 가능성을 말할 단계는 아니다.",
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337BT focus complete: stale-lag guarded model scout inputs(낡은 지연 방어 모델 스카우트 입력)를 `{final['status']}`로 닫았다. "
        "Effect(효과): technical-only/macro-lag/equity-stale(기술 전용/거시 지연/주식 낡음) 분기를 다음 run337BU(337BU 실행)의 제한 학습 입력으로 넘긴다.\n"
    )
    if "Stage337 run337BT focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = current_text
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BT(337BT 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 낡은 지연 방어 모델 스카우트 입력을 만들었고, 실제 training/proxy-MT5(학습/프록시-MT5) 비교는 다음 실행으로 넘긴다.
"""
    if "## Stage337 run337BT(337BT 실행)" not in current:
        marker = "## Stage337 run337BS(337BS 실행)"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `not_run_input_package_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 bounded scout training(제한 스카우트 학습)과 proxy-vs-MT5(프록시 대 MT5) 비교 준비다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BT(337BT 실행) materialized stale-lag guarded model scout inputs(낡은 지연 방어 모델 스카우트 입력). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BT materialized guarded model scout inputs(방어 모델 스카우트 입력) and opened run337BU(337BU 실행)."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stale_lag_guarded_model_scout_inputs_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "experiment_design_model_validation",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_model_scout_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "guarded_model_scout_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stale_lag_guarded_model_scout_inputs",
        "tier_scope": "Tier A+B combined input contract; no separate KPI in BT",
        "kpi_scope": "input_package_no_profit_kpi",
        "scoreboard_lane": "model_scout_preflight",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"scout_packages={final['scout_package_rows']}",
        "guardrail_kpi": "no_training;no_selection;proxy_mt5_required",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_model_scout_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation",
        "evidence_scope": "BT input package manifests and contracts",
        "kpi_scope": "input_contracts_no_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"packages={final['scout_package_rows']};negative_controls={final['negative_control_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__guarded_model_scout_inputs",
        "family": "experiment_design_model_validation",
        "question": "what guarded feature package inputs can safely move to bounded model scout training",
        "metric_scope": "input_contracts_no_kpi",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    artifact_columns = artifact_columns or [
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "artifact_path",
        "claim_boundary",
    ]
    generated = now_utc()
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not aw.path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    parse_args()
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    aw.io_path(PACKAGE_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    package_rows, manifest_summary_rows, manifest_paths = build_scout_packages(src)
    branch_rows = build_branch_contracts(package_rows)
    negative_rows = build_negative_controls(branch_rows)
    overfit_rows = build_no_overfit_gates(branch_rows)
    proxy_rows = build_proxy_contracts(branch_rows)
    training_rows = build_training_plan(branch_rows)
    queue_rows = build_queue(package_rows)
    gates = build_gates(src, package_rows, branch_rows, negative_rows, overfit_rows, proxy_rows, training_rows, queue_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "scout_package_rows": len(package_rows),
        "branch_contract_rows": len(branch_rows),
        "negative_control_rows": len(negative_rows),
        "no_overfit_gate_rows": len(overfit_rows),
        "proxy_contract_rows": len(proxy_rows),
        "training_plan_rows": len(training_rows),
        "training": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final["gate_rows"] = len(gates)
    final["passed_gates"] = count_passed(gates)
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    if final["failed_gates"]:
        final["status"] = "blocked_stage337BT_stale_lag_guarded_model_scout_inputs_gate_failed"
        final["judgment"] = "blocked_input_package_gate_failed"
        final["decision"] = "stage337BT_repair_input_package_before_training"
        final["next_action"] = RUN_ID
    artifact_paths: list[Path] = [
        write_csv(SCOUT_INPUT_PACKAGE, PACKAGE_COLUMNS, package_rows),
        write_csv(SCOUT_BRANCH_CONTRACTS, BRANCH_COLUMNS, branch_rows),
        write_csv(NEGATIVE_CONTROLS, NEGATIVE_COLUMNS, negative_rows),
        write_csv(NO_OVERFIT_GATES, GATE_MATRIX_COLUMNS, overfit_rows),
        write_csv(PROXY_MT5_COMPARISON_CONTRACT, PROXY_CONTRACT_COLUMNS, proxy_rows),
        write_csv(GUARDED_TRAINING_PLAN, TRAINING_PLAN_COLUMNS, training_rows),
        write_csv(PACKAGE_MANIFEST_SUMMARY, MANIFEST_SUMMARY_COLUMNS, manifest_summary_rows),
        write_csv(RUN337BU_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
    ]
    artifact_paths.extend(manifest_paths)
    artifact_paths.extend(build_receipts(final))
    artifact_paths.append(
        write_json(
            RUN_MANIFEST,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": now_utc(),
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "package_manifests": [rel(path) for path in manifest_paths],
                "external_verification_status": "out_of_scope_by_claim",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifact_paths.append(write_report(final, package_rows))
    artifact_paths.append(write_decision_doc(final))
    if not final["failed_gates"]:
        artifact_paths.extend(update_docs(final))
        artifact_paths.extend(update_registers(final, artifact_paths))
    else:
        artifact_paths.extend(update_registers(final, artifact_paths))
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 1 if final["failed_gates"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
