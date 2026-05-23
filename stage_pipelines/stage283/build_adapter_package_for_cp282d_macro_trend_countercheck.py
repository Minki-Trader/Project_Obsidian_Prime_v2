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
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402


STAGE283_ID = "283_onnx_candidate_campaign__adapter_package_for_cp282d_macro_trend_countercheck"
STAGE284_ID = "284_onnx_candidate_campaign__onnx_go_pressure_for_cp282d_adapter"
RUN_ID = "run283A_build_adapter_package_for_cp282d_macro_trend_countercheck_v1"
SOURCE_RUN_ID = "run282C_review_validation_first_asymmetric_confirmation_mt5_probe_v1"
STATUS = "completed_adapter_package_for_selected_candidate_stage284_opened"
JUDGMENT = "adapter_package_built_no_onnx_readiness"
SELECTED_CANDIDATE = "cp282D_macro_trend_countercheck_surface"
SELECTED_BRANCH = "run282A_cp282D_macro_trend_countercheck"
ADAPTER_PACKAGE_ID = "stage283_cp282d_macro_trend_countercheck_adapter_package_v1"
NEXT_ACTION = "run284A_execute_onnx_go_pressure_for_cp282d_adapter_package"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE283 = ROOT / "stages" / STAGE283_ID
RUN_DIR = STAGE283 / "02_runs" / "run283A"
REVIEWS283 = STAGE283 / "03_reviews"
SELECTED283 = STAGE283 / "04_selected" / "selection_status.md"
REVIEW_INDEX283 = REVIEWS283 / "review_index.md"
STAGE_LEDGER283 = REVIEWS283 / "stage_run_ledger.csv"
INPUTS283 = STAGE283 / "01_inputs"

STAGE282 = ROOT / "stages" / "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild"
RUN282A = STAGE282 / "02_runs" / "run282A"
RUN282C = STAGE282 / "02_runs" / "run282C"
SOURCE_MANIFEST = RUN282A / "candidate_payload_manifest.csv"
SOURCE_BRANCH_QUEUE = RUN282A / "branch_design_queue.csv"
SOURCE_SCOREBOARD = RUN282C / "stability_scoreboard.csv"
SOURCE_FAILURE = RUN282C / "failure_memory.csv"
SOURCE_SELECTED_PACKAGE = INPUTS283 / "selected_candidate_package.json"

PACKAGE_DIR = RUN_DIR / "adapter_package"
FEATURE_ORDER_RUNTIME = PACKAGE_DIR / "feature_order_runtime.csv"
FEATURE_ORDER_SOURCE = PACKAGE_DIR / "feature_order_source.csv"
ADAPTER_SCHEMA = PACKAGE_DIR / "adapter_schema.json"
DECISION_SURFACE = PACKAGE_DIR / "decision_surface.json"
RISK_LOGIC = PACKAGE_DIR / "risk_logic.json"
RUNTIME_HANDOFF = PACKAGE_DIR / "runtime_handoff_manifest.json"
CANDIDATE_EVIDENCE = PACKAGE_DIR / "candidate_evidence_summary.csv"
FAILURE_MEMORY = PACKAGE_DIR / "failure_memory_summary.csv"
PACKAGE_MANIFEST = PACKAGE_DIR / "adapter_package_manifest.json"
PACKAGE_RECEIPT = PACKAGE_DIR / "adapter_package_hash_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS283 / "run283A_adapter_package_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage283_adapter_package_built_stage284_onnx_go_pressure_open.md"
PRODUCER = Path("stage_pipelines/stage283/build_adapter_package_for_cp282d_macro_trend_countercheck.py")

STAGE284 = ROOT / "stages" / STAGE284_ID
SPEC284 = STAGE284 / "00_spec" / "stage_brief.md"
INPUTS284 = STAGE284 / "01_inputs"
REVIEWS284 = STAGE284 / "03_reviews"
SELECTED284 = STAGE284 / "04_selected" / "selection_status.md"
STAGE_LEDGER284 = REVIEWS284 / "stage_run_ledger.csv"
REVIEW_INDEX284 = REVIEWS284 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

