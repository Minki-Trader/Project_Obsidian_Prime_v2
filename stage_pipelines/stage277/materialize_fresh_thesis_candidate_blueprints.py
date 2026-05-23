from __future__ import annotations

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


STAGE_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild"
RUN_ID = "run277B_materialize_fresh_thesis_candidate_blueprints_v1"
SOURCE_RUN_ID = "run277A_design_fresh_thesis_rebuild_packet_v1"
STATUS = "completed_fresh_thesis_candidate_blueprint_materialization_no_candidate_selection"
JUDGMENT = "fresh_thesis_candidate_blueprints_materialized_no_candidate_selection"
NEXT_ACTION = "run277C_materialize_fresh_thesis_scoring_handoff_inputs"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN277A = STAGE / "02_runs" / "run277A"
RUN_DIR = STAGE / "02_runs" / "run277B"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SOURCE_PACKAGE_QUEUE = RUN277A / "candidate_package_queue.csv"
SOURCE_REQUIRED_EVIDENCE = RUN277A / "required_evidence_matrix.csv"
SOURCE_ADAPTER_PLAN = RUN277A / "adapter_handoff_plan.csv"
SOURCE_MANIFEST = RUN277A / "run_manifest.json"
FEATURE_ORDER = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_feature_order.txt"
FEATURE_MANIFEST = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "feature_set_manifest.json"
MODEL_INPUT_SUMMARY = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_summary.json"

PACKAGE_BLUEPRINTS_JSON = RUN_DIR / "package_blueprints.json"
PACKAGE_BLUEPRINTS_CSV = RUN_DIR / "package_blueprints.csv"
BLUEPRINT_IDENTITY = RUN_DIR / "blueprint_identity_receipts.csv"
SCORING_COLUMN_PLAN = RUN_DIR / "scoring_column_plan.csv"
ADAPTER_SCHEMA_PLAN = RUN_DIR / "adapter_schema_plan.csv"
HANDOFF_SKELETONS = RUN_DIR / "handoff_skeletons.json"
HANDOFF_INDEX = RUN_DIR / "handoff_skeleton_index.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run277B_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage277/materialize_fresh_thesis_candidate_blueprints.py")

BASE_ADAPTER_OUTPUTS = [
    "entry_signal",
    "route_code",
    "model_risk_pct",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "max_hold_bars",
    "reentry_cooldown_bars",
]
PACKAGE_COLUMNS = (
    "package_id",
    "package_role",
    "source_seed_id",
    "blueprint_hash",
    "feature_order_hash",
    "feature_contract_hash",
    "decision_rule_hash",
    "adapter_schema_hash",
    "score_columns_hash",
    "selected_candidate",
    "onnx_readiness",
    "next_action",
)
IDENTITY_COLUMNS = (
    "package_id",
    "package_role",
    "feature_order_hash",
    "feature_contract_hash",
    "blueprint_hash",
    "decision_rule_hash",
    "adapter_schema_hash",
    "score_columns_hash",
    "identity_judgment",
)
PLAN_COLUMNS = ("package_id", "package_role", "columns_or_fields", "hash_value", "source", "effect")
HANDOFF_COLUMNS = ("package_id", "handoff_file_plan", "required_hashes", "runtime_payload_fields", "next_consumer", "boundary")
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
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

