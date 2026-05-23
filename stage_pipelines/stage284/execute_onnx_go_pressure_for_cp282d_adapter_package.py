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

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE284_ID = "284_onnx_candidate_campaign__onnx_go_pressure_for_cp282d_adapter"
STAGE285_ID = "285_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp282d"
RUN_ID = "run284A_execute_onnx_go_pressure_for_cp282d_adapter_package_v1"
SOURCE_RUN_ID = "run283A_build_adapter_package_for_cp282d_macro_trend_countercheck_v1"
STATUS = "completed_onnx_go_pressure_passed_stage285_opened"
JUDGMENT = "onnx_go_approved_for_export_no_parity_yet"
SELECTED_CANDIDATE = "cp282D_macro_trend_countercheck_surface"
ADAPTER_PACKAGE_ID = "stage283_cp282d_macro_trend_countercheck_adapter_package_v1"
ONNX_READINESS = "approved_for_export_not_parity_complete"
NEXT_ACTION = "run285A_export_cp282d_adapter_to_onnx_and_python_parity"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_runtime_authority_until_onnx_and_mt5_reproduction_receipts"
)

STAGE284 = ROOT / "stages" / STAGE284_ID
RUN_DIR = STAGE284 / "02_runs" / "run284A"
REVIEWS284 = STAGE284 / "03_reviews"
SELECTED284 = STAGE284 / "04_selected" / "selection_status.md"
REVIEW_INDEX284 = REVIEWS284 / "review_index.md"
STAGE_LEDGER284 = REVIEWS284 / "stage_run_ledger.csv"
INPUTS284 = STAGE284 / "01_inputs"
ADAPTER_MANIFEST_INPUT = INPUTS284 / "adapter_package_manifest.json"
ADAPTER_HASH_INPUT = INPUTS284 / "adapter_package_hash_receipt.json"

STAGE282_SCOREBOARD = ROOT / "stages" / "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild" / "02_runs" / "run282C" / "stability_scoreboard.csv"
STAGE282_SELECTED_PACKAGE = ROOT / "stages" / "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild" / "02_runs" / "run282C" / "selected_candidate_package.json"
STAGE283_PACKAGE_DIR = ROOT / "stages" / "283_onnx_candidate_campaign__adapter_package_for_cp282d_macro_trend_countercheck" / "02_runs" / "run283A" / "adapter_package"
PRODUCER = Path("stage_pipelines/stage284/execute_onnx_go_pressure_for_cp282d_adapter_package.py")

GO_SCORECARD = RUN_DIR / "onnx_go_pressure_scorecard.csv"
PACKAGE_AUDIT = RUN_DIR / "adapter_package_integrity_audit.csv"
PRESSURE_RECEIPT = RUN_DIR / "onnx_go_pressure_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS284 / "run284A_onnx_go_pressure_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage284_onnx_go_pass_stage285_export_open.md"

STAGE285 = ROOT / "stages" / STAGE285_ID
SPEC285 = STAGE285 / "00_spec" / "stage_brief.md"
INPUTS285 = STAGE285 / "01_inputs"
REVIEWS285 = STAGE285 / "03_reviews"
SELECTED285 = STAGE285 / "04_selected" / "selection_status.md"
STAGE_LEDGER285 = REVIEWS285 / "stage_run_ledger.csv"
REVIEW_INDEX285 = REVIEWS285 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

GO_COLUMNS = ("check_name", "status", "value", "threshold", "effect")
AUDIT_COLUMNS = ("path", "status", "sha256", "expected_sha256", "effect")
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


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def f(row: Mapping[str, str], key: str) -> float:
    try:
        return float(row.get(key, 0) or 0)
    except ValueError:
        return 0.0


def selected_scoreboard_row() -> dict[str, str]:
    for row in read_csv_dicts(STAGE282_SCOREBOARD):
        if row.get("selected_candidate") == SELECTED_CANDIDATE or row.get("package_id") == SELECTED_CANDIDATE:
            return row
    raise RuntimeError("selected candidate scoreboard row missing")


