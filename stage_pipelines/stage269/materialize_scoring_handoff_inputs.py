from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
RUN_ID = "run269C_materialized_scoring_handoff_inputs_v1"
RUN_ROOT = ROOT / "stages" / STAGE_ID / "02_runs" / "run269C"
REVIEW_ROOT = ROOT / "stages" / STAGE_ID / "03_reviews"
SOURCE_BLUEPRINTS = ROOT / "stages" / STAGE_ID / "02_runs" / "run269B" / "package_blueprints.json"
SOURCE_MANIFEST = ROOT / "stages" / STAGE_ID / "02_runs" / "run269B" / "run_manifest.json"

CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

BASE_ADAPTER_OUTPUTS = [
    "entry_signal",
    "route_code",
    "model_risk_pct",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "max_hold_bars",
    "reentry_cooldown_bars",
]

SCORING_COLUMNS = {
    "cp269A_asymmetric_nonfilter_reentry_surface": [
        "entry_probability",
        "reward_skew_score",
        "weak_context_cost",
        "failure_zone_cut_flag",
        "candidate_decision_score",
    ],
    "cp269B_identity_collapse_disambiguator": [
        "source_mask_id",
        "source_a_score",
        "source_b_score",
        "divergence_metric",
        "duplicate_signature_flag",
    ],
    "cp269C_session_skew_reward_surface": [
        "session_code",
        "session_reward_score",
        "session_risk_cap",
        "distance_to_open_close",
        "morphology_shock",
    ],
    "cp269D_runtime_handoff_isolation_control": [
        "feature_order_hash",
        "model_hash",
        "adapter_hash",
        "handoff_hash",
        "identity_match_flag",
    ],
}

TELEMETRY_EXTENSIONS = {
    "cp269A_asymmetric_nonfilter_reentry_surface": [
        "reward_skew_score",
        "weak_context_cost",
        "decision_rule_hash",
        "package_id",
    ],
    "cp269B_identity_collapse_disambiguator": [
        "feature_order_hash",
        "model_hash",
        "decision_hash",
        "divergence_metric",
        "duplicate_signature_flag",
    ],
    "cp269C_session_skew_reward_surface": [
        "session_code",
        "session_reward_score",
        "session_risk_cap",
        "adapter_schema_extension_flag",
    ],
    "cp269D_runtime_handoff_isolation_control": [
        "feature_order_hash",
        "model_hash",
        "adapter_hash",
        "handoff_hash",
        "identity_match_flag",
    ],
}


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig")


def package_hash(package: dict[str, Any]) -> str:
    return sha256_text(json.dumps(package, ensure_ascii=False, sort_keys=True))


