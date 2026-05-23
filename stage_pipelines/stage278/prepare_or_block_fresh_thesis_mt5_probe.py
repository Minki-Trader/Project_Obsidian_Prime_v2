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
    upsert_csv_rows,
    write_csv_rows,
)


STAGE278_ID = "278_onnx_candidate_campaign__fresh_thesis_mt5_probe"
RUN_ID = "run278C_prepare_or_block_fresh_thesis_mt5_probe_v1"
SOURCE_RUN_ID = "run278B_materialize_fresh_thesis_mt5_probe_payloads_v1"
PARENT_RUN_ID = "run278A_design_fresh_thesis_mt5_probe_packet_v1"
STATUS = "blocked_fresh_thesis_mt5_probe_direction_mapping_missing_no_candidate_selection"
JUDGMENT = "blocked_runtime_probe_missing_supported_direction_mapping"
NEXT_ACTION = "stage279_design_directional_runtime_mapping_or_discard_active_flat_surfaces"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE278_ID
RUN278B = STAGE / "02_runs" / "run278B"
RUN_DIR = STAGE / "02_runs" / "run278C"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

MT5_QUEUE = RUN278B / "mt5_probe_queue.csv"
PAYLOAD_MANIFEST = RUN278B / "probe_payload_manifest.csv"
TIER_ROUTE_RECEIPT = RUN278B / "tier_route_receipt.csv"
RUN278B_MANIFEST = RUN278B / "run_manifest.json"
RUN278B_LINEAGE = RUN278B / "artifact_lineage_receipt.json"

ATTEMPT_SUMMARY = RUN_DIR / "attempt_summary.csv"
DIRECTION_MAPPING_GAP = RUN_DIR / "direction_mapping_gap_receipt.csv"
PAYLOAD_READINESS = RUN_DIR / "runtime_probe_readiness_receipt.csv"
BACKTEST_FORENSICS_PLAN = RUN_DIR / "backtest_forensics_plan.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run278C_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage278/prepare_or_block_fresh_thesis_mt5_probe.py")

ATTEMPT_COLUMNS = (
    "attempt_id",
    "queue_id",
    "branch_id",
    "package_id",
    "payload_path",
    "mt5_actual_routed_signal_path",
    "signal_policy",
    "tester_status",
    "runtime_status",
    "blocked_reason",
    "required_repair",
    "claim_boundary",
)
GAP_COLUMNS = (
    "branch_id",
    "package_id",
    "active_flat_signal_available",
    "direction_signal_available",
    "runtime_harness_requirement",
    "semantic_gap",
    "allowed_next_action",
    "forbidden_action",
    "claim_boundary",
)
READINESS_COLUMNS = ("check_name", "status", "effect")
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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(text: str) -> Path:
    return ROOT / text