FEATURE_ORDER_COLUMNS = ("position", "feature_name", "dtype", "source", "required", "meaning")
EVIDENCE_COLUMNS = ("metric", "value", "scope", "source")
FAILURE_COLUMNS = ("materialized_branch_id", "package_id", "failure_type", "failure_reasons", "salvage_value", "reopen_condition", "claim_boundary")
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


def selected_manifest_row() -> dict[str, str]:
    for row in read_csv_dicts(SOURCE_MANIFEST):
        if row.get("materialized_branch_id") == SELECTED_BRANCH or row.get("package_id") == SELECTED_CANDIDATE:
            return row
    raise RuntimeError(f"selected branch not found: {SELECTED_BRANCH}")


def selected_branch_row() -> dict[str, str]:
    for row in read_csv_dicts(SOURCE_BRANCH_QUEUE):
        if row.get("materialized_branch_id") == SELECTED_BRANCH or row.get("package_id") == SELECTED_CANDIDATE:
            return row
    raise RuntimeError(f"selected branch design not found: {SELECTED_BRANCH}")


def selected_scoreboard_row() -> dict[str, str]:
    for row in read_csv_dicts(SOURCE_SCOREBOARD):
        if row.get("materialized_branch_id") == SELECTED_BRANCH or row.get("package_id") == SELECTED_CANDIDATE:
            return row
    raise RuntimeError(f"selected scoreboard row not found: {SELECTED_BRANCH}")


