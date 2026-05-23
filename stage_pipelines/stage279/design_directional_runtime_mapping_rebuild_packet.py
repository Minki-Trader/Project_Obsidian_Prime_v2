from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
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


STAGE279_ID = "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild"
RUN_ID = "run279A_design_directional_runtime_mapping_rebuild_packet_v1"
SOURCE_RUN_ID = "stage279_directional_runtime_mapping_rebuild_open_v1"
SOURCE_TRANSITION_RUN_ID = "run278D_close_stage278_open_stage279_directional_runtime_mapping_v1"
STATUS = "completed_directional_runtime_mapping_rebuild_packet_design_no_candidate_selection"
JUDGMENT = "directional_runtime_mapping_rebuild_packet_ready_no_candidate_selection"
NEXT_ACTION = "run279B_materialize_directional_runtime_mapping_inputs"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE279_ID
RUN_DIR = STAGE / "02_runs" / "run279A"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_BRIEF = STAGE / "00_spec" / "stage_brief.md"
SOURCE_INPUT_REFS = STAGE / "01_inputs" / "input_refs.md"
SOURCE_GAP = STAGE / "01_inputs" / "stage278_direction_mapping_gap_receipt.csv"
SOURCE_ATTEMPTS = STAGE / "01_inputs" / "stage278_blocked_attempt_summary.csv"
SOURCE_PAYLOAD_MANIFEST = STAGE / "01_inputs" / "stage278_payload_manifest.csv"
SOURCE_MT5_QUEUE = STAGE / "01_inputs" / "stage278_mt5_probe_queue.csv"
SOURCE_TIER_ROUTE = STAGE / "01_inputs" / "stage278_tier_route_receipt.csv"
SOURCE_TRANSITION_MANIFEST = ROOT / "stages" / "278_onnx_candidate_campaign__fresh_thesis_mt5_probe" / "02_runs" / "run278D" / "run_manifest.json"
SOURCE_TRANSITION_LINEAGE = ROOT / "stages" / "278_onnx_candidate_campaign__fresh_thesis_mt5_probe" / "02_runs" / "run278D" / "artifact_lineage_receipt.json"
SOURCE_CLOSEOUT = ROOT / "stages" / "278_onnx_candidate_campaign__fresh_thesis_mt5_probe" / "03_reviews" / "stage278_closeout_stage279_handoff.md"

SOURCE_STAGE277_SPEC = ROOT / "stages" / "277_onnx_candidate_campaign__fresh_thesis_rebuild" / "02_runs" / "run277C" / "scoring_input_specs.csv"
SOURCE_STAGE277_SEED = ROOT / "stages" / "277_onnx_candidate_campaign__fresh_thesis_rebuild" / "01_inputs" / "stage277_rebuild_thesis_seed_queue.csv"

DIRECTION_SOURCE_AUDIT = RUN_DIR / "direction_source_audit.csv"
BRANCH_PLAN = RUN_DIR / "direction_mapping_branch_plan.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "direction_mapping_materialization_queue.csv"
DISCARD_MATRIX = RUN_DIR / "direction_mapping_discard_matrix.csv"
RUNTIME_MAPPING_CONTRACT = RUN_DIR / "runtime_mapping_contract_plan.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run279A_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage279/design_directional_runtime_mapping_rebuild_packet.py")

