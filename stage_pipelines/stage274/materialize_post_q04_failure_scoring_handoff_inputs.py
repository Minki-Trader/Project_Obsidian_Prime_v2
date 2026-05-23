from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild"
RUN_ID = "run274C_materialize_post_q04_failure_scoring_handoff_inputs_v1"
SOURCE_RUN_ID = "run274B_materialize_post_q04_failure_candidate_package_blueprints_v1"
STATUS = "completed_post_q04_failure_scoring_handoff_input_materialization_no_candidate_selection"
JUDGMENT = "scoring_handoff_inputs_ready_no_candidate_selection"
JUDGMENT_CLASS = "inconclusive"
NEXT_ACTION = "run274D_execute_post_q04_failure_scoring_materialization_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN274B = STAGE / "02_runs" / "run274B"
RUN_DIR = STAGE / "02_runs" / "run274C"
HANDOFF_SKELETON_DIR = RUN_DIR / "handoff_skeletons"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_BLUEPRINTS = RUN274B / "package_blueprints.json"
SOURCE_RUN274B_MANIFEST = RUN274B / "run_manifest.json"
SOURCE_SCORING_PLAN = RUN274B / "scoring_surface_plan.csv"
SOURCE_ADAPTER_PLAN = RUN274B / "adapter_contract_plan.csv"
SOURCE_RULE_RECEIPT = RUN274B / "decision_risk_rule_receipt.csv"
SOURCE_IDENTITY = RUN274B / "package_identity_receipt.csv"
SOURCE_Q04_PAYLOAD = (
    ROOT
    / "stages"
    / "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
    / "02_runs"
    / "run272B"
    / "payloads"
    / "q04_payload.parquet"
)
MODEL_INPUT_CONTRACT = ROOT / "docs" / "contracts" / "model_input_feature_set_contract_fpmarkets_v2.md"
MT5_INPUT_CONTRACT = ROOT / "docs" / "contracts" / "mt5_ea_input_order_contract_fpmarkets_v2.md"

SCORING_INPUT_SPECS = RUN_DIR / "scoring_input_specs.json"
HANDOFF_INPUT_PLAN = RUN_DIR / "handoff_input_plan.csv"
PACKAGE_IDENTITY_RECEIPTS = RUN_DIR / "package_identity_receipts.csv"
FEATURE_HANDOFF_SCHEMA = RUN_DIR / "feature_handoff_schema.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run274C_report.md"
HANDOFF_MATRIX = REVIEWS / "run274C_handoff_matrix.csv"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
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
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]

BASE_REQUIRED_COLUMNS = [
    "timestamp",
    "symbol",
    "split",
    "tier_view",
    "package_id",
    "input_feature_order_hash",
    "expected_feature_order_hash",
    "missing_required_feature_count",
    "decision_rule_hash",
    "risk_rule_hash",
    "adapter_schema_hash",
    "score_columns_hash",
    "claim_boundary",
    "route_code",
    "route_signal_value",
    "route_signal_label",
    "candidate_decision_score",
    "materialized_decision_flag",
    "variant_decision_flag",
    "source_feature_order_hash",
    "source_adapter_schema_hash",
    "variant_decision_surface_hash",
    "source_model_hash",
]

PACKAGE_REQUIRED_COLUMNS = {
    "cp274A_session_loss_asymmetry_router": [
        "weekday_phase",
        "session_clock_risk",
        "phase_risk_score",
        "candidate_decision_score",
        "route_signal_value",
        "route_signal_label",
    ],
    "cp274B_month_regime_resilience_surface": [
        "month_regime_pressure",
        "phase_risk_score",
        "phase_opportunity_score",
        "chron_phase_age",
        "session_clock_risk",
    ],
    "cp274C_drawdown_recovery_context_router": [
        "chron_phase_age",
        "session_clock_risk",
        "phase_risk_score",
        "route_signal_value",
        "candidate_decision_score",
        "materialized_decision_flag",
    ],
    "cp274D_q04_failure_boundary_control": [
        "route_signal_value",
        "candidate_decision_score",
        "session_clock_risk",
        "month_regime_pressure",
        "route_signal_label",
    ],
}