def build_package(created_at: str) -> list[Path]:
    io_path(PACKAGE_DIR).mkdir(parents=True, exist_ok=True)
    manifest_row = selected_manifest_row()
    branch_row = selected_branch_row()
    score_row = selected_scoreboard_row()
    selected_package = load_json(SOURCE_SELECTED_PACKAGE)
    runtime_rows = [
        {
            "position": 0,
            "feature_name": "route_signal_value",
            "dtype": "int8",
            "source": "Stage282 precomputed validation-first direction surface",
            "required": True,
            "meaning": "-1 short, 0 flat, +1 long for single-feature runtime table",
        }
    ]
    source_rows = [
        (0, "direction_signal_value", "int8", "Stage279 q02/q03 directional payload", True, "base direction source before countercheck"),
        (1, "historical_vol_5_over_20", "float", "Stage279 feature payload", True, "volatility compression/expansion guard"),
        (2, "return_zscore_20", "float", "Stage279 feature payload", True, "return pressure guard"),
        (3, "di_spread_14", "float", "Stage279 feature payload", True, "local trend direction check"),
        (4, "ema20_ema50_diff", "float", "Stage279 feature payload", True, "local trend slope check"),
        (5, "rsi_14_slope_3", "float", "Stage279 feature payload", True, "q03 replacement countercheck"),
        (6, "us100_minus_mega8_equal_return_1", "float", "Stage279 feature payload", True, "macro relative strength check"),
        (7, "us100_minus_top3_weighted_return_1", "float", "Stage279 feature payload", True, "macro concentration countercheck"),
    ]
    write_csv(FEATURE_ORDER_RUNTIME, FEATURE_ORDER_COLUMNS, runtime_rows)
    write_csv(
        FEATURE_ORDER_SOURCE,
        FEATURE_ORDER_COLUMNS,
        [
            {
                "position": pos,
                "feature_name": name,
                "dtype": dtype,
                "source": source,
                "required": required,
                "meaning": meaning,
            }
            for pos, name, dtype, source, required, meaning in source_rows
        ],
    )
    write_json(
        ADAPTER_SCHEMA,
        {
            "adapter_package_id": ADAPTER_PACKAGE_ID,
            "selected_candidate": SELECTED_CANDIDATE,
            "runtime_input_features": ["route_signal_value"],
            "source_reconstruction_features": [row[1] for row in source_rows],
            "runtime_output": {
                "score_short": "1.0 when route_signal_value is -1 else 0.0",
                "score_flat": "1.0 when route_signal_value is 0 else 0.0",
                "score_long": "1.0 when route_signal_value is +1 else 0.0",
            },
            "feature_order_hash": ordered_hash(["route_signal_value"]),
            "source_feature_order_hash": ordered_hash([row[1] for row in source_rows]),
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DECISION_SURFACE,
        {
            "selected_candidate": SELECTED_CANDIDATE,
            "surface_summary": branch_row.get("decision_surface", ""),
            "materialized_branch_id": SELECTED_BRANCH,
            "direction_surface_hash": manifest_row.get("direction_surface_hash", ""),
            "rule": {
                "blend": "Use q03 direction only when q03 is non-flat and DI spread or RSI slope agrees; otherwise use q02 direction.",
                "countercheck": "Allow direction only when local DI/EMA trend agrees or macro relative strength plus DI agree.",
                "pressure": "Require historical_vol_5_over_20 in [0.70, 1.50] and abs(return_zscore_20) <= 1.25.",
            },
            "runtime_signal": "route_signal_value",
        },
    )
    write_json(
        RISK_LOGIC,
        {
            "selected_candidate": SELECTED_CANDIDATE,
            "risk_summary": branch_row.get("risk_logic", ""),
            "mt5_runtime_parameters": {
                "max_hold_bars": 12,
                "close_on_flat_signal": False,
                "reverse_on_opposite_signal": True,
                "entry_transition_only": False,
                "same_direction_reentry_cooldown_bars": 0,
            },
            "known_weakness": "validation losing streak remains watch-listed; Stage284 must pressure this before ONNX export.",
            "discard_condition": "If Stage284 expands weak-month/session or losing-streak risk, Adapter package is not ONNX-go.",
        },
    )
    write_json(
        RUNTIME_HANDOFF,
        {
            "selected_candidate": SELECTED_CANDIDATE,
            "adapter_package_id": ADAPTER_PACKAGE_ID,
            "payload_path": manifest_row.get("payload_path", ""),
            "payload_hash": manifest_row.get("payload_hash", ""),
            "handoff_path": manifest_row.get("handoff_path", ""),
            "handoff_hash": manifest_row.get("handoff_hash", ""),
            "mt5_tier_a_signal_path": manifest_row.get("mt5_tier_a_signal_path", ""),
            "mt5_tier_a_signal_hash": manifest_row.get("mt5_tier_a_signal_hash", ""),
            "mt5_tier_b_stress_signal_path": manifest_row.get("mt5_tier_b_stress_signal_path", ""),
            "mt5_tier_b_stress_signal_hash": manifest_row.get("mt5_tier_b_stress_signal_hash", ""),
            "mt5_actual_routed_signal_path": manifest_row.get("mt5_actual_routed_signal_path", ""),
            "mt5_actual_routed_signal_hash": manifest_row.get("mt5_actual_routed_signal_hash", ""),
            "mt5_probe_execution_result": rel(ROOT / "stages" / "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild" / "02_runs" / "run282B" / "execution_result.json"),
            "mt5_probe_kpi_summary": rel(ROOT / "stages" / "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild" / "02_runs" / "run282B" / "mt5_kpi_summary.csv"),
            "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
        },
    )
    evidence_rows = [
        {"metric": key, "value": value, "scope": "selected_candidate_scoreboard", "source": rel(SOURCE_SCOREBOARD)}
        for key, value in score_row.items()
        if key
        in {
            "validation_net_profit",
            "validation_pf",
            "validation_trade_count",
            "validation_dd",
            "validation_recovery",
            "oos_net_profit",
            "oos_pf",
            "oos_trade_count",
            "oos_dd",
            "oos_recovery",
            "validation_worst_month_net",
            "validation_worst_session_net",
            "validation_max_losing_streak",
            "validation_top_10pct_contribution_share",
        }
    ]
    write_csv(CANDIDATE_EVIDENCE, EVIDENCE_COLUMNS, evidence_rows)
    failure_rows = read_csv_dicts(SOURCE_FAILURE) if path_exists(SOURCE_FAILURE) else []
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    package_manifest = {
        "adapter_package_id": ADAPTER_PACKAGE_ID,
        "selected_candidate": SELECTED_CANDIDATE,
        "selected_branch": SELECTED_BRANCH,
        "source_selected_package": selected_package,
        "created_at_utc": created_at,
        "runtime_feature_order_path": rel(FEATURE_ORDER_RUNTIME),
        "source_feature_order_path": rel(FEATURE_ORDER_SOURCE),
        "adapter_schema_path": rel(ADAPTER_SCHEMA),
        "decision_surface_path": rel(DECISION_SURFACE),
        "risk_logic_path": rel(RISK_LOGIC),
        "runtime_handoff_path": rel(RUNTIME_HANDOFF),
        "candidate_evidence_path": rel(CANDIDATE_EVIDENCE),
        "adapter_package": ADAPTER_PACKAGE_ID,
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(PACKAGE_MANIFEST, package_manifest)
    package_paths = [
        FEATURE_ORDER_RUNTIME,
        FEATURE_ORDER_SOURCE,
        ADAPTER_SCHEMA,
        DECISION_SURFACE,
        RISK_LOGIC,
        RUNTIME_HANDOFF,
        CANDIDATE_EVIDENCE,
        FAILURE_MEMORY,
        PACKAGE_MANIFEST,
    ]
    write_json(
        PACKAGE_RECEIPT,
        {
            "adapter_package_id": ADAPTER_PACKAGE_ID,
            "selected_candidate": SELECTED_CANDIDATE,
            "package_paths": [rel(path) for path in package_paths],
            "package_hashes": {rel(path): sha256_file(path) for path in package_paths if path_exists(path)},
            "package_hash": hashlib.sha256(
                json.dumps({rel(path): sha256_file(path) for path in package_paths if path_exists(path)}, sort_keys=True).encode("utf-8")
            ).hexdigest(),
            "adapter_package": ADAPTER_PACKAGE_ID,
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    package_paths.append(PACKAGE_RECEIPT)
    return package_paths


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


def stage284_spec_markdown() -> str:
    return f"""# Stage284 Brief(284단계 개요): ONNX-Go Pressure for cp282D Adapter(cp282D 어댑터 온엑스 진행 압박)

- canonical_stage_id(정식 단계 ID): `{STAGE284_ID}`
- single_question(단일 질문): `{ADAPTER_PACKAGE_ID}`가 ONNX(온엑스) export(내보내기)와 parity(동등성)로 넘어갈 만큼 압박을 견디는가?
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): Stage284(284단계)는 export(내보내기) 전에 약한 월, 세션, 손실 연속, Tier B 대체, 런타임 인계 추적성을 마지막으로 압박한다.

`{BOUNDARY}`
"""


def report_markdown() -> str:
    return "\n".join(
        [
            "# run283A Report(283A 보고서): Adapter Package Built(어댑터 패키지 구성 완료)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`",
            f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "Effect(효과): feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), runtime handoff(런타임 인계)를 한 패키지로 묶었다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def write_stage284_inputs() -> None:
    for path in (SPEC284.parent, INPUTS284, REVIEWS284, SELECTED284.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(SPEC284, stage284_spec_markdown())
    write_json(INPUTS284 / "adapter_package_manifest.json", load_json(PACKAGE_MANIFEST))
    write_json(INPUTS284 / "adapter_package_hash_receipt.json", load_json(PACKAGE_RECEIPT))
    write_md(
        INPUTS284 / "input_refs.md",
        f"""# Stage284 Input References(284단계 입력 참조)

- adapter_package_manifest(어댑터 패키지 목록): `{rel(INPUTS284 / 'adapter_package_manifest.json')}`
- adapter_package_hash_receipt(어댑터 패키지 해시 영수증): `{rel(INPUTS284 / 'adapter_package_hash_receipt.json')}`
- source_report(원천 보고서): `{rel(REPORT)}`

Effect(효과): Stage284(284단계)는 온엑스 내보내기 전에 어댑터 패키지의 추적성과 약점 구간을 압박한다.
""",
    )
    write_md(
        SELECTED284,
        f"""# Stage284 Selection Status(284단계 선택 상태)

- stage_status(단계 상태): `opened_onnx_go_pressure_no_onnx_readiness_claim`
- current_packet(현재 작업 묶음): `stage284_onnx_go_pressure_for_cp282d_adapter_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE283_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUTS284 / 'input_refs.md')}`
""",
    )
    write_md(
        REVIEW_INDEX284,
        f"""# Stage284 Review Index(284단계 검토 색인)

- stage_brief(단계 개요): `{rel(SPEC284)}`
- input_refs(입력 참조): `{rel(INPUTS284 / 'input_refs.md')}`
""",
    )
    write_csv(
        STAGE_LEDGER284,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage284_open",
                "stage_id": STAGE284_ID,
                "run_id": RUN_ID,
                "view": "stage284_open_onnx_go_pressure",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_onnx_go_pressure_no_onnx_readiness_claim",
                "judgment": JUDGMENT,
                "evidence_boundary": "adapter_package_built_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_outputs(package_paths: Sequence[Path], created_at: str) -> list[Path]:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"adapter_package={ADAPTER_PACKAGE_ID};paths={len(package_paths)}",
                "evidence_missing": "ONNX go pressure;ONNX export;ONNX parity;MT5 ONNX runtime reproduction",
                "judgment_label": JUDGMENT,
                "judgment_class": "adapter_package_built",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "어댑터 패키지는 만들어졌지만 온엑스 준비는 아직 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "feature_order_traceable(피처 순서 추적 가능)",
                "status": "passed",
                "evidence_path": f"{rel(FEATURE_ORDER_RUNTIME)};{rel(FEATURE_ORDER_SOURCE)}",
                "effect": "런타임 입력과 원천 재구성 입력을 분리해 추적한다.",
            },
            {
                "gate_name": "decision_risk_handoff_packaged(판단/위험/인계 패키지화)",
                "status": "passed",
                "evidence_path": f"{rel(DECISION_SURFACE)};{rel(RISK_LOGIC)};{rel(RUNTIME_HANDOFF)}",
                "effect": "후보를 이름이 아니라 패키지 단위로 다룬다.",
            },
            {
                "gate_name": "no_onnx_readiness_claim(온엑스 준비 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "Stage284 압박 전에는 온엑스 준비를 주장하지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown())
    write_md(
        DECISION,
        f"""# Decision(결정): Stage283 Adapter Package Built and Stage284 Open(283단계 어댑터 패키지 구성과 284단계 개방)

- date(날짜): `{UPDATED_ON}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- decision(결정): Adapter package(어댑터 패키지)를 구성하고 Stage284(284단계) ONNX-go pressure(온엑스 진행 압박)를 연다.
- effect(효과): ONNX export(온엑스 내보내기) 전에 패키지 추적성과 약점 구간을 한 번 더 압박한다.
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage284_inputs()
    artifacts = [
        *package_paths,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC284,
        INPUTS284 / "adapter_package_manifest.json",
        INPUTS284 / "adapter_package_hash_receipt.json",
        INPUTS284 / "input_refs.md",
        SELECTED284,
        STAGE_LEDGER284,
        REVIEW_INDEX284,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE283_ID,
            "target_stage_id": STAGE284_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": SELECTED_CANDIDATE,
            "adapter_package": ADAPTER_PACKAGE_ID,
            "onnx_readiness": "not_claimed",
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
            "source_inputs": [rel(SOURCE_SELECTED_PACKAGE), rel(SOURCE_MANIFEST), rel(SOURCE_BRANCH_QUEUE), rel(SOURCE_SCOREBOARD), rel(ROOT / PRODUCER)],
            "source_hashes": {
                rel(path): sha256_file(path)
                for path in [SOURCE_SELECTED_PACKAGE, SOURCE_MANIFEST, SOURCE_BRANCH_QUEUE, SOURCE_SCOREBOARD, ROOT / PRODUCER]
                if path_exists(path)
            },
            "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "lineage_judgment": "connected_with_boundary_adapter_package_built_no_onnx_claim",
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
                "stage_id": STAGE283_ID,
                "lane": "adapter_package_build",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"selected_candidate={SELECTED_CANDIDATE};adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE284_ID}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__adapter_package",
                "stage_id": STAGE283_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage283_adapter_package_stage284_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "adapter_package_build(어댑터 패키지 구성)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "adapter_package_no_onnx_readiness",
                "scoreboard_lane": "adapter_package",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"selected_candidate={SELECTED_CANDIDATE};adapter_package={ADAPTER_PACKAGE_ID}",
                "guardrail_kpi": "onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_adapter_packaging",
                "notes": f"target_stage={STAGE284_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER283,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage283_closeout",
                "stage_id": STAGE283_ID,
                "run_id": RUN_ID,
                "view": "stage283_adapter_package_stage284_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "adapter_package_manifest",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "adapter_package_built_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE284_ID}.",
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage283_adapter_package_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE283_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run283A adapter package(283A 어댑터 패키지)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED283).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- Adapter package(어댑터 패키지):", f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run283A_report", f"- run283A_report(283A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage284_open", f"- stage284_open(284단계 개방): `{STAGE284_ID}`")
    write_md(SELECTED283, selected)

    review_index = io_path(REVIEW_INDEX283).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX283) else "# Stage283 Review Index(283단계 검토 색인)\n"
    review_index = append_once(review_index, "run283A_report", f"- run283A_report(283A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX283, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage284_onnx_go_pressure_for_cp282d_adapter_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE284_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE283_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `onnx_go_pressure_for_cp282d_adapter`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", f"- adapter_under_review(검토 중 어댑터): `{ADAPTER_PACKAGE_ID}`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_onnx_go_pressure_no_onnx_readiness_claim`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run283A_summary",
        f"- run283A_summary(283A 요약): `{SELECTED_CANDIDATE}`의 Adapter package(어댑터 패키지) `{ADAPTER_PACKAGE_ID}`를 구성하고 Stage284(284단계)를 열었다. Effect(효과): ONNX readiness(온엑스 준비)는 아직 주장하지 않고 마지막 압박 검증으로 넘긴다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE284_ID}")
    focus = (
        f"- >-\n"
        f"  Stage284(284단계) ONNX-go pressure(온엑스 진행 압박) opened for Adapter package(어댑터 패키지) `{ADAPTER_PACKAGE_ID}` by `{RUN_ID}`. "
        f"Effect(효과): ONNX export(온엑스 내보내기) 전에 약점 구간과 패키지 추적성을 압박한다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run283A Adapter package(283A 어댑터 패키지)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): `{ADAPTER_PACKAGE_ID}`를 구성하고 Stage284(284단계)를 열었다.\n- boundary(경계): ONNX readiness(온엑스 준비)와 Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    for path in (RUN_DIR, PACKAGE_DIR, REVIEWS283):
        io_path(path).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    package_paths = build_package(created_at)
    artifacts = write_outputs(package_paths, created_at)
    update_registers_and_docs(created_at, artifacts)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "selected_candidate": SELECTED_CANDIDATE,
                "adapter_package": ADAPTER_PACKAGE_ID,
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "target_stage": STAGE284_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