AUDIT_COLUMNS = (
    "audit_id",
    "package_id",
    "source_branch_count",
    "active_flat_payload_available",
    "payload_direction_columns",
    "score_table_direction_columns",
    "stage277_direction_hint",
    "usable_direction_source",
    "blocker",
    "required_rebuild",
    "claim_boundary",
)
BRANCH_COLUMNS = (
    "branch_id",
    "package_id",
    "branch_role",
    "fresh_thesis",
    "direction_source",
    "active_mask_source",
    "direction_rule",
    "feature_source",
    "changed_variables",
    "control_variables",
    "success_condition",
    "failure_condition",
    "invalid_condition",
    "materialization_status",
    "selected_candidate",
    "onnx_readiness",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "queue_priority",
    "branch_id",
    "package_id",
    "materialization_input",
    "required_output",
    "tier_records",
    "runtime_mapping_contract",
    "next_action",
    "selected_candidate",
    "onnx_readiness",
    "claim_boundary",
)
DISCARD_COLUMNS = (
    "subject_id",
    "subject_type",
    "discard_reason",
    "salvage_value",
    "reopen_condition",
    "current_judgment",
    "claim_boundary",
)
CONTRACT_COLUMNS = (
    "branch_id",
    "runtime_signal_field",
    "allowed_values",
    "forbidden_mapping",
    "feature_order_requirement",
    "handoff_requirement",
    "mt5_probe_requirement",
    "claim_boundary",
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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


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


def source_inputs() -> list[Path]:
    return [
        SOURCE_BRIEF,
        SOURCE_INPUT_REFS,
        SOURCE_GAP,
        SOURCE_ATTEMPTS,
        SOURCE_PAYLOAD_MANIFEST,
        SOURCE_MT5_QUEUE,
        SOURCE_TIER_ROUTE,
        SOURCE_TRANSITION_MANIFEST,
        SOURCE_TRANSITION_LINEAGE,
        SOURCE_CLOSEOUT,
        SOURCE_STAGE277_SPEC,
        SOURCE_STAGE277_SEED,
    ]


def load_package_ids() -> list[str]:
    rows = read_csv_rows(SOURCE_GAP)
    packages = sorted({row["package_id"] for row in rows if row.get("package_id")})
    if not packages:
        raise RuntimeError("No package ids in Stage279 direction gap input.")
    return packages


def source_branch_count(package_id: str) -> int:
    return sum(1 for row in read_csv_rows(SOURCE_PAYLOAD_MANIFEST) if row.get("package_id") == package_id)


def payload_direction_columns(package_id: str) -> str:
    manifest = next(row for row in read_csv_rows(SOURCE_PAYLOAD_MANIFEST) if row.get("package_id") == package_id)
    payload_path = ROOT / manifest["payload_path"]
    frame = pd.read_parquet(io_path(payload_path))
    candidates = [column for column in frame.columns if "direction" in column or column in {"side", "side_state", "route_signal_value", "route_signal_label"}]
    return ";".join(candidates) if candidates else "none"


def stage277_hint(package_id: str) -> str:
    specs = read_csv_rows(SOURCE_STAGE277_SPEC)
    for row in specs:
        if row.get("package_id") == package_id:
            return f"feature_surface={row.get('feature_surface')};runtime_handoff_plan={row.get('runtime_handoff_plan')}"
    return "missing_required(필수 누락)"


def build_audit_rows(packages: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package_id in packages:
        direction_columns = payload_direction_columns(package_id)
        rows.append(
            {
                "audit_id": f"run279A_{package_id}_direction_source_audit",
                "package_id": package_id,
                "source_branch_count": source_branch_count(package_id),
                "active_flat_payload_available": "yes",
                "payload_direction_columns": direction_columns,
                "score_table_direction_columns": "none_materialized_as_direction_signal(방향 신호로 물질화된 열 없음)",
                "stage277_direction_hint": stage277_hint(package_id),
                "usable_direction_source": "no_direct_runtime_direction_source(직접 런타임 방향 원천 없음)",
                "blocker": "active_flat_only_cannot_enter_MT5_tester_without_direction_surface",
                "required_rebuild": "attach supported direction source(지원되는 방향 원천 부착) or discard(폐기)",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_branch_rows(packages: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package_id in packages:
        base = "cp277C" if package_id.startswith("cp277C") else "cp277D"
        for suffix, role, source, rule, success, failure in [
            (
                "directional_breakout_overlay",
                "rebuild_candidate(재구성 후보)",
                "foundation.features.independent_alpha_campaign directional_breakout(방향 돌파)",
                "active_mask AND directional_breakout_signal in {-1,+1}(활성 마스크와 방향 돌파 신호)",
                "Tier A/Tier B(Tier A/Tier B) validation/OOS(검증/표본외) signal supply(신호 공급)가 유지되고 directional_hit_rate(방향 적중률)가 flat/no-direction control(무방향 대조)보다 낫다.",
                "direction overlay(방향 덧씌우기)가 한쪽 방향만 과도하거나 OOS(표본외)에서 active supply(활성 공급)를 죽인다.",
            ),
            (
                "direction_consensus_overlay",
                "rebuild_candidate(재구성 후보)",
                "foundation.features.independent_alpha_campaign direction_consensus(방향 합의)",
                "active_mask AND direction_consensus_signal in {-1,+1}(활성 마스크와 방향 합의 신호)",
                "direction consensus(방향 합의)가 active mask(활성 마스크)의 공급을 줄여도 validation/OOS(검증/표본외)에서 균형을 만든다.",
                "consensus(합의)가 지나치게 희소하거나 Tier B(Tier B)에서만 좋아 보인다.",
            ),
        ]:
            branch_id = f"run279A_{base}_{suffix}"
            rows.append(
                {
                    "branch_id": branch_id,
                    "package_id": package_id,
                    "branch_role": role,
                    "fresh_thesis": f"{package_id} active/flat(활성/관망) mask(마스크)에 supported direction source(지원되는 방향 원천)를 붙이면 MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침) 의미를 만들 수 있다.",
                    "direction_source": source,
                    "active_mask_source": "Stage278 run278B payload signal_active(278B 페이로드 활성 신호)",
                    "direction_rule": rule,
                    "feature_source": "run279B must materialize feature source with timestamp/symbol/split/tier keys(run279B가 타임스탬프/심볼/분할/티어 키로 피처 원천을 물질화해야 함)",
                    "changed_variables": "direction source(방향 원천), polarity rule(극성 규칙), active mask join(활성 마스크 조인)",
                    "control_variables": "source payload hashes(원천 페이로드 해시), feature_order_hash(피처 순서 해시), Stage278 branch identity(278단계 분기 정체성)",
                    "success_condition": success,
                    "failure_condition": failure,
                    "invalid_condition": "direction source uses future label in runtime feature(런타임 피처에 미래 라벨 사용), missing join keys(조인 키 누락), or active=1 forced long/short(활성 1을 강제 롱/숏으로 변환)",
                    "materialization_status": "queue_for_run279B_direction_mapping_materialization(run279B 방향 매핑 물질화 대기)",
                    "selected_candidate": "none",
                    "onnx_readiness": "not_claimed",
                    "claim_boundary": BOUNDARY,
                }
            )
    rows.append(
        {
            "branch_id": "run279A_active_flat_discard_control",
            "package_id": "Stage278 active_flat_surfaces(278단계 활성/관망 표면)",
            "branch_role": "discard_control(폐기 대조)",
            "fresh_thesis": "지원되는 방향 원천이 없으면 active/flat(활성/관망) 표면은 MT5 tester(MT5 테스터)로 가지 않고 폐기한다.",
            "direction_source": "none(없음)",
            "active_mask_source": "Stage278 run278B payload signal_active(278B 페이로드 활성 신호)",
            "direction_rule": "blocked_do_not_map_active_to_long_or_short(차단: 활성 신호를 롱/숏으로 매핑 금지)",
            "feature_source": "not_applicable(해당 없음)",
            "changed_variables": "none(없음)",
            "control_variables": "Stage278 blocker(278단계 차단 사유)",
            "success_condition": "discard condition(폐기 조건)이 명확해져 false MT5 runtime result(가짜 MT5 런타임 결과)를 방지한다.",
            "failure_condition": "none(없음): this is a guardrail control(가드레일 대조)",
            "invalid_condition": "used as candidate(후보로 사용)",
            "materialization_status": "hold_as_discard_control(폐기 대조로 보류)",
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
    )
    return rows


def build_queue_rows(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(
        [item for item in branch_rows if str(item["materialization_status"]).startswith("queue_for_run279B")],
        start=1,
    ):
        rows.append(
            {
                "queue_id": f"run279B_{index:02d}_{row['branch_id']}",
                "queue_priority": index,
                "branch_id": row["branch_id"],
                "package_id": row["package_id"],
                "materialization_input": "Stage279 input payload manifest + direction source feature materialization(279단계 페이로드 목록 + 방향 원천 피처 물질화)",
                "required_output": "directional payload parquet(방향 페이로드 파케이); -1/0/+1 signal CSV(신호 CSV); handoff JSON(인계 JSON); parity receipt(동등성 영수증)",
                "tier_records": "Tier A used(Tier A 사용);Tier B fallback stress(Tier B 대체 스트레스);actual routed total(실제 라우팅 전체)",
                "runtime_mapping_contract": rel(RUNTIME_MAPPING_CONTRACT),
                "next_action": NEXT_ACTION,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def write_receipts(
    audit_rows: Sequence[Mapping[str, Any]],
    branch_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "active/flat(활성/관망) payload(페이로드)에 supported direction source(지원되는 방향 원천)를 붙이면 MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침)가 가능한 -1/0/+1 signal(신호)을 만들 수 있다.",
            "decision_use": "run279B materialization(물질화) 대상을 정하고, 방향 원천이 없으면 해당 active/flat 계열을 폐기한다.",
            "comparison_baseline": "Stage278 active/flat blocker(278단계 활성/관망 차단)",
            "control_variables": "Stage278 payload identity(페이로드 정체성), split/tier keys(분할/티어 키), feature_order_hash(피처 순서 해시)",
            "changed_variables": "direction source(방향 원천) and polarity rule(극성 규칙)",
            "sample_scope": "FPMarkets US100 M5, Tier A/Tier B, validation/OOS from Stage278 payloads(FPMarkets US100 5분봉, 티어 A/B, 278단계 페이로드 검증/표본외)",
            "success_criteria": "queued branches create auditable -1/0/+1 direction signal(감사 가능한 방향 신호) without label leakage(라벨 누출 없음).",
            "failure_criteria": "direction source unavailable(방향 원천 없음), active supply collapse(활성 공급 붕괴), or only forced polarity(강제 극성만 존재).",
            "invalid_conditions": "future label in runtime feature(런타임 피처의 미래 라벨), missing timestamp join(타임스탬프 조인 누락), or candidate/ONNX claim(후보/온엑스 주장).",
            "stop_conditions": "If no supported direction source materializes, close as discard memory(지원되는 방향 원천이 없으면 폐기 기억으로 종료).",
            "evidence_plan": "direction_source_audit;branch_plan;materialization_queue;runtime_mapping_contract;receipts;ledgers",
            "branch_rows": len(branch_rows),
            "queue_rows": len(queue_rows),
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "data_source": [rel(SOURCE_PAYLOAD_MANIFEST), rel(SOURCE_GAP), rel(SOURCE_STAGE277_SPEC)],
            "time_axis": "Stage278 payload timestamp(페이로드 타임스탬프)은 UTC closed M5 bar(UTC 마감 5분봉)로 보존한다.",
            "sample_scope": "Stage279 design only(설계 전용); run279B must count rows/run joins(run279B가 행 수와 조인을 계산해야 함)",
            "missing_or_duplicate_check": "planned_for_run279B(279B 실행에서 예정)",
            "feature_label_boundary": "direction source(방향 원천)는 runtime feature(런타임 피처)여야 하며 future label(미래 라벨)은 training/evaluation boundary(학습/평가 경계) 밖으로 나가면 invalid(무효)다.",
            "split_boundary": "Stage278 train/validation/oos split(학습/검증/표본외 분할)을 그대로 이월한다.",
            "leakage_risk": "direction overlay(방향 덧씌우기)를 OOS(표본외) 결과에 맞춰 고르면 selection bias(선택 편향)가 생긴다.",
            "data_hash_or_identity": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs() if path_exists(path)},
            "integrity_judgment": "usable_with_boundary_design_only(설계 전용 경계 포함 사용 가능)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "model_family": "directional overlay design only(방향 덧씌우기 설계 전용); no training yet(아직 학습 없음)",
            "target_and_label": "pending run279B/run279C; direction labels(방향 라벨)은 runtime features(런타임 피처)와 분리해야 한다.",
            "split_method": "Stage278 fixed train/validation/oos split(고정 분할)",
            "selection_metric": "direction signal availability(방향 신호 가능성), supply preservation(공급 보존), leakage safety(누출 안전성)",
            "secondary_metrics": "Tier A/Tier B signal rate(신호 비율), directional balance(방향 균형), active mask retention(활성 마스크 유지)",
            "threshold_policy": "no threshold selected in run279A(279A 실행에서 임계값 선택 없음)",
            "overfit_risk": "multiple direction overlays(다중 방향 덧씌우기)를 본 뒤 선택하는 위험",
            "calibration_risk": "direction overlays(방향 덧씌우기)는 probability(확률)가 아니라 discrete signal(이산 신호)일 수 있다.",
            "comparison_baseline": "Stage278 active/flat blocker(278단계 활성/관망 차단)",
            "validation_judgment": "exploratory_design_only_no_candidate(탐색 설계 전용, 후보 없음)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "research_path": rel(PRODUCER_PATH),
            "runtime_path": "planned run279B directional signal handoff(279B 방향 신호 인계 예정)",
            "shared_contract": "-1/0/+1 signal(신호), feature_order_hash(피처 순서 해시), handoff JSON(인계 JSON), Tier A/B route records(티어 A/B 경로 기록)",
            "known_differences": "No MT5 tester output(MT5 테스터 출력 없음); run279A is design only(설계 전용).",
            "parity_check": "planned_direction_contract_only(방향 계약 계획만)",
            "parity_identity": {"branch_rows": len(branch_rows), "queue_rows": len(queue_rows)},
            "runtime_claim_boundary": "runtime_mapping_design_only(런타임 매핑 설계만 해당)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run279A directional runtime mapping rebuild packet design(279A 방향 런타임 매핑 재구성 묶음 설계)",
                "evidence_available": "direction source audit(방향 원천 감사), branch plan(분기 계획), materialization queue(물질화 대기열), runtime mapping contract(런타임 매핑 계약)",
                "evidence_missing": "materialized direction payload(물질화 방향 페이로드), MT5 tester output(MT5 테스터 출력), trade list(거래 목록), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "design_ready_no_candidate_selection(설계 준비, 후보 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": f"방향 재구성 분기 `{len(queue_rows)}`개를 run279B(279B 실행)로 넘기지만 아직 후보나 ONNX 준비는 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "experiment_design_gate(실험 설계 게이트)",
                "status": "passed_design_receipt_created(설계 영수증 생성으로 통과)",
                "evidence_path": rel(EXPERIMENT_RECEIPT),
                "effect": "hypothesis/comparison/control/stop condition(가설/비교/고정/중단 조건)을 기록한다.",
            },
            {
                "gate_name": "data_integrity_gate(데이터 무결성 게이트)",
                "status": "passed_design_boundary_recorded(설계 경계 기록으로 통과)",
                "evidence_path": rel(DATA_INTEGRITY_RECEIPT),
                "effect": "future label(미래 라벨)을 runtime feature(런타임 피처)로 쓰지 못하게 한다.",
            },
            {
                "gate_name": "model_validation_gate(모델 검증 게이트)",
                "status": "passed_no_threshold_or_model_claim(임계값/모델 주장 없음으로 통과)",
                "evidence_path": rel(MODEL_VALIDATION_RECEIPT),
                "effect": "설계를 성능 주장으로 바꾸지 않는다.",
            },
            {
                "gate_name": "runtime_parity_gate(런타임 동등성 게이트)",
                "status": "passed_contract_planned_no_runtime_claim(계약 계획, 런타임 주장 없음으로 통과)",
                "evidence_path": rel(RUNTIME_PARITY_RECEIPT),
                "effect": "run279B(279B 실행) 전에는 MT5 결과를 주장하지 않는다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_adapter_no_onnx_no_goal(선택 후보/어댑터/온엑스/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "Stage279(279단계) 설계를 ONNX-worthy candidate(온엑스 가치 후보)로 오해하지 않는다.",
            },
        ],
    )


def report_markdown(branch_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    queued = "\n".join(
        f"- `{row['branch_id']}` package(패키지) `{row['package_id']}`"
        for row in queue_rows
    )
    held = "\n".join(
        f"- `{row['branch_id']}`: `{row['materialization_status']}`"
        for row in branch_rows
        if not str(row["materialization_status"]).startswith("queue_for_run279B")
    )
    return f"""# run279A Report(279A 보고서): Directional Runtime Mapping Rebuild Packet Design(방향 런타임 매핑 재구성 묶음 설계)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE279_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_rows(분기 행): `{len(branch_rows)}`
- materialization_queue_rows(물질화 대기열 행): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Queued Branches(대기 분기)

{queued}

## Held/Discard Branches(보류/폐기 분기)

{held}

## Meaning(의미)

run279A(279A 실행)는 Stage278(278단계)의 active/flat(활성/관망) blocker(차단 사유)를 direction mapping(방향 매핑) 재구성 질문으로 바꿨다.
Effect(효과): run279B(279B 실행)는 방향 원천을 물질화하거나, 원천이 없으면 해당 active/flat 계열을 폐기할 수 있다.

## Boundary(경계)

`{BOUNDARY}`
"""


def update_ledgers(created_at: str, branch_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE279_ID,
                "lane": "experiment_design_directional_runtime_mapping",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"branch_rows={len(branch_rows)};queue_rows={len(queue_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__direction_mapping_design",
                "stage_id": STAGE279_ID,
                "run_id": RUN_ID,
                "subrun_id": "direction_mapping_design",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "directional runtime mapping design(방향 런타임 매핑 설계)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "design_no_trading_kpi",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(BRANCH_PLAN),
                "primary_kpi": f"branch_rows={len(branch_rows)};queue_rows={len(queue_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_design_only",
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
                "row_id": f"{RUN_ID}__direction_mapping_design",
                "stage_id": STAGE279_ID,
                "run_id": RUN_ID,
                "view": "directional_runtime_mapping_rebuild_packet_design",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"branch_rows={len(branch_rows)};queue_rows={len(queue_rows)}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run279A_directional_mapping_design_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE279_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run279A directional runtime mapping design artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(branch_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run279A_report", f"- run279A_report(279A 보고서): `{rel(RUN_REPORT)}`")
    selected = append_once(selected, "run279A_branch_plan", f"- run279A_branch_plan(279A 분기 계획): `{rel(BRANCH_PLAN)}`")
    selected = append_once(selected, "run279A_materialization_queue", f"- run279A_materialization_queue(279A 물질화 대기열): `{rel(MATERIALIZATION_QUEUE)}`")
    write_md(SELECTED, selected)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run279A_report",
        f"- run279A_report(279A 보고서): `{rel(RUN_REPORT)}`\n- run279A_direction_source_audit(279A 방향 원천 감사): `{rel(DIRECTION_SOURCE_AUDIT)}`\n- run279A_branch_plan(279A 분기 계획): `{rel(BRANCH_PLAN)}`\n- run279A_materialization_queue(279A 물질화 대기열): `{rel(MATERIALIZATION_QUEUE)}`",
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `directional_runtime_mapping_rebuild_packet_design`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run279A_summary",
        f"- run279A_summary(279A 요약): direction mapping rebuild(방향 매핑 재구성) branch(분기) `{len(branch_rows)}`개와 materialization queue(물질화 대기열) `{len(queue_rows)}`개를 설계했다. Effect(효과): run279B(279B 실행)가 supported direction source(지원되는 방향 원천)를 물질화하거나 폐기할 수 있고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE279_ID}")
    focus = (
        "- >-\n"
        f"  Stage279(279단계) run279A(279A 실행) directional runtime mapping rebuild packet design(방향 런타임 매핑 재구성 묶음 설계) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(branch_rows)}`개와 run279B materialization queue(279B 물질화 대기열) `{len(queue_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage279(279단계) run279A(279A 실행)")
    write_text(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## 2026-05-23 run279A Directional runtime mapping rebuild packet design(방향 런타임 매핑 재구성 묶음 설계)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): branch(분기) `{len(branch_rows)}`개와 queue(대기열) `{len(queue_rows)}`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST279-DIRECTIONAL-MAPPING-RUN279A",
        f"| `IDEA-ST279-DIRECTIONAL-MAPPING-RUN279A` | `{STAGE279_ID}` | active/flat(활성/관망) mask(마스크)에 supported direction source(지원되는 방향 원천)를 붙이는 branch(분기)를 설계한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `design_ready_no_candidate` | branch(분기) `{len(branch_rows)}`개, queue(대기열) `{len(queue_rows)}`개, selected candidate(선택 후보) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def build_contract_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "branch_id": row["branch_id"],
            "runtime_signal_field": "direction_signal_value(방향 신호 값)",
            "allowed_values": "-1 short(숏);0 flat(관망);+1 long(롱)",
            "forbidden_mapping": "active=1 forced to long/short without direction source(방향 원천 없이 활성 1을 롱/숏으로 강제)",
            "feature_order_requirement": "must record feature_order_hash and source feature list(피처 순서 해시와 원천 피처 목록 기록 필수)",
            "handoff_requirement": "timestamp,symbol,split,tier_scope,branch_id,direction_signal_value,signal_active,feature_order_hash,decision_surface_hash",
            "mt5_probe_requirement": "only after direction_signal_value exists(방향 신호 값이 있을 때만)",
            "claim_boundary": BOUNDARY,
        }
        for row in queue_rows
    ]


def run() -> dict[str, Any]:
    created_at = utc_now()
    must_exist(source_inputs())
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    packages = load_package_ids()
    audit_rows = build_audit_rows(packages)
    branch_rows = build_branch_rows(packages)
    queue_rows = build_queue_rows(branch_rows)
    discard_rows = [
        {
            "subject_id": "Stage278 active_flat_direct_mt5_probe",
            "subject_type": "blocked_runtime_probe_path",
            "discard_reason": "active/flat(활성/관망)을 direction(방향) 없이 MT5 tester(MT5 테스터)로 실행하면 의미가 깨진다.",
            "salvage_value": "active mask supply(활성 마스크 공급) and branch identity(분기 정체성)",
            "reopen_condition": "supported direction source(지원되는 방향 원천)가 timestamp/symbol/split/tier(타임스탬프/심볼/분할/티어) 키로 붙을 때",
            "current_judgment": "valid_blocker_memory(유효 차단 기억)",
            "claim_boundary": BOUNDARY,
        }
    ]
    contract_rows = build_contract_rows(queue_rows)

    write_csv(DIRECTION_SOURCE_AUDIT, AUDIT_COLUMNS, audit_rows)
    write_csv(BRANCH_PLAN, BRANCH_COLUMNS, branch_rows)
    write_csv(MATERIALIZATION_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(DISCARD_MATRIX, DISCARD_COLUMNS, discard_rows)
    write_csv(RUNTIME_MAPPING_CONTRACT, CONTRACT_COLUMNS, contract_rows)
    write_receipts(audit_rows, branch_rows, queue_rows)
    write_md(RUN_REPORT, report_markdown(branch_rows, queue_rows))

    outputs = [
        DIRECTION_SOURCE_AUDIT,
        BRANCH_PLAN,
        MATERIALIZATION_QUEUE,
        DISCARD_MATRIX,
        RUNTIME_MAPPING_CONTRACT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE279_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_transition_run_id": SOURCE_TRANSITION_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "created_at_utc": created_at,
        "source_inputs": [rel(path) for path in source_inputs()],
        "source_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs() if path_exists(path)},
        "output_artifacts": [rel(path) for path in outputs],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in outputs if path_exists(path)},
        "branch_rows": len(branch_rows),
        "materialization_queue_rows": len(queue_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_design_only",
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "artifact_paths": [rel(path) for path in outputs],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in outputs if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    outputs.append(LINEAGE_RECEIPT)
    manifest["output_artifacts"] = [rel(path) for path in outputs]
    manifest["output_hashes"] = {rel(path): sha256_file_lf_normalized(path) for path in outputs if path_exists(path)}
    write_json(RUN_MANIFEST, manifest)

    update_ledgers(created_at, branch_rows, queue_rows, outputs)
    update_state_docs(branch_rows, queue_rows)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE279_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "branch_rows": len(branch_rows),
        "materialization_queue_rows": len(queue_rows),
        "selected_candidate": "none",
        "adapter_package": "none",
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
