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


STAGE324_ID = "324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter"
STAGE325_ID = "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
RUN_ID = "run324A_execute_onnx_go_pressure_for_cp322a_adapter_package_v1"
SOURCE_RUN_ID = "run323A_build_adapter_package_for_cp322a_selected_curve_v1"
STATUS = "completed_onnx_go_pressure_passed_stage325_opened"
JUDGMENT = "onnx_go_approved_for_export_no_parity_yet"
SELECTED_CANDIDATE = "cp322A_cp321b_exact_replay_control_surface"
ADAPTER_PACKAGE_ID = "stage323_cp322a_selected_curve_adapter_package_v1"
ONNX_READINESS = "approved_for_export_not_parity_complete"
NEXT_ACTION = "run325A_export_cp322a_adapter_to_onnx_and_runtime_reproduction"
UPDATED_ON = "2026-05-26"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_runtime_authority_until_onnx_and_mt5_reproduction_receipts"
)

STAGE324 = ROOT / "stages" / STAGE324_ID
RUN_DIR = STAGE324 / "02_runs" / "run324A"
REVIEWS324 = STAGE324 / "03_reviews"
SELECTED324 = STAGE324 / "04_selected" / "selection_status.md"
REVIEW_INDEX324 = REVIEWS324 / "review_index.md"
STAGE_LEDGER324 = REVIEWS324 / "stage_run_ledger.csv"
INPUTS324 = STAGE324 / "01_inputs"
ADAPTER_MANIFEST_INPUT = INPUTS324 / "adapter_package_manifest.json"
ADAPTER_HASH_INPUT = INPUTS324 / "adapter_package_hash_receipt.json"

PRODUCER = ROOT / "stage_pipelines" / "stage324" / "execute_onnx_go_pressure_for_cp322a_adapter_package.py"
GO_SCORECARD = RUN_DIR / "onnx_go_pressure_scorecard.csv"
PACKAGE_AUDIT = RUN_DIR / "adapter_package_integrity_audit.csv"
FEATURE_HANDOFF_AUDIT = RUN_DIR / "feature_handoff_audit.csv"
PRESSURE_RECEIPT = RUN_DIR / "onnx_go_pressure_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS324 / "run324A_onnx_go_pressure_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-26_stage324_cp322a_onnx_go_pass_stage325_open.md"

STAGE325 = ROOT / "stages" / STAGE325_ID
SPEC325 = STAGE325 / "00_spec" / "stage_brief.md"
INPUTS325 = STAGE325 / "01_inputs"
REVIEWS325 = STAGE325 / "03_reviews"
SELECTED325 = STAGE325 / "04_selected" / "selection_status.md"
STAGE_LEDGER325 = REVIEWS325 / "stage_run_ledger.csv"
REVIEW_INDEX325 = REVIEWS325 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

GO_COLUMNS = ("check_name", "status", "value", "threshold", "effect")
AUDIT_COLUMNS = ("path", "status", "sha256", "expected_sha256", "effect")
FEATURE_AUDIT_COLUMNS = ("check_name", "status", "value", "expected", "effect")
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