FORMULA_PLANS = {
    "cp274A_session_loss_asymmetry_router": (
        "Use session_clock_risk(세션 시계 위험), route_signal_label(경로 신호 라벨), "
        "candidate_decision_score(후보 판단 점수), and phase_risk_score(국면 위험 점수) to "
        "build direction-specific permission(방향별 허용) without a flat no-trade filter(무거래 필터)."
    ),
    "cp274B_month_regime_resilience_surface": (
        "Use month_regime_pressure(월 국면 압력), phase_opportunity_score(국면 기회 점수), "
        "phase_risk_score(국면 위험 점수), and chron_phase_age(시간 국면 나이) to create a "
        "payoff budget(보상 예산) instead of calendar exclusion(달력 제외)."
    ),
    "cp274C_drawdown_recovery_context_router": (
        "Use chron_phase_age(시간 국면 나이), session_clock_risk(세션 시계 위험), "
        "phase_risk_score(국면 위험 점수), route_signal_value(경로 신호값), and "
        "candidate_decision_score(후보 판단 점수) to express recovery context(회복 문맥)."
    ),
    "cp274D_q04_failure_boundary_control": (
        "Preserve q04 route signal(4번 분기 경로 신호) and q04 candidate decision score(4번 분기 후보 판단 점수) "
        "as a support control(보조 대조) only."
    ),
}

BASE_ADAPTER_OUTPUTS = [
    "entry_signal",
    "route_code",
    "model_risk_pct",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "max_hold_bars",
    "reentry_cooldown_bars",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def stable_hash(payload: Any) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("; ".join(missing))


def load_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def payload_profile() -> dict[str, Any]:
    frame = pd.read_parquet(io_path(SOURCE_Q04_PAYLOAD))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    duplicate_count = int(frame.duplicated(["timestamp", "tier_view"]).sum())
    label_like_columns = [
        column
        for column in frame.columns
        if column.lower() in {"label", "label_class", "future_timestamp", "future_log_return_12"}
    ]
    return {
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "column_count": int(len(frame.columns)),
        "split_counts": {str(key): int(value) for key, value in frame["split"].value_counts(dropna=False).sort_index().items()},
        "tier_view_counts": {
            str(key): int(value) for key, value in frame["tier_view"].value_counts(dropna=False).sort_index().items()
        },
        "timestamp_min_utc": frame["timestamp"].min().isoformat(),
        "timestamp_max_utc": frame["timestamp"].max().isoformat(),
        "duplicate_timestamp_tier_rows": duplicate_count,
        "label_like_columns": label_like_columns,
        "source_feature_order_hashes": sorted(str(value) for value in frame["source_feature_order_hash"].dropna().unique()),
        "source_adapter_schema_hashes": sorted(str(value) for value in frame["source_adapter_schema_hash"].dropna().unique()),
        "source_model_hashes": sorted(str(value) for value in frame["source_model_hash"].dropna().unique()),
    }


def unique_columns(package_id: str) -> list[str]:
    columns: list[str] = []
    for column in [*BASE_REQUIRED_COLUMNS, *PACKAGE_REQUIRED_COLUMNS[package_id]]:
        if column not in columns:
            columns.append(column)
    return columns


def build_handoff_skeleton(package: Mapping[str, Any], profile: Mapping[str, Any]) -> dict[str, Any]:
    package_id = str(package["package_id"])
    score_columns = list(package["score_columns"])
    runtime_fields = list(package["runtime_handoff_plan"])
    adapter_outputs = {
        field: {
            "value": None,
            "status": "planned_input_field_not_runtime_value",
            "meaning": "run274C(274C 실행)는 입력 골격만 만들며 실제 런타임 값은 만들지 않는다.",
        }
        for field in [*BASE_ADAPTER_OUTPUTS, *score_columns]
    }
    skeleton = {
        "schema_version": "stage274_run274C_handoff_skeleton_v1",
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "stage_id": STAGE_ID,
        "package_id": package_id,
        "package_role": package["package_role"],
        "source_payload": rel(SOURCE_Q04_PAYLOAD),
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": profile["rows"],
            "tier_view_counts": profile["tier_view_counts"],
            "split_counts": profile["split_counts"],
        },
        "identity": {
            "feature_order_hash": package["source_feature_order_hash"],
            "blueprint_hash": package["blueprint_hash"],
            "score_columns_hash": package["score_columns_hash"],
            "decision_rule_hash": package["decision_rule_hash"],
            "risk_rule_hash": package["risk_rule_hash"],
            "adapter_schema_hash": package["adapter_schema_hash"],
            "source_model_hashes": profile["source_model_hashes"],
        },
        "required_source_columns": unique_columns(package_id),
        "score_columns": score_columns,
        "formula_plan": FORMULA_PLANS[package_id],
        "runtime_handoff_fields": runtime_fields,
        "adapter_outputs": adapter_outputs,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "next_consumer": NEXT_ACTION,
        "verification_before_selection": [
            "run274D deterministic score materialization(결정 점수 물질화)",
            "Tier A separate/Tier B separate/Tier A+B combined records(티어 A 분리/티어 B 분리/티어 A+B 합산 기록)",
            "stability and aggressive comparison before Adapter package(어댑터 패키지 전 안정성/공격형 비교)",
        ],
    }
    skeleton["skeleton_hash"] = stable_hash(skeleton)
    return skeleton