PACKAGE_SURFACES = {
    "cp277A_session_loss_avoidance_surface": {
        "changed_variables": ["session_loss_state", "chron_bucket", "weak_session_retention_flag", "risk_multiplier"],
        "base_features": ["is_us_cash_open", "minutes_from_cash_open", "is_first_30m_after_open", "is_last_30m_before_cash_close", "historical_vol_5_over_20", "atr_14_over_atr_50", "bb_squeeze", "adx_14", "vix_zscore_20"],
        "score_columns": ["session_loss_state_score", "entry_retention_score", "weak_session_cut_score", "risk_multiplier_score", "candidate_decision_score"],
        "telemetry": ["session_loss_state", "chron_bucket", "risk_multiplier_score", "decision_rule_hash", "package_id"],
    },
    "cp277B_validation_pf_floor_rebalanced_entry_surface": {
        "changed_variables": ["validation_pf_margin", "oos_supply_state", "entry_source_rebalance", "risk_cap"],
        "base_features": ["log_return_1", "log_return_3", "return_zscore_20", "atr_14", "atr_50", "atr_14_over_atr_50", "rsi_14", "rsi_14_slope_3", "adx_14", "di_spread_14"],
        "score_columns": ["pf_floor_score", "supply_state_score", "validation_margin_score", "risk_cap_score", "candidate_decision_score"],
        "telemetry": ["validation_pf_margin", "oos_supply_state", "risk_cap_score", "decision_rule_hash", "package_id"],
    },
    "cp277C_directional_asymmetry_reversal_surface": {
        "changed_variables": ["side_state", "divergence_sign_state", "session_side_pressure", "side_risk_cap"],
        "base_features": ["us100_minus_mega8_equal_return_1", "us100_minus_top3_weighted_return_1", "mega8_pos_breadth_1", "mega8_dispersion_5", "top3_weighted_return_1", "vortex_indicator", "di_spread_14", "minutes_from_cash_open"],
        "score_columns": ["side_reversal_score", "divergence_sign_score", "session_pressure_score", "side_risk_score", "candidate_decision_score"],
        "telemetry": ["side_state", "divergence_sign_state", "session_side_pressure", "side_risk_cap", "package_id"],
    },
    "cp277D_macro_squeeze_failure_contrast_surface": {
        "changed_variables": ["macro_squeeze_state", "post_release_cooldown", "late_chron_risk_state", "contrast_reward_state"],
        "base_features": ["bb_squeeze", "bollinger_width_20", "historical_vol_20", "historical_vol_5_over_20", "vix_change_1", "vix_zscore_20", "us10yr_zscore_20", "usdx_zscore_20", "mega8_dispersion_5"],
        "score_columns": ["macro_squeeze_state_score", "contrast_reward_score", "late_loss_compression_score", "cooldown_score", "candidate_decision_score"],
        "telemetry": ["macro_squeeze_state", "contrast_reward_state", "late_chron_risk_state", "cooldown_state", "package_id"],
    },
}


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def read_feature_order() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def materialize_blueprints(package_queue: Sequence[Mapping[str, str]], feature_order: Sequence[str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    feature_order_hash = sha256_text("\n".join(feature_order))
    packages: list[dict[str, Any]] = []
    for row in package_queue:
        package_id = row["package_id"]
        surface = PACKAGE_SURFACES[package_id]
        missing_features = [feature for feature in surface["base_features"] if feature not in feature_order]
        if missing_features:
            raise ValueError(f"{package_id} has missing base features: {missing_features}")
        feature_contract = {
            "base_feature_order_hash": feature_order_hash,
            "base_features": surface["base_features"],
            "derived_features": surface["changed_variables"],
            "feature_surface": row["feature_surface"],
        }
        score_columns = surface["score_columns"]
        adapter_schema = BASE_ADAPTER_OUTPUTS + surface["telemetry"]
        decision_source = "|".join([package_id, row["decision_surface"], row["risk_logic"], ",".join(surface["changed_variables"])])
        package = {
            "package_id": package_id,
            "package_role": "selectable_blueprint_not_selected_candidate",
            "source_seed_id": row["source_seed_id"],
            "fresh_thesis": row["fresh_thesis"],
            "hypothesis": row["fresh_thesis"],
            "comparison_baseline": "Stage276 failure memory(276단계 실패 기억) as reference only(참고만), no selected baseline(선택 기준선 없음)",
            "control_variables": [
                "FPMarkets US100 M5",
                f"base feature order hash(기본 피처 순서 해시) {feature_order_hash}",
                "Tier A separate/Tier B separate/Tier A+B combined evidence required(Tier A 분리/Tier B 분리/Tier A+B 합산 근거 필수)",
                BOUNDARY,
            ],
            "changed_variables": surface["changed_variables"],
            "feature_contract": feature_contract,
            "feature_contract_hash": sha256_text(json.dumps(feature_contract, ensure_ascii=False, sort_keys=True)),
            "model_or_scoring_surface": row["model_or_scoring_surface"],
            "score_columns": score_columns,
            "score_columns_hash": sha256_text("\n".join(score_columns)),
            "decision_surface": row["decision_surface"],
            "decision_rule_hash": sha256_text(decision_source),
            "risk_logic": row["risk_logic"],
            "adapter_schema": adapter_schema,
            "adapter_schema_hash": sha256_text("\n".join(adapter_schema)),
            "runtime_handoff_plan": row["runtime_handoff"],
            "success_criteria": "run277C(277C 실행)가 deterministic scoring/handoff input(결정적 점수/인계 입력)을 만들고 Tier A/B(티어 A/B) 누락 없이 추적할 수 있어야 한다.",
            "failure_criteria": row["discard_condition"],
            "invalid_conditions": "feature order source(피처 순서 원천), decision hash(판단 해시), adapter schema hash(어댑터 스키마 해시) 중 하나라도 빠지면 invalid(무효)다.",
            "stop_conditions": "두 stage(단계) 안에 materialized score surface(물질화 점수 표면)로 가지 못하면 폐기 또는 새 thesis(논제)로 전환한다.",
            "evidence_plan": "run277C scoring/handoff input(점수/인계 입력), run277D scoring probe(점수 탐침), later MT5 probe(이후 MT5 탐침)",
            "failure_memory": "Do not preserve cp275A/cp275B/cp275D(275A/275B/275D 패키지)를 candidate(후보)로 보존하지 않는다.",
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        package["blueprint_hash"] = sha256_text(json.dumps(package, ensure_ascii=False, sort_keys=True))
        packages.append(package)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "blueprint_status": "materialized_no_candidate_selection",
        "shared_controls": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "feature_order_source": rel(FEATURE_ORDER),
            "feature_order_hash": feature_order_hash,
            "feature_manifest": rel(FEATURE_MANIFEST),
            "model_input_summary": rel(MODEL_INPUT_SUMMARY),
            "tier_records_required": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
            "claim_boundary": BOUNDARY,
        },
        "packages": packages,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }
    return payload, packages


def csv_rows_from_packages(packages: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    package_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    scoring_rows: list[dict[str, Any]] = []
    adapter_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    for package in packages:
        package_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "source_seed_id": package["source_seed_id"],
                "blueprint_hash": package["blueprint_hash"],
                "feature_order_hash": package["feature_contract"]["base_feature_order_hash"],
                "feature_contract_hash": package["feature_contract_hash"],
                "decision_rule_hash": package["decision_rule_hash"],
                "adapter_schema_hash": package["adapter_schema_hash"],
                "score_columns_hash": package["score_columns_hash"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "next_action": NEXT_ACTION,
            }
        )
        identity_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "feature_order_hash": package["feature_contract"]["base_feature_order_hash"],
                "feature_contract_hash": package["feature_contract_hash"],
                "blueprint_hash": package["blueprint_hash"],
                "decision_rule_hash": package["decision_rule_hash"],
                "adapter_schema_hash": package["adapter_schema_hash"],
                "score_columns_hash": package["score_columns_hash"],
                "identity_judgment": "blueprint_identity_materialized_no_performance_claim(청사진 정체성 물질화, 성과 주장 없음)",
            }
        )
        scoring_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "columns_or_fields": ";".join(package["score_columns"]),
                "hash_value": package["score_columns_hash"],
                "source": "run277B package_blueprints.json(277B 패키지 청사진)",
                "effect": "run277C(277C 실행)가 점수 열을 결정적으로 만들 수 있게 한다.",
            }
        )
        adapter_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "columns_or_fields": ";".join(package["adapter_schema"]),
                "hash_value": package["adapter_schema_hash"],
                "source": "run277B package_blueprints.json(277B 패키지 청사진)",
                "effect": "Adapter handoff(어댑터 인계) 필드 의미를 고정한다.",
            }
        )
        handoff_fields = [
            "package_id",
            "feature_order_hash",
            "feature_contract_hash",
            "blueprint_hash",
            "decision_rule_hash",
            "adapter_schema_hash",
            "score_columns_hash",
            "claim_boundary",
        ]
        handoff_rows.append(
            {
                "package_id": package["package_id"],
                "handoff_file_plan": f"stages/{STAGE_ID}/02_runs/run277C/handoff/{package['package_id']}_handoff.json",
                "required_hashes": "feature_order_hash;feature_contract_hash;blueprint_hash;decision_rule_hash;adapter_schema_hash;score_columns_hash",
                "runtime_payload_fields": ";".join(handoff_fields),
                "next_consumer": NEXT_ACTION,
                "boundary": BOUNDARY,
            }
        )
    return package_rows, identity_rows, scoring_rows, adapter_rows, handoff_rows


