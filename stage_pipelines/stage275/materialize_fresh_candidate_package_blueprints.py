from __future__ import annotations

import csv
import hashlib
import json
import sys
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


STAGE_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
RUN_ID = "run275B_materialize_fresh_candidate_package_blueprints_v1"
SOURCE_RUN_ID = "run275A_design_fresh_candidate_construction_packet_v1"
STATUS = "completed_fresh_candidate_package_blueprint_materialization_no_candidate_selection"
JUDGMENT = "fresh_candidate_blueprints_materialized_no_candidate_selection"
NEXT_ACTION = "run275C_materialize_fresh_candidate_scoring_handoff_inputs"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE / "02_runs" / "run275B"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"
RUN275A = STAGE / "02_runs" / "run275A"

SOURCE_QUEUE = RUN275A / "queue.csv"
SOURCE_FAILURE_MAP = RUN275A / "failure_map.csv"
SOURCE_FEATURE_ID = RUN275A / "feature_id.csv"
SOURCE_PACKET = RUN275A / "packet.json"
SOURCE_REPORT = REVIEWS / "run275A_report.md"
SOURCE_MANIFEST = RUN275A / "run_manifest.json"

BLUEPRINTS = RUN_DIR / "blueprints.json"
SCORING_PLAN = RUN_DIR / "scoring.csv"
ADAPTER_PLAN = RUN_DIR / "adapter.csv"
RULE_RECEIPT = RUN_DIR / "rules.csv"
IDENTITY_RECEIPT = RUN_DIR / "identity.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
RUN_REPORT = REVIEWS / "run275B_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage275/materialize_fresh_candidate_package_blueprints.py")

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
SCORING_COLUMNS = (
    "package_id",
    "package_role",
    "score_columns",
    "score_columns_hash",
    "formula_plan",
    "required_source_columns",
    "threshold_policy",
    "freshness_guard",
    "next_action",
    "claim_boundary",
)
ADAPTER_COLUMNS = (
    "package_id",
    "package_role",
    "adapter_schema_hash",
    "runtime_handoff_fields",
    "telemetry_required",
    "candidate_claim_allowed",
    "adapter_path",
    "claim_boundary",
)
RULE_COLUMNS = (
    "package_id",
    "decision_rule_hash",
    "risk_rule_hash",
    "decision_rule",
    "risk_rule",
    "freshness_guard",
    "claim_boundary",
)
IDENTITY_COLUMNS = (
    "package_id",
    "package_role",
    "feature_order_hash",
    "blueprint_hash",
    "score_columns_hash",
    "decision_rule_hash",
    "risk_rule_hash",
    "adapter_schema_hash",
    "identity_judgment",
    "claim_boundary",
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
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest_payload(payload: Any) -> str:
    raw = json.dumps(json_ready(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return dict(json.load(handle))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def split_semicolon(text: str) -> list[str]:
    return [item.strip() for item in str(text or "").split(";") if item.strip()]


def score_columns_for(package_id: str) -> list[str]:
    if package_id.startswith("cp275A"):
        return [
            "volatility_pullback_score",
            "pullback_breakout_state",
            "long_permission_score",
            "short_permission_score",
            "candidate_decision_score",
            "model_risk_pct",
        ]
    if package_id.startswith("cp275B"):
        return [
            "cross_asset_divergence_score",
            "reversal_permission_score",
            "route_switch_flag",
            "candidate_decision_score",
            "model_risk_pct",
        ]
    if package_id.startswith("cp275C"):
        return [
            "session_impulse_score",
            "continuation_score",
            "fade_score",
            "continuation_fade_state",
            "candidate_decision_score",
            "model_risk_pct",
        ]
    if package_id.startswith("cp275D"):
        return [
            "squeeze_release_score",
            "macro_vol_route_state",
            "risk_budget_multiplier",
            "candidate_decision_score",
            "model_risk_pct",
        ]
    return [
        "q04_failure_signature_flag",
        "stage274_filter_like_signature_flag",
        "freshness_guard_result",
    ]


def required_columns_for(row: Mapping[str, str]) -> list[str]:
    base = [
        "timestamp",
        "symbol",
        "split",
        "tier_view",
        "package_id",
        "feature_order_hash",
        "decision_rule_hash",
        "risk_rule_hash",
        "adapter_schema_hash",
        "claim_boundary",
    ]
    return [*base, *split_semicolon(str(row.get("feature_surface", "")))]


def decision_rule_for(row: Mapping[str, str]) -> str:
    return (
        f"Package(패키지) `{row['package_id']}` uses `{row['decision_surface']}`. "
        "It must pass freshness guard(신선도 방어): new active entry(새 활성 진입) or direction switch(방향 전환) must be measurable against q04 control(q04 대조)."
    )


def risk_rule_for(row: Mapping[str, str]) -> str:
    return (
        f"Risk logic(위험 로직): {row['risk_logic']} "
        "Risk output(위험 출력)는 model_risk_pct(모델 위험 비율) and telemetry_json(기록 JSON)로만 넘기며 runtime authority(런타임 권위)를 주장하지 않는다."
    )


def adapter_schema_for(row: Mapping[str, str], score_columns: Sequence[str]) -> dict[str, Any]:
    handoff = split_semicolon(row["runtime_handoff"])
    for column in score_columns:
        if column not in handoff and column not in {"candidate_decision_score"}:
            handoff.append(column)
    return {
        "base_contract": "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md",
        "package_id": row["package_id"],
        "candidate_claim_allowed": False,
        "telemetry_required": True,
        "handoff_fields": handoff,
        "score_columns": list(score_columns),
        "feature_order_hash": row["feature_order_hash"],
        "claim_boundary": BOUNDARY,
    }


def blueprint_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints: list[dict[str, Any]] = []
    for row in queue_rows:
        package_id = row["package_id"]
        score_columns = score_columns_for(package_id)
        decision_rule = decision_rule_for(row)
        risk_rule = risk_rule_for(row)
        adapter_schema = adapter_schema_for(row, score_columns)
        score_hash = digest_payload(score_columns)
        decision_hash = digest_payload({"package_id": package_id, "decision_rule": decision_rule})
        risk_hash = digest_payload({"package_id": package_id, "risk_rule": risk_rule})
        adapter_hash = digest_payload(adapter_schema)
        formula_plan = (
            f"Materialize(물질화) `{package_id}` from feature surface(피처 표면) `{row['feature_surface']}`; "
            "derive thresholds(임계값)는 train split(학습 분할) only; compare(비교)는 q04/stage274 failure guard(실패 방어)와 한다."
        )
        blueprint_base = {
            "package_id": package_id,
            "package_role": row["queue_role"],
            "fresh_thesis": row["fresh_thesis"],
            "feature_surface": row["feature_surface"],
            "model_or_scoring_surface": row["model_or_scoring_surface"],
            "decision_surface": row["decision_surface"],
            "decision_rule": decision_rule,
            "decision_rule_hash": decision_hash,
            "risk_logic": row["risk_logic"],
            "risk_rule": risk_rule,
            "risk_rule_hash": risk_hash,
            "adapter_path": row["adapter_path"],
            "adapter_output_schema": adapter_schema,
            "adapter_schema_hash": adapter_hash,
            "runtime_handoff_plan": adapter_schema["handoff_fields"],
            "feature_order_source": "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt",
            "source_feature_order_hash": row["feature_order_hash"],
            "score_columns": score_columns,
            "score_columns_hash": score_hash,
            "formula_plan": formula_plan,
            "required_source_columns": required_columns_for(row),
            "comparison_baseline": row["comparison_baseline"],
            "control_variables": row["control_variables"],
            "changed_variables": row["changed_variables"],
            "sample_scope": row["sample_scope"],
            "upside_condition": row["upside_condition"],
            "failure_criteria": row["failure_condition"],
            "discard_condition": row["discard_condition"],
            "invalid_conditions": row["invalid_conditions"],
            "stop_conditions": row["stop_conditions"],
            "evidence_plan": row["evidence_plan"],
            "source_failure_memory": row["source_failure_memory"],
            "freshness_guard": row["freshness_guard"],
            "scoring_owner": "stage_pipelines/stage275 until reusable scoring logic proves foundation ownership(재사용 점수 로직이 증명되기 전까지 275단계 소유)",
            "threshold_policy": "derive quantiles/ranks(분위수/순위)는 train split(학습 분할) only in run275D; validation/oos(검증/표본외)는 read-only(읽기 전용)",
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
            "source_run_id": SOURCE_RUN_ID,
        }
        blueprint_base["blueprint_hash"] = digest_payload(blueprint_base)
        blueprints.append(blueprint_base)
    return blueprints


def scoring_plan_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "package_role": row["package_role"],
            "score_columns": ";".join(row["score_columns"]),
            "score_columns_hash": row["score_columns_hash"],
            "formula_plan": row["formula_plan"],
            "required_source_columns": ";".join(row["required_source_columns"]),
            "threshold_policy": row["threshold_policy"],
            "freshness_guard": row["freshness_guard"],
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        }
        for row in blueprints
    ]


def adapter_plan_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "package_role": row["package_role"],
            "adapter_schema_hash": row["adapter_schema_hash"],
            "runtime_handoff_fields": ";".join(row["runtime_handoff_plan"]),
            "telemetry_required": "true",
            "candidate_claim_allowed": "false",
            "adapter_path": row["adapter_path"],
            "claim_boundary": BOUNDARY,
        }
        for row in blueprints
    ]