def build_go_scorecard(row: Mapping[str, str]) -> list[dict[str, Any]]:
    checks = [
        ("validation_net_profit", f(row, "validation_net_profit") >= 75.0, f(row, "validation_net_profit"), ">=75", "검증 순수익이 어댑터 이후 온엑스 내보내기 압박을 견딘다."),
        ("validation_pf", f(row, "validation_pf") >= 1.25, f(row, "validation_pf"), ">=1.25", "검증 수익 팩터가 약한 후보 수준을 넘는다."),
        ("validation_recovery", f(row, "validation_recovery") >= 0.45, f(row, "validation_recovery"), ">=0.45", "검증 손실폭 대비 회복이 최소선을 넘는다."),
        ("validation_trade_count", f(row, "validation_trade_count") >= 75.0, f(row, "validation_trade_count"), ">=75", "검증 거래 수가 너무 얇지 않다."),
        ("tier_b_validation_net_profit", f(row, "tier_b_validation_net_profit") > 50.0, f(row, "tier_b_validation_net_profit"), ">50", "Tier B 대체 검증이 음수로 깨지지 않는다."),
        ("oos_net_profit", f(row, "oos_net_profit") >= 150.0, f(row, "oos_net_profit"), ">=150", "표본외 상방이 유지된다."),
        ("oos_pf", f(row, "oos_pf") >= 1.50, f(row, "oos_pf"), ">=1.50", "표본외 수익 팩터가 충분하다."),
        ("oos_recovery", f(row, "oos_recovery") >= 1.50, f(row, "oos_recovery"), ">=1.50", "표본외 회복이 충분하다."),
        ("weak_month_floor", f(row, "validation_worst_month_net") > -90.0, f(row, "validation_worst_month_net"), ">-90", "검증 최악 월이 치명적이지 않다."),
        ("weak_session_floor", f(row, "validation_worst_session_net") > -5.0, f(row, "validation_worst_session_net"), ">-5", "검증 세션이 모두 양수권이다."),
        ("losing_streak_watch", f(row, "validation_max_losing_streak") <= 11.0, f(row, "validation_max_losing_streak"), "<=11", "손실 연속은 감시 대상이지만 폐기선은 넘지 않는다."),
        ("concentration_watch", f(row, "validation_top_10pct_contribution_share") <= 2.50, f(row, "validation_top_10pct_contribution_share"), "<=2.50", "상위 거래 집중이 온엑스 진행 전 폐기선은 아니다."),
    ]
    return [
        {
            "check_name": name,
            "status": "passed" if passed else "failed",
            "value": round(value, 6),
            "threshold": threshold,
            "effect": effect,
        }
        for name, passed, value, threshold, effect in checks
    ]


def build_package_audit(hash_receipt: Mapping[str, Any]) -> list[dict[str, str]]:
    expected = dict(hash_receipt.get("package_hashes", {}))
    rows: list[dict[str, str]] = []
    for path_text, expected_hash in expected.items():
        path = ROOT / path_text
        exists = path_exists(path)
        actual = sha256_file(path) if exists else ""
        rows.append(
            {
                "path": path_text,
                "status": "passed" if exists and actual == expected_hash else "failed",
                "sha256": actual,
                "expected_sha256": str(expected_hash),
                "effect": "패키지 산출물 해시가 Stage283 영수증과 일치한다." if exists and actual == expected_hash else "패키지 산출물 재생성이 필요하다.",
            }
        )
    return rows


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


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def stage285_spec_markdown() -> str:
    return f"""# Stage285 Brief(285단계 개요): ONNX Export, Parity, Runtime Reproduction(온엑스 내보내기, 동등성, 런타임 재현)

- canonical_stage_id(정식 단계 ID): `{STAGE285_ID}`
- single_question(단일 질문): `{ADAPTER_PACKAGE_ID}`를 ONNX(온엑스)로 내보내고 Python parity(파이썬 동등성)와 MT5 runtime reproduction(MT5 런타임 재현)을 완료할 수 있는가?
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): Stage285(285단계)부터는 ONNX export(온엑스 내보내기), Python inference check(파이썬 추론 확인), feature order parity(피처 순서 동등성), ONNX parity receipt(온엑스 동등성 영수증), MT5 runtime reproduction(MT5 런타임 재현)을 같은 흐름에서 닫는다.

`{BOUNDARY}`
"""