def write_text(path: Path, text: str, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_md(path: Path, text: str) -> None:
    write_text(path, text, bom=True)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def between(value: float, low: float, high: float) -> bool:
    return low <= value <= high


def evidence_map(path: Path) -> dict[tuple[str, str], str]:
    rows = read_csv_dicts(path)
    return {(row.get("scope", ""), row.get("metric", "")): row.get("value", "") for row in rows}


def value(evidence: Mapping[tuple[str, str], str], scope: str, metric: str) -> float:
    return as_float(evidence.get((scope, metric)))


def package_path(manifest: Mapping[str, Any], key: str) -> Path:
    raw = manifest.get(key, "")
    if not raw:
        raise RuntimeError(f"missing package path key: {key}")
    return ROOT / str(raw)


def build_go_scorecard(manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    evidence_path = package_path(manifest, "candidate_evidence_path")
    evidence = evidence_map(evidence_path)
    val_tpd = value(evidence, "stage322_selected_scoreboard", "validation_trades_per_day")
    oos_tpd = value(evidence, "stage322_selected_scoreboard", "oos_trades_per_day")
    val_trades = value(evidence, "stage322_selected_scoreboard", "validation_trades")
    oos_trades = value(evidence, "stage322_selected_scoreboard", "oos_trades")
    val_net = value(evidence, "stage322_selected_scoreboard", "validation_net_profit")
    oos_net = value(evidence, "stage322_selected_scoreboard", "oos_net_profit")
    combined_net = value(evidence, "stage322_selected_scoreboard", "combined_net_profit")
    val_pf = value(evidence, "stage322_selected_scoreboard", "validation_pf")
    oos_pf = value(evidence, "stage322_selected_scoreboard", "oos_pf")
    val_dd = value(evidence, "stage322_selected_scoreboard", "validation_max_dd_percent")
    oos_dd = value(evidence, "stage322_selected_scoreboard", "oos_max_dd_percent")
    val_recovery = value(evidence, "stage322_selected_scoreboard", "validation_recovery")
    oos_recovery = value(evidence, "stage322_selected_scoreboard", "oos_recovery")
    val_expectancy = value(evidence, "stage322_selected_scoreboard", "validation_expectancy")
    oos_expectancy = value(evidence, "stage322_selected_scoreboard", "oos_expectancy")
    val_chunk = value(evidence, "stage322_selected_scoreboard", "validation_worst_chunk_net")
    oos_chunk = value(evidence, "stage322_selected_scoreboard", "oos_worst_chunk_net")
    val_negative_months = value(evidence, "stage322_selected_scoreboard", "validation_negative_month_count")
    oos_negative_months = value(evidence, "stage322_selected_scoreboard", "oos_negative_month_count")
    checks = [
        ("validation_minimum_trade_count", val_trades >= 750, val_trades, ">=750", "검증 거래 수가 ONNX(온엑스) 패키지 실험을 할 만큼 충분하다."),
        ("oos_minimum_trade_count", oos_trades >= 500, oos_trades, ">=500", "표본외 거래 수가 과소 표본이 아니다."),
        ("validation_trades_per_day_4_10", between(val_tpd, 4.0, 10.0), val_tpd, "4..10", "검증 일 거래수가 사용자가 요구한 4-10 trades/day(일 4-10거래)에 들어온다."),
        ("oos_trades_per_day_4_10", between(oos_tpd, 4.0, 10.0), oos_tpd, "4..10", "표본외 일 거래수가 사용자가 요구한 4-10 trades/day(일 4-10거래)에 들어온다."),
        ("validation_net_profit_scale", val_net >= 450000, val_net, ">=450000", "검증 순수익(net profit, 순수익)이 규모 조건을 넘는다."),
        ("oos_net_profit_scale", oos_net >= 200000, oos_net, ">=200000", "표본외 순수익(net profit, 순수익)이 규모 조건을 넘는다."),
        ("combined_net_profit_scale", combined_net >= 650000, combined_net, ">=650000", "검증+표본외 합산 순수익이 scale(규모) 조건을 넘는다."),
        ("validation_pf_efficiency", val_pf >= 1.55, val_pf, ">=1.55", "검증 profit factor(수익 팩터)가 효율 조건을 넘는다."),
        ("oos_pf_efficiency", oos_pf >= 1.50, oos_pf, ">=1.50", "표본외 profit factor(수익 팩터)가 효율 조건을 넘는다."),
        ("validation_dd_bound", val_dd <= 20.0, val_dd, "<=20", "검증 drawdown(손실폭)이 Stage322 압박 한계 안에 있다."),
        ("oos_dd_bound", oos_dd <= 18.0, oos_dd, "<=18", "표본외 drawdown(손실폭)이 Stage322 압박 한계 안에 있다."),
        ("validation_recovery", val_recovery >= 4.0, val_recovery, ">=4.0", "검증 recovery(회복)가 손실 대비 회복 조건을 넘는다."),
        ("oos_recovery", oos_recovery >= 5.0, oos_recovery, ">=5.0", "표본외 recovery(회복)가 손실 대비 회복 조건을 넘는다."),
        ("validation_expectancy", val_expectancy >= 450, val_expectancy, ">=450", "검증 expectancy(기대값)가 비용 후 여유를 남긴다."),
        ("oos_expectancy", oos_expectancy >= 350, oos_expectancy, ">=350", "표본외 expectancy(기대값)가 비용 후 여유를 남긴다."),
        ("validation_zoom_pocket", val_chunk >= -1500, val_chunk, ">=-1500", "검증 확대 구간의 움푹 파인 포켓이 Stage322 기준 안에 있다."),
        ("oos_zoom_pocket", oos_chunk >= -500, oos_chunk, ">=-500", "표본외 확대 구간의 움푹 파인 포켓이 Stage322 기준 안에 있다."),
        ("validation_negative_month_count", val_negative_months <= 3, val_negative_months, "<=3", "검증 음수 월이 과하게 퍼지지 않는다."),
        ("oos_negative_month_count", oos_negative_months <= 1, oos_negative_months, "<=1", "표본외 음수 월이 제한적이다."),
    ]
    return [
        {
            "check_name": name,
            "status": "passed" if passed else "failed",
            "value": round(check_value, 6),
            "threshold": threshold,
            "effect": effect,
        }
        for name, passed, check_value, threshold, effect in checks
    ]


def build_package_audit(hash_receipt: Mapping[str, Any]) -> list[dict[str, str]]:
    expected = dict(hash_receipt.get("package_hashes", {}))
    rows: list[dict[str, str]] = []
    for path_text, expected_hash in expected.items():
        path = ROOT / path_text
        exists = path_exists(path)
        actual = sha256_file(path) if exists else ""
        passed = exists and actual == expected_hash
        rows.append(
            {
                "path": path_text,
                "status": "passed" if passed else "failed",
                "sha256": actual,
                "expected_sha256": str(expected_hash),
                "effect": "패키지 산출물 해시가 Stage323(323단계) 영수증과 일치한다." if passed else "패키지 산출물 재생성 또는 추적 수리가 필요하다.",
            }
        )
    return rows


def build_feature_handoff_audit(manifest: Mapping[str, Any]) -> list[dict[str, str]]:
    schema = load_json(package_path(manifest, "adapter_schema_path"))
    handoff = load_json(package_path(manifest, "runtime_handoff_path"))
    runtime_features = schema.get("runtime_input_features", [])
    aliases = schema.get("runtime_feature_aliases", {})
    known_differences = " ".join(str(item) for item in handoff.get("known_differences", []))
    metrics = handoff.get("parity_identity", {}).get("mt5_actual_routed_metrics", [])
    tier_b_fallback = sum(as_float(row.get("tier_b_fallback_used_count")) for row in metrics if isinstance(row, Mapping))
    checks = [
        (
            "runtime_feature_order",
            runtime_features == ["run322b_route_signal"],
            "|".join(str(item) for item in runtime_features),
            "run322b_route_signal",
            "ONNX(온엑스) 입력 순서가 MT5 feature CSV(피처 CSV)와 맞는다.",
        ),
        (
            "logical_alias",
            aliases.get("run322b_route_signal") == "route_signal_value",
            aliases.get("run322b_route_signal", ""),
            "route_signal_value",
            "Stage322(322단계) 논리 신호와 MT5 열 이름의 alias(별칭)가 명시됐다.",
        ),
        (
            "known_difference_recorded",
            "run322b_route_signal" in known_differences and "route_signal_value" in known_differences,
            known_differences[:160],
            "both names recorded",
            "feature order parity(피처 순서 동등성) 때 이름 혼동을 줄인다.",
        ),
        (
            "tier_b_fallback_usage",
            tier_b_fallback == 0.0,
            str(tier_b_fallback),
            "0",
            "선택 후보는 Tier A used(티어 A 사용)만으로 재현됐고 fallback(대체)에 숨은 수익을 기대지 않는다.",
        ),
    ]
    return [
        {
            "check_name": name,
            "status": "passed" if passed else "failed",
            "value": actual,
            "expected": expected,
            "effect": effect,
        }
        for name, passed, actual, expected, effect in checks
    ]


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


def stage325_spec_markdown() -> str:
    return f"""# Stage325 Brief(325단계 개요): ONNX Export, Parity, Runtime Reproduction(온엑스 내보내기, 동등성, 런타임 재현)

- stage_id(단계 ID): `{STAGE325_ID}`
- source_stage(원천 단계): `{STAGE324_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`
- Goal Achieve(목표 달성): `not_claimed`
- question(질문): Can this package(패키지) complete ONNX export(온엑스 내보내기), Python inference check(파이썬 추론 확인), feature order parity(피처 순서 동등성), ONNX parity receipt(온엑스 동등성 영수증), and MT5 runtime reproduction(MT5 런타임 재현)?
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): Stage325(325단계)는 패키지 생성을 넘어서 실제 ONNX artifact(온엑스 산출물)와 runtime reproduction receipt(런타임 재현 영수증)를 만든다.

`{BOUNDARY}`
"""


def report_markdown(go_rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, str]], feature_rows: Sequence[Mapping[str, str]]) -> str:
    failed = [row for row in list(go_rows) + list(audit_rows) + list(feature_rows) if row.get("status") != "passed"]
    return "\n".join(
        [
            "# run324A ONNX-Go Pressure Report(324A 온엑스 진행 압박 보고)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`",
            f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`",
            f"- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- failed_checks(실패 검사): `{len(failed)}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "Effect(효과): minimum trade count(최소 거래수), 4-10 trades/day(일 4-10거래), net/PF/DD/recovery/expectancy(순수익/수익 팩터/손실폭/회복/기대값), zoom pocket(확대 포켓), feature handoff(피처 인계), package hash(패키지 해시)를 함께 통과했다.",
            "",
            "Boundary(경계): export(내보내기)를 시작할 수 있다는 뜻이지 runtime authority(런타임 권위)나 Goal Achieve(목표 달성)가 아니다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def write_stage325_inputs() -> None:
    for path in (SPEC325.parent, INPUTS325, REVIEWS325, SELECTED325.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(SPEC325, stage325_spec_markdown())
    write_json(INPUTS325 / "adapter_package_manifest.json", load_json(ADAPTER_MANIFEST_INPUT))
    write_json(INPUTS325 / "adapter_package_hash_receipt.json", load_json(ADAPTER_HASH_INPUT))
    write_csv(INPUTS325 / "onnx_go_pressure_scorecard.csv", GO_COLUMNS, read_csv_dicts(GO_SCORECARD))
    write_json(INPUTS325 / "onnx_go_pressure_receipt.json", load_json(PRESSURE_RECEIPT))
    write_md(
        INPUTS325 / "input_refs.md",
        f"""# Stage325 Input References(325단계 입력 참조)

- adapter_package_manifest(어댑터 패키지 목록): `{rel(INPUTS325 / 'adapter_package_manifest.json')}`
- adapter_package_hash_receipt(어댑터 패키지 해시 영수증): `{rel(INPUTS325 / 'adapter_package_hash_receipt.json')}`
- onnx_go_pressure_scorecard(온엑스 진행 압박 점수표): `{rel(INPUTS325 / 'onnx_go_pressure_scorecard.csv')}`
- onnx_go_pressure_receipt(온엑스 진행 압박 영수증): `{rel(INPUTS325 / 'onnx_go_pressure_receipt.json')}`
- source_report(원천 보고): `{rel(REPORT)}`

Effect(효과): Stage325(325단계)가 같은 Adapter package(어댑터 패키지)를 export/parity/runtime reproduction(내보내기/동등성/런타임 재현)에 쓴다.
""",
    )
    write_md(
        SELECTED325,
        f"""# Stage325 Selection Status(325단계 선택 상태)

- stage_status(단계 상태): `opened_onnx_export_parity_runtime_reproduction_after_stage324_go`
- current_packet(현재 작업 묶음): `325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE324_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUTS325 / 'input_refs.md')}`
""",
    )
    write_md(
        REVIEW_INDEX325,
        f"""# Stage325 Review Index(325단계 검토 색인)

- stage_brief(단계 개요): `{rel(SPEC325)}`
- input_refs(입력 참조): `{rel(INPUTS325 / 'input_refs.md')}`
""",
    )
    write_csv(
        STAGE_LEDGER325,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage325_open",
                "stage_id": STAGE325_ID,
                "run_id": RUN_ID,
                "view": "stage325_open_onnx_export_parity_runtime_reproduction",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_onnx_export_parity_runtime_reproduction_after_stage324_go",
                "judgment": JUDGMENT,
                "evidence_boundary": "onnx_go_approved_no_parity_yet",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_outputs(created_at: str) -> list[Path]:
    manifest = load_json(ADAPTER_MANIFEST_INPUT)
    hash_receipt = load_json(ADAPTER_HASH_INPUT)
    go_rows = build_go_scorecard(manifest)
    audit_rows = build_package_audit(hash_receipt)
    feature_rows = build_feature_handoff_audit(manifest)
    failed = [row for row in list(go_rows) + list(audit_rows) + list(feature_rows) if row.get("status") != "passed"]
    if failed:
        write_csv(GO_SCORECARD, GO_COLUMNS, go_rows)
        write_csv(PACKAGE_AUDIT, AUDIT_COLUMNS, audit_rows)
        write_csv(FEATURE_HANDOFF_AUDIT, FEATURE_AUDIT_COLUMNS, feature_rows)
        raise RuntimeError(f"ONNX-go pressure failed; failed checks: {[row.get('check_name', row.get('path')) for row in failed]}")
    write_csv(GO_SCORECARD, GO_COLUMNS, go_rows)
    write_csv(PACKAGE_AUDIT, AUDIT_COLUMNS, audit_rows)
    write_csv(FEATURE_HANDOFF_AUDIT, FEATURE_AUDIT_COLUMNS, feature_rows)
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
            "feature_handoff_check_count": len(feature_rows),
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
                "evidence_available": f"go_checks={len(go_rows)};package_audits={len(audit_rows)};feature_handoff_checks={len(feature_rows)};adapter_package={ADAPTER_PACKAGE_ID}",
                "evidence_missing": "ONNX export(온엑스 내보내기);Python inference check(파이썬 추론 확인);ONNX parity(온엑스 동등성);MT5 runtime reproduction(MT5 런타임 재현)",
                "judgment_label": JUDGMENT,
                "judgment_class": "onnx_go_approved_no_parity_yet",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "ONNX 내보내기를 시작할 수 있지만 동등성과 런타임 재현은 아직 끝나지 않았다.",
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
                "effect": "Stage323(323단계) 패키지 해시가 현재 파일과 일치한다.",
            },
            {
                "gate_name": "trade_density_scale_efficiency(거래 밀도/규모/효율)",
                "status": "passed",
                "evidence_path": rel(GO_SCORECARD),
                "effect": "최소 거래수, 4-10 trades/day(일 4-10거래), 순수익, PF(수익 팩터), DD(손실폭), 회복, 기대값을 함께 통과했다.",
            },
            {
                "gate_name": "zoom_curve_pressure(확대 곡선 압박)",
                "status": "passed",
                "evidence_path": rel(GO_SCORECARD),
                "effect": "Stage322(322단계) 확대 구간 포켓 기준을 통과한 후보만 export(내보내기)로 넘긴다.",
            },
            {
                "gate_name": "feature_handoff_trace(피처 인계 추적)",
                "status": "passed",
                "evidence_path": rel(FEATURE_HANDOFF_AUDIT),
                "effect": "run322b_route_signal(실행 신호)과 route_signal_value(경로 신호값) alias(별칭)를 확인했다.",
            },
            {
                "gate_name": "parity_not_yet_claimed(동등성 아직 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "Stage325(325단계) 전에는 ONNX parity(온엑스 동등성)나 runtime authority(런타임 권위)를 주장하지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(go_rows, audit_rows, feature_rows))
    write_md(
        DECISION,
        f"""# Decision(결정): Stage324 ONNX-Go Passed and Stage325 Opened(324단계 온엑스 진행 통과와 325단계 개방)

- date(날짜): `{UPDATED_ON}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`
- decision(결정): ONNX export/parity/runtime reproduction(온엑스 내보내기/동등성/런타임 재현) 단계로 넘긴다.
- effect(효과): Goal Achieve(목표 달성)는 아직 아니며, Stage325(325단계)에서 export(내보내기), Python inference check(파이썬 추론 확인), parity receipt(동등성 영수증), MT5 runtime reproduction(MT5 런타임 재현)을 닫아야 한다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage325_inputs()
    artifacts = [
        GO_SCORECARD,
        PACKAGE_AUDIT,
        FEATURE_HANDOFF_AUDIT,
        PRESSURE_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC325,
        INPUTS325 / "adapter_package_manifest.json",
        INPUTS325 / "adapter_package_hash_receipt.json",
        INPUTS325 / "onnx_go_pressure_scorecard.csv",
        INPUTS325 / "onnx_go_pressure_receipt.json",
        INPUTS325 / "input_refs.md",
        SELECTED325,
        STAGE_LEDGER325,
        REVIEW_INDEX325,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE324_ID,
            "target_stage_id": STAGE325_ID,
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
            "source_inputs": [rel(ADAPTER_MANIFEST_INPUT), rel(ADAPTER_HASH_INPUT), rel(PRODUCER)],
            "source_hashes": {
                rel(path): sha256_file(path)
                for path in [ADAPTER_MANIFEST_INPUT, ADAPTER_HASH_INPUT, PRODUCER]
                if path_exists(path)
            },
            "producer": rel(PRODUCER),
            "consumer": f"{STAGE325_ID}:{NEXT_ACTION}",
            "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER324)],
            "availability": "tracked_stage324_pressure_artifacts_required_force_add_under_ignored_02_runs",
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
                "stage_id": STAGE324_ID,
                "lane": "onnx_go_pressure",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"selected_candidate={SELECTED_CANDIDATE};adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE325_ID}.",
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
                "stage_id": STAGE324_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage324_onnx_go_stage325_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "onnx_go_pressure(온엑스 진행 압박)",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "onnx_go_no_parity_yet",
                "scoreboard_lane": "onnx_go_pressure",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"adapter_package={ADAPTER_PACKAGE_ID};onnx_readiness={ONNX_READINESS}",
                "guardrail_kpi": "goal_achieve=not_claimed;runtime_authority=not_claimed",
                "external_verification_status": "not_applicable_pre_export_pressure",
                "notes": f"target_stage={STAGE325_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER324,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage324_closeout",
                "stage_id": STAGE324_ID,
                "run_id": RUN_ID,
                "view": "stage324_onnx_go_stage325_open",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "scoreboard": "onnx_go_pressure_scorecard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "onnx_go_no_parity_yet",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE325_ID}.",
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage324_onnx_go_pressure_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE324_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run324A ONNX-go pressure(324A 온엑스 진행 압박)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED324).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", f"- ONNX readiness(온엑스 준비): `{ONNX_READINESS}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run324A_report", f"- run324A_report(324A 보고): `{rel(REPORT)}`")
    selected = append_once(selected, "stage325_open(325단계 개방)", f"- stage325_open(325단계 개방): `{STAGE325_ID}`")
    write_md(SELECTED324, selected)

    review_index = io_path(REVIEW_INDEX324).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX324) else "# Stage324 Review Index(324단계 검토 색인)\n"
    review_index = append_once(review_index, "run324A_report", f"- run324A_report(324A 보고): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX324, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE325_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE324_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `cp322A_onnx_export_parity_runtime_reproduction`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", f"- adapter_under_review(검토 중 어댑터): `{ADAPTER_PACKAGE_ID}`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_onnx_export_parity_runtime_reproduction_after_stage324_go`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = replace_line_prefix(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{BOUNDARY}`")
    current = append_once(
        current,
        "run324A_summary",
        f"- run324A_summary(324A 요약): `{ADAPTER_PACKAGE_ID}`가 ONNX-go pressure(온엑스 진행 압박)를 통과해 Stage325(325단계)를 열었다. Effect(효과): export(내보내기)를 시작할 수 있지만 ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현), Goal Achieve(목표 달성)는 아직 아니다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE325_ID}")
    focus = (
        f"- >-\n"
        f"  Stage325(325단계) ONNX export/parity/runtime reproduction(온엑스 내보내기/동등성/런타임 재현) opened for Adapter package(어댑터 패키지) `{ADAPTER_PACKAGE_ID}` by `{RUN_ID}`. "
        f"Effect(효과): Stage324(324단계) 압박을 통과했지만 Goal Achieve(목표 달성)는 Stage325(325단계) 산출물 이후에만 판단한다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace, bom=True)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run324A ONNX-go pressure(324A 온엑스 진행 압박)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): `{ADAPTER_PACKAGE_ID}`가 export(내보내기) 전 압박을 통과해 Stage325(325단계)를 열었다.\n- boundary(경계): ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현), Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    for path in (RUN_DIR, REVIEWS324):
        io_path(path).mkdir(parents=True, exist_ok=True)
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
                "target_stage": STAGE325_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
