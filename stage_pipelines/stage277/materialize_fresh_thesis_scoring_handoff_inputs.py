from __future__ import annotations

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
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild"
RUN_ID = "run277C_materialize_fresh_thesis_scoring_handoff_inputs_v1"
SOURCE_RUN_ID = "run277B_materialize_fresh_thesis_candidate_blueprints_v1"
STATUS = "completed_fresh_thesis_scoring_handoff_input_materialization_no_candidate_selection"
JUDGMENT = "fresh_thesis_scoring_handoff_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run277D_execute_fresh_thesis_scoring_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN277B = STAGE / "02_runs" / "run277B"
RUN_DIR = STAGE / "02_runs" / "run277C"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SOURCE_BLUEPRINTS = RUN277B / "package_blueprints.json"
SOURCE_IDENTITY = RUN277B / "blueprint_identity_receipts.csv"
SOURCE_HANDOFF = RUN277B / "handoff_skeleton_index.csv"
SOURCE_MANIFEST = RUN277B / "run_manifest.json"

SCORING_SPECS_JSON = RUN_DIR / "scoring_input_specs.json"
SCORING_SPECS_CSV = RUN_DIR / "scoring_input_specs.csv"
HANDOFF_INPUT_PLAN = RUN_DIR / "handoff_input_plan.csv"
PACKAGE_IDENTITY = RUN_DIR / "package_identity_receipts.csv"
FEATURE_CONTRACT_RECEIPTS = RUN_DIR / "feature_contract_receipts.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run277C_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage277/materialize_fresh_thesis_scoring_handoff_inputs.py")

SCORING_COLUMNS = (
    "package_id",
    "package_role",
    "materialization_status",
    "feature_order_hash",
    "feature_contract_hash",
    "feature_surface",
    "score_columns",
    "score_columns_hash",
    "model_or_scoring_surface",
    "decision_surface",
    "decision_rule_hash",
    "risk_logic",
    "adapter_schema",
    "adapter_schema_hash",
    "runtime_handoff_fields",
    "runtime_handoff_plan",
    "claim_boundary",
)
HANDOFF_COLUMNS = (
    "package_id",
    "package_role",
    "handoff_file_plan",
    "required_hashes",
    "runtime_payload_fields",
    "runtime_claim_boundary",
    "next_consumer",
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
FEATURE_CONTRACT_COLUMNS = (
    "package_id",
    "base_feature_order_hash",
    "base_features",
    "derived_features",
    "feature_contract_hash",
    "feature_contract_judgment",
)
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


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def load_blueprints() -> dict[str, Any]:
    return json.loads(io_path(SOURCE_BLUEPRINTS).read_text(encoding="utf-8"))


def materialize_specs(blueprints: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    scoring_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    for package in blueprints["packages"]:
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
        scoring_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "materialization_status": "scoring_handoff_input_spec_materialized(점수/인계 입력 규격 물질화)",
                "feature_order_hash": package["feature_contract"]["base_feature_order_hash"],
                "feature_contract_hash": package["feature_contract_hash"],
                "feature_surface": package["feature_contract"]["feature_surface"],
                "score_columns": ";".join(package["score_columns"]),
                "score_columns_hash": package["score_columns_hash"],
                "model_or_scoring_surface": package["model_or_scoring_surface"],
                "decision_surface": package["decision_surface"],
                "decision_rule_hash": package["decision_rule_hash"],
                "risk_logic": package["risk_logic"],
                "adapter_schema": ";".join(package["adapter_schema"]),
                "adapter_schema_hash": package["adapter_schema_hash"],
                "runtime_handoff_fields": ";".join(handoff_fields),
                "runtime_handoff_plan": package["runtime_handoff_plan"],
                "claim_boundary": BOUNDARY,
            }
        )
        handoff_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "handoff_file_plan": f"stages/{STAGE_ID}/02_runs/run277D/handoff/{package['package_id']}_handoff.json",
                "required_hashes": "feature_order_hash;feature_contract_hash;blueprint_hash;decision_rule_hash;adapter_schema_hash;score_columns_hash",
                "runtime_payload_fields": ";".join(handoff_fields),
                "runtime_claim_boundary": BOUNDARY,
                "next_consumer": NEXT_ACTION,
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
                "identity_judgment": "scoring_handoff_identity_materialized_no_performance_claim(점수/인계 정체성 물질화, 성과 주장 없음)",
            }
        )
        feature_rows.append(
            {
                "package_id": package["package_id"],
                "base_feature_order_hash": package["feature_contract"]["base_feature_order_hash"],
                "base_features": ";".join(package["feature_contract"]["base_features"]),
                "derived_features": ";".join(package["feature_contract"]["derived_features"]),
                "feature_contract_hash": package["feature_contract_hash"],
                "feature_contract_judgment": "connected_to_base_58_feature_order_with_derived_features_declared(기본 58개 피처 순서에 연결되고 파생 피처 선언됨)",
            }
        )
    return scoring_rows, handoff_rows, identity_rows, feature_rows


def write_report(scoring_rows: Sequence[Mapping[str, Any]]) -> None:
    lines = "\n".join(
        f"- `{row['package_id']}`: score_columns(점수 열) `{row['score_columns']}`"
        for row in scoring_rows
    )
    write_md(
        REPORT,
        f"""# run277C Report(277C 보고서): Fresh Thesis Scoring/Handoff Inputs(새 논제 점수/인계 입력)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- package_rows(패키지 행): `{len(scoring_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Scoring Inputs(점수 입력)

{lines}

## Boundary(경계)

run277C(277C 실행)는 scoring/handoff input(점수/인계 입력)을 고정했다.
Effect(효과): 다음 run277D(277D 실행)가 점수표와 handoff JSON(인계 JSON)을 만들 수 있지만 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 아직 없다.
""",
    )


