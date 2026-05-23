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
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE277_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild"
RUN_ID = "run277A_design_fresh_thesis_rebuild_packet_v1"
SOURCE_RUN_ID = "run276E_close_stage276_open_stage277_fresh_thesis_rebuild_v1"
STATUS = "completed_fresh_thesis_rebuild_packet_design_no_candidate_selection"
JUDGMENT = "fresh_thesis_rebuild_packet_ready_no_candidate_selection"
NEXT_ACTION = "run277B_materialize_fresh_thesis_candidate_blueprints"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE277 = ROOT / "stages" / STAGE277_ID
RUN_DIR = STAGE277 / "02_runs" / "run277A"
REVIEWS = STAGE277 / "03_reviews"
SELECTED = STAGE277 / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE277 / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE277 / "01_inputs" / "input_refs.md"
SEED_QUEUE = STAGE277 / "01_inputs" / "stage277_rebuild_thesis_seed_queue.csv"
FAILURE_MEMORY = STAGE277 / "01_inputs" / "stage276_failure_memory.csv"
NEGATIVE_SLICE = STAGE277 / "01_inputs" / "stage276_negative_slice_summary.csv"
VARIANT_SUMMARY = STAGE277 / "01_inputs" / "stage276_variant_summary.csv"

PACKAGE_QUEUE = RUN_DIR / "candidate_package_queue.csv"
FEATURE_SURFACE_PLAN = RUN_DIR / "feature_surface_plan.csv"
DECISION_SURFACE_PLAN = RUN_DIR / "decision_surface_plan.csv"
RISK_LOGIC_PLAN = RUN_DIR / "risk_logic_plan.csv"
ADAPTER_HANDOFF_PLAN = RUN_DIR / "adapter_handoff_plan.csv"
SUPPORT_CONTROL = RUN_DIR / "support_control.csv"
DISCARD_CONDITIONS = RUN_DIR / "discard_conditions.csv"
REQUIRED_EVIDENCE = RUN_DIR / "required_evidence_matrix.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run277A_report.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEWS / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage277/design_fresh_thesis_rebuild_packet.py")

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
PACKAGE_COLUMNS = (
    "package_id",
    "source_seed_id",
    "fresh_thesis",
    "feature_surface",
    "model_or_scoring_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "broad_sweep",
    "extreme_sweep",
    "micro_search_gate",
    "discard_condition",
    "tier_scope",
    "next_action",
    "selected_candidate",
    "onnx_readiness",
)
PLAN_COLUMNS = ("package_id", "surface_id", "owner", "plan", "trace_input", "acceptance_gate", "effect")
SUPPORT_COLUMNS = ("control_id", "purpose", "source", "expected_use", "boundary")


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