def write_report(packages: Sequence[Mapping[str, Any]]) -> None:
    lines = "\n".join(
        f"- `{package['package_id']}`: blueprint_hash(청사진 해시) `{package['blueprint_hash'][:12]}`; score_columns(점수 열) `{len(package['score_columns'])}`"
        for package in packages
    )
    write_md(
        REPORT,
        f"""# run277B Report(277B 보고서): Fresh Thesis Candidate Blueprint Materialization(새 논제 후보 청사진 물질화)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- package_rows(패키지 행): `{len(packages)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Blueprint Rows(청사진 행)

{lines}

## Meaning(의미)

run277B(277B 실행)는 package blueprint(패키지 청사진), feature contract(피처 계약), decision rule hash(판단 규칙 해시), adapter schema hash(어댑터 스키마 해시)를 만들었다.
Effect(효과): 다음 run277C(277C 실행)가 scoring/handoff input(점수/인계 입력)을 만들 수 있지만, selected candidate(선택 후보)나 ONNX readiness(온엑스 준비)는 아직 없다.
""",
    )


def write_receipts(packages: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run277B fresh thesis candidate blueprint materialization(277B 새 논제 후보 청사진 물질화)",
                "evidence_available": "package_blueprints.json(패키지 청사진), identity receipts(정체성 영수증), scoring column plan(점수 열 계획), adapter schema plan(어댑터 스키마 계획)",
                "evidence_missing": "materialized score table(물질화 점수표), MT5 runtime result(MT5 런타임 결과), selected candidate(선택 후보), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "blueprint_materialized_no_selection(청사진 물질화, 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "청사진은 생겼지만 아직 후보 선택이나 ONNX(온엑스) 준비가 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "feature_order_trace_gate(피처 순서 추적 게이트)",
                "status": "passed_base_feature_order_hash_recorded(기본 피처 순서 해시 기록으로 통과)",
                "evidence_path": rel(PACKAGE_BLUEPRINTS_JSON),
                "effect": "기존 58개 feature order(피처 순서)를 새 파생 피처와 분리해 추적한다.",
            },
            {
                "gate_name": "blueprint_identity_gate(청사진 정체성 게이트)",
                "status": "passed_hash_receipts_written(해시 영수증 작성으로 통과)",
                "evidence_path": rel(BLUEPRINT_IDENTITY),
                "effect": "package(패키지)마다 blueprint/decision/adapter/score hash(청사진/판단/어댑터/점수 해시)를 가진다.",
            },
            {
                "gate_name": "adapter_handoff_gate(어댑터 인계 게이트)",
                "status": "passed_handoff_skeletons_written(인계 골격 작성으로 통과)",
                "evidence_path": rel(HANDOFF_SKELETONS),
                "effect": "runtime handoff(런타임 인계)가 다음 실행 입력으로 추적된다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "청사진 물질화를 선택 후보로 올려 말하지 않는다.",
            },
        ],
    )


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], packages: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    sources = [SOURCE_PACKAGE_QUEUE, SOURCE_REQUIRED_EVIDENCE, SOURCE_ADAPTER_PLAN, SOURCE_MANIFEST, FEATURE_ORDER, FEATURE_MANIFEST, MODEL_INPUT_SUMMARY]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "consumer": [STAGE_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "source_inputs": [rel(path) for path in sources],
        "source_hashes": output_hashes(sources),
        "output_artifacts": [rel(path) for path in outputs],
        "output_hashes": output_hashes(outputs),
        "package_count": len(packages),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": manifest["consumer"],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, packages: Sequence[Mapping[str, Any]], outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "blueprint_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"package_rows={len(packages)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__blueprint_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "blueprint_materialization",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "run277B blueprint materialization(277B 청사진 물질화)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "blueprint",
                "scoreboard_lane": "fresh_thesis_rebuild",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"package_rows={len(packages)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_blueprint_materialization",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__blueprint_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_candidate_blueprint_materialization",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "blueprint_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "blueprint_only_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"package_rows={len(packages)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run277B_blueprint_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run277B blueprint artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(packages: Sequence[Mapping[str, Any]]) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run277B_report", f"- run277B_report(277B 보고서): `{rel(REPORT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run277B_report",
        "\n".join(
            [
                f"- run277B_report(277B 보고서): `{rel(REPORT)}`",
                f"- run277B_blueprints(277B 청사진): `{rel(PACKAGE_BLUEPRINTS_JSON)}`",
                f"- run277B_identity(277B 정체성): `{rel(BLUEPRINT_IDENTITY)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_candidate_blueprint_materialization`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run277B_summary",
        (
            f"- run277B_summary(277B 요약): package blueprint(패키지 청사진) `{len(packages)}`개와 "
            "feature contract/decision rule/adapter schema/hash receipts(피처 계약/판단 규칙/어댑터 스키마/해시 영수증)를 만들었다. "
            "Effect(효과): run277C(277C 실행) scoring/handoff input(점수/인계 입력)으로 넘기며 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage277(277단계) run277B(277B 실행) fresh thesis candidate blueprint materialization(새 논제 후보 청사진 물질화) `{RUN_ID}`. "
        f"Effect(효과): package blueprint(패키지 청사진) `{len(packages)}`개와 hash receipts(해시 영수증)를 만들었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage277(277단계) run277B(277B 실행)")
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run277B Fresh thesis candidate blueprint materialization(새 논제 후보 청사진 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): blueprint(청사진) `{len(packages)}`개를 만들고 run277C(277C 실행) scoring/handoff input(점수/인계 입력)으로 넘긴다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST277-FRESH-THESIS-REBUILD-RUN277B",
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277B` | `{STAGE_ID}` | run277A(277A 실행) package queue(패키지 대기열)를 materialized blueprint(물질화 청사진)로 바꾼다. | `blueprints={len(packages)}` | `blueprint_materialized_no_selection` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def run() -> dict[str, Any]:
    must_exist([SOURCE_PACKAGE_QUEUE, SOURCE_REQUIRED_EVIDENCE, SOURCE_ADAPTER_PLAN, SOURCE_MANIFEST, FEATURE_ORDER, FEATURE_MANIFEST, MODEL_INPUT_SUMMARY])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    feature_order = read_feature_order()
    package_queue = read_csv_rows(SOURCE_PACKAGE_QUEUE)
    blueprints, packages = materialize_blueprints(package_queue, feature_order)
    package_rows, identity_rows, scoring_rows, adapter_rows, handoff_rows = csv_rows_from_packages(packages)
    write_json(PACKAGE_BLUEPRINTS_JSON, blueprints)
    write_csv(PACKAGE_BLUEPRINTS_CSV, PACKAGE_COLUMNS, package_rows)
    write_csv(BLUEPRINT_IDENTITY, IDENTITY_COLUMNS, identity_rows)
    write_csv(SCORING_COLUMN_PLAN, PLAN_COLUMNS, scoring_rows)
    write_csv(ADAPTER_SCHEMA_PLAN, PLAN_COLUMNS, adapter_rows)
    write_csv(HANDOFF_INDEX, HANDOFF_COLUMNS, handoff_rows)
    write_json(HANDOFF_SKELETONS, {"run_id": RUN_ID, "stage_id": STAGE_ID, "handoff_rows": handoff_rows, "claim_boundary": BOUNDARY})
    write_report(packages)
    write_receipts(packages)

    outputs = [
        PACKAGE_BLUEPRINTS_JSON,
        PACKAGE_BLUEPRINTS_CSV,
        BLUEPRINT_IDENTITY,
        SCORING_COLUMN_PLAN,
        ADAPTER_SCHEMA_PLAN,
        HANDOFF_SKELETONS,
        HANDOFF_INDEX,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
    ]
    manifest = manifest_payload(created_at, outputs, packages)
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, outputs, packages)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    outputs.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, outputs, packages)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, packages, outputs)
    update_state_docs(packages)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "package_rows": len(packages),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