def sha256_file(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


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
        raise FileNotFoundError("Missing required input artifacts: " + "; ".join(missing))


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


def source_paths() -> list[Path]:
    return [MT5_QUEUE, PAYLOAD_MANIFEST, TIER_ROUTE_RECEIPT, RUN278B_MANIFEST, RUN278B_LINEAGE]


def load_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    must_exist(source_paths())
    queue_rows = read_csv_rows(MT5_QUEUE)
    manifest_rows = read_csv_rows(PAYLOAD_MANIFEST)
    if not queue_rows:
        raise RuntimeError("run278B MT5 queue is empty.")
    return queue_rows, manifest_rows


def inspect_payload_signal_policy(payload_path: Path) -> dict[str, Any]:
    frame = pd.read_parquet(io_path(payload_path), columns=["signal_active", "route_signal_value", "route_signal_label"])
    values = sorted(str(value) for value in frame["route_signal_label"].dropna().unique().tolist())
    numeric_values = sorted(int(value) for value in pd.to_numeric(frame["route_signal_value"], errors="coerce").dropna().unique().tolist())
    return {
        "rows": int(len(frame)),
        "signal_labels": values,
        "route_signal_values": numeric_values,
        "active_count": int(pd.to_numeric(frame["signal_active"], errors="coerce").fillna(0).sum()),
        "has_directional_negative": -1 in numeric_values,
        "has_directional_positive": 1 in numeric_values,
        "active_flat_only": set(values).issubset({"active", "flat"}) and set(numeric_values).issubset({0, 1}),
    }


def build_blocker_rows(
    queue_rows: Sequence[Mapping[str, str]],
    manifest_rows: Sequence[Mapping[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    manifest_by_branch = {row["branch_id"]: row for row in manifest_rows}
    attempt_rows: list[dict[str, Any]] = []
    gap_rows: list[dict[str, Any]] = []
    inspections: dict[str, Any] = {}
    for index, row in enumerate(queue_rows, start=1):
        branch_id = row["branch_id"]
        manifest = manifest_by_branch[branch_id]
        payload_path = repo_path(manifest["payload_path"])
        inspection = inspect_payload_signal_policy(payload_path)
        inspections[branch_id] = inspection
        attempt_rows.append(
            {
                "attempt_id": f"run278C_blocked_{index:02d}",
                "queue_id": row["queue_id"],
                "branch_id": branch_id,
                "package_id": row["package_id"],
                "payload_path": manifest["payload_path"],
                "mt5_actual_routed_signal_path": manifest["mt5_actual_routed_signal_path"],
                "signal_policy": row["signal_policy"],
                "tester_status": "not_attempted_semantic_blocker",
                "runtime_status": "blocked_before_tester",
                "blocked_reason": "active_flat_signal_has_no_supported_direction_mapping",
                "required_repair": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            }
        )
        gap_rows.append(
            {
                "branch_id": branch_id,
                "package_id": row["package_id"],
                "active_flat_signal_available": "yes" if inspection["active_flat_only"] else "no",
                "direction_signal_available": "no",
                "runtime_harness_requirement": "RuntimeProbeEA single discrete table expects -1/0/+1(short/flat/long, 숏/관망/롱)",
                "semantic_gap": "run278B preserved active/flat(활성/관망) only; mapping active=1 to long(롱) would invent direction(방향)",
                "allowed_next_action": NEXT_ACTION,
                "forbidden_action": "do_not_run_mt5_tester_as_long_only_or_short_only_without_direction_surface",
                "claim_boundary": BOUNDARY,
            }
        )
    return attempt_rows, gap_rows, inspections


def write_receipts(
    attempt_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    inspections: Mapping[str, Any],
) -> None:
    write_csv(ATTEMPT_SUMMARY, ATTEMPT_COLUMNS, attempt_rows)
    write_csv(DIRECTION_MAPPING_GAP, GAP_COLUMNS, gap_rows)
    write_csv(
        PAYLOAD_READINESS,
        READINESS_COLUMNS,
        [
            {
                "check_name": "payloads_available",
                "status": "passed(통과)",
                "effect": f"run278B(278B 실행) payload(페이로드) `{len(attempt_rows)}`개를 확인했다.",
            },
            {
                "check_name": "mt5_runtime_semantic_mapping",
                "status": "blocked(차단)",
                "effect": "active/flat(활성/관망) 신호를 RuntimeProbeEA(런타임 탐침 EA)의 short/flat/long(숏/관망/롱) 의미로 바꿀 근거가 없다.",
            },
            {
                "check_name": "external_verification_attempt",
                "status": "blocked_before_tester(테스터 전 차단)",
                "effect": "의미가 다른 신호를 MT5(`MetaTrader 5`, 메타트레이더5) 수익 결과로 만들지 않는다.",
            },
            {
                "check_name": "claim_guard",
                "status": "passed_no_candidate_no_adapter_no_onnx_no_goal(후보/어댑터/온엑스/목표 달성 없음으로 통과)",
                "effect": "blocked(차단) 결과를 selected candidate(선택 후보)나 ONNX readiness(온엑스 준비)로 읽지 않는다.",
            },
        ],
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "research_path": rel(RUN278B),
            "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
            "shared_contract": "payload identity(페이로드 정체성)는 연결됐지만 direction contract(방향 계약)는 없다.",
            "known_differences": "run278B signal(신호)은 active/flat(활성/관망)이고 RuntimeProbeEA(런타임 탐침 EA) harness(실행 장치)는 -1/0/+1(short/flat/long, 숏/관망/롱)을 기대한다.",
            "parity_check": "blocked_before_tester_due_to_direction_mapping_gap(방향 매핑 공백 때문에 테스터 전 차단)",
            "parity_identity": {"attempt_rows": len(attempt_rows), "inspections": inspections},
            "runtime_claim_boundary": "blocked_runtime_probe_no_runtime_result(차단된 런타임 탐침, 런타임 결과 없음)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        BACKTEST_FORENSICS_PLAN,
        {
            "tester_identity": "not_attempted_semantic_blocker(의미 차단으로 미시도)",
            "ea_identity": "RuntimeProbeEA requires directional discrete signal(RuntimeProbeEA는 방향성 이산 신호 필요)",
            "report_identity": "missing_no_tester_run(테스터 실행 없음으로 누락)",
            "trade_evidence": "missing_no_tester_run(테스터 실행 없음으로 누락)",
            "cost_assumptions": "not_observed_no_tester_run(테스터 실행 없음으로 관측 불가)",
            "forensic_checks": "payload active/flat policy(활성/관망 정책) compared with runtime harness directional requirement(런타임 실행 장치 방향 요구)",
            "backtest_judgment": "blocked_before_tester(테스터 전 차단)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run278C fresh thesis MT5 probe readiness(278C 새 논제 MT5 탐침 준비)",
                "evidence_available": "run278B payload manifest(페이로드 목록), MT5 queue(MT5 대기열), direction mapping gap receipt(방향 매핑 공백 영수증)",
                "evidence_missing": "supported direction surface(지원되는 방향 표면), MT5 tester output(MT5 테스터 출력), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선)",
                "judgment_label": JUDGMENT,
                "judgment_class": "blocked_runtime_probe_semantic_gap(의미 공백으로 런타임 탐침 차단)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "페이로드는 준비됐지만 active/flat(활성/관망)을 long/short(롱/숏)로 바꾸는 근거가 없어 MT5 수익 테스트를 멈췄다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "external_verification_anti_deferral_gate(외부 검증 지연 방지 게이트)",
                "status": "blocked_with_reason_recorded(차단 사유 기록으로 차단)",
                "evidence_path": rel(DIRECTION_MAPPING_GAP),
                "effect": "MT5(`MetaTrader 5`, 메타트레이더5) 실행을 그냥 다음으로 미루지 않고 의미 공백을 명시한다.",
            },
            {
                "gate_name": "runtime_parity_gate(런타임 동등성 게이트)",
                "status": "blocked_direction_mapping_missing(방향 매핑 누락으로 차단)",
                "evidence_path": rel(RUNTIME_PARITY_RECEIPT),
                "effect": "payload(페이로드) 의미와 EA harness(EA 실행 장치) 의미가 같다고 주장하지 않는다.",
            },
            {
                "gate_name": "backtest_forensics_gate(백테스트 포렌식 게이트)",
                "status": "blocked_no_tester_output(테스터 출력 없음으로 차단)",
                "evidence_path": rel(BACKTEST_FORENSICS_PLAN),
                "effect": "tester report(테스터 보고서) 없이 trade quality(거래 품질)를 말하지 않는다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_adapter_no_onnx_no_goal(선택 후보/어댑터/온엑스/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "blocked(차단)을 긍정 판정(positive judgment, 긍정 판정)으로 바꾸지 않는다.",
            },
        ],
    )


def report_markdown(attempt_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = "\n".join(
        f"- `{row['branch_id']}`: `{row['blocked_reason']}`"
        for row in attempt_rows
    )
    return f"""# run278C Report(278C 보고서): Fresh Thesis MT5 Probe Readiness Block(새 논제 MT5 탐침 준비 차단)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE278_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- attempted_tester_runs(시도한 테스터 실행): `0`
- blocked_attempts(차단 시도): `{len(attempt_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run278C(278C 실행)는 run278B(278B 실행)의 payload(페이로드)를 MT5(`MetaTrader 5`, 메타트레이더5) tester(테스터)에 바로 넣지 않았다.
Effect(효과): active/flat(활성/관망)을 long/short(롱/숏) 방향으로 임의 변환해 가짜 runtime result(런타임 결과)를 만들지 않는다.

## Blocked Rows(차단 행)

{lines}

## Required Repair(필수 수정)

다음 질문은 direction surface(방향 표면)다.
Effect(효과): active/flat(활성/관망) 신호를 버릴지, supported direction mapping(지원되는 방향 매핑)을 만들지, 아니면 새 후보 구성을 열지 결정한다.

## Boundary(경계)

`{BOUNDARY}`
"""


def update_ledgers(attempt_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE278_ID,
                "lane": "runtime_probe_readiness_block",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"blocked_attempts={len(attempt_rows)};reason=direction_mapping_missing;selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__direction_mapping_block",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_mt5_probe_readiness",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "runtime_probe_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "blocked_before_tester_no_runtime_kpi",
                "report_path": rel(RUN_REPORT),
                "notes": f"blocked_attempts={len(attempt_rows)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__direction_mapping_block",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "subrun_id": "direction_mapping_block",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "MT5 probe readiness block(MT5 탐침 준비 차단)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "runtime_probe_block_no_trading_kpi",
                "scoreboard_lane": "runtime_probe_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(DIRECTION_MAPPING_GAP),
                "primary_kpi": f"blocked_attempts={len(attempt_rows)};tester_runs=0",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "blocked_direction_mapping_missing_before_tester",
                "notes": "MT5 tester was not run because active/flat signal lacks supported direction mapping.",
            }
        ],
        key="ledger_row_id",
    )


def update_state_docs(attempt_count: int) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run278C_report", f"- run278C_report(278C 보고서): `{rel(RUN_REPORT)}`")
    selected = append_once(selected, "run278C_direction_mapping_gap", f"- run278C_direction_mapping_gap(278C 방향 매핑 공백): `{rel(DIRECTION_MAPPING_GAP)}`")
    write_md(SELECTED, selected)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run278C_report",
        f"- run278C_report(278C 보고서): `{rel(RUN_REPORT)}`\n- run278C_direction_mapping_gap(278C 방향 매핑 공백): `{rel(DIRECTION_MAPPING_GAP)}`\n- run278C_runtime_parity_receipt(278C 런타임 동등성 영수증): `{rel(RUNTIME_PARITY_RECEIPT)}`",
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_mt5_probe_direction_mapping_gap`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run278C_summary",
        f"- run278C_summary(278C 요약): run278C(278C 실행)는 MT5 probe(MT5 탐침)를 tester(테스터) 전에 차단했다. Effect(효과): active/flat(활성/관망) 신호 `{attempt_count}`개를 long/short(롱/숏)로 임의 변환하지 않고 direction mapping gap(방향 매핑 공백)으로 기록했으며 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE278_ID}")
    focus = (
        "- >-\n"
        f"  Stage278(278단계) run278C(278C 실행) fresh thesis MT5 probe readiness block(새 논제 MT5 탐침 준비 차단) `{RUN_ID}`. "
        f"Effect(효과): active/flat(활성/관망) payload(페이로드) `{attempt_count}`개는 준비됐지만 supported direction mapping(지원되는 방향 매핑)이 없어 MT5 tester(MT5 테스터)를 차단했고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage278(278단계) run278C(278C 실행)")
    write_text(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## 2026-05-23 run278C Fresh thesis MT5 probe readiness block(새 논제 MT5 탐침 준비 차단)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): supported direction mapping(지원되는 방향 매핑)이 없어 MT5 tester(MT5 테스터)를 실행하지 않고 차단 근거를 남겼다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278C",
        f"| `IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278C` | `{STAGE278_ID}` | active/flat(활성/관망) payload(페이로드)를 MT5 tester(MT5 테스터)에 넣기 전 direction mapping gap(방향 매핑 공백)을 검사한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `blocked_direction_mapping_missing` | blocked attempts(차단 시도) `{attempt_count}`개, selected candidate(선택 후보) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def generated_artifacts() -> list[Path]:
    return [
        ATTEMPT_SUMMARY,
        DIRECTION_MAPPING_GAP,
        PAYLOAD_READINESS,
        BACKTEST_FORENSICS_PLAN,
        RUNTIME_PARITY_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
        STAGE_LEDGER,
        SELECTED,
        RUN_MANIFEST,
        LINEAGE_RECEIPT,
    ]


def write_manifest_and_lineage(created_at: str, attempt_count: int) -> None:
    artifacts = [path for path in generated_artifacts() if path_exists(path) and path != LINEAGE_RECEIPT]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE278_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in source_paths()],
        "source_hashes": {rel(path): sha256_file(path) for path in source_paths() if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "blocked_attempts": attempt_count,
        "tester_runs": 0,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "blocked_direction_mapping_missing_before_tester",
        "claim_boundary": BOUNDARY,
        "next_action": NEXT_ACTION,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"] + [rel(RUN_MANIFEST), rel(LINEAGE_RECEIPT)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts + [RUN_MANIFEST] if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_blocker(차단 사유 포함 연결)",
        "runtime_claim_boundary": "blocked_before_tester_no_runtime_result(테스터 전 차단, 런타임 결과 없음)",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)


def update_artifact_registry(created_at: str) -> None:
    rows = []
    for path in generated_artifacts():
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
                    "artifact_type": "run278C_runtime_probe_block_artifact",
                    "path": rel(path),
                    "sha256": sha256_file(path),
                    "stage_id": STAGE278_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": "run278C direction mapping blocker artifact.",
                }
            )
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def run() -> dict[str, Any]:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    queue_rows, manifest_rows = load_rows()
    attempt_rows, gap_rows, inspections = build_blocker_rows(queue_rows, manifest_rows)
    write_receipts(attempt_rows, gap_rows, inspections)
    write_md(RUN_REPORT, report_markdown(attempt_rows))
    update_ledgers(attempt_rows)
    update_state_docs(len(attempt_rows))
    write_manifest_and_lineage(created_at, len(attempt_rows))
    update_artifact_registry(created_at)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE278_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "blocked_attempts": len(attempt_rows),
        "tester_runs": 0,
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
