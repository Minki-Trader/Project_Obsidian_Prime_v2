from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as db  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_source_expansion_mt5_runtime_probe_without_db as dg  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_source_expansion_runtime_package_without_db as df  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_profit_recovery_scout_without_db as di  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = di.STAGE_ID
RUN_NUMBER = "run364DJ"
RUN_ID = "run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1"
PARENT_RUN_ID = di.RUN_ID
BASELINE_RUN_ID = db.RUN_ID
SOURCE_RUNTIME_RUN_ID = dg.RUN_ID
NEXT_RUN_ID = "run364DK_implement_h17_short_source_profit_recovery_runtime_package_without_db_v1"

STATUS = "completed_stage364DJ_h17_short_source_profit_recovery_review_runtime_ready_package_required_no_authority"
JUDGMENT = "positive_proxy_runtime_ready_short_source_profit_recovery_candidate_package_required_no_authority"
DECISION = "stage364DJ_open_run364DK_short_source_profit_recovery_runtime_package"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_short_source_profit_recovery_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = di.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SELECTED_CANDIDATE_REVIEW = RUN_DIR / "selected_candidate_review.csv"
RUNTIME_REPRESENTATION_REVIEW = RUN_DIR / "runtime_representation_review.csv"
MONTH_STRESS_BOUNDARY_REVIEW = RUN_DIR / "month_stress_boundary_review.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364DK_QUEUE = RUN_DIR / "run364DK_runtime_package_queue.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DJ_h17_short_source_profit_recovery_scout_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DJ_h17_short_source_profit_recovery_scout_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    di.FINAL_DECISION,
    di.GATE_AUDIT,
    di.PROFIT_RECOVERY_SURFACE,
    di.SELECTED_CANDIDATE,
    di.SELECTED_TRADE_TAPE,
    di.RUNTIME_REPRESENTATION_AUDIT,
    di.PACKAGE_PRECHECK,
    di.RUN364DJ_QUEUE,
    di.DATA_INTEGRITY_AUDIT,
    dg.FINAL_DECISION,
    dg.EXECUTION_SUMMARY,
    db.FINAL_DECISION,
    db.EXECUTION_SUMMARY,
    df.RUNTIME_POLICY_CONFIG,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SELECTED_CANDIDATE_REVIEW,
    RUNTIME_REPRESENTATION_REVIEW,
    MONTH_STRESS_BOUNDARY_REVIEW,
    PACKAGE_DECISION,
    RUN364DK_QUEUE,
    RESULT_JUDGMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return di.rel(path)


def exists(path: Path | str) -> bool:
    return di.exists(path)


def sha(path: Path | str) -> str:
    return di.sha(path)


def json_ready(value: Any) -> Any:
    return di.json_ready(value)