def report_markdown(go_rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, str]]) -> str:
    failed = [row for row in list(go_rows) + list(audit_rows) if row.get("status") != "passed"]
    return "\n".join(
        [
            "# run284A Report(284A 보고서): ONNX-Go Pressure(온엑스 진행 압박)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`",
            f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`",
            f"- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- failed_checks(실패 검사): `{len(failed)}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "Effect(효과): 어댑터 패키지와 선택 후보가 온엑스 내보내기를 시도할 만큼 통과했지만, 아직 동등성과 런타임 재현은 완료되지 않았다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def write_stage285_inputs() -> None:
    for path in (SPEC285.parent, INPUTS285, REVIEWS285, SELECTED285.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(SPEC285, stage285_spec_markdown())
    write_json(INPUTS285 / "adapter_package_manifest.json", load_json(ADAPTER_MANIFEST_INPUT))
    write_json(INPUTS285 / "adapter_package_hash_receipt.json", load_json(ADAPTER_HASH_INPUT))
    write_csv(INPUTS285 / "onnx_go_pressure_scorecard.csv", GO_COLUMNS, read_csv_dicts(GO_SCORECARD))
    write_md(
        INPUTS285 / "input_refs.md",
        f"""# Stage285 Input References(285단계 입력 참조)

- adapter_package_manifest(어댑터 패키지 목록): `{rel(INPUTS285 / 'adapter_package_manifest.json')}`
- adapter_package_hash_receipt(어댑터 패키지 해시 영수증): `{rel(INPUTS285 / 'adapter_package_hash_receipt.json')}`
- onnx_go_pressure_scorecard(온엑스 진행 압박 점수판): `{rel(INPUTS285 / 'onnx_go_pressure_scorecard.csv')}`
- source_report(원천 보고서): `{rel(REPORT)}`

Effect(효과): Stage285(285단계)는 온엑스 내보내기와 동등성 검증을 시작할 수 있다.
""",
    )
    write_md(
        SELECTED285,
        f"""# Stage285 Selection Status(285단계 선택 상태)

- stage_status(단계 상태): `opened_onnx_export_parity_runtime_reproduction`
- current_packet(현재 작업 묶음): `stage285_onnx_export_parity_runtime_reproduction_cp282d_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE284_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUTS285 / 'input_refs.md')}`
""",
    )
    write_md(
        REVIEW_INDEX285,
        f"""# Stage285 Review Index(285단계 검토 색인)

- stage_brief(단계 개요): `{rel(SPEC285)}`
- input_refs(입력 참조): `{rel(INPUTS285 / 'input_refs.md')}`
""",
    )
    write_csv(
        STAGE_LEDGER285,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage285_open",
                "stage_id": STAGE285_ID,
                "run_id": RUN_ID,
                "view": "stage285_open_onnx_export_parity_runtime_reproduction",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_onnx_export_parity_runtime_reproduction",
                "judgment": JUDGMENT,
                "evidence_boundary": "onnx_go_approved_no_parity_yet",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_outputs(created_at: str) -> list[Path]:
    score_row = selected_scoreboard_row()
    manifest = load_json(ADAPTER_MANIFEST_INPUT)
    hash_receipt = load_json(ADAPTER_HASH_INPUT)
    go_rows = build_go_scorecard(score_row)
    audit_rows = build_package_audit(hash_receipt)
    if any(row["status"] != "passed" for row in go_rows + audit_rows):
        raise RuntimeError("ONNX-go pressure failed; do not open Stage285.")
    write_csv(GO_SCORECARD, GO_COLUMNS, go_rows)
    write_csv(PACKAGE_AUDIT, AUDIT_COLUMNS, audit_rows)
    write_json(
        PRESSURE_RECEIPT,
        {
            "run_id": RUN_ID,
            "selected_candidate": SELECTED_CANDIDATE,
            "adapter_package": ADAPTER_PACKAGE_ID,
            "onnx_go_decision": "approved_for_export",
            "onnx_readiness": ONNX_READINESS,
            "go_check_count": len(go_rows),
            "package_audit_count": len(audit_rows),
            "judgment": JUDGMENT,
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
            "adapter_manifest": manifest,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"go_checks={len(go_rows)};package_audits={len(audit_rows)};adapter_package={ADAPTER_PACKAGE_ID}",
                "evidence_missing": "ONNX export;Python inference check;ONNX parity;MT5 runtime reproduction",
                "judgment_label": JUDGMENT,
                "judgment_class": "onnx_go_approved_no_parity_yet",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "온엑스 내보내기 진행은 허용됐지만 동등성은 아직 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "adapter_package_integrity(어댑터 패키지 무결성)",
                "status": "passed",
                "evidence_path": rel(PACKAGE_AUDIT),
                "effect": "Stage283 패키지 해시와 현재 파일이 일치한다.",
            },
            {
                "gate_name": "onnx_go_pressure_metrics(온엑스 진행 압박 지표)",
                "status": "passed",
                "evidence_path": rel(GO_SCORECARD),
                "effect": "검증, 표본외, Tier B, 약한 월/세션 기준을 통과했다.",
            },
            {
                "gate_name": "parity_not_yet_claimed(동등성 아직 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "내보내기와 동등성 검증 전에는 완료를 주장하지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(go_rows, audit_rows))
    write_md(
        DECISION,
        f"""# Decision(결정): Stage284 ONNX-Go Passed and Stage285 Open(284단계 온엑스 진행 통과와 285단계 개방)

- date(날짜): `{UPDATED_ON}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`
- decision(결정): ONNX export/parity/runtime reproduction(온엑스 내보내기/동등성/런타임 재현) 단계로 넘어간다.
- effect(효과): 아직 Goal Achieve(목표 달성)는 아니며, Stage285(285단계)에서 내보내기와 재현 영수증을 완료해야 한다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage285_inputs()
    artifacts = [
        GO_SCORECARD,
        PACKAGE_AUDIT,
        PRESSURE_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC285,
        INPUTS285 / "adapter_package_manifest.json",
        INPUTS285 / "adapter_package_hash_receipt.json",
        INPUTS285 / "onnx_go_pressure_scorecard.csv",
        INPUTS285 / "input_refs.md",
        SELECTED285,
        STAGE_LEDGER285,
        REVIEW_INDEX285,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE284_ID,
            "target_stage_id": STAGE285_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": SELECTED_CANDIDATE,
            "adapter_package": ADAPTER_PACKAGE_ID,
            "onnx_readiness": ONNX_READINESS,
            "goal_achieve": "not_claimed",
            "created_at_utc": created_at,
            "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts.append(RUN_MANIFEST)
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(ADAPTER_MANIFEST_INPUT), rel(ADAPTER_HASH_INPUT), rel(STAGE282_SCOREBOARD), rel(ROOT / PRODUCER)],
            "source_hashes": {
                rel(path): sha256_file(path)
                for path in [ADAPTER_MANIFEST_INPUT, ADAPTER_HASH_INPUT, STAGE282_SCOREBOARD, ROOT / PRODUCER]
                if path_exists(path)
            },
            "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "lineage_judgment": "connected_onnx_go_approved_no_parity_yet",
        },
    )
    artifacts.append(LINEAGE)
    return artifacts


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE284_ID,
                "lane": "onnx_go_pressure",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"selected_candidate={SELECTED_CANDIDATE};adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE285_ID}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__onnx_go_pressure",
                "stage_id": STAGE284_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage284_onnx_go_stage285_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "onnx_go_pressure(온엑스 진행 압박)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "onnx_go_no_parity_yet",
                "scoreboard_lane": "onnx_go_pressure",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"adapter_package={ADAPTER_PACKAGE_ID};onnx_readiness={ONNX_READINESS}",
                "guardrail_kpi": "goal_achieve=not_claimed;runtime_authority=not_claimed",
                "external_verification_status": "not_applicable_pre_export_pressure",
                "notes": f"target_stage={STAGE285_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER284,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage284_closeout",
                "stage_id": STAGE284_ID,
                "run_id": RUN_ID,
                "view": "stage284_onnx_go_stage285_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "onnx_go_pressure_scorecard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "onnx_go_no_parity_yet",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE285_ID}.",
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage284_onnx_go_pressure_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE284_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run284A ONNX-go pressure(284A 온엑스 진행 압박)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED284).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", f"- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run284A_report", f"- run284A_report(284A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage285_open", f"- stage285_open(285단계 개방): `{STAGE285_ID}`")
    write_md(SELECTED284, selected)

    review_index = io_path(REVIEW_INDEX284).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX284) else "# Stage284 Review Index(284단계 검토 색인)\n"
    review_index = append_once(review_index, "run284A_report", f"- run284A_report(284A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX284, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage285_onnx_export_parity_runtime_reproduction_cp282d_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE285_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE284_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `onnx_export_parity_runtime_reproduction_cp282d`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_onnx_export_parity_runtime_reproduction`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run284A_summary",
        f"- run284A_summary(284A 요약): Adapter package(어댑터 패키지) `{ADAPTER_PACKAGE_ID}`가 ONNX-go pressure(온엑스 진행 압박)를 통과했다. Effect(효과): Stage285(285단계)에서 ONNX export/parity/runtime reproduction(온엑스 내보내기/동등성/런타임 재현)을 시작한다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE285_ID}")
    focus = (
        f"- >-\n"
        f"  Stage285(285단계) ONNX export/parity/runtime reproduction(온엑스 내보내기/동등성/런타임 재현) opened by `{RUN_ID}`. "
        f"Effect(효과): ONNX-go(온엑스 진행)는 통과했지만 Goal Achieve(목표 달성)는 동등성/런타임 재현 뒤에만 가능하다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run284A ONNX-go pressure(284A 온엑스 진행 압박)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Stage285(285단계) ONNX export/parity/runtime reproduction(온엑스 내보내기/동등성/런타임 재현)을 열었다.\n- boundary(경계): Goal Achieve(목표 달성)와 런타임 권위는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS284).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    artifacts = write_outputs(created_at)
    update_registers_and_docs(created_at, artifacts)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "selected_candidate": SELECTED_CANDIDATE,
                "adapter_package": ADAPTER_PACKAGE_ID,
                "onnx_readiness": ONNX_READINESS,
                "goal_achieve": "not_claimed",
                "target_stage": STAGE285_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