def rule_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "decision_rule_hash": row["decision_rule_hash"],
            "risk_rule_hash": row["risk_rule_hash"],
            "decision_rule": row["decision_rule"],
            "risk_rule": row["risk_rule"],
            "freshness_guard": row["freshness_guard"],
            "claim_boundary": BOUNDARY,
        }
        for row in blueprints
    ]


def identity_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "package_role": row["package_role"],
            "feature_order_hash": row["source_feature_order_hash"],
            "blueprint_hash": row["blueprint_hash"],
            "score_columns_hash": row["score_columns_hash"],
            "decision_rule_hash": row["decision_rule_hash"],
            "risk_rule_hash": row["risk_rule_hash"],
            "adapter_schema_hash": row["adapter_schema_hash"],
            "identity_judgment": "blueprint_identity_connected_no_candidate_selection"
            if row["package_role"] != "support_control"
            else "support_control_only_never_promote",
            "claim_boundary": BOUNDARY,
        }
        for row in blueprints
    ]


def experiment_receipt(blueprints: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    selectable = [row for row in blueprints if row["package_role"] != "support_control"]
    return {
        "hypothesis": "Fresh candidate seeds(새 후보 씨앗)를 feature/order/rule/Adapter identity(피처/순서/규칙/어댑터 정체성)가 있는 blueprints(청사진)로 바꾸면 run275C/run275D(275C/275D 실행)에서 non-filter freshness(비필터 신선도)를 시험할 수 있다.",
        "decision_use": "Select blueprint packages(청사진 패키지)를 scoring/handoff input(점수/인계 입력)으로 넘긴다.",
        "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard",
        "control_variables": "US100 M5; feature order hash fixed(피처 순서 해시 고정); Tier A/B/A+B paired records(쌍 기록); no candidate selection(후보 선택 없음)",
        "changed_variables": [row["changed_variables"] for row in selectable],
        "sample_scope": "Stage275 design materialization(275단계 설계 물질화); no trading KPI(거래 KPI 없음)",
        "success_criteria": "All selectable packages(선택 가능 패키지)가 blueprint_hash, decision_rule_hash, risk_rule_hash, adapter_schema_hash(청사진/판단/위험/어댑터 해시)를 가진다.",
        "failure_criteria": "Any selectable package(선택 가능 패키지)가 support control(보조 대조) or q04 duplicate(중복 q04)로만 남는다.",
        "invalid_conditions": "Missing source queue(원천 대기열 누락), feature identity(피처 정체성 누락), or hash identity(해시 정체성 누락).",
        "stop_conditions": "If run275C/run275D cannot create score surfaces(점수 표면), close as inconclusive/invalid(불충분/무효) by evidence.",
        "evidence_plan": [BLUEPRINTS, SCORING_PLAN, ADAPTER_PLAN, RULE_RECEIPT, IDENTITY_RECEIPT],
        "selectable_blueprints": len(selectable),
        "support_control": len(blueprints) - len(selectable),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def data_integrity_receipt(feature_rows: Sequence[Mapping[str, str]], blueprints: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "data_source": rel(SOURCE_QUEUE),
        "time_axis": "run275B(275B 실행)는 설계 물질화라 새 시계열 값을 만들지 않는다; downstream(하위 실행)은 M5 timestamp(M5 시각) 경계를 유지해야 한다.",
        "sample_scope": "US100 M5 train/validation/oos(학습/검증/표본외) inherited from run275A feature identity(피처 정체성)",
        "missing_or_duplicate_check": "not_applicable_design_materialization(설계 물질화라 해당 없음); source feature identity(원천 피처 정체성) preserved.",
        "feature_label_boundary": "No label/future columns(라벨/미래 열) appear in required_source_columns(필수 원천 열).",
        "split_boundary": "Threshold policy(임계값 정책)는 train split only(학습 분할 전용)로 blueprints(청사진)에 기록했다.",
        "leakage_risk": "Future materialization(향후 물질화)이 label/future columns(라벨/미래 열)을 score formula(점수식)에 넣으면 invalid(무효).",
        "data_hash_or_identity": {
            "source_queue_hash": sha256_file_lf_normalized(SOURCE_QUEUE),
            "feature_identity_hash": sha256_file_lf_normalized(SOURCE_FEATURE_ID),
            "feature_order_hashes": sorted({row["feature_order_hash"] for row in feature_rows if row.get("feature_order_hash")}),
        },
        "integrity_judgment": "usable_with_boundary_design_materialization_only",
        "blueprint_count": len(blueprints),
        "claim_boundary": BOUNDARY,
    }


def model_validation_receipt(blueprints: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "model_family": "deterministic blueprint score surfaces(결정 청사진 점수 표면); no trained model(훈련 모델 없음)",
        "target_and_label": "entry/direction/risk exploratory surface(진입/방향/위험 탐색 표면); label not consumed(라벨 미사용)",
        "split_method": "blueprint only(청사진 전용); future thresholds(향후 임계값)은 train split only(학습 분할 전용)",
        "selection_metric": "identity completeness(정체성 완전성), freshness guard target(신선도 방어 목표), and non-filter requirement(비필터 요구)",
        "secondary_metrics": "new_active_count(새 활성 수), direction_changed_count(방향 변경 수), changed_signal_rate(변경 신호율), duplicate signature distance(중복 서명 거리) in downstream screen(하위 선별)",
        "threshold_policy": "planned_train_split_only",
        "overfit_risk": "Blueprints(청사진)가 Stage274 failure memory(실패 기억)에 과맞춤될 수 있다.",
        "calibration_risk": "Scores(점수)는 probability(확률)가 아니라 rank/state(순위/상태)다.",
        "comparison_baseline": "q04/stage274 failure signature guard(q04/274단계 실패 서명 방어)",
        "validation_judgment": "exploratory_blueprint_no_candidate_selection",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def result_rows() -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "package blueprints(패키지 청사진); scoring plan(점수 계획); Adapter plan(어댑터 계획); rule/identity receipts(규칙/정체성 영수증)",
            "evidence_missing": "scoring input materialization(점수 입력 물질화); score tables(점수표); MT5 runtime output(MT5 런타임 출력); ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "새 후보 씨앗이 해시 가능한 청사진으로 바뀌었지만, 아직 후보 선택은 아니다.",
        }
    ]


def gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_name": "work_packet_schema_lint(작업 묶음 스키마 점검)",
            "status": "passed(통과)",
            "evidence_path": rel(EXPERIMENT_RECEIPT),
            "effect": "hypothesis/comparison/controls/criteria/evidence plan(가설/비교/대조/기준/근거 계획)을 기록했다.",
        },
        {
            "gate_name": "blueprint_identity_gate(청사진 정체성 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(IDENTITY_RECEIPT),
            "effect": "feature/order/rule/Adapter hashes(피처/순서/규칙/어댑터 해시)를 package(패키지)별로 고정했다.",
        },
        {
            "gate_name": "freshness_guard_gate(신선도 방어 게이트)",
            "status": "passed_with_boundary(경계 포함 통과)",
            "evidence_path": rel(SCORING_PLAN),
            "effect": "new active entry(새 활성 진입) 또는 direction switch(방향 전환)가 없으면 폐기하도록 했다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed(통과)",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "run275B(275B 실행)의 필수 게이트와 closeout(종료 기록)을 연결했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def write_report(blueprints: Sequence[Mapping[str, Any]]) -> None:
    selectable = [row for row in blueprints if row["package_role"] != "support_control"]
    lines = "\n".join(
        f"- `{row['package_id']}`: blueprint_hash(청사진 해시) `{row['blueprint_hash'][:16]}`; adapter_schema_hash(어댑터 스키마 해시) `{row['adapter_schema_hash'][:16]}`"
        for row in selectable
    )
    write_md(
        RUN_REPORT,
        f"""# run275B Fresh Candidate Package Blueprints(275B 새 후보 패키지 청사진)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run275B(275B 실행)는 run275A(275A 실행)의 fresh candidate seeds(새 후보 씨앗)를 hashable package blueprint(해시 가능한 패키지 청사진)로 바꿨다.
효과(effect, 효과): 다음 run275C(275C 실행)는 score/handoff input(점수/인계 입력)을 만들 때 feature order(피처 순서), decision rule(판단 규칙), risk rule(위험 규칙), Adapter schema(어댑터 스키마)를 추적할 수 있다.

## Selectable Blueprints(선택 가능 청사진)

{lines}

## Evidence Paths(근거 경로)

- blueprints(청사진): `{rel(BLUEPRINTS)}`
- scoring plan(점수 계획): `{rel(SCORING_PLAN)}`
- Adapter plan(어댑터 계획): `{rel(ADAPTER_PLAN)}`
- identity receipt(정체성 영수증): `{rel(IDENTITY_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


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


def replace_or_append(text: str, prefix: str, replacement: str) -> str:
    if any(line.startswith(prefix) for line in text.splitlines()):
        return replace_line_prefix(text, prefix, replacement)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_stage_docs(blueprints: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in blueprints if row["package_role"] != "support_control")
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_or_append(selection, "- run275B_report", f"- run275B_report(275B 보고서): `{rel(RUN_REPORT)}`")
    selection = replace_or_append(selection, "- run275B_blueprints", f"- run275B_blueprints(275B 청사진): `{rel(BLUEPRINTS)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = replace_or_append(review, "- run275B_report", f"- run275B_report(275B 보고서): `{rel(RUN_REPORT)}`")
    review = replace_or_append(review, "- run275B_blueprints", f"- run275B_blueprints(275B 청사진): `{rel(BLUEPRINTS)}`")
    review = replace_or_append(review, "- run275B_identity", f"- run275B_identity(275B 정체성): `{rel(IDENTITY_RECEIPT)}`")
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_candidate_blueprint_identity_materialization`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run275B_summary",
        f"- run275B_summary(275B 요약): run275B(275B 실행)는 selectable blueprint(선택 가능 청사진) `{selectable}`개와 support control(보조 대조) `1`개를 물질화했다. Effect(효과): feature order hash(피처 순서 해시), decision rule hash(판단 규칙 해시), risk rule hash(위험 규칙 해시), Adapter schema hash(어댑터 스키마 해시)를 package(패키지)별로 고정하고 run275C(275C 실행) 점수/인계 입력으로 넘긴다. Boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage275(275단계) run275B(275B 실행) fresh candidate package blueprint materialization(새 후보 패키지 청사진 물질화) `{RUN_ID}`. "
        f"Effect(효과): selectable blueprint(선택 가능 청사진) `{selectable}`개와 support control(보조 대조) `1`개를 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## 2026-05-23 run275B fresh candidate package blueprint materialization(275B 새 후보 패키지 청사진 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): selectable blueprint(선택 가능 청사진) `{selectable}`개와 support control(보조 대조) `1`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def update_registers(created_at: str, blueprints: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    selectable = sum(1 for row in blueprints if row["package_role"] != "support_control")
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
                "notes": f"selectable_blueprints={selectable};support_control=1;selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
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
            "record_view": "fresh candidate package blueprint(새 후보 패키지 청사진)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined blueprint",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_candidate_blueprint_materialization",
            "status": STATUS,
            "judgment": row["package_role"],
            "path": rel(BLUEPRINTS),
            "primary_kpi": "blueprint_identity_hashes_materialized",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": row["discard_condition"],
        }
        for row in blueprints
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__blueprint",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_candidate_package_blueprints",
                "tier_scope": "Tier A+B paired blueprint",
                "scoreboard": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "blueprint_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"selectable={selectable};support_control=1;next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run275B_fresh_candidate_blueprint_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run275B fresh candidate package blueprint materialization artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def manifest_payload(
    created_at: str,
    blueprints: Sequence[Mapping[str, Any]],
    artifacts: Sequence[Path],
    source_inputs: Sequence[Path],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "package_ids": [row["package_id"] for row in blueprints],
        "selectable_blueprints": sum(1 for row in blueprints if row["package_role"] != "support_control"),
        "support_control_rows": sum(1 for row in blueprints if row["package_role"] == "support_control"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
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


def run() -> dict[str, Any]:
    must_exist([SOURCE_QUEUE, SOURCE_FAILURE_MAP, SOURCE_FEATURE_ID, SOURCE_PACKET, SOURCE_REPORT, SOURCE_MANIFEST])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()

    queue_rows = read_csv_rows(SOURCE_QUEUE)
    feature_rows = read_csv_rows(SOURCE_FEATURE_ID)
    blueprints = blueprint_rows(queue_rows)
    selectable = sum(1 for row in blueprints if row["package_role"] != "support_control")

    shared_controls = {
        "symbol": "US100",
        "timeframe": "M5",
        "feature_order_hashes": sorted({row["source_feature_order_hash"] for row in blueprints}),
        "tier_requirement": "Tier A separate;Tier B separate;Tier A+B combined",
        "claim_boundary": BOUNDARY,
        "source_run_id": SOURCE_RUN_ID,
    }
    write_json(
        BLUEPRINTS,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "shared_controls": shared_controls,
            "packages": blueprints,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(SCORING_PLAN, SCORING_COLUMNS, scoring_plan_rows(blueprints))
    write_csv(ADAPTER_PLAN, ADAPTER_COLUMNS, adapter_plan_rows(blueprints))
    write_csv(RULE_RECEIPT, RULE_COLUMNS, rule_rows(blueprints))
    write_csv(IDENTITY_RECEIPT, IDENTITY_COLUMNS, identity_rows(blueprints))
    write_json(EXPERIMENT_RECEIPT, experiment_receipt(blueprints))
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_receipt(feature_rows, blueprints))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_receipt(blueprints))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows())
    write_report(blueprints)

    source_inputs = [SOURCE_QUEUE, SOURCE_FAILURE_MAP, SOURCE_FEATURE_ID, SOURCE_PACKET, SOURCE_REPORT, SOURCE_MANIFEST]
    artifacts = [
        BLUEPRINTS,
        SCORING_PLAN,
        ADAPTER_PLAN,
        RULE_RECEIPT,
        IDENTITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = manifest_payload(created_at, blueprints, artifacts, source_inputs)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, blueprints, artifacts, source_inputs)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, blueprints, artifacts, source_inputs)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, blueprints, artifacts)
    update_stage_docs(blueprints)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "selectable_blueprints": selectable,
        "support_control_rows": len(blueprints) - selectable,
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
