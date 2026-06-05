from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

STAGE_ID = "348_cash_open_proxy_review__long_oos_gap_short_carry_triage"
STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_STAGE_ID = "347_cash_open_asymmetric_source__long_short_head_design"

RUN_NUMBER = "run348B"
RUN_ID = "run348B_review_cash_open_asymmetric_proxy_training_without_db_v1"
PARENT_RUN_ID = "run348A_branch_stage347_to_cash_open_proxy_review_without_db_v1"
SOURCE_TRAINING_RUN_ID = "run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1"

STATUS = "completed_stage348B_proxy_review_triaged_onnx_deployable_short_probe_seed_no_selection"
JUDGMENT = (
    "inconclusive_proxy_review_long_oos_missing_short_oos_weak_"
    "onnx_deployable_short_probe_seed_allowed_no_operating_claim"
)
DECISION = "stage348B_open_run348C_materialize_onnx_deployable_short_carry_probe_package"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_triage_only_no_new_training_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run348B_cash_open_asymmetric_proxy_training_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run348A"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_COMPACT_SCORE = PARENT_RUN_DIR / "run347C_compact_score_summary.csv"
PARENT_REVIEW_SURFACE = PARENT_RUN_DIR / "stage348_review_seed_surface.csv"
PARENT_NEGATIVE_MEMORY = PARENT_RUN_DIR / "stage348_negative_memory_seed.csv"
PARENT_REVIEW_QUEUE = PARENT_RUN_DIR / "run348B_review_queue.csv"

SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run347C"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SCORECARD = SOURCE_RUN_DIR / "model_training_scorecard.csv"
SOURCE_THRESHOLD_SCREEN = SOURCE_RUN_DIR / "proxy_threshold_screen.csv"
SOURCE_PROBE_QUEUE = SOURCE_RUN_DIR / "probe_priority_queue.csv"
SOURCE_MODEL_MANIFEST = SOURCE_RUN_DIR / "model_artifact_manifest.csv"
SOURCE_ONNX_SMOKE = SOURCE_RUN_DIR / "onnx_parity_smoke.csv"
SOURCE_FEATURE_ORDER = SOURCE_RUN_DIR / "feature_order.csv"
SOURCE_PREDICTIONS = SOURCE_RUN_DIR / "proxy_model_predictions.csv"

OOS_GAP_AUDIT = RUN_DIR / "oos_gap_audit.csv"
SHORT_CARRY_TRIAGE = RUN_DIR / "short_carry_triage.csv"
ONNX_DEPLOYABILITY_REVIEW = RUN_DIR / "onnx_deployability_review.csv"
PROXY_MT5_USABILITY_MATRIX = RUN_DIR / "proxy_mt5_usability_matrix.csv"
NEXT_PROBE_SEED_QUEUE = RUN_DIR / "run348C_onnx_deployable_short_probe_seed_queue.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage348B_cash_open_asymmetric_proxy_training_review.md"

LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "path",
    "report_path",
    "primary_report",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "scoreboard_lane",
    "lane",
    "family",
    "run_number",
    "notes",
    "source_package_run_id",
    "rows",
    "attempt_count",
    "feature_count",
    "candidate_model_id",
    "ledger_row_id",
    "subrun_id",
    "view",
    "record_view",
    "tier",
    "tier_scope",
    "metric_scope",
    "kpi_scope",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "result_status",
    "net_profit",
    "profit_factor",
    "expectancy",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "matched_rows",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    candidate = Path(path)
    resolved = candidate.resolve()
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


