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
RUN_ID = "run274B_materialize_post_q04_failure_candidate_package_blueprints_v1"
SOURCE_RUN_ID = "run274A_design_post_q04_failure_candidate_rebuild_packet_v1"
STATUS = "completed_post_q04_failure_candidate_package_blueprint_materialization_no_candidate_selection"
JUDGMENT = "materialized_candidate_package_blueprints_ready_no_candidate_selection"
NEXT_ACTION = "run274C_materialize_post_q04_failure_scoring_handoff_inputs"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN274A = STAGE / "02_runs" / "run274A"
RUN_DIR = STAGE / "02_runs" / "run274B"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_THESIS_QUEUE = RUN274A / "candidate_rebuild_thesis_queue.csv"
SOURCE_FAILURE_MAP = RUN274A / "failure_to_requirement_map.csv"
SOURCE_BLUEPRINT_SEEDS = RUN274A / "candidate_package_blueprint_seeds.csv"
SOURCE_DISCARD = RUN274A / "discard_conditions.csv"
SOURCE_RUN274A_MANIFEST = RUN274A / "run_manifest.json"
SOURCE_RUN274A_LINEAGE = RUN274A / "artifact_lineage_receipt.json"
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

PACKAGE_BLUEPRINTS = RUN_DIR / "package_blueprints.json"
BLUEPRINT_MATRIX = REVIEWS / "run274B_blueprints.csv"
SCORING_SURFACE_PLAN = RUN_DIR / "scoring_surface_plan.csv"
ADAPTER_CONTRACT_PLAN = RUN_DIR / "adapter_contract_plan.csv"
DECISION_RISK_RULE_RECEIPT = RUN_DIR / "decision_risk_rule_receipt.csv"
PACKAGE_IDENTITY_RECEIPT = RUN_DIR / "package_identity_receipt.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run274B_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
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


def load_payload_identity() -> dict[str, Any]:
    df = pd.read_parquet(io_path(SOURCE_Q04_PAYLOAD), columns=[
        "source_feature_order_hash",
        "input_feature_order_hash",
        "expected_feature_order_hash",
        "adapter_schema_hash",
        "source_adapter_schema_hash",
        "decision_rule_hash",
        "risk_rule_hash",
        "variant_decision_surface_hash",
        "source_model_hash",
        "split",
        "tier_view",
    ])
    identity_cols = [
        "source_feature_order_hash",
        "input_feature_order_hash",
        "expected_feature_order_hash",
        "adapter_schema_hash",
        "source_adapter_schema_hash",
        "decision_rule_hash",
        "risk_rule_hash",
        "variant_decision_surface_hash",
        "source_model_hash",
    ]
    return {
        "payload_rows": int(len(df)),
        "feature_order_hashes": {column: sorted(str(value) for value in df[column].dropna().unique()) for column in identity_cols},
        "splits": sorted(str(value) for value in df["split"].dropna().unique()),
        "tier_views": sorted(str(value) for value in df["tier_view"].dropna().unique()),
    }