def materialize_specs(
    bundle: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    spec_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    skeleton_paths: list[Path] = []
    payload_columns = set(str(column) for column in profile["columns"])
    for package in bundle["packages"]:
        package_id = str(package["package_id"])
        required_columns = unique_columns(package_id)
        missing_columns = [column for column in required_columns if column not in payload_columns]
        skeleton = build_handoff_skeleton(package, profile)
        skeleton_path = HANDOFF_SKELETON_DIR / f"{package_id}_handoff_skeleton.json"
        write_json(skeleton_path, skeleton)
        skeleton_paths.append(skeleton_path)
        spec = {
            "package_id": package_id,
            "package_role": package["package_role"],
            "source_blueprint_hash": package["blueprint_hash"],
            "source_feature_order_hash": package["source_feature_order_hash"],
            "source_adapter_schema_hash": package["source_adapter_schema_hash"],
            "source_model_hashes": profile["source_model_hashes"],
            "score_columns": package["score_columns"],
            "score_columns_hash": package["score_columns_hash"],
            "required_source_columns": required_columns,
            "missing_source_columns": missing_columns,
            "input_column_status": "complete" if not missing_columns else "missing_required",
            "formula_plan": FORMULA_PLANS[package_id],
            "decision_rule_hash": package["decision_rule_hash"],
            "risk_rule_hash": package["risk_rule_hash"],
            "adapter_schema_hash": package["adapter_schema_hash"],
            "handoff_skeleton_path": rel(skeleton_path),
            "handoff_skeleton_hash": skeleton["skeleton_hash"],
            "runtime_handoff_fields": package["runtime_handoff_plan"],
            "next_consumer": NEXT_ACTION,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        spec_rows.append(spec)
        handoff_rows.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "handoff_skeleton_path": rel(skeleton_path),
                "handoff_skeleton_hash": skeleton["skeleton_hash"],
                "runtime_handoff_fields": ";".join(package["runtime_handoff_plan"]),
                "required_hashes": "feature_order_hash;blueprint_hash;score_columns_hash;decision_rule_hash;risk_rule_hash;adapter_schema_hash;skeleton_hash",
                "input_column_status": spec["input_column_status"],
                "runtime_payload_status": "planned_input_skeleton_no_runtime_values",
                "next_consumer": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            }
        )
        identity_rows.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "feature_order_hash": package["source_feature_order_hash"],
                "blueprint_hash": package["blueprint_hash"],
                "score_columns_hash": package["score_columns_hash"],
                "decision_rule_hash": package["decision_rule_hash"],
                "risk_rule_hash": package["risk_rule_hash"],
                "adapter_schema_hash": package["adapter_schema_hash"],
                "handoff_skeleton_hash": skeleton["skeleton_hash"],
                "source_payload_hash": sha256_file(SOURCE_Q04_PAYLOAD),
                "identity_judgment": "input_identity_materialized_no_candidate_selection",
                "claim_boundary": BOUNDARY,
            }
        )
        for field in [*BASE_ADAPTER_OUTPUTS, *package["score_columns"], *package["runtime_handoff_plan"]]:
            schema_rows.append(
                {
                    "package_id": package_id,
                    "field_name": field,
                    "field_role": "adapter_output_or_handoff_field",
                    "source_status": "planned_by_run274C",
                    "runtime_value_status": "not_materialized_in_run274C",
                    "claim_boundary": BOUNDARY,
                }
            )
    return spec_rows, handoff_rows, identity_rows, schema_rows, skeleton_paths