def materialize() -> dict[str, Any]:
    blueprints = json.loads(SOURCE_BLUEPRINTS.read_text(encoding="utf-8"))
    source_manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    shared_controls = blueprints["shared_controls"]
    packages = blueprints["packages"]

    scoring_specs: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []

    for package in packages:
        package_id = package["package_id"]
        score_columns = SCORING_COLUMNS[package_id]
        telemetry_extensions = TELEMETRY_EXTENSIONS[package_id]
        adapter_schema = BASE_ADAPTER_OUTPUTS + telemetry_extensions
        decision_rule_hash = sha256_text(
            "|".join(
                [
                    package_id,
                    package["decision_surface"],
                    package["risk_logic"],
                    ",".join(package["changed_variables"]),
                ]
            )
        )
        adapter_schema_hash = sha256_text("\n".join(adapter_schema))
        blueprint_hash = package_hash(package)
        handoff_fields = [
            "package_id",
            "feature_order_hash",
            "blueprint_hash",
            "decision_rule_hash",
            "adapter_schema_hash",
            "score_columns_hash",
            "claim_boundary",
        ]

        scoring_specs.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "materialization_status": "scoring_handoff_input_spec_materialized",
                "feature_order_hash": shared_controls["feature_order_hash"],
                "feature_surface": package["feature_surface"],
                "scoring_columns": score_columns,
                "score_columns_hash": sha256_text("\n".join(score_columns)),
                "model_or_scoring_surface": package["model_or_scoring_surface"],
                "decision_surface": package["decision_surface"],
                "decision_rule_hash": decision_rule_hash,
                "risk_logic": package["risk_logic"],
                "adapter_schema": adapter_schema,
                "adapter_schema_hash": adapter_schema_hash,
                "runtime_handoff_fields": handoff_fields,
                "runtime_handoff_plan": package["runtime_handoff_plan"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        handoff_rows.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "handoff_file_plan": f"stages/{STAGE_ID}/02_runs/run269D/handoff/{package_id}_handoff.json",
                "required_hashes": "feature_order_hash;blueprint_hash;decision_rule_hash;adapter_schema_hash;score_columns_hash",
                "runtime_payload_fields": ";".join(handoff_fields),
                "runtime_claim_boundary": CLAIM_BOUNDARY,
                "next_consumer": "run269D_execute_scoring_materialization_probe",
            }
        )
        identity_rows.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "feature_order_hash": shared_controls["feature_order_hash"],
                "blueprint_hash": blueprint_hash,
                "decision_rule_hash": decision_rule_hash,
                "adapter_schema_hash": adapter_schema_hash,
                "score_columns_hash": sha256_text("\n".join(score_columns)),
                "identity_judgment": "input_identity_materialized_no_performance_claim",
            }
        )

    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)

    scoring_spec_path = RUN_ROOT / "scoring_input_specs.json"
    handoff_plan_path = RUN_ROOT / "handoff_input_plan.csv"
    identity_receipts_path = RUN_ROOT / "package_identity_receipts.csv"
    manifest_path = RUN_ROOT / "run_manifest.json"
    lineage_path = RUN_ROOT / "lineage.json"
    report_path = REVIEW_ROOT / "run269C_report.md"

    write_json(
        scoring_spec_path,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_blueprint_run": source_manifest["run_id"],
            "feature_order_hash": shared_controls["feature_order_hash"],
            "claim_boundary": CLAIM_BOUNDARY,
            "packages": scoring_specs,
        },
    )
    write_csv(
        handoff_plan_path,
        handoff_rows,
        [
            "package_id",
            "package_role",
            "handoff_file_plan",
            "required_hashes",
            "runtime_payload_fields",
            "runtime_claim_boundary",
            "next_consumer",
        ],
    )
    write_csv(
        identity_receipts_path,
        identity_rows,
        [
            "package_id",
            "package_role",
            "feature_order_hash",
            "blueprint_hash",
            "decision_rule_hash",
            "adapter_schema_hash",
            "score_columns_hash",
            "identity_judgment",
        ],
    )

    output_paths = [scoring_spec_path, handoff_plan_path, identity_receipts_path]
    input_hashes = {
        repo_path(SOURCE_BLUEPRINTS): sha256_file(SOURCE_BLUEPRINTS),
        repo_path(SOURCE_MANIFEST): sha256_file(SOURCE_MANIFEST),
    }
    output_hashes = {repo_path(path): sha256_file(path) for path in output_paths}

    manifest_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "completed_scoring_handoff_input_materialization_no_candidate_selection",
        "producer": "stage_pipelines/stage269/materialize_scoring_handoff_inputs.py",
        "entry_command": "python stage_pipelines/stage269/materialize_scoring_handoff_inputs.py",
        "source_inputs": list(input_hashes.keys()),
        "input_hashes": input_hashes,
        "output_artifacts": [repo_path(path) for path in output_paths],
        "output_hashes": output_hashes,
        "package_count": len(packages),
        "selectable_packages": sum(1 for package in packages if package["package_role"] == "selectable_blueprint"),
        "support_controls": sum(1 for package in packages if package["package_role"] == "support_control"),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": "run269D_execute_scoring_materialization_probe",
    }
    write_json(manifest_path, manifest_payload)

    report = f"""# Stage269 Run269C Scoring/Handoff Input Materialization(269단계 269C 점수/인계 입력 물질화)

- status(상태): `completed_scoring_handoff_input_materialization_no_candidate_selection`
- run(실행): `{RUN_ID}`
- source_run(원천 실행): `{source_manifest["run_id"]}`
- packages(패키지): `{len(packages)}`
- selectable_packages(선택 가능 패키지): `{manifest_payload["selectable_packages"]}`
- support_controls(보조 대조): `{manifest_payload["support_controls"]}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run269D_execute_scoring_materialization_probe`

## Plain Result(쉬운 결과)

run269C(269C 실행)는 run269B(269B 실행)의 candidate package blueprint(후보 패키지 청사진)를 scoring input spec(점수 입력 규격), handoff input plan(인계 입력 계획), package identity receipt(패키지 정체성 영수증)로 바꿨다.
효과(effect, 효과): 다음 run269D(269D 실행)는 각 package(패키지)의 score columns(점수 열), adapter schema hash(어댑터 스키마 해시), decision rule hash(판단 규칙 해시), handoff payload fields(인계 페이로드 필드)를 소비할 수 있다.

## Artifacts(산출물)

- run_manifest(실행 목록): `{repo_path(manifest_path)}`
- scoring_input_specs(점수 입력 규격): `{repo_path(scoring_spec_path)}`
- handoff_input_plan(인계 입력 계획): `{repo_path(handoff_plan_path)}`
- package_identity_receipts(패키지 정체성 영수증): `{repo_path(identity_receipts_path)}`
- lineage(계보): `{repo_path(lineage_path)}`

## Boundary(경계)

This report(이 보고서)는 deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
"""
    write_md(report_path, report)

    lineage_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_inputs": list(input_hashes.keys()),
        "producer": "stage_pipelines/stage269/materialize_scoring_handoff_inputs.py",
        "consumer": "run269D_execute_scoring_materialization_probe",
        "artifact_paths": [repo_path(path) for path in [manifest_path, *output_paths, lineage_path, report_path]],
        "artifact_hashes": {
            **input_hashes,
            **output_hashes,
            repo_path(manifest_path): sha256_file(manifest_path),
            repo_path(report_path): sha256_file(report_path),
        },
        "self_hash_note": "lineage file hash is recorded in docs/registers/artifact_registry.csv after generation",
        "registry_links": [
            "docs/registers/run_registry.csv",
            "docs/registers/alpha_run_ledger.csv",
            f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv",
            "docs/registers/artifact_registry.csv",
        ],
        "availability": "tracked",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(lineage_path, lineage_payload)

    final_hashes = {repo_path(path): sha256_file(path) for path in [manifest_path, scoring_spec_path, handoff_plan_path, identity_receipts_path, lineage_path, report_path]}
    return {
        "run_id": RUN_ID,
        "status": manifest_payload["status"],
        "packages": len(packages),
        "outputs": final_hashes,
    }


if __name__ == "__main__":
    print(json.dumps(materialize(), ensure_ascii=False, indent=2))