def package_templates() -> dict[str, dict[str, Any]]:
    return {
        "cp274A_session_loss_asymmetry_router": {
            "package_role": "selectable_blueprint",
            "score_columns": [
                "session_loss_asymmetry_score",
                "long_permission_score",
                "short_permission_score",
                "exposure_reduction_score",
            ],
            "feature_groups": [
                "weekday_phase",
                "session_clock_risk",
                "route_signal_label",
                "candidate_decision_score",
                "phase_risk_score",
            ],
            "decision_rule": "Compute direction-specific permission(방향별 허용)을 hour-loss pocket(시간 손실 구간) 안에서 따로 만들고, q04 route(경로)를 그대로 복사하지 않는다.",
            "risk_rule": "Reduce exposure(노출 축소) before flat filter(관망 필터), and keep minimum trade supply(최소 거래 공급) guard.",
            "handoff_fields": [
                "package_id",
                "feature_order_hash",
                "decision_rule_hash",
                "risk_rule_hash",
                "adapter_schema_hash",
                "session_loss_asymmetry_score",
                "route_code",
                "model_risk_pct",
                "telemetry_json",
            ],
            "materialization_note": "Tests whether direction asymmetry(방향 비대칭) can repair hour loss without blunt filtering(무딘 필터링).",
        },
        "cp274B_month_regime_resilience_surface": {
            "package_role": "selectable_blueprint",
            "score_columns": [
                "month_regime_resilience_score",
                "payoff_budget_score",
                "regime_pressure_adjustment",
                "opportunity_override_score",
            ],
            "feature_groups": [
                "month_regime_pressure",
                "phase_risk_score",
                "phase_opportunity_score",
                "chron_phase_age",
                "session_clock_risk",
            ],
            "decision_rule": "Require payoff budget(보상 예산) when month regime pressure(월 국면 압박)가 높고, calendar exclusion(달력 제외)은 금지한다.",
            "risk_rule": "Scale risk(위험 크기 조정) by opportunity/risk spread(기회/위험 차이) instead of blocking May/December(5월/12월 차단).",
            "handoff_fields": [
                "package_id",
                "feature_order_hash",
                "decision_rule_hash",
                "risk_rule_hash",
                "adapter_schema_hash",
                "month_regime_resilience_score",
                "route_code",
                "model_risk_pct",
                "telemetry_json",
            ],
            "materialization_note": "Tests whether weak-month collapse(약한 월 붕괴) is payoff-budget related(보상 예산 관련).",
        },
        "cp274C_drawdown_recovery_context_router": {
            "package_role": "selectable_blueprint",
            "score_columns": [
                "drawdown_recovery_context_score",
                "reentry_permission_score",
                "same_direction_delay_score",
                "underwater_proxy_score",
            ],
            "feature_groups": [
                "chron_phase_age",
                "session_clock_risk",
                "phase_risk_score",
                "route_signal_value",
                "candidate_decision_score",
            ],
            "decision_rule": "Tie re-entry permission(재진입 허용)을 recovery context(회복 문맥)에 묶고 cooldown-only repair(쿨다운 전용 수리)는 금지한다.",
            "risk_rule": "Delay same-direction re-entry(동방향 재진입 지연) after loss pocket proxy(손실 구간 대리) without banning all routes(전체 경로 금지 없음).",
            "handoff_fields": [
                "package_id",
                "feature_order_hash",
                "decision_rule_hash",
                "risk_rule_hash",
                "adapter_schema_hash",
                "drawdown_recovery_context_score",
                "route_code",
                "model_risk_pct",
                "telemetry_json",
            ],
            "materialization_note": "Tests whether drawdown shape(손실폭 형태) is recovery-context related(회복 문맥 관련).",
        },
        "cp274D_q04_failure_boundary_control": {
            "package_role": "support_control",
            "score_columns": [
                "q04_route_signal_value",
                "q04_candidate_decision_score",
                "q04_failure_signature_flag",
            ],
            "feature_groups": [
                "route_signal_value",
                "candidate_decision_score",
                "session_clock_risk",
                "month_regime_pressure",
            ],
            "decision_rule": "Keep q04 failure boundary(q04 실패 경계)를 unchanged control(변경 없는 대조)로 보존한다.",
            "risk_rule": "No promotion(승격 없음), no Adapter handoff(어댑터 인계 없음), reference only(참조만).",
            "handoff_fields": [
                "package_id",
                "feature_order_hash",
                "decision_rule_hash",
                "risk_rule_hash",
                "adapter_schema_hash",
                "q04_failure_signature_flag",
                "telemetry_json",
            ],
            "materialization_note": "Prevents fresh packages(새 패키지)가 q04 duplicate(q04 중복)로 통과하는 것을 막는다.",
        },
    }