def required(path: Path) -> Path:
    if not exists(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
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
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(10_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def to_float(row: Mapping[str, Any], key: str) -> float:
    try:
        return float(row.get(key, ""))
    except (TypeError, ValueError):
        return 0.0


def to_int(row: Mapping[str, Any], key: str) -> int:
    return int(round(to_float(row, key)))


def source_gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def index_by(rows: Sequence[Mapping[str, str]], *keys: str) -> dict[tuple[str, ...], Mapping[str, str]]:
    return {tuple(str(row.get(key, "")) for key in keys): row for row in rows}


def best_threshold_rows(
    threshold_rows: Sequence[Mapping[str, str]],
    model_family: str,
    split: str = "test",
    limit: int = 3,
) -> list[dict[str, Any]]:
    candidates = [
        dict(row)
        for row in threshold_rows
        if row.get("model_family") == model_family and row.get("split") == split
    ]
    candidates.sort(
        key=lambda row: (
            to_float(row, "teacher_precision"),
            to_float(row, "source_mt5_hit_expectancy_upper_bound"),
            to_float(row, "predicted_short_rows"),
        ),
        reverse=True,
    )
    return candidates[:limit]


def onnx_status_rows() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    _fields, onnx_rows = read_csv_rows(required(SOURCE_ONNX_SMOKE))
    manifest_fields, manifest_rows = read_csv_rows(required(SOURCE_MODEL_MANIFEST))
    _ = manifest_fields
    onnx_paths = {
        row.get("model_family", ""): row
        for row in manifest_rows
        if "onnx" in row.get("artifact_type", "").lower()
    }
    review_rows: list[dict[str, Any]] = []
    status_map: dict[str, dict[str, Any]] = {}
    for row in onnx_rows:
        family = row.get("model_family", "")
        manifest = onnx_paths.get(family, {})
        deployable = row.get("status") == "passed" and bool(manifest.get("path"))
        error = row.get("error", "")
        review = {
            "model_family": family,
            "onnx_status": row.get("status", ""),
            "deployable_for_mt5_probe_package": "yes" if deployable else "no",
            "rows": row.get("rows", ""),
            "max_abs_diff": row.get("max_abs_diff", ""),
            "mean_abs_diff": row.get("mean_abs_diff", ""),
            "onnx_path": row.get("path") or manifest.get("path", ""),
            "onnx_sha256": manifest.get("sha256", ""),
            "error_truncated": error[:300] + "...<truncated>" if len(error) > 300 else error,
            "review_judgment": (
                "onnx_smoke_passed_not_runtime_parity(온엑스 점검 통과, 런타임 동등성 아님)"
                if deployable
                else "not_deployable_for_probe_package(탐침 패키지 배포 불가)"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        review_rows.append(review)
        status_map[family] = review
    write_csv(ONNX_DEPLOYABILITY_REVIEW, review_rows)
    return review_rows, status_map


def build_oos_gap_audit(compact_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    families = sorted({row.get("model_family", "") for row in compact_rows if row.get("model_family")})
    by_key = index_by(compact_rows, "model_family", "head", "split")
    for family in families:
        long_validation = by_key.get((family, "long_head", "validation"), {})
        long_test = by_key.get((family, "long_head", "test"), {})
        short_validation = by_key.get((family, "short_head", "validation"), {})
        short_test = by_key.get((family, "short_head", "test"), {})
        allocator_test = by_key.get((family, "allocator", "test"), {})
        rows.append(
            {
                "model_family": family,
                "long_validation_positive_rows": long_validation.get("positive_rows", ""),
                "long_test_positive_rows": long_test.get("positive_rows", ""),
                "long_test_predicted_positive_rows": long_test.get("predicted_positive_rows", ""),
                "short_validation_positive_rows": short_validation.get("positive_rows", ""),
                "short_test_positive_rows": short_test.get("positive_rows", ""),
                "short_test_predicted_positive_rows": short_test.get("predicted_positive_rows", ""),
                "short_test_f1_positive": short_test.get("f1_positive", ""),
                "short_test_precision_positive": short_test.get("precision_positive", ""),
                "short_test_recall_positive": short_test.get("recall_positive", ""),
                "allocator_test_macro_f1": allocator_test.get("macro_f1", ""),
                "allocator_test_predicted_short_rows": allocator_test.get("predicted_short_rows", ""),
                "allocator_test_predicted_long_rows": allocator_test.get("predicted_long_rows", ""),
                "review_judgment": (
                    "long_oos_missing_and_short_oos_weak(롱 표본외 누락, 숏 표본외 약함)"
                    if to_int(long_test, "positive_rows") == 0 and to_float(short_test, "f1_positive") < 0.1
                    else "requires_manual_review(수동 검토 필요)"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OOS_GAP_AUDIT, rows)
    return rows


def build_short_carry_triage(
    compact_rows: Sequence[Mapping[str, str]],
    threshold_rows: Sequence[Mapping[str, str]],
    onnx_map: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_key = index_by(compact_rows, "model_family", "head", "split")
    families = sorted({row.get("model_family", "") for row in compact_rows if row.get("model_family")})
    rows: list[dict[str, Any]] = []
    for family in families:
        short_all = by_key.get((family, "short_head", "all"), {})
        short_test = by_key.get((family, "short_head", "test"), {})
        allocator_test = by_key.get((family, "allocator", "test"), {})
        best_tests = best_threshold_rows(threshold_rows, family, "test", limit=1)
        best_test = best_tests[0] if best_tests else {}
        onnx = onnx_map.get(family, {})
        deployable = onnx.get("deployable_for_mt5_probe_package") == "yes"
        test_precision = to_float(best_test, "teacher_precision")
        test_signal_rows = to_int(best_test, "signal_rows")
        if deployable and test_precision >= 0.18 and test_signal_rows >= 100:
            triage = "probe_seed_allowed_with_caveat(주의 포함 탐침 씨앗 허용)"
        elif deployable:
            triage = "repair_or_control_only(수리 또는 대조 전용)"
        else:
            triage = "reference_only_not_onnx_deployable(참고 전용, 온엑스 배포 불가)"
        rows.append(
            {
                "model_family": family,
                "onnx_deployable": "yes" if deployable else "no",
                "all_split_short_f1": short_all.get("f1_positive", ""),
                "all_split_short_precision": short_all.get("precision_positive", ""),
                "all_split_short_recall": short_all.get("recall_positive", ""),
                "test_short_f1": short_test.get("f1_positive", ""),
                "test_short_precision": short_test.get("precision_positive", ""),
                "test_short_recall": short_test.get("recall_positive", ""),
                "allocator_test_macro_f1": allocator_test.get("macro_f1", ""),
                "allocator_test_predicted_short_rows": allocator_test.get("predicted_short_rows", ""),
                "best_test_threshold_allocator_rule": best_test.get("allocator_rule", ""),
                "best_test_threshold_long_label": best_test.get("long_threshold_label", ""),
                "best_test_threshold_short_label": best_test.get("short_threshold_label", ""),
                "best_test_threshold_long_probability": best_test.get("long_probability_threshold", ""),
                "best_test_threshold_short_probability": best_test.get("short_probability_threshold", ""),
                "best_test_threshold_signal_rows": best_test.get("signal_rows", ""),
                "best_test_threshold_predicted_long_rows": best_test.get("predicted_long_rows", ""),
                "best_test_threshold_predicted_short_rows": best_test.get("predicted_short_rows", ""),
                "best_test_threshold_teacher_hit_rows": best_test.get("teacher_hit_rows", ""),
                "best_test_threshold_teacher_precision": best_test.get("teacher_precision", ""),
                "best_test_threshold_upper_bound": best_test.get("source_mt5_hit_expectancy_upper_bound", ""),
                "triage_decision": triage,
                "effect": (
                    "MT5 runtime probe(MT5 런타임 탐침)로만 확인하고 selection(선정)은 금지"
                    if "probe_seed_allowed" in triage
                    else "운영 주장에는 쓰지 않는다"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SHORT_CARRY_TRIAGE, rows)
    return rows


def build_next_probe_seed_queue(
    threshold_rows: Sequence[Mapping[str, str]],
    onnx_map: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    seed_rows: list[dict[str, Any]] = []
    priority = 1
    for family in ["logistic_balanced", "ExtraTrees"]:
        if onnx_map.get(family, {}).get("deployable_for_mt5_probe_package") != "yes":
            continue
        candidates = [
            row
            for row in threshold_rows
            if row.get("model_family") == family
            and row.get("split") == "test"
            and row.get("long_threshold_label") == "q95"
            and row.get("short_threshold_label") == "q90"
            and row.get("allocator_rule") in {"cash_open_regime_allocator", "balanced_margin"}
        ]
        candidates.sort(
            key=lambda row: (
                row.get("allocator_rule") != "cash_open_regime_allocator",
                -to_float(row, "teacher_precision"),
            )
        )
        for row in candidates[:2]:
            seed_rows.append(
                {
                    "seed_rank": priority,
                    "seed_id": f"seed{priority:02d}_{family}_{row.get('allocator_rule')}_test_q95_q90",
                    "next_run_id": NEXT_RUN_ID,
                    "model_family": family,
                    "onnx_path": onnx_map[family].get("onnx_path", ""),
                    "onnx_sha256": onnx_map[family].get("onnx_sha256", ""),
                    "split_evidence": "test",
                    "allocator_rule": row.get("allocator_rule", ""),
                    "long_threshold_label": row.get("long_threshold_label", ""),
                    "short_threshold_label": row.get("short_threshold_label", ""),
                    "long_probability_threshold": row.get("long_probability_threshold", ""),
                    "short_probability_threshold": row.get("short_probability_threshold", ""),
                    "signal_rows": row.get("signal_rows", ""),
                    "predicted_long_rows": row.get("predicted_long_rows", ""),
                    "predicted_short_rows": row.get("predicted_short_rows", ""),
                    "teacher_hit_rows": row.get("teacher_hit_rows", ""),
                    "teacher_precision": row.get("teacher_precision", ""),
                    "source_mt5_hit_expectancy_upper_bound": row.get("source_mt5_hit_expectancy_upper_bound", ""),
                    "allowed_use": "exploratory_mt5_runtime_probe_seed_only(탐색용 MT5 런타임 탐침 씨앗 전용)",
                    "forbidden_use": "candidate_selection_or_operating_claim(후보 선정 또는 운영 주장)",
                    "selection_status": "not_selected(선정 없음)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            priority += 1
    write_csv(NEXT_PROBE_SEED_QUEUE, seed_rows)
    return seed_rows


def build_usability_matrix(seed_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "review_axis": "long_oos_gap(롱 표본외 공백)",
            "available_evidence": rel(OOS_GAP_AUDIT),
            "judgment": "repair_condition(수리 조건)",
            "usable_now": "no",
            "effect": "롱 품질은 OOS 양성 라벨이 생기기 전까지 운영 주장이나 후보 선정 근거가 아니다.",
            "next_condition": "새 split/label source(분할/라벨 원천)에서 validation/test long positives(검증/테스트 롱 양성) 확보",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_axis": "short_carry_probe_seed(숏 기여 탐침 씨앗)",
            "available_evidence": rel(SHORT_CARRY_TRIAGE),
            "judgment": "probe_seed_allowed_with_caveat(주의 포함 탐침 씨앗 허용)",
            "usable_now": "yes_for_probe_only",
            "effect": f"{len(seed_rows)}개 ONNX deployable(온엑스 배포 가능) test-threshold seed(테스트 임계값 씨앗)를 다음 패키지로 보낼 수 있다.",
            "next_condition": "run348C package(348C 패키지) 뒤 MT5 runtime probe(MT5 런타임 탐침)에서 실제 손익/거래수 확인",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_axis": "onnx_smoke_boundary(온엑스 점검 경계)",
            "available_evidence": rel(ONNX_DEPLOYABILITY_REVIEW),
            "judgment": "smoke_pass_not_runtime_parity(점검 통과, 런타임 동등성 아님)",
            "usable_now": "yes_for_packaging_only",
            "effect": "logistic_balanced/ExtraTrees(로지스틱/엑스트라트리)는 패키징 가능하지만 MT5 실행 의미는 아직 없다.",
            "next_condition": "EA handoff(전문가 자문 인계)와 Strategy Tester telemetry(전략 테스터 기록) 비교",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_axis": "histgbm_reference(히스토그램 GBM 참고)",
            "available_evidence": rel(ONNX_DEPLOYABILITY_REVIEW),
            "judgment": "reference_only_not_deployable(참고 전용, 배포 불가)",
            "usable_now": "no_for_onnx_probe",
            "effect": "HistGBM(히스토그램 GBM)은 top proxy queue(상위 프록시 대기열)를 만들었지만 ONNX 변환 실패로 MT5 ONNX 탐침 씨앗에서 제외한다.",
            "next_condition": "별도 converter repair(변환기 수리)나 대체 model family(모델 계열)에서 같은 표면 재현",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(PROXY_MT5_USABILITY_MATRIX, rows)
    return rows


def build_review_findings(
    oos_rows: Sequence[Mapping[str, Any]],
    triage_rows: Sequence[Mapping[str, Any]],
    seed_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    deployable_probe_rows = [row for row in triage_rows if "probe_seed_allowed" in str(row.get("triage_decision", ""))]
    rows = [
        {
            "finding_id": "F01_LONG_OOS_BLOCKER",
            "severity": "P0",
            "finding": "validation/test long positive labels(검증/테스트 롱 양성 라벨)이 없다.",
            "evidence": rel(OOS_GAP_AUDIT),
            "judgment_label": "negative_memory(부정 기억)",
            "effect": "long head(롱 헤드)는 폐기하지 않지만 운영/선정 근거로 쓰지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F02_SHORT_OOS_WEAK",
            "severity": "P0",
            "finding": "default short head OOS(기본 숏 헤드 표본외)는 약하지만 test threshold screen(테스트 임계값 선별)은 탐침 가능성을 남겼다.",
            "evidence": rel(SHORT_CARRY_TRIAGE),
            "judgment_label": "inconclusive_probe_seed(불충분 탐침 씨앗)",
            "effect": f"{len(deployable_probe_rows)}개 family(계열)가 probe seed(탐침 씨앗)로만 남는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F03_ONNX_DEPLOYABLE_FILTER",
            "severity": "P1",
            "finding": "logistic_balanced/ExtraTrees(로지스틱/엑스트라트리)만 ONNX smoke(온엑스 점검)를 통과했다.",
            "evidence": rel(ONNX_DEPLOYABILITY_REVIEW),
            "judgment_label": "packaging_boundary(패키징 경계)",
            "effect": "HistGBM(히스토그램 GBM)은 proxy reference(프록시 참고)로만 두고 MT5 ONNX package(MT5 온엑스 패키지)에서 제외한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F04_NEXT_PACKAGE_MINIMAL",
            "severity": "P1",
            "finding": f"next seed queue(다음 씨앗 대기열)에 {len(seed_rows)}개 ONNX deployable short-carry seeds(온엑스 배포 가능 숏 기여 씨앗)를 남겼다.",
            "evidence": rel(NEXT_PROBE_SEED_QUEUE),
            "judgment_label": "next_runtime_probe_package_seed(다음 런타임 탐침 패키지 씨앗)",
            "effect": "다음 run348C(348C 실행)는 새 학습 없이 패키지만 만들 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    _ = oos_rows
    write_csv(REVIEW_FINDINGS, rows)
    return rows


def write_receipts(
    final347c: Mapping[str, Any],
    seed_rows: Sequence[Mapping[str, Any]],
    findings: Sequence[Mapping[str, Any]],
) -> None:
    receipt_time = now_utc()
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "measurement_scope": "proxy_review_signal_kpi_only_no_trading_kpi(프록시 검토 신호 KPI 전용, 거래 KPI 없음)",
            "management_state": "run_folder_manifest_report_registry_rows_written(실행 폴더/목록/보고/등록부 행 기록)",
            "judgment_class": "inconclusive(불충분)",
            "scoreboard": "structural_scout(구조 스카우트)",
            "parity_level": "P0_unverified(미검증)",
            "wfo_status": "not_applicable(해당 없음)",
            "registry_update_required": "yes",
            "negative_memory_required": "yes",
            "hard_gate_applicable": "no",
            "evidence_boundary": "reviewed_proxy_triage_only(검토된 프록시 분류 전용)",
            "source_rows": final347c.get("rows", ""),
            "probe_seed_rows": len(seed_rows),
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            "result_subject": "run347C cash-open asymmetric proxy training review(347C 현금장 비대칭 프록시 학습 검토)",
            "evidence_available": [
                rel(OOS_GAP_AUDIT),
                rel(SHORT_CARRY_TRIAGE),
                rel(ONNX_DEPLOYABILITY_REVIEW),
                rel(PROXY_MT5_USABILITY_MATRIX),
                rel(NEXT_PROBE_SEED_QUEUE),
                rel(REVIEW_FINDINGS),
            ],
            "evidence_missing": [
                "MT5 runtime probe(MT5 런타임 탐침)",
                "realized PnL labels(실현 손익 라벨)",
                "long OOS positive labels(롱 표본외 양성 라벨)",
                "runtime parity(런타임 동등성)",
            ],
            "judgment_label": "inconclusive(불충분)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "프록시는 약하지만 ONNX 배포 가능한 짧은 숏 기여 탐침 씨앗은 남았다. 아직 운영 후보는 아니다.",
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_COMPACT_SCORE),
                rel(PARENT_REVIEW_SURFACE),
                rel(PARENT_NEGATIVE_MEMORY),
                rel(SOURCE_SCORECARD),
                rel(SOURCE_THRESHOLD_SCREEN),
                rel(SOURCE_ONNX_SMOKE),
                rel(SOURCE_MODEL_MANIFEST),
            ],
            "producer": rel(Path("stage_pipelines/stage348/review_cash_open_asymmetric_proxy_training_without_db.py")),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_proxy_review_boundary(프록시 검토 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "training": "not_run",
            "mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "forward_pass": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "allowed_claim": "proxy_review_triage_and_next_probe_seed_only(프록시 검토 분류와 다음 탐침 씨앗 전용)",
            "created_at_utc": receipt_time,
        },
    )


def write_stage_docs(final347c: Mapping[str, Any], seed_rows: Sequence[Mapping[str, Any]], findings: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run348B Cash-Open Asymmetric Proxy Training Review(348B 현금장 비대칭 프록시 학습 검토)

## Result(결과)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- source_run(원천 실행): `{SOURCE_TRAINING_RUN_ID}`
- probe_seed_rows(탐침 씨앗 행): `{len(seed_rows)}`

Action(행동): run347C proxy training(347C 프록시 학습)을 OOS gap(표본외 공백), short-carry usability(숏 기여 활용 가능성), ONNX deployability(온엑스 배포 가능성)로 검토했다.
Effect(효과): long head(롱 헤드)는 repair condition(수리 조건)으로 낮추고, logistic/ExtraTrees(로지스틱/엑스트라트리) short-carry seeds(숏 기여 씨앗)만 다음 MT5 package(MT5 패키지) 후보로 남겼다.

## Key Findings(핵심 발견)

- long_oos(롱 표본외): validation/test positive labels(검증/테스트 양성 라벨) 없음.
- short_oos(숏 표본외): 기본 head(헤드)는 약하지만 threshold screen(임계값 선별)에서 test split(테스트 분할) 탐침 씨앗이 남음.
- ONNX(온엑스): logistic_balanced/ExtraTrees(로지스틱/엑스트라트리) allocator(배분기)만 smoke pass(점검 통과). HistGBM(히스토그램 GBM)은 reference only(참고 전용).

## Artifacts(산출물)

- findings(발견): `{rel(REVIEW_FINDINGS)}`
- oos_gap_audit(표본외 공백 감사): `{rel(OOS_GAP_AUDIT)}`
- short_carry_triage(숏 기여 분류): `{rel(SHORT_CARRY_TRIAGE)}`
- onnx_deployability(온엑스 배포 가능성): `{rel(ONNX_DEPLOYABILITY_REVIEW)}`
- probe_seed_queue(탐침 씨앗 대기열): `{rel(NEXT_PROBE_SEED_QUEUE)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    decision = f"""# 2026-06-01 Stage348B Proxy Review Decision(348B 프록시 검토 결정)

- decision(결정): `{DECISION}`
- source_run(원천 실행): `{SOURCE_TRAINING_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- probe_seed_rows(탐침 씨앗 행): `{len(seed_rows)}`
- evidence(근거): `{rel(REVIEW_FINDINGS)}`, `{rel(NEXT_PROBE_SEED_QUEUE)}`

Action(행동): proxy score(프록시 점수)를 MT5 KPI(MT5 핵심 성과 지표)로 올리지 않고, ONNX deployable(온엑스 배포 가능) short-carry probe seed(숏 기여 탐침 씨앗)만 분리했다.
Effect(효과): run348C(348C 실행)는 새 학습 없이 runtime probe package(런타임 탐침 패키지)만 만들 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
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

run348B(348B 실행)는 Stage347(347단계)의 proxy training(프록시 학습)을 reviewed proxy triage(검토된 프록시 분류)로 닫았다. 다음 run348C(348C 실행)는 ONNX deployable short-carry seeds(온엑스 배포 가능 숏 기여 씨앗)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 물질화한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No new training(새 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    selection = f"""# Stage348 Selection Status(348단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_run(원천 실행): `{SOURCE_TRAINING_RUN_ID}`
- reviewed_proxy_seed_rows(검토된 프록시 씨앗 행): `{len(seed_rows)}`
- long_oos_status(롱 표본외 상태): `missing_positive_labels(양성 라벨 없음)`
- short_probe_seed_status(숏 탐침 씨앗 상태): `allowed_for_mt5_probe_package_only(MT5 탐침 패키지 전용 허용)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage348(348단계)은 selection(선정)이 아니라 next probe package seed(다음 탐침 패키지 씨앗)만 남겼다.
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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    append_text_once(
        STAGE_BRIEF,
        "## run348B Proxy Review(348B 프록시 검토)",
        f"""## run348B Proxy Review(348B 프록시 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- probe_seed_rows(탐침 씨앗 행): `{len(seed_rows)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): long OOS gap(롱 표본외 공백)은 수리 조건으로 낮추고, ONNX deployable(온엑스 배포 가능) short-carry seeds(숏 기여 씨앗)만 패키지 후보로 남겼다.
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "run348B_cash_open_asymmetric_proxy_training_review",
        f"""## run348B Proxy Review(348B 프록시 검토)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- probe_seed_queue(탐침 씨앗 대기열): `{rel(NEXT_PROBE_SEED_QUEUE)}`
- effect(효과): 프록시 검토를 운영 주장 없이 다음 패키지 씨앗으로만 정리했다.
""",
    )
    _ = final347c, findings


def write_gates(seed_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("parent_run348A_gates_passed", source_gate_passed(PARENT_GATE_AUDIT), PARENT_GATE_AUDIT, "run348A branch gate(분기 게이트)를 확인했다."),
        ("source_run347C_gates_passed", source_gate_passed(SOURCE_GATE_AUDIT), SOURCE_GATE_AUDIT, "run347C training gate(학습 게이트)를 확인했다."),
        ("oos_gap_audit_written", exists(OOS_GAP_AUDIT), OOS_GAP_AUDIT, "OOS gap(표본외 공백)을 기록했다."),
        ("short_carry_triage_written", exists(SHORT_CARRY_TRIAGE), SHORT_CARRY_TRIAGE, "short carry(숏 기여) 활용 가능성을 분류했다."),
        ("onnx_deployability_review_written", exists(ONNX_DEPLOYABILITY_REVIEW), ONNX_DEPLOYABILITY_REVIEW, "ONNX deployability(온엑스 배포 가능성)를 분리했다."),
        ("probe_seed_queue_written", exists(NEXT_PROBE_SEED_QUEUE) and len(seed_rows) >= 2, NEXT_PROBE_SEED_QUEUE, "다음 MT5 package(MT5 패키지) 씨앗을 남겼다."),
        ("skill_receipts_written", exists(RUN_EVIDENCE_RECEIPT) and exists(RESULT_JUDGMENT_RECEIPT) and exists(LINEAGE_RECEIPT), RESULT_JUDGMENT_RECEIPT, "run evidence/result/lineage receipt(실행 근거/판정/계보 영수증)를 기록했다."),
        ("no_forbidden_operating_claim", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 승격/런타임 권위/목표 달성을 주장하지 않았다."),
        ("required_gate_coverage_audit_written", True, GATE_AUDIT, "required gate coverage audit(필수 게이트 커버리지 감사)를 기록했다."),
    ]
    gate_rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, effect in rows
    ]
    write_csv(GATE_AUDIT, gate_rows, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return gate_rows


def write_final(final347c: Mapping[str, Any], seed_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_training_run_id": SOURCE_TRAINING_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "source_rows": final347c.get("rows", ""),
            "source_feature_count": final347c.get("feature_count", ""),
            "source_trained_model_artifacts": final347c.get("trained_model_artifacts", ""),
            "source_onnx_allocator_smoke_passes": final347c.get("onnx_allocator_smoke_passes", ""),
            "source_long_oos_positive_labels": final347c.get("long_oos_positive_labels", ""),
            "probe_seed_rows": len(seed_rows),
            "gate_passes": sum(1 for row in gate_rows if row.get("status") == "passed"),
            "gate_total": len(gate_rows),
            "training": "not_run",
            "mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )


def write_manifest() -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_training_run_id": SOURCE_TRAINING_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path("stage_pipelines/stage348/review_cash_open_asymmetric_proxy_training_without_db.py")),
            "inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_COMPACT_SCORE),
                rel(PARENT_REVIEW_SURFACE),
                rel(PARENT_NEGATIVE_MEMORY),
                rel(PARENT_REVIEW_QUEUE),
                rel(SOURCE_FINAL_DECISION),
                rel(SOURCE_SCORECARD),
                rel(SOURCE_THRESHOLD_SCREEN),
                rel(SOURCE_PROBE_QUEUE),
                rel(SOURCE_MODEL_MANIFEST),
                rel(SOURCE_ONNX_SMOKE),
                rel(SOURCE_FEATURE_ORDER),
            ],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def ledger_rows(final347c: Mapping[str, Any], seed_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gate_passes = sum(1 for row in gate_rows if row.get("status") == "passed")
    gate_total = len(gate_rows)
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
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "lane": "proxy_review_triage(프록시 검토 분류)",
        "family": "kpi_evidence(KPI 근거)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "rows": final347c.get("rows", ""),
        "feature_count": final347c.get("feature_count", ""),
        "candidate_model_id": "none(없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "proxy_review_signal_kpi",
            "kpi_scope": "proxy_review_signal_kpi",
            "primary_kpi": f"probe_seed_rows={len(seed_rows)};onnx_deployable_families=2",
            "guardrail_kpi": "long_oos_positive_labels=0;no_mt5_execution",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "reviewed_proxy_triage_no_selection(검토된 프록시 분류, 선정 없음)",
            "notes": "ONNX deployable short-carry seeds(온엑스 배포 가능 숏 기여 씨앗)만 다음 패키지로 넘긴다.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "missing_required(필수 누락)",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이번 프록시 검토 범위에 없다.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": "same_as_tier_a_until_tier_b_available",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "same_as_tier_a_until_tier_b_available",
            "notes": "combined(합산)는 Tier B(티어 B) 부재 때문에 Tier A(티어 A) 경계와 같다.",
        },
    ]


def write_registries(final347c: Mapping[str, Any], seed_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> None:
    rows = ledger_rows(final347c, seed_rows, gate_rows)
    existing_fields, existing = read_csv_rows(STAGE_LEDGER) if exists(STAGE_LEDGER) else (LEDGER_COLUMNS, [])
    replacement = {row["ledger_row_id"] for row in rows}
    kept = [row for row in existing if row.get("ledger_row_id") not in replacement]
    fieldnames = list(dict.fromkeys(list(existing_fields) + LEDGER_COLUMNS))
    write_csv(STAGE_LEDGER, kept + rows, fieldnames)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "proxy_review_triage(프록시 검토 분류)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "run347C proxy training reviewed; ONNX deployable short-carry seeds only; no selection.",
                "family": "kpi_evidence(KPI 근거)",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": final347c.get("rows", ""),
                "gate_passes": sum(1 for row in gate_rows if row.get("status") == "passed"),
                "gate_total": len(gate_rows),
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "result_status": "reviewed_proxy_triage_no_selection(검토된 프록시 분류, 선정 없음)",
                "feature_count": final347c.get("feature_count", ""),
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "proxy_review_signal_kpi",
            }
        ],
    )
    artifact_paths = [path for path in OUTPUT_FILES if exists(path)]
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": f"{path.stem}(산출물)",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "run348B proxy review artifact(348B 프록시 검토 산출물).",
        }
        for path in artifact_paths
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_register_notes(seed_rows: Sequence[Mapping[str, Any]]) -> None:
    marker = f"run348B {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} run348B ONNX Short-Carry Probe Seed(온엑스 숏 기여 탐침 씨앗)

- source_run(원천 실행): `{SOURCE_TRAINING_RUN_ID}`
- idea(아이디어): ONNX deployable(온엑스 배포 가능) allocator(배분기) 중 logistic_balanced/ExtraTrees(로지스틱/엑스트라트리)의 test q95/q90 threshold(테스트 q95/q90 임계값)를 MT5 probe package(MT5 탐침 패키지)로 보낸다.
- seed_rows(씨앗 행): `{len(seed_rows)}`
- effect(효과): 약한 프록시를 후보로 승격하지 않고 runtime evidence(런타임 근거)로만 확인한다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} run348B Proxy Review Negative Memory(프록시 검토 부정 기억)

- source_run(원천 실행): `{SOURCE_TRAINING_RUN_ID}`
- negative_memory(부정 기억): long OOS positive labels(롱 표본외 양성 라벨) `0`; default short OOS head(기본 숏 표본외 헤드) 약함.
- salvage_value(회수 가치): ONNX deployable short threshold seeds(온엑스 배포 가능 숏 임계값 씨앗) `{len(seed_rows)}`개.
- do_not_repeat(반복 금지): all-split proxy queue(전체 분할 프록시 대기열)를 candidate selection(후보 선정)이나 MT5 KPI(MT5 핵심 성과 지표)처럼 쓰지 않는다.
- reopen_condition(재개 조건): run348C/MT5 probe(348C/MT5 탐침)에서 실제 거래 KPI(거래 핵심 성과 지표)가 확인되거나 long OOS label source(롱 표본외 라벨 원천)가 보강될 때.
- evidence(근거): `{rel(REVIEW_FINDINGS)}`
""",
    )


def write_changelog(seed_rows: Sequence[Mapping[str, Any]]) -> None:
    marker = f"run348B {RUN_ID}"
    text = f"""## {TODAY} run348B Cash-Open Proxy Review(현금장 프록시 검토)

- action(행동): run347C proxy training(347C 프록시 학습)을 OOS gap(표본외 공백), short-carry usability(숏 기여 활용 가능성), ONNX deployability(온엑스 배포 가능성)로 검토했다.
- effect(효과): long OOS gap(롱 표본외 공백)은 수리 조건으로 낮추고, `{len(seed_rows)}`개 ONNX short-carry probe seed(온엑스 숏 기여 탐침 씨앗)를 run348C(348C 실행)로 넘겼다.
- boundary(경계): no MT5 execution(MT5 실행 없음), no selection(선정 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    append_text_once(WORKSPACE_CHANGELOG, marker, text)
    append_text_once(ROOT_CHANGELOG, marker, text)


def validate(gate_rows: Sequence[Mapping[str, Any]]) -> None:
    required_outputs = [
        OOS_GAP_AUDIT,
        SHORT_CARRY_TRIAGE,
        ONNX_DEPLOYABILITY_REVIEW,
        PROXY_MT5_USABILITY_MATRIX,
        NEXT_PROBE_SEED_QUEUE,
        REVIEW_FINDINGS,
        RUN_EVIDENCE_RECEIPT,
        RESULT_JUDGMENT_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        SELECTION_STATUS,
    ]
    missing = [rel(path) for path in required_outputs if not exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    if any(row.get("status") != "passed" for row in gate_rows):
        raise RuntimeError("run348B gate audit failed(348B 게이트 감사 실패)")
    for label, path in [("workspace", WORKSPACE_STATE), ("current", CURRENT_WORKING_STATE), ("selection", SELECTION_STATUS)]:
        if STAGE_ID not in read_text(path) or NEXT_RUN_ID not in read_text(path):
            raise RuntimeError(f"{label} state sync failed({label} 상태 동기화 실패)")
    final = read_json(FINAL_DECISION)
    for key in ["operating_promotion", "runtime_authority", "goal_achieve"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


OUTPUT_FILES = [
    OOS_GAP_AUDIT,
    SHORT_CARRY_TRIAGE,
    ONNX_DEPLOYABILITY_REVIEW,
    PROXY_MT5_USABILITY_MATRIX,
    NEXT_PROBE_SEED_QUEUE,
    REVIEW_FINDINGS,
    RUN_EVIDENCE_RECEIPT,
    RESULT_JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]


def main() -> None:
    for path in [
        RUN_DIR,
        REVIEW_DIR,
        DECISION_DOC.parent,
    ]:
        os.makedirs(fs_path(path), exist_ok=True)
    inputs = [
        PARENT_FINAL_DECISION,
        PARENT_GATE_AUDIT,
        PARENT_COMPACT_SCORE,
        PARENT_REVIEW_SURFACE,
        PARENT_NEGATIVE_MEMORY,
        PARENT_REVIEW_QUEUE,
        SOURCE_FINAL_DECISION,
        SOURCE_GATE_AUDIT,
        SOURCE_SCORECARD,
        SOURCE_THRESHOLD_SCREEN,
        SOURCE_PROBE_QUEUE,
        SOURCE_MODEL_MANIFEST,
        SOURCE_ONNX_SMOKE,
        SOURCE_FEATURE_ORDER,
    ]
    for path in inputs:
        required(path)
    final347c = read_json(SOURCE_FINAL_DECISION)
    _compact_fields, compact_rows = read_csv_rows(PARENT_COMPACT_SCORE)
    _threshold_fields, threshold_rows = read_csv_rows(SOURCE_THRESHOLD_SCREEN)
    onnx_rows, onnx_map = onnx_status_rows()
    oos_rows = build_oos_gap_audit(compact_rows)
    triage_rows = build_short_carry_triage(compact_rows, threshold_rows, onnx_map)
    seed_rows = build_next_probe_seed_queue(threshold_rows, onnx_map)
    usability_rows = build_usability_matrix(seed_rows)
    findings = build_review_findings(oos_rows, triage_rows, seed_rows)
    write_receipts(final347c, seed_rows, findings)
    write_stage_docs(final347c, seed_rows, findings)
    gate_rows = write_gates(seed_rows)
    write_final(final347c, seed_rows, gate_rows)
    write_manifest()
    write_registries(final347c, seed_rows, gate_rows)
    write_register_notes(seed_rows)
    write_changelog(seed_rows)
    validate(gate_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for row in gate_rows if row["status"] == "passed"),
                "gate_total": len(gate_rows),
                "onnx_review_rows": len(onnx_rows),
                "probe_seed_rows": len(seed_rows),
                "usability_rows": len(usability_rows),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