def write_receipts() -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run277C scoring/handoff input materialization(277C 점수/인계 입력 물질화)",
                "evidence_available": "scoring input specs(점수 입력 규격), handoff plan(인계 계획), identity receipts(정체성 영수증), feature contract receipts(피처 계약 영수증)",
                "evidence_missing": "score table(점수표), MT5 runtime result(MT5 런타임 결과), selected candidate(선택 후보), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "input_materialized_no_selection(입력 물질화, 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "점수/인계 입력은 생겼지만 후보 선택은 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "scoring_input_gate(점수 입력 게이트)",
                "status": "passed_scoring_specs_written(점수 규격 작성으로 통과)",
                "evidence_path": rel(SCORING_SPECS_JSON),
                "effect": "각 package(패키지)의 score columns(점수 열)를 고정한다.",
            },
            {
                "gate_name": "runtime_handoff_gate(런타임 인계 게이트)",
                "status": "passed_handoff_plan_written(인계 계획 작성으로 통과)",
                "evidence_path": rel(HANDOFF_INPUT_PLAN),
                "effect": "run277D(277D 실행)가 handoff JSON(인계 JSON)을 만들 수 있다.",
            },
            {
                "gate_name": "feature_contract_gate(피처 계약 게이트)",
                "status": "passed_feature_contract_receipts_written(피처 계약 영수증 작성으로 통과)",
                "evidence_path": rel(FEATURE_CONTRACT_RECEIPTS),
                "effect": "기본 58개 피처와 파생 피처가 분리되어 추적된다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "입력 물질화를 후보 선택으로 올려 말하지 않는다.",
            },
        ],
    )


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], package_count: int) -> dict[str, Any]:
    sources = [SOURCE_BLUEPRINTS, SOURCE_IDENTITY, SOURCE_HANDOFF, SOURCE_MANIFEST]
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
        "package_count": package_count,
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


def update_registers(created_at: str, package_count: int, outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "scoring_handoff_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"package_rows={package_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__scoring_handoff_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "scoring_handoff_inputs",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "run277C scoring/handoff inputs(277C 점수/인계 입력)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "input_materialization",
                "scoreboard_lane": "fresh_thesis_rebuild",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"package_rows={package_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_input_materialization",
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
                "row_id": f"{RUN_ID}__scoring_handoff_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_scoring_handoff_input_materialization",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "input_materialization_only_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"package_rows={package_count};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run277C_scoring_handoff_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run277C scoring/handoff input artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(package_count: int) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run277C_report", f"- run277C_report(277C 보고서): `{rel(REPORT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run277C_report",
        "\n".join(
            [
                f"- run277C_report(277C 보고서): `{rel(REPORT)}`",
                f"- run277C_scoring_specs(277C 점수 규격): `{rel(SCORING_SPECS_JSON)}`",
                f"- run277C_handoff_plan(277C 인계 계획): `{rel(HANDOFF_INPUT_PLAN)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_scoring_handoff_input_materialization`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run277C_summary",
        (
            f"- run277C_summary(277C 요약): scoring/handoff input(점수/인계 입력) `{package_count}`개를 만들었다. "
            "Effect(효과): run277D(277D 실행)가 점수표와 handoff JSON(인계 JSON)을 만들 수 있지만 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage277(277단계) run277C(277C 실행) fresh thesis scoring/handoff input materialization(새 논제 점수/인계 입력 물질화) `{RUN_ID}`. "
        f"Effect(효과): scoring specs(점수 규격) `{package_count}`개와 handoff plan(인계 계획)을 만들었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage277(277단계) run277C(277C 실행)")
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run277C Fresh thesis scoring/handoff input materialization(새 논제 점수/인계 입력 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): scoring specs(점수 규격) `{package_count}`개를 만들고 run277D(277D 실행) scoring probe(점수 탐침)로 넘긴다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST277-FRESH-THESIS-REBUILD-RUN277C",
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277C` | `{STAGE_ID}` | run277B(277B 실행) blueprints(청사진)를 scoring/handoff input(점수/인계 입력)으로 바꾼다. | `scoring_specs={package_count}` | `input_materialized_no_selection` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def run() -> dict[str, Any]:
    must_exist([SOURCE_BLUEPRINTS, SOURCE_IDENTITY, SOURCE_HANDOFF, SOURCE_MANIFEST])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    blueprints = load_blueprints()
    scoring_rows, handoff_rows, identity_rows, feature_rows = materialize_specs(blueprints)
    write_json(
        SCORING_SPECS_JSON,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "feature_order_hash": blueprints["shared_controls"]["feature_order_hash"],
            "claim_boundary": BOUNDARY,
            "packages": scoring_rows,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
        },
    )
    write_csv(SCORING_SPECS_CSV, SCORING_COLUMNS, scoring_rows)
    write_csv(HANDOFF_INPUT_PLAN, HANDOFF_COLUMNS, handoff_rows)
    write_csv(PACKAGE_IDENTITY, IDENTITY_COLUMNS, identity_rows)
    write_csv(FEATURE_CONTRACT_RECEIPTS, FEATURE_CONTRACT_COLUMNS, feature_rows)
    write_report(scoring_rows)
    write_receipts()

    outputs = [
        SCORING_SPECS_JSON,
        SCORING_SPECS_CSV,
        HANDOFF_INPUT_PLAN,
        PACKAGE_IDENTITY,
        FEATURE_CONTRACT_RECEIPTS,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
    ]
    manifest = manifest_payload(created_at, outputs, len(scoring_rows))
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, outputs, len(scoring_rows))
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    outputs.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, outputs, len(scoring_rows))
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, len(scoring_rows), outputs)
    update_state_docs(len(scoring_rows))

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "package_rows": len(scoring_rows),
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