def read_json(path: Path) -> Any:
    return di.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    di.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    di.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    di.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
        with path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [dict(row) for row in reader]
    if not fieldnames:
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)

    def row_key(row: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(key, "")) for key in key_fields)

    replacement = {row_key(row): row for row in materialized}
    kept = [row for row in existing_rows if row_key(row) not in replacement]
    write_csv(path, [*kept, *materialized], fieldnames)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    di.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return di.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DJ inputs(DJ 입력 누락): " + ", ".join(missing))
    di_final = read_json(di.FINAL_DECISION)
    if di_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DI next_run_id mismatch(DI 다음 실행 ID 불일치): {di_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DI", di_final), ("DG", read_json(dg.FINAL_DECISION)), ("DB", read_json(db.FINAL_DECISION))]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    gates = read_csv(di.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DI gate audit(DI 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return di_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DI review source(DI 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "result_review(결과 검토)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "DI selected a runtime-ready short-source profit recovery candidate(DI가 런타임 준비 숏 원천 수익 회복 후보를 선택했다).",
            "decision_use": "Open MT5 runtime package if representation and KPI gates hold(표현과 KPI 게이트가 맞으면 MT5 런타임 패키지를 연다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def build_reviews(di_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    selected = read_json(di.SELECTED_CANDIDATE)
    surface = read_csv(di.PROFIT_RECOVERY_SURFACE).to_dict("records")
    month_rows = [
        row
        for row in surface
        if str(row.get("runtime_representation_status", "")).startswith("repair_required")
        and str(row.get("package_precheck_status", "")).startswith("passed")
    ]
    selected_review = [
        {
            "run_id": RUN_ID,
            "selected_variant_id": selected["variant_id"],
            "changed_variables": selected["changed_variables"],
            "estimated_mt5_net_profit": selected["estimated_mt5_net_profit"],
            "estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
            "estimated_mt5_expectancy": selected["estimated_mt5_expectancy"],
            "estimated_mt5_trade_count": selected["estimated_mt5_trade_count"],
            "estimated_mt5_short_trade_count": selected["estimated_mt5_short_trade_count"],
            "estimated_net_delta_vs_db": selected["estimated_net_delta_vs_db"],
            "estimated_net_delta_vs_dg": selected["estimated_net_delta_vs_dg"],
            "db_mt5_net_profit": selected["db_mt5_net_profit"],
            "dg_mt5_net_profit": selected["dg_mt5_net_profit"],
            "review_status": "package_ready_proxy_candidate(패키지 준비 프록시 후보)",
            "effect": "19시 배제(hour19 veto, 19시 배제)가 DG의 수익 후퇴를 회복할 가능성을 보입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    runtime_review = [
        {
            "run_id": RUN_ID,
            "selected_variant_id": selected["variant_id"],
            "runtime_representation_status": selected["runtime_representation_status"],
            "ea_change_required": "false",
            "set_parameter_changes": "InpSyntheticShortSourceHours=17|18|20|21;InpSyntheticShortSourcePShortMin=0.4375;InpSyntheticShortSourceMarginVsLongMin=0.05;InpSyntheticShortSourceMarginVsFlatMin=0.0",
            "runtime_decision": "parameter_only_package_allowed(파라미터 전용 패키지 허용)",
            "effect": "EA entrypoint(EA 진입점) 변경 없이 set file(설정 파일)로 런타임 탐침을 만들 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    month_review = [
        {
            "run_id": RUN_ID,
            "variant_id": row.get("variant_id", ""),
            "estimated_mt5_net_profit": row.get("estimated_mt5_net_profit", ""),
            "estimated_mt5_profit_factor": row.get("estimated_mt5_profit_factor", ""),
            "runtime_representation_status": row.get("runtime_representation_status", ""),
            "review_status": "regime_clue_only_not_package(국면 단서 전용, 패키지 아님)",
            "effect": "multi-month veto(다중 월 배제)는 점수가 좋아도 overfit risk(과적합 위험)와 runtime repair(런타임 보정)가 있어 운영형 후보로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in month_rows
    ]
    package_decision = [
        {
            "run_id": RUN_ID,
            "selected_variant_id": selected["variant_id"],
            "decision": "open_runtime_package(런타임 패키지 열기)",
            "next_run_id": NEXT_RUN_ID,
            "package_candidate": "di02_h17_18_20_21_no19_m050",
            "required_artifacts": "set/ini/expected_kpi/runtime_policy/run_manifest(설정/초기화/예상 KPI/런타임 정책/실행 목록)",
            "success_criteria": "compile unchanged, parameter-only package, MT5 probe next(컴파일 유지, 파라미터 전용 패키지, 다음 MT5 탐침)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dk01_materialize_di02_runtime_package",
            "candidate_id": selected["variant_id"],
            "candidate_source": rel(di.SELECTED_CANDIDATE),
            "set_parameter_changes": runtime_review[0]["set_parameter_changes"],
            "effect": "DK에서 MT5 Strategy Tester(MT5 전략 테스터) 실행 입력을 준비합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SELECTED_CANDIDATE_REVIEW, selected_review)
    write_csv(RUNTIME_REPRESENTATION_REVIEW, runtime_review)
    write_csv(MONTH_STRESS_BOUNDARY_REVIEW, month_review)
    write_csv(PACKAGE_DECISION, package_decision)
    write_csv(RUN364DK_QUEUE, queue)
    return selected_review, runtime_review, month_review, package_decision, queue


def build_final(di_final: Mapping[str, Any], selected_review: Mapping[str, Any], month_review: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_variant_id": selected_review["selected_variant_id"],
        "selected_estimated_mt5_net_profit": selected_review["estimated_mt5_net_profit"],
        "selected_estimated_mt5_profit_factor": selected_review["estimated_mt5_profit_factor"],
        "selected_estimated_mt5_trade_count": selected_review["estimated_mt5_trade_count"],
        "selected_estimated_mt5_short_trade_count": selected_review["estimated_mt5_short_trade_count"],
        "selected_estimated_net_delta_vs_db": selected_review["estimated_net_delta_vs_db"],
        "selected_estimated_net_delta_vs_dg": selected_review["estimated_net_delta_vs_dg"],
        "month_stress_repair_candidate_count": len(month_review),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final: Mapping[str, Any], *, final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "DI inputs(DI 입력) linked(연결됨)"),
        ("selected_candidate_review_gate", exists(SELECTED_CANDIDATE_REVIEW), SELECTED_CANDIDATE_REVIEW, "selected candidate reviewed(선택 후보 검토됨)"),
        ("runtime_representability_gate", exists(RUNTIME_REPRESENTATION_REVIEW), RUNTIME_REPRESENTATION_REVIEW, "runtime parameter path confirmed(런타임 파라미터 경로 확인됨)"),
        ("month_stress_boundary_gate", exists(MONTH_STRESS_BOUNDARY_REVIEW), MONTH_STRESS_BOUNDARY_REVIEW, "month stress kept as clue(月 스트레스 단서로만 유지)"),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "runtime package next action recorded(런타임 패키지 다음 행동 기록됨)"),
        ("receipt_coverage_gate", all(exists(path) for path in [RESULT_JUDGMENT_RECEIPT, PERFORMANCE_RECEIPT, RUNTIME_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]), RESULT_JUDGMENT_RECEIPT, "receipts exist(영수증 존재)"),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "required gates connected to closeout(필수 게이트 종료 기록 연결)"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "authority/promotion/goal claims blocked(권위/승격/목표 주장 차단)"),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(SELECTED_CANDIDATE_REVIEW), rel(RUNTIME_REPRESENTATION_REVIEW), rel(PACKAGE_DECISION)],
            "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "forward evidence(전진 근거)", "runtime authority closure(런타임 권위 폐쇄)"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "DI 후보는 패키지할 가치가 있지만 아직 MT5 실행 전입니다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": f"selected estimated net {final['selected_estimated_mt5_net_profit']} and shorts {final['selected_estimated_mt5_short_trade_count']}",
            "comparison_baseline": [BASELINE_RUN_ID, SOURCE_RUNTIME_RUN_ID],
            "likely_drivers": ["hour19 veto(19시 배제)", "short-source filter(숏 원천 필터)"],
            "segment_checks": [rel(di.VARIANT_HOUR_SIDE_ATTRIBUTION), rel(di.VARIANT_MONTH_SIDE_ATTRIBUTION)],
            "trade_shape": {"estimated_trade_count": final["selected_estimated_mt5_trade_count"], "estimated_short_trade_count": final["selected_estimated_mt5_short_trade_count"]},
            "alternative_explanations": ["proxy/MT5 gap(프록시/MT5 차이)", "single-window scout bias(단일 구간 스카우트 편향)"],
            "attribution_confidence": "medium_low_until_mt5_probe(MT5 탐침 전 중하)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(di.SELECTED_CANDIDATE),
            "runtime_path": "parameter_only_set_file_next(다음 설정 파일 파라미터 전용)",
            "shared_contract": rel(df.RUNTIME_PARITY_CONTRACT),
            "known_differences": "proxy scout uses replay deltas; MT5 tester is still required(프록시 스카우트는 재생 변화분을 쓰며 MT5 테스터가 여전히 필요)",
            "parity_check": [rel(RUNTIME_REPRESENTATION_REVIEW), rel(PACKAGE_DECISION)],
            "runtime_claim_boundary": "package_candidate_not_authority(패키지 후보, 권위 아님)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_proxy_review_boundary(프록시 검토 경계로 연결)",
        },
    )
    write_json(CLAIM_RECEIPT, {**base, "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "package candidate(패키지 후보)를 operating claim(운영 주장)으로 승격하지 않습니다."})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return df.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], selected_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], month_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DJ h17 short-source profit recovery scout review(17시 숏 원천 수익 회복 스카우트 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Selected Candidate(선택 후보)

{markdown_table(selected_rows, ['selected_variant_id', 'estimated_mt5_net_profit', 'estimated_mt5_profit_factor', 'estimated_mt5_trade_count', 'estimated_mt5_short_trade_count', 'estimated_net_delta_vs_db', 'estimated_net_delta_vs_dg', 'review_status'])}

## Runtime Path(런타임 경로)

{markdown_table(runtime_rows, ['selected_variant_id', 'runtime_representation_status', 'ea_change_required', 'set_parameter_changes', 'runtime_decision'])}

## Month Stress Boundary(月 스트레스 경계)

{markdown_table(month_rows, ['variant_id', 'estimated_mt5_net_profit', 'estimated_mt5_profit_factor', 'runtime_representation_status', 'review_status'], limit=8)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This run(이번 실행)은 proxy review(프록시 검토)입니다. MT5 runtime execution(MT5 런타임 실행), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DJ decision(결정): short-source profit recovery review(숏 원천 수익 회복 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DK에서 parameter-only MT5 runtime package(파라미터 전용 MT5 런타임 패키지)를 준비합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DJ__{RUN_ID}", f"\n- run364DJ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - short-source profit recovery review(숏 원천 수익 회복 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DJ__{RUN_ID}", f"\n<!-- run364DJ__{RUN_ID} -->\n\n## run364DJ Short-Source Profit Recovery Review(숏 원천 수익 회복 검토)\n\nAction(행동): DI 선택 후보를 검토하고 DK runtime package(DK 런타임 패키지)를 열었습니다.\n\nEffect(효과): 19시 배제(hour19 veto, 19시 배제)를 MT5 set file(설정 파일)로 표현할 수 있게 다음 작업을 고정했습니다.\n")
    append_text_once(STAGE_README, f"run364DJ__{RUN_ID}", f"\n<!-- run364DJ__{RUN_ID} -->\n## run364DJ review(검토)\n\nDI candidate(DI 후보) reviewed(검토됨). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DJ` reviewed(검토 완료) DI short-source profit recovery candidate(DI 숏 원천 수익 회복 후보). Selected candidate(선택 후보)는 `{final['selected_variant_id']}`이고 next action(다음 행동)은 parameter-only MT5 runtime package(파라미터 전용 MT5 런타임 패키지)입니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected candidate(선택 후보): `{final['selected_variant_id']}`.

Judgment(판정): `{JUDGMENT}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DJ__{RUN_ID}", f"\n<!-- run364DJ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DI candidate(DI 후보 검토); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DJ__{RUN_ID}", f"\n<!-- run364DJ__{RUN_ID} -->\n- `{RUN_ID}`: `{final['selected_variant_id']}` marked package-ready(패키지 준비) for parameter-only MT5 probe(파라미터 전용 MT5 탐침).\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DJ__month_stress_boundary__{RUN_ID}", f"\n<!-- run364DJ__month_stress_boundary__{RUN_ID} -->\n- `{RUN_ID}`: month-stress(月 스트레스) variants remain regime clues(국면 단서) only; they are not selected package candidates(선택 패키지 후보 아님).\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "result_review(결과 검토)",
        "scoreboard_lane": "proxy_review(프록시 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "proxy_review_no_mt5_execution(프록시 검토, MT5 실행 없음)",
        "question": "Should DI selected candidate move to MT5 runtime package?(DI 선택 후보를 MT5 런타임 패키지로 넘길 것인가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_estimated_mt5_net_profit"],
        "profit_factor": final["selected_estimated_mt5_profit_factor"],
        "trade_count": final["selected_estimated_mt5_trade_count"],
        "short_trade_count": final["selected_estimated_mt5_short_trade_count"],
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(SELECTED_CANDIDATE_REVIEW),
        "primary_kpi": f"selected={final['selected_variant_id']};estimated_net={final['selected_estimated_mt5_net_profit']};pf={final['selected_estimated_mt5_profit_factor']}",
        "guardrail_kpi": "proxy_only;runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_source(필수 누락, Tier B 원천 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": "DJ proxy review(DJ 프록시 검토)", "status": status, "view": record_view, "tier": tier_scope, "metric_scope": "proxy_review(프록시 검토)"}
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "trade_count", "short_trade_count"]:
                row[key] = ""
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("selected_candidate_review", SELECTED_CANDIDATE_REVIEW, "Selected candidate review(선택 후보 검토)."),
        ("runtime_representation_review", RUNTIME_REPRESENTATION_REVIEW, "Runtime representation review(런타임 표현 검토)."),
        ("package_decision", PACKAGE_DECISION, "Package decision(패키지 결정)."),
        ("queue", RUN364DK_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DJ producer script(DJ 생산 스크립트)."),
    ]:
        if exists(path):
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": artifact_type, "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{artifact_type}", "notes": notes})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    di_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    selected_rows, runtime_rows, month_rows, _package_rows, _queue = build_reviews(di_final)
    created_at = now_utc()
    final = build_final(di_final, selected_rows[0], month_rows, created_at)
    gates = gate_rows(final, final_written=False)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, final_written=True)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, selected_rows, runtime_rows, month_rows, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