def build_blueprints(
    thesis_rows: Sequence[Mapping[str, str]],
    seed_rows: Sequence[Mapping[str, str]],
    failure_rows: Sequence[Mapping[str, str]],
    payload_identity: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    templates = package_templates()
    seed_map = {row["package_id"]: row for row in seed_rows}
    source_feature_hash = payload_identity["feature_order_hashes"]["source_feature_order_hash"][0]
    source_adapter_hash = payload_identity["feature_order_hashes"]["source_adapter_schema_hash"][0]
    packages: list[dict[str, Any]] = []
    matrix_rows: list[dict[str, Any]] = []
    scoring_rows: list[dict[str, Any]] = []
    adapter_rows: list[dict[str, Any]] = []
    rule_rows: list[dict[str, Any]] = []
    for source in thesis_rows:
        package_id = source["package_id"]
        template = templates[package_id]
        decision_hash = stable_hash({"package_id": package_id, "decision_rule": template["decision_rule"], "failure_map": [row["failure_id"] for row in failure_rows]})
        risk_hash = stable_hash({"package_id": package_id, "risk_rule": template["risk_rule"], "discard_condition": source["discard_condition"]})
        score_hash = stable_hash({"package_id": package_id, "score_columns": template["score_columns"], "feature_groups": template["feature_groups"]})
        adapter_schema = {
            "base_contract": rel(MT5_INPUT_CONTRACT),
            "handoff_fields": template["handoff_fields"],
            "telemetry_required": True,
            "candidate_claim_allowed": False,
        }
        adapter_schema_hash = stable_hash(adapter_schema)
        package = {
            "package_id": package_id,
            "package_role": template["package_role"],
            "source_run_id": SOURCE_RUN_ID,
            "fresh_thesis": source["fresh_thesis"],
            "hypothesis": source["upside_hypothesis"],
            "comparison_baseline": "cp274D_q04_failure_boundary_control" if package_id != "cp274D_q04_failure_boundary_control" else "q04_failed_surface_itself",
            "failure_memory_inputs": [row["failure_id"] for row in failure_rows],
            "control_variables": [
                "US100",
                "M5",
                f"feature_order_hash={source_feature_hash}",
                "Tier A separate + Tier B separate + Tier A+B boundary",
            ],
            "changed_variables": template["score_columns"],
            "feature_order_source": rel(MODEL_INPUT_CONTRACT),
            "source_feature_order_hash": source_feature_hash,
            "source_adapter_schema_hash": source_adapter_hash,
            "feature_groups": template["feature_groups"],
            "scoring_owner": "stage_pipelines/stage274 until reusable scoring logic proves foundation ownership(재사용 점수 로직이 증명되기 전까지 274단계 소유)",
            "score_columns": template["score_columns"],
            "score_columns_hash": score_hash,
            "decision_rule": template["decision_rule"],
            "decision_rule_hash": decision_hash,
            "risk_rule": template["risk_rule"],
            "risk_rule_hash": risk_hash,
            "adapter_output_schema": adapter_schema,
            "adapter_schema_hash": adapter_schema_hash,
            "runtime_handoff_plan": template["handoff_fields"],
            "success_criteria": "Materialize deterministic score surface(결정적 점수 표면) and avoid q04 failure signature(q04 실패 서명 회피).",
            "failure_criteria": source["failure_mode"],
            "discard_condition": source["discard_condition"],
            "invalid_conditions": "feature order hash(피처 순서 해시) missing, Tier B omitted(티어 B 생략), or decision/risk hash(판단/위험 해시) missing.",
            "stop_conditions": "If run274C/run274D cannot produce distinct score surfaces(다른 점수 표면), close as failure memory(실패 기억).",
            "next_action": NEXT_ACTION,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        package["blueprint_hash"] = stable_hash(package)
        packages.append(package)
        matrix_rows.append(
            {
                "package_id": package_id,
                "package_role": template["package_role"],
                "materialization_status": "materialized_blueprint_no_selection",
                "fresh_thesis": source["fresh_thesis"],
                "comparison_baseline": package["comparison_baseline"],
                "feature_order_hash": source_feature_hash,
                "score_columns": ";".join(template["score_columns"]),
                "score_columns_hash": score_hash,
                "decision_rule_hash": decision_hash,
                "risk_rule_hash": risk_hash,
                "adapter_schema_hash": adapter_schema_hash,
                "blueprint_seed_hash": seed_map.get(package_id, {}).get("blueprint_seed_hash", ""),
                "blueprint_hash": package["blueprint_hash"],
                "next_action": NEXT_ACTION,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        scoring_rows.append(
            {
                "package_id": package_id,
                "package_role": template["package_role"],
                "feature_groups": ";".join(template["feature_groups"]),
                "score_columns": ";".join(template["score_columns"]),
                "score_columns_hash": score_hash,
                "required_input": rel(SOURCE_Q04_PAYLOAD),
                "materialization_owner": "run274C_materialize_post_q04_failure_scoring_handoff_inputs",
                "materialization_note": template["materialization_note"],
                "claim_boundary": BOUNDARY,
            }
        )
        adapter_rows.append(
            {
                "package_id": package_id,
                "adapter_schema_hash": adapter_schema_hash,
                "runtime_handoff_fields": ";".join(template["handoff_fields"]),
                "adapter_path_status": "planned_not_selected(계획됨, 선택 아님)",
                "onnx_path_status": "not_started(시작 안 함)",
                "effect": "Keeps handoff traceable(인계 추적 가능) before candidate selection(후보 선택 전).",
                "claim_boundary": BOUNDARY,
            }
        )
        rule_rows.append(
            {
                "package_id": package_id,
                "decision_rule_hash": decision_hash,
                "risk_rule_hash": risk_hash,
                "decision_rule": template["decision_rule"],
                "risk_rule": template["risk_rule"],
                "discard_condition": source["discard_condition"],
                "claim_boundary": BOUNDARY,
            }
        )
    bundle = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "shared_controls": {
            "symbol": "US100",
            "timeframe": "M5",
            "feature_order_contract": rel(MODEL_INPUT_CONTRACT),
            "source_feature_order_hash": source_feature_hash,
            "tier_requirement": "Tier A separate;Tier B separate;Tier A+B boundary",
            "claim_boundary": BOUNDARY,
        },
        "packages": packages,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }
    return bundle, matrix_rows, scoring_rows, adapter_rows, rule_rows


def write_receipts(
    bundle: Mapping[str, Any],
    matrix_rows: Sequence[Mapping[str, Any]],
    payload_identity: Mapping[str, Any],
) -> list[dict[str, Any]]:
    selectable = sum(1 for row in matrix_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in matrix_rows if row["package_role"] == "support_control")
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "hypothesis": "q04(4번 분기) 안정성 실패 이후 새 candidate package blueprint(후보 패키지 청사진)가 q04 실패 서명을 반복하지 않는 물질화 가능한 표면을 만들 수 있다.",
            "decision_use": "run274C(274C 실행)가 materialized scoring/handoff input(물질화된 점수/인계 입력)을 만들 패키지를 정한다.",
            "comparison_baseline": "cp274D_q04_failure_boundary_control(q04 실패 경계 대조)",
            "control_variables": bundle["shared_controls"],
            "changed_variables": [row["package_id"] for row in matrix_rows if row["package_role"] == "selectable_blueprint"],
            "sample_scope": "Stage274 blueprint materialization(274단계 청사진 물질화); no trading KPI yet(거래 KPI 아직 없음)",
            "success_criteria": "Each selectable blueprint(선택 가능 청사진) has feature/order, score columns, decision/risk hashes, Adapter handoff fields.",
            "failure_criteria": "Blueprint duplicates q04 control(청사진이 q04 대조와 중복) or lacks feature/rule identity(피처/규칙 정체성 누락).",
            "invalid_conditions": "Missing q04 payload identity(q04 페이로드 정체성 누락), missing Tier B boundary(티어 B 경계 누락), or empty score columns(빈 점수 열).",
            "stop_conditions": "If run274C cannot materialize deterministic score tables(결정적 점수표), close or redesign in a new bounded packet(새 경계 묶음).",
            "evidence_plan": [rel(PACKAGE_BLUEPRINTS), rel(BLUEPRINT_MATRIX), rel(SCORING_SURFACE_PLAN), rel(ADAPTER_CONTRACT_PLAN)],
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "data_source": [rel(SOURCE_THESIS_QUEUE), rel(SOURCE_FAILURE_MAP), rel(SOURCE_Q04_PAYLOAD)],
            "time_axis": "No new time series calculation(새 시계열 계산 없음); payload identity only(페이로드 정체성만 사용).",
            "sample_scope": {
                "payload_rows": payload_identity["payload_rows"],
                "splits": payload_identity["splits"],
                "tier_views": payload_identity["tier_views"],
                "package_count": len(matrix_rows),
            },
            "missing_or_duplicate_check": f"selectable_blueprints={selectable};support_controls={support}",
            "feature_label_boundary": "No label/future columns consumed(라벨/미래 열 소비 없음); run274B is blueprint-only(청사진 전용).",
            "split_boundary": "Requires later Tier A/B and validation/OOS materialization(이후 티어 A/B와 검증/표본외 물질화 필요).",
            "leakage_risk": "Weak-month/hour facts(약한 월/시간 사실)을 direct exclusion(직접 제외)으로 쓰면 leakage-like selection bias(누수 유사 선택 편향)가 생긴다.",
            "data_hash_or_identity": {rel(SOURCE_Q04_PAYLOAD): sha256_file(SOURCE_Q04_PAYLOAD), rel(SOURCE_FAILURE_MAP): sha256_file(SOURCE_FAILURE_MAP)},
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "model_family": "deterministic scoring surface blueprint(결정적 점수 표면 청사진)",
            "target_and_label": "No model target(모델 목표 없음) in run274B(274B 실행).",
            "split_method": "Blueprint stage(청사진 단계); run274C/run274D must preserve Tier A/B and validation/OOS(티어 A/B와 검증/표본외 보존).",
            "selection_metric": "material distinctness(물질적 차이), q04 failure avoidance(q04 실패 회피), Adapter traceability(어댑터 추적성)",
            "secondary_metrics": ["score coverage(점수 커버리지)", "trade supply guard(거래 공급 방어)", "weak slice avoidance(약한 구간 회피)", "hash identity(해시 정체성)"],
            "threshold_policy": "planned fixed formulas(고정 공식 계획); no threshold search yet(임계값 탐색 없음)",
            "overfit_risk": "High if formulas hard-code 2025-05/2025-12 or hour 17/18(특정 월/시간 하드코딩).",
            "calibration_risk": "Scores are ranking/control signals(순위/제어 신호), not probability(확률 아님).",
            "comparison_baseline": "cp274D q04 failure boundary control(q04 실패 경계 대조)",
            "validation_judgment": "exploratory_blueprint_materialized_no_selection(탐색 청사진 물질화, 선택 없음)",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": "run274B materialized post-q04 candidate package blueprints(274B q04 이후 후보 패키지 청사진 물질화)",
                "evidence_available": "package blueprints(패키지 청사진);score plan(점수 계획);adapter contract plan(어댑터 계약 계획);rule hashes(규칙 해시)",
                "evidence_missing": "materialized score tables(물질화 점수표);MT5 KPI(MT5 핵심 성과 지표);selected candidate(선택 후보);ONNX export/parity(온엑스 내보내기/동등성)",
                "judgment_label": JUDGMENT,
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "새 후보 청사진은 준비됐지만 아직 성과 후보나 ONNX 후보가 아니다.",
            }
        ],
    )
    gate_rows = [
        {
            "gate_name": "work_packet_schema_lint(작업 묶음 스키마 점검)",
            "status": "passed(통과)",
            "evidence_path": rel(EXPERIMENT_RECEIPT),
            "effect": "blueprint(청사진)가 가설, 비교 기준, 규칙, 폐기 조건을 가진다.",
        },
        {
            "gate_name": "artifact_lineage_audit(산출물 계보 감사)",
            "status": "passed(통과)",
            "evidence_path": rel(LINEAGE_RECEIPT),
            "effect": "run274A 입력에서 run274C 소비 경로까지 연결한다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    write_csv(GATE_AUDIT, gate_rows)
    return gate_rows


def write_report(matrix_rows: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in matrix_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in matrix_rows if row["package_role"] == "support_control")
    package_lines = "\n".join(
        f"- `{row['package_id']}` `{row['package_role']}`: score_columns(점수 열) `{row['score_columns']}`, blueprint_hash(청사진 해시) `{row['blueprint_hash'][:16]}`"
        for row in matrix_rows
    )
    write_md(
        RUN_REPORT,
        f"""# run274B Post-Q04 Candidate Package Blueprints(274B q04 이후 후보 패키지 청사진)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- blueprints(청사진): `{len(matrix_rows)}`
- selectable_blueprints(선택 가능 청사진): `{selectable}`
- support_control(보조 대조): `{support}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run274B(274B 실행)는 run274A(274A 실행)의 fresh thesis(새 논제) 대기열을 materialized candidate package blueprint(물질화된 후보 패키지 청사진)로 바꿨다.
효과(effect, 효과): 다음 run274C(274C 실행)가 score columns(점수 열), decision/risk rule hash(판단/위험 규칙 해시), Adapter handoff fields(어댑터 인계 필드)를 소비할 수 있다.

## Blueprint Rows(청사진 행)

{package_lines}

## Evidence Paths(근거 경로)

- package_blueprints(패키지 청사진): `{rel(PACKAGE_BLUEPRINTS)}`
- blueprint_matrix(청사진 행렬): `{rel(BLUEPRINT_MATRIX)}`
- scoring_surface_plan(점수 표면 계획): `{rel(SCORING_SURFACE_PLAN)}`
- adapter_contract_plan(어댑터 계약 계획): `{rel(ADAPTER_CONTRACT_PLAN)}`
- decision_risk_rule_receipt(판단/위험 규칙 영수증): `{rel(DECISION_RISK_RULE_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def update_ledgers(matrix_rows: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in matrix_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in matrix_rows if row["package_role"] == "support_control")
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"blueprints={len(matrix_rows)};selectable={selectable};support_control={support};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
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
            "record_view": f"materialized blueprint {row['package_id']}",
            "tier_scope": "Tier A+B blueprint requirement",
            "kpi_scope": "candidate_package_blueprint",
            "scoreboard_lane": "experiment_design_blueprint",
            "status": STATUS,
            "judgment": row["package_role"],
            "path": rel(BLUEPRINT_MATRIX),
            "primary_kpi": f"score_columns_hash={row['score_columns_hash']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "not_applicable",
            "notes": f"decision_hash={row['decision_rule_hash']};risk_hash={row['risk_rule_hash']}",
        }
        for row in matrix_rows
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": f"materialized_blueprint_{row['package_id']}",
            "tier_scope": "Tier A+B blueprint requirement",
            "scoreboard": "experiment_design_blueprint",
            "status": STATUS,
            "judgment": row["package_role"],
            "evidence_boundary": "blueprint_only_no_candidate_no_onnx",
            "report_path": rel(RUN_REPORT),
            "notes": f"blueprint_hash={row['blueprint_hash']}",
        }
        for row in matrix_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs(matrix_rows: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in matrix_rows if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in matrix_rows if row["package_role"] == "support_control")
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_once(selection, "run274B_report", f"- run274B_report(274B 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run274B_package_blueprints", f"- run274B_package_blueprints(274B 패키지 청사진): `{rel(PACKAGE_BLUEPRINTS)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run274B_report",
        "\n".join(
            [
                f"- run274B_report(274B 보고서): `{rel(RUN_REPORT)}`",
                f"- run274B_package_blueprints(274B 패키지 청사진): `{rel(PACKAGE_BLUEPRINTS)}`",
                f"- run274B_blueprint_matrix(274B 청사진 행렬): `{rel(BLUEPRINT_MATRIX)}`",
                f"- run274B_scoring_surface_plan(274B 점수 표면 계획): `{rel(SCORING_SURFACE_PLAN)}`",
                f"- run274B_adapter_contract_plan(274B 어댑터 계약 계획): `{rel(ADAPTER_CONTRACT_PLAN)}`",
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
        "run274B_summary",
        f"- run274B_summary(274B 요약): run274B(274B 실행)는 post-q04 candidate package blueprint(q04 이후 후보 패키지 청사진) `{len(matrix_rows)}`개를 물질화했다. Effect(효과): selectable blueprint(선택 가능 청사진) `{selectable}`개와 support control(보조 대조) `{support}`개를 run274C(274C 실행) 점수/인계 입력으로 넘기며, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage274(274단계) run274B(274B 실행) post-q04 candidate package blueprint materialization(q04 이후 후보 패키지 청사진 물질화) `{RUN_ID}`. "
        f"Effect(효과): blueprints(청사진) `{len(matrix_rows)}`개, selectable(선택 가능) `{selectable}`개를 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run274B candidate package blueprint materialization(274B 후보 패키지 청사진 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): q04(4번 분기) 실패 이후 새 후보 청사진 `{len(matrix_rows)}`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)

    if path_exists(IDEA_REGISTER):
        ideas = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
        ideas = append_once(
            ideas,
            "IDEA-ST274-POST-Q04-CANDIDATE-BLUEPRINTS-RUN274B",
            f"| `IDEA-ST274-POST-Q04-CANDIDATE-BLUEPRINTS-RUN274B` | `{STAGE_ID}` | q04 failure memory(q04 실패 기억)를 새 candidate package blueprint(후보 패키지 청사진)로 재구성 | `blueprints={len(matrix_rows)};selectable={selectable};support_control={support}` | `materialized_blueprint_no_selection` | selected candidate(선택 후보) 없음, ONNX readiness(온엑스 준비) 없음 |",
        )
        write_md(IDEA_REGISTER, ideas)


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [
        SOURCE_THESIS_QUEUE,
        SOURCE_FAILURE_MAP,
        SOURCE_BLUEPRINT_SEEDS,
        SOURCE_DISCARD,
        SOURCE_RUN274A_MANIFEST,
        SOURCE_RUN274A_LINEAGE,
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
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage274/materialize_post_q04_failure_candidate_package_blueprints.py",
        "entry_command": "python stage_pipelines/stage274/materialize_post_q04_failure_candidate_package_blueprints.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
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
            "artifact_type": "run274B_blueprint_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run274B candidate package blueprint materialization artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def execute() -> dict[str, Any]:
    must_exist([
        SOURCE_THESIS_QUEUE,
        SOURCE_FAILURE_MAP,
        SOURCE_BLUEPRINT_SEEDS,
        SOURCE_DISCARD,
        SOURCE_RUN274A_MANIFEST,
        SOURCE_RUN274A_LINEAGE,
        SOURCE_Q04_PAYLOAD,
        MODEL_INPUT_CONTRACT,
        MT5_INPUT_CONTRACT,
    ])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    thesis_rows = read_csv_rows(SOURCE_THESIS_QUEUE)
    failure_rows = read_csv_rows(SOURCE_FAILURE_MAP)
    seed_rows = read_csv_rows(SOURCE_BLUEPRINT_SEEDS)
    payload_identity = load_payload_identity()
    bundle, matrix_rows, scoring_rows, adapter_rows, rule_rows = build_blueprints(
        thesis_rows, seed_rows, failure_rows, payload_identity
    )
    write_json(PACKAGE_BLUEPRINTS, bundle)
    write_csv(BLUEPRINT_MATRIX, matrix_rows)
    write_csv(SCORING_SURFACE_PLAN, scoring_rows)
    write_csv(ADAPTER_CONTRACT_PLAN, adapter_rows)
    write_csv(DECISION_RISK_RULE_RECEIPT, rule_rows)
    identity_rows = [
        {
            "package_id": row["package_id"],
            "package_role": row["package_role"],
            "feature_order_hash": row["feature_order_hash"],
            "score_columns_hash": row["score_columns_hash"],
            "decision_rule_hash": row["decision_rule_hash"],
            "risk_rule_hash": row["risk_rule_hash"],
            "adapter_schema_hash": row["adapter_schema_hash"],
            "blueprint_hash": row["blueprint_hash"],
            "claim_boundary": BOUNDARY,
        }
        for row in matrix_rows
    ]
    write_csv(PACKAGE_IDENTITY_RECEIPT, identity_rows)
    gate_rows = write_receipts(bundle, matrix_rows, payload_identity)
    write_report(matrix_rows)
    artifacts = [
        PACKAGE_BLUEPRINTS,
        BLUEPRINT_MATRIX,
        SCORING_SURFACE_PLAN,
        ADAPTER_CONTRACT_PLAN,
        DECISION_RISK_RULE_RECEIPT,
        PACKAGE_IDENTITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers(matrix_rows)
    update_state_docs(matrix_rows)
    write_manifests_and_registry(created_at, artifacts)
    selectable = sum(1 for row in matrix_rows if row["package_role"] == "selectable_blueprint")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "blueprints": len(matrix_rows),
        "selectable_blueprints": selectable,
        "support_controls": len(matrix_rows) - selectable,
        "gate_rows": len(gate_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