def package_rows(seeds: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    seed_by_id = {row["seed_id"]: row for row in seeds}
    specs = [
        {
            "package_id": "cp277A_session_loss_avoidance_surface",
            "source_seed_id": "stage277A_session_loss_avoidance_surface",
            "feature_surface": "session/chron/volatility loss-state features(세션/시간순서/변동성 손실 상태 피처)",
            "model_or_scoring_surface": "loss-avoidance score plus entry-retention score(손실 회피 점수와 진입 보존 점수)",
            "decision_surface": "trade only when weak-session state improves expected loss(약한 세션 상태가 기대 손실을 줄일 때만 거래)",
            "risk_logic": "session-aware reduced risk or no-trade branch(세션 인식 축소 위험 또는 미거래 분기)",
            "adapter_path": "foundation adapter candidate path(공유 어댑터 후보 경로) to be materialized in run277B(277B 실행에서 물질화)",
            "runtime_handoff": "MT5 signal fields(MT5 신호 필드): timestamp, side, score, session_loss_state, risk_multiplier",
        },
        {
            "package_id": "cp277B_validation_pf_floor_rebalanced_entry_surface",
            "source_seed_id": "stage277B_validation_pf_floor_rebalanced_entry_surface",
            "feature_surface": "entry source, score margin, risk distance, hold horizon features(진입 원천/점수 여유/위험 거리/보유 예측수평선 피처)",
            "model_or_scoring_surface": "validation-PF floor score with OOS supply preservation(검증 수익 팩터 하한 점수와 표본외 공급 보존)",
            "decision_surface": "enter only when validation floor and OOS supply gates agree(검증 하한과 표본외 공급 게이트가 함께 맞을 때 진입)",
            "risk_logic": "validation-first risk cap with OOS density guard(검증 우선 위험 상한과 표본외 밀도 보호)",
            "adapter_path": "adapter schema(어댑터 스키마): feature_order, pf_floor_score, supply_state, risk_cap",
            "runtime_handoff": "MT5 signal fields(MT5 신호 필드): timestamp, side, pf_floor_score, supply_state, risk_cap",
        },
        {
            "package_id": "cp277C_directional_asymmetry_reversal_surface",
            "source_seed_id": "stage277C_directional_asymmetry_reversal_from_failure_memory",
            "feature_surface": "side-state, divergence sign, session side pressure features(방향 상태/괴리 부호/세션 방향 압박 피처)",
            "model_or_scoring_surface": "side-asymmetry reversal score(방향 비대칭 반전 점수)",
            "decision_surface": "side-specific entry or side flip when loss attribution repeats(손실 귀속이 반복될 때 방향별 진입 또는 방향 반전)",
            "risk_logic": "side-specific risk cap and danger-session no-trade(방향별 위험 상한과 위험 세션 미거래)",
            "adapter_path": "adapter schema(어댑터 스키마): side_state, divergence_sign, side_score, side_risk_cap",
            "runtime_handoff": "MT5 signal fields(MT5 신호 필드): timestamp, side, side_score, side_state, session_pressure",
        },
        {
            "package_id": "cp277D_macro_squeeze_failure_contrast_surface",
            "source_seed_id": "stage277D_macro_squeeze_failure_contrast_surface",
            "feature_surface": "macro proxy, squeeze state, late-chron risk compression features(거시 대리/압축 상태/후반 시간 위험 압축 피처)",
            "model_or_scoring_surface": "failure-contrast reward asymmetry score(실패 대비 보상 비대칭 점수)",
            "decision_surface": "trade squeeze contrast only when late-loss risk is compressed(후반 손실 위험이 압축될 때만 압축 대비 거래)",
            "risk_logic": "post-release cooldown and late-OOS stop branch(해제 후 냉각과 후반 표본외 중단 분기)",
            "adapter_path": "adapter schema(어댑터 스키마): macro_state, squeeze_state, contrast_score, cooldown_state",
            "runtime_handoff": "MT5 signal fields(MT5 신호 필드): timestamp, side, contrast_score, squeeze_state, cooldown_state",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        seed = seed_by_id[spec["source_seed_id"]]
        rows.append(
            {
                **spec,
                "fresh_thesis": seed["fresh_thesis"],
                "broad_sweep": seed["broad_sweep"],
                "extreme_sweep": seed["extreme_sweep"],
                "micro_search_gate": seed["micro_search_gate"],
                "discard_condition": seed["discard_condition"],
                "tier_scope": seed["tier_scope"],
                "next_action": NEXT_ACTION,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return rows


def feature_rows(packages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "package_id": row["package_id"],
            "surface_id": f"{row['package_id']}__feature_surface",
            "owner": "foundation/features or stage-local materializer(공유 피처 또는 단계 로컬 물질화기)",
            "plan": row["feature_surface"],
            "trace_input": rel(SEED_QUEUE),
            "acceptance_gate": "feature order receipt(피처 순서 영수증) must be written before MT5 payload(MT5 페이로드 전 작성)",
            "effect": "feature order(피처 순서)를 후보 패키지 정체성에 묶는다.",
        }
        for row in packages
    ]


def decision_rows(packages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "package_id": row["package_id"],
            "surface_id": f"{row['package_id']}__decision_surface",
            "owner": "stage277 decision materializer(277단계 판단 물질화기)",
            "plan": row["decision_surface"],
            "trace_input": rel(PACKAGE_QUEUE),
            "acceptance_gate": "decision rule hash(판단 규칙 해시) and discard condition(폐기 조건) required",
            "effect": "score(점수)를 단순 순위가 아니라 실행 가능한 판단 규칙으로 바꾼다.",
        }
        for row in packages
    ]


def risk_rows(packages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "package_id": row["package_id"],
            "surface_id": f"{row['package_id']}__risk_logic",
            "owner": "stage277 risk materializer(277단계 위험 물질화기)",
            "plan": row["risk_logic"],
            "trace_input": rel(PACKAGE_QUEUE),
            "acceptance_gate": "risk rule receipt(위험 규칙 영수증) required before runtime handoff(런타임 인계 전 필요)",
            "effect": "약한 구간을 단순 제거가 아니라 위험 로직으로 추적한다.",
        }
        for row in packages
    ]


def adapter_rows(packages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "package_id": row["package_id"],
            "surface_id": f"{row['package_id']}__adapter_handoff",
            "owner": "Adapter handoff planner(어댑터 인계 계획기)",
            "plan": row["adapter_path"] + "; " + row["runtime_handoff"],
            "trace_input": rel(PACKAGE_QUEUE),
            "acceptance_gate": "adapter schema hash(어댑터 스키마 해시), feature order hash(피처 순서 해시), handoff manifest(인계 목록) required",
            "effect": "ONNX(온엑스) 이전에 Python/MT5(파이썬/메타트레이더5) 인계 의미를 고정한다.",
        }
        for row in packages
    ]


def support_rows() -> list[dict[str, str]]:
    return [
        {
            "control_id": "ctrl277A_stage276_failure_memory_replay",
            "purpose": "Stage276 failure replay control(276단계 실패 재생 대조)",
            "source": rel(FAILURE_MEMORY),
            "expected_use": "run277B(277B 실행)에서 새 package(패키지)가 기존 실패 이름을 후보로 보존하지 않는지 비교한다.",
            "boundary": "support control only(보조 대조만), selected candidate(선택 후보) 아님",
        }
    ]


def discard_rows(packages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "package_id": row["package_id"],
            "surface_id": f"{row['package_id']}__discard_condition",
            "owner": "obsidian-exploration-mandate(탐색 원칙)",
            "plan": row["discard_condition"],
            "trace_input": rel(SEED_QUEUE),
            "acceptance_gate": "discard condition(폐기 조건) must be checked before survivor watch(생존 관찰) claim",
            "effect": "무한 repair loop(수리 반복)를 막는다.",
        }
        for row in packages
    ]