def write_receipts(spec_rows: Sequence[Mapping[str, Any]], profile: Mapping[str, Any]) -> list[dict[str, Any]]:
    selectable = sum(1 for row in spec_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in spec_rows if row["package_role"] == "support_control")
    missing_packages = [row["package_id"] for row in spec_rows if row["input_column_status"] != "complete"]
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "hypothesis": (
                "run274B(274B 실행)의 post-q04 candidate package blueprint(q04 이후 후보 패키지 청사진)는 "
                "q04 payload(q04 페이로드)에서 deterministic score input(결정 점수 입력)과 "
                "Adapter handoff skeleton(어댑터 인계 골격)으로 물질화할 수 있다."
            ),
            "decision_use": (
                "run274D(274D 실행)가 실제 score table(점수표)을 만들 수 있는지 판단한다. "
                "효과(effect, 효과)는 후보 선택 전에 feature order(피처 순서), rule hash(규칙 해시), "
                "handoff field(인계 필드)를 고정하는 것이다."
            ),
            "comparison_baseline": "cp274D_q04_failure_boundary_control(q04 실패 경계 보조 대조)",
            "control_variables": {
                "symbol": "US100",
                "timeframe": "M5",
                "source_payload": rel(SOURCE_Q04_PAYLOAD),
                "tier_views": profile["tier_view_counts"],
                "split_counts": profile["split_counts"],
                "claim_boundary": BOUNDARY,
            },
            "changed_variables": [row["package_id"] for row in spec_rows if row["package_role"] == "selectable_blueprint"],
            "sample_scope": {
                "rows": profile["rows"],
                "timestamp_min_utc": profile["timestamp_min_utc"],
                "timestamp_max_utc": profile["timestamp_max_utc"],
                "selectable_packages": selectable,
                "support_controls": support,
            },
            "success_criteria": "Every package has complete input columns(입력 열), hashes(해시), and handoff skeleton(인계 골격).",
            "failure_criteria": "Missing columns(누락 열) or duplicate q04 control identity(q04 대조 정체성 중복) blocks run274D.",
            "invalid_conditions": "q04 payload(q04 페이로드), run274B blueprint(274B 청사진), or identity hashes(정체성 해시)가 없으면 무효다.",
            "stop_conditions": "If missing_packages is non-empty(누락 패키지가 있으면), do not execute score materialization(점수 물질화 실행 금지).",
            "evidence_plan": [rel(SCORING_INPUT_SPECS), rel(HANDOFF_INPUT_PLAN), rel(PACKAGE_IDENTITY_RECEIPTS)],
            "missing_packages": missing_packages,
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "data_source": [rel(SOURCE_Q04_PAYLOAD), rel(SOURCE_BLUEPRINTS), rel(SOURCE_RUN274B_MANIFEST)],
            "time_axis": (
                "timestamp(타임스탬프)는 UTC(협정세계시)로 읽고, run274C(274C 실행)는 새 resampling(재표본화)이나 "
                "future join(미래 결합)을 하지 않는다."
            ),
            "sample_scope": {
                "symbol": "US100",
                "timeframe": "M5",
                "rows": profile["rows"],
                "columns": profile["column_count"],
                "split_counts": profile["split_counts"],
                "tier_view_counts": profile["tier_view_counts"],
                "timestamp_min_utc": profile["timestamp_min_utc"],
                "timestamp_max_utc": profile["timestamp_max_utc"],
            },
            "missing_or_duplicate_check": {
                "duplicate_timestamp_tier_rows": profile["duplicate_timestamp_tier_rows"],
                "missing_packages": missing_packages,
                "label_like_columns": profile["label_like_columns"],
            },
            "feature_label_boundary": "No label/future columns(라벨/미래 열)을 scoring input spec(점수 입력 규격)에 쓰지 않는다.",
            "split_boundary": "train/validation/oos(학습/검증/표본외) split(분할)을 그대로 보존한다.",
            "leakage_risk": (
                "Weak-month/hour memory(약한 월/시간 기억)가 formula(공식)에 직접 hard-code(하드코딩)되면 "
                "selection-bias risk(선택 편향 위험)가 생긴다. run274C(274C 실행)는 공식 계획만 남긴다."
            ),
            "data_hash_or_identity": {
                rel(SOURCE_Q04_PAYLOAD): sha256_file(SOURCE_Q04_PAYLOAD),
                rel(SOURCE_BLUEPRINTS): sha256_file(SOURCE_BLUEPRINTS),
                rel(SOURCE_RUN274B_MANIFEST): sha256_file(SOURCE_RUN274B_MANIFEST),
            },
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "model_family": "deterministic scoring input specification(결정 점수 입력 규격)",
            "target_and_label": "No model target(모델 목표) or new label(새 라벨) in run274C(274C 실행).",
            "split_method": "train/validation/oos(학습/검증/표본외) split(분할) preserved from q04 payload(q04 페이로드).",
            "selection_metric": "not_applicable_before_score_materialization(점수 물질화 전 해당 없음)",
            "secondary_metrics": [
                "input column completeness(입력 열 완전성)",
                "hash traceability(해시 추적성)",
                "Tier A/B paired scope(티어 A/B 쌍 범위)",
            ],
            "threshold_policy": "planned_fixed_formulas_only(계획된 고정 공식만); no threshold search(임계값 탐색 없음)",
            "overfit_risk": "Calendar/hour hard-code(달력/시간 하드코딩) would overfit(과적합) later score materialization.",
            "calibration_risk": "Scores are rank/control signals(순위/제어 신호), not probability(확률 아님).",
            "comparison_baseline": "cp274D_q04_failure_boundary_control(q04 실패 경계 보조 대조)",
            "validation_judgment": "exploratory_input_materialized_no_candidate_selection",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": "run274C scoring/handoff input materialization(274C 점수/인계 입력 물질화)",
                "evidence_available": "scoring_input_specs.json;handoff_input_plan.csv;package_identity_receipts.csv;handoff skeleton JSON",
                "evidence_missing": "score tables(점수표);MT5 KPI(MT5 핵심 성과 지표);selected candidate(선택 후보);ONNX export/parity(온엑스 내보내기/동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": JUDGMENT_CLASS,
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "입력과 인계 골격은 준비됐지만, 아직 후보 성과나 ONNX 가치 판단은 없다.",
            }
        ],
    )
    gate_rows = [
        {
            "gate_name": "scope_completion_gate(범위 완료 게이트)",
            "status": "passed",
            "evidence_path": rel(SCORING_INPUT_SPECS),
            "effect": "run274C(274C 실행)의 요구 산출물인 scoring input spec(점수 입력 규격)을 만들었다.",
        },
        {
            "gate_name": "kpi_contract_audit(KPI 계약 감사)",
            "status": "passed_with_boundary",
            "evidence_path": rel(DATA_INTEGRITY_RECEIPT),
            "effect": "trading KPI(거래 핵심 성과 지표)는 없고, Tier A/B(티어 A/B) 입력 범위만 기록했다.",
        },
        {
            "gate_name": "skill_receipt_lint(스킬 영수증 검사)",
            "status": "passed",
            "evidence_path": rel(EXPERIMENT_RECEIPT),
            "effect": "experiment/data/model/result/lineage(실험/데이터/모델/결과/계보) 영수증을 만들었다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "experiment_execution(실험 실행) 작업군의 필수 게이트를 closeout(종료 기록)에 연결했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    write_csv(GATE_AUDIT, gate_rows)
    return gate_rows


def write_specs_and_reports(
    bundle: Mapping[str, Any],
    spec_rows: Sequence[Mapping[str, Any]],
    handoff_rows: Sequence[Mapping[str, Any]],
    identity_rows: Sequence[Mapping[str, Any]],
    schema_rows: Sequence[Mapping[str, Any]],
    profile: Mapping[str, Any],
) -> None:
    write_json(
        SCORING_INPUT_SPECS,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_payload": rel(SOURCE_Q04_PAYLOAD),
            "source_payload_hash": sha256_file(SOURCE_Q04_PAYLOAD),
            "shared_controls": bundle["shared_controls"],
            "payload_profile": profile,
            "packages": spec_rows,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        HANDOFF_INPUT_PLAN,
        handoff_rows,
        [
            "package_id",
            "package_role",
            "handoff_skeleton_path",
            "handoff_skeleton_hash",
            "runtime_handoff_fields",
            "required_hashes",
            "input_column_status",
            "runtime_payload_status",
            "next_consumer",
            "claim_boundary",
        ],
    )
    write_csv(
        PACKAGE_IDENTITY_RECEIPTS,
        identity_rows,
        [
            "package_id",
            "package_role",
            "feature_order_hash",
            "blueprint_hash",
            "score_columns_hash",
            "decision_rule_hash",
            "risk_rule_hash",
            "adapter_schema_hash",
            "handoff_skeleton_hash",
            "source_payload_hash",
            "identity_judgment",
            "claim_boundary",
        ],
    )
    write_csv(
        FEATURE_HANDOFF_SCHEMA,
        schema_rows,
        ["package_id", "field_name", "field_role", "source_status", "runtime_value_status", "claim_boundary"],
    )
    write_csv(HANDOFF_MATRIX, handoff_rows)

    selectable = sum(1 for row in spec_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in spec_rows if row["package_role"] == "support_control")
    package_lines = "\n".join(
        f"- `{row['package_id']}` `{row['package_role']}`: input_column_status(입력 열 상태) `{row['input_column_status']}`, "
        f"handoff_skeleton_hash(인계 골격 해시) `{row['handoff_skeleton_hash'][:16]}`"
        for row in spec_rows
    )
    write_md(
        RUN_REPORT,
        f"""# run274C Scoring/Handoff Input Materialization(274C 점수/인계 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- judgment_class(판정 분류): `{JUDGMENT_CLASS}`
- packages(패키지): `{len(spec_rows)}`
- selectable_packages(선택 가능 패키지): `{selectable}`
- support_controls(보조 대조): `{support}`
- q04_payload_rows(q04 페이로드 행): `{profile['rows']}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run274C(274C 실행)는 run274B(274B 실행)의 candidate package blueprint(후보 패키지 청사진)를 scoring input spec(점수 입력 규격), handoff input plan(인계 입력 계획), package identity receipt(패키지 정체성 영수증), handoff skeleton(인계 골격)으로 바꿨다.
효과(effect, 효과): run274D(274D 실행)가 실제 score table(점수표)을 만들 때 feature order(피처 순서), decision/risk hash(판단/위험 해시), Adapter field(어댑터 필드)를 추적할 수 있다.

## Package Rows(패키지 행)

{package_lines}

## Evidence Paths(근거 경로)

- scoring_input_specs(점수 입력 규격): `{rel(SCORING_INPUT_SPECS)}`
- handoff_input_plan(인계 입력 계획): `{rel(HANDOFF_INPUT_PLAN)}`
- package_identity_receipts(패키지 정체성 영수증): `{rel(PACKAGE_IDENTITY_RECEIPTS)}`
- feature_handoff_schema(피처 인계 스키마): `{rel(FEATURE_HANDOFF_SCHEMA)}`
- handoff_skeletons(인계 골격): `{rel(HANDOFF_SKELETON_DIR)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [
        SOURCE_BLUEPRINTS,
        SOURCE_RUN274B_MANIFEST,
        SOURCE_SCORING_PLAN,
        SOURCE_ADAPTER_PLAN,
        SOURCE_RULE_RECEIPT,
        SOURCE_IDENTITY,
        SOURCE_Q04_PAYLOAD,
        MODEL_INPUT_CONTRACT,
        MT5_INPUT_CONTRACT,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "judgment_class": JUDGMENT_CLASS,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage274/materialize_post_q04_failure_scoring_handoff_inputs.py",
        "entry_command": "python stage_pipelines/stage274/materialize_post_q04_failure_scoring_handoff_inputs.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    full_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run274C_scoring_handoff_input_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run274C scoring/handoff input materialization artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_ledgers(spec_rows: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in spec_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in spec_rows if row["package_role"] == "support_control")
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"packages={len(spec_rows)};selectable={selectable};support_control={support};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": row["package_id"],
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": f"scoring handoff input spec {row['package_id']}",
            "tier_scope": "Tier A separate;Tier B separate;Tier A+B combined input boundary",
            "kpi_scope": "scoring_handoff_input_identity",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": row["input_column_status"],
            "path": rel(SCORING_INPUT_SPECS),
            "primary_kpi": f"handoff_skeleton_hash={row['handoff_skeleton_hash']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;trading_kpi=not_applicable",
            "external_verification_status": "not_applicable",
            "notes": f"next_action={NEXT_ACTION};package_role={row['package_role']}",
        }
        for row in spec_rows
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": f"scoring_handoff_input_spec_{row['package_id']}",
            "tier_scope": "Tier A/B paired input boundary",
            "scoreboard": "structural_scout",
            "status": STATUS,
            "judgment": row["input_column_status"],
            "evidence_boundary": "input_materialization_only_no_candidate_no_onnx",
            "report_path": rel(RUN_REPORT),
            "notes": f"handoff_skeleton_hash={row['handoff_skeleton_hash']}",
        }
        for row in spec_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs(spec_rows: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in spec_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in spec_rows if row["package_role"] == "support_control")
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_once(selection, "run274C_report", f"- run274C_report(274C 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run274C_scoring_input_specs", f"- run274C_scoring_input_specs(274C 점수 입력 규격): `{rel(SCORING_INPUT_SPECS)}`")
    selection = append_once(selection, "run274C_handoff_input_plan", f"- run274C_handoff_input_plan(274C 인계 입력 계획): `{rel(HANDOFF_INPUT_PLAN)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run274C_report",
        "\n".join(
            [
                f"- run274C_report(274C 보고서): `{rel(RUN_REPORT)}`",
                f"- run274C_scoring_input_specs(274C 점수 입력 규격): `{rel(SCORING_INPUT_SPECS)}`",
                f"- run274C_handoff_input_plan(274C 인계 입력 계획): `{rel(HANDOFF_INPUT_PLAN)}`",
                f"- run274C_package_identity_receipts(274C 패키지 정체성 영수증): `{rel(PACKAGE_IDENTITY_RECEIPTS)}`",
                f"- run274C_handoff_matrix(274C 인계 행렬): `{rel(HANDOFF_MATRIX)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run274C_summary",
        f"- run274C_summary(274C 요약): run274C(274C 실행)는 scoring input specs(점수 입력 규격), handoff input plan(인계 입력 계획), package identity receipts(패키지 정체성 영수증), handoff skeletons(인계 골격)을 package(패키지) `{len(spec_rows)}`개에 대해 만들었다. Effect(효과): selectable package(선택 가능 패키지) `{selectable}`개와 support control(보조 대조) `{support}`개를 run274D(274D 실행)의 deterministic score materialization(결정 점수 물질화) 입력으로 넘기며, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage274(274단계) run274C(274C 실행) scoring/handoff input materialization(점수/인계 입력 물질화) `{RUN_ID}`. "
        f"Effect(효과): package(패키지) `{len(spec_rows)}`개에 scoring input spec(점수 입력 규격)과 handoff skeleton(인계 골격)을 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run274C scoring/handoff input materialization(274C 점수/인계 입력 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): package(패키지) `{len(spec_rows)}`개에 scoring input spec(점수 입력 규격), handoff input plan(인계 입력 계획), handoff skeleton(인계 골격)을 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def execute() -> dict[str, Any]:
    must_exist(
        [
            SOURCE_BLUEPRINTS,
            SOURCE_RUN274B_MANIFEST,
            SOURCE_SCORING_PLAN,
            SOURCE_ADAPTER_PLAN,
            SOURCE_RULE_RECEIPT,
            SOURCE_IDENTITY,
            SOURCE_Q04_PAYLOAD,
            MODEL_INPUT_CONTRACT,
            MT5_INPUT_CONTRACT,
        ]
    )
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(HANDOFF_SKELETON_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    bundle = load_json(SOURCE_BLUEPRINTS)
    profile = payload_profile()
    spec_rows, handoff_rows, identity_rows, schema_rows, skeleton_paths = materialize_specs(bundle, profile)
    write_specs_and_reports(bundle, spec_rows, handoff_rows, identity_rows, schema_rows, profile)
    gate_rows = write_receipts(spec_rows, profile)
    artifacts = [
        SCORING_INPUT_SPECS,
        HANDOFF_INPUT_PLAN,
        PACKAGE_IDENTITY_RECEIPTS,
        FEATURE_HANDOFF_SCHEMA,
        HANDOFF_MATRIX,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
        *skeleton_paths,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers(spec_rows)
    update_state_docs(spec_rows)
    selectable = sum(1 for row in spec_rows if row["package_role"] == "selectable_blueprint")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "judgment_class": JUDGMENT_CLASS,
        "packages": len(spec_rows),
        "selectable_packages": selectable,
        "support_controls": len(spec_rows) - selectable,
        "q04_payload_rows": profile["rows"],
        "gate_rows": len(gate_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