def required_evidence_rows(packages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in packages:
        for surface in ("feature_order", "decision_rule", "risk_rule", "adapter_schema", "runtime_handoff", "paired_tier_review", "failure_memory"):
            rows.append(
                {
                    "package_id": row["package_id"],
                    "surface_id": f"{row['package_id']}__{surface}",
                    "owner": "run277B materialization(277B 물질화)",
                    "plan": f"{surface}(표면 근거) receipt(영수증)를 만든다.",
                    "trace_input": rel(PACKAGE_QUEUE),
                    "acceptance_gate": "required before selected candidate(선택 후보 전 필수)",
                    "effect": "candidate package(후보 패키지) 단위 추적성을 만든다.",
                }
            )
    return rows


def write_report(packages: Sequence[Mapping[str, str]], controls: Sequence[Mapping[str, str]]) -> None:
    package_lines = "\n".join(
        f"- `{row['package_id']}` from `{row['source_seed_id']}`: {row['fresh_thesis']}"
        for row in packages
    )
    control_lines = "\n".join(f"- `{row['control_id']}`: {row['purpose']}" for row in controls)
    write_md(
        REPORT,
        f"""# run277A Report(277A 보고서): Fresh Thesis Rebuild Packet Design(새 논제 재구성 묶음 설계)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE277_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- package_rows(패키지 행): `{len(packages)}`
- support_control_rows(보조 대조 행): `{len(controls)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Package Queue(패키지 대기열)

{package_lines}

## Support Control(보조 대조)

{control_lines}

## Boundary(경계)

run277A(277A 실행)는 design packet(설계 묶음)이다.
Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX export/parity(온엑스 내보내기/동등성), MT5 runtime reproduction(MT5 런타임 재현)를 아직 주장하지 않는다.
""",
    )


def write_receipts(packages: Sequence[Mapping[str, str]], controls: Sequence[Mapping[str, str]]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run277A fresh thesis rebuild packet design(277A 새 논제 재구성 묶음 설계)",
                "evidence_available": "seed queue(씨앗 대기열), package queue(패키지 대기열), feature/decision/risk/adapter plans(피처/판단/위험/어댑터 계획)",
                "evidence_missing": "materialized score surface(물질화 점수 표면), MT5 runtime result(MT5 런타임 결과), selected candidate(선택 후보), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "design_packet_ready(설계 묶음 준비)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "패키지 대기열은 생겼지만 선택 후보는 아직 없다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "exploration_mandate_gate(탐색 원칙 게이트)",
                "status": "passed_broad_extreme_micro_discard_present(넓은/극단/미세/폐기 조건 있음으로 통과)",
                "evidence_path": rel(PACKAGE_QUEUE),
                "effect": "각 thesis(논제)가 broad sweep/extreme sweep/micro gate/discard condition(넓은 훑기/극단 훑기/미세 게이트/폐기 조건)을 가진다.",
            },
            {
                "gate_name": "candidate_package_definition_gate(후보 패키지 정의 게이트)",
                "status": "passed_package_trace_fields_present(패키지 추적 필드 있음으로 통과)",
                "evidence_path": rel(REQUIRED_EVIDENCE),
                "effect": "feature/decision/risk/Adapter/runtime handoff(피처/판단/위험/어댑터/런타임 인계)를 후보 단위로 요구한다.",
            },
            {
                "gate_name": "paired_tier_gate(티어 쌍 게이트)",
                "status": "passed_required_for_next_run(다음 실행 필수 조건으로 통과)",
                "evidence_path": rel(PACKAGE_QUEUE),
                "effect": "run277B(277B 실행)는 Tier A separate/Tier B separate/Tier A+B combined(Tier A 분리/Tier B 분리/Tier A+B 합산)을 만들어야 한다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "설계 완료를 후보 선택으로 올려 말하지 않는다.",
            },
            {
                "gate_name": "next_action_gate(다음 행동 게이트)",
                "status": "passed_run277B_materialization_queue(277B 물질화 대기열로 통과)",
                "evidence_path": rel(PACKAGE_QUEUE),
                "effect": "다음 행동은 package blueprint materialization(패키지 청사진 물질화)이다.",
            },
        ],
    )


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], packages: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    source_inputs = [STAGE_BRIEF, INPUT_REFS, SEED_QUEUE, FAILURE_MEMORY, NEGATIVE_SLICE, VARIANT_SUMMARY]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "stage_id": STAGE277_ID,
        "source_run_id": SOURCE_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "consumer": [STAGE277_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "source_inputs": [rel(path) for path in source_inputs],
        "source_hashes": output_hashes(source_inputs),
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


def update_registers(created_at: str, packages: Sequence[Mapping[str, str]], outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE277_ID,
                "lane": "experiment_design",
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
                "ledger_row_id": f"{RUN_ID}__design_packet",
                "stage_id": STAGE277_ID,
                "run_id": RUN_ID,
                "subrun_id": "design_packet",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "run277A design packet(277A 설계 묶음)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "design",
                "scoreboard_lane": "fresh_thesis_rebuild",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"package_rows={len(packages)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_design_packet",
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
                "row_id": f"{RUN_ID}__design_packet",
                "stage_id": STAGE277_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_rebuild_packet_design",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"package_rows={len(packages)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run277A_design_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE277_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run277A design packet artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(packages: Sequence[Mapping[str, str]]) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run277A_report", f"- run277A_report(277A 보고서): `{rel(REPORT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run277A_report",
        "\n".join(
            [
                f"- run277A_report(277A 보고서): `{rel(REPORT)}`",
                f"- run277A_package_queue(277A 패키지 대기열): `{rel(PACKAGE_QUEUE)}`",
                f"- run277A_required_evidence(277A 필수 근거): `{rel(REQUIRED_EVIDENCE)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage277_fresh_thesis_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE277_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_rebuild_packet_design`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run277A_summary",
        (
            f"- run277A_summary(277A 요약): seed(씨앗) `4`개를 package queue(패키지 대기열) `{len(packages)}`개와 "
            "feature/decision/risk/Adapter handoff(피처/판단/위험/어댑터 인계) 계획으로 바꿨다. "
            "Effect(효과): 다음 run277B(277B 실행)에서 물질화할 수 있지만 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE277_ID}")
    focus = (
        "- >-\n"
        f"  Stage277(277단계) run277A(277A 실행) fresh thesis rebuild packet design(새 논제 재구성 묶음 설계) `{RUN_ID}`. "
        f"Effect(효과): package queue(패키지 대기열) `{len(packages)}`개와 Adapter handoff requirement(어댑터 인계 요구조건)를 만들었고 "
        "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage277(277단계) run277A(277A 실행)")
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run277A Fresh thesis rebuild packet design(새 논제 재구성 묶음 설계)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): package queue(패키지 대기열) `{len(packages)}`개를 만들고 run277B(277B 실행) materialization(물질화)으로 넘긴다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST277-FRESH-THESIS-REBUILD-RUN277A",
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277A` | `{STAGE277_ID}` | Stage276(276단계) failure memory(실패 기억)를 candidate package queue(후보 패키지 대기열)로 재구성한다. | `package_rows={len(packages)};support_control=1` | `design_packet_ready_no_selection` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def run() -> dict[str, Any]:
    must_exist([STAGE_BRIEF, INPUT_REFS, SEED_QUEUE, FAILURE_MEMORY, NEGATIVE_SLICE, VARIANT_SUMMARY])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    seeds = read_csv_rows(SEED_QUEUE)
    packages = package_rows(seeds)
    controls = support_rows()
    write_csv(PACKAGE_QUEUE, PACKAGE_COLUMNS, packages)
    write_csv(FEATURE_SURFACE_PLAN, PLAN_COLUMNS, feature_rows(packages))
    write_csv(DECISION_SURFACE_PLAN, PLAN_COLUMNS, decision_rows(packages))
    write_csv(RISK_LOGIC_PLAN, PLAN_COLUMNS, risk_rows(packages))
    write_csv(ADAPTER_HANDOFF_PLAN, PLAN_COLUMNS, adapter_rows(packages))
    write_csv(SUPPORT_CONTROL, SUPPORT_COLUMNS, controls)
    write_csv(DISCARD_CONDITIONS, PLAN_COLUMNS, discard_rows(packages))
    write_csv(REQUIRED_EVIDENCE, PLAN_COLUMNS, required_evidence_rows(packages))
    write_report(packages, controls)
    write_receipts(packages, controls)

    outputs = [
        PACKAGE_QUEUE,
        FEATURE_SURFACE_PLAN,
        DECISION_SURFACE_PLAN,
        RISK_LOGIC_PLAN,
        ADAPTER_HANDOFF_PLAN,
        SUPPORT_CONTROL,
        DISCARD_CONDITIONS,
        REQUIRED_EVIDENCE,
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
        "stage_id": STAGE277_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "package_rows": len(packages),
        "support_control_rows": len(controls),
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
